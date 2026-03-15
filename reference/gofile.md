# Gofile — Free Anonymous File Hosting

Gofile is a free, anonymous file hosting service with no file size limits, no account requirement for uploading, and no artificial download wait times. Files are stored until there is no activity on them for 10 days (guest uploads) or indefinitely for account holders.

- **Website:** https://gofile.io
- **Type:** Free file hosting
- **Account Required:** No (guest upload), optional (account extends retention)
- **Max File Size:** Unlimited
- **API:** Full REST API available

---

## Table of Contents
1. [Free vs Account Usage](#1-free-vs-account-usage)
2. [Uploading Files](#2-uploading-files)
3. [Managing Files](#3-managing-files)
4. [Gofile API](#4-gofile-api)
5. [Use Cases](#5-use-cases)
6. [Limitations & Gotchas](#6-limitations--gotchas)
7. [Comparison Table](#7-comparison-table)

---

## 1. Free vs Account Usage

| Feature | Guest (No Account) | Account (Free) |
|---------|-------------------|----------------|
| **Upload** | ✅ | ✅ |
| **Max file size** | Unlimited | Unlimited |
| **File retention** | 10 days no activity | Indefinite |
| **Download password** | ❌ | ✅ |
| **File management** | ❌ | ✅ |
| **Folder organization** | ❌ | ✅ |
| **Direct links** | ✅ | ✅ |
| **API access** | ✅ (limited) | ✅ (full) |
| **Storage quota** | None stated | None stated |

Gofile is notably more generous than most competitors on the free tier — no file size cap and direct download links are available even without an account.

---

## 2. Uploading Files

### Web Upload

1. Visit https://gofile.io
2. Drag and drop files onto the page or click the upload area
3. Files upload immediately — no account needed
4. You receive a shareable link when complete

**Link format:**
```
https://gofile.io/d/FOLDERID
```

Each upload creates a folder on Gofile, even if you upload a single file. The folder link is what you share.

### CLI Upload via API

```bash
# Step 1: Get a server to upload to
SERVER=$(curl -s "https://api.gofile.io/servers" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['servers'][0]['name'])")
echo "Uploading to: $SERVER"

# Step 2: Upload the file (guest — no token needed)
curl -F "file=@/path/to/your/file.zip" "https://$SERVER.gofile.io/contents/uploadfile"

# Step 3: Response contains the download page link
# {"status":"ok","data":{"guestToken":"...","folderId":"...","folderCode":"abc123",...}}
```

```python
import requests

def upload_to_gofile(filepath: str, token: str = None) -> dict:
    """Upload a file to Gofile. Token optional (extends retention)."""
    # Get best server
    servers = requests.get("https://api.gofile.io/servers").json()
    server = servers["data"]["servers"][0]["name"]

    with open(filepath, "rb") as f:
        data = {}
        if token:
            data["token"] = token
        r = requests.post(
            f"https://{server}.gofile.io/contents/uploadfile",
            files={"file": f},
            data=data
        )
    result = r.json()
    if result["status"] == "ok":
        code = result["data"]["folderCode"]
        print(f"Uploaded: https://gofile.io/d/{code}")
        return result["data"]
    raise Exception(f"Upload failed: {result}")

# Guest upload
upload_to_gofile("/path/to/file.zip")

# Authenticated upload (token from account settings)
upload_to_gofile("/path/to/file.zip", token="YOUR_ACCOUNT_TOKEN")
```

---

## 3. Managing Files

File management (renaming, organizing, setting passwords, deleting) requires a Gofile account. Register free at https://gofile.io/register.

```python
import requests

TOKEN = "your_account_token"
BASE = "https://api.gofile.io"

def get_account_info(token: str) -> dict:
    r = requests.get(f"{BASE}/accounts/getid", headers={"Authorization": f"Bearer {token}"})
    return r.json()["data"]

def set_folder_password(folder_id: str, password: str, token: str) -> bool:
    r = requests.put(
        f"{BASE}/contents/{folder_id}/update",
        headers={"Authorization": f"Bearer {token}"},
        json={"attribute": "password", "attributeValue": password}
    )
    return r.json()["status"] == "ok"

def delete_content(content_id: str, token: str) -> bool:
    r = requests.delete(
        f"{BASE}/contents",
        headers={"Authorization": f"Bearer {token}"},
        json={"contentsId": content_id}
    )
    return r.json()["status"] == "ok"

def get_folder_contents(folder_id: str, token: str) -> list:
    r = requests.get(
        f"{BASE}/contents/{folder_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"token": token, "wt": "4fd6sg89d7s6"}
    )
    return r.json()["data"]["children"]
```

---

## 4. Gofile API

Full API documentation: https://gofile.io/api

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/servers` | GET | Get available upload servers |
| `/contents/uploadfile` | POST | Upload a file |
| `/contents/{id}` | GET | Get content metadata |
| `/contents/{id}/update` | PUT | Update content (name, password, etc.) |
| `/contents` | DELETE | Delete content |
| `/accounts/getid` | GET | Get account ID from token |
| `/accounts/{id}` | GET | Get account details |

### Authentication

All authenticated requests use a Bearer token in the `Authorization` header:
```
Authorization: Bearer YOUR_TOKEN
```

Get your token from https://gofile.io/myprofile after logging in.

---

## 5. Use Cases

**Large file distribution:** Gofile's unlimited file size makes it ideal for distributing ISOs, virtual machine images, large datasets, and video files that exceed limits on other platforms.

**Quick anonymous sharing:** No account required means you can upload and share a file in seconds with zero friction.

**Temporary file exchange:** Guest uploads lasting 10 days of inactivity are perfect for sharing files with someone who needs them once rather than permanently hosting them.

**Developer testing:** The API makes Gofile convenient for automated upload pipelines, CI/CD artifact sharing, and temporary storage in scripts.

---

## 6. Limitations & Gotchas

**Guest file expiry:** Guest uploads are deleted after 10 days without a download. This is shorter than some competitors. If you need permanent storage, create a free account.

**No encryption:** Files are stored unencrypted. Do not upload sensitive data without encrypting it yourself first.

**Content policy:** Gofile prohibits illegal content and will remove files that violate their terms. DMCA takedowns are processed.

**Server availability:** Upload server selection is important — always use the API to get the recommended server dynamically rather than hardcoding one.

**Download link is a folder page:** The share link opens a Gofile folder page, not a direct file download. Recipients see a web interface and click to download. Direct download links require constructing them from the API response.

---

## 7. Comparison Table

| Service | Max File Size | Free Retention | Account Required | No-Wait Download | API |
|---------|-------------|----------------|-----------------|-----------------|-----|
| **Gofile** | Unlimited | 10 days (guest) | Optional | ✅ | ✅ |
| **MediaFire** | 20 GB | Indefinite | For upload | ✅ | ✅ |
| **Mega.nz** | None | Indefinite | Yes | ✅ | ✅ |
| **WeTransfer** | 2 GB | 7 days | No | ✅ | Paid |
| **Catbox.moe** | 200 MB | Indefinite | No | ✅ | ✅ |
| **Archive.org** | Unlimited | Indefinite | For upload | ✅ | ✅ |

---

## See Also

- [MediaFire](mediafire.md) — Commercial file hosting with no-expiry free tier
- [Mega.nz](mega-nz.md) — Encrypted cloud storage with generous free quota
- [Archive.org](archive-org.md) — Permanent archival storage and the Wayback Machine
- [Smash](smash.md) — Transfer-focused file sending service
