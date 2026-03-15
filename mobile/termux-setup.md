# Termux Documentation

## 📌 What is Termux?

Termux is an Android terminal emulator and Linux environment app that allows you to run a minimal Linux system without rooting your device. It provides access to a package manager and supports many common Linux tools.
Official Sites: https://github.com/termux/termux-app & https://termux.dev/en/

---

## 📥 Installation

### From F-Droid (Recommended)
1. Install F-Droid from: https://f-droid.org
2. Search for **Termux**
3. Install the latest version

> ⚠️ The Google Play version is outdated. Use F-Droid for the latest updates.

---

## 🚀 First Setup

After installing, open Termux and run:

```bash
pkg update && pkg upgrade -y 
```

### Optional Basic Tools And Useful Scripts
```bash
pkg install git curl wget nano vim -y
```
```bash
pkg install root-repo
pkg install x11-repo
```
## 📦 Package Management
Termux uses pkg as a wrapper for apt.
### Update packages
```bash
pkg update
```
### Upgrade packages
```bash
pkg upgrade
```
### Install Package
```bash
pkg install <package-name>
```
### Search For a Package
```bash
pkg search <query>
```
### Remove package
```bash
pkg uninstall <name>
```
## File System Basics
- Home Directory
```bash
/data/data/com.termux/files/home
```
- Access Shared Storage
```bash
termux-setup-storage
```
Storage Path
```bash
/storage/emulated/0
```

### 🛠 Useful Commands

| Command | Description |
| :--- | :--- |
| `ls` | List files |
| `cd` | Change directory |
| `pwd` | Show current directory |
| `cp` | Copy files |
| `mv` | Move files |
| `rm` | Delete files |
| `mkdir` | Create directory |

# 🐍 Install Programming Languages

## **Python**
To install Python, run:
```bash
pkg install python
```

## Node.js
```bash
pkg install nodejs
```
## C/C++
```bash
pkg install clang
```
## PHP
```bash
pkg install php
```
# Running a Simple Web Server (Python Example)
```bash
python -m http.server 8080
```
Access From Browser
http://localhost:8080
# SSH Usage
## Install openssh
```bash
pkg install openssh
```
## Connect to remote server 
```bash
ssh user@ip-address
```
# Git Usage
## Install Git
```bash
pkg install git
```
Clone Repo
```bash
git clone https://github.com/username/repo.git
```
# ⚙️ Change Repository (If Needed)
```bash
termux-change-repo
```
Choose official repos

# 🧹 Cleaning Cache
```bash
pkg clean
```
# 📱 Extra Termux APIs
Install termux API | API = Application Programming Interface
```bash
pkg install termux-api
```
Download Temux Api App

Example Usage
```bash
termux-battery-status
termux-toast "Hello from Termux"
```
# 🔥 Tips & Best Practices
- pkg update regularly
- Backup Important Files
- pkg autoclean to clean unwanted packages
- use -y flag to auto accept prompts for example
```bash
pkg update -y
```

# 📚 Useful Packages
```bash
pkg install htop neovim tmux zsh fish ffmpeg
```

# Pro Tip
## You can enable a GUI for Termux by following the setup guide at: https://github.com/sabamdarif/termux-desktop