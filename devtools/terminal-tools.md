# Terminal Tools — Tmux, Tabby & Modern Terminal Emulators

The terminal remains the most powerful interface for developers and system administrators. Modern terminal emulators and multiplexers extend the classic shell experience with GPU-accelerated rendering, session persistence, split panes, and built-in SSH management. This guide covers the essential terminal tools for productive command-line work.

---

## Table of Contents
1. [Tmux (Terminal Multiplexer)](#1-tmux-terminal-multiplexer)
2. [Tabby](#2-tabby)
3. [Other Notable Terminals](#3-other-notable-terminals)
4. [Comparison Table](#4-comparison-table)

---

## 1. Tmux (Terminal Multiplexer)

### What is Tmux?

Tmux is a terminal multiplexer that lets you create multiple terminal sessions within a single window, detach from them, and reattach later. Sessions persist even if your SSH connection drops, making tmux essential for remote work.

### Installation

```bash
# Debian/Ubuntu
sudo apt install tmux

# Fedora/RHEL
sudo dnf install tmux

# macOS
brew install tmux

# Arch Linux
sudo pacman -S tmux

# Verify
tmux -V
```

### Core Concepts

```
┌─────────────────────────────────────────────────────┐
│  tmux server                                        │
│                                                     │
│  ┌─── Session: "dev" ───────────────────────────┐   │
│  │                                               │   │
│  │  ┌─ Window 0: "editor" ──┐  ┌─ Window 1 ──┐ │   │
│  │  │  ┌─────┐ ┌─────────┐  │  │             │ │   │
│  │  │  │Pane │ │  Pane   │  │  │   Pane 0   │ │   │
│  │  │  │  0  │ │   1     │  │  │             │ │   │
│  │  │  └─────┘ └─────────┘  │  └─────────────┘ │   │
│  │  └────────────────────────┘                   │   │
│  └───────────────────────────────────────────────┘   │
│                                                     │
│  ┌─── Session: "server" ────────────────────────┐   │
│  │  ...                                          │   │
│  └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

- **Session** — a collection of windows managed by tmux; can be detached/reattached
- **Window** — a full-screen tab within a session (like browser tabs)
- **Pane** — a split within a window (horizontal or vertical)

### Essential Keybindings

All tmux commands use a prefix key (default: `Ctrl+b`), followed by a command key.

#### Session Management

| Keybinding | Action |
|------------|--------|
| `tmux new -s name` | Create a new named session |
| `tmux attach -t name` | Attach to an existing session |
| `tmux ls` | List all sessions |
| `Ctrl+b d` | Detach from current session |
| `Ctrl+b s` | Interactive session switcher |
| `Ctrl+b $` | Rename current session |
| `tmux kill-session -t name` | Kill a session |

#### Window Management

| Keybinding | Action |
|------------|--------|
| `Ctrl+b c` | Create a new window |
| `Ctrl+b n` | Next window |
| `Ctrl+b p` | Previous window |
| `Ctrl+b 0-9` | Switch to window by number |
| `Ctrl+b ,` | Rename current window |
| `Ctrl+b w` | Interactive window list |
| `Ctrl+b &` | Close current window (confirm) |

#### Pane Management

| Keybinding | Action |
|------------|--------|
| `Ctrl+b %` | Split pane horizontally (left/right) |
| `Ctrl+b "` | Split pane vertically (top/bottom) |
| `Ctrl+b Arrow` | Navigate between panes |
| `Ctrl+b z` | Zoom/unzoom current pane (fullscreen toggle) |
| `Ctrl+b x` | Close current pane (confirm) |
| `Ctrl+b {` / `}` | Swap pane position |
| `Ctrl+b Ctrl+Arrow` | Resize pane (hold Ctrl, press arrow) |
| `Ctrl+b Space` | Cycle through pane layouts |

### Configuration (~/.tmux.conf)

```bash
# Remap prefix from Ctrl+b to Ctrl+a (more ergonomic)
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Enable mouse support (click panes, resize, scroll)
set -g mouse on

# Start window numbering at 1 (not 0)
set -g base-index 1
setw -g pane-base-index 1

# Increase scrollback buffer
set -g history-limit 50000

# Reduce escape key delay (important for Vim users)
set -sg escape-time 10

# Use vi keybindings in copy mode
setw -g mode-keys vi

# Split panes with | and - (more intuitive)
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# Reload config with prefix + r
bind r source-file ~/.tmux.conf \; display-message "Config reloaded"

# Status bar customization
set -g status-style 'bg=#282a36 fg=#f8f8f2'
set -g status-left '#[fg=#50fa7b,bold] #S '
set -g status-right '#[fg=#bd93f9] %Y-%m-%d %H:%M '
```

### Plugin Manager (tpm)

```bash
# Install tpm
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Add to ~/.tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'       # Sensible defaults
set -g @plugin 'tmux-plugins/tmux-resurrect'       # Save/restore sessions
set -g @plugin 'tmux-plugins/tmux-continuum'       # Auto-save sessions
set -g @plugin 'tmux-plugins/tmux-yank'            # System clipboard integration

# Auto-restore sessions on tmux start
set -g @continuum-restore 'on'

# Initialize tpm (keep this at the bottom of .tmux.conf)
run '~/.tmux/plugins/tpm/tpm'

# Install plugins: prefix + I (capital i)
# Update plugins:  prefix + U
```

### Copy Mode and Scrollback

```bash
# Enter copy mode
# Ctrl+b [

# Navigate with vi keys (hjkl, Ctrl+u/d for page up/down)
# Press Space to start selection, Enter to copy
# Ctrl+b ] to paste

# Search in copy mode
# Press / for forward search, ? for backward search
```

### Tmux vs Screen

| Feature | Tmux | Screen |
|---------|------|--------|
| **Pane splitting** | Native, flexible | Limited |
| **Scripting** | Extensive, modern | Basic |
| **Status bar** | Highly customizable | Basic |
| **Plugin system** | Yes (tpm) | No |
| **Unicode support** | Good | Limited |
| **Active development** | Yes | Minimal |
| **Default on systems** | Usually needs install | Often pre-installed |

---

## 2. Tabby

### Overview

Tabby (formerly Terminus) is a modern, cross-platform terminal emulator with a built-in SSH connection manager, SFTP integration, and a polished interface.

- **Website:** https://tabby.sh
- **Source:** https://github.com/Eugeny/tabby
- **License:** MIT
- **Platform:** Windows, macOS, Linux

### Key Features

- **SSH connection manager** — save hosts, keys, jump hosts, port forwarding
- **SFTP file transfer** — browse and transfer files alongside your SSH session
- **Serial terminal** — connect to serial devices (Arduino, ESP32, etc.)
- **Split panes** — horizontal and vertical splits within tabs
- **Profiles** — preconfigured shell environments (bash, zsh, PowerShell, WSL)
- **Themes and appearance** — customizable colors, fonts, acrylic/blur backgrounds
- **Plugin system** — extend functionality with community plugins
- **Encrypted vault** — store SSH passwords and keys securely

### Installation

```bash
# macOS (Homebrew)
brew install --cask tabby

# Windows (winget)
winget install Eugeny.Tabby

# Windows (Chocolatey)
choco install tabby

# Linux (Snap)
sudo snap install tabby

# Or download from https://tabby.sh/
```

### SSH Configuration

Tabby provides a GUI for managing SSH connections, but it also reads from `~/.ssh/config`:

```
# ~/.ssh/config (Tabby picks this up automatically)
Host myserver
    HostName 192.168.1.100
    User admin
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes

Host jumphost
    HostName bastion.example.com
    User ops

Host internal
    HostName 10.0.0.5
    User deploy
    ProxyJump jumphost
```

### Profiles and Configuration

Tabby stores its configuration in a YAML file accessible via Settings:
- **Shell profiles** — configure default shells, environment variables, working directories
- **Hotkeys** — customize all keyboard shortcuts
- **Appearance** — font family, size, line height, cursor style, tab bar position

---

## 3. Other Notable Terminals

### Alacritty

A GPU-accelerated, minimal terminal emulator focused on speed and simplicity.

- **Website:** https://alacritty.org
- **License:** Apache 2.0
- **Platform:** Windows, macOS, Linux, BSD
- **Config:** `~/.config/alacritty/alacritty.toml`

```bash
# Install
# macOS
brew install --cask alacritty
# Arch
sudo pacman -S alacritty
# Cargo (from source)
cargo install alacritty
```

Key traits: fastest terminal emulator available, no tabs or splits (use tmux), configuration via TOML file, Vi mode for scrollback.

### Kitty

A GPU-based terminal emulator that is fast, feature-rich, and scriptable.

- **Website:** https://sw.kovidgoyal.net/kitty/
- **License:** GPL-3.0
- **Platform:** macOS, Linux

```bash
# Install
curl -L https://sw.kovidgoyal.net/kitty/installer.sh | sh /dev/stdin
# macOS
brew install --cask kitty
```

Key traits: GPU rendering, built-in tabs and splits, image display protocol (show images in terminal), kitten framework for extensions, remote control via CLI.

### Warp

An AI-powered terminal with modern UX features.

- **Website:** https://www.warp.dev
- **License:** Proprietary (free tier available)
- **Platform:** macOS, Linux

Key traits: AI command search and suggestions, block-based output (select/copy command outputs individually), collaborative features, IDE-like text editing in the input area, built-in workflows.

### Windows Terminal

Microsoft's modern terminal for Windows, supporting multiple shell profiles.

- **License:** MIT
- **Platform:** Windows

```powershell
# Install (Windows)
winget install Microsoft.WindowsTerminal
```

Key traits: tabs for CMD, PowerShell, WSL, and Azure Cloud Shell; GPU-accelerated text rendering; JSON configuration; custom themes and backgrounds; built into Windows 11.

---

## 4. Comparison Table

| Feature | Tmux | Tabby | Alacritty | Kitty | Warp | Windows Terminal |
|---------|------|-------|-----------|-------|------|------------------|
| **Type** | Multiplexer | Emulator | Emulator | Emulator | Emulator | Emulator |
| **GPU Accel** | N/A | Yes | Yes | Yes | Yes | Yes |
| **SSH Manager** | No | Yes (built-in) | No | No | No | No |
| **Multiplexer** | Yes (core feature) | Split panes | No (use tmux) | Built-in splits | Built-in | Tabs only |
| **Plugins** | Yes (tpm) | Yes | No | Kittens | No | No |
| **Platform** | Linux/macOS | Win/Mac/Linux | Win/Mac/Linux/BSD | Mac/Linux | Mac/Linux | Windows |
| **Image Display** | No | No | No | Yes (protocol) | Yes | No |
| **AI Features** | No | No | No | No | Yes | No |
| **Config Format** | .tmux.conf | YAML (GUI) | TOML | .conf | GUI | JSON |
| **Price** | Free | Free | Free | Free | Free/Paid | Free |
| **Best For** | Remote sessions, persistence | SSH management, all-in-one | Speed purists | Power users, images | AI-assisted CLI | Windows multi-shell |

---

## See Also

- [Termux Setup](../mobile/termux-setup.md) — Full Linux terminal environment on Android
- [Editors & IDEs](editors-and-ides.md) — VS Code, code-server, and modern code editors
- [Remote Access](../networking/remote-access.md) — SSH configuration and remote machine access
- [SSH Tunneling](../networking/ssh-tunneling.md) — Port forwarding and tunnel management
