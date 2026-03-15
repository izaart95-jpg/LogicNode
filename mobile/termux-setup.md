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

---

# 🖥️ Tmux (Terminal Multiplexer)

Tmux lets you run multiple terminal sessions inside a single window, and keeps sessions alive when you disconnect.

## Install
```bash
pkg install tmux
```

## Core Concepts
- **Session** — A collection of windows (persists when detached)
- **Window** — A full-screen tab within a session
- **Pane** — A split within a window

## Essential Commands
```bash
# Start new session
tmux

# Start named session
tmux new -s mysession

# Detach from session
# Press: Ctrl+b, then d

# List sessions
tmux ls

# Reattach to session
tmux attach -t mysession

# Kill session
tmux kill-session -t mysession
```

## Key Bindings (prefix: Ctrl+b)

| Key | Action |
|-----|--------|
| `c` | Create new window |
| `n` | Next window |
| `p` | Previous window |
| `,` | Rename window |
| `%` | Split pane horizontally |
| `"` | Split pane vertically |
| `Arrow keys` | Navigate panes |
| `z` | Toggle pane zoom (fullscreen) |
| `d` | Detach session |
| `[` | Enter copy/scroll mode (q to exit) |

## Basic Configuration (~/.tmux.conf)
```bash
# Enable mouse support
set -g mouse on

# Set prefix to Ctrl+a (easier than Ctrl+b)
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Start windows at 1 instead of 0
set -g base-index 1

# Faster escape time
set -sg escape-time 10

# Increase scrollback buffer
set -g history-limit 10000
```

> **See Also:** [Terminal Tools](../devtools/terminal-tools.md) for a full Tmux guide with plugins and advanced configuration

---

# 🎬 FFmpeg in Termux

FFmpeg is a powerful multimedia tool for converting, streaming, and processing audio/video.

```bash
pkg install ffmpeg
```

**Quick examples:**
```bash
# Convert video format
ffmpeg -i input.mp4 output.avi

# Extract audio from video
ffmpeg -i video.mp4 -vn audio.mp3

# Compress video
ffmpeg -i input.mp4 -crf 28 output.mp4

# Trim video (start at 1:00, 30 seconds)
ffmpeg -i input.mp4 -ss 00:01:00 -t 00:00:30 -c copy clip.mp4
```

> **See Also:** [Media Tools](../media/media-tools.md) for the complete FFmpeg reference with filters, streaming, and batch processing

---

# Pro Tip
## You can enable a GUI for Termux by following the setup guide at: https://github.com/sabamdarif/termux-desktop