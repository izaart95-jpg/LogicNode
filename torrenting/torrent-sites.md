# Torrent Sites Directory

A reference for major torrent indexing sites — what they specialize in, their status, domain history, notable features, and how to find them when domains change.

> **Legal notice:** Torrenting copyrighted material without authorization is illegal in many countries. This document covers the technology and platforms for educational and research purposes. Only download content you have the right to access.

---

## Table of Contents
1. [Finding Current Domains](#1-finding-current-domains)
2. [The Pirate Bay (TPB)](#2-the-pirate-bay-tpb)
3. [1337x](#3-1337x)
4. [YTS (YIFY)](#4-yts-yify)
5. [RARBG — Shutdown (2023)](#5-rarbg--shutdown-2023)
6. [Torlock](#6-torlock)
7. [LimeTorrents](#7-limetorrents)
8. [KickassTorrents (KAT)](#8-kickasstorrents-kat)
9. [ETTV](#9-ettv)
10. [TorrentGalaxy (TGx)](#10-torrentgalaxy-tgx)
11. [Torrends.to](#11-torrendsto)
12. [Appdoze](#12-appdoze)
13. [Site Comparison](#13-site-comparison)

---

## 1. Finding Current Domains

Torrent sites regularly change domains due to ISP blocking, domain seizures, and takedown orders. Before assuming a site is down, check these resources:

```
Domain status / current URLs:
  https://torrends.to          ← Aggregates torrent site status (meta-site)
  Reddit: r/Piracy             ← Community-maintained wiki with current domains
  GitHub: "piracy" repos       ← Community megathreads

For ISP-blocked sites:
  Use a VPN (recommended)
  Use the site's .onion address (Tor browser)
  Search "site-name unblock proxy 2026"

Domain change pattern:
  Most sites register alternative TLDs when primary is blocked:
  .to → .st → .ws → .eu → .se → .cc → .onion
  The official domains page (if any) always has the canonical list.
```

---

## 2. The Pirate Bay (TPB)

- **Primary domain:** https://thepiratebay.org
- **Onion (Tor):** `piratebayo3klnzokct3wt5yyxb2vpebbuyjl7m623iaxmqhsd52coid.onion`
- **Founded:** 2003 (Stockholm, Sweden)
- **Status:** Active (domain renewed to 2030)
- **Ranking:** Consistently #1 or #2 most visited torrent site

### Overview

The Pirate Bay is the oldest and most resilient torrent site in history. Founded in 2003 by Gottfrid Svartholm, Fredrik Neij, and Peter Sunde under the Swedish Piratbyrån. Survived domain seizures, criminal prosecutions (founders convicted in 2009, appealed), hosting migrations across dozens of countries, and continuous ISP blocks globally.

TPB does not host any files — it is purely an index of torrent metadata (magnet links and .torrent files). The site uses search-only navigation with no mandatory account requirement for browsing.

### Key Features

- **Trusted/VIP uploaders:** Skull icons indicate trusted uploaders (pink skull = VIP, green skull = trusted). These are the most reliable uploads. Anonymous uploads without skulls have higher risk of fakes.
- **Browse by category:** Video (Movies, TV, HD Video, Video clips), Audio, Applications, Games, Porn, Other
- **Advanced search:** Filter by category, file type, age
- **RSS feeds:** Subscribe to categories or search queries for automatic new-release notification
- **No account required:** Browse and download without registration
- **Open registration:** Accounts allow commenting and uploading

### Magnet Link Example

```
# TPB search result → "Copy Magnet Link"
magnet:?xt=urn:btih:INFOHASH&dn=Movie+Name+2024+1080p+BluRay&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://open.tracker.cl:1337/announce
```

### Domain History

TPB has operated under dozens of domains over the years. The `.org` domain (`thepiratebay.org`) is the official primary domain. The `.com` and `.org` variants were sold at auction — `piratebay.org` sold for $50,000. The current domain registration extends to 2030, ensuring stability.

### Blocked Countries

TPB is ISP-blocked in the UK, Australia, Germany, France, Italy, India, Portugal, Spain, and many others. Access via VPN or the .onion address bypasses these blocks.

---

## 3. 1337x

- **Primary domains:** https://1337x.to, https://1337x.st, https://x1337x.ws, https://x1337x.eu
- **Onion:** `l337xdarkkaqfwzntnfk5bmoaroivtl6xsbatabvlb52umg6v3ch44yd.onion` (Beta)
- **Status page:** https://1337x-status.org
- **Founded:** 2007
- **Status:** Active — second most popular torrent site (TorrentFreak 2025)

### Overview

1337x is widely considered the most user-friendly torrent site with the cleanest interface. Gained dominance when KickassTorrents was seized in 2016. Known for being more strictly moderated than TPB — lower risk of fakes and malware.

### Key Features

- **Trending / Top 100:** Homepage shows trending torrents by category
- **Organized categories:** Movies, TV, Games, Music, Apps, Anime, Documentaries, Other
- **User accounts:** Uploaders have profiles and track records — check uploader history before downloading
- **Verified uploaders:** Trusted/VIP uploader badges for known reliable sources
- **Community reviews:** Comment sections help verify quality
- **Clean interface:** No deceptive fake download buttons (unlike some competitors)

### Domain Warning

`1337x.so` expired by mistake in May 2024 and is no longer controlled by 1337x. Use `1337x.to` (primary) or `1337x.st`. Always verify via the official status page: https://1337x-status.org

---

## 4. YTS (YIFY)

- **Primary domain:** https://yts.mx
- **Founded:** 2010 (original YIFY); current YTS group since ~2015
- **Status:** Active — specializes exclusively in movies
- **Specialization:** Movies only, compressed to smallest possible filesize at acceptable quality

### Overview

YTS specializes in releasing movie torrents in small file sizes with good visual quality using H.265/x265 encoding at multiple resolutions (720p, 1080p, 2160p). A 1080p BluRay movie that would typically be 15–50GB is often 1.5–3GB as a YTS release. This makes YTS extremely popular for users with limited bandwidth or storage.

### File Specifications

```
YTS release naming convention:
  Movie.Name.Year.Resolution.Source.Codec-YTS[MX]

  Movie.Name.2024.1080p.BluRay.x265-YTS
  Movie.Name.2024.2160p.4K.BluRay.x265.10bit-YTS

Typical sizes:
  720p  x264:   600MB – 1.2GB
  1080p x264:   1.5GB – 2.5GB
  1080p x265:   700MB – 1.5GB    ← Most popular (half size of x264)
  2160p x265:   3GB – 8GB        ← 4K HDR

Audio: typically AAC stereo or 5.1 Dolby Digital (not lossless like full BluRay rips)
Subtitles: separate .srt files included

YTS API:
  https://yts.mx/api/v2/list_movies.json?query_term=matrix&quality=1080p
  Returns JSON with torrent hashes, magnet links, metadata
```

### YTS API

```python
import requests

def search_yts(query, quality="1080p"):
    r = requests.get("https://yts.mx/api/v2/list_movies.json", params={
        "query_term": query,
        "quality": quality,
        "sort_by": "seeds"
    })
    data = r.json()
    for movie in data["data"]["movies"]:
        print(f"{movie['title']} ({movie['year']})")
        for torrent in movie["torrents"]:
            if torrent["quality"] == quality:
                print(f"  {torrent['quality']} | {torrent['size']} | Seeds: {torrent['seeds']}")
                print(f"  Magnet: magnet:?xt=urn:btih:{torrent['hash']}&dn={movie['slug']}")

search_yts("Dune", "1080p")
```

### Limitations

- Movies only — no TV shows, software, games, music
- Compressed audio (no lossless Atmos/TrueHD)
- Sometimes slow to release new films (quality over speed)
- For TV shows: use 1337x or TPB instead

---

## 5. RARBG — Shutdown (2023)

- **Status:** ⚠️ **PERMANENTLY SHUT DOWN — May 31, 2023**
- **Was at:** rarbg.to, rarbg.is (both dead)

### What Was RARBG

RARBG was founded in 2008 as a Bulgarian BitTorrent tracker and grew into one of the four most visited torrent sites in the world. It was particularly respected for:

- High-quality verified video releases
- Internal quality control (did not allow unverified uploads)
- Trusted internal groups (YIFY-quality compression)
- Clean interface with detailed torrent information
- Ranked #4 globally by TorrentFreak as recently as January 2023

### Why It Shut Down

On May 31, 2023, the RARBG team posted a final message explaining the shutdown: team members had died from COVID complications, others were still suffering from health issues, and some were involved on both sides of the war in Europe. Combined with energy price increases and inflation making data center costs unaffordable, the team voted unanimously to shut down permanently.

```
Final RARBG message (verbatim excerpt):
"Hello guys, We would like to inform you that we have decided to shut down
our site. The past 2 years have been very difficult for us – some of the
people in our team died due to covid complications, others still suffer
the side effects of it – not being able to work at all. Some are also
fighting the war in Europe – ON BOTH SIDES. Also, the power price increase
in data centers in Europe hit us pretty hard. Inflation makes our daily
expenses impossible to bare. After an unanimous vote we've decided that we
can no longer do it. We are sorry :( Bye"
```

### RARBG Replacements

The community migrated to:
- **1337x** — closest equivalent in quality and organization
- **TorrentGalaxy** — similar UI philosophy, active community
- **YTS** — for movies specifically (better compression)
- **The Pirate Bay** — broadest selection, longest history

No site has perfectly replicated RARBG's combination of quality control and breadth.

---

## 6. Torlock

- **Website:** https://www.torlock.com
- **Founded:** 2012
- **Status:** Active
- **Specialization:** General — movies, TV, music, apps, games, anime

### Overview

Torlock markets itself as a "verified torrent site" — it claims to vet uploads and remove fake and malicious torrents. Offers a $1 per fake torrent bounty to users who report fakes that are verified. Has a relatively clean interface and reasonable selection.

### Features

- Verified torrent badge system
- Large anime section
- No deceptive buttons (clear download links)
- Fast search
- Sort by seeds, age, size
- No account required for downloading

---

## 7. LimeTorrents

- **Website:** https://www.limetorrents.lol (domain changes; search for current)
- **Founded:** 2009
- **Status:** Active
- **Specialization:** General, with strong TV show and anime coverage

### Overview

LimeTorrents is a mid-tier general torrent index with a clean green-themed interface. Known for consistently maintaining uptime and keeping a steady flow of new uploads. Smaller selection than TPB or 1337x but reliable for mainstream content.

### Features

- Clean interface, easy navigation
- Categories: Movies, TV, Music, Games, Apps, Anime, Other
- Search across multiple trackers
- Verified health indicators (seeds/leechers clearly shown)
- RSS feeds available
- No account required

---

## 8. KickassTorrents (KAT)

- **Status:** Domain seized in 2016, community mirrors continue
- **Community mirrors:** kat.am, kickasstorrents.to, katcr.co (availability varies)
- **Founded:** 2008 (by Artem Vaulin, Ukraine)

### History

KickassTorrents was the #1 torrent site in the world in 2014–2016, briefly surpassing The Pirate Bay. In July 2016, the US Department of Justice arrested founder Artem Vaulin on copyright infringement charges. The official domains were seized and shut down.

The KAT community database was preserved by fans and relaunched as community mirrors. These mirrors are not operated by the original team and quality varies significantly.

### Current Status

The original KAT team is gone. Community mirrors exist but are inconsistently maintained. For equivalent functionality, 1337x is the recommended alternative (it grew largely because of KAT refugees post-seizure).

---

## 9. ETTV

- **Website:** https://www.ettv.to
- **Status page / alternative domains:** https://torrends.to/site/ettv
- **Specialization:** TV shows and movies — known for rapid releases

### Overview

ETTV is a torrent release group and indexing site primarily known for fast TV show releases. They often post episodes within hours of airing. Particularly known for:

- Fast TV episode releases (often within 1–2 hours of air)
- Consistent naming conventions (ETTV release group tag)
- Movies with HD quality
- SD and HD variants for each release

ETTV operates primarily as a release group — their content appears on all major torrent sites as ETTV-tagged releases. The ETTV site itself is an index of their own releases.

### Finding ETTV Content

```
# ETTV content appears on major sites tagged as:
# Show.Name.S01E01.720p.HDTV.x264-ETTV
# Show.Name.S01E01.1080p.WEB.H264-ETTV

# Check current domain via:
https://torrends.to/site/ettv
```

---

## 10. TorrentGalaxy (TGx)

- **Website:** https://torrentgalaxy.to, https://torrentgalaxy-official.is
- **Founded:** 2018 (post-RARBG community)
- **Status:** Active — one of the fastest-growing sites after RARBG shutdown

### Overview

TorrentGalaxy launched in 2018 with a modern Netflix-like interface and quickly grew in popularity. After RARBG's shutdown in 2023, many RARBG uploaders and community members migrated to TGx. It now has one of the more active communities among public torrent sites.

### Key Features

- **Modern interface:** Poster-based browsing with cover art (like a streaming site)
- **User comments:** Active discussion per torrent
- **Verified uploaders:** Internal verification system for trusted accounts
- **RSS feeds:** Subscribe to categories or uploaders
- **Multi-language content:** Good selection of non-English content
- **Categories:** Movies, TV, Music, Games, Apps, Anime, Documentaries, XXX, Other
- **Streaming preview:** Some content can be previewed in-browser

### Interface Style

TGx was designed to be more visually appealing than traditional torrent sites — browse movies by poster art, filter by genre, see IMDb ratings inline. This makes it one of the easiest torrent sites to casually browse.

---

## 11. Torrends.to

- **Website:** https://torrends.to
- **Type:** Torrent meta-aggregator / site status tracker — NOT a torrent site itself

### Overview

Torrends.to is a meta-site that tracks the status and current domains of dozens of torrent sites. It does not host torrents — it tells you:
- Which sites are currently up or down
- Current working domains for each site
- Status history
- Alternative/mirror domains

```
Use case:
  "Is 1337x down or is it just me?"
  → Go to torrends.to → check 1337x status → see all known working domains

  "RARBG isn't working"
  → torrends.to/site/rarbg → see shutdown notice + migration alternatives
```

---

## 12. Appdoze

- **Website:** https://appdoze.com
- **Type:** Software and application-focused torrent/direct download site
- **Specialization:** Windows software, macOS apps, Android APKs, PC games

### Overview

Appdoze is a software download site focusing on Windows applications, utilities, games, and mobile apps. It provides both direct download links and magnet/torrent links for software releases. Known in the warez community for hosting cracked/patched software releases.

### Content Categories

- Windows software (Adobe CC, Microsoft Office, creative tools, utilities)
- macOS applications
- Android APKs (patched/cracked apps)
- PC games (pre-cracked installers)
- Software tutorials

### Safety Considerations

```
Warning: Software from sites like Appdoze carries significant risk:
  - Cracks and patches can contain bundled malware
  - Keygens are frequently trojanized
  - Adobe/Microsoft cracks are high-value targets for malware distributors
  - Antivirus will flag most cracks (intentional — they modify executables)

If you use such software:
  - Run in a VM or isolated environment
  - Never enter real credentials after installing cracked software
  - Use a dedicated machine / VM for cracked software
  - Alternatives: legitimate free software (LibreOffice, GIMP, VLC, Kdenlive)
```

---

## 13. Site Comparison

| Site | Best For | Content | Quality Control | Status |
|------|---------|---------|-----------------|--------|
| **The Pirate Bay** | Everything, largest index | All categories | Skull/VIP system | Active |
| **1337x** | General, best UI | All categories | Moderated, VIP badges | Active |
| **YTS** | Movies (compressed) | Movies only | High (internal QC) | Active |
| **RARBG** | High-quality video | All categories | Excellent | ⚠️ Shutdown 2023 |
| **TorrentGalaxy** | Modern browsing, community | All categories | Growing community | Active |
| **KickassTorrents** | Legacy, mirrors only | All categories | Original team gone | Mirror only |
| **ETTV** | Fast TV releases | TV, Movies | Release group | Active |
| **Torlock** | Verified content | All categories | Verification badges | Active |
| **LimeTorrents** | TV shows, anime | All categories | Moderate | Active |
| **Appdoze** | Software, apps | Software only | Low (user uploads) | Active |
| **Torrends.to** | Site status / meta | N/A (meta-site) | N/A | Active |

### By Use Case

| Need | Go To |
|------|-------|
| Specific movie, want small file | YTS |
| Latest TV episode | ETTV or 1337x |
| Best general selection | 1337x or TPB |
| Most modern/visual browsing | TorrentGalaxy |
| Find current domain for any site | Torrends.to |
| Software/apps | 1337x (verified) or Appdoze (more selection, higher risk) |
| Anime | 1337x, Nyaa.si (specialized) |

---

## See Also

- [BitTorrent Technology](bittorrent-technology.md) — Protocol internals, DHT, magnet links
- [Deluge](deluge.md) — BitTorrent client setup and configuration
- [VPN & ZTNA](../networking/vpn-and-ztna.md) — VPN for private torrenting
- [Anime Streaming](../streaming/anime-streaming.md) — Legal and grey-area anime platforms
