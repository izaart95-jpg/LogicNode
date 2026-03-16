# Android System Tools — Shizuku, Phantom Process Killer & Display Configuration

This document covers tools and techniques for unlocking deeper Android system access without root, fixing Android 12+ background process limitations, and understanding display density configuration for responsive layouts and Termux GUI apps.

---

## Table of Contents
1. [Shizuku](#1-shizuku)
2. [Phantom Process Killer — Fix](#2-phantom-process-killer--fix)
3. [Smallest Width (sw dp) & Display Density](#3-smallest-width-sw-dp--display-density)

---

## 1. Shizuku

### 1.1 What is Shizuku?

**Shizuku** is an Android app that lets other apps use system APIs directly with elevated (`adb` or `root`) privileges — without requiring the device to be rooted. It acts as a privilege broker, running a background service at a higher permission level that partner apps can connect to and call privileged APIs through.

- **Website:** https://shizuku.rikka.app
- **Source:** https://github.com/RikkaApps/Shizuku
- **Platform:** Android 6.0+ (ADB mode), Android 11+ (Wireless ADB mode recommended)
- **Root Required:** No (ADB mode), Optional (root mode)

### 1.2 Why Shizuku?

Many Android power-user and developer tools need system-level permissions that are only granted to `adb` or root processes. Examples include:

- Disabling the Phantom Process Killer (see §2)
- Changing display density / smallest width without root
- Granting or revoking app permissions programmatically
- Automating system settings
- Tools like Canta (debloater), App Ops, LSPatch, and many Termux helpers

Without Shizuku, achieving any of this on a non-rooted device requires keeping a PC connected via USB ADB — Shizuku eliminates that dependency by keeping the privileged service alive on-device.

### 1.3 How Shizuku Works

```
┌─────────────────────────────────────────────────────┐
│  Partner App (e.g., Canta, App Ops, your script)    │
│  → calls Shizuku's Binder API                        │
└──────────────────────┬──────────────────────────────┘
                       │ Binder IPC
┌──────────────────────▼──────────────────────────────┐
│  Shizuku Service (runs as adb / root shell)          │
│  → executes privileged API calls on behalf of app    │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  Android System APIs (normally restricted)           │
└─────────────────────────────────────────────────────┘
```

### 1.4 Starting Shizuku

There are three ways to start the Shizuku service:

#### Method 1: Wireless ADB (Android 11+ — Recommended, No PC Needed)

1. Enable **Developer Options** (Settings → About Phone → tap Build Number 7 times)
2. Enable **Wireless Debugging** (Settings → Developer Options → Wireless Debugging)
3. Open the Shizuku app → tap **Pairing** → follow the on-screen pairing flow
4. Once paired, tap **Start** — Shizuku starts via Wireless ADB

> **Note:** On Android 12+, Wireless ADB pairing can be done entirely on-device with no PC required.

#### Method 2: USB ADB (All Android versions)

```bash
# On a connected PC with ADB installed
adb shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh
```

1. Enable **USB Debugging** in Developer Options
2. Connect phone to PC via USB
3. Open Shizuku → follow the on-screen ADB command instructions
4. Run the command shown on your PC terminal

#### Method 3: Root

If your device is rooted, Shizuku can start automatically at boot via the root option in-app — no ADB needed at all.

### 1.5 Auto-Start After Reboot

A known limitation of non-root Shizuku is that the service stops after reboot. Solutions:

- **Wireless ADB auto-start:** On Android 11+, some devices maintain the Wireless ADB session after reboot if Wireless Debugging is left enabled and the pairing persists. Shizuku can reconnect automatically.
- **Tasker / MacroDroid:** Trigger the Shizuku start script on boot event via a shell command task.
- **Root mode:** Survives reboot natively.

### 1.6 Apps That Use Shizuku

| App | Function |
|-----|----------|
| **Canta** | Debloat system apps without root |
| **App Ops** | Fine-grained app permission management |
| **LSPatch** | Patch APKs with Xposed modules without root |
| **aShell** | ADB shell via Shizuku (useful for running commands on-device) |
| **Termux:ADB** | ADB shell access from Termux using Shizuku |
| **PixelFlasher** | ROM/firmware tools |
| **SetEdit** | Edit Android settings database without root |

### 1.7 Shizuku vs Root vs ADB-over-USB

| Feature | Shizuku (ADB Mode) | Root | ADB (USB) |
|---------|-------------------|------|-----------|
| **Requires PC** | No (Android 11+) | No | Yes |
| **Root required** | No | Yes | No |
| **Survives reboot** | Needs re-trigger | ✅ | Needs reconnect |
| **Security risk** | Low | High (if misused) | Low |
| **App ecosystem** | Growing | Largest | Limited (manual) |
| **Bootloader unlock needed** | No | Usually yes | No |

---

## 2. Phantom Process Killer — Fix

### 2.1 What is the Phantom Process Killer?

Introduced in **Android 12**, the Phantom Process Killer (PPK) is a system mechanism that automatically kills "phantom processes" — child processes spawned by apps (especially shell processes launched by apps like Termux). The system limits the number of such processes per app to **32**, and kills them aggressively when the device is under memory pressure or simply as part of routine background process management.

**Affected apps:**
- **Termux** — shell sessions, background scripts, SSH sessions, `proot-distro` environments
- **UserLAnd** — Linux environments
- Any app that forks child processes (compilers, servers, development tools)

**Symptoms:**
- Termux sessions dying unexpectedly mid-operation
- `proot-distro` or chroot environments crashing
- Long-running scripts (builds, backups, servers) terminating without warning
- `[Process completed (signal 9) - press Enter]` appearing in Termux

### 2.2 Why It Happens

Android treats processes forked by non-system apps as "phantom processes" because they are not directly managed by the Android activity manager. The killer targets these specifically, not the parent app itself.

```
Termux (parent app — protected by Android activity manager)
  └── bash (child/phantom process — UNPROTECTED, killable)
        └── python script (grandchild — killable)
        └── proot session (killable)
        └── ssh server (killable)
```

### 2.3 The Fix — Disable Phantom Process Killer

The fix involves changing a `device_config` flag that controls phantom process monitoring. This requires `adb` or Shizuku privileges.

#### Method 1: Using Shizuku + aShell (No PC Required)

1. Install **Shizuku** and start it (see §1.4)
2. Install **aShell** from F-Droid or GitHub
3. Open aShell and run:

```bash
# Disable phantom process killing entirely
device_config set_sync_disabled_for_tests persistent
device_config put activity_manager max_phantom_processes 2147483647
```

#### Method 2: USB ADB from PC

```bash
# Connect phone via USB with USB Debugging enabled
adb shell device_config set_sync_disabled_for_tests persistent
adb shell device_config put activity_manager max_phantom_processes 2147483647
```

#### Method 3: Termux (if ADB over TCP is enabled)

```bash
# If wireless ADB is active and you know the port
adb connect 127.0.0.1:PORT
adb shell device_config set_sync_disabled_for_tests persistent
adb shell device_config put activity_manager max_phantom_processes 2147483647
```

### 2.4 Command Breakdown

| Command | Effect |
|---------|--------|
| `device_config set_sync_disabled_for_tests persistent` | Prevents the system from resetting `device_config` values after reboot or remote sync |
| `device_config put activity_manager max_phantom_processes 2147483647` | Sets the phantom process limit to `Integer.MAX_VALUE` — effectively unlimited |

> **Why `persistent`?** Without this flag, `device_config` changes are reset when the system syncs with remote config servers (typically after reboot or periodically). Setting it to `persistent` makes the change survive reboots.

### 2.5 Verify the Fix

```bash
# Check the current phantom process limit
adb shell device_config get activity_manager max_phantom_processes
# Expected: 2147483647

# Check sync disabled state
adb shell device_config get_sync_disabled_for_tests
# Expected: persistent
```

### 2.6 Reverting the Fix

```bash
# Restore default phantom process limit (32)
adb shell device_config put activity_manager max_phantom_processes 32
adb shell device_config set_sync_disabled_for_tests none
```

### 2.7 Does It Survive Reboot?

With `set_sync_disabled_for_tests persistent`, **yes** — the values persist across reboots on most devices. However, some manufacturer firmware or major Android updates may reset `device_config` values. Re-run the commands if Termux begins dying again after a system update.

### 2.8 Android Version Behavior

| Android Version | Phantom Process Killer | Notes |
|----------------|----------------------|-------|
| Android 11 and below | ❌ Not present | No action needed |
| Android 12 | ✅ Introduced | Fix required for Termux heavy use |
| Android 12L | ✅ Active | Same fix applies |
| Android 13 | ✅ Active | Same fix applies |
| Android 14+ | ✅ Active | Same fix applies |

---

## 3. Smallest Width (sw dp) & Display Density

### 3.1 What is Smallest Width?

**Smallest Width** (`sw` qualifier) is an Android resource qualifier that defines the minimum width of the screen in **density-independent pixels (dp)**. Android uses it to select the appropriate layout resources for a device's screen size — independently of orientation.

Unlike screen width (which changes on rotation), `sw` always represents the **shorter dimension** of the screen regardless of portrait or landscape mode.

```
Device in portrait:
  width  = 360dp  →  sw = 360dp
  height = 800dp

Device in landscape:
  width  = 800dp  →  sw still = 360dp  (shortest side never changes)
  height = 360dp
```

### 3.2 Common Smallest Width Breakpoints

| sw Value | Typical Device | Example |
|----------|---------------|---------|
| `sw320dp` | Small phones | Old/budget Android phones |
| `sw360dp` | Normal phones | Most Android phones (common default) |
| `sw411dp` | Large phones | Pixel 6, Samsung Galaxy S-series |
| `sw480dp` | Large phones / small tablets | 5.5"+ phablets |
| `sw600dp` | 7" tablets | Nexus 7, Fire HD 8 |
| `sw720dp` | 10" tablets | Nexus 10, Galaxy Tab |
| `sw840dp` | Large tablets | iPad Pro equivalent |

### 3.3 Density vs Smallest Width

| Concept | Unit | What it measures | Changes with rotation |
|---------|------|-----------------|----------------------|
| **Density (dpi)** | dots per inch | Pixel density of the screen | No |
| **Smallest Width (sw dp)** | dp | Shortest screen dimension | No |
| **Screen Width (dp)** | dp | Current width | Yes |

**Density buckets:**

| Bucket | dpi Range | Scale Factor | Common Devices |
|--------|-----------|-------------|----------------|
| ldpi | ~120 dpi | 0.75× | Very old/cheap devices |
| mdpi | ~160 dpi | 1.0× (baseline) | Old phones |
| hdpi | ~240 dpi | 1.5× | Mid-range phones |
| xhdpi | ~320 dpi | 2.0× | Most modern phones |
| xxhdpi | ~480 dpi | 3.0× | High-end phones (Pixels, Samsung flagships) |
| xxxhdpi | ~640 dpi | 4.0× | Highest-end devices |

### 3.4 Checking Your Device's Values

```bash
# Via ADB
adb shell wm size        # Physical pixel resolution
adb shell wm density     # Current DPI

# In Termux (no ADB needed)
getprop ro.sf.lcd_density

# Manual calculation
# sw_dp = (shorter_side_px / dpi) * 160
# Example: 1080px shorter side, 420 dpi → (1080/420)*160 = 411dp
```

### 3.5 Changing Density / Smallest Width (Without Root)

You can override display density via ADB or Shizuku, which effectively changes how the device reports its smallest width to apps. This is useful for:

- Making Termux display more content per screen
- Triggering tablet UI layouts on large phones
- Fixing apps that don't scale well on your device
- Adjusting GUI rendering in `proot-distro` environments

```bash
# View current density
adb shell wm density

# Set custom density (higher number = smaller UI elements, more content visible)
adb shell wm density 420     # Good for most large phones
adb shell wm density 480     # Compact, tablet-like density
adb shell wm density 560     # Very compact

# Reset to device default
adb shell wm density reset

# Virtual resolution scaling (affects sw calculation differently)
adb shell wm size 1080x2340   # Set to native resolution
adb shell wm size reset       # Reset to default
```

**Via Shizuku + aShell (no PC required):**

```bash
# Same commands work in aShell with Shizuku active
wm density 420
wm density reset
```

### 3.6 Smallest Width in App Development

For developers writing Android apps or customizing layouts for proot/Termux tools:

```
res/
├── layout/                    # Default (phones)
├── layout-sw600dp/            # 7"+ tablets
├── layout-sw720dp/            # 10"+ tablets
├── values/                    # Default dimens/strings
├── values-sw600dp/            # Tablet overrides
└── values-night/              # Dark mode
```

```xml
<!-- values/dimens.xml — phone default -->
<dimen name="nav_drawer_width">280dp</dimen>

<!-- values-sw600dp/dimens.xml — tablet override -->
<dimen name="nav_drawer_width">320dp</dimen>
```

### 3.7 Smallest Width in Termux / proot-distro GUI Context

When running GUI apps via `proot-distro` with Termux X11 or VNC, display density affects rendering quality and element size.

```bash
# Inside proot Linux environment — set DPI for X11/GUI apps
export GDK_DPI_SCALE=1.5          # GTK apps (XFCE, LXDE, GNOME)
export QT_SCALE_FACTOR=1.5        # Qt apps (LXQt, KDE)
export GDK_SCALE=2                # Integer scaling for GTK (sharper)

# Set Xorg DPI — add to ~/.Xresources inside proot
Xft.dpi: 120

# Or pass DPI when starting the desktop session
startxfce4 -- -dpi 120
```

**Suggested X11 DPI by device:**

| Screen Size | Suggested DPI |
|------------|---------------|
| Small phone (~5") | 190–200 |
| Normal phone (~6") | 300–420 |
| Large phone (~6.5"+) | 320–440 |
| Small tablet (~8") | 380–510 |
| Large tablet (~10"+) | 396–512 |

---

## 4. Canta — Rootless Android Debloater

- **Repository:** https://github.com/samolego/Canta
- **License:** LGPL-3.0
- **Requires:** Shizuku (see Shizuku section above)
- **Android:** 9.0+ (SDK 28+)
- **Download:** F-Droid, IzzyOnDroid, GitHub Releases
- **Stars:** 4.3k+

### Overview

Canta lets you uninstall any pre-installed or user app without root, using Shizuku's privileged ADB shell to call `pm uninstall --user 0 <package>`. It integrates with the Universal Android Debloater (UAD) list to tag packages with safety recommendations — telling you whether removing a package is Safe, Recommended, Expert-only, or Unsafe.

No PC, no ADB USB cable, no root required. Everything runs on-device once Shizuku is active.

### Installation

```
1. Install and activate Shizuku (see Shizuku section above)
2. Install Canta:
   F-Droid:     https://f-droid.org/packages/io.github.samolego.canta/
   IzzyOnDroid: https://apt.izzysoft.de/fdroid/index/apk/io.github.samolego.canta
   GitHub:      https://github.com/samolego/Canta/releases/latest
3. Open Canta → grant Shizuku permission when prompted
4. Browse or search the app list
5. Tap the trash icon on any app to uninstall
```

### Features

- **UAD list integration:** Each app shows a safety tag from the Universal Debloater Alliance database — green (safe to remove), yellow (caution), red (system-critical)
- **Uninstall for current user only:** Uses `--user 0` — the app is hidden/disabled rather than permanently deleted from all users. Factory reset restores it.
- **View previously uninstalled apps:** Canta tracks what it removed and shows a "Restore" list — you can reinstall any debloated package without a factory reset
- **Search and filter:** Filter by safety level, installed/uninstalled state, or search by name/package
- **No permanent bricking:** Since removal is per-user (not system-wide `pm uninstall`), critical mistakes are recoverable. If you cause a bootloop: factory reset restores all system apps.
- **APK verification:** Releases are signed; verify with SHA-256 fingerprint `0A:26:40:31:7C:43:27:21:88:C3:E1:31:94:C1:54:60:69:1F:12:C3:9E:A1:9B:BA:72:7D:D6:7F:B5:62:89:D4`

### Common Debloat Targets

```
# Safe to remove on most devices:
com.facebook.appmanager       Facebook App Manager (background updater)
com.facebook.services         Facebook Services
com.microsoft.skydrive        OneDrive
com.google.android.videos     Google Play Movies
com.google.android.music      Google Play Music
com.samsung.android.game.gamehome  Samsung Game Launcher
com.samsung.android.bixby.agent   Bixby
com.amazon.kindle             Kindle (OEM-installed)

# Caution — may break things:
com.android.phone             Phone app (breaks calls if removed)
com.google.android.gms        Google Play Services (breaks almost everything)
```

### Android 16 Note

Android 16 may require a forked version of Shizuku: https://github.com/thedjchi/Shizuku. Standard Shizuku may not work on Android 16 devices. Check Canta's GitHub issues for current status.

### OPlus / OnePlus / Realme Warning

Some OPlus (OPPO/Realme/OnePlus) system apps are hardened and resist uninstallation even via Shizuku. A tracking issue exists at https://github.com/samolego/Canta/issues/338. For these devices, ADB from PC may be required for stubborn packages.

## See Also

- [Termux Setup](termux-setup.md) — Terminal setup, packages, FFmpeg, and Tmux
- [Linux on Android](linux-on-android.md) — Ubuntu via proot-distro with VNC GUI
- [Android Automation](android-automation.md) — Tasker, MacroDroid, ArduinoDroid
- [Desktop Environments](desktop-environments.md) — XFCE, LXDE, LXQt on headless/mobile systems
- [Environment Isolation](environment-isolation.md) — chroot vs proot vs proot-distro
