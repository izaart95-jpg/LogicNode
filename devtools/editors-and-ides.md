# Editors & IDEs — VS Code, code-server, Void & Modern Code Editors

A code editor is the most important tool in any developer's workflow. Modern editors go far beyond syntax highlighting, offering built-in debugging, AI assistance, remote development, and rich extension ecosystems. This guide covers the leading open-source and free editors for local and remote development.

---

## Table of Contents
1. [Visual Studio Code (VS Code)](#1-visual-studio-code-vs-code)
2. [code-server](#2-code-server)
3. [Void Editor](#3-void-editor)
4. [Comparison Table](#4-comparison-table)

---

## 1. Visual Studio Code (VS Code)

### Overview

VS Code is Microsoft's free, open-source code editor built on Electron. It has become the most popular editor worldwide due to its speed, extensibility, and deep ecosystem of extensions.

- **Website:** https://code.visualstudio.com
- **License:** MIT (source), proprietary (Microsoft build with telemetry)
- **Platform:** Windows, macOS, Linux

### Key Features

- **IntelliSense** — context-aware code completions, parameter hints, type info
- **Built-in debugging** — breakpoints, call stacks, variable inspection for Node.js, Python, C++, and more
- **Integrated Git** — staging, diffing, branching, and merge conflict resolution in the sidebar
- **Integrated terminal** — run shell commands without leaving the editor
- **Extensions marketplace** — over 40,000 extensions for languages, tools, and themes
- **Settings sync** — sync settings, keybindings, extensions, and snippets across machines via GitHub/Microsoft account
- **Profiles** — switch between different configurations for different workflows (e.g., Python vs. web dev)

### Remote Development

VS Code supports developing on remote machines as if they were local:

| Remote Target | Extension | Description |
|---------------|-----------|-------------|
| **SSH** | Remote - SSH | Edit files on any SSH-accessible machine |
| **Containers** | Dev Containers | Develop inside Docker containers with full toolchain |
| **WSL** | WSL | Seamless Linux development on Windows |
| **Tunnels** | Remote - Tunnels | Connect to any machine via secure tunnel (no SSH needed) |

```bash
# Connect to a remote host via SSH
# 1. Install "Remote - SSH" extension
# 2. Ctrl+Shift+P → "Remote-SSH: Connect to Host..."
# 3. Enter: user@hostname

# Or from the command line
code --remote ssh-remote+user@hostname /path/to/project
```

### Essential Extensions

| Extension | Purpose |
|-----------|---------|
| **Prettier** | Automatic code formatting (JS, TS, CSS, HTML, JSON) |
| **ESLint** | JavaScript/TypeScript linting |
| **GitLens** | Enhanced Git history, blame annotations, file history |
| **Docker** | Dockerfile/Compose support, container management |
| **Remote - SSH** | Edit files on remote machines |
| **Python** | IntelliSense, linting, debugging for Python |
| **Live Server** | Local development server with live reload |
| **Thunder Client** | Lightweight REST API client (alternative to Postman) |

### Keyboard Shortcuts Reference

| Action | Windows/Linux | macOS |
|--------|---------------|-------|
| Command Palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Quick Open (file) | `Ctrl+P` | `Cmd+P` |
| Toggle Terminal | `` Ctrl+` `` | `` Cmd+` `` |
| Go to Definition | `F12` | `F12` |
| Find in Files | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Multi-cursor | `Alt+Click` | `Opt+Click` |
| Rename Symbol | `F2` | `F2` |
| Toggle Sidebar | `Ctrl+B` | `Cmd+B` |
| Split Editor | `Ctrl+\` | `Cmd+\` |
| Format Document | `Shift+Alt+F` | `Shift+Opt+F` |

### Installation

```bash
# Debian/Ubuntu
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] \
  https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update && sudo apt install code

# Fedora/RHEL
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo dnf install code

# macOS (Homebrew)
brew install --cask visual-studio-code

# Snap (Ubuntu)
sudo snap install code --classic
```

---

## 2. code-server

### Overview

code-server runs VS Code in the browser, letting you develop on any device with a web browser — including iPads, Chromebooks, and thin clients. It is fully self-hosted.

- **Website:** https://github.com/coder/code-server
- **License:** MIT

### Installation

```bash
# One-line install script (Linux/macOS)
curl -fsSL https://code-server.dev/install.sh | sh

# Start code-server
code-server

# Docker
docker run -d --name code-server \
  -p 8080:8080 \
  -v "$HOME/.local:/home/coder/.local" \
  -v "$PWD:/home/coder/project" \
  -e PASSWORD="your-password" \
  codercom/code-server:latest

# Homebrew (macOS)
brew install code-server
brew services start code-server
```

### Configuration

The configuration file lives at `~/.config/code-server/config.yaml`:

```yaml
bind-addr: 0.0.0.0:8080
auth: password
password: your-secure-password
cert: false
```

### Reverse Proxy Setup

To expose code-server securely over HTTPS, place it behind a reverse proxy.

```nginx
# Nginx configuration
server {
    listen 443 ssl;
    server_name code.example.com;

    ssl_certificate     /etc/letsencrypt/live/code.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/code.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Accept-Encoding gzip;
    }
}
```

```
# Caddyfile (simpler alternative — auto HTTPS)
code.example.com {
    reverse_proxy 127.0.0.1:8080
}
```

### Use Cases

- Develop from an iPad or Chromebook with a full VS Code experience
- Access your development environment from any browser, anywhere
- Run a shared coding environment on a powerful remote server
- Standardize development environments across a team

---

## 3. Void Editor

### Overview

Void is an open-source AI code editor forked from VS Code. It integrates AI assistance directly into the editing experience while keeping the codebase fully open source.

- **Website:** https://github.com/voideditor/void
- **License:** MIT (fully open source)

### Key Features

- **Built-in AI features** — code completion, inline editing, chat sidebar
- **Local model support** — run AI models locally for offline and private development
- **Bring your own API keys** — connect to OpenAI, Anthropic, or any compatible API
- **VS Code compatible** — supports VS Code extensions, themes, and keybindings
- **Privacy-first** — no telemetry, no data collection, fully transparent codebase

### Void vs Cursor

| Aspect | Void | Cursor |
|--------|------|--------|
| **Open Source** | Yes (MIT) | No (proprietary) |
| **Base** | VS Code fork | VS Code fork |
| **AI Models** | BYO keys + local models | Built-in (proprietary backend) |
| **Pricing** | Free | Free tier + paid plans |
| **Telemetry** | None | Yes |
| **Local Models** | Full support | Limited |
| **Extension Support** | VS Code extensions | VS Code extensions |

### Installation

```bash
# Download from GitHub releases
# https://github.com/voideditor/void/releases

# Or build from source
git clone https://github.com/voideditor/void.git
cd void
npm install
npm run build
```

---

## 4. Comparison Table

| Feature | VS Code | code-server | Void | Neovim | JetBrains IDEs |
|---------|---------|-------------|------|--------|-----------------|
| **Open Source** | MIT (source) | MIT | MIT | Apache 2.0 | No |
| **AI Built-in** | Via extensions | Via extensions | Yes | Via plugins | Yes (AI Assistant) |
| **Remote Dev** | SSH, Containers, WSL, Tunnels | Browser-based | Same as VS Code | SSH + tmux | SSH, Gateway |
| **Extensions** | 40,000+ marketplace | VS Code extensions | VS Code extensions | Lua plugins | Plugin marketplace |
| **Performance** | Good (Electron) | Depends on server | Good (Electron) | Excellent (native) | Heavy (JVM) |
| **Price** | Free | Free | Free | Free | Free (Community) / Paid |
| **Platform** | Win/Mac/Linux | Any browser | Win/Mac/Linux | Win/Mac/Linux | Win/Mac/Linux |
| **Best For** | General development | Remote / browser dev | AI-assisted, privacy | Terminal power users | Enterprise, Java/Kotlin |

---

## See Also

- [Terminal Tools](terminal-tools.md) — Tmux, Tabby, and modern terminal emulators
- [Docker Essentials](docker-essentials.md) — Dev Containers and Dockerized development environments
- [Remote Access](../networking/remote-access.md) — SSH and remote machine access
- [Tunneling Tools](../networking/tunneling-tools.md) — Expose local dev servers remotely
