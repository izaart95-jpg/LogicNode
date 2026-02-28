# Android PC Emulation & Compatibility Tools Documentation

This document explains the origin, purpose, features, and differences between:

- Winlator  
- XoDos  
- Vectras VM  
- Horizon Emulator  
- GameHub  

These tools are commonly used to run PC games or operating systems on Android devices.

---

# 1. Winlator

## Origin

Winlator is an Android application that allows users to run Windows (x86) applications and games on ARM-based Android devices.

- Based on: Wine + Box86/Box64
- Platform: Android
- Purpose: Run Windows software and games

Winlator gained popularity for enabling offline PC game execution without cloud streaming.

## How It Works

Winlator uses:
- Wine (Windows compatibility layer)
- Box86 / Box64 (x86-to-ARM translation)
- DXVK / VKD3D (DirectX → Vulkan translation)

This allows Windows games to run on Android using the device GPU.

## Features

- Runs many Windows games
- DirectX 9/10/11 support (via DXVK)
- Custom container system
- Adjustable GPU drivers (Turnip, VirGL)
- On-screen controls
- Gamepad support
- Offline execution (no cloud needed)

## Limitations

- Requires powerful device
- Compatibility varies
- High storage usage
- Some games crash or need tweaks

---

# 2. XoDos

## Origin

XoDos is an Android DOS emulator focused on running classic DOS games.

- Type: DOS Emulator
- Platform: Android
- Focus: Retro DOS gaming

It is similar in concept to DOSBox but packaged for easier Android usage.

## Features

- Runs classic DOS games
- Sound Blaster emulation
- Keyboard + mouse emulation
- Touch controls
- Low hardware requirements

## Best For

- 1990s DOS games
- Retro PC software
- Lightweight devices

## Limitations

- No modern Windows game support
- Limited 3D acceleration

---

# 3. Vectras VM

## Origin

Vectras VM is an Android virtualization tool based on QEMU technology.

- Based on: QEMU
- Platform: Android
- Purpose: Run full operating systems

It allows users to install Windows, Linux, and other OS images.

## Features

- Full OS virtualization
- Supports Windows XP/7 (better performance)
- Supports Linux distributions
- ISO boot support
- Disk image management
- Snapshot support

## Performance Notes

- Slower than Winlator for games
- CPU virtualization only (no strong GPU acceleration)
- Better for OS testing than gaming

## Limitations

- Heavy CPU usage
- Limited GPU acceleration
- Not ideal for modern games

---

# 4. Horizon Emulator

## Origin

Horizon Emulator is an Android-based tool designed to run Windows games using compatibility layers.

- Platform: Android
- Focus: Windows gaming compatibility

It is often compared to Winlator in purpose.

## Features

- Windows game container system
- Wine-based compatibility
- Touch control mapping
- Custom driver support
- Performance profiles

## Differences from Winlator

- Different UI
- Different container management
- May support different driver builds
- Compatibility may vary per game

---

# 5. GameHub

## Origin

GameHub is an Android gaming launcher environment designed to manage and run PC games via emulation layers.

- Platform: Android
- Purpose: Game management + execution

It often integrates with compatibility tools.

## Features

- Game library management
- Controller support
- Performance tuning profiles
- Touch overlay controls
- Game organization tools

## Not a Full Emulator

GameHub itself is usually:
- A launcher
- A management system
- A frontend

It may rely on:
- Wine
- Box86/Box64
- Other compatibility engines

---

# Comparison Table

| Feature | Winlator | XoDos | Vectras VM | Horizon Emulator | GameHub |
|----------|-----------|--------|-------------|------------------|----------|
| Windows Apps | Yes | No | Yes (via OS) | Yes | Yes (frontend) |
| DOS Games | Limited | Yes | Yes | Limited | Limited |
| Full OS Virtualization | No | No | Yes | No | No |
| DirectX Support | Yes | No | Limited | Yes | Depends |
| GPU Acceleration | Yes | No | Limited | Yes | Depends |
| Best For | Modern PC Games | Retro DOS | OS Testing | Windows Games | Game Management |

---

# Use Case Guide

- Want to run modern Windows games → Winlator or Horizon Emulator
- Want to run DOS games → XoDos
- Want to install full Windows OS → Vectras VM
- Want a launcher environment → GameHub

---

# Performance Requirements

For smooth usage:

- Snapdragon 865+ recommended for Winlator/Horizon
- 6GB+ RAM recommended
- Vulkan-supported GPU required for best performance
- Large internal storage recommended

---

# Final Summary

These Android tools allow users to transform smartphones into lightweight PC gaming environments.

- Winlator and Horizon focus on compatibility layers.
- Vectras VM focuses on full virtualization.
- XoDos focuses on retro gaming.
- GameHub focuses on organization and launching.

Performance and compatibility depend heavily on device hardware.