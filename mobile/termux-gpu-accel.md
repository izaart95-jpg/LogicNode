# Hardware Acceleration in Termux (Proot & Chroot)

Enable GPU-accelerated OpenGL and Vulkan rendering inside Termux proot/chroot environments — allowing Linux desktop applications, games, and 3D software to use the Android device's GPU rather than slow CPU-based software rendering.

---

## Table of Contents
1. [How It Works](#1-how-it-works)
2. [Prerequisites](#2-prerequisites)
3. [Method 1 — VirGL (OpenGL via VIRGL)](#3-method-1--virgl-opengl-via-virgl)
4. [Method 2 — Zink (OpenGL via Vulkan/ZINK)](#4-method-2--zink-opengl-via-vulkanzink)
5. [Method 3 — Turnip (Native Vulkan, Adreno only)](#5-method-3--turnip-native-vulkan-adreno-only)
6. [Running the Desktop with Acceleration](#6-running-the-desktop-with-acceleration)
7. [Running Applications with Acceleration](#7-running-applications-with-acceleration)
8. [Troubleshooting](#8-troubleshooting)
9. [Performance Expectations](#9-performance-expectations)

---

## 1. How It Works

Android blocks direct GPU access from Linux containers (proot/chroot) for security. Three translation paths work around this:

```
VirGL path (VIRGL):
  proot app → OpenGL API → Mesa virpipe → VirGL protocol → virgl_test_server_android
  virgl_test_server_android → Android's OpenGL ES (via EGL) → GPU

ZINK path (Zink over Vulkan):
  proot app → OpenGL API → Mesa virpipe → VirGL protocol → virgl_test_server
  virgl_test_server → Mesa Zink → Vulkan → GPU

Turnip path (Adreno only):
  proot app → Vulkan API → Mesa Turnip (open-source Adreno driver) → GPU directly
  No server process needed — Turnip talks to the Adreno GPU directly from proot

Key difference:
  VirGL/Zink: Server process in Termux acts as bridge → any GPU
  Turnip:     Direct driver in proot → Adreno GPU only, but faster + more features

All paths provide:
  OpenGL: 3.x or 4.x compatibility (good enough for most Linux desktop apps)
  Vulkan: full support via Turnip (Adreno), or via Zink translation (others)
```

---

## 2. Prerequisites

### Termux packages

```bash
pkg update && pkg upgrade

# Install GPU acceleration stack
pkg install mesa-zink virglrenderer-mesa-zink vulkan-loader-android virglrenderer-android

# Package purposes:
# mesa-zink:                Mesa with Zink (OpenGL → Vulkan) driver
# virglrenderer-mesa-zink:  VirGL renderer server using Zink backend
# vulkan-loader-android:    Vulkan loader for Android
# virglrenderer-android:    VirGL renderer server using Android's OpenGL ES

# Also needed for running a desktop:
pkg install x11-repo
pkg install xorg-server xfce4 tigervnc  # or use termux-x11

# proot-distro (if not already set up)
pkg install proot-distro
proot-distro install debian    # or ubuntu, fedora, archlinux
```

### System requirements

```
Android:  8.0+ (API 26+)
GPU:      Any for VirGL/Zink
          Adreno 6xx/7xx for Turnip native Vulkan
RAM:      4GB+ recommended (2GB minimum)
Storage:  4GB+ for proot distro + apps

Check your GPU:
  Qualcomm Adreno:  Turnip available (best option)
  ARM Mali:         VirGL or Zink only
  MediaTek IMG:     VirGL or Zink only
  
Check GPU in Termux:
  cat /proc/cpuinfo | grep -i "hardware"
  # or install: pkg install vulkan-tools → vulkaninfo 2>/dev/null | grep "deviceName"
```

---

## 3. Method 1 — VirGL (OpenGL via VIRGL)

VirGL uses Android's native OpenGL ES as the backend. Most compatible method, works on all Android GPUs.

### Start the VirGL server (in Termux, BEFORE entering proot)

```bash
# Start VirGL server using Android's OpenGL ES
virgl_test_server_android &

# The & runs it in background
# Verify it started:
jobs                           # should show [1] virgl_test_server_android
# or:
pgrep virgl_test_server        # should return a PID
```

### Inside proot — use VirGL

```bash
# Enter proot distro
proot-distro login debian

# Inside proot, run apps with VirGL:
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 glxinfo | grep "OpenGL version"
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 glxgears   # Classic test

# The vars explained:
# GALLIUM_DRIVER=virpipe   → use VirGL pipe driver (connects to server in Termux)
# MESA_GL_VERSION_OVERRIDE=4.0 → report GL 4.0 to apps (actual support varies)
```

---

## 4. Method 2 — Zink (OpenGL via Vulkan/ZINK)

Zink translates OpenGL to Vulkan, then to the GPU. Generally better performance and higher OpenGL version support than VirGL on capable devices.

### Start the Zink server (in Termux, BEFORE entering proot)

```bash
# Start VirGL server using Zink (Vulkan) as backend
MESA_NO_ERROR=1 \
MESA_GL_VERSION_OVERRIDE=4.3COMPAT \
MESA_GLES_VERSION_OVERRIDE=3.2 \
GALLIUM_DRIVER=zink \
ZINK_DESCRIPTORS=lazy \
virgl_test_server --use-egl-surfaceless --use-gles &

# Variable explanations:
# MESA_NO_ERROR=1                 → Disable GL error checking (performance)
# MESA_GL_VERSION_OVERRIDE=4.3COMPAT → Report OpenGL 4.3 compatibility profile
# MESA_GLES_VERSION_OVERRIDE=3.2 → Report GLES 3.2 support
# GALLIUM_DRIVER=zink             → Use Zink (OpenGL-over-Vulkan) driver
# ZINK_DESCRIPTORS=lazy           → Lazy descriptor updates (better performance)
# --use-egl-surfaceless           → No physical display surface needed
# --use-gles                      → Use OpenGL ES (Android's native API)

# Verify server started:
pgrep virgl_test_server
```

### Inside proot — use Zink

```bash
# Same environment variables as VirGL — the driver in proot doesn't change
# The server handles which backend (virgl vs zink) is used
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 your_app

# For apps that specifically need GLES:
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.3COMPAT your_app
```

---

## 5. Method 3 — Turnip (Native Vulkan, Adreno only)

Turnip is Mesa's open-source Vulkan driver for Qualcomm Adreno GPUs. Unlike VirGL/Zink, it runs directly inside proot with no server process in Termux — closer to bare metal.

### Check if your device is compatible

```bash
# In Termux:
cat /proc/cpuinfo | grep -i "qualcomm\|adreno\|snapdragon"
# Supported: Adreno 6xx (Snapdragon 700/800 series, 2018+)
#            Adreno 7xx (Snapdragon 8 Gen 1/2/3, 2022+)
# Not supported: Adreno 5xx and below
```

### Install Turnip driver inside proot

```bash
# In Termux, download the driver package:
# Get the latest from: https://github.com/K11MCH1/AdrenoToolsDrivers/releases
# OR the specific version mentioned in guides:

wget https://github.com/K11MCH1/AdrenoToolsDrivers/releases/download/v24.1.0/mesa-vulkan-kgsl_24.1.0-devel-20240120_arm64.deb
# (Replace URL with current release from the repo)

# Copy to proot:
cp mesa-vulkan-kgsl_*.deb ~/.local/share/proot-distro/installed-rootfs/debian/root/

# Enter proot:
proot-distro login debian

# Inside proot — install the driver:
dpkg -i /root/mesa-vulkan-kgsl_*.deb

# Verify installation:
ls /usr/lib/aarch64-linux-gnu/dri/   # Should show kgsl_dri.so or similar
vulkaninfo 2>/dev/null | head -20     # Should show Turnip device

# Remove driver if needed:
dpkg -r mesa-vulkan-drivers:arm64
```

### Using Turnip inside proot

```bash
# Vulkan apps — just run them, Turnip is the Vulkan driver:
vulkaninfo
vkcube                                # Rotating cube test

# OpenGL apps using Zink on Turnip (OpenGL → Zink → Turnip → Adreno):
MESA_LOADER_DRIVER_OVERRIDE=zink \
TU_DEBUG=noconform \
your_opengl_app

# Variable explanations:
# MESA_LOADER_DRIVER_OVERRIDE=zink → force Zink (not virpipe) as GL driver
# TU_DEBUG=noconform               → disable Vulkan conformance checks (needed for KGSL)

# Blender, Godot, etc. — run with these vars set
```

---

## 6. Running the Desktop with Acceleration

### Termux-X11 (recommended for Wayland/X11)

```bash
# In Termux — install termux-x11-nightly
pkg install x11-repo
pkg install termux-x11-nightly

# Install termux-x11 APK on Android (from GitHub releases)
# https://github.com/termux/termux-x11/releases

# Start the graphical server AND VirGL server together
# (before proot login)

# Option A — Zink server + X11:
MESA_NO_ERROR=1 MESA_GL_VERSION_OVERRIDE=4.3COMPAT MESA_GLES_VERSION_OVERRIDE=3.2 \
GALLIUM_DRIVER=zink ZINK_DESCRIPTORS=lazy \
virgl_test_server --use-egl-surfaceless --use-gles &

# Start X11 display
termux-x11 :0 &

sleep 2

# Option B — VirGL server + X11:
virgl_test_server_android &
termux-x11 :0 &
sleep 2
```

### Enter proot and start XFCE4

```bash
# Login to proot, sharing /tmp for display socket
proot-distro login debian --shared-tmp

# Inside proot:
export DISPLAY=:0
export PULSE_SERVER=tcp:127.0.0.1:4713   # Audio (optional)

# Start XFCE4 desktop:
startxfce4

# Or with acceleration explicitly set:
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 startxfce4
```

### Using a startup script (recommended)

```bash
# ~/startxfce4_debian.sh (example startup script)
#!/bin/bash

# Kill previous sessions
pkill -f virgl_test_server
pkill -f termux-x11

sleep 1

# Start acceleration server (choose one):
# VirGL:
virgl_test_server_android &

# OR Zink:
# MESA_NO_ERROR=1 MESA_GL_VERSION_OVERRIDE=4.3COMPAT MESA_GLES_VERSION_OVERRIDE=3.2 \
# GALLIUM_DRIVER=zink ZINK_DESCRIPTORS=lazy \
# virgl_test_server --use-egl-surfaceless --use-gles &

sleep 1

# Start X11
termux-x11 :0 -xstartup "proot-distro login debian --shared-tmp -- bash -c 'export DISPLAY=:0; startxfce4'" &

sleep 2

# Open termux-x11 app on Android
am start --user 0 -n com.termux.x11/com.termux.x11.MainActivity
```

### VNC alternative

```bash
# If not using termux-x11, use VNC:
# In proot:
export DISPLAY=:1
Xvnc :1 -geometry 1920x1080 -depth 24 &
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 startxfce4 &

# Connect with VNC client on same device or network to localhost:5901
```

---

## 7. Running Applications with Acceleration

### VirGL / Zink (server running in Termux)

```bash
# Inside proot — prefix any GPU-accelerated app:

# General formula:
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 <app>

# Test first (confirm acceleration works):
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 glxinfo | grep "OpenGL renderer"
# Should show: OpenGL renderer string: virgl  (or similar)
# NOT: llvmpipe (that's software rendering)

# Blender:
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.3COMPAT blender

# Godot:
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 godot

# GIMP:
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 gimp

# Wine games:
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 wine game.exe

# Firefox (hardware accelerated video):
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 MOZ_USE_XINPUT2=1 firefox

# OpenArena (game test):
GALLIUM_DRIVER=virpipe MESA_GL_VERSION_OVERRIDE=4.0 openarena
```

### Turnip (Adreno only — no server needed)

```bash
# Inside proot:

# OpenGL apps:
MESA_LOADER_DRIVER_OVERRIDE=zink TU_DEBUG=noconform glxinfo | grep renderer
MESA_LOADER_DRIVER_OVERRIDE=zink TU_DEBUG=noconform glxgears

# Vulkan apps (native):
vkcube
vulkaninfo

# Blender with Turnip:
MESA_LOADER_DRIVER_OVERRIDE=zink TU_DEBUG=noconform blender

# Games with Turnip + Wine/Box64:
MESA_LOADER_DRIVER_OVERRIDE=zink TU_DEBUG=noconform wine game.exe
```

### Make it permanent (avoid typing every time)

```bash
# Add to ~/.bashrc or ~/.profile inside proot:
# For VirGL/Zink:
export GALLIUM_DRIVER=virpipe
export MESA_GL_VERSION_OVERRIDE=4.0

# For Turnip:
export MESA_LOADER_DRIVER_OVERRIDE=zink
export TU_DEBUG=noconform

# Source it:
source ~/.bashrc
```

---

## 8. Troubleshooting

```
Error: "virgl_test_server: command not found"
  Fix: pkg install virglrenderer-android virglrenderer-mesa-zink

Error: "libvulkan.so not found" or Vulkan not working
  Fix: pkg install vulkan-loader-android
       In proot: apt install libvulkan1

Error: OpenGL renderer shows "llvmpipe" (software rendering)
  Means: Not using GPU — acceleration not working
  Checks:
    Is virgl_test_server running in Termux? (pgrep virgl_test_server)
    Did you start the server BEFORE entering proot?
    Is DISPLAY set correctly? (echo $DISPLAY — should be :0 or :1)
    Did you share /tmp? (proot-distro login debian --shared-tmp)
  
Error: Black screen or no window
  Fix: Make sure X server is running before starting desktop
       Check: DISPLAY=:0 xterm (try launching simple app first)
       Try restarting both virgl server and X server

Error: "cannot connect to X server"
  Fix: export DISPLAY=:0 (or whatever display number you're using)
       Verify: ls /tmp/.X11-unix/X0 (socket should exist)

Error: Turnip crashes or "VK_ERROR_INITIALIZATION_FAILED"
  Fix: Verify device is Adreno 6xx+
       Try different driver version from AdrenoToolsDrivers repo
       Ensure dpkg -i succeeded without errors

Error: Poor performance even with acceleration
  Use GALLIUM_HUD=fps to show FPS:
    GALLIUM_DRIVER=virpipe GALLIUM_HUD=fps glxgears
  If FPS < 10 for glxgears: likely still software rendering
  
Audio in proot:
  Install PulseAudio in both Termux and proot
  Termux: pkg install pulseaudio && pulseaudio --start
  proot: apt install pulseaudio && export PULSE_SERVER=tcp:127.0.0.1:4713
```

---

## 9. Performance Expectations

```
Turnip (Adreno 7xx):
  Best performance — close to native Android GPU
  OpenGL 4.x via Zink on top of Turnip
  Vulkan: full native support
  Good for: Blender, 3D games, GPU compute
  
Turnip (Adreno 6xx):
  Good performance — most features work
  
Zink server (mid-range Android GPU):
  Moderate performance
  Good for: 2D desktop, light 3D, older games
  OpenGL 4.3 compatible profile available
  
VirGL (any GPU):
  Most compatible, slowest
  Good for: 2D apps, light OpenGL, GTK/Qt apps
  Limited to OpenGL 4.0 level features
  
Software rendering (llvmpipe — no acceleration):
  Very slow, avoid
  If you see llvmpipe: acceleration is not working

Typical FPS (approximate, vary widely by device/app):
  glxgears (simple triangles test):
    llvmpipe:     10–50 FPS
    VirGL:        100–500 FPS
    Zink:         200–1000 FPS
    Turnip:       1000–5000 FPS
    
  OpenArena (game):
    llvmpipe:     unplayable
    VirGL:        20–60 FPS
    Zink:         30–90 FPS
    Turnip:       60–120 FPS
```

---

## See Also

- [Termux Setup](termux-setup.md) — Termux installation and package management
- [Linux on Android](linux-on-android.md) — proot-distro setup guide
- [Desktop Environments](desktop-environments.md) — Installing XFCE, GNOME in proot
- [Environment Isolation](environment-isolation.md) — chroot vs proot differences
- [GPU Architecture](../fundamentals/gpu-architecture.md) — How GPU drivers and APIs work
