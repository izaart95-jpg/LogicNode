# Plex — Self-Hosted Media Server

Plex is a media server platform that organizes your personal collection of movies, TV shows, music, and photos and makes them streamable to any device — exactly like Netflix, but from your own files. You run the server on your hardware; Plex handles the interface, metadata scraping, transcoding, and multi-device streaming.

- **Website:** https://www.plex.tv
- **Media Server:** Free (Plex Media Server)
- **Plex Pass:** Optional paid subscription for advanced features (~$4.99/mo or $119.99 lifetime)
- **Platforms:** Server: Windows, macOS, Linux, Docker, NAS (Synology, QNAP), NVIDIA Shield. Client: Every platform including smart TVs, game consoles, mobile, web.

---

## Table of Contents
1. [How Plex Works](#1-how-plex-works)
2. [Installation](#2-installation)
3. [Setting Up Libraries](#3-setting-up-libraries)
4. [File Naming Conventions](#4-file-naming-conventions)
5. [Transcoding](#5-transcoding)
6. [Remote Access](#6-remote-access)
7. [Plex Pass Features](#7-plex-pass-features)
8. [Plex Free Streaming (FAST)](#8-plex-free-streaming-fast)
9. [Docker Deployment](#9-docker-deployment)
10. [Plex API](#10-plex-api)
11. [Alternatives](#11-alternatives)

---

## 1. How Plex Works

```
Your files (movies, shows, music)
        │
        ▼
Plex Media Server (runs on your machine/NAS)
  - Scans and indexes your files
  - Fetches metadata (posters, descriptions, ratings) from TMDB/TheTVDB
  - Transcodes video to match client device capabilities
  - Streams over local network or internet
        │
        ▼
Plex clients (web, phone, TV, Roku, Xbox, PS5...)
  - Stream your library anywhere
  - Native apps on every platform
```

**Key concept — Direct Play vs Transcoding:**
- **Direct Play:** Client plays the file as-is (no server CPU used) — requires device supports the codec
- **Direct Stream:** Container is remuxed on the fly, codec unchanged
- **Transcoding:** Server converts video in real-time to a format the client can handle — CPU/GPU intensive

---

## 2. Installation

### Linux (Debian/Ubuntu)

```bash
# Download the latest .deb from https://www.plex.tv/media-server-downloads/
wget https://downloads.plex.tv/plex-media-server-new/VERSION/debian/plexmediaserver_VERSION_amd64.deb

# Install
sudo dpkg -i plexmediaserver_*.deb

# Enable and start
sudo systemctl enable plexmediaserver
sudo systemctl start plexmediaserver

# Check status
sudo systemctl status plexmediaserver

# Plex runs on port 32400
# Initial setup: http://localhost:32400/web
```

### macOS

```bash
# Homebrew
brew install --cask plex-media-server

# Or download .dmg from plex.tv
```

### Windows

Download the installer from https://www.plex.tv/media-server-downloads/ and run it. Plex installs as a background service and starts automatically.

### Permissions (Linux)

Plex runs as the `plex` user by default. Your media files must be readable by this user:

```bash
# Option 1: Add plex user to your media group
sudo usermod -aG your_media_group plex

# Option 2: Set read permissions on media directory
sudo chmod -R a+rX /path/to/media

# Option 3: Change ownership
sudo chown -R plex:plex /path/to/media
```

---

## 3. Setting Up Libraries

After installation, open `http://localhost:32400/web` to complete setup.

1. **Sign in** with a Plex account (free — needed for remote access and metadata)
2. **Add Library:** Click `+` next to Libraries in the left sidebar
3. **Choose type:** Movies, TV Shows, Music, Photos, or Other Videos
4. **Add folders:** Point Plex to the directory containing your files
5. Plex scans the folder and automatically matches files to metadata

### Library Types

| Type | Metadata Source | NFO Support |
|------|----------------|-------------|
| **Movies** | TMDB, IMDB | Yes |
| **TV Shows** | TheTVDB, TMDB | Yes |
| **Music** | MusicBrainz, Last.fm | Yes |
| **Photos** | EXIF data | N/A |

---

## 4. File Naming Conventions

Plex relies on consistent file naming to correctly identify and match your media to its database. Incorrect naming is the most common cause of unmatched or wrongly identified files.

### Movies

```
/Movies
  /The Dark Knight (2008)
    The Dark Knight (2008).mkv
  /Interstellar (2014)
    Interstellar (2014).mkv
  /Parasite (2019) {tmdb-496243}
    Parasite (2019) {tmdb-496243}.mkv   # Explicit TMDB ID avoids ambiguity
```

**Format:** `Movie Title (Year).ext`

### TV Shows

```
/TV Shows
  /Breaking Bad
    /Season 01
      Breaking Bad - S01E01 - Pilot.mkv
      Breaking Bad - S01E02 - Cat's in the Bag.mkv
    /Season 02
      Breaking Bad - S02E01 - Seven Thirty-Seven.mkv
  /The Office (US)
    /Season 01
      The Office (US) - S01E01.mkv
```

**Format:** `Show Name - SXXEXX - Episode Title.ext`

### Multi-Episode Files

```
Breaking Bad - S01E01E02.mkv        # Two episodes in one file
Breaking Bad - S01E01-E03.mkv       # Range (episodes 1-3)
```

### Specials and Extras

```
/Breaking Bad
  /Season 00                         # Season 00 = Specials in Plex
    Breaking Bad - S00E01 - Pilot Extra.mkv
  /Extras                            # Local extras folder
    Making of Breaking Bad.mkv
    Behind the Scenes.mkv
```

### Subtitles

Plex picks up external subtitle files automatically if named identically to the video:

```
Movie Title (2008).mkv
Movie Title (2008).en.srt           # English subtitles
Movie Title (2008).fr.srt           # French subtitles
Movie Title (2008).en.forced.srt    # Forced English (for foreign language parts)
```

---

## 5. Transcoding

Transcoding converts video on-the-fly when a client cannot direct play the source format. This is CPU-intensive.

### Hardware Transcoding (Plex Pass Required)

Hardware transcoding uses GPU/iGPU for much faster conversion with lower CPU usage.

```bash
# Check if hardware transcoding is available
# Plex Settings → Troubleshooting → Download Logs
# Look for: "Hardware-accelerated decoding is available"

# On Linux, ensure GPU drivers are installed and Plex can access the device
# NVIDIA:
sudo usermod -aG video plex
# Intel Quick Sync:
sudo apt install intel-media-va-driver
```

### Transcoding Quality Settings

In **Settings → Remote Access / Quality:**

| Setting | Use Case |
|---------|---------|
| **Original Quality** | Local network, gigabit — no transcoding |
| **20 Mbps 1080p** | High quality remote streaming |
| **8 Mbps 1080p** | Standard remote streaming |
| **4 Mbps 720p** | Mobile or slow connection |

### Reducing Transcoding

To avoid transcoding (better performance):
- Encode files in H.264 with AAC audio — plays natively on almost all devices
- Keep resolution at 1080p or below for most clients
- Avoid DTS, TrueHD, Atmos audio if clients don't support it (Plex transcodes audio separately)

---

## 6. Remote Access

Plex handles remote access automatically using their relay servers (no port forwarding required on free tier, but with bandwidth limits). For direct access:

### Port Forwarding (Faster, No Relay)

```
Router settings:
  External port: 32400
  Internal IP: your Plex server's local IP
  Internal port: 32400
  Protocol: TCP
```

After port forwarding, go to **Plex Settings → Remote Access** and verify the green checkmark.

### Access from Outside

Once configured, your Plex library is accessible at:
```
https://app.plex.tv   (web, uses your Plex account login)
Plex app on any device → Sign in → your library appears automatically
```

### Sharing with Others

```
Plex Web → Settings → Manage → Users & Sharing → Invite Friend
```

Enter their email — they create a free Plex account and your libraries appear in their app. You control which libraries they can see.

---

## 7. Plex Pass Features

Plex Pass (~$4.99/mo, $39.99/yr, or $119.99 lifetime) adds:

| Feature | Description |
|---------|-------------|
| **Hardware transcoding** | GPU-accelerated conversion |
| **Mobile sync/downloads** | Download to phone for offline viewing |
| **Live TV + DVR** | Connect a TV tuner (HDHomeRun) for live TV |
| **Multi-user home** | Separate watch history per household member |
| **Lyrics** | Synced lyrics for music |
| **Trailer/extras** | Auto-download movie trailers and extras |
| **Skip Intro** | Skip opening credits automatically |
| **Plexamp** | Dedicated music player app |
| **Early access** | New features before general release |

---

## 8. Plex Free Streaming (FAST)

Plex also offers a free ad-supported streaming service (similar to Tubi) built directly into the Plex app — no Plex Media Server required. Browse and watch free movies and live TV channels from the Plex app without setting up your own server.

```
Plex app (web or mobile) → "Movies & TV" or "Live TV" sections
(These are Plex's free catalog, not your personal library)
```

This makes Plex useful even if you don't want to run a media server — it's a legal free streaming platform on its own.

---

## 9. Docker Deployment

Running Plex in Docker is the recommended approach for servers and NAS devices.

```yaml
# docker-compose.yml
services:
  plex:
    image: plexinc/pms-docker:latest
    container_name: plex
    network_mode: host        # Required for local network discovery
    environment:
      - PLEX_CLAIM=claim-XXXXXXXXXX   # Get from plex.tv/claim (valid 4 min)
      - TZ=America/New_York
    volumes:
      - /opt/plex/config:/config       # Plex database and metadata
      - /opt/plex/transcode:/transcode # Temp transcoding storage (use SSD)
      - /mnt/media/movies:/movies:ro   # Your movie files (read-only)
      - /mnt/media/tv:/tv:ro          # Your TV files
      - /mnt/media/music:/music:ro    # Your music
    devices:
      - /dev/dri:/dev/dri              # Intel/AMD GPU for HW transcoding
    restart: unless-stopped
```

```bash
# Get your claim token (expires in 4 minutes)
# Visit: https://www.plex.tv/claim

# Start Plex
docker compose up -d

# Access: http://YOUR_SERVER_IP:32400/web

# View logs
docker logs plex -f

# Update Plex
docker compose pull
docker compose up -d
```

### GPU Passthrough (NVIDIA)

```yaml
services:
  plex:
    image: plexinc/pms-docker:latest
    runtime: nvidia              # Requires nvidia-container-toolkit
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,video,utility
```

---

## 10. Plex API

Plex exposes a REST API for automation, building custom clients, and integration with other tools.

```bash
# Get your Plex token
# Plex Web → Account → Settings → scroll down → "XML" link → token in URL
# Or: check any Plex request in browser DevTools → X-Plex-Token header

PLEX_URL="http://localhost:32400"
TOKEN="your_plex_token"

# Get all libraries
curl "$PLEX_URL/library/sections?X-Plex-Token=$TOKEN" -H "Accept: application/json"

# Get all movies in a library (section 1)
curl "$PLEX_URL/library/sections/1/all?X-Plex-Token=$TOKEN" -H "Accept: application/json"

# Search across all libraries
curl "$PLEX_URL/search?query=batman&X-Plex-Token=$TOKEN" -H "Accept: application/json"

# Get recently added
curl "$PLEX_URL/library/recentlyAdded?X-Plex-Token=$TOKEN" -H "Accept: application/json"

# Trigger library scan
curl -X PUT "$PLEX_URL/library/sections/1/refresh?X-Plex-Token=$TOKEN"
```

```python
# Using the plexapi Python library
pip install plexapi

from plexapi.server import PlexServer

PLEX_URL = 'http://localhost:32400'
PLEX_TOKEN = 'your_token'

plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# List all movies
movies = plex.library.section('Movies')
for movie in movies.all():
    print(f"{movie.title} ({movie.year}) — {movie.duration // 60000} min")

# Search
results = plex.search('Inception')
for r in results:
    print(r.title, r.type)

# Get recently added
for item in plex.library.recentlyAdded():
    print(item.title)

# Mark as watched
movie = plex.library.section('Movies').get('The Dark Knight')
movie.markWatched()

# Get watch history
history = plex.history()
for item in history[:10]:
    print(item.title, item.viewedAt)
```

---

## 11. Alternatives

| Software | Self-Hosted | Free | Best For |
|----------|------------|------|---------|
| **Plex** | ✅ | ✅ (core) | Ease of use, any device |
| **Jellyfin** | ✅ | ✅ (fully open source) | No account required, privacy |
| **Emby** | ✅ | ✅ (limited) | Plex-like but open source roots |
| **Kodi** | Local only | ✅ | Local playback, advanced control |
| **Navidrome** | ✅ | ✅ | Music only, Subsonic API |

**Jellyfin** (https://jellyfin.org) is the most notable alternative — fully open source (GPL), no account required, no cloud dependency, all Plex Pass features free. Drop-in replacement for users who don't want any Plex telemetry or account requirement.

---

## See Also

- [Movie Streaming](movie-streaming.md) — PRMovies, FMovies, Nunflix for streaming without your own files
- [Docker Essentials](../devtools/docker-essentials.md) — Running Plex and other services in containers
- [Anime Streaming](anime-streaming.md) — HiAnime, AnimePahe, Toono
- [Media Tools](../media/media-tools.md) — FFmpeg for preparing media files for Plex
