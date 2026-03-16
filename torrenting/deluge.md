# Deluge — BitTorrent Client

Deluge is a free, open-source, cross-platform BitTorrent client built on the libtorrent library. It uses a daemon/client architecture — separating the download engine from the UI — making it ideal for headless servers, seedboxes, and remote management.

- **Website:** https://deluge-torrent.org
- **Repository:** https://github.com/deluge-torrent/deluge
- **License:** GNU GPL v3
- **Platform:** Linux, Windows, macOS, BSD
- **Version:** 2.2.x (latest stable)

---

## Table of Contents
1. [Why Deluge](#1-why-deluge)
2. [Architecture — Daemon / Client Model](#2-architecture--daemon--client-model)
3. [Installation](#3-installation)
4. [Configuration](#4-configuration)
5. [Interfaces — GTK, Web UI, Console](#5-interfaces--gtk-web-ui-console)
6. [Plugin System](#6-plugin-system)
7. [Remote Management](#7-remote-management)
8. [Docker Deployment](#8-docker-deployment)
9. [Privacy & Security Settings](#9-privacy--security-settings)
10. [Comparison with Other Clients](#10-comparison-with-other-clients)

---

## 1. Why Deluge

**Pros:**
- **Completely ad-free** — no bundled offers, no adware, no monetization in the client
- **Fully open source** — GPL v3, auditable code, no closed components
- **Daemon architecture** — runs headless on a server, control from anywhere
- **Lightweight** — minimal RAM and CPU usage vs. clients like Vuze
- **Highly customizable** — plugin system extends every aspect
- **MSE/PE encryption** — built-in BitTorrent traffic encryption
- **Proxy support** — SOCKS5/HTTP proxy per-client for additional privacy

**Cons:**
- Development has slowed since ~2019 (community maintained)
- No native mobile app (control via web UI on mobile browser)
- Some users report upload inconsistencies — qBittorrent is more actively developed
- GTK UI can feel dated vs. qBittorrent's Qt interface

**Alternatives to consider:**
- **qBittorrent** — more actively developed, similar ad-free open-source philosophy, recommended if you want the most current client
- **Transmission** — extremely lightweight, popular on macOS and NAS devices
- **rtorrent** — headless CLI client, popular for seedboxes

---

## 2. Architecture — Daemon / Client Model

```
deluged (daemon)  ←→  deluge-gtk (GTK desktop UI)
                  ←→  deluge-web (Web UI — browser accessible)
                  ←→  deluge-console (CLI interface)
                  ←→  Remote clients on other machines

The daemon handles all BitTorrent activity:
  - Connecting to peers and trackers
  - Downloading and uploading data
  - DHT, PEX, local peer discovery
  - Piece verification
  - Plugin execution

The UI connects to the daemon via RPC (Remote Procedure Call)
The daemon can run on a remote machine (seedbox, NAS, home server)
The UI connects over the network — same interface whether local or remote
```

This separation means you can:
- Run `deluged` headlessly on a server and manage it from your laptop
- Run the daemon on startup (boot) and access it from any device via web browser
- Use the console UI via SSH for lightweight remote control

---

## 3. Installation

### Linux

```bash
# Ubuntu/Debian (stable)
sudo apt update && sudo apt install deluge deluged deluge-web deluge-console

# Latest via PPA (Ubuntu)
sudo add-apt-repository ppa:deluge-team/stable
sudo apt update && sudo apt install deluge-gtk deluged deluge-web

# Arch Linux
sudo pacman -S deluge

# From PyPI (any Python 3.8+ system)
pip install deluge
```

### Windows

```
Download installer from: https://deluge-torrent.org/download/
  → deluge-2.x.x-win64-setup.exe
Installs: deluged.exe, deluge.exe (GTK), deluge-web.exe, deluge-console.exe
```

### macOS

```bash
brew install deluge
# or download from official site
```

---

## 4. Configuration

### First Launch Setup

```bash
# Start the daemon
deluged

# Launch GTK UI (auto-connects to local daemon)
deluge-gtk

# Or: Web UI
deluge-web
# → Open http://localhost:8112 (default password: deluge)
```

### Key Settings (Preferences)

```
Downloads:
  Download To:        /path/to/downloads
  Move Completed To:  /path/to/completed    ← Separate dir after finish
  Prioritize First/Last Pieces: ✅           ← Enables fast streaming start

Connection:
  Incoming Port:      6881 (or random)       ← Open this in router/firewall
  Max Connections:    200 (global)
  Max per Torrent:    50
  Use Random Port:    ✅ (or fixed for firewall rules)

Bandwidth:
  Max Download:       0 (unlimited)          ← Set to your ISP download speed
  Max Upload:         100 KB/s               ← Leave bandwidth for browsing
  Max Half-Open:      50

Queue:
  Total Active:       5
  Active Downloading: 3
  Active Seeding:     5
  Stop Seed at Ratio: 1.0                    ← Seed back what you took

Network:
  Encryption (Incoming): Enabled
  Encryption (Outgoing): Enabled
  Prefer Encrypted Connections: ✅

Interface:
  Show notification when torrent completes: ✅
```

### Configuring Network Interface (VPN Binding)

To force all Deluge traffic through a VPN interface:

```bash
# Find your VPN interface name
ip link show
# Common names: tun0, wg0, proton0, nordlynx

# In Deluge: Preferences → Network → Interface
# Enter the VPN interface name (e.g., tun0)
# Deluge will only connect through this interface
# → If VPN drops, Deluge stops downloading (no IP leak)
```

---

## 5. Interfaces — GTK, Web UI, Console

### GTK Desktop UI

The primary graphical interface. Columns to display (right-click column headers):
```
Name | Size | Progress | Seeds | Peers | Download Speed | Upload Speed | ETA | Ratio
```

Useful view options:
```
View → Columns → enable: Seeds, Peers, Ratio
View → State Filter → show All / Downloading / Seeding / Paused
```

### Web UI

```bash
# Start daemon + web UI
deluged && deluge-web

# Access at:
http://localhost:8112
# Default password: deluge   (change immediately in Preferences)

# Run on custom port:
deluge-web --port 8080

# Allow remote access (bind to all interfaces):
deluged
deluge-web --base /deluge  # accessible at http://YOUR_IP:8112/deluge

# Enable HTTPS (generate or provide cert):
deluge-web --ssl --cert /path/to/cert.pem --pkey /path/to/key.pem
```

### Console UI

```bash
deluge-console

# Commands:
help                    # List all commands
info                    # List all torrents
info <hash>             # Details for specific torrent
add <magnet/url>        # Add a torrent
add /path/to/file.torrent
pause <hash>            # Pause torrent
resume <hash>           # Resume torrent
rm <hash>               # Remove torrent (add --rm_data to delete files)
config                  # Show configuration
config --show <key>     # Show specific config key
config --set max_download_speed 1024  # Set download limit (KB/s)
quit                    # Exit console
```

---

## 6. Plugin System

Deluge ships with 8 built-in plugins and supports community plugins. Enable via Preferences → Plugins.

### Built-in Plugins

**Scheduler**
```
Set bandwidth limits and active torrent counts by time of day and day of week.
Example: full speed overnight (00:00–08:00), limited during day (08:00–23:00)
Preferences → Plugins → Scheduler → Configure
```

**Label**
```
Organize torrents with colored labels (Movies, TV, Software, etc.)
Auto-labeling rules: automatically apply labels based on tracker or save path
```

**AutoAdd**
```
Watch a folder for new .torrent files — automatically add them to Deluge.
Useful with other automation tools (Prowlarr, RSS fetchers).
Set: Watch Folder = /home/user/torrent-watch
     Save To = /home/user/downloads/auto
```

**Execute**
```
Run a script when a torrent event occurs (finishes, is added, etc.)
Example: run a post-processing script when download completes
Event: Torrent Complete
Command: /home/user/scripts/move_and_notify.sh "%T" "%D"
  %T = torrent name, %D = download directory
```

**Extractor**
```
Automatically extract .rar/.zip archives after download completes.
Useful for scene releases packed in multi-part RARs.
```

**Blocklist**
```
Block IP ranges known to be copyright monitors, anti-piracy firms, etc.
Downloads blocklist files (e.g., I-Blocklist format) automatically.
```

**WebAPI**
```
JSON REST API for programmatic control of Deluge.
Enables integration with automation tools.
```

**Queue**
```
Automatic queue management — active torrent limits with auto-pause/resume.
```

### Community Plugins

```bash
# Install a plugin (as .egg file from community sources)
# In GTK UI: Preferences → Plugins → Install Plugin → select .egg file
# Or place .egg in ~/.config/deluge/plugins/

# Popular community plugins:
# YaRSS2:  RSS feed monitor with filtering rules (auto-download from feeds)
# ltConfig: Advanced libtorrent settings not exposed in main UI
# SimpleExtractor: Better archive extraction than built-in
# TotalTraffic: Track total uploaded/downloaded per torrent
# AutoRemovePlus: Automatically remove torrents based on ratio/seed time
```

---

## 7. Remote Management

### Connecting from Another Machine

```bash
# On server: start daemon with remote connections enabled
deluged

# Edit ~/.config/deluge/auth (add remote user)
# Format: username:password:level (level: 1=read-only, 5=admin, 10=superuser)
echo "remoteuser:mypassword:10" >> ~/.config/deluge/auth

# Edit ~/.config/deluge/core.conf — allow remote connections
# "allow_remote": true

# On client machine (GTK UI):
# Connection Manager → Add → Server IP, Port 58846, username/password

# Forward port 58846 if behind NAT (or use SSH tunnel)
# SSH tunnel method (no port forwarding needed):
ssh -L 58846:localhost:58846 user@server
# Then connect GTK to localhost:58846
```

### Web UI Remote Access

```bash
# Server: run deluge-web bound to all interfaces
deluge-web --host 0.0.0.0 --port 8112

# Access from anywhere: http://SERVER_IP:8112

# Behind a reverse proxy (nginx):
location /deluge/ {
    proxy_pass http://localhost:8112/;
    proxy_set_header X-Deluge-Base "/deluge/";
    add_header X-Frame-Options SAMEORIGIN;
}
```

---

## 8. Docker Deployment

The most popular Deluge Docker image is from LinuxServer.io:

```yaml
# docker-compose.yml
version: "3.8"
services:
  deluge:
    image: lscr.io/linuxserver/deluge:latest
    container_name: deluge
    environment:
      - PUID=1000             # Your user ID (id -u)
      - PGID=1000             # Your group ID (id -g)
      - TZ=Asia/Kolkata       # Your timezone
      - DELUGE_LOGLEVEL=error # Optional: reduce log noise
    volumes:
      - /opt/deluge/config:/config   # Deluge config persistence
      - /media/downloads:/downloads  # Download directory
    ports:
      - 8112:8112             # Web UI
      - 6881:6881             # BitTorrent port (TCP)
      - 6881:6881/udp         # BitTorrent port (UDP) for DHT
    restart: unless-stopped
```

```bash
# Deploy
docker-compose up -d

# Access Web UI at: http://localhost:8112
# Default password: deluge

# View logs
docker logs deluge -f
```

### With VPN (ProtonVPN example)

```yaml
services:
  vpn:
    image: qmcgaw/gluetun:latest
    container_name: vpn
    cap_add: [NET_ADMIN]
    environment:
      - VPN_SERVICE_PROVIDER=protonvpn
      - VPN_TYPE=wireguard
      - WIREGUARD_PRIVATE_KEY=YOUR_KEY
      - SERVER_COUNTRIES=Switzerland
    ports:
      - 8112:8112   # Expose Deluge's port through VPN container

  deluge:
    image: lscr.io/linuxserver/deluge:latest
    network_mode: "service:vpn"   # Route all Deluge traffic through VPN
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Kolkata
    volumes:
      - /opt/deluge/config:/config
      - /media/downloads:/downloads
    depends_on:
      - vpn
```

---

## 9. Privacy & Security Settings

### Encryption

```
Preferences → Network → Encryption:
  Incoming: Enabled
  Outgoing: Enabled
  Level:    Full stream (RC4)

"Enabled" = prefer encrypted connections, allow unencrypted
"Forced"  = only connect to peers that support encryption (may reduce peers)
```

### VPN Kill Switch via Network Binding

```
Preferences → Network:
  Interface: [select your VPN adapter — tun0, wg0, nordlynx, etc.]

Effect: Deluge ONLY uses this interface for all connections.
If VPN drops → Deluge stops → no IP leak via BitTorrent.
```

### SOCKS5 Proxy

```
Preferences → Proxy:
  Peer proxy:     SOCKS5 proxy address/port (e.g., your VPN's SOCKS5 endpoint)
  Tracker proxy:  Same (hides IP from tracker)
  DHT proxy:      Same
  Web seed proxy: Same

Note: SOCKS5 proxy does NOT encrypt traffic on its own.
Use BOTH VPN + proxy for layered privacy.
```

### Private Trackers / Ratio

```
For private tracker torrents:
  - Enable Force Encryption (private trackers often require it)
  - Set seed ratio ≥ 1.0 to maintain account health
  - Do NOT use public trackers alongside private ones for the same torrent
    (leaks info about what you're downloading to non-private parties)
```

---

## 10. Comparison with Other Clients

| Feature | Deluge | qBittorrent | Transmission | rtorrent |
|---------|--------|-------------|-------------|---------|
| **License** | GPL v3 | GPL v2 | MIT | GPL v2 |
| **Ad-free** | ✅ | ✅ | ✅ | ✅ |
| **Platform** | All | All | All (no Win native) | Linux/macOS |
| **Daemon mode** | ✅ Native | ✅ headless | ✅ daemon | ✅ CLI only |
| **Web UI** | ✅ | ✅ | ✅ | via ruTorrent |
| **Plugin system** | ✅ Rich | Limited | Minimal | ✅ (scripts) |
| **Resource usage** | Low | Low | Very low | Very low |
| **Active dev** | Slowed | ✅ Active | ✅ Active | ✅ Active |
| **Mobile app** | ❌ | ❌ | iOS only | via ruTorrent |
| **Sequential DL** | Via plugin | ✅ Built-in | ❌ | ❌ |
| **RSS reader** | Via plugin | ✅ Built-in | ❌ | Via plugin |

**Current recommendation:**
- **Deluge** — excellent choice, especially for server/daemon use with plugins
- **qBittorrent** — recommended if you want the most actively developed client with similar philosophy
- **Transmission** — best for minimal resource usage on NAS / Raspberry Pi
- **rtorrent + ruTorrent** — most powerful for advanced seedbox setups

---

## See Also

- [BitTorrent Technology](bittorrent-technology.md) — Protocol internals, DHT, magnet links
- [Torrent Sites](torrent-sites.md) — TPB, 1337x, YTS, TorrentGalaxy, and site directory
- [VPN & ZTNA](../networking/vpn-and-ztna.md) — VPN configuration for private torrenting
- [Docker Essentials](../devtools/docker-essentials.md) — Docker Compose for containerized Deluge
