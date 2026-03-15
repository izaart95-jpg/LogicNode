# How a Computer Really Works — From Electrons to YouTube

**Scenario:** A MacBook with Apple M-series chip opens YouTube in Safari and plays a video with audio. This document traces every physical and computational process that makes this happen — from electrons flowing through silicon to photons leaving the display and pressure waves leaving the speaker.

Nothing is skipped. Every layer is real.

---

## Table of Contents
1. [Layer 0 — Physics: Electrons & Silicon](#layer-0--physics-electrons--silicon)
2. [Layer 1 — Transistors: Switches from Physics](#layer-1--transistors-switches-from-physics)
3. [Layer 2 — Logic Gates: Computation from Switches](#layer-2--logic-gates-computation-from-switches)
4. [Layer 3 — Digital Circuits: Memory, Arithmetic, Clocks](#layer-3--digital-circuits-memory-arithmetic-clocks)
5. [Layer 4 — The CPU Die: Apple M-Series Architecture](#layer-4--the-cpu-die-apple-m-series-architecture)
6. [Layer 5 — Memory: DRAM, Caches & Unified Memory](#layer-5--memory-dram-caches--unified-memory)
7. [Layer 6 — Boot: From Power Button to macOS Desktop](#layer-6--boot-from-power-button-to-macos-desktop)
8. [Layer 7 — The Operating System: macOS & XNU Kernel](#layer-7--the-operating-system-macos--xnu-kernel)
9. [Layer 8 — Networking: WiFi to YouTube's Servers](#layer-8--networking-wifi-to-youtubes-servers)
10. [Layer 9 — TLS & HTTPS: Encrypted Connection](#layer-9--tls--https-encrypted-connection)
11. [Layer 10 — HTTP/3 & QUIC: The Modern Web Transport](#layer-10--http3--quic-the-modern-web-transport)
12. [Layer 11 — DNS: Resolving youtube.com](#layer-11--dns-resolving-youtubecom)
13. [Layer 12 — The Browser Engine: Safari & WebKit](#layer-12--the-browser-engine-safari--webkit)
14. [Layer 13 — Video Delivery: CDN, DASH & Codecs](#layer-13--video-delivery-cdn-dash--codecs)
15. [Layer 14 — Video Decode: H.264/VP9/AV1 on Apple Silicon](#layer-14--video-decode-h264vp9av1-on-apple-silicon)
16. [Layer 15 — The Display Pipeline: GPU to Photons](#layer-15--the-display-pipeline-gpu-to-photons)
17. [Layer 16 — Audio Pipeline: AAC to Pressure Waves](#layer-16--audio-pipeline-aac-to-pressure-waves)
18. [Layer 17 — Power: How the Battery Keeps It All Running](#layer-17--power-how-the-battery-keeps-it-all-running)
19. [The Full Stack: Everything Simultaneously](#the-full-stack-everything-simultaneously)

---

## Layer 0 — Physics: Electrons & Silicon

Everything in a computer ultimately runs on quantum mechanics and electromagnetism. Before there are bits, there are atoms.

### Silicon as a Semiconductor

Silicon (Si) is element 14 — it sits between conductors (copper) and insulators (glass) in the periodic table. Pure silicon conducts electricity poorly. Its usefulness comes from **doping** — adding trace amounts of other elements to precisely control its electrical behavior.

```
Silicon crystal structure:
  Each Si atom has 4 valence electrons
  Forms a lattice where each atom shares electrons with 4 neighbors
  All electrons are tightly bound → poor conductor at room temperature

N-type doping (add phosphorus — 5 valence electrons):
  Extra electron is loosely bound → free to move
  Result: more free electrons → conducts via electrons (negative carriers)
  Donor atoms: P, As, Sb

P-type doping (add boron — 3 valence electrons):
  Missing electron creates a "hole" (positive vacancy)
  Electrons move into holes → holes appear to move in opposite direction
  Result: conducts via holes (positive carriers)
  Acceptor atoms: B, Al, Ga
```

### P-N Junction — The Diode

When P-type and N-type silicon are joined:

```
P side | N side
  ←←←  |  →→→
holes  | electrons

At the junction:
  Electrons from N diffuse into P, fill holes
  Creates a "depletion zone" with no free carriers
  Net charge: P side becomes negative, N side becomes positive
  This charge creates an electric field opposing further diffusion
  → Equilibrium: a built-in potential of ~0.6V forms

Forward bias (+ on P, - on N):
  External voltage opposes built-in field
  Depletion zone shrinks → current flows freely
  → CONDUCTS

Reverse bias (- on P, + on N):
  External voltage reinforces built-in field
  Depletion zone widens → no current
  → INSULATES
```

This is a **diode** — current flows in one direction only. The p-n junction is the physical basis for all transistors.

### Electrons as Information Carriers

```
What "voltage" physically means:
  Voltage = potential energy per unit charge (joules/coulomb)
  1V means each coulomb of charge has 1 joule of potential energy
  Electrons "want" to move from high potential energy to low

What current physically means:
  Current = charge flow rate (coulombs/second = amperes)
  1A = 6.24 × 10^18 electrons passing a point per second

In digital circuits:
  0V (ground, GND) = logic 0
  1.8V (supply, VDD) = logic 1  (Apple M-series uses ~0.7–1.1V)
  The exact threshold: anything < 0.4V = definitely 0
                       anything > 0.8V = definitely 1
                       middle = undefined (avoided by circuit design)

Electron drift velocity (actual physical speed in copper wire):
  Surprisingly slow: ~0.1 mm/s at typical current densities
  But the electric field propagates at ~60–90% of the speed of light
  Analogy: water in a full hose — push one end, flow starts immediately
           even though individual water molecules move slowly
```

---

## Layer 1 — Transistors: Switches from Physics

The MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor) is the fundamental switch. Apple M-series uses 3nm and 5nm MOSFET technology. The M3 chip contains approximately 25 billion transistors.

### MOSFET Structure

```
Cross-section of an NMOS transistor (N-channel MOSFET):

                    GATE (metal/polysilicon)
                        |
         ┌──────────────┼──────────────┐
         │    insulator (SiO₂, ~1nm)   │
─────────┼─────────────────────────────┼─────────
 Source  │         P-type substrate    │  Drain
 (N+)    │                             │  (N+)
         │         channel region      │
─────────┴─────────────────────────────┴─────────

Source: heavily doped N+ region (electrons abundant)
Drain:  heavily doped N+ region (electrons abundant)
Gate:   conductor separated from substrate by thin oxide insulator
Channel: P-type region between source and drain
```

### How the MOSFET Switches

```
GATE = LOW voltage (0V):
  No electric field through oxide
  P-type channel has no free electrons
  No path between Source and Drain
  → Transistor OFF (open circuit)

GATE = HIGH voltage (1.8V):
  Electric field penetrates oxide
  Attracts electrons into channel region
  Creates an N-type "inversion layer" connecting Source to Drain
  → Transistor ON (current flows from Drain to Source)

The oxide is so thin (~1nm in modern chips) that quantum tunneling
occurs — electrons can leak through even in the "off" state.
This is why transistors have static power consumption even when idle.
This is also why chip designers need quantum mechanics, not just classical physics.
```

### 3nm vs 5nm: What "nm" Actually Means

The "3nm" and "5nm" labels are marketing designations, not literal measurements. The actual gate length of modern transistors is typically 6–12nm even in "3nm" processes. The number refers to a transistor density metric (how many transistors per mm²).

```
TSMC N3 (3nm, used in Apple M3):
  Transistor density: ~167 million transistors/mm²
  Gate pitch: ~48nm
  Metal pitch: ~20nm
  Apple M3: 25 billion transistors on ~140mm² die

TSMC N5 (5nm, used in Apple M1/M2):
  Transistor density: ~171 million transistors/mm²
  Apple M1: 16 billion transistors on ~120mm²

For comparison:
  Intel 4004 (1971): 2,300 transistors, 10,000nm (10μm)
  Apple M3 (2023): 25,000,000,000 transistors, ~3nm equivalent
  Scaling: 10 million times more transistors in 52 years
```

### CMOS — Complementary MOS

Real logic gates use **CMOS** — pairs of NMOS and PMOS transistors working complementarily. PMOS transistors turn ON when gate is LOW (opposite of NMOS).

```
CMOS NOT gate (inverter):
  VDD (1.8V)
    │
   PMOS (gate = input)   ← ON when input = 0, passes VDD to output
    │
  ──┼── output
    │
   NMOS (gate = input)   ← ON when input = 1, pulls output to GND
    │
   GND (0V)

When Input = 0:
  PMOS: gate=0 → ON → output connected to VDD → Output = 1
  NMOS: gate=0 → OFF → output not connected to GND
  Output = 1  ✓ (NOT 0 = 1)

When Input = 1:
  PMOS: gate=1 → OFF → VDD disconnected from output
  NMOS: gate=1 → ON → output pulled to GND
  Output = 0  ✓ (NOT 1 = 0)

Key CMOS property:
  In steady state, either PMOS or NMOS is off (never both on)
  → No direct path from VDD to GND → near-zero static current
  → Power only consumed during switching (charging/discharging capacitance)
  → This is why CMOS dominates — it's power-efficient
```

---

## Layer 2 — Logic Gates: Computation from Switches

Every computation a CPU performs — adding numbers, comparing values, controlling flow — reduces to combinations of logic gates, which are combinations of transistors.

### Fundamental Gates

```
NAND gate (2-transistor CMOS, the universal gate):
  A=0, B=0: PMOS both on  → output = 1
  A=0, B=1: one PMOS on   → output = 1
  A=1, B=0: one PMOS on   → output = 1
  A=1, B=1: PMOS both off, NMOS both on → output = 0
  Truth: output = NOT(A AND B)

  Every other gate can be built from NAND alone.
  Intel i7 has billions of gates, most reduce to NAND.

XOR gate (2 inputs, exclusive or — used in adders):
  A=0, B=0: 0
  A=0, B=1: 1
  A=1, B=0: 1
  A=1, B=1: 0
  Sum output in addition (without carry)

AND gate: NAND + NOT
OR gate:  NAND inputs, then NAND outputs
NOT gate: NAND with both inputs tied together
```

### Half Adder — Adding Two Bits

```
Inputs: A, B (1-bit each)
Outputs: Sum, Carry

Sum   = A XOR B      (the result bit)
Carry = A AND B      (the overflow bit)

  A=0, B=0: Sum=0, Carry=0  (0+0=0)
  A=0, B=1: Sum=1, Carry=0  (0+1=1)
  A=1, B=0: Sum=1, Carry=0  (1+0=1)
  A=1, B=1: Sum=0, Carry=1  (1+1=2, which is 10 in binary)
```

### Full Adder — The Building Block of the ALU

```
Inputs: A, B, Cin (carry-in from previous bit)
Outputs: Sum, Cout

Sum  = A XOR B XOR Cin
Cout = (A AND B) OR (Cin AND (A XOR B))

64 full adders chained together = 64-bit integer adder
The chain propagates carry bits from bit 0 to bit 63
"Carry lookahead" adders pre-compute carries in parallel to go faster
```

### From Gates to Arithmetic Logic Unit (ALU)

```
ALU = collection of logic circuits selected by a control signal:
  ADD:   64-bit adder
  SUB:   adder with B complemented (+1 for two's complement)
  AND:   64 parallel AND gates
  OR:    64 parallel OR gates
  XOR:   64 parallel XOR gates
  SHL:   barrel shifter (shift left)
  SHR:   barrel shifter (shift right)
  CMP:   subtractor + check if result is 0 (sets flags: ZF, NF, CF, VF)

One clock cycle: present operands A and B at inputs
                 select operation via control bits
                 output is valid after gate propagation delay (~50ps at 3GHz)
```

---

## Layer 3 — Digital Circuits: Memory, Arithmetic, Clocks

### Flip-Flop — One Bit of State

A gate network is combinational — outputs depend only on current inputs, no memory. To store state, we need **feedback** — output fed back to input.

```
D flip-flop (the fundamental memory cell):

     D ──→ [Logic] ──→ Q
               ↑
           CLK (clock)

Behavior:
  On rising edge of CLK: Q is updated to match D
  Between clock edges:   Q holds its value (ignores D)

This is how a register works:
  64 D flip-flops = one 64-bit register
  On each clock cycle, all 64 bits can be updated simultaneously
  
SRAM (L1/L2 cache) uses 6 transistors per bit to store state:
  Two cross-coupled inverters hold a bit
  Two access transistors allow reading/writing
  Very fast (1–4 cycle access) but large (6T per bit)

DRAM (main memory) uses 1 transistor + 1 capacitor per bit:
  Capacitor stores charge = 1, no charge = 0
  Leaks charge → must be refreshed every ~64ms
  Smaller (1T1C), denser, but slower (40–100ns access)
```

### The Clock — The Heartbeat

```
CPU clock: a crystal oscillator producing a precise square wave
  Apple M3 Pro CPU cores: up to 4.05 GHz
  4.05 GHz = 4,050,000,000 cycles per second
  One clock cycle = 1/4,050,000,000 seconds ≈ 0.247 nanoseconds

Physical clock distribution:
  A single oscillator signal must reach all flip-flops simultaneously
  Clock tree: hierarchical buffer network distributing clock signal
  Skew: time difference between when clock arrives at different parts
  → Must be < 20ps (picoseconds) across a chip the size of a stamp
  Clock tree distribution is one of the hardest chip design problems

Dynamic frequency scaling (Apple Silicon's efficiency cores):
  P-cores (performance): up to 4.05 GHz (YouTube playback, active work)
  E-cores (efficiency): up to 2.6 GHz (background tasks, idle)
  GPU: up to 1.4 GHz
  Frequency varies dynamically based on thermal and power budget
  Lower frequency = quadratically lower power (P ∝ C·V²·f)
```

---

## Layer 4 — The CPU Die: Apple M-Series Architecture

Apple M-series chips are Systems-on-a-Chip (SoC) — an entire computer on one die. Everything that a MacBook needs (CPU, GPU, RAM, neural engine, media engine, I/O controllers) is integrated on a single piece of silicon.

### Die Floorplan (Apple M3 Pro)

```
┌─────────────────────────────────────────────────────────┐
│                    Apple M3 Pro Die (~20mm²)             │
│                                                          │
│  ┌──────────────┐  ┌──────────────────────────────────┐  │
│  │ P-Cores ×6   │  │     GPU (18 cores)               │  │
│  │ (4.05 GHz)   │  │     (1.4 GHz)                    │  │
│  │ L1: 192KB i  │  │     Tile-based deferred rendering │  │
│  │ L1: 128KB d  │  │     Unified L2 Cache: 8MB        │  │
│  │ L2: 4MB      │  └──────────────────────────────────┘  │
│  └──────────────┘                                        │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │ E-Cores ×6   │  │ Neural     │  │ Media Engine     │  │
│  │ (2.6 GHz)    │  │ Engine     │  │ H.264, HEVC,     │  │
│  │ Shared L2    │  │ 18 TOPS    │  │ VP9, AV1, ProRes │  │
│  │ 4MB          │  │            │  │ Hardware decode  │  │
│  └──────────────┘  └────────────┘  └──────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Unified Memory (36GB LPDDR5) — Shared by CPU + GPU   │ │
│  │ 150 GB/s bandwidth                                   │ │
│  └──────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ I/O: USB4/TB4, PCIe, SDXC, SPI (flash), I²S (audio) │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Why Unified Memory Matters

In a traditional PC, CPU and GPU have separate memory pools:
```
Traditional:
  CPU → System RAM (DDR5, 64GB/s)     [CPU memory]
  GPU → VRAM (GDDR6, 500GB/s)         [GPU memory]
  Transfer between them:               [PCIe bus, 32GB/s — bottleneck]
  Copying video frame: CPU→VRAM copy costs time and PCIe bandwidth

Apple M-series:
  CPU, GPU, Neural Engine all access the same physical LPDDR5 pool
  Memory bandwidth: 150–800 GB/s (M3 Ultra: 800 GB/s)
  No PCIe copy needed — GPU reads from same location CPU wrote
  Video decoder writes decoded frame → GPU composites it → display reads it
  Zero-copy the entire pipeline
```

### Apple Silicon Instruction Pipeline

Apple M-series P-cores implement an ARM64 (AArch64) ISA with Apple-specific extensions. The microarchitecture is Apple's own design — not licensed from ARM.

```
Apple Firestorm/Everest (P-core) microarchitecture:

Fetch:       8 instructions/cycle (widest in any CPU)
Decode:      8 micro-ops/cycle
Rename:      ~12 micro-ops/cycle (register renaming → eliminate false deps)
Dispatch:    Issue queue depth: ~800 entries (enormous — deep OoO window)
Execute:     Multiple execution units in parallel:
               6× ALU (integer)
               4× FP/SIMD (float, NEON)
               2× Load
               2× Store
               1× Branch
Reorder:     ~3500 entry ROB (largest in any consumer CPU — deep speculation)
Commit:      8 instructions/cycle

For context, Intel Alder Lake:
  Fetch: 6/cycle, ROB: 512 entries, instruction window: ~200 entries
  Apple M2: 3500 ROB entries = 7× deeper speculation than Intel

Why the deep window matters for YouTube:
  The video codec hot loops have complex data dependencies
  Deeper OoO window = more independent instructions found and overlapped
  → Higher effective IPC (instructions per cycle)
  → Faster decode in fewer cycles
  → Earlier completion for the same clock speed
```

---

## Layer 5 — Memory: DRAM, Caches & Unified Memory

### The Memory Hierarchy (MacBook M3 Pro)

```
Latency        Size         Location        Access
─────────────────────────────────────────────────────────
~0 cycles      384 registers  In CPU core    Register file
4 cycles        192KB L1-i    In CPU core    Instruction cache (P-core)
4 cycles        128KB L1-d    In CPU core    Data cache (P-core)
12 cycles       4MB L2        In CPU cluster Shared among P-cores
40 cycles       24MB L3 / SLC On-die        System Level Cache (all agents)
90 cycles       36GB LPDDR5   On-package     Unified memory (CPU+GPU+NE)
~10,000 cycles  512GB–4TB SSD NVMe flash     Apple custom SSD controller

During YouTube playback, which levels are active:
  Registers: codec loop variables (motion vectors, DCT coefficients)
  L1 cache: hot code paths in the decode loop (~16KB inner loop fits in L1-i)
  L2 cache: decoded block caches, codec state
  L3/SLC:   video frame buffers, GPU working data
  LPDDR5:   full video buffer, network receive buffers, app heap
  SSD:       Safari cache, downloaded segments pending decode
```

### How Virtual Memory Works

Every process (Safari, the YouTube tab process) thinks it owns the entire 64-bit address space. The CPU + OS collaborate to make this illusion real.

```
Virtual address space of the Safari renderer process:
  0x000000000000 to 0x7FFFFFFFFFFF  (128TB virtual space)
  
Physical memory mapping via page tables:
  Virtual address 0x000100004000
    → MMU translates via 4-level page table
    → Physical page frame 0x1A2B3C4 (somewhere in 36GB LPDDR5)

TLB (Translation Lookaside Buffer):
  Cache of recent virtual→physical translations
  M3 Pro L1 TLB: ~192 entries (instruction), ~128 (data)
  M3 Pro L2 TLB: ~3072 entries
  TLB miss: walk 4 levels of page table (~100 cycles)
  TLB hit:  ~1 cycle overhead

Page sizes:
  Base: 16KB pages (Apple Silicon uses 16KB, not the x86 standard 4KB)
  Large: 2MB, 32MB, 64GB "huge pages" for reducing TLB pressure
```

### LPDDR5 Physical Operation

```
LPDDR5 (Low Power Double Data Rate 5):
  In MacBook M3 Pro: 36GB on-package (not on the same die, but same package)
  Bandwidth: 150 GB/s (M3 Pro, 6-channel)
  Latency: ~90ns (row access + column access + bus transfer)

Physical DRAM operation:
  DRAM organized in banks → rows → columns
  
  Read sequence:
    1. Row activation (RAS): select row, charge sense amplifiers (~15ns)
    2. Column access (CAS): select column, data appears on bus (~10ns)
    3. Data transfer: burst of bits transferred (~4ns per word at LPDDR5 speeds)
    4. Precharge: discharge sense amplifiers, ready for next row (~10ns)
  
  tRAS = 45ns, tCL = 15ns, tRP = 15ns (typical LPDDR5)

Memory controller (inside Apple M-series die):
  Schedules read/write requests to minimize bus idle time
  Reorders requests for same-row (open-page policy) to avoid RAS overhead
  Refresh: DRAM cells leak charge → controller sends refresh commands every 64ms
```

---

## Layer 6 — Boot: From Power Button to macOS Desktop

Pressing the MacBook power button initiates a carefully choreographed sequence:

### Boot Sequence

```
T=0ms:   Power button pressed
         Battery Management IC signals PMIC (Power Management IC)
         
T=1ms:   PMIC enables power rails in sequence:
         1.8V → 1.2V → 3.3V rails stabilize
         CPU receives power-good signal

T=2ms:   Apple M-series Boot ROM (hardwired in chip):
         - ROM is read-only memory baked into silicon at fabrication
         - Not writable, not erasable — permanent firmware
         - Verifies LLB (Low Level Bootloader) signature using Apple's root key
         - Root key is burned into chip at factory (eFuses)
         - If signature invalid → boot halts (Secure Boot)

T=10ms:  LLB (Low Level Bootloader) executes:
         - Initializes LPDDR5 memory controller
         - Memory training: negotiates timings with DRAM
         - Loads and verifies iBoot (main bootloader)

T=200ms: iBoot executes:
         - Initializes NVMe SSD controller
         - Reads macOS volume from APFS (Apple File System)
         - Loads kernel (XNU) from /System/Library/Kernels/kernel
         - Verifies kernel with Apple signing certificate
         - Sets up memory layout (page tables, KASLR — randomizes kernel base address)
         - Passes control to XNU

T=1s:    XNU kernel initializes:
         - CPU topology detection (which cores exist)
         - Memory zone allocator initialization
         - IOKit: hardware driver framework
         - BSD layer: POSIX process model, filesystem, networking
         - Mach layer: IPC, VM, scheduling primitives
         - Registers interrupt handlers (timers, I/O, page faults)

T=3s:    launchd (PID 1) starts:
         - The first userspace process
         - Reads /System/Library/LaunchDaemons/*.plist
         - Starts all system services (mDNSResponder, configd, diskarbitrationd, etc.)

T=5s:    WindowServer starts:
         - macOS's display compositor
         - Creates the GPU rendering context
         - Establishes connections to the display

T=6s:    Login window appears → user authenticates
         LoginWindow starts user session (Dock, Finder, menubar, etc.)
         
Total: ~8–15 seconds from cold boot to usable desktop (M-series MacBook)
```

---

## Layer 7 — The Operating System: macOS & XNU Kernel

### XNU Architecture

XNU (X is Not Unix) is macOS's kernel — a hybrid combining the Mach microkernel with a BSD (Berkeley Software Distribution) Unix layer, wrapped in IOKit for hardware drivers.

```
User space (ring 3 on x86; EL0 on ARM64):
  Safari browser process (renderer, GPU process, networking process)
  System services (mDNSResponder, etc.)
  
────────────────── syscall boundary ──────────────────────
Kernel space (ring 0 on x86; EL1 on ARM64):

  BSD layer:
    POSIX API (open, read, write, socket, mmap...)
    VFS (Virtual File System) — APFS, HFS+, NFS, FAT
    Network stack (BSD TCP/IP)
    Process model (fork, exec, signals)
  
  Mach layer:
    Tasks and Threads (VM containers, execution units)
    Mach ports (IPC — inter-process communication)
    Virtual memory manager (vm_map, mach_vm_allocate)
    Scheduling (timeshare + real-time policies)
  
  IOKit:
    C++ driver framework
    Every hardware device has an IOKit driver
    WiFi: AirPortFamilyDarwin.kext
    NVMe SSD: AppleNVMeController.kext
    GPU: AGXFamily.kext (Apple GPU driver)
    Audio: AppleHDA.kext → IOAudioFamily.kext
    USB: IOUSBFamily.kext
    Display: AppleDisplay.kext

  Hardware abstraction layer:
    Interrupt controller (AIC — Apple Interrupt Controller)
    Timer (APIC equivalent — Apple calls it the CPU PMU)
```

### Process Model During YouTube Playback

Safari uses a **multi-process architecture** — each tab runs in a separate sandboxed process:

```
Processes running for YouTube in Safari:

/usr/bin/Safari (UIProcess)          → Browser chrome (tabs, address bar)
/usr/bin/com.apple.WebKit.WebContent → Renderer: HTML parsing, JS, layout
/usr/bin/com.apple.WebKit.Networking → Network requests (DNS, TLS, HTTP)
/usr/bin/com.apple.WebKit.GPU        → GPU compositing of rendered content

IPC between these processes:
  XPC (Apple's IPC built on Mach ports)
  Shared memory for large data (video frames shared zero-copy)
  Messages for control (start decode, advance frame, etc.)

Sandbox rules (com.apple.security.sandbox):
  WebContent process: can read specific files, CANNOT:
    - Access most of filesystem
    - Make arbitrary network connections
    - Access camera/microphone without permission
    - See other processes' memory
  
  Networking process: CAN make network connections, CANNOT:
    - Access disk (except specific caches)
    - Access user data
  
  If the renderer is compromised (malicious JS exploit):
    It cannot escape its sandbox to affect the rest of the system
    → Defense in depth against web-based attacks
```

### macOS Memory Management

```
APFS SSD as virtual memory backing store:
  When physical RAM is full:
  macOS compressed memory (Zswap equivalent):
    First: compress cold pages in RAM using WKdm algorithm (~2:1 compression)
    If still full: write compressed pages to SSD swap
    M-series SSDs: ~3GB/s write → swapping is fast (but still avoid)

For YouTube:
  Total memory for one YouTube tab (~4K stream):
    JavaScript heap (V8): ~200MB
    Video decode buffer (2 frames × 4K × 4 bytes): ~66MB
    Encoded segment buffer: ~50MB
    DOM tree + CSSOM: ~30MB
    WebGL textures (if any): ~50MB
    Total: ~400MB active per tab
```

---

## Layer 8 — Networking: WiFi to YouTube's Servers

When you click a YouTube link, data has to travel from Google's servers in a data center to your MacBook. Here is every physical and protocol layer.

### WiFi Physical Layer (IEEE 802.11)

The MacBook's WiFi chip (Apple's own W3 or BCM chip) communicates wirelessly with your router.

```
Physical transmission (WiFi 6E, 6GHz band example):

1. Data to transmit (binary): 10110100 11001010...

2. Bit encoding: OFDM (Orthogonal Frequency Division Multiplexing)
   Split data across 996 subcarriers (each ~78 kHz wide)
   Each subcarrier modulated independently:
     BPSK:  1 bit per symbol  (most robust, used for control)
     QPSK:  2 bits per symbol
     16-QAM:  4 bits per symbol
     64-QAM:  6 bits per symbol
     256-QAM: 8 bits per symbol
     1024-QAM: 10 bits per symbol (WiFi 6, good signal required)

3. What modulation means physically:
   Each subcarrier is a sinusoidal radio wave at a specific frequency
   Amplitude and phase of the sine wave encode bits
   256-QAM: 8 possible amplitudes × 32 possible phases = 256 combinations
   One "symbol" = one configuration of amplitude+phase = 8 bits

4. IFFT (Inverse Fast Fourier Transform):
   All subcarrier signals added together in the frequency domain
   IFFT converts to time domain (the actual waveform to transmit)
   This waveform is a complex superposition of all subcarriers

5. DAC (Digital-to-Analog Converter):
   Digital samples → analog voltage → WiFi amplifier → antenna
   Transmit power: ~15–20 dBm (30–100mW)

6. Radio propagation:
   2.4 GHz: ~12.5cm wavelength
   5 GHz:   ~6cm wavelength
   6 GHz:   ~5cm wavelength
   Travels at speed of light (~30cm/ns)
   Distance home → router: ~10m → propagation delay: ~33ns
   Walls, furniture: absorb and reflect signal → multipath
   MIMO (Multiple Input Multiple Output): 4×4 in WiFi 6E
   → Multiple antennas send/receive simultaneously
   → Spatial multiplexing: 4 parallel data streams

7. At the router: ADC converts received waveform back to samples
   FFT: converts time domain → frequency domain
   Equalization: compensates for multipath distortion
   Demodulation: extract bits from each subcarrier
   Error correction: LDPC (Low-Density Parity Check) codes
   → Original bits recovered

WiFi 6E theoretical max: 9.6 Gbps (with 160MHz channel, 4×4 MIMO, 1024-QAM)
Typical real speed: 500–1500 Mbps close to router
YouTube 4K stream: ~20 Mbps → WiFi is not the bottleneck
```

### Network Stack (Router to YouTube)

```
Your home network:
  MacBook (192.168.1.50) ←→ Router (192.168.1.1) ←→ ISP ←→ Internet ←→ Google

Packet journey:
  1. MacBook creates IP packet:
     Source IP:       203.45.67.89 (your public IP, via NAT)
     Destination IP:  142.250.x.x (YouTube/Google CDN)
     Protocol:        UDP (QUIC) or TCP (HTTPS fallback)
  
  2. Router NAT (Network Address Translation):
     Source 192.168.1.50:52341 → translated to 203.45.67.89:52341
     Router maintains NAT table mapping private to public
  
  3. ISP backbone routing:
     BGP (Border Gateway Protocol) routes packet across internet
     Each router checks its routing table → next hop
     Typically 10–20 hops, 10–50ms RTT depending on distance to CDN
  
  4. Google CDN (Content Delivery Network):
     YouTube video requests hit the nearest Google edge node
     India → Google's POP in Mumbai, Chennai, or Bangalore
     ~5–15ms RTT within India to Google's CDN

Physical layers involved:
  Home: WiFi (electromagnetic waves, ~GHz)
  ISP local: Ethernet or fiber (photons in optical fiber)
  ISP backbone: fiber (1550nm wavelength, DWDM — multiple wavelengths)
  Speed of light in fiber: ~200,000 km/s (2/3 of c in vacuum)
  Mumbai to Bangalore: ~1000km → ~5ms propagation delay
```

---

## Layer 9 — TLS & HTTPS: Encrypted Connection

Before any YouTube data flows, Safari establishes a TLS 1.3 session. This involves asymmetric cryptography (key exchange) followed by symmetric encryption for all data.

### TLS 1.3 Handshake

```
Timeline: ~1 RTT (round trip) for new connection, 0-RTT for resumed

T=0ms:   Client Hello (MacBook → Google):
  TLS version: 1.3
  Random: 32 random bytes (client nonce)
  Key Share: X25519 public key (Diffie-Hellman public parameter)
    MacBook generates: random private key a → public key A = a×G (elliptic curve)
    G = generator point on Curve25519
    Sends A to Google
  Supported cipher suites: TLS_AES_128_GCM_SHA256, TLS_CHACHA20_POLY1305_SHA256
  SNI (Server Name Indication): "www.youtube.com"

T+RTT:   Server Hello (Google → MacBook):
  Server's Key Share: B = b×G (Google's DH public key)
  Both sides compute shared secret:
    MacBook: secret = a×B = a×(b×G) = ab×G
    Google:  secret = b×A = b×(a×G) = ba×G = ab×G
    Same result! But attacker cannot compute ab×G without knowing a or b.
    This is the Diffie-Hellman key exchange — magic of elliptic curves.
  
  From shared secret → HKDF derivation → symmetric keys:
    handshake_secret → client_handshake_key, server_handshake_key
    master_secret    → client_application_key, server_application_key
    (one-way derivation — compromise of app key doesn't reveal handshake key)
  
  Certificate: Google's TLS certificate (signed by DigiCert/Google Trust Services)
  Certificate Verify: signature over transcript (proves possession of private key)
  Finished: HMAC of entire handshake transcript

T+RTT:   MacBook verifies certificate:
  Certificate chain: leaf cert → intermediate CA → root CA
  Root CA must be in macOS Keychain (trusted by Apple)
  Checks: not expired, hostname matches, not revoked (OCSP/CRL)

Now: all data encrypted with AES-128-GCM (authenticated encryption)
  AES-GCM:
    AES block cipher in Galois/Counter Mode
    Encryption + integrity check (AEAD — Authenticated Encryption with Associated Data)
    Apple M-series: hardware AES acceleration → AES-128-GCM at ~50 GB/s
    Authentication tag: 128-bit GHASH — detects any tampering

Perfect Forward Secrecy: ephemeral DH keys (a, b) discarded after session
  Even if Google's long-term private key is stolen later:
  Past recorded sessions cannot be decrypted (keys were never stored)
```

---

## Layer 10 — HTTP/3 & QUIC: The Modern Web Transport

YouTube uses QUIC (Quick UDP Internet Connections) — Google's transport protocol that replaces TCP for most web traffic.

### Why QUIC Replaces TCP

```
TCP problems for web:
  Head-of-line blocking: if packet 5 is lost, packets 6,7,8 wait
    → Video stalls even though later packets arrived fine
  Connection setup: TCP 3-way handshake + TLS = 2 RTTs minimum
  No multiplexing: one stream per connection (HTTP/1.1)
    HTTP/2 fixed multiplexing but still has TCP HOL blocking

QUIC solutions:
  Built on UDP: no kernel TCP stack overhead
  Multiplexed streams: video, audio, thumbnails all in parallel
    Each stream has independent loss recovery
    Lost packet in one stream doesn't block others
  Integrated TLS 1.3: 0-RTT for resumed connections
  Connection migration: if your IP changes (WiFi → 4G), connection continues
    TCP: change of IP = new connection = re-authentication
    QUIC: uses connection ID, not IP tuple → survives network change

QUIC packet structure:
  UDP header (8 bytes)
  QUIC header: connection ID, packet number, packet type
  QUIC frames:
    STREAM frame:  stream ID, offset, data
    ACK frame:     which packets received (selective ACK, no cumulative only)
    PADDING:       fill to prevent traffic analysis
  TLS record embedded directly in QUIC (not separate layer)
```

### HTTP/3 Semantics

```
HTTP/3 request for YouTube video segment:
  HEADERS frame:
    :method: GET
    :scheme: https
    :authority: rr3---sn-3c27sn7k.googlevideo.com
    :path: /videoplayback?id=...&range=0-5242880&...
    user-agent: Mozilla/5.0 ... Safari/605.1.15
    accept-encoding: gzip, deflate, br
    range: bytes=0-5242880      ← DASH segment range request

  DATA frame:
    Response: 5MB encoded video data
    Compressed with Brotli (br)

QPACK: HTTP/3's header compression (replaces HPACK from HTTP/2)
  Static table: 99 commonly used headers pre-indexed
  Dynamic table: learned headers from this session
  Result: "content-type: video/mp4" compressed to 1 byte (table entry 4)
```

---

## Layer 11 — DNS: Resolving youtube.com

Before any TCP/QUIC connection, the MacBook needs to translate "youtube.com" into an IP address.

### DNS Resolution (Step by Step)

```
T=0: Safari tells the WebKit networking process: "resolve youtube.com"

T=1: Check NSCache (in-memory DNS cache):
  Hit? Return immediately.
  TTL expired? Proceed to resolver.

T=2: Send DNS query to resolver:
  macOS uses mDNSResponder (Bonjour daemon) as local resolver
  Configured resolver: 
    Your router (192.168.1.1) → ISP DNS, OR
    8.8.8.8 (Google), 1.1.1.1 (Cloudflare) if manually set
  
  DNS query (UDP to port 53 or DoH/DoT):
    Question: youtube.com, type A (IPv4) / AAAA (IPv6)

T=3: DNS over HTTPS (DoH) — macOS 11+ uses DoH by default:
  Encrypts DNS queries (prevents ISP snooping on domains you visit)
  Query goes to the DNS resolver as an HTTPS request:
    POST https://dns.google/dns-query
    Body: DNS wire format encoded query

T=4: Recursive resolution (if resolver doesn't have it cached):
  Resolver → Root nameservers (.): "who handles .com?"
    Response: 13 root nameserver IPs
  Resolver → .com TLD nameserver: "who handles youtube.com?"
    Response: ns1.google.com, ns2.google.com, ns3.google.com
  Resolver → ns1.google.com: "what is youtube.com?"
    Response: 142.250.77.46 (or similar), TTL=300

T=5: macOS receives answer, caches for TTL=300 seconds (5 minutes)
  Returns to WebKit networking process

For YouTube video segments:
  The actual video comes from: googlevideo.com subdomains
    e.g., rr3---sn-3c27sn7k.googlevideo.com
  This is a geographically close Google CDN node
  DNS returns the nearest edge server IP based on your resolver's location
  → Anycast routing: same domain → different IP depending on where you are
```

---

## Layer 12 — The Browser Engine: Safari & WebKit

Once YouTube's page is downloaded, WebKit (Safari's rendering engine) must parse, interpret, and display it. For a video page this means HTML, CSS, JavaScript, and the HTML5 video element all working together.

### Page Rendering Pipeline

```
Network → WebKit → Screen (simplified):

1. HTML Parser (WebContent process):
   Tokenizer: bytes → tokens (DOCTYPE, start-tag, end-tag, text, comment)
   Tree constructor: tokens → DOM tree (Document Object Model)
   DOM example for YouTube player:
   Document
   └── html
       ├── head (meta, scripts, styles)
       └── body
           └── div#page-manager
               └── ytd-app
                   └── ytd-watch-flexy
                       └── #player
                           └── video#movie_player  ← The actual <video> element

2. CSS Parser:
   Download stylesheets (cached) → parse to CSSOM (CSS Object Model)
   Merge DOM + CSSOM → Render Tree (only visible elements with computed styles)

3. JavaScript Engine (JavaScriptCore — WebKit's JS engine):
   YouTube is a React/Polymer hybrid single-page app
   Download youtube.com → minimal HTML shell
   Download main.js (~3MB minified, ~15MB uncompressed) → execute
   JS dynamically builds entire page: fetch video metadata, setup player

   JavaScriptCore tiers:
   a. LLInt (Low Level Interpreter): parse JS → bytecode, execute immediately
   b. DFG JIT (Data Flow Graph): hot functions → native machine code (fast)
   c. FTL JIT (Faster Than Light): very hot functions → LLVM-optimized code

   For YouTube's player.js:
   - Bytecode: 50ms to parse + compile
   - DFG JIT fires after ~10 executions of a function
   - Video decode callback (called 30/60× per second) quickly goes FTL
   - The decode dispatch loop runs at sub-microsecond speed after JIT warm-up

4. Layout (LayoutEngine):
   Compute every element's position and size
   CSS Flexbox/Grid algorithms, text layout (font metrics, line wrapping)
   Result: layout tree with pixel coordinates for every element

5. Paint (RenderLayer):
   Determine what to draw for each layer
   Separate layers for: video element, overlay UI, thumbnails, ads (sadly)
   "Composited layers" for elements that animate (the video)

6. Composite (GPU Process):
   Upload layers as GPU textures
   GPU composites all layers → final frame
   Display frame via Core Animation / QuartzCore
```

### JavaScript and the YouTube Player

```javascript
// YouTube player initialization (simplified pseudocode):
// This runs when the page loads

// 1. Check MediaSource Extensions (MSE) support
const mediaSource = new MediaSource();
videoElement.src = URL.createObjectURL(mediaSource);

// 2. Adaptive Bitrate Selection (DASH/ABR)
const manifest = await fetch('/api/manifest?videoId=...');
const { videoFormats, audioFormats } = parseManifest(manifest);
const selectedVideo = ABRAlgorithm.select(videoFormats, bandwidth);
// Selects: "1080p VP9, 3Mbps" based on current network conditions

// 3. Feed encoded data to MediaSource
const videoSourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp09.00.50.08"');
const audioSourceBuffer = mediaSource.addSourceBuffer('audio/mp4; codecs="mp4a.40.2"');

// 4. Download and append segments in a loop
async function downloadLoop() {
  while (!done) {
    const segment = await fetch(nextSegmentUrl);
    const data = await segment.arrayBuffer();
    videoSourceBuffer.appendBuffer(data);  // Demux + queue for decoder
    // The browser's internal decoder (Hardware Media Engine) picks this up
  }
}

// 5. 60fps playback loop (runs 60× per second)
requestAnimationFrame(function renderLoop(timestamp) {
  // Sync video to audio clock
  // Update progress bar
  // Handle buffer stalls
  requestAnimationFrame(renderLoop);
});
```

---

## Layer 13 — Video Delivery: CDN, DASH & Codecs

### DASH — Dynamic Adaptive Streaming over HTTP

YouTube uses DASH to deliver video — the same video is pre-encoded at many bitrates and resolutions. The player continuously selects the appropriate quality level.

```
Available representations for a typical YouTube video:
  Video (VP9 codec):
    144p   @ 100 Kbps
    240p   @ 300 Kbps
    360p   @ 700 Kbps
    480p   @ 1,200 Kbps
    720p   @ 2,500 Kbps
    1080p  @ 4,500 Kbps
    1440p  @ 8,000 Kbps
    2160p  @ 20,000 Kbps (4K)
  
  Audio (AAC and Opus):
    opus 48kHz 50 Kbps (stereo)
    aac  44.1kHz 128 Kbps (stereo)
    aac  44.1kHz 256 Kbps (stereo)

ABR (Adaptive Bitrate) algorithm:
  Every 5 seconds, measure: actual_throughput = bytes_received / time
  Buffer health = seconds_of_video_buffered
  
  If buffer > 15s AND throughput > 1.2× selected_bitrate:
    Upgrade quality (next higher bitrate)
  If buffer < 5s OR throughput < 0.9× selected_bitrate:
    Downgrade quality (next lower bitrate)
  
  Result: smooth playback even on variable connections
  Tradeoff: may see brief quality drop when network degrades

Segment structure:
  Each "segment" = 5 seconds of video (or 10 seconds for lower resolutions)
  1080p segment: 4,500 Kbps × 5s = ~2.8 MB per segment
  Player fetches segments 2–3 ahead: buffer = 10–15s of video
  
  fMP4 format (fragmented MP4):
    Movie fragment header (moof): timing, sample info
    Movie fragment data (mdat): encoded video/audio bytes
```

### H.264 Video Codec Deep Dive

Most YouTube streams use VP9 (Google's codec) or H.264 (universal compatibility). They work similarly — here's H.264/AVC:

```
A video is not stored as independent frames. That would be enormous.
Instead, only differences between frames are stored.

Frame types:
  I-frame (Intra-coded):  Complete standalone image
                          ~300KB for 1080p frame
                          Like a JPEG — all pixels encoded
  
  P-frame (Predicted):    Differences from previous frame
                          ~30KB for 1080p frame
                          Motion vectors + residuals
  
  B-frame (Bidirectional): Differences from BOTH previous AND future frames
                           ~15KB for 1080p frame
                           Best compression, most complex to decode

GOP (Group of Pictures):
  I P P P P B B P P P P B B ... I P P P ...
  Typical GOP length: 30–60 frames (1–2 seconds at 30fps)
  Jump to any timestamp: seek to nearest I-frame, then decode forward

How P-frame encoding works:
  Divide frame into 16×16 pixel macroblocks
  
  For each macroblock:
  1. Motion estimation: search previous frame for best matching block
     Find best match at offset (Δx, Δy) — the motion vector
     "Block at (100,200) in current frame is at (98,195) in previous frame"
  
  2. Motion compensation: subtract the matched block from current block
     Result: residual (small differences after compensation)
     For a static background: residual ≈ 0 (nothing to encode)
  
  3. DCT (Discrete Cosine Transform) on residual 8×8 blocks:
     Transform spatial domain → frequency domain
     Low frequencies (gradients) → large coefficients
     High frequencies (fine texture) → small coefficients
  
  4. Quantization: divide coefficients by quantization step
     High-frequency coefficients rounded to 0 → discarded
     This is the "lossy" step — where quality is traded for size
     Quantization Parameter (QP): 0=lossless, 51=maximum compression
  
  5. Entropy coding (CABAC):
     Zigzag scan coefficients (DC first, then AC by frequency)
     Run-length encode the zeros (many zeros after quantization)
     Huffman/arithmetic code the result → bit stream

Decoding (what your MacBook does):
  Reverse every step:
  Entropy decode → Dequantize → IDCT → Add motion-compensated prediction
  → Reconstructed pixel block
  
  For a 1080p30 stream: 30 frames × 1920×1080 pixels × decode steps
  ~10 billion operations per second — why hardware decode exists
```

---

## Layer 14 — Video Decode: H.264/VP9/AV1 on Apple Silicon

Playing video would kill your battery if done in software. Apple M-series includes dedicated **Media Engine** hardware that decodes video at essentially zero power.

### Apple Media Engine

```
Apple M3 Pro Media Engine:
  Dedicated hardware decoders (fixed-function, not programmable):
    H.264 (AVC): encode + decode
    HEVC (H.265): encode + decode
    VP9: decode only
    AV1: decode only (M3 and later)
    ProRes: encode + decode
  
  Performance:
    H.264 4K 30fps: <50mW (vs ~3W in software)
    HEVC 4K 60fps: hardware, near-zero CPU
    AV1 4K: hardware from M3 (M1/M2 need software → hot + battery drain)
  
  Media Engine interface:
    VideoToolbox framework (CoreMedia.framework)
    VTDecompressionSession: feed encoded data, get decoded frames
    Internally: DMA to media engine, IOMMU-protected memory regions
    Output: CVPixelBuffer (CoreVideo pixel buffer)
    Format: YCbCr 420 (luma + chroma planes) or 422/444 for HDR

Hardware decode pipeline:
  Network → NSURLSession (URLSession) → MediaSource buffer
         ↓
  WebKit demuxer: parse fMP4 container → extract NAL units
         ↓
  VideoToolbox → Media Engine (hardware)
  DMA: encoded data → media engine internal buffer (no CPU copy)
  Decode:
    Entropy decoder (hardware CABAC parser)
    Motion compensation unit (reads reference frames from cache)
    IDCT unit (inverse DCT, 8×8 blocks)
    Deblocking filter (smooth block boundaries)
    SAO filter (HEVC) / Loop filter (VP9)
  Output: raw YUV frame in hardware pixel buffer
         ↓
  CVPixelBuffer in IOSurface (shared memory GPU can read directly)
         ↓
  GPU compositor reads frame without any CPU copy (zero-copy)
```

### Color Science: YCbCr and HDR

```
Why video uses YCbCr instead of RGB:
  Human vision: more sensitive to luminance (Y) than color (Cb, Cr)
  YCbCr 4:2:0: store luma at full resolution, chroma at half
    For a 1920×1080 frame:
      Y (luma):  1920×1080 = 2,073,600 bytes
      Cb (blue): 960×540   = 518,400 bytes
      Cr (red):  960×540   = 518,400 bytes
      Total: ~3MB per raw frame vs ~6MB for RGB
  
  Color space conversion (for display):
    Matrix multiply: [R,G,B] = M × [Y,Cb,Cr]
    ITU-R BT.709: standard HD color matrix
    ITU-R BT.2020: wide color gamut for HDR content
    GPU handles this conversion at display time

HDR (High Dynamic Range):
  SDR: 8-bit per channel (256 levels), 100 nits max
  HDR10: 10-bit per channel (1024 levels), up to 1000 nits
  Dolby Vision: 12-bit, metadata per scene for dynamic tone mapping
  MacBook ProMotion display: up to 1600 nits peak (M3 Pro/Max)
  
  HDR decode path uses 10-bit or 12-bit buffers throughout
  GPU tone maps to display's actual brightness capabilities
```

---

## Layer 15 — The Display Pipeline: GPU to Photons

### Metal Graphics API

The GPU process uses Apple's Metal API (the macOS/iOS equivalent of Vulkan) to composite the video frame onto the display.

```
WebKit GPU process compositing:

1. Layers received from renderer:
   - Video layer (updated every frame at 30/60fps)
   - UI overlay (controls, progress bar)
   - Page background
   - Other DOM content

2. Metal command buffer:
   // Render video frame texture
   let encoder = commandBuffer.makeRenderCommandEncoder(descriptor: ...)
   encoder.setRenderPipelineState(videoPipeline)
   encoder.setFragmentTexture(videoFrameTexture, index: 0) // CVPixelBuffer as MTLTexture
   encoder.drawPrimitives(type: .triangleStrip, vertexStart: 0, vertexCount: 4)
   // Draws a fullscreen quad with video frame texture mapped onto it
   encoder.endEncoding()

3. Fragment shader (GPU shader code, runs per pixel):
   // Convert YCbCr → RGB
   // Apply color space transform (BT.709 → display P3)
   // Tone map if HDR
   // Apply brightness/contrast
   
4. Present to display:
   commandBuffer.present(drawable)  // schedule for display refresh
   commandBuffer.commit()           // submit to GPU

Metal command buffer execution:
  Runs entirely on GPU without CPU intervention
  GPU cores execute shader code for all pixels in parallel
  For 2560×1600 @ 60fps: 245,760,000 pixels/second
  GPU: 18 cores × ~64 ALUs × 1.4GHz → ~1.6 TFLOPS for this task
```

### Display Hardware: Liquid Retina XDR

```
MacBook Pro 14" / 16" display (Liquid Retina XDR):

Panel type: mini-LED backlit IPS
  (ProMotion XDR on MacBook Pro 14/16 = very high quality)
  
Resolution: 3024×1964 (14"), 3456×2234 (16")
  "Retina" = pixel density > 220 PPI (human eye limit at arm's length)
  14": 254 PPI → individual pixels invisible at normal viewing distance

Refresh rate: ProMotion adaptive, 1–120Hz
  Static content: drops to 1Hz (saves power)
  Video at 24fps film: displays at 48Hz or 120Hz (smooth motion with interpolation)
  Scrolling: ramps to 120Hz instantly (imperceptible latency)
  
Mini-LED backlight:
  10,000 individual LEDs arranged in zones
  Local dimming: dark areas of video → LEDs dimmed or off
  Contrast ratio: up to 1,000,000:1 (vs 1000:1 on standard LCD)
  Peak brightness: 1600 nits (HDR)
  
IPS LCD operation (how pixels actually work):
  LED backlight → diffuser → light guide → polarizer (horizontal)
  → Liquid crystal layer → color filter (R,G,B subpixels) → polarizer (vertical)
  
  Liquid crystal: twisted nematic LC molecules between two glass plates
  No voltage: LC molecules twisted 90° → light rotates 90° → passes vertical polarizer → pixel ON
  Full voltage: LC molecules align with field → light doesn't rotate → blocked by vertical polarizer → pixel OFF
  Partial voltage: partial twist → partial light transmission → grey levels
  
  Each pixel has: R subpixel + G subpixel + B subpixel (plus W for brightness)
  R subpixel uses a red color filter that transmits ~625nm light
  G subpixel uses a green filter (~530nm)
  B subpixel uses a blue filter (~460nm)
  
  Mixing RGB:
    Pure white: R=255, G=255, B=255 (all subpixels pass light)
    Pure black: R=0, G=0, B=0 (backlight dimmed by mini-LED local dimming)
    YouTube's red logo: R=255, G=0, B=0 (only red subpixels transmit)
    Video frame: each pixel set to exact R,G,B values from decoded video

Display controller (TCON — Timing Controller):
  Receives digital pixel data from GPU via MIPI DSI interface
  Drives each row of pixels via TFT (Thin Film Transistor) addressing
  Refreshes display 120 times per second
  Each refresh: scan all 3024×1964 = 5,935,136 pixels row by row

OLED vs IPS LCD (MacBook Pro uses IPS; iPhone uses OLED):
  IPS LCD: backlit (backlight always on unless mini-LED dims it)
  OLED: each pixel emits its own light (perfect blacks, no backlight)
  OLED advantages: infinite contrast, faster response time, thinner
  OLED disadvantages: burn-in risk, lower max brightness for large areas

How photons reach your eye:
  LED backlight → ~435nm blue LED peak
  Quantum dot layer (on some displays) converts blue → white
  Through LC layer modulated by TFT voltages
  Through RGB color filters → specific wavelengths transmitted
  Through cover glass (anti-reflection coated, scratch-resistant)
  ~12–20 inches air gap
  → Cornea → lens → retina → photoreceptors (cones: S=blue, M=green, L=red)
  → Retinal ganglion cells → optic nerve → lateral geniculate nucleus
  → Primary visual cortex (V1) → visual association areas
  → Conscious perception of the video image
```

---

## Layer 16 — Audio Pipeline: AAC to Pressure Waves

### Audio Decoding

YouTube audio streams use AAC (Advanced Audio Coding) at 128–256 Kbps, or Opus at lower bitrates.

```
AAC encoding (what happened on YouTube's server):
  Original audio: 44,100 samples/second, 16-bit PCM stereo
  = 44,100 × 2 channels × 2 bytes = 176,400 bytes/second (1.41 Mbps raw)

  AAC compression:
  1. Psychoacoustic model:
     FFT of each 1024-sample window (~23ms of audio)
     Compute "masking threshold": which frequencies are inaudible
       Simultaneous masking: loud 1kHz tone masks nearby frequencies
       Temporal masking: loud sound masks sounds in next 5–20ms
     Allocate more bits to audible frequencies, fewer to masked
  
  2. MDCT (Modified DCT): convert time domain → frequency domain
     1024 overlapping samples → 512 frequency coefficients
  
  3. Quantize coefficients (discard inaudible ones → near-zero bits)
  
  4. Huffman encode the quantized spectrum
  
  Result: ~128 Kbps (11:1 compression) with near-transparent quality

AAC decoding (in Safari on your MacBook):
  Parse AAC bitstream → ADTS or LATM container
  Entropy decode (Huffman) → quantized spectral coefficients
  Dequantize → frequency domain representation
  Inverse MDCT → time domain audio (PCM samples)
  Overlap-add: smooth block boundaries
  Stereo reconstruction (joint stereo): decode mid-side → left-right
  Output: 44,100 Hz, 32-bit float PCM, stereo
  
  AudioToolbox does this on Apple Silicon (hardware assist for AAC)
```

### CoreAudio Pipeline

```
CoreAudio architecture (macOS):

Decoded PCM samples
     ↓
AVFoundation / WebAudio API
     ↓
CoreAudio AudioUnit graph:
  [IO Unit] ← system mixer
     ↓
HAL (Hardware Abstraction Layer)
     ↓
Audio driver (AppleHDA.kext or USBAudio.kext)
     ↓
Hardware

CoreAudio is a real-time audio system:
  Audio thread runs at highest priority (SCHED_RR real-time class)
  I/O buffer size: 256 samples = 256/44100 = 5.8ms
  Every 5.8ms: audio thread must deliver 256 new samples
  If it misses this deadline: audible glitch (click, dropout)

Sample rate conversion:
  YouTube audio: 44.1 kHz
  Hardware output: may be 48 kHz (common on Macs)
  SRC (Sample Rate Conversion): polyphase filter resampling
  44,100 → 48,000: multiply by 160/147 ratio

Volume mixing:
  Multiple audio sources (YouTube + Spotify + notification sounds)
  All mixed by CoreAudio's software mixer before sending to hardware

Format conversion for hardware:
  Software: 32-bit float PCM (FP32)
  DAC input: typically 24-bit integer PCM
  Conversion: float × 8,388,607 → round to nearest 24-bit integer
```

### Digital-to-Analog Conversion (DAC)

```
The MacBook's audio hardware:

Apple custom codec chip (part of the T2/M-series or discrete codec)
Cirrus Logic CS42L83 or Apple custom (on newer models)

DAC operation:
  Input: stream of 24-bit integers at 48,000 samples/second
  
  Delta-Sigma DAC (used in modern audio chips):
  Not: "take 24-bit value → output that voltage" (R-2R ladder)
  Instead:
    1. Oversample: upsample 48kHz → 12.288 MHz (256×)
    2. Noise-shape: push quantization noise above hearing range (>20kHz)
    3. 1-bit output: rapidly alternate between VDD and GND
       Duty cycle encodes the value: 50% duty = 0V, 75% duty = +0.5V, etc.
    4. Lowpass filter (anti-aliasing): smooth the 1-bit stream
       Result: smooth analog voltage proportional to the digital sample
  
  Output voltage swing: typically ±1V peak (headphone output)
  SNR: >100dB (the 24-bit DAC is essentially perfect — thermal noise limits performance)

Headphone driver amplifier:
  DAC output: ~1V, high impedance
  Need: ~1V, low impedance to drive headphones (16–32Ω load)
  Op-amp buffer: provides current gain (power amplification)
  Output power: ~40mW into 16Ω headphones (adequate for ~105 dB SPL)
```

### Speaker Physics

```
MacBook built-in speakers (force-canceling woofers in MacBook Pro):

Speaker driver (electrodynamic transducer):
  Permanent magnet creates static magnetic field
  Voice coil: small coil of wire attached to speaker cone
  AC current from amp → alternating magnetic field
  Alternating field interacts with permanent magnet:
    Current direction A: coil pushed forward → cone moves forward
    Current direction B: coil pushed backward → cone moves backward
  
  Cone movement → compression and rarefaction of air
  Air pressure waves propagate at ~343 m/s (speed of sound, room temp)
  
  Frequency response:
    Larger cones: better bass (low frequency, long wavelengths)
    Smaller cones: better treble (high frequency, short wavelengths)
    MacBook uses multiple drivers: woofers + tweeters

Force-canceling design (MacBook Pro):
  Two woofers push in opposite directions simultaneously
  Mechanical force they exert on the chassis: cancels out
  Result: louder bass without vibrating (and damaging) the laptop chassis

Pressure waves reach your ear:
  Sound pressure level (SPL):
    Measured in dB SPL (relative to 20 μPa — threshold of hearing)
    Normal conversation: 60 dB SPL
    MacBook max volume: ~85 dB SPL at 1m (3.16 mPa pressure variation)
  
  Ear canal: resonates at ~3,500 Hz (amplifies this frequency ~20dB)
  Eardrum: vibrates with incoming pressure wave
  Ossicles (malleus, incus, stapes): mechanical amplification
  Oval window → cochlea: fluid wave in spiral canal
  Basilar membrane: different frequencies peak at different positions
    Base: high frequencies (20kHz)
    Apex: low frequencies (20Hz)
  Hair cells: transduce mechanical → electrical (stretch-activated ion channels)
  Auditory nerve → cochlear nucleus → auditory cortex
  → Conscious perception of YouTube's audio
```

---

## Layer 17 — Power: How the Battery Keeps It All Running

### Battery Chemistry

```
MacBook Pro battery: Lithium-Ion Polymer (LiPo)
  Capacity: ~99.6 Wh (MacBook Pro 14")
  Nominal voltage: ~11.5V (3 cells × 3.83V nominal)
  Chemistry: LiCoO₂ cathode / graphite anode

Electrochemical operation:
  Discharge (powering the MacBook):
    Anode (negative, graphite): Li → Li⁺ + e⁻
      Lithium ions deintercalate from graphite lattice
    Cathode (positive, LiCoO₂): Li⁺ + e⁻ + CoO₂ → LiCoO₂
      Lithium ions intercalate into cobalt oxide lattice
    
    Lithium ions flow through electrolyte (internal, ionic)
    Electrons flow through external circuit (power!)
    Voltage: determined by electrochemical potential difference
    
  Charging (reverse):
    External voltage forces reverse reaction
    Li⁺ moves back to graphite anode
    Apple M3 MacBook: 67W–140W charging depending on model

  Why batteries degrade:
    Solid Electrolyte Interphase (SEI) grows on anode over cycles
    Lithium plating at high charge rates (fast charging damage)
    Cathode structural changes after many cycles
    ~500 charge cycles to 80% of original capacity (Apple spec)
```

### Power Management During YouTube

```
Apple Silicon power management (CLPC — Closed Loop Power Controller):

What's consuming power during 1080p YouTube playback:

Component          Typical Power    Notes
───────────────────────────────────────────────────────────
Media Engine       0.1W             Hardware VP9/AV1 decode
P-cores (2 active) 1.5W             JS engine, UI, networking
E-cores (4 active) 0.8W             Background tasks
GPU (partial)      1.5W             Compositing, display
Neural Engine      0.0W             Idle
WiFi chip          0.3W             Continuous receive
LPDDR5 memory      0.8W             Active data access
Display            3.0W             1000 nit backlight, IPS
Display controller 0.2W             
SSD controller     0.05W            Mostly idle (RAM buffering)
USB controller     0.05W            
Touch ID/T2        0.02W
Board/PMIC         0.5W             Voltage regulation losses
───────────────────────────────────────────────────────────
Total:             ~8.8W

MacBook Pro 14" battery: 70 Wh
Battery life playing YouTube: 70 / 8.8 ≈ ~8 hours
  (Apple claims 18 hours for video streaming — at lower brightness, WiFi off)

Thermal management:
  8.8W of power → 8.8W of heat (energy conservation)
  Copper heat pipe transfers heat from chip to aluminum heatsink
  Fan (single or dual depending on model) blows air through heatsink
  M3 MacBook Air: fanless → throttles if sustained load exceeds ~8W
  M3 MacBook Pro: fan kicks in above ~8W sustained

Dynamic Voltage and Frequency Scaling (DVFS):
  When playing video:
  P-cores: 3.2 GHz @ 0.9V (not max — no need for full speed)
  E-cores: 1.3 GHz @ 0.7V (background tasks, very low voltage)
  GPU: 600 MHz @ 0.7V (compositing only — no 3D rendering)
  
  Power ∝ C × V² × f (where C = capacitance of switching transistors)
  Reducing from 4.0 GHz → 3.2 GHz: saves 20% frequency × lower voltage savings
  Total power: roughly (3.2/4.0)³ ≈ 51% of max power (frequency + voltage scaling)
```

---

## The Full Stack: Everything Simultaneously

Here is every process running simultaneously at the precise moment a YouTube video frame is displayed:

```
T = one frame boundary (16.67ms at 60fps)

[Electrons & Physics]
  25 billion transistors switching on/off at 4 GHz
  ~100 billion logic transitions per nanosecond
  Battery delivering 8.8W via LiPo electrochemistry
  WiFi antenna transmitting/receiving at 5GHz EM waves

[Memory System]
  L1 cache serving codec loop at 4-cycle latency
  L3/SLC fetching next video segment from network buffer
  LPDDR5 delivering video frame to GPU at 150 GB/s

[CPU — P-cores]
  Core 0: JavaScriptCore JIT-compiled player loop
          managing DASH buffer, calling requestAnimationFrame
  Core 1: WebKit layout + CSS paint for DOM updates
  Core 2: URLSession — downloading next 5MB video segment via QUIC
  Core 3: IDLE (waiting for next work)

[CPU — E-cores]
  Core 0: mDNSResponder — handling DNS TTL refresh for googlevideo.com
  Core 1: XPC message passing between WebContent/GPU processes
  Core 2-5: IDLE, parked at low frequency/voltage

[Media Engine — Hardware]
  Decoding VP9 encoded P-frame:
    CABAC entropy decode → dequantize → IDCT → motion compensation
    Output: 1920×1080 YCbCr frame to CVPixelBuffer in IOSurface
  This takes ~0.2ms, uses 0.1W, runs entirely independent of CPU

[GPU — 18 cores]
  Fragment shaders executing for 3024×1964 display pixels:
    Read YCbCr texture (decoded video frame)
    YCbCr → RGB matrix multiply (BT.709 color matrix)
    Composite over UI layer (player controls)
    Output RGB values to display framebuffer
  Duration: ~2ms for full frame composite

[CoreAudio — Real-time thread]
  Every 5.8ms (256 samples): AAC decoder outputs PCM samples
  Software mixer: blend YouTube audio + system sounds
  SRC: resample 44.1kHz → 48kHz
  Send 256 × 48kHz samples to audio hardware DMA buffer

[DAC → Speaker]
  Delta-sigma DAC converting digital samples to analog voltage at 12.288 MHz
  Amplifier driving speaker voice coil
  Speaker cone moving ±0.3mm at 440Hz (if an 'A' note is playing)
  Air molecules compressed and rarefied in spherical pressure waves
  Traveling at 343 m/s toward your ears

[Display — Every 8.3ms at 120Hz]
  TCON scanning 3,456 rows of pixels
  Each row: TFT transistors activated, LC cells charged to target voltage
  Mini-LED local dimming: 10,000 LEDs at individually tuned brightness
  Backlight photons: 435nm blue LED → quantum dot conversion → white
  Through twisted nematic LC layer → color filter subpixels
  R,G,B photons exit screen at ~500 nm average wavelength
  Travel 14 inches, enter your cornea

[Networking — Background]
  QUIC connection to rr3---sn-3c27sn7k.googlevideo.com maintained
  UDP ACK frames sent every ~200 packets
  WiFi beacon exchange every 102ms (keeping association alive)
  Segment downloaded: 2.8MB in 22ms at 1 Gbps WiFi

[Power & Thermal]
  PMIC regulating: 1.0V core, 0.7V E-cores, 1.8V I/O, 3.3V peripherals
  Thermal sensor at 23°C — fan at minimum speed
  Battery SoC: dropping at ~0.00025% per second (8.8W / 99.6Wh × 100%)

Everything listed above happens every 16.67 milliseconds.
60 times per second.
Trillions of electron movements.
One smooth YouTube video frame.
```

---

## Summary: The Abstraction Stack

```
Level          What You See          What's Really Happening
──────────────────────────────────────────────────────────────────
User           Video playing         —
Application    HTML <video> element  —
JS Engine      VP9 bitstream in MSE  —
OS / API       CVPixelBuffer frame   —
Codec          Decoded YUV pixels    —
Hardware       Metal GPU texture     —
Driver         MMIO register writes  —
CPU            Machine code          —
ISA            ARM64 instructions    —
Microarch      µops in ROB           —
Pipeline       Gate outputs          —
CMOS           Transistor on/off     —
Physics        Electron potential    —
```

Every layer exists to provide a simpler abstraction to the layer above. You press play — and 25 billion transistors, bouncing electrons, electromagnetic waves, photons, and pressure waves collaborate in 16 milliseconds to deliver what your brain interprets as "video with sound."

---

## See Also

- [CPU Architecture](cpu-architecture.md) — Pipeline, caches, OoO execution, NUMA
- [GPU Architecture](gpu-architecture.md) — SM model, rasterization, CUDA, Vulkan
- [Linux Internals](linux-internals.md) — Scheduler, VFS, memory management, system calls
- [Kernel Architecture](kernel-architecture.md) — Kernel overview and subsystems
- [Compilers & Interpreters](compilers-and-interpreters.md) — How JS and native code are compiled
- [Drivers & DLLs](drivers-and-dlls.md) — How CoreAudio, Metal, and hardware drivers work
- [Network Protocols](network-protocols.md) — TCP, TLS, QUIC, HTTP/3, DNS in depth
- [BitTorrent Technology](../torrenting/bittorrent-technology.md) — P2P as contrast to CDN delivery
