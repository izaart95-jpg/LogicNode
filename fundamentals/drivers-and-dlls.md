# Drivers, DLLs & System Services

This document covers the software layer between hardware and applications — device drivers, shared libraries (DLLs/.so files), Windows services, Linux daemons, and how operating systems manage the interface between user code and hardware.

---

## Table of Contents
1. [Device Drivers](#1-device-drivers)
2. [Windows DLLs](#2-windows-dlls)
3. [Linux Shared Libraries (.so)](#3-linux-shared-libraries-so)
4. [Windows Services](#4-windows-services)
5. [Linux Daemons & systemd](#5-linux-daemons--systemd)
6. [The Dynamic Linker / Loader](#6-the-dynamic-linker--loader)
7. [Graphics Drivers Deep Dive](#7-graphics-drivers-deep-dive)
8. [Writing a Simple Driver (Linux)](#8-writing-a-simple-driver-linux)
9. [Debugging & Inspection Tools](#9-debugging--inspection-tools)

---

## 1. Device Drivers

A device driver is kernel-mode code that manages a specific hardware device. It translates generic OS requests into hardware-specific commands.

### Why Drivers Run in the Kernel

Hardware interaction requires:
- Direct memory-mapped I/O (reading/writing device registers at physical addresses)
- DMA (Direct Memory Access) setup — device transfers data to/from physical RAM
- Interrupt handling — hardware signals the CPU asynchronously
- Privileged instructions — only ring 0 can configure the MMU, IOAPIC, PCI config space

User-mode code cannot do any of these things. The driver acts as a trusted intermediary.

### Driver Architecture (General)

```
Application
    ↓ System call (open, read, write, ioctl)
VFS / Device subsystem (kernel)
    ↓ Generic interface
Block driver / Character driver / Network driver
    ↓ Device-specific commands
PCI/USB/SATA/I2C hardware bus abstraction
    ↓ Physical transactions
Hardware (disk controller, GPU, NIC, keyboard...)
```

### Driver Types

**Character drivers:** Byte-stream devices. Read/write sequentially. Examples: serial ports, keyboards, mice, terminal (tty).

**Block drivers:** Fixed-size block devices. Random access. Buffered through page cache. Examples: hard drives, SSDs, NVMe.

**Network drivers:** Packet-based. Bypass the file system entirely. Use kernel networking stack (sk_buff). Examples: Ethernet, Wi-Fi.

**Platform drivers:** Devices on the SoC (System on Chip) bus, not PCI. Used heavily in ARM/embedded Linux.

**Virtual drivers:** No physical hardware. Examples: loopback network interface, /dev/null, /dev/urandom, /dev/loop (loop block device).

### Driver Model (Linux)

```
Every device in Linux is modeled by three structures:

struct bus_type:    Represents the bus (PCI, USB, SPI, I2C, platform...)
struct device:      Represents a physical or logical device on the bus
struct device_driver: Code that handles this device

Device binding:
  When a device is detected (PCI probe, USB plug-in):
    → kernel calls probe() functions of registered drivers
    → driver with matching device_id claims the device
    → driver initializes hardware, registers it with appropriate subsystem

Example: plug in a USB keyboard:
  USB bus detects new device
  Kernel tries to match USB vendor:product against registered USB drivers
  usbhid driver matches → its probe() is called
  probe() initializes HID input layer, registers /dev/input/eventN
  keyboard is now usable
```

### PCI Driver Example (Linux, simplified)

```c
#include <linux/module.h>
#include <linux/pci.h>

// Table of supported PCI device IDs
static const struct pci_device_id mydriver_ids[] = {
    { PCI_DEVICE(0x1234, 0x5678) },   // vendor:device pair
    { 0, }
};
MODULE_DEVICE_TABLE(pci, mydriver_ids);

// Called when kernel finds a matching device
static int mydriver_probe(struct pci_dev *pdev, const struct pci_device_id *id) {
    int err;

    // Enable PCI device
    err = pci_enable_device(pdev);
    if (err) return err;

    // Request exclusive access to BARs (Base Address Registers = memory regions)
    err = pci_request_regions(pdev, "mydriver");
    if (err) goto disable_device;

    // Map device memory into kernel virtual address space
    void __iomem *regs = pci_iomap(pdev, 0, 0);  // BAR 0

    // Enable DMA
    pci_set_master(pdev);

    // Initialize hardware via register writes
    iowrite32(0x01, regs + CONTROL_REG);

    printk(KERN_INFO "mydriver: device initialized\n");
    return 0;

disable_device:
    pci_disable_device(pdev);
    return err;
}

// Called when device is removed
static void mydriver_remove(struct pci_dev *pdev) {
    pci_release_regions(pdev);
    pci_disable_device(pdev);
}

static struct pci_driver mydriver = {
    .name     = "mydriver",
    .id_table = mydriver_ids,
    .probe    = mydriver_probe,
    .remove   = mydriver_remove,
};

module_pci_driver(mydriver);   // Macro: module_init + module_exit
MODULE_LICENSE("GPL");
```

---

## 2. Windows DLLs

A Dynamic Link Library (DLL) is a Windows executable file containing code and data that multiple programs can use simultaneously. It is the Windows equivalent of a Unix shared library.

### DLL Structure (PE Format)

```
PE Header
  ├── DOS stub
  ├── PE signature ("PE\0\0")
  ├── COFF header (machine type, section count, timestamp)
  └── Optional header (entry point, image base, section alignment)

Sections:
  .text    — executable code
  .rdata   — read-only data (string literals, const arrays)
  .data    — initialized read-write data (global variables)
  .idata   — Import Address Table (IAT) — addresses of imported functions
  .edata   — Export table — names and addresses of exported functions
  .rsrc    — resources (icons, dialogs, version info)
  .reloc   — relocation table (for ASLR)
```

### Loading a DLL

```c
// Implicit (load-time) linking — most common
// Just include the header and link against the import library (.lib)
#include <windows.h>
MessageBoxA(NULL, "Hello", "Title", MB_OK);
// Linker sees MessageBoxA → records it in .idata
// At program startup, Windows loader resolves it to user32.dll!MessageBoxA

// Explicit (runtime) loading — for plugins, optional features
HMODULE hDll = LoadLibraryA("myplugin.dll");
if (hDll) {
    // Get function pointer by name
    typedef void (*MyFunc)(int);
    MyFunc f = (MyFunc) GetProcAddress(hDll, "MyExportedFunction");
    if (f) f(42);
    FreeLibrary(hDll);
}
```

### DLL Export and Import

```c
// DLL source — exporting functions
// Method 1: __declspec(dllexport)
__declspec(dllexport) int Add(int a, int b) {
    return a + b;
}

// Method 2: .def file (explicit export table)
// mylib.def:
//   EXPORTS
//     Add         @1
//     Subtract    @2

// Consuming code — importing
__declspec(dllimport) int Add(int a, int b);
// Or just include the header that declares it
```

### DLL Hell

"DLL Hell" refers to conflicts when multiple applications need different versions of the same DLL:

- App A needs `mylib.dll v1.0`
- App B installs `mylib.dll v2.0` (incompatible, same filename)
- App A breaks

**Solutions:**
- **Side-by-side assemblies (WinSxS):** Windows stores multiple versions in `C:\Windows\WinSxS\`, applications specify required version in their manifest
- **Delay-load DLLs:** Load DLL only when actually needed
- **Static linking:** Include library code in the executable (no runtime dependency)
- **DLL redirection:** App-local DLL in the same directory as the exe takes precedence over system DLL

### Important Windows DLLs

| DLL | Contents |
|-----|---------|
| **ntdll.dll** | Native API — lowest-level user-mode DLL, wraps syscalls directly. All other DLLs call through here. |
| **kernel32.dll** | Core Win32 API — file I/O, memory, threads, processes |
| **user32.dll** | Window management, message loop, GUI controls |
| **gdi32.dll** | GDI graphics — drawing to device contexts (2D only) |
| **advapi32.dll** | Registry, security, services, event log |
| **ws2_32.dll** | Winsock (sockets, network I/O) |
| **msvcrt.dll** | Microsoft C runtime (old) |
| **vcruntime*.dll** | Modern MSVC runtime (per Visual Studio version) |
| **d3d11.dll** | Direct3D 11 |
| **d3d12.dll** | Direct3D 12 |
| **nvapi64.dll** | NVIDIA API (GPU settings, overclocking) |
| **nvcuda.dll** | NVIDIA CUDA runtime |

### DLL Injection

DLL injection inserts a DLL into a running process. Used legitimately (game cheats, debugging tools, AV hooks) and maliciously (malware).

```c
// Method: CreateRemoteThread + LoadLibrary
// 1. Open target process
HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetPid);

// 2. Allocate memory in target process for DLL path
LPVOID remotePath = VirtualAllocEx(hProcess, NULL, pathLen, MEM_COMMIT, PAGE_READWRITE);

// 3. Write DLL path into target process memory
WriteProcessMemory(hProcess, remotePath, dllPath, pathLen, NULL);

// 4. Create thread in target process that calls LoadLibrary
HANDLE hThread = CreateRemoteThread(
    hProcess, NULL, 0,
    (LPTHREAD_START_ROUTINE) GetProcAddress(GetModuleHandleA("kernel32.dll"), "LoadLibraryA"),
    remotePath, 0, NULL
);
WaitForSingleObject(hThread, INFINITE);
```

---

## 3. Linux Shared Libraries (.so)

Linux shared libraries (`.so` — shared object) are the equivalent of Windows DLLs. They use the ELF (Executable and Linkable Format) file format.

### Naming Convention

```
libname.so.MAJOR.MINOR.PATCH

Examples:
  libc.so.6           — glibc, major version 6
  libssl.so.3         — OpenSSL 3.x
  libpython3.11.so.1  — CPython 3.11

Symlinks created during installation:
  libssl.so → libssl.so.3 → libssl.so.3.0.5
  (linker uses .so, loader uses .so.3, actual file is .so.3.0.5)
```

### Creating and Using Shared Libraries

```bash
# Create a shared library
# Write source
cat > mylib.c << 'EOF'
int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }
EOF

# Compile to position-independent code (-fPIC required for .so)
gcc -fPIC -c mylib.c -o mylib.o

# Create shared library
gcc -shared -o libmylib.so.1.0 mylib.o
ln -sf libmylib.so.1.0 libmylib.so.1
ln -sf libmylib.so.1 libmylib.so

# Use the library
cat > main.c << 'EOF'
extern int add(int, int);
int main() {
    return add(3, 4) - 7;  // returns 0
}
EOF

gcc main.c -L. -lmylib -o program
LD_LIBRARY_PATH=. ./program   # Set library search path for runtime

# Install system-wide
sudo cp libmylib.so.1.0 /usr/local/lib/
sudo ldconfig   # Update dynamic linker cache
```

### Library Search Path

The dynamic linker searches for libraries in this order:

```
1. DT_RPATH in the ELF binary (set at compile time, not recommended)
2. LD_LIBRARY_PATH environment variable
3. DT_RUNPATH in the ELF binary (similar to RPATH but respects LD_LIBRARY_PATH)
4. /etc/ld.so.cache (generated by ldconfig from /etc/ld.so.conf)
5. Default paths: /lib, /usr/lib, /lib64, /usr/lib64
```

```bash
# Check what libraries a binary links against
ldd /usr/bin/python3
ldd /bin/ls

# View library cache
ldconfig -p | grep libssl

# Set RPATH at build time (embed library path in binary)
gcc -Wl,-rpath,/opt/myapp/lib main.c -o program
# Now program always looks in /opt/myapp/lib regardless of LD_LIBRARY_PATH
```

### ELF Symbol Visibility

```c
// Control which symbols are exported from a shared library

// Default: visible (exported)
int exported_function(int x) { return x + 1; }

// Hidden: not exported (internal use only)
__attribute__((visibility("hidden")))
int internal_helper(int x) { return x * 2; }

// Compiler flag alternative: -fvisibility=hidden makes everything hidden by default
// Then selectively export:
__attribute__((visibility("default")))
int my_public_api(int x) { ... }
```

---

## 4. Windows Services

A Windows service is a long-running background process managed by the Service Control Manager (SCM). Services start at boot, run without user interaction, and can be configured to restart automatically on failure.

```
Service Control Manager (services.exe)
  ├── Manages service lifecycle (start, stop, pause, restart)
  ├── Handles automatic restart on failure
  ├── Provides service status queries
  └── Enforces service permissions

Service types:
  Win32 own process:     Service runs in its own dedicated process
  Win32 share process:   Multiple services share a svchost.exe process (common)
  Kernel driver service: Drivers registered as services (.sys files)
  File system driver:    Filesystem filter drivers

Service states:
  STOPPED → STARTING → RUNNING → PAUSING → PAUSED → RESUMING → STOPPING → STOPPED
```

### Creating a Service (sc.exe)

```cmd
:: Create a service
sc create MyService binPath= "C:\myapp\service.exe" start= auto DisplayName= "My Service"

:: Start / stop / delete
sc start MyService
sc stop MyService
sc delete MyService

:: Query status
sc query MyService

:: Configure failure actions (restart on crash)
sc failure MyService reset= 3600 actions= restart/5000/restart/5000/restart/5000
:: Restart after 5 seconds on 1st, 2nd, 3rd failure; reset counter after 1 hour
```

### Service in C (Windows API)

```c
#include <windows.h>

SERVICE_STATUS serviceStatus;
SERVICE_STATUS_HANDLE serviceStatusHandle;

void ServiceMain(DWORD argc, LPSTR *argv) {
    serviceStatusHandle = RegisterServiceCtrlHandler("MyService", ServiceCtrlHandler);

    serviceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
    serviceStatus.dwCurrentState = SERVICE_RUNNING;
    serviceStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP;
    SetServiceStatus(serviceStatusHandle, &serviceStatus);

    // Main service loop
    while (running) {
        DoWork();
        Sleep(5000);
    }

    serviceStatus.dwCurrentState = SERVICE_STOPPED;
    SetServiceStatus(serviceStatusHandle, &serviceStatus);
}

void ServiceCtrlHandler(DWORD control) {
    if (control == SERVICE_CONTROL_STOP) {
        running = FALSE;
        serviceStatus.dwCurrentState = SERVICE_STOP_PENDING;
        SetServiceStatus(serviceStatusHandle, &serviceStatus);
    }
}

int main() {
    SERVICE_TABLE_ENTRY serviceTable[] = {
        { "MyService", ServiceMain },
        { NULL, NULL }
    };
    StartServiceCtrlDispatcher(serviceTable);
}
```

### Common Services (Windows)

```
wuauserv       — Windows Update
Themes         — Desktop theming
AudioSrv       — Windows Audio
DcomLaunch     — DCOM server launcher
RpcSs          — Remote Procedure Call
EventLog       — Event logging
Winmgmt        — WMI (Windows Management Instrumentation)
Schedule       — Task Scheduler
spooler        — Print spooler
WinDefend      — Windows Defender
```

---

## 5. Linux Daemons & systemd

A daemon is a background process in Linux/Unix. Daemons conventionally have names ending in 'd' (sshd, httpd, systemd, journald).

### systemd Unit Files

systemd is the init system and service manager for modern Linux. Services are defined in unit files.

```ini
# /etc/systemd/system/myapp.service

[Unit]
Description=My Application Service
Documentation=https://example.com/docs
After=network-online.target    # Start after network is up
Wants=network-online.target
Requires=postgresql.service    # Stop if postgres stops

[Service]
Type=simple                    # Process stays in foreground (systemd tracks it)
# Type=forking: old-style daemon that forks and exits (legacy)
# Type=notify:  process signals ready via sd_notify()
# Type=oneshot: run to completion and exit

ExecStart=/opt/myapp/bin/myapp --config /etc/myapp/config.yaml
ExecReload=/bin/kill -HUP $MAINPID  # Reload config on SIGHUP
ExecStop=/bin/kill -TERM $MAINPID

User=myapp
Group=myapp
WorkingDirectory=/opt/myapp

# Environment
Environment=NODE_ENV=production
EnvironmentFile=/etc/myapp/environment

# Restart policy
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=60
StartLimitBurst=5             # Give up after 5 restarts in 60 seconds

# Resource limits
LimitNOFILE=65536             # Max open file descriptors
MemoryLimit=512M              # cgroup memory limit

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes                # Private /tmp filesystem
ProtectSystem=strict          # Read-only /usr, /boot, /etc
ProtectHome=yes               # No access to /home
ReadWritePaths=/var/lib/myapp

[Install]
WantedBy=multi-user.target    # Enable in multi-user runlevel
```

```bash
# Manage services
sudo systemctl start myapp
sudo systemctl stop myapp
sudo systemctl restart myapp
sudo systemctl reload myapp          # Reload config without restart
sudo systemctl enable myapp          # Enable at boot
sudo systemctl disable myapp
sudo systemctl status myapp

# View logs
journalctl -u myapp                  # All logs for unit
journalctl -u myapp -f               # Follow
journalctl -u myapp --since "1 hour ago"
journalctl -u myapp -n 50            # Last 50 lines

# List units
systemctl list-units --type=service
systemctl list-units --failed        # Show failed services

# Analyze boot time
systemd-analyze
systemd-analyze blame                # Time each unit took to start
systemd-analyze critical-chain       # Critical path
```

---

## 6. The Dynamic Linker / Loader

When an executable is launched, the OS loads it into memory and hands control to the dynamic linker (on Linux: `/lib64/ld-linux-x86-64.so.2`). The dynamic linker resolves all shared library dependencies before the program starts.

### Loading Process (Linux ELF)

```
exec() system call:
  1. Kernel reads ELF header
  2. Kernel maps PT_LOAD segments into memory (code, data)
  3. Kernel reads PT_INTERP segment → path to dynamic linker
  4. Kernel maps dynamic linker into process address space
  5. Kernel transfers control to dynamic linker entry point

Dynamic linker (_start in ld-linux):
  6. Parse ELF dynamic section (DT_NEEDED, DT_RPATH, etc.)
  7. For each needed library (libc.so.6, libssl.so.3...):
     a. Find the .so file (search path as described above)
     b. Map its PT_LOAD segments into process address space
     c. Recursively load ITS dependencies
  8. Resolve symbols: fill Import Address Table (GOT/PLT) with actual addresses
  9. Run .init sections of all libraries (constructors)
  10. Transfer control to main executable's entry point (_start → main)
```

### PLT / GOT — Procedure Linkage Table / Global Offset Table

```
Function call to printf (first call):
  main.c: call printf
  → Calls PLT stub: printf@plt

  PLT stub (first call — lazy binding):
    JMP  [GOT entry for printf]   ← GOT initially points back to resolver
    → Dynamic linker resolver
    → Looks up printf in libc.so
    → Writes actual address into GOT
    → Jumps to actual printf

  PLT stub (subsequent calls):
    JMP  [GOT entry for printf]   ← Now points to actual printf
    → Calls printf directly (one indirect jump overhead)

LD_BIND_NOW=1: force immediate binding (all symbols resolved at startup)
```

---

## 7. Graphics Drivers Deep Dive

See [GPU Architecture](gpu-architecture.md) for the hardware side. Here we focus on the software driver stack.

### NVIDIA Driver Stack (Linux)

```
Application → Vulkan / OpenGL / CUDA
        ↓
Loader: libvulkan.so or libGL.so
        ↓
NVIDIA user-space driver: libGLX_nvidia.so / libnvcuvid.so / libcuda.so
  (this is the giant ~600 MB package from nvidia.com)
        ↓
/dev/nvidia0, /dev/nvidiactl, /dev/nvidia-uvm  (device files)
        ↓
nvidia.ko (kernel module) — ring 0
  ← Loaded by: modprobe nvidia
  ← Provides: GPU command scheduling, memory management, interrupt handling
        ↓
GPU hardware via PCIe MMIO and DMA
```

```bash
# NVIDIA driver management on Linux
lsmod | grep nvidia          # Check if module is loaded
sudo modprobe nvidia         # Load nvidia kernel module
nvidia-smi                   # GPU status and process list
nvidia-smi -L                # List GPUs
nvidia-smi dmon              # Real-time metrics stream
cat /proc/driver/nvidia/version  # Driver version

# DKMS: automatic kernel module recompilation on kernel update
dkms status                  # Check DKMS modules
```

### Mesa (Open-Source GPU Stack)

```
Application → OpenGL / Vulkan
        ↓
Mesa3D (open-source implementation):
  ├── Gallium3D framework (common driver interface)
  ├── RadeonSI (AMD)
  ├── IRIS (Intel Xe)
  ├── NVK (NVIDIA, experimental Vulkan)
  └── zink (OpenGL over Vulkan — any Vulkan driver gets OpenGL for free)
        ↓
DRM (Direct Rendering Manager) — kernel subsystem
  ├── amdgpu.ko
  ├── i915.ko
  └── nouveau.ko (NVIDIA, open-source, limited)
        ↓
GPU hardware
```

---

## 8. Writing a Simple Driver (Linux)

A minimal Linux kernel module (not a full driver, but the foundation):

```c
// hello_module.c
#include <linux/module.h>   // module_init, module_exit, MODULE_* macros
#include <linux/kernel.h>   // printk, KERN_INFO
#include <linux/init.h>     // __init, __exit

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("Minimal Linux kernel module");
MODULE_VERSION("1.0");

// __init: function is discarded from memory after init (saves RAM)
static int __init hello_init(void) {
    printk(KERN_INFO "hello_module: loaded, CPU %d\n", smp_processor_id());
    return 0;   // 0 = success, negative = error (e.g., -ENOMEM, -ENODEV)
}

// __exit: function is discarded if module is compiled into kernel (not module)
static void __exit hello_exit(void) {
    printk(KERN_INFO "hello_module: unloaded\n");
}

module_init(hello_init);
module_exit(hello_exit);
```

```makefile
# Makefile
obj-m += hello_module.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

```bash
make
sudo insmod hello_module.ko    # Load
dmesg | tail -5                # See printk output
sudo rmmod hello_module        # Unload
```

---

## 9. Debugging & Inspection Tools

### Windows

```powershell
# List loaded DLLs for a process
Get-Process -Name notepad | Select-Object -ExpandProperty Modules

# Dependency Walker equivalent (modern)
# dumpbin.exe (Visual Studio)
dumpbin /imports program.exe       # Show imported DLLs and functions
dumpbin /exports mylib.dll         # Show exported functions
dumpbin /headers program.exe       # PE header info

# Process Monitor (Sysinternals) — trace file/registry/network/DLL access
# ProcMon captures every LoadLibrary call, registry read, file open

# WinDbg — debug DLL loading
.load sos.dll                      # Load SOS extension for .NET
!analyze -v                        # Analyze crash
lm                                 # List loaded modules
!dlls                             # Show loaded DLLs with base addresses
```

### Linux

```bash
# Trace dynamic library loading
LD_DEBUG=files ./program         # Print every library file opened
LD_DEBUG=bindings ./program      # Print every symbol binding
LD_DEBUG=all ./program           # Everything (very verbose)

# strace: trace system calls (see every file open, mmap, etc.)
strace -e trace=open,openat,mmap ./program 2>&1 | grep ".so"

# ltrace: trace library calls
ltrace -l "*.so*" ./program

# readelf: inspect ELF structure
readelf -d ./program              # Dynamic section (needed libs)
readelf -S ./program              # Sections
readelf --syms libmylib.so        # Symbol table

# nm: list symbols
nm -D libmylib.so                 # Dynamic symbols (exported by .so)
nm -u ./program                   # Undefined symbols (imports)

# objdump: disassemble + inspect
objdump -T libmylib.so            # Dynamic symbol table
objdump -d -M intel ./program     # Disassemble

# Check shared memory usage of libraries
pmap -p $(pgrep python3) | grep ".so"
```

---

## See Also

- [CPU Architecture](cpu-architecture.md) — Hardware that drivers program directly
- [GPU Architecture](gpu-architecture.md) — GPU driver stack in detail
- [Linux Internals](linux-internals.md) — Kernel module infrastructure, kernel data structures
- [Kernel Architecture](kernel-architecture.md) — Overview of kernel subsystems drivers plug into
