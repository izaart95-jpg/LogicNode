# Reverse Engineering MCP Server — Setup & Integration Guide

**Version:** 1.4  
**Scope:** Claude Code · Cline · 5ire · Cursor · All MCP-Compatible Clients  
**Prerequisite:** [Java Development Kit 21 (JDK 21)](https://adoptium.net/temurin/releases/?version=21) — ensure `JAVA_HOME` is set before proceeding.

---

> **Reading this guide for the first time?**
>
> Each server section is organized with experience level in mind:
>
> - **Beginners** — follow **Option A (Direct Download / Automated)** in each section. These paths use pre-built releases and installer scripts that handle the heavy lifting for you.
> - **Professionals** — **manual installation (Option B / Build From Source)** is strongly recommended. It gives you full control over the build, lets you pin exact dependency versions, and produces reproducible environments — especially important for CI/CD, air-gapped networks, and security-sensitive workflows.

---

## Overview

This guide provides authoritative setup instructions for integrating Reverse Engineering MCP (Model Context Protocol) servers with Claude and other MCP-compatible clients. All configurations follow the MCP uniform protocol — only the command, arguments, and environment variables differ between tools.

**Covered Servers**

| Server | Maintainer | Key Capability |
|---|---|---|
| [ReVa](#1-reva--reverse-engineering-assistant) | cyberkaida | Headless mode, HTTP transport, CI/CD support |
| [GhydraMCP](#2-ghydramcp-starsong-consulting) | starsong-consulting | HATEOAS REST API, multi-instance support |
| [GhidraMCP](#3-ghidramcp-lauriewired) | LaurieWired | Direct Ghidra-to-AI bridge, SSE transport |
| [GhidraMCP (fork)](#4-ghidramcp-bethington-fork) | bethington | Extended build tooling, PowerShell/Bash setup |
| [Binary Ninja MCP](#5-binary-ninja-mcp-fosdickio) | fosdickio | Binary Ninja integration, npm package, auto-setup |
| [Binary Ninja MCP (MCPPhalanx)](#6-binary-ninja-mcp-mcpphalanx) | MCPPhalanx | UI plugin + headless mode, SSE transport, uvx-based |
| [Binja Lattice MCP](#7-binja-lattice-mcp-invoke-re) | Invoke-RE | API-key auth, venv/uv/direct Python, remote support |
| [Radare2 MCP](#8-radare2-mcp-r2mcp) | radareorg | r2pm-native install, Docker support, multi-client |
| [mcp-server-gdb](#9-mcp-server-gdb-pansila) | pansila | Rust-based, stdio/SSE transport, Nix support |
| [mcp-gdb](#10-mcp-gdb-signal-slot) | signal-slot | npm-native, zero-config Claude Code integration |
| [LLDB MCP](#11-lldb-mcp) | LLVM | Built-in LLDB protocol server, netcat bridge |
| [CutterMCP](#12-cuttermcp-ap425q) | ap425q | Cutter plugin, Python bridge, env-var remote |
| [CutterMCP-plus](#13-cuttermcp-plus-restkhz) | restkhz | Streamable HTTP mode, bottom-panel remote config |
| [x64dbg_automate](#14-x64dbg_automate-dariushoule) | dariushoule | ZeroMQ transport, Python MCP client, remote debug |
| [x64dbgMCP](#15-x64dbgmcp-wasdubya) | Wasdubya | HTTP bridge plugin, Python bridge script |
| [IDA Pro MCP (mrexodia)](#16-ida-pro-mcp-mrexodia) | mrexodia | pip-installable, streamable HTTP, idalib headless mode |
| [mcp-server-ida (MxIris)](#17-mcp-server-ida-mxiris) | MxIris-Reverse-Engineering | uvx/pip, env-var remote host, PYTHONPATH patching |

---

## Reference: Claude Code MCP Template

All Claude Code commands in this guide follow the same template. Use the JSON `mcpServers` blocks with any other client — consult that client's documentation for config file placement.

```bash
claude mcp add <server-name> --scope user \
  -e ENV_VAR=value \
  -- <command> [args...]
```

**Flag Reference**

| Flag | Description |
|---|---|
| `--scope user` / `-s user` | Register for your user account; persists across projects |
| `-e KEY=VALUE` | Set an environment variable passed to the server process |
| `--transport http` | Use HTTP transport instead of stdio (required for some servers) |
| `--` | Separates `claude mcp add` flags from the server command and its arguments |

---

## 1. ReVa — Reverse Engineering Assistant

**Repository:** [cyberkaida/reverse-engineering-assistant](https://github.com/cyberkaida/reverse-engineering-assistant)

ReVa is an AI-powered reverse engineering assistant built around Ghidra. It ships its own MCP server binary (`mcp-reva`) installable via `uv`, exposes an HTTP MCP endpoint, and supports **headless mode** — making it well-suited for automation, CI/CD pipelines, and Docker workflows.

---

### 1.1 Installation

#### Option A — Direct Download (Recommended for Beginners)

1. Download the latest release from `https://github.com/cyberkaida/reverse-engineering-assistant/releases/latest`

2. Install the Ghidra extension:
   - Open Ghidra → **File** → **Install Extensions**
   - Click **+** and select the extension ZIP — do **not** extract it
   - Restart Ghidra when prompted

3. Activate the plugin in both locations:

   **Project Window:** File → Configure → Configure All Plugins → enable **ReVa Application Plugin**

   **Code Browser** (open a file or click the Dragon icon): File → Configure → Configure All Plugins → enable **ReVa Plugin** → File → **Save Tool**

> Saving the tool persists the setting and enables ReVa by default on subsequent launches.

---

#### Option B — Build From Source (Recommended for Professionals)

> **Pro note:** Building from source lets you audit the codebase, pin a specific commit, and integrate cleanly into internal toolchains. Pair with a `JAVA_HOME` pointing to a verified JDK 21 distribution.

**Requirements:** JDK 21, Gradle

```bash
git clone https://github.com/cyberkaida/reverse-engineering-assistant.git
cd reverse-engineering-assistant

export GHIDRA_INSTALL_DIR=/path/to/ghidra
gradle install
```

After the build completes, activate the plugin as described in Option A, Step 3.

---

### 1.2 MCP Client Configuration

#### Standard Setup — Install via `uv`

```bash
# Set your Ghidra installation directory
export GHIDRA_INSTALL_DIR=/path/to/ghidra

# Install the MCP server binary
uv tool install reverse-engineering-assistant

# Register with Claude Code
claude mcp add --scope user ReVa -- mcp-reva
```

**Claude Code one-liner:**
```bash
GHIDRA_INSTALL_DIR=/path/to/ghidra claude mcp add --scope user ReVa -- mcp-reva
```

**JSON configuration:**
```json
{
  "mcpServers": {
    "ReVa": {
      "command": "mcp-reva",
      "args": [],
      "env": {
        "GHIDRA_INSTALL_DIR": "/path/to/ghidra"
      }
    }
  }
}
```

> Replace `/path/to/ghidra` with your actual Ghidra installation directory. If `mcp-reva` is not on your `PATH`, use its full absolute path as the command value.

---

#### HTTP Transport (GUI Mode)

Use this when Ghidra is already running with ReVa loaded.

**Claude Code:**
```bash
claude mcp add --scope user --transport http ReVa -- http://localhost:8080/mcp/message
```

**JSON configuration:**
```json
{
  "mcpServers": {
    "ReVa": {
      "type": "http",
      "url": "http://localhost:8080/mcp/message"
    }
  }
}
```

---

#### Remote Access

> ⚠️ **Security Notice:** Binding to `0.0.0.0` exposes the MCP server on all network interfaces. Only enable on trusted, isolated networks or behind a firewall/VPN.

1. In the Ghidra Project Window: **Edit** → **Tool Options** → **ReVa Server Options**
   - Change **Server Host** from `127.0.0.1` to `0.0.0.0`
   - Optionally adjust **Server Port** (default: `8080`)
   - Click **OK**

2. Update the client configuration:

**Claude Code:**
```bash
claude mcp add --scope user --transport http reva http://TARGET_IP:8080/message
```

**JSON configuration:**
```json
{
  "mcpServers": {
    "ReVa": {
      "type": "http",
      "url": "http://TARGET_IP:8080/mcp/message"
    }
  }
}
```

---

#### Headless Mode (Automation / No GUI)

ReVa can run without the Ghidra GUI — ideal for Docker containers, CI/CD pipelines, and PyGhidra workflows.

```python
import pyghidra
pyghidra.start()

from reva.headless import RevaHeadlessLauncher

launcher = RevaHeadlessLauncher()
launcher.start()

if launcher.waitForServer(30000):
    print(f"Server ready on port {launcher.getPort()}")
    # Insert analysis code or agent logic here

launcher.stop()
```

---

### 1.3 Claude Code Marketplace Plugin

ReVa ships an official Claude Code marketplace plugin with pre-built skills for common reverse engineering workflows.

**Install:**
```bash
claude plugin marketplace add cyberkaida/reverse-engineering-assistant
```

**Available Skills**

| Skill | Description |
|---|---|
| Binary Triage | Quick initial assessment of an unknown binary |
| Deep Analysis | Thorough function-by-function reverse engineering |
| Cryptography Analysis | Identify and analyze cryptographic routines |
| CTF Guides | Guided workflows for CTF challenge solving |

**Quick start:**
```bash
claude -p "Import /bin/ls with ReVa and tell me how it works"
```

---

## 2. GhydraMCP (starsong-consulting)

**Repository:** [starsong-consulting/GhydraMCP](https://github.com/starsong-consulting/GhydraMCP)

GhydraMCP exposes a comprehensive HATEOAS REST API with support for multiple simultaneous Ghidra instances, automatic discovery, structs, data types, namespaces, cross-references, and memory access.

> **Note:** The bridge script for this server is `bridge_mcp_hydra.py` — not `bridge_mcp_ghidra.py`.

---

### 2.1 Installation

#### Option A — Direct Download (Recommended for Beginners)

Two release variants are available — always prefer the **Complete** release:

| Release | Contents | Recommendation |
|---|---|---|
| `GhydraMCP-Complete-<version>.zip` | Extension ZIP + `bridge_mcp_hydra.py` | **Preferred** |
| `GhydraMCP-<version>.zip` | Extension ZIP only | Download `bridge_mcp_hydra.py` separately |

1. Download the latest Complete release from `https://github.com/starsong-consulting/GhydraMCP/releases/latest`
2. Extract the archive — you will find the inner extension ZIP and `bridge_mcp_hydra.py`. Do **not** extract the inner ZIP.
3. Install the extension: Ghidra → **File** → **Install Extensions** → **+** → select the inner extension ZIP → restart
4. Enable the plugin: Code Browser → **File** → **Configure** → **Configure All** → enable **GhidraMCP**

---

#### Option B — Build From Source (Recommended for Professionals)

> **Pro note:** Maven's clean lifecycle ensures no stale artifacts. Use the `complete-only` profile to get a single reproducible artifact bundle for deployment.

**Requirements:** JDK 21, Maven

```bash
git clone https://github.com/starsong-consulting/GhydraMCP.git
cd GhydraMCP
```

| Command | Output |
|---|---|
| `mvn clean package` | Both ZIPs (default — recommended) |
| `mvn clean package -P plugin-only` | Plugin ZIP only |
| `mvn clean package -P complete-only` | Complete ZIP only |

Install the generated ZIP using Option A, Steps 3–4.

---

### 2.2 MCP Client Configuration

#### Claude Code

```bash
# Using uv (recommended)
claude mcp add ghydra --scope user \
  -e GHIDRA_HYDRA_HOST=localhost \
  -- uv run /ABSOLUTE_PATH_TO/bridge_mcp_hydra.py

# Using plain Python
claude mcp add ghydra --scope user \
  -e GHIDRA_HYDRA_HOST=localhost \
  -- python3 /ABSOLUTE_PATH_TO/bridge_mcp_hydra.py
```

#### JSON Configuration

**Using `uv` (recommended):**
```json
{
  "mcpServers": {
    "ghydra": {
      "command": "uv",
      "args": ["run", "/ABSOLUTE_PATH_TO/bridge_mcp_hydra.py"],
      "env": {
        "GHIDRA_HYDRA_HOST": "localhost"
      }
    }
  }
}
```

**Using plain Python:**
```json
{
  "mcpServers": {
    "ghydra": {
      "command": "python3",
      "args": ["/ABSOLUTE_PATH_TO/bridge_mcp_hydra.py"],
      "env": {
        "GHIDRA_HYDRA_HOST": "localhost"
      }
    }
  }
}
```

> **Path examples:**  
> Linux/macOS: `/home/username/GhydraMCP/bridge_mcp_hydra.py`  
> Windows: `C:\\Users\\username\\GhydraMCP\\bridge_mcp_hydra.py`

#### Cline (VS Code)

1. Click **MCP Servers** → **Configure** tab → **Configure MCP Servers** to open `cline_mcp_settings.json`
2. Add the JSON block above, appending `"disabled": false` to each server entry

#### 5ire

Navigate to **Tools** → **New** and fill in:

| Field | Value |
|---|---|
| Tool Key | `ghydra` |
| Name | `GhydraMCP` |
| Command | `uv run /ABSOLUTE_PATH_TO/bridge_mcp_hydra.py` |

---

### 2.3 Remote Access

> ⚠️ **Security Notice:** The following patches remove SSRF protection. Apply only on isolated or trusted networks.

#### Patch `bridge_mcp_hydra.py`

**1. Allow all origins in `validate_origin`:**

```python
# Replace the existing validate_origin function with:
def validate_origin(headers: dict) -> bool:
    return True
```

**2. Set a permissive default for `ALLOWED_ORIGINS`:**

```python
# Before
ALLOWED_ORIGINS = os.environ.get(
    "GHIDRA_ALLOWED_ORIGINS", "http://localhost").split(",")

# After
ALLOWED_ORIGINS = os.environ.get(
    "GHIDRA_ALLOWED_ORIGINS", "*").split(",")
```

#### Connect to the Remote Host

**JSON configuration:**
```json
{
  "mcpServers": {
    "ghydra": {
      "command": "uv",
      "args": ["run", "/ABSOLUTE_PATH_TO/bridge_mcp_hydra.py"],
      "env": {
        "GHIDRA_HYDRA_HOST": "TARGET_IP"
      }
    }
  }
}
```

---

## 3. GhidraMCP (LaurieWired)

**Repository:** [LaurieWired/GhidraMCP](https://github.com/LaurieWired/GhidraMCP)  
**Tested against:** GhidraMCP v1.4

GhidraMCP bridges the Ghidra reverse engineering framework with MCP clients, enabling AI assistants to interact directly with Ghidra projects.

---

### 3.1 Installation

#### Option A — Direct Download (Recommended for Beginners)

1. Download the latest release from `https://github.com/LaurieWired/GhidraMCP/releases/latest`
2. Extract the archive to obtain the inner extension ZIP and `bridge_mcp_ghidra.py`
3. Install the extension: Ghidra → **File** → **Install Extensions** → **+** → select the inner ZIP → restart
4. Enable the plugin: Code Browser → **File** → **Configure** → **Load All Plugins** → enable **GhidraMCP**

---

#### Option B — Build From Source (Recommended for Professionals)

> **Pro note:** Copying JARs from your own Ghidra installation ensures version compatibility. Pin the commit you build from and store the resulting ZIP in your artifact registry for reproducibility.

**Requirements:** JDK 21, Maven

1. Clone the repository:
   ```bash
   git clone https://github.com/LaurieWired/GhidraMCP.git
   cd GhidraMCP
   ```

2. Copy the required JARs from your Ghidra installation into `lib/`:
   ```
   Ghidra/Features/Base/lib/Base.jar
   Ghidra/Features/Decompiler/lib/Decompiler.jar
   Ghidra/Framework/Docking/lib/Docking.jar
   Ghidra/Framework/Generic/lib/Generic.jar
   Ghidra/Framework/Project/lib/Project.jar
   Ghidra/Framework/SoftwareModeling/lib/SoftwareModeling.jar
   Ghidra/Framework/Utility/lib/Utility.jar
   Ghidra/Framework/Gui/lib/Gui.jar
   ```

3. Build:
   ```bash
   mvn clean package assembly:single
   ```

4. Install the generated ZIP using Option A, Steps 3–4.

---

### 3.2 MCP Client Configuration

#### Claude Code

```bash
claude mcp add ghidra --scope user \
  -- python3 /ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py \
  --ghidra-server http://127.0.0.1:8080/
```

#### JSON Configuration

```json
{
  "mcpServers": {
    "ghidra": {
      "command": "python3",
      "args": [
        "/ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py",
        "--ghidra-server",
        "http://127.0.0.1:8080/"
      ]
    }
  }
}
```

> Use `python` instead of `python3` on Windows.

#### Cline

Cline requires the MCP bridge to be started manually before connecting.

1. Start the bridge in SSE mode:
   ```bash
   python3 bridge_mcp_ghidra.py \
     --transport sse \
     --mcp-host 127.0.0.1 \
     --mcp-port 8081 \
     --ghidra-server http://127.0.0.1:8080/
   ```

2. In Cline: **MCP Servers** → **Remote Servers**
   - **Server Name:** `GhidraMCP`
   - **Server URL:** `http://127.0.0.1:8081/sse`

#### 5ire

Navigate to **Tools** → **New** and fill in:

| Field | Value |
|---|---|
| Tool Key | `ghidra` |
| Name | `GhidraMCP` |
| Command | `python /ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py` |

---

### 3.3 Remote Ghidra Targets

**JSON configuration:**
```json
{
  "mcpServers": {
    "ghidra": {
      "command": "python3",
      "args": [
        "/ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py",
        "--ghidra-server",
        "http://TARGET_IP:8080/"
      ]
    }
  }
}
```

---

## 4. GhidraMCP (bethington fork)

**Repository:** [bethington/ghidra-mcp](https://github.com/bethington/ghidra-mcp)

A fork of GhidraMCP with expanded build tooling — including PowerShell and Bash setup scripts — and a different MCP configuration shape (`"type": "stdio"` with an `env` block instead of CLI arguments).

---

### 4.1 Installation

#### Option A — Direct Download (Recommended for Beginners)

1. Download the latest release from `https://github.com/bethington/ghidra-mcp/releases/latest`

   The release provides two files:
   - The extension ZIP — this **is** the extension; do **not** extract it
   - `bridge_mcp_ghidra.py`

2. Install: Ghidra → **File** → **Install Extensions** → **+** → select the extension ZIP → restart
3. Enable: Code Browser → **File** → **Configure** → **Load All Plugins** → enable **GhidraMCP**

---

#### Option B — Build From Source (Recommended for Professionals)

##### Windows (PowerShell)

```powershell
git clone https://github.com/bethington/ghidra-mcp.git
cd ghidra-mcp

# Preflight check (recommended)
.\ghidra-mcp-setup.ps1 -Preflight -GhidraPath "C:\ghidra_12.0.3_PUBLIC"

# Build and deploy
.\ghidra-mcp-setup.ps1 -Deploy -GhidraPath "C:\ghidra_12.0.3_PUBLIC"
```

| Flag | Description |
|---|---|
| `-Deploy` | Standard end-to-end build and deploy (recommended) |
| `-SetupDeps` | Install Maven and Ghidra JAR dependencies only |
| `-Preflight` | Validate prerequisites without making changes |
| `-NoAutoPrereqs` | Skip automatic prerequisites (manual/strict mode) |
| `-BuildOnly` | Build only; skip deployment |
| `-Help` | Display full help |

---

##### Linux (Ubuntu/Debian)

**Requirements:** JDK 21, Maven, Python 3, pip

```bash
git clone https://github.com/bethington/ghidra-mcp.git
cd ghidra-mcp

sudo apt update && sudo apt install -y \
  openjdk-21-jdk maven python3 python3-pip curl jq unzip

./ghidra-mcp-setup.sh --preflight --ghidra-path ~/ghidra_12.0.3_PUBLIC
./ghidra-mcp-setup.sh --deploy --ghidra-path ~/ghidra_12.0.3_PUBLIC
```

**Linux artifact paths:**

| Artifact | Path |
|---|---|
| Extension | `$HOME/.config/ghidra/ghidra_<version>_PUBLIC/Extensions/GhidraMCP/` |
| Configuration | `$HOME/.config/ghidra/ghidra_<version>_PUBLIC/` |

**Helper scripts:**

| Script | Description |
|---|---|
| `functions-extract.sh` | Extracts functions via the Ghidra REST API using `curl` and `jq` |
| `functions-process.sh` | Parallel function processing with the Claude CLI |

---

##### macOS (Homebrew)

**Requirements:** JDK 21, Maven, Python 3, Ghidra (all via Homebrew)

```bash
brew install openjdk@21 maven python ghidra

git clone https://github.com/bethington/ghidra-mcp.git
cd ghidra-mcp

./ghidra-mcp-setup.sh --setup-deps \
  --ghidra-path /opt/homebrew/opt/ghidra/libexec \
  --ghidra-version 12.0.4

./ghidra-mcp-setup.sh --deploy \
  --ghidra-path /opt/homebrew/opt/ghidra/libexec \
  --ghidra-version 12.0.4
```

> `--ghidra-version` is **required** on the Homebrew path because the install directory contains no version string.

Extension installs to: `~/Library/ghidra/ghidra_12.0.4_PUBLIC/Extensions/GhidraMCP/`

Launch Ghidra and start the server: **Tools** → **GhidraMCP** → **Start MCP Server**

---

### 4.2 MCP Client Configuration

> This fork uses `"type": "stdio"` and an `env` block — not `--ghidra-server` CLI arguments.

#### Claude Code

```bash
claude mcp add ghidra --scope user \
  -e GHIDRA_SERVER=http://127.0.0.1:8089 \
  -- python3 /ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py
```

> Omitting `-e GHIDRA_SERVER=...` falls back to `localhost:8089`.

#### JSON Configuration

**Standard:**
```json
{
  "mcpServers": {
    "ghidra": {
      "type": "stdio",
      "command": "python3",
      "args": ["/ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py"],
      "env": {}
    }
  }
}
```

**Using `uv`:**
```json
{
  "mcpServers": {
    "ghidra": {
      "command": "uv",
      "args": ["run", "--script", "/ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py"]
    }
  }
}
```

#### 5ire

Navigate to **Tools** → **New** and fill in:

| Field | Value |
|---|---|
| Tool Key | `ghidra` |
| Name | `GhidraMCP` |
| Command | `python /ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py` |

---

### 4.3 Remote Access

#### Step 1 — Disable UDS Transport in Ghidra

Disable UDS transport in **both** the Project Window and the Code Browser:

- **Edit** → **Tool Options** → **GhidraMCP** → disable UDS transport
- Repeat in the Code Browser tool options

> If UDS transport is enabled in either location, remote connections will fail.

#### Step 2 - Make port proxy
```
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8089 connectaddress=127.0.0.1 connectport=8089
```
#### Step 3 — Patch `bridge_mcp_ghidra.py`

**Allow all hosts in `validate_server_url`:**

```python
# Replace the existing function with:
def validate_server_url(url: str) -> bool:
    return True
```

**Remove the refusal branch from the TCP fallback (first occurrence):**

```python
# Remove these lines:
if not validate_server_url(tcp_url):
    return json.dumps(
        {
            "error": f"Refusing to connect to non-local URL: {tcp_url}. Only 127.0.0.1, localhost, and ::1 are allowed."
        }
    )
```

**Remove the warning from the auto-connect path (second occurrence):**

```python
# Remove these lines:
if not validate_server_url(tcp_url):
    logger.warning(f"Refusing to auto-connect to non-local URL: {tcp_url}")
    return
```

#### Step 4 — Point to the Remote Host

**JSON configuration:**
```json
{
  "mcpServers": {
    "ghidra": {
      "type": "stdio",
      "command": "python3",
      "args": ["/ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py"],
      "env": {
        "GHIDRA_MCP_URL": "http://TARGET_IP:8089"
      }
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add ghidra --scope user \
  -e GHIDRA_MCP_URL=http://TARGET_IP:8089 \
  -- python3 /ABSOLUTE_PATH_TO/bridge_mcp_ghidra.py
```

> Replace `TARGET_IP` with the IP address or hostname of the machine running Ghidra. Ensure port `8089` is reachable through any intervening firewalls.

---

## 5. Binary Ninja MCP (fosdickio)

**Repository:** [fosdickio/binary_ninja_mcp](https://github.com/fosdickio/binary_ninja_mcp)

Binary Ninja MCP bridges the Binary Ninja reverse engineering platform with MCP clients, enabling AI assistants to interact directly with Binary Ninja projects. It ships with auto-setup support for the most common MCP clients and an official npm package for easy configuration.

---

### 5.1 Prerequisites

- [Binary Ninja](https://binary.ninja/)
- Python 3.12+
- An MCP client (see supported clients below)

> **Install your MCP client before installing Binary Ninja MCP.** The extension auto-configures supported clients on installation. If you install the extension first, reinstall it after adding the client.

**Auto-setup is supported for:**

| # | Client |
|---|--------|
| 1 | Cline (recommended) |
| 2 | Roo Code |
| 3 | Claude Desktop (recommended) |
| 4 | Cursor |
| 5 | Windsurf |
| 6 | Claude Code |
| 7 | LM Studio |

---

### 5.2 Installation

#### Option A — Binary Ninja Plugin Manager (Recommended for Beginners)

Open Binary Ninja and navigate to **Plugins → Manage Plugins**. Search for `binary_ninja_mcp` and click **Install**.

> The Plugin Manager version may lag behind the latest release. For the most current version, use the manual install method below.

---

#### Option B — Manual Install (Recommended for Professionals)

> **Pro note:** Cloning directly into the plugins folder gives you a live working copy — `git pull` is all you need to update, and you can track or cherry-pick specific commits for stability.

Clone or download this repository into your [Binary Ninja plugins folder](https://docs.binary.ninja/guide/plugins.html):

```bash
git clone https://github.com/fosdickio/binary_ninja_mcp.git \
  /path/to/BinaryNinja/plugins/binary_ninja_mcp
```

Both installation methods trigger MCP client auto-setup if a supported client is already present.

---

### 5.3 MCP Client Configuration

#### Using npm (Recommended)

The official npm package is the preferred setup method:

```bash
npx -y binary-ninja-mcp
```

**JSON configuration:**
```json
{
  "mcpServers": {
    "binary-ninja-mcp": {
      "command": "npx",
      "args": ["-y", "binary-ninja-mcp", "--host", "localhost", "--port", "9009"]
    }
  }
}
```

**If installed globally (`npm install -g binary-ninja-mcp`):**
```json
{
  "mcpServers": {
    "binary-ninja-mcp": {
      "command": "binary-ninja-mcp",
      "args": ["--host", "localhost", "--port", "9009"]
    }
  }
}
```

---

#### Using the Python Bridge (Legacy)

For clients not covered by the npm package:

```json
{
  "mcpServers": {
    "binary_ninja_mcp": {
      "command": "/ABSOLUTE/PATH/TO/Binary Ninja/plugins/repositories/community/plugins/fosdickio_binary_ninja_mcp/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/Binary Ninja/plugins/repositories/community/plugins/fosdickio_binary_ninja_mcp/bridge/binja_mcp_bridge.py"
      ]
    }
  }
}
```

> Replace `/ABSOLUTE/PATH/TO` with your actual Binary Ninja installation path. The virtual environment's Python interpreter must be used to ensure all dependencies are available.

---

#### Manual MCP Client Management

If auto-setup did not run (e.g., extension installed before the client), use the installer script directly:

```bash
# Auto-setup all supported MCP clients
python scripts/mcp_client_installer.py --install

# Remove all entries and reset auto-setup state
python scripts/mcp_client_installer.py --uninstall

# Print a generic JSON config snippet
python scripts/mcp_client_installer.py --config
```

---

### 5.4 Usage

1. Open Binary Ninja and load a binary
2. Click the **MCP** button in the bottom-left status bar
3. Connect from your MCP client and start issuing analysis tasks

---

### 5.5 Remote Access

#### Option A — Settings UI (Recommended)

1. Open **Edit → Settings** and search for **MCP Server**
2. Enable **Expose to Network**
3. Optionally change the port or rename the tool prefix
4. Restart the server: **Plugins → MCP Server → Stop Server**, then **Plugins → MCP Server → Start Server**

---

#### Option B — Manual Config Edit

Locate `plugin/__init__.py` inside the plugin installation directory and edit the defaults directly:

```python
$cpp = "__init__.py"
(Get-Content $cpp) -replace 'plugin\.config\.server\.host = "0\.0\.0\.0" if expose_to_network else "localhost"', 'plugin.config.server.host = "0.0.0.0"' | Set-Content $cpp
          
```

Then update your client configuration to point at the remote host:

```json
{
  "mcpServers": {
    "binary-ninja-mcp": {
      "command": "npx",
      "args": ["-y", "binary-ninja-mcp", "--host", "TARGET_IP", "--port", "9009"]
    }
  }
}
```

> ⚠️ **Security Notice:** Binding to `0.0.0.0` exposes the MCP server on all network interfaces. Only do this on trusted, isolated networks or behind a firewall/VPN.

---

### 5.6 Claude Code

```bash
claude mcp add binary-ninja --scope user \
  -- npx -y binary-ninja-mcp --host localhost --port 9009
```

---

## 6. Binary Ninja MCP (MCPPhalanx)

**Repository:** [MCPPhalanx/binaryninja-mcp](https://github.com/MCPPhalanx/binaryninja-mcp)

A `uvx`-native Binary Ninja MCP server with two operating modes: a UI plugin that runs inside Binary Ninja and a fully headless mode for scripted or multi-file workflows. All opened files are exposed as separate MCP resources. The server natively supports both SSE and stdio relay transports, making it compatible with a wide range of MCP clients.

---

### 6.1 Installation

#### Mode 1 — Binary Ninja UI Plugin (Recommended for Beginners)

1. Open Binary Ninja and navigate to **Plugins → Manage Plugins**
2. Search for **MCPPhalanx** and click the **MCP** plugin entry
3. Click **Install**

The MCP server starts automatically when the first file is loaded.

**Configurable options (Edit → Settings → MCP Server):**

| Setting | Description | Default |
|---|---|---|
| Auto Start | Start server automatically on file load | Enabled |
| Server port number | Port the server listens on | `7000` |

---

#### Mode 2 — Headless Mode (Recommended for Professionals)

> **Pro note:** Headless mode is ideal for batch analysis pipelines. Combine it with `--port` to run multiple server instances in parallel on different ports, each targeting a different binary.

Run the server without the Binary Ninja GUI, targeting one or more binary files or BNDB databases.

```bash
# One-time setup: install the Binary Ninja API for headless use
uvx binaryninja-mcp install-api

# Start the server with one or more files
uvx binaryninja-mcp server <filename> [filename]...
```

- `<filename>` accepts any binary file or `.bndb` database — all opened files are exposed as separate MCP resources, identical to UI mode
- Default port: **7000**
- Use `--port <PORT>` to specify a different port:
  ```bash
  uvx binaryninja-mcp server --port 12345 <filename>
  ```

---

### 6.2 MCP Client Configuration

#### stdio Relay (Claude Code / Claude Desktop / most stdio clients)

The built-in relay client bridges stdio transport to the running server. This is the recommended method for Claude Code and Claude Desktop.

**Claude Code:**
```bash
claude mcp add binaryninja --scope user \
  -- uvx binaryninja-mcp client
```

**JSON configuration:**
```json
{
  "mcpServers": {
    "binaryninja": {
      "command": "uvx",
      "args": ["binaryninja-mcp", "client"]
    }
  }
}
```

> If the server is running on a non-default port, append `--port <PORT>` to both the server command and the client args. For example:
> ```json
> "args": ["binaryninja-mcp", "client", "--port", "12345"]
> ```

---

#### SSE Transport (Cherry Studio and SSE-enabled clients)

SSE-enabled clients can connect directly to the running server — no relay needed.

| Client | Connection method | Value |
|---|---|---|
| Cherry Studio (recommended) | SSE endpoint URL | `http://localhost:7000/sse` |
| Cherry Studio (alternative) | stdio client — Command: `uvx`, Arguments: `binaryninja-mcp` then `client` | — |
| Any SSE-enabled client | SSE endpoint URL | `http://localhost:7000/sse` |

---

#### Development Setup

For MCP clients with stdio transport (such as Claude Desktop) when working from a local development checkout:

```json
{
  "mcpServers": {
    "binaryninja": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/path/to/binaryninja-mcp",
        "run",
        "binaryninja-mcp",
        "client"
      ]
    }
  }
}
```

> Replace `C:/path/to/binaryninja-mcp` with the absolute path to your local clone of the repository. Use forward slashes on all platforms.

---

### 6.3 Remote Access

#### Step 1 — Expose the Server on the Remote Machine

By default the server only listens on `localhost`. To accept remote connections, change the bind address.

**Option A — Settings UI (UI plugin only):**

1. Open Binary Ninja → **Edit → Settings → MCP Server**
2. Change **Listen Host** from `localhost` to `0.0.0.0` (or a specific network interface address)
3. Restart the server: **Plugins → MCP Server → Stop Server**, then **Start Server**

**Option B — Headless mode:**

Pass the `--host` flag when starting the server:

```bash
uvx binaryninja-mcp server --host 0.0.0.0 --port 7000 <filename>
```

**Option C — SSH tunnel / port proxy:**

Use SSH tunneling or OS-level port forwarding (e.g., `netsh interface portproxy` on Windows) to relay traffic without exposing the server on a network interface directly.

> ⚠️ **Security Notice:** Binding to `0.0.0.0` exposes the server to your entire network. Recommended mitigations: use a VPN, set up SSH tunneling, or add firewall rules to restrict access to trusted hosts only.

---

#### Step 2 — Connect from the Local Machine

Point the client relay at the remote host using `--host` and `--port`:

**JSON configuration:**
```json
{
  "mcpServers": {
    "binaryninja": {
      "command": "uvx",
      "args": ["binaryninja-mcp", "client", "--host", "TARGET_IP", "--port", "7000"]
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add binaryninja --scope user \
  -- uvx binaryninja-mcp client --host TARGET_IP --port 7000
```

> Replace `TARGET_IP` with the IP address or hostname of the machine running Binary Ninja. Ensure the chosen port is reachable through any intervening firewalls.

---

### 6.4 Building From Source

```bash
git clone https://github.com/MCPPhalanx/binaryninja-mcp.git
cd binaryninja-mcp
uv build
```

---

## 7. Binja Lattice MCP (Invoke-RE)

**Repository:** [Invoke-RE/binja-lattice-mcp](https://github.com/Invoke-RE/binja-lattice-mcp)

Binja Lattice MCP connects Binary Ninja to MCP clients via an authenticated Lattice Protocol server. The plugin runs inside Binary Ninja and issues an API key on startup; all MCP client connections authenticate using that key via the `BNJLAT` environment variable.

> ⚠️ **Known issue (as of this writing):** The upstream `config.ini` parser reads string values including their surrounding quotes, which causes silent failures when values other than the default are set. A fix has been reported to the repository owner. Until it is merged, follow the workarounds documented in the Remote Access section below.

---

### 7.1 Installation

#### Option A — Windows Automated Installer (Recommended for Beginners)

Run the PowerShell installer for a one-shot setup:

```powershell
.\scripts\install_windows.ps1
```

This will:
- Install the plugin to `%APPDATA%\Binary Ninja\plugins\`
- Create a Python virtual environment (`.venv`)
- Install all dependencies
- Output a ready-to-use MCP configuration

---

#### Option B — Manual Installation (Recommended for Professionals)

> **Pro note:** Manual installation gives you full control over the virtual environment location, Python version, and dependency pinning — important for air-gapped or regulated environments.

**Step 1 — Clone the repository:**

```bash
git clone https://github.com/Invoke-RE/binja-lattice-mcp.git
cd binja-lattice-mcp
```

**Step 2 — Copy the plugin to your Binary Ninja plugins directory:**

| Platform | Plugins directory |
|---|---|
| Linux | `~/.binaryninja/plugins/` |
| macOS | `~/Library/Application Support/Binary Ninja/plugins/` |
| Windows | `%APPDATA%\Binary Ninja\plugins\` |

```bash
# Linux / macOS example
cp -r plugin ~/.binaryninja/plugins/binja-lattice-mcp
```

**Step 3 — Set up a virtual environment and install dependencies:**

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

### 7.2 Starting the Server

1. Open Binary Ninja and load a binary file
2. Go to **Plugins → Start Lattice Protocol Server**
3. The server starts and displays a randomly generated API key in the log console
4. Set that API key as the `BNJLAT` environment variable in your MCP client configuration

---

### 7.3 MCP Client Configuration

Three setup methods are available. Choose the one that matches your workflow.

---

#### Method 1 — Virtual Environment Python (Recommended for Most Users)

Uses the isolated `.venv` created during installation — the safest and most portable approach.

**JSON configuration (Linux / macOS):**
```json
{
  "mcpServers": {
    "binja-lattice-mcp": {
      "command": "/path/to/binja-lattice-mcp/.venv/bin/python",
      "args": ["/path/to/binja-lattice-mcp/mcp_server.py"],
      "env": {
        "BNJLAT": "your_api_key_here"
      }
    }
  }
}
```

**JSON configuration (Windows — use backslashes):**
```json
{
  "mcpServers": {
    "binja-lattice-mcp": {
      "command": "C:\\path\\to\\binja-lattice-mcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\binja-lattice-mcp\\mcp_server.py"],
      "env": {
        "BNJLAT": "your_api_key_here"
      }
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add binja-lattice --scope user \
  -e BNJLAT=your_api_key_here \
  -- /path/to/binja-lattice-mcp/.venv/bin/python \
     /path/to/binja-lattice-mcp/mcp_server.py
```

---

#### Method 2 — System Python (No Virtual Environment)

Install dependencies into your system Python and point directly at the script. Simpler, but may conflict with other packages.

```bash
pip install -r requirements.txt
```

**JSON configuration:**
```json
{
  "mcpServers": {
    "binja-lattice-mcp": {
      "command": "python3",
      "args": ["/path/to/binja-lattice-mcp/mcp_server.py"],
      "env": {
        "BNJLAT": "your_api_key_here"
      }
    }
  }
}
```

> Use `python` instead of `python3` on Windows if your installation does not alias the command.

---

#### Method 3 — uv (Recommended for Professionals)

`uv` manages the virtual environment and dependencies automatically. No manual `venv` or `pip install` required.

```bash
# Install uv if not already present
pip install uv

# Run the server directly — uv handles the environment
uv run --with-requirements requirements.txt mcp_server.py
```

**JSON configuration:**
```json
{
  "mcpServers": {
    "binja-lattice-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--with-requirements", "/path/to/binja-lattice-mcp/requirements.txt",
        "/path/to/binja-lattice-mcp/mcp_server.py"
      ],
      "env": {
        "BNJLAT": "your_api_key_here"
      }
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add binja-lattice --scope user \
  -e BNJLAT=your_api_key_here \
  -- uv run \
     --with-requirements /path/to/binja-lattice-mcp/requirements.txt \
     /path/to/binja-lattice-mcp/mcp_server.py
```

---

### 7.4 Remote Access

Connecting to a Binary Ninja instance on a different machine requires changes to both `mcp_server.py` (the MCP bridge) and `plugin/config.ini` (the Binary Ninja plugin).

---

#### Step 1 — Patch `mcp_server.py`

The default `mcp_server.py` only connects to `127.0.0.1`. Replace the initialization block to accept a target host and port via environment variables or CLI arguments.

**Before:**
```python
# Initialize and run the server
api_key = os.getenv("BNJLAT")
if not api_key:
    raise ValueError("BNJLAT environment variable not set")
global lattice_client
lattice_client = Lattice()
print(f"Authenticating with {api_key}")
lattice_client.authenticate("mcp-user", api_key)
mcp.run(transport='stdio')
```

**After:**
```python
import argparse

# Initialize and run the server
api_key = os.getenv("BNJLAT")
if not api_key:
    raise ValueError("BNJLAT environment variable not set")

# Support target IP via env var or CLI arg
parser = argparse.ArgumentParser()
parser.add_argument("--target-ip", default=None, help="IP of machine running Binary Ninja")
parser.add_argument("--target-port", type=int, default=None, help="Port of Lattice server")
args, _ = parser.parse_known_args()

target_host = args.target_ip or os.getenv("BNJLAT_HOST", "127.0.0.1")
target_port = args.target_port or int(os.getenv("BNJLAT_PORT", "9000"))

global lattice_client
lattice_client = Lattice(host=target_host, port=target_port)
print(f"Connecting to Lattice at {target_host}:{target_port}")
lattice_client.authenticate("mcp-user", api_key)
mcp.run(transport='stdio')
```

---

#### Step 2 — Configure `plugin/config.ini` on the Binary Ninja machine

> ⚠️ **Known bug — quote stripping not implemented (fix pending):** The upstream config parser reads values including any surrounding quotes. This means `ip_address = "0.0.0.0"` is read as the literal string `"0.0.0.0"` (with quotes), which fails to parse as an IP address and silently falls back to `127.0.0.1`. The same bug affects `api_key`.
>
> **Workaround: omit all quotes in `config.ini` until the upstream fix is merged.**

Edit `plugin/config.ini` on the machine running Binary Ninja:

```ini
[lattice]
# Bind on all interfaces so remote clients can connect
ip_address = 0.0.0.0

# Port the Lattice plugin listens on
port = 9000

# SSL — leave disabled unless you have a certificate configured
use_ssl = False

# Optional: set a permanent API key instead of using the randomly generated one
api_key = use_a_strong_api_key_here
```

**Rules for values in this file (until the bug is fixed):**
- Do **not** wrap values in quotes — `ip_address = 0.0.0.0` not `ip_address = "0.0.0.0"`
- The same applies to `api_key` — if your key contains special characters, either avoid them or apply the escaped variant: `api_key = \"my_key_here\"` (escaping with backslash-quote works as an alternative)
- `ip_address = "127.0.0.1"` happens to work because the parse failure falls back to `127.0.0.1` — this is coincidental, not correct behavior

---

#### Step 3 — Point the MCP client at the remote host

**Via environment variables (simplest):**
```json
{
  "mcpServers": {
    "binja-lattice-mcp": {
      "command": "/path/to/binja-lattice-mcp/.venv/bin/python",
      "args": ["/path/to/binja-lattice-mcp/mcp_server.py"],
      "env": {
        "BNJLAT": "your_api_key_here",
        "BNJLAT_HOST": "192.168.1.50",
        "BNJLAT_PORT": "9000"
      }
    }
  }
}
```

**Via CLI arguments:**
```json
{
  "mcpServers": {
    "binja-lattice-mcp": {
      "command": "/path/to/binja-lattice-mcp/.venv/bin/python",
      "args": [
        "/path/to/binja-lattice-mcp/mcp_server.py",
        "--target-ip", "192.168.1.50",
        "--target-port", "9000"
      ],
      "env": {
        "BNJLAT": "your_api_key_here"
      }
    }
  }
}
```

> Replace `192.168.1.50` with the actual IP or hostname of the Binary Ninja machine. Ensure port `9000` (or your chosen port) is open through any intervening firewalls.

---

## 8. Radare2 MCP (r2mcp)

**Repository:** [radareorg/radare2](https://github.com/radareorg/radare2) · Plugin: `r2mcp` via r2pm  
**GUI:** [iaito](https://github.com/radareorg/iaito) · **Web UI:** [r2.revengi.in](https://r2.revengi.in)

r2mcp is the official MCP server plugin for [radare2](https://rada.re/n/), the open-source reverse engineering framework. It is distributed through radare2's own package manager (`r2pm`) and runs as a process managed by your MCP client — the `r2mcp` binary is not meant to be launched directly from a shell.

> **Tip:** Useful companion plugins for deeper analysis: `r2ghidra`, `r2frida`, `r2reNEF`, `r2dec`, `r2yara`. GUI users can use **iaito**; a web-based interface is available at [r2.revengi.in](https://r2.revengi.in).

---

### 8.1 Installation

#### Option A — Package Install (Recommended for Beginners)

Install a pre-built radare2 release package for your system. Example for ARM64 Debian/Ubuntu:

```bash
# Download the latest release (adjust URL/filename for your platform and version)
wget https://github.com/radareorg/radare2/releases/download/6.1.4/radare2_6.1.4_arm64.deb

# Install
sudo apt install ./radare2_6.1.4_arm64.deb
```

For other platforms, find the appropriate package on the [radare2 releases page](https://github.com/radareorg/radare2/releases/latest) and install it with your system's package manager.

---

#### Option B — Build From Source (Recommended for Professionals)

> **Pro note:** Building from source gives you full control over compile-time options and lets you pin an exact commit. Radare2 uses `meson`/`ninja` on all platforms.

```bash
git clone https://github.com/radareorg/radare2.git
cd radare2
./sys/install.sh   # Linux/macOS
```

---

#### Step 2 — Install r2mcp via r2pm

After radare2 is installed, update r2pm and install the plugin:

```bash
# Update r2pm package index
r2pm -U

# Install the r2mcp plugin
r2pm -ci r2mcp
```

The `r2mcp` binary is placed in r2pm's bindir inside your home directory. It must be launched by your MCP client — not run directly from the shell.

---

#### Step 3 — (Optional) Install Codex Plugin

```bash
make codex-plugin-install
```

This creates a personal marketplace in your home directory and copies the files from `dist/codex-plugin`.

---

### 8.2 MCP Client Configuration

#### Claude Code

```bash
claude mcp add --scope user radare2 -- r2pm -r r2mcp
```

#### JSON Configuration

```json
{
  "mcpServers": {
    "radare2": {
      "command": "r2pm",
      "args": ["-r", "r2mcp"]
    }
  }
}
```

#### Claude Desktop

1. Press `CMD + ,` to open Developer settings
2. Edit the configuration file at:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
3. Add the JSON block above and restart Claude Desktop

#### VS Code (GitHub Copilot Chat)

Open the Command Palette (`CMD/Ctrl + Shift + P`), select **Copilot: Open User Configuration** (`~/Library/Application Support/Code/User/mcp.json` on macOS), and add:

```json
{
  "servers": {
    "radare2": {
      "type": "stdio",
      "command": "r2pm",
      "args": ["-r", "r2mcp"]
    }
  },
  "inputs": []
}
```

#### Zed

Open the Command Palette and select **agent: open configuration**, then add:

```json
"context_servers": {
  "r2-mcp-server": {
    "source": "custom",
    "command": "r2pm",
    "args": ["-r", "r2mcp"],
    "env": {}
  }
}
```

> Zed requires a separate LLM agent (Claude, Gemini, etc.) to be configured alongside the MCP server.

---

### 8.3 Docker

Build and run r2mcp in a container — useful for isolated or reproducible analysis environments:

```bash
docker build -t r2mcp .
```

**JSON configuration:**
```json
{
  "mcpServers": {
    "radare2": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-v", "/tmp/data:/data", "r2mcp"]
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add --scope user radare2 \
  -- docker run --rm -i -v /tmp/data:/data r2mcp
```

> Mount a local directory into `/data` inside the container to give r2mcp access to the binaries you want to analyze.

---

## 9. mcp-server-gdb (pansila)

**Repository:** [pansila/mcp_server_gdb](https://github.com/pansila/mcp_server_gdb)

A Rust-based MCP server that exposes a GDB interface to AI clients. It supports both stdio (default) and SSE transports and can be configured via environment variables or by editing `src/config.rs`.

---

### 9.1 Installation

#### Option A — Pre-built Binaries (Recommended for Beginners)

Download the binary for your platform from the [releases page](https://github.com/pansila/mcp_server_gdb/releases) and run it directly — no build step required.

---

#### Option B — Build From Source (Recommended for Professionals)

> **Pro note:** Rust's cargo build system produces fully static binaries on most targets, making the output easy to distribute or embed in Docker images.

**Requirements:** Rust toolchain (`cargo`)

```bash
git clone https://github.com/pansila/mcp_server_gdb.git
cd mcp_server_gdb

cargo build --release
# Binary: target/release/mcp-server-gdb
```

---

#### Option C — Nix

```bash
# Run locally (after cloning)
nix run .

# Run directly from GitHub without cloning
nix run "git+https://github.com/pansila/mcp_server_gdb.git" -- --help

# Enter a development shell with all dependencies
nix develop
```

---

### 9.2 MCP Client Configuration

The server runs in **stdio mode by default**. Start it and let your MCP client manage the process lifecycle.

#### Claude Code

```bash
claude mcp add --scope user mcp-server-gdb -- ./mcp-server-gdb
```

> Replace `./mcp-server-gdb` with the full path to the binary if it is not in your working directory or on `PATH`.

#### JSON Configuration (stdio — default)

```json
{
  "mcpServers": {
    "mcp-server-gdb": {
      "command": "/path/to/mcp-server-gdb",
      "args": []
    }
  }
}
```

#### SSE Transport

Start the server in SSE mode manually, then connect your client to the HTTP endpoint:

```bash
./mcp-server-gdb --transport sse
# Listens on http://127.0.0.1:8080 by default
```

```json
{
  "mcpServers": {
    "mcp-server-gdb": {
      "type": "sse",
      "url": "http://127.0.0.1:8080"
    }
  }
}
```

---

### 9.3 Configuration

Server behavior can be adjusted by editing `src/config.rs` before building, or by setting environment variables at runtime:

| Parameter | Description | Default |
|---|---|---|
| Server IP Address | Interface to bind | `127.0.0.1` |
| Server Port | Port for SSE transport | `8080` |
| GDB command timeout | Seconds before a GDB command times out | (project default) |

---

## 10. mcp-gdb (signal-slot)

**Repository:** [signal-slot/mcp-gdb](https://github.com/signal-slot/mcp-gdb)

An npm-native MCP server for GDB with zero-configuration Claude Code integration. The simplest way to connect an AI client to a GDB session.

---

### 10.1 Installation

#### Option A — npx (No Install Required, Recommended for Beginners)

No installation step needed — `npx` fetches and runs the package on demand:

```bash
npx -y mcp-gdb
```

---

#### Option B — Build From Source (Recommended for Professionals)

```bash
git clone https://github.com/signal-slot/mcp-gdb.git
cd mcp-gdb
npm install
npm run build
```

---

### 10.2 MCP Client Configuration

#### Claude Code

```bash
claude mcp add --scope user gdb -- npx -y mcp-gdb
```

#### JSON Configuration

```json
{
  "mcpServers": {
    "gdb": {
      "command": "npx",
      "args": ["-y", "mcp-gdb"]
    }
  }
}
```

---

## 11. LLDB MCP

**Documentation:** [lldb.llvm.org/use/mcp.html](https://lldb.llvm.org/use/mcp.html)

LLDB has built-in MCP server support via the `protocol-server` command. It listens on a TCP socket; MCP clients connect through a `netcat` bridge that forwards stdio over the network connection.

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│          │         │          │         │          │
│   LLDB   ├─socket──┤  netcat  ├─stdio───┤MCP Client│
│          │         │          │         │          │
└──────────┘         └──────────┘         └──────────┘
```

---

### 11.1 Starting the MCP Server in LLDB

Start the server from within an LLDB session, specifying a URI to listen on:

```
(lldb) protocol-server start MCP listen://localhost:59999
MCP server started with connection listeners: connection://[::1]:59999, connection://[127.0.0.1]:59999
```

Stop the server explicitly when no longer needed:

```
(lldb) protocol-server stop MCP
```

> The server stops automatically when LLDB exits. The commands fail if a server is already running (start) or not running (stop).

---

### 11.2 MCP Client Configuration

MCP clients connect via a `netcat` process that bridges stdio to LLDB's TCP socket.

#### Claude Code

```bash
claude mcp add --scope user lldb -- /usr/bin/nc localhost 59999
```

#### JSON Configuration (Claude Code / Claude Desktop)

```json
{
  "mcpServers": {
    "tool": {
      "command": "/usr/bin/nc",
      "args": ["localhost", "59999"]
    }
  }
}
```

#### VS Code (`mcp.json`)

```json
{
  "servers": {
    "lldb": {
      "type": "stdio",
      "command": "/usr/bin/nc",
      "args": ["localhost", "59999"]
    }
  }
}
```

> Adjust the `nc` path if `netcat` is installed elsewhere on your system (e.g., `/usr/local/bin/nc` on Homebrew macOS or `ncat` on some Linux distributions). The port (`59999`) must match the URI passed to `protocol-server start`.

---

## 12. CutterMCP (ap425q)

**Repository:** [ap425q/CutterMCP](https://github.com/ap425q/CutterMCP)

CutterMCP bridges the [Cutter](https://cutter.re/) reverse engineering GUI (built on radare2) to MCP clients via a Python plugin and bridge script. Any MCP client can connect; the Cutter plugin exposes an HTTP API that the bridge script forwards over stdio.

---

### 12.1 Installation

1. Download the latest release from [github.com/ap425q/CutterMCP/releases/latest](https://github.com/ap425q/CutterMCP/releases/latest) — the release contains both `CutterMCPPlugin.py` and `bridge_mcp_cutter.py`.
2. Run Cutter → **Edit → Preferences → Plugins** → note the plugin directory location.
3. Copy `CutterMCPPlugin.py` into the **python** subfolder of that directory.
4. Restart Cutter. The plugin appears under **Windows → Plugins** and adds a widget in the bottom panel.

---

### 12.2 MCP Client Configuration

#### Claude Code

```bash
claude mcp add --scope user cutter \
  -- python /ABSOLUTE_PATH_TO/bridge_mcp_cutter.py
```

> Use `python3` on Linux/macOS if `python` is not aliased.

#### JSON Configuration

**Linux / macOS:**
```json
{
  "mcpServers": {
    "cutter": {
      "command": "python",
      "args": ["/ABSOLUTE_PATH_TO/bridge_mcp_cutter.py"]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "cutter": {
      "command": "python",
      "args": ["C:\\ABSOLUTE_PATH_TO\\bridge_mcp_cutter.py"]
    }
  }
}
```

---

### 12.3 Remote Access

The Cutter plugin already binds to all interfaces (`''`, port `8000`) in the current release. Only the bridge script needs to be updated to point at the remote host.

#### Option A — Hardcoded (Quick)

Edit `bridge_mcp_cutter.py` and change the default server URL:

```python
DEFAULT_CUTTER_SERVER = "http://TARGET_IP:8000/"
cutter_server_url = DEFAULT_CUTTER_SERVER
```

#### Option B — Environment Variable (Recommended, Reusable)

Patch `bridge_mcp_cutter.py` to read from an environment variable:

```python
import os
DEFAULT_CUTTER_SERVER = os.getenv("CUTTER_SERVER_URL", "http://127.0.0.1:8000/")
cutter_server_url = DEFAULT_CUTTER_SERVER
```

Then set the variable in your MCP client configuration:

**JSON configuration:**
```json
{
  "mcpServers": {
    "cutter": {
      "command": "python",
      "args": ["/ABSOLUTE_PATH_TO/bridge_mcp_cutter.py"],
      "env": {
        "CUTTER_SERVER_URL": "http://TARGET_IP:8000/"
      }
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add --scope user cutter \
  -e CUTTER_SERVER_URL=http://TARGET_IP:8000/ \
  -- python /ABSOLUTE_PATH_TO/bridge_mcp_cutter.py
```

> If the plugin's bind address ever changes back to `localhost`, edit `CutterMCPPlugin.py` and set `server_address = ('', 8000)` to restore all-interfaces binding.

---

## 13. CutterMCP-plus (restkhz)

**Repository:** [restkhz/CutterMCP-plus](https://github.com/restkhz/CutterMCP-plus)

An enhanced fork of CutterMCP that adds a **Streamable HTTP mode** alongside the standard stdio mode, a bottom-panel remote config UI inside Cutter, and a standard-library-only plugin (no FastAPI/Pydantic required inside Cutter's embedded Python).

---

### 13.1 Installation

**Dependencies (for `mcp_server.py` wrapper only):**

```bash
pip install -r requirements.txt
```

The Cutter plugin (`mcp_plugin.py`) uses Python's standard library HTTP server and has no external dependencies.

**Default local endpoints exposed by the plugin:**

| Endpoint | Description |
|---|---|
| `http://127.0.0.1:8000/api/v1` | Main API root |
| `http://127.0.0.1:8000/api/v1/health` | Health check |
| `http://127.0.0.1:8000/docs` | API documentation |

**Plugin installation:**

1. Run Cutter → **Edit → Preferences → Plugins** → note the plugin directory.
2. Copy `mcp_plugin.py` (not `mcp_server.py`) into the **python** subfolder.
3. Restart Cutter.

---

### 13.2 MCP Client Configuration

#### stdio Mode (Standard)

```json
{
  "mcpServers": {
    "cuttermcp-plus": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp_server.py"]
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add --scope user cuttermcp-plus \
  -- python /ABSOLUTE/PATH/TO/mcp_server.py
```

---

#### Streamable HTTP Mode

Start the MCP wrapper manually after the Cutter plugin server is running:

```bash
python mcp_server.py --http --host 127.0.0.1 --port 9000
```

Then connect your client to the HTTP endpoint:

```json
{
  "mcpServers": {
    "cutter-mcp-http": {
      "autoApprove": [],
      "disabled": false,
      "timeout": 60,
      "type": "streamableHttp",
      "url": "http://127.0.0.1:9000/"
    }
  }
}
```

---

### 13.3 Remote Access

#### Change interface

1. In Cutter's bottom panel MCP tab, change the host from `127.0.0.1` to `0.0.0.0`
2. Click **Stop**, then **Start** to restart the server on all interfaces

Connect using Streamable HTTP from the remote client:

```json
{
  "mcpServers": {
    "cutter-mcp-http": {
      "autoApprove": [],
      "disabled": false,
      "timeout": 60,
      "type": "streamableHttp",
      "url": "http://TARGET_IP:9000/"
    }
  }
}
```

---

#### Patch `mcp_server.py` (stdio mode)

**Hardcoded:**

```python
# Change from:
BASE = "http://127.0.0.1:8000/api/v1"
# To:
BASE = "http://TARGET_IP:8000/api/v1"
```

**Environment variable (recommended, reusable):**

```python
import os
BASE = os.getenv("CUTTER_API_BASE", "http://127.0.0.1:8000/api/v1")
```

Then set it in your client configuration:

```json
{
  "mcpServers": {
    "cuttermcp-plus": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp_server.py"],
      "env": {
        "CUTTER_API_BASE": "http://TARGET_IP:8000/api/v1"
      }
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add --scope user cuttermcp-plus \
  -e CUTTER_API_BASE=http://TARGET_IP:8000/api/v1 \
  -- python /ABSOLUTE/PATH/TO/mcp_server.py
```

> ⚠️ **Security Notice:** Exposing the Cutter plugin API on all interfaces makes it reachable to anyone on the network. Only do this on trusted, isolated networks or behind a VPN/firewall.

---

## 14. x64dbg_automate (dariushoule)

**Repository:** [dariushoule/x64dbg-automate](https://github.com/dariushoule/x64dbg-automate)  
**Related resource:** [x64dbg-automate-pyclient](https://github.com/dariushoule/x64dbg-automate-pyclient)

x64dbg_automate is a plugin and Python client library that exposes x64dbg's debugging API over a ZeroMQ-based PubSub/ReqRep transport. It ships an MCP server entry-point (`x64dbg-automate-mcp`) making it compatible with Claude Code and any other MCP-aware client. The plugin supports both local (loopback) and remote (network) debugging targets.

---

### 14.1 Prerequisites

Ensure you have the latest Visual C++ Runtime Redistributable installed before proceeding:

| Package | Download |
|---|---|
| `vc_redist.x64.exe` (64-bit) | [aka.ms/vs/17/release/vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe) |
| `vc_redist.x86.exe` (32-bit) | [aka.ms/vs/17/release/vc_redist.x86.exe](https://aka.ms/vs/17/release/vc_redist.x86.exe) |

---

### 14.2 Installation

#### Step 1 — Install the x64dbg Plugin

1. Download the latest plugin release from `https://github.com/dariushoule/x64dbg-automate/releases`
2. Extract the entire contents of the archive's `Release` directory into your debugger's `plugins` directory (creating it if needed):

| Install Directory | Bitness |
|---|---|
| `x64dbg\release\x64\plugins` | 64-bit |
| `x64dbg\release\x32\plugins` | 32-bit |

#### Step 2 — Install the Python Client Library

Standard install (client only):

```sh
pip install x64dbg_automate --upgrade
```

To also install the MCP server for use with Claude Code or other MCP-compatible clients:

```sh
pip install x64dbg_automate[mcp] --upgrade
```

> 🔔 **Important:** The Microsoft Store builds of Python are restricted such that the client library may not function well. Use them at your own risk.

---

### 14.3 MCP Client Configuration

#### Claude Code

```bash
claude mcp add --scope user x64dbg -- x64dbg-automate-mcp
```

#### JSON Configuration

```json
{
  "mcpServers": {
    "x64dbg": {
      "command": "x64dbg-automate-mcp",
      "env": {
        "X64DBG_PATH": "C:\\path\\to\\x96dbg.exe"
      }
    }
  }
}
```

> Replace `C:\path\to\x96dbg.exe` with the absolute path to your x64dbg (or x32dbg) executable. The `X64DBG_PATH` environment variable is required at runtime.

---

#### Local Development (poetry)

To run the MCP server from a local source checkout — for example when testing changes to the client library — install with poetry and point your MCP configuration at the entry-point:

```powershell
cd C:\path\to\x64dbg-automate-pyclient
poetry install --extras mcp
```

JSON configuration for development use:

```json
{
  "mcpServers": {
    "x64dbg": {
      "command": "poetry",
      "args": [
        "-C", "C:\\path\\to\\x64dbg-automate-pyclient",
        "run", "x64dbg-automate-mcp"
      ],
      "env": {
        "X64DBG_PATH": "C:\\path\\to\\x96dbg.exe"
      }
    }
  }
}
```

---

### 14.4 Remote Access

x64dbg_automate uses ZeroMQ for transport. To connect to a remote x64dbg instance, configure the plugin on the guest/remote machine to bind on an accessible address by editing `x64dbg.ini`:

```ini
[XAutomate]
BindAddress=0.0.0.0
Mode=remote
PubSubPort=69BA
ReqRepPort=69BB
```

**Port reference:**

| Hex value | Decimal | Channel |
|---|---|---|
| `69BA` | 27066 | PubSub (publish) |
| `69BB` | 27067 | ReqRep (command) |

Once the plugin is bound and listening, instruct your agent to connect:

> *"Connect to the remote x64dbg at 192.168.x.x with REQ port 27067 and PUB port 27066"*

> ⚠️ **Security Notice:** Binding to `0.0.0.0` exposes the debug server on all network interfaces. Only do this on trusted, isolated networks or behind a firewall/VPN.

---

### 14.5 Building From Source

From a Visual Studio command prompt:

**64-bit plugin:**
```
cmake -B build64 -A x64
cmake --build build64 --config Release
```

**32-bit plugin:**
```
cmake -B build32 -A Win32
cmake --build build32 --config Release
```

---

## 15. x64dbgMCP (Wasdubya)

**Repository:** [Wasdubya/x64dbgMCP](https://github.com/Wasdubya/x64dbgMCP)

x64dbgMCP is a lightweight plugin that exposes an HTTP API from within x64dbg, paired with a Python bridge script (`x64dbg.py`) that forwards MCP protocol messages over that API. It requires no additional Python packages beyond what ships with the bridge script, and it works with Claude Desktop and any other MCP-compatible client.

---

### 15.1 Installation

#### Option A — Pre-built Plugin (Recommended for Beginners)

1. Grab the `.dp64` (64-bit) or `.dp32` (32-bit) plugin file from the repository's `build/release` directory at `https://github.com/Wasdubya/x64dbgMCP/releases`
2. Copy the file to your x64dbg plugins directory:

| Install Directory | Bitness |
|---|---|
| `[x64dbg_dir]\release\x64\plugins\` | 64-bit (`.dp64`) |
| `[x64dbg_dir]\release\x32\plugins\` | 32-bit (`.dp32`) |

3. Download `x64dbg.py` (the MCP bridge script) from the repository root.

---

#### Option B — Build From Source (Recommended for Professionals)

**Requirements:** CMake, MSVC (both must be on PATH)

```bash
git clone https://github.com/wasdubya/x64dbgmcp
cd x64dbgmcp
cmake -S . -B build
cmake --build build --target all_plugins --config Release
```

> **Tip:** Use `--target all_plugins` to build both 32-bit and 64-bit variants in a single pass. To build only one architecture, use the `-A` flag:

32-bit only:
```bash
cmake -S . -B build32 -A Win32 -DBUILD_BOTH_ARCHES=OFF
cmake --build build32 --config Release
```

The cmake configuration resolves the pluginsdk automatically — no manual dependency management is required.

---

### 15.2 MCP Client Configuration

#### JSON Configuration

```json
{
  "mcpServers": {
    "x64dbg": {
      "command": "Path\\To\\Python",
      "args": [
        "Path\\to\\x64dbg.py"
      ]
    }
  }
}
```

> Replace `Path\To\Python` with the full path to your Python interpreter, and `Path\to\x64dbg.py` with the absolute path to the bridge script.

---

### 15.3 Usage

1. Launch x64dbg and load a target binary.
2. Verify the plugin loaded successfully: press **ALT+L** in x64dbg to open the log window and confirm the MCP plugin entry appears.
3. Start Claude Desktop (or your MCP client) — it will connect to the bridge automatically.

---

### 15.4 Remote Access

By default, the HTTP server inside the plugin binds only to the loopback interface (`127.0.0.1`). Two changes are needed to accept connections from other machines.

#### Step 1 — Patch the Plugin Source

In `src/mcpserver.cpp`, change the bind address from loopback to any-interface:

**Before:**
```cpp
serverAddr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
```

**After:**
```cpp
serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
```

Rebuild the plugin (see Section 15.1 Option B) and copy the resulting `.dp64`/`.dp32` to your plugins directory.

#### Step 2 — Update the Bridge Script

In `x64dbg.py`, either change the default server address directly:

**Before:**
```python
DEFAULT_X64DBG_SERVER = "http://127.0.0.1:8888/"
```

**After:**
```python
DEFAULT_X64DBG_SERVER = "http://TARGET_IP:8888/"
```

Or keep the default and pass the target address via the `X64DBG_URL` environment variable in your MCP client configuration:

```json
{
  "mcpServers": {
    "x64dbg": {
      "command": "Path\\To\\Python",
      "args": ["Path\\to\\x64dbg.py"],
      "env": {
        "X64DBG_URL": "http://TARGET_IP:8888/"
      }
    }
  }
}
```

> ⚠️ **Security Notice:** Binding the plugin server to `INADDR_ANY` exposes the x64dbg HTTP API on all network interfaces. Only use this on trusted, isolated networks or behind a VPN/firewall.

---

## 16. IDA Pro MCP (mrexodia)

**Repository:** [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp)

A comprehensive MCP server for IDA Pro supporting stdio, Streamable HTTP, and SSE transports. It also ships `idalib-mcp` for fully headless analysis without the IDA GUI. New tools can be added by annotating Python functions with `@tool` in the modular API files — no additional boilerplate required.

---

### 16.1 Installation

#### Step 1 — Install the Python Package

```bash
pip install https://github.com/mrexodia/ida-pro-mcp/archive/refs/heads/main.zip
```

> To update, uninstall first then reinstall:
> ```bash
> pip uninstall ida-pro-mcp
> pip install https://github.com/mrexodia/ida-pro-mcp/archive/refs/heads/main.zip
> ```

#### Step 2 — Install the IDA Plugin and Configure MCP Clients

```bash
ida-pro-mcp --install
```

This command installs the IDA plugin and auto-configures supported MCP clients. For an automated single-step install targeting a specific client:

```bash
# Pro tip: automate for a named client with global scope and HTTP transport
ida-pro-mcp --install client-name --scope global --transport streamable-http
```

> **Important:** Completely restart IDA Pro and your MCP client after installation. Some clients (such as Claude) run in the background — quit them from the system tray icon before restarting.

---

### 16.2 MCP Client Configuration

Run `ida-pro-mcp --config` to print ready-to-use configuration blocks for all supported transports:

```
[STDIO MCP CONFIGURATION]
{
  "mcpServers": {
    "ida-pro-mcp": {
      "command": "C:\\...\\python.exe",
      "args": ["C:\\...\\ida_pro_mcp\\server.py"]
    }
  }
}

[STREAMABLE HTTP MCP CONFIGURATION]
{
  "mcpServers": {
    "ida-pro-mcp": {
      "type": "http",
      "url": "http://127.0.0.1:13337/mcp"
    }
  }
}

[SSE MCP CONFIGURATION]
{
  "mcpServers": {
    "ida-pro-mcp": {
      "type": "http",
      "url": "http://127.0.0.1:13337/mcp"
    }
  }
}
```

#### stdio (default)

```json
{
  "mcpServers": {
    "ida-pro-mcp": {
      "command": "/path/to/python",
      "args": ["/path/to/site-packages/ida_pro_mcp/server.py"]
    }
  }
}
```

#### Streamable HTTP / SSE

The IDA plugin exposes an HTTP server on port `13337`. Connect directly using the HTTP transport:

```json
{
  "mcpServers": {
    "ida-pro-mcp": {
      "type": "http",
      "url": "http://127.0.0.1:13337/mcp"
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add --scope user ida-pro-mcp --transport http -- http://127.0.0.1:13337/mcp
```

---

### 16.3 SSE Transport & Headless Mode

#### SSE Server (GUI mode)

Run an SSE bridge that connects to a running IDA instance:

```bash
uv run ida-pro-mcp --transport http://127.0.0.1:8744/sse
```

#### Headless SSE Server (idalib — no GUI required)

After installing `idalib`, analyze a binary entirely without the IDA GUI:

```bash
uv run idalib-mcp --host 127.0.0.1 --port 8745 path/to/executable
```

---

### 16.4 Remote Access

To accept connections from machines other than `localhost`, patch the IDA plugin to bind on all interfaces.

#### Patch `ida_mcp.py` (PowerShell)

Locate the IDA plugin directory, then apply the patch:

```powershell
$pluginDir = "C:\path\to\IDA\plugins"
$cpp = "$pluginDir\ida_mcp.py"
(Get-Content $cpp) -replace 'DEFAULT_HOST = "127\.0\.0\.1"', 'DEFAULT_HOST = "0.0.0.0"' | Set-Content $cpp
```

After patching, connect from the remote client using Streamable HTTP or SSE:

```json
{
  "mcpServers": {
    "ida-pro-mcp": {
      "type": "http",
      "url": "http://TARGET_IP:13337/mcp"
    }
  }
}
```

> ⚠️ **Security Notice:** Binding to `0.0.0.0` exposes the IDA MCP server on all network interfaces. Only do this on trusted, isolated networks or behind a VPN/firewall.

---

### 16.5 Testing & Development

#### Inspect MCP Tools Interactively

```bash
npx -y @modelcontextprotocol/inspector
```

Opens a web interface at `http://localhost:5173` for browsing and calling MCP tools without a full client.

#### Add New Tools

All tool functions live in `src/ida_pro_mcp/ida_mcp/api_*.py`. Decorate any new function with `@tool` and it is automatically registered in the MCP server — no boilerplate, no registration step:

```python
@tool
def get_metadata() -> dict:
    """Return basic metadata about the loaded binary."""
    return {
        "filename": idc.get_input_file_path(),
        "md5": idc.retrieve_input_file_md5(),
    }
```

#### Generate a Changelog

```bash
git log --first-parent --no-merges 1.2.0..main "--pretty=- %s"
```

---

## 17. mcp-server-ida (MxIris)

**Repository:** [MxIris-Reverse-Engineering/ida-mcp-server](https://github.com/MxIris-Reverse-Engineering/ida-mcp-server)

A lightweight IDA Pro MCP server distributed as the `mcp-server-ida` Python package. The IDA-side plugin is a pair of files copied manually into IDA's plugin directory. Remote access requires patching both the plugin (to bind on all interfaces) and the bridge module (to read the target host from environment variables).

---

### 17.1 Installation

#### Step 1 — Install the Python Package

**Using `uv` (recommended — no explicit install needed):**

```bash
# Run directly via uvx — uv fetches and manages the environment automatically
uvx mcp-server-ida
```

**Using pip:**

```bash
pip install mcp-server-ida
```

Run after pip install:

```bash
python -m mcp_server_ida
```

#### Step 2 — Install the IDA Plugin

Copy both of the following from the repository into your IDA plugins directory:

- `repository/plugin/ida_mcp_server_plugin.py`
- `repository/plugin/ida_mcp_server_plugin/` (the entire directory)

IDA plugins directories by platform:

| Platform | Path |
|---|---|
| Windows | `%APPDATA%\Hex-Rays\IDA Pro\plugins\` |
| macOS | `~/Library/Application Support/Hex-Rays/IDA Pro/plugins/` |
| Linux | `~/.idapro/plugins/` |

---

### 17.2 MCP Client Configuration

#### Using `uvx` (recommended)

```json
{
  "mcpServers": {
    "ida": {
      "command": "uvx",
      "args": ["mcp-server-ida"]
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add --scope user ida -- uvx mcp-server-ida
```

#### Using pip / system Python

```json
{
  "mcpServers": {
    "ida": {
      "command": "python",
      "args": ["-m", "mcp_server_ida"]
    }
  }
}
```

---

### 17.3 Remote Access

Connecting to an IDA instance on a different machine requires two patches: one to the IDA plugin (to bind on all interfaces) and one to the bridge module (to read the remote host from environment variables).

#### Step 1 — Patch the IDA Plugin (on the IDA machine)

Change the default bind host from `localhost` to `0.0.0.0` in the plugin file:

**PowerShell:**
```powershell
$pluginDir = "C:\path\to\IDA\plugins"
$cpp = "$pluginDir\ida_mcp_server_plugin.py"
(Get-Content $cpp) -replace 'DEFAULT_HOST = "localhost"', 'DEFAULT_HOST = "0.0.0.0"' | Set-Content $cpp
```

**sed (Linux / macOS):**
```bash
sed -i 's/DEFAULT_HOST = "localhost"/DEFAULT_HOST = "0.0.0.0"/' \
  ~/.idapro/plugins/ida_mcp_server_plugin.py
```

#### Step 2 — Patch the Bridge Module (on the client machine)

Edit `src/mcp_server_ida/server.py`. Add `import os` at the top of the file, then update the `serve()` function to read the host and port from environment variables:

```python
import os

# In the serve() function, replace the IDAProCommunicator instantiation:
host = os.environ.get("IDA_HOST", "localhost")
port = int(os.environ.get("IDA_PORT", "5000"))
ida_communicator: IDAProCommunicator = IDAProCommunicator(host=host, port=port)
```

#### Step 3 — Make the Patched Module Available

Place the modified `mcp_server_ida` package in a directory of your choice, then add that directory to `PYTHONPATH`:

```bash
# Linux / macOS
export PYTHONPATH="$HOME/my_modules:$PYTHONPATH"

# Windows (PowerShell)
$env:PYTHONPATH = "C:\my_modules;$env:PYTHONPATH"
```

Put the patched package inside that directory, then invoke it:

```bash
python3 -m mcp_server_ida
```

#### Step 4 — Configure the MCP Client

Pass `IDA_HOST` and `IDA_PORT` as environment variables in your client configuration:

**JSON configuration:**
```json
{
  "mcpServers": {
    "ida": {
      "command": "python",
      "args": ["-m", "mcp_server_ida"],
      "env": {
        "IDA_HOST": "192.168.1.50",
        "IDA_PORT": "5000",
        "PYTHONPATH": "/path/to/my_modules"
      }
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add --scope user ida \
  -e IDA_HOST=192.168.1.50 \
  -e IDA_PORT=5000 \
  -e PYTHONPATH=/path/to/my_modules \
  -- python3 -m mcp_server_ida
```

> Replace `192.168.1.50` with the IP or hostname of the machine running IDA Pro. Ensure port `5000` (or your chosen port) is reachable through any firewalls.

> ⚠️ **Security Notice:** Patching the plugin to bind on `0.0.0.0` exposes the IDA MCP server on all network interfaces. Only do this on trusted, isolated networks or behind a VPN/firewall.

---

## Security Considerations

Remote access patches in this guide disable origin validation and localhost-only restrictions. Before enabling remote access, ensure:

- The host is on a trusted, isolated network or behind a VPN/firewall
- Exposed ports are not accessible from untrusted networks
- Access is logged and monitored where required by your organization's security policy

---

*For the most current information on each server, refer to the official repositories linked in each section.*
