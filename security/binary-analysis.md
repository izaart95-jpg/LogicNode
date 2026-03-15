# Binary Analysis Tools

A comprehensive reference for static analysis, dynamic analysis, emulation, symbolic execution, decompilation, and reverse engineering frameworks. Covers 30+ tools across the full binary analysis spectrum.

---

## Table of Contents
1. [Debuggers](#1-debuggers)
2. [Disassemblers & Decompilers](#2-disassemblers--decompilers)
3. [Symbolic Execution & Formal Analysis](#3-symbolic-execution--formal-analysis)
4. [Emulation & Dynamic Analysis](#4-emulation--dynamic-analysis)
5. [Binary Lifting & Recompilation](#5-binary-lifting--recompilation)
6. [Go Binary Analysis](#6-go-binary-analysis)
7. [Memory & Introspection](#7-memory--introspection)
8. [File Format Parsers](#8-file-format-parsers)
9. [Specialized Tools](#9-specialized-tools)
10. [Tool Selection Guide](#10-tool-selection-guide)

---

## 1. Debuggers

### x64dbg

- **Website:** https://x64dbg.com
- **Repository:** https://github.com/x64dbg/x64dbg
- **License:** MIT
- **Platform:** Windows only (x32dbg for 32-bit, x64dbg for 64-bit)
- **Type:** User-mode debugger

The standard open-source Windows debugger for malware analysis and reverse engineering. Replaces OllyDbg as the community default. Features a clean GUI with plugins, scriptable via Python, and supports hardware breakpoints, memory breakpoints, conditional logging, and trace recording.

```
Key features:
  - Hardware, software, and memory breakpoints
  - Conditional breakpoints with logging
  - Trace into / trace over / run trace recording
  - Memory map view, heap view, call stack
  - Thread management
  - Plugin system (x64dbg Python plugin, Ret-Sync for sync with IDA/Ghidra)
  - Import/export reconstruction
  - Anti-anti-debug bypass plugins (ScyllaHide)

Keyboard shortcuts:
  F7    — Step into
  F8    — Step over
  F9    — Run
  F2    — Toggle breakpoint
  Ctrl+G — Go to address
  Ctrl+B — Memory map
  Alt+M  — Memory breakpoints
```

### GDB — GNU Debugger

- **Website:** https://sourceware.org/gdb/
- **Type:** Cross-platform debugger (Linux, macOS, Windows, embedded)
- **Languages:** C, C++, Go, Rust, Python, Fortran (via debug info)

The universal Linux debugger. Supports local and remote debugging (GDB server over TCP/serial), kernel debugging, and coredump analysis. Extensible via Python GDB API.

```bash
# Basic usage
gdb ./binary
gdb ./binary core       # Debug coredump

# Attach to running process
gdb -p PID

# Key commands
(gdb) run [args]           # Start with arguments
(gdb) break main           # Breakpoint at function
(gdb) break *0x401234      # Breakpoint at address
(gdb) continue             # Continue execution
(gdb) next / ni            # Step over
(gdb) step / si            # Step into (si = instruction level)
(gdb) finish               # Run until function returns
(gdb) info registers       # Show registers
(gdb) x/10i $rip           # Examine 10 instructions at RIP
(gdb) x/20wx $rsp          # Examine 20 words at RSP
(gdb) print $rax           # Print register
(gdb) set $rax = 0x42      # Modify register
(gdb) disassemble main     # Disassemble function
(gdb) bt                   # Backtrace (call stack)
(gdb) info breakpoints     # List breakpoints
(gdb) watch *0x404000      # Watchpoint (break on memory write)
(gdb) catch syscall write  # Break on syscall
(gdb) layout asm           # TUI assembly view
(gdb) layout src           # TUI source view
```

**GDB Python API:**
```python
# ~/.gdbinit or loaded script
import gdb

class PrintRIPCommand(gdb.Command):
    def __init__(self):
        super().__init__("printrip", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        rip = gdb.parse_and_eval("$rip")
        print(f"RIP = {rip}")

PrintRIPCommand()
```

**pwndbg / peda / gef — GDB enhancement plugins:**
```bash
# pwndbg (recommended)
git clone https://github.com/pwndbg/pwndbg
cd pwndbg && ./setup.sh
# Adds: context view, heap analysis, ROP gadget search, telescope, checksec

# GEF (GDB Enhanced Features)
bash -c "$(curl -fsSL https://gef.blah.cat/sh)"
# Adds: heap visualization, pattern generation, telescope, deref chains
```

### LLDB

- **Website:** https://lldb.llvm.org
- **License:** Apache 2.0 (LLVM)
- **Platform:** macOS (default), Linux, Windows
- **Type:** LLVM-based debugger

LLDB is the default debugger on macOS (used by Xcode) and the most capable debugger for Apple Silicon binaries. Also used for debugging LLVM/Clang itself and for scripting complex debug scenarios.

```bash
# Basic usage (similar to GDB but different syntax)
lldb ./binary
lldb -p PID              # Attach

(lldb) run [args]
(lldb) breakpoint set --name main          # Break at function
(lldb) breakpoint set --address 0x100001234
(lldb) process continue
(lldb) thread step-over                   # Step over
(lldb) thread step-in                     # Step into
(lldb) thread step-inst                   # Step instruction
(lldb) frame info                         # Current frame
(lldb) register read                      # All registers
(lldb) register read rip rsp rax          # Specific registers
(lldb) memory read --format x 0x401000    # Read memory
(lldb) memory read --count 20 --format i $pc  # Disassemble at PC
(lldb) expression $rax = 0x42             # Modify register
(lldb) disassemble --name main
(lldb) bt                                 # Backtrace
(lldb) watchpoint set variable global_var

# Python scripting
(lldb) script
>>> import lldb
>>> process = lldb.debugger.GetSelectedTarget().GetProcess()
>>> thread = process.GetSelectedThread()
>>> frame = thread.GetSelectedFrame()
>>> print(frame.FindRegister("rip"))
```

### gdbgui

- **Repository:** https://github.com/cs01/gdbgui
- **License:** GPL v3
- **Type:** Browser-based GDB frontend

A web server that wraps GDB in a browser-based GUI — useful for remote debugging over SSH where installing a full GUI is impractical.

```bash
pip install gdbgui
gdbgui ./binary          # Opens browser GUI at http://localhost:5000
gdbgui --remote          # Allow connections from other hosts
gdbgui --port 8080 ./binary
```

Features: source code display, register view, memory explorer, call stack, breakpoint management — all via browser.

---

## 2. Disassemblers & Decompilers

### Radare2

- **Repository:** https://github.com/radareorg/radare2
- **Website:** https://rada.re
- **License:** LGPL v3
- **Type:** Full reverse engineering framework (CLI)
- **Stars:** 20k+

Radare2 is a complete reverse engineering toolkit: disassembler, debugger, hex editor, binary patcher, scripting engine, and more — all accessible from the command line. Steep learning curve but extremely powerful and scriptable.

```bash
# Open a binary
r2 ./binary
r2 -A ./binary    # Auto-analyze on open (-A = aaa)
r2 -d ./binary    # Open in debug mode
r2 -w ./binary    # Open in write mode (patching)

# Core commands (inside r2):
aa        # Analyze all (functions, strings, references)
aaa       # Deeper analysis
afl       # List all functions
afl~main  # Filter functions containing "main"
pdf @main # Print disassembly of function "main"
pdf @0x401000
px 64 @ 0x402000  # Print 64 bytes hexdump at address
ps @ 0x403000     # Print string at address
iz        # List strings in binary
iS        # List sections
ii        # List imports
ie        # List exports
db 0x401234       # Set breakpoint
dc        # Continue (debug mode)
dr        # Show registers (debug mode)

# Seek (navigate)
s main    # Seek to main
s 0x401000
s+10      # Seek forward 10 bytes

# Write/patch
wa nop    @ 0x401234   # Write NOP at address
wao nop                # Write NOP at current position

# Visual mode
V         # Enter visual mode
VV        # Graph view
p         # Cycle panel views in visual mode
q         # Exit

# Scripting with r2pipe
```

```python
# r2pipe — Python API for radare2
import r2pipe

r2 = r2pipe.open("./binary")
r2.cmd("aaa")                          # Analyze
funcs = r2.cmdj("aflj")               # Functions as JSON
for f in funcs:
    print(f["name"], hex(f["offset"]))

disasm = r2.cmdj("pdfj @main")         # Disassembly as JSON
for op in disasm["ops"]:
    print(hex(op["offset"]), op["disasm"])

r2.quit()
```

### Binary Ninja

- **Website:** https://binary.ninja
- **Type:** Commercial disassembler + decompiler with Python API
- **Platforms:** Windows, macOS, Linux
- **Price:** Commercial ($300–$500 personal), free cloud version at cloud.binary.ninja

Binary Ninja is a modern reverse engineering platform known for its high-quality decompiler (HLIL — High Level IL), its clean Python API, and its intermediate language lifters. Particularly popular among CTF players and security researchers for programmatic binary analysis.

```
Architecture:
  Raw binary
    ↓ Disassembly
  LLIL (Low Level IL) — close to assembly
    ↓ Lifted
  MLIL (Medium Level IL) — simplified, SSA
    ↓ Lifted
  HLIL (High Level IL) — C-like pseudocode
    ↓ Lifted
  Pseudo-C / Decompiler output

Each level is queryable via Python API.
```

```python
# Binary Ninja Python API
import binaryninja as bn

bv = bn.open_view("./binary")
bv.update_analysis_and_wait()

# List all functions
for func in bv.functions:
    print(func.name, hex(func.start))

# Get disassembly
func = bv.get_function_at(bv.start)
for block in func.basic_blocks:
    for insn in block:
        print(hex(insn[1]), insn[0])

# Get HLIL (decompiled)
for func in bv.functions:
    hlil = func.hlil
    for insn in hlil.instructions:
        print(insn)

# Find cross-references to an address
for ref in bv.get_code_refs(0x401234):
    print(ref.function.name, hex(ref.address))

# Rename a function
func = bv.get_function_at(0x401234)
func.name = "decrypt_payload"

# Add a comment
bv.set_comment_at(0x401234, "Key derivation starts here")
```

### amoco

- **Repository:** https://github.com/bdcht/amoco
- **License:** GPL v2
- **Type:** Static binary analysis framework (Python)

amoco is a Python framework for binary analysis focused on formal semantics — it models instructions as mathematical transformations on machine state, enabling precise static analysis. Useful for: CFG reconstruction in obfuscated binaries, semantic equivalence checking, and research into binary analysis algorithms.

```python
from amoco.system.elf import ELF
from amoco.system.linux_x86 import OS

p = OS.read("binary")
# Disassemble
b = p.cpu.disassemble(p.state.mem[p.state.pc:p.state.pc+16])
# Symbolic execution of a basic block
# Tracks register/memory state as symbolic expressions
```

---

## 3. Symbolic Execution & Formal Analysis

### angr

- **Website:** https://angr.io
- **Repository:** https://github.com/angr/angr
- **License:** BSD
- **Type:** Python binary analysis framework — symbolic execution, CFG, decompilation
- **Stars:** 7k+

angr is the leading open-source binary analysis platform. It can automatically find vulnerabilities, generate exploits, solve CTF challenges, and analyze malware — using symbolic execution to explore all possible program paths.

```python
import angr

# Load binary
p = angr.Project("./binary", auto_load_libs=False)

# ===== Simple symbolic execution =====
# Find: reach address 0x401234
# Avoid: address 0x401500 (bad path)
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x401234, avoid=0x401500)

if simgr.found:
    solution = simgr.found[0]
    # What was stdin that got us here?
    print(solution.posix.dumps(0))  # stdin content

# ===== Solve a crackme =====
# Find path where program prints "Correct!"
import claripy

# Create symbolic input
password = claripy.BVS("password", 8 * 20)  # 20-byte symbolic input
state = p.factory.full_init_state(stdin=angr.SimFileStream(content=password))

simgr = p.factory.simulation_manager(state)
simgr.explore(
    find=lambda s: b"Correct" in s.posix.dumps(1),    # stdout contains "Correct"
    avoid=lambda s: b"Wrong" in s.posix.dumps(1)
)

if simgr.found:
    s = simgr.found[0]
    print(s.solver.eval(password, cast_to=bytes))

# ===== CFG Analysis =====
cfg = p.analyses.CFGFast()       # Fast CFG (no execution)
cfg_accurate = p.analyses.CFGEmulated()  # Accurate CFG (symbolic exec)

for node in cfg.graph.nodes():
    print(hex(node.addr), node.name)

# ===== Vulnerability finding =====
# Find buffer overflow: detect when symbolic input reaches memcpy size arg
state = p.factory.full_init_state()
state.options.add(angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY)
simgr = p.factory.simulation_manager(state)
simgr.run()
```

### BinCAT

- **Repository:** https://github.com/airbus-seclab/bincat
- **Authors:** Airbus SecLab
- **License:** LGPL v2
- **Type:** Binary-level static analysis with abstract interpretation (IDA Pro plugin)

BinCAT (Binary Code Analysis Toolkit) performs abstract interpretation on binary code — tracking taint propagation, value ranges, and type information without running the binary. Implemented as an IDA Pro plugin.

```
Use cases:
  - Taint analysis: trace where user-controlled data flows
  - Vulnerability detection: find where tainted data reaches dangerous ops
  - Type recovery: infer data types from usage patterns
  - CVE analysis: verify patch effectiveness

Architecture:
  IDA Pro plugin (GUI) → sends analysis request
  OCaml analysis engine → abstract interpretation
  Results: annotated IDA listing with taint/value info
```

### BAP — Binary Analysis Platform

- **Repository:** https://github.com/BinaryAnalysisPlatform/bap
- **License:** MIT
- **Type:** Binary analysis framework (OCaml)
- **Stars:** 2k+

BAP is a CMU research framework for binary analysis. It lifts binary code to BIL (Binary Intermediate Language) — a simple, formally-specified IL — enabling formal analysis, taint tracking, and verification.

```bash
# Install
opam install bap    # Via OCaml package manager

# Disassemble a binary
bap ./binary --disassemble

# Run a pass (analysis plugin)
bap ./binary --pass=callgraph-collage

# BIL output (intermediate language)
bap ./binary --bil
```

---

## 4. Emulation & Dynamic Analysis

### Qiling Framework

- **Repository:** https://github.com/qilingframework/qiling
- **Website:** https://qiling.io
- **License:** GPL v2
- **Type:** Cross-platform binary emulation framework (Python)
- **Stars:** 5k+

Qiling emulates binary execution at the OS level — it emulates syscalls, filesystem, and OS APIs so binaries run on a different OS or architecture than the host. Unlike QEMU (which emulates hardware), Qiling emulates the OS environment, giving full introspection hooks.

```python
from qiling import Qiling
from qiling.const import QL_VERBOSE

# Emulate a Linux x86-64 binary on Windows host (or any platform)
ql = Qiling(["./target_binary", "arg1"], "/path/to/rootfs/x8664_linux",
            verbose=QL_VERBOSE.DEBUG)

# Hook a syscall
def my_read_hook(ql, fd, buf, count):
    print(f"read({fd}, buf, {count}) called")
    return 0

ql.os.set_syscall("read", my_read_hook)

# Hook an address
def hook_at_addr(ql):
    rax = ql.arch.regs.rax
    print(f"Reached 0x401234, RAX = {hex(rax)}")

ql.hook_address(hook_at_addr, 0x401234)

# Hook memory access
def mem_write_hook(ql, access, addr, size, value):
    print(f"Memory write to {hex(addr)}: {hex(value)}")

ql.hook_mem_write(mem_write_hook)

ql.run()
```

```python
# Emulate Windows PE on Linux
ql = Qiling(["./malware.exe"], "/path/to/rootfs/x8664_windows")

# Intercept Windows API calls
def intercept_CreateFileA(ql):
    filename_ptr = ql.arch.regs.rcx
    filename = ql.mem.string(filename_ptr)
    print(f"CreateFileA called with: {filename}")

ql.os.set_api("CreateFileA", intercept_CreateFileA)
ql.run()
```

**Supported architectures:** x86, x86-64, ARM, ARM64, MIPS, RISC-V, 8086
**Supported OSes:** Linux, Windows, macOS, FreeBSD, DOS, EFI, MBR

### PANDA — Platform for Architecture-Neutral Dynamic Analysis

- **Repository:** https://github.com/panda-re/panda
- **License:** GPL v2
- **Type:** QEMU-based whole-system analysis platform
- **Stars:** 2.5k+

PANDA extends QEMU to provide record-and-replay with analysis plugins. Record a full system execution (every instruction, memory access, syscall), then replay it multiple times with different analysis plugins — without re-running the actual workload.

```python
# PyPANDA API
from pandare import Panda

panda = Panda(generic="x86_64")

@panda.cb_insn_exec
def insn_exec(env, pc):
    # Called for every instruction executed
    print(f"PC: {hex(pc)}")
    return 0

@panda.cb_on_sys_read_enter
def sys_read(env, pc, fd, buf, count):
    print(f"read({fd}, ..., {count})")

panda.run()
```

**PANDA plugins (C/C++):**
- `taint2` — taint tracking through entire execution
- `callstack_instr` — full call stack at every instruction
- `syscalls2` — system call logging
- `osi` — OS introspection (process list, memory maps)
- `coverage` — code coverage recording

### PyREBox

- **Repository:** https://github.com/Cisco-Talos/pyrebox
- **Authors:** Cisco Talos
- **License:** GPL v2
- **Type:** QEMU-based scriptable sandbox for malware analysis (Python)

PyREBox is a Python-scriptable sandbox built on QEMU for interactive malware analysis. Similar to PANDA but focused on Python scripting and malware analysis workflows.

```python
# PyREBox script
from api import *

def new_process_cb(pid, pgd, name):
    print(f"New process: {name} (PID {pid})")

def syscall_cb(params):
    print(f"Syscall {params['name']} from PID {params['pid']}")

register_callback(CallbackManager.CREATEPROC_CB, new_process_cb)
register_callback(CallbackManager.SYSCALL_CB, syscall_cb)
```

### LibVMI

- **Website:** https://libvmi.com
- **Repository:** https://github.com/libvmi/libvmi
- **License:** LGPL v3
- **Type:** Virtual machine introspection library

LibVMI provides OS-agnostic access to a running VM's memory from outside the VM — without installing anything inside the guest. Used for forensics, rootkit detection, and intrusion detection at the hypervisor level.

```c
#include <libvmi/libvmi.h>

vmi_instance_t vmi;
vmi_init_complete(&vmi, "vm-name", VMI_INIT_DOMAINNAME, NULL,
                  VMI_CONFIG_GLOBAL_FILE_ENTRY, NULL, NULL);

// Read kernel's process list from outside the VM
addr_t list_head;
vmi_read_addr_ksym(vmi, "init_task", &list_head);

// Walk process list
addr_t current = list_head;
do {
    char *name = vmi_read_str_va(vmi, current + OFFSET_NAME, 0);
    printf("Process: %s\n", name);
    vmi_read_addr_va(vmi, current + OFFSET_TASKS, 0, &current);
} while (current != list_head);

vmi_destroy(vmi);
```

---

## 5. Binary Lifting & Recompilation

### remill

- **Repository:** https://github.com/lifting-bits/remill
- **License:** Apache 2.0
- **Type:** Binary-to-LLVM IR lifter

remill lifts machine code (x86, x86-64, ARM, AArch64, MIPS) to LLVM IR. It models each instruction's semantics precisely in LLVM IR, enabling downstream LLVM-based analysis, optimization, and recompilation.

```
Binary (x86-64 .exe)
    ↓ remill lifts
LLVM IR (semantically equivalent)
    ↓ LLVM analysis passes
    → Optimize, instrument, analyze, recompile to any target
```

### McSema

- **Repository:** https://github.com/lifting-bits/mcsema
- **License:** Apache 2.0
- **Type:** Full binary decompilation to LLVM IR + recompilation

McSema uses remill to lift entire binary executables to LLVM IR, enabling:
- Recompiling an x86 binary for ARM
- Adding instrumentation (coverage, sanitizers) to stripped binaries
- Running LLVM-based static analysis on binary code

```bash
# Disassemble binary (IDA or Binary Ninja frontend)
mcsema-disass --os linux --arch amd64 --binary ./target \
  --output target.cfg --entrypoint main

# Lift to LLVM IR
mcsema-lift-9.0 --os linux --arch amd64 --cfg target.cfg \
  --output target.bc

# Recompile
clang -o target_lifted target.bc -lmcsema_rt_linux_amd64
```

### medusa

- **Repository:** https://github.com/wisk/medusa
- **License:** MIT
- **Type:** Interactive disassembler / binary analysis framework (C++)

medusa is a modular, cross-platform disassembler with plugin support for architectures and OS formats. Designed as a programmatic alternative to IDA for scriptable analysis workflows.

---

## 6. Go Binary Analysis

Go binaries strip symbol information by default and include the entire runtime, making standard RE tools less effective. These tools are specialized for Go binary analysis.

### GoReSym

- **Repository:** https://github.com/mandiant/GoReSym
- **Authors:** Mandiant
- **License:** Apache 2.0
- **Type:** Go binary symbol recovery

GoReSym recovers function names, source file paths, and line number information from stripped Go binaries — information that the Go runtime keeps even when symbols are stripped.

```bash
# Install
go install github.com/mandiant/GoReSym@latest

# Recover symbols from stripped Go binary
GoReSym ./go_binary

# Output JSON with recovered symbols
GoReSym -d ./go_binary    # Include data symbols
GoReSym -t ./go_binary    # Include type information

# Apply to IDA Pro: GoReSym outputs a JSON that can be
# fed to an IDA script to rename all functions
```

### redress

- **Repository:** https://github.com/goretk/redress
- **License:** GPL v3
- **Type:** Go binary analysis tool (CLI)

redress extracts information from Go binaries: package list, function list, compiler version, Go version, build ID, and type information.

```bash
go install github.com/goretk/redress@latest

redress ./go_binary            # Summary
redress -src ./go_binary       # Source file info
redress -packages ./go_binary  # Package list
redress -version ./go_binary   # Go version info
```

### IDAGolangHelper

- **Repository:** https://github.com/sibears/IDAGolangHelper
- **License:** MIT
- **Type:** IDA Pro plugin for Go binary analysis

IDA Pro plugin that automatically renames Go functions based on recovered symbol information, restoring readable function names in IDA's disassembly.

```python
# Install: copy to IDA plugins directory
# Run from IDA: Edit → Plugins → Go Helper → Rename functions
# Works with GoReSym output or standalone symbol recovery
```

### garble

- **Repository:** https://github.com/burrowers/garble
- **License:** BSD-3-Clause
- **Type:** Go binary obfuscation tool

garble obfuscates Go binaries at compile time — scrambles symbol names, control flow, and string literals. Useful for understanding what a hardened Go binary has done to defeat analysis.

```bash
go install mvdan.cc/garble@latest

# Build obfuscated binary
garble build ./...
garble -literals build ./...       # Also obfuscate string literals
garble -seed=random build ./...    # Random obfuscation seed

# Obfuscation techniques:
#   Function/variable names → random identifiers
#   String literals → runtime-decrypted
#   Control flow → flattened
#   Import paths → scrambled
```

---

## 7. Memory & Introspection

### MemProcFS

- **Repository:** https://github.com/ufrisk/MemProcFS
- **License:** AGPL v3
- **Type:** Memory process filesystem — mount RAM dump as filesystem
- **Stars:** 3k+

MemProcFS mounts a physical memory dump (or live memory via DMA) as a virtual filesystem. Every process, its memory, handles, modules, and registry appear as files and directories — enabling analysis with standard file tools.

```bash
# Mount a memory dump as filesystem
MemProcFS -device memory.dmp -mount /mnt/mem

# Browse the virtual filesystem:
ls /mnt/mem/
# proc/     sys/    forensic/    misc/

ls /mnt/mem/proc/
# 1234-explorer.exe/   4-System/   ...

# View process memory regions
cat /mnt/mem/proc/1234-explorer.exe/maps.txt

# Dump a specific module
cp /mnt/mem/proc/1234-explorer.exe/modules/kernel32.dll /tmp/

# View handles
cat /mnt/mem/proc/1234-explorer.exe/handles.txt

# Registry hives
ls /mnt/mem/registry/

# Process heap
cat /mnt/mem/proc/1234-explorer.exe/heap/
```

**Supported sources:** WinPmem, LiME, VMware .vmem, Hyper-V, DMA via FPGA, raw memory files.

### PINCE

- **Repository:** https://github.com/korcankaraokcu/PINCE
- **License:** GPL v3
- **Type:** Linux process memory analysis GUI (GDB frontend)

PINCE (PINCE Is Not Cheat Engine) is a Linux equivalent of Cheat Engine — a GUI memory scanner and editor that hooks GDB for process inspection. Useful for game hacking, crash analysis, and runtime binary analysis on Linux.

```
Features:
  - Memory scanning (find specific values — like Cheat Engine)
  - Memory editor (modify values at runtime)
  - Pointer scanning (find pointer chains to stable addresses)
  - Function injection
  - Tracing (instruction trace, call trace)
  - Code injection
  - Register view/edit
  - Watchpoints
```

---

## 8. File Format Parsers

### python-pefile

- **Repository:** https://github.com/erocarrera/pefile
- **License:** MIT
- **Type:** PE (Portable Executable) file parser — Python library
- **PyPI:** `pip install pefile`

```python
import pefile

pe = pefile.PE("./malware.exe")

# Headers
print(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
print(pe.FILE_HEADER.Machine)          # 0x8664 = x86-64, 0x14c = x86

# Sections
for section in pe.sections:
    print(section.Name.decode().rstrip('\x00'),
          hex(section.VirtualAddress),
          section.SizeOfRawData)

# Imports
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    print(entry.dll.decode())
    for imp in entry.imports:
        print(f"  {imp.name.decode() if imp.name else 'ordinal'}")

# Exports
for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
    print(exp.name.decode(), hex(exp.address))

# Resources
pe.parse_data_directories()
for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
    print(resource_type.name, resource_type.id)

# Check for suspicious characteristics
print("Is packed?", pe.is_exe())
print("Signed:", pe.verify_checksum())

# Dump to JSON
import json
print(json.dumps(pe.dump_dict(), indent=2))
```

### Kaitai Struct

- **Website:** https://kaitai.io
- **Repository:** https://github.com/kaitai-io/kaitai_struct
- **License:** MIT
- **Type:** Declarative binary format description language + compiler

Kaitai Struct lets you describe binary file formats in a YAML-based DSL (.ksy files), then auto-generates parsers in Python, Java, C++, Go, Ruby, and more. The web IDE provides interactive binary visualization.

```yaml
# PNG file format in Kaitai Struct (.ksy)
meta:
  id: png
  file-extension: png
  endian: be

seq:
  - id: magic
    contents: [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
  - id: chunks
    type: chunk
    repeat: eos

types:
  chunk:
    seq:
      - id: len
        type: u4
      - id: type
        type: str
        size: 4
        encoding: ASCII
      - id: body
        size: len
      - id: crc
        type: u4
```

```python
# Generated Python parser usage
from png import Png
data = Png.from_file("image.png")
for chunk in data.chunks:
    print(chunk.type, chunk.len)
```

---

## 9. Specialized Tools

### cemu

- **Repository:** https://github.com/hugsy/cemu
- **License:** MIT
- **Type:** Polyglot assembly + emulation IDE

cemu is a lightweight IDE for writing, assembling, and emulating shellcode across multiple architectures (x86, x86-64, ARM, ARM64, MIPS). Useful for shellcode development and testing without setting up a full VM.

```bash
pip install cemu
cemu    # GUI launches

# Supported: x86-16/32/64, ARM/Thumb, ARM64, MIPS, PowerPC, SPARC
# Write assembly in left panel
# See registers + memory update in real-time as code runs
# Generate shellcode as hex/python/C string
```

### Jakstab

- **Website:** https://www.jakstab.org
- **Type:** Static analysis platform for embedded firmware and binaries (Java)

Jakstab uses abstract interpretation to analyze binary executables — focusing on low-level code without OS libraries (firmware, bootloaders, embedded systems). Handles incomplete and obfuscated binaries where standard disassemblers fail.

### Panopticon

- **Repository:** https://github.com/das-labor/panopticon
- **License:** GPL v3
- **Type:** Disassembler with data flow analysis (Rust)

Panopticon is a Rust-based disassembler and binary analysis tool with built-in data flow analysis. Designed to be embeddable and scriptable.

### Pharos

- **Repository:** https://github.com/cmu-sei/pharos
- **Authors:** Carnegie Mellon University SEI
- **License:** MIT
- **Type:** Binary analysis framework for OO code (C++)

Pharos analyzes C++ binaries — recovering object-oriented structure (classes, virtual function tables, inheritance hierarchies) from compiled code. Integrates with IDA Pro.

```bash
# Object-oriented recovery
objdigger --serialize=out.json ./binary

# Function call analysis
fn2hash ./binary

# Defuse: detect use-before-init vulnerabilities
defuse ./binary
```

### Ponce

- **Repository:** https://github.com/illera88/Ponce
- **License:** MIT
- **Type:** IDA Pro plugin — symbolic execution and taint analysis

Ponce brings symbolic execution and taint analysis directly into IDA Pro's interface — right-click a register/memory location to taint it, then step through code watching how taint propagates. Uses the Triton symbolic execution engine.

```
Install: copy Ponce64.dll to IDA plugins directory
Usage:
  Ctrl+Shift+Z  — Symbolize register
  Ctrl+Shift+A  — Symbolize memory
  Right-click   — Taint/symbolize in context menu
  View → Ponce — see symbolic state panel
```

### miasm

- **Repository:** https://github.com/cea-sec/miasm
- **Authors:** CEA (French Alternative Energies and Atomic Energy Commission)
- **License:** GPL v2
- **Type:** Reverse engineering framework with DSE (Python)
- **Stars:** 3k+

miasm is a Python RE framework with its own IR (intermediate representation), symbolic execution (Dynamic Symbolic Execution), code obfuscation/deobfuscation, and JIT compilation.

```python
from miasm.analysis.machine import Machine
from miasm.analysis.binary import Container

# Load a binary
con = Container.from_stream(open("./binary", "rb"))
machine = Machine("x86_64")
dis_engine = machine.dis_engine

# Disassemble a function
asmcfg = dis_engine(con.bin_stream, loc_db=con.loc_db)
asmcfg.dis_multiblock(0x401234)

# Lift to IR
ira = machine.ira(con.loc_db)
for block in asmcfg.blocks:
    ira_block = ira.get_block(block)
    for assignblk in ira_block:
        for dst, src in assignblk.items():
            print(f"{dst} = {src}")

# Symbolic execution
from miasm.ir.symbexec import SymbolicExecutionEngine
sb = SymbolicExecutionEngine(ira)
sb.run_block_at(ira_cfg, 0x401234)
print(sb.symbols)
```

---

## 10. Tool Selection Guide

### By Task

| Task | Primary Tools |
|------|-------------|
| **Quick disassembly** | radare2 (`r2 -A binary; pdf @main`), objdump |
| **Full decompilation** | Binary Ninja (HLIL), Ghidra (see RE doc), IDA Pro |
| **Windows malware** | x64dbg + Ghidra, Binary Ninja |
| **Linux binary exploitation** | GDB + pwndbg, pwntools |
| **macOS RE** | LLDB, Binary Ninja, Ghidra |
| **CTF binary challenges** | angr (auto-solve), pwndbg, Binary Ninja |
| **Go binary RE** | GoReSym + IDAGolangHelper or Binary Ninja |
| **Firmware analysis** | Qiling, Jakstab, radare2 |
| **Malware dynamic analysis** | PyREBox, PANDA, Qiling |
| **Cross-arch emulation** | Qiling, PANDA (QEMU-based) |
| **Symbolic execution** | angr, Ponce (IDA), BinCAT (IDA), miasm |
| **Windows memory forensics** | MemProcFS |
| **PE parsing** | python-pefile |
| **Binary format reverse** | Kaitai Struct |
| **Shellcode development** | cemu |
| **Runtime process analysis (Linux)** | PINCE, GDB + pwndbg |

### By Experience Level

| Level | Start With |
|-------|-----------|
| Beginner | x64dbg (Windows), GDB + pwndbg (Linux), radare2 basics |
| Intermediate | Binary Ninja, angr for CTF automation |
| Advanced | PANDA/Qiling for malware, miasm/BAP for research, LibVMI for forensics |

---

## See Also

- [Reverse Engineering](reverse-engineering.md) — Ghidra, Frida, IDA Pro, dynamic instrumentation
- [Exploit Development](exploit-development.md) — Using these tools for vulnerability research
- [Drivers & DLLs](../fundamentals/drivers-and-dlls.md) — PE format internals
- [Compilers & Interpreters](../fundamentals/compilers-and-interpreters.md) — What these tools are reading
