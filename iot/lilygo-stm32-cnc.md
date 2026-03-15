# LilyGo Devices, STM32 & CNC

Hardware reference for LilyGo ESP32-based development boards, STM32 microcontrollers, and CNC machine control systems.

---

## Table of Contents
1. [LilyGo T-Deck](#1-lilygo-t-deck)
2. [LilyGo T-Embed](#2-lilygo-t-embed)
3. [Other LilyGo Boards](#3-other-lilygo-boards)
4. [STM32](#4-stm32)
5. [CNC — Computer Numerical Control](#5-cnc--computer-numerical-control)

---

## 1. LilyGo T-Deck

- **Buy:** https://lilygo.cc/products/t-deck
- **Chip:** ESP32-S3 (dual-core Xtensa LX7 @ 240 MHz, WiFi+BT)
- **Price:** ~$30–45
- **Form factor:** Blackberry-style full keyboard + screen

### Hardware Specs

```
MCU:          ESP32-S3R8 (8MB PSRAM, 16MB Flash)
Display:      2.8" IPS TFT, 320×240, SPI interface
Keyboard:     Full QWERTY mechanical keyboard (42 keys)
Touchpad:     Optical trackpad (like laptop touchpad, miniature)
LoRa:         Optional SX1262 LoRa module (868/915 MHz)
Microphone:   PDM MEMS microphone
Speaker:      I2S DAC + speaker
MicroSD:      SD card slot (SPI)
Battery:      JST connector for LiPo (1200 mAh bundled)
USB:          USB-C (USB Serial/JTAG)
Antenna:      2.4 GHz ceramic antenna (WiFi/BT) + U.FL for LoRa
```

### Firmware Options

```
MicroPython:
  Good for scripting and quick prototyping
  T-Deck has display + keyboard → natural REPL terminal
  Flash: esptool.py + MicroPython T-Deck firmware from micropython.org

Bruce Firmware:
  Full offensive security toolkit (see offensive-firmware.md)
  Flash Bruce-TDeck.bin via esptool.py
  Best all-in-one security tool on T-Deck hardware

ESP32 Marauder T-Deck:
  Community fork: https://github.com/jstockdale/ESP32Marauder-T-Deck
  Alpha quality — functional but less stable than Bruce

Custom Arduino / ESP-IDF:
  Board support: https://github.com/Xinyuan-LilyGO/T-Deck
  Arduino: select "ESP32S3 Dev Module" with PSRAM enabled
  Good for: custom tools, SSH client, network scanner
```

### Programming T-Deck

```cpp
// Display (ST7789 via LVGL)
#define TFT_CS    12
#define TFT_DC    11
#define TFT_RST   -1
#define TFT_SCLK  40
#define TFT_MOSI  41

// Keyboard (I2C)
#define KEYBOARD_ADDR 0x55
#define I2C_SDA       18
#define I2C_SCL       8

// Trackpad (I2C, same bus)
#define TRACKPAD_ADDR 0x15

// Read keyboard input
Wire.beginTransmission(KEYBOARD_ADDR);
Wire.requestFrom(KEYBOARD_ADDR, 1);
if (Wire.available()) {
    char key = Wire.read();
    if (key != 0) Serial.print(key);
}
```

---

## 2. LilyGo T-Embed

- **Buy:** https://lilygo.cc/products/t-embed
- **Variants:** T-Embed (base), T-Embed CC1101 (adds Sub-GHz radio)
- **Chip:** ESP32-S3
- **Form factor:** Cylindrical device with rotary encoder + round display

### Hardware Specs

```
MCU:        ESP32-S3R8 (8MB PSRAM, 16MB Flash)
Display:    1.9" ST7789 TFT, 170×320 (rotated = 320×170 landscape)
            OR round display variant (GC9A01)
Input:      Rotary encoder with push button
Audio:      I2S DAC + speaker
RGB LED:    WS2812B addressable LED strip
MicroSD:    SD card slot
Battery:    JST LiPo connector + charging IC
USB-C:      Programming and power

T-Embed CC1101 variant adds:
  CC1101 Sub-GHz transceiver module (315/433/868/915 MHz)
  Enables RF signal capture/replay (like Flipper Zero Sub-GHz)
```

### Firmware Options

```
Bruce Firmware (recommended for security use):
  Full feature set including RF if CC1101 variant
  Flash: esptool.py write_flash 0x0 Bruce-TEmbed.bin
  
  With CC1101: Sub-GHz record/replay, frequency analyzer
  Without CC1101: WiFi/BT attacks, BadUSB, wardriving

GhostESP:
  Flash GhostESP T-Embed build
  WiFi/BLE testing with web UI control

Stock firmware:
  LilyGo provides basic demo firmware
  Not useful for security testing — use Bruce or GhostESP
```

### T-Embed vs T-Deck

| Feature | T-Embed | T-Deck |
|---------|---------|--------|
| Keyboard | ❌ | ✅ Full QWERTY |
| Touchpad | ❌ | ✅ Optical |
| Input | Rotary encoder | Full keyboard + touchpad |
| Display | 1.9" small | 2.8" larger |
| Sub-GHz | CC1101 variant | LoRa variant |
| Size | Small/cylinder | Blackberry-style |
| Best for | Portable tools | Development terminal |

---

## 3. Other LilyGo Boards

```
T-Watch S3:
  Smartwatch form factor, ESP32-S3
  Round display, touchscreen, IMU (accelerometer)
  Bruce firmware support
  Use case: covert security tool, wearable sensor

T-Beam:
  ESP32 + LoRa (SX1262) + GPS + 18650 battery holder
  Designed for Meshtastic (LoRa mesh network)
  Use case: off-grid communication, GPS tracker, wardriving with GPS

T-Display S3:
  ESP32-S3 + 1.9" color display
  No keyboard, but programmable and cheap
  Popular for: dashboards, smart displays

T-SIM7670:
  ESP32 + 4G LTE modem
  Cellular connectivity for IoT
  
T-PCIE:
  ESP32 + mini PCIe slot for modems
  
Shopping:
  Official: https://lilygo.cc
  AliExpress: search "LilyGo" — same hardware, often cheaper, longer shipping
  Amazon: faster shipping, higher price
```

---

## 4. STM32

STM32 is STMicroelectronics' family of 32-bit ARM Cortex-M microcontrollers. The workhorse of professional embedded development — used in industrial, medical, automotive, and consumer electronics.

### STM32 Family Overview

```
Series      Core           Speed    Flash    RAM     Use Case
─────────────────────────────────────────────────────────────────
STM32F0     Cortex-M0      48 MHz   16–256KB 4–32KB  Ultra-low-cost
STM32F1     Cortex-M3      72 MHz   16KB–1MB 6–96KB  Legacy workhorse
STM32F2     Cortex-M3      120 MHz  128KB–1MB 16–128KB Connectivity
STM32F4     Cortex-M4+FPU  168 MHz  512KB–2MB 64–384KB Most popular series
STM32F7     Cortex-M7+FPU  216 MHz  256KB–2MB 256KB–512KB High performance
STM32H7     Cortex-M7      480 MHz  128KB–2MB 1MB    Maximum performance
STM32L0     Cortex-M0+     32 MHz   8–192KB  1.5–20KB Ultra-low power
STM32L4     Cortex-M4      80 MHz   64KB–2MB 32–640KB Low power + performance
STM32G0     Cortex-M0+     64 MHz   16–512KB 8–144KB Cost-sensitive
STM32G4     Cortex-M4      170 MHz  32KB–512KB 22–128KB Advanced analog
STM32WB     Cortex-M4+M0   64 MHz   256KB–1MB 256KB  BLE 5.0 (Flipper Zero!)
STM32WL     Cortex-M4+M0   48 MHz   64–256KB 20–64KB LoRa wireless
```

### Popular Development Boards

```
Blue Pill (STM32F103C8T6):
  The "Arduino of STM32" — cheapest way to learn STM32
  ~$2 on AliExpress
  72 MHz Cortex-M3, 64KB Flash, 20KB RAM
  Fully Arduino IDE compatible with STM32duino
  
Nucleo boards (ST official):
  Nucleo-32, Nucleo-64, Nucleo-144 (different connector sizes)
  Onboard ST-LINK/V2 debugger (no separate programmer needed)
  Best for professional development
  
STM32 Discovery boards:
  Evaluation boards with displays, audio, sensors pre-installed
  STM32F429I-DISC1: 240×320 LCD, gyroscope, accelerometer
  
WeAct Studio boards:
  BlackPill (STM32F411 / STM32F401): better Blue Pill replacement
  USB DFU bootloader, better clock, USB HID support
  
Flipper Zero (STM32WB55):
  Uses STM32WB for its dual-core BLE+application architecture
  (See flipper-zero.md)
```

### Programming STM32

```bash
# Arduino IDE (easiest start)
# Install STM32duino: Boards Manager → search "STM32" → install
# Board: STM32 Boards → Generic STM32F1 series (for Blue Pill)

# STM32CubeIDE (ST's official IDE, free)
# Based on Eclipse + ST's HAL libraries
# Best for: professional development, CubeMX code generation
# Download: https://www.st.com/en/development-tools/stm32cubeide.html

# PlatformIO (VS Code + CLI)
# platformio.ini:
# [env:genericSTM32F103C8]
# platform = ststm32
# board = genericSTM32F103C8
# framework = arduino

# Flashing methods:
# 1. ST-LINK/V2 (SWD): fast, reliable, enables debugging
#    stlink-tools: st-flash write firmware.bin 0x08000000
#    OpenOCD: openocd -f interface/stlink.cfg -f target/stm32f1x.cfg

# 2. USB DFU bootloader (WeAct/BlackPill boards):
#    Hold BOOT0 button → connect USB → dfu-util
#    dfu-util -a 0 -s 0x08000000:leave -D firmware.bin

# 3. UART bootloader (Blue Pill):
#    BOOT0 pin HIGH → TX/RX to USB-UART adapter
#    stm32flash -w firmware.bin -v /dev/ttyUSB0
```

### STM32 HAL Example (Blink)

```c
#include "main.h"

int main(void) {
    HAL_Init();
    SystemClock_Config();
    
    // Enable GPIOC clock
    __HAL_RCC_GPIOC_CLK_ENABLE();
    
    // Configure PC13 (Blue Pill LED) as output
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
    
    while (1) {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
        HAL_Delay(500);
    }
}
```

### STM32 vs ESP32 vs Arduino

| Feature | STM32 | ESP32 | Arduino Uno |
|---------|-------|-------|------------|
| Core | ARM Cortex-M | Xtensa/RISC-V | AVR 8-bit |
| Speed | 48–480 MHz | 240 MHz | 16 MHz |
| WiFi | Some (STM32W) | ✅ Built-in | ❌ |
| BLE | Some (STM32WB) | ✅ Built-in | ❌ |
| Debugging | SWD/JTAG | JTAG/OpenOCD | Limited |
| ADC | 12–16 bit | 12 bit (noisy) | 10 bit |
| Professional use | ✅ | Maker/IoT | Educational |
| Price | $2–$20 | $2–$15 | $3–$25 |

---

## 5. CNC — Computer Numerical Control

CNC machines execute pre-programmed sequences to control machine tools — mills, routers, lathes, laser cutters, plasma cutters, 3D printers. The machine reads G-code instructions to move along X/Y/Z axes with precision.

### G-code Basics

```gcode
; G-code is the language CNC machines and 3D printers use
; Lines beginning with ; are comments

G28          ; Home all axes (move to endstops)
G21          ; Set units to millimeters
G90          ; Absolute positioning mode

G0 X10 Y10   ; Rapid move to X=10, Y=10 (no cutting)
G1 X50 Y50 F500  ; Linear move to X=50, Y=50 at feed rate 500 mm/min
G2 X10 Y10 I5 J0 F300  ; Arc clockwise
G3 X10 Y10 I5 J0 F300  ; Arc counterclockwise

M3 S1000     ; Spindle ON, clockwise, 1000 RPM
M5           ; Spindle OFF
M8           ; Coolant ON
M9           ; Coolant OFF
M0           ; Pause (wait for operator)
M2           ; End program

; Tool change
T1 M6        ; Select tool 1, execute change
G43 H1       ; Apply tool length offset for tool 1

; Coordinate systems
G54          ; Work Coordinate System 1 (most common)
G92 X0 Y0 Z0 ; Set current position as origin

; Common patterns:
; Drill cycle:
G81 Z-5 R2 F100   ; Drill at current XY, 5mm deep, retract 2mm
G80               ; Cancel drill cycle
```

### CNC Controller Software

```
GRBL (Arduino/STM32 based):
  Open-source G-code interpreter for 3-axis CNC
  Runs on Arduino Uno/Mega or dedicated GRBL boards
  Repository: https://github.com/grbl/grbl
  
  Hardware: Arduino + CNC shield + stepper drivers (A4988/DRV8825)
  Configure: $$ command to see all settings
  Important settings:
    $100=800  ; X steps/mm (depends on your stepper + leadscrew)
    $101=800  ; Y steps/mm
    $102=800  ; Z steps/mm
    $110=500  ; X max rate mm/min
    $120=10   ; X acceleration mm/sec^2
    $21=1     ; Hard limits enable
    $22=1     ; Homing cycle enable

LinuxCNC:
  Full-featured CNC control for complex machines
  Runs on Linux (typically Ubuntu + RTAI/Preempt-RT kernel)
  Supports: mills, lathes, plasma, laser, robots
  Good for: professional/industrial use
  
Marlin:
  Primarily for 3D printers but supports CNC routing
  Huge community, extensive configuration

FluidNC:
  Modern GRBL replacement for ESP32
  WiFi-based control, web UI
  Supports more axes than GRBL
```

### CNC CAM Software (Design → G-code)

```
Free:
  FreeCAD (Path workbench): full parametric CAD + CAM
  Fusion 360 (free for personal use): industry standard, excellent CAM
  Inkscape + gcodetools plugin: convert SVG paths to G-code (2D)
  EstlCAM: simple, cheap, good for hobbyists

Commercial:
  Mastercam: industry standard for production machining
  SolidCAM: integrates with SolidWorks
  HSMWorks: Autodesk CAM in SolidWorks

Workflow:
  1. Create part geometry (FreeCAD, Fusion 360, Inkscape)
  2. Define toolpaths (pocket, contour, drill, adaptive clearing)
  3. Post-process to G-code for your specific controller
  4. Simulate (verify no crashes before cutting)
  5. Send to machine (Universal G-code Sender, CNCjs, Candle)
```

### Common CNC Machine Types

```
CNC Router (wood/plastic/soft metal):
  Working volume: 300×300mm to 1500×3000mm
  Spindle: 300W–3.5kW
  Popular DIY: 3018 Pro (~$80), Sainsmart Genmitsu, Shapeoko, X-Carve
  
CNC Mill (metal):
  Hard materials: aluminum, steel, titanium
  Higher rigidity required, slower speeds
  Benchtop: Grizzly G0704, LittleMachine Shop mills
  
Laser Cutter:
  CO2 laser (wood, acrylic, leather): 40W–150W
  Diode laser (wood, leather, some metals): 5W–80W
  Popular: xTool, Sculpfun, K40
  Software: LightBurn (best for laser, ~$60)
  
3D Printer (FDM):
  Extruder + heated bed instead of spindle
  Uses Marlin/Klipper G-code variant
  Popular: Bambu Lab, Prusa, Voron (DIY)
  
Plasma Cutter:
  Metal cutting with plasma torch
  Requires THC (Torch Height Control)
  LinuxCNC recommended for plasma
```

---

## See Also

- [ESP32 Offensive Firmware](offensive-firmware.md) — Bruce, Marauder, GhostESP for T-Deck/T-Embed
- [ESP32](esp32.md) — ESP32 architecture, GPIO, programming
- [Arduino](arduino.md) — Arduino platform (many CNC controllers run Arduino-based firmware)
- [Flipper Zero](flipper-zero.md) — Contains STM32WB55 as main MCU
