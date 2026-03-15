# ESP32 Offensive Security Firmware

Three major open-source firmware projects that turn ESP32 microcontrollers into WiFi/Bluetooth security testing tools. All require authorized access to networks you are testing.

> **Legal notice:** Using these tools against networks or devices without explicit authorization is illegal. These tools are for authorized penetration testing, CTF challenges, and security research on networks you own or have permission to test.

---

## Table of Contents
1. [Hardware Overview](#1-hardware-overview)
2. [ESP32 Marauder](#2-esp32-marauder)
3. [Bruce Firmware](#3-bruce-firmware)
4. [GhostESP](#4-ghostesp)
5. [Firmware Comparison](#5-firmware-comparison)
6. [Flashing Guide](#6-flashing-guide)
7. [Compatible Hardware](#7-compatible-hardware)

---

## 1. Hardware Overview

These firmwares run on ESP32-based hardware. The ESP32 has built-in 802.11 b/g/n WiFi and Bluetooth 4.2/BLE — making it ideal for wireless security tools at minimal cost.

```
Core attack capabilities of ESP32 WiFi:
  Monitor mode:  Passively capture all 802.11 frames in range
  Packet inject: Craft and inject arbitrary 802.11 frames
  Promiscuous:   See all WiFi traffic, not just packets addressed to you

What you can do with this:
  Deauthentication attacks: send forged deauth frames → kick clients off AP
  PMKID capture:            capture PMKID from beacon/probe frames → offline crack
  EAPOL capture:            capture WPA2 4-way handshake → offline crack with Hashcat
  Evil Portal:              fake captive portal to capture credentials
  Beacon spam:              flood airspace with fake SSIDs
  Wardriving:               log APs + GPS coordinates to SD card

What ESP32 cannot do:
  5 GHz WiFi (ESP32-C5 supports it, but most boards are 2.4 GHz only)
  WPA3 cracking (not yet practical)
  Active MitM without additional hardware
```

---

## 2. ESP32 Marauder

- **Repository:** https://github.com/justcallmekoko/ESP32Marauder
- **Author:** JustCallMeKoko
- **License:** GPL v3
- **Stars:** 10k+
- **Website:** https://marauder.justcallmekoko.com

### Overview

ESP32 Marauder is the original and most established ESP32 security firmware. It provides a comprehensive suite of WiFi and Bluetooth offensive and defensive tools, accessible via a touchscreen UI, serial CLI, or Flipper Zero companion app.

### Features

**WiFi Attack:**
```
Scan APs:        Discover all nearby WiFi networks + clients
Scan Stations:   List connected clients per AP
Deauth:          Continuously send deauthentication frames to AP or client
Beacon Spam:     Flood airspace with up to 100 fake SSIDs (rickroll, custom names)
PMKID Attack:    Capture PMKID without associating to AP → crack offline
EAPOL Sniff:     Capture WPA2 handshakes → export .pcap for Hashcat
Evil Portal:     Spawn fake captive portal AP → log submitted credentials
Probe Attack:    Send probe requests for saved networks → reveal hidden SSIDs
WPS Scan:        Identify APs with WPS enabled
Packet Monitor:  Live display of WiFi frame types and counts
```

**Bluetooth:**
```
BT Scan:         Classic Bluetooth device scan
BLE Scan:        Bluetooth Low Energy scan (show device names, MACs, RSSI)
BLE Spam:        Spam BLE advertisement packets
  Modes: Apple devices (popup spam), Samsung, Google Fast Pair, Windows Swift Pair
Sour Apple:      Specific Apple device notification flood
```

**Capture & Logging:**
```
SD card logging: Save pcap captures, wardrive logs, portal creds to microSD
GPS integration: Log AP locations with GPS coordinates (optional GPS module)
Wardrive:        Combine WiFi scan + GPS → produce WiGLE-compatible CSV
Export pcap:     Compatible with Wireshark for offline analysis
```

**Serial CLI (Marauder commands):**
```
scanap           Scan for APs
scansta          Scan for connected stations
attack -t deauth -i AP_INDEX    Deauth attack on specific AP
attack -t beacon                Beacon spam
attack -t pmkid -i AP_INDEX     PMKID capture
capture eapol                   Capture handshakes
list -t ap                      List scanned APs
select -t ap -i 0               Select AP by index
stopscan                        Stop current scan
stopattack                      Stop current attack
```

### Flipper Zero Integration

Marauder runs on the Flipper Zero WiFi Dev Board (ESP32-S2 based). The Flipper acts as a controller — the ESP32 handles all WiFi operations while Flipper provides UI and saves captures to its SD card.

```
Setup:
  1. Flash Marauder firmware to Flipper WiFi Dev Board
  2. Install Marauder companion .fap to Flipper
  3. Connect Dev Board to Flipper GPIO pins
  4. Control via Flipper screen: Apps → GPIO → [ESP32] WiFi Marauder
```

---

## 3. Bruce Firmware

- **Repository:** https://github.com/BruceDevices/firmware
- **Website:** https://bruce.computer
- **License:** AGPL v3
- **Stars:** 5k+
- **Focus:** Red team operations, broader feature set than Marauder

### Overview

Bruce is described as "Predatory ESP32 Firmware" designed for red team operations. It supports a wider range of hardware than Marauder (M5Stack, LilyGo, Cardputer, CYD) and includes RF, RFID, and additional modules beyond WiFi/BT. Born from the observation that Flipper Zero's functionality could be replicated on cheaper ESP32 hardware.

### Features

**WiFi:**
```
Evil Portal:     Fake captive portal with credential logging
Deauth Attack:   Deauthentication frames
EAPOL Capture:   WPA2 handshake capture → pcap
Beacon Spam:     Custom SSID flood
AP Scanner:      Network discovery with signal strength
Wardriving:      GPS-tagged AP logging
WPS Scan:        WPS-enabled AP detection
PMKID Capture:   Offline crack prep
Probe Sniffer:   Capture probe requests
Sniff RAW:       Raw 802.11 frame capture
```

**Bluetooth:**
```
BLE Scan:        BLE device discovery
BLE Spam:        Apple/Android/Windows notification attacks
BT Classic Scan: Classic Bluetooth discovery
```

**Sub-GHz RF (with CC1101 module):**
```
RF Frequency Analyzer: Scan for radio signals across bands
RF Signal Record:      Record and replay RF signals (garage doors, remotes)
Jammer:               Jamming (use only on your own equipment)
Supported: 315, 433, 868, 915 MHz bands
```

**RFID (with PN532/RC522):**
```
RFID Read:       Read 125kHz / 13.56MHz (NFC) cards
RFID Emulate:    Emulate saved cards
NFC Read:        ISO14443A/B card reading
```

**BadUSB:**
```
Run DuckyScript payloads when connected to a computer
When connected via USB: Bruce acts as a keyboard HID
Executes scripts stored on SD card
```

**Other:**
```
IR Transceiver:  Record and replay infrared signals (TV remotes, AC)
TCP/UDP Client:  Connect to remote hosts over WiFi
Port Scanner:    Basic network port scanning
SSH Client:      Connect to SSH servers from the device
Dial Protocol:   Cast content to Chromecast, smart TVs
JS Interpreter:  Run JavaScript scripts on device
SD Card Browser: Browse and manage SD card files
```

### Flashing Bruce

```bash
# Via esptool.py (command line)
pip install esptool
esptool.py --port /dev/ttyACM0 write_flash 0x00000 Bruce-CardputerV2.bin

# Via M5Burner tool (GUI, no command line):
# Download M5Burner → search "Bruce" → select your device → Burn

# Via web flasher: https://bruce.computer/flasher
# Use Chrome (requires WebSerial API)
```

---

## 4. GhostESP

- **Repository:** https://github.com/Spooks4576/Ghost_ESP
- **Revival fork:** https://github.com/GhostESP-Revival/GhostESP
- **Website:** https://ghostesp.net
- **License:** Open source
- **Framework:** ESP-IDF (not Arduino)

### Overview

GhostESP is built on the ESP-IDF framework (not Arduino), giving it lower-level hardware access and better performance. It focuses on WiFi and BLE testing with a clean web UI accessible over the device's own AP — you connect to GhostESP's WiFi hotspot, then control it via browser.

### Features

```
WiFi:
  AP Scan:          List nearby networks with signal, channel, encryption
  Station Scan:     List clients connected to nearby APs
  Deauth Attack:    Targeted or broadcast deauthentication
  Beacon Spam:      Custom SSID flood
  Evil Portal:      Online and offline modes; credential capture
  EAPOL Capture:    WPA2 handshake sniffing
  Probe Sniffer:    Log hidden SSID probes from nearby devices
  Packet Capture:   Raw frame capture to pcap

BLE:
  BLE Scan:         Device discovery with name, RSSI, service UUIDs
  BLE Spam:         Apple/Samsung/Google notification floods
  BLE Sniffer:      Passive BLE advertisement capture

Web UI:
  Connect to GhostESP-XXXXXX AP
  Open 192.168.4.1 in browser
  Full control from phone or laptop — no serial cable needed
  Real-time output, settings save to device
  Qt6-based desktop control app also available

Other:
  Dial Connect:     Cast to Chromecast/smart TVs
  GPS Wardriving:   Log APs with coordinates (GPS module required)
  Flappy Ghost:     Built-in game (on screen-equipped devices)
  SD Card:          Save captures and logs (device-dependent)
```

### GhostESP vs Original vs Revival

```
Original (Spooks4576/Ghost_ESP):
  Original implementation, Arduino + ESP-IDF hybrid
  
GhostESP Revival (GhostESP-Revival/GhostESP):
  Community continuation of GhostESP
  Full ESP-IDF rewrite
  Active development, newer features
  Use this one for current development
```

---

## 5. Firmware Comparison

| Feature | Marauder | Bruce | GhostESP |
|---------|---------|-------|---------|
| **Maturity** | Most mature | Active dev | Active dev |
| **Stars** | 10k+ | 5k+ | 3k+ |
| **Framework** | Arduino | Arduino | ESP-IDF |
| **Flipper Zero** | ✅ Official support | Limited | ✅ |
| **RF (Sub-GHz)** | ❌ | ✅ (CC1101) | ❌ |
| **RFID** | ❌ | ✅ (PN532) | ❌ |
| **IR** | ❌ | ✅ | ❌ |
| **BadUSB** | ❌ | ✅ | ❌ |
| **Web UI** | ❌ (serial CLI) | ❌ (device UI) | ✅ (browser control) |
| **Evil Portal** | ✅ | ✅ | ✅ |
| **BLE Spam** | ✅ | ✅ | ✅ |
| **GPS Wardriving** | ✅ | ✅ | ✅ |
| **EAPOL Capture** | ✅ | ✅ | ✅ |
| **Best hardware** | AWOK / Marauder boards | M5Stack / LilyGo | Any ESP32 |
| **5 GHz** | ESP32-C5 only | ESP32-C5 only | ESP32-C5 only |

---

## 6. Flashing Guide

### esptool.py (Universal)

```bash
pip install esptool

# Put ESP32 in bootloader mode:
# Hold BOOT button → plug USB → release BOOT (after 3 seconds)

# Flash single bin (if firmware is combined):
esptool.py --port /dev/ttyUSB0 --baud 921600 write_flash 0x0 firmware_combined.bin

# Flash separate bins (Marauder):
esptool.py --port /dev/ttyUSB0 --baud 921600 write_flash \
  0x1000  bootloader.bin \
  0x8000  partitions.bin \
  0x10000 firmware.bin

# Windows: replace /dev/ttyUSB0 with COM3 (or whatever port)
# macOS: /dev/cu.usbserial-XXXX

# Verify flash:
esptool.py --port /dev/ttyUSB0 flash_id    # Shows chip info

# Erase flash (start clean):
esptool.py --port /dev/ttyUSB0 erase_flash
```

### Web Flashers (No tools needed — Chrome only)

```
Marauder: https://github.com/justcallmekoko/ESP32Marauder (Spacehuhn Web Updater link in README)
Bruce:    https://bruce.computer/flasher
GhostESP: ghostesp.net → Flash
```

### OTA Update (After initial flash)

```
Bruce:    Device UI → Settings → OTA Update → connects to WiFi, downloads latest
GhostESP: Web UI → Settings → OTA
Marauder: SD card update: put update.bin on SD as /update.bin → device prompts on boot
```

---

## 7. Compatible Hardware

### Dedicated Marauder Hardware (AWOK / JustCallMeKoko)

```
Marauder Mini:    Small form factor, GPS, LiPo, 1.44" screen, 5-way joystick
Marauder v6/v7:  Full-size, SD card, optional GPS, touchscreen
Flipper Dev Board: ESP32-S2 board for Flipper Zero GPIO
Dev Board Pro:   Enhanced Flipper Zero module with screen
```

### M5Stack (Bruce + others)

```
M5Stack Cardputer: Small keyboard + screen + ESP32-S3. Best all-in-one Bruce device.
M5StickC Plus2:   Pocket-sized, screen, battery
M5Stack Core:     Larger, 3 programmable buttons, bigger display
```

### LilyGo Devices (see lilygo-devices.md)

```
T-Deck:     Full keyboard + large screen + ESP32-S3. Bruce/Marauder/GhostESP.
T-Embed:    ESP32-S3 + rotary encoder + display. Bruce/GhostESP.
T-Watch:    Watch form factor. Bruce support.
```

### DIY / Generic Boards

```
Any ESP32/ESP32-S2/ESP32-S3/ESP32-C3/ESP32-C5 devkit
Cheap Yellow Display (CYD): ESP32 + 2.8" touchscreen, ~$10 on AliExpress
  Marauder CYD fork: https://github.com/Fr4nkFletcher/ESP32-Marauder-Cheap-Yellow-Display
```

---

## See Also

- [Flipper Zero](flipper-zero.md) — Multi-tool device that pairs with Marauder/GhostESP
- [LilyGo Devices](lilygo-devices.md) — T-Deck, T-Embed hardware overview
- [ESP32](esp32.md) — ESP32 fundamentals, pinouts, programming
- [Network Analysis](../security/network-analysis.md) — Zeek for analyzing captured traffic
- [Penetration Testing Tools](../security/penetration-testing-tools.md) — Hashcat for cracking captures
