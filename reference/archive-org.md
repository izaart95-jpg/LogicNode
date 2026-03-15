# Archive.org — The Internet Archive

The Internet Archive is a nonprofit digital library offering free public access to digitized books, websites, software, music, video, and more. It is one of the most important resources on the internet for research, preservation, and recovery of lost content.

- **Website:** https://archive.org
- **Founded:** 1996 by Brewster Kahle
- **Type:** 501(c)(3) nonprofit
- **Motto:** "Universal Access to All Knowledge"
- **Scale:** 40+ petabytes of data, 800+ billion web pages archived

---

## Table of Contents
1. [Core Services Overview](#1-core-services-overview)
2. [Wayback Machine](#2-wayback-machine)
3. [Software Library](#3-software-library)
4. [Books & Texts](#4-books--texts)
5. [Audio & Music](#5-audio--music)
6. [Video Archive](#6-video-archive)
7. [Uploading & Contributing](#7-uploading--contributing)
8. [APIs & Programmatic Access](#8-apis--programmatic-access)
9. [Use Cases for Developers & Researchers](#9-use-cases-for-developers--researchers)
10. [Limitations & Gotchas](#10-limitations--gotchas)

---

## 1. Core Services Overview

| Service | URL | Description |
|---------|-----|-------------|
| **Wayback Machine** | https://web.archive.org | Archived snapshots of websites across time |
| **Software Library** | https://archive.org/details/software | DOS, Amiga, Console, PC games — playable in browser |
| **Books & Texts** | https://archive.org/details/texts | 40M+ digitized books, papers, and documents |
| **Audio Archive** | https://archive.org/details/audio | Music, concerts, podcasts, radio broadcasts |
| **Video Archive** | https://archive.org/details/movies | Films, TV, documentaries, internet video |
| **Live Music Archive** | https://archive.org/details/etree | 250,000+ live concert recordings |
| **Open Library** | https://openlibrary.org | Digital lending of books (borrow for 1 hour) |

All content on Archive.org is accessible without an account. Uploading requires a free account.

---

## 2. Wayback Machine

The Wayback Machine is the most widely used part of Archive.org. It crawls the public web continuously and saves snapshots of pages — currently over 800 billion URLs.

### Basic Usage

Visit https://web.archive.org, paste any URL, and see a calendar of every snapshot ever saved.

**Direct URL format:**
```
https://web.archive.org/web/TIMESTAMP/ORIGINAL_URL

# Examples:
https://web.archive.org/web/20100101000000/http://google.com
https://web.archive.org/web/2024*/https://example.com    # Wildcard — all 2024 snapshots
https://web.archive.org/web/https://example.com          # Most recent snapshot
```

### Saving a Page Right Now

You can manually trigger a save of any public URL:

```
https://web.archive.org/save/https://example.com/page-you-want-saved

# Or use the Save Page Now form on the homepage
```

```bash
# Save via curl
curl -s "https://web.archive.org/save/https://example.com" | grep -o 'web/[0-9]*/.*'
```

### Wayback Machine API

```bash
# Check if a URL has been archived and get the most recent snapshot
curl "http://archive.org/wayback/available?url=example.com"
# Returns: {"archived_snapshots":{"closest":{"available":true,"url":"https://web.archive.org/web/20250101120000/https://example.com/","timestamp":"20250101120000","status":"200"}}}

# Get closest snapshot to a specific timestamp
curl "http://archive.org/wayback/available?url=example.com&timestamp=20150101"

# CDX API — get a list of all snapshots with metadata
curl "http://web.archive.org/cdx/search/cdx?url=example.com&output=json&limit=10"

# CDX with filters (only 200 OK responses, only HTML pages)
curl "http://web.archive.org/cdx/search/cdx?url=example.com/*&output=json&fl=timestamp,original,statuscode&filter=statuscode:200&limit=20"
```

**CDX API fields (`fl` parameter):**
`timestamp`, `original`, `mimetype`, `statuscode`, `digest`, `length`, `urlkey`

### Python: Wayback Machine Client

```python
import requests

def get_wayback_snapshot(url, timestamp=None):
    """Get the closest archived snapshot to a given timestamp."""
    params = {"url": url}
    if timestamp:
        params["timestamp"] = timestamp
    r = requests.get("http://archive.org/wayback/available", params=params)
    data = r.json()
    snapshots = data.get("archived_snapshots", {})
    closest = snapshots.get("closest", {})
    if closest.get("available"):
        return closest["url"]
    return None

# Get most recent snapshot
print(get_wayback_snapshot("example.com"))

# Get snapshot from 2015
print(get_wayback_snapshot("example.com", "20150601"))
```

```python
# Bulk save a list of URLs
import requests, time

urls_to_save = [
    "https://example.com/important-page",
    "https://docs.example.com/reference",
]

for url in urls_to_save:
    r = requests.get(f"https://web.archive.org/save/{url}")
    print(f"Saved: {url} → {r.url}")
    time.sleep(2)  # Be respectful of rate limits
```

---

## 3. Software Library

Archive.org hosts an enormous collection of vintage and historical software, most of which can be run directly in the browser via emulation (DOSBox, MAME, JSMESS).

### Collections

| Collection | URL | Content |
|------------|-----|---------|
| **MS-DOS Games** | https://archive.org/details/softwarelibrary_msdos_games | 7,000+ DOS games |
| **Console Living Room** | https://archive.org/details/consolelivingroom | Atari, NES, SNES, Sega ROMs |
| **Shareware CDs** | https://archive.org/details/cd_shareware | Historic shareware collections |
| **Apple II Library** | https://archive.org/details/softwarelibrary_apple2 | Apple II software |
| **Amiga** | https://archive.org/details/softwarelibrary_amiga | Amiga demos and games |
| **Windows 3.1 Software** | https://archive.org/details/softwarelibrary_win3 | Windows 3.x era apps |

### Browser Emulation

Many items have an embedded emulator — just click **Run Now** on the item page. No installation required.

---

## 4. Books & Texts

Archive.org provides free access to millions of digitized texts in multiple formats.

### Access

- **No DRM public domain works:** Download directly as PDF, EPUB, TXT, DJVU
- **In-copyright modern books:** Borrow via Open Library (1-hour or 14-day loans, requires free account)
- **Lending Library:** ~2 million books available to borrow one at a time

### Download Formats

| Format | Best For |
|--------|---------|
| **PDF** | Exact page scans, printing |
| **EPUB** | E-readers, mobile devices |
| **DJVU** | Compressed scanned books |
| **TXT** | Full-text search, processing |

### Finding Books

```bash
# Direct search
https://archive.org/search?query=linux+kernel+programming&mediatype=texts

# Advanced search with filters
https://archive.org/search?query=subject:"computer science"&mediatype=texts&year=1990-2000

# Open Library (book metadata + borrow interface)
https://openlibrary.org/search?q=operating+systems
```

---

## 5. Audio & Music

Archive.org is a major host for legally free music and audio.

### Live Music Archive

The most popular audio collection — 250,000+ live concert recordings donated by tapers (audience recorders), primarily for jam bands, folk, and touring acts that permit taping.

```
https://archive.org/details/GratefulDead  # Grateful Dead concerts
https://archive.org/details/PhishNetBand  # Phish
```

### Other Audio Collections

| Collection | Content |
|------------|---------|
| **Netlabel** | Creative Commons electronic music |
| **78 RPMs and Cylinder Recordings** | Pre-1930 recordings |
| **Old Time Radio** | Classic radio dramas and shows |
| **Podcasts** | Historical podcast archives |

---

## 6. Video Archive

```
https://archive.org/details/movies          # All video content
https://archive.org/details/feature_films   # Public domain feature films
https://archive.org/details/opensource_movies  # Open source films
https://archive.org/details/newsandpublicaffairs  # News footage archive
```

The **Prelinger Archives** (https://archive.org/details/prelinger) contain 6,000+ historical advertising, industrial, educational, and government films — all free to use, mostly public domain.

---

## 7. Uploading & Contributing

Anyone with a free account can upload and preserve content on Archive.org. All uploads are permanent (by design) and publicly accessible by default.

### Create an Account

https://archive.org/account/signup — free, no payment required.

### Upload via Web

1. Log in → click the **Upload** button (top right)
2. Add files (up to 10GB per upload via web interface)
3. Fill in metadata: title, description, subject tags, creator
4. Choose license (Creative Commons options or choose "No Known Copyright")
5. Submit

### Upload via CLI (internetarchive tool)

```bash
# Install the ia CLI tool
pip install internetarchive

# Configure with your account credentials
ia configure

# Upload a single file
ia upload my-identifier-name file.pdf \
  --metadata="title:My Important Document" \
  --metadata="creator:John Doe" \
  --metadata="subject:linux"

# Upload an entire directory
ia upload my-project-archive ./project-folder/ \
  --metadata="title:My Project Archive" \
  --metadata="mediatype:software"

# Upload with multiple metadata fields
ia upload historic-recording concert.flac \
  --metadata="title:Live at the Fillmore 1969" \
  --metadata="creator:The Example Band" \
  --metadata="date:1969-10-15" \
  --metadata="mediatype:audio"

# Download an item
ia download identifier-name

# Download a specific file from an item
ia download identifier-name specific-file.pdf

# Search for items
ia search "subject:linux AND mediatype:texts"

# Get item metadata as JSON
ia metadata identifier-name

# List files in an item
ia list identifier-name
```

### Identifiers

Every item on Archive.org has a unique **identifier** — a short string used in the URL:
`https://archive.org/details/IDENTIFIER`

Choose identifiers that are descriptive and unlikely to conflict with existing items. Identifiers cannot be changed after upload.

---

## 8. APIs & Programmatic Access

### Search API

```bash
# Full-text search (returns JSON)
curl "https://archive.org/advancedsearch.php?q=linux+kernel&fl%5B%5D=identifier,title,date&rows=10&output=json"

# Filter by media type
curl "https://archive.org/advancedsearch.php?q=subject:security&mediatype=texts&output=json&rows=5"
```

```python
import requests

def search_archive(query, mediatype=None, rows=10):
    params = {
        "q": query,
        "fl[]": ["identifier", "title", "date", "creator"],
        "rows": rows,
        "output": "json",
        "sort[]": "downloads desc"
    }
    if mediatype:
        params["q"] += f" AND mediatype:{mediatype}"
    r = requests.get("https://archive.org/advancedsearch.php", params=params)
    return r.json()["response"]["docs"]

results = search_archive("linux kernel book", mediatype="texts")
for item in results:
    print(f"{item['title']} — {item['identifier']}")
```

### Metadata API

```bash
# Get metadata for any item
curl "https://archive.org/metadata/IDENTIFIER"

# Get just files list
curl "https://archive.org/metadata/IDENTIFIER/files"

# Specific file metadata
curl "https://archive.org/metadata/IDENTIFIER/files/filename.pdf"
```

### Download URLs

Files on Archive.org follow a consistent URL pattern:

```
https://archive.org/download/IDENTIFIER/FILENAME

# Example:
https://archive.org/download/gd73-01-27.sbd.hollister.94.sbeok.t-flac16/gd73-01-27d1t01.flac
```

---

## 9. Use Cases for Developers & Researchers

**Recover a deleted or changed webpage:**
```bash
curl "http://archive.org/wayback/available?url=example.com/deleted-page"
```

**Check what a site looked like before a redesign:**
Visit `https://web.archive.org/web/20200101000000/https://yoursite.com`

**Mirror important documentation:**
```bash
# Save pages before a library or wiki shuts down
ia upload my-wiki-backup wiki-dump.tar.gz --metadata="title:Example Wiki Backup 2025"
```

**Bulk download public domain books for NLP/ML:**
```python
import requests

# Get list of public domain programming books
results = search_archive("subject:computer science programming", mediatype="texts", rows=50)
for item in results:
    # Download each item's text version
    files_url = f"https://archive.org/metadata/{item['identifier']}/files"
    files = requests.get(files_url).json()
    # Find TXT or EPUB versions...
```

**Historical software testing:**
Use the Software Library emulator to test in historical OS environments without setting up your own VM.

**OSINT — find old versions of a target site:**
```bash
# Get all snapshots of a domain in JSON
curl "http://web.archive.org/cdx/search/cdx?url=*.example.com&output=json&fl=timestamp,original&collapse=urlkey&limit=100"
```

---

## 10. Limitations & Gotchas

**Permanence:** Uploads are intended to be permanent. Archive.org is not a temporary storage service. Think carefully before uploading — you cannot easily delete your own uploads (requires a support request with justification).

**Copyright:** You are responsible for only uploading content you have rights to share. Archive.org will comply with valid DMCA takedown requests. Public domain status varies by country.

**Wayback Machine gaps:** Not every page has been archived. Sites using `robots.txt` to block crawlers, JavaScript-heavy SPAs, and paywalled content may have incomplete or no snapshots.

**Speed:** Archive.org servers can be slow compared to commercial CDNs, especially for large files and during peak times.

**Identifiers are permanent:** Once you choose an identifier for an upload, it cannot be changed. Choose carefully.

**No private uploads:** All uploads are public by default. Archive.org is not suitable for private file storage.

---

## See Also

- [MediaFire](mediafire.md) — Commercial file hosting for private and large file sharing
- [APIs & Resources](apis-and-resources.md) — Public APIs and developer resources
- [OPSEC & Proxies](../security/opsec-and-proxies.md) — Accessing Archive.org anonymously via Tor
