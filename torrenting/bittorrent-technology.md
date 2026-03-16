# BitTorrent Technology — Protocol, Magnet Links & P2P Architecture

A deep technical reference for the BitTorrent protocol — how peer-to-peer file transfer works at every layer, from info hashes and piece verification to DHT, magnet links, and tracker communication.

---

## Table of Contents
1. [What BitTorrent Is](#1-what-bittorrent-is)
2. [Torrent Files — .torrent Structure](#2-torrent-files--torrent-structure)
3. [Info Hash — The Torrent's Identity](#3-info-hash--the-torrents-identity)
4. [Magnet Links — Trackerless Discovery](#4-magnet-links--trackerless-discovery)
5. [Trackers — Peer Discovery (Classic)](#5-trackers--peer-discovery-classic)
6. [DHT — Distributed Hash Table](#6-dht--distributed-hash-table)
7. [PEX — Peer Exchange](#7-pex--peer-exchange)
8. [The Swarm — Peers, Seeds, Leechers](#8-the-swarm--peers-seeds-leechers)
9. [Piece Selection & Download Strategy](#9-piece-selection--download-strategy)
10. [Choking, Unchoking & Tit-for-Tat](#10-choking-unchoking--tit-for-tat)
11. [Protocol Encryption (MSE/PE)](#11-protocol-encryption-mseppe)
12. [BitTorrent v2](#12-bittorrent-v2)
13. [Safety & Privacy](#13-safety--privacy)

---

## 1. What BitTorrent Is

BitTorrent is a peer-to-peer (P2P) file transfer protocol designed for distributing large files efficiently across many participants simultaneously. Unlike HTTP downloads where one server serves all clients, BitTorrent breaks files into pieces and has every downloader simultaneously upload pieces to other downloaders.

```
Traditional HTTP download:
  Server → Client A
  Server → Client B
  Server → Client C
  Server handles all load; bandwidth bottleneck at server

BitTorrent swarm:
  Server (seeder) → Client A (piece 1-10)
  Server (seeder) → Client B (piece 11-20)
  Client A (has 1-10) → Client C
  Client B (has 11-20) → Client C
  All peers share bandwidth; load distributed across participants
```

**Key insight:** The more popular a torrent, the faster it downloads — because more people seeding means more bandwidth available. This is the opposite of HTTP where popularity increases server load and slows downloads.

**Invented by:** Bram Cohen, 2001. The protocol specification has been extended many times. The main spec is maintained at https://www.bittorrent.org/beps/bep_0000.html (BEP = BitTorrent Enhancement Proposal).

---

## 2. Torrent Files — .torrent Structure

A `.torrent` file is a small metadata file (typically 10KB–2MB) encoded in **Bencoding** (a simple serialization format). It contains everything needed to start downloading — except the actual data.

### Bencoding

```
Integers:     i42e         → 42
Strings:      4:spam       → "spam" (4-byte string)
Lists:        l4:spam4:eggse → ["spam", "eggs"]
Dicts:        d3:cow3:moo4:spam4:eggse → {"cow":"moo", "spam":"eggs"}
```

### .torrent File Structure

```
d                           ← dictionary start
  8:announce                ← key: tracker URL
  41:http://tracker.example.com/announce

  13:announce-list          ← list of tracker tiers (BEP 12)
  l
    l 41:http://tracker1.example.com/announce e
    l 41:http://tracker2.example.com/announce e
  e

  7:comment                 ← optional: uploader comment
  19:Uploaded by MyGroup

  10:created by             ← client that created the torrent
  13:qBittorrent/4.4

  13:creation date          ← Unix timestamp of creation
  i1700000000e

  4:info                    ← THE CORE — this dict is hashed to get info hash
  d
    4:name                  ← suggested filename / directory name
    12:MyFile.mkv

    12:piece length         ← bytes per piece (typically 256KB–4MB)
    i524288e                ← 512 KB pieces

    6:pieces                ← concatenated SHA-1 hashes of all pieces (20 bytes each)
    [20N bytes]             ← N = number of pieces

    Single file:
      6:length              ← total file size in bytes
      i1073741824e          ← 1 GB

    Multi-file (directory):
      5:files               ← list of file dicts
      l
        d
          6:length i524288000e
          4:path l 12:Subdirectory 8:file.mkv e
        e
      e
  e
e
```

### Parsing a .torrent in Python

```python
import hashlib, bencodepy

# Parse torrent file
with open("file.torrent", "rb") as f:
    torrent = bencodepy.decode(f.read())

info = torrent[b"info"]

# Get info hash (SHA-1 of bencoded info dict)
info_hash = hashlib.sha1(bencodepy.encode(info)).hexdigest()
print(f"Info hash: {info_hash}")

# File details
name = info[b"name"].decode()
piece_length = info[b"piece length"]
pieces_raw = info[b"pieces"]
num_pieces = len(pieces_raw) // 20

print(f"Name: {name}")
print(f"Piece size: {piece_length // 1024} KB")
print(f"Number of pieces: {num_pieces}")

# Single file
if b"length" in info:
    size = info[b"length"]
    print(f"Size: {size / 1024**3:.2f} GB")

# Multi-file
elif b"files" in info:
    for file_dict in info[b"files"]:
        path = "/".join(p.decode() for p in file_dict[b"path"])
        size = file_dict[b"length"]
        print(f"  {path}: {size / 1024**2:.1f} MB")

# Tracker(s)
tracker = torrent.get(b"announce", b"").decode()
print(f"Tracker: {tracker}")
```

---

## 3. Info Hash — The Torrent's Identity

The **info hash** is the cryptographic fingerprint of the `info` dictionary from the .torrent file:

```
SHA-1(bencoded info dict) → 20 bytes → displayed as 40 hex chars
Example: a1b2c3d4e5f6789012345678901234567890abcd
```

This hash is the torrent's universal identifier. It is used:
- As the key in DHT to find peers
- In magnet links to reference the torrent without a file
- To verify you're connecting to the right swarm
- By torrent sites to identify unique torrents

**Two different .torrent files with different tracker lists but identical content will have the same info hash** — because the tracker list is outside the `info` dict.

### BitTorrent v2 Info Hash

BitTorrent v2 (BEP 52) uses SHA-256 instead of SHA-1 for the info hash, and each piece's hash uses a Merkle tree. v2 info hashes are 32 bytes (64 hex chars). Hybrid torrents advertise both v1 and v2 hashes for backward compatibility.

---

## 4. Magnet Links — Trackerless Discovery

A magnet link contains an info hash and optional metadata — everything needed to start downloading without a .torrent file. The client uses DHT and PEX to discover peers using just the hash.

### Magnet Link Format

```
magnet:?xt=urn:btih:INFOHASH&dn=DISPLAYNAME&tr=TRACKER&tr=TRACKER2&xl=SIZE

Parameters:
  xt   (Exact Topic)    Required. urn:btih: = BitTorrent info hash (v1 SHA-1)
                        urn:btmh: = BitTorrent v2 info hash (SHA-256)
  dn   (Display Name)  Filename/directory hint (not verified — can be spoofed)
  tr   (Tracker)       Optional tracker URL for faster peer discovery
                       Can be repeated for multiple trackers
  xl   (Exact Length)  File size in bytes (hint, not verified)
  as   (Acceptable Source) Direct download URL fallback
  xs   (Exact Source)  P2P link source (e.g., eD2K hash)

Example:
magnet:?xt=urn:btih:a1b2c3d4e5f6789012345678901234567890abcd
       &dn=Ubuntu+22.04+Desktop+amd64.iso
       &tr=udp://tracker.opentrackr.org:1337/announce
       &tr=udp://open.tracker.cl:1337/announce
       &xl=1477980160
```

### Magnet Link Resolution Process

```
Client receives magnet link with info hash H

Step 1: Look up H in DHT
  → Client sends FIND_NODE(H) to bootstrap nodes
  → DHT routes to nodes closest to H
  → Those nodes return peers who have advertised H

Step 2: Connect to discovered peers
  → BitTorrent handshake: exchange protocol capabilities
  → Extension protocol (BEP 10): negotiate extensions

Step 3: Request ut_metadata (BEP 9)
  → If peer supports it, request the info dictionary
  → Receive info dict in pieces
  → Verify SHA-1(received_info_dict) == H
  → If verified: proceed with download
  → If mismatch: discard (tampered metadata)

Step 4: Normal download begins
  → Client now has piece hashes to verify data

Timeline: typically 5–30 seconds for magnet resolution
  (vs instant for .torrent file which already has the info dict)
```

---

## 5. Trackers — Peer Discovery (Classic)

A **tracker** is an HTTP or UDP server that maintains a list of peers participating in a torrent. It does not store or transfer file data — only peer IP addresses.

### How Tracker Communication Works

```
Client → Tracker (HTTP GET):
  GET /announce?
    info_hash=<20-byte-binary-encoded>
    &peer_id=-DE1350-xyz...     (random 20-byte client ID)
    &port=51413                  (client's listening port)
    &uploaded=0
    &downloaded=0
    &left=1073741824             (bytes remaining)
    &event=started               (started/stopped/completed)
    &compact=1                   (request compact peer list)
    &numwant=50                  (how many peers to return)

Tracker → Client (Bencoded response):
  d
    8:interval     i1800e         ← re-announce every 30 minutes
    8:min interval i900e          ← minimum re-announce interval
    8:complete     i142e          ← number of seeders
    10:incomplete  i38e           ← number of leechers
    5:peers                       ← compact format: 6 bytes per peer
    [6N bytes]                    ← IPv4:port packed as 4+2 bytes each
  e
```

### UDP Tracker Protocol (BEP 15)

UDP trackers are more efficient than HTTP — less overhead, faster responses, widely used.

```
Connect request:
  [connection_id=0x41727101980][action=0][transaction_id=random]

Connect response:
  [action=0][transaction_id][connection_id] ← use this for subsequent requests

Announce request:
  [connection_id][action=1][transaction_id]
  [info_hash][peer_id][downloaded][left][uploaded]
  [event][ip=0][key][num_want=-1][port]

Announce response:
  [action=1][transaction_id][interval][leechers][seeders]
  [peers: ip:port pairs]
```

### Tracker Types

| Type | Protocol | Notes |
|------|---------|-------|
| HTTP tracker | HTTP/HTTPS | Oldest, most compatible |
| UDP tracker | UDP | Faster, less overhead |
| WebSocket tracker | WebSockets | For WebTorrent (browser-based) |
| DHT | UDP P2P | Trackerless (see §6) |
| Private tracker | HTTP + auth | Require registration, enforce ratio |

### Private Trackers

Private trackers require an account and enforce an upload/download ratio — you must upload at least as much as you download. They typically have:
- Better quality control (no fakes/malware)
- Faster speeds (dedicated seeders)
- Wider catalogs in niche categories
- No public access — invitation only

---

## 6. DHT — Distributed Hash Table

DHT (Distributed Hash Table, BEP 5) eliminates tracker dependency. Peers maintain a distributed database mapping info hashes to peer lists — the database has no central server; it's spread across all participating clients.

BitTorrent uses the **Kademlia** algorithm for DHT.

### Kademlia Overview

```
Each DHT node has a random 160-bit Node ID (same format as info hash)
Distance between two IDs: XOR metric
  distance(A, B) = A XOR B

Kademlia property: nodes close (by XOR) to an info hash
  are responsible for storing peers who have that hash

Routing table (k-buckets):
  For each bit position 0–159, maintain a bucket of up to k=8 closest nodes
  Buckets for far-away distances hold few entries (mostly empty)
  Buckets for nearby distances hold many entries

Lookup algorithm:
  To find peers for info hash H:
    1. Find the 8 DHT nodes in my routing table closest to H
    2. Send FIND_NODE(H) to those 8 nodes in parallel
    3. Each returns their 8 closest nodes to H
    4. Recurse: contact returned nodes closer to H
    5. Terminate when no closer nodes are found
    6. The closest nodes will have the peer list for H
    → Typically reaches correct region in log2(N) hops
```

### DHT Messages (Kademlia/BEP 5)

```python
# All DHT messages are Bencoded UDP datagrams

# PING — check if node is alive
# query: {"t": "aa", "y": "q", "q": "ping", "a": {"id": my_node_id}}
# response: {"t": "aa", "y": "r", "r": {"id": their_node_id}}

# FIND_NODE — find nodes close to target
# query: {"t": "aa", "y": "q", "q": "find_node",
#         "a": {"id": my_id, "target": target_node_id}}
# response: {"t": "aa", "y": "r", "r": {"id": their_id, "nodes": compact_node_list}}

# GET_PEERS — find peers for info hash
# query: {"t": "aa", "y": "q", "q": "get_peers",
#         "a": {"id": my_id, "info_hash": info_hash_bytes}}
# response (has peers):
#   {"t": "aa", "y": "r", "r": {"id": their_id, "token": token, "values": [ip:port]}}
# response (no peers, closer nodes):
#   {"t": "aa", "y": "r", "r": {"id": their_id, "token": token, "nodes": compact_nodes}}

# ANNOUNCE_PEER — tell DHT node "I have this torrent"
# query: {"t": "aa", "y": "q", "q": "announce_peer",
#         "a": {"id": my_id, "info_hash": info_hash, "port": 6881,
#               "token": token_from_get_peers, "implied_port": 0}}
```

### Bootstrap Nodes

DHT requires at least one known node to join the network:

```
router.bittorrent.com:6881  ← Bram Cohen's official bootstrap
router.utorrent.com:6881    ← BitTorrent Inc.
dht.transmissionbt.com:6881 ← Transmission client
```

On first startup, your client contacts these to find nearby nodes and build its routing table.

---

## 7. PEX — Peer Exchange

PEX (Peer Exchange, BEP 11) is an extension where connected peers share lists of other peers they know. It's faster than DHT for discovering peers — if you're connected to 20 peers and each shares 10 peers, you instantly get 200 candidates.

```
PEX Extension handshake:
  Both peers advertise "ut_pex" extension in BEP 10 handshake

PEX message (sent periodically):
  d
    5:added      [compact peer list added since last message]
    7:added.f    [flags per peer: 0x01=prefers encryption, 0x02=seeder]
    7:dropped    [peers no longer connected to]
  e
```

PEX only works between already-connected peers — it speeds up swarm growth but requires an initial peer from DHT or tracker.

---

## 8. The Swarm — Peers, Seeds, Leechers

```
Swarm: all peers participating in a torrent (uploading + downloading)

Seeder:    Has 100% of the file, only uploading
Leecher:   Downloading (has < 100%), also uploading what they have
Peer:      Generic term for any participant

Seed ratio: total uploaded / total downloaded
  Ratio 1.0 = you've given back as much as you took
  Good practice: seed to at least 1.0 before stopping
  Private trackers typically enforce minimum ratios

Pieces vs Blocks:
  Piece:  Unit of data with a SHA-1/SHA-256 hash for verification
          Typical size: 256 KB – 4 MB (power of 2)
  Block:  Sub-unit that pieces are requested in
          Fixed 16 KB per block (across all clients)

Piece count = file_size / piece_length (rounded up)
Total hash data in .torrent = num_pieces × 20 bytes (SHA-1)
```

### Health Indicators

```
Availability (copies): how many complete copies of the torrent exist in the swarm
  availability 1.0 = one complete seeder exists
  availability 0.5 = only half the pieces are available — some pieces missing
  
Seed:leech ratio:
  10 seeds / 1 leecher → excellent (fast download)
  1 seed / 100 leechers → slow (seeder bandwidth shared 100 ways)
  0 seeds, leechers only → dead torrent (may never complete)
```

---

## 9. Piece Selection & Download Strategy

BitTorrent clients use smart algorithms to decide which pieces to request first:

### Rarest First

The default strategy: prioritize downloading pieces that are rarest in the swarm. This ensures rare pieces get spread quickly, preventing scenarios where one piece is unavailable because no peer has it.

```
Each peer broadcasts its "bitfield" (which pieces it has) when connecting.
Client maintains a piece availability count across all connected peers.
Download order: sort pieces ascending by rarity (availability count).

Effect: rare pieces get replicated faster → swarm stays healthy.
```

### End-game Mode

Near the end of a download, a few missing pieces may only be at slow peers. End-game mode: request the same missing pieces from multiple peers simultaneously, accept the first response, cancel the rest. This minimizes the "last piece" waiting time.

### Sequential Download

Override rarest-first to download pieces in order (first to last). Useful when you want to stream the video before it's fully downloaded.

```
Most clients support: "Download in sequential order" option
Deluge: Preferences → ltConfig → piece_out_of_order_max
qBittorrent: Right-click torrent → Download in sequential order
```

---

## 10. Choking, Unchoking & Tit-for-Tat

BitTorrent manages upload bandwidth using a **choking** mechanism — you only upload to a limited number of peers simultaneously to maximize your upload efficiency.

### How It Works

```
Each client:
  unchoked_upload_slots = 4 (typically)
  unchoke algorithm runs every 10 seconds

Algorithm:
  1. Sort all interested peers by their upload rate to you (descending)
     → Reciprocate to peers who give you the most
  2. Unchoke the top N peers (they receive your data)
  3. Choke all others (they receive nothing from you)
  4. Optimistic unchoke (every 30 seconds):
     Randomly unchoke one additional peer regardless of their rate
     → Discovers new peers with good bandwidth
     → Gives new peers a chance to prove themselves
```

```
States:
  choked:     Peer is not sending you data (they've choked you)
  unchoked:   Peer is actively sending you data
  interested: You want data from a peer
  not interested: Peer has no pieces you need

  Peer chokes you → you stop requesting from them
  You choke a peer → you stop uploading to them
```

**Tit-for-tat effect:** clients who upload more receive better download rates in return. Pure leechers (who throttle uploads) get poor speeds. This creates an incentive to participate fully.

---

## 11. Protocol Encryption (MSE/PE)

MSE (Message Stream Encryption) / PE (Protocol Encryption) wraps BitTorrent traffic in an encrypted stream to prevent ISP throttling or blocking.

```
Negotiation:
  Initiator sends encrypted DH key exchange
  Responder replies with its DH key
  Both derive a shared RC4 stream cipher key
  Subsequent traffic is RC4-encrypted (or plaintext with header obfuscation)

Modes:
  plaintext:  No encryption (default for older clients)
  RC4:        Full stream encryption (hides protocol signature)
  header:     Only encrypt the handshake header (limited obfuscation)

Settings in Deluge:
  Preferences → Network → Encryption:
    Incoming: Enabled / Forced
    Outgoing: Enabled / Forced
  "Forced" = only connect to peers supporting encryption
  "Enabled" = prefer encryption, fall back to plain if needed
```

MSE/PE prevents ISP deep packet inspection from identifying BitTorrent traffic. It does **not** hide IP addresses from peers or trackers — for IP privacy, use a VPN.

---

## 12. BitTorrent v2

BEP 52 defines BitTorrent v2 with significant improvements:

```
Changes from v1:
  SHA-256 instead of SHA-1 for piece hashes
    → Collision-resistant (SHA-1 has known weaknesses)

  Merkle tree for file verification
    → Each file has its own root hash
    → Can verify individual files without downloading entire torrent
    → Enables "piece layer" — verify any arbitrary piece subset

  Per-file piece hashes instead of single global sequence
    → Can deduplicate identical files across torrents

  New info hash format: 32 bytes / 64 hex chars

Hybrid torrents (v1 + v2):
  Advertise both SHA-1 (v1) and SHA-256 (v2) hashes
  Backward compatible with v1 clients
  v2 clients can use stronger verification
```

---

## 13. Safety & Privacy

### IP Address Exposure

In a BitTorrent swarm, **your IP address is visible to all peers** — this is fundamental to how the protocol works. Every peer you connect to sees your IP. Copyright monitoring companies ("anti-piracy firms") join popular swarms and log all IPs.

```
Who sees your IP:
  ✓ All peers in the swarm (direct connections)
  ✓ DHT nodes (node ID + IP for routing)
  ✓ Trackers (logged in announce requests)
  ✓ Passive monitors (companies scanning DHT/swarms)
```

### VPN for Torrenting

A VPN replaces your real IP with the VPN server's IP in the swarm:

```
Without VPN:
  Your IP (1.2.3.4) → BitTorrent swarm
  Copyright holder sees 1.2.3.4 → contacts your ISP → DMCA notice

With VPN:
  Your IP (1.2.3.4) → VPN tunnel → VPN server (5.6.7.8) → swarm
  Copyright holder sees 5.6.7.8 → VPN server has many users → no attribution

VPN kill switch: critically important
  If VPN drops, BitTorrent falls back to direct connection → IP exposed
  Kill switch: blocks all internet traffic if VPN disconnects
  Set in VPN client AND in torrent client:
    qBittorrent: Advanced → Network interface → select VPN adapter
    Deluge: Plugin "YaRSS2" or route via VPN interface in OS
```

### Fake .torrent Files & Malware

```
Risks:
  Fake torrents: .torrent file with wrong/tampered data
    → Verification fails piece-by-piece (SHA-1 hash mismatch)
    → Modern clients reject tampered pieces automatically

  Trojanized executables: real video files are safe; .exe/.bat files in torrents are not
    → Only run executables from torrents you completely trust
    → Scan with antivirus before executing

  Malicious .torrent files: .torrent file itself could contain exploits
    → Use reputable torrent sites (see torrent-sites.md)
    → Look for verified/trusted uploaders (skulls/VIP icons on TPB)

  JavaScript malware on torrent sites
    → Always use uBlock Origin on torrent sites
    → Never disable your ad blocker on torrent sites
```

### Public Trackers vs Private Trackers

| Aspect | Public | Private |
|--------|--------|---------|
| Access | Open to all | Invitation or application |
| Content quality | Mixed (fakes exist) | Curated (scene releases) |
| Speed | Variable | Generally faster |
| Uptime | Many torrents go dead | Maintained by community |
| Privacy | Lower (monitored) | Better (less public scanning) |
| Ratio enforcement | None | Required (seed back) |

---

## See Also

- [Torrent Sites](torrent-sites.md) — TPB, 1337x, YTS, TorrentGalaxy, and more
- [Deluge](deluge.md) — BitTorrent client setup and configuration
- [VPN & ZTNA](../networking/vpn-and-ztna.md) — VPN setup for private torrenting
- [OPSEC & Proxies](../security/opsec-and-proxies.md) — Privacy techniques
