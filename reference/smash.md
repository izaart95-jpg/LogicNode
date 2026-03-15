# Smash — Large File Transfer Service

Smash is a file transfer service designed for sending large files easily. Unlike traditional cloud storage, Smash is optimized for the transfer workflow: upload once, send a link, recipient downloads, done. No account required for the sender on the free tier.

- **Website:** https://fromsmash.com
- **Type:** File transfer (send-focused, not storage-focused)
- **Account Required:** No (free tier), optional (account for tracking/management)
- **Max File Size:** Unlimited (free), with bandwidth and expiry restrictions
- **Encryption:** TLS in transit, AES-256 at rest

---

## Table of Contents
1. [Free vs Paid Plans](#1-free-vs-paid-plans)
2. [How Smash Works](#2-how-smash-works)
3. [Sending Files](#3-sending-files)
4. [Smash API](#4-smash-api)
5. [Use Cases](#5-use-cases)
6. [Limitations & Gotchas](#6-limitations--gotchas)
7. [Comparison Table](#7-comparison-table)

---

## 1. Free vs Paid Plans

| Feature | Free | Premium (~€6/mo) | Business (custom) |
|---------|------|------------------|-------------------|
| **Max file size** | Unlimited | Unlimited | Unlimited |
| **Transfer expiry** | 14 days | 1 year | Custom |
| **Password protection** | ❌ | ✅ | ✅ |
| **Custom link** | ❌ | ✅ | ✅ |
| **Download tracking** | ❌ | ✅ | ✅ |
| **Remove Smash branding** | ❌ | ✅ | ✅ |
| **Custom domain** | ❌ | ❌ | ✅ |
| **API access** | Limited | ✅ | ✅ |

**Key differentiator from competitors:** Smash has no file size limit on any plan — including free. The constraints on the free tier are about expiry (14 days) and features, not file size.

---

## 2. How Smash Works

Smash is transfer-centric, not storage-centric. The mental model is closer to WeTransfer than to Dropbox or Google Drive.

```
Sender uploads file → Smash generates a link → Sender shares link → Recipient downloads
                                                                       (link expires in 14 days)
```

Files are stored on Smash's infrastructure in AES-256 encrypted form during the active transfer period. After expiry, files are permanently deleted.

---

## 3. Sending Files

### Web Interface

1. Visit https://fromsmash.com
2. Drag and drop files or folders onto the upload area
3. Optionally add recipient email addresses (Smash will send them the link directly)
4. Click **Transfer** — Smash uploads and generates a link
5. Share the link with recipients

The link format:
```
https://fromsmash.com/TRANSFERID
```

### Email Integration

Smash can send the download link directly to recipient email addresses. You enter the email addresses before clicking Transfer. Recipients get a nicely formatted email with the download link — no Smash account required on their end.

### Tracking Downloads (Premium)

Premium users can see when recipients download the file, how many times it was downloaded, and from which locations. Free users have no download visibility.

---

## 4. Smash API

Smash provides a REST API for integrating file transfers into applications and automating uploads.

- **API Docs:** https://api.fromsmash.com/docs
- **Authentication:** API key (from account dashboard)

```bash
# Upload a file via API
curl -X POST https://api.fromsmash.com/v1/transfers \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [{"name": "report.pdf", "size": 1048576}],
    "availabilityDuration": 14
  }'
# Returns upload URL and transfer ID

# Then upload the actual file to the returned URL
curl -X PUT "UPLOAD_URL_FROM_RESPONSE" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @report.pdf
```

```python
import requests

API_KEY = "your_api_key"
BASE = "https://api.fromsmash.com/v1"

def create_transfer(filename: str, filesize: int, days: int = 14) -> dict:
    """Create a transfer and get an upload URL."""
    r = requests.post(
        f"{BASE}/transfers",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "files": [{"name": filename, "size": filesize}],
            "availabilityDuration": days
        }
    )
    return r.json()

def upload_file(filepath: str, days: int = 14) -> str:
    """Upload a file to Smash and return the shareable link."""
    import os
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    # Create transfer
    transfer = create_transfer(filename, filesize, days)
    upload_url = transfer["files"][0]["uploadUrl"]
    transfer_id = transfer["id"]

    # Upload file content
    with open(filepath, "rb") as f:
        requests.put(
            upload_url,
            headers={"Content-Type": "application/octet-stream"},
            data=f
        )

    return f"https://fromsmash.com/{transfer_id}"

link = upload_file("/path/to/largefile.zip")
print(f"Share link: {link}")
```

### Node.js SDK

```bash
npm install @smash-sdk/uploader
```

```javascript
const { Uploader } = require("@smash-sdk/uploader");

const uploader = new Uploader({
    token: "YOUR_API_KEY",
    files: ["./large-file.zip"],
    availabilityDuration: 14
});

uploader.on("progress", (progress) => {
    console.log(`Upload progress: ${progress.percent}%`);
});

uploader.on("finish", (transfer) => {
    console.log(`Transfer link: https://fromsmash.com/${transfer.id}`);
});

await uploader.start();
```

---

## 5. Use Cases

**Sending large video files:** Smash is widely used by video editors and creative professionals for delivering raw footage, final renders, and project files to clients. No size limit means a 100 GB export is as easy to send as a 100 MB file.

**Client file delivery:** The email notification feature makes Smash feel professional for sending deliverables to clients — they receive a clean email with a download button, not a raw link.

**One-time large file sharing:** When you need to send something big to someone once and don't need permanent hosting, Smash's 14-day free tier is ideal.

**Replacing FTP for creative handoff:** Many agencies use Smash as a simpler alternative to FTP or SFTP for delivering assets to partners.

---

## 6. Limitations & Gotchas

**14-day expiry on free tier:** Files are deleted after 14 days. Smash is a transfer service, not a storage service. Do not use it as a backup or permanent hosting solution.

**No password protection on free:** The link is publicly accessible to anyone who has it. For sensitive files, upgrade to Premium for password-protected transfers.

**Bandwidth limitations:** Free transfers may be throttled compared to paid plans on download speed, particularly for large files during peak times.

**No anonymous upload tracking:** Free users cannot see if or when their transfer was downloaded.

**Account not required — but token needed for API:** The web interface works without an account, but API access requires an API key, which requires creating a free account.

---

## 7. Comparison Table

| Service | Max File Size | Free Expiry | No Account | Password | Email Notify |
|---------|-------------|-------------|-----------|----------|--------------|
| **Smash** | Unlimited | 14 days | ✅ | Paid only | ✅ (web) |
| **WeTransfer** | 2 GB | 7 days | ✅ | Paid | ✅ |
| **Gofile** | Unlimited | 10 days (guest) | ✅ | Paid | ❌ |
| **MediaFire** | 20 GB | Never | ✅ | Paid | ❌ |
| **Mega.nz** | None | Never | ❌ | ✅ | ❌ |
| **Send.vis.ee** | 2.5 GB | 7 days | ✅ | ✅ | ❌ |

### Quick Decision Guide

| Need | Recommendation |
|------|---------------|
| Send a huge file once (no account) | **Smash** |
| Permanent hosting of large files | **Gofile** or **MediaFire** |
| Encrypted permanent storage | **Mega.nz** |
| Maximum privacy, no third party | **OnionShare** |
| Quick small file send | **WeTransfer** |

---

## See Also

- [Gofile](gofile.md) — Anonymous unlimited-size file hosting, no expiry with account
- [Mega.nz](mega-nz.md) — Encrypted cloud storage with generous free quota
- [MediaFire](mediafire.md) — Commercial file hosting with no-expiry free tier
