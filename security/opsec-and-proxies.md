# OPSEC and Proxies

A comprehensive guide to operational security (OPSEC) practices, proxy tools, anonymization techniques, and disposable services. This document covers threat modeling, digital fingerprint management, proxy chaining, anti-fingerprint browsers, and temporary identity services for maintaining privacy during security research.

> **Disclaimer:** All tools, techniques, and services described in this document are intended for **authorized security testing, privacy protection, and educational purposes only**. Misusing these techniques to evade law enforcement, conduct unauthorized access, or engage in illegal activities is strictly prohibited. Always comply with applicable laws and regulations in your jurisdiction.

---

## Table of Contents

1. [OPSEC Fundamentals](#1-opsec-fundamentals)
2. [ProxyChains](#2-proxychains)
3. [Proxy Sources](#3-proxy-sources)
4. [Camoufox](#4-camoufox)
5. [Disposable Services](#5-disposable-services)
6. [Comparison Table](#6-comparison-table)
7. [See Also](#7-see-also)

---

## 1. OPSEC Fundamentals

### 1.1 What is OPSEC?

Operations Security (OPSEC) is the practice of identifying, controlling, and protecting critical information that could be used by adversaries to compromise your activities, identity, or infrastructure. Originally a military concept, OPSEC is now essential for security researchers, penetration testers, journalists, and privacy-conscious individuals.

The five-step OPSEC process:

1. **Identify critical information** — What data, if exposed, would compromise your operation?
2. **Analyze threats** — Who are your adversaries and what are their capabilities?
3. **Analyze vulnerabilities** — How could your critical information be exposed?
4. **Assess risk** — What is the likelihood and impact of exposure?
5. **Apply countermeasures** — Implement protections proportional to the risk

### 1.2 Threat Modeling Basics

Threat modeling helps you understand what you are protecting, from whom, and how. Key questions:

- **What am I protecting?** (Identity, location, activities, communications)
- **Who am I protecting it from?** (Script kiddies, corporations, nation-states)
- **What are the consequences of failure?** (Embarrassment, job loss, legal action, physical danger)
- **How likely is each threat?** (Prioritize based on realism)

Popular frameworks:

- **STRIDE:** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
- **LINDDUN:** Linkability, Identifiability, Non-repudiation, Detectability, Disclosure, Unawareness, Non-compliance (privacy-focused)

### 1.3 Digital Fingerprinting

Every interaction with the internet leaves traces. Your digital fingerprint includes:

- **Browser Fingerprint:** User-Agent, screen resolution, installed plugins, fonts, canvas rendering, WebGL, timezone, language
- **OS Fingerprint:** TCP/IP stack behavior, MTU, TTL values, clock skew
- **Hardware Fingerprint:** GPU rendering, audio context, battery API (deprecated but still used)
- **Behavioral Fingerprint:** Typing patterns, mouse movements, browsing habits

Check your fingerprint: https://browserleaks.com, https://amiunique.org

### 1.4 Compartmentalization

Compartmentalization means separating your identities, activities, and data so that a compromise of one does not expose others.

Best practices:

- **Separate VMs:** Use different virtual machines for different activities (Whonix, Qubes OS)
- **Separate Accounts:** Never reuse usernames, emails, or passwords across identities
- **Separate Browsers:** Dedicated browser profiles for each identity
- **Separate Networks:** Use different VPNs, Tor circuits, or networks per identity
- **Physical Separation:** Dedicated hardware for sensitive operations when necessary

### 1.5 Metadata Awareness

Metadata is data about data — often more revealing than the content itself.

| Source | Metadata Exposed | Mitigation |
|--------|-----------------|------------|
| **Photos (EXIF)** | GPS coordinates, camera model, timestamp | `exiftool -all= photo.jpg` |
| **Documents (Office/PDF)** | Author name, organization, revision history, software version | Remove via document properties or `mat2` |
| **Email Headers** | Sender IP, mail server chain, client software | Use privacy-focused email providers, Tor |
| **Network Traffic** | Source IP, DNS queries, timing, packet sizes | VPN, Tor, encrypted DNS |

```bash
# Remove EXIF metadata from images
exiftool -all= -overwrite_original image.jpg

# Remove metadata from multiple file types using mat2
pip install mat2
mat2 document.pdf
mat2 image.png

# View email headers (look for Received:, X-Originating-IP:)
cat email.eml | grep -i "received:\|x-originating"
```

---

## 2. ProxyChains

### 2.1 Overview

ProxyChains is a tool that forces any TCP connection made by a given application to go through one or more proxy servers (SOCKS4, SOCKS5, or HTTP). It works by hooking the network-related libc functions of dynamically linked programs via a preloaded DLL (LD_PRELOAD).

- **Website:** https://github.com/haad/proxychains
- **Maintained Fork:** https://github.com/rofl0r/proxychains-ng (proxychains4)
- **License:** GPLv2

### 2.2 Installation

```bash
# Debian/Ubuntu
sudo apt install proxychains4

# Arch Linux
sudo pacman -S proxychains-ng

# From source
git clone https://github.com/rofl0r/proxychains-ng.git
cd proxychains-ng
./configure --prefix=/usr --sysconfdir=/etc
make
sudo make install
```

### 2.3 Configuration

The main configuration file is `/etc/proxychains4.conf` (or `~/.proxychains/proxychains.conf` for per-user config).

```bash
# /etc/proxychains4.conf

# Chain mode (uncomment ONE):
dynamic_chain      # Skip dead proxies, continue through chain
# strict_chain     # All proxies must be online, fail if any is down
# random_chain     # Pick random proxies from the list each time
# round_robin_chain # Round-robin through the proxy list

# Proxy DNS requests through the chain (prevents DNS leaks)
proxy_dns

# Timeout settings
tcp_read_time_out 15000
tcp_connect_time_out 8000

# Proxy list (format: type host port [user] [pass])
[ProxyList]
socks5 127.0.0.1 9050         # Tor SOCKS proxy
socks5 proxy1.example.com 1080
http   proxy2.example.com 8080 user password
```

### 2.4 Chain Modes Explained

| Mode | Behavior | Use Case |
|------|----------|----------|
| **dynamic_chain** | Routes through each proxy in order, skips dead proxies | General use, most reliable |
| **strict_chain** | Routes through each proxy in exact order, fails if any is down | When exact routing matters |
| **random_chain** | Picks proxies randomly from the list | Maximum randomization |
| **round_robin_chain** | Cycles through proxies sequentially | Load distribution |

### 2.5 Usage

```bash
# Route nmap through proxy chain
proxychains4 nmap -sT -Pn target.example.com

# Route curl through proxy chain
proxychains4 curl https://check.torproject.org

# Route a web browser through proxy chain
proxychains4 firefox

# Combine with Tor for anonymity
# Ensure Tor is running (default SOCKS5 on 127.0.0.1:9050)
sudo systemctl start tor
proxychains4 curl https://check.torproject.org
```

### 2.6 Combining with Tor

For maximum anonymity, configure ProxyChains to route through Tor, then optionally through additional proxies:

```bash
# Install Tor
sudo apt install tor
sudo systemctl start tor

# Configure proxychains4.conf:
# [ProxyList]
# socks5 127.0.0.1 9050   # Tor first
# socks5 additional.proxy 1080  # Then through another proxy

# Your traffic flow: You -> Tor Network -> Additional Proxy -> Target
proxychains4 curl https://icanhazip.com
```

**Important:** ProxyChains only works with TCP connections and dynamically linked programs. It does not proxy UDP, ICMP, or statically compiled binaries.

---

## 3. Proxy Sources

### 3.1 spys.one

**spys.one** (formerly spys.ru) is a popular free proxy list aggregator that provides regularly updated lists of public proxy servers.

- **Website:** https://spys.one
- **Features:** Filter by country, anonymity level (transparent, anonymous, elite), protocol (HTTP, HTTPS, SOCKS4, SOCKS5), speed, and uptime
- **Update Frequency:** Lists refresh every few minutes
- **Anonymity Levels:**
  - **Transparent:** Target sees your real IP
  - **Anonymous:** Target knows you use a proxy but not your real IP
  - **Elite (High Anonymous):** Target cannot detect proxy usage

**Scraping Considerations:** spys.one uses JavaScript rendering for proxy display (anti-scraping measure). Automated scraping requires a headless browser or solving the JavaScript challenge. Respect the site's terms of service.

### 3.2 Webshare

**Webshare** is a commercial proxy provider offering datacenter and residential proxies with API access.

- **Website:** https://www.webshare.io
- **Free Tier:** 10 proxies with 1 GB bandwidth/month
- **Features:** Rotating proxies, static proxies, API access, SOCKS5 support
- **Authentication:** Username/password or IP whitelist

```python
# Python example: Using Webshare proxies with requests
import requests

proxy_url = "http://username:password@proxy.webshare.io:80"

proxies = {
    "http": proxy_url,
    "https": proxy_url,
}

response = requests.get("https://httpbin.org/ip", proxies=proxies)
print(response.json())
```

```python
# Webshare API: Fetch proxy list
import requests

API_KEY = "your-api-key"
url = "https://proxy.webshare.io/api/v2/proxy/list/"
headers = {"Authorization": f"Token {API_KEY}"}

response = requests.get(url, headers=headers)
proxies = response.json()["results"]

for p in proxies:
    print(f"{p['proxy_address']}:{p['port']}")
```

### 3.3 Other Proxy Sources

| Source | Type | Free Tier | Notes |
|--------|------|-----------|-------|
| **free-proxy-list.net** | Aggregator | Fully free | Basic filtering, frequent updates |
| **ProxyScrape** | Aggregator + API | Free + Premium | API access, protocol filtering |
| **Bright Data** | Commercial | Trial available | Enterprise-grade, residential/mobile proxies, expensive |
| **Oxylabs** | Commercial | Trial available | Large residential proxy pool |
| **SOCKS Proxy** | Aggregator | Free lists | SOCKS4/5 specific proxy lists |

**Warning:** Free public proxies are unreliable, slow, and potentially malicious (traffic interception, credential harvesting). Use them only for testing and never for sensitive operations. For any serious work, use paid proxy services or self-hosted solutions.

---

## 4. Camoufox

### 4.1 Overview

Camoufox is an anti-fingerprint browser based on Firefox, specifically designed for web scraping, automation, and avoiding browser fingerprint detection. It spoofs numerous browser attributes to blend in with regular browser traffic.

- **Website:** https://camoufox.com
- **Source:** https://github.com/daijro/camoufox
- **License:** MIT
- **Based on:** Firefox

### 4.2 Key Features

- **Canvas Fingerprint Spoofing:** Randomizes canvas rendering output
- **WebGL Spoofing:** Masks GPU information and rendering differences
- **Font Fingerprint Masking:** Normalizes font enumeration results
- **Screen Resolution Spoofing:** Reports configurable screen dimensions
- **Navigator Properties:** Spoofs platform, language, hardware concurrency
- **Timezone Masking:** Configurable timezone independent of system
- **Audio Context Spoofing:** Prevents audio-based fingerprinting

### 4.3 Installation and Usage

```bash
# Install via pip
pip install camoufox

# Download the Camoufox browser binary
camoufox fetch

# Verify installation
python -c "from camoufox.sync_api import Camoufox; print('OK')"
```

```python
# Basic usage with Python (synchronous API)
from camoufox.sync_api import Camoufox

with Camoufox() as browser:
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    page.screenshot(path="screenshot.png")
```

```python
# Async usage with Playwright
from camoufox.async_api import AsyncCamoufox
import asyncio

async def main():
    async with AsyncCamoufox() as browser:
        page = await browser.new_page()
        await page.goto("https://browserleaks.com/canvas")
        await page.screenshot(path="fingerprint_test.png")
        await page.close()

asyncio.run(main())
```

```python
# Configure specific fingerprint properties
from camoufox.sync_api import Camoufox

with Camoufox(
    os="windows",              # Spoof OS (windows, macos, linux)
    screen={"width": 1920, "height": 1080},
    locale="en-US",
) as browser:
    page = browser.new_page()
    page.goto("https://amiunique.org")
```

### 4.4 Camoufox vs Other Anti-Detect Browsers

| Browser | Open Source | Free | Based On | Automation Support |
|---------|-----------|------|----------|-------------------|
| **Camoufox** | Yes | Yes | Firefox | Playwright |
| **Multilogin** | No | No | Chromium/Firefox | Selenium, Playwright |
| **GoLogin** | No | Freemium | Chromium | Selenium |
| **AdsPower** | No | Freemium | Chromium | Selenium |

---

## 5. Disposable Services

### 5.1 Temporary Phone Numbers

Temporary or virtual phone numbers allow you to receive SMS messages without using your personal number. Common use cases include account verification, testing SMS-based workflows, and privacy protection.

**Recommended: https://temp-number.com/**

- Free temporary numbers from multiple countries
- Web-based interface, no registration required
- Numbers refresh periodically

**Alternatives:**

| Service | Free | Countries | Notes |
|---------|------|-----------|-------|
| **SMSReceiveFree** | Yes | US, UK, others | Public numbers, shared with all users |
| **ReceiveSMS** | Yes | Multiple | Web-based, no registration |
| **TextNow** | Yes (ad-supported) | US, Canada | Requires app install, own persistent number |
| **Google Voice** | Yes | US only | Requires existing US number to set up |

**Paid vs Free Comparison:**

| Feature | Free Services | Paid Services |
|---------|--------------|---------------|
| **Privacy** | Numbers shared publicly | Private, dedicated numbers |
| **Reliability** | Numbers expire quickly, shared | Persistent, guaranteed delivery |
| **Coverage** | Limited countries | Wide country selection |
| **Risk** | Numbers may be banned by services | Less likely to be flagged |
| **Cost** | Free | $0.50-$5.00 per number/verification |

### 5.2 Temporary Email

Temporary (disposable) email addresses provide one-time-use inboxes for avoiding spam, maintaining privacy during signups, and testing email workflows.

**Recommended**:  https://smailpro.com/

**Services:**

| Service | URL | Duration | Custom Domain | Features |
|---------|-----|----------|---------------|----------|
| **Guerrilla Mail** | guerrillamail.com | 1 hour | Yes (scramble) | Attachments, compose |
| **TempMail** | temp-mail.org | ~2 hours | Auto-generated | Simple, fast |
| **10MinuteMail** | 10minutemail.com | 10 min (extendable) | No | Quick verifications |
| **Mailinator** | mailinator.com | Several hours | Yes (public) | Public inboxes, API |
| **ThrowAwayMail** | throwawaymail.com | 48 hours | No | Longer retention |

**Self-Hosted Alternatives:**

For greater control and privacy, consider self-hosted email aliasing services:

- **SimpleLogin** (https://simplelogin.io) — Open source, self-hostable, alias-based forwarding, PGP encryption
- **AnonAddy / addy.io** (https://addy.io) — Open source, unlimited aliases, self-hostable
- **Firefox Relay** (https://relay.firefox.com) — Mozilla-backed, limited free aliases

```bash
# Quick curl to check a temp email inbox (Guerrilla Mail API)
# Get a temporary email address
curl -s "https://api.guerrillamail.com/ajax.php?f=get_email_address" | python3 -m json.tool

# Check inbox for messages
curl -s "https://api.guerrillamail.com/ajax.php?f=get_email_list&offset=0&sid_token=YOUR_TOKEN" | python3 -m json.tool
```

---

## 6. Comparison Table

| Tool/Service | Type | Free | Anonymity Level | Best For |
|-------------|------|------|-----------------|----------|
| **ProxyChains** | Proxy routing tool | Yes (open source) | High (depends on proxies) | Routing any tool through proxies |
| **Tor** | Anonymity network | Yes (open source) | Very High | Maximum anonymity for browsing/traffic |
| **spys.one** | Proxy list aggregator | Yes | Varies by proxy | Finding free public proxies |
| **Webshare** | Commercial proxy provider | Free tier (10 proxies) | High (paid proxies) | Reliable proxy access with API |
| **Camoufox** | Anti-fingerprint browser | Yes (open source) | High | Scraping, automation, fingerprint evasion |
| **temp-number.com** | Temp phone numbers | Yes | Medium | SMS verification bypass |
| **Guerrilla Mail** | Temp email | Yes | Medium | One-time email signups |
| **SimpleLogin** | Email aliasing | Freemium | High | Long-term email privacy |

---

## 7. See Also

- [VPN and ZTNA](../networking/vpn-and-ztna.md) — VPN services and Zero Trust Network Access solutions
- [Penetration Testing Tools](penetration-testing-tools.md) — Core tools for network and application security testing
