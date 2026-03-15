# Privacy-Focused Email Providers

This document covers privacy-first encrypted email providers — services built around protecting your communications from surveillance, data harvesting, and unauthorized access. Unlike Gmail or Outlook, these providers cannot read your emails and do not monetize your data.

---

## Table of Contents
1. [Why Privacy Email?](#1-why-privacy-email)
2. [ProtonMail](#2-protonmail)
3. [Tuta Mail](#3-tuta-mail)
4. [Comparison Table](#4-comparison-table)
5. [Migration Tips](#5-migration-tips)

---

## 1. Why Privacy Email?

Standard email providers (Gmail, Outlook, Yahoo) scan your emails to serve ads, may comply with government requests, and store your messages in a way they can read. Privacy email providers address this with:

- **End-to-end encryption (E2EE):** Messages encrypted so only sender and recipient can read them — the provider cannot
- **Zero-knowledge architecture:** Provider holds encrypted data but not the keys to decrypt it
- **No ad-based business model:** Revenue from subscriptions, not from reading your data
- **Jurisdiction:** Switzerland (Proton) and Germany (Tuta) have stronger privacy laws than the US

**Important caveat:** E2EE only applies between users of the same provider, or when using PGP with external contacts. Email to/from Gmail is standard unencrypted SMTP unless you use PGP.

---

## 2. ProtonMail

- **Website:** https://proton.me/mail
- **Company:** Proton AG
- **Founded:** 2013 at CERN (Geneva, Switzerland)
- **Jurisdiction:** Switzerland (strong privacy laws, not in EU/US)
- **Encryption:** E2EE between Proton users; PGP with external users

### Free vs Paid Plans

| Feature | Free | Mail Plus (~€3.99/mo) | Proton Unlimited (~€9.99/mo) |
|---------|------|----------------------|------------------------------|
| **Storage** | 1 GB | 15 GB | 500 GB |
| **Email addresses** | 1 | 10 | 15+ |
| **Custom domain** | ❌ | ✅ | ✅ |
| **Folders/Labels** | Limited | Unlimited | Unlimited |
| **ProtonVPN** | Free tier | ❌ | ✅ |
| **ProtonDrive** | 1 GB | ❌ | ✅ |
| **ProtonCalendar** | ✅ | ✅ | ✅ |
| **Bridge (IMAP)** | ❌ | ✅ | ✅ |
| **Priority support** | ❌ | ✅ | ✅ |

### Key Features

**Zero-access encryption:** All emails are encrypted server-side with your key. Even emails from non-Proton senders are encrypted when stored — Proton cannot read your inbox.

**Proton-to-Proton E2EE:** Emails between Proton accounts are automatically end-to-end encrypted. No setup required.

**PGP support:** Proton supports PGP for encrypted communication with external email users. You can import external PGP keys, and Proton automatically encrypts outgoing mail to contacts whose PGP public keys are known.

**Password-protected emails:** Send encrypted emails to non-Proton users. The recipient receives a link and needs a password (shared separately) to read the message.

**Self-destructing messages:** Set an expiry time on emails — they are automatically deleted after the set period.

**Proton Bridge:** A local IMAP/SMTP bridge that lets you use Proton with desktop email clients like Thunderbird or Apple Mail. **Requires a paid plan.**

```bash
# Install Proton Bridge (Linux)
# Download from https://proton.me/mail/bridge
# Available as .deb, .rpm, or AppImage

# After installing and logging in, configure Thunderbird:
# IMAP server: 127.0.0.1, port 1143
# SMTP server: 127.0.0.1, port 1025
# Username: your Proton email
# Password: Bridge-generated password (shown in Bridge app)
```

**Import Assistant:** Tool for migrating your existing email from Gmail, Outlook, or other services to Proton. Available at https://proton.me/support/import-assistant.

### Proton Ecosystem

Proton has expanded beyond email into a full privacy suite:

| Product | Function | Free |
|---------|---------|------|
| **Proton Mail** | Encrypted email | 1 GB |
| **Proton VPN** | VPN service | ✅ (limited servers) |
| **Proton Drive** | Encrypted cloud storage | 1 GB |
| **Proton Calendar** | Encrypted calendar | ✅ |
| **Proton Pass** | Password manager | ✅ (limited) |

**SimpleLogin integration:** Proton acquired SimpleLogin, an email alias service. Generate throwaway aliases that forward to your Proton inbox — useful for signups.

### Accessing Proton Mail

```bash
# Web app
# https://mail.proton.me

# Desktop app (Windows, macOS, Linux)
# https://proton.me/mail/download

# Mobile (iOS, Android)
# App Store / Google Play

# Tor hidden service (maximum anonymity)
# https://protonmailrmez3lotccipshtkleegetolb73fuirgj7r4o4vfu7ozyd.onion
```

### API Usage (Proton does not offer a public REST API)

Proton does not provide a public API for third-party email access. The Proton Bridge provides IMAP/SMTP access for desktop clients (paid plans only). For automation, use Bridge with `imaplib` in Python:

```python
import imaplib, email

# Requires Proton Bridge running with a paid Proton account
mail = imaplib.IMAP4('127.0.0.1', 1143)
mail.login('your@proton.me', 'BRIDGE_PASSWORD')
mail.select('INBOX')

# Fetch recent emails
_, messages = mail.search(None, 'ALL')
for num in messages[0].split()[-5:]:
    _, data = mail.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    print(f"From: {msg['From']}")
    print(f"Subject: {msg['Subject']}")
```

---

## 3. Tuta Mail

- **Website:** https://tuta.com
- **Company:** Tutao GmbH
- **Founded:** 2011 (Hannover, Germany)
- **Jurisdiction:** Germany (GDPR, strict German privacy laws)
- **Encryption:** E2EE with proprietary protocol (not PGP)
- **Open Source:** ✅ Fully open source (GitHub: https://github.com/tutao/tutanota)

### Free vs Paid Plans

| Feature | Free | Revolutionary (~€3/mo) | Legend (~€8/mo) |
|---------|------|------------------------|-----------------|
| **Storage** | 1 GB | 20 GB | 500 GB |
| **Email addresses** | 1 | 15 | 30 |
| **Custom domain** | ❌ | ✅ | ✅ |
| **Aliases** | 1 | Unlimited | Unlimited |
| **Calendar** | ✅ | ✅ | ✅ |
| **Contact management** | ✅ | ✅ | ✅ |
| **Priority support** | ❌ | ✅ | ✅ |
| **Multiple accounts** | ❌ | 3 | 6 |

**Tuta does not offer paid plans in USD/EUR equivalent to major providers — it is considerably cheaper than Proton for comparable storage.**

### Key Features

**Full end-to-end encryption:** Tuta encrypts not just the email body but also subject lines, attachment names, and contact/calendar data. This is more comprehensive than Proton's default encryption (Proton only encrypts subject lines by default with extra setting).

**Proprietary encryption protocol:** Unlike Proton which uses PGP, Tuta uses its own AES-128 + RSA-2048 based system. This means Tuta users cannot directly exchange encrypted email with PGP users without a workaround — but it allows Tuta to encrypt subject lines and more metadata.

**Encrypted calendar and contacts:** Tuta Calendar and Tuta Contacts are fully end-to-end encrypted, including event titles, descriptions, and contact details.

**Password-protected external emails:** Like Proton, Tuta can send password-protected emails to non-Tuta recipients. The recipient gets a link and enters a password to read the message in a browser — the message is never transmitted unencrypted.

**No IP logging:** Tuta does not log user IP addresses by default. This is a stronger privacy stance than Proton (Proton logs IPs for abuse prevention with some exceptions).

**Fully open source:** Both the client and server code are open source and available on GitHub for audit.

```bash
# Accessing Tuta
# Web: https://app.tuta.com
# Desktop: https://tuta.com/download
# Mobile: iOS App Store / Google Play / F-Droid
# F-Droid: Available for Android without Google Play
```

### Tuta Limitations Compared to Proton

- **No IMAP/SMTP bridge:** Tuta does not support IMAP or SMTP. You cannot use Tuta with Thunderbird, Apple Mail, or any standard email client. Tuta-only apps only.
- **No PGP:** Tuta's proprietary encryption cannot interoperate with PGP. If you need to exchange encrypted email with external PGP users, Proton is more suitable.
- **No email import tool:** Migrating existing email into Tuta is more difficult — no official import assistant.

---

## 4. Comparison Table

| Feature | ProtonMail | Tuta Mail | Gmail | Outlook |
|---------|-----------|----------|-------|---------|
| **Free storage** | 1 GB | 1 GB | 15 GB | 15 GB |
| **E2EE (same provider)** | ✅ | ✅ | ❌ | ❌ |
| **E2EE subject line** | Optional | ✅ Default | ❌ | ❌ |
| **PGP support** | ✅ | ❌ | ❌ (via extension) | ❌ |
| **Open source** | Partial | ✅ Full | ❌ | ❌ |
| **IMAP/SMTP** | ✅ (paid, Bridge) | ❌ | ✅ | ✅ |
| **IP logging** | Some | ❌ | Yes | Yes |
| **Custom domain** | Paid | Paid | Paid (Workspace) | Paid |
| **Jurisdiction** | Switzerland | Germany | USA | USA |
| **Business model** | Subscriptions | Subscriptions | Advertising | Advertising |
| **Self-destructing mail** | ✅ | ❌ | ❌ | ❌ |
| **Tor .onion address** | ✅ | ❌ | ❌ | ❌ |

### Quick Decision Guide

| Need | Recommendation |
|------|---------------|
| Best free privacy email, no IMAP needed | **Tuta** (more comprehensive encryption) |
| Need IMAP/Thunderbird compatibility | **ProtonMail** (Bridge, paid) |
| Need PGP with external contacts | **ProtonMail** |
| Open-source auditable client | **Tuta** (fully open source) |
| Broadest privacy ecosystem (VPN, Drive) | **ProtonMail** |
| Minimum IP logging | **Tuta** |
| Migrating existing email | **ProtonMail** (Import Assistant) |

---

## 5. Migration Tips

**From Gmail to Proton:**
1. Use Proton's Import Assistant (https://proton.me/support/import-assistant)
2. Connect Gmail via OAuth
3. Select date range and folders to import
4. Proton imports and encrypts all messages

**From Gmail to Tuta:**
- No official import tool
- Manual option: Export Gmail via Google Takeout (`.mbox` format), then use third-party tools to convert and import — this is not straightforward
- Easiest: set up email forwarding from Gmail to Tuta while you transition, and use both during the migration period

**Custom domain setup:**
Both providers support using your own domain (paid plans). Add MX records pointing to the provider's mail servers, then create addresses under your domain.

---

## See Also

- [Email Clients](email-clients.md) — Thunderbird, Canary Mail — desktop and mobile email apps
- [OPSEC & Proxies](../security/opsec-and-proxies.md) — Disposable email, temp addresses, anonymity practices
- [VPN & ZTNA](../networking/vpn-and-ztna.md) — ProtonVPN and other VPN services
