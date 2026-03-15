# Linux Environment Isolation: chroot, proot, and proot-distro

## 1. Overview

This documentation explains the differences and usage of three methods for running isolated Linux environments or changing the root filesystem context on Linux/Android systems.

- **chroot**: The traditional kernel-level change root.
- **proot**: A user-space implementation of chroot, bind mounts, and `personality`.
- **proot-distro**: A helper script (popular in Termux) to manage `proot` Linux distributions easily.

---

## 2. chroot (Change Root)

### Description
`chroot` is a Unix operation that changes the apparent root directory for the current running process and its children. A program that is run in this modified environment cannot access files outside the designated directory tree.

### Requirements
- **Root Privileges**: Requires `sudo` or root access.
- **Architecture**: The binary architecture inside the chroot must match the host (e.g., ARM64 host needs ARM64 chroot).
- **Setup**: Requires manual mounting of virtual filesystems (`/proc`, `/sys`, `/dev`) for a functional environment.

### Basic Usage
```bash
# 1. Create a directory for the new root
sudo mkdir -p /mnt/newroot

# 2. Mount necessary virtual filesystems
sudo mount -t proc /proc /mnt/newroot/proc
sudo mount -t sysfs /sys /mnt/newroot/sys
sudo mount --rbind /dev /mnt/newroot/dev

# 3. Enter the chroot environment
sudo chroot /mnt/newroot /bin/bash

# 4. Exit
exit
```

### Pros & Cons
| Pros | Cons |
| :--- | :--- |
| Native performance (no overhead) | Requires Root access |
| Kernel-level isolation | Architecture must match host |
| Standard tool on all Unix systems | Complex manual setup (mounting) |

---

## 3. proot (User-space Chroot)

### Description
`proot` is a user-space implementation of `chroot`, `mount --bind`, and `binfmt_misc`. It uses the `ptrace` system call to intercept and modify system calls, allowing unprivileged users to pretend they have root privileges for filesystem operations.

### Requirements
- **No Root**: Can be run by a standard user.
- **Binary**: Requires the `proot` binary installed on the host.
- **Performance**: Slight overhead due to `ptrace` interception.

### Basic Usage
```bash
# Run a command with a different root directory
proot -r /path/to/rootfs /bin/bash

# Bind mount a host directory into the proot environment
proot -b /home/user/shared:/mnt/shared -r /path/to/rootfs /bin/bash

# Verbose mode for debugging
proot -v 9 -r /path/to/rootfs /bin/bash
```

### Pros & Cons
| Pros | Cons |
| :--- | :--- |
| **No Root required** | Performance overhead (ptrace) |
| Works on Android (Termux) | Not a security boundary (see Warning) |
| Cross-architecture support (via QEMU) | Some syscalls may not be fully emulated |

---

## 4. proot-distro (Management Tool)

### Description
`proot-distro` is a shell script designed to simplify the installation and management of Linux distributions inside a `proot` environment. It is most commonly used within the **Termux** application on Android.

It automates downloading rootfs tarballs, configuring DNS, and setting up login scripts.

### Installation (Termux Context)
```bash
# Update package list
pkg update

# Install proot-distro
pkg install proot-distro
```

### Common Commands

| Command | Description |
| :--- | :--- |
| `proot-distro list` | List available Linux distributions. |
| `proot-distro install <os>` | Install a specific OS (e.g., `ubuntu`, `debian`, `archlinux`). |
| `proot-distro login <os>` | Log into the installed environment. |
| `proot-distro remove <os>` | Remove an installed environment. |
| `proot-distro reset <os>` | Reset the environment to fresh state. |

### Usage Examples
```bash
# Install Ubuntu
proot-distro install ubuntu

# Login to Ubuntu
proot-distro login ubuntu

# Login with specific user (if supported)
proot-distro login ubuntu --user root

# Bind mount host storage (Termux specific)
proot-distro login ubuntu --shared-tmp
```

---

## 5. Comparison Summary

| Feature | chroot | proot | proot-distro |
| :--- | :--- | :--- | :--- |
| **Root Access** | Required | Not Required | Not Required |
| **Performance** | Native | Slight Overhead | Slight Overhead |
| **Setup Difficulty**| High (Manual) | Medium | Low (Automated) |
| **Primary Use Case**| System Recovery, Containers | Android/Linux User Spaces | Termux Linux Environments |
| **Security** | Moderate | **Low** (See Warning) | **Low** (See Warning) |

---

## 6. Security Warning

> **⚠️ CRITICAL: proot is NOT a security boundary.**
>
> `proot` does not provide isolation comparable to containers (Docker/LXC) or virtual machines.
> - A malicious process inside `proot` may be able to escape or crash the host process.
> - Do not use `proot` to run untrusted code if security is a concern.
> - `chroot` is also not a complete security boundary but is stronger than `proot`.

---

## 7. Troubleshooting

### Issue: `proot` is slow
- **Cause**: `ptrace` overhead.
- **Fix**: Ensure you are not running heavy I/O operations. Use native binaries where possible.

### Issue: `chroot: failed to run command '/bin/bash': No such file or directory`
- **Cause**: Architecture mismatch or missing shared libraries.
- **Fix**: Ensure the binary inside the chroot matches the host architecture. Check `ldd` on the binary.

### Issue: `proot-distro` login fails with signal 11
- **Cause**: Compatibility issue with specific Android kernels.
- **Fix**: Try updating Termux and `proot-distro`. Some kernels disable `ptrace` functionality partially.

---

## 8. See Also
- [proot GitHub Repository](https://github.com/proot-me/PRoot)
- [Termux Wiki - PRoot](https://wiki.termux.com/wiki/PRoot)
- [Linux chroot man page](https://man7.org/linux/man-pages/man1/chroot.1.html)
