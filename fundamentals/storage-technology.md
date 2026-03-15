# Storage & Interface Technology

How data storage and transfer hardware actually works — from the electrons in NAND flash cells to the signaling protocols on USB and Thunderbolt cables.

---

## Table of Contents
1. [NAND Flash Memory — How It Works](#1-nand-flash-memory--how-it-works)
2. [SD Cards — Technology & Specs](#2-sd-cards--technology--specs)
3. [USB Flash Drives (Pendrives)](#3-usb-flash-drives-pendrives)
4. [RAM — How It Works](#4-ram--how-it-works)
5. [USB — Complete Protocol Guide](#5-usb--complete-protocol-guide)
6. [Thunderbolt](#6-thunderbolt)
7. [NVMe SSD](#7-nvme-ssd)
8. [Storage Interface Comparison](#8-storage-interface-comparison)

---

## 1. NAND Flash Memory — How It Works

NAND flash stores data without power by trapping electrons in a floating gate transistor — a modification of the standard MOSFET.

### Floating Gate Transistor

```
Standard MOSFET:
  Gate → Control Gate
  Oxide → Thin gate oxide
  Channel → Source → Drain

Flash MOSFET (adds floating gate):
  Control Gate (connected to circuitry)
  ───────────────────────────
  Thin oxide (tunnel oxide ~8nm)
  ───────────────────────────
  Floating Gate (electrically isolated — trapped electrons stay here)
  ───────────────────────────
  Tunnel oxide (~10nm)
  ───────────────────────────
  Channel (Source → Drain)

Floating gate is surrounded by insulating oxide on ALL sides.
Electrons can only enter/exit by quantum tunneling — requires high voltage.
```

### Writing and Erasing

```
Writing (programming a 0):
  Apply high voltage (~15–20V) to Control Gate
  Electric field forces electrons to tunnel through oxide → into Floating Gate
  Electrons trapped there → raises threshold voltage (Vt) of transistor
  High Vt → harder to turn on → cell reads as "0"

Erasing (restoring to 1):
  Apply high voltage to substrate (or negative voltage to Control Gate)
  Forces electrons to tunnel back OUT of Floating Gate
  Low Vt → easy to turn on → cell reads as "1"

Reading:
  Apply small read voltage to Control Gate (between low Vt and high Vt)
  Cell with no electrons (Vt low): transistor turns ON → current flows → "1"
  Cell with electrons (Vt high):  transistor stays OFF → no current → "0"

Critical constraint: CAN'T write 0→1 directly on a cell.
  Must ERASE (set all bits to 1) an entire BLOCK first, then WRITE (set individual bits to 0).
  This is why flash wears out: each erase cycle degrades the tunnel oxide.
  Typical endurance: SLC=100K, MLC=10K, TLC=3K, QLC=1K erase cycles.
```

### SLC / MLC / TLC / QLC

```
Traditional (SLC — Single Level Cell):
  1 bit per cell: 2 voltage levels (0 or 1)
  Simple, fast, durable (100K P/E cycles)
  Used in: industrial flash, embedded systems, high-end SSDs (cache)
  
MLC (Multi Level Cell):
  2 bits per cell: 4 voltage levels (00, 01, 10, 11)
  More complex threshold sensing → slower, less durable (10K P/E cycles)
  Used in: mid-range SSDs
  
TLC (Triple Level Cell):
  3 bits per cell: 8 voltage levels
  Slower, less durable (3K P/E cycles), cheaper per bit
  Used in: consumer SSDs, most SD cards, most USB drives
  
QLC (Quad Level Cell):
  4 bits per cell: 16 voltage levels
  Very tight voltage windows → needs sophisticated error correction
  ~1K P/E cycles — writes wear it out quickly
  Used in: high-capacity consumer SSDs, lowest cost
  
pSLC (pseudo-SLC):
  MLC/TLC cells operated in SLC mode (only use 2 of 4/8 voltage levels)
  Faster and more durable than native mode — used for write cache (SLC cache)
  When SLC cache fills: performance drops to native TLC/QLC speed
```

### NAND Architecture

```
Cell → String (32–128 cells in series) → Page → Block → Plane → Die → Package

Page:    Smallest unit that can be READ or WRITTEN (typically 4–16 KB)
Block:   Smallest unit that can be ERASED (typically 256KB–4MB, ~128 pages)
Plane:   Collection of blocks that can be operated in parallel
Die:     Single NAND chip (contains multiple planes)
Package: Stacked dies in one physical chip

Because erase is block-level:
  To modify 1 byte: read entire block → erase block → write modified block back
  This is called a "write amplification" — one user write → many flash writes
  
Flash Translation Layer (FTL):
  Software layer in SSD/SD card controller that manages this:
  - Wear leveling: spread writes evenly across all blocks
  - Garbage collection: reclaim blocks with stale data
  - Write amplification reduction: buffer writes, write full pages
  - Bad block management: mark bad blocks, use spares
  - ECC (Error Correcting Code): correct bit errors (LDPC or BCH)
```

### 3D NAND (V-NAND)

```
Traditional 2D NAND: all cells on one layer → limited by photolithography
3D NAND: stack cells vertically in layers → increase density without smaller feature size

Samsung V-NAND:
  Cells stacked 128–300+ layers high
  Vertical channel through all layers
  Dramatically increases bits/mm²
  Better endurance per bit vs scaled 2D NAND (looser spacing, less interference)
  
Modern SSDs: almost all use 3D NAND (Samsung, SK Hynix, Micron, Kioxia, WD)
```

---

## 2. SD Cards — Technology & Specs

### Physical Layers

```
Full-size SD (24×32mm), microSD (11×15mm), miniSD (21.5×20mm — rare)
All electrically equivalent with adapters.

Contacts: 8 pins on microSD (9 on SD)
  Pin 1: DAT2  (data line 2, for 4-bit mode)
  Pin 2: CD/DAT3 (card detect / data line 3)
  Pin 3: CMD   (command line)
  Pin 4: VDD   (3.3V power)
  Pin 5: CLK   (clock from host)
  Pin 6: GND   (ground)
  Pin 7: DAT0  (data line 0)
  Pin 8: DAT1  (data line 1)
```

### Speed Classes

```
Speed Class rating:       Minimum sustained write speed
  Class 2 (C2):           2 MB/s
  Class 4 (C4):           4 MB/s
  Class 6 (C6):           6 MB/s
  Class 10 (C10):         10 MB/s

UHS Speed Class (U symbol):
  U1:                     10 MB/s minimum write
  U3:                     30 MB/s minimum write ← required for 4K video

Video Speed Class (V symbol):
  V6:    6 MB/s
  V10:   10 MB/s
  V30:   30 MB/s   ← minimum for 4K30
  V60:   60 MB/s   ← for high bitrate 4K/8K
  V90:   90 MB/s   ← professional video

Application Performance Class (A):
  A1: 1500 IOPS read, 500 IOPS write, 10 MB/s sequential
  A2: 4000 IOPS read, 2000 IOPS write, 10 MB/s sequential
  ← Required for running Android apps from SD card

Bus interfaces:
  Default Speed:       25 MB/s max (SPI or 1-bit SD mode)
  High Speed:          50 MB/s max (4-bit mode, 50 MHz)
  UHS-I:               104 MB/s max (4-bit, 104 MHz SDR)
  UHS-II:              312 MB/s max (adds second row of pins, two-lane LVDS)
  UHS-III:             624 MB/s max
  SD Express:          ~985 MB/s (PCIe 3.0 x1 via new pins)
```

### SD Card Capacity Classes

```
SDSC (Standard Capacity):  up to 2 GB   — FAT16 filesystem
SDHC (High Capacity):      2–32 GB      — FAT32 filesystem
SDXC (Extended Capacity):  32GB–2TB     — exFAT filesystem
SDUC (Ultra Capacity):     2–128TB      — exFAT (future)
```

### Why SD Cards Fail

```
1. Write cycle exhaustion:
   TLC NAND: ~3000 P/E cycles per block
   FTL wear leveling extends life but eventually all blocks wear out
   Typical failure: a few years of heavy recording use

2. Fake capacity (counterfeit cards):
   A 256GB fake card physically has 8GB of NAND
   FTL modified to "loop" — writes wrap around, overwriting old data
   Data appears to write but is silently lost
   Test with: H2testw (Windows) or f3write/f3read (Linux/macOS)

3. Data corruption without errors:
   SDcards don't guarantee power-off safety like SSDs
   Removing card mid-write can corrupt filesystem or individual files
   Use proper unmount/eject procedure

4. Contact corrosion:
   Gold contacts can oxidize — clean gently with isopropyl alcohol
```

---

## 3. USB Flash Drives (Pendrives)

A USB flash drive (pendrive, thumb drive) is a NAND flash controller + NAND chips + USB interface chip in a small package.

### Internal Architecture

```
USB-A/C connector
      ↓
USB Controller IC (e.g., Phison PS2251, Silicon Motion SM3281)
  - Implements USB mass storage class (MSC) protocol
  - Contains FTL (Flash Translation Layer)
  - Interfaces to NAND via parallel flash bus
      ↓
NAND Flash chips (1–4 chips, soldered directly)
  - Usually TLC or QLC for cost
  - No DRAM cache on most cheap drives (DRAM-less)
```

### USB Mass Storage Class (MSC) Protocol

```
How your OS communicates with a USB flash drive:

1. USB enumeration (plug in):
   Device sends descriptor → OS identifies as Mass Storage Class
   OS loads USB storage driver (usbstor.sys on Windows)
   Driver presents device as a generic block device

2. SCSI over USB:
   Mass Storage Class uses Bulk-Only Transfer (BOT) protocol
   Commands are SCSI commands wrapped in USB bulk transfers:
   
   Command Block Wrapper (CBW):
     SCSI command: READ(10) — read 8 sectors at LBA 500
   
   Data transport:
     Host reads 8 × 512 = 4096 bytes from device
   
   Command Status Wrapper (CSW):
     Device confirms success/failure

3. OS file system:
   OS reads MBR/GPT → finds partition table
   Mounts FAT32/exFAT/NTFS filesystem
   File access translated to sector reads/writes

Speed reality:
  Cheap 16GB USB 2.0 drive: 5–25 MB/s read, 2–10 MB/s write
  USB 3.0 drive with SLC cache: 100–200 MB/s read, 50–100 MB/s write burst
  USB 3.2 Gen 2 high-end: 400–600 MB/s (Samsung FIT Plus, SanDisk Extreme Pro)
```

### Why Flash Drives Are Slow

```
1. QLC/TLC without DRAM cache: no buffer, writes go directly to slow NAND
2. USB 2.0 theoretical max: 480 Mbps = 60 MB/s (controllers rarely hit this)
3. Small FTL with poor garbage collection → write slowdown over time
4. Bus sharing: if many USB devices on same root hub, bandwidth is shared

Checking real speed:
  Windows: CrystalDiskMark
  Linux:   dd if=/dev/zero of=/dev/sdX bs=4M status=progress
           dd if=/dev/sdX of=/dev/null bs=4M status=progress
```

---

## 4. RAM — How It Works

### DRAM (Dynamic RAM) — Main Memory

DRAM stores each bit as a charge on a tiny capacitor paired with one transistor (1T1C cell). "Dynamic" means it must be refreshed — capacitors leak charge and data is lost without periodic refresh.

```
DRAM cell operation:

Write 1: transistor ON → charge capacitor → store charge
Write 0: transistor ON → drain capacitor → no charge
Read:    transistor ON → sense amplifier detects charge vs no charge
         (reading is destructive — must rewrite after read)

Refresh:
  Every 64ms: memory controller reads every row and rewrites it
  Refresh occupies the bus: during refresh, CPU cannot access RAM
  Modern DRAM: refresh takes ~1–3% of total bandwidth

Address multiplexing:
  DRAM address sent in two halves: Row Address Strobe (RAS), Column Address Strobe (CAS)
  This is why latency is specified as: CL-tRCD-tRP-tRAS
  Example: DDR5-6000 CL30-38-38-96:
    CL=30:   CAS latency = 30 clock cycles (from column address to data)
    tRCD=38: Row-to-Column Delay = 38 cycles (row activation to column access)
    tRP=38:  Row Precharge = 38 cycles (precharge before next row access)
    tRAS=96: Active-to-Precharge = 96 cycles minimum
```

### DDR Generations

```
Generation  Data Rate     Voltage  Bandwidth (single channel)
──────────────────────────────────────────────────────────────
DDR1        200–400 MT/s  2.5V     3.2 GB/s  (DDR-400)
DDR2        400–1066 MT/s 1.8V     8.5 GB/s  (DDR2-1066)
DDR3        800–2133 MT/s 1.5V     17 GB/s   (DDR3-2133)
DDR4        1600–3200 MT/s 1.2V    25.6 GB/s (DDR4-3200)
DDR5        3200–8400 MT/s 1.1V    67.2 GB/s (DDR5-8400)
LPDDR5X    8533 MT/s     0.9V     68.3 GB/s (mobile, e.g. MacBook M-series)

"DDR" = Double Data Rate: data transferred on both rising AND falling edges of clock
DDR5-6000 means 6000 million transfers per second
Bandwidth = transfers/sec × 8 bytes (64-bit bus) = 6000×10⁶ × 8 = 48 GB/s
```

### How RAM Sticks Work

```
DIMM (Dual Inline Memory Module):
  PCB with DRAM chips on one or both sides
  168/184/240/288-pin connectors (DDR1/2/3/4/5 respectively)
  
Each DRAM chip on the stick: 8 or 16 data bits wide
Multiple chips combined: 64-bit total data bus (8 × 8-bit chips = 64 bits)
ECC DIMM: 72-bit bus (9 × 8-bit chips — extra 8 bits for error correction)

Channels:
  Single channel: one 64-bit path to memory controller
  Dual channel:  two 64-bit paths = 128-bit effective bus = 2× bandwidth
  Quad channel:  four paths (Xeon/Threadripper workstations)
  
Install DIMMs in matching slots (A1+B1 for dual channel) for best performance.
Mixing different speed DIMMs: all run at lowest speed.

SPD (Serial Presence Detect):
  Small EEPROM chip on every DIMM
  Contains timing specifications, manufacturer, capacity
  BIOS reads SPD at boot → configures memory controller
  
XMP/EXPO profiles:
  Factory-programmed overclocking profiles in SPD extended data
  XMP (Intel eXtreme Memory Profile) or EXPO (AMD)
  Enable in BIOS to use advertised speed (e.g., DDR5-6000 instead of DDR5-4800 base)
```

### SRAM (Static RAM) — Cache Memory

```
SRAM: 6 transistors per bit (cross-coupled inverters + access transistors)
  No capacitor → no refresh needed → "static"
  Fast: 1–4 cycle access (vs 40–100 for DRAM)
  Expensive: 30–100× cost per bit vs DRAM
  
Used for: CPU L1/L2/L3 cache, register files, microcontroller on-chip memory

Apple M3 Pro L1 cache: 128KB D-cache + 192KB I-cache per P-core (SRAM)
  12 MB L2 cache per cluster (SRAM)
  24 MB shared L3/SLC (SRAM)
  36 GB unified memory (LPDDR5 DRAM)
```

---

## 5. USB — Complete Protocol Guide

### USB Versions & Speeds

```
Version        Marketing Name      Speed          Notes
──────────────────────────────────────────────────────────────────────
USB 1.0/1.1    (USB 1.1)          12 Mbps        Low/Full Speed. Keyboards, mice.
USB 2.0        Hi-Speed USB       480 Mbps       Still used for flash drives, HID
USB 3.0        USB 3.2 Gen 1      5 Gbps         Originally "SuperSpeed", blue ports
USB 3.1        USB 3.2 Gen 2      10 Gbps        SuperSpeed+
USB 3.2        USB 3.2 Gen 2×2    20 Gbps        Dual lane, requires USB-C
USB4 Gen 2×2   USB4 20Gbps        20 Gbps        Uses Thunderbolt 3 protocol
USB4 Gen 3×2   USB4 40Gbps        40 Gbps        Requires Thunderbolt 4 cable
USB 2.0 = 480 Mbps = 60 MB/s theoretical max
USB 3.2 Gen 1 = 5 Gbps = 625 MB/s theoretical max
USB4 40Gbps = 5 GB/s theoretical max
```

### USB Physical Layer

```
USB 2.0 (D+ / D-):
  Differential pair signaling
  D+ and D- carry complementary signals
  Receiver looks at DIFFERENCE between D+ and D-, ignoring common noise
  Signal levels: 0V/3.3V differential → noise immunity

USB 3.x SuperSpeed (SSTX+/SSTX-/SSRX+/SSRX-):
  Separate SuperSpeed TX and RX pairs (full duplex!)
  8b/10b encoding (USB 3.0) or 128b/132b (USB 3.1+)
  Scrambling + LFSR: prevents DC bias, helps with EMI
  
USB-C connector (24 pins):
  Pin A1/B12: GND
  Pin A4/B9:  VBUS (+5V to +20V)
  Pin A5/B5:  CC1/CC2 (Configuration Channel — determines orientation, role)
  Pin A6/B6:  D+ / D-  (USB 2.0)
  Pin A7/B7:  D- / D+  (USB 2.0 — both orientations)
  Pin A8/B8:  SBU1/SBU2 (Sideband Use — alt modes like DisplayPort audio)
  Pin A2/B11: TX1+/TX2+ (SuperSpeed TX differential)
  Pin A3/B10: TX1-/TX2-
  Pin B2/A11: RX2+/RX1+ (SuperSpeed RX differential)
  Pin B3/A10: RX2-/RX1-

Cable flip detection (CC pins):
  When you flip a USB-C cable, CC1 and CC2 swap roles
  Device detects which CC pin is pulled → knows orientation
  No special "right side up" — both orientations work identically
```

### USB Protocol Stack

```
USB Host (computer)                    USB Device (drive, phone)
──────────────────────────────────────────────────────────────────
Application (file system driver)
      ↓
USB Class Driver (Mass Storage, HID, Audio...)
      ↓
USB Core (enumeration, pipe management)
      ↓
USB Host Controller Driver (xHCI for USB 3.x, EHCI for USB 2.0)
      ↓
Host Controller Hardware (Intel USB controller in chipset)
      ↓
USB physical layer (differential signaling on cable)
      ↕  ←  cable
USB physical layer
      ↓
Device Controller Hardware
      ↓
Device Class Firmware (implements Mass Storage: SCSI over USB)
      ↓
Flash controller / application processor
```

### USB Enumeration (Plug and Play)

```
Device plugged in → VBUS present → device waits (default address 0)

1. Host detects device (D+ pull-up for Full Speed, D- for Low Speed)
2. Host resets bus (D+/D- both low for >10ms)
3. Host reads device descriptor at address 0:
   GET_DESCRIPTOR (Device) → returns: USB version, class, subclass, protocols, vendor/product ID
4. Host assigns address: SET_ADDRESS (e.g., 3)
5. Host reads full descriptors:
   GET_DESCRIPTOR (Configuration) → interfaces, endpoints, class-specific descriptors
6. Host loads matching driver (based on VID:PID or class code)
7. Driver claims interface → device ready

Vendor ID (VID): 16-bit, assigned by USB-IF ($5000 for membership)
Product ID (PID): 16-bit, assigned by vendor

Check USB devices on Linux:
  lsusb                 → list all USB devices
  lsusb -v              → verbose (full descriptor dump)
  cat /sys/kernel/debug/usb/devices  → detailed tree
  usbmon (kernel module) → capture raw USB traffic
```

### USB Power Delivery (USB PD)

```
USB baseline power:
  USB 2.0:      5V, 500mA = 2.5W
  USB 3.x:      5V, 900mA = 4.5W (USB 3.0) or 1.5A (USB 3.2)
  USB BC 1.2:   5V, 1.5A = 7.5W (Battery Charging spec, non-PD fast charge)

USB Power Delivery (PD):
  Negotiated over CC pins using PD protocol (BMC encoding, 300 kbps)
  Supports: 5V/9V/15V/20V at up to 5A
  Max: 100W (20V × 5A) — original PD 3.0
  Extended Power Range: 240W (48V × 5A) — PD 3.1 (laptop chargers)
  
  PD negotiation:
    Source advertises: "I can supply 5V/3A, 9V/3A, 20V/3A"
    Sink requests:     "Give me 20V/3A" (60W)
    Source agrees:     switches to 20V output
  
Proprietary fast charging (not USB PD):
  Qualcomm Quick Charge: 9V/12V at up to 3A
  MediaTek Pump Express: similar
  OnePlus VOOC/SuperVOOC: high current (5V/6A, 10V/6.5A)
  Apple Fast Charge: USB PD compliant (9V/2A = 18W minimum)
```

---

## 6. Thunderbolt

Thunderbolt (TB) is Intel's high-speed interface that combines PCIe, DisplayPort, and USB into a single cable — using USB-C connector from TB3 onwards.

### Thunderbolt Versions

```
TB1 (2011): 10 Gbps, Mini DisplayPort connector
TB2 (2013): 20 Gbps, Mini DisplayPort connector
TB3 (2015): 40 Gbps, USB-C connector
             4× PCIe 3.0 lanes + DisplayPort 1.4 + USB 3.1
             Power delivery: up to 100W
             
TB4 (2020): 40 Gbps, USB-C connector
             Same speed as TB3, stricter requirements:
             - Mandatory: 4K @ 60Hz on 2 displays
             - Minimum: 32 GB/s PCIe storage bandwidth
             - USB4 compatible (TB4 cables work with USB4)
             - Daisy chain: up to 6 devices

TB5 (2024): 120 Gbps bidirectional, USB-C connector
             PAM4 signaling (vs NRZ in previous versions)
             Up to 240W power delivery (USB PD 3.1)
             External GPU at full PCIe 4.0 x4 speeds
             Found in: Intel Core Ultra 2 (Lunar Lake), planned for Apple M4
```

### How Thunderbolt Works Internally

```
Thunderbolt architecture:
  Host Thunderbolt controller (in CPU/chipset)
        ↓
  TB cable (active or passive)
        ↓
  Device Thunderbolt controller (in peripheral)
        ↓
  PCIe endpoint (inside the device)

PCIe over Thunderbolt:
  Thunderbolt is a PCIe tunnel — the device appears as a PCIe device to the host
  Same PCIe protocol as a desktop GPU or NVMe SSD plugged in internally
  Latency: slightly higher than direct PCIe (~1–2 μs overhead for encapsulation)
  
DisplayPort over Thunderbolt:
  DisplayPort stream tunneled simultaneously with PCIe
  No performance penalty for running display + storage simultaneously
  
Thunderbolt hub/daisy chain:
  Each TB controller has 2 downstream ports
  Chain up to 6 devices (7 including host)
  Each device gets a "slice" of the 40 Gbps bandwidth
```

### Thunderbolt vs USB4 vs USB 3.x

```
Interface     Speed   Protocol          Cable       Alt Mode
──────────────────────────────────────────────────────────────────────────
USB 3.2 Gen 2   10G   USB               USB-C       DP, HDMI (optional)
USB 3.2 Gen2×2  20G   USB               USB-C       DP, HDMI (optional)
USB4 Gen 2×2    20G   USB + PCIe tunnel USB-C       DP 2.1
USB4 Gen 3×2    40G   USB + PCIe tunnel USB-C       DP 2.1
TB3             40G   PCIe + DP + USB   USB-C (Active cable for 2m+)
TB4             40G   PCIe + DP + USB   USB-C (Active for 2m+)    
TB5            120G   PCIe + DP + USB   USB-C (Active)

Key difference:
  USB4 40Gbps = optionally implements Thunderbolt spec (may not have PCIe tunnel)
  TB4 = ALWAYS has PCIe tunnel, strict certification, guaranteed compatibility
  A TB4 port accepts any USB-C device. A USB4 port may not support TB3 devices.
  
Thunderbolt cables:
  Passive (up to 0.8m): cheaper, works for most uses
  Active (1–2m): more expensive, required for longer runs, has chips in connector
  Only active cables support Thunderbolt at full speed over 0.8m
  Look for Thunderbolt lightning bolt logo on cable/connector
```

### Thunderbolt Security

```
DMA (Direct Memory Access) attack risk:
  Thunderbolt devices get direct PCIe access to system RAM
  A malicious TB device = memory read/write without OS permission
  Traditional cold boot attacks: plug malicious TB device → read entire RAM
  
  This is called "DMA attack" or "Thunderspy" (Björn Ruytenberg, 2020)

Mitigations:
  Thunderbolt Security Levels (in BIOS/UEFI):
    None:        All devices trusted (maximum risk)
    User:        User must approve each new device (default)
    Secure:      Only pre-approved devices (white-list)
    DisplayPort: No PCIe tunneling — only DisplayPort/USB allowed
    No:          Thunderbolt disabled entirely
  
  Kernel DMA protection (Windows 10 v1803+, Linux 5.x+):
    IOMMU restricts what memory each PCIe device can access
    Malicious TB device: only accesses memory it's been assigned
    Requires: IOMMU enabled (Intel VT-d, AMD-Vi in BIOS)
  
  Practical advice:
    Never connect a Thunderbolt device you don't trust
    Enable IOMMU in BIOS
    Use "User" security level minimum
```

---

## 7. NVMe SSD

NVMe (Non-Volatile Memory Express) is the protocol designed specifically for NAND flash storage over PCIe. Replaces SATA which was designed for spinning hard drives.

```
SATA problems for SSD:
  SATA (Serial ATA): designed in 2000 for spinning disks
  Max throughput: 600 MB/s (SATA III)
  Command queue depth: 32 commands
  One command queue — serialized requests

NVMe advantages:
  Direct PCIe connection: bypasses storage controller chipset
  PCIe 4.0 x4: 8 GB/s theoretical bandwidth
  PCIe 5.0 x4: 16 GB/s theoretical bandwidth
  65,535 I/O queues × 65,536 commands each
  → Massively parallel → critical for server workloads

NVMe form factors:
  M.2 2280:    22×80mm card (most common in laptops)
  M.2 2242:    22×42mm (smaller laptops, handheld PCs)
  PCIe x4 card: desktop add-in card (high-capacity/enterprise)
  U.2 / U.3:   2.5" enterprise form factor with PCIe

NVMe protocol:
  Submission Queue (SQ): host writes command entries
  Completion Queue (CQ): device writes completion entries
  Host rings doorbell register → device processes command
  No polling needed — device generates PCIe interrupt when done
  
  Command types:
    Read:  LBA range → data returned in host buffer
    Write: data from host buffer → LBA range on NAND
    Flush: ensure all writes committed to non-volatile media
    Trim/Deallocate: mark LBA range as unused → FTL can garbage collect
```

---

## 8. Storage Interface Comparison

```
Interface    Max Speed     Connector    Protocol    Use Case
─────────────────────────────────────────────────────────────────────────
SATA III     600 MB/s      SATA L       ATA/AHCI    Older SSDs, HDDs
M.2 SATA     600 MB/s      M.2 (SATA)  ATA/AHCI    Budget SSDs (same speed as SATA)
USB 2.0      60 MB/s       USB-A/C     MSC/SCSI    Flash drives, card readers
USB 3.2 G1   625 MB/s      USB-A/C     MSC/SCSI    Fast flash drives
USB 3.2 G2   1250 MB/s     USB-C       MSC/SCSI    High-speed external SSDs
NVMe PCIe3   3500 MB/s     M.2 or PCIe NVMe        Consumer SSDs
NVMe PCIe4   7000 MB/s     M.2 or PCIe NVMe        Current high-end SSDs
NVMe PCIe5   14000 MB/s    M.2 or PCIe NVMe        Cutting-edge (2024+)
Thunderbolt 4 5000 MB/s    USB-C       PCIe tunnel  External NVMe enclosures
SD UHS-I     104 MB/s      SD/microSD  SD protocol  Camera cards
SD UHS-II    312 MB/s      SD (2 rows) SD protocol  Professional cameras
microSD A2   ~100 MB/s seq microSD     SD protocol  Phone storage, Raspberry Pi
```

---

## See Also

- [How a Computer Really Works](how-computers-work.md) — Memory hierarchy in context
- [CPU Architecture](cpu-architecture.md) — DRAM timing, memory controller, caches
- [Linux Internals](linux-internals.md) — Block I/O stack, filesystem layer above storage
- [ESP32](../iot/esp32.md) — ESP32 uses SPI-connected flash for firmware storage
