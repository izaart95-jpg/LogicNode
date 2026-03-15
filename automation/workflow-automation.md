# Workflow Automation — n8n, Tasker & MacroDroid

Workflow automation connects services, triggers actions based on events, and eliminates repetitive manual tasks. From self-hosted server pipelines to Android device automation, these tools let you build complex multi-step workflows with visual builders and code-level customization.

---

## Table of Contents
1. [What is Workflow Automation?](#1-what-is-workflow-automation)
2. [n8n](#2-n8n)
3. [Tasker (Android)](#3-tasker-android)
4. [MacroDroid (Android)](#4-macrodroid-android)
5. [Comparison Table](#5-comparison-table)

---

## 1. What is Workflow Automation?

### Core Concepts

Workflow automation is the process of connecting multiple services and actions into automated pipelines that execute without human intervention.

- **Triggers** — events that start a workflow (webhook received, file uploaded, time schedule, sensor change)
- **Actions** — operations performed in response (send email, update database, call API, toggle device)
- **Conditions** — logic gates that control flow (if/else, filters, switches)
- **Loops** — iterate over lists of items (process each row, handle batch data)

### Event-Driven Architecture

```
┌──────────┐     Trigger      ┌──────────────┐     Action      ┌──────────────┐
│  Event   │ ──────────────▶  │  Automation   │ ─────────────▶  │  Service /   │
│  Source  │                  │  Engine       │                 │  Output      │
│          │                  │  (n8n/Tasker) │                 │              │
└──────────┘                  └──────────────┘                 └──────────────┘
  Webhook                       Filter, Transform,               Slack message
  Schedule                      Route, Enrich                    Database write
  Sensor                                                         API call
```

### Self-Hosted vs SaaS

| Approach | Pros | Cons | Examples |
|----------|------|------|----------|
| **Self-hosted** | Full control, no data leaves your server, no usage limits | Maintenance, hosting costs | n8n, Huginn, Node-RED |
| **SaaS** | Zero maintenance, instant setup | Vendor lock-in, usage limits, data privacy | Zapier, Make (Integromat), IFTTT |

---

## 2. n8n

- **Website:** https://n8n.io
- **License:** Sustainable Use License (fair-code, source-available)
- **Type:** Self-hosted workflow automation platform with optional cloud offering
- **Integrations:** 400+ built-in nodes

### 2.1 Installation

```bash
# Docker (recommended)
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n

# Docker Compose
cat > docker-compose.yml << 'EOF'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=changeme
    restart: unless-stopped

volumes:
  n8n_data:
EOF
docker compose up -d

# npm (global install)
npm install n8n -g
n8n start
# Opens at http://localhost:5678
```

### 2.2 Key Concepts

| Concept | Description |
|---------|-------------|
| **Workflow** | A pipeline of connected nodes that processes data |
| **Node** | A single step — trigger, action, or logic operation |
| **Trigger node** | Starts the workflow (webhook, cron, app event) |
| **Credentials** | Stored API keys and OAuth tokens for services |
| **Execution** | A single run of a workflow with its input/output data |
| **Pinned data** | Test data pinned to a node for development |

### 2.3 Visual Workflow Editor

The browser-based editor lets you drag-and-drop nodes, connect them with wires, and test each step interactively.

```
[Webhook Trigger] → [HTTP Request] → [IF Condition] → [Slack]
                                           ↓
                                      [Google Sheets]
```

### 2.4 Code Nodes

Write custom JavaScript or Python within workflows:

```javascript
// JavaScript Code node
const items = $input.all();
const processed = items.map(item => ({
    json: {
        name: item.json.name.toUpperCase(),
        timestamp: new Date().toISOString()
    }
}));
return processed;
```

```python
# Python Code node
from datetime import datetime

items = []
for item in _input.all():
    items.append({
        "name": item["json"]["name"].upper(),
        "timestamp": datetime.now().isoformat()
    })
return items
```

### 2.5 Webhook Triggers

```bash
# n8n creates webhook URLs like:
# http://localhost:5678/webhook/abc-123-def

# Test with curl
curl -X POST http://localhost:5678/webhook/abc-123-def \
  -H "Content-Type: application/json" \
  -d '{"event": "push", "repo": "myapp"}'
```

### 2.6 Example Workflow: GitHub to Slack

1. **Webhook Trigger** — receives GitHub push events
2. **Set Node** — extracts commit message, author, repo name
3. **IF Node** — checks if branch is `main`
4. **Slack Node** — sends formatted notification to `#deployments` channel

### 2.7 n8n vs Zapier vs Make

| Feature | n8n | Zapier | Make (Integromat) |
|---------|-----|--------|-------------------|
| **Pricing** | Free (self-hosted) | Free: 100 tasks/mo | Free: 1,000 ops/mo |
| **Self-hosted** | Yes | No | No |
| **Integrations** | 400+ | 6,000+ | 1,500+ |
| **Code nodes** | JavaScript, Python | Limited (JS only) | Limited |
| **Branching/Logic** | Full (IF, Switch, Merge) | Paths (limited) | Routers, filters |
| **Webhooks** | Unlimited | Limited on free | Unlimited |
| **Data privacy** | Full control | Cloud only | Cloud only |
| **Complexity** | Medium-High | Low | Medium |
| **Open source** | Fair-code | No | No |

---

## 3. Tasker (Android)

- **Website:** https://tasker.joaoapps.com
- **Price:** ~$3.49 on Google Play Store
- **Type:** Android automation powerhouse
- **Requirements:** Android 7.0+, some features need ADB or root

### 3.1 Core Concepts

| Component | Purpose |
|-----------|---------|
| **Profile** | Defines WHEN to trigger (context: time, location, app, event) |
| **Task** | Defines WHAT to do (sequence of actions) |
| **Scene** | Custom UI elements (popups, overlays, full screens) |
| **Variable** | Data storage (`%BATT` = battery, `%TIME` = current time) |
| **Project** | Groups related profiles, tasks, and scenes |

### 3.2 Triggers (Profile Contexts)

| Trigger Type | Examples |
|-------------|----------|
| **Time** | 8:00 AM daily, every 30 minutes, date range |
| **Location** | Enter/exit geofence, cell tower proximity |
| **Application** | App opened/closed (e.g., camera launched) |
| **Event** | SMS received, call incoming, notification posted, shake |
| **State** | WiFi connected, Bluetooth on, headphones plugged, orientation |
| **NFC** | Specific NFC tag scanned |

### 3.3 Actions (350+ Built-in)

```
Categories:
  - Alert (flash, notify, vibrate, say)
  - App (launch, kill, open settings)
  - Audio (volume, ringtone, media control)
  - Display (brightness, rotation, wallpaper)
  - File (read, write, copy, delete, list)
  - Input (type, tap coordinates, swipe)
  - Net (WiFi toggle, HTTP request, Bluetooth)
  - Phone (call, SMS, contacts)
  - Script (Run Shell, JavaScriptlet, Python)
  - System (set alarm, airplane mode, reboot)
  - Variables (set, split, convert, array)
```

### 3.4 Example: Auto-Toggle WiFi by Location

```
Profile: "Home WiFi"
  Trigger: Location (enter home geofence, 200m radius)
  Entry Task:
    1. WiFi → On
    2. Flash "Welcome home"
  Exit Task:
    1. WiFi → Off
    2. Flash "WiFi off - using mobile data"
```

### 3.5 Integration with Termux

```bash
# Install Termux:Tasker plugin from F-Droid
# Create scripts in ~/.termux/tasker/

# Example: ~/.termux/tasker/backup.sh
#!/bin/bash
tar -czf /sdcard/backup/home-$(date +%F).tar.gz ~/projects/

# Tasker action: Plugin → Termux:Tasker → script: backup.sh
```

### 3.6 JavaScript & Shell in Tasks

```javascript
// Tasker JavaScriptlet action
var battery = global('%BATT');
var ssid = global('%WIFII').split('"')[1];

if (battery < 20 && ssid !== 'HomeWiFi') {
    performTask('PowerSave', 10);  // Run another task
    flash('Low battery - enabling power save');
}
```

```bash
# Tasker Run Shell action
# Get public IP
curl -s ifconfig.me
# Result stored in %stdout
```

---

## 4. MacroDroid (Android)

- **Website:** https://www.macrodroid.com
- **Price:** Free (5 macros) / Pro ~$4.99 (unlimited)
- **Type:** User-friendly Android automation
- **Requirements:** Android 5.0+

### 4.1 Core Model

MacroDroid uses a simplified three-part structure:

```
┌──────────┐     ┌──────────┐     ┌─────────────┐
│ Trigger  │ ──▶ │ Action   │ ──▶ │ Constraint  │
│ (when)   │     │ (do)     │     │ (only if)   │
└──────────┘     └──────────┘     └─────────────┘
```

- **Triggers** — what starts the macro (time, event, location, sensor)
- **Actions** — what happens (send SMS, toggle setting, launch app)
- **Constraints** — conditions that must be true for the macro to run (battery level, day of week, WiFi state)

### 4.2 Visual Macro Builder

The drag-and-drop interface makes complex automations accessible:

1. Tap **Add Macro**
2. Select a **Trigger** (e.g., "SMS Received")
3. Add **Actions** (e.g., "Send SMS", "Speak Text")
4. Add **Constraints** (e.g., "Only when Driving")
5. Name and save

### 4.3 Templates Marketplace

MacroDroid includes a community template library with pre-built macros:

- Auto-reply to calls when busy
- Battery charge notification
- Auto-rotate for specific apps
- WiFi toggle on home location
- Silence phone during calendar events

### 4.4 Example: Auto-Reply to SMS When Driving

```
Macro: "Driving Auto-Reply"
  Trigger: SMS Received (any number)
  Constraint: Bluetooth connected to "CarBT"
  Actions:
    1. Wait 5 seconds
    2. Send SMS → sender number → "I'm driving. I'll reply later."
    3. Notification: "Auto-replied to {sender}"
```

### 4.5 MacroDroid vs Tasker

| Feature | MacroDroid | Tasker |
|---------|-----------|--------|
| **Ease of use** | Beginner-friendly | Steep learning curve |
| **Free tier** | 5 macros | None (paid app) |
| **Actions** | 100+ | 350+ |
| **Scripting** | Limited (variables, basic logic) | Full (JavaScript, Shell, Python) |
| **UI creation** | No | Yes (Scenes) |
| **Plugin ecosystem** | Small | Large (AutoInput, Join, etc.) |
| **Reliability** | Good | Excellent (more mature) |
| **Community** | Templates marketplace | Large community, forums, Reddit |
| **Best for** | Simple automations, beginners | Power users, complex workflows |

---

## 5. Comparison Table

| Feature | n8n | Tasker | MacroDroid |
|---------|-----|--------|------------|
| **Platform** | Web (self-hosted/cloud) | Android | Android |
| **Type** | Service integration | Device automation | Device automation |
| **Free Tier** | Unlimited (self-hosted) | None (~$3.49) | 5 macros |
| **Integrations** | 400+ web services | 350+ device actions | 100+ device actions |
| **Self-Hosted** | Yes (Docker/npm) | N/A (on-device) | N/A (on-device) |
| **Visual Builder** | Yes (node editor) | Yes (profile/task) | Yes (macro builder) |
| **Code Support** | JavaScript, Python | JavaScript, Shell | Variables only |
| **Webhooks** | Yes | Via HTTP Request | Via HTTP Request |
| **Complexity** | Medium | High | Low |
| **Best For** | Server workflows, API chains | Android power users | Simple phone automation |

---

## See Also

- [Web Automation](web-automation.md) — Playwright, Selenium, Puppeteer for browser automation
- [Docker Essentials](../devtools/docker-essentials.md) — Running n8n and other services in containers
- [Termux Setup](../mobile/termux-setup.md) — Terminal environment for Tasker integration
- [Linux on Android](../mobile/linux-on-android.md) — Advanced Android automation with Linux tools
