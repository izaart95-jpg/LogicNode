# Android Automation

A guide to automating tasks on Android devices, covering Arduino development on mobile with ArduinoDroid, advanced automation with Tasker, and user-friendly macro creation with MacroDroid. This document explores root and non-root approaches, accessibility services, and ADB-based automation strategies.

---

## Table of Contents

1. [Android Automation Overview](#1-android-automation-overview)
2. [ArduinoDroid](#2-arduinodroid)
3. [Tasker](#3-tasker)
4. [MacroDroid](#4-macrodroid)
5. [Comparison Table](#5-comparison-table)

---

## 1. Android Automation Overview

### 1.1 What is Android Automation?

Android automation refers to the practice of configuring a device to perform tasks automatically based on triggers, conditions, or schedules. This ranges from simple actions like toggling WiFi at specific locations to complex workflows involving shell commands, HTTP requests, and inter-app communication.

### 1.2 Root vs Non-Root Approaches

- **Non-root**: Most automation apps work without root access by leveraging Android's Accessibility Services, notification listeners, and standard APIs. This is sufficient for the majority of automation tasks.
- **Root**: Rooted devices unlock additional capabilities such as modifying system settings, simulating input events at a lower level, controlling other apps directly, and running privileged shell commands. Root is required for tasks like changing CPU governors, modifying system files, or capturing screen content without user interaction.

### 1.3 Accessibility Services vs ADB-Based Automation

- **Accessibility Services**: Android's built-in framework that allows apps to observe and interact with the UI. Used by automation apps like Tasker (via AutoInput plugin) and MacroDroid to tap buttons, read screen text, and detect UI changes. No PC required.
- **ADB-based**: Android Debug Bridge commands can be sent from a connected PC or from the device itself (via Termux or wireless ADB). ADB provides low-level control including `input tap`, `input swipe`, `am start` (launch activities), `pm` (package management), and `settings put` (modify system settings).

```bash
# ADB examples for automation
adb shell input tap 500 800          # Tap at coordinates (500, 800)
adb shell input swipe 300 1000 300 300  # Swipe up
adb shell am start -n com.app/.MainActivity  # Launch an app
adb shell settings put system screen_brightness 128  # Set brightness
adb shell dumpsys battery             # Get battery info
```

---

## 2. ArduinoDroid

ArduinoDroid is an Arduino IDE for Android that allows users to write, compile, and upload Arduino sketches directly from a phone or tablet. It brings portable microcontroller development to mobile devices.

### 2.1 Key Features

- **C/C++ code editor**: Full-featured editor with syntax highlighting, auto-indentation, line numbers, and find/replace.
- **Real-time compilation on device**: Compiles sketches locally on the Android device without needing a remote server.
- **USB OTG upload**: Upload compiled sketches to Arduino boards via USB OTG connection. Supported boards include Arduino Uno, Nano, Mega, Leonardo, ESP8266, and ESP32.
- **Serial monitor**: Read and send serial data to/from connected boards for debugging and communication.
- **Library manager**: Browse, install, and manage Arduino libraries directly within the app.
- **Code examples**: Built-in example sketches for common tasks (Blink, Serial communication, sensor reading, etc.).

### 2.2 Requirements

- Android device with USB OTG support
- USB OTG adapter (USB-C or Micro-USB to USB-A)
- Arduino board (or compatible: ESP8266, ESP32)
- USB cable for the board
- ArduinoDroid app (Google Play Store: free with ads, paid version for ad-free)

### 2.3 Limitations vs Desktop Arduino IDE

| Feature | ArduinoDroid | Desktop Arduino IDE |
|---------|-------------|-------------------|
| Compilation speed | Slower (mobile CPU) | Fast |
| Library support | Most common libraries | Full library ecosystem |
| Board support | Major boards + ESP | All officially supported boards |
| Debugger | No | Yes (Arduino IDE 2.x) |
| Serial plotter | No | Yes |
| OTA updates | Limited | Full support |
| Multiple tabs/files | Limited | Full support |
| Third-party tools integration | No | Yes (platformio, etc.) |

### 2.4 Use Cases

- **Field programming**: Update firmware on deployed devices without carrying a laptop.
- **Quick fixes**: Make small code changes and upload on the go.
- **Portable development**: Develop and test Arduino projects anywhere.
- **Education**: Learn Arduino programming on a phone or tablet.
- **IoT debugging**: Connect to ESP devices and monitor serial output in the field.

---

## 3. Tasker

Tasker is the most powerful and flexible automation app available for Android. It allows users to create complex automated workflows based on a wide range of triggers, conditions, and actions.

- **Install**: Google Play Store (~$3.49, one-time purchase)
- **Developer**: Joao Dias
- **Requirements**: Android 7.0+

### 3.1 Core Architecture

Tasker is built around four fundamental components:

- **Profiles**: Define trigger conditions that activate tasks. A profile consists of one or more contexts (time, location, application, event, state, NFC tag) and linked entry/exit tasks.
- **Tasks**: Sequences of actions that execute in order. Tasker provides 350+ built-in action types covering device settings, app control, media, networking, scripting, and more.
- **Scenes**: Custom UI overlays and dialogs that can be designed within Tasker. Scenes support buttons, text fields, sliders, images, and web views.
- **Variables**: Store and manipulate data. Local variables (`%var`) are scoped to a task; global variables (`%VAR`) persist across tasks and are accessible everywhere.

### 3.2 Termux Integration

Tasker can execute commands in Termux via the Termux:Tasker plugin, enabling powerful shell scripting capabilities:

```bash
# Install Termux:Tasker plugin from F-Droid
# Then install the helper package in Termux
pkg install termux-tasker

# Create a script directory for Tasker
mkdir -p ~/.termux/tasker

# Create a script that Tasker can execute
echo '#!/bin/bash
echo "Hello from Tasker"
date
uptime' > ~/.termux/tasker/myscript.sh
chmod +x ~/.termux/tasker/myscript.sh

# Create a backup script triggered by Tasker
echo '#!/bin/bash
tar -czf /sdcard/backup_$(date +%Y%m%d).tar.gz ~/important_files/
echo "Backup complete"' > ~/.termux/tasker/backup.sh
chmod +x ~/.termux/tasker/backup.sh
```

### 3.3 ADB WiFi Commands from Tasker

Tasker can send ADB commands over WiFi to other Android devices or to itself (if ADB over WiFi is enabled):

```bash
# Enable ADB over WiFi (requires initial USB connection or root)
adb tcpip 5555

# From Tasker, use Shell action to run ADB commands
# Target: the device itself or another device on the network
adb connect 192.168.1.100:5555
adb -s 192.168.1.100:5555 shell input tap 500 800
```

### 3.4 JavaScript and Shell Within Tasks

Tasker supports inline JavaScript and shell scripting within tasks:

- **JavaScriptlet action**: Execute JavaScript code with access to Tasker variables and functions.
- **Shell action**: Run shell commands (with or without root).
- **Run Shell action**: Execute commands and capture stdout/stderr into variables.

### 3.5 Popular Plugins

Tasker's functionality is extended through a plugin ecosystem:

- **AutoInput**: Simulate taps, swipes, and text input; read on-screen text via Accessibility Service.
- **AutoNotification**: Intercept, create, and manage notifications; reply to messaging apps.
- **AutoVoice**: Custom voice commands, Google Assistant integration, natural language processing.
- **Termux:Tasker**: Execute Termux shell scripts from Tasker profiles.
- **AutoWear**: Extend Tasker automation to Wear OS smartwatches.
- **AutoContacts**: Access and manipulate contacts database.

### 3.6 Example Profiles

- **Auto-WiFi toggle by location**: Turn WiFi on when arriving at home/office (GPS or cell tower geofence), turn off when leaving.
- **Battery saver at low percentage**: When battery drops below 20%, disable WiFi/Bluetooth/sync, reduce brightness, enable battery saver mode.
- **Auto-DND during meetings**: Read calendar events and enable Do Not Disturb mode during scheduled meetings. Send auto-reply SMS to callers.
- **Automated backup via Termux script**: Trigger a Termux backup script every night at 2 AM when connected to WiFi and charging.
- **Smart alarm**: Adjust alarm time based on calendar events; play weather report via TTS after dismissing alarm.

---

## 4. MacroDroid

MacroDroid is a user-friendly Android automation app that provides an intuitive visual interface for creating automated workflows. It is designed to be accessible to users who find Tasker's learning curve too steep.

- **Install**: Google Play Store (free tier: 5 macros, Pro unlock for unlimited)
- **Developer**: ArloSoft
- **Requirements**: Android 5.0+

### 4.1 Macro Architecture

MacroDroid uses a simple three-part model:

- **Triggers**: Events that start the macro (what causes it to run).
- **Actions**: Operations to perform when triggered (what it does).
- **Constraints**: Conditions that must be met for the macro to execute (when it is allowed to run).

### 4.2 Visual Macro Builder

MacroDroid features a drag-and-drop interface for building macros:

- Category-based browsing of triggers, actions, and constraints
- Visual flow representation
- Color-coded elements for easy identification
- Built-in testing for individual actions
- Macro templates marketplace with pre-made macros ready to import

### 4.3 Key Triggers

- **Time-based**: Specific time, interval, day of week, recurring schedule
- **Battery**: Level thresholds, charging state changes
- **Communication**: Incoming/outgoing call, SMS received/sent, missed call
- **Notification**: Specific app notification, notification content matching
- **Location**: GPS geofence, WiFi network detection, cell tower
- **Connectivity**: NFC tag scanned, Bluetooth device connected/disconnected, WiFi connected/disconnected
- **Device**: Screen on/off, boot completed, headphones plugged in, shake/flip detection
- **App**: Application launched/closed

### 4.4 Key Actions

- Launch application or activity
- Show notification or toast message
- Speak text (text-to-speech)
- Send HTTP request (GET/POST)
- Execute shell command (root or non-root)
- Toggle settings (WiFi, Bluetooth, GPS, brightness, volume)
- Send SMS or make a call
- Control media playback
- Write to file or clipboard
- Set variable values

### 4.5 Constraints

Constraints act as guards that prevent a macro from running unless conditions are met:

- Battery level above/below threshold
- WiFi connected to specific network
- Screen on or off
- Bluetooth connected to specific device
- Time window (only between certain hours)
- Day of week
- Device orientation

### 4.6 Example Macros

- **Auto-reply to missed calls via SMS**: Trigger on missed call, action sends a pre-written SMS to the caller, constrained to work hours only.
- **Toggle flashlight by shaking device**: Trigger on device shake, action toggles flashlight, constrained to screen-off state.
- **Auto-enable hotspot when specific Bluetooth device connects**: Trigger on Bluetooth connection with a specific device name, action enables mobile hotspot.
- **Morning routine**: Trigger at 7:00 AM on weekdays, actions: disable DND, set volume to 70%, speak weather forecast, open news app.
- **Low storage warning**: Trigger on storage below 1GB, action shows persistent notification with storage details.

### 4.7 MacroDroid vs Tasker

| Feature | MacroDroid | Tasker |
|---------|-----------|--------|
| Price | Free (5 macros) / Pro | ~$3.49 (one-time) |
| Learning curve | Easy (visual builder) | Steep (powerful but complex) |
| Interface | Drag-and-drop, intuitive | Tab-based, dense |
| Built-in actions | ~100+ | ~350+ |
| Plugin ecosystem | Limited | Extensive (Auto* plugins) |
| Scripting | Shell commands | JavaScript, shell, Java functions |
| Custom UI (Scenes) | No | Yes |
| Termux integration | No (shell commands only) | Yes (via Termux:Tasker) |
| Variables | Basic | Advanced (arrays, structures) |
| Community | Templates marketplace | Profiles on Reddit, TaskerNet |
| Best for | Beginners, simple automations | Power users, complex workflows |

---

## 5. Comparison Table

| App | Price | Complexity | Triggers | Termux Integration | Best For |
|-----|-------|-----------|----------|-------------------|----------|
| ArduinoDroid | Free (ads) / Paid | Low | N/A (IDE, not automation) | No | Arduino development on mobile |
| Tasker | ~$3.49 (one-time) | High | 30+ categories | Yes (via plugin) | Complex automation, scripting, power users |
| MacroDroid | Free (5 macros) / Pro | Low | 20+ categories | Limited (shell only) | Simple automation, beginners |

---

## See Also

- [mobile/termux-setup.md](termux-setup.md) - Termux installation, setup, and package management
- [automation/workflow-automation.md](../automation/workflow-automation.md) - General workflow automation tools and strategies
- [iot/arduino.md](../iot/arduino.md) - Arduino development and IoT projects
