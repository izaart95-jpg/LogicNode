# Network Protocols — Comprehensive Reference

This document covers all major network protocols organized by the OSI model and TCP/IP stack. Each entry includes purpose, port (if applicable), and practical context.

---

## Table of Contents
1. [The OSI Model](#1-the-osi-model)
2. [TCP/IP Model Mapping](#2-tcpip-model-mapping)
3. [Layer 1 — Physical](#3-layer-1--physical)
4. [Layer 2 — Data Link](#4-layer-2--data-link)
5. [Layer 3 — Network](#5-layer-3--network)
6. [Layer 4 — Transport](#6-layer-4--transport)
7. [Layer 5 — Session](#7-layer-5--session)
8. [Layer 6 — Presentation](#8-layer-6--presentation)
9. [Layer 7 — Application](#9-layer-7--application)
10. [Security Protocols](#10-security-protocols)
11. [IoT & Embedded Protocols](#11-iot--embedded-protocols)
12. [Tunneling & VPN Protocols](#12-tunneling--vpn-protocols)
13. [Routing Protocols](#13-routing-protocols)
14. [Name Resolution & Discovery](#14-name-resolution--discovery)
15. [Quick Reference Table](#15-quick-reference-table)

---

## 1. The OSI Model

```
┌─────────────────────────────────────────────┐
│  Layer 7 — Application    │ HTTP, FTP, DNS  │
├─────────────────────────────────────────────┤
│  Layer 6 — Presentation   │ SSL/TLS, MIME   │
├─────────────────────────────────────────────┤
│  Layer 5 — Session        │ NetBIOS, RPC    │
├─────────────────────────────────────────────┤
│  Layer 4 — Transport      │ TCP, UDP, QUIC  │
├─────────────────────────────────────────────┤
│  Layer 3 — Network        │ IP, ICMP, ARP   │
├─────────────────────────────────────────────┤
│  Layer 2 — Data Link      │ Ethernet, Wi-Fi │
├─────────────────────────────────────────────┤
│  Layer 1 — Physical       │ Cables, Radio   │
└─────────────────────────────────────────────┘
```

---

## 2. TCP/IP Model Mapping

The TCP/IP model condenses OSI into 4 layers:

| TCP/IP Layer | OSI Layers | Protocols |
|-------------|------------|-----------|
| **Application** | 5, 6, 7 | HTTP, FTP, SMTP, DNS, SSH |
| **Transport** | 4 | TCP, UDP, QUIC, SCTP |
| **Internet** | 3 | IPv4, IPv6, ICMP, IGMP |
| **Network Access** | 1, 2 | Ethernet, Wi-Fi, ARP, PPP |

---

## 3. Layer 1 — Physical

Physical layer defines electrical, optical, and radio specifications.

### Wired Standards
| Standard | Speed | Medium | Use Case |
|----------|-------|--------|----------|
| **Ethernet (IEEE 802.3)** | 10 Mbps – 400 Gbps | Copper / Fiber | LAN |
| **USB** | 1.5 Mbps – 80 Gbps | Copper | Peripheral connectivity |
| **RS-232 (Serial)** | Up to 115.2 Kbps | Copper | Embedded, console access |
| **RS-485** | Up to 10 Mbps | Copper | Industrial automation |
| **Fiber Channel** | 1 – 128 Gbps | Fiber | Storage Area Networks (SAN) |

### Wireless Standards
| Standard | Speed | Range | Use Case |
|----------|-------|-------|----------|
| **Wi-Fi (IEEE 802.11)** | Up to 46 Gbps (Wi-Fi 7) | ~100m | LAN, Internet |
| **Bluetooth** | 1 – 50 Mbps | ~100m | Short-range devices |
| **Zigbee (IEEE 802.15.4)** | 250 Kbps | ~100m | IoT, home automation |
| **LoRa** | 0.3 – 50 Kbps | ~15 km | Long-range IoT |
| **NFC** | 424 Kbps | ~10 cm | Contactless payments |
| **5G NR** | Up to 20 Gbps | ~1 km | Mobile broadband |
| **Satellite (LEO)** | ~100 Mbps | Global | Remote connectivity (Starlink) |

---

## 4. Layer 2 — Data Link

Handles frame delivery between directly connected nodes.

### Ethernet (IEEE 802.3)
- Most common LAN technology
- Uses MAC addresses (48-bit, e.g., `AA:BB:CC:DD:EE:FF`)
- Frame structure: Preamble → Dest MAC → Src MAC → EtherType → Payload → FCS
- Variants: Fast Ethernet (100M), Gigabit (1G), 10G, 25G, 40G, 100G

### Wi-Fi (IEEE 802.11)
- Wireless LAN standard
- Versions: a/b/g/n (Wi-Fi 4) / ac (Wi-Fi 5) / ax (Wi-Fi 6) / be (Wi-Fi 7)
- Security: WEP → WPA → WPA2 → WPA3
- Frequencies: 2.4 GHz, 5 GHz, 6 GHz

### ARP (Address Resolution Protocol)
- Maps IPv4 addresses to MAC addresses
- Operates at Layer 2/3 boundary
- Vulnerable to ARP spoofing/poisoning attacks

```bash
# View ARP cache
arp -a

# Send ARP request
arping 192.168.1.1
```

### PPP (Point-to-Point Protocol)
- Direct link between two nodes
- Used in DSL connections (PPPoE)
- Supports authentication (PAP, CHAP)

### VLAN (IEEE 802.1Q)
- Virtual LAN tagging
- Logically separates broadcast domains on shared physical infrastructure
- VLAN ID: 1–4094

### STP (Spanning Tree Protocol — IEEE 802.1D)
- Prevents broadcast loops in switched networks
- Variants: RSTP (802.1w), MSTP (802.1s)

### LLDP (Link Layer Discovery Protocol)
- Network device discovery
- Advertises device identity, capabilities, and neighbors

---

## 5. Layer 3 — Network

Handles logical addressing and routing between networks.

### IPv4 (Internet Protocol version 4)
- 32-bit addresses (e.g., `192.168.1.1`)
- ~4.3 billion addresses (exhausted)
- Header: 20–60 bytes
- Fragmentation supported

**Private Ranges:**
| Range | CIDR | Use |
|-------|------|-----|
| `10.0.0.0 – 10.255.255.255` | 10.0.0.0/8 | Large networks |
| `172.16.0.0 – 172.31.255.255` | 172.16.0.0/12 | Medium networks |
| `192.168.0.0 – 192.168.255.255` | 192.168.0.0/16 | Home/small networks |

```bash
# View IP configuration
ip addr show
ifconfig

# Trace route to destination
traceroute 8.8.8.8
```

### IPv6 (Internet Protocol version 6)
- 128-bit addresses (e.g., `2001:0db8::1`)
- 340 undecillion addresses
- No NAT needed (every device gets a public address)
- Built-in IPsec support
- No fragmentation by routers (path MTU discovery)
- Neighbor Discovery Protocol (NDP) replaces ARP

**Address Types:**
| Type | Prefix | Purpose |
|------|--------|---------|
| Link-local | `fe80::/10` | Local network only |
| Global Unicast | `2000::/3` | Public addresses |
| Loopback | `::1` | Localhost |
| Multicast | `ff00::/8` | One-to-many |

### ICMP (Internet Control Message Protocol)
- Error reporting and diagnostics
- Used by `ping` and `traceroute`
- Types: Echo Request/Reply, Destination Unreachable, Time Exceeded, Redirect

```bash
# Ping
ping -c 4 google.com

# Traceroute (uses ICMP/UDP)
traceroute google.com
```

### IGMP (Internet Group Management Protocol)
- Manages multicast group membership
- Used by IPTV, video streaming

### NAT (Network Address Translation)
- Translates private IPs to public IPs
- Types: SNAT (source), DNAT (destination), PAT (port-based)
- Enables multiple devices to share one public IP

### IPsec (Internet Protocol Security)
- Encrypts and authenticates IP packets
- Modes: Transport (end-to-end) and Tunnel (gateway-to-gateway)
- Components: AH (Authentication Header), ESP (Encapsulating Security Payload)
- Used in VPN tunnels

---

## 6. Layer 4 — Transport

Handles end-to-end communication, reliability, and flow control.

### TCP (Transmission Control Protocol)
- **Connection-oriented** — 3-way handshake (SYN → SYN-ACK → ACK)
- **Reliable** — guaranteed delivery, ordering, retransmission
- **Flow control** — sliding window
- **Congestion control** — slow start, congestion avoidance
- **Port range:** 0–65535

```
TCP Header (20 bytes minimum):
┌──────────────┬──────────────┐
│ Source Port   │ Dest Port    │
├──────────────┴──────────────┤
│       Sequence Number        │
├──────────────────────────────┤
│    Acknowledgment Number     │
├────────┬─────────┬──────────┤
│Offset  │ Flags   │ Window   │
├────────┴─────────┴──────────┤
│ Checksum  │ Urgent Pointer  │
└──────────────────────────────┘

Flags: SYN, ACK, FIN, RST, PSH, URG
```

**Common TCP Ports:**
| Port | Service |
|------|---------|
| 20, 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |
| 5432 | PostgreSQL |
| 8080 | HTTP Alt |

### UDP (User Datagram Protocol)
- **Connectionless** — no handshake
- **Unreliable** — no guaranteed delivery or ordering
- **Fast** — minimal overhead (8-byte header)
- Used when speed matters more than reliability

```
UDP Header (8 bytes):
┌──────────────┬──────────────┐
│ Source Port   │ Dest Port    │
├──────────────┼──────────────┤
│ Length        │ Checksum     │
└──────────────┴──────────────┘
```

**Common UDP Ports:**
| Port | Service |
|------|---------|
| 53 | DNS |
| 67, 68 | DHCP |
| 69 | TFTP |
| 123 | NTP |
| 161, 162 | SNMP |
| 443 | QUIC/HTTP3 |
| 500 | IKE (IPsec) |
| 514 | Syslog |
| 1194 | OpenVPN |
| 51820 | WireGuard |

### TCP vs UDP Comparison

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best-effort |
| Ordering | Ordered | Unordered |
| Speed | Slower (overhead) | Faster |
| Header Size | 20+ bytes | 8 bytes |
| Use Cases | Web, email, file transfer | DNS, streaming, gaming, VoIP |

### QUIC
- Built by Google, adopted as HTTP/3 transport
- **UDP-based** but provides TCP-like reliability
- Built-in TLS 1.3 encryption
- Multiplexed streams (no head-of-line blocking)
- 0-RTT connection resumption
- Used by: Chrome, YouTube, Cloudflare, Meta

### SCTP (Stream Control Transmission Protocol)
- Combines TCP reliability with UDP speed
- Multi-homing (multiple IP addresses per connection)
- Multi-streaming (parallel data streams)
- Used in telecom (SS7/Diameter signaling)

### DCCP (Datagram Congestion Control Protocol)
- UDP-like but with congestion control
- Used for streaming media

---

## 7. Layer 5 — Session

Manages sessions between applications.

### NetBIOS
- Legacy session management for Windows networking
- Ports: 137 (name service), 138 (datagram), 139 (session)
- Being replaced by DNS + SMB over TCP

### RPC (Remote Procedure Call)
- Allows programs to execute functions on remote systems
- Implementations: Sun RPC, DCE/RPC, gRPC
- **gRPC** (Google): Modern HTTP/2-based RPC framework, Protocol Buffers serialization

### SIP (Session Initiation Protocol)
- Initiates, maintains, and terminates VoIP/video sessions
- Port: 5060 (TCP/UDP), 5061 (TLS)
- Used by: VoIP phones, video conferencing

### RTP (Real-time Transport Protocol)
- Delivers audio/video streams
- Works alongside SIP
- Used by: VoIP, video calls, IPTV

### SOCKS
- Proxy protocol for routing traffic through intermediary
- **SOCKS5**: Supports UDP, authentication, IPv6
- Port: 1080
- Used by: Tor, SSH tunnels, proxy chains

---

## 8. Layer 6 — Presentation

Handles data formatting, encryption, and compression.

### TLS/SSL (Transport Layer Security / Secure Sockets Layer)
- Encrypts data in transit
- **TLS 1.3** is current standard (faster handshake, stronger ciphers)
- SSL is deprecated (SSLv3 broken since POODLE attack)
- Used by: HTTPS, SMTPS, IMAPS, FTPS

```
TLS 1.3 Handshake (1-RTT):
Client → Server: ClientHello + key share
Server → Client: ServerHello + key share + encrypted extensions + certificate + finished
Client → Server: Finished
→ Encrypted application data begins
```

### MIME (Multipurpose Internet Mail Extensions)
- Defines content types for email and HTTP
- Examples: `text/html`, `application/json`, `image/png`

### ASN.1 / BER / DER
- Data serialization for certificates, SNMP, LDAP
- X.509 certificates use DER encoding

---

## 9. Layer 7 — Application

User-facing protocols.

### HTTP (Hypertext Transfer Protocol)
- Foundation of the web
- Port: 80 (HTTP), 443 (HTTPS)
- Methods: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- Versions:
  - HTTP/1.1: Persistent connections, chunked transfer
  - HTTP/2: Multiplexing, header compression, server push
  - HTTP/3: QUIC-based, removes head-of-line blocking

### HTTPS
- HTTP over TLS
- Port: 443
- Verified via X.509 certificates (Let's Encrypt, DigiCert, etc.)

### DNS (Domain Name System)
- Translates domain names to IP addresses
- Port: 53 (TCP/UDP)
- Record types:

| Record | Purpose | Example |
|--------|---------|---------|
| **A** | IPv4 address | `example.com → 93.184.216.34` |
| **AAAA** | IPv6 address | `example.com → 2606:2800:220:1:...` |
| **CNAME** | Alias | `www.example.com → example.com` |
| **MX** | Mail server | `example.com → mail.example.com` |
| **TXT** | Text data | SPF, DKIM, verification |
| **NS** | Name server | `example.com → ns1.example.com` |
| **SOA** | Zone authority | Start of Authority |
| **SRV** | Service locator | `_sip._tcp.example.com` |
| **PTR** | Reverse lookup | IP → domain |
| **CAA** | Certificate authority | Allowed CA for domain |

```bash
# DNS lookups
dig example.com A
dig example.com AAAA
dig example.com MX
nslookup example.com
host example.com
```

**Secure DNS:**
| Protocol | Description |
|----------|-------------|
| **DoH** (DNS over HTTPS) | DNS queries encrypted via HTTPS (port 443) |
| **DoT** (DNS over TLS) | DNS queries encrypted via TLS (port 853) |
| **DNSSEC** | Cryptographic authentication of DNS responses |

### DHCP (Dynamic Host Configuration Protocol)
- Auto-assigns IP addresses, subnet masks, gateways, DNS
- Ports: 67 (server), 68 (client)
- Process: DISCOVER → OFFER → REQUEST → ACKNOWLEDGE (DORA)

### FTP (File Transfer Protocol)
- File transfers between client and server
- Ports: 21 (control), 20 (data)
- Modes: Active, Passive
- **SFTP** (SSH-based) and **FTPS** (TLS-based) are secure alternatives

### SSH (Secure Shell)
- Encrypted remote access and file transfer
- Port: 22
- Features: Remote shell, SFTP, port forwarding, key-based auth
- Replaces: Telnet, rsh, rlogin

```bash
# SSH connection
ssh user@host

# Key-based authentication
ssh-keygen -t ed25519
ssh-copy-id user@host

# Port forwarding
ssh -L 8080:localhost:80 user@host    # Local forward
ssh -R 80:localhost:8080 user@host    # Remote forward
ssh -D 1080 user@host                 # SOCKS proxy
```

### SMTP (Simple Mail Transfer Protocol)
- Sends email between servers
- Port: 25 (unencrypted), 465 (SMTPS), 587 (submission with STARTTLS)
- Used by: Mail servers (Postfix, Sendmail, Exchange)

### POP3 (Post Office Protocol v3)
- Downloads email from server (deletes from server by default)
- Port: 110 (unencrypted), 995 (POP3S)

### IMAP (Internet Message Access Protocol)
- Manages email on server (synced across devices)
- Port: 143 (unencrypted), 993 (IMAPS)

### LDAP (Lightweight Directory Access Protocol)
- Directory service queries (users, groups, computers)
- Port: 389 (unencrypted), 636 (LDAPS)
- Used by: Active Directory, OpenLDAP

### SMB/CIFS (Server Message Block)
- Windows file/printer sharing
- Port: 445 (direct), 139 (over NetBIOS)
- Versions: SMBv1 (deprecated, insecure), SMBv2, SMBv3 (encrypted)

### NFS (Network File System)
- Unix/Linux file sharing
- Port: 2049
- Versions: NFSv3, NFSv4 (Kerberos support)

### SNMP (Simple Network Management Protocol)
- Network device monitoring and management
- Ports: 161 (agent), 162 (trap)
- Versions: v1, v2c (community strings), v3 (authentication + encryption)

```bash
# Query SNMP device
snmpwalk -v2c -c public 192.168.1.1
```

### NTP (Network Time Protocol)
- Synchronizes clocks across networks
- Port: 123 (UDP)
- Stratum levels: 0 (atomic clock) → 15

### Telnet
- Unencrypted remote access (deprecated — use SSH)
- Port: 23
- Still used for network device console access and testing ports

### TFTP (Trivial File Transfer Protocol)
- Simplified file transfer (no authentication)
- Port: 69 (UDP)
- Used for: PXE boot, firmware updates

### Syslog
- System logging protocol
- Port: 514 (UDP), 6514 (TLS)
- Severity levels: Emergency (0) → Debug (7)

### HTTP Websockets
- Full-duplex communication over single TCP connection
- Starts as HTTP upgrade request
- Used by: Real-time apps, chat, live feeds, gaming

### gRPC
- High-performance RPC framework (Google)
- HTTP/2 transport, Protocol Buffers serialization
- Bidirectional streaming
- Used by: Microservices, Kubernetes, cloud APIs

### GraphQL
- Query language for APIs (Facebook/Meta)
- Single endpoint, client specifies exact data needed
- Alternative to REST APIs

### REST (Representational State Transfer)
- Architectural style for web APIs
- Uses HTTP methods (GET, POST, PUT, DELETE)
- Stateless, resource-oriented
- Most common web API pattern

---

## 10. Security Protocols

### TLS 1.3
- Current standard for transport encryption
- Reduced handshake (1-RTT, 0-RTT resumption)
- Forward secrecy mandatory
- Removed: RSA key exchange, CBC ciphers, RC4, SHA-1

### WPA3
- Latest Wi-Fi security standard
- SAE (Simultaneous Authentication of Equals) replaces PSK
- 192-bit security suite for enterprise
- Protected Management Frames mandatory

### Kerberos
- Network authentication protocol
- Ticket-based (TGT + service tickets)
- Used by: Active Directory, SSH (GSSAPI)
- Port: 88

### RADIUS
- Authentication, Authorization, Accounting (AAA)
- Ports: 1812 (auth), 1813 (accounting)
- Used by: Wi-Fi enterprise (WPA2/3-Enterprise), VPN authentication

### OAuth 2.0 / OpenID Connect
- Authorization framework for web applications
- OAuth 2.0: Delegated authorization (access tokens)
- OpenID Connect: Identity layer on top of OAuth (ID tokens)
- Used by: Google, GitHub, Microsoft login

### SAML (Security Assertion Markup Language)
- XML-based SSO (Single Sign-On) framework
- Enterprise identity federation
- Used by: Corporate SSO, Okta, Azure AD

---

## 11. IoT & Embedded Protocols

| Protocol | Transport | Use Case | QoS |
|----------|-----------|----------|-----|
| **MQTT** | TCP (port 1883/8883) | IoT messaging, telemetry | 3 levels |
| **CoAP** | UDP (port 5683/5684) | Constrained devices, REST-like | Confirmable/Non-confirmable |
| **AMQP** | TCP (port 5672/5671) | Enterprise messaging queues | Yes |
| **Zigbee** | IEEE 802.15.4 | Home automation, sensors | Mesh networking |
| **Z-Wave** | Sub-GHz radio | Smart home | Mesh networking |
| **Thread** | IEEE 802.15.4 | IoT mesh (Matter/HomeKit) | IPv6-based |
| **Matter** | Thread/Wi-Fi | Smart home interoperability | Cross-vendor |
| **Modbus** | TCP/Serial (port 502) | Industrial automation (SCADA) | None |
| **OPC UA** | TCP (port 4840) | Industrial IoT | Secure, structured |
| **BLE (Bluetooth Low Energy)** | 2.4 GHz | Wearables, beacons | Low power |
| **LoRaWAN** | Sub-GHz radio | Long-range IoT | Low data rate |
| **LwM2M** | CoAP/UDP | Device management | Lightweight |

### MQTT Deep Dive
```
Publisher → Broker → Subscriber

Topics: home/temperature, device/status
QoS Levels:
  0 = At most once (fire & forget)
  1 = At least once (acknowledged)
  2 = Exactly once (4-step handshake)

Common Brokers: Mosquitto, HiveMQ, EMQX
Port: 1883 (TCP), 8883 (TLS)
```

---

## 12. Tunneling & VPN Protocols

| Protocol | Layer | Port | Encryption | Use Case |
|----------|-------|------|------------|----------|
| **WireGuard** | 3 | 51820/UDP | ChaCha20 | Modern VPN |
| **OpenVPN** | 3 | 1194/UDP or TCP | OpenSSL | Traditional VPN |
| **IPsec (IKEv2)** | 3 | 500, 4500/UDP | AES, ChaCha20 | Enterprise VPN |
| **L2TP** | 2 | 1701/UDP | None (paired with IPsec) | Legacy VPN |
| **PPTP** | 2 | 1723/TCP | MPPE (broken) | Deprecated |
| **GRE** | 3 | Protocol 47 | None | Tunnel encapsulation |
| **VXLAN** | 2 | 4789/UDP | None | Data center overlay |
| **Tor** | 7 | 9050/SOCKS | Onion routing | Anonymity |
| **SSH Tunnel** | 7 | 22/TCP | SSH encryption | Ad-hoc tunneling |

### WireGuard vs OpenVPN vs IPsec

| Feature | WireGuard | OpenVPN | IPsec/IKEv2 |
|---------|-----------|---------|-------------|
| Codebase | ~4,000 lines | ~100,000 lines | Complex |
| Speed | Fastest | Moderate | Fast |
| Crypto | ChaCha20, Curve25519 | OpenSSL (configurable) | AES, ChaCha20 |
| Roaming | Excellent | Poor | Good (MOBIKE) |
| Auditing | Easy (small code) | Hard | Hard |
| NAT Traversal | Built-in | Via config | NAT-T (port 4500) |

---

## 13. Routing Protocols

### Interior Gateway Protocols (IGP)

| Protocol | Type | Use Case | Metric |
|----------|------|----------|--------|
| **OSPF** | Link-state | Enterprise LAN/WAN | Cost (bandwidth) |
| **IS-IS** | Link-state | ISP backbone | Cost |
| **EIGRP** | Hybrid (Cisco) | Cisco networks | Composite (bandwidth, delay, load) |
| **RIP** | Distance-vector | Small networks | Hop count (max 15) |

### Exterior Gateway Protocols (EGP)

| Protocol | Use Case | Description |
|----------|----------|-------------|
| **BGP** | Internet backbone | Routes between autonomous systems (AS). The protocol that holds the internet together. |

```bash
# View routing table
ip route show
route -n
netstat -rn

# BGP looking glass
# https://www.bgp.he.net/
```

---

## 14. Name Resolution & Discovery

| Protocol | Purpose | Port |
|----------|---------|------|
| **DNS** | Domain → IP | 53 |
| **mDNS** | Local network discovery (.local) | 5353/UDP |
| **LLMNR** | Windows local name resolution | 5355/UDP |
| **NBNS (NetBIOS)** | Legacy Windows name resolution | 137/UDP |
| **SSDP (UPnP)** | Device discovery | 1900/UDP |
| **Bonjour** | Apple service discovery (mDNS + DNS-SD) | 5353/UDP |
| **DHCP** | Auto IP assignment | 67, 68/UDP |
| **DHCPv6** | Auto IPv6 assignment | 546, 547/UDP |
| **NDP** | IPv6 neighbor discovery | ICMPv6 |

---

## 15. Quick Reference Table

### Most Important Protocols by Category

| Category | Protocols |
|----------|-----------|
| **Web** | HTTP, HTTPS, HTTP/2, HTTP/3 (QUIC), WebSockets, REST, GraphQL, gRPC |
| **Email** | SMTP, POP3, IMAP |
| **File Transfer** | FTP, SFTP, TFTP, SMB/CIFS, NFS |
| **Remote Access** | SSH, Telnet, RDP |
| **DNS** | DNS, DoH, DoT, DNSSEC, mDNS |
| **Network Config** | DHCP, DHCPv6, ARP, NDP, NTP |
| **Transport** | TCP, UDP, QUIC, SCTP |
| **Network Layer** | IPv4, IPv6, ICMP, IGMP, IPsec |
| **Routing** | BGP, OSPF, IS-IS, EIGRP, RIP |
| **VPN/Tunneling** | WireGuard, OpenVPN, IPsec/IKEv2, L2TP, GRE, VXLAN, Tor |
| **Security/Auth** | TLS, WPA3, Kerberos, RADIUS, OAuth 2.0, SAML |
| **IoT** | MQTT, CoAP, Zigbee, Z-Wave, Thread, Matter, BLE, Modbus |
| **Monitoring** | SNMP, Syslog, NetFlow, IPFIX |
| **Wireless** | Wi-Fi (802.11), Bluetooth, NFC, LoRa, 5G NR |
| **Directory** | LDAP, Active Directory (Kerberos + LDAP) |
| **Streaming** | RTP, RTSP, RTMP, HLS, DASH, SIP |

### Port Quick Reference

```
20-21   FTP            80     HTTP           443    HTTPS/QUIC
22      SSH            110    POP3           445    SMB
23      Telnet         123    NTP            514    Syslog
25      SMTP           143    IMAP           993    IMAPS
53      DNS            161    SNMP           995    POP3S
67-68   DHCP           389    LDAP           1194   OpenVPN
69      TFTP           443    HTTPS          1883   MQTT
88      Kerberos       465    SMTPS          3306   MySQL
                       587    SMTP Sub       3389   RDP
                       636    LDAPS          5432   PostgreSQL
                       853    DoT            5900   VNC
                                             8080   HTTP Alt
                                             8883   MQTT TLS
                                             51820  WireGuard
```

---

## See Also

- [SSH Tunneling](../networking/ssh-tunneling.md)
- [VPN & ZTNA](../networking/vpn-and-ztna.md)
- [Penetration Testing Tools](../security/penetration-testing-tools.md)
- [OSINT Platforms](../security/osint-platforms.md)
