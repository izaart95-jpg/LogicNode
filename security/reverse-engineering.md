# Reverse Engineering

A comprehensive guide to reverse engineering tools and techniques for analyzing binaries, malware, firmware, and applications. This document covers the fundamentals of static and dynamic analysis, along with detailed usage of leading tools including x64dbg, Ghidra, Frida, and IDA Pro.

> **Disclaimer:** All tools, techniques, and examples described in this document are intended for **authorized security research and educational purposes only**. Reverse engineering software may be subject to legal restrictions depending on your jurisdiction, licensing agreements, and applicable laws (e.g., DMCA, CFAA). Always ensure you have proper authorization before analyzing any software.

---

## Table of Contents

1. [What is Reverse Engineering?](#1-what-is-reverse-engineering)
2. [x64dbg](#2-x64dbg)
3. [Ghidra](#3-ghidra)
4. [Frida](#4-frida)
5. [IDA Pro](#5-ida-pro)
6. [Comparison Table](#6-comparison-table)
7. [See Also](#7-see-also)

---

## 1. What is Reverse Engineering?

Reverse engineering (RE) is the process of analyzing software or hardware to understand its design, functionality, and behavior without access to the original source code or documentation. In cybersecurity, RE is a critical skill for malware analysis, vulnerability research, exploit development, and software security auditing.

### 1.1 Static vs Dynamic Analysis

| Approach | Description | Tools | Advantages | Disadvantages |
|----------|-------------|-------|------------|---------------|
| **Static Analysis** | Examining code/binary without executing it | Ghidra, IDA Pro, radare2, strings, objdump | Safe (no execution), full code coverage | Obfuscation/packing can hinder analysis, no runtime context |
| **Dynamic Analysis** | Observing the program during execution | x64dbg, Frida, strace, Process Monitor | See actual runtime behavior, bypass obfuscation | Risk of executing malicious code, may miss code paths |

Most real-world analysis combines both approaches: static analysis to understand structure, dynamic analysis to observe behavior and confirm hypotheses.

### 1.2 Common Targets

- **Malware:** Understanding capabilities, C2 communication, persistence mechanisms, indicators of compromise (IOCs)
- **Binaries:** Vulnerability research in compiled applications, patch diffing, protocol analysis
- **Firmware:** Embedded device analysis, extracting file systems, finding hardcoded credentials
- **Mobile Apps:** Android APK and iOS IPA analysis, API endpoint discovery, certificate pinning bypass

### 1.3 Legal Considerations

Reverse engineering legality varies by jurisdiction:

- **United States:** DMCA Section 1201 restricts circumvention of technological protection measures, but has exemptions for security research
- **European Union:** EU Directive 2009/24/EC allows decompilation for interoperability purposes
- **General Guidance:** RE for personal learning, interoperability, and authorized security testing is generally permitted; RE to bypass DRM, pirate software, or attack systems without authorization is illegal

Always consult applicable laws and licensing agreements before conducting reverse engineering work.

---

## 2. x64dbg

### 2.1 Overview

x64dbg is an open-source user-mode debugger for Windows, designed for analyzing 32-bit and 64-bit executables. It provides a modern, extensible interface and has become the go-to alternative to OllyDbg for Windows debugging.

- **Website:** https://x64dbg.com
- **Source:** https://github.com/x64dbg/x64dbg
- **License:** GPLv3
- **Platform:** Windows only

### 2.2 Installation

Download the latest release from the official website or GitHub. Extract the archive and run `x96dbg.exe` for the launcher, which provides both `x32dbg.exe` (32-bit) and `x64dbg.exe` (64-bit) debuggers.

```bash
# No traditional install needed — portable application
# Extract and run:
# x96dbg.exe   -> Launcher (selects x32 or x64)
# x32/x32dbg.exe -> 32-bit debugger
# x64/x64dbg.exe -> 64-bit debugger
```

### 2.3 UI Overview

The x64dbg interface is organized into key panels:

- **CPU View:** Disassembly, registers, stack, and dump side by side
- **Stack View:** Call stack and stack contents
- **Memory Map:** All loaded modules and memory regions
- **Breakpoints:** Hardware, software, and conditional breakpoints
- **References:** Cross-references and search results
- **Call Stack:** Function call trace

### 2.4 Basic Workflow

1. **Load Binary:** File -> Open or drag and drop the executable
2. **Set Breakpoints:** Right-click on an instruction -> Breakpoint -> Toggle, or press F2
3. **Run:** Press F9 to run to the next breakpoint
4. **Step Through:** F7 (step into), F8 (step over), Ctrl+F9 (run to return)
5. **Inspect Memory:** Follow addresses in dump, examine stack values
6. **Patch:** Modify instructions in-place for testing (Assemble with Space key)

### 2.5 Plugin Ecosystem

x64dbg supports a rich plugin ecosystem:

- **ScyllaHide:** Anti-anti-debug plugin (hides debugger from detection)
- **xAnalyzer:** Extended analysis plugin for better function recognition
- **SharpOD:** Advanced anti-debug bypass
- **Multiline Ultimate Assembler:** Inline assembler for patching
- Plugin manager available at: https://github.com/x64dbg/x64dbg/wiki/Plugins

### 2.6 x32dbg vs x64dbg

| Feature | x32dbg | x64dbg |
|---------|--------|--------|
| **Architecture** | 32-bit (x86) processes | 64-bit (x86_64) processes |
| **Use Case** | Legacy apps, 32-bit malware | Modern 64-bit applications |
| **Interface** | Identical | Identical |
| **Plugins** | Shared ecosystem | Shared ecosystem |

Use x32dbg for 32-bit targets and x64dbg for 64-bit targets. The launcher (`x96dbg.exe`) automatically selects the correct version.

---

## 3. Ghidra

### 3.1 Overview

Ghidra is a free, open-source software reverse engineering framework developed by the NSA (National Security Agency). Released publicly in 2019, it provides comprehensive disassembly, decompilation, and analysis capabilities rivaling commercial tools.

- **Website:** https://ghidra-sre.org
- **Source:** https://github.com/NationalSecurityAgency/ghidra
- **License:** Apache 2.0
- **Platforms:** Windows, Linux, macOS

### 3.2 Installation

Ghidra requires a Java Development Kit (JDK 17+).

```bash
# Install Java (Ubuntu/Debian)
sudo apt install openjdk-17-jdk

# Download Ghidra from the official GitHub releases
# https://github.com/NationalSecurityAgency/ghidra/releases

# Extract and run
unzip ghidra_*.zip
cd ghidra_*
./ghidraRun
```

### 3.3 Project Setup and Code Browser

1. **Create a Project:** File -> New Project -> Non-Shared Project
2. **Import Binary:** File -> Import File -> select target binary
3. **Auto-Analysis:** When prompted, accept default analyzers (or customize)
4. **Code Browser:** Double-click the imported file to open the main analysis window

The Code Browser contains:

- **Listing View:** Disassembly with labels, cross-references, and comments
- **Decompiler Window:** Pseudo-C output from the decompiler (side by side with assembly)
- **Symbol Tree:** Functions, labels, classes, namespaces
- **Data Type Manager:** Structures, enums, typedefs
- **Function Graph:** Visual control flow graph of the selected function

### 3.4 Key Analysis Features

- **Auto-Analysis:** Identifies functions, strings, data types, and cross-references automatically
- **Function Identification:** Signature matching against known libraries (FID — Function ID)
- **Cross-References (XREFs):** Navigate where functions and data are called/used
- **Type Propagation:** Infer and apply data types throughout the binary
- **Diffing:** Compare two binaries to identify changes (Version Tracking)

### 3.5 Ghidra Scripting

Ghidra supports scripting in Java and Python (Jython) for automating analysis tasks.

```python
# Ghidra Python script: List all functions in the binary
from ghidra.program.model.listing import FunctionManager

fm = currentProgram.getFunctionManager()
funcs = fm.getFunctions(True)
for func in funcs:
    print("Function: {} at {}".format(func.getName(), func.getEntryPoint()))
```

```bash
# Run Ghidra in headless mode for batch/automated analysis
./analyzeHeadless /path/to/project MyProject \
  -import /path/to/binary \
  -postScript MyScript.py \
  -scriptPath /path/to/scripts
```

### 3.6 Headless Mode

Headless mode allows batch processing without the GUI — useful for CI/CD pipelines, automated malware triage, and large-scale analysis. Scripts can import, analyze, and export results programmatically.

---

## 4. Frida

### 4.1 Overview

Frida is a dynamic instrumentation toolkit that lets you inject JavaScript (or other languages) into running processes on Windows, macOS, Linux, iOS, Android, and QNX. It is widely used for mobile application analysis, API monitoring, and security research.

- **Website:** https://frida.re
- **Source:** https://github.com/frida/frida
- **License:** wxWindows Library Licence

### 4.2 Installation

```bash
# Install Frida tools via pip
pip install frida-tools

# Verify installation
frida --version

# Install Frida Python bindings (if needed separately)
pip install frida
```

### 4.3 JavaScript API for Hooking

Frida uses a JavaScript API to hook and intercept function calls at runtime.

```javascript
// Hook a native function (e.g., open() on Linux)
Interceptor.attach(Module.findExportByName(null, "open"), {
    onEnter: function(args) {
        console.log("open() called with: " + Memory.readUtf8String(args[0]));
    },
    onLeave: function(retval) {
        console.log("open() returned: " + retval);
    }
});
```

### 4.4 Use Cases

- **Android App Analysis:** Hook Java methods, bypass certificate pinning, extract encryption keys
- **iOS Analysis:** Bypass jailbreak detection, intercept Objective-C messages
- **Windows:** Hook Win32 API calls, monitor registry access, trace crypto operations
- **Linux:** Trace system calls, intercept library functions, analyze server applications

### 4.5 Frida-Server Setup on Android

```bash
# Download frida-server for Android (match your device architecture)
# https://github.com/frida/frida/releases
# Example: frida-server-16.x.x-android-arm64

# Push to device
adb push frida-server-arm64 /data/local/tmp/frida-server
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"

# List running processes on the device
frida-ps -U

# Attach to a specific app
frida -U -n "com.example.app"
```

### 4.6 Example: Hook a Java Method on Android

```javascript
Java.perform(function() {
    var Activity = Java.use('com.example.app.MainActivity');
    Activity.secretFunction.implementation = function() {
        console.log('Function called!');
        return this.secretFunction();
    };
});
```

```bash
# Run a Frida script against an Android app
frida -U -l hook_script.js -n "com.example.app"

# Spawn and hook from the start
frida -U -l hook_script.js -f com.example.app --no-pause
```

### 4.7 Additional Frida Tools

- **frida-trace:** Automatically generate hooks for matching functions
- **frida-discover:** Discover internal functions in a running process
- **frida-ls-devices:** List all connected Frida-capable devices
- **Objection:** Runtime mobile exploration toolkit built on Frida (https://github.com/sensepost/objection)

---

## 5. IDA Pro

### 5.1 Overview

IDA Pro (Interactive Disassembler) is the industry-standard commercial disassembler and debugger. It has been the dominant tool in reverse engineering since the 1990s and is used by security researchers, government agencies, and malware analysts worldwide.

- **Website:** https://hex-rays.com/ida-pro/
- **Developer:** Hex-Rays
- **Platforms:** Windows, Linux, macOS

### 5.2 IDA Free vs IDA Pro vs IDA Home

| Feature | IDA Free | IDA Home | IDA Pro |
|---------|----------|----------|---------|
| **Price** | Free | ~$365/year | ~$1,400+/year |
| **Architectures** | x86, x64, ARM, MIPS | x86, x64, ARM, MIPS | 40+ processors |
| **Decompiler** | Cloud-based (limited) | Local (x86/x64/ARM) | Full Hex-Rays decompiler |
| **Debugging** | Local only | Local only | Local + remote debugging |
| **Plugins** | Limited | Full support | Full support |
| **Commercial Use** | No | No | Yes |

### 5.3 Basic Workflow

1. **Load Binary:** Drag and drop or File -> Open, IDA auto-detects format and architecture
2. **Initial Analysis:** IDA performs auto-analysis (function identification, string detection, type inference)
3. **Navigate:** Use the Functions window, Names window, or press G to go to an address
4. **Cross-References (XREFs):** Press X on any symbol to see all references to it
5. **Rename:** Press N to rename functions and variables for clarity
6. **Comment:** Press ; (repeatable) or : (non-repeatable) to add comments
7. **Graph View:** Press Space to toggle between linear and graph view

### 5.4 IDAPython Scripting

IDA Pro includes a powerful Python scripting interface for automating analysis.

```python
# IDAPython: Find all calls to a specific function
import idautils
import idc

target_func = "CreateFileW"
for addr in idautils.CodeRefsTo(idc.get_name_ea_simple(target_func), 0):
    func_name = idc.get_func_name(addr)
    print(f"Call to {target_func} from {func_name} at {hex(addr)}")
```

```python
# IDAPython: Rename functions matching a pattern
import idautils
import ida_funcs

for func_ea in idautils.Functions():
    func = ida_funcs.get_func(func_ea)
    name = ida_funcs.get_func_name(func_ea)
    if name.startswith("sub_"):
        # Custom logic to identify and rename functions
        print(f"Unnamed function at {hex(func_ea)}")
```

### 5.5 Hex-Rays Decompiler

The Hex-Rays decompiler transforms assembly code into readable pseudo-C code. Press F5 on any function to decompile. The decompiler supports:

- Variable type recovery and renaming
- Structure reconstruction
- Interactive refinement (change types, rename variables in decompiled view)
- Output synchronization with the disassembly view

---

## 6. Comparison Table

| Tool | Type | Platform | Open Source | Best For | Price |
|------|------|----------|-------------|----------|-------|
| **x64dbg** | Debugger | Windows | Yes (GPLv3) | Windows binary debugging, malware analysis | Free |
| **Ghidra** | Disassembler / Decompiler | Windows, Linux, macOS | Yes (Apache 2.0) | Static RE, multi-architecture analysis | Free |
| **Frida** | Dynamic Instrumentation | Cross-platform | Yes (wxWindows) | Mobile app analysis, runtime hooking | Free |
| **IDA Pro** | Disassembler / Debugger | Windows, Linux, macOS | No (Proprietary) | Professional RE, malware analysis | $1,400+/year |
| **IDA Free** | Disassembler | Windows, Linux, macOS | No (Freeware) | Basic static analysis, learning | Free |
| **radare2** | RE Framework | Cross-platform | Yes (LGPLv3) | CLI-based analysis, scripting | Free |
| **Binary Ninja** | Disassembler / Decompiler | Windows, Linux, macOS | No (Proprietary) | Modern UI, IL-based analysis | $299+ |

---

## 7. See Also

- [Penetration Testing Tools](penetration-testing-tools.md) — Core tools for network and application security testing
- [Web Application Security](web-application-security.md) — OWASP, training platforms, and web security resources
