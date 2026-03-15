# Mega.nz — Encrypted Cloud Storage

Mega.nz is a cloud storage and file sharing platform built around end-to-end encryption. Unlike most cloud storage services, Mega encrypts files client-side before they leave your device — Mega themselves cannot read your files. It offers one of the most generous free storage tiers available.

- **Website:** https://mega.nz
- **Founded:** 2013 by Kim Dotcom (now operated by Mega Limited, NZ)
- **Free Storage:** 20 GB (additional temporary bonus storage offered on signup)
- **Encryption:** AES-128 end-to-end (client-side)
- **Open Source:** Client-side cryptography is open source

---

## Table of Contents
1. [Free vs Paid Plans](#1-free-vs-paid-plans)
2. [Core Features](#2-core-features)
3. [Sharing Files & Folders](#3-sharing-files--folders)
4. [MEGAcmd — Command Line](#4-megacmd--command-line)
5. [MEGA API & SDK](#5-mega-api--sdk)
6. [Security Model](#6-security-model)
7. [Limitations & Gotchas](#7-limitations--gotchas)
8. [Comparison Table](#8-comparison-table)

---

## 1. Free vs Paid Plans

| Feature | Free | Pro I | Pro II | Pro III |
|---------|------|-------|--------|---------|
| **Storage** | 20 GB | 2 TB | 8 TB | 16 TB |
| **Transfer quota** | Limited | 2 TB/mo | 8 TB/mo | 16 TB/mo |
| **Max upload size** | Unlimited | Unlimited | Unlimited | Unlimited |
| **End-to-end encryption** | ✅ | ✅ | ✅ | ✅ |
| **File versioning** | ✅ | ✅ | ✅ | ✅ |
| **Chat (MEGAchat)** | ✅ | ✅ | ✅ | ✅ |
| **Price** | Free | ~€5/mo | ~€10/mo | ~€20/mo |

**Transfer quota:** Free accounts have a limited monthly transfer quota. When exceeded, recipients temporarily cannot download your shared files until the quota resets (after a few hours or the next day). Paid accounts have significantly higher limits.

---

## 2. Core Features

### End-to-End Encryption

All files are encrypted with AES-128 before leaving your device. The encryption key is derived from your account password. Mega holds encrypted data only — they have no access to your files, filenames, or folder structure.

**Important:** If you forget your password, your files are unrecoverable. Mega cannot reset your encryption key. Always export your Recovery Key from account settings and store it safely.

```
Your file → AES-128 encrypt (client-side) → upload encrypted blob → Mega servers
                                ↑
                    Key stored only in your browser/app
                    (Mega never sees the key)
```

### File Versioning

Mega keeps previous versions of files. If you overwrite a file, the previous version is retained and recoverable from the Versions section in file properties. Useful for accidental overwrites.

### MEGAchat

Built-in encrypted chat and video calls, accessible from the web app and mobile apps. Chat history is end-to-end encrypted.

### Multi-Device Sync

The MEGA desktop app syncs folders between your computer and your MEGA cloud storage. Supports selective sync (choose which folders to sync).

---

## 3. Sharing Files & Folders

### Public Links

Any file or folder can be shared as a public link. The encryption key is appended to the URL after a `#` — this is intentional and how end-to-end encryption works without requiring recipients to have an account.

```
https://mega.nz/file/FILEID#ENCRYPTIONKEY
https://mega.nz/folder/FOLDERID#ENCRYPTIONKEY
```

**The `#ENCRYPTIONKEY` part is never sent to Mega's servers** (browser fragment identifiers are not transmitted in HTTP requests). Mega only sees the file ID, not the key needed to decrypt it.

### Password-Protected Links

Add an extra password on top of the encryption key for additional protection:

1. Right-click file → Share → Get Link
2. Enable **Set password**
3. Enter a password — this re-encrypts the link key with your chosen password
4. Recipients need the password to access the file

### Expiry Dates

Pro accounts can set expiry dates on share links. Free accounts cannot.

### Collaboration

Share folders with specific Mega accounts for read-only or read-write collaboration. Changes sync in real-time across all collaborators.

---

## 4. MEGAcmd — Command Line

MEGAcmd is the official command-line tool for MEGA. It provides full access to your account from a terminal.

```bash
# Install MEGAcmd
# Ubuntu/Debian — download .deb from https://mega.nz/cmd
sudo apt install ./megacmd-*.deb

# Arch (AUR)
yay -S megacmd

# macOS
brew install --cask megacmd
```

### Authentication & Basic Navigation

```bash
# Login
mega-login your@email.com your_password

# Check account info and quota
mega-df -h

# List files in root
mega-ls /

# List with details
mega-ls -l /

# Change directory
mega-cd /MyFolder

# Print working directory
mega-pwd

# Logout
mega-logout
```

### File Operations

```bash
# Upload a file
mega-put file.zip /MyFolder/

# Upload a directory (recursive)
mega-put -r ./my-project/ /Backups/my-project/

# Download a file
mega-get /MyFolder/file.zip ./

# Download a folder (recursive)
mega-get -r /MyFolder ./local-folder/

# Copy
mega-cp /Source/file.zip /Destination/

# Move
mega-mv /Source/file.zip /Destination/

# Delete (moves to trash)
mega-rm /MyFolder/file.zip

# Delete permanently
mega-rm -f /MyFolder/file.zip

# Create folder
mega-mkdir /NewFolder
mega-mkdir -p /Parent/Child/GrandChild   # Create nested

# Get file info
mega-ls -l /MyFolder/file.zip
```

### Sharing

```bash
# Export a file as a public link (prints the shareable URL with key)
mega-export -a /MyFolder/file.zip

# Export a folder
mega-export -a /MyFolder/

# List existing shared links
mega-export /

# Remove a shared link
mega-export -d /MyFolder/file.zip

# Share a folder with a specific Mega user
mega-share -a --with=their@email.com /SharedFolder

# Share read-only
mega-share -a --with=their@email.com --level=0 /SharedFolder
```

### Sync

```bash
# Sync a local folder to MEGA
mega-sync /local/path /RemotePath

# List active syncs
mega-sync

# Remove a sync (stops syncing, does not delete files)
mega-sync -d /local/path
```

### Scripting Example: Automated Backup

```bash
#!/bin/bash
# Daily backup script using MEGAcmd

DATE=$(date +%Y-%m-%d)
BACKUP_NAME="backup-$DATE.tar.gz"
LOCAL_SOURCE="/home/user/important-data"
MEGA_DEST="/Backups"

# Create compressed archive
tar -czf "/tmp/$BACKUP_NAME" "$LOCAL_SOURCE"

# Upload to MEGA
mega-put "/tmp/$BACKUP_NAME" "$MEGA_DEST/"
echo "Backup uploaded: $MEGA_DEST/$BACKUP_NAME"

# Clean up old backups (keep last 7)
mega-ls -l "$MEGA_DEST" | awk '{print $NF}' | sort -r | tail -n +8 | while read f; do
    mega-rm "$MEGA_DEST/$f"
    echo "Deleted old backup: $f"
done

rm "/tmp/$BACKUP_NAME"
```

---

## 5. MEGA API & SDK

MEGA provides official SDKs for C++, Python, Android, iOS, and JavaScript.

```bash
# Python SDK
pip install mega.py
```

```python
from mega import Mega

mega = Mega()
m = mega.login("your@email.com", "your_password")

# Get account info
info = m.get_user()
print(f"Email: {info['email']}")
print(f"Storage used: {info['cstor']} bytes")

# Upload a file
file = m.upload("local_file.zip")
print(f"File ID: {file['f'][0]['h']}")

# Get a public link for the uploaded file
link = m.get_upload_link(file)
print(f"Share link: {link}")

# Find a file by name
file = m.find("filename.zip")

# Download a file by its node
m.download(file)

# Download from a public link
m.download_url("https://mega.nz/file/FILEID#KEY")

# Get all files
files = m.get_files()
for fh, f in files.items():
    if f.get("t") == 0:  # type 0 = file
        print(f["a"].get("n", "unknown"))  # filename
```

---

## 6. Security Model

### What Mega Protects Against

| Threat | Protected? | Notes |
|--------|-----------|-------|
| **Mega reading your files** | ✅ | Client-side AES-128 — they hold ciphertext only |
| **Server breach exposing content** | ✅ | Encrypted before upload |
| **Share link interception** | ✅ | Key in `#fragment` never sent to server |
| **Shared link access** | Partial | Anyone with the link can decrypt — share carefully |
| **Password-protected links** | ✅ | Extra encryption layer on the key |

### What Mega Does NOT Protect Against

- **Forgotten password** — your key is lost forever, files unrecoverable
- **Compromised browser/device** — if malware is on your machine, files can be read before encryption
- **Account metadata** — Mega knows when you log in, file sizes, folder structure (names are encrypted but the tree structure is visible to Mega)
- **Legal requests** — Mega is subject to New Zealand law and responds to valid court orders (though they cannot decrypt file content, they can hand over metadata and account information)

---

## 7. Limitations & Gotchas

**Transfer quota throttling:** Free accounts have strict monthly transfer limits. When exceeded, downloads of your shared files fail for recipients until quota resets. This is the biggest practical limitation of the free tier for public file sharing.

**Password recovery is impossible:** Unlike most services, Mega cannot reset your password because they don't hold your decryption key. If you forget your password without a saved Recovery Key, your files are permanently inaccessible.

**Link key in URL:** The encryption key is in the shareable URL. If you post a Mega link somewhere, anyone who sees the full URL (including the `#KEY` part) can download and decrypt the file. Be careful where you share links.

**Browser extension:** Mega works better with the official MEGA browser extension installed, which speeds up transfers and reduces memory usage for large files.

**Free storage bonuses expire:** Signup bonuses (sometimes 35-50 GB additional) expire after a set period, leaving you with the base 20 GB.

---

## 8. Comparison Table

| Service | Free Storage | Encryption | No-Account Download | CLI Tool | API |
|---------|-------------|------------|--------------------|---------|----|
| **Mega.nz** | 20 GB | ✅ E2E | ✅ (with link) | ✅ MEGAcmd | ✅ |
| **Google Drive** | 15 GB | ❌ | ✅ (public) | ✅ | ✅ |
| **Dropbox** | 2 GB | ❌ | ✅ | ✅ | ✅ |
| **ProtonDrive** | 1 GB | ✅ E2E | ❌ (requires account) | Limited | ✅ |
| **MediaFire** | 10 GB | ❌ | ✅ | ❌ | ✅ |
| **Gofile** | Unlimited (10d) | ❌ | ✅ | ❌ | ✅ |
| **OnionShare** | Your disk | ✅ Tor | ✅ | ✅ | N/A |

---

## See Also

- [Gofile](gofile.md) — Anonymous unlimited-size file hosting
- [MediaFire](mediafire.md) — Commercial file hosting with no-expiry free tier
- [OnionShare](../networking/onionshare.md) — Anonymous file sharing over Tor
- [Archive.org](archive-org.md) — Permanent public archival storage
