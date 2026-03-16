# Free Movie & TV Streaming Platforms

This document covers free web-based movie and TV streaming platforms that provide access to films and series without subscription fees. These sites aggregate content from various sources and serve it through embedded video players.

> **Note:** The legal status of these platforms varies by jurisdiction. Many operate in gray areas regarding content licensing. Where legal free alternatives exist (Tubi, Pluto TV, YouTube Movies), they are noted. For full control over your media library, consider [Plex](plex.md) with your own files.

---

## Table of Contents
1. [Platform Overview](#1-platform-overview)
2. [PRMovies](#2-prmovies)
3. [FMovies](#3-fmovies)
4. [Nunflix](#4-nunflix)
5. [Legal Free Alternatives](#5-legal-free-alternatives)
6. [Comparison Table](#6-comparison-table)
7. [General Usage Tips](#7-general-usage-tips)

---

## 1. Platform Overview

| Platform | URL | Content | Account | Quality | Downloads |
|----------|-----|---------|---------|---------|-----------|
| **PRMovies** | prmovies.com | Movies + TV | No | Up to 4K | No |
| **FMovies** | fmovies.to (may vary) | Movies + TV | Optional | Up to 1080p | No |
| **Nunflix** | nunflix.org | Movies + TV | No | Up to 1080p | No |

> Domain names for these sites change frequently. If a URL is unreachable, search the platform name to find the current active domain.

---

## 2. PRMovies

- **Website:** https://prmovies.com (domain may vary)
- **Content:** Movies and TV series, heavy focus on Bollywood and South Asian cinema alongside Hollywood

### Overview

PRMovies has a strong catalog of Indian cinema (Bollywood, Tollywood, Malayalam, Tamil) alongside Hollywood films. It is particularly popular with South Asian diaspora audiences looking for regional language content with subtitles.

### Key Features

- Large Bollywood and Indian regional cinema catalog
- Hollywood movies and international titles
- Multiple streaming quality options (360p to 4K where available)
- No account required to watch
- Subtitles available for many titles
- TV series with episode-by-episode listing

### Content Strengths

- **Bollywood:** Most major releases including new releases
- **South Indian cinema:** Tamil, Telugu, Malayalam, Kannada films
- **Hollywood:** Major studio releases, independent films
- **Dubbed versions:** Many Indian films available with English or regional language dubs

### Navigation

```
Homepage → Recently added / Trending
Browse → By genre, by language, by year
Search → Title search across entire catalog
TV Shows → Separate section for series content
```

---

## 3. FMovies

- **Website:** https://fmovies.to (domain changes frequently — search "FMovies" for current domain)
- **Content:** Broad Hollywood and international film/TV catalog

### Overview

FMovies is one of the longest-running free streaming aggregators. It has been active in various forms since the mid-2010s and is known for a large and frequently updated catalog. The site has been cloned and mirrored many times — the "official" domain shifts periodically.

### Key Features

- Very large catalog spanning decades of Hollywood releases
- Both movies and complete TV series seasons
- Multiple server options per title — switch servers if one is slow
- Optional account for watchlist and watch history tracking
- Generally fast CDN servers
- Filters by genre, country, rating, and year

### Finding the Current Domain

FMovies operates under several domains simultaneously and migrates when one is blocked. Common current domains include:
```
fmovies.to
fmovies.ps
fmovies.wtf
```
Search "FMovies official" to find the currently active primary domain.

### Server Selection

Each title on FMovies has multiple streaming servers labeled by provider (e.g., Vidcloud, UpCloud, MyCloud). If one server buffers or fails:
1. Look for the server list below or beside the player
2. Click an alternative server name
3. The player reloads with a different CDN source

---

## 4. Nunflix

- **Website:** https://nunflix.org
- **Content:** Movies and TV series with a clean Netflix-inspired interface

### Overview

Nunflix is designed to mimic the Netflix UX — a grid-based browsing interface with category rows, hover previews, and a familiar navigation pattern. It serves as a free alternative for people who want the Netflix-style browsing experience without a subscription.

### Key Features

- Netflix-inspired UI — familiar layout for Netflix users
- Clean, modern interface with minimal ads compared to older streaming sites
- Movies and TV series organized into genre categories
- Trending and recently added sections on the homepage
- No account required
- Works well on mobile browsers

### Interface Layout

```
Homepage rows:
  - Trending Now
  - Recently Added Movies
  - Recently Added TV Shows
  - By Genre (Action, Comedy, Drama, Horror, etc.)
  - Top Rated
```

### Nunflix vs Netflix

Nunflix is an unofficial aggregator — content availability and quality varies, there is no original content, downloads are not available, and there is no offline mode. For users who want a legal Netflix-style experience for free, **Tubi** (tubi.tv) is a legal ad-supported alternative.

---

## 5. Legal Free Alternatives

If content is available legally for free, these platforms support the studios and creators directly:

| Platform | URL | Content | Region |
|----------|-----|---------|--------|
| **Tubi** | tubi.tv | 50,000+ movies and TV shows | US, CA, AU, UK, MX |
| **Pluto TV** | pluto.tv | Live channels + on-demand | US and many regions |
| **YouTube Movies** | youtube.com/movies | Free ad-supported films | Global |
| **Crackle** | crackle.com | Movies and originals | US |
| **Plex (free tier)** | plex.tv | Movies and TV | Global |
| **Kanopy** | kanopy.com | Arthouse and documentaries | Library card required |
| **Hoopla** | hoopladigital.com | Films, comics, audiobooks | Library card required |

---

## 6. Comparison Table

| Platform | Bollywood | Hollywood | TV Series | Account | Ads | Interface |
|----------|-----------|-----------|-----------|---------|-----|-----------|
| **PRMovies** | ✅ Strong | ✅ | ✅ | No | Yes | Basic |
| **FMovies** | Limited | ✅ Strong | ✅ | Optional | Yes | Standard |
| **Nunflix** | Limited | ✅ | ✅ | No | Minimal | Netflix-style |
| **Tubi (legal)** | Limited | ✅ | ✅ | Optional | Yes | Clean |
| **Pluto TV (legal)** | ❌ | ✅ | ✅ | Optional | Yes | TV-channel style |

---

## 7. General Usage Tips

**Ad blockers are essential:** All free streaming sites serve ads, often aggressively. Install **uBlock Origin** in Firefox or Chrome before visiting any of these sites. On mobile, use Firefox with uBlock Origin.

**Avoid fake download buttons:** These sites often have ads styled to look like download or play buttons. The real player is usually centered on the page — anything in sidebars or popups is typically an ad.

**Use yt-dlp for offline viewing:** Some streams on these platforms can be captured:
```bash
# Attempt to download (success varies by site and CDN)
yt-dlp "https://site.com/movie/title"

# If the site uses HLS (.m3u8), extract stream URL from browser DevTools:
# DevTools → Network → filter "m3u8" → play video → copy URL
ffmpeg -i "https://cdn.example.com/playlist.m3u8" -c copy output.mp4
```

**VPN for geo-restrictions:** Some streaming sites block certain countries. A VPN (ProtonVPN free tier, or any WireGuard provider) can bypass these restrictions.

**Self-hosting alternative:** If you own digital copies of films, [Plex](plex.md) gives you a private Netflix-quality experience from your own library with no ads and no third-party dependencies.

**BONUS** - New site: https://moontv.to

---

## See Also

- [Plex](plex.md) — Self-hosted media server for your own movie/TV collection
- [Anime Streaming](anime-streaming.md) — AnimePahe, HiAnime, Toono for anime content
- [Video Platforms](video-platforms.md) — Dailymotion, EverythingMoe
- [Media Tools](../media/media-tools.md) — FFmpeg, VLC for processing and playing downloaded video
