# Minecraft Utility Clients — Meteor Client & Baritone

This document covers open-source Minecraft utility mods designed for anarchy servers, automation, and advanced gameplay. These tools are openly distributed and widely used on servers that permit or do not restrict client-side modifications.

> **Server Rules Notice:** Using utility clients or automation bots on servers that prohibit them can result in bans. Always check a server's rules before using these tools. They are intended for single-player use, anarchy servers (like 2b2t), or servers that explicitly permit client modifications.

---

## Table of Contents
1. [Meteor Client](#1-meteor-client)
2. [Baritone](#2-baritone)
3. [Comparison Table](#3-comparison-table)

---

## 1. Meteor Client

- **Website:** https://meteorclient.com
- **Repository:** https://github.com/MeteorDevelopment/meteor-client
- **License:** GPL v3
- **Type:** Fabric utility mod
- **Minecraft version:** Latest stable (tracks Minecraft releases)
- **Stars:** 4,000+

### Overview

Meteor Client is a Minecraft Fabric utility mod designed for anarchy servers. Launched in 2021, the Meteor client is specifically designed for Java Edition, offering a suite of features that cater to a variety of playstyles, with a notable focus on PvP combat and anarchy servers. It is open-source under GPL v3, meaning all source code is publicly auditable and forks must remain open source.

### Installation

```
Prerequisites: Fabric Loader + Fabric API for the target Minecraft version

1. Download Fabric Loader from https://fabricmc.net/use/installer/
2. Install it for the Minecraft version matching Meteor's current release
3. Download Meteor Client .jar from https://meteorclient.com
4. Place the .jar in your .minecraft/mods/ folder
5. Launch Minecraft with the Fabric profile
6. In-game: press Right Shift to open the Meteor GUI
```

### Module System

Meteor organizes features into modules across categories. Meteor Client comes with an extremely customizable GUI and HUD giving you a beautiful but functional interface to interact with as well as the powerful macros system which allows you to change almost anything about the client in the press of a key.

**Combat modules:**
Modules like AutoAnvil, AnchorAura, BedAura, CrystalAura, and KillAura provide players with a considerable advantage in combat, offering offensive and defensive enhancements.

**Exploration and movement:**
Features such as ESP, Fly, Kill Aura, NoFall, and NoClip allow for improved navigation, strategic positioning, and safe exploration within the game world.

**Module categories:**

| Category | Examples |
|----------|---------|
| **Combat** | KillAura, CrystalAura, BedAura, AnchorAura, AutoTotem |
| **Movement** | Fly, NoFall, Speed, Sprint, Step, Jesus (walk on water) |
| **Render** | ESP, Xray, Fullbright, FreeLook, Tracers |
| **World** | AutoMine, InfinityMiner, Nuker, Timer |
| **Player** | AutoEat, AutoArmor, AutoFish, Freecam |
| **Misc** | AntiAFK, AutoReconnect, ChatFilter, FakePlayer |
| **HUD** | Customizable overlay elements (coords, speed, lag meter, inventory) |

### Baritone Integration

Meteor comes with Baritone built in, you don't need to download a standalone baritone. Baritone's default command prefix is #. This means all Baritone pathfinding commands work directly inside Meteor without separate installation.

### Addons

Meteor supports third-party addons — additional modules distributed separately from the main client. Community addons extend functionality with modules the Meteor team won't officially include (e.g., griefing-specific features). Addons are placed in `.minecraft/meteor-client/addons/`.

### Configuration

```
# In-game commands (prefix: .)
.help                   List all commands
.modules                List all modules
.toggle <module>        Toggle a module on/off
.bind <module> <key>    Bind a key to a module
.config <module> get    View a module's settings

# Baritone commands (prefix: #)
#goto 1000 500          Walk to coordinates (X=1000, Z=500)
#mine diamond_ore       Mine diamond ore automatically
#follow player          Follow a player
#stop                   Stop current Baritone task
```

### ViaFabric Compatibility

You can use ViaFabric if you want to connect to servers running other versions of Minecraft. Install ViaFabric alongside Meteor to connect to servers running older or different Minecraft versions.

---

## 2. Baritone

- **Repository:** https://github.com/cabaletta/baritone
- **License:** LGPL v3
- **Author:** leijurv (cabaletta)
- **Type:** Pathfinding bot — standalone or embedded in clients
- **Nickname:** "Google Maps for block game"

### Overview

Baritone is a Minecraft pathfinder bot and is the pathfinding system used in Impact since 4.4. It is an A* (A-star) pathfinding implementation for Minecraft that allows the game to navigate the world autonomously — walking to coordinates, mining specific ores, building from schematics, and farming — all without player input.

Baritone focuses on reliability and particularly performance — it's over 30x faster than MineBot at calculating paths.

### Getting Started

Baritone is bundled with Meteor Client, Impact, and several other utility clients — if you're using one of those, Baritone is already available. For standalone installation:

```
Fabric (1.16.5+):
  Download baritone-api-fabric-X.X.X.jar from GitHub Releases
  Place in .minecraft/mods/ with Fabric Loader

Forge (legacy versions):
  Download baritone-api-forge-X.X.X.jar from GitHub Releases
  Place in .minecraft/mods/ with Forge

Standalone (Impact client):
  Impact comes with Baritone pre-installed
  https://impactclient.net
```

### Core Commands

All Baritone commands use the `#` prefix by default:

```bash
# Navigation
#goto 1000 64 500        # Walk to X=1000, Y=64, Z=500
#goto 1000 500           # Walk to X=1000, Z=500 (ignores Y)
#goal 1000 500           # Set destination without starting
#path                    # Start pathing toward current goal
#stop                    # Stop all current tasks
#cancel                  # Cancel and clear goal

# Mining
#mine diamond_ore        # Find and mine diamond ore
#mine iron_ore gold_ore  # Mine multiple block types
#mining                  # Check mining progress

# Farming / Gathering
#farm                    # Auto-farm crops in an area
#follow playername       # Follow a player
#follow                  # Follow nothing (stop following)

# Building
#schematic load path/to/schematic.litematic
#build                   # Build loaded schematic at current position
#sel                     # Make a selection for building

# Elytra
#elytra                  # Use elytra to fly in the Nether (uses fireworks)

# Utilities
#come                    # Path back to where you started
#invert                  # Invert the current goal (walk away from it)
#blacklist               # Blacklist the current block type from mining
#save name               # Save current location as a named waypoint
#goto name               # Go to a saved waypoint
```

### Key Settings

Baritone has over 100 configurable settings. The most commonly adjusted:

```bash
# In-game: #set settingName value

#set allowSprint true           # Sprint while pathfinding (default: true)
#set allowParkour true          # Jump across gaps (default: true)
#set allowBreak true            # Break blocks in the way (default: true)
#set allowPlace true            # Place blocks to bridge gaps (default: true)
#set chatDebug false            # Hide debug messages in chat
#set renderPath true            # Show planned path visually
#set followRadius 3             # Distance to maintain when following
#set mineScanDroppedItems true  # Pick up dropped items while mining
```

### Java API

Baritone exposes a well-documented API for mod developers:

```java
// Set a pathfinding goal and start
BaritoneAPI.getSettings().allowSprint.value = true;
BaritoneAPI.getProvider()
    .getPrimaryBaritone()
    .getCustomGoalProcess()
    .setGoalAndPath(new GoalXZ(10000, 20000));

// Mine specific blocks
BaritoneAPI.getProvider()
    .getPrimaryBaritone()
    .getMineProcess()
    .mine(Blocks.DIAMOND_ORE, Blocks.DEEPSLATE_DIAMOND_ORE);

// Stop everything
BaritoneAPI.getProvider()
    .getPrimaryBaritone()
    .getPathingBehavior()
    .cancelEverything();
```

### Pathfinding Algorithm

Baritone uses a modified A* algorithm that accounts for Minecraft-specific costs:

- Block breaking time (based on tool, enchantments, efficiency)
- Falling block awareness (gravel/sand stacks above target blocks)
- Liquid avoidance (won't break blocks adjacent to lava/water by default)
- Fire and magma block avoidance
- Fall damage calculation
- Parkour jumps across gaps
- Bridging over gaps when blocks are available

---

## 3. Comparison Table

| Feature | Meteor Client | Baritone |
|---------|--------------|---------|
| **Type** | Full utility mod (modules + HUD) | Pathfinding bot / API |
| **Primary use** | PvP, anarchy, automation | Navigation, mining, farming automation |
| **Loader** | Fabric | Fabric, Forge, standalone |
| **Open source** | ✅ GPL v3 | ✅ LGPL v3 |
| **Baritone included** | ✅ Built-in | It IS Baritone |
| **GUI** | Full in-game clickable GUI | Command-based (`#` prefix) |
| **Minecraft version** | Latest (tracks releases) | 1.12.2 to latest |
| **API available** | ✅ Addon system | ✅ Java API |
| **Use case** | Anarchy servers, PvP advantage | Automation, navigation, botting |

---

## See Also

- [Ghost Clients](ghost-clients.md) — Vape, Raven B+, Hydrogen, Vestige — stealth PvP clients
- [Minecraft Servers](servers.md) — FakePixel and other Minecraft server networks
- [Frameworks & Libraries](../devtools/frameworks-and-libraries.md) — Mineflayer, minecraft-protocol, go-mc for bot development
