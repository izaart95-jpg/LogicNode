# Linux Internals — Deep Dive

This document goes deep into Linux kernel internals — beyond the overview in [Kernel Architecture](kernel-architecture.md). It covers the scheduler, memory management, virtual filesystem, system calls in detail, networking stack, eBPF, and how every major kernel subsystem works from the inside.

> **Prerequisite:** Read [Kernel Architecture](kernel-architecture.md) first for the overview and basic commands. This document assumes that foundation.

---

## Table of Contents
1. [Process & Thread Model](#1-process--thread-model)
2. [The Scheduler — CFS Deep Dive](#2-the-scheduler--cfs-deep-dive)
3. [Memory Management](#3-memory-management)
4. [Virtual Filesystem (VFS)](#4-virtual-filesystem-vfs)
5. [System Call Internals](#5-system-call-internals)
6. [Signals](#6-signals)
7. [IPC — Inter-Process Communication](#7-ipc--inter-process-communication)
8. [The Networking Stack](#8-the-networking-stack)
9. [Block I/O and Storage Stack](#9-block-io-and-storage-stack)
10. [cgroups — Resource Control](#10-cgroups--resource-control)
11. [Namespaces — Isolation](#11-namespaces--isolation)
12. [eBPF — Extended Berkeley Packet Filter](#12-ebpf--extended-berkeley-packet-filter)
13. [Kernel Locking & Synchronization](#13-kernel-locking--synchronization)
14. [The Boot Process](#14-the-boot-process)

---

## 1. Process & Thread Model

In Linux, both processes and threads are represented by `struct task_struct` — the same data structure. The difference is in what they share.

### task_struct — The Process Descriptor

`task_struct` is the largest structure in the kernel, containing everything the kernel knows about a process:

```c
struct task_struct {
    /* Scheduling */
    volatile long state;           // TASK_RUNNING, TASK_INTERRUPTIBLE, TASK_STOPPED...
    unsigned int flags;            // Per-process flags (PF_KTHREAD, PF_SUPERPRIV...)
    int on_cpu;                    // Which CPU is running this task
    struct sched_entity se;        // CFS scheduler entity (vruntime, etc.)

    /* Identity */
    pid_t pid;                     // Process ID
    pid_t tgid;                    // Thread group ID (process ID for main thread)
    uid_t uid, gid;                // Effective user/group IDs
    struct cred *cred;             // Credentials (full capability set)

    /* Memory */
    struct mm_struct *mm;          // Virtual address space descriptor (NULL for kernel threads)
    struct mm_struct *active_mm;   // Active mm (kernel threads borrow from last user process)

    /* Files */
    struct files_struct *files;    // Open file descriptors
    struct fs_struct *fs;          // Filesystem info (root, cwd)

    /* Signal handling */
    struct signal_struct *signal;  // Shared signal queue (all threads in process share this)
    struct sighand_struct *sighand; // Signal handlers (sigaction per signal)
    sigset_t blocked;              // Mask of blocked signals

    /* Relationships */
    struct task_struct *parent;    // Parent process
    struct list_head children;     // List of children
    struct list_head sibling;      // Sibling processes

    /* Timers and stats */
    cputime_t utime, stime;        // User and system CPU time
    struct timespec64 start_time;  // When task was created

    /* Stack */
    void *stack;                   // Kernel stack (usually 16 KB)

    /* Namespaces */
    struct nsproxy *nsproxy;       // Pointer to all namespace structs

    /* cgroups */
    struct css_set *cgroups;       // cgroup membership

    // ... ~600 more fields
};
```

### Process States

```
TASK_RUNNING:         Actively running on a CPU or ready to run (in run queue)
TASK_INTERRUPTIBLE:   Sleeping, waiting for event; can be woken by signal
TASK_UNINTERRUPTIBLE: Deep sleep; cannot be woken by signal (e.g., waiting for I/O)
                      Appears as 'D' in ps output — "D state" processes
TASK_STOPPED:         Stopped by SIGSTOP or SIGTSTP; waiting for SIGCONT
TASK_TRACED:          Being debugged (ptrace attached — used by strace, gdb)
TASK_ZOMBIE:          Task has exited; waiting for parent to read exit status via wait()
                      Process entry cleaned up once parent calls wait()
```

### Process vs Thread Creation

```c
// fork() — new process, copies address space (copy-on-write)
pid_t pid = fork();
// Child gets new PID, new address space (COW mapped pages)
// Shares file descriptors initially (close-on-exec may close some)
// Each write to a shared page triggers COW: page is duplicated

// clone() — flexible process/thread creation (what fork() and pthread_create() use)
// Flags control what is shared:
int flags = SIGCHLD;                           // fork() — share nothing (new process)
int flags = CLONE_VM | CLONE_FS | CLONE_FILES   // pthread_create() — share everything (thread)
          | CLONE_SIGHAND | CLONE_THREAD;

// Threads share: address space (CLONE_VM), file descriptors, signal handlers
// Threads have own: stack, registers, signal mask, TLS (thread-local storage)

// vfork() — share address space with parent until exec() or exit
// Parent is suspended until child execs or exits
// Used for fork+exec patterns: minimizes COW overhead
```

---

## 2. The Scheduler — CFS Deep Dive

Linux's Completely Fair Scheduler (CFS) aims to give each task its fair share of CPU time proportional to its weight (nice value).

### Virtual Runtime (vruntime)

CFS tracks `vruntime` — the amount of CPU time a task has conceptually received, adjusted by its weight:

```
vruntime += delta_execution * NICE_0_WEIGHT / task_weight

Where:
  delta_execution = actual time spent on CPU
  NICE_0_WEIGHT   = weight of a nice-0 task (1024 by default)
  task_weight     = weight corresponding to nice value
                    (nice -20 = 88761, nice 0 = 1024, nice 19 = 15)

Key insight: a task with 2× the weight will have its vruntime increase 2× slower
→ it gets scheduled 2× more often to accumulate 2× more CPU time
```

### Red-Black Tree

CFS stores all runnable tasks in a red-black tree ordered by `vruntime`:

```
          [vruntime: 50]
          /             \
    [vruntime: 30]    [vruntime: 70]
    /        \
[vruntime: 20] [vruntime: 40]

The task with smallest vruntime (leftmost node) is always next to run.
Insertion, deletion, and lookup: O(log N) where N = number of runnable tasks.

CFS picks the next task:
  1. Get leftmost node of the tree
  2. Run it for min(timeslice, scheduler_latency/nr_running)
  3. Re-insert with updated vruntime
  4. Go to step 1
```

### Scheduler Latency

```
scheduler_latency: 6–48ms (scales with number of tasks)
  = how long it takes every task to get at least one turn

Minimum granularity: 0.75ms
  = minimum time a task runs before being preempted

With N running tasks:
  timeslice = scheduler_latency / N (but at least min_granularity)
```

### Priority and Nice Values

```
Nice values: -20 (highest priority) to +19 (lowest priority)
  Mapped to weights: nice -20 = 88761, nice 0 = 1024, nice 19 = 15

Real-time scheduling policies (bypass CFS entirely):
  SCHED_FIFO:    Real-time, first-in-first-out, no timeslice
  SCHED_RR:      Real-time, round-robin with timeslice
  SCHED_DEADLINE: Earliest-deadline-first (EDF) scheduling

Priority order:
  SCHED_DEADLINE > SCHED_FIFO/RR > CFS (SCHED_NORMAL/BATCH/IDLE)
```

```bash
# View scheduler info
cat /proc/$(pgrep firefox)/sched    # Scheduler statistics for a process
chrt -p $(pgrep my_rt_app)         # Check real-time priority

# Change nice value (priority)
nice -n 10 ./cpu_intensive_task    # Start with nice 10
renice -n 5 -p $(pgrep app)        # Change running process

# Set real-time scheduling
sudo chrt -f -p 50 $(pgrep critical_app)  # FIFO priority 50

# CPU affinity — pin process to specific CPUs
taskset -c 0,1 ./program                  # Run only on CPUs 0 and 1
taskset -cp 0,1 $(pgrep app)             # Pin running process
```

---

## 3. Memory Management

### Virtual Memory Layout (x86-64 Linux)

```
0xFFFF_FFFF_FFFF_FFFF  ─────────────────────
                         Kernel space (128 TB)
  VMALLOC area          Kernel dynamic allocations (vmalloc)
  KASAN shadow memory   AddressSanitizer shadow (debug builds)
  Kernel code           .text, .data, .bss (physical = virtual - 0xFFFF_8000_0000_0000)
  physmap               Direct 1:1 mapping of all physical RAM
  Kernel stacks         One 16KB stack per thread
  Modules               Loadable kernel modules (.ko)

0xFFFF_8000_0000_0000  ─────────────────────
                         (non-canonical hole: 64-bit architecture gap)
0x0000_7FFF_FFFF_FFFF  ─────────────────────
                         User space (128 TB usable)
  Stack                 Top of address space, grows DOWN
  |                     (ulimit -s controls max size, default 8MB)
  ↓
  mmap region           Shared libraries, mmap() calls, anonymous mappings
  |
  ↑
  Heap                  malloc()/free(), grows UP via brk() syscall
  BSS                   Uninitialized global variables (zero-initialized)
  Data                  Initialized global variables
  Text                  Executable code (read-only)
  vDSO/vvar             Kernel-provided user-space page (fast clock, syscall ABI)
0x0000_0000_0000_0000  ─────────────────────
```

### Page Tables (x86-64)

Virtual address translation uses a 4-level page table on x86-64 (5-level with LA57):

```
Virtual address: [PML4 index (9 bits)] [PDP index (9 bits)] [PD index (9 bits)] [PT index (9 bits)] [Offset (12 bits)]

Translation:
  CR3 register → Physical address of PML4 table
  PML4[index]  → Physical address of PDP table
  PDP[index]   → Physical address of PD table
  PD[index]    → Physical address of PT table
  PT[index]    → Physical address of 4KB page
  Add offset   → Final physical address

TLB (Translation Lookaside Buffer):
  Caches recent virtual→physical translations
  ~1500 entries (varies by CPU)
  Context switch: flushes TLB (INVLPG / INVPCID)
  ASID (Address Space ID): allows TLB entries tagged per process (avoids full flush)
```

### Page Fault Handling

```c
// When a virtual address is accessed but has no valid page table entry:
// CPU raises #PF exception → handle_page_fault() in kernel

// Cases:
//   1. Access to unmapped region → SIGSEGV (segmentation fault)
//   2. Write to read-only page → SIGSEGV
//   3. COW (Copy-on-Write) fault:
//        Page is shared but write was attempted
//        → Allocate new page, copy data, map to writing process
//   4. Demand paging:
//        Page was never loaded (file-backed or anon, not yet in memory)
//        → Load page from file/swap, update page tables
//   5. Guard page fault:
//        Stack needs to grow → extend stack mapping
//   6. Swap fault:
//        Page was swapped to disk
//        → Read page from swap, update page tables, wake up process

void do_page_fault(struct pt_regs *regs, unsigned long error_code, unsigned long address) {
    struct vm_area_struct *vma = find_vma(current->mm, address);
    if (!vma || vma->vm_start > address) {
        // No VMA covers this address → SIGSEGV
        force_sig_fault(SIGSEGV, SEGV_MAPERR, address);
        return;
    }
    handle_mm_fault(vma, address, flags, regs);
}
```

### Memory Allocators

**Buddy Allocator (page allocator):**
```
Manages physical pages in groups of 2^N (buddies).
  Free list for order 0 (1 page = 4KB)
  Free list for order 1 (2 pages = 8KB)
  Free list for order 2 (4 pages = 16KB)
  ...
  Free list for order 11 (2048 pages = 8MB)

Allocation: find smallest free block ≥ requested size
  If too big: split in half, put one half on next-lower free list
Deallocation: if buddy (adjacent same-size block) is also free → merge into larger block

External fragmentation: unavoidable for larger orders — no page of order > highest_available
```

**SLAB/SLUB Allocator (kmalloc):**
```
Object cache allocator for frequently allocated kernel structures.
Maintains per-object-size "slabs" — groups of pages pre-carved into fixed-size objects.

struct kmem_cache for each type:
  "task_struct": objects of sizeof(task_struct) = 9568 bytes
  "inode_cache": objects of sizeof(struct inode) = 648 bytes
  "dentry": objects of sizeof(struct dentry) = 192 bytes

Per-CPU caches: each CPU has a cache of recently freed objects
  → Allocation from per-CPU cache: O(1), no lock required
  → When per-CPU cache is empty: refill from slab (spinlock required)

SLUB (modern default): simpler than SLAB, better debugging support, per-CPU slabs
```

```bash
# View memory usage
cat /proc/meminfo                 # System-wide memory breakdown
cat /proc/buddyinfo               # Buddy allocator free lists per zone
cat /proc/slabinfo                # SLAB/SLUB per-cache statistics
sudo slabtop                      # Real-time slab usage top-like view

# Per-process memory
cat /proc/$(pgrep chrome)/status  # VmRSS, VmVirtual, etc.
cat /proc/$(pgrep chrome)/maps    # All memory mappings
cat /proc/$(pgrep chrome)/smaps   # Detailed per-mapping stats

# Free memory with confidence
free -h
vmstat 1                          # Memory stats every second
```

---

## 4. Virtual Filesystem (VFS)

VFS is an abstraction layer that provides a uniform interface for all filesystems. Every filesystem (ext4, XFS, Btrfs, NFS, procfs, tmpfs, devtmpfs...) registers operations with VFS, which routes all file operations to the appropriate implementation.

### VFS Data Structures

```c
struct super_block {
    // Represents a mounted filesystem
    struct file_system_type *s_type;     // ext4_fs_type, xfs_fs_type...
    struct super_operations *s_op;       // read_inode, write_inode, sync_fs...
    unsigned long s_flags;               // MS_RDONLY, MS_NOSUID...
    struct dentry *s_root;               // Root directory dentry
    struct list_head s_inodes;           // All inodes in this filesystem
    void *s_fs_info;                     // Filesystem-private data (ext4_sb_info etc.)
};

struct inode {
    // Represents a file or directory (metadata only, no filename)
    unsigned long i_ino;                 // Inode number
    umode_t i_mode;                      // File type + permissions (rwxrwxrwx)
    uid_t i_uid; gid_t i_gid;           // Owner
    loff_t i_size;                       // File size in bytes
    struct timespec64 i_mtime;           // Modification time
    struct inode_operations *i_op;       // lookup, create, link, unlink, mkdir...
    struct file_operations *i_fop;       // open, read, write, mmap, ioctl...
    struct address_space *i_mapping;     // Page cache for this file's data
    void *i_private;                     // Filesystem-private inode data
};

struct dentry {
    // Represents a directory entry (filename → inode mapping)
    // Cached in the dcache (dentry cache) for fast path lookups
    struct inode *d_inode;               // Inode this name points to
    struct dentry *d_parent;             // Parent directory
    struct qstr d_name;                  // Filename (quick string: hash + name)
    struct dentry_operations *d_op;      // hash, compare, revalidate...
    struct list_head d_subdirs;          // Children (subdirectories)
};

struct file {
    // Represents an open file descriptor
    // Created by open(), destroyed by close()
    struct dentry *f_path.dentry;        // What file is open
    struct file_operations *f_op;        // read, write, seek, mmap, ioctl...
    loff_t f_pos;                        // Current file position (seek pointer)
    unsigned int f_flags;                // O_RDONLY, O_WRONLY, O_NONBLOCK...
    void *private_data;                  // Driver/fs private data (e.g., socket buffer)
    struct fown_struct f_owner;          // For async I/O notification
};
```

### Path Lookup (namei)

```
open("/home/user/documents/file.txt", O_RDONLY)

Kernel path lookup:
  1. Start at root dentry (/) or current directory (.)
  2. Split path into components: ["home", "user", "documents", "file.txt"]
  3. For each component:
     a. Check dentry cache (dcache) — hash lookup on parent + name
     b. Cache hit: use cached dentry → get inode
     c. Cache miss: call parent's inode->i_op->lookup(parent_inode, "home")
                   → ext4 lookup: read directory blocks, find entry
                   → allocate new dentry, add to dcache
  4. Permission check at each step (execute bit on directory = can traverse)
  5. Handle symlinks (recursive lookup of link target)
  6. Final component: get/create inode, open file, create struct file

Dcache is the most performance-critical cache in the kernel.
  Negative dentries: cache "file doesn't exist" to avoid disk lookups
  RCU-based lockless lookup: read path without taking any locks (modern kernel)
```

### Page Cache

The page cache stores file data in RAM, mapping (inode, page_index) → physical page:

```
read() from file:
  1. Compute page index = file_offset / PAGE_SIZE
  2. Look up page in page cache: find_get_page(inode->i_mapping, index)
  3. Cache hit: copy data from page to user buffer
  4. Cache miss: allocate new page, call readpage() to fill from disk
                → submits bio (block I/O request) to block layer
                → process sleeps until I/O completes
                → page added to page cache
                → copy to user buffer

write() to file:
  1. Find/allocate page in cache
  2. Copy user data to page
  3. Mark page dirty
  4. Optionally: call balance_dirty_pages() if too many dirty pages
  5. pdflush/writeback thread periodically flushes dirty pages to disk

mmap():
  1. Create VMA (vm_area_struct) mapping virtual range to file
  2. On first access: page fault → find page in cache or read from disk
  3. Map cache page directly into process virtual address space
  4. No copy — process reads/writes directly to/from cache pages
```

---

## 5. System Call Internals

```c
// What happens when user code calls read(fd, buf, count)

// User space: glibc wrapper
ssize_t read(int fd, void *buf, size_t count) {
    return syscall(SYS_read, fd, buf, count);
    // Compiles to:
    //   mov rax, 0        (SYS_read = 0 on x86-64)
    //   mov rdi, fd
    //   mov rsi, buf
    //   mov rdx, count
    //   syscall           (trap to ring 0)
    //   cmp rax, 0        (check for error)
    //   jge return_success
    //   neg rax           (error: kernel returns -ERRNO, glibc returns -1 + sets errno)
    //   mov errno, eax
    //   mov rax, -1
    //   ret
}

// Kernel entry point (arch/x86/entry/entry_64.S)
// SYSCALL instruction:
//   1. Saves user RIP, RSP, RFLAGS to MSRs
//   2. Loads kernel RSP from MSR_LSTAR kernel stack
//   3. Switches to kernel GS
//   4. Jumps to do_syscall_64()

// do_syscall_64() (arch/x86/entry/common.c)
__visible noinstr void do_syscall_64(struct pt_regs *regs, int nr) {
    // Validate syscall number
    if ((unsigned long)nr < NR_syscalls) {
        // Call the actual implementation via syscall table
        regs->ax = sys_call_table[nr](
            regs->di, regs->si, regs->dx,
            regs->r10, regs->r8, regs->r9
        );
        // sys_call_table[0] = __x64_sys_read
        // sys_call_table[1] = __x64_sys_write
        // sys_call_table[2] = __x64_sys_open
        // ... 400+ entries
    }
    syscall_exit_to_user_mode(regs);
}

// The actual read implementation (fs/read_write.c)
SYSCALL_DEFINE3(read, unsigned int, fd, char __user *, buf, size_t, count) {
    struct fd f = fdget_pos(fd);     // Get struct file * from fd number
    if (!f.file) return -EBADF;      // fd not valid
    loff_t pos = file_pos_read(f.file);
    ssize_t ret = vfs_read(f.file, buf, count, &pos);
    if (ret >= 0) file_pos_write(f.file, pos);
    fdput_pos(f);
    return ret;
}
```

### vDSO — Virtual Dynamic Shared Object

```
Some syscalls don't need to trap to ring 0:
  clock_gettime(), gettimeofday(), time(), getcpu()

vDSO: kernel maps a special page into every process's address space
      This page contains:
        - current time (updated by kernel at each tick, readable without syscall)
        - CPU number
        - Syscall implementation that reads these directly

  clock_gettime() with CLOCK_MONOTONIC:
    Old: trap to kernel (~100ns overhead), kernel reads clock, return
    vDSO: read kernel-updated time directly from mapped page (~5ns)

See the vDSO:
  cat /proc/self/maps | grep vdso
  0x7ffd...000-0x7ffd...000 r-xp 00000000 00:00 0  [vdso]
```

---

## 6. Signals

Signals are asynchronous notifications sent to processes.

### Signal Delivery

```c
// Sending a signal
kill(pid, SIGTERM);      // From another process (requires permission)
raise(SIGUSR1);          // Send to self
pthread_kill(tid, sig);  // Send to specific thread

// In the kernel:
// kill() → find_vpid(pid) → send_signal_locked() →
//   Adds siginfo to target's pending signal queue
//   Wakes target if it's sleeping: sets TIF_SIGPENDING flag

// Delivery timing: signals are delivered when returning from kernel to user space
//   After syscall
//   After interrupt handler
//   After preemption

// Signal handling in kernel exit path:
exit_to_user_mode_prepare() → handle_signal_work() →
  Check TIF_SIGPENDING flag
  → dequeue_signal() → get next pending signal
  → get_signal() → look up handler from sighand->action[sig]
  → Handle: run handler, SIG_DFL (default), SIG_IGN (ignore)
```

### Signal Handlers

```c
#include <signal.h>

// sigaction — proper signal handling
struct sigaction sa = {0};
sa.sa_handler = my_handler;           // Simple handler (no siginfo)
// OR
sa.sa_sigaction = my_sigaction;       // Extended handler (with siginfo)
sa.sa_flags = SA_SIGINFO | SA_RESTART;  // Pass siginfo, auto-restart interrupted syscalls
sigemptyset(&sa.sa_mask);            // Don't block additional signals during handler
sigaction(SIGTERM, &sa, NULL);

void my_sigaction(int signo, siginfo_t *info, void *context) {
    // info->si_signo: signal number
    // info->si_code: SI_USER (kill()), SI_KERNEL (hardware fault), ...
    // info->si_pid: sending process's PID
    // context: ucontext_t* — can examine/modify registers at point of interrupt
}

// Signal mask — block signals from delivery
sigset_t mask;
sigemptyset(&mask);
sigaddset(&mask, SIGINT);   // Block SIGINT
sigprocmask(SIG_BLOCK, &mask, &old_mask);
// ... critical section ...
sigprocmask(SIG_SETMASK, &old_mask, NULL);  // Restore

// Default actions for common signals:
// SIGTERM: terminate (graceful, can be caught)
// SIGKILL: terminate (cannot be caught or blocked)
// SIGSTOP: stop process (cannot be caught or blocked)
// SIGCONT: continue stopped process
// SIGSEGV: invalid memory access (generate core dump by default)
// SIGBUS:  bus error (misaligned memory access)
// SIGFPE:  floating point exception (divide by zero, overflow)
// SIGCHLD: child process changed state
// SIGUSR1/SIGUSR2: user-defined (application uses as needed)
// SIGPIPE: write to pipe with no readers (default: terminate)
```

---

## 7. IPC — Inter-Process Communication

### Pipes

```bash
# Anonymous pipe: unidirectional, between related processes
ls | grep ".txt"    # Shell creates pipe: ls writes, grep reads
                    # ls(stdout) → [pipe buffer 64KB] → grep(stdin)

# Named pipe (FIFO): persists in filesystem, unrelated processes
mkfifo /tmp/mypipe
cat /tmp/mypipe &   # Reader blocks waiting for data
echo "hello" > /tmp/mypipe   # Writer — reader unblocks
```

```c
int pipefd[2];
pipe(pipefd);        // pipefd[0]=read end, pipefd[1]=write end
if (fork() == 0) {   // Child
    close(pipefd[0]);
    write(pipefd[1], "data", 4);
    exit(0);
} else {             // Parent
    close(pipefd[1]);
    char buf[100];
    read(pipefd[0], buf, sizeof(buf));
}
```

### Unix Domain Sockets

```c
// Bidirectional, same machine only, much faster than TCP loopback
int sock = socket(AF_UNIX, SOCK_STREAM, 0);
struct sockaddr_un addr = {.sun_family = AF_UNIX};
strncpy(addr.sun_path, "/tmp/myapp.sock", sizeof(addr.sun_path));
bind(sock, (struct sockaddr*)&addr, sizeof(addr));
listen(sock, 5);
// → systemd, Docker daemon, DBus, X11 all use Unix sockets
```

### Shared Memory

```c
// POSIX shared memory — fastest IPC (zero copy)
// Create/open shared memory object
int fd = shm_open("/myshm", O_CREAT | O_RDWR, 0666);
ftruncate(fd, 4096);   // Set size

// Map into address space
void *ptr = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

// Write data (visible immediately to other processes with the same mapping)
*(int*)ptr = 42;

// Both processes need synchronization (mutex in shared memory, or semaphore):
pthread_mutex_t *mutex = ptr + sizeof(int);
pthread_mutexattr_t attr;
pthread_mutexattr_init(&attr);
pthread_mutexattr_setpshared(&attr, PTHREAD_PROCESS_SHARED);  // Cross-process mutex
pthread_mutex_init(mutex, &attr);
```

---

## 8. The Networking Stack

```
Application: send(sock, buf, len, 0)
      ↓
Socket API (BSD sockets layer)
  struct socket → struct sock (protocol state machine)
      ↓
Transport layer: TCP/UDP/RAW
  TCP: congestion control, retransmission, flow control
  sk_buff manipulation: add TCP header
      ↓
Network layer: IPv4/IPv6
  Route lookup: fib_lookup() → find output interface and next hop
  Netfilter/iptables hooks: NF_INET_LOCAL_OUT
  sk_buff: add IP header
      ↓
Network device layer
  dev_queue_xmit() → qdisc (Traffic Control queue discipline: pfifo, htb, fq...)
      ↓
NIC driver
  DMA ring buffer → kick NIC to transmit
  NIC transmits on wire
```

### sk_buff — The Socket Buffer

```c
struct sk_buff {
    // Doubly-linked list management
    struct sk_buff *next, *prev;
    struct sock *sk;          // Owning socket

    // Data pointers
    unsigned char *head;      // Allocated memory start
    unsigned char *data;      // Current data start (after headers are consumed)
    unsigned char *tail;      // Current data end
    unsigned char *end;       // Allocated memory end

    // sk_buff is like a rope:
    // [head.....data..payload..tail.....end]
    //           ↑ data
    // To add a header: skb_push(skb, sizeof_header) → data -= sizeof_header
    // To consume a header: skb_pull(skb, sizeof_header) → data += sizeof_header

    unsigned int len;         // Current data length (tail - data)
    unsigned int data_len;    // Length in frags (scatter-gather)
    __u16 protocol;           // ETH_P_IP, ETH_P_IPV6, etc.
    __u32 priority;           // QoS priority
    struct net_device *dev;   // Network device

    // Protocol headers (set by each layer as it processes the packet)
    union { struct tcphdr *th; struct udphdr *uh; ... } h;
    union { struct iphdr *iph; struct ipv6hdr *ipv6h; ... } nh;
    union { struct ethhdr *ethernet; ... } mac;
};
```

### Netfilter / iptables

```
Netfilter hooks in the network stack:

  Incoming packet:
    NF_INET_PRE_ROUTING   → NF_INET_LOCAL_IN (for local processes)
                          → NF_INET_FORWARD (for routed packets)

  Outgoing packet:
    NF_INET_LOCAL_OUT → NF_INET_POST_ROUTING

Each hook: list of registered handlers (iptables rules are one such handler)
iptables rules evaluated in order: ACCEPT, DROP, RETURN, LOG, MASQUERADE...

nftables (modern replacement):
  More flexible than iptables, uses a bytecode VM to evaluate rules
  Same kernel hooks, different userspace tool
```

---

## 9. Block I/O and Storage Stack

```
Application: read(fd, buf, count)
      ↓
VFS: vfs_read() → generic_file_read_iter()
      ↓
Page cache: find_get_page() — hit? return cached data
                             — miss? submit_bio() to fill page
      ↓
Block layer: blk_mq (multi-queue block layer)
  I/O scheduler: merges and reorders requests
    none: no reordering (NVMe SSDs — already have internal queues)
    mq-deadline: deadline-based (prevent starvation)
    bfq: Budget Fair Queuing (good for desktops, mixed workloads)
      ↓
  Request queues (per hardware queue)
  DMA mapping: convert kernel virtual addresses to physical for DMA
      ↓
Block driver: SCSI, NVMe, virtio-blk
  NVMe: sends command to NVMe submission queue
  NIC: sends DMA address to device
  Device completes → interrupt → completion queue → page filled
      ↓
Hardware: NVMe SSD, SATA HDD, virtio (VM)
```

---

## 10. cgroups — Resource Control

cgroups (control groups) limit, account, and isolate resource usage of process groups. They are the foundation of containers (Docker, LXC, systemd services).

### cgroups v2

```bash
# cgroups v2 unified hierarchy at /sys/fs/cgroup/
ls /sys/fs/cgroup/
# cpu.max  memory.max  io.max  pids.max  ...

# Create a new cgroup
mkdir /sys/fs/cgroup/mygroup

# Set memory limit (200 MB)
echo "209715200" > /sys/fs/cgroup/mygroup/memory.max

# Set CPU limit (50% of one CPU = 50ms out of every 100ms period)
echo "50000 100000" > /sys/fs/cgroup/mygroup/cpu.max

# Add a process to the cgroup
echo $$ > /sys/fs/cgroup/mygroup/cgroup.procs

# View current cgroup membership
cat /proc/$$/cgroup
# 0::/mygroup     (cgroups v2 unified hierarchy)

# systemd uses cgroups automatically per service
systemctl show myapp | grep -i cgroup
systemd-cgls     # Show cgroup tree
systemd-cgtop    # cgroup resource usage
```

### cgroup Controllers

| Controller | Resource | Key Files |
|-----------|---------|-----------|
| **cpu** | CPU bandwidth | cpu.max (quota/period), cpu.weight |
| **memory** | RAM + swap | memory.max, memory.high, memory.current |
| **io** | Block I/O | io.max (rbps/wbps/riops/wiops per device) |
| **pids** | Process count | pids.max |
| **cpuset** | CPU/NUMA pinning | cpuset.cpus, cpuset.mems |
| **freezer** | Pause/resume | cgroup.freeze |
| **devices** | Device access | (v1 only; v2 uses BPF) |

---

## 11. Namespaces — Isolation

Namespaces wrap global system resources in an abstraction that appears private to processes in the namespace. Each namespace type isolates a different resource.

```bash
# View current namespaces
ls -la /proc/$$/ns/
# lrwxrwxrwx ... cgroup -> cgroup:[4026531835]
# lrwxrwxrwx ... ipc    -> ipc:[4026531839]
# lrwxrwxrwx ... mnt    -> mnt:[4026531840]
# lrwxrwxrwx ... net    -> net:[4026531992]
# lrwxrwxrwx ... pid    -> pid:[4026531836]
# lrwxrwxrwx ... user   -> user:[4026531837]
# lrwxrwxrwx ... uts    -> uts:[4026531838]
```

### Namespace Types

**Mount namespace (mnt):** Each namespace has its own filesystem hierarchy. Processes in different mount namespaces see different filesystem layouts. Foundation of container filesystems.

**PID namespace:** PIDs start at 1 inside the namespace. The process appearing as PID 1 inside a container is just another process from the host's view. Children namespaces can see their own PIDs only.

```bash
# A process in a PID namespace
unshare --fork --pid --mount-proc /bin/bash
# Inside: ps aux shows only a few processes (PID 1 = bash)
# Host: can see the real PID of our bash
```

**Network namespace (net):** Private network stack — own interfaces, routing tables, iptables rules, sockets. Used by containers to have isolated networking.

```bash
# Create network namespace
ip netns add myns
ip netns exec myns ip link list    # Only loopback visible
ip netns exec myns bash           # Shell inside namespace

# Create veth pair (virtual ethernet — two ends, like a cable)
ip link add veth0 type veth peer name veth1
ip link set veth1 netns myns     # Move one end into namespace
ip addr add 10.0.0.1/24 dev veth0
ip netns exec myns ip addr add 10.0.0.2/24 dev veth1
# Now: host can ping 10.0.0.2, container can ping 10.0.0.1
```

**UTS namespace:** Hostname and domain name isolation. Each container can have its own hostname.

**User namespace:** UID/GID mapping — a process can appear as root inside a user namespace without any real privileges on the host. Enables rootless containers.

**IPC namespace:** Private System V IPC (message queues, semaphores, shared memory) and POSIX message queues.

**Time namespace (since 5.6):** Isolate CLOCK_BOOTTIME and CLOCK_MONOTONIC offsets.

---

## 12. eBPF — Extended Berkeley Packet Filter

eBPF is a revolutionary kernel technology that lets you run sandboxed programs in the kernel without writing kernel modules. eBPF programs are verified for safety before running.

### What eBPF Can Do

```
eBPF programs can attach to:
  kprobes/kretprobes:  Any kernel function entry/exit
  uprobes/uretprobes:  Any user-space function entry/exit
  tracepoints:         Static instrumentation points in the kernel
  perf events:         CPU performance counters
  network hooks:       XDP (eXpress Data Path — before sk_buff allocation!)
                       TC (Traffic Control — after sk_buff)
                       socket operations
  LSM hooks:           Security policy decisions
  cgroup hooks:        Per-cgroup actions
```

### eBPF Architecture

```
User space tool (bpftool, bcc, libbpf)
  → compile eBPF C code to eBPF bytecode
  → bpf() syscall: load program into kernel
      ↓
Kernel verifier:
  - Bounds check all memory accesses
  - Verify no infinite loops (bounded loops allowed since 5.3)
  - Verify stack usage ≤ 512 bytes
  - Verify register types (prevent type confusion)
  → REJECT if unsafe

JIT compiler:
  - Translate verified eBPF bytecode to native machine code
  - x86-64, ARM64, RISC-V, etc.

eBPF Maps (shared data structures):
  Hash, Array, LRU Hash, LPM Trie, RingBuffer, Stack Trace...
  Shared between eBPF program (kernel) and user space
  bpf_map_lookup/update/delete from both sides

eBPF program (kernel):
  - Triggered at attachment point (kprobe, tracepoint, XDP...)
  - Reads context (CPU registers, packet data, syscall args)
  - Writes to maps, ring buffers, perf events
  - Returns decision (XDP_PASS, XDP_DROP, XDP_REDIRECT for network)
```

### eBPF Example — Tracing a Syscall

```c
// trace_open.bpf.c — using libbpf + BTF (BPF Type Format)
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>

// Map to store counts per PID
struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 1024);
    __type(key, u32);    // PID
    __type(value, u64);  // Open count
} open_count SEC(".maps");

// Attach to the openat syscall entry
SEC("tracepoint/syscalls/sys_enter_openat")
int trace_openat(struct trace_event_raw_sys_enter *ctx) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    u64 *count = bpf_map_lookup_elem(&open_count, &pid);
    if (count) {
        (*count)++;
    } else {
        u64 one = 1;
        bpf_map_update_elem(&open_count, &pid, &one, BPF_ANY);
    }
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
```

```bash
# BCC tools (Python frontend to eBPF)
pip install bcc

# Pre-built useful tools:
sudo execsnoop    # Trace exec() calls
sudo opensnoop    # Trace open() calls
sudo tcpconnect   # Trace TCP connections
sudo runqlat      # CPU run queue latency histogram
sudo biolatency   # Block I/O latency histogram
sudo funccount 'vfs_*'  # Count VFS function calls

# bpftool — inspect loaded eBPF programs
bpftool prog list
bpftool map list
bpftool net list
```

---

## 13. Kernel Locking & Synchronization

### Locking Primitives

**Spinlock:**
```c
spinlock_t lock;
spin_lock_init(&lock);

spin_lock(&lock);         // Acquire (spins if held — no sleep)
// critical section
spin_unlock(&lock);

// With IRQ disable (interrupt handlers on same CPU won't preempt):
spin_lock_irqsave(&lock, flags);
spin_unlock_irqrestore(&lock, flags);
```
Spinlocks: CPU busy-waits. Use only for very short critical sections. Never sleep while holding a spinlock.

**Mutex:**
```c
DEFINE_MUTEX(mymutex);

mutex_lock(&mymutex);     // Acquire (sleeps if held — can schedule)
// critical section
mutex_unlock(&mymutex);
```
Mutexes: sleeping lock. Task sleeps (removed from run queue) if mutex is held. Use for longer critical sections.

**RCU (Read-Copy-Update):**
```c
// Extremely efficient read-mostly data structures
// Readers: zero-cost, no lock
// Writers: copy the data structure, update, then replace atomically

// Reader side:
rcu_read_lock();
struct data *p = rcu_dereference(global_ptr);  // Safe pointer dereference
// Use p — guaranteed not to be freed while in RCU read-side critical section
rcu_read_unlock();

// Writer side:
struct data *new_data = kmalloc(sizeof(*new_data), GFP_KERNEL);
*new_data = *old_data;           // Copy
new_data->field = new_value;     // Modify copy
rcu_assign_pointer(global_ptr, new_data);  // Atomic pointer swap
synchronize_rcu();               // Wait for all existing readers to finish
kfree(old_data);                 // Safe to free now
```
RCU: the dcache, the process list, network routing tables, and hundreds of other kernel data structures use RCU. It allows lock-free concurrent reads.

---

## 14. The Boot Process

```
Power On
    ↓
UEFI / BIOS firmware
  - POST (Power-On Self Test)
  - Initialize CPU, RAM, buses
  - UEFI: locate and load EFI System Partition (ESP)
  - BIOS: locate MBR, jump to bootloader

GRUB2 (or systemd-boot)
  - Stage 1: tiny code in MBR or ESP
  - Stage 2: loads kernel image + initramfs from /boot
  - Passes kernel command line parameters

Linux kernel decompression
  - Kernel image is compressed (GZIP/LZ4/ZSTD)
  - Decompresses itself in place
  - arch/x86/boot/compressed/head_64.S → startup_32/64

Kernel initialization
  - start_kernel() in init/main.c
  - Setup: CPU, memory zones, scheduler, interrupt subsystems
  - init_mm: initialize kernel memory management
  - trap_init: set up IDT (Interrupt Descriptor Table)
  - sched_init: initialize scheduler run queues
  - time_init: set up timers (APIC, HPET)
  - init_IRQ: initialize interrupt subsystem
  - softirq_init: initialize software interrupt (bottom halves)
  - console_init: early console (for boot messages)
  - rest_init() → kernel_init thread (PID 1) + kthreadd (PID 2)

Initial RAM filesystem (initramfs)
  - Temporary filesystem loaded into memory by bootloader
  - Contains: modprobe, udev, cryptsetup, mdadm, btrfs tools
  - Kernel mounts initramfs as root
  - Loads drivers needed to mount real root filesystem
    (NVMe driver, filesystem driver, LUKS crypto, RAID...)
  - Pivots to real root filesystem

/sbin/init (systemd PID 1)
  - Reads /etc/systemd/system/*.target
  - Starts all units in dependency order
  - Mounts filesystems (/etc/fstab)
  - Starts network, display manager, user services

Login
  - getty on TTYs / graphical display manager
  - User authenticates (PAM)
  - Shell or desktop environment starts
```

```bash
# Analyze boot time
systemd-analyze                      # Total boot time
systemd-analyze blame                # Time per unit
systemd-analyze critical-chain       # Critical path (bottleneck)
systemd-analyze plot > boot.svg      # Visual boot timeline

# Kernel boot messages
dmesg --color=always | less
dmesg -T | grep -i error            # Timestamped, filter errors
journalctl -b                        # All boot messages via journal
journalctl -b -0 | head -100         # Current boot
journalctl -b -1 | head -100         # Previous boot
```

---

## See Also

- [Kernel Architecture](kernel-architecture.md) — Overview, commands, and module management
- [CPU Architecture](cpu-architecture.md) — Hardware that the kernel manages
- [Drivers & DLLs](drivers-and-dlls.md) — Writing kernel modules and drivers
- [Operating Systems](operating-systems.md) — OS theory, chroot, proot, namespaces
