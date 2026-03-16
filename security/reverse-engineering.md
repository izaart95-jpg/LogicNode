# Reverse Engineering

Static analysis, dynamic instrumentation, disassemblers, debuggers, and RE workflows. For deeper coverage of binary analysis frameworks (angr, Qiling, PANDA, miasm, etc.) see [Binary Analysis](binary-analysis.md).

---

## Table of Contents
1. [Ghidra](#1-ghidra)
2. [IDA Pro](#2-ida-pro)
3. [x64dbg](#3-x64dbg)
4. [Radare2](#4-radare2)
5. [Binary Ninja](#5-binary-ninja)
6. [GDB](#6-gdb)
7. [LLDB](#7-lldb)
8. [Frida](#8-frida)
9. [Frida Practical Examples](#9-frida-practical-examples)
10. [RE Workflow Reference](#10-re-workflow-reference)
11. [Platform-Specific Notes](#11-platform-specific-notes)

---

## 1. Ghidra

- **Website:** https://ghidra-sre.org
- **Developer:** NSA (open-sourced 2019)
- **License:** Apache 2.0
- **Platform:** Windows, Linux, macOS (Java-based)
- **Price:** Free

The NSA's internal reverse engineering suite, open-sourced in 2019. Ghidra is a full-featured disassembler + decompiler + analysis platform. Its decompiler output is competitive with IDA Pro's Hex-Rays at no cost, making it the default choice for most open-source RE work.

### Features

- Multi-architecture decompiler (x86, ARM, MIPS, PPC, RISC-V, 68k...)
- Code browser with cross-references, call graphs, type inference
- Multi-user collaboration (shared project server)
- Version tracking — track changes to analysis over time
- Script API in Java and Python (Jython)
- Scripting console for automation
- Symbol importation from PDB files
- DWARF debug info parsing
- Headless analysis mode (automation without GUI)

### Installation and Usage

```bash
# Download from https://ghidra-sre.org
# Requires Java 17+

# Launch
./ghidraRun             # Linux/macOS
ghidraRun.bat           # Windows

# Headless analysis
./support/analyzeHeadless /path/to/project ProjectName \
  -import ./binary \
  -postScript MyAnalysisScript.java \
  -scriptPath /path/to/scripts
```

### Ghidra Python Scripting (Jython)

```python
# Run from Script Manager or headless mode
from ghidra.program.model.symbol import SymbolType
from ghidra.app.decompiler import DecompInterface

# List all functions
fm = currentProgram.getFunctionManager()
for func in fm.getFunctions(True):
    print(func.getName(), func.getEntryPoint())

# Decompile a function
decomp = DecompInterface()
decomp.openProgram(currentProgram)
func = getGlobalFunctions("main")[0]
result = decomp.decompileFunction(func, 30, monitor)
print(result.getDecompiledFunction().getC())

# Find all strings referencing "password"
for s in currentProgram.getListing().getDefinedData(True):
    if hasattr(s, 'getValue') and "password" in str(s.getValue()).lower():
        print(s.getAddress(), s.getValue())

# Rename a function
func = getFunctionAt(toAddr(0x401234))
func.setName("decrypt_payload", SourceType.USER_DEFINED)

# Add comment
setPlateComment(toAddr(0x401234), "Key derivation starts here")
```

---

## 2. IDA Pro

- **Website:** https://hex-rays.com
- **License:** Commercial (IDA Free available for limited use)
- **Type:** Industry-standard disassembler and decompiler

IDA Pro is the industry standard, used extensively in professional malware analysis and vulnerability research. Its Hex-Rays decompiler produces high-quality pseudocode. IDA Free (limited version) is available for non-commercial use.

### Key Concepts

```
IDA database (.idb / .i64):
  Stores all analysis — functions, names, comments, types
  Load once, annotate over time

Navigation:
  G — Go to address
  N — Rename (function, variable, label)
  : — Add comment
  ; — Add repeatable comment
  Y — Set type (for function signature or variable)
  H — Toggle hex/decimal
  X — Cross-references TO this item
  Ctrl+X — Cross-references FROM this item

Views:
  IDA View — disassembly
  Pseudocode (F5) — decompiler output (Hex-Rays license)
  Structures — type definitions
  Enums — enumeration types
  Imports / Exports
  Strings — all string literals
  Functions — full function list
```

### IDAPython

```python
import idc, idautils, idaapi

# List all functions
for func in idautils.Functions():
    print(hex(func), idc.get_func_name(func))

# Get disassembly
for insn in idautils.FuncItems(here()):
    print(hex(insn), idc.GetDisasm(insn))

# Rename function
idc.set_name(0x401234, "decrypt_payload", idc.SN_CHECK)

# Add comment
idc.set_cmt(0x401234, "Key derivation", 0)

# Cross-references TO address
for ref in idautils.CodeRefsTo(0x401234, False):
    print(hex(ref))

# Patch bytes
idc.patch_byte(0x401234, 0x90)   # NOP
idc.patch_bytes(0x401234, b'\x90\x90\x90')

# Read/write memory
data = idc.get_bytes(0x401234, 16)
```

---

## 3. x64dbg

- **Website:** https://x64dbg.com
- **License:** MIT
- **Platform:** Windows only
- **Download:** https://github.com/x64dbg/x64dbg/releases

The standard open-source Windows user-mode debugger. Covers both x64 (x64dbg.exe) and x86 (x32dbg.exe). See [Binary Analysis](binary-analysis.md) for detailed coverage.

### Quick Reference

```
F7    Step into (instruction level)
F8    Step over
F9    Run
F2    Toggle software breakpoint
Ctrl+F2  Restart
Alt+F9   Execute until return
Ctrl+G   Go to address
Ctrl+B   Memory breakpoints view
Spacebar  Assemble at cursor (patch)
Right-click → Follow in dump/disassembler/stack

Key plugins:
  ScyllaHide     — Anti-anti-debug bypass
  xAnalyzer      — Automatic function analysis
  ret-sync       — Sync with IDA/Ghidra/Binary Ninja
  Strings        — Enhanced string extraction
  APIBreak       — Break on specific Windows API calls
```

### ScyllaHide — Anti-Anti-Debug

```
Most packers and malware detect debuggers via:
  IsDebuggerPresent() → PEB.BeingDebugged flag
  CheckRemoteDebuggerPresent()
  NtQueryInformationProcess(ProcessDebugPort)
  Timing checks (RDTSC)
  Heap flags / Heap Force Flags in PEB
  Exception handling quirks
  Parent process name check

ScyllaHide bypasses all of these transparently.
Install: drop ScyllaHide.dp64 into x64dbg plugins folder
```

---

## 4. Radare2

- **Repository:** https://github.com/radareorg/radare2
- **License:** LGPL v3
- **Type:** Complete RE framework (CLI)

See [Binary Analysis](binary-analysis.md) for full coverage including r2pipe Python API. Quick command reference:

```bash
r2 -A ./binary        # Open and auto-analyze

# Essential commands
afl           # List functions
pdf @main     # Disassemble main
iz            # List strings
ii            # Imports
iS            # Sections
s 0x401234    # Seek to address
V             # Visual mode  (VV for graph)
db 0x401234   # Breakpoint (debug mode: r2 -d ./binary)
dc            # Continue
dr            # Registers
```

---

## 5. Binary Ninja

- **Website:** https://binary.ninja
- **Free tier:** https://cloud.binary.ninja
- **Type:** Commercial disassembler + decompiler with Python API

Multi-level IL (LLIL → MLIL → HLIL) with clean Python API. See [Binary Analysis](binary-analysis.md) for full Python API coverage.

```python
import binaryninja as bn

bv = bn.open_view("./binary")
bv.update_analysis_and_wait()

# Decompile function
for func in bv.functions:
    for insn in func.hlil.instructions:
        print(insn)

# Find all calls to malloc
malloc_sym = bv.get_symbol_by_raw_name("malloc")
if malloc_sym:
    for ref in bv.get_code_refs(malloc_sym.address):
        print(hex(ref.address), ref.function.name)
```

---

## 6. GDB

See [Binary Analysis](binary-analysis.md) for full GDB reference including Python API, pwndbg/GEF setup, and all commands.

**Essential quick reference:**

```bash
gdb ./binary
(gdb) break main; run
(gdb) ni / si                 # Next instruction / step into
(gdb) x/10i $rip              # Examine instructions at RIP
(gdb) info registers
(gdb) x/20wx $rsp             # Stack contents
(gdb) bt                      # Backtrace
(gdb) layout asm              # TUI mode
```

---

## 7. LLDB

See [Binary Analysis](binary-analysis.md) for full LLDB reference. Default debugger on macOS/Xcode.

```bash
lldb ./binary
(lldb) breakpoint set --name main
(lldb) process continue
(lldb) register read
(lldb) memory read --format x --count 20 $sp
(lldb) disassemble --name main
(lldb) bt
```

---

## 8. Frida

- **Website:** https://frida.re
- **Repository:** https://github.com/frida/frida
- **License:** wxWindows Library Licence (permissive)
- **Type:** Dynamic instrumentation toolkit
- **Platforms:** Windows, macOS, Linux, iOS, Android

Frida injects JavaScript into running processes, letting you hook functions, intercept arguments and return values, modify memory, and call arbitrary functions — all at runtime without recompiling.

### Installation

```bash
pip install frida-tools
pip install frida

# Android: push frida-server to device
adb push frida-server-16.x.x-android-arm64 /data/local/tmp/frida-server
adb shell chmod +x /data/local/tmp/frida-server
adb shell /data/local/tmp/frida-server &
```

### Core Concepts

```javascript
// Interceptor.attach: hook a function
Interceptor.attach(Module.findExportByName("libc.so", "open"), {
    onEnter: function(args) {
        // Called when function is entered
        console.log("open() called with path: " + args[0].readUtf8String());
        this.path = args[0].readUtf8String();  // save for onLeave
    },
    onLeave: function(retval) {
        // Called when function returns
        console.log("open() returned fd: " + retval.toInt32());
        // Modify return value:
        // retval.replace(ptr(-1));  // make it fail
    }
});

// Hook by address
var target_addr = ptr("0x401234");
Interceptor.attach(target_addr, {
    onEnter: function(args) {
        console.log("Hit 0x401234");
        console.log("arg0 = " + args[0]);
        console.log("RIP = " + this.context.rip);
    }
});

// Read / write memory
var addr = ptr("0x402000");
var data = addr.readByteArray(16);
addr.writeByteArray([0x90, 0x90, 0x90]);   // Write NOPs
console.log(hexdump(addr, { length: 32 }));

// Call a function directly
var func = new NativeFunction(ptr("0x401234"), 'int', ['int', 'pointer']);
var result = func(42, Memory.allocUtf8String("hello"));
```

### Frida CLI Tools

```bash
# List running processes
frida-ps

# Android: list apps
frida-ps -U         # USB device
frida-ps -U -a      # All apps (including background)

# Attach to process
frida -p PID script.js
frida -n "process_name" script.js
frida -U -f "com.app.id" script.js   # Spawn Android app

# REPL mode (interactive)
frida -p PID
> Module.findExportByName(null, "malloc")
> Process.enumerateModules()

# Run a script
frida -p PID -l my_script.js --no-pause

# Trace function calls
frida-trace -n Chrome -i "open"          # Trace libc open
frida-trace -n Chrome -i "Crypto*"       # Wildcard trace
frida-trace -U -f com.app.id -i "Java.*" # Android Java
```

---

## 9. Frida Practical Examples

### Android SSL Pinning Bypass

```javascript
// Bypass certificate pinning in Android apps
Java.perform(function() {
    // TrustManager bypass
    var TrustManager = Java.registerClass({
        name: "com.bypass.TrustManager",
        implements: [Java.use("javax.net.ssl.X509TrustManager")],
        methods: {
            checkClientTrusted: function(chain, authType) {},
            checkServerTrusted: function(chain, authType) {},
            getAcceptedIssuers: function() { return []; }
        }
    });

    var SSLContext = Java.use("javax.net.ssl.SSLContext");
    SSLContext.init.overload(
        "[Ljavax.net.ssl.KeyManager;",
        "[Ljavax.net.ssl.TrustManager;",
        "java.security.SecureRandom"
    ).implementation = function(km, tm, sr) {
        this.init(km, [TrustManager.$new()], sr);
    };

    // OkHttp pinning bypass
    try {
        var CertificatePinner = Java.use("okhttp3.CertificatePinner");
        CertificatePinner.check.overload("java.lang.String", "java.util.List")
            .implementation = function(hostname, peerCertificates) {
                console.log("Bypassed OkHttp cert pin for: " + hostname);
            };
    } catch(e) {}
});
```

### Hook Java Method (Android)

```javascript
Java.perform(function() {
    var Activity = Java.use("android.app.Activity");
    Activity.onCreate.overload("android.os.Bundle").implementation = function(bundle) {
        console.log("Activity.onCreate called: " + this.getClass().getName());
        this.onCreate(bundle);
    };

    // Hook string decrypt function
    var DecryptClass = Java.use("com.app.crypto.Decrypt");
    DecryptClass.decrypt.overload("java.lang.String").implementation = function(ciphertext) {
        var result = this.decrypt(ciphertext);
        console.log("Decrypted: " + ciphertext + " → " + result);
        return result;
    };
});
```

### Trace All Native Calls

```javascript
// Trace every function call in a library
Process.enumerateModules().forEach(function(mod) {
    if (mod.name.includes("target_library")) {
        mod.enumerateExports().forEach(function(exp) {
            if (exp.type === "function") {
                Interceptor.attach(exp.address, {
                    onEnter: function(args) {
                        console.log("[+] " + exp.name + " called");
                    }
                });
            }
        });
    }
});
```

---

## 10. RE Workflow Reference

### Static Analysis Workflow

```
1. Identify binary type
   file ./binary                      # ELF/PE/Mach-O, arch, stripped?
   strings ./binary | grep -i pass    # Quick string recon
   objdump -f ./binary                # File headers

2. Import into disassembler
   Ghidra: create project → import → auto-analyze → decompile
   IDA: open file → auto-analyze → F5 for pseudocode
   Binary Ninja: open file → analysis completes → view HLIL

3. Orient yourself
   Check main() or entry point
   Check imports — what APIs does it use?
   Check strings — hardcoded IPs, URLs, keys, debug messages
   Check for anti-debug / anti-analysis code

4. Understand the core logic
   Follow data flow from user input
   Look for crypto (high entropy data, math patterns)
   Look for network communication
   Rename functions as you understand them

5. Document findings
   Comment addresses, rename functions
   Save disassembler database
```

### Dynamic Analysis Workflow

```
1. Set up isolated environment
   VM (VMware/VirtualBox) isolated from network
   Snapshot before running

2. Monitor before running
   Process Monitor (Windows) — watch file/registry/network
   Wireshark/Zeek — capture network traffic
   Procmon — API calls

3. Run the target
   Execute with debugger attached (x64dbg/GDB)
   Set breakpoints at: CreateFile, WriteFile, connect, CreateProcess

4. Observe behavior
   What files does it create/modify?
   What network connections?
   What processes spawned?
   What registry keys touched?

5. Deep dive with Frida
   Hook interesting functions found in static analysis
   Capture decrypted strings, keys, plaintext network data
```

---

## 11. Platform-Specific Notes

### Windows Malware RE Checklist

```
Static:
  pefile — check imports (suspicious: VirtualAlloc, WriteProcessMemory, CreateRemoteThread)
  strings — look for URLs, IPs, mutex names, registry keys
  entropy analysis — high entropy sections = packed/encrypted
  Authenticode signature check: sigcheck.exe (Sysinternals)

Dynamic (x64dbg):
  ScyllaHide enabled
  Break on: CreateProcess, VirtualAlloc+WriteProcessMemory (injection)
  Break on: WSAConnect, connect (network)
  Break on: CryptDecrypt, CryptImportKey (crypto)
  Watch: PEB traversal (manual DLL resolution)
```

### Android APK RE Checklist

```
Static:
  apktool d app.apk      # Decompile to Smali
  jadx-gui app.apk       # Java decompilation (better than dex2jar)
  grep -r "password\|key\|secret" ./   # Find hardcoded secrets
  Check AndroidManifest.xml — permissions, activities, providers

Dynamic (Frida):
  SSL pinning bypass
  Hook SharedPreferences (sensitive data storage)
  Hook crypto functions
  Hook network (OkHttp, Retrofit)
  Use objection: objection -g com.app.id explore
```

---

## See Also

- [Binary Analysis](binary-analysis.md) — angr, Qiling, PANDA, GDB/LLDB in depth, MemProcFS
- [Exploit Development](exploit-development.md) — Using RE for vulnerability research
- [Drivers & DLLs](../fundamentals/drivers-and-dlls.md) — PE/ELF format internals
- [Compilers & Interpreters](../fundamentals/compilers-and-interpreters.md) — What the disassembler sees
