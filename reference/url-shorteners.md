# URL Shorteners

URL shorteners convert long URLs into compact links, track click analytics, and in some cases monetize traffic. This document covers earning-based shorteners, free shorteners, the underlying technology, and self-hosting options.

---

## Table of Contents
1. [Overview](#1-overview)
2. [Shrink.pe](#2-shrinkpe)
3. [ShrinkEarn](#3-shrinkearn)
4. [Other Notable Shorteners](#4-other-notable-shorteners)
5. [How URL Shortening Works](#5-how-url-shortening-works)
6. [Self-Hosting](#6-self-hosting)

---

## 1. Overview

| Type | Model | Examples |
|------|-------|---------|
| **Free/clean** | No ads, direct redirect | TinyURL, is.gd |
| **Earning** | Interstitial ad before redirect, pay per 1K views | Shrink.pe, ShrinkEarn, AdFly |
| **Analytics** | Track clicks, geo, device | Bit.ly, Rebrandly |
| **Self-hosted** | Full control, custom domain | YOURLS, Shlink, Kutt |
| **Temporary** | Link expires after time/clicks | Some free tiers |

---

## 2. Shrink.pe

- **Website:** https://shrink.pe
- **Model:** Ad-based earning — interstitial ad shown before redirect
- **Payout:** CPM (per 1,000 views), varies by country
- **Minimum withdrawal:** Low threshold; supports PayPal, crypto, bank transfer
- **API:** REST API for programmatic link creation

### Features

- Unlimited URL shortening
- Custom alias support (`shrink.pe/my-link`)
- Analytics dashboard — clicks, countries, referrers, devices
- Bulk shortening via API
- Password-protected links
- Link expiry by date or click count
- Real-time earning stats

### API Usage

```bash
# Shorten a URL
curl "https://shrink.pe/api?api=YOUR_API_KEY&url=https://example.com/long-url"

# Response:
# { "status": "success", "shortenedUrl": "https://shrink.pe/AbCdEf" }
```

```python
import requests

def shorten(api_key, url):
    r = requests.get("https://shrink.pe/api",
                     params={"api": api_key, "url": url})
    return r.json().get("shortenedUrl")
```

### Approximate Earning Rates (CPM)

| Traffic Region | Per 1,000 views |
|---------------|----------------|
| US / UK / CA / AU | $2–$5 |
| EU | $1–$3 |
| IN / PK / BD | $0.50–$1.50 |
| Other | $0.20–$0.80 |

---

## 3. ShrinkEarn

- **Website:** https://shrinkearn.com
- **Model:** Monetized link shortening with interstitial ads
- **Payout:** CPM rates via PayPal, Payoneer, bank transfer
- **Minimum payout:** ~$5
- **Referral:** Earn a percentage of referral earnings

### Features

- Free to use — earn from your audience's clicks
- Custom short domain option
- Full real-time analytics (clicks, country, device)
- REST API for automated shortening
- AdBlock detection — may serve alternate experience to users with blockers

### API Usage

```bash
curl "https://shrinkearn.com/api?api=YOUR_API_KEY&url=https://example.com"
```

```python
import requests
resp = requests.get("https://shrinkearn.com/api",
                    params={"api": "KEY", "url": "https://target.com"})
data = resp.json()
print(data.get("shortenedUrl"))
```

---

## 4. Other Notable Shorteners

| Service | Best For | Notes |
|---------|---------|-------|
| **Bit.ly** | Analytics, branded links | Free tier limited; full features paid |
| **TinyURL** | Simplest possible redirect | No account needed, no tracking |
| **is.gd / v.gd** | Clean API redirects | No ads, API available, privacy-friendly |
| **Rebrandly** | Custom branded domains | `brand.ly/link` style |
| **Kutt.it** | Self-hosted or free cloud | Open source, full-featured |
| **t.ly** | Tracking + QR codes | QR generation built in |
| **AdFly** | Earning (older) | Established platform |
| **LinkVertise** | Earning + content locking | Common in game/software download communities |

---

## 5. How URL Shortening Works

```
User visits: https://shrink.pe/AbCdEf

1. DNS: shrink.pe → server IP
2. HTTP GET /AbCdEf
3. Server looks up "AbCdEf" in database:
     { short: "AbCdEf", target: "https://example.com/long", clicks: 1234 }
4a. Clean redirect:
     HTTP 301/302 Location: https://example.com/long
     → browser follows immediately

4b. Earning interstitial:
     HTTP 200 → serve ad page
     Ad counts impression → after ~5 seconds → JS redirects to target
     Or user clicks "Skip" → redirect
```

### Short ID Generation

```
Option 1: Sequential base62 encoding
  ID 1000000 → encode in base62 (a-zA-Z0-9) → "4c92"
  Fast lookup, predictable length growth

Option 2: Random 6–8 char base62 string
  Collision-checked before inserting into DB

Option 3: Hash of URL
  SHA-256 of URL → first 6 base62 chars
  Deterministic — same URL always gets same short code
  Risk: hash collisions for different URLs (rare but handled)
```

### Redirect HTTP Status Codes

| Code | Type | Browser Cache | SEO |
|------|------|--------------|-----|
| **301** | Permanent | Yes — cached forever | Link equity passes to target |
| **302** | Temporary | No caching | No SEO transfer |
| **307** | Temporary (method-safe) | No | No SEO transfer |
| **JS redirect** | Via `window.location` | No | Not followed by crawlers |
| **Meta refresh** | `<meta http-equiv="refresh">` | No | Weak/no SEO |

Earning shorteners use JavaScript redirect after showing the ad, bypassing HTTP redirect entirely — this is intentional to prevent direct navigation to the target.

---

## 6. Self-Hosting

### YOURLS (PHP, lightweight)

```bash
# Requirements: PHP 7.4+, MySQL/MariaDB
git clone https://github.com/YOURLS/YOURLS.git
cd YOURLS/user
cp config-sample.php config.php
# Edit: DB credentials, YOURLS_SITE, admin user/password

# Nginx config
server {
    server_name short.example.com;
    root /var/www/yourls;
    location / {
        try_files $uri $uri/ /yourls-loader.php$is_args$args;
    }
}

# API
curl "https://short.example.com/yourls-api.php?signature=SIG&action=shorturl&url=https://example.com&format=json"
```

### Shlink (PHP, Docker, modern REST API)

```bash
docker run -d \
  -p 8080:8080 \
  -e DEFAULT_DOMAIN=short.example.com \
  -e DB_DRIVER=mysql \
  -e DB_HOST=db \
  -e DB_NAME=shlink \
  -e DB_USER=shlink \
  -e DB_PASSWORD=secret \
  shlinkio/shlink:stable

# CLI management
docker exec shlink_container shlink short-url:create https://example.com
docker exec shlink_container shlink short-url:list
```

### Kutt (Node.js, full dashboard)

```bash
git clone https://github.com/thedevs-network/kutt.git
cd kutt
cp .env.example .env    # Configure DB, Redis, JWT secret, domain
docker-compose up -d
# Dashboard: http://localhost:3000
```

---

## See Also

- [Platforms & Communities](platforms-and-communities.md) — Social platforms and content sharing
- [APIs & Resources](../devtools/apis-and-resources.md) — REST API patterns
- [Web Automation](../automation/web-automation.md) — Automating link generation at scale
