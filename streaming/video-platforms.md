# Video Streaming Platforms — Dailymotion & EverythingMoe

This document covers open video streaming platforms for hosting, discovering, and watching video content outside the mainstream YouTube/Netflix ecosystem.

---

## Table of Contents
1. [Dailymotion](#1-dailymotion)
2. [EverythingMoe](#2-everythingmoe)
3. [Comparison Table](#3-comparison-table)

---

## 1. Dailymotion

- **Website:** https://www.dailymotion.com
- **Founded:** 2005 (Paris, France)
- **Owner:** Vivendi (since 2015)
- **Content:** User-uploaded videos, licensed content, news, entertainment
- **Monetization:** Ad-supported free watching

### Overview

Dailymotion is one of the world's largest video hosting platforms, second only to YouTube in terms of reach. It hosts user-uploaded videos, licensed music videos, news clips, sports highlights, and original content. It is particularly strong in French and European content.

### Key Features

**For Viewers:**
- No account required to watch
- HD playback up to 4K on supported content
- Playlist support and channel following
- Embedded player available on external sites
- Mobile apps (iOS, Android)
- Live streaming support

**For Creators:**
- Free video hosting up to 4 GB per video / 60 minutes per video
- Unlimited uploads
- Analytics dashboard
- Monetization via Dailymotion Partner Program
- Customizable channel pages
- API access for developers

### Video Limits (Free Upload)

| Limit | Value |
|-------|-------|
| **Max file size** | 4 GB |
| **Max duration** | 60 minutes |
| **Supported formats** | MP4, AVI, MOV, WMV, FLV, MKV, and more |
| **Max resolution** | Up to 4K (UHD) |
| **Uploads per day** | Up to 10 per account |

### Dailymotion API

Dailymotion provides a REST API for embedding, searching, and managing videos programmatically.

- **API Docs:** https://developer.dailymotion.com
- **Authentication:** OAuth 2.0

```bash
# Search for public videos (no auth required for read)
curl "https://api.dailymotion.com/videos?search=linux+tutorial&limit=5&fields=id,title,url,duration"

# Get a specific video's metadata
curl "https://api.dailymotion.com/video/VIDEO_ID?fields=id,title,description,duration,thumbnail_url"

# Get videos from a channel
curl "https://api.dailymotion.com/user/USERNAME/videos?fields=id,title,url&limit=10"
```

```python
import requests

BASE = "https://api.dailymotion.com"

def search_videos(query: str, limit: int = 10) -> list:
    r = requests.get(f"{BASE}/videos", params={
        "search": query,
        "limit": limit,
        "fields": "id,title,url,duration,thumbnail_url,views_total"
    })
    return r.json().get("list", [])

def get_video_info(video_id: str) -> dict:
    r = requests.get(f"{BASE}/video/{video_id}", params={
        "fields": "id,title,description,duration,thumbnail_url,embed_url"
    })
    return r.json()

# Embed URL format
def get_embed_url(video_id: str) -> str:
    return f"https://www.dailymotion.com/embed/video/{video_id}"

results = search_videos("open source tutorial")
for v in results:
    print(f"{v['title']} — {v['url']}")
```

### Embed a Dailymotion Video

```html
<!-- Basic embed -->
<iframe
  frameborder="0"
  width="640"
  height="360"
  src="https://www.dailymotion.com/embed/video/VIDEO_ID"
  allowfullscreen
  allow="autoplay">
</iframe>

<!-- With parameters -->
<iframe
  src="https://www.dailymotion.com/embed/video/VIDEO_ID?autoplay=0&mute=1&queue-enable=false"
  width="640"
  height="360"
  frameborder="0"
  allowfullscreen>
</iframe>
```

### yt-dlp Support

Dailymotion videos can be downloaded with `yt-dlp`:

```bash
# Install yt-dlp
pip install yt-dlp

# Download a video
yt-dlp https://www.dailymotion.com/video/VIDEO_ID

# List available formats
yt-dlp -F https://www.dailymotion.com/video/VIDEO_ID

# Download specific quality
yt-dlp -f 'bestvideo[height<=1080]+bestaudio' https://www.dailymotion.com/video/VIDEO_ID

# Download a playlist
yt-dlp https://www.dailymotion.com/playlist/PLAYLIST_ID
```

### Dailymotion vs YouTube

| Feature | Dailymotion | YouTube |
|---------|-------------|---------|
| **Max duration (free)** | 60 min | Unlimited (verified) |
| **Storage** | Unlimited | Unlimited |
| **Monetization** | Partner Program | AdSense |
| **Algorithm reach** | Smaller | Massive |
| **Content moderation** | Less strict | Strict |
| **API** | ✅ REST | ✅ REST |
| **Live streaming** | ✅ | ✅ |
| **Shorts equivalent** | ❌ | ✅ |
| **Geographic restrictions** | Less | More |

---

## 2. EverythingMoe

- **Website:** https://www.everythingmoe.com
- **Content type:** Anime streaming
- **Account Required:** No (for watching)
- **Ad-supported:** Yes

### Overview

EverythingMoe is a free anime streaming site that aggregates anime content. It provides a large library of subbed and dubbed anime series and movies, updated regularly with new episodes.

### Key Features

- Large anime library covering seasonal, classic, and ongoing series
- Both subbed (English subtitles) and dubbed (English audio) options
- No account required to watch
- Episode tracking for series
- Search by genre, season, year, and status (ongoing, completed)
- Mobile-friendly interface

### Content Library

EverythingMoe covers:
- **Seasonal anime:** Currently airing series updated as episodes release
- **Completed series:** Full library of finished shows
- **Movies:** Anime films including major studio releases
- **OVAs and specials:** Original video animations and bonus episodes

### Finding Content

```
Main site:     https://www.everythingmoe.com
Browse all:    https://www.everythingmoe.com/anime
Search:        Use the search bar at the top of the page
By genre:      Filter using the genre dropdown
By season:     Filter by year and season (Winter, Spring, Summer, Fall)
```

### Usage Tips

- **Use an ad blocker:** The site is ad-supported with aggressive ads. uBlock Origin is strongly recommended for a better viewing experience
- **Streaming quality:** Multiple quality options are typically available (360p, 720p, 1080p)
- **Multiple servers:** If one streaming server is slow or broken, try switching to an alternative server for the same episode

---

## 3. Comparison Table

| Platform | Content | Account Needed | Download | API | Ad-Free Option |
|----------|---------|---------------|---------|-----|----------------|
| **Dailymotion** | General video | No (watching) | Via yt-dlp | ✅ | No |
| **EverythingMoe** | Anime | No | No | No | Via ad blocker |
| **YouTube** | General video | No (watching) | Via yt-dlp | ✅ | YouTube Premium |
| **Crunchyroll** | Anime (legal) | Free/Paid | Paid | ✅ | Paid plan |
| **Vimeo** | General/creative | No (watching) | Limited | ✅ | Paid |

---

## See Also

- [Anime Streaming](anime-streaming.md) — AnimePahe, AnimeKai, HiAnime, Toono, RareAnimes
- [Media Tools](../media/media-tools.md) — FFmpeg, VLC for processing downloaded video
- [Platforms & Communities](platforms-and-communities.md) — Social platforms and content communities
