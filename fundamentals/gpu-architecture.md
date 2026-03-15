# GPU Architecture — Hardware, CUDA, TPU & Graphics Pipeline

This document covers GPU architecture from silicon to shader — how GPUs differ from CPUs, how the graphics pipeline works, how CUDA/compute APIs map to hardware, and how modern rendering techniques like rasterization and ray tracing are implemented.

---

## Table of Contents
1. [GPU vs CPU Architecture](#1-gpu-vs-cpu-architecture)
2. [GPU Hardware Internals](#2-gpu-hardware-internals)
3. [Rasterization Pipeline](#3-rasterization-pipeline)
4. [Ray Tracing](#4-ray-tracing)
5. [CUDA — NVIDIA Compute Architecture](#5-cuda--nvidia-compute-architecture)
6. [AMD ROCm / HIP](#6-amd-rocm--hip)
7. [TPU — Tensor Processing Unit](#7-tpu--tensor-processing-unit)
8. [Graphics APIs Overview](#8-graphics-apis-overview)
9. [Vulkan Deep Dive](#9-vulkan-deep-dive)
10. [OpenGL](#10-opengl)
11. [GPU Memory Architecture](#11-gpu-memory-architecture)
12. [GPU Drivers](#12-gpu-drivers)

---

## 1. GPU vs CPU Architecture

CPUs and GPUs are designed for fundamentally different workloads:

```
CPU design philosophy:
  Minimize latency for a single thread
  Large caches, complex branch predictors, OoO execution
  4–16 powerful cores
  Optimized for sequential, branchy code

GPU design philosophy:
  Maximize throughput across thousands of threads
  Simple cores, minimal branch prediction, in-order execution
  Thousands of small cores
  Optimized for data-parallel code with predictable access patterns

CPU (Intel i9, 24 cores):          GPU (NVIDIA RTX 4090, 16,384 CUDA cores):
  ┌────┬────┬────┬────┐              ┌──┬──┬──┬──┬──┬──┬──┬──┐ × 128 SMs
  │ C0 │ C1 │ C2 │ C3 │              │  │  │  │  │  │  │  │  │
  │Big │Big │Big │Big │              │Small cores, in groups  │
  │    │    │    │    │              │  │  │  │  │  │  │  │  │
  └────┴────┴────┴────┘              └──┴──┴──┴──┴──┴──┴──┴──┘

FLOPS (fp32): ~1 TFLOP              FLOPS (fp32): ~82 TFLOP
Memory BW:    ~100 GB/s             Memory BW:    ~1000 GB/s (HBM3)
Latency hide: Via cache, OoO        Latency hide: Via thread switching
```

**The fundamental insight:** GPUs hide memory latency by having thousands of threads. When one warp (group of threads) is stalled waiting for memory, the GPU instantly switches to another warp that is ready — zero-cost context switch because each warp has its own dedicated register set.

---

## 2. GPU Hardware Internals

### NVIDIA Ampere/Ada Lovelace Hierarchy

```
GPU Die
  └── GPC (Graphics Processing Cluster) × 7–12
        └── TPC (Texture Processing Cluster) × 2–3
              └── SM (Streaming Multiprocessor) × 2
                    ├── CUDA cores (FP32): 128 per SM
                    ├── Tensor cores: 4 per SM (matrix multiply)
                    ├── RT cores: 1 per SM (ray tracing BVH traversal)
                    ├── L1 Cache / Shared Memory: 128 KB (configurable)
                    ├── Register file: 256 KB (64K × 32-bit registers)
                    ├── Warp schedulers: 4 (each schedules 1 warp/cycle)
                    └── Dispatch units: 2 per scheduler
```

**RTX 4090 (Ada Lovelace):**
- 16,384 CUDA cores (128 SMs × 128 cores/SM)
- 512 Tensor cores (4th gen)
- 128 RT cores
- 16,384 active threads per SM
- 82.6 TFLOPS FP32
- 330.3 TFLOPS with sparsity (Tensor Core)
- 24 GB GDDR6X, 1008 GB/s

### Streaming Multiprocessor (SM) — The Core Unit

The SM is the fundamental GPU execution unit. Everything below the SM level is pipelined execution hardware.

```
SM (Streaming Multiprocessor):

  Warp Scheduler 0   Warp Scheduler 1   Warp Scheduler 2   Warp Scheduler 3
        ↓                    ↓                   ↓                  ↓
  [32 threads]         [32 threads]       [32 threads]       [32 threads]
  Warp 0               Warp 1             Warp 2              Warp 3

  Execution units:
    INT32 CUDA cores: 128    FP32 CUDA cores: 128
    FP64 cores: 2 (consumer) or 64 (data center)
    Tensor cores: 4 (matrix multiply accelerators)
    Special Function Units (SFU): 4 (sin, cos, sqrt, reciprocal)
    Load/Store Units: 32

  Memory:
    L1 cache + shared memory: 128 KB combined
    Register file: 256 KB (fastest on-chip storage)
    Constant cache: 8 KB
    Texture cache: 8–16 KB
```

### Warps — The Execution Unit

A **warp** is 32 threads that execute in lockstep — all 32 execute the same instruction simultaneously on different data. This is SIMT (Single Instruction Multiple Thread), the GPU's equivalent of SIMD.

```
Warp execution:
  32 threads, all running the same instruction
  Each thread has different register values (different data)
  All 32 results computed in one clock cycle (one instruction)

Example: Vector addition kernel
  Thread 0: c[0] = a[0] + b[0]  ─┐
  Thread 1: c[1] = a[1] + b[1]   │
  Thread 2: c[2] = a[2] + b[2]   │ All execute simultaneously
  ...                              │
  Thread 31: c[31] = a[31] + b[31]─┘

Occupancy: how many warps are active per SM
  More warps = better latency hiding
  Constrained by register usage and shared memory per thread
```

### Warp Divergence

When threads in a warp take different branches, the warp must execute BOTH paths — inactive threads are masked off:

```cuda
// Divergent branch — bad for GPU performance
if (threadIdx.x % 2 == 0) {
    // Executed by threads 0, 2, 4, ... (16 threads active)
    // Threads 1, 3, 5 ... are MASKED OFF
    result = expensive_path_A();
} else {
    // Executed by threads 1, 3, 5 ... (16 threads active)
    // Threads 0, 2, 4 ... are now MASKED OFF
    result = expensive_path_B();
}
// Total execution time = A_time + B_time (serialized!)
// Without divergence it would be max(A_time, B_time)
```

---

## 3. Rasterization Pipeline

Rasterization converts 3D geometry to 2D pixels. It is the primary rendering technique used in real-time graphics (games, UI, visualization).

```
CPU side:                           GPU pipeline:
  Application logic            →    Vertex Shader (programmable)
  Draw calls                   →    Tessellation (optional, programmable)
  Vertex buffers               →    Geometry Shader (optional, programmable)
  Index buffers                →    Primitive Assembly
  Uniform/constant data        →    Rasterization (fixed-function)
                                    Fragment/Pixel Shader (programmable)
                                    Depth Test (fixed-function)
                                    Blending (configurable)
                                    Framebuffer output
```

### Stage by Stage

**Vertex Shader:**
Runs once per vertex. Transforms 3D world-space positions to 2D clip-space positions. Can also calculate normals, texture coordinates, per-vertex lighting.

```glsl
// GLSL Vertex Shader
#version 450
layout(location = 0) in vec3 position;   // Vertex attribute from VBO
layout(location = 1) in vec3 normal;

layout(set = 0, binding = 0) uniform Matrices {
    mat4 model;
    mat4 view;
    mat4 projection;
} ubo;

layout(location = 0) out vec3 fragNormal;

void main() {
    gl_Position = ubo.projection * ubo.view * ubo.model * vec4(position, 1.0);
    fragNormal = mat3(ubo.model) * normal;
}
```

**Rasterization (fixed-function):**
Converts triangles to fragments (candidate pixels). For each pixel the triangle covers, a fragment is generated with interpolated attributes (position, normal, UV, color) from the three vertex values. Perspective-correct interpolation is applied.

```
Triangle vertices:  A(0,0), B(100,0), C(50,100)
Rasterizer asks: for each pixel (x,y) in the screen, is it inside this triangle?
  → Yes: generate fragment at (x,y), interpolate attributes from A,B,C
  → No: skip

Coverage: which pixels are covered (subpixel MSAA for anti-aliasing)
Interpolation: barycentric coordinates (α,β,γ) such that α+β+γ=1
  Normal at (x,y) = α*normalA + β*normalB + γ*normalC
```

**Fragment (Pixel) Shader:**
Runs once per fragment. Determines the color of each pixel. Samples textures, performs lighting calculations, applies effects.

```glsl
// GLSL Fragment Shader — Blinn-Phong lighting
#version 450
layout(location = 0) in vec3 fragNormal;
layout(location = 1) in vec2 fragTexCoord;
layout(location = 2) in vec3 fragPos;

layout(set = 1, binding = 0) uniform sampler2D albedoMap;
layout(set = 1, binding = 1) uniform sampler2D normalMap;

layout(location = 0) out vec4 outColor;

void main() {
    vec3 albedo = texture(albedoMap, fragTexCoord).rgb;
    vec3 N = normalize(fragNormal);
    vec3 L = normalize(vec3(1, 2, 1));      // Light direction
    float NdotL = max(dot(N, L), 0.0);
    outColor = vec4(albedo * NdotL + albedo * 0.1, 1.0);
}
```

**Depth Test:**
Each fragment has a depth value (z in clip space). The depth buffer (Z-buffer) stores the depth of the closest fragment rendered so far. If the new fragment is farther away than what's already in the depth buffer, it's discarded (occluded). This handles correct visibility ordering without sorting geometry.

**Z-fighting:** When two surfaces have nearly identical depth values, the depth buffer alternates between them per pixel — flickering. Fixed by adding a small bias or increasing depth buffer precision (24-bit → 32-bit float).

---

## 4. Ray Tracing

Ray tracing simulates how light physically behaves — casting rays from the camera, computing intersections with geometry, and recursively tracing reflections and shadows.

```
Rasterization (per-triangle):         Ray Tracing (per-pixel):
  For each triangle:                     For each pixel:
    Project to screen                      Cast ray from camera
    Find covered pixels                    Find closest intersection
    Shade covered pixels                   → Shadow ray to lights
                                           → Reflection ray
  Fast (parallelizes well)                 → Refraction ray (glass)
  Approximate shadows (shadow maps)        Recursive shading
  Approximate reflections (cubemaps/SSR)
                                         Slow (many rays/pixel for quality)
                                         Physically correct shadows
                                         Physically correct reflections
```

### BVH — Bounding Volume Hierarchy

Naively testing a ray against every triangle in a scene is O(N) per ray. A BVH reduces this to O(log N) using a tree of bounding boxes:

```
BVH Tree:
  Root: AABB bounding entire scene
    Left child: AABB bounding left half of scene
      Left-left: AABB bounding subset
        Leaf: Triangle 0, Triangle 1
      Left-right: AABB bounding subset
        Leaf: Triangle 2, Triangle 3
    Right child: AABB bounding right half
      ...

Ray traversal:
  1. Test ray vs root AABB: hit? descend.
  2. Test ray vs left child AABB and right child AABB.
  3. Descend children in front-to-back order.
  4. Skip children if ray misses their AABB.
  5. At leaf: test ray vs actual triangles.
  
Most rays only test ~log2(N) AABBs + a few triangles.
```

### RT Cores (Hardware Ray Tracing)

NVIDIA RT cores (Turing and later) perform BVH traversal and ray-AABB/triangle intersection in dedicated fixed-function hardware, separate from CUDA cores. This is 10–100× faster than doing the same in a CUDA shader.

```
Ray tracing pipeline (DirectX Raytracing / Vulkan Ray Tracing):

  Ray Generation Shader → fires initial rays from camera
         ↓
  RT Core hardware performs BVH traversal
         ↓
  Miss Shader → if ray hits nothing (sample skybox)
         ↓
  Any Hit Shader → optional early out (transparency check)
         ↓
  Closest Hit Shader → shade the intersection point
         ↓
  Recursion: fire shadow rays, reflection rays, etc.
```

### Hybrid Rendering

Modern games use **hybrid rendering** — rasterization for primary visibility (fast), ray tracing for high-quality effects:

| Effect | Rasterization | Ray Tracing |
|--------|-------------|------------|
| Primary visibility | ✅ (always) | Too slow |
| Shadows | Shadow maps (approximate) | ✅ Accurate soft shadows |
| Reflections | SSR, cubemaps (approximate) | ✅ Accurate reflections |
| Ambient Occlusion | SSAO (screen-space approximate) | ✅ Path-traced AO |
| Global Illumination | Many approximations | ✅ Path traced GI (expensive) |

---

## 5. CUDA — NVIDIA Compute Architecture

CUDA (Compute Unified Device Architecture) is NVIDIA's parallel computing platform. It exposes GPU hardware through C/C++ extensions for general-purpose computation.

### Thread Hierarchy

```
Grid (entire kernel launch)
  └── Block (group of threads, up to 1024)
        └── Thread (individual execution unit)

Grid → maps to entire GPU
Block → maps to one SM (all threads in a block share L1/shared memory)
Thread → maps to one CUDA core for computation
Warp → 32 consecutive threads that execute together (hardware grouping)
```

### CUDA Programming Model

```cuda
#include <cuda_runtime.h>

// Kernel function — runs on GPU, called from CPU
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    // Each thread computes one element
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    int n = 1 << 20;  // 1M elements
    float *d_a, *d_b, *d_c;  // d_ prefix = device (GPU) memory

    // Allocate GPU memory
    cudaMalloc(&d_a, n * sizeof(float));
    cudaMalloc(&d_b, n * sizeof(float));
    cudaMalloc(&d_c, n * sizeof(float));

    // Copy data from CPU to GPU
    cudaMemcpy(d_a, h_a, n * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, n * sizeof(float), cudaMemcpyHostToDevice);

    // Launch kernel: 1024 blocks × 256 threads = 1M threads
    int threads = 256;
    int blocks = (n + threads - 1) / threads;
    vectorAdd<<<blocks, threads>>>(d_a, d_b, d_c, n);

    // Copy result back to CPU
    cudaMemcpy(h_c, d_c, n * sizeof(float), cudaMemcpyDeviceToHost);

    cudaFree(d_a); cudaFree(d_b); cudaFree(d_c);
}
```

### Memory Types in CUDA

```cuda
// 1. Global memory — main GPU DRAM, accessible by all threads
//    Slow (~400 cycles), large (GBs), cached in L2
__global__ void kernel(float *global_ptr) { ... }

// 2. Shared memory — fast on-chip memory, shared within a block
//    Fast (~4 cycles), small (48–96 KB per SM), explicitly managed
__global__ void kernel() {
    __shared__ float tile[256];  // Declared in kernel
    tile[threadIdx.x] = ...;     // Written by all threads in block
    __syncthreads();             // Synchronize before reading
    float val = tile[255 - threadIdx.x];  // Read by all threads
}

// 3. Registers — fastest, private per thread, compiler-managed
//    Local variables become registers automatically
__global__ void kernel() {
    float local_var = 3.14f;  // In register, zero overhead
}

// 4. Constant memory — 64 KB read-only, cached, broadcast to all threads
__constant__ float weights[256];  // Declared globally

// 5. Texture memory — 2D-optimized cached read-only memory
// Accessed via tex2D() — good spatial locality, hardware interpolation
```

### Streams and Async Execution

```cuda
// CUDA streams allow overlapping compute and data transfers
cudaStream_t stream1, stream2;
cudaStreamCreate(&stream1);
cudaStreamCreate(&stream2);

// Launch in different streams — can run concurrently
cudaMemcpyAsync(d_a, h_a, size, cudaMemcpyHostToDevice, stream1);
kernel1<<<grid, block, 0, stream1>>>(d_a, d_out1);

cudaMemcpyAsync(d_b, h_b, size, cudaMemcpyHostToDevice, stream2);
kernel2<<<grid, block, 0, stream2>>>(d_b, d_out2);

cudaStreamSynchronize(stream1);
cudaStreamSynchronize(stream2);
```

### Tensor Cores

Tensor cores perform 4×4 matrix multiply-accumulate in a single clock cycle:
```
D = A × B + C
where A, B, C, D are 4×4 matrices
Input precision: FP16, BF16, INT8, FP8
Output precision: FP32 (accumulate)

NVIDIA A100: 312 TFLOPS FP16 with Tensor Cores (vs 19.5 TFLOPS FP32 on CUDA cores)
Used by: PyTorch, TensorFlow, cuDNN for neural network training/inference
```

---

## 6. AMD ROCm / HIP

AMD's compute platform for their RDNA and CDNA GPU architectures.

- **ROCm:** AMD's open-source GPU compute stack (drivers, runtime, libraries)
- **HIP:** Hardware Interface for Portability — CUDA-compatible API that compiles for both NVIDIA and AMD GPUs

```cpp
// HIP code — runs on both NVIDIA (via CUDA) and AMD (via ROCm)
#include <hip/hip_runtime.h>

__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) c[idx] = a[idx] + b[idx];
}

// hipify-perl: tool to convert CUDA code to HIP automatically
// hipcc: compiler (uses nvcc or AMD's rocm compiler based on target)
```

---

## 7. TPU — Tensor Processing Unit

Google's custom ASIC for neural network inference and training. Designed specifically around matrix multiply — the dominant operation in neural networks.

### Architecture

```
TPU v4 chip:
  Core: MXU (Matrix Multiply Unit) — 128×128 systolic array
  Peak: 275 TFLOPS BF16 per chip
  Memory: 32 GB HBM2e
  Interconnect: 2D torus ICI (Inter-Chip Interconnect) for pods

Systolic array operation (matrix multiply):
  Data flows through a grid of multiply-accumulate units in a wave
  Each cell multiplies its input and passes results to neighbors
  No data fetch per operation — data "flows" through hardware
  Extremely efficient for GEMM (general matrix-matrix multiply)
```

### TPU vs GPU for ML

| Aspect | GPU | TPU |
|--------|-----|-----|
| **Flexibility** | High (any compute) | Limited (ML-focused) |
| **Memory BW** | Very high (HBM3) | Very high (HBM2) |
| **Precision** | FP32/FP16/BF16/INT8/FP8 | BF16 primary |
| **Power efficiency** | Good | Excellent for matrix ops |
| **Ecosystem** | CUDA (broad) | JAX, TF (restricted) |
| **Availability** | Consumer + cloud | Google Cloud only |

---

## 8. Graphics APIs Overview

Graphics APIs are software interfaces between application code and GPU hardware. They submit rendering commands to the GPU driver, which translates them to hardware operations.

```
Application code (C++, Rust, game engine)
        ↓
Graphics API (Vulkan / OpenGL / DirectX / Metal)
        ↓
GPU Driver (NVIDIA/AMD/Intel proprietary, or open-source Mesa)
        ↓
Kernel-mode driver (ring 0 — manages GPU memory, command ring)
        ↓
GPU hardware
```

| API | Vendor | OS | Abstraction Level | Age |
|-----|--------|----|------------------|-----|
| **Vulkan** | Khronos (cross-vendor) | All | Low (explicit) | 2016 |
| **OpenGL** | Khronos | All | High (implicit) | 1992 |
| **DirectX 12** | Microsoft | Windows/Xbox | Low (explicit) | 2015 |
| **DirectX 11** | Microsoft | Windows | Medium | 2009 |
| **Metal** | Apple | macOS/iOS | Low-Medium | 2014 |
| **WebGPU** | W3C | Browser | Medium | 2023 |
| **OpenGL ES** | Khronos | Mobile/Embedded | High (implicit) | 2003 |

---

## 9. Vulkan Deep Dive

Vulkan is a low-overhead graphics and compute API. It gives applications explicit control over GPU command recording, synchronization, memory allocation, and render passes — at the cost of significant verbosity.

### Why Vulkan Exists

OpenGL hides enormous complexity: the driver manages state tracking, implicit synchronization, memory allocation, shader compilation, and pipeline caching. This hidden work caused unpredictable performance (driver-level hitches). Vulkan moves all this explicit into the application.

```
OpenGL: "Draw this triangle."
  Driver: validate state, check for errors, compile shader if needed,
          allocate memory, synchronize with previous frame, submit...
          (unpredictable work, random stutters)

Vulkan: "Here is a pre-compiled pipeline, pre-allocated buffer,
         pre-recorded command buffer, properly synchronized.
         Submit this to the queue."
  Driver: Submit exactly what was asked. Minimal hidden work.
          (predictable performance, you own the complexity)
```

### Vulkan Core Concepts

**Instance:** Represents the Vulkan library state. Created once per application.

**Physical Device:** Represents actual GPU hardware. Query capabilities, memory types, queue families.

**Logical Device:** Interface to the physical device for your application. Create queues from it.

**Queue:** GPU work submission channel. Types: graphics, compute, transfer. Work is submitted as VkCommandBuffers to queues.

**Command Buffer:** Pre-recorded list of GPU commands. Record once, submit many times (or re-record each frame).

**Render Pass:** Describes the structure of a rendering operation — which attachments (color, depth) are used, load/store operations, subpass dependencies.

**Pipeline:** Pre-compiled, pre-linked GPU program state — shaders + fixed-function state (blending, rasterization, depth test). Compilation at pipeline creation time (explicit and potentially cached), not at draw time.

**Descriptor Set:** Binds resources (textures, buffers) to shader binding points.

**Synchronization:** Explicit via semaphores (queue-to-queue), fences (CPU-GPU), pipeline barriers (within command buffer, memory and execution dependencies).

### Minimal Vulkan Application Flow

```cpp
// Extremely abbreviated — real Vulkan initialization is ~1000+ lines

// 1. Create instance
VkInstanceCreateInfo instanceInfo = {};
vkCreateInstance(&instanceInfo, nullptr, &instance);

// 2. Select physical device (GPU)
vkEnumeratePhysicalDevices(instance, &deviceCount, physicalDevices);
physicalDevice = pickBestGPU(physicalDevices, deviceCount);

// 3. Create logical device and queues
vkCreateDevice(physicalDevice, &deviceCreateInfo, nullptr, &device);
vkGetDeviceQueue(device, graphicsQueueFamily, 0, &graphicsQueue);

// 4. Create swap chain (window surface images)
vkCreateSwapchainKHR(device, &swapchainInfo, nullptr, &swapchain);

// 5. Create render pass, framebuffers, pipeline, descriptors...

// 6. Record command buffers
vkBeginCommandBuffer(cmdBuffer, &beginInfo);
vkCmdBeginRenderPass(cmdBuffer, &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);
vkCmdBindPipeline(cmdBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, pipeline);
vkCmdBindDescriptorSets(cmdBuffer, ..., &descriptorSet, 0, nullptr);
vkCmdBindVertexBuffers(cmdBuffer, 0, 1, &vertexBuffer, offsets);
vkCmdDrawIndexed(cmdBuffer, indexCount, 1, 0, 0, 0);
vkCmdEndRenderPass(cmdBuffer);
vkEndCommandBuffer(cmdBuffer);

// 7. Submit to queue with synchronization
VkSubmitInfo submitInfo = {};
submitInfo.commandBufferCount = 1;
submitInfo.pCommandBuffers = &cmdBuffer;
vkQueueSubmit(graphicsQueue, 1, &submitInfo, fence);

// 8. Present rendered image to screen
vkQueuePresentKHR(presentQueue, &presentInfo);
```

### Vulkan Synchronization

```cpp
// Pipeline barrier: ensure writes in vertex shader are visible to fragment shader
VkMemoryBarrier memBarrier = {};
memBarrier.srcAccessMask = VK_ACCESS_VERTEX_ATTRIBUTE_READ_BIT;
memBarrier.dstAccessMask = VK_ACCESS_SHADER_READ_BIT;

vkCmdPipelineBarrier(
    cmdBuffer,
    VK_PIPELINE_STAGE_VERTEX_INPUT_BIT,   // Wait for this stage to finish
    VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT, // Before this stage begins
    0, 1, &memBarrier, 0, nullptr, 0, nullptr
);

// Semaphore: signal when GPU finishes rendering, wait before presenting
VkSemaphore renderFinished;
vkCreateSemaphore(device, &semaphoreInfo, nullptr, &renderFinished);
// submitInfo.pSignalSemaphores = &renderFinished; (signal when done)
// presentInfo.pWaitSemaphores = &renderFinished;  (wait before present)
```

---

## 10. OpenGL

OpenGL is a state-machine-based graphics API from 1992. Still widely used for compatibility, education, and cross-platform 2D/3D graphics.

### Core Concepts

**State machine:** OpenGL maintains global state — bound textures, active shaders, blend mode, etc. Every draw call uses whatever state is currently set.

```c
// Bind shader program — affects all subsequent draws
glUseProgram(shaderProgram);

// Set uniform variable in shader
int loc = glGetUniformLocation(shaderProgram, "modelMatrix");
glUniformMatrix4fv(loc, 1, GL_FALSE, &model[0][0]);

// Bind texture
glActiveTexture(GL_TEXTURE0);
glBindTexture(GL_TEXTURE_2D, textureID);

// Bind vertex data
glBindVertexArray(vao);

// Draw
glDrawElements(GL_TRIANGLES, indexCount, GL_UNSIGNED_INT, 0);
```

### VAO / VBO / EBO

```c
// Vertex Array Object — remembers buffer bindings and attribute config
GLuint vao;
glGenVertexArrays(1, &vao);
glBindVertexArray(vao);

// Vertex Buffer Object — GPU memory containing vertex data
GLuint vbo;
glGenBuffers(1, &vbo);
glBindBuffer(GL_ARRAY_BUFFER, vbo);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

// Attribute format: location 0, 3 floats, stride, offset
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
// Location 1: normals (3 floats, offset 3 floats in)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6*sizeof(float), (void*)(3*sizeof(float)));
glEnableVertexAttribArray(1);

// Element Buffer Object — index buffer
GLuint ebo;
glGenBuffers(1, &ebo);
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
```

### OpenGL Shader Compilation

```c
// Create, compile, link shaders at runtime
GLuint vertShader = glCreateShader(GL_VERTEX_SHADER);
glShaderSource(vertShader, 1, &vertSrc, NULL);
glCompileShader(vertShader);

GLuint fragShader = glCreateShader(GL_FRAGMENT_SHADER);
glShaderSource(fragShader, 1, &fragSrc, NULL);
glCompileShader(fragShader);

GLuint program = glCreateProgram();
glAttachShader(program, vertShader);
glAttachShader(program, fragShader);
glLinkProgram(program);
```

### OpenGL vs Vulkan

| Aspect | OpenGL | Vulkan |
|--------|--------|--------|
| **Driver work** | Enormous (hidden) | Minimal (explicit) |
| **Setup code** | ~50 lines | ~1000+ lines |
| **Performance** | Good (unpredictable peaks) | Excellent (predictable) |
| **Multi-threading** | Limited (one context/thread) | Full (multiple queues/threads) |
| **Shader caching** | Driver-managed | Application-managed |
| **Learning curve** | Moderate | Steep |
| **Best for** | Learning, tools, prototyping | Games, engines, AAA |

---

## 11. GPU Memory Architecture

```
GPU Memory Types:

GDDR6X (RTX 4090):
  192-bit bus, 24 GB
  1008 GB/s bandwidth
  On-package discrete chips

HBM3 (A100, H100):
  5120-bit bus (stacked dies)
  3.35 TB/s bandwidth
  On-package, stacked with interposer
  Used in data center / ML GPUs

Unified Memory (Apple M-series, AMD integrated):
  CPU and GPU share the same physical DRAM
  No explicit transfer needed between CPU and GPU
  Apple M2 Max: 400 GB/s (entire pool accessible to GPU)

Virtual Memory:
  GPUs support virtual memory (managed by driver)
  Physical pages allocated on demand
  cudaMallocManaged() / Vulkan VK_MEMORY_HEAP_DEVICE_LOCAL_BIT
```

---

## 12. GPU Drivers

### Driver Stack (Linux)

```
Application (game, ML framework)
        ↓
User-space driver library (libvulkan, libOpenGL, libcuda)
        ↓
Mesa (open-source: AMD, Intel, Apple) or
NVIDIA proprietary user-space library
        ↓
DRM (Direct Rendering Manager) — kernel subsystem
        ↓
KMS (Kernel Mode Setting) — display output
GPU kernel module (nvidia.ko / amdgpu.ko / i915.ko)
        ↓
GPU hardware via PCIe / MMIO
```

```bash
# Check GPU and driver info on Linux
lspci | grep -i vga           # What GPU
nvidia-smi                    # NVIDIA driver version, memory, processes
rocm-smi                      # AMD ROCm info
glxinfo | grep "OpenGL"       # OpenGL version and renderer
vulkaninfo | head -30          # Vulkan capabilities
cat /proc/driver/nvidia/...   # NVIDIA kernel module details
```

### DXVK and Translation Layers

```
Windows game using DirectX 11
        ↓
DXVK (translation layer) → Vulkan API calls
        ↓
Native Vulkan driver on Linux
        ↓
GPU hardware
```

This is how Steam Proton runs Windows games on Linux — DXVK translates DirectX 11/12 to Vulkan with minimal overhead.

---

## See Also

- [CPU Architecture](cpu-architecture.md) — CPU hardware internals, pipelines, caches
- [Drivers & DLLs](drivers-and-dlls.md) — How drivers and shared libraries work
- [Compilers & Interpreters](compilers-and-interpreters.md) — How shader code gets compiled
