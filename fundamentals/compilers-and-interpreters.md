# Compilers, Interpreters, Assemblers & Low-Level Languages

This document covers the full software translation stack — from human-written source code down to machine instructions — including Assembly language, compiler internals, interpreter design, JIT compilation, and how different languages map to execution.

---

## Table of Contents
1. [The Translation Stack](#1-the-translation-stack)
2. [Assembly Language](#2-assembly-language)
3. [Assemblers](#3-assemblers)
4. [Compilers — How They Work](#4-compilers--how-they-work)
5. [Intermediate Representations (IR)](#5-intermediate-representations-ir)
6. [Optimization Passes](#6-optimization-passes)
7. [Linkers](#7-linkers)
8. [Interpreters](#8-interpreters)
9. [JIT Compilation](#9-jit-compilation)
10. [Language Implementation Taxonomy](#10-language-implementation-taxonomy)
11. [LLVM — The Universal Compiler Backend](#11-llvm--the-universal-compiler-backend)
12. [Historical Languages](#12-historical-languages)

---

## 1. The Translation Stack

```
Source code (C, Rust, Python, Java...)
        ↓  Lexer/Tokenizer
Token stream
        ↓  Parser
Abstract Syntax Tree (AST)
        ↓  Semantic Analysis
Typed/Annotated AST
        ↓  IR Generation
Intermediate Representation (IR)
        ↓  Optimization Passes (many)
Optimized IR
        ↓  Code Generation (backend)
Assembly (target ISA)
        ↓  Assembler
Object file (.o / .obj) — machine code + relocation info
        ↓  Linker
Executable (ELF / PE / Mach-O) — final binary
        ↓  Loader (OS)
Process in memory — CPU executes
```

Each stage narrows the representation, making it more concrete and closer to hardware.

---

## 2. Assembly Language

Assembly is a human-readable one-to-one representation of machine code instructions. Each line maps to exactly one machine instruction (or a macro that expands to a few).

### Why Learn Assembly?

- Understand what compiled code actually does
- Write performance-critical inner loops (SIMD, tight compute)
- Reverse engineering — decompilers produce pseudo-C, but the ground truth is assembly
- Exploit development — shellcode, ROP chains
- Embedded systems — hardware bring-up, interrupt handlers
- Understand CPU behavior directly (pipeline, registers, flags)

### x86-64 Assembly (Intel/AT&T Syntax)

```nasm
; Intel syntax (used by NASM, MASM, Intel documentation)
; Destination is on the LEFT: op dest, src

section .data
    msg db "Hello, World!", 10, 0   ; String with newline, null terminator
    msg_len equ $ - msg              ; Length = current address - msg start

section .text
    global _start

_start:
    ; Write syscall (Linux x86-64: syscall number in RAX)
    mov rax, 1          ; sys_write
    mov rdi, 1          ; fd = stdout (1)
    mov rsi, msg        ; buffer address
    mov rdx, msg_len    ; length
    syscall             ; Enter kernel

    ; Exit syscall
    mov rax, 60         ; sys_exit
    xor rdi, rdi        ; exit code = 0 (XOR self = 0, faster than MOV RDI, 0)
    syscall
```

```nasm
; AT&T syntax (used by GAS, GCC output)
; Source is on the LEFT: op src, dest
; Size suffixes: b=byte, w=word, l=long(32), q=quadword(64)

movq $1, %rax          ; Move immediate 1 into RAX (AT&T: $ = immediate)
movq $1, %rdi          ; fd = stdout
leaq msg(%rip), %rsi   ; Load address of msg (RIP-relative, position-independent)
movq $14, %rdx
syscall
```

### x86-64 Instruction Categories

```nasm
; Data Movement
mov rax, rbx            ; Copy RBX → RAX
mov rax, [rbx]          ; Load from memory at address RBX → RAX
mov [rbx], rax          ; Store RAX → memory at RBX
movzx eax, byte [rbx]   ; Zero-extend byte load into EAX
movsx rax, dword [rbx]  ; Sign-extend 32-bit load into RAX
xchg rax, rbx           ; Atomic swap (without LOCK prefix: not really atomic)
push rax                ; RSP -= 8; [RSP] = RAX
pop rax                 ; RAX = [RSP]; RSP += 8
lea rax, [rbx + rcx*4 + 16]  ; Load Effective Address — compute address, don't dereference

; Arithmetic
add rax, rbx            ; RAX = RAX + RBX; sets flags
sub rax, rbx            ; RAX = RAX - RBX
mul rbx                 ; RDX:RAX = RAX × RBX (unsigned, 128-bit result)
imul rax, rbx           ; RAX = RAX × RBX (signed, lower 64 bits)
div rbx                 ; RAX = RDX:RAX / RBX; RDX = remainder
inc rax                 ; RAX++
dec rax                 ; RAX--
neg rax                 ; RAX = -RAX (two's complement negate)
adc rax, rbx            ; RAX = RAX + RBX + CF (add with carry)

; Bitwise
and rax, rbx            ; RAX = RAX AND RBX; clears ZF if result is nonzero
or  rax, rbx            ; RAX = RAX OR RBX
xor rax, rbx            ; RAX = RAX XOR RBX (xor rax, rax = zeroing idiom)
not rax                 ; RAX = ~RAX (bitwise NOT)
shl rax, cl             ; Logical shift left by CL bits (multiply by 2^CL)
shr rax, cl             ; Logical shift right (unsigned divide by 2^CL)
sar rax, cl             ; Arithmetic shift right (signed divide, preserves sign)
rol rax, cl             ; Rotate left
ror rax, cl             ; Rotate right
bt  rax, rbx            ; Bit Test: CF = bit RBX of RAX

; Comparison and Branching
cmp rax, rbx            ; Compute RAX - RBX, set flags, discard result
test rax, rbx           ; Compute RAX AND RBX, set flags, discard result
                        ; test rax, rax → ZF set if RAX is zero
je  label               ; Jump if ZF=1 (equal / zero)
jne label               ; Jump if ZF=0
jl  label               ; Jump if less (signed: SF ≠ OF)
jle label               ; Jump if less or equal
jg  label               ; Jump if greater (signed)
jge label               ; Jump if greater or equal
jb  label               ; Jump if below (unsigned: CF=1)
jbe label               ; Jump if below or equal
ja  label               ; Jump if above (unsigned: CF=0 and ZF=0)
jmp label               ; Unconditional jump
jz  label               ; Jump if zero (same as je)
js  label               ; Jump if sign flag set (result was negative)
jo  label               ; Jump if overflow flag set

; Procedure calls
call func               ; PUSH return address (RIP+len); JMP func
ret                     ; POP return address; JMP to it
enter n, 0              ; Equivalent to: PUSH RBP; MOV RBP, RSP; SUB RSP, n (rarely used)
leave                   ; Equivalent to: MOV RSP, RBP; POP RBP

; String operations (with REP prefix for repetition)
rep movsb               ; Copy ECX bytes from [RSI] to [RDI], advance both
rep stosb               ; Fill ECX bytes at [RDI] with AL
rep scasb               ; Scan [RDI] for byte AL, decrement RCX until match
```

### ARM64 Assembly

```
; AArch64 — Load-Store architecture
; 31 general-purpose 64-bit registers: X0–X30 (or W0–W30 for 32-bit view)
; X29 = frame pointer, X30 = link register (return address), SP = stack pointer

; Load/Store (explicit — no memory operands in ALU instructions)
LDR X0, [X1]            ; X0 = Memory[X1]       (64-bit load)
LDR W0, [X1]            ; W0 = Memory[X1]       (32-bit load, zero-extends to X0)
LDRB W0, [X1]           ; W0 = Memory[X1]       (byte load, zero-extend)
LDRSB X0, [X1]          ; X0 = sign-extend(Memory[X1]) (signed byte)
LDP X0, X1, [X2]        ; X0 = [X2], X1 = [X2+8] (load pair)
STR X0, [X1]            ; Memory[X1] = X0
STUR X0, [X1, #-16]     ; Unscaled offset (negative)
LDR X0, [X1, X2, LSL #3] ; Address = X1 + X2*8 (scaled index)

; Pre/Post indexing
LDR X0, [X1, #8]!       ; X1 += 8 first, then load (pre-indexed)
LDR X0, [X1], #8        ; Load first, then X1 += 8 (post-indexed)

; Arithmetic (register only — no memory operands)
ADD X0, X1, X2          ; X0 = X1 + X2
ADD X0, X1, #100        ; X0 = X1 + 100 (immediate)
ADDS X0, X1, X2         ; Add and set flags (S suffix)
SUB X0, X1, X2
MUL X0, X1, X2          ; X0 = X1 × X2 (lower 64 bits)
MADD X0, X1, X2, X3     ; X0 = X1×X2 + X3 (multiply-add)
LSL X0, X1, #3          ; X0 = X1 << 3 (multiply by 8)
LSR X0, X1, #3          ; X0 = X1 >> 3 (unsigned)
ASR X0, X1, #3          ; X0 = X1 >> 3 (signed, arithmetic)

; Branching
CMP X0, X1              ; Set flags from X0 - X1
B.EQ label              ; Branch if equal (ZF=1)
B.NE label              ; Branch if not equal
B.LT label              ; Branch if less than (signed)
B.GT label              ; Branch if greater than (signed)
B.CS label              ; Branch if carry set (unsigned ≥)
CBZ X0, label           ; Branch if X0 == 0 (compact compare-and-branch)
CBNZ X0, label          ; Branch if X0 != 0
TBZ X0, #3, label       ; Branch if bit 3 of X0 is zero

; Procedure calls
BL func                 ; Branch with Link: X30 = return address; jump
RET                     ; Return: jump to address in X30 (link register)
```

### Calling Conventions

```
; x86-64 System V AMD64 ABI (Linux, macOS, most non-Windows):
; Arguments:   RDI, RSI, RDX, RCX, R8, R9, then stack
; Return val:  RAX (and RDX for 128-bit)
; Caller-saved (can trash): RAX, RCX, RDX, RSI, RDI, R8-R11, XMM0-XMM15
; Callee-saved (must preserve): RBX, RBP, R12-R15

; x86-64 Windows ABI:
; Arguments:   RCX, RDX, R8, R9, then stack (first 4 have shadow space on stack too)
; Return val:  RAX
; Callee-saved: RBX, RBP, RDI, RSI, R12-R15, XMM6-XMM15

; AArch64 (ARM64) AAPCS:
; Arguments:   X0-X7 (integer), V0-V7 (float)
; Return val:  X0 (and X1 for 128-bit)
; Caller-saved: X0-X17
; Callee-saved: X19-X28, X29 (frame ptr), X30 (link register)

; C function call example (x86-64 Linux):
;   int result = add(5, 3);
mov rdi, 5          ; First argument
mov rsi, 3          ; Second argument
call add            ; Call function
; Return value now in RAX
```

---

## 3. Assemblers

An assembler translates assembly source text into machine code (object files). The mapping is nearly 1:1.

| Assembler | Syntax | OS | Notes |
|-----------|--------|-----|-------|
| **NASM** | Intel | All | Most popular x86 assembler, clean syntax |
| **GAS** (GNU Assembler) | AT&T (default) or Intel | Linux/macOS | Used by GCC, comes with binutils |
| **MASM** | Intel | Windows | Microsoft Macro Assembler — Windows ABI |
| **YASM** | Intel / AT&T | All | NASM-compatible, extended |
| **FASM** | Intel | All | Self-hosting, flat assembler |

```bash
# NASM: assemble and link a Linux x86-64 program
nasm -f elf64 hello.asm -o hello.o    # Assemble to ELF64 object
ld hello.o -o hello                   # Link (no C library)
./hello

# GAS: emit from GCC
gcc -S program.c -o program.s          # Compile to assembly only
gcc program.c -o program               # Compile + assemble + link

# View assembly from compiled code
objdump -d -M intel program            # Disassemble with Intel syntax
objdump -d -M att program              # AT&T syntax
```

---

## 4. Compilers — How They Work

A compiler translates high-level source code into a lower-level representation (usually machine code or assembly).

### Stage 1: Lexing (Tokenization)

The source text is split into tokens — the atomic units of the language.

```
Source: int x = 42 + y;
Tokens: [KW_INT] [IDENT "x"] [ASSIGN] [INT_LIT 42] [PLUS] [IDENT "y"] [SEMICOLON]

Implemented as: state machine or regex-based scanner
Tools: Flex (generates C lexer from regex rules), ANTLR, hand-written
```

### Stage 2: Parsing

Tokens are organized into a parse tree / Abstract Syntax Tree (AST) according to the grammar.

```
Source: a + b * c

AST:
       ADD
      /   \
    VAR   MUL
     a   /   \
       VAR   VAR
        b     c

Operator precedence is encoded in grammar rules:
  expr  → term (('+' | '-') term)*
  term  → factor (('*' | '/') factor)*
  factor → '(' expr ')' | NUM | IDENT

Parser types:
  Recursive Descent: hand-written, easy to understand, used by Clang/GCC
  LR parsers (yacc/bison): table-driven, handles ambiguous grammars
  PEG parsers: ordered choice, no ambiguity, used in modern compilers
```

### Stage 3: Semantic Analysis

The AST is checked for correctness: type checking, name resolution, scope analysis.

```
Type checking example:
  float x = "hello";   → Type error: cannot assign string to float
  x = undefined_var;   → Name error: undefined_var not in scope
  int a = 2147483648;  → Warning: integer overflow (exceeds INT_MAX)

Symbol table: maps identifiers to their types, locations, scopes
Type inference (Rust, Hindley-Milner): deduce types from usage without annotation
```

### Stage 4: IR Generation

The annotated AST is lowered to Intermediate Representation — a simpler, more machine-like format easier to optimize than the AST.

### Stage 5: Optimization (see §6)

### Stage 6: Code Generation

IR is translated to target assembly. Register allocation assigns variables to physical registers. Instruction selection picks the best machine instruction for each IR operation.

```
IR:  %tmp = mul i32 %x, 8
x86 output: lea rax, [rdi*8]    ; LEA is faster than IMUL for powers of 2
ARM output: lsl x0, x0, #3      ; Shift left by 3 = multiply by 8
```

---

## 5. Intermediate Representations (IR)

IR sits between source language and machine code. It's designed to be easy to analyze and transform.

### Three-Address Code (TAC)

```
Source:  y = a + b * c - d
TAC:
  t1 = b * c
  t2 = a + t1
  t3 = t2 - d
  y  = t3

Properties: at most one operation per statement, unlimited "virtual registers"
```

### Static Single Assignment (SSA)

Every variable is assigned exactly once. When control flow merges, a φ (phi) function selects the value from the correct predecessor.

```
if (cond) {
    x = 1;    → x1 = 1
} else {
    x = 2;    → x2 = 2
}
use(x);       → x3 = φ(x1, x2)   ← phi function: pick x1 or x2 based on which branch was taken
use(x3);

Benefits of SSA:
  Trivial to find all uses of a definition (just one assignment point)
  Enables constant propagation, dead code elimination, and many other passes
  Used by: LLVM IR, GCC GIMPLE, Java HotSpot JIT
```

### LLVM IR

```llvm
; LLVM IR — typed, SSA form, explicit memory model

define i32 @add_ten(i32 %x) {
entry:
  %result = add i32 %x, 10     ; %result = %x + 10
  ret i32 %result               ; return result
}

define i32 @factorial(i32 %n) {
entry:
  %cond = icmp sle i32 %n, 1   ; n <= 1?
  br i1 %cond, label %base, label %recurse

base:
  ret i32 1

recurse:
  %n_minus_1 = sub i32 %n, 1
  %sub_result = call i32 @factorial(i32 %n_minus_1)
  %result = mul i32 %n, %sub_result
  ret i32 %result
}
```

---

## 6. Optimization Passes

Compilers apply dozens of optimization passes to improve generated code.

### Common Optimizations

**Constant Folding:**
```
int x = 2 * 3 + 4;
→ Computed at compile time: int x = 10;
   No multiplication at runtime.
```

**Dead Code Elimination:**
```
int x = 5;
if (false) {   // Never taken — entire block removed
    int y = expensive_computation();
}
```

**Inlining:**
```c
// Before: function call overhead
int square(int x) { return x * x; }
int result = square(y);

// After inlining: direct substitution
int result = y * y;   // No call, no return, no stack frame
```

**Loop Optimizations:**
```c
// Loop invariant code motion — hoist computation out of loop
for (int i = 0; i < n; i++) {
    x[i] = y[i] * sqrt(constant);   // sqrt(constant) is same every iteration
}
// → becomes:
float c = sqrt(constant);            // Computed once
for (int i = 0; i < n; i++) {
    x[i] = y[i] * c;
}

// Loop unrolling — reduce branch overhead
for (int i = 0; i < 4; i++) x[i] = y[i];
// → unrolled:
x[0] = y[0]; x[1] = y[1]; x[2] = y[2]; x[3] = y[3];

// Vectorization (auto-vectorization)
for (int i = 0; i < n; i++) c[i] = a[i] + b[i];
// → SIMD: process 8 floats at once with VADDPS
```

**Alias Analysis:**
```c
void f(int *a, int *b) {
    *a = 1;
    *b = 2;
    return *a;   // Does writing *b affect *a? Depends on aliasing.
}
// With __restrict__: compiler knows a ≠ b → *a is still 1 → return 1 directly
```

**Tail Call Optimization:**
```c
// Recursive tail call — last operation is the recursive call
int factorial_tail(int n, int acc) {
    if (n <= 1) return acc;
    return factorial_tail(n - 1, n * acc);  // Tail call
}
// Compiler converts to a loop — no stack growth:
// while (n > 1) { acc = n * acc; n--; } return acc;
```

### Optimization Levels (GCC/Clang)

| Flag | Level | Effect |
|------|-------|--------|
| `-O0` | None | No optimization. Best for debugging (vars in predictable places) |
| `-O1` | Basic | Simple inlining, dead code, constant folding |
| `-O2` | Standard | Loop optimization, auto-vectorization, alias analysis |
| `-O3` | Aggressive | More inlining, more vectorization, function cloning |
| `-Os` | Size | Optimize for code size (avoid inlining/unrolling) |
| `-Oz` | Min size | Maximum size reduction (Clang) |
| `-Og` | Debug | Some optimization, debuggable (GCC) |

---

## 7. Linkers

After compiling, each source file is an object file (.o) with machine code and symbol references. The linker combines them into an executable.

```
Linker tasks:
  1. Symbol resolution: find the definition of every referenced symbol
     main.o references: printf (in libc), helper (in helper.o)
     → linker finds printf in libc.so, helper in helper.o

  2. Relocation: fix up addresses
     Code in main.o assumes helper is at address 0 (placeholder)
     → linker knows final address → patches all references

  3. Layout: assign final virtual memory addresses to code and data sections
     .text section (code): 0x401000
     .rodata (read-only data): 0x402000
     .data (initialized globals): 0x403000
     .bss (uninitialized globals): 0x404000

Output: ELF executable (Linux), PE executable (Windows), Mach-O (macOS)
```

### Static vs Dynamic Linking

```
Static linking:
  All library code copied into the executable
  ./program: self-contained, large binary
  No runtime dependency on library files
  Used for: system tools, single-file distribution, embedded

Dynamic linking:
  Executable contains references to shared libraries (.so / .dll / .dylib)
  Library code loaded at program startup by the dynamic linker (ld.so on Linux)
  Multiple programs share one copy of the library in memory
  Used for: most programs (libc, system libraries)

$ ldd /bin/ls         # Show shared library dependencies
  linux-vdso.so.1
  libselinux.so.1 → /lib/x86_64-linux-gnu/libselinux.so.1
  libc.so.6 → /lib/x86_64-linux-gnu/libc.so.6
  libpcre2-8.so.0 → /lib/x86_64-linux-gnu/libpcre2-8.so.0
```

---

## 8. Interpreters

An interpreter executes source code (or a parsed representation) without converting it to machine code first. It reads instructions and acts on them immediately.

```
Types:
  1. Tree-walking interpreter: execute the AST directly
     Simple, slow. Used by: early Python, Ruby, Bash (partially)

  2. Bytecode interpreter: compile to bytecode, then interpret bytecode
     Bytecode: compact, platform-independent instruction set
     Used by: CPython, JVM (before JIT), Lua 5.x

  3. JIT interpreter: compile hot paths to native code (see §9)
     Used by: modern Python (PyPy), V8, HotSpot JVM
```

### CPython Bytecode

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
# Output:
# LOAD_FAST   0 (a)      # Push 'a' onto value stack
# LOAD_FAST   1 (b)      # Push 'b' onto value stack
# BINARY_ADD             # Pop both, push sum
# RETURN_VALUE           # Return top of stack
```

CPython's interpreter is a giant `switch` statement — for each bytecode opcode, execute the corresponding C code.

---

## 9. JIT Compilation

Just-In-Time compilation compiles code to native machine instructions at runtime, after observing actual execution patterns.

```
Tiered JIT (V8 / SpiderMonkey JavaScript example):

  First execution:
    Interpreted (fast startup, no compilation cost)

  Hot function (called many times):
    Baseline JIT: quick compile to native, unoptimized
    ~5–10× faster than interpretation

  Very hot function:
    Optimizing JIT: full optimization using observed types
    Inline caches: if obj.x always returns an integer, emit fast integer code
    ~50–100× faster than interpretation

  Deoptimization:
    If observed assumption violated (obj.x suddenly returns string):
    Throw away optimized code, fall back to interpreter
    Recompile later with updated type information
```

### Inline Caches

```javascript
function getX(obj) {
    return obj.x;   // Property lookup — obj could be anything
}

// After calling with {x: 42} 1000 times:
// JIT generates: if (obj.shape == Shape_int_x) return *(obj + 8);
//                else deoptimize;
// Shape: pointer to object layout descriptor — if shape matches, skip generic lookup
```

### LLVM JIT

```cpp
// Using LLVM JIT to compile and execute code at runtime
#include <llvm/IR/IRBuilder.h>
#include <llvm/ExecutionEngine/MCJIT.h>

// Build IR
auto M = std::make_unique<llvm::Module>("jit_module", ctx);
auto F = llvm::Function::Create(funcType, llvm::Function::ExternalLinkage, "add", M.get());
auto BB = llvm::BasicBlock::Create(ctx, "entry", F);
llvm::IRBuilder<> B(BB);
auto sum = B.CreateAdd(F->arg_begin(), std::next(F->arg_begin()), "sum");
B.CreateRet(sum);

// Compile to native code
auto EE = llvm::EngineBuilder(std::move(M)).create();
auto FPtr = (int(*)(int, int)) EE->getFunctionAddress("add");
int result = FPtr(3, 4);   // Calls native machine code
```

---

## 10. Language Implementation Taxonomy

| Language | Primary Execution Model | Notes |
|----------|------------------------|-------|
| **C / C++** | AOT compiled (static binary) | GCC, Clang → native machine code |
| **Rust** | AOT compiled | LLVM backend |
| **Go** | AOT compiled | Own backend + optional LLVM |
| **Java** | Bytecode → JIT (HotSpot JVM) | .class bytecode, tiered JIT |
| **Kotlin** | Bytecode → JVM JIT or AOT (native) | Kotlin/Native uses LLVM |
| **Python** | Bytecode interpreted (CPython) | PyPy adds JIT |
| **JavaScript** | JIT (V8, SpiderMonkey) | Tiered JIT, highly optimized |
| **Ruby** | Bytecode + JIT (YJIT since 3.1) | MJIT/YJIT use basic block versioning |
| **Lua** | Bytecode (PUC Lua) or JIT (LuaJIT) | LuaJIT among fastest scripting |
| **PHP** | Bytecode (OPcache) | JIT since 8.0 |
| **C#** | MSIL bytecode → JIT (.NET CLR) | RyuJIT; AOT with NativeAOT |
| **Swift** | AOT compiled | LLVM backend, ARC memory |
| **Assembly** | Assembled directly to machine code | NASM, GAS |
| **Bash/sh** | Tree-walking interpreted | Each command: parse → execute |

---

## 11. LLVM — The Universal Compiler Backend

LLVM is a collection of modular compiler infrastructure. It provides a common IR (LLVM IR) and optimizing backends for every major CPU architecture. Writing a frontend that emits LLVM IR gives you high-quality code generation for x86, ARM, RISC-V, WebAssembly, and more — for free.

```
Language Frontend    → LLVM IR    → LLVM Optimizer → Backend → Machine Code
  Clang (C/C++)                                      x86-64
  Rust (rustc)                                       ARM64
  Swift                                              RISC-V
  Kotlin/Native                                      WebAssembly
  Julia                                              MIPS
  Your language here                                 SPIR-V (GPU shaders)
```

```bash
# Compile C to LLVM IR
clang -S -emit-llvm hello.c -o hello.ll

# Optimize IR
opt -O2 hello.ll -o hello_opt.ll

# Compile IR to native binary
llc hello_opt.ll -o hello.s    # IR → assembly
clang hello.s -o hello         # assemble + link

# Cross-compile for ARM
llc hello_opt.ll -march=aarch64 -o hello_arm.s
```

---

## 12. Historical Languages

### Assembly (1949+)

The first assembly language was developed for EDSAC at Cambridge in 1949. Before assembly, programs were written directly in binary — machine code by hand. Assembly made programming human-accessible at the machine level.

**Why assembly still matters:**
- Boot code, firmware (UEFI bootloaders still use some asm)
- Context switch code in OS kernels (saves/restores registers)
- SIMD inner loops (hand-optimized beyond auto-vectorization)
- Shellcode and exploits (security research)
- Reverse engineering artifacts

### FORTRAN (1957)

First widely-used high-level language. Designed at IBM for scientific computation. Introduced: variables, expressions, conditionals, loops (DO loops), subroutines.

```fortran
! FORTRAN 77 style
      PROGRAM HELLO
      REAL A, B, C
      A = 3.14159
      B = 2.71828
      C = A + B
      PRINT *, 'Sum:', C
      END
```

Still used in HPC (High Performance Computing), weather modeling, physics simulations — decades of optimized numerical routines (BLAS, LAPACK) are written in FORTRAN.

### COBOL (1959)

Designed for business data processing. English-like syntax. Vast amounts of banking, insurance, and government systems still run COBOL. Estimated 800 billion lines of COBOL code still in production.

```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. HELLO-WORLD.
PROCEDURE DIVISION.
    DISPLAY 'Hello, World!'.
    STOP RUN.
```

### LISP (1958)

John McCarthy's language built around symbolic computation and s-expressions (nested lists). Homoiconic — code and data have the same form. Introduced garbage collection, recursion as primary construct, closures, and macros (code that writes code).

```lisp
; Everything is a list: (operator arg1 arg2 ...)
(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(mapcar #'(lambda (x) (* x x)) '(1 2 3 4 5))
; → (1 4 9 16 25)
```

Influenced: Scheme, Clojure, Common Lisp, Racket. Ideas from LISP permeate modern languages (lambdas, GC, macros, REPL).

### ALGOL (1960)

Algorithmic Language — introduced block structure, lexical scoping, and the formal grammar specification (BNF notation). Hugely influential even though it was never widely deployed commercially.

Direct descendants: Pascal, C, Java, basically all of modern programming.

### PL/I (1964)

IBM's attempt at a universal language combining FORTRAN's numerics and COBOL's data handling. Introduced exceptions, concurrency, and complex data structures. Notable for being the first language formally defined using VDM.

### Pascal (1970)

Niklaus Wirth's teaching language — clean, structured, strongly typed. Turbo Pascal (Borland, 1983) brought compilation in seconds on PCs. Delphi (Object Pascal) still used for Windows desktop development.

### Smalltalk (1972)

Everything is an object — integers, classes, methods, the environment itself. Invented the GUI concept (later borrowed by Apple/Microsoft), the MVC pattern, and live programming (modify running code). Influenced: Ruby, Objective-C, Self → JavaScript's prototypes.

### C (1972)

Dennis Ritchie at Bell Labs. Designed for writing UNIX. The C language is close to the machine while remaining portable — "portable assembly." Became the lingua franca of systems programming. Direct ancestor of C++, Objective-C, Java (syntax), C#, D, and many more.

```c
/* C89 — the foundation */
#include <stdio.h>

int main(void) {
    int arr[10];
    int i;
    for (i = 0; i < 10; i++) {
        arr[i] = i * i;
        printf("%d\n", arr[i]);
    }
    return 0;
}
```

### Forth (1970)

Stack-based, concatenative language. Extremely minimal — an entire Forth interpreter fits in 1KB. Used in embedded systems, OpenBoot (Sun/Oracle firmware), and as a language for language experimentation. No heap allocation, no garbage collection.

```forth
: SQUARE DUP * ;          \ Define: SQUARE = duplicate top, multiply
5 SQUARE .                \ Push 5, square it, print → 25
: FACTORIAL               \ Define factorial
  DUP 1 <= IF DROP 1 EXIT THEN
  DUP 1 - RECURSE * ;
10 FACTORIAL .            \ → 3628800
```

---

## See Also

- [CPU Architecture](cpu-architecture.md) — How the CPU executes the machine code that compilers produce
- [GPU Architecture](gpu-architecture.md) — GPU shading languages and compute, GLSL/SPIR-V compilation
- [Drivers & DLLs](drivers-and-dlls.md) — How compiled code is loaded and linked at runtime
- [Linux Internals](linux-internals.md) — How the OS loads and executes compiled programs
