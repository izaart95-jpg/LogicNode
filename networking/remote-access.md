# Remote Access, Display Protocols & Remote Desktop Tools

This document covers display server protocols (X11, VNC, SPICE, RDP), remote desktop software, SSH fundamentals, and related tools like Win-KeX and VcXsrv.

---

## Table of Contents
1. [Display Protocol Concepts](#1-display-protocol-concepts)
2. [X Window System (X11/Xorg)](#2-x-window-system-x11xorg)
3. [VNC (Virtual Network Computing)](#3-vnc-virtual-network-computing)
4. [RDP (Remote Desktop Protocol)](#4-rdp-remote-desktop-protocol)
5. [SPICE (Simple Protocol for Independent Computing Environments)](#5-spice)
6. [SSH (Secure Shell)](#6-ssh-secure-shell)
7. [X Servers for Windows — VcXsrv & Kali Win-KeX](#7-x-servers-for-windows--vcxsrv--kali-win-kex)
8. [Remote Desktop Tools](#8-remote-desktop-tools)
9. [Web-Based Remote Access](#9-web-based-remote-access)
10. [Linux Remote Display Servers](#10-linux-remote-display-servers)
11. [Comparison Tables](#11-comparison-tables)

---

## 1. Display Protocol Concepts

A **display protocol** transmits graphical output from a server/application to a client screen. Understanding the differences is critical for remote access, virtualization, and headless server management.

```
┌──────────────┐    Display Protocol    ┌──────────────┐
│  Application │ ──────────────────────▶ │    Screen    │
│  (runs here) │   X11 / VNC / RDP /    │ (viewed here)│
│              │   SPICE / Wayland      │              │
│   SERVER     │ ◀────────────────────── │   CLIENT     │
│              │   Input (keyboard,      │              │
│              │   mouse)               │              │
└──────────────┘                        └──────────────┘
```

**Key distinction:**
- **X11** — The application (X client) sends draw commands; the display (X server) renders them. The "server" is where the screen is.
- **VNC** — Sends raw framebuffer (pixel data) over the network. Like a screenshot stream.
- **RDP** — Sends high-level drawing commands + compression. More efficient than VNC.
- **SPICE** — Optimized for VMs. Sends drawing commands + video streams + USB/audio redirection.

---

## 2. X Window System (X11/Xorg)

### What is X11?

**X11** (X Window System, version 11) is the standard display protocol for Linux/Unix graphical environments since 1987. It uses a **client-server architecture** where:

- **X Server** = the machine with the display (your screen)
- **X Client** = the application generating graphics (can be remote)

> This naming is counterintuitive: the "server" is your local screen, and the "client" is the remote application.

```
┌───────────────────────────┐          ┌───────────────────────────┐
│  Remote Machine           │          │  Your Machine             │
│                           │          │                           │
│  X Client (Firefox,       │──X11───▶│  X Server (Xorg, XWayland,│
│  Terminal, GIMP)          │ protocol │  VcXsrv, XQuartz)         │
│                           │          │  → Renders on your screen │
└───────────────────────────┘          └───────────────────────────┘
```

### X11 Forwarding over SSH

```bash
# Forward remote GUI apps to your local X server
ssh -X user@remote-server
firefox &   # Opens Firefox window on YOUR screen

# Trusted forwarding (faster, less secure)
ssh -Y user@remote-server
```

### Xorg vs Wayland

| Feature | Xorg (X11) | Wayland |
|---------|-----------|---------|
| **Age** | 1984/1987 | 2008+ |
| **Architecture** | Client-server, network-transparent | Compositor-based, local |
| **Network Support** | Native (X11 forwarding) | No native network transparency |
| **Security** | Weak (any X client can snoop others) | Strong (isolated clients) |
| **Performance** | More overhead | Lower latency |
| **Compatibility** | Everything works | Some legacy apps need XWayland |
| **Status** | Mature, stable | Default on Fedora, Ubuntu 22.04+ |

### DISPLAY Environment Variable

```bash
# X11 uses $DISPLAY to know where to render
echo $DISPLAY
# :0        = local display 0
# :1        = local display 1 (e.g., VNC)
# host:0    = remote X server

# Set display manually
export DISPLAY=:0
export DISPLAY=192.168.1.100:0
```

---

## 3. VNC (Virtual Network Computing)

### What is VNC?

**VNC** sends the raw **framebuffer** (pixel data) of a desktop over the network. It's simple, universal, and platform-independent.

- **Protocol:** RFB (Remote Framebuffer)
- **Port:** 5900 + display number (e.g., `:1` = port 5901)
- **Encryption:** None by default (tunnel through SSH!)
- **Performance:** Lower than RDP/SPICE (sends pixels, not drawing commands)

### How VNC Works

```
┌──────────────┐                    ┌──────────────┐
│  VNC Server  │ ──framebuffer───▶  │  VNC Client  │
│  (remote)    │   (pixel data)     │  (your PC)   │
│              │ ◀──input events──  │              │
│  Captures    │   (mouse, keys)    │  Displays    │
│  screen      │                    │  screen      │
└──────────────┘                    └──────────────┘
```

### VNC Implementations

| Software | Platform | Notes |
|----------|----------|-------|
| **TigerVNC** | Linux/Windows/macOS | Most common on Linux, good performance |
| **TightVNC** | Windows/Linux | Efficient compression |
| **RealVNC** | All | Commercial + free edition |
| **TurboVNC** | Linux | Optimized for 3D/high-bandwidth |
| **UltraVNC** | Windows | Windows-focused, file transfer |
| **x11vnc** | Linux | Shares existing X11 display (no virtual desktop) |

### Basic VNC Usage

```bash
# --- Server Side (Linux) ---

# Install TigerVNC
sudo apt install tigervnc-standalone-server    # Debian/Ubuntu
sudo dnf install tigervnc-server               # Fedora

# Set VNC password
vncpasswd

# Start VNC server (creates virtual display :1)
vncserver :1 -geometry 1920x1080 -depth 24

# Stop VNC server
vncserver -kill :1

# --- Client Side ---
# Connect with any VNC viewer to: server_ip:5901

# --- ALWAYS tunnel VNC through SSH ---
ssh -L 5901:localhost:5901 user@remote-server
# Then connect VNC client to localhost:5901
```

---

## 4. RDP (Remote Desktop Protocol)

### What is RDP?

**RDP** is Microsoft's proprietary remote desktop protocol. Unlike VNC, it sends **high-level drawing commands** rather than raw pixels, making it significantly more efficient.

- **Developer:** Microsoft
- **Port:** 3389 (TCP/UDP)
- **Encryption:** TLS by default
- **Performance:** Much better than VNC (adaptive compression, bitmap caching)
- **Features:** Multi-monitor, audio redirection, clipboard sync, drive mapping, printer sharing

### RDP Clients

| Client | Platform | Notes |
|--------|----------|-------|
| **mstsc.exe** | Windows | Built-in Windows Remote Desktop |
| **Remmina** | Linux | Full-featured, supports RDP/VNC/SSH |
| **FreeRDP** | Linux/macOS | Open-source command-line + library |
| **Microsoft Remote Desktop** | macOS/iOS/Android | Official Microsoft client |
| **Guacamole** | Web browser | Clientless web-based RDP (see §9) |

### RDP Usage

```bash
# Linux — Connect with FreeRDP
xfreerdp /v:192.168.1.100 /u:username /p:password /size:1920x1080

# Linux — Connect with Remmina (GUI)
sudo apt install remmina remmina-plugin-rdp

# Windows — Built-in
mstsc /v:192.168.1.100
```

### RDP vs VNC

| Feature | RDP | VNC |
|---------|-----|-----|
| **Efficiency** | High (drawing commands) | Low (pixel data) |
| **Bandwidth** | Low | High |
| **Multi-monitor** | ✅ | Limited |
| **Audio** | ✅ Built-in | ❌ Separate |
| **File Transfer** | ✅ Drive mapping | ❌ (most impls) |
| **Encryption** | ✅ TLS | ❌ (use SSH tunnel) |
| **Platform** | Windows-native | Universal |
| **Session Type** | New session or take over | Shares existing screen |

---

## 5. SPICE

### What is SPICE?

**SPICE** (Simple Protocol for Independent Computing Environments) is a remote display protocol **optimized for virtual machines**, developed by Red Hat.

- **Developer:** Red Hat
- **Port:** 5900 (default)
- **Encryption:** TLS support
- **Best for:** KVM/QEMU virtual machines
- **Features:** USB redirection, audio, clipboard, multi-monitor, video streaming, dynamic resolution

### SPICE vs VNC vs RDP

| Feature | SPICE | VNC | RDP |
|---------|-------|-----|-----|
| **Designed for** | VMs | General remote | Windows |
| **USB Passthrough** | ✅ | ❌ | ✅ (limited) |
| **Video Optimization** | ✅ | ❌ | ✅ |
| **Audio** | ✅ | ❌ | ✅ |
| **Clipboard** | ✅ | Basic | ✅ |
| **Dynamic Resolution** | ✅ | ❌ | ✅ |
| **Performance** | Excellent (VMs) | Moderate | Good |

### SPICE Usage

```bash
# QEMU VM with SPICE display
qemu-system-x86_64 \
  -spice port=5900,disable-ticketing=on \
  -device virtio-serial \
  -chardev spicevmc,id=vdagent,debug=0,name=vdagent \
  -device virtserialport,chardev=vdagent,name=com.redhat.spice.0 \
  -hda disk.qcow2

# Connect with SPICE client
remote-viewer spice://localhost:5900

# Install virt-viewer (includes remote-viewer)
sudo apt install virt-viewer
```

---

## 6. SSH (Secure Shell)

### What is SSH?

**SSH** is an encrypted protocol for secure remote access, file transfer, and tunneling. It replaced insecure protocols like Telnet, rsh, and rlogin.

- **Port:** 22 (TCP)
- **Encryption:** AES, ChaCha20
- **Authentication:** Password, public key, certificates
- **Standard:** RFC 4253

### Basic SSH Usage

```bash
# Connect to remote server
ssh user@hostname
ssh user@192.168.1.100
ssh -p 2222 user@hostname       # Non-standard port

# First connection — verify fingerprint
# The authenticity of host 'hostname' can't be established.
# ED25519 key fingerprint is SHA256:abc123...
# Type 'yes' to accept
```

### SSH Key Authentication

```bash
# Generate key pair (Ed25519 recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"
# Keys saved to: ~/.ssh/id_ed25519 (private) and ~/.ssh/id_ed25519.pub (public)

# Copy public key to remote server
ssh-copy-id user@remote-server
# Or manually:
cat ~/.ssh/id_ed25519.pub | ssh user@remote-server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Now login without password
ssh user@remote-server
```

### SSH Config File

```bash
# ~/.ssh/config — saves typing
Host myserver
    HostName 192.168.1.100
    User admin
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

Host devbox
    HostName dev.example.com
    User developer
    ForwardAgent yes

# Now just type:
ssh myserver
ssh devbox
```

### SCP & SFTP (File Transfer)

```bash
# Copy file to remote
scp file.txt user@remote:/home/user/

# Copy file from remote
scp user@remote:/var/log/syslog ./

# Copy directory recursively
scp -r ./project user@remote:/home/user/

# SFTP interactive session
sftp user@remote
sftp> put localfile.txt
sftp> get remotefile.txt
sftp> ls
sftp> exit
```

### SSH Port Forwarding

```bash
# Local forwarding — access remote service on local port
ssh -L 8080:localhost:80 user@remote
# Now localhost:8080 → remote's localhost:80

# Remote forwarding — expose local service to remote
ssh -R 9090:localhost:3000 user@remote
# Now remote:9090 → your localhost:3000

# Dynamic SOCKS proxy
ssh -D 1080 user@remote
# Configure browser to use SOCKS5 proxy at localhost:1080

# X11 forwarding
ssh -X user@remote    # Run GUI apps remotely
```

### SSH Hardening

```bash
# /etc/ssh/sshd_config — recommended settings
PermitRootLogin no
PasswordAuthentication no          # Key-only
PubkeyAuthentication yes
MaxAuthTries 3
Port 2222                          # Non-standard port
AllowUsers admin developer
Protocol 2

# Restart sshd
sudo systemctl restart sshd
```

### Essential SSH Commands

```bash
ssh user@host                      # Connect
ssh -p PORT user@host              # Custom port
ssh -i keyfile user@host           # Specific key
ssh -L local:remote:port user@host # Local forward
ssh -R remote:local:port user@host # Remote forward
ssh -D 1080 user@host              # SOCKS proxy
ssh -X user@host                   # X11 forwarding
ssh -N -f user@host                # Background tunnel (no shell)
ssh-keygen -t ed25519              # Generate keys
ssh-copy-id user@host              # Install public key
scp file user@host:/path           # Copy file
sftp user@host                     # File transfer session
```

---

## 7. X Servers for Windows — VcXsrv & Kali Win-KeX

### VcXsrv

**VcXsrv** is a free, open-source X server for Windows. It allows Linux GUI applications (running in WSL, SSH, or remote systems) to display windows on your Windows desktop.

- **Website:** https://sourceforge.net/projects/vcxsrv/
- **License:** MIT
- **Use case:** Run Linux GUI apps from WSL or remote servers on Windows

```powershell
# 1. Install VcXsrv (download from website or winget)
winget install VcXsrv

# 2. Launch XLaunch (VcXsrv configuration wizard)
#    - Display number: 0
#    - "Multiple windows" (recommended)
#    - "Start no client"
#    - CHECK "Disable access control" (for WSL)

# 3. In WSL:
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
# Or for WSL2:
export DISPLAY=:0   # If using WSLg

# 4. Run GUI apps
sudo apt install x11-apps
xclock &
xeyes &
firefox &
```

### Kali Win-KeX

**Win-KeX** (Windows + Kali Desktop EXperience) provides a full Kali Linux desktop experience inside WSL2 with seamless integration.

- **Developed by:** Kali Linux / Offensive Security
- **Requires:** Kali Linux on WSL2

**Three Modes:**

| Mode | Description | Command |
|------|-------------|---------|
| **Window** | Full Kali desktop in a VNC window | `kex --win` |
| **Seamless** | Kali apps appear as native Windows windows | `kex --sl` |
| **Enhanced** | RDP-based (best performance) | `kex --esm` |

```bash
# Install Kali on WSL2
wsl --install -d kali-linux

# Inside Kali WSL:
sudo apt update && sudo apt install kali-win-kex -y

# Launch modes:
kex --win         # Windowed mode (VNC-based)
kex --sl          # Seamless mode (apps float on Windows desktop)
kex --esm         # Enhanced session mode (RDP-based)

# Stop
kex --stop
```

**How Win-KeX works:**
- **Window mode:** Starts TigerVNC server in Kali → VcXsrv-like viewer on Windows
- **Seamless mode:** Uses VcXsrv X server → individual Kali app windows appear on Windows
- **Enhanced mode:** Uses Windows RDP client → connects to xrdp in Kali WSL

---

## 8. Remote Desktop Tools

### 8.1 Parsec
- **Website:** https://parsec.app
- **What it is:** Ultra-low latency remote desktop, originally designed for cloud gaming
- **Pricing:** Free (personal), Teams ($8/user/mo)
- **Platform:** Windows, macOS, Linux, Android, Raspberry Pi
- **Protocol:** Proprietary (hardware-accelerated H.265/H.264)

**Key Features:**
- Sub-10ms latency (suitable for gaming)
- Hardware encoding/decoding (NVIDIA, AMD, Intel)
- 4K 60fps support
- Controller passthrough
- Multi-monitor
- Peer-to-peer connection

**Best for:** Remote gaming, low-latency desktop access, creative work (video editing remotely)

---

### 8.2 AnyDesk
- **Website:** https://anydesk.com
- **What it is:** Cross-platform remote desktop with proprietary DeskRT codec
- **Pricing:** Free (personal), paid for commercial
- **Platform:** Windows, macOS, Linux, Android, iOS, ChromeOS, FreeBSD

**Key Features:**
- Proprietary DeskRT video codec (low bandwidth)
- File transfer
- Unattended access
- Address book
- Session recording
- Works behind firewalls/NAT
- No router config needed

```bash
# Install on Linux
curl -fsSL https://keys.anydesk.com/repos/DEB-GPG-KEY | sudo gpg --dearmor -o /etc/apt/keyrings/anydesk.gpg
echo "deb [signed-by=/etc/apt/keyrings/anydesk.gpg] http://deb.anydesk.com/ all main" | sudo tee /etc/apt/sources.list.d/anydesk.list
sudo apt update && sudo apt install anydesk
```

**Best for:** Quick support sessions, cross-platform access, works well on slow connections

---

### 8.3 Sunshine + Moonlight
- **Sunshine:** https://github.com/LizardByte/Sunshine (open-source game streaming host)
- **Moonlight:** https://moonlight-stream.org (open-source client)
- **What it is:** Open-source alternative to NVIDIA GameStream — low-latency game/desktop streaming

**How it works:**
```
┌──────────────┐    H.264/H.265/AV1    ┌──────────────┐
│   Sunshine   │ ──────────────────────▶│   Moonlight  │
│   (Host PC)  │   hardware-encoded     │  (Client)    │
│  Windows/    │   stream               │  Any device  │
│  Linux/macOS │ ◀──────────────────────│              │
│              │   input (gamepad,      │              │
│              │   mouse, keyboard)     │              │
└──────────────┘                        └──────────────┘
```

**Sunshine (Server):**
```bash
# Install on Linux
sudo apt install sunshine
# Or Flatpak:
flatpak install dev.lizardbyte.sunshine

# Access web UI to configure: https://localhost:47990
```

**Moonlight (Client):**
- Available on: Windows, macOS, Linux, Android, iOS, ChromeOS, PS Vita, Nintendo Switch, Raspberry Pi

**Key Features:**
- 4K 120fps HDR support
- Hardware encoding (NVIDIA NVENC, AMD AMF, Intel QSV)
- Sub-frame latency
- Controller passthrough
- Open source (both ends)

**Best for:** Remote gaming, highest quality streaming, open-source alternative to Parsec

---

### 8.4 RustDesk
- **Website:** https://rustdesk.com
- **Repository:** https://github.com/rustdesk/rustdesk
- **What it is:** Open-source remote desktop — self-hostable alternative to TeamViewer/AnyDesk
- **License:** AGPL-3.0
- **Platform:** Windows, macOS, Linux, Android, iOS, Web

**Key Features:**
- Fully open-source
- Self-host your own relay server (full control, no third party)
- End-to-end encryption
- File transfer
- TCP tunneling
- Unattended access
- Works behind NAT/firewall

```bash
# Install client
# Download from https://rustdesk.com or:
wget https://github.com/rustdesk/rustdesk/releases/latest/download/rustdesk-x86_64.deb
sudo dpkg -i rustdesk-x86_64.deb

# Self-host relay server (Docker)
docker run --name rustdesk-server \
  -p 21115:21115 -p 21116:21116 -p 21116:21116/udp \
  -p 21117:21117 -p 21118:21118 -p 21119:21119 \
  -d rustdesk/rustdesk-server
```

**Best for:** Privacy-conscious users, self-hosting, TeamViewer/AnyDesk replacement

---

### 8.5 NoMachine
- **Website:** https://www.nomachine.com
- **What it is:** High-performance remote desktop using NX protocol
- **Pricing:** Free (personal, up to 10 connections), Enterprise (paid)
- **Platform:** Windows, macOS, Linux, Android, iOS

**Key Features:**
- NX protocol (very efficient, better than VNC)
- Hardware-accelerated encoding
- Audio + USB + printing
- Multi-display
- File transfer
- Works on slow connections

```bash
# Install on Linux
wget https://download.nomachine.com/download/8.x/Linux/nomachine_x.x.x_amd64.deb
sudo dpkg -i nomachine_*.deb
```

**Best for:** Linux remote desktop (superior to VNC), works well on poor connections

---

## 9. Web-Based Remote Access

### 9.1 Apache Guacamole
- **Website:** https://guacamole.apache.org
- **What it is:** Clientless remote desktop gateway — access RDP, VNC, SSH through a **web browser**
- **License:** Apache 2.0
- **Protocol Support:** RDP, VNC, SSH, Telnet, Kubernetes

**How it works:**
```
┌──────────┐     HTML5      ┌───────────────┐     RDP/VNC/SSH    ┌──────────┐
│  Browser  │ ─────────────▶│   Guacamole   │ ──────────────────▶│  Target  │
│  (Client) │   WebSocket   │   Server      │   native protocol  │  Machine │
└──────────┘               └───────────────┘                    └──────────┘
```

```bash
# Docker deployment
docker run --name guacamole -d \
  -p 8080:8080 \
  guacamole/guacd

# Access at http://localhost:8080/guacamole
# Default login: guacadmin / guacadmin
```

**Key Features:**
- No client software needed (just a browser)
- Multi-protocol (RDP + VNC + SSH in one interface)
- User management and MFA
- Session recording
- LDAP/Active Directory integration
- Clipboard and file transfer

**Best for:** Enterprise remote access portals, zero-install access, managing many machines via web

---

### 9.2 noVNC
- **Website:** https://novnc.com
- **Repository:** https://github.com/novnc/noVNC
- **What it is:** VNC client running entirely in a web browser (HTML5 + WebSocket)
- **License:** MPL 2.0

```bash
# Quick launch — proxy to existing VNC server
git clone https://github.com/novnc/noVNC.git
cd noVNC
./utils/novnc_proxy --vnc localhost:5901

# Access in browser: http://localhost:6080/vnc.html

# Or with websockify standalone
pip install websockify
websockify --web /path/to/noVNC 6080 localhost:5901
```

**Best for:** Quick browser-based VNC access, embedding VNC in web apps, Docker containers

---

## 10. Linux Remote Display Servers

### 10.1 xrdp
- **Website:** https://www.xrdp.org
- **What it is:** Open-source RDP server for Linux — lets Windows Remote Desktop clients connect to Linux
- **License:** Apache 2.0

```bash
# Install
sudo apt install xrdp             # Debian/Ubuntu
sudo dnf install xrdp             # Fedora

# Enable and start
sudo systemctl enable xrdp
sudo systemctl start xrdp

# Connect from Windows: mstsc → linux_ip:3389
# Or from Linux: xfreerdp /v:linux_ip
```

**How xrdp works:**
- Listens on port 3389 (RDP)
- Creates a new X session (Xvnc or Xorg backend)
- Windows RDP client connects natively
- Supports clipboard, drive mapping, audio (limited)

**Best for:** Accessing Linux desktops from Windows using the built-in Remote Desktop client

---

## 11. Comparison Tables

### Display Protocols

| Protocol | Type | Encryption | Performance | Audio | USB | Best For |
|----------|------|-----------|-------------|-------|-----|----------|
| **X11** | Draw commands | None (use SSH) | Good (local), moderate (remote) | ❌ | ❌ | Linux GUI forwarding |
| **VNC (RFB)** | Framebuffer (pixels) | None (use SSH) | Moderate | ❌ | ❌ | Universal remote desktop |
| **RDP** | Draw commands + bitmap | TLS | Very good | ✅ | ✅ | Windows remote access |
| **SPICE** | Draw commands + video | TLS | Excellent | ✅ | ✅ | VM displays (KVM/QEMU) |
| **Wayland** | Compositor-based | N/A (local only) | Excellent | N/A | N/A | Modern Linux desktops |

### Remote Desktop Tools

| Tool | Open Source | Self-Host | Latency | Gaming | Platform | Free |
|------|-----------|-----------|---------|--------|----------|------|
| **Parsec** | ❌ | ❌ | Ultra-low | ✅ Best | Win/Mac/Lin/Android | ✅ Personal |
| **AnyDesk** | ❌ | ❌ | Low | ⚠️ | All | ✅ Personal |
| **Sunshine+Moonlight** | ✅ | ✅ | Ultra-low | ✅ Best | All | ✅ |
| **RustDesk** | ✅ | ✅ | Low | ❌ | All + Web | ✅ |
| **NoMachine** | ❌ | ✅ | Low | ⚠️ | All | ✅ Personal |
| **Guacamole** | ✅ | ✅ | Moderate | ❌ | Web browser | ✅ |
| **noVNC** | ✅ | ✅ | Moderate | ❌ | Web browser | ✅ |
| **xrdp** | ✅ | ✅ | Good | ❌ | Linux server | ✅ |

### Quick Decision Guide

| Need | Best Choice |
|------|------------|
| Remote gaming | **Parsec** or **Sunshine + Moonlight** |
| Quick support/help | **AnyDesk** or **RustDesk** |
| Privacy / self-hosted | **RustDesk** (full control) |
| Linux remote desktop | **NoMachine** or **xrdp** |
| Browser-based access | **Guacamole** (multi-protocol) or **noVNC** |
| VM console access | **SPICE** (with virt-viewer) |
| WSL GUI apps on Windows | **VcXsrv** or **Win-KeX** |
| Enterprise / many machines | **Guacamole** |
| Open-source gaming stream | **Sunshine + Moonlight** |

---

## See Also

- [SSH Tunneling](ssh-tunneling.md) — Reverse proxies and advanced tunneling
- [VPN & ZTNA](vpn-and-ztna.md) — Tailscale, WireGuard for private remote access
- [Network Protocols](../fundamentals/network-protocols.md) — SSH, RDP, VNC protocol details
- [Desktop Environments](../mobile/desktop-environments.md) — VNC/X11 setup on Termux
