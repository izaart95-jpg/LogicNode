# Wine — Windows Compatibility Layer

Wine (Wine Is Not an Emulator) allows running Windows applications and games on Linux, macOS, and BSD. It reimplements the Windows API in native code — no virtualization, no emulation of x86 hardware.

---

## Table of Contents
1. [What Wine Actually Is](#1-what-wine-actually-is)
2. [Wine Architecture](#2-wine-architecture)
3. [Installation](#3-installation)
4. [Running Applications](#4-running-applications)
5. [Prefixes — Wine Environments](#5-prefixes--wine-environments)
6. [DXVK & DirectX Translation](#6-dxvk--directx-translation)
7. [Proton — Wine for Steam Games](#7-proton--wine-for-steam-games)
8. [Lutris — Game Manager](#8-lutris--game-manager)
9. [Bottles — GUI Wine Manager](#9-bottles--gui-wine-manager)
10. [Configuration & Tweaks](#10-configuration--tweaks)
11. [Common Issues & Fixes](#11-common-issues--fixes)
12. [Wine on macOS](#12-wine-on-macos)

---

## 1. What Wine Actually Is

```
Emulation (NOT what Wine does):
  Emulator simulates the CPU and hardware
  Guest OS runs inside emulated hardware
  Every instruction translated: slow (~10–100× overhead)
  Examples: QEMU, VirtualBox

Wine (what it actually does):
  Runs Windows binaries NATIVELY on the host CPU
  No instruction translation — x86 code executes at native speed
  Wine intercepts Windows API calls and handles them using Linux/macOS equivalents

Example — application calls CreateWindowExA():
  Windows:   application → kernel32.dll → win32k.sys → draws window
  Wine:      application → Wine's kernel32.dll.so → X11/Wayland/Quartz → draws window
  Same binary, different API backend, native performance

What Wine implements:
  Win32 API:      CreateFile, ReadFile, GetSystemInfo, Registry, etc.
  DirectX:        D3D9/10/11/12 (via DXVK/WineD3D), OpenAL, XAudio2
  COM/OLE:        Component Object Model
  .NET:           via Mono (Wine's .NET implementation)
  VBScript/JScript: via Wine's scripting engines
  PE loader:      loads .exe and .dll files

What Wine does NOT do:
  Run Windows kernel drivers (.sys files) — user-space only
  Run ARM Windows apps on x86 Linux (without additional tools)
  Guarantee perfect compatibility — complex apps may have issues
```

---

## 2. Wine Architecture

```
Windows Application (.exe)
        ↓
Wine Loader (wine, wine64)
  - Loads PE executable into memory
  - Sets up wine process (which is a Linux process)
  - Maps Wine DLLs into process address space
        ↓
Wine DLLs (reimplemented Windows DLLs):
  ntdll.dll.so      ← Lowest level: NT API (NtCreateFile, NtQueryInformationProcess...)
  kernel32.dll.so   ← Win32 kernel: CreateFile, CreateProcess, VirtualAlloc...
  user32.dll.so     ← GUI: CreateWindow, MessageBox, GetMessage, DispatchMessage...
  gdi32.dll.so      ← GDI drawing: BitBlt, TextOut, etc. → Cairo/FreeType
  advapi32.dll.so   ← Registry, security, services
  ws2_32.dll.so     ← Winsock → POSIX sockets
  d3d9/10/11.dll.so ← DirectX (WineD3D or DXVK)
  opengl32.dll.so   ← OpenGL passthrough
  winmm.dll.so      ← Windows multimedia (audio → PulseAudio/ALSA)
  msvcrt.dll.so     ← C runtime

Wine Server (wineserver process):
  Separate process per Wine prefix
  Manages: window manager, registry, process/thread synchronization
  IPC: Windows named pipes/events/mutexes implemented via wineserver
  Inter-process COM (DCOM) coordination

Display backends:
  Linux:  X11 (most common) or Wayland (experimental, improving)
  macOS:  Quartz (via XQuartz or native)

Audio backends:
  Linux:  PulseAudio, PipeWire, ALSA, OSS
  macOS:  CoreAudio
```

---

## 3. Installation

### Linux

```bash
# Ubuntu/Debian — Wine stable
sudo dpkg --add-architecture i386
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
sudo add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ jammy main'
sudo apt update
sudo apt install --install-recommends winehq-stable

# Ubuntu — Wine staging (newer, more patches)
sudo apt install --install-recommends winehq-staging

# Arch Linux
sudo pacman -S wine wine-mono wine-gecko

# Fedora
sudo dnf install wine

# Check version
wine --version

# Install Wine Mono (for .NET apps)
# Download from: https://dl.winehq.org/wine/wine-mono/
wine64 uninstaller  # GUI installer within Wine prefix

# Install Wine Gecko (for Internet Explorer rendering engine)
# Usually auto-prompted when needed
```

### Required 32-bit libraries (Ubuntu)

```bash
sudo apt install libc6:i386 libgcc-s1:i386 libstdc++6:i386
# These let 32-bit Windows apps run on 64-bit Linux
```

---

## 4. Running Applications

```bash
# Run a Windows executable
wine program.exe
wine64 program64.exe     # Force 64-bit Wine

# Run with specific Windows version emulated
WINEARCH=win64 wine program.exe

# Debug output (see what Wine is doing)
WINEDEBUG=+all wine program.exe 2>&1 | head -100
WINEDEBUG=+loaddll wine program.exe  # Just show DLL loading
WINEDEBUG=-all wine program.exe      # Suppress all debug (quiet run)

# Run Windows Control Panel applets
wine control           # Windows Control Panel
wine regedit           # Registry Editor
wine notepad           # Notepad
wine cmd               # Windows command prompt in Wine
wine explorer          # Windows Explorer

# Install .msi packages
wine msiexec /i package.msi

# Install via Wine's built-in installer
wine start /unix setup.exe   # Handles path translation

# Run a specific program in a prefix
WINEPREFIX=~/.wine-myapp wine program.exe
```

---

## 5. Prefixes — Wine Environments

A **Wine prefix** is an isolated directory that acts like a Windows installation — it has its own C: drive, registry, and installed software. Multiple prefixes keep apps isolated from each other.

```
Default prefix: ~/.wine/
  drive_c/          ← C: drive
    Program Files/
    Program Files (x86)/
    users/
      username/     ← %USERPROFILE%
        Desktop/
        Documents/
    windows/
      system32/     ← 64-bit Windows DLLs (Wine implementations)
      syswow64/     ← 32-bit Windows DLLs
  system.reg        ← HKEY_LOCAL_MACHINE registry
  user.reg          ← HKEY_CURRENT_USER registry
  userdef.reg       ← Default user registry
```

```bash
# Create a new prefix (automatically done on first run)
WINEPREFIX=~/.wine-game1 WINEARCH=win64 wine wineboot

# Switch prefix with env var
export WINEPREFIX=~/.wine-photoshop
wine photoshop.exe

# List all prefixes
ls ~/.wine-*

# Destroy and recreate a prefix (nuclear reset)
rm -rf ~/.wine-game1
WINEPREFIX=~/.wine-game1 wine wineboot --init

# winetricks — essential helper for installing prerequisites
# Download: https://github.com/Winetricks/winetricks
# OR: sudo apt install winetricks

# Install common dependencies in a prefix
WINEPREFIX=~/.wine-myapp winetricks vcrun2019   # Visual C++ 2019 runtime
WINEPREFIX=~/.wine-myapp winetricks dotnet48     # .NET Framework 4.8
WINEPREFIX=~/.wine-myapp winetricks d3dx9        # DirectX 9
WINEPREFIX=~/.wine-myapp winetricks d3dcompiler_47
WINEPREFIX=~/.wine-myapp winetricks corefonts    # Microsoft Core Fonts
WINEPREFIX=~/.wine-myapp winetricks allfonts     # All fonts

# Common app prerequisites:
winetricks list-installed           # See installed components
winetricks list-available           # See all available components
```

---

## 6. DXVK & DirectX Translation

WineD3D (Wine's built-in DirectX implementation) translates DirectX to OpenGL — slow and incomplete. DXVK translates DirectX 9/10/11 to **Vulkan** — dramatically faster and more compatible.

```
Translation layers:

DirectX 9/10/11 → DXVK → Vulkan → GPU
DirectX 12      → VKD3D-Proton → Vulkan → GPU

WineD3D (fallback, avoid for games):
  DirectX → OpenGL → GPU
  Slower (OpenGL overhead), less complete
  Use only if Vulkan not available

DXVK performance:
  WineD3D: ~50–70% of native Windows performance
  DXVK:    ~85–95% of native Windows performance (sometimes equals or beats Windows!)

Install DXVK manually:
  # Download from: https://github.com/doitsujin/dxvk/releases
  # Extract: contains d3d9.dll, d3d10core.dll, d3d11.dll, dxgi.dll
  WINEPREFIX=~/.wine-game setup_dxvk.sh install   # Script included in release

  # Or via winetricks:
  WINEPREFIX=~/.wine-game winetricks dxvk

DXVK_HUD (performance overlay):
  DXVK_HUD=1 wine game.exe               # Show FPS
  DXVK_HUD=full wine game.exe            # Full GPU stats
  DXVK_HUD=fps,frametime wine game.exe  # Custom selection

DXVK state cache:
  ~/.cache/dxvk-cache/ — compiled pipeline shaders
  First run: stutters while shaders compile
  Subsequent runs: smooth (cache hit)

VKD3D-Proton (DirectX 12):
  Fork of VKD3D by the Proton team, much more optimized
  https://github.com/HansKristian-Work/vkd3d-proton
  Required for DX12 games like Cyberpunk 2077, Elden Ring under Proton
```

---

## 7. Proton — Wine for Steam Games

Proton is Valve's customized Wine distribution for Steam on Linux. It bundles Wine + DXVK + VKD3D-Proton + Steam Runtime + many patches for game compatibility.

```
Proton = Wine + DXVK + VKD3D-Proton + Steam Linux Runtime + esync/fsync + patches

Enable Proton in Steam:
  Steam → Settings → Compatibility → Enable Steam Play for all titles
  Choose Proton version (Proton 9.x is current stable)

Per-game Proton settings:
  Right-click game → Properties → Compatibility → Force specific version

Proton versions:
  Proton 9.x:      Current stable, most games
  Proton Experimental: Bleeding edge, newer patches
  Proton-GE (GloriousEggroll): Community builds, faster updates, extra codecs
    Install via ProtonUp-Qt: https://github.com/DavidoTek/ProtonUp-Qt

Check game compatibility: https://www.protondb.com
  Gold: works perfectly, minor tweaks
  Silver: some issues, workarounds available
  Platinum: better on Linux than Windows (with Proton)
  Borked: broken

Proton launch options (Steam → Properties → Launch Options):
  PROTON_ENABLE_NVAPI=1 %command%     # NVIDIA DLSS support
  PROTON_USE_WINED3D=1 %command%      # Force WineD3D (disable DXVK)
  DXVK_HUD=fps %command%              # Show FPS overlay
  WINEDEBUG=-all %command%            # Suppress Wine debug output
  gamemoderun %command%               # Enable GameMode (CPU optimization)
  mangohud %command%                  # MangoHud overlay (FPS, GPU, CPU)

Proton game data location:
  ~/.steam/steam/steamapps/compatdata/APPID/
  Each game gets its own Wine prefix under compatdata/
```

---

## 8. Lutris — Game Manager

Lutris is an open-source game launcher that manages Wine prefixes, installs games from GOG/Epic/Humble, and handles runner configuration automatically.

```
Install Lutris:
  sudo add-apt-repository ppa:lutris-team/lutris
  sudo apt install lutris

Features:
  Runners: Wine (multiple versions), DXVK, Python, DOSBox, emulators
  Install scripts: community scripts auto-configure games (GOG, Epic, Battle.net)
  Game library: aggregates all games (Steam, GOG, Epic, native, emulated)
  Wine management: download, switch, and configure Wine versions per game
  
Install Battle.net (Blizzard):
  Lutris website → search "Battle.net" → Install (uses community script)
  Script handles: Wine prefix, DXVK, Visual C++ runtimes, launcher setup

Custom Wine prefix in Lutris:
  Right-click game → Configure → Runner Options → Wine version, prefix path
  Game Options → Executable path
  System Options → Environment variables

Wine runners in Lutris:
  wine-ge (GloriousEggroll): https://github.com/GloriousEggrollMaster/wine-ge-custom
  Download in Lutris: Runners → Wine → Download icon
```

---

## 9. Bottles — GUI Wine Manager

Bottles is a modern GNOME app for managing Wine environments with a clean UI, focused on app (not just game) compatibility.

```
Install:
  flatpak install flathub com.usebottles.bottles

Concepts:
  Bottle = Wine prefix with configuration
  Environment presets: Gaming, Application, Custom
  
Features:
  Per-bottle component management (DXVK, VKD3D, .NET, VC++ runtimes)
  Backup/restore bottles
  Dependency manager (installable components with one click)
  Steam integration (detect and run Steam games)
  Sandboxed Flatpak: bottles don't interfere with system Wine

Create a bottle for Photoshop:
  Bottles → + New Bottle
  Name: Photoshop
  Environment: Application
  After creation → Install Dependencies: vcrun2019, dotnet48
  → Install Photoshop: Run Executable → select setup.exe
```

---

## 10. Configuration & Tweaks

### winecfg

```bash
WINEPREFIX=~/.wine-myapp winecfg
# Opens Wine configuration GUI:
  Applications tab: Windows version per application (Win10, Win7, XP...)
  Libraries tab: Override DLLs (native vs builtin)
    Important: set specific DLLs to "native, builtin" for better compatibility
    Example: force native d3d11.dll to use DXVK's version
  Graphics tab: screen resolution, virtual desktop, multisampling
  Audio tab: driver selection (PulseAudio, ALSA)
  Drives tab: map drive letters to Linux paths
```

### DLL Override (Manual)

```bash
# Override a specific DLL to use native (system) version
WINEDLLOVERRIDES="d3d11=n,b" wine game.exe
#   n = native (use Windows version from filesystem)
#   b = builtin (use Wine's implementation)
#   n,b = try native first, fall back to builtin

# Common overrides:
WINEDLLOVERRIDES="mscoree=n;mshtml=n" wine app.exe  # Use .NET and IE native
WINEDLLOVERRIDES="d3d9=n;d3d11=n;dxgi=n" wine game.exe  # Force DXVK

# Set permanently in prefix via winecfg → Libraries tab
```

### esync / fsync (Faster Synchronization)

```bash
# esync: eventfd-based synchronization (replaces wineserver for sync objects)
# Dramatically reduces CPU usage and improves performance in busy games
# Requires: system max open files ≥ 524288

# Check current limit:
ulimit -Hn

# Set limit (for current session):
ulimit -n 524288

# Permanent (add to /etc/security/limits.conf):
# username hard nofile 524288

# Enable esync:
WINESYNC=1 wine game.exe        # fsync (newer, better — if kernel supports it)
WINEESYNC=1 wine game.exe       # esync (older, more compatible)

# Proton enables these automatically when available
```

---

## 11. Common Issues & Fixes

```
Issue: "cannot find L"C:\\windows\\system32\\..."
  Fix: Run: wineboot && wine cmd /c "reg add ..."
  Or: wineboot -u (reinitialize prefix links)

Issue: Missing DLL (e.g., msvcp140.dll not found)
  Fix: winetricks vcrun2019   (Visual C++ 2015-2019 runtime)
       winetricks vcrun2022   (Visual C++ 2022)

Issue: .NET application crashes
  Fix: winetricks dotnet48
       or: winetricks mono (Wine's .NET replacement)

Issue: No audio
  Fix: Check audio driver in winecfg
       sudo apt install libpulse-dev:i386 (for 32-bit apps)
       Try: pasuspender -- wine game.exe (reset PulseAudio)

Issue: Fonts look wrong / missing
  Fix: winetricks corefonts
       winetricks allfonts

Issue: DirectX game won't start
  Fix: Install DXVK: winetricks dxvk
       Install DirectX: winetricks d3dx9 d3dcompiler_47

Issue: Anti-cheat blocks Wine (EAC, BattlEye)
  Cannot fix: these use kernel drivers unavailable in Wine
  Modern EAC/BattlEye on Linux: some games now natively support Linux via
  EAC/BattlEye's Linux support — enabled by game developer in Proton

Issue: Game runs but screen is black
  Fix: Try different Wine version; try PROTON_USE_WINED3D=1; try windowed mode first

Issue: 32-bit app fails on 64-bit system
  Fix: WINEARCH=win32 WINEPREFIX=~/.wine32 wine app.exe
       sudo dpkg --add-architecture i386 && sudo apt install wine32
```

---

## 12. Wine on macOS

```
CrossOver (commercial Wine for macOS, by CodeWeavers):
  $74/year or $494 perpetual
  Polished UI, curated app/game support, tech support
  Best for: professional Windows apps (Office, Adobe, etc.)
  https://www.codeweavers.com/crossover

Whisky (free, open source macOS Wine frontend):
  Modern SwiftUI app wrapping Wine
  Easy game/app installation with Bottle management
  Installs via Homebrew or .dmg
  https://getwhisky.app

  brew install --cask whisky

GPTK (Game Porting Toolkit, Apple, macOS 14+):
  Apple's own D3DMetal translation layer
  DirectX 12 → Metal (Apple's GPU API)
  Better performance than DXVK on Apple Silicon
  Integrated in Whisky as a rendering backend
  Best for: modern DX12 games on Mac

Rosetta 2 + Wine:
  On Apple Silicon (M-series):
  Wine runs under Rosetta 2 (x86-64 → ARM64 translation)
  Performance: surprisingly good (~native for Wine workloads)
  No need for separate ARM builds of Windows apps
```

---

## See Also

- [File Systems](file-systems.md) — The filesystem Wine's C: drive sits on
- [Virtualization](virtualization.md) — Full VM alternative when Wine fails
- [Linux Distributions](linux-distributions.md) — Linux Wine compatibility varies by distro
- [GPU Architecture](gpu-architecture.md) — DXVK Vulkan translation uses GPU driver
