# Glazed Client

A Minecraft client focused on providing a clean, modern experience with a comprehensive module set for PvP and quality-of-life improvements.

- **Website:** https://glazedclient.com
- **Type:** Paid Minecraft client (injection-based)
- **Minecraft versions:** 1.8.9, 1.12.2, 1.16.5+
- **Platform:** Windows, macOS, Linux

---

## Table of Contents
1. [Overview](#1-overview)
2. [Features & Modules](#2-features--modules)
3. [Installation](#3-installation)
4. [GUI & Configuration](#4-gui--configuration)
5. [Comparison with Other Clients](#5-comparison-with-other-clients)

---

## 1. Overview

Glazed Client is a feature-rich Minecraft modification with emphasis on a polished user interface, smooth animation, and a broad module list covering combat, movement, render, and utility categories. It targets competitive PvP servers while also including quality-of-life modules for general play.

Glazed distinguishes itself with its clean GUI aesthetic — the module menu and HUD elements are designed to be visually cohesive rather than utilitarian. It is an injection-based client, meaning it runs alongside Minecraft without requiring Forge or Fabric.

---

## 2. Features & Modules

### Combat
- **AimAssist** — subtle aim correction toward nearest target with configurable FOV and speed
- **AutoClicker** — humanized CPS automation with jitter simulation
- **KillAura** — target tracking with range, speed, and FOV configuration
- **Reach** — extended attack range configuration
- **Velocity** — knockback reduction with horizontal/vertical percentage control
- **CritSpam** — automated critical hit timing
- **AutoArmor** — equips best available armor from inventory

### Movement
- **Sprint** — always sprint, legit sprint, or omni-directional sprint modes
- **NoFall** — prevents fall damage
- **Speed** — movement acceleration
- **Step** — step up blocks without jumping
- **Fly** — creative-style flight or glide mode
- **Scaffold** — automated block placement while bridging
- **NoSlow** — removes slowdown when eating/blocking

### Render
- **ESP** — player, mob, and item highlighting through walls
- **Chams** — model rendering overlay for players
- **Tracers** — directional lines to entities
- **FullBright** — maximum ambient light
- **Xray** — see through blocks to locate ores and caves
- **HUD** — modular HUD elements (coordinates, FPS, CPS, armor status, potion effects)
- **Breadcrumbs** — trail of blocks showing recent movement path
- **FreeLook** — rotate camera freely without affecting movement direction

### Utility
- **AutoEat** — automatic food consumption at configurable hunger level
- **AutoReconnect** — reconnects to server after disconnect
- **ChatFilter** — filter or modify chat messages
- **FakePlayer** — place a dummy player model for practice
- **PacketFly** — packet-based flight bypass for some anti-cheats
- **Timer** — adjusts game tick speed
- **NoRotate** — prevent server-forced rotation

---

## 3. Installation

```
1. Purchase at https://glazedclient.com
2. Download the Glazed launcher from your account dashboard
3. Open Minecraft to your desired version
4. Launch the Glazed injector with Minecraft open
5. In-game: use the configured keybind (default: Right Shift) to open the GUI
```

Glazed is injection-based — it does not modify game files on disk. Each session requires re-injection when Minecraft is launched. No Forge or Fabric installation is needed.

---

## 4. GUI & Configuration

Glazed features a click-based GUI with:

- **Module list** — scrollable categorized module list, click to toggle
- **Search** — type to filter modules by name
- **Config system** — save and load module configurations as named profiles
- **Bind manager** — assign keyboard shortcuts to any module
- **HUD editor** — drag-and-drop HUD element positioning
- **Theme customization** — accent color, font, and transparency options

```
# Common keybinds (defaults)
Right Shift    Open/close module GUI
Right Control  Open HUD editor
Insert         Toggle all enabled modules (panic key)
```

---

## 5. Comparison with Other Clients

| Feature | Glazed | Vape | Hydrogen | Raven B+ |
|---------|--------|------|----------|----------|
| **Price** | Paid | ~$35 | Free | Free |
| **Open source** | ❌ | ❌ | ✅ | ✅ (forks) |
| **Injection type** | Injection | Injection | Forge mod | Forge mod |
| **MC versions** | Multi | Multi | 1.8.9 | 1.8.9 |
| **GUI quality** | Modern | Standard | Standard | Standard |
| **Module count** | 50+ | 40+ | 50+ | 40+ |

---

## See Also

- [Ghost Clients](ghost-clients.md) — Vape, Raven B+, Hydrogen, Vestige — other PvP clients
- [Utility Clients](utility-clients.md) — Meteor Client, Baritone — open-source utility mods
- [Servers](servers.md) — FakePixel and other server networks
