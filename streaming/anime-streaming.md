# Anime Streaming Platforms

This document covers free anime streaming platforms — sites and apps providing access to subbed and dubbed anime series, movies, and OVAs. These are community-oriented platforms for anime viewers who want broad access outside official paid services.

> **Note:** The legal status of streaming on these platforms varies by region and content. Many aggregate from third-party sources. Where legal alternatives exist (Crunchyroll, HIDIVE, Netflix), they support the creators directly.

---

## Table of Contents
1. [Platform Overview](#1-platform-overview)
2. [AnimePahe](#2-animepahe)
3. [AnimeKai](#3-animekai)
4. [HiAnime (Aniwatch)](#4-hianime-aniwatch)
5. [Toono](#5-toono)
6. [RareAnimes](#6-rareanimes)
7. [Comparison Table](#7-comparison-table)
8. [General Usage Tips](#8-general-usage-tips)

---

## 1. Platform Overview

| Platform | URL | Sub | Dub | Download | Mobile App | Account Needed |
|----------|-----|-----|-----|---------|-----------|---------------|
| **AnimePahe** | animepahe.ru | ✅ | Limited | ✅ | Via browser | No |
| **AnimeKai** | animekai.bz | ✅ | ✅ | ❌ | Via browser | No |
| **HiAnime** | hianime.to | ✅ | ✅ | Via scripts | Via browser | No |
| **Toono** | toono.app | ✅ | ✅ | ❌ | ✅ Native | Optional |
| **RareAnimes** | rareanimes.app | ✅ | Limited | ❌ | ✅ Native | Optional |

> URLs may change over time as these sites sometimes switch domains. If a URL is unreachable, search for the current domain.

---

## 2. AnimePahe

- **Website:** https://animepahe.ru (domain may vary)
- **Specialty:** High-quality compressed video files, direct download

### Overview

AnimePahe is known for providing high-quality anime encodes at significantly smaller file sizes than most streaming platforms. The site uses efficient video compression (typically x265/HEVC) to deliver 720p and 1080p quality at 50–150 MB per episode rather than 500+ MB.

### Key Features

- **Compressed downloads:** Episodes available for direct download, typically 80–150 MB at 720p with x265 encoding — significantly smaller than comparable quality on other sites
- **High video quality:** Despite small file sizes, video quality is generally excellent due to efficient encoding
- **Minimal ads:** Relatively fewer and less intrusive ads compared to competitors
- **Fast updates:** New episodes typically available within hours of Japanese broadcast
- **Large library:** Comprehensive catalog of ongoing and completed series
- **English subtitles only:** Primarily fansub and official subs — limited dubbing

### How to Use

1. Visit the site and search for an anime title
2. Click the series to see episode list
3. Click an episode
4. Select quality (360p, 480p, 720p, 1080p)
5. **Stream:** Click the play button to watch directly
6. **Download:** Right-click the player or use the download button that appears to save the file

### Download Quality Sizes (approximate per episode)

| Quality | Encoding | Approx Size |
|---------|---------|------------|
| 360p | x264 | 30–60 MB |
| 480p | x264/x265 | 60–100 MB |
| 720p | x265 | 80–150 MB |
| 1080p | x265 | 120–250 MB |

### yt-dlp / Gallery-dl

AnimePahe streams can sometimes be captured with yt-dlp:

```bash
# Attempt to download an episode
yt-dlp "https://animepahe.ru/play/EPISODE_URL"

# If direct stream capture is blocked, use browser extension
# "Video DownloadHelper" for Firefox/Chrome can capture HLS streams
```

---

## 3. AnimeKai

- **Website:** https://animekai.bz (domain may vary)
- **Specialty:** Large library with both sub and dub, fast streaming

### Overview

AnimeKai provides a large catalog of both subbed and dubbed anime with multiple streaming servers per episode. It is a solid general-purpose anime streaming site with a clean interface.

### Key Features

- **Sub and dub:** Most popular titles available in both subbed and English dubbed versions
- **Multiple servers:** Each episode typically has 3–5 different streaming servers — if one is slow or broken, switch to another
- **No account required:** Watch without creating an account
- **Episode comments:** Community comments per episode (requires account to post)
- **Watchlist:** Track your watching progress (requires account)
- **Mobile-friendly:** Works well on mobile browsers

### Navigation

```
Homepage → Currently airing / Recently updated
Search → By title, genre, year, type (TV, Movie, OVA, ONA)
Schedule → Weekly airing schedule showing which shows release on which day
```

---

## 4. HiAnime (Aniwatch)

- **Website:** https://hianime.to (also known as Aniwatch)
- **Specialty:** Extensive library, clean UI, popular community

### Overview

HiAnime (formerly known as Aniwatch) is one of the most popular free anime streaming platforms due to its large library, clean interface, fast servers, and consistent updates. It has a strong community following.

### Key Features

- **Massive library:** One of the largest free anime catalogs available, covering seasonal, classic, and obscure titles
- **Clean interface:** Well-organized UI with minimal visual clutter compared to many competitors
- **Sub + Dub toggle:** Easy switch between subbed and dubbed within the same player
- **Fast CDN:** Generally fast loading and buffering
- **Episode thumbnails:** See preview thumbnails when scrubbing through an episode
- **Continue watching:** Browser-based tracking of where you left off (no account needed)
- **Community features:** Comments, ratings, recommendations
- **AniList/MyAnimeList sync:** Can sync your watching progress to AniList or MAL with an account

### Advanced Features

**Keyboard shortcuts in the player:**

| Key | Action |
|-----|--------|
| Space / K | Play/Pause |
| F | Fullscreen |
| M | Mute |
| ← / → | Seek 5 seconds |
| J / L | Seek 10 seconds |
| , / . | Frame-by-frame (when paused) |
| Shift + N | Next episode |
| Shift + P | Previous episode |

### Downloading from HiAnime

HiAnime does not provide direct download links. Options for saving episodes:

```bash
# Use yt-dlp (may work on some episodes)
yt-dlp "https://hianime.to/watch/ANIME-SLUG-ID?ep=EPISODE_ID"

# Use browser developer tools to capture the .m3u8 stream URL:
# 1. Open DevTools (F12) → Network tab
# 2. Play the episode
# 3. Filter by "m3u8" in the search box
# 4. Copy the m3u8 URL
# 5. Download with yt-dlp or ffmpeg:
yt-dlp "https://example.cdn.com/path/playlist.m3u8"
# or
ffmpeg -i "https://example.cdn.com/path/playlist.m3u8" -c copy output.mp4
```

---

## 5. Toono

- **Website / App:** https://toono.app
- **Platforms:** iOS, Android, Web
- **Specialty:** Native mobile app experience for anime streaming

### Overview

Toono is a dedicated anime streaming app with a native mobile experience. Unlike browser-based sites, Toono provides a purpose-built iOS and Android app for smooth anime watching on mobile devices.

### Key Features

- **Native mobile apps:** Proper iOS and Android apps rather than a mobile web browser experience
- **Smooth UI:** App-native interface designed for touch navigation
- **Large catalog:** Covers ongoing seasonal anime and an extensive back catalog
- **Sub and dub:** Both options available for supported titles
- **Offline/download:** Some versions support downloading episodes for offline viewing
- **Tracking:** Built-in watch history and progress tracking
- **Search and discovery:** Browse by genre, season, popularity

### Getting the App

```
iOS:     App Store → search "Toono"
Android: Google Play → search "Toono"
         or APK from https://toono.app/download
Web:     https://toono.app (browser streaming)
```

### Why Use Toono Over Browser Sites?

- No need to deal with browser ad redirects on mobile
- Native video player with proper gesture controls (swipe to seek, pinch to zoom)
- Better battery life than a browser on mobile
- Push notifications for new episodes of followed shows

---

## 6. RareAnimes

- **Website / App:** https://rareanimes.app
- **Platforms:** iOS, Android, Web
- **Specialty:** Obscure, classic, and hard-to-find anime titles

### Overview

RareAnimes focuses specifically on the harder-to-find corner of the anime catalog — classic series from the 80s and 90s, obscure OVAs, regional releases, and titles that mainstream platforms like Crunchyroll do not carry. It fills a genuine gap for anime enthusiasts looking for older or niche content.

### Key Features

- **Rare and obscure titles:** The core differentiator — focus on anime not available on mainstream platforms
- **Classic anime:** Strong catalog of 80s, 90s, and early 2000s series
- **OVAs and specials:** Extensive collection of original video animations, bonus episodes, and short films
- **Native mobile app:** iOS and Android apps for clean mobile experience
- **Subtitle options:** Often includes multiple subtitle tracks including older fansubs for classic titles

### Getting the App

```
iOS:     App Store → search "RareAnimes"
Android: Google Play → search "RareAnimes"
         or APK from https://rareanimes.app
Web:     https://rareanimes.app (browser streaming)
```

### What "Rare" Means Here

Examples of content types RareAnimes specializes in:

- Anime from the 1970s–1990s (Fist of the North Star, City Hunter, Slam Dunk originals)
- OVAs that were never licensed for Western streaming
- Short film collections and anthology series
- Regional anime with limited international release
- Series that left Crunchyroll/HIDIVE licensing windows

---

## 7. Comparison Table

| Platform | Library Size | Sub | Dub | Download | Mobile App | Rare/Classic | Best For |
|----------|-------------|-----|-----|---------|-----------|-------------|---------|
| **AnimePahe** | Large | ✅ | Limited | ✅ Direct | Browser | Some | Download quality, file size |
| **AnimeKai** | Large | ✅ | ✅ | ❌ | Browser | Some | Sub+Dub availability |
| **HiAnime** | Very Large | ✅ | ✅ | Via script | Browser | Some | General use, community |
| **Toono** | Large | ✅ | ✅ | Some | ✅ Native | Limited | Mobile experience |
| **RareAnimes** | Niche | ✅ | Limited | ❌ | ✅ Native | ✅ Specialty | Classic + obscure anime |
| **Crunchyroll** | Very Large | ✅ | ✅ | Paid | ✅ Native | Limited | Legal, creator support |
| **HIDIVE** | Large | ✅ | ✅ | Paid | ✅ Native | Some | Legal, niche titles |

---

## 8. General Usage Tips

**Use an ad blocker:** All free streaming sites serve ads. Install **uBlock Origin** (Firefox/Chrome) for the best experience. On mobile, use Firefox with uBlock Origin rather than Chrome.

**Switch servers if buffering:** Every platform offers multiple streaming servers per episode. If buffering is slow, look for a server selector button (often labeled S1, S2, S3 or by provider names like Vidcloud, Doodstream) and switch.

**Check subtitle quality:** Some episodes have machine-translated or low-quality subtitles. If a subtitle track seems off, check if the player has alternative subtitle options.

**Tracking your watching:** These sites have limited built-in tracking. Use **AniList** (https://anilist.co) or **MyAnimeList** (https://myanimelist.net) to maintain a proper watch list and history — these are separate free services you manage independent of which streaming site you use.

**Legal alternatives:** If a title is available on Crunchyroll (free ad-supported tier available), HIDIVE, or Netflix, watching there directly supports the creators and studios. Many seasonal titles are available legally and for free.

---

## See Also

- [Video Platforms](video-platforms.md) — Dailymotion, EverythingMoe — general video streaming
- [Media Tools](../media/media-tools.md) — FFmpeg for processing downloaded anime files
- [Platforms & Communities](../reference/platforms-and-communities.md) — Community platforms and discussion forums
