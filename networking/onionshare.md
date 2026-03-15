# OnionShare — Anonymous File Sharing & Services over Tor

OnionShare is a free, open-source tool that lets you securely and anonymously share files, host websites, and set up chat rooms using the Tor network. Everything runs as a temporary `.onion` service — no accounts, no central servers, no third parties.

- **Website:** https://onionshare.org
- **Source:** https://github.com/onionshare/onionshare
- **License:** GPLv3
- **Developed by:** Micah Lee (journalist/security researcher, The Intercept)
- **Platforms:** Windows, macOS, Linux

---

## Table of Contents
1. [How OnionShare Works](#1-how-onionshare-works)
2. [Installation](#2-installation)
3. [Share Files](#3-share-files)
4. [Receive Files](#4-receive-files)
5. [Host a Website](#5-host-a-website)
6. [Chat Room](#6-chat-room)
7. [Persistent Addresses](#7-persistent-addresses)
8. [CLI Usage](#8-cli-usage)
9. [Security Model](#9-security-model)
10. [Comparison Table](#10-comparison-table)

---

## 1. How OnionShare Works

OnionShare runs a local web server on your machine and exposes it as a Tor `.onion` hidden service. The recipient accesses it using the Tor Browser. No files ever pass through a third-party server — the connection goes directly from the Tor network to your machine.

```
Traditional file sharing:
  You ──upload──▶ Cloud Server ◀──download── Recipient
  (server sees your file, your IP, recipient's IP)

OnionShare:
  You (OnionShare server)
    │
    └── Tor Circuit ──▶ Tor Network ──▶ Tor Circuit
                                              │
                                         Recipient (Tor Browser)
  (no intermediary sees the file or either party's real IP)
```

**Key properties:**
- Your real IP address is hidden from the recipient
- The recipient's IP is hidden from you
- Files are not stored anywhere except your own machine
- The `.onion` address is the access credential — anyone who has it can connect

---

## 2. Installation

```bash
# Ubuntu / Debian
sudo apt install onionshare

# Fedora
sudo dnf install onionshare

# macOS (Homebrew)
brew install --cask onionshare

# Windows / macOS
# Download installer from https://onionshare.org

# Flatpak (cross-distribution)
flatpak install flathub org.onionshare.OnionShare

# pip (CLI only)
pip install onionshare-cli
```

OnionShare bundles its own Tor process — you do not need to install Tor separately. However, recipients must use **Tor Browser** (https://www.torproject.org/download/) to access your `.onion` address.

---

## 3. Share Files

The most common use case: send files to someone without using email, cloud storage, or any intermediary.

**GUI steps:**
1. Open OnionShare → click **Share Files** tab
2. Drag and drop files or folders onto the window
3. Configure options (see below)
4. Click **Start Sharing**
5. Copy the generated `.onion` address and send it to the recipient
6. Recipient opens the address in Tor Browser → downloads the file(s)

**Options:**
- **Stop sharing after files have been sent** (default) — the server shuts down after the first successful download, preventing repeated access
- **Send individual files** — recipients can download files one at a time rather than as a ZIP
- **Use a password** — adds HTTP basic authentication to the `.onion` address

**What the recipient sees:**
A clean web interface listing your files with download buttons. No installation needed on their end beyond Tor Browser.

---

## 4. Receive Files

Turn your machine into a temporary secure dropbox. Others can upload files to you anonymously.

**Use case:** A journalist publishing a secure tip line. A team member submitting files without revealing their identity.

**GUI steps:**
1. Open OnionShare → click **Receive Files** tab
2. Set the save location (where uploaded files go on your disk)
3. Optionally require a password or disable text message submissions
4. Click **Start Receive Mode**
5. Share the `.onion` address — senders visit it in Tor Browser and upload files

**Options:**
- **Disable submitting text** — receive files only, no freeform messages
- **Disable uploading files** — receive text messages only

---

## 5. Host a Website

Serve a static website as a `.onion` site directly from your machine. No web hosting account or domain needed.

**Use case:** Temporary anonymous publications, whistleblowing pages, documentation that should only be accessible via Tor.

**GUI steps:**
1. Click **Host a Website** tab
2. Add your website files (HTML, CSS, JS, images)
3. OnionShare serves them as a static site over Tor
4. The `.onion` URL is your website address

**Limitations:**
- Static sites only (no server-side code execution)
- The site is only accessible while OnionShare is running on your machine
- For persistent sites, enable persistent addresses (see §7)

---

## 6. Chat Room

Create an ephemeral, encrypted, anonymous chat room — no accounts, no logs, no server retention.

**Use case:** Coordinating with sources, team communication when email is too risky.

**GUI steps:**
1. Click **Chat** tab
2. Click **Start Chat Server**
3. Share the `.onion` address
4. Participants open it in Tor Browser → they get a random codename automatically
5. Messages are not stored — when everyone disconnects, the conversation is gone

**Properties:**
- End-to-end encrypted via Tor
- No message history
- Participants are identified only by random codenames (no registration)
- Server shuts down when you close OnionShare

---

## 7. Persistent Addresses

By default, each OnionShare session generates a new random `.onion` address. Enable **Private Key** mode to keep the same address across sessions — useful for ongoing tip lines or sites.

**GUI:** Settings → Check **Use a persistent address**

The private key is stored locally. Back it up — if lost, you cannot recover the same `.onion` address.

```bash
# CLI — use a saved private key file
onionshare --persistent my-key.key --receive
```

---

## 8. CLI Usage

OnionShare includes a full CLI (`onionshare-cli`) for scripting and headless server use.

```bash
# Install CLI
pip install onionshare-cli

# Share a file
onionshare-cli document.pdf

# Share multiple files
onionshare-cli file1.txt file2.pdf /path/to/folder/

# Share and stop after first download (default behavior)
onionshare-cli --stop-after-first-download secret.zip

# Disable stop-after-download (allow multiple downloads)
onionshare-cli --no-autostop-sharing document.pdf

# Receive files (dropbox mode)
onionshare-cli --receive

# Host a website
onionshare-cli --website /path/to/site/

# Start a chat server
onionshare-cli --chat

# Add password protection
onionshare-cli --password "hunter2" document.pdf

# Persistent address
onionshare-cli --persistent ~/mykey.key document.pdf

# Verbose output (see connection events)
onionshare-cli --verbose document.pdf

# Use a custom Tor control port (if Tor is already running)
onionshare-cli --tor-control-port 9051 document.pdf
```

**Example output when sharing:**
```
OnionShare 2.6 | https://onionshare.org/

Connecting to the Tor network: 100% - Done
Setting up onion service on port 17614.

 * Running on http://127.0.0.1:17614
 * Running on http://onionsharebm5yqkj.onion

Files to share:
 - secret.pdf

Waiting for connections...
```

---

## 9. Security Model

### What OnionShare Protects Against

| Threat | Protected? | How |
|--------|-----------|-----|
| **Third-party server seeing your files** | ✅ | Files never leave your machine |
| **Your IP being revealed to recipient** | ✅ | Tor hides source IP |
| **Recipient's IP being revealed to you** | ✅ | Tor hides their IP too |
| **Traffic analysis by ISP** | ✅ | Tor encrypts and routes through relays |
| **File interception in transit** | ✅ | Tor provides end-to-end encryption |
| **Link being guessed/brute-forced** | ✅ | `.onion` addresses are 56-character random strings |

### Limitations and Risks

**Operational security is your responsibility.** OnionShare secures the transport, not the content or your behavior.

- **Malware in received files** — OnionShare does not scan files you receive. Open received files in a sandbox or air-gapped machine.
- **Metadata in shared files** — Documents, images, and videos may contain embedded metadata (GPS, author name, timestamps). Strip metadata before sharing sensitive files with `exiftool -all= file` or `mat2`.
- **Timing correlation attacks** — Nation-state adversaries may be able to correlate Tor traffic timing. For very high-risk use, add random delays.
- **The link itself is the secret** — Whoever has the `.onion` URL can access the service. Share it only through a secure channel (Signal, PGP email). Do not share it via SMS or unencrypted email.
- **Machine must stay on** — The `.onion` service only runs while OnionShare is open. If your machine sleeps or loses power, the service stops.
- **Tor Browser required for recipients** — Regular browsers cannot access `.onion` addresses. Recipients need Tor Browser.

### Comparison with SecureDrop

| Feature | OnionShare | SecureDrop |
|---------|-----------|------------|
| **Setup complexity** | Minutes | Days/weeks |
| **Requires dedicated server** | ❌ | ✅ |
| **Persistence** | Optional | Always-on |
| **For journalists** | Good for one-offs | Production tip lines |
| **Audit trail** | None | Full logging |
| **Best for** | Individuals, quick shares | Organizations, newsrooms |

---

## 10. Comparison Table

| Service | Anonymous | No Account | No Server | Encrypted | Files Expire | .onion Support |
|---------|-----------|-----------|-----------|-----------|-------------|----------------|
| **OnionShare** | ✅ | ✅ | ✅ (local) | ✅ (Tor) | ✅ | ✅ Native |
| **WeTransfer** | ❌ | ✅ | ❌ | TLS only | ✅ (7 days) | ❌ |
| **MediaFire** | ❌ | No | ❌ | TLS only | ❌ | ❌ |
| **Google Drive** | ❌ | ❌ | ❌ | TLS only | ❌ | ❌ |
| **Signal Note to Self** | ✅ (partial) | ❌ | ❌ | ✅ (E2E) | ❌ | ❌ |
| **SecureDrop** | ✅ | ✅ | ❌ (dedicated) | ✅ (Tor) | ❌ | ✅ |

### Quick Decision Guide

| Need | Recommendation |
|------|---------------|
| Send sensitive files to a specific person anonymously | **OnionShare share mode** |
| Accept anonymous tips / files from the public | **OnionShare receive mode** |
| Host a censorship-resistant anonymous site | **OnionShare website mode** |
| Ephemeral encrypted group chat, no accounts | **OnionShare chat mode** |
| Permanent anonymous website (full infrastructure) | **SecureDrop** or self-hosted Tor hidden service |
| Large files, no anonymity needed | **MediaFire** or **Archive.org** |

---

## See Also

- [VPN & ZTNA](vpn-and-ztna.md) — Tor, ProtonVPN, WireGuard, Tailscale for network-level anonymity
- [OPSEC & Proxies](../security/opsec-and-proxies.md) — ProxyChains, metadata stripping, compartmentalization
- [SSH Tunneling](ssh-tunneling.md) — Secure port forwarding without Tor
