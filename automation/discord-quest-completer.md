# Discord Quest Completer

A Windows desktop application that completes Discord Quests by faking game presence — without installing the actual games. Uses Discord's Rich Presence system to make Discord believe a game is running.

- **Repository:** https://github.com/markterence/discord-quest-completer
- **Author:** markterence
- **License:** MIT
- **Platform:** Windows only (Linux/macOS not supported)
- **Built with:** Tauri (Rust + Vue.js), dummy game executable

> **Disclaimer:** This tool operates in a gray area with Discord's Terms of Service. Use at your own risk. The author is not affiliated with Discord Inc. Account suspension is possible. Use on alt accounts if concerned.

---

## Table of Contents
1. [What are Discord Quests?](#1-what-are-discord-quests)
2. [How It Works](#2-how-it-works)
3. [Installation](#3-installation)
4. [Usage](#4-usage)
5. [How Discord Detection Works](#5-how-discord-detection-works)
6. [Limitations](#6-limitations)

---

## 1. What are Discord Quests?

Discord Quests are time-limited promotional activities where Discord rewards users (typically with profile decorations, avatar frames, or Nitro credits) for playing sponsored games for a set duration — commonly 15 minutes. The quests are visible in the Discord app under the gift/quest icon.

**The problem Discord Quest Completer solves:** Many quests require games that are large downloads (10–100+ GB), require specific hardware, use invasive anti-cheat software, or simply aren't games the user wants to install. This tool lets you claim the reward without the installation.

---

## 2. How It Works

```
Discord Quest Completer
  → launches a tiny dummy .exe named after the required game
  → dummy exe creates a visible window (required for Discord detection)
  → Discord's game detection scans running processes by name
  → Discord sees the "game" running → activates quest timer
  → after 15 minutes → quest reward is credited
```

The application:
1. Fetches Discord's list of detectable games from their API (`/api/applications/detectable`)
2. Lets you search and select the quest's required game
3. Launches a small dummy executable renamed to match the game's process name
4. Discord detects the process → shows "Playing X" on your profile → quest timer starts
5. You close it after the required time

The dummy exe is a minimal Windows application (~100KB) that creates a window. It contains no game code whatsoever.

---

## 3. Installation

```
1. Go to: https://github.com/markterence/discord-quest-completer/releases
2. Download the latest portable build (.zip)
3. Extract to a folder where you have write permissions
   (NOT C:\Program Files\ — the app creates files in its own directory)
4. Run discord-quest-completer.exe
```

**Important:** Do not extract to a write-protected directory. The app writes dummy game folders relative to its own location to simulate an installed game for Discord to detect.

**Build from source:**
```bash
# Prerequisites: Node.js, Rust, Tauri CLI
git clone https://github.com/markterence/discord-quest-completer.git
cd discord-quest-completer

npm install
npm run tauri dev      # Development
npm run tauri build    # Production build
```

---

## 4. Usage

1. **Open Discord** — make sure Discord is running and you're logged in
2. **Check your active quest** — Discord app → gift icon → see which game is required
3. **Open Discord Quest Completer**
4. **Search for the game** — type the game name in the search box (uses fuzzy search)
5. **Click Launch** — the dummy game starts running in the background
6. **Wait** — Discord shows "Playing [Game]" on your profile; quest timer runs
7. **Close after quest completes** — right-click the system tray icon → Quit

**System tray behavior:**
- The dummy exe runs minimized to the system tray
- Right-click tray icon → Show (makes window visible, may help if Discord doesn't detect)
- Right-click tray icon → Quit (stops the dummy process)

**Game list:**
The app fetches Discord's detectable game list on startup from the repository's GitHub Pages (updated daily). If that fails, it falls back to Discord's API directly, then to the bundled list included with the app.

---

## 5. How Discord Detection Works

Discord scans running processes on your system at regular intervals. For each running process, it checks the executable name against its internal database of ~10,000+ detectable games. When a match is found:

- Discord shows "Playing [Game Name]" on your status
- Your activity appears in your profile
- Quest timers activate if that game has an active quest

Discord Quest Completer exploits this by running a process with the exact executable name Discord expects. No game code, no network connections to game servers — just a process name match.

```
Discord's detection (simplified):
  for each running_process in system_processes:
    if running_process.name in discord_detectable_games:
      show_rich_presence(running_process.game_name)
      activate_quest_if_applicable()
```

---

## 6. Limitations

**Windows only:** Discord's game detection works differently on Linux and macOS. The author has stated Linux support may come later; macOS support is not planned.

**Quest-specific:** Works for "Play game for X minutes" quests. Does not work for quests requiring actual gameplay milestones (e.g., "complete a match," "reach level 5").

**Discord may patch this:** Discord can update their detection to require additional signals beyond process name (e.g., checking window class, verifying game files exist at expected paths, anti-cheat presence). If patched, dummy processes may no longer trigger quest completion.

**ToS risk:** Using this tool likely violates Discord's Terms of Service. The risk of account action appears low currently (it's just process name spoofing), but is not zero.

**Antivirus false positives:** Security software may flag the dummy executable as suspicious because it's an unknown unsigned executable that masquerades as a game. The source code is open and auditable on GitHub.

---

## See Also

- [Workflow Automation](workflow-automation.md) — n8n, Tasker, MacroDroid for broader automation
- [Web Automation](web-automation.md) — Playwright, Selenium for browser-based automation
- [Platforms & Communities](../reference/platforms-and-communities.md) — Discord as a community platform
