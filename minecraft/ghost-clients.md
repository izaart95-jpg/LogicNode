# Minecraft Ghost Clients — Vape, Raven B+, Hydrogen & Vestige

Ghost clients are Minecraft modifications designed to give players advantages in PvP while appearing to play normally — the modifications are "invisible" to spectators and recording software. They are primarily used on servers like Hypixel where blatant hacking is detectable but subtle enhancements may pass anti-cheat checks.

> **Server Rules Notice:** Using ghost clients on servers that prohibit modifications will result in bans if detected. These tools are documented here for educational and research purposes. The existence of these clients is publicly known and discussed in the Minecraft community.

---

## Table of Contents
1. [Ghost Client Concepts](#1-ghost-client-concepts)
2. [Vape](#2-vape)
3. [Raven B+](#3-raven-b)
4. [Hydrogen Client](#4-hydrogen-client)
5. [Vestige](#5-vestige)
6. [Comparison Table](#6-comparison-table)

---

## 1. Ghost Client Concepts

### What Makes a Client "Ghost"

A ghost client provides subtle PvP advantages designed to mimic natural human behavior:

- **AimAssist:** Slightly corrects aim toward targets — not snapping like KillAura, but barely perceptible micro-corrections
- **AutoClicker:** Clicks at a consistent high CPS (clicks per second) with humanized timing variance
- **Reach:** Extends attack range by a fraction of a block (e.g., 3.2 blocks instead of 3.0)
- **Velocity:** Reduces knockback received, maintaining positioning after being hit
- **WTap / FakeLag:** Timing tricks that affect hit registration

### Ghost vs Utility Clients

| Type | Examples | Visibility | Use Case |
|------|---------|-----------|---------|
| **Ghost** | Vape, Raven B+ | Undetectable to spectators | Competitive servers (Hypixel) |
| **Utility** | Meteor, Wurst | Visually obvious (ESP, flying) | Anarchy servers (2b2t) |
| **Semi-legit** | Raven B+, Vestige | Subtle | Semi-competitive, mixed |

### Anti-Cheat Landscape

| Anti-Cheat | Server | Detection Strength |
|-----------|--------|-------------------|
| **Watchdog** | Hypixel | Moderate (bans obvious cheats) |
| **Grim** | Many servers | Strong statistical analysis |
| **Intave** | Private servers | Strong |
| **Matrix** | Wide use | Moderate |
| **NCP** (NoCheatPlus) | Bukkit/Spigot | Weak, easily bypassed |

---

## 2. Vape

- **Website:** https://www.vape.gg
- **Type:** Ghost client — injection-based
- **Price:** ~$35 (one-time purchase)
- **Versions:** 1.7, 1.8.9, 1.12+
- **Developer:** Manthe (since 2015)

### Overview

Vape is described as the oldest continuously active Minecraft ghost client, in development since 2015. Vape is designed specifically for the closet cheater, giving you undetectable advantages in combat. It is an injection client — it doesn't require Forge or Fabric installation and instead injects directly into the running Minecraft process at launch.

Our combat modules are designed to last, built to work on any anticheat without relying on temporary bypasses. Rather than using short-term bypasses that get patched, Vape's modules are designed from the ground up to replicate human behavior.

### Key Features

- **Injection-based:** No mod installation — run Vape alongside Minecraft without modifying the game files
- **AimAssist:** Subtle aim correction with full cursor control retention
- **AutoClicker:** Humanized CPS patterns
- **Reach:** Configurable extended reach
- **WTap:** Automatic W-tap (sprinting reset) timing for combo maintenance
- **AutoArmor:** Equips best available armor automatically
- **Velocity:** Configurable knockback reduction
- **Timer:** Controls game tick rate for speed effects
- **HUD modules:** Keystrokes display, FPS, CPS, coordinates, armor status
- **Freelook:** Look around while movement remains forward
- **NoClickDelay:** Removes the 1-tick delay between clicks

### Installation

```
1. Purchase Vape at https://www.vape.gg
2. Download the Vape launcher from the client dashboard
3. Open Minecraft (any supported version)
4. Launch Vape — it injects into the running Minecraft process
5. In-game: Right-click tray icon or use the configured keybind to open GUI
```

Vape is safe for your main account — alt accounts are not required. The launch process is designed to be simple, you simply download and run Vape while you have Minecraft open. There is no formal installation process since Vape is an injection client and only modifies your game at run time.

### Versions

- **Vape V4:** Current version, actively maintained for 1.8.9 and modern versions
- **Vape Lite:** Lighter version with fewer modules, lower price

---

## 3. Raven B+

- **Type:** Free Forge mod / ghost client
- **Minecraft version:** 1.8.9
- **Source:** Multiple open-source forks exist on GitHub
- **Primary site:** https://k-ov.github.io/ (Raven B++)

### Overview

Raven B+ is a free, Forge-based ghost client for Minecraft 1.8.9, focused on Hypixel PvP. Raven b++ is a pvp client and utility mod for minecraft 1.8.x. It supports Forge and Feather adding quality of life improvements, bug fixes, and so much more. It is community-maintained with multiple active forks.

### Key Features

- Free and open source (multiple forks)
- Forge-based — installs as a standard .jar mod
- AimAssist, AutoClicker, Reach, Velocity modules
- Sprint-Scaffold for bridging
- BowLongJump
- Legit aura (subtle KillAura within normal-looking parameters)
- ClickGUI for module management
- Custom HUD elements (keystrokes, CPS, FPS)
- Feather client compatible

### Installation

```
Prerequisites: Minecraft Forge for 1.8.9
  Download Forge from: https://files.minecraftforge.net (version 1.8.9)

1. Download the Raven B++ jar from https://k-ov.github.io/download/
   (or from a GitHub release of any fork)
2. Place the .jar in .minecraft/mods/
   Windows: %appdata%\.minecraft\mods\
   macOS: ~/Library/Application Support/minecraft/mods/
3. Launch Minecraft with Forge 1.8.9 profile
4. Open the GUI with Left Shift (default)
```

### Notable Forks

| Fork | Notes |
|------|-------|
| **Raven B++** (k-ov) | Most maintained, stable version |
| **Raven XD** (xia-mc) | Extended beyond Hypixel focus |
| **Raven B+** (xXxVPNxXx) | Basic version, 1.8.9 only |

---

## 4. Hydrogen Client

- **Website:** https://zpeanut.github.io
- **Repository:** https://github.com/zPeanut/Hydrogen
- **License:** Open source
- **Type:** Open-source Forge ghost client
- **Minecraft version:** 1.8.9

### Overview

Hydrogen is an advanced ghost client for Minecraft version 1.8.9, based on Minecraft Forge. Hydrogen is made for the purpose of giving yourself various utilities, which all give you an advantage without anyone noticing it, including many render related modules.

Hydrogen is completely open-source, hosted on our GitHub. No sneaky bitcoin-miners and IP-Loggers.

There are currently over 50 modules included in Hydrogen, including a fully customizable in-game GUI, as well as various render, combat and utility focused modules.

### Key Features

- **50+ modules** across combat, render, movement, and utility categories
- **Open source** — full code available on GitHub, no hidden payloads
- **Customizable GUI** — font selection, theme customization (Classic, Tephra layouts)
- **Pre-1.8 visual modules** — restores removed visual behaviors (2D dropped items, old bow animation, armor damage visual)
- **Fuzzy game name search** for finding modules quickly
- **Forge-based** — standard mod installation

### Module Highlights

**Combat:** AimAssist, AutoClicker, Reach, Velocity, KillAura (legit mode), Criticals

**Render:** ESP, Tracers, FullBright, ChestESP, PlayerESP, Nametags

**Movement:** Sprint, NoFall, Step, LongJump

**Utility:** AutoArmor, AutoEat, FreeCam, NameProtect (disguise your username in your own HUD)

**Pre-1.8 Cosmetics:**
- Bow — scales bow back to pre-1.8 style
- Third-person Block — blocking looks like pre-1.8
- Dropped Items — makes dropped items appear 2D (pre-1.8 style)

### Installation

```bash
# Prerequisites: Forge 1.8.9
# Download Forge: https://files.minecraftforge.net/net/minecraftforge/forge/index_1.8.9.html

# Option 1: Pre-built jar (recommended)
# Download from: https://github.com/zPeanut/Hydrogen/releases
# Place hydrogen-X.X.X.jar in .minecraft/mods/
# Launch with Forge 1.8.9

# Option 2: Build from source
git clone https://github.com/zPeanut/Hydrogen.git
cd Hydrogen
# Open in IntelliJ IDEA
./gradlew setupDecompWorkspace idea
./gradlew build
# Output jar is in build/libs/
```

---

## 5. Vestige

- **Website:** https://vestige.my.canva.site
- **Type:** Paid ghost client
- **Minecraft version:** 1.8.9
- **Developer:** YesCheatPlus

### Overview

Vestige is an affordable and multi-server client. It includes hypixel bypasses such as a strafe and timer disabler, a bow longjump and a sprint scaffold. It also includes redesky, minemenclub, ncp and aac bypasses.

Vestige is notable for its multi-server focus — it includes specific bypass profiles for several different servers, not just Hypixel. It has gained popularity among players for its features and performance including scaffold, auto block, and ghost modules, especially in blade mode.

### Key Features

- Multi-server bypass profiles (Hypixel, RedesKy, MineMenClub, NCP, AAC servers)
- Scaffold (automated bridging)
- SprintScaffold (bridging while sprinting)
- BowLongJump
- Strafe and Timer disabler (Hypixel-specific)
- AutoBlock
- Ghost modules (subtle PvP enhancements)
- Blade mode (specialized fast-attack configuration)

### Pricing

Vestige has both a free and paid version. The free version is no longer being updated. Paid version available via their Discord community.

### Note on Free Version

The free version is deprecated — if you wish to receive updates, the paid version is required. The exact current pricing and download location is provided through their Discord server linked on the Canva website.

---

## 6. Comparison Table

| Client | Price | Type | MC Version | Open Source | Primary Use |
|--------|-------|------|-----------|-------------|-------------|
| **Vape** | ~$35 | Injection | 1.7/1.8.9/1.12+ | ❌ | Hypixel, ghost cheating |
| **Raven B+** | Free | Forge mod | 1.8.9 | ✅ (forks) | Hypixel BedWars/SkyWars |
| **Hydrogen** | Free | Forge mod | 1.8.9 | ✅ | Ghost cheating, render mods |
| **Vestige** | Free/Paid | Client | 1.8.9 | ❌ | Multi-server bypass |
| **Meteor Client** | Free | Fabric mod | Latest | ✅ | Anarchy, utility |

### Which to Use?

| Scenario | Recommendation |
|----------|---------------|
| Budget-conscious, open source | **Hydrogen** or **Raven B++** |
| Maximum anti-cheat bypass (paid) | **Vape** |
| Multi-server support | **Vestige** |
| Modern Minecraft / anarchy | **Meteor Client** (see utility-clients.md) |
| Learning / source code study | **Hydrogen** (best code quality for a ghost client) |

---

## See Also

- [Utility Clients](utility-clients.md) — Meteor Client, Baritone — open utility mods for anarchy servers
- [Minecraft Servers](servers.md) — FakePixel and other Minecraft server networks
- [Frameworks & Libraries](../devtools/frameworks-and-libraries.md) — Mineflayer, go-mc for Minecraft bot development
