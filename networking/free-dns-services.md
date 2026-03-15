# Free Dynamic DNS & Domain Services

This document covers free Dynamic DNS (DDNS) providers, free domain services, and related tools for pointing domain names at dynamic IP addresses — essential for self-hosting, home labs, IoT projects, and development.

---

## Table of Contents
1. [What is Dynamic DNS?](#1-what-is-dynamic-dns)
2. [How DDNS Works](#2-how-ddns-works)
3. [Free DDNS Providers](#3-free-ddns-providers)
4. [Free Domain Name Services](#4-free-domain-name-services)
5. [Free DNS Hosting (Static)](#5-free-dns-hosting-static)
6. [Comparison Table](#6-comparison-table)
7. [Setup Guides](#7-setup-guides)
8. [Use Cases](#8-use-cases)
9. [Security Considerations](#9-security-considerations)

---

## 1. What is Dynamic DNS?

Most home internet connections have **dynamic IP addresses** — the ISP changes your public IP periodically. Dynamic DNS services automatically update a hostname to point to your current IP, so you can always reach your server by name.

```
Without DDNS:
  Your IP changes: 203.0.113.50 → 198.51.100.22 → ???
  You lose access to your server.

With DDNS:
  myhomelab.ddns.net → always resolves to your current IP
  DDNS client detects IP change → updates DNS record automatically
```

---

## 2. How DDNS Works

```
┌─────────────┐         ┌──────────────────┐         ┌──────────┐
│ Your Device  │──HTTP──▶│  DDNS Provider   │──DNS──▶ │ Visitors  │
│ (runs client)│  update │  (No-IP, Dynu)   │  query  │           │
│              │         │                  │         │           │
│ Detects IP   │         │ Updates A record │         │ Resolves  │
│ change       │         │ for your hostname│         │ hostname  │
└─────────────┘         └──────────────────┘         └──────────┘
```

**Update methods:**
- Dedicated client software (runs on your device)
- Router built-in DDNS support (most routers support No-IP, DynDNS, Dynu)
- Cron job with `curl` or `wget` hitting an update URL
- API calls (for automation)

---

## 3. Free DDNS Providers

### 3.1 No-IP
- **Website:** https://www.noip.com
- **Free Tier:** Up to 3 hostnames
- **Domains:** `*.ddns.net`, `*.hopto.org`, `*.zapto.org`, `*.sytes.net`, and ~15 more
- **Renewal:** Must confirm hostnames every 30 days (free tier)
- **Clients:** Windows, macOS, Linux, router built-in
- **API:** Yes

**Setup:**
```bash
# Linux — Install No-IP DUC (Dynamic Update Client)
wget https://www.noip.com/client/linux/noip-duc-linux.tar.gz
tar xf noip-duc-linux.tar.gz
cd noip-2.1.9-1/
make
sudo make install
sudo /usr/local/bin/noip2 -C    # Configure (enter credentials)
sudo /usr/local/bin/noip2        # Start
```

**Or update via cron:**
```bash
# Simple curl-based update
curl "https://dynupdate.no-ip.com/nic/update?hostname=myhost.ddns.net" \
  --user "email:password"
```

**Router Support:** Most consumer routers (TP-Link, ASUS, Netgear, etc.) have No-IP built in under WAN → DDNS settings.

---

### 3.2 Dynu
- **Website:** https://www.dynu.com
- **Free Tier:** Up to 4 hostnames, unlimited updates
- **Domains:** `*.dynu.net`, `*.freeddns.org`, `*.mywire.org`, `*.loseyourip.com`, and ~10 more
- **Renewal:** No 30-day confirmation required
- **Clients:** Windows, Linux, macOS, DD-WRT, router built-in
- **API:** Full REST API
- **Extras:** Free DNS hosting, email forwarding, SSL certificates

**Setup:**
```bash
# Linux — Dynu DDNS Client
wget https://www.dynu.com/support/downloadfile/34
chmod +x dynuiuc
./dynuiuc

# Or API update
curl "https://api.dynu.com/nic/update?hostname=myhost.dynu.net&myip=auto" \
  --user "username:password"
```

**Advantage over No-IP:** No forced 30-day renewal. Set and forget.

---

### 3.3 DuckDNS
- **Website:** https://www.duckdns.org
- **Free Tier:** Up to 5 subdomains
- **Domain:** `*.duckdns.org`
- **Renewal:** No forced renewals
- **Auth:** Token-based (GitHub, Google, Reddit login)
- **API:** Simple HTTP update
- **Extras:** Built-in Let's Encrypt support guides

**Setup:**
```bash
# Update via curl (cron every 5 minutes)
echo "*/5 * * * * curl -s 'https://www.duckdns.org/update?domains=myhost&token=YOUR_TOKEN&ip='" >> /etc/crontab

# Or one-liner
curl "https://www.duckdns.org/update?domains=myhost&token=YOUR_TOKEN&ip="
```

**Popular with:** Home Assistant, Raspberry Pi, self-hosting communities.

---

### 3.4 FreeDNS (afraid.org)
- **Website:** https://freedns.afraid.org
- **Free Tier:** Up to 5 subdomains (shared domains) or bring your own domain
- **Domains:** Hundreds of community-shared domains (e.g., `*.mooo.com`, `*.us.to`, `*.chickenkiller.com`)
- **Renewal:** No forced renewals
- **API:** Direct URL update
- **Extras:** Supports A, AAAA, CNAME, MX, TXT, NS, LOC, RP, SRV records

**Setup:**
```bash
# Get your update URL from the FreeDNS web interface
# Then cron it:
*/5 * * * * curl -s "https://freedns.afraid.org/dynamic/update.php?YOUR_UPDATE_KEY"
```

**Advantage:** Massive selection of free subdomains. Good for creative domain names.

---

### 3.5 Cloudflare (DDNS via API)
- **Website:** https://www.cloudflare.com
- **Free Tier:** Unlimited DNS records, free DNS hosting (bring your own domain)
- **DDNS:** Not native — use API + script to auto-update
- **Extras:** Free CDN, DDoS protection, SSL, analytics

**DDNS Script:**
```bash
#!/bin/bash
# Cloudflare DDNS updater
ZONE_ID="your_zone_id"
RECORD_ID="your_record_id"
API_TOKEN="your_api_token"
HOSTNAME="home.yourdomain.com"

IP=$(curl -s https://api.ipify.org)

curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  --data "{\"type\":\"A\",\"name\":\"$HOSTNAME\",\"content\":\"$IP\",\"ttl\":120,\"proxied\":false}"
```

**Community tools:**
- `cloudflare-ddns` (Python): https://github.com/timothymiller/cloudflare-ddns
- `ddclient` (supports Cloudflare)

**Best for:** People who already own a domain and want free professional DNS with DDNS.

---

### 3.6 Desec.io
- **Website:** https://desec.io
- **Free Tier:** Unlimited domains and records
- **DDNS:** Native API support
- **Extras:** DNSSEC enabled by default, privacy-focused (non-profit, German)
- **API:** Full REST API with token auth

**Setup:**
```bash
# Update via API
curl -s -X PATCH "https://update.dedyn.io/?hostname=myhost.dedyn.io" \
  -H "Authorization: Token YOUR_TOKEN"
```

**Best for:** Privacy-conscious users who want DNSSEC out of the box.

---

### 3.7 nsupdate.info
- **Website:** https://www.nsupdate.info
- **Free Tier:** Free DDNS with own subdomains
- **Domain:** `*.nsupdate.info`
- **Extras:** Open source, self-hostable
- **Source:** https://github.com/nsupdate-info/nsupdate.info

---

### 3.8 Sslip.io
- **Website:** https://sslip.io
- **How it works:** Embeds the IP address in the domain name itself
- **Example:** `192-168-1-50.sslip.io` resolves to `192.168.1.50`
- **No account needed** — instant, no setup
- **Use case:** Development, testing, quick demos

```bash
# Any IP works:
nslookup 10-0-0-1.sslip.io        # → 10.0.0.1
nslookup 192-168-1-100.sslip.io   # → 192.168.1.100
```

---

### 3.9 nip.io
- **Website:** https://nip.io
- **Same concept as sslip.io**
- **Example:** `app.192.168.1.50.nip.io` resolves to `192.168.1.50`
- **Use case:** Local development with wildcard DNS

---

## 4. Free Domain Name Services

These provide actual free domain names (not just subdomains).

### 4.1 Freenom (Status: Mostly Defunct)
- **Was:** Free .tk, .ml, .ga, .cf, .gq domains
- **Current status:** No longer registering new free domains (as of 2023, after ICANN dispute)
- **Note:** Existing domains may still work but are unreliable

### 4.2 FreeDomain.one
- **Website:** https://freedomain.one
- **Offers:** Free subdomain under their domain
- **Use case:** Quick project hosting

### 4.3 pp.ua
- **Website:** https://nic.ua/en/domains/.pp.ua
- **Offers:** Free `.pp.ua` subdomains (Ukrainian ccTLD)
- **Registration:** Manual, requires account

### 4.4 eu.org
- **Website:** https://nic.eu.org
- **Offers:** Free `.eu.org` domains
- **Wait time:** Manual approval (can take days/weeks)
- **Quality:** Looks professional (`yourname.eu.org`)
- **Best for:** Non-commercial projects

### 4.5 is-a.dev
- **Website:** https://is-a.dev
- **Offers:** Free `yourname.is-a.dev` subdomain
- **How:** Submit a PR on GitHub with your DNS config
- **Best for:** Developer portfolios

### 4.6 js.org
- **Website:** https://js.org
- **Offers:** Free `yourproject.js.org` subdomain
- **How:** GitHub PR-based
- **Best for:** JavaScript project documentation

---

## 5. Free DNS Hosting (Static)

If you own a domain and need free DNS hosting (not DDNS):

| Provider | Free Records | DNSSEC | Extras |
|----------|-------------|--------|--------|
| **Cloudflare** | Unlimited | Yes | CDN, DDoS protection, analytics |
| **Desec.io** | Unlimited | Yes | Privacy-focused, non-profit |
| **Hurricane Electric** (dns.he.net) | 50 zones | Yes | Full record types, DDNS, slave DNS |
| **Namecheap FreeDNS** | 100 records | No | Basic DNS hosting |
| **ClouDNS** | 1 zone, 4 records | No | Paid plans for more |
| **Dynu** | 4 hostnames | No | Also offers DDNS |
| **1984.is** | Unlimited | Yes | Icelandic, privacy-focused |
| **Gcore** | Unlimited | Yes | CDN and DNS |

**Recommendation:** Cloudflare for most users (free, fast, DDoS-protected). Desec.io for privacy.

---

## 6. Comparison Table

### DDNS Providers

| Provider | Free Hostnames | Renewal Required | Own Domain Support | Router Support | API | DNSSEC |
|----------|---------------|-----------------|-------------------|----------------|-----|--------|
| **No-IP** | 3 | Every 30 days | Paid | Excellent | Yes | No |
| **Dynu** | 4 | No | Yes (free) | Good | REST | No |
| **DuckDNS** | 5 | No | No | Limited | HTTP | No |
| **FreeDNS** | 5 | No | Yes (free) | Manual | URL | No |
| **Cloudflare** | Unlimited | No | Required (BYO) | Via script | REST | Yes |
| **Desec.io** | Unlimited | No | Yes (free) | Via script | REST | Yes |
| **nsupdate.info** | Free | No | No | Manual | HTTP | No |

### Quick Decision Guide

| Need | Best Choice |
|------|------------|
| Easiest setup, router support | **No-IP** |
| No renewal hassle, set-and-forget | **Dynu** or **DuckDNS** |
| Creative free subdomains | **FreeDNS (afraid.org)** |
| Professional DNS + CDN + DDoS protection | **Cloudflare** (BYO domain) |
| Privacy + DNSSEC | **Desec.io** |
| Development / testing only | **sslip.io** or **nip.io** |
| Free real-looking domain | **eu.org** |

---

## 7. Setup Guides

### Generic DDNS with ddclient (Linux)

`ddclient` is a universal DDNS update client supporting most providers.

```bash
# Install
sudo apt install ddclient    # Debian/Ubuntu
sudo dnf install ddclient    # Fedora

# Configure
sudo nano /etc/ddclient.conf
```

**Example configs:**

```ini
# No-IP
protocol=noip
login=your_email
password=your_password
your-hostname.ddns.net

# DuckDNS
protocol=duckdns
password=your-token
your-hostname

# Cloudflare
protocol=cloudflare
zone=yourdomain.com
login=token
password=your-api-token
home.yourdomain.com

# Dynu
protocol=dyndns2
server=api.dynu.com
login=username
password=password
your-hostname.dynu.net
```

```bash
# Test
sudo ddclient -daemon=0 -verbose -noquiet

# Enable service
sudo systemctl enable ddclient
sudo systemctl start ddclient
```

### Router-Based DDNS

Most routers support DDNS natively:
1. Login to router admin (usually `192.168.1.1`)
2. Navigate to **WAN** or **Internet** → **DDNS**
3. Select provider (No-IP, DynDNS, Dynu)
4. Enter hostname and credentials
5. Save — router handles updates automatically

---

## 8. Use Cases

| Use Case | Recommended Setup |
|----------|-------------------|
| **Home web server** | DuckDNS or No-IP + Let's Encrypt SSL |
| **Home lab SSH access** | Dynu + SSH on non-standard port |
| **Minecraft/game server** | No-IP (best router support) |
| **IoT device access** | DuckDNS (simple API for ESP32/Pi) |
| **Professional self-hosting** | Cloudflare (own domain) + DDNS script |
| **Security camera remote access** | Dynu + VPN (don't expose cameras directly!) |
| **Development/testing** | sslip.io or nip.io (zero setup) |

### ESP32 / Raspberry Pi DDNS Example

```python
# MicroPython — DuckDNS update on ESP32
import urequests

TOKEN = "your-duckdns-token"
DOMAIN = "myesp32"

def update_ddns():
    url = f"https://www.duckdns.org/update?domains={DOMAIN}&token={TOKEN}&ip="
    response = urequests.get(url)
    print("DDNS update:", response.text)
    response.close()

update_ddns()
```

---

## 9. Security Considerations

### Do's
- ✅ Always use HTTPS for DDNS update URLs
- ✅ Use API tokens instead of passwords where possible
- ✅ Combine DDNS with a VPN (Tailscale, WireGuard) for private access
- ✅ Use Let's Encrypt for free SSL on your DDNS hostname
- ✅ Enable DNSSEC if your provider supports it
- ✅ Use non-standard ports for SSH (change from 22)

### Don'ts
- ❌ Don't expose admin panels directly to the internet
- ❌ Don't use DDNS credentials in plaintext in shared scripts
- ❌ Don't rely on free DDNS for critical production services
- ❌ Don't expose IoT devices (cameras, NAS) without VPN or firewall

### DDNS + Let's Encrypt

```bash
# Get free SSL cert for your DDNS hostname
# (DuckDNS has a dedicated Certbot plugin)
sudo apt install certbot python3-certbot-dns-duckdns

# Or use HTTP challenge with any DDNS hostname
sudo certbot certonly --standalone -d myhost.ddns.net
```

---

## See Also

- [SSH Tunneling](ssh-tunneling.md) — Expose local services without DDNS
- [VPN & ZTNA](vpn-and-ztna.md) — Tailscale/WireGuard as DDNS alternatives
- [Network Protocols](../fundamentals/network-protocols.md) — DNS protocol deep dive
