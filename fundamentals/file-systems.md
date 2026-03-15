# File Systems

How file systems work — from the on-disk data structures that store your files to the VFS layer that unifies them under one interface. Covers every major file system in use today.

---

## Table of Contents
1. [What a File System Does](#1-what-a-file-system-does)
2. [File System Internals — Concepts](#2-file-system-internals--concepts)
3. [ext4 — Linux Default](#3-ext4--linux-default)
4. [Btrfs — Copy-on-Write Linux FS](#4-btrfs--copy-on-write-linux-fs)
5. [ZFS — The Indestructible FS](#5-zfs--the-indestructible-fs)
6. [XFS — High-Performance Linux FS](#6-xfs--high-performance-linux-fs)
7. [NTFS — Windows Default](#7-ntfs--windows-default)
8. [APFS — Apple File System](#8-apfs--apple-file-system)
9. [FAT32 & exFAT — Universal Compatibility](#9-fat32--exfat--universal-compatibility)
10. [F2FS — Flash-Friendly FS](#10-f2fs--flash-friendly-fs)
11. [tmpfs & ramfs — Memory File Systems](#11-tmpfs--ramfs--memory-file-systems)
12. [FUSE — User-Space File Systems](#12-fuse--user-space-file-systems)
13. [Network File Systems](#13-network-file-systems)
14. [Virtual File Systems](#14-virtual-file-systems)
15. [File System Operations Reference](#15-file-system-operations-reference)
16. [Choosing a File System](#16-choosing-a-file-system)

---

## 1. What a File System Does

```
Raw storage (SSD/HDD/RAM/network) = flat array of blocks, no structure
File system = abstraction layer giving blocks meaning

A file system provides:
  Namespace:      Files and directories with human-readable names
  Metadata:       Size, timestamps (created/modified/accessed), permissions, ownership
  Data location:  Maps filename → blocks on storage device
  Integrity:      Ensure data survives crashes, power loss
  Access control: Permissions (rwxr-xr-x), ACLs, extended attributes
  Space management: Track which blocks are free vs used

Without a file system, an SSD is just:
  [block 0][block 1][block 2]...[block N]
  You'd have to remember "my file is at blocks 500–523" manually.

With ext4:
  open("/etc/hosts", O_RDONLY)
  → VFS → ext4 → lookup "hosts" in /etc directory → find inode 12345
  → inode 12345 → block pointers [500, 501, 502]
  → read blocks → return file data
```

---

## 2. File System Internals — Concepts

### Inodes

```
An inode (index node) stores file METADATA — not the filename, not the data.

Inode contents:
  File type:       regular, directory, symlink, device, socket, pipe
  Permissions:     rwxrwxrwx + setuid/setgid/sticky bits
  Owner:           UID + GID
  Timestamps:      atime (accessed), mtime (modified), ctime (inode changed), crtime (created)
  Size:            in bytes
  Link count:      number of hard links pointing to this inode
  Block pointers:  where the file's data blocks are on disk
  Extended attrs:  security labels, capabilities, ACLs

What inode does NOT contain:
  The filename — filenames are stored in directories
  A directory is just a list of (name → inode number) mappings

Inode number:
  Each file/dir has a unique inode number within its filesystem
  ls -i file.txt      → show inode number
  stat file.txt       → full inode info
  find / -inum 12345  → find file by inode number
```

### Hard Links vs Soft Links

```
Hard link:
  Two directory entries pointing to the SAME inode
  ln file.txt hardlink.txt
  
  file.txt   → inode 12345 → data blocks
  hardlink.txt → inode 12345 → same data blocks
  
  Delete file.txt: inode still exists (link count: 2→1)
  Delete hardlink.txt: link count 1→0, inode freed, blocks reclaimed
  Cannot cross filesystem boundaries (inode numbers are per-filesystem)
  Cannot hard link directories (prevents cycles)

Soft link (symbolic link):
  A file that contains a PATH to another file
  ln -s /etc/hosts /tmp/hosts_link
  
  /tmp/hosts_link → inode 99 (type: symlink, data: "/etc/hosts")
  Reading /tmp/hosts_link → kernel follows path → reads /etc/hosts
  
  Can cross filesystems, can link directories
  Dangling symlink: target deleted → link broken (ENOENT when accessed)
```

### Block Allocation

```
Files stored as sequences of blocks on disk
Block size: typically 4096 bytes (4 KB)

Small file (< 1 block = 4 KB):
  Inode → 1 direct block pointer → 4 KB data

Large file (ext4):
  Extents: contiguous range of blocks described as (start_block, length)
  More efficient than block lists for large sequential files
  
  Example: 100 MB file = 25,600 blocks
  Old method: 25,600 block pointers in inode (waste)
  Extents: [(start=1000, len=25600)] = 1 extent describes all 25,600 blocks

Fragmentation:
  When file blocks are non-contiguous on disk
  HDDs: severe penalty (seek time between non-contiguous blocks)
  SSDs: minimal penalty (random access ≈ sequential access)
  
  Defragmentation: e4defrag (ext4), btrfs balance, NTFS defrag
  On SSDs: don't defragment — unnecessary wear, minimal benefit
```

### Journaling

```
Problem: power loss mid-write can leave filesystem inconsistent
  (directory updated but file data not written, or vice versa)

Solution: journal (write-ahead log)
  Before modifying filesystem: write intent to journal
  If crash: replay journal on mount → restore consistency
  
Journal modes:
  writeback:  Only metadata journaled (fastest, some data loss risk)
  ordered:    Data written BEFORE metadata journaled (default ext4, good balance)
  data:       Both data AND metadata journaled (safest, slowest)

Set on ext4 at mount time:
  /dev/sda1 / ext4 errors=remount-ro,data=ordered 0 1

No journal → fsck required after crash (slow, may fail):
  FAT32: no journal → long fsck after unclean shutdown
  ext2: no journal (ext3 added journaling)
```

---

## 3. ext4 — Linux Default

The default Linux filesystem, successor to ext2 (1993) and ext3 (2001).

```
Key features:
  Extents:           contiguous block ranges (vs block lists in ext2/3)
  Delayed allocation: buffer writes, allocate optimal blocks later
  Journal:           ordered mode by default
  64-bit support:    up to 1 Exabyte volumes
  Directory indexing: HTree (hash tree) for large directories
  Persistent pre-allocation: reserve space without writing (e.g., for video)
  Multiblock allocation: allocate multiple blocks in one operation

Limits:
  Max file size:   16 TB
  Max volume:      1 EB (Exabyte)
  Max filenames:   255 bytes
  Max files:       4 billion (limited by 32-bit inode count)

Create and use:
  mkfs.ext4 /dev/sdb1                         # Format
  mkfs.ext4 -b 4096 -N 1000000 /dev/sdb1      # Custom block size, inode count
  mount /dev/sdb1 /mnt/data                    # Mount
  tune2fs -l /dev/sdb1                         # Inspect filesystem info
  e2fsck -f /dev/sdb1                          # Check and repair (unmounted)
  resize2fs /dev/sdb1 200G                     # Resize (can grow online)
  dumpe2fs /dev/sdb1 | head -50                # Dump superblock info

Check filesystem usage:
  df -h /mnt/data                              # Space usage
  df -i /mnt/data                              # Inode usage (can run out of inodes!)
  
inode exhaustion:
  Can have free space but no free inodes → "No space left" error
  Fix (recreate FS): mkfs.ext4 -N 4000000 /dev/sdb1  (more inodes)
```

---

## 4. Btrfs — Copy-on-Write Linux FS

Btrfs (B-tree filesystem, "butter fs") is a modern Linux filesystem with advanced features: snapshots, subvolumes, built-in RAID, checksums, compression.

### Key Concepts

```
Copy-on-Write (CoW):
  Never overwrite data in place
  Write new version to different location → update reference
  Old version remains until space is reclaimed
  
  Benefits:
    Atomic updates: no inconsistency possible (either new or old version)
    Snapshots: cheap (just record the current tree root — O(1))
    Data integrity: checksums prevent silent corruption

Subvolumes:
  Independent filesystem subtrees within one Btrfs partition
  Each has its own inode namespace
  Can be mounted independently
  Can be snapshotted independently
  
  Example layout for Linux installation:
    Subvolume @       → mounted at /
    Subvolume @home   → mounted at /home
    Subvolume @var    → mounted at /var/log
    Snapshots stored separately from active subvolumes
```

### Btrfs Operations

```bash
# Create Btrfs filesystem
mkfs.btrfs /dev/sdb1
mkfs.btrfs -d raid1 -m raid1 /dev/sdb1 /dev/sdc1  # RAID 1 across two devices

# Mount with options
mount -o compress=zstd:3,subvol=@ /dev/sdb1 /

# Common mount options:
#   compress=zstd:3       transparent compression (zstd algorithm, level 3)
#   compress=lzo          faster, less compression ratio
#   noatime               don't update access times (performance)
#   ssd                   enable SSD optimizations
#   discard=async         enable TRIM for SSDs

# Subvolume management
btrfs subvolume list /                      # List all subvolumes
btrfs subvolume create /mnt/data/@home      # Create subvolume
btrfs subvolume delete /mnt/data/@old       # Delete subvolume

# Snapshots (INSTANT — O(1) time and space)
btrfs subvolume snapshot / /.snapshots/2024-01-15           # Read-write snapshot
btrfs subvolume snapshot -r / /.snapshots/2024-01-15-ro     # Read-only snapshot

# Send/receive (incremental backup)
btrfs send /.snapshots/snap1 | btrfs receive /backup/
btrfs send -p /.snapshots/snap1 /.snapshots/snap2 | btrfs receive /backup/
# -p: only send changes since snap1 (incremental — tiny transfer)

# Balance (redistribute data across devices, reclaim space after deletes)
btrfs balance start /                        # Rebalance everything
btrfs balance start -dusage=50 /            # Only rebalance chunks <50% full

# Scrub (verify all data checksums, fix errors from redundant copies)
btrfs scrub start /
btrfs scrub status /

# Check/repair (unmounted)
btrfs check /dev/sdb1
btrfs check --repair /dev/sdb1             # USE WITH CAUTION

# Compression stats
compsize /home                              # Show compression ratio (need compsize package)

# Device management
btrfs device add /dev/sdc1 /               # Add device to pool
btrfs device remove /dev/sdb1 /            # Remove device (data migrated first)
btrfs filesystem show /                    # Show all devices in pool
```

### Snapper — Automated Btrfs Snapshots

```bash
sudo apt install snapper
snapper -c root create-config /            # Create config for root
snapper list                               # List snapshots
snapper create --description "before update"  # Manual snapshot
snapper rollback 3                         # Roll back to snapshot 3
# Snapper auto-creates pre/post snapshots around package installs
```

---

## 5. ZFS — The Indestructible FS

ZFS combines a volume manager (like LVM) and filesystem in one. Originally developed by Sun Microsystems for Solaris. The "last word in filesystems."

```
ZFS philosophy:
  "Pools, not partitions"
  Data integrity above all else
  Every data block has a checksum — silent corruption detected and repaired
  
ZFS uniqueness vs other filesystems:
  Other FS: partition → filesystem (separate tools for each)
  ZFS:      pool (vdev collection) → datasets (filesystems/volumes) all in one
```

### ZFS Architecture

```
ZPool (storage pool):
  Collection of vdevs
  
  vdev types:
    Single disk:    no redundancy (avoid for data)
    Mirror:         RAID-1 (2–N disks, any one can fail)
    RAIDZ1:        RAID-5 equivalent (N disks, 1 parity, 1 disk can fail)
    RAIDZ2:        RAID-6 equivalent (N disks, 2 parity, 2 disks can fail)
    RAIDZ3:        3 parity (rare, maximum redundancy)
    
Dataset types:
  Filesystem:       like a directory, mountable, CoW
  Volume (zvol):    block device (for VMs, swap, other filesystems)
  Snapshot:         read-only point-in-time copy (instant, CoW)
  Clone:            writable copy based on a snapshot (CoW)
  Bookmark:         lightweight snapshot reference (no space, can't rollback but can send)
```

### ZFS Commands

```bash
# Install (Linux)
sudo apt install zfsutils-linux       # Ubuntu/Debian
sudo pacman -S zfs-dkms               # Arch (AUR)

# Create pool
zpool create mypool /dev/sdb          # Simple pool on one disk
zpool create mypool mirror /dev/sdb /dev/sdc              # Mirror
zpool create mypool raidz /dev/sdb /dev/sdc /dev/sdd      # RAIDZ1
zpool create mypool raidz2 /dev/sd{b..f}                  # RAIDZ2 on 5 disks

# Pool status and health
zpool status                          # Detailed health, errors
zpool list                            # Size, usage, health summary
zpool iostat -v 1                     # I/O stats per device (1s interval)

# Dataset management
zfs list                              # List all datasets
zfs create mypool/data                # Create dataset (auto-mounted at /mypool/data)
zfs set mountpoint=/data mypool/data  # Custom mount point
zfs set compression=lz4 mypool/data   # Enable compression
zfs set quota=100G mypool/data        # Set quota
zfs set recordsize=1M mypool/data     # Tune record size (128K default, 1M for sequential)

# Properties
zfs get all mypool/data               # Show all properties
zfs get compression,compressratio mypool/data

# Snapshots
zfs snapshot mypool/data@2024-01-15                  # Create snapshot
zfs list -t snapshot                                  # List snapshots
zfs rollback mypool/data@2024-01-15                  # Roll back (destroys newer snaps)
zfs destroy mypool/data@2024-01-15                   # Delete snapshot
zfs diff mypool/data@snap1 mypool/data@snap2         # Show changes between snaps

# Clone (writable snapshot)
zfs clone mypool/data@snap1 mypool/data-test         # Create writable clone

# Send/receive (backup, replication)
zfs send mypool/data@snap1 | zfs receive backup/data          # Initial replication
zfs send -i mypool/data@snap1 mypool/data@snap2 | ssh host zfs receive backup/data
# -i: incremental send (only changes between snaps)

# ZFS-specific integrity
zpool scrub mypool            # Verify all checksums, repair from redundancy
zpool status -v mypool        # Show errors per device

# Online expansion
zpool add mypool /dev/sde         # Add another vdev
zpool attach mypool /dev/sdb /dev/sdf   # Convert single disk to mirror
```

### ZFS ARC (Adaptive Replacement Cache)

```
ZFS has its own kernel-level read cache (ARC) separate from the Linux page cache.
ARC is typically 50% of RAM by default.

Check ARC:
  arc_summary                     # ZFS ARC statistics
  cat /proc/spl/kstat/zfs/arcstats

Limit ARC (if RAM needed for other things):
  echo "options zfs zfs_arc_max=4294967296" | sudo tee /etc/modprobe.d/zfs.conf
  # Limits ARC to 4 GB (in bytes)

L2ARC (Level 2 ARC — SSD read cache):
  Use an SSD as extended read cache beyond RAM
  zpool add mypool cache /dev/ssd1
  Good for: all-HDD pools accessed frequently
```

---

## 6. XFS — High-Performance Linux FS

XFS is optimized for large files and high-throughput workloads. Default on RHEL/CentOS/Fedora.

```
Strengths:
  Exceptional large file performance
  Parallel I/O: multiple allocation groups, each independently locked
  Online defragmentation and expansion
  Delayed logging (journal): metadata batched for efficiency
  Reflinks (since 4.9): CoW file copies (like Btrfs/APFS)
  
Limitations:
  Cannot shrink (only grow) — plan volume size carefully
  Repair (xfs_repair) is slower than ext4 e2fsck for large filesystems
  Not ideal for many small files vs large sequential
  
Best for:
  Database servers, media servers, large file workloads
  RHEL-based servers (RHEL 7+ defaults to XFS)

Commands:
  mkfs.xfs /dev/sdb1
  xfs_info /mnt/data          # Filesystem info
  xfs_repair /dev/sdb1        # Repair (unmounted)
  xfs_growfs /mnt/data        # Grow (online, mounted)
  xfs_fsr /mnt/data           # Online defragmentation
  xfs_quota                   # Quota management
  xfs_db /dev/sdb1            # Low-level debugger
```

---

## 7. NTFS — Windows Default

NTFS (New Technology File System) has been the Windows default since Windows NT 3.1 (1993).

```
Architecture:
  MFT (Master File Table): database of all file records
    Each file/directory = one MFT record (1 KB)
    Contains: all metadata + small files (< ~900 bytes) stored INLINE in MFT
  MFT Mirror: backup of critical MFT records
  Volume Bitmap: tracks used/free clusters
  
Key features:
  Journal ($LogFile): crash recovery
  Compression: transparent per-file/directory compression
  Encryption (EFS): per-file encryption via certificate
  Hard links, junctions, symbolic links
  ACLs: full Windows security model (user/group/deny/allow)
  Alternate Data Streams (ADS): multiple data streams per file
    file.txt:secret_stream  (hidden data, used by Windows for metadata)
    Zone.Identifier stream: marks downloaded files (why "unblock" dialog appears)
  
NTFS on Linux (ntfs3 kernel driver, since 5.15):
  Previously: ntfs-3g (FUSE driver) — slow but reliable
  Now: ntfs3 in kernel — native performance
  
  # Mount NTFS with new kernel driver
  mount -t ntfs3 /dev/sdb1 /mnt/windows
  
  # Mount NTFS via ntfs-3g (older, more compatible for edge cases)
  mount -t ntfs-3g /dev/sdb1 /mnt/windows
  
  # /etc/fstab entry for NTFS auto-mount
  /dev/sdb1  /mnt/windows  ntfs3  defaults,uid=1000,gid=1000  0  0

NTFS limits:
  Max file size:   16 EB (theoretical), ~2 TB practical on most Windows
  Max volume size: 256 TB (Windows) / 8 PB (theoretical)
  Max path:        260 characters (historical Win32 limit, removable via registry)
```

---

## 8. APFS — Apple File System

APFS (Apple File System) replaced HFS+ in 2017. Used on all Apple devices (Mac, iPhone, iPad, Apple Watch, Apple TV).

```
Architecture:
  Container = physical storage (entire SSD)
  Volume = logical partition within container
  Multiple volumes share the same container freely (no fixed partition sizes)
  
  Apple Silicon Mac typical layout:
    Container (500GB SSD)
    ├── Volume: Preboot
    ├── Volume: Recovery
    ├── Volume: VM (swap)
    ├── Volume: Macintosh HD (system — read-only, signed)
    ├── Volume: Macintosh HD - Data (user data — read-write)
    └── (free space shared by all volumes)

Key features:
  Copy-on-Write:  No data overwrite in place (like Btrfs/ZFS)
  Snapshots:      Instant, CoW — Time Machine uses APFS snapshots
  Cloning:        cp -c src dst — instant clone (reflink), no extra space until modified
  Encryption:     Full-disk or per-file, AES-128/256 with hardware keys
  Space sharing:  All volumes in container share free space (no fixed partition sizes)
  Sparse files:   Holes in files take no disk space
  
Encryption on Apple Silicon:
  Data Protection classes (like iOS):
    Complete: encrypted when device locked
    Complete Unless Open: encrypted when locked (except files being accessed)
  Hardware key: stored in Secure Enclave (T2 / M-series)
  Cannot be decrypted without valid credentials even if SSD removed

APFS on Linux:
  apfs-fuse (read-only): https://github.com/sgan81/apfs-fuse
  Limited compatibility — use caution with production data
  
  # Mount macOS APFS volume on Linux (read-only)
  apfs-fuse /dev/sdb2 /mnt/mac
  
HFS+ legacy:
  Still used on some older Macs, HDDs, Time Machine volumes
  Linux support: hfsplus kernel module (read-write with limitations)
```

---

## 9. FAT32 & exFAT — Universal Compatibility

The most compatible filesystems — readable/writable on Windows, macOS, Linux, cameras, consoles, and embedded devices without any additional software.

### FAT32

```
FAT (File Allocation Table) — the original PC filesystem (MS-DOS 1.0, 1981)
FAT32 introduced in Windows 95 OSR2 (1996)

Structure:
  Boot sector: filesystem metadata
  FAT table:   chains of cluster numbers (map of file data locations)
  Root directory: root folder entries (special in FAT32)
  Data area:   actual file and directory content

Cluster chain example:
  File.txt starts at cluster 5
  FAT[5] = 12    (next cluster is 12)
  FAT[12] = 8    (next cluster is 8)
  FAT[8] = 0xFFFFFFFF  (end of chain)
  → File occupies clusters 5, 12, 8

Limits (why FAT32 is obsolete):
  Max file size:   4 GB - 1 byte (32-bit FAT entry)
  Max volume:      2 TB (8 TB with 64 KB clusters, but Windows won't format >32 GB)
  Max filename:    255 characters (LFN — Long File Name extension)
  No permissions, no encryption, no journaling
  
Still used for:
  Boot partitions (EFI System Partition: FAT32 is required by UEFI spec)
  SD cards < 32 GB (SDHC spec)
  USB drives for maximum compatibility
  Embedded devices (cameras, GPS units, car stereos)
```

### exFAT

```
Extended FAT: Microsoft's answer to FAT32 size limitations (2006)
Designed for: flash drives, SD cards, portable devices

Limits:
  Max file size:   128 PB (petabytes) — effectively unlimited
  Max volume:      128 PB
  Max filename:    255 UTF-16 characters
  
Added vs FAT32:
  Large file support (no 4 GB limit)
  Access Control List (optional, rarely used)
  UTC timestamps
  Boot checksum

No journal, no permissions, no hardlinks
Simple and fast — good for flash media

exFAT vs FAT32:
  SD cards ≥ 64 GB: SDXC spec requires exFAT
  USB drives > 32 GB: exFAT or NTFS
  Cross-platform: exFAT is supported natively on Windows, macOS, Linux (kernel 5.4+)
  
Commands:
  mkfs.fat -F 32 /dev/sdb1          # Format FAT32
  mkfs.exfat /dev/sdb1              # Format exFAT
  fsck.fat /dev/sdb1                # Check FAT32
  exfatfsck /dev/sdb1               # Check exFAT
```

---

## 10. F2FS — Flash-Friendly FS

F2FS (Flash-Friendly File System) was developed by Samsung (2012) specifically for NAND flash storage — phones, embedded SSDs, SD cards.

```
Key design choices for flash:
  Log-structured: append-only writes (avoids random writes that wear NAND)
  Hot/cold data separation: frequently changed data (hot) vs static data (cold)
    Separated to different NAND regions → hot data wears its region, cold data preserved
  Node Address Table: two-level indirection for fast metadata access
  Multi-head logging: parallel write streams for metadata and data
  
Benefits vs ext4 on flash:
  Better random write performance on eMMC/SD
  Less write amplification (NAND endurance)
  Faster mount after unclean shutdown (roll-forward recovery)
  
Used by:
  Android internal storage (eMMC/UFS) — Samsung, many others
  ChromeOS (some configurations)
  
Commands:
  mkfs.f2fs /dev/mmcblk0p1          # Format
  fsck.f2fs /dev/mmcblk0p1          # Check
  mount -t f2fs /dev/mmcblk0p1 /data
```

---

## 11. tmpfs & ramfs — Memory File Systems

### tmpfs

```
tmpfs: a filesystem entirely in RAM (and swap).
  Located at: /tmp, /run, /dev/shm on modern Linux systems
  
Properties:
  Extremely fast (RAM speed)
  Size grows/shrinks dynamically as files are added/removed
  Can use swap if RAM pressure is high
  All data LOST on reboot
  
Mount:
  mount -t tmpfs -o size=1G tmpfs /mnt/ramdisk
  mount -t tmpfs -o size=50% tmpfs /mnt/ramdisk  # 50% of RAM

/etc/fstab:
  tmpfs   /tmp   tmpfs   defaults,size=2G,mode=1777   0 0

Common uses:
  /tmp:     Temporary file storage (auto-cleaned on reboot)
  /run:     PID files, sockets, runtime data
  /dev/shm: POSIX shared memory (applications use for IPC)
  Build cache: compile in RAM for much faster builds
    export TMPDIR=/dev/shm && cmake --build . (builds in RAM, faster on HDDs)
  
tmpfs on modern Linux:
  /tmp as tmpfs: default on many distros (Arch, Ubuntu 22.04+)
  Check: df -h /tmp | grep tmpfs
```

### ramfs

```
ramfs: simpler, older predecessor to tmpfs
  No size limit (can fill ALL of RAM — dangerous!)
  Cannot use swap
  No disk backing at all
  
tmpfs is almost always preferred over ramfs.
Use ramfs only if you specifically don't want swap usage.
```

---

## 12. FUSE — User-Space File Systems

FUSE (Filesystem in Userspace) allows implementing a filesystem in a regular user-space program without kernel code.

```
How FUSE works:
  Kernel receives filesystem call (open, read, write, readdir...)
  Kernel VFS checks: is this path on a FUSE mount?
  If yes: forward call to FUSE kernel module
  FUSE module: send request to user-space daemon via /dev/fuse
  User daemon: handle request (can do anything: network, encryption, transformation)
  User daemon: send response back
  FUSE module: return result to caller

Performance: ~30–50% slower than kernel filesystems (user-kernel round trip)
Use case: flexibility >> performance is acceptable

Popular FUSE filesystems:
  sshfs:     Mount remote directories over SSH
    sshfs user@server:/path /mnt/remote
    
  s3fs:      Mount Amazon S3 bucket as filesystem
    s3fs mybucket /mnt/s3 -o passwd_file=~/.s3cfg
    
  encfs:     Encrypted overlay filesystem
    encfs ~/.encrypted ~/decrypted
    
  gocryptfs: Modern AES-GCM encrypted filesystem (recommended over encfs)
    gocryptfs -init ~/.vault && gocryptfs ~/.vault ~/decrypted
    
  ntfs-3g:   NTFS support via FUSE (legacy, see §7)
  
  apfs-fuse: Read-only macOS APFS support on Linux (see §8)
  
  rclone mount: Mount any cloud storage (Google Drive, Dropbox, S3, etc.)
    rclone mount gdrive:/ /mnt/gdrive --vfs-cache-mode full

Writing a FUSE filesystem (Python):
  pip install fusepy
  # Implement: getattr, read, write, readdir, open, create, unlink...
  # Mount and all standard filesystem calls work automatically
```

---

## 13. Network File Systems

```
NFS (Network File System):
  Most common Linux network FS
  Server exports directories, clients mount them
  
  # Server (install nfs-kernel-server)
  echo "/data 192.168.1.0/24(rw,sync,no_subtree_check)" >> /etc/exports
  exportfs -r
  
  # Client
  mount -t nfs server:/data /mnt/nfs
  # /etc/fstab: server:/data /mnt/nfs nfs defaults,_netdev 0 0

Samba/CIFS (Windows File Sharing):
  Used for: Windows shares, NAS devices
  
  # Mount a Windows share
  mount -t cifs //server/share /mnt/share -o username=user,password=pass
  
  # With credentials file
  mount -t cifs //server/share /mnt/share -o credentials=/etc/.cifs-creds

SSHFS (SSH File System):
  Mount any SSH-accessible server as local directory
  Uses SFTP protocol over SSH
  
  sshfs user@server:/ /mnt/remote
  fusermount -u /mnt/remote           # Unmount

GlusterFS:
  Distributed filesystem for scale-out NAS
  Redundancy across multiple servers

CephFS:
  Distributed filesystem from the Ceph storage system
  Used in large-scale cloud infrastructure (OpenStack, Kubernetes)
  
9P (Plan 9 File Protocol):
  Used by: QEMU virtio-9p, WSL2, Lima, VS Code devcontainers
  Efficient for virtual machine shared folders
```

---

## 14. Virtual File Systems

Linux VFS provides special filesystems that expose kernel data as readable/writable files.

```
/proc (procfs):
  Process and kernel information as files
  /proc/cpuinfo:        CPU details
  /proc/meminfo:        Memory statistics
  /proc/[pid]/status:   Process status
  /proc/[pid]/maps:     Memory mappings
  /proc/[pid]/fd/:      Open file descriptors (symlinks)
  /proc/sys/:           Tunable kernel parameters
    echo 1 > /proc/sys/net/ipv4/ip_forward    # Enable IP forwarding
  /proc/net/:           Network statistics

/sys (sysfs):
  Hardware and driver information
  /sys/class/net/:      Network interfaces
  /sys/block/:          Block devices
  /sys/bus/pci/:        PCI devices
  /sys/power/state:     System power states
    echo mem > /sys/power/state              # Suspend to RAM

/dev (devtmpfs):
  Device files
  /dev/sda, /dev/nvme0n1:    Block devices
  /dev/tty, /dev/pts/:       Terminals
  /dev/null:                 Discard all writes, returns EOF on read
  /dev/zero:                 Returns infinite stream of zero bytes
  /dev/urandom:              Cryptographically secure random bytes
  /dev/random:               Blocks until entropy pool refills (legacy behavior)
  /dev/mem:                  Physical memory (requires root, most systems restrict)
  
  dd if=/dev/urandom of=random.bin bs=1M count=10  # Generate 10MB random file
  dd if=/dev/zero of=/dev/sdb bs=1M status=progress  # Zero a disk

/run:
  Runtime data, cleared on boot
  PID files: /run/nginx.pid
  Sockets: /run/dbus/system_bus_socket
  Implements as tmpfs
  
cgroups v2 (/sys/fs/cgroup):
  Hierarchical resource control filesystem
  Write PIDs, read statistics, set limits via file writes
  
debugfs (/sys/kernel/debug):
  Kernel debugging interface
  Requires: mount -t debugfs debugfs /sys/kernel/debug
  Used by: ftrace, perf, eBPF
```

---

## 15. File System Operations Reference

```bash
# Create filesystems
mkfs.ext4 /dev/sdb1
mkfs.btrfs /dev/sdb1
mkfs.xfs /dev/sdb1
mkfs.fat -F 32 /dev/sdb1
mkfs.exfat /dev/sdb1
zpool create poolname /dev/sdb

# Check/repair (UNMOUNTED)
e2fsck -f /dev/sdb1               # ext2/3/4
btrfs check /dev/sdb1             # Btrfs
xfs_repair /dev/sdb1              # XFS
fsck.fat /dev/sdb1                # FAT32
zpool scrub poolname              # ZFS (online)

# Mount
mount /dev/sdb1 /mnt
mount -t ext4 -o ro /dev/sdb1 /mnt          # Read-only
mount -o remount,rw /mnt                     # Remount read-write
mount -o loop disk.img /mnt                  # Mount image file
umount /mnt

# Partition info
lsblk -f                     # Block devices + filesystem types + mount points
blkid                         # UUIDs and filesystem types
fdisk -l                      # Partition table
parted /dev/sdb print         # Parted info

# /etc/fstab (persistent mounts)
UUID=abc123  /mnt/data  ext4  defaults  0 2
# format: device  mountpoint  type  options  dump  fsck-order
# Use UUID (not /dev/sdX) — device names can change between boots

# Get UUID for fstab
blkid /dev/sdb1 | grep UUID

# Disk usage
df -h                         # Filesystem space usage
df -i                         # Inode usage
du -sh /path                  # Directory size
du -h --max-depth=1 /var      # Directory tree sizes
ncdu /                        # Interactive ncurses disk usage browser

# Find large files
find / -type f -size +1G -exec ls -lh {} \; 2>/dev/null
```

---

## 16. Choosing a File System

```
Linux root partition (desktop):
  ext4:   Safe, well-tested, widely supported. Default on Ubuntu/Debian.
  Btrfs:  Snapshots, CoW, compression. Default on Fedora/openSUSE. Slightly more complex.
  → ext4 for simplicity, Btrfs for snapshots and compression

Linux server (large files, databases):
  XFS:    Large file performance, parallel I/O. RHEL/Fedora default.
  ext4:   Reliable, fast enough for most workloads.
  ZFS:    Maximum data integrity, snapshots, RAID built-in. Use on NAS/storage servers.

NAS / Home Server:
  ZFS:    Best choice: checksums, snapshots, CoW, built-in RAID
  Btrfs:  Good alternative, native Linux, simpler than ZFS
  → ZFS for maximum reliability, Btrfs for flexibility

Flash storage (phone, SD card, embedded):
  F2FS:   Best for internal flash (phones, eMMC)
  ext4:   Acceptable with journal on UFS storage
  exFAT:  SD cards, portability across devices

Cross-platform (must work on Windows + Mac + Linux):
  exFAT:  Best choice: no 4 GB limit, supported everywhere natively
  FAT32:  If files < 4 GB and maximum compatibility needed
  NTFS:   If Windows-centric, Linux can read/write (ntfs3 kernel driver)

Boot partitions:
  EFI System Partition: FAT32 (required by UEFI spec)
  /boot: ext4 (most bootloaders support it)
  
Windows default: NTFS
macOS default:   APFS (HFS+ on older Macs)
Android default: F2FS (Samsung) or ext4 (others)
ChromeOS:        ext4 / squashfs (system)
Raspberry Pi:    FAT32 (/boot) + ext4 (root)
```

---

## See Also

- [Linux Internals](linux-internals.md) — VFS layer, page cache, block I/O stack
- [Storage Technology](storage-technology.md) — NAND flash, RAM, USB, NVMe hardware
- [Wine Compatibility Layer](wine-compatibility.md) — Wine's C: drive is a directory on your Linux FS
- [Docker Essentials](../devtools/docker-essentials.md) — Overlay filesystem (OverlayFS) used by Docker
