# Kali NetHunter Rootless Installation Guide

## 1. Overview

**Kali NetHunter Rootless** is a penetration testing platform designed for Android devices that does not require root access. It runs inside a **proot** environment within **Termux**. 

While it provides access to most Kali tools, it lacks low-level hardware access (such as WiFi monitor mode) due to the absence of root privileges.

---

## 2. Prerequisites

Before beginning, ensure the following requirements are met:

| Requirement | Details |
| :--- | :--- |
| **Device** | Android Smartphone or Tablet (ARM/ARM64) |
| **Storage** | At least 10 GB of free space recommended |
| **Terminal App** | **Termux** (Must be downloaded from **F-Droid**, not Play Store) |
| **Internet** | Stable connection for downloading rootfs packages |
| **Battery** | Device should be charged or plugged in during installation |

> **⚠️ Important:** The Google Play Store version of Termux is outdated and no longer supported. Using it will cause installation failures. Download Termux from [F-Droid](https://f-droid.org/en/packages/com.termux/).

---

## 3. Installation Steps

### Step 1: Prepare Termux
Open Termux and grant storage permissions. Then update the package repository.

```bash
# Grant storage access
termux-setup-storage

# Update and upgrade packages
pkg update && pkg upgrade -y

# Install necessary dependencies
pkg install wget -y
```

### Step 2: Download the Installer
Download the official NetHunter installation script.

```bash
# Download the installer script
wget -O install-nethunter-termux https://offs.ec/2MceZWr

# Verify download (optional but recommended)
# sha256sum install-nethunter-termux

# Make the script executable
chmod 755 install-nethunter-termux
```

### Step 3: Run the Installer
Execute the script to begin the installation process.

```bash
# Run the installer
./install-nethunter-termux
```

**During Installation:**
1.  **Image Selection:** You will be prompted to choose between a **Full** image (~2 GB) or a **Minimal** image (~500 MB). 
    - *Recommendation:* Choose **Minimal** if storage is limited; choose **Full** for all tools pre-installed.
2.  **KeX Password:** Set a password for the graphical interface (KeX). Remember this password.
3.  **Confirmation:** Type `Y` to confirm installation.

---

## 4. Launching NetHunter

Once installation is complete, you can launch the NetHunter environment using the `nh` command.

### Command Line Interface (CLI)
```bash
# Launch NetHunter CLI
nh

# Exit NetHunter
exit
```

### Custom Commands
You can run specific tools directly without entering the shell:
```bash
# Run nmap inside NetHunter
nh nmap -v target.com

# Run metasploit inside NetHunter
nh msfconsole
```

---

## 5. Graphical Interface (KeX)

NetHunter includes **KeX**, a VNC-based graphical environment to run GUI tools (e.g., Burp Suite, OWASP ZAP).

### Starting KeX
```bash
# Start the KeX server (default port 5901)
nh kex start

# Start KeX with specific resolution
nh kex start --res 1920x1080
```

### Connecting to KeX
1.  Install a VNC Viewer app on your Android device (e.g., "bVNC" or "RealVNC").
2.  Connect to `localhost:5901` (or `127.0.0.1:5901`).
3.  Enter the password set during installation.

### Stopping KeX
```bash
# Stop the KeX server
nh kex stop
```

### Killing KeX (If stuck)
```bash
# Force kill KeX sessions
nh kex kill
```

---

## 6. Limitations (Rootless vs. Rooted)

Since this installation is **Rootless**, certain hardware-level features are unavailable.

| Feature | Rootless NetHunter | Rooted NetHunter |
| :--- | :--- | :--- |
| **Kali Tools** | ✅ Available | ✅ Available |
| **GUI (KeX)** | ✅ Available | ✅ Available |
| **WiFi Monitor Mode** | ❌ Not Supported | ✅ Supported (with compatible adapter) |
| **Packet Injection** | ❌ Not Supported | ✅ Supported |
| **HID Attacks** | ❌ Not Supported | ✅ Supported (via USB) |
| **Bluetooth Attacks** | ⚠️ Limited | ✅ Full Access |
| **Performance** | ⚠️ Slight Overhead (proot) | ✅ Native Performance |

---

## 7. Troubleshooting

### Issue: `permission denied` when running `./install-nethunter-termux`
- **Fix:** Ensure you ran `chmod 755 install-nethunter-termux`.

### Issue: `proot` error or `signal 11`
- **Fix:** This is often due to an outdated Termux version. Reinstall Termux from F-Droid and run `pkg update` again.

### Issue: KeX won't start
- **Fix:** 
  1. Ensure no other VNC server is running on port 5901.
  2. Try killing existing sessions: `nh kex kill`.
  3. Check storage permissions: `termux-setup-storage`.

### Issue: `nh` command not found
- **Fix:** Ensure you are in the Termux environment, not inside another shell. If installed elsewhere, try sourcing the bashrc: `source ~/.bashrc`.

---

## 8. Uninstallation

To remove NetHunter completely:

```bash
# Remove the NetHunter rootfs
rm -rf ~/nethunter-rootfs

# Remove the launcher script
rm -rf ~/bin/nh

# Remove the installer
rm install-nethunter-termux
```

---

## 9. See Also
- [Kali NetHunter Official Docs](https://www.kali.org/docs/nethunter/)
- [Termux Wiki](https://wiki.termux.com/wiki/Main_Page)
- [NetHunter GitHub Repository](https://github.com/offensive-security/kali-nethunter)
