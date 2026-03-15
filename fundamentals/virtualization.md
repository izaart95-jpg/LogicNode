# Virtualization — WSL, VMware, QEMU, VirtualBox & Hyper-V

This document covers virtualization technologies from lightweight subsystems (WSL) to full hypervisors (QEMU/KVM, VMware, VirtualBox, Hyper-V).

---

## Table of Contents
1. [Virtualization Concepts](#1-virtualization-concepts)
2. [WSL (Windows Subsystem for Linux)](#2-wsl-windows-subsystem-for-linux)
3. [QEMU & KVM](#3-qemu--kvm)
4. [VirtualBox](#4-virtualbox)
5. [VMware](#5-vmware)
6. [Hyper-V](#6-hyper-v)
7. [Comparison Table](#7-comparison-table)
8. [Which Should You Use?](#8-which-should-you-use)

---

## 1. Virtualization Concepts

### Types of Virtualization

```
┌─────────────────────────────────────────────────────────┐
│  Type 1 — Bare-Metal Hypervisor                         │
│  Runs directly on hardware. No host OS.                 │
│  Examples: Hyper-V, VMware ESXi, Xen, KVM               │
│                                                          │
│  ┌────────┐ ┌────────┐ ┌────────┐                      │
│  │  VM 1  │ │  VM 2  │ │  VM 3  │                      │
│  └────┬───┘ └────┬───┘ └────┬───┘                      │
│       └──────────┼──────────┘                           │
│           ┌──────▼──────┐                               │
│           │  Hypervisor │                               │
│           └──────┬──────┘                               │
│           ┌──────▼──────┐                               │
│           │  Hardware   │                               │
│           └─────────────┘                               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Type 2 — Hosted Hypervisor                              │
│  Runs on top of a host OS as an application.            │
│  Examples: VirtualBox, VMware Workstation, QEMU (no KVM)│
│                                                          │
│  ┌────────┐ ┌────────┐                                  │
│  │  VM 1  │ │  VM 2  │                                  │
│  └────┬───┘ └────┬───┘                                  │
│       └──────┬───┘                                      │
│       ┌──────▼──────┐                                   │
│       │  Hypervisor │  (application)                    │
│       └──────┬──────┘                                   │
│       ┌──────▼──────┐                                   │
│       │   Host OS   │                                   │
│       └──────┬──────┘                                   │
│       ┌──────▼──────┐                                   │
│       │  Hardware   │                                   │
│       └─────────────┘                                   │
└─────────────────────────────────────────────────────────┘
```

### Key Terms

| Term | Meaning |
|------|---------|
| **Hypervisor** | Software that creates and manages VMs |
| **Guest OS** | Operating system running inside a VM |
| **Host OS** | Operating system running the hypervisor |
| **VM (Virtual Machine)** | Isolated virtual computer with its own OS |
| **VT-x / AMD-V** | CPU hardware virtualization extensions |
| **VT-d / AMD-Vi** | I/O virtualization (GPU passthrough) |
| **Paravirtualization** | Guest OS aware it's virtualized (VirtIO drivers) |
| **Emulation** | Software-simulated hardware (slow, cross-arch capable) |
| **Snapshot** | Saved state of a VM at a point in time |

---

## 2. WSL (Windows Subsystem for Linux)

### What is WSL?

**WSL** runs a real Linux kernel inside Windows, allowing you to use Linux tools, shells, and applications natively alongside Windows software.

- **Developer:** Microsoft
- **WSL1:** Translation layer (Linux syscalls → Windows NT kernel). No real Linux kernel.
- **WSL2:** Runs an actual Linux kernel in a lightweight Hyper-V VM. Full syscall compatibility.

### WSL1 vs WSL2

| Feature | WSL1 | WSL2 |
|---------|------|------|
| **Kernel** | Syscall translation | Real Linux kernel (Microsoft-maintained) |
| **Performance** | Fast file I/O (Windows FS) | Near-native Linux perf |
| **Compatibility** | Partial (some syscalls missing) | Full (Docker, systemd, etc.) |
| **Memory** | Shared with Windows | Dynamic (lightweight VM) |
| **Networking** | Shared Windows network stack | Separate virtual NIC (NAT by default) |
| **Docker** | ❌ | ✅ |
| **systemd** | ❌ | ✅ (WSL 0.67.6+) |
| **GUI Apps** | ❌ (need VcXsrv) | ✅ WSLg (built-in) |

### Installation & Usage

```powershell
# Install WSL2 + default distro (Ubuntu)
wsl --install

# Install specific distro
wsl --install -d kali-linux
wsl --install -d debian
wsl --install -d Ubuntu-24.04

# List available distros
wsl --list --online

# List installed distros
wsl --list --verbose

# Set default WSL version
wsl --set-default-version 2

# Start distro
wsl -d Ubuntu

# Shut down all WSL instances
wsl --shutdown

# Import/export distros
wsl --export Ubuntu ubuntu-backup.tar
wsl --import MyUbuntu C:\WSL\MyUbuntu ubuntu-backup.tar

# Access Windows files from WSL
ls /mnt/c/Users/

# Access WSL files from Windows
# File Explorer → \\wsl$\Ubuntu\home\user\
```

### WSLg (GUI Support)

WSL2 includes **WSLg** — built-in GUI app support (no VcXsrv needed):

```bash
# Inside WSL2 — GUI apps just work
sudo apt install firefox gedit nautilus
firefox &    # Opens in a Windows window
```

### WSL Networking

```bash
# Get WSL IP
hostname -I

# Access WSL services from Windows
# localhost works for most ports (WSL2 port forwarding)

# Access Windows from WSL
cat /etc/resolv.conf    # nameserver = Windows host IP

# Port forwarding (if localhost doesn't work)
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=$(wsl hostname -I)
```

### WSL Config

```ini
# /etc/wsl.conf (inside distro)
[boot]
systemd=true

[automount]
enabled=true
root=/mnt/

[network]
hostname=mydevbox

[user]
default=myuser
```

```ini
# C:\Users\<user>\.wslconfig (Windows-side, global)
[wsl2]
memory=8GB
processors=4
swap=4GB
localhostForwarding=true
```

---

## 3. QEMU & KVM

### What is QEMU?

**QEMU** (Quick EMUlator) is an open-source machine emulator and virtualizer.

- **Emulation mode:** Translates CPU instructions (run ARM on x86, etc.) — slow but cross-architecture
- **KVM mode:** Uses Linux kernel's KVM (Kernel-based Virtual Machine) for near-native speed
- **License:** GPL v2
- **Platform:** Linux, macOS, Windows

### What is KVM?

**KVM** is a Linux kernel module that turns Linux into a Type-1 hypervisor. QEMU uses KVM for hardware-accelerated virtualization.

```
QEMU alone:        Software emulation (slow, cross-arch)
QEMU + KVM:        Hardware virtualization (near-native, same-arch only)
```

### Installation

```bash
# Debian/Ubuntu
sudo apt install qemu-system-x86 qemu-utils ovmf virt-manager libvirt-daemon-system

# Fedora
sudo dnf install @virtualization

# Arch
sudo pacman -S qemu-full virt-manager libvirt

# Check KVM support
egrep -c '(vmx|svm)' /proc/cpuinfo    # >0 means supported
lsmod | grep kvm

# Enable libvirt
sudo systemctl enable --now libvirtd
sudo usermod -aG libvirt $USER
```

### Basic QEMU Usage

```bash
# Create disk image
qemu-img create -f qcow2 disk.qcow2 40G

# Boot from ISO (install OS)
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -smp 4 \
  -hda disk.qcow2 \
  -cdrom ubuntu.iso \
  -boot d

# Boot existing VM
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -smp 4 \
  -hda disk.qcow2

# With VirtIO (best performance)
qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -smp 4 \
  -drive file=disk.qcow2,if=virtio \
  -net nic,model=virtio -net user \
  -vga virtio \
  -display spice-app
```

### virt-manager (GUI)

```bash
# GUI for managing QEMU/KVM VMs
virt-manager

# Or use virsh (CLI)
virsh list --all
virsh start myvm
virsh shutdown myvm
virsh snapshot-create-as myvm snap1
```

### QEMU Cross-Architecture Emulation

```bash
# Run ARM binary on x86
sudo apt install qemu-user-static
qemu-aarch64-static ./arm-binary

# Run full ARM system
qemu-system-aarch64 \
  -machine virt \
  -cpu cortex-a72 \
  -m 2048 \
  -drive file=arm-disk.qcow2
```

---

## 4. VirtualBox

### What is VirtualBox?

**VirtualBox** is a free, open-source Type-2 hypervisor by Oracle. It's the easiest way to run VMs on desktop operating systems.

- **Developer:** Oracle
- **License:** GPL v2 (base), PUEL (Extension Pack)
- **Platform:** Windows, macOS, Linux
- **Guest OS:** Windows, Linux, macOS (limited), BSD, Solaris

### Installation

```bash
# Debian/Ubuntu
sudo apt install virtualbox virtualbox-ext-pack

# Fedora
sudo dnf install VirtualBox

# Windows / macOS
# Download from https://www.virtualbox.org/wiki/Downloads

# Extension Pack (USB 2.0/3.0, RDP, disk encryption)
# Download from same page, install via VirtualBox GUI
```

### CLI Usage (VBoxManage)

```bash
# Create VM
VBoxManage createvm --name "Ubuntu" --ostype Ubuntu_64 --register

# Configure
VBoxManage modifyvm "Ubuntu" --memory 4096 --cpus 2 --vram 128
VBoxManage modifyvm "Ubuntu" --nic1 nat

# Create and attach disk
VBoxManage createmedium disk --filename Ubuntu.vdi --size 40000
VBoxManage storagectl "Ubuntu" --name "SATA" --add sata
VBoxManage storageattach "Ubuntu" --storagectl "SATA" --port 0 --type hdd --medium Ubuntu.vdi

# Attach ISO
VBoxManage storageattach "Ubuntu" --storagectl "SATA" --port 1 --type dvddrive --medium ubuntu.iso

# Start VM
VBoxManage startvm "Ubuntu"
VBoxManage startvm "Ubuntu" --type headless    # No GUI

# Snapshots
VBoxManage snapshot "Ubuntu" take "clean-install"
VBoxManage snapshot "Ubuntu" restore "clean-install"

# List VMs
VBoxManage list vms
VBoxManage list runningvms
```

### Guest Additions

```bash
# Inside the guest VM — improves performance and features
sudo apt install virtualbox-guest-additions-iso
# Or: Devices → Insert Guest Additions CD → run installer

# Features enabled:
# - Shared folders
# - Seamless mode (guest windows on host desktop)
# - Shared clipboard
# - Drag and drop
# - Dynamic resolution
# - Better graphics
```

---

## 5. VMware

### Products

| Product | Type | Platform | License |
|---------|------|----------|---------|
| **VMware Workstation Pro** | Type-2 (desktop) | Windows, Linux | Free (personal since 2024) |
| **VMware Fusion** | Type-2 (desktop) | macOS | Free (personal since 2024) |
| **VMware ESXi** | Type-1 (bare-metal) | Server | Free (limited) / Enterprise |
| **VMware vSphere** | Data center platform | Server | Enterprise |

### VMware Workstation/Fusion

```bash
# Install on Linux (Workstation Pro)
# Download .bundle from https://www.vmware.com/products/workstation-pro.html
chmod +x VMware-Workstation-*.bundle
sudo ./VMware-Workstation-*.bundle

# CLI management (vmrun)
vmrun list                                          # List running VMs
vmrun start /path/to/vm.vmx                         # Start VM
vmrun stop /path/to/vm.vmx                          # Stop VM
vmrun suspend /path/to/vm.vmx                       # Suspend VM
vmrun snapshot /path/to/vm.vmx "clean-install"      # Take snapshot
vmrun revertToSnapshot /path/to/vm.vmx "clean-install"
```

### Key Features

- **Snapshots** — save/restore VM states
- **Linked clones** — space-efficient VM copies
- **Unity mode** — guest apps appear as host windows
- **VMware Tools** — guest drivers for performance + integration
- **3D acceleration** — DirectX 11, OpenGL 4.1
- **Nested virtualization** — run VMs inside VMs
- **OVF/OVA import/export** — portable VM format

### VMware vs VirtualBox

| Feature | VMware Workstation | VirtualBox |
|---------|-------------------|------------|
| **Performance** | Better (optimized drivers) | Good |
| **3D Graphics** | DirectX 11, OpenGL 4.1 | DirectX 9, OpenGL 3.0 |
| **Snapshots** | ✅ Advanced | ✅ Basic |
| **USB Passthrough** | ✅ | ✅ (Extension Pack) |
| **Pricing** | Free (personal) | Free |
| **Open Source** | ❌ | ✅ (base) |
| **Enterprise** | ✅ vSphere ecosystem | ❌ |

---

## 6. Hyper-V

### What is Hyper-V?

**Hyper-V** is Microsoft's Type-1 (bare-metal) hypervisor built into Windows Pro/Enterprise/Education and Windows Server.

- **Developer:** Microsoft
- **Type:** Type-1 (runs below Windows, not on top of it)
- **Available on:** Windows 10/11 Pro+, Windows Server 2012+
- **Key Use:** WSL2, Docker Desktop, Windows VMs, development environments

> **Important:** Once Hyper-V is enabled, it becomes the hypervisor for the entire system. VirtualBox and VMware may need configuration changes to work alongside it.

### Enable Hyper-V

```powershell
# PowerShell (Admin)
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

# Or via DISM
DISM /Online /Enable-Feature /All /FeatureName:Microsoft-Hyper-V

# Or: Settings → Apps → Optional Features → More Windows Features → Hyper-V

# Reboot required
```

### PowerShell VM Management

```powershell
# Create VM
New-VM -Name "Ubuntu" -MemoryStartupBytes 4GB -NewVHDPath "C:\VMs\Ubuntu.vhdx" -NewVHDSizeBytes 40GB -Generation 2

# Configure
Set-VMProcessor -VMName "Ubuntu" -Count 4
Set-VMMemory -VMName "Ubuntu" -DynamicMemoryEnabled $true -MinimumBytes 2GB -MaximumBytes 8GB

# Attach ISO
Add-VMDvdDrive -VMName "Ubuntu" -Path "C:\ISOs\ubuntu.iso"

# Configure boot order (Gen2)
$dvd = Get-VMDvdDrive -VMName "Ubuntu"
Set-VMFirmware -VMName "Ubuntu" -FirstBootDevice $dvd

# Network
Get-VMSwitch
New-VMSwitch -Name "External" -NetAdapterName "Ethernet" -AllowManagementOS $true
Connect-VMNetworkAdapter -VMName "Ubuntu" -SwitchName "External"

# Start/Stop
Start-VM -Name "Ubuntu"
Stop-VM -Name "Ubuntu"

# Snapshots (Checkpoints)
Checkpoint-VM -Name "Ubuntu" -SnapshotName "clean-install"
Restore-VMCheckpoint -Name "clean-install" -VMName "Ubuntu" -Confirm:$false

# List VMs
Get-VM
Get-VM | Where-Object {$_.State -eq "Running"}
```

### Hyper-V Enhanced Session Mode

Connects via RDP to the VM for:
- Clipboard sharing
- Audio redirection
- Drive mapping
- USB redirection
- Dynamic resolution

```powershell
# Enable Enhanced Session
Set-VMHost -EnableEnhancedSessionMode $true

# For Linux guests, install xrdp
# Inside Ubuntu VM:
sudo apt install xrdp
sudo systemctl enable xrdp
```

### Hyper-V + Other Hypervisors

```powershell
# Check if Hyper-V is active
systeminfo | findstr /i "hypervisor"
# "A hypervisor has been detected" = Hyper-V is on

# VirtualBox 6.0+ and VMware 15.5+ support running alongside Hyper-V
# But performance may be reduced (nested virtualization)

# Disable Hyper-V temporarily (for better VirtualBox/VMware perf)
bcdedit /set hypervisorlaunchtype off
# Re-enable:
bcdedit /set hypervisorlaunchtype auto
# Reboot required for both
```

---

## 7. Comparison Table

| Feature | WSL2 | QEMU/KVM | VirtualBox | VMware Workstation | Hyper-V |
|---------|------|----------|------------|-------------------|---------|
| **Type** | Lightweight VM | Type-1 (KVM) / Emulator | Type-2 | Type-2 | Type-1 |
| **Host OS** | Windows | Linux | Win/Mac/Lin | Win/Lin (Mac=Fusion) | Windows |
| **Guest OS** | Linux only | Any | Any | Any | Any |
| **Performance** | Near-native | Near-native (KVM) | Good | Very Good | Near-native |
| **GPU Passthrough** | ❌ | ✅ (VFIO) | Limited | Limited | ✅ (DDA) |
| **Snapshots** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **GUI** | WSLg | virt-manager | ✅ | ✅ | Hyper-V Manager |
| **CLI** | wsl.exe | virsh, qemu | VBoxManage | vmrun | PowerShell |
| **Networking** | NAT (default) | Bridge/NAT/Host | NAT/Bridge/Host | NAT/Bridge/Host | Virtual Switch |
| **Docker** | ✅ | ✅ | ✅ (inside VM) | ✅ (inside VM) | ✅ |
| **Nested Virt** | ❌ | ✅ | Limited | ✅ | ✅ |
| **Free** | ✅ | ✅ | ✅ | ✅ (personal) | ✅ (Win Pro+) |
| **Open Source** | Partial | ✅ | ✅ (base) | ❌ | ❌ |
| **Cross-Arch** | ❌ | ✅ (QEMU) | ❌ | ❌ | ❌ |
| **Best For** | Linux dev on Windows | Linux servers, labs | Desktop VMs, learning | Desktop VMs, enterprise | Windows Server, WSL2 backend |

---

## 8. Which Should You Use?

| Need | Best Choice |
|------|------------|
| **Linux tools on Windows** | **WSL2** (simplest, fastest) |
| **Full Linux desktop VM on Windows** | **VMware Workstation** or **VirtualBox** |
| **Linux server virtualization** | **QEMU/KVM** + virt-manager |
| **Windows VM on Linux** | **QEMU/KVM** (with VirtIO) or **VirtualBox** |
| **macOS VM** | **QEMU** (limited) or **VMware** (limited) |
| **Cross-architecture emulation** | **QEMU** (ARM on x86, etc.) |
| **Enterprise / data center** | **VMware ESXi** or **Hyper-V Server** |
| **Quick VM for testing** | **VirtualBox** (easiest GUI) |
| **GPU passthrough** | **QEMU/KVM + VFIO** |
| **Docker on Windows** | **WSL2** (Docker Desktop backend) |
| **Security lab** | **VirtualBox** or **VMware** (snapshots for malware analysis) |
| **Learning/education** | **VirtualBox** (free, cross-platform, great docs) |

---

## See Also

- [Operating Systems](operating-systems.md) — OS theory, chroot, proot, containers
- [Kernel Architecture](kernel-architecture.md) — KVM internals, kernel modules
- [Remote Access](../networking/remote-access.md) — VNC, RDP, SPICE for VM display
- [Linux Distributions](linux-distributions.md) — Choosing a guest OS
