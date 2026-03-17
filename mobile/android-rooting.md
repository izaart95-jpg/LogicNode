# Rooting Android

Rooting gives you superuser (root) access on Android — the ability to run commands as `uid=0`, modify system partitions, and install software that requires privileged access. This document covers what root is, how it works, major rooting methods, and what you can do with it.

> **Warning:** Rooting voids warranties, may trip Knox/SafetyNet/Play Integrity, can brick your device if done incorrectly, and removes some security guarantees. Proceed with full understanding.

---

## Table of Contents
1. [What Root Access Is](#1-what-root-access-is)
2. [Before You Root](#2-before-you-root)
3. [Bootloader Unlocking](#3-bootloader-unlocking)
4. [Magisk — The Standard Root Method](#4-magisk--the-standard-root-method)
5. [KernelSU](#5-kernelsu)
6. [APatch](#6-apatch)
7. [Custom Recovery — TWRP](#7-custom-recovery--twrp)
8. [Custom ROMs](#8-custom-roms)
9. [What You Can Do with Root](#9-what-you-can-do-with-root)
10. [SafetyNet / Play Integrity Bypass](#10-safetynet--play-integrity-bypass)
11. [Device-Specific Notes](#11-device-specific-notes)

---

## 1. What Root Access Is

Android is Linux under the hood. Every process runs as an unprivileged user (your app = some `uid` like 10234). The `root` user (`uid=0`) has unrestricted access to everything.

```
Android security model:
  App A (uid=10050):    can only read/write its own /data/data/com.app.a/
  App B (uid=10051):    completely isolated from App A
  System services:      run as system (uid=1000) or specific UIDs
  Root (uid=0):         can read/write everything, kill any process,
                        remount filesystems read-write, load kernel modules

Without root:
  You cannot: read other apps' data, modify /system, run tcpdump,
              install system-level apps, block ads system-wide

With root:
  You can: read/write all partitions, install Xposed/LSposed modules,
           run full packet captures, debloat system apps permanently,
           bypass app restrictions, backup any app fully (including data)
```

---

## 2. Before You Root

```
Checklist:
  □ Back up ALL data — bootloader unlock WIPES the device
  □ Check if your device's bootloader can be unlocked
    (Xiaomi, OnePlus, Pixel: yes | Samsung Exynos/US: very hard | Huawei: nearly impossible)
  □ Know your device codename (e.g., "cheetah" for Pixel 7 Pro)
  □ Download ADB and fastboot (Android Platform Tools)
  □ Enable Developer Options: Settings → About Phone → tap Build Number 7×
  □ Enable USB Debugging: Developer Options → USB Debugging
  □ Understand: bootloader unlock = factory reset (all data gone)

Tools needed:
  platform-tools: https://developer.android.com/studio/releases/platform-tools
  Device drivers (Windows): https://developer.android.com/studio/run/win-usb

Verify ADB is working:
  adb devices   ← should show your device serial number
```

---

## 3. Bootloader Unlocking

The bootloader is the first code that runs at power-on. It verifies the OS signature before booting. Unlocking it allows loading unsigned (custom) software — required for rooting.

```bash
# Enable OEM unlocking (in Developer Options on device)
# Then unlock via fastboot:

adb reboot bootloader                    # Enter fastboot mode
fastboot flashing unlock                 # Modern devices (Android 9+)
# OR
fastboot oem unlock                      # Older devices

# Device will show warning → use volume keys to confirm → factory reset occurs

# Verify unlock status:
fastboot oem device-info                 # Shows "Device unlocked: true"
```

### Device-Specific Bootloader Unlock

| Brand | Method | Notes |
|-------|--------|-------|
| **Google Pixel** | `fastboot flashing unlock` | Easy, officially supported |
| **OnePlus** | `fastboot oem unlock` | Easy on most models |
| **Xiaomi** | Mi Unlock Tool (7–30 day wait) | Requires Mi account binding |
| **Motorola** | Submit request at motorola.com/unlockbootloader | Model-dependent |
| **Samsung (International)** | heimdall / Odin — complex | Trips Knox eFuse permanently |
| **Samsung (US Snapdragon)** | Not possible | Bootloader locked by carrier |
| **Huawei** | No longer possible (2018+) | Huawei stopped providing codes |

---

## 4. Magisk — The Standard Root Method

- **Repository:** https://github.com/topjohnwu/Magisk
- **Developer:** topjohnwu
- **License:** GPL v3
- **Method:** Systemless root — patches the boot image, does NOT modify `/system`

### How Magisk Works

```
Traditional root (SuperSU era):
  Modified /system/xbin/su → wrote to system partition
  Easy to detect: check if /system was modified

Magisk systemless root:
  Patches the boot.img (ramdisk) instead of /system
  At boot: Magisk mounts a virtual overlay (MagiskMount) over /system
  Apps see a clean /system + su binary injected at runtime
  Detection: harder — system partition is untouched

Magisk Hide / DenyList:
  For apps that detect root (banking apps, Google Play):
  Add them to DenyList → Magisk hides itself from those specific apps
  The app sees a "clean" environment when it checks
```

### Installation

```bash
# Method 1: Patch boot image (recommended, works universally)

# 1. Download your device's stock firmware / factory image
#    Pixel: https://developers.google.com/android/images
#    Others: XDA Developers forum for your device

# 2. Extract boot.img from the firmware ZIP

# 3. Transfer boot.img to your phone
adb push boot.img /sdcard/Download/

# 4. On device: install Magisk APK, open it
#    → Install → Select and Patch a File → choose boot.img
#    → Magisk patches it → saves magisk_patched_xxxx.img to /sdcard/Download/

# 5. Pull patched image back
adb pull /sdcard/Download/magisk_patched_xxxx.img

# 6. Flash patched boot image
adb reboot bootloader
fastboot flash boot magisk_patched_xxxx.img
fastboot reboot

# Magisk is now installed — open Magisk app to manage

# Method 2: Custom Recovery (if TWRP is available for your device)
# Flash Magisk ZIP via TWRP
```

### Magisk Modules

Magisk supports modules — systemless modifications installed as ZIP files:

```
Popular modules:
  LSPosed:          Xposed framework for Android 8+ (inject code into apps)
  Shamiko:          Better root hiding (works with Zygisk)
  Zygisk-Assistant: Enhanced Zygisk (root hiding improvements)
  MagiskHide Props Config: Spoof device fingerprint (pass CTS)
  Riru / Zygisk:    Code injection framework (required by some modules)
  AdAway:           System-level hosts file ad blocking
  Busybox:          Full Unix toolbox (grep, sed, awk, wget, etc.)
  BootloopProtector: Protects against modules causing bootloops
  ViPER4Android FX: System audio enhancement
  KTweak:           Kernel performance tweaks
  
Installing: Magisk app → Modules → Install from storage → select .zip
```

---

## 5. KernelSU

- **Repository:** https://github.com/tiann/KernelSU
- **Method:** Kernel-level root (built into the kernel itself)
- **Detection resistance:** Higher than Magisk — root is inside the kernel

```
How it differs from Magisk:
  Magisk: patches boot ramdisk, operates in userspace
  KernelSU: root is implemented inside the Linux kernel
             su binary calls a kernel syscall → kernel grants root
             Cannot be detected by scanning /system or /data
             
Requirements:
  Device must support GKI (Generic Kernel Image) — Android 12+ most devices
  OR: custom kernel with KernelSU patch applied

Installation:
  Check: https://kernelsu.org
  Download KernelSU APK + matching kernel ZIP for your device
  Flash kernel via custom recovery
  App manages root grants like Magisk does

When to use KernelSU over Magisk:
  When banking apps or games specifically scan for Magisk processes
  When you want deeper root hiding
  When your device supports GKI kernels
```

---

## 6. APatch

- **Repository:** https://github.com/bmax121/APatch
- **Method:** Kernel patching via boot image (like Magisk) but with kernel-level root
- **Compatibility:** Supports both GKI and non-GKI kernels

APatch combines Magisk's boot-image-patch approach with KernelSU-style kernel-level root implementation. Useful for devices that don't support GKI but you still want kernel-level root hiding.

---

## 7. Custom Recovery — TWRP

TWRP (Team Win Recovery Project) is a custom recovery that replaces Android's stock recovery partition. It allows flashing ZIP files, making NANDroid backups, accessing ADB in recovery mode, and decrypting data partitions.

```bash
# Flash TWRP (if available for your device)
# Check: https://twrp.me/Devices/

adb reboot bootloader
fastboot flash recovery twrp-x.x.x-devicename.img
fastboot reboot recovery                # Boot into TWRP

# TWRP capabilities:
  Install:   Flash ZIP files (Magisk, ROMs, mods)
  Backup:    Full NANDroid backup (boot, system, data, vendor)
  Restore:   Restore from backup
  Wipe:      Factory reset, dalvik cache, system
  Mount:     Read/write access to all partitions from ADB
  File Mgr:  Browse and edit filesystem
  Terminal:  Run root shell commands in recovery

# Full backup before ROM change:
# TWRP → Backup → select: Boot, System, Data, Vendor → Swipe
# Saved to: /sdcard/TWRP/BACKUPS/
```

---

## 8. Custom ROMs

Custom ROMs replace the entire Android OS. Popular choices:

| ROM | Based on | Features |
|-----|---------|---------|
| **LineageOS** | AOSP | Clean Android, wide device support, monthly updates |
| **GrapheneOS** | AOSP | Maximum security/privacy (Pixel only) |
| **CalyxOS** | AOSP | Privacy-focused, microG option (Pixel + Fairphone) |
| **PixelExperience** | AOSP + Pixel UI | Looks like stock Pixel, wide device support |
| **crDroid** | AOSP | Feature-rich customization |
| **Evolution X** | AOSP | Heavy Pixel-inspired theming |
| **ArrowOS** | AOSP | Minimal, clean |

```bash
# Flashing a custom ROM via TWRP:
# 1. Wipe: TWRP → Wipe → Format Data (type "yes")
# 2. Flash ROM ZIP: Install → select ROM zip → swipe
# 3. Flash GApps (if needed): Install → select GApps package
# 4. Flash Magisk (for root): Install → select Magisk zip
# 5. Reboot System

# GApps packages (Google apps for AOSP ROMs):
#   NikGApps: https://nikgapps.com
#   MindTheGapps: bundled with LineageOS
#   BiTGApps: minimal Google services
```

---

## 9. What You Can Do with Root

```
System modifications:
  Remove bloatware: adb shell pm uninstall -k --user 0 com.package.name
                    (or permanent with root: rm /system/app/Bloatware/)
  Hosts file blocking: edit /etc/hosts for system-wide ad blocking
  Modify build.prop: change device fingerprint, UI tweaks
  CPU/GPU tweaks: governor, scheduler, thermal profiles
  Custom kernel: better battery, performance, overclocking

Backup and restore:
  Titanium Backup / Swift Backup: back up app data including paid apps
  Full NANDroid backup via TWRP: complete system snapshot
  
Privacy and security:
  AFWall+: iptables-based firewall (per-app internet control)
  XPrivacyLua: spoof permissions and data (location, contacts, IMEI)
  AdAway: hosts file ad blocking (more effective than browser extensions)
  
Automation:
  Tasker + root access: automate anything (kill apps, modify settings, etc.)
  
Debugging:
  tcpdump: capture all network traffic (including HTTPS with Frida)
  strace: trace system calls of any app
  Read /proc/[pid]/maps: inspect any app's memory layout
  
Xposed / LSPosed framework:
  Inject code into any running app without modifying its APK
  Popular modules:
    GravityBox: deep UI customization
    Xposed Edge Pro: gestures and shortcuts  
    YouTube AdAway: remove YouTube ads at framework level
    MiXplorer: enhanced file manager with root access
```

---

## 10. SafetyNet / Play Integrity Bypass

Google's Play Integrity API (successor to SafetyNet) checks if a device is "certified" — unrooted, unmodified, running official firmware.

```
Play Integrity verdicts:
  MEETS_DEVICE_INTEGRITY:   Real Android device with no signs of tampering
  MEETS_BASIC_INTEGRITY:    App is running on Android (no device guarantee)
  MEETS_STRONG_INTEGRITY:   Pixel/certified device, verified boot passing

Apps using Play Integrity:
  Banking apps (most), Google Pay, Pokemon GO, Netflix,
  some multiplayer games

Bypass methods (cat and mouse — may break after updates):
  
  1. Magisk DenyList:
     Magisk → Settings → Zygisk ON → DenyList → add banking app
     Hides Magisk from that app's process

  2. Shamiko module:
     More aggressive hiding, hides root from all processes in DenyList
     
  3. MagiskHide Props Config:
     Spoof device fingerprint to a certified device
     Props that matter: ro.product.model, ro.build.fingerprint
     
  4. PlayIntegrityFix module:
     Specifically targets Play Integrity API responses
     https://github.com/chiteroman/PlayIntegrityFix

  5. KernelSU + Zygisk Next:
     Kernel-level root is harder for user-space detection

Checking your integrity:
  Play Integrity API Checker app on Play Store
  Checks: BASIC, DEVICE, STRONG verdicts
```

---

## 11. Device-Specific Notes

```
Google Pixel (best for rooting):
  Official factory images available
  Easy bootloader unlock (single fastboot command)
  GrapheneOS available for maximum security
  Supports KernelSU via GKI

Xiaomi / POCO / Redmi:
  Mi Unlock Tool required + 7–30 day waiting period after binding account
  Then standard fastboot unlock
  Good device support on XDA and LineageOS

OnePlus:
  Generally easy to unlock and root
  Older models: fastboot oem unlock
  Newer with OxygenOS 11+: fastboot flashing unlock

Samsung:
  International Exynos: possible but trips Knox eFuse (permanent flag)
  Knox trips = Samsung Pay dead, Samsung Secure Folder dead
  US Snapdragon variants: bootloader permanently locked
  Method: Odin flash with custom recovery + Magisk on patched AP

Fairphone:
  Officially supports unlocking and custom ROMs
  Best choice if you want root and care about repairability
```

---

## See Also

- [Android System](android-system.md) — Shizuku (rootless ADB alternative), Canta debloater
- [Android Automation](android-automation.md) — Tasker, MacroDroid (works better with root)
- [Termux Pentesting](termux-pentesting.md) — Penetration testing on Android
- [Environment Isolation](environment-isolation.md) — chroot, proot on Android
