# Headless Desktop Environment Installation Guide

This guide covers installing Graphical Desktop Environments (DE) on minimal headless Linux systems (Debian/Ubuntu/Arch) and configuring access via **TigerVNC** or **Local X11**. Includes a bonus section for **Termux X11** on Android.

> **⚠️ Resource Warning:** GNOME and KDE Plasma are resource-intensive. For headless/VPS/Proot environments, **XFCE**, **LXDE**, or **LXQT** are strongly recommended.

---

## 1. Prerequisites

Update your package manager and install base utilities before proceeding.

### Debian/Ubuntu (apt)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git nano tasksel
```

### Arch Linux (pacman)
```bash
sudo pacman -Syu
sudo pacman -S --needed base-devel curl wget git nano
```

---

## 2. Installing Desktop Environments

Choose **one** of the following environments. Installing multiple may cause conflicts.

| # | Desktop Environment | Package (Debian/Ubuntu) | Package (Arch) | Resource Usage |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **LXDE** | `lxde-core` | `lxde-group` | 🟢 Very Low |
| 2 | **LXQT** | `lxqt-core` | `lxqt-group` | 🟢 Very Low |
| 3 | **XFCE** | `xfce4` | `xfce4` | 🟡 Low |
| 4 | **GNOME** | `gnome-core` | `gnome` | 🔴 High |
| 5 | **KDE Plasma** | `kde-plasma-desktop` | `plasma-desktop` | 🟠 Medium/High |

### Installation Commands

#### Option 1: LXDE (Lightweight)
```bash
# Debian/Ubuntu
sudo apt install -y lxde-core lxappearance

# Arch
sudo pacman -S lxde-group
```

#### Option 2: LXQT (Modern Lightweight)
```bash
# Debian/Ubuntu
sudo apt install -y lxqt-core lxqt-config

# Arch
sudo pacman -S lxqt-group
```

#### Option 3: XFCE (Balanced)
```bash
# Debian/Ubuntu
sudo apt install -y xfce4 xfce4-goodies

# Arch
sudo pacman -S xfce4 xfce4-goodies
```

#### Option 4: GNOME (Heavy)
```bash
# Debian/Ubuntu
sudo apt install -y gnome-core gnome-tweaks

# Arch
sudo pacman -S gnome
```

#### Option 5: KDE Plasma (Feature Rich)
```bash
# Debian/Ubuntu
sudo apt install -y kde-plasma-desktop dolphin konsole

# Arch
sudo pacman -S plasma-desktop
```

---

## 3. Access Method 1: TigerVNC (Standalone Server)

Best for remote access over network without physical monitoring.

### Step 1: Install TigerVNC
```bash
# Debian/Ubuntu
sudo apt install -y tigervnc-standalone-server tigervnc-common

# Arch
sudo pacman -S tigervnc
```

### Step 2: Set VNC Password
```bash
vncpasswd
# Enter a password (view-only password optional)
```

### Step 3: Configure Startup Script
Create/edit `~/.vnc/xstartup` to launch your DE.

```bash
nano ~/.vnc/xstartup
```

**Paste the following based on your DE:**

```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec /etc/X11/Xsession

# Uncomment ONE of the following based on your installed DE:

# LXDE
# exec startlxde

# LXQT
# exec startlxqt

# XFCE
# exec startxfce4

# GNOME (Requires gnome-session-binary)
# exec gnome-session

# KDE Plasma
# exec startplasma-x11
```

**Make executable:**
```bash
chmod +x ~/.vnc/xstartup
```

### Step 4: Start VNC Server
```bash
# Start on display :1
vncserver :1 -geometry 1920x1080 -depth 24

# Stop server
vncserver -kill :1
```

### Step 5: Connect
Use a VNC Client (RealVNC, TigerVNC Viewer) to connect to:
`<IP_ADDRESS>:5901` (Port is 5900 + Display Number)

---

## 4. Access Method 2: Local X11 (Xorg)

Best for local monitoring or nested X servers (Xephyr). Requires a display manager or `startx`.

### Step 1: Install Xorg
```bash
# Debian/Ubuntu
sudo apt install -y xorg xinit

# Arch
sudo pacman -S xorg xorg-init
```

### Step 2: Configure .xinitrc
Edit `~/.xinitrc` to launch your DE when `startx` is run.

```bash
nano ~/.xinitrc
```

**Add at the end:**
```bash
# LXDE
exec startlxde

# XFCE
exec startxfce4

# KDE
exec startplasma-x11
```

### Step 3: Launch
```bash
startx
```

> **Note for Headless Servers:** If no physical monitor is attached, Xorg may fail. Use **Xvfb** (Virtual Framebuffer) instead:
> ```bash
> sudo apt install xvfb
> Xvfb :1 -screen 0 1920x1080x24 &
> export DISPLAY=:1
> startxfce4 &
> ```

---

## 5. Bonus: Termux X11 & PulseAudio (Android)

Specific setup for running Linux DEs inside Termux using the **Termux:X11** Android app (lower latency than VNC).

### Step 1: Prepare Termux
```bash
# Enable X11 repo
pkg install x11-repo

# Install Termux X11 loader and audio
pkg install termux-x11-nightly pulseaudio
```

### Step 2: Prepare Linux Environment (Proot/Chroot)
Inside your Linux environment (e.g., Ubuntu via proot-distro):

```bash
# Install DE (e.g., XFCE) and X11 apps
sudo apt update
sudo apt install -y xfce4 termux-x11 x11-apps

# Install PulseAudio for sound forwarding
sudo apt install -y pulseaudio
```

### Step 3: Configure PulseAudio (Linux Side)
Edit `/etc/pulse/client.conf` or create `~/.pulse/client.conf`:
```ini
default-server = 127.0.0.1
```

### Step 4: Launch Sequence

1.  **Open Termux:X11 App** on Android.
2.  **In Termux Shell:**
    ```bash
    # Start PulseAudio
    pulseaudio --start --load="module-native-protocol-tcp auth-anonymous=1"

    # Start X11 Session
    termux-x11 :0 &
    ```
3.  **In Linux Environment (Proot):**
    ```bash
    # Set Display
    export DISPLAY=:0

    # Start Audio Client
    pulseaudio --start --daemon=false

    # Launch DE
    startxfce4
    ```

---

## 6. Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **VNC Black Screen** | Check `~/.vnc/xstartup` is executable (`chmod +x`). Ensure DE is installed correctly. |
| **GNOME/KDE Crash** | These DEs often require `systemd`. In Proot/Chroot, use `XFCE` or `LXQT` instead. |
| **No Audio (VNC)** | Install `pulseaudio-utils` on client and server. Tunnel audio via SSH (`ssh -X`). |
| **Termux X11 Lag** | Ensure "Force GPU Rendering" is on in Android Developer Options. Use XFCE/LXQT. |
| **Clipboard Sync** | Install `autocutsel` or `parcellite` inside the Linux environment. |

---

## 7. Security Recommendations

1.  **SSH Tunneling:** Never expose VNC (port 5901) directly to the internet.
    ```bash
    # Connect via SSH Tunnel
    ssh -L 5901:localhost:5901 user@server
    # Then connect VNC client to localhost:5901
    ```
2.  **Firewall:** Block port 5901 on `ufw` or `iptables` unless tunneling.
3.  **Encryption:** VNC password is weakly encrypted. Use SSH tunnels for encryption.
