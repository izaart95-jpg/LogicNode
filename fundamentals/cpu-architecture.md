# CPU Architecture — Hardware & Software Internals

This document covers Central Processing Unit architecture from silicon to software — how CPUs are physically built, how they execute instructions, and how operating systems and compilers interact with the hardware.

---

## Table of Contents
1. [What a CPU Actually Is](#1-what-a-cpu-actually-is)
2. [Instruction Set Architectures — CISC vs RISC](#2-instruction-set-architectures--cisc-vs-risc)
3. [The Execution Pipeline](#3-the-execution-pipeline)
4. [Caches — L1, L2, L3](#4-caches--l1-l2-l3)
5. [Branch Prediction](#5-branch-prediction)
6. [Out-of-Order Execution & Speculative Execution](#6-out-of-order-execution--speculative-execution)
7. [NUMA — Non-Uniform Memory Access](#7-numa--non-uniform-memory-access)
8. [Multicore & Hyperthreading](#8-multicore--hyperthreading)
9. [CPU Rings & Privilege Levels](#9-cpu-rings--privilege-levels)
10. [Interrupts & Exceptions](#10-interrupts--exceptions)
11. [SIMD — Vectorized Computation](#11-simd--vectorized-computation)
12. [CPU Performance Counters & Profiling](#12-cpu-performance-counters--profiling)
13. [Modern CPU Microarchitectures](#13-modern-cpu-microarchitectures)

---

## 1. What a CPU Actually Is

A CPU is a chip containing billions of transistors arranged into functional units that fetch, decode, and execute instructions. The transistors act as electrical switches — on = 1, off = 0. Layers of abstraction sit between physical electrons and the C code you write.

```
Electrons flowing through transistors
    ↓
Logic gates (AND, OR, NOT, XOR) — built from transistors
    ↓
Functional units (adder, multiplier, comparator) — built from gates
    ↓
Registers — tiny ultra-fast storage built from flip-flops
    ↓
ALU (Arithmetic Logic Unit) — performs integer operations
FPU (Floating Point Unit) — handles IEEE 754 float math
    ↓
Execution core — ties ALU, FPU, registers into a pipeline
    ↓
Instruction Set Architecture (ISA) — the contract between hardware and software
    ↓
Machine code — binary instructions matching the ISA
    ↓
Assembly — human-readable representation of machine code
    ↓
High-level languages (C, Rust, Go) — compiled to assembly/machine code
```

### Registers

Registers are the fastest storage on the system — 0–1 clock cycles to access, located physically inside the CPU die.

**x86-64 general purpose registers:**

| Register | 64-bit | 32-bit | 16-bit | 8-bit | Conventional Use |
|----------|--------|--------|--------|-------|-----------------|
| Accumulator | RAX | EAX | AX | AL/AH | Return values, arithmetic |
| Base | RBX | EBX | BX | BL/BH | Base pointer (preserved) |
| Counter | RCX | ECX | CX | CL/CH | Loop counter, shift amount |
| Data | RDX | EDX | DX | DL/DH | I/O port, multiply overflow |
| Source Index | RSI | ESI | SI | SIL | Source of memory ops |
| Dest Index | RDI | EDI | DI | DIL | Destination of memory ops |
| Stack Pointer | RSP | ESP | SP | SPL | Top of stack |
| Base Pointer | RBP | EBP | BP | BPL | Stack frame base |
| R8–R15 | R8-R15 | R8D-R15D | R8W-R15W | R8B-R15B | General purpose (x86-64 only) |

**Special registers:**
- **RIP** — Instruction Pointer. Points to the next instruction to execute. Cannot be directly written.
- **RFLAGS** — Flags register. Bits set by arithmetic results: ZF (zero), CF (carry), SF (sign), OF (overflow), PF (parity).
- **CR0–CR4** — Control registers. Govern protected mode, paging, cache, FPU. Accessible only in ring 0.
- **XMM0–XMM15** — 128-bit SIMD registers (SSE)
- **YMM0–YMM15** — 256-bit SIMD registers (AVX)
- **ZMM0–ZMM31** — 512-bit SIMD registers (AVX-512)

---

## 2. Instruction Set Architectures — CISC vs RISC

The ISA is the contract — it defines what instructions exist, what they do, how they're encoded in binary, and how the processor behaves. Software compiled for one ISA cannot run on another without translation.

### CISC (Complex Instruction Set Computer)

CISC designs provide many specialized instructions, some very complex. A single instruction may perform memory access, arithmetic, and writeback simultaneously.

**x86-64 (Intel/AMD):** The dominant desktop/server ISA. Evolved from 8086 (1978). Variable-length encoding (1–15 bytes per instruction). Thousands of instructions. Hardware internally translates complex CISC instructions into simpler micro-operations (µops) for the execution engine.

```nasm
; x86-64 CISC example — single instruction does a lot
; REP MOVSB: copy ECX bytes from [RSI] to [RDI]
mov rcx, 1024
mov rsi, source
mov rdi, destination
rep movsb            ; Copy 1024 bytes — one instruction, many operations

; SCAS: scan string for a value
; LODS/STOS: load/store string operations
; These are "CISC" — one mnemonic, complex behavior
```

**Why CISC complexity?** Historical: code density mattered when RAM was expensive. Compilers and programmers hand-wrote tight loops using powerful single instructions. The hardware complexity was moved from the programmer to the CPU designer.

### RISC (Reduced Instruction Set Computer)

RISC designs use fewer, simpler, fixed-length instructions. Each instruction does exactly one simple thing. Complexity is pushed to the compiler, which generates more instructions but each is trivially decoded.

**ARM (AArch64 / ARM64):** Dominant in mobile (all phones), Apple Silicon (M-series), increasingly in servers (AWS Graviton, Ampere). Fixed 32-bit instruction encoding. Load-Store architecture: arithmetic only operates on registers, never directly on memory.

```
; AArch64 RISC example — ARM64
; Load from memory (explicit load required — no memory operands in arithmetic)
LDR X0, [X1]         ; Load 64-bit value from address in X1 into X0
ADD X2, X0, X3       ; X2 = X0 + X3 (only registers)
STR X2, [X4]         ; Store X2 to address in X4

; Compare to x86-64 which can:
; ADD RAX, [RBX]     ; Directly add memory operand — CISC
```

**RISC-V:** Open-source ISA (no license fees). Growing in embedded, research, and starting to appear in commercial hardware. Modular: base integer ISA + extension letters (M=multiply, F=float, V=vector, etc.)

### ISA Comparison

| ISA | Instruction Length | Register Count | Memory Model | Primary Use |
|-----|--------------------|---------------|-------------|-------------|
| **x86-64** | Variable (1–15 bytes) | 16 GP + 32 SIMD | Memory operands in arithmetic | Desktop, server, laptop |
| **ARM64** | Fixed 32-bit | 31 GP + 32 FP/SIMD | Load-Store only | Mobile, Apple Silicon, server |
| **RISC-V (RV64I)** | Fixed 32-bit (or 16-bit compressed) | 32 GP | Load-Store only | Embedded, research |
| **MIPS64** | Fixed 32-bit | 32 GP | Load-Store only | Routers, older consoles |

---

## 3. The Execution Pipeline

A pipeline breaks instruction execution into stages that can be overlapped — like an assembly line. While instruction N is executing, instruction N+1 is being decoded, and N+2 is being fetched.

### Classic 5-Stage RISC Pipeline

```
Stage 1: IF  — Instruction Fetch
  CPU reads the next instruction from memory (or cache) at address RIP/PC.
  RIP is incremented to point to the following instruction.

Stage 2: ID  — Instruction Decode
  The fetched bits are decoded: which operation? which registers? what immediate?
  Register file is read — operand values are retrieved.

Stage 3: EX  — Execute
  ALU performs the operation (add, compare, shift, etc.)
  Address calculation for memory instructions.

Stage 4: MEM — Memory Access
  Load instructions read data from the data cache.
  Store instructions write data to the data cache.
  Arithmetic instructions: this stage is idle (pass-through).

Stage 5: WB  — Write Back
  Result is written back to the destination register.
```

```
Clock cycle:  1    2    3    4    5    6    7    8    9
Instruction 1: IF  ID   EX   MEM  WB
Instruction 2:      IF  ID   EX   MEM  WB
Instruction 3:           IF  ID   EX   MEM  WB
Instruction 4:                IF  ID   EX   MEM  WB
                                        ↑
                                 All 4 in flight simultaneously
```

### Pipeline Hazards

Pipelines break down in three hazard scenarios:

**Data hazard:** Instruction needs a value not yet written back by a prior instruction.
```
ADD R1, R2, R3    ; R1 = R2 + R3 (writes R1 at WB, cycle 5)
SUB R4, R1, R5    ; Needs R1 at EX (cycle 7) — OK with forwarding
MUL R6, R1, R7    ; Needs R1 at EX (cycle 6) — STALL (R1 not ready yet)
```
Solution: **Forwarding** (bypass) — route result directly from EX to the next EX stage without waiting for WB.

**Control hazard:** Branch instruction — pipeline fetches wrong instructions.
```
CMP R1, R2
JE  somewhere     ; If equal, jump to somewhere — but we've already
                  ; started fetching the next sequential instruction!
```
Solution: **Branch prediction** (see §5). If mispredicted, flush the pipeline.

**Structural hazard:** Two instructions need the same hardware resource simultaneously.
Solution: **Pipeline stall** (bubble) — insert a NOP cycle until resource is free.

### Modern Superscalar Pipelines

Modern CPUs have deeply pipelined, superscalar architectures:
- **Superscalar:** Multiple execution units in parallel — 4–6+ instructions per clock cycle
- **Pipeline depth:** Intel Alder Lake has ~14 pipeline stages
- **Out-of-order execution:** Instructions execute in a different order than written (see §6)

---

## 4. Caches — L1, L2, L3

Memory hierarchy exists because DRAM is ~100–200 cycles away; registers are 0–1 cycles. Caches bridge this gap using fast SRAM physically close to the CPU cores.

```
Registers     — 0–1 cycles    ~1 KB     On-chip, per-core
L1 Cache      — 4–5 cycles    32–64 KB  On-chip, per-core (split: L1i instructions, L1d data)
L2 Cache      — 12–15 cycles  256 KB–1 MB  On-chip, per-core (unified)
L3 Cache      — 40–60 cycles  8–64 MB   On-chip, shared across all cores
DRAM          — 100–200 cycles 8–256 GB  Off-chip, DDR5/DDR4/LPDDR
NVMe SSD      — 10,000+ cycles Terabytes Off-chip, PCIe
HDD           — 10,000,000+ cycles      Mechanical (seek time)
```

### Cache Organization

A cache is divided into **sets** and **ways**. An n-way set-associative cache has n slots per set.

```
Cache line size: 64 bytes (universal on x86/ARM)
A cache line maps to one set based on address bits [11:6] (for a 4KB, 8-way cache)

Physical address: [Tag bits | Set index bits | Block offset bits]
                  [  43    |      6         |       6          ] = 55 bits (partial)

Lookup:
  1. Extract set index from address → which set to look in
  2. Compare tag bits against all ways in that set in parallel
  3. Cache hit: return data from matched way
  4. Cache miss: fetch 64-byte line from next level, evict if needed
```

### Write Policies

**Write-through:** Every write immediately goes to the next cache level and DRAM. Slower, but always consistent.

**Write-back:** Writes stay in cache (cache line marked "dirty"). Only written to DRAM when evicted. Faster, but needs careful coherence.

### Cache Coherence (MESI Protocol)

In multicore systems, each core has its own L1/L2 cache. If Core 0 writes to address X and Core 1 reads address X, what does Core 1 see?

MESI protocol tracks cache line state:
- **M (Modified):** Only in this cache, dirty (differs from memory)
- **E (Exclusive):** Only in this cache, clean (matches memory)
- **S (Shared):** In multiple caches, clean
- **I (Invalid):** Not present / stale

When Core 0 modifies a shared line, it broadcasts an **invalidation** — all other caches mark their copy Invalid. Next read from Core 1 triggers a cache miss and fetches the updated value from Core 0's cache (cache-to-cache transfer).

### Cache Performance in Code

```c
// Cache-friendly: sequential access (spatial locality)
for (int i = 0; i < N; i++) {
    sum += array[i];   // Prefetcher detects stride, loads lines ahead
}

// Cache-hostile: random access
for (int i = 0; i < N; i++) {
    sum += array[random_index[i]];   // Each access likely a cache miss
}

// False sharing: two threads access different variables in the same cache line
struct bad {
    int counter_a;   // Core 0 writes this
    int counter_b;   // Core 1 writes this
    // Both are in the same 64-byte cache line — MESI invalidation storms
};

struct good {
    int counter_a;
    char pad[60];    // Pad to separate cache lines
    int counter_b;
};
```

---

## 5. Branch Prediction

Branches (if/else, loops) break pipeline flow — the CPU doesn't know which instruction comes next until the branch is evaluated. Rather than stall, modern CPUs predict the outcome and speculatively execute the predicted path.

### Types of Predictors

**Static prediction:** Always predict taken (branches in loops are usually taken). Simple, ~65% accurate.

**Dynamic prediction:** Uses execution history stored in dedicated hardware tables.

**Two-bit saturating counter (bimodal predictor):**
```
States: Strongly Not Taken (00) → Weakly Not Taken (01) → Weakly Taken (10) → Strongly Taken (11)
Each branch has an entry indexed by its PC bits.
Correct prediction: counter moves toward "Strongly" end.
Wrong prediction: counter decrements one step.
```

**Tournament predictor (modern):** Combines local history (per-branch pattern) and global history (recent branch outcomes across the program). A meta-predictor chooses which to use for each branch.

**TAGE predictor:** Tagged Geometric history length predictor. Uses multiple tables with geometrically increasing history lengths. Powers Intel and AMD predictors. Achieves 95%+ accuracy on real programs.

### Misprediction Cost

```
Pipeline depth: 14–20 stages (modern CPUs)
Misprediction penalty: flush pipeline + fetch from correct path
Cost: 15–20 wasted cycles per misprediction

At 3 GHz with 3 billion cycles/second:
  20 wasted cycles = 6.67 nanoseconds per misprediction
  In a tight loop executing 1 billion iterations: 6.67 seconds wasted
```

### Writing Branch-Predictor-Friendly Code

```c
// Predictable branch (always true in loop) → predictor learns it
for (int i = 0; i < 1000000; i++) {
    if (i < 999999) {  // This branch is taken 999999/1000000 times
        do_work();
    }
}

// Unpredictable branch (random) → 50% miss rate
if (rand() % 2) {
    path_a();
} else {
    path_b();
}

// Branchless alternative using conditional move (no branch at all):
int result = (condition) ? a : b;
// Compiler often emits CMOV (conditional move) instead of a branch
// CMOV never mispredicts — no branch, just a multiplexer
```

---

## 6. Out-of-Order Execution & Speculative Execution

### Out-of-Order Execution (OoO)

Modern CPUs do not execute instructions in program order. The CPU looks ahead at many instructions (the "instruction window"), finds ones whose operands are ready, and executes them immediately — even if earlier instructions are still waiting.

```
Program order:         CPU execution order (example):
  DIV R1, R2, R3  →   (waiting for divisor — slow)
  ADD R4, R5, R6  →   ADD executes immediately (operands ready)
  MUL R7, R4, R8  →   MUL executes after ADD (depends on R4)
  SUB R9, R1, R4  →   SUB waits for DIV to complete (depends on R1)
```

**Key hardware structures:**
- **Reorder Buffer (ROB):** Tracks all in-flight instructions in program order. Instructions commit (become architecturally visible) in order even if executed out of order.
- **Reservation Stations:** Buffer instructions waiting for operands. When operands are available (forwarded from other units), the instruction is dispatched to an execution unit.
- **Register File + Register Renaming:** The physical register file has more registers than the ISA exposes (e.g., Intel has 280 physical integer registers vs 16 architectural). Renaming eliminates false dependencies (WAW, WAR hazards).

### Speculative Execution

The CPU executes instructions before knowing if they should execute — across branches, across memory loads, across system calls.

```
if (x < array_size) {          // Branch — CPU speculates the branch is taken
    int val = array[x];        // Load — executes speculatively
    int secret = cache[val];   // This executes before branch is confirmed!
}
```

**Spectre vulnerability (2018):** Speculative loads can bring data into cache even if the speculative path is later discarded. An attacker can measure cache timing to infer what data was loaded, leaking memory they shouldn't have access to. Mitigations (retpoline, IBRS, STIBP) impose performance costs of 5–30% on some workloads.

---

## 7. NUMA — Non-Uniform Memory Access

In multi-socket server systems, each CPU socket has local DRAM attached directly to it. Accessing local memory is fast; accessing memory attached to another socket (remote memory) crosses an interconnect — slower.

```
Socket 0                Socket 1
  CPU 0–15                CPU 16–31
  Memory Bank A           Memory Bank B
      ↕ fast                  ↕ fast
  Local access:            Local access:
    ~70 ns latency           ~70 ns latency
        ↕ interconnect (QPI/UPI/XGMI) ↕
  Remote access:           Remote access:
    ~140 ns latency          ~140 ns latency
```

### NUMA Topology

```bash
# View NUMA topology on Linux
numactl --hardware
# Output:
# node 0 cpus: 0 1 2 3 4 5 6 7 ... (local cores)
# node 1 cpus: 16 17 18 19 ...
# node distances:
# node   0   1
#   0:  10  21   (10 = local, 21 = remote — 2.1x slower)

# Check NUMA node distances
cat /sys/devices/system/node/node0/distance
```

### NUMA-Aware Programming

```c
#include <numa.h>

// Allocate memory on the local NUMA node (avoid remote access)
void *local_mem = numa_alloc_local(size);

// Pin a thread to specific NUMA node's CPUs
cpu_set_t cpuset;
CPU_ZERO(&cpuset);
// Add CPUs 0-7 (NUMA node 0)
for (int i = 0; i < 8; i++) CPU_SET(i, &cpuset);
pthread_setaffinity_np(pthread_self(), sizeof(cpuset), &cpuset);

// Allocate memory on a specific node
void *mem = numa_alloc_onnode(size, 0);  // On node 0
```

```bash
# Run a process on a specific NUMA node
numactl --cpunodebind=0 --membind=0 ./my_program

# Check NUMA statistics
numastat
```

### NUMA Effects on Performance

```
Database query performance (hypothetical):
  NUMA-unaware: all threads on node 0, memory scattered → 60% remote accesses → 1x speed
  NUMA-aware:   threads pinned to nodes, memory local → <5% remote → 1.8x speed
```

---

## 8. Multicore & Hyperthreading

### Multiple Cores

A modern CPU die contains multiple independent cores — each has its own L1 and L2 cache, register file, execution units, and pipeline. They share the L3 cache and memory controller.

```bash
# View CPU topology
lscpu
# Output includes:
# Thread(s) per core:  2    (hyperthreading enabled)
# Core(s) per socket:  8
# Socket(s):           2
# NUMA node(s):        2
# CPU(s):              32   (2 sockets × 8 cores × 2 threads)
```

### Hyperthreading (Intel) / SMT (AMD Simultaneous Multi-Threading)

Each physical core pretends to be two logical CPUs by maintaining two sets of architectural state (registers, program counters) while sharing execution units. When one thread stalls (e.g., waiting for a cache miss), the other thread uses the idle execution units.

```
Physical Core:
  [Thread 0 registers + PC]  [Thread 1 registers + PC]
         ↓                          ↓
  Shared execution units (ALU, FPU, load/store units)

Benefit: Better utilization of execution units when threads have complementary stall patterns
Drawback: Cache and TLB sharing causes interference; security implications (same physical core)
```

**Performance impact:** Hyperthreading adds ~20–30% throughput for mixed workloads. For memory-bound or compute-bound workloads already saturating execution units, it may add <5% and increase cache pressure.

---

## 9. CPU Rings & Privilege Levels

x86 defines four privilege rings. Linux and Windows use only Ring 0 (kernel) and Ring 3 (user).

```
Ring 0 (Kernel mode):
  - Full access to all hardware
  - Can execute privileged instructions (HLT, LGDT, MOV CR0, etc.)
  - Can access all memory (no paging restrictions at this level)
  - Direct I/O port access

Ring 3 (User mode):
  - Cannot execute privileged instructions
  - Cannot access arbitrary memory (enforced by paging hardware)
  - Cannot do I/O directly — must request via system call
  - Code crashes here safely without affecting the OS

Transition Ring 3 → Ring 0 (system call):
  SYSCALL instruction on x86-64:
    1. Save user-mode RIP, RSP, RFLAGS to MSRs
    2. Load kernel RSP from MSR_LSTAR
    3. Switch to kernel stack
    4. Execute kernel system call handler
    5. SYSRET returns to Ring 3
```

### Memory Protection

The CPU's Memory Management Unit (MMU) enforces per-page permissions via page table entries:

| Bit | Meaning |
|-----|---------|
| Present | Page is in physical memory (vs. swapped) |
| Writable | CPU allows writes (read-only if clear) |
| User | Accessible from Ring 3 (kernel-only if clear) |
| NX/XD | No-Execute — can't run code from this page |
| Dirty | CPU has written to this page since last check |
| Accessed | CPU has read this page since last check |

---

## 10. Interrupts & Exceptions

### Hardware Interrupts

An external device (keyboard, network card, timer) signals the CPU via an interrupt line. The CPU finishes the current instruction, saves state, and jumps to the interrupt handler.

```
Hardware interrupt flow:
  1. Device asserts IRQ line to APIC (Advanced Programmable Interrupt Controller)
  2. APIC forwards interrupt to CPU with vector number (0–255)
  3. CPU: push RFLAGS, CS, RIP onto stack
  4. Jump to handler address from IDT[vector]
  5. Handler runs (kernel code, ring 0)
  6. Handler sends EOI (End of Interrupt) to APIC
  7. IRET instruction restores RIP, CS, RFLAGS — returns to interrupted code
```

### Software Interrupts and Exceptions

```
Exception types:
  Fault:    Correctable — instruction can be restarted after fixing
            Example: Page fault (#PF) — OS loads page from disk, restarts instruction
  Trap:     Deliberately triggered — INT3 (debugger breakpoint), INT 0x80 (old syscall)
  Abort:    Unrecoverable — double fault, machine check error

Common x86 exceptions:
  #DE  (0)  Division by zero
  #DB  (1)  Debug exception (hardware breakpoints, single-step)
  #NMI (2)  Non-maskable interrupt (hardware failure)
  #BP  (3)  Breakpoint (INT3 — debugger inserts this byte)
  #PF  (14) Page fault — triggers OS virtual memory system
  #GP  (13) General Protection Fault — illegal instruction/privilege violation
  #UD  (6)  Invalid opcode
```

---

## 11. SIMD — Vectorized Computation

SIMD (Single Instruction Multiple Data) executes one instruction on multiple data elements simultaneously — crucial for multimedia, machine learning, and scientific computing.

```
Scalar (regular):      SIMD (AVX2, 256-bit):
  ADD R0, R1, R2       VADDPS YMM0, YMM1, YMM2
  One addition         Eight 32-bit float additions simultaneously

  Result: 1 float      Result: [f0+f4, f1+f5, f2+f6, f3+f7, ...]
```

### SIMD Instruction Sets (x86)

| Extension | Width | Year | Elements | Use |
|-----------|-------|------|---------|-----|
| **MMX** | 64-bit | 1996 | 8×i8, 4×i16, 2×i32 | Legacy |
| **SSE** | 128-bit | 1999 | 4×f32 | Still common |
| **SSE2** | 128-bit | 2001 | 2×f64, 16×i8 | Baseline for x86-64 |
| **AVX** | 256-bit | 2011 | 8×f32, 4×f64 | Modern FP compute |
| **AVX2** | 256-bit | 2013 | 32×i8, 8×i32 | Modern int compute |
| **AVX-512** | 512-bit | 2017 | 16×f32, 8×f64 | HPC, ML inference |

### Auto-Vectorization

Modern compilers automatically generate SIMD code from scalar loops:

```c
// Scalar loop — compiler will vectorize this automatically
void add_arrays(float *a, float *b, float *c, int n) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}
// With -O2 -march=native, GCC emits VADDPS YMM instructions
// Processing 8 floats per iteration instead of 1

// Help the compiler: use __restrict__ to indicate no aliasing
void add_arrays(float * __restrict__ a, float * __restrict__ b,
                float * __restrict__ c, int n)

// Explicit SIMD intrinsics (maximum control)
#include <immintrin.h>
void add_avx(float *a, float *b, float *c, int n) {
    int i = 0;
    for (; i <= n - 8; i += 8) {
        __m256 va = _mm256_load_ps(&a[i]);   // Load 8 floats
        __m256 vb = _mm256_load_ps(&b[i]);
        __m256 vc = _mm256_add_ps(va, vb);   // Add 8 floats
        _mm256_store_ps(&c[i], vc);           // Store 8 floats
    }
    for (; i < n; i++) c[i] = a[i] + b[i];  // Scalar remainder
}
```

---

## 12. CPU Performance Counters & Profiling

The CPU contains hardware performance counters — programmable registers that count micro-architectural events.

```bash
# Linux perf — CPU performance profiling
# Count cache misses during a run
perf stat -e cache-misses,cache-references,instructions,cycles ./program

# Output:
# 2,847,312   cache-misses    # 12.3% miss rate
# 23,142,088  cache-references
# 4,892,041,221 instructions
# 2,193,882,010 cycles         # IPC = 4892/2193 = 2.23

# Profile with call graph (find hot spots)
perf record -g ./program
perf report

# Real-time event monitoring
perf top

# Count branch mispredictions
perf stat -e branch-misses,branches ./program
```

```bash
# Intel VTune / AMD uProf — commercial profiling
# valgrind --tool=callgrind — software simulation of cache behavior
valgrind --tool=callgrind ./program
callgrind_annotate callgrind.out.*
```

---

## 13. Modern CPU Microarchitectures

### Intel Golden Cove (Alder Lake P-core, 2021)

- 6-wide superscalar decode
- 12 execution ports
- 512-entry reorder buffer
- ~1800 branch prediction entries updated per cycle
- L1i: 32KB, L1d: 48KB, L2: 1.25MB, L3: shared 30MB

### AMD Zen 4 (Ryzen 7000, 2022)

- 4+4 decode (integer + float)
- 6-wide integer execution
- 320-entry reorder buffer
- TAGE branch predictor
- Chiplet design: 5nm compute dies + 6nm I/O die
- Support for DDR5 and PCIe 5.0

### Apple M2 (ARM64, 2022)

- 8-wide decode (largest in industry)
- 12 execution ports
- 3500-entry reorder buffer (largest in industry — deep speculation)
- Out-of-order window: 7–8× larger than typical x86
- 192-byte cache lines (3× x86) for memory bandwidth
- Unified Memory Architecture — CPU and GPU share the same DRAM pool

---

## See Also

- [GPU Architecture](gpu-architecture.md) — GPU hardware, CUDA, TPU, compute shaders
- [Compilers & Interpreters](compilers-and-interpreters.md) — How source code becomes machine code
- [Kernel Architecture](kernel-architecture.md) — How the OS interacts with CPU hardware
- [Linux Internals](linux-internals.md) — Scheduler, memory management, interrupts from OS perspective
