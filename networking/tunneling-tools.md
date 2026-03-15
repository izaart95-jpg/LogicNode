# Tunneling Tools — Ngrok, LocalXpose, Cloudflared

Expose local services to the internet using dedicated tunneling tools. These go beyond SSH-based tunneling (see [ssh-tunneling.md](ssh-tunneling.md)) by offering dashboards, custom domains, authentication, and persistent tunnels.

---

## Table of Contents
1. [Overview & How Tunneling Works](#1-overview--how-tunneling-works)
2. [Ngrok](#2-ngrok)
3. [LocalXpose](#3-localxpose)
4. [Cloudflared (Cloudflare Tunnel)](#4-cloudflared-cloudflare-tunnel)
5. [Comparison Table](#5-comparison-table)
6. [Advanced Techniques](#6-advanced-techniques)

---

## 1. Overview & How Tunneling Works

```
┌──────────────┐         Encrypted Tunnel        ┌──────────────┐        ┌──────────┐
│  Your Local  │ ──────────────────────────────▶  │  Relay/Edge  │ ◀───── │  Public  │
│  Service     │  (outbound connection, no NAT    │  Server      │  HTTP  │  Users   │
│  :8080       │   issues, no port forwarding)    │  (ngrok/cf)  │        │          │
└──────────────┘                                  └──────────────┘        └──────────┘
```

**Why use tunneling tools instead of port forwarding?**
- No router access needed (works behind NAT, CGNAT, firewalls)
- Instant HTTPS with valid TLS certificates
- Built-in request inspection/replay (ngrok)
- Auth, rate limiting, IP restrictions
- Custom/stable subdomains
- Works from any network (hotel, office, mobile hotspot)

---

## 2. Ngrok

- **Website:** https://ngrok.com
- **What it is:** The most popular tunneling tool — exposes local servers with a single command
- **Pricing:** Free tier + paid plans ($8/mo+)
- **Platform:** Windows, macOS, Linux, Docker
- **Protocols:** HTTP, HTTPS, TCP, TLS

### 2.1 Installation

```bash
# Linux (snap)
sudo snap install ngrok

# Linux (apt)
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# macOS
brew install ngrok

# Direct download
curl -sSL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz | tar xz
sudo mv ngrok /usr/local/bin/

# Docker
docker run -it -e NGROK_AUTHTOKEN=<token> ngrok/ngrok http 8080
```

### 2.2 Authentication

```bash
# Sign up at https://dashboard.ngrok.com/signup
# Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken

ngrok config add-authtoken YOUR_AUTH_TOKEN
# Stored in ~/.config/ngrok/ngrok.yml
```

### 2.3 Basic Usage

```bash
# Expose HTTP server on port 8080
ngrok http 8080

# Expose with specific subdomain (paid)
ngrok http --domain=myapp.ngrok-free.app 8080

# Expose TCP (any protocol — SSH, database, game server)
ngrok tcp 22        # SSH
ngrok tcp 3306      # MySQL
ngrok tcp 5432      # PostgreSQL
ngrok tcp 25565     # Minecraft

# Expose TLS
ngrok tls 443

# Expose a file server (built-in)
ngrok http file:///home/user/share

# Expose HTTPS backend (skip cert verification)
ngrok http https://localhost:8443
```

### 2.4 Ngrok Dashboard & Inspection

When you start a tunnel, ngrok provides:
- **Public URL:** `https://xxxx-xx-xx-xx-xx.ngrok-free.app`
- **Web Inspector:** `http://127.0.0.1:4040` — view all requests, replay them, inspect headers/body

```
Session Status    online
Account           user@email.com (Plan: Free)
Version           3.x.x
Region            United States (us)
Latency           45ms
Web Interface     http://127.0.0.1:4040
Forwarding        https://a1b2-203-0-113-1.ngrok-free.app -> http://localhost:8080
```

### 2.5 Configuration File

```yaml
# ~/.config/ngrok/ngrok.yml
version: "3"
agent:
  authtoken: YOUR_AUTH_TOKEN

tunnels:
  webapp:
    proto: http
    addr: 8080
    inspect: true
    domain: myapp.ngrok-free.app  # paid feature

  api:
    proto: http
    addr: 3000
    inspect: true

  ssh:
    proto: tcp
    addr: 22

  database:
    proto: tcp
    addr: 5432
```

```bash
# Start all tunnels
ngrok start --all

# Start specific tunnel
ngrok start webapp api
```

### 2.6 Advanced Features

```bash
# Basic auth (protect your tunnel)
ngrok http 8080 --basic-auth="user:password"

# OAuth (Google, GitHub, etc.) — paid
ngrok http 8080 --oauth=google --oauth-allow-email=you@gmail.com

# Webhook verification
ngrok http 8080 --verify-webhook=stripe --verify-webhook-secret=whsec_xxx

# IP restrictions (paid)
ngrok http 8080 --cidr-allow="203.0.113.0/24"

# Custom headers
ngrok http 8080 --request-header-add="X-Custom: value"

# Rate limiting
ngrok http 8080 --traffic-policy-file=policy.yml
```

**Traffic Policy (policy.yml):**
```yaml
on_http_request:
  - actions:
      - type: rate-limit
        config:
          name: general
          algorithm: sliding_window
          capacity: 100
          rate: 60s
```

### 2.7 Ngrok API

```bash
# List tunnels
curl http://localhost:4040/api/tunnels

# Create tunnel via API
curl -X POST http://localhost:4040/api/tunnels \
  -H "Content-Type: application/json" \
  -d '{"name":"test","proto":"http","addr":"8080"}'

# Ngrok Cloud API (manage from anywhere)
curl https://api.ngrok.com/tunnels \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Ngrok-Version: 2"
```

### 2.8 Ngrok Free Tier Limits

| Feature | Free | Personal ($8/mo) | Pro ($20/mo) |
|---------|------|-------------------|--------------|
| **Tunnels** | 1 agent, 1 domain | 1 agent, 1 domain | 2 agents, 2 domains |
| **Endpoints** | 3 | 10 | 20 |
| **Bandwidth** | 1 GB/mo | 1 GB/mo | 1 GB/mo |
| **Requests** | 20,000/mo | 40,000/mo | 80,000/mo |
| **TCP tunnels** | ❌ | ✅ | ✅ |
| **Custom domains** | ❌ (ngrok subdomain) | ✅ | ✅ |
| **OAuth/OIDC** | ❌ | ✅ | ✅ |
| **IP Restrictions** | ❌ | ✅ | ✅ |
| **Web Inspector** | ✅ | ✅ | ✅ |

> ⚠️ Free tier URLs change every restart. Visitors see a "ngrok" interstitial warning page.

---

## 3. LocalXpose

- **Website:** https://localxpose.io
- **What it is:** Reverse proxy / tunneling tool with generous free tier and support for HTTP, TCP, UDP, TLS
- **Pricing:** Free tier + paid ($6/mo+)
- **Platform:** Windows, macOS, Linux, Docker
- **Protocols:** HTTP, HTTPS, TCP, UDP, TLS

### 3.1 Installation

```bash
# Linux
curl -sSL https://localxpose.io/install | bash

# Or direct binary
wget https://api.localxpose.io/api/v2/downloads/loclx-linux-amd64.zip
unzip loclx-linux-amd64.zip
sudo mv loclx /usr/local/bin/

# macOS
brew install localxpose

# npm
npm install -g localxpose

# Docker
docker run --rm -it localxpose/localxpose http --to 8080
```

### 3.2 Authentication

```bash
# Sign up at https://localxpose.io
# Get token from dashboard

loclx account login
# Or
loclx account login --token YOUR_ACCESS_TOKEN
```

### 3.3 Basic Usage

```bash
# HTTP tunnel
loclx tunnel http --to 8080

# HTTP with custom subdomain (free!)
loclx tunnel http --to 8080 --subdomain myapp

# HTTPS with Let's Encrypt cert
loclx tunnel http --to 8080 --https

# TCP tunnel (SSH, databases, game servers)
loclx tunnel tcp --to 22
loclx tunnel tcp --to 3306
loclx tunnel tcp --to 25565

# UDP tunnel (game servers, DNS, VoIP)
loclx tunnel udp --to 53
loclx tunnel udp --to 19132     # Minecraft Bedrock

# TLS tunnel
loclx tunnel tls --to 443

# Custom domain (paid)
loclx tunnel http --to 8080 --domain mydomain.com
```

### 3.4 Configuration File

```yaml
# ~/.localxpose/config.yaml
tunnels:
  web:
    type: http
    to: 8080
    subdomain: myapp
    https: true
    basic_auth: "user:password"

  ssh:
    type: tcp
    to: 22

  game:
    type: udp
    to: 19132

  api:
    type: http
    to: 3000
    subdomain: api
```

```bash
# Start all tunnels from config
loclx tunnel --config
```

### 3.5 Key Features

| Feature | Details |
|---------|---------|
| **Custom subdomains** | Free on `.loclx.io` domain |
| **UDP support** | Unique — most tunneling tools don't support UDP |
| **Let's Encrypt** | Auto TLS certificates |
| **Basic Auth** | Protect tunnels with username/password |
| **Reserved domains** | Keep your subdomain across restarts (paid) |
| **Multiple tunnels** | Run several simultaneously |
| **Dashboard** | Web dashboard with connection logs |
| **Regions** | US, EU, Asia-Pacific |

### 3.6 LocalXpose Free vs Paid

| Feature | Free | Pro ($6/mo) | Business ($12/mo) |
|---------|------|-------------|-------------------|
| **Tunnels** | 1 | 5 | 10 |
| **HTTP/HTTPS** | ✅ | ✅ | ✅ |
| **TCP** | ✅ | ✅ | ✅ |
| **UDP** | ✅ | ✅ | ✅ |
| **Custom subdomains** | ✅ (random or chosen) | ✅ (reserved) | ✅ (reserved) |
| **Custom domains** | ❌ | ✅ | ✅ |
| **Bandwidth** | 5 GB/mo | 50 GB/mo | 200 GB/mo |
| **Connections** | Limited | Higher | Highest |

---

## 4. Cloudflared (Cloudflare Tunnel)

- **Website:** https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
- **What it is:** Cloudflare's tunneling daemon — connect local services to Cloudflare's edge network for free, with full DDoS protection, WAF, caching, and zero-trust access
- **Pricing:** **Free** (with a Cloudflare account and your own domain)
- **Platform:** Windows, macOS, Linux, Docker, ARM
- **Protocols:** HTTP, HTTPS, SSH, RDP, TCP, Unix sockets

### 4.1 Why Cloudflared?

Unlike ngrok/localxpose which give you a random subdomain, Cloudflare Tunnel connects your service to **your own domain** — with Cloudflare's entire infrastructure in front:

- **Free DDoS protection** (enterprise-grade)
- **Free WAF** (Web Application Firewall)
- **Free CDN/caching**
- **Free SSL/TLS** (edge certificates)
- **Zero Trust access policies** (Cloudflare Access)
- **No exposed ports** — your server has no public IP needed
- **Unlimited bandwidth** on free plan

### 4.2 Installation

```bash
# Debian/Ubuntu
curl -sSL https://pkg.cloudflare.com/cloudflare-main.gpg \
  | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update && sudo apt install cloudflared

# macOS
brew install cloudflare/cloudflare/cloudflared

# Docker
docker run cloudflare/cloudflared:latest tunnel --no-autoupdate run --token YOUR_TOKEN

# Direct binary
curl -sSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared && sudo mv cloudflared /usr/local/bin/
```

### 4.3 Quick Tunnel (No Setup — Like Ngrok)

```bash
# Instant tunnel — no account, no domain needed
cloudflared tunnel --url http://localhost:8080

# Output:
# +-----------------------------------------------------------+
# |  Your quick Tunnel has been created! Visit it at:          |
# |  https://random-words-here.trycloudflare.com              |
# +-----------------------------------------------------------+

# Expose any local service instantly
cloudflared tunnel --url http://localhost:3000    # Web app
cloudflared tunnel --url http://localhost:8888    # Jupyter
cloudflared tunnel --url http://localhost:5000    # Flask
cloudflared tunnel --url tcp://localhost:22       # SSH
```

> **Quick tunnels are free, no account required**, and use `*.trycloudflare.com` domains. Great for testing.

### 4.4 Named Tunnels (Production Setup)

For persistent tunnels with your own domain:

```bash
# Step 1: Login to Cloudflare
cloudflared tunnel login
# Opens browser → authorize → cert saved to ~/.cloudflared/cert.pem

# Step 2: Create a named tunnel
cloudflared tunnel create my-tunnel
# Output: Created tunnel my-tunnel with id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Step 3: Configure DNS (auto)
cloudflared tunnel route dns my-tunnel app.yourdomain.com
# Creates a CNAME: app.yourdomain.com → xxxxxxxx.cfargotunnel.com

# Step 4: Create config file
cat > ~/.cloudflared/config.yml << 'EOF'
tunnel: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
credentials-file: /root/.cloudflared/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.json

ingress:
  # Route app.yourdomain.com → local port 8080
  - hostname: app.yourdomain.com
    service: http://localhost:8080

  # Route api.yourdomain.com → local port 3000
  - hostname: api.yourdomain.com
    service: http://localhost:3000

  # Route ssh.yourdomain.com → local SSH
  - hostname: ssh.yourdomain.com
    service: ssh://localhost:22

  # Route rdp.yourdomain.com → local RDP
  - hostname: rdp.yourdomain.com
    service: rdp://localhost:3389

  # Catch-all (required)
  - service: http_status:404
EOF

# Step 5: Run the tunnel
cloudflared tunnel run my-tunnel
```

### 4.5 Run as a Service (Persistent)

```bash
# Install as systemd service
sudo cloudflared service install

# Or manually
sudo cloudflared --config /root/.cloudflared/config.yml tunnel run my-tunnel

# Enable on boot
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

### 4.6 Cloudflare Zero Trust Access

Protect your tunneled services with authentication — no VPN needed:

```
Browser → Cloudflare Edge → Access Policy (login required) → Tunnel → Your Service
```

1. Go to **Cloudflare Zero Trust Dashboard** (https://one.dash.cloudflare.com)
2. **Access → Applications → Add Application**
3. Set policy: require email, Google login, GitHub login, one-time pin, etc.
4. Apply to your tunnel hostname

Now `app.yourdomain.com` requires login before anyone can reach your local service.

**Free Zero Trust includes:**
- 50 users
- Email OTP, Google, GitHub, SAML, OIDC identity providers
- Device posture checks
- Session duration controls

### 4.7 Multi-Service Config Example

```yaml
# ~/.cloudflared/config.yml — expose entire homelab
tunnel: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
credentials-file: /root/.cloudflared/xxxxxxxx.json

ingress:
  # Web app
  - hostname: app.example.com
    service: http://localhost:8080

  # API server
  - hostname: api.example.com
    service: http://localhost:3000

  # Grafana dashboard
  - hostname: grafana.example.com
    service: http://localhost:3001

  # Home Assistant
  - hostname: home.example.com
    service: http://localhost:8123

  # SSH (use with `cloudflared access ssh`)
  - hostname: ssh.example.com
    service: ssh://localhost:22

  # RDP
  - hostname: rdp.example.com
    service: rdp://localhost:3389

  # Minecraft server
  - hostname: mc.example.com
    service: tcp://localhost:25565

  # Catch-all
  - service: http_status:404
```

### 4.8 SSH Through Cloudflare Tunnel

**Server side:**
```yaml
# In config.yml ingress:
- hostname: ssh.example.com
  service: ssh://localhost:22
```

**Client side:**
```bash
# Install cloudflared on client machine too, then:

# Option 1: ProxyCommand in SSH config
# ~/.ssh/config
Host ssh.example.com
  ProxyCommand cloudflared access ssh --hostname %h

ssh user@ssh.example.com

# Option 2: Short-lived certificates (no SSH keys needed!)
# Configure in Zero Trust dashboard
```

### 4.9 Cloudflared Commands Reference

```bash
cloudflared tunnel --url http://localhost:8080   # Quick tunnel
cloudflared tunnel login                          # Authenticate
cloudflared tunnel create NAME                    # Create named tunnel
cloudflared tunnel route dns NAME HOSTNAME        # Add DNS route
cloudflared tunnel run NAME                       # Start tunnel
cloudflared tunnel list                           # List tunnels
cloudflared tunnel info NAME                      # Tunnel details
cloudflared tunnel delete NAME                    # Delete tunnel
cloudflared tunnel cleanup NAME                   # Remove stale connections
cloudflared service install                       # Install as service
cloudflared update                                # Update cloudflared
```

---

## 5. Comparison Table

| Feature | Ngrok | LocalXpose | Cloudflared |
|---------|-------|------------|-------------|
| **Free Tier** | Limited (1 tunnel, 1GB/mo) | Generous (5GB/mo) | **Unlimited** (with own domain) |
| **Quick Tunnel (no account)** | ❌ (need auth) | ❌ (need auth) | ✅ `trycloudflare.com` |
| **HTTP/HTTPS** | ✅ | ✅ | ✅ |
| **TCP** | ✅ (paid) | ✅ (free) | ✅ |
| **UDP** | ❌ | ✅ | ❌ (QUIC only) |
| **TLS** | ✅ | ✅ | ✅ |
| **Custom Subdomains (free)** | ❌ | ✅ | ✅ (own domain) |
| **Custom Domains** | Paid | Paid | **Free** (your domain on CF) |
| **DDoS Protection** | ❌ | ❌ | ✅ (enterprise-grade) |
| **WAF** | ❌ | ❌ | ✅ (free) |
| **CDN/Caching** | ❌ | ❌ | ✅ (free) |
| **Zero Trust Auth** | OAuth (paid) | Basic auth | ✅ (free, 50 users) |
| **Request Inspection** | ✅ (localhost:4040) | Dashboard | Cloudflare dashboard |
| **Multiple Services** | Config file | Config file | ✅ (single tunnel, multi-ingress) |
| **Run as Service** | ❌ (use supervisor) | ❌ | ✅ (native systemd) |
| **Bandwidth** | 1 GB/mo (free) | 5 GB/mo (free) | **Unlimited** |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ (setup), ⭐⭐⭐⭐⭐ (after) |
| **Best For** | Dev/testing, webhooks | UDP tunnels, quick sharing | Production, homelab, security |

### Quick Decision Guide

| Use Case | Best Tool |
|----------|-----------|
| Webhook testing / quick demo | **Ngrok** (inspect + replay) |
| Expose game server (UDP) | **LocalXpose** |
| Production web app | **Cloudflared** (DDoS + WAF + CDN free) |
| Homelab (many services) | **Cloudflared** (multi-ingress) |
| SSH access without VPN | **Cloudflared** (Zero Trust) |
| No account, instant tunnel | **Cloudflared** quick tunnel |
| API development / debugging | **Ngrok** (request inspector) |
| Free TCP tunnels | **LocalXpose** |

---

## 6. Advanced Techniques

### 6.1 Persistent Tunnel with Auto-Restart

```bash
# Ngrok with systemd
sudo cat > /etc/systemd/system/ngrok.service << 'EOF'
[Unit]
Description=Ngrok Tunnel
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/ngrok http 8080 --log=stdout
Restart=always
RestartSec=10
User=youruser

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now ngrok
```

### 6.2 Chaining with Reverse Proxy

```bash
# Expose multiple local services through one tunnel using nginx
# nginx.conf
upstream app    { server 127.0.0.1:8080; }
upstream api    { server 127.0.0.1:3000; }
upstream grafana { server 127.0.0.1:3001; }

server {
    listen 9000;
    location /         { proxy_pass http://app; }
    location /api/     { proxy_pass http://api; }
    location /grafana/ { proxy_pass http://grafana; }
}

# Then expose single port
ngrok http 9000
```

### 6.3 Webhook Development Workflow

```bash
# 1. Start your API locally
python app.py  # listening on :5000

# 2. Expose with ngrok
ngrok http 5000

# 3. Copy the URL: https://abc123.ngrok-free.app
# 4. Set it as webhook URL in Stripe/GitHub/Slack/etc.
# 5. Open http://localhost:4040 to inspect incoming webhooks
# 6. Replay failed requests with one click
```

---

## See Also

- [SSH Tunneling](ssh-tunneling.md) — Pinggy, Serveo, localhost.run (SSH-based tunnels)
- [Remote Access](remote-access.md) — RDP, VNC, remote desktop tools
- [VPN & ZTNA](vpn-and-ztna.md) — Tailscale, WireGuard, Cloudflare WARP
- [Free DNS Services](free-dns-services.md) — DuckDNS, FreeDNS for custom domains
- [APIs & Developer Resources](../reference/apis-and-resources.md) — Public APIs, webhook testing endpoints
