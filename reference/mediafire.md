# MediaFire — File Hosting & Sharing Platform

MediaFire is a free cloud file hosting and sharing service. It is widely used for distributing large files, ROM collections, software archives, and datasets without a time limit or mandatory login for download recipients.

- **Website:** https://www.mediafire.com
- **Founded:** 2006
- **Headquarters:** Shenandoah, Texas, USA
- **Storage:** 10 GB free, up to 100 GB paid

---

## Table of Contents
1. [Overview & Free Tier](#1-overview--free-tier)
2. [Uploading Files](#2-uploading-files)
3. [Sharing Links](#3-sharing-links)
4. [Folders & Organization](#4-folders--organization)
5. [MediaFire API](#5-mediafire-api)
6. [Downloading via CLI](#6-downloading-via-cli)
7. [Use Cases](#7-use-cases)
8. [Limitations & Gotchas](#8-limitations--gotchas)
9. [Comparison Table](#9-comparison-table)

---

## 1. Overview & Free Tier

MediaFire's free tier is notably generous compared to many competitors:

| Feature | Free | Pro ($3.75/mo) | Business ($40/mo) |
|---------|------|-----------------|-------------------|
| **Storage** | 10 GB | 1 TB | 100 TB |
| **Max file size** | 20 GB | 20 GB | 20 GB |
| **Bandwidth** | Unlimited | Unlimited | Unlimited |
| **Download wait** | None (no countdown timer) | None | None |
| **Direct links** | ✅ | ✅ | ✅ |
| **No account for download** | ✅ | ✅ | ✅ |
| **Ad-free downloads** | ❌ (ads shown) | ✅ | ✅ |
| **Custom subdomain** | ❌ | ✅ | ✅ |
| **Password protection** | ❌ | ✅ | ✅ |
| **One-time links** | ❌ | ❌ | ✅ |

**Key differentiators from competitors:**
- No download countdown timers on the free tier
- No file expiry — files persist as long as your account is active
- Recipients do not need a MediaFire account to download
- Supports files up to 20 GB per upload

---

## 2. Uploading Files

### Web Upload

1. Log in at https://www.mediafire.com
2. Click **Upload** (top navigation)
3. Drag and drop files or use the file picker
4. Files appear in your MediaFire Drive when complete

### Desktop App

MediaFire offers desktop apps for Windows and macOS that add a sync folder (like Dropbox) to your computer.

### Mobile App

Available on Android and iOS for uploading directly from your phone.

### Upload via API

See [§5 MediaFire API](#5-mediafire-api) for programmatic uploads.

---

## 3. Sharing Links

After uploading, every file gets a shareable link in the format:

```
https://www.mediafire.com/file/FILEID/filename.ext/file
```

**Getting the link:**
1. Click the file in your MediaFire Drive
2. Click **Share** or **Get Link**
3. Copy the public link

**Link types:**

| Type | Who can access | Availability |
|------|---------------|-------------|
| **Public link** | Anyone with the URL | Free |
| **Direct download link** | Bypasses MediaFire page (not reliably available) | See notes below |
| **Password-protected** | Only those with password | Pro+ |
| **Folder link** | Anyone — downloads entire folder or individual files | Free |

**Direct download link:**
MediaFire does not officially offer permanent direct download links on the free tier. However, tools like `wget` and `curl` with the `--content-disposition` flag can often trigger a direct download by following redirects.

---

## 4. Folders & Organization

MediaFire supports folder-based organization of files, and you can share entire folders as a single link.

**Folder link format:**
```
https://www.mediafire.com/folder/FOLDERID/FolderName
```

Recipients can browse the folder contents in a web interface and download individual files or the entire folder as a ZIP.

**Creating a folder:**
1. Click **New Folder** in your Drive
2. Upload files into it
3. Right-click the folder → **Share** to get a folder link

---

## 5. MediaFire API

MediaFire provides a REST API for programmatic file management.

- **API Docs:** https://www.mediafire.com/developers/core-api/

### Authentication

The API uses session tokens. Get a session token by authenticating with your email and password hash.

```python
import requests
import hashlib

def get_session_token(email: str, password: str) -> str:
    """Authenticate and get a MediaFire session token."""
    # MediaFire requires SHA-256 of (email + password + app_id + api_key)
    # For basic auth, use the simpler password hash approach
    password_hash = hashlib.sha256(password.encode()).hexdigest()[:10].upper()

    url = "https://www.mediafire.com/api/1.5/user/get_session_token.php"
    params = {
        "email": email,
        "password": password_hash,
        "application_id": "YOUR_APP_ID",   # Register at mediafire.com/developers
        "signature": "YOUR_SIGNATURE",
        "response_format": "json"
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data["response"]["session_token"]
```

### File Operations

```python
import requests

SESSION_TOKEN = "your_session_token"
BASE = "https://www.mediafire.com/api/1.5"

def get_file_info(quickkey: str) -> dict:
    """Get metadata for a file by its quickkey (the ID in the share link)."""
    r = requests.get(f"{BASE}/file/get_info.php", params={
        "quick_key": quickkey,
        "session_token": SESSION_TOKEN,
        "response_format": "json"
    })
    return r.json()["response"]["file_info"]

def get_folder_content(folder_key: str = "myfiles") -> list:
    """List files in a folder. 'myfiles' is the root folder."""
    r = requests.get(f"{BASE}/folder/get_content.php", params={
        "folder_key": folder_key,
        "content_type": "files",
        "session_token": SESSION_TOKEN,
        "response_format": "json"
    })
    return r.json()["response"]["folder_content"]["files"]

def get_links(quickkey: str) -> dict:
    """Get all download links for a file."""
    r = requests.get(f"{BASE}/file/get_links.php", params={
        "quick_keys": quickkey,
        "session_token": SESSION_TOKEN,
        "response_format": "json"
    })
    return r.json()["response"]["links"]

def delete_file(quickkey: str) -> bool:
    """Move a file to trash."""
    r = requests.post(f"{BASE}/file/delete.php", data={
        "quick_keys": quickkey,
        "session_token": SESSION_TOKEN,
        "response_format": "json"
    })
    return r.json()["response"]["result"] == "Success"
```

### Upload via API

```python
def upload_file(filepath: str, folder_key: str = None) -> dict:
    """Upload a file to MediaFire."""
    import os
    filename = os.path.basename(filepath)

    headers = {
        "x-filehash": compute_sha256(filepath),     # SHA-256 of file content
        "x-filename": filename,
        "x-filesize": str(os.path.getsize(filepath)),
        "x-session-token": SESSION_TOKEN,
    }
    if folder_key:
        headers["x-folder-key"] = folder_key

    url = "https://www.mediafire.com/api/1.5/upload/simple.php?response_format=json"
    with open(filepath, "rb") as f:
        r = requests.post(url, headers=headers, data=f)
    return r.json()
```

---

## 6. Downloading via CLI

MediaFire's download page is a standard HTML page with a download button. Automated downloading requires either the API or following the redirect chain.

```bash
# Using wget (follows redirects, works on many MediaFire links)
wget "https://www.mediafire.com/file/FILEID/filename.zip/file" \
  --content-disposition \
  --user-agent="Mozilla/5.0"

# Using curl with redirect following
curl -L -J -O \
  "https://www.mediafire.com/file/FILEID/filename.zip/file" \
  -H "User-Agent: Mozilla/5.0"

# Using gdown (originally for Google Drive but works for some services)
# pip install gdown

# Using aria2c (faster multi-connection download)
aria2c "https://www.mediafire.com/file/FILEID/filename.zip/file"
```

**Note:** MediaFire may redirect download requests through a confirmation page for large files. If direct wget/curl fails, try fetching the HTML page first, extracting the direct link from `a[href*="download"]`, then downloading that URL.

```python
# Python: Extract direct download URL from MediaFire page
import requests
from bs4 import BeautifulSoup

def get_mediafire_direct_link(page_url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    r = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    # Look for the download button anchor
    link = soup.find("a", id="downloadButton")
    if link:
        return link["href"]
    # Fallback: look for any download link
    for a in soup.find_all("a", href=True):
        if "download" in a["href"].lower():
            return a["href"]
    return None

direct = get_mediafire_direct_link("https://www.mediafire.com/file/FILEID/file.zip/file")
if direct:
    import subprocess
    subprocess.run(["wget", "-O", "output.zip", direct])
```

---

## 7. Use Cases

**Distributing large files publicly:**
MediaFire is popular for sharing ISOs, ROM packs, video files, and software archives. The lack of a download timer and no account requirement for recipients makes it more user-friendly than some alternatives.

**Backup storage:**
Use the desktop sync app or API to back up important files to 10 GB of free cloud storage.

**Game ROM and emulation communities:**
MediaFire is heavily used in emulation communities for hosting ROM archives, BIOS files, and emulator configurations.

**Sharing work files:**
For files too large to email, MediaFire folder links provide a simple way to share collections with clients or team members.

**Bulk media distribution:**
Musicians, podcasters, and video creators use MediaFire to host files for direct distribution where streaming platform policies are too restrictive.

---

## 8. Limitations & Gotchas

**No encryption at rest:** MediaFire does not offer client-side encryption. Files are stored unencrypted on MediaFire's servers. Do not store sensitive files without encrypting them yourself first.

**Terms of Service:** MediaFire prohibits illegal content, copyright infringement, adult content, and malware distribution. Files that violate ToS will be removed without notice.

**Account inactivity:** Free accounts that are inactive for long periods may have files deleted. Log in at least once every few months.

**Download throttling:** Free tier downloads may be throttled compared to Pro tier, though MediaFire claims "unlimited bandwidth."

**No password protection on free:** The free plan does not offer password-protected links — anyone with the URL can download the file.

**Link harvesting:** Because MediaFire links are non-expiring and public, they can be shared, indexed, and cached in ways you cannot control. Do not use MediaFire for private files you may want to revoke access to.

**DMCA takedowns:** MediaFire complies with DMCA takedown requests. Widely-shared files (especially ROMs, movies, software) are frequently taken down.

---

## 9. Comparison Table

| Service | Free Storage | Max File | Link Expiry | No Account to Download | Direct Links | E2E Encryption |
|---------|-------------|---------|-------------|----------------------|-------------|----------------|
| **MediaFire** | 10 GB | 20 GB | Never | ✅ | Sometimes | ❌ |
| **Google Drive** | 15 GB | 5 TB | Never | ✅ (public) | ❌ | ❌ |
| **Mega** | 20 GB | No limit | Never | ✅ | ✅ | ✅ |
| **WeTransfer** | N/A | 2 GB (free) | 7 days | ✅ | ✅ | ❌ |
| **Gofile** | Unlimited | No limit | ~10 days inactive | ✅ | ✅ | ❌ |
| **Catbox.moe** | Unlimited | 200 MB | Never | ✅ | ✅ | ❌ |
| **Archive.org** | Unlimited | No limit | Never | ✅ | ✅ | ❌ |
| **OnionShare** | Your disk | Your disk | Session only | ✅ (Tor) | ✅ | ✅ (Tor) |

### Quick Decision Guide

| Need | Recommendation |
|------|---------------|
| Large files (1-20 GB), no expiry, public sharing | **MediaFire** |
| Permanent archival, public domain content | **Archive.org** |
| Private encrypted cloud storage | **Mega** |
| Quick temporary share (under 2 GB) | **WeTransfer** |
| Anonymous sharing, no account | **OnionShare** |
| Tiny files with permanent direct links | **Catbox.moe** |
| Files for a project/team | **Google Drive** |

---

## See Also

- [Archive.org](archive-org.md) — Permanent free archival storage and the Wayback Machine
- [OnionShare](../networking/onionshare.md) — Anonymous file sharing over Tor
- [APIs & Resources](apis-and-resources.md) — Developer API reference
