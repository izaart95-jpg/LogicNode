# Email Clients — Thunderbird & Canary Mail

This document covers desktop and mobile email clients — applications that connect to email accounts via IMAP/SMTP and provide a local interface for reading, writing, and managing email. Unlike webmail, clients store mail locally, work offline, and give you control over your data.

---

## Table of Contents
1. [Email Client Fundamentals](#1-email-client-fundamentals)
2. [Mozilla Thunderbird](#2-mozilla-thunderbird)
3. [Canary Mail](#3-canary-mail)
4. [Comparison Table](#4-comparison-table)

---

## 1. Email Client Fundamentals

### IMAP vs POP3 vs SMTP

| Protocol | Port | Role |
|----------|------|------|
| **IMAP** | 993 (SSL) / 143 | Receive — syncs email between server and client, messages stay on server |
| **POP3** | 995 (SSL) / 110 | Receive — downloads email locally, typically deletes from server |
| **SMTP** | 465 (SSL) / 587 (STARTTLS) | Send outgoing email |

**Use IMAP** for all modern setups. It keeps messages synchronized across multiple devices and the server acts as the source of truth.

### Connection Security Settings

When configuring any email client:

| Setting | Value |
|---------|-------|
| **IMAP Port** | 993 with SSL/TLS |
| **SMTP Port** | 587 with STARTTLS, or 465 with SSL/TLS |
| **Authentication** | Normal password or OAuth2 |
| **Security** | Never use plain/unencrypted on port 143 or 25 |

### Common Provider IMAP/SMTP Servers

| Provider | IMAP Server | SMTP Server |
|----------|-------------|-------------|
| Gmail | `imap.gmail.com:993` | `smtp.gmail.com:587` |
| Outlook/Hotmail | `outlook.office365.com:993` | `smtp.office365.com:587` |
| ProtonMail | `127.0.0.1:1143` (via Bridge) | `127.0.0.1:1025` (via Bridge) |
| Tuta | Not supported (own apps only) | Not supported |
| FastMail | `imap.fastmail.com:993` | `smtp.fastmail.com:587` |
| Zoho | `imappro.zoho.com:993` | `smtppro.zoho.com:587` |

---

## 2. Mozilla Thunderbird

- **Website:** https://www.thunderbird.net
- **Developer:** Mozilla Foundation (MZLA Technologies Corporation)
- **License:** MPL 2.0 (open source)
- **Platforms:** Windows, macOS, Linux
- **Price:** Free

### Overview

Thunderbird is the most widely used open-source desktop email client. It is feature-rich, highly extensible via add-ons, supports PGP encryption natively (since version 78), and handles email, calendars, tasks, and chat in a single application.

### Installation

```bash
# Ubuntu/Debian
sudo apt install thunderbird

# Fedora
sudo dnf install thunderbird

# Arch
sudo pacman -S thunderbird

# Flatpak (cross-distribution)
flatpak install flathub org.mozilla.Thunderbird

# macOS
brew install --cask thunderbird

# Windows — download from https://www.thunderbird.net
```

### Account Setup

Thunderbird auto-detects settings for most major email providers:

1. **Menu → Account Settings → Account Actions → Add Mail Account**
2. Enter your name, email address, and password
3. Thunderbird queries Mozilla's ISPDB database for server settings automatically
4. For providers not in the database, click **Configure manually** and enter IMAP/SMTP settings

### PGP Encryption (OpenPGP)

Thunderbird has built-in OpenPGP support since version 78 — no Enigmail extension required.

```
Setup:
1. Account Settings → End-To-End Encryption
2. Click "Add Key" → Generate new key or import existing
3. Set the key for your account

Send encrypted email:
1. Compose a new message
2. Click the lock icon in the toolbar → Enable encryption
3. Thunderbird uses the recipient's published PGP key automatically
   (if they've published one to a keyserver)

Import a contact's public key:
1. Open an email from them
2. If they attached their public key → import it
3. Or: Tools → OpenPGP Key Manager → Import from keyserver
```

```bash
# Export your public key for sharing
# Tools → OpenPGP Key Manager → right-click your key → Export
# Share the .asc file with people you email

# Import a public key file
# OpenPGP Key Manager → File → Import Public Key(s)
```

### Calendar with CalDAV

Thunderbird includes **Lightning** (now integrated as Calendar) for CalDAV/iCalendar support:

1. **Calendar → New Calendar → On the Network → CalDAV**
2. Enter your CalDAV URL (e.g., from Fastmail, Nextcloud, ProtonCalendar via Bridge)
3. Thunderbird syncs events bidirectionally

### Useful Add-ons

| Add-on | Function | URL |
|--------|---------|-----|
| **Thunderbird Conversations** | Gmail-style threaded conversations | addons.thunderbird.net |
| **ImportExportTools NG** | Batch export/import .eml, .mbox | addons.thunderbird.net |
| **Cardbook** | Advanced CardDAV contact management | addons.thunderbird.net |
| **FileLink for Dropbox/NextCloud** | Large file attachment via cloud link | addons.thunderbird.net |

### Configuration Tips

```javascript
// Access advanced config: Help → Troubleshooting Info → profile folder
// Or: Edit → Settings → Advanced → Config Editor (about:config equivalent)

// Useful settings:
mail.compose.autosave = true          // Auto-save drafts
mail.compose.autosaveinterval = 5     // Save every 5 minutes
mailnews.default_sort_order = 2       // Sort newest first
mailnews.mark_message_read.delay = 5  // Mark read after 5 seconds
mail.spam.manualMark = true           // Manual junk marking
```

### Proton Bridge + Thunderbird Setup

To use Thunderbird with ProtonMail (requires paid Proton plan):

```
1. Install and log in to Proton Bridge
2. Bridge shows: IMAP port 1143, SMTP port 1025, and a Bridge password
3. In Thunderbird → Add Mail Account → Manual setup:
   - IMAP: 127.0.0.1, port 1143, SSL: None, Auth: Normal
   - SMTP: 127.0.0.1, port 1025, SSL: None, Auth: Normal
   - Username: your@proton.me
   - Password: Bridge-generated password (NOT your Proton login password)
4. Thunderbird now sends/receives via ProtonMail with full E2EE preserved
```

### Thunderbird on Android

Thunderbird for Android is now available (formerly K-9 Mail, acquired by Mozilla in 2022):

```
App Store / Google Play: search "Thunderbird"
Or: https://www.thunderbird.net/en-US/mobile/
```

It shares the Thunderbird name and branding but is a separate codebase optimized for mobile. Supports IMAP, POP3, multiple accounts, and OpenPGP encryption.

---

## 3. Canary Mail

- **Website:** https://canarymail.io
- **Developer:** Canary Mail Inc.
- **Platforms:** macOS, iOS, iPad OS, Windows (beta), Android (beta)
- **Price:** Free (basic), Pro (~$20/year or $2.49/month)

### Overview

Canary Mail is a modern, AI-powered email client designed for the Apple ecosystem (macOS and iOS). It emphasizes clean design, smart features like read receipts and send-later, and built-in S/MIME and PGP encryption. It is particularly popular among Apple users who want something more polished than Apple Mail with better security features than standard clients.

### Key Features

**AI email assistant (Copilot):** Canary includes an AI assistant that can summarize long email threads, draft replies, and categorize incoming mail. The AI runs on-device for free users, with cloud-based models available in Pro.

**End-to-end encryption:**
- **S/MIME:** Supported natively — request a free S/MIME certificate, import it, and your emails to other S/MIME users are encrypted and signed
- **PGP:** Full PGP support for encrypted email with external contacts
- **SecureSend:** Canary's own E2EE between Canary users, requiring no PGP key setup

```
S/MIME setup in Canary:
1. Settings → Encryption → S/MIME
2. Get a free certificate from Actalis or Comodo (personal use)
3. Import the .p12 certificate file
4. Canary automatically signs outgoing mail and encrypts to contacts whose certs you have
```

**Read receipts:** Know when your sent emails are opened (optional, can be turned off). Works without any recipient-side setup.

**Send later:** Schedule emails to send at a specific time.

**Snooze:** Temporarily hide emails and have them reappear at a time you choose.

**One-click unsubscribe:** Detects marketing emails and offers a one-tap unsubscribe.

**Focused Inbox:** AI-powered inbox filtering that separates important mail from newsletters and notifications.

**Multiple account support:** Manage Gmail, Outlook, iCloud, Yahoo, custom IMAP, ProtonMail (via Bridge), and Fastmail accounts from one interface.

### Plans

| Feature | Free | Pro (~$20/yr) |
|---------|------|--------------|
| **Accounts** | Unlimited | Unlimited |
| **AI features** | On-device (limited) | Cloud AI + advanced |
| **Read receipts** | 5/month | Unlimited |
| **Send later** | ✅ | ✅ |
| **Snooze** | ✅ | ✅ |
| **PGP/S/MIME** | ✅ | ✅ |
| **Priority support** | ❌ | ✅ |
| **Email templates** | ❌ | ✅ |

### Canary vs Apple Mail

| Feature | Canary | Apple Mail |
|---------|--------|-----------|
| **AI assistant** | ✅ | ❌ |
| **Read receipts** | ✅ | ❌ |
| **Send later** | ✅ | ✅ (macOS Ventura+) |
| **PGP** | ✅ | ❌ (plugin needed) |
| **S/MIME** | ✅ | ✅ |
| **Snooze** | ✅ | ❌ |
| **Smart inbox** | ✅ | Limited |
| **Price** | Free/Pro | Free (macOS built-in) |

---

## 4. Comparison Table

| Client | Platforms | Open Source | PGP | S/MIME | IMAP | Free | AI |
|--------|-----------|-------------|-----|--------|------|------|-----|
| **Thunderbird** | Win/Mac/Linux + Android | ✅ | ✅ | ✅ | ✅ | ✅ | Limited |
| **Canary Mail** | Mac/iOS/Win(beta) | ❌ | ✅ | ✅ | ✅ | Free/Pro | ✅ |
| **Apple Mail** | Mac/iOS | ❌ | ❌ | ✅ | ✅ | ✅ | Limited |
| **Outlook** | All | ❌ | ❌ | ✅ | ✅ | Paid | ✅ (Copilot) |
| **Fastmail** | Web/iOS/Android | ❌ | ❌ | ❌ | ✅ | Paid | ❌ |
| **K-9 Mail** | Android | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| **FairEmail** | Android | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

### Quick Decision Guide

| Need | Recommendation |
|------|---------------|
| Cross-platform open-source client | **Thunderbird** |
| macOS/iOS with modern UI and AI | **Canary Mail** |
| ProtonMail with desktop client | **Thunderbird + Proton Bridge** |
| Android email with PGP | **Thunderbird for Android** (K-9 successor) |
| Maximum privacy + open source | **Thunderbird** |

---

## See Also

- [Email Providers](email-providers.md) — ProtonMail, Tuta Mail — privacy-focused email services
- [OPSEC & Proxies](../security/opsec-and-proxies.md) — Temp email, anonymity practices
- [Network Protocols](../fundamentals/network-protocols.md) — SMTP, IMAP, POP3 protocol details
