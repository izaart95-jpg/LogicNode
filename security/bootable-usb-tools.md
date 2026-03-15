# Bootable USB Tools

A guide to creating bootable USB drives for installing operating systems, running live environments, performing system recovery, and maintaining portable security toolkits. This document covers the leading tools Rufus and Ventoy, along with other utilities and a comparison of features.

> **Disclaimer:** The tools described in this document are intended for **legitimate system administration, authorized security testing, and educational purposes only**. Creating bootable media for unauthorized access to systems or bypassing security controls without permission is illegal. Always ensure you have authorization before booting into any system.

---

## Table of Contents

1. [Why Bootable USB?](#1-why-bootable-usb)
2. [Rufus](#2-rufus)
3. [Ventoy](#3-ventoy)
4. [Other Tools](#4-other-tools)
5. [Comparison Table](#5-comparison-table)
6. [See Also](#6-see-also)

---

## 1. Why Bootable USB?

### 1.1 Use Cases

Bootable USB drives serve several critical purposes:

- **OS Installation:** Install Windows, Linux, or other operating systems from USB media
- **Live OS Testing:** Try Linux distributions without installing them to disk
- **System Recovery:** Boot into a repair environment when the primary OS fails
- **Portable Environments:** Carry a complete working OS and toolset on a USB drive
- **Security Testing:** Boot into specialized distributions like Kali Linux or Tails
- **Disk Utilities:** Run partitioning tools, data recovery software, or antivirus scanners from a clean environment

### 1.2 UEFI vs Legacy BIOS Boot Modes

| Feature | Legacy BIOS | UEFI |
|---------|------------|------|
| **Partition Table** | MBR (Master Boot Record) | GPT (GUID Partition Table) |
| **Max Disk Size** | 2 TB | 9.4 ZB (effectively unlimited) |
| **Max Partitions** | 4 primary (or 3 + extended) | 128 partitions |
| **Boot Speed** | Slower | Faster |
| **Secure Boot** | Not supported | Supported |
| **Compatibility** | Older hardware | Modern hardware (2012+) |

Most modern systems use UEFI. When creating bootable USB drives, you must match the boot mode of the target system. Some tools (like Rufus) let you choose the partition scheme (MBR for BIOS, GPT for UEFI) during creation.

---

## 2. Rufus

### 2.1 Overview

Rufus is a lightweight, fast, and reliable Windows utility for creating bootable USB drives. It is one of the most popular tools for writing ISO images to USB and supports a wide range of formats and configurations.

- **Website:** https://rufus.ie
- **Developer:** Pete Batard (pbatard)
- **License:** GPLv3
- **Platform:** Windows only (7 and later)
- **Size:** ~1.5 MB

### 2.2 Supported Formats

- ISO images (Linux distributions, Windows installers, utilities)
- IMG / VHD / VHDX disk images
- DD images
- Windows To Go (portable Windows installation)

### 2.3 Key Features

- **GPT/MBR Partition Schemes:** Full support for both UEFI and Legacy BIOS boot modes
- **File Systems:** FAT32, NTFS, UDF, exFAT, ext2/ext3/ext4
- **Persistent Storage:** Create persistent partitions for Linux live environments (Ubuntu, Debian, etc.)
- **Windows To Go:** Install a portable Windows environment on USB
- **Floppy Disk Images:** Create bootable floppy images (FreeDOS, MS-DOS)
- **Checksum Verification:** Verify ISO integrity (MD5, SHA-1, SHA-256) before writing
- **UEFI + Secure Boot:** Supports UEFI:NTFS for large Windows ISOs with Secure Boot

### 2.4 Step-by-Step Usage

1. **Download Rufus** from https://rufus.ie (standard or portable version)
2. **Insert USB Drive** (all data will be erased)
3. **Select Device:** Choose your USB drive from the Device dropdown
4. **Select ISO:** Click SELECT and browse to your ISO file
5. **Choose Partition Scheme:**
   - **GPT** for UEFI systems (most modern computers)
   - **MBR** for Legacy BIOS or UEFI-CSM systems
6. **Choose File System:** FAT32 for most Linux ISOs, NTFS for large Windows ISOs
7. **Click START** and wait for the process to complete

```bash
# Rufus is GUI-only on Windows, but you can automate via command line:
# Download portable version
# rufus-4.x.exe -h   (shows command-line help)

# Example: Non-interactive mode (advanced)
rufus-4.x.exe -i image.iso -d X: -p gpt -t fat32 -n "BOOT_USB"
```

### 2.5 Advanced: Portable Mode

Rufus runs in portable mode when placed in a directory containing a file named `rufus.ini`. In portable mode, all settings are stored in the INI file instead of the Windows registry, making it ideal for carrying on a USB drive alongside your ISOs.

```bash
# Create rufus.ini in the same directory as rufus.exe
# to enable portable mode (empty file is sufficient)
```

---

## 3. Ventoy

### 3.1 Overview

Ventoy is a revolutionary bootable USB tool that takes a fundamentally different approach: install Ventoy once to the USB drive, then simply copy ISO files onto it. No need to reformat or rewrite the drive for each new image. You can store multiple ISOs and select which one to boot from a menu.

- **Website:** https://www.ventoy.net
- **Source:** https://github.com/ventoy/Ventoy
- **License:** GPLv3
- **Platforms:** Windows, Linux (for installation)

### 3.2 Key Features

- **Multi-ISO Boot:** Store unlimited ISO/IMG/WIM/VHD files on one USB drive
- **No Reformatting:** Add or remove ISOs by simply copying/deleting files
- **Wide Compatibility:** Tested with 900+ ISO files (Linux distros, Windows installers, WinPE, utilities)
- **Persistence Support:** Configure persistent storage for Linux live environments via plugin
- **Secure Boot:** Supports UEFI Secure Boot (requires enrolling Ventoy certificate)
- **Plugin System:** Themes, auto-install scripts, persistence, injection, and more
- **Large Drive Support:** Works with USB drives of any size

### 3.3 Installation

```bash
# Linux installation
# Download from https://github.com/ventoy/Ventoy/releases
tar -xzf ventoy-*-linux.tar.gz
cd ventoy-*

# Install Ventoy to USB drive (WARNING: destroys all data on target)
sudo ./Ventoy2Disk.sh -i /dev/sdX

# Update existing Ventoy installation (preserves ISOs)
sudo ./Ventoy2Disk.sh -u /dev/sdX
```

```bash
# Windows installation
# Run Ventoy2Disk.exe
# Select the USB drive
# Click Install (first time) or Update (existing installation)
```

After installation, the USB drive has two partitions:
- **Partition 1 (exFAT):** Data partition where you copy ISO files
- **Partition 2 (EFI):** Ventoy boot partition (do not modify)

### 3.4 Usage

Simply copy ISO files to the data partition:

```bash
# Copy ISOs to the Ventoy USB drive
cp ubuntu-24.04-desktop-amd64.iso /media/user/Ventoy/
cp kali-linux-2024.1-installer-amd64.iso /media/user/Ventoy/
cp Win11_English_x64.iso /media/user/Ventoy/

# Organize with directories (Ventoy searches recursively)
mkdir -p /media/user/Ventoy/linux /media/user/Ventoy/windows
cp *.iso /media/user/Ventoy/linux/
```

Boot from the USB drive and a menu displays all available ISOs. Select one to boot.

### 3.5 Plugin System

Ventoy plugins are configured via a JSON file at `/ventoy/ventoy.json` on the data partition.

```bash
# Example: /ventoy/ventoy.json
# Configure a theme and persistence
{
    "theme": {
        "file": "/ventoy/themes/flavor/theme.txt"
    },
    "persistence": [
        {
            "image": "/linux/ubuntu-24.04-desktop-amd64.iso",
            "backend": "/ventoy/persistence/ubuntu.dat"
        }
    ]
}
```

```bash
# Create a persistence file for Ubuntu
# (creates a 4GB ext4 image for persistent storage)
sudo ./CreatePersistentImg.sh -s 4096 -l casper-rw
cp persistence.dat /media/user/Ventoy/ventoy/persistence/ubuntu.dat
```

### 3.6 Secure Boot Support

Ventoy supports UEFI Secure Boot but requires enrolling the Ventoy certificate (ENROLL_THIS_KEY_IN_MOKMANAGER.cer) on first boot:

1. Boot from the Ventoy USB with Secure Boot enabled
2. Select "Enroll Key from disk" in the MOK Manager
3. Navigate to the Ventoy partition and select the certificate
4. Reboot — Ventoy will now boot with Secure Boot

### 3.7 VentoyPlugson

VentoyPlugson is a web-based GUI for configuring Ventoy plugins without manually editing JSON files.

```bash
# Launch VentoyPlugson (Linux)
sudo ./VentoyPlugson.sh /dev/sdX

# Opens a browser interface at http://127.0.0.1:24681
# Configure themes, persistence, auto-install, and more via the GUI
```

### 3.8 Ventoy vs Rufus

| Feature | Ventoy | Rufus |
|---------|--------|-------|
| **Multi-ISO** | Yes (unlimited) | No (one ISO per write) |
| **Reformat Required** | No (copy files) | Yes (each new ISO) |
| **Boot Menu** | Yes (select from list) | N/A |
| **Speed** | Instant (just copy ISO) | Must write entire ISO each time |
| **Platform** | Windows, Linux | Windows only |
| **Persistent Storage** | Plugin-based | Built-in option |
| **Best For** | Multi-boot USB, testing many ISOs | Single-purpose bootable USB |

---

## 4. Other Tools

### 4.1 BalenaEtcher

BalenaEtcher is a cross-platform (Windows, macOS, Linux) tool focused on simplicity. It features a clean three-step interface: select image, select drive, flash.

- **Website:** https://etcher.balena.io
- **Pros:** Extremely simple, validates writes, cross-platform
- **Cons:** No multi-ISO support, no advanced options (partition scheme, file system), large Electron-based app (~130 MB)

### 4.2 dd (Linux Command)

The `dd` command is a low-level Unix utility that can write raw disk images to USB drives. It offers maximum flexibility but no safety nets — writing to the wrong device will destroy data.

```bash
# Write an ISO to a USB drive using dd
# CAUTION: Double-check the target device (/dev/sdX)
sudo dd if=image.iso of=/dev/sdX bs=4M status=progress oflag=sync

# Verify the write
sync
```

**Warning:** `dd` has no confirmation prompt. The target device (`of=`) is overwritten immediately. Misidentifying the target drive can result in catastrophic data loss. Always verify the correct device with `lsblk` before running.

### 4.3 UNetbootin

UNetbootin (Universal Netboot Installer) is a cross-platform tool that can create bootable USB drives and also download Linux distributions directly within the app.

- **Website:** https://unetbootin.github.io
- **Pros:** Built-in distro downloader, cross-platform, supports persistence
- **Cons:** Less reliable with newer ISOs, known compatibility issues with some distributions, slower than alternatives

---

## 5. Comparison Table

| Tool | Platform | Multi-ISO | Persistent Storage | UEFI Support | Open Source | Ease of Use |
|------|----------|-----------|-------------------|--------------|-------------|-------------|
| **Rufus** | Windows | No | Yes (Linux) | Yes (GPT) | Yes (GPLv3) | Easy |
| **Ventoy** | Windows, Linux | Yes | Yes (plugin) | Yes (GPT) | Yes (GPLv3) | Easy |
| **BalenaEtcher** | Windows, Linux, macOS | No | No | Yes | Yes (Apache 2.0) | Very Easy |
| **dd** | Linux, macOS | No | No | Yes | Yes (coreutils) | Advanced |
| **UNetbootin** | Windows, Linux, macOS | No | Yes (limited) | Partial | Yes (GPLv2) | Easy |

---

## 6. See Also

- [Termux Pentesting](../mobile/termux-pentesting.md) — Mobile penetration testing tools and setup
- [Linux Distributions](../fundamentals/linux-distributions.md) — Overview of Linux distributions including security-focused options
