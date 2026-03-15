# Minecraft Server Networks

This document covers notable Minecraft server networks — third-party multiplayer servers that run game modes beyond vanilla Minecraft. Includes FakePixel (a free Hypixel alternative) and context on major server types.

---

## Table of Contents
1. [Minecraft Server Types](#1-minecraft-server-types)
2. [FakePixel](#2-fakepixel)
3. [Other Notable Networks](#3-other-notable-networks)
4. [Connecting to Servers](#4-connecting-to-servers)
5. [Server Software](#5-server-software)

---

## 1. Minecraft Server Types

| Type | Description | Examples |
|------|-------------|---------|
| **Minigame Network** | Multiple game modes in one network | Hypixel, FakePixel |
| **Anarchy** | No rules, no bans, anything goes | 2b2t, 9b9t |
| **Survival** | Standard survival, may have economies | Many community servers |
| **SkyBlock** | Island-based progression server | Hypixel SkyBlock, FakePixel SkyBlock |
| **Prison** | Mine to earn money, rank up | Traditional prison servers |
| **Factions** | Team-based land claiming, raiding | Classic faction servers |
| **Creative** | Building focus, plot-based | PlotSquared servers |
| **PvP** | Combat-focused, arena or open world | Practice servers |

---

## 2. FakePixel

- **IP:** `fakepixel.fun` (also `mc.fakepixel.fun`)
- **Version support:** 1.8 through 1.21
- **Website/Discord:** Search "FakePixel Minecraft" for current links
- **Type:** Free Hypixel alternative network
- **Players:** Up to 3,000 concurrent

### Overview

FakePixel is a free-to-play Minecraft network that replicates Hypixel's game modes without requiring a paid Minecraft account for some versions. It is explicitly positioned as an alternative to Hypixel for players who want the same game modes without the cost barrier. Every component belongs to the Hypixel Inc. and Hypixel Studios, including the visual design — FakePixel does not claim affiliation.

### Game Modes

| Game Mode | Description |
|-----------|-------------|
| **BedWars** | Team-based game — destroy enemy beds to prevent respawning, eliminate all teams |
| **SkyWars** | Players on separate islands collect resources and fight to be last standing |
| **SkyBlock** | Private island progression — farming, mining, crafting economy |
| **BuildFFA** | Build mode free-for-all combat |
| **Survival Games** | Hunger Games-style battle royale |
| **Parkour** | Movement challenge courses |
| **Minigames** | Various smaller game modes |

### Why Play FakePixel Instead of Hypixel?

| Reason | Detail |
|--------|--------|
| **No Java license required** (some builds) | FakePixel has historically allowed cracked (non-premium) accounts |
| **No queue times** | Hypixel has peak-time queues; FakePixel's smaller population means immediate joins |
| **Ghost client friendly** | FakePixel's anti-cheat is less strict than Hypixel's Watchdog |
| **Testing ground** | Safe to test clients, configs, and settings before using on Hypixel |
| **Free progression** | Ranks and cosmetics are more accessible |

### Anti-Cheat

FakePixel runs less aggressive anti-cheat than Hypixel. This makes it popular in the ghost client community for testing configurations and settings before applying them on stricter servers.

### Connecting

```
Java Edition:
  1. Open Minecraft (version 1.8 through 1.21 supported)
  2. Multiplayer → Add Server
  3. Server Address: fakepixel.fun
  4. Join Server

Alternative IPs (if main is down):
  mc.fakepixel.fun
  play.fakepixel.fun
```

---

## 3. Other Notable Networks

### Hypixel (The Original)
- **IP:** `mc.hypixel.net`
- **Version:** Java Edition 1.8–1.21
- **Note:** Requires paid Java Edition account
- **Anti-cheat:** Watchdog (strict for obvious cheats)
- **Player count:** Up to 200,000 concurrent — largest Minecraft server in the world
- **Notable modes:** SkyBlock (most complex game mode on any server), BedWars, SkyWars, Duels

### 2b2t (Anarchy)
- **IP:** `2b2t.org`
- **Type:** Oldest active anarchy server (since 2010)
- **Rules:** None — no bans, no rules enforced
- **Version:** 1.12.2 (stable, rarely updated intentionally)
- **Queue:** Long queue times for non-priority accounts
- **Notable for:** History, exploration, mega bases, griefing

### MineMenClub
- **IP:** `minemen.club`
- **Type:** Practice PvP server
- **Focus:** 1v1 duels, ranked ladder, combo/sword PvP
- **Notable:** Popular for testing aim and PvP settings with ghost clients

### RedesKy
- **IP:** `redesky.com`
- **Type:** Spanish-language BedWars/SkyWars network
- **Notable:** Has dedicated bypass profiles in several ghost clients

---

## 4. Connecting to Servers

### Version Compatibility

Most networks support a range of Minecraft versions. If you need to join a server running a different version:

```bash
# ViaFabric — connect to any version server from any client version
# Install alongside Meteor Client or any Fabric client
# Download: https://github.com/ViaVersion/ViaFabric

# ViaForge — same for Forge clients
# Download: https://viaversion.com

# Example: Join a 1.8.9 server from 1.21 Minecraft client
# Install ViaFabric → launch 1.21 → connect to 1.8.9 server
```

### Performance Tips

```
# Optimal settings for PvP servers:
- Set render distance to 2-4 chunks (reduces network load)
- Disable Smooth Lighting for better FPS
- Use OptiFine or Sodium for performance
- Set max FPS to 60 or Unlimited depending on monitor
- Disable VSync for minimum input latency

# Network settings:
- Use Ethernet rather than WiFi (reduces packet loss)
- Close background applications consuming bandwidth
- Choose server regions geographically close to you
```

---

## 5. Server Software

If you want to run your own server:

| Software | Type | Notes |
|----------|------|-------|
| **Paper** | High-performance Bukkit | Most popular for plugin servers |
| **Fabric** | Mod support | Best for mods (not plugins) |
| **Forge** | Mod support | Legacy mod ecosystem |
| **Velocity** | Proxy | Connect multiple backend servers as one network |
| **BungeeCord** | Proxy | Older network proxy (use Velocity instead) |
| **Minestom** | From scratch | Java API, no Minecraft code — for complete custom servers |

```bash
# Run a basic Paper server
java -Xmx2G -Xms2G -jar paper-1.21.jar --nogui

# Run with Docker
docker run -d \
  -p 25565:25565 \
  -e EULA=TRUE \
  -e TYPE=PAPER \
  -v minecraft_data:/data \
  itzg/minecraft-server
```

---

## See Also

- [Utility Clients](utility-clients.md) — Meteor Client, Baritone — open-source utility mods
- [Ghost Clients](ghost-clients.md) — Vape, Raven B+, Hydrogen, Vestige — PvP ghost clients
- [Frameworks & Libraries](../devtools/frameworks-and-libraries.md) — Mineflayer, go-mc — programmatic Minecraft clients
