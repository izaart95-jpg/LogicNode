# CGI & VFX — Computer Graphics and Visual Effects

How CGI (Computer Generated Imagery) and VFX (Visual Effects) work — from 3D scene construction to the final rendered pixel. Covers the rendering pipeline, major techniques, industry software, and how Hollywood VFX is actually produced.

---

## Table of Contents
1. [CGI vs VFX — The Distinction](#1-cgi-vs-vfx--the-distinction)
2. [The 3D Graphics Pipeline](#2-the-3d-graphics-pipeline)
3. [Rendering — Ray Tracing vs Rasterization](#3-rendering--ray-tracing-vs-rasterization)
4. [Global Illumination & Lighting](#4-global-illumination--lighting)
5. [Shaders and Materials (PBR)](#5-shaders-and-materials-pbr)
6. [VFX Pipeline — Film Production](#6-vfx-pipeline--film-production)
7. [Compositing](#7-compositing)
8. [Simulation — Fluids, Cloth, Particles](#8-simulation--fluids-cloth-particles)
9. [Motion Capture](#9-motion-capture)
10. [Industry Software](#10-industry-software)
11. [Real-time vs Offline Rendering](#11-real-time-vs-offline-rendering)

---

## 1. CGI vs VFX — The Distinction

```
CGI (Computer Generated Imagery):
  Fully digital content — characters, environments, objects created in 3D software
  The dragon in How to Train Your Dragon: 100% CGI
  The environments in Avatar: ~70% CGI

VFX (Visual Effects):
  Any post-production technique that creates imagery that would be
  impossible, impractical, or too dangerous to capture on set
  Includes: CGI elements, but also compositing, matte painting,
            green screen replacement, particle effects, motion tracking
  The Avengers' fight scene: CGI characters composited onto real set footage

Practical effects (not VFX):
  Physical effects on set: pyrotechnics, miniatures, make-up prosthetics
  Star Wars original trilogy: mostly practical effects
  Many studios combine practical + digital for best result

FX vs VFX:
  FX (Special Effects): on-set physical effects (explosions, weather machines)
  VFX: post-production digital effects
  The distinction matters for awards and credits
```

---

## 2. The 3D Graphics Pipeline

Every frame of a CGI film or video game starts as mathematical data and becomes pixels through these stages:

### Stage 1: Scene Construction

```
3D World:
  Geometry:    Meshes (triangulated surfaces) defining shapes
  Transforms:  Translation, rotation, scale — position everything in 3D space
  Lights:      Point lights, spotlights, area lights, HDRI environment
  Camera:      Position, orientation, FOV, depth of field, motion blur
  Materials:   Shaders defining surface appearance (color, roughness, metalness)
  Animation:   Keyframed or procedural motion, skeletal deformation

Coordinate systems:
  Object space:  Local to each mesh (origin at object center)
  World space:   Global scene coordinate system
  Camera space:  Origin at camera, looking down -Z axis
  Clip space:    NDC (Normalized Device Coordinates) after projection
  Screen space:  Final pixel coordinates on the 2D image plane
  
Transformations (Model-View-Projection = MVP matrix):
  1. Object → World: model matrix (scale, rotate, translate object)
  2. World → Camera: view matrix (inverse of camera's transform)
  3. Camera → Clip:  projection matrix (perspective or orthographic)
  
  For every vertex:  gl_Position = P × V × M × vertex_position
```

### Stage 2: Geometry Processing

```
Subdivision surfaces (SubDiv):
  Coarse cage mesh (low polygon) → mathematically smooth surface
  Catmull-Clark subdivision: each quad split into 4, vertices smoothed
  Film standard: render at subdivision level 2–4 (4× to 16× more polys)
  Animation rigs work on low-poly cage, render uses smooth surface

Level of Detail (LOD):
  Close objects: full polygon count
  Distant objects: simplified mesh (fewer triangles)
  Automatic: distance-based or screen-space coverage threshold

Tessellation (GPU stage):
  Control mesh → GPU generates additional triangles based on view distance
  Hardware tessellation (DirectX 11 / OpenGL 4.0): done entirely on GPU

Normal mapping:
  Low-poly mesh + normal map texture = appearance of high-poly detail
  Normal map stores surface normal directions as RGB colors
  Fakes lighting of fine surface details without actual geometry cost
```

### Stage 3: Rasterization (real-time) or Ray Tracing (offline)

See §3 for full detail.

### Stage 4: Shading

```
For each visible surface point:
  1. Evaluate material shader: albedo, roughness, metalness, emission, opacity
  2. Accumulate light contributions from all light sources
  3. Apply indirect illumination (GI — pre-computed or ray-traced)
  4. Apply post effects: depth of field, motion blur, lens flare

Output: RGBA values per pixel (HDR — floating point, not clamped to 0–1)
```

### Stage 5: Post-Processing / Compositing

```
Raw render passes (EXR files):
  beauty:       final combined image
  diffuse:      albedo × diffuse lighting
  specular:     specular highlights
  reflection:   pure reflections
  emission:     self-illuminated surfaces
  depth (Z):    distance from camera per pixel
  normal:       surface normals
  cryptomatte:  per-object/material ID masks for isolation

Post-processing:
  Tone mapping: HDR → SDR (Reinhard, ACES, AgX filmic)
  Color grading: LUT (Look-Up Table) for cinematic color treatment
  Bloom:         glow around bright areas (lens scattering simulation)
  Depth of field: bokeh blur from Z-pass using circle of confusion
  Motion blur:   velocity vectors → directional blur
  Film grain:    add noise for organic look
  Chromatic aberration: RGB channel offset (lens distortion)
```

---

## 3. Rendering — Ray Tracing vs Rasterization

See [GPU Architecture](gpu-architecture.md) for technical detail on hardware implementation. Here is the conceptual and artistic side:

### Ray Tracing Physics

```
Ray tracing simulates physical light transport:

Camera → virtual pixel → shoot ray into scene
  Hit object surface:
    Material evaluation: absorption, reflection, transmission
    
    Diffuse surface (matte):
      Bounce ray in random hemisphere direction (cosine-weighted)
      Color = integral over hemisphere of incoming light × albedo
    
    Specular surface (mirror):
      Reflect ray: direction = incident - 2(incident·normal)×normal
      Color = color of what reflected ray hits × reflectivity
    
    Glass/water (transmission):
      Refract ray: Snell's law → n₁sin(θ₁) = n₂sin(θ₂)
      Partial reflection (Fresnel equations)
    
    Recursive: reflected/refracted ray hits next surface → repeat
    Terminate: max depth (typically 5–12 bounces) or when contribution < threshold

Physical accuracy:
  Path tracing (Monte Carlo integration) IS physically accurate
  Approximations:
    Not enough samples → noisy image (fireflies, variance)
    Denoising AI (NVIDIA OptiX, Intel Open Image Denoise): clean noisy renders
    
Convergence: path tracing converges to the physically correct answer with infinite samples
Film rendering: 512–4096 samples per pixel (SPP), hours per frame
Real-time (DLSS/DLAA + RTX): 1–4 SPP + AI denoising → 30/60fps
```

### Why Films Take So Long to Render

```
Toy Story (1995): 
  Average: 45 CPU hours per frame × 1,561,291 frames = 70 million CPU hours
  1000 CPUs × 24 hours/day = ~6 years. Rendered in 2 years with larger farm.

Modern film (2024):
  Pixar "Elemental" (2023):
  Complex fire/water simulation + GI + subsurface scattering
  Peak render: 250 hours per frame on some shots
  ~250 CPU-hours × 24fps × 100 min = 36 million core-hours per hour of film
  Render farms: hundreds of thousands of CPU cores
  AWS, Google Cloud, and on-premises farms used

Why so slow:
  Path tracing needs thousands of samples to converge
  Each sample = shoot and follow one ray through scene
  Complex scenes: 10M polygons, 50 lights, deep recursion
  Volume rendering (clouds, fire, smoke): especially expensive
  Motion blur + depth of field: require extra samples
```

---

## 4. Global Illumination & Lighting

```
Direct illumination: light from source directly to surface (fast)
Global illumination: bounced light from surface to surface (expensive, realistic)

Without GI:
  Dark areas = pure black (no bounce light)
  Looks flat and fake ("plastic" appearance)

With GI:
  Light bounces off walls → colored fill light (color bleeding)
  Sky light fills in shadows (sky dome illumination)
  Caustics: focused light through glass/water (hard to compute)

GI algorithms:

Path tracing (ground truth):
  Shoot thousands of rays per pixel, follow bounces
  Physically accurate, extremely slow
  Film standard (Arnold, RenderMan, V-Ray, Cycles)

Radiosity (early method, now historical):
  Divide scene into patches
  Solve linear system of equations for patch energies
  Baked into texture maps → very fast at runtime
  Problem: static lighting only, no specular

Irradiance caching / Photon mapping:
  Pre-compute photon bounces → build map → sample at render time
  Hybrid: fast GI approximation

HDRI (High Dynamic Range Image) lighting:
  360° panoramic photograph of a real environment
  Used as infinite sphere light source around scene
  Provides realistic ambient light matching real-world conditions
  Used in: product visualization, VFX integration (match real set lighting)

Light probes (real-time):
  Sphere of rendered environment captured at key points
  GPU samples probe → fast approximate GI
  Used in: game engines (Unreal, Unity)
```

---

## 5. Shaders and Materials (PBR)

### Physically Based Rendering (PBR)

PBR is the current industry standard for materials — parameters correspond to real-world physical properties, producing consistent results under any lighting.

```
Core PBR parameters:
  Base Color (Albedo): surface color, free of lighting information (0–1 per channel)
  Metalness:           0 = dielectric (plastic, wood, skin), 1 = metal
  Roughness:           0 = mirror smooth, 1 = completely diffuse
  Normal Map:          surface micro-detail encoded as normal vectors
  Ambient Occlusion:   pre-baked shadow in crevices
  Emission:            self-illumination (glow)

Metalness workflow (used by Substance, Unreal, Unity, Blender):
  Metals:     color from BaseColor, no albedo in specular, high reflectivity
  Dielectrics: specular = ~4% reflectance (n=1.5 for most non-metals), color in diffuse

Speculative/Glossiness workflow (used by V-Ray, older pipelines):
  Specular map: reflectivity per pixel
  Glossiness:   inverse of roughness
  Different math, same visual result

BSDF — Bidirectional Scattering Distribution Function:
  Mathematical function describing how light scatters at a surface
  BRDF: Reflectance (opaque surfaces)
  BTDF: Transmittance (transparent surfaces)
  BSSRDF: Subsurface scattering (skin, marble, wax)

Important BRDFs:
  Lambertian: perfect matte diffuse (cos(θ) distribution)
  Cook-Torrance GGX: physically accurate specular (most common in PBR)
  Disney "principled" BSDF: artist-friendly, production proven (Pixar)
    Parameters: subsurface, metallic, specular, roughness, anisotropic,
                sheen, clearcoat, transmission — all 0–1, intuitive
```

### Subsurface Scattering (SSS)

```
Light enters translucent material, scatters inside, exits at different point
Critical for: human skin, candle wax, marble, jade, milk, leaves

Without SSS: skin looks like painted plastic
With SSS:    ears glow when backlit, skin has natural warmth, translucency

Implementation:
  Simple: screen-space blur of diffuse component (fast, game quality)
  Accurate: BSSRDF evaluation with random walk inside volume (offline)
  
  Scattering parameters per material:
    Mean free path: how far light travels before scattering
    Scattering color: what frequencies are absorbed vs scattered
    Skin: strong red scattering (blood), deeper blue penetration
```

---

## 6. VFX Pipeline — Film Production

### Pre-production

```
Pre-vis (Previzualization):
  Rough 3D animation showing camera moves, scene layout, action beats
  Director approves timing before any expensive production begins
  Tools: Previz-specific tools, game engines (Unreal for real-time previz)

Layout:
  Place cameras, set dressing, characters in digital environment
  Establish shot composition before shot is given to animators

Storyboard → Animatic:
  2D sketches → basic timed animation + temp audio
  Production relies on animatic for planning resources
```

### Production Phases

```
1. Tracking / Matchmove:
   Analyze live footage → extract camera movement as 3D data
   3D camera must exactly match real camera for compositing to work
   Tools: SynthEyes, PFTrack, 3DEqualizer (industry standard)
   
2. Roto / Paint:
   Rotoscoping: frame-by-frame manual masking (isolate actors from background)
   Paint: remove wires, rigs, crew from footage
   Tools: Silhouette FX, Nuke

3. Modeling:
   Create 3D geometry for characters, props, environments
   Tools: Maya, ZBrush (digital sculpting), Houdini, Blender

4. Rigging:
   Create skeleton and control system for animated characters
   Blend shapes for facial animation (52+ blend shapes for realistic faces)

5. Animation:
   Keyframe or motion capture driven
   Physics simulation (cloth, hair, soft body)
   Crowd simulation (thousands of animated characters)

6. FX/Simulation:
   Fluid simulation, pyro (fire, smoke), rigid body destruction
   Tools: Houdini (industry standard for FX), Bifrost (Maya)

7. Lighting:
   Place virtual lights matching real set photography
   HDRI from on-set light probes
   Match plate lighting exactly

8. Rendering:
   Submit to render farm
   Output: EXR image sequences (one per frame, multiple render passes)
   
9. Compositing:
   Combine all render passes + live plate + grades
   Match colors, add camera grain, integration
   Tools: Nuke (industry standard), After Effects (broadcast)

10. DI (Digital Intermediate):
    Final color grade for entire film
    HDR mastering, theatrical vs streaming deliverables
    DaVinci Resolve (industry standard colorist tool)
```

---

## 7. Compositing

Compositing combines multiple image layers into a single final image.

### Alpha Compositing (Porter-Duff)

```
Every pixel has RGBA: Red, Green, Blue, Alpha (opacity)
Alpha: 0 = fully transparent, 1 = fully opaque

Over operation (A over B — most common):
  output = A_rgb + B_rgb × (1 - A_alpha)
  
  Perfectly opaque A: output = A (B not visible)
  Perfectly transparent A: output = B
  Semi-transparent A: blend according to alpha
  
Premultiplied alpha (standard in VFX):
  RGB values already multiplied by alpha
  Premult: color = [1.0, 0.0, 0.0, 0.5] → premultiplied [0.5, 0.0, 0.0, 0.5]
  Avoids black fringing in compositing
  Always work in premultiplied space in Nuke/After Effects

Common operations in Nuke node graph:
  Merge:      combine two images (Over, Under, Screen, Multiply, Plus...)
  Grade:      adjust exposure, lift/gamma/gain (color correction)
  Roto:       manual mask drawing (isolate elements)
  Keyer:      extract alpha from green/blue screen
  Tracker:    2D tracking for stabilization or match-move
  Camera3D:   project 3D elements using tracked camera
  ScanlineRender: render geometry in composite
  Blur/Defocus: depth of field from Z-depth pass
```

### Green Screen / Chroma Key

```
Why green (or blue)?
  Human skin has very little green → green channel is easy to isolate
  Blue used in older film (lower noise in film stock)
  Green = brightest channel on digital cameras (Bayer pattern: 2G, 1R, 1B)

Keying process:
  1. Sample green screen color → define key color
  2. Chroma keyer: pixels similar to key color → become transparent
  3. Spill suppression: remove green cast from subject's edges
  4. Matte refinement: erode/dilate edges, blur for naturalness
  5. Despill: color correct green fringing on hair/fine details
  
Common problems:
  Color spill: green light reflected on subject → despill algorithms
  Fine hair/flyaways: difficult to key cleanly → Primatte, Keylight, IBK tools
  Wrinkles/shadows: varying green value → need multiple samples
  
Blue screen advantages:
  Better for digital actors under very dark or night shots
  Higher reflectance from blue screens vs green at night
  Used in: sci-fi sets, nighttime sequences, blue clothing shots
```

---

## 8. Simulation — Fluids, Cloth, Particles

### Fluid Simulation

```
Navier-Stokes equations govern fluid motion:
  ∂u/∂t + (u·∇)u = -∇P/ρ + ν∇²u + f
  ∇·u = 0  (incompressibility)

  u = velocity field, P = pressure, ρ = density, ν = viscosity, f = external forces

Solving numerically on a voxel grid (Eulerian) or particles (SPH/Lagrangian):

Houdini FLIP fluid (industry standard):
  Particles carry velocity information
  Transfer to grid → solve Navier-Stokes → transfer back to particles
  FLIP (Fluid Implicit Particles): combines benefits of grid and particles
  
Pyro (fire, smoke, explosions):
  Smoke: density + temperature fields, buoyancy drives upward motion
  Fire: fuel burns → release heat → buoyancy + hot gas expansion
  Vorticity confinement: add artificial vorticity to prevent numerical diffusion

GPU simulation:
  Houdini: CPU-based, high quality but slow
  Real-time: Niagara (Unreal), VFX Graph (Unity) — GPU particles
  PhysX Flex / NVIDIA FleX: position-based dynamics on GPU
```

### Cloth Simulation

```
Position-Based Dynamics (PBD):
  Most common in real-time (games)
  Solve spring/distance constraints between cloth vertices
  
FEM (Finite Element Method):
  More physically accurate, used in offline VFX
  Deformable solids: cloth, skin, soft bodies
  
Parameters:
  Stiffness:    resistance to stretching
  Bending:      resistance to folding
  Friction:     collision friction against body/ground
  Self-collision: prevent cloth passing through itself (expensive)

Houdini Vellum: unified simulation for cloth, hair, wires, soft bodies
Marvelous Designer: specialized cloth/fashion simulation tool
```

---

## 9. Motion Capture

```
Marker-based (optical):
  Retroreflective markers placed on actor's body at key joints
  Multiple calibrated infrared cameras surrounding capture volume
  Software (Vicon, OptiTrack) triangulates marker positions at 120–480 fps
  
  Data: skeleton joint positions per frame → retargeted to CG character
  Problem: only captures body mechanics, not facial (separate facial mocap)
  Used for: body performance, stunt work, creature reference

Markerless (video-based):
  AI-based estimation from video (OpenPose, MediaPipe, DeepMotion)
  Lower accuracy but no suit required
  Used in: indie productions, pre-vis, game dev

Facial capture:
  Helmet cam with downward-pointing camera at actor's face
  Small dots on face → track dot positions → drive 52+ blend shapes
  Industrial Light & Magic: MOVA (projection-based, used in Avatar)
  
Performance capture:
  Full facial + body simultaneously
  Andy Serkis (Gollum, Thanos, Caesar): performance capture pioneer
  Actor performs entire role in mocap suit → digital character driven by performance

Inertial capture (IMU-based):
  Accelerometers + gyroscopes on suit → calculate joint rotations
  No camera required → use outdoors, any lighting
  Less accurate than optical but very portable
  Used for: quick prototypes, broadcast sports analysis
```

---

## 10. Industry Software

### 3D / DCC (Digital Content Creation)

```
Houdini (SideFX):
  Industry standard for FX, simulations, procedural workflows
  Used in: ILM, Weta, DNEG, Framestore, almost all major VFX houses
  Node-based procedural graphs (SOPs, DOPs, ROPs, VOPs)
  HQueue: Houdini's render farm management
  Price: Apprentice (free), Indie ($270/yr), Commercial ($4450/yr)

Maya (Autodesk):
  Industry standard for character animation and rigging
  MEL scripting + Python API
  Used alongside Houdini: Maya for animation, Houdini for FX
  Price: ~$1,870/yr subscription

ZBrush (Maxon):
  Digital sculpting — create organic shapes (creatures, characters)
  Works with polygons in the tens of millions
  DynaMesh, ZRemesher, Sculptris Pro
  Price: ~$40/mo or $895 perpetual

Cinema 4D:
  Strong in motion graphics (MoGraph toolset)
  Good integration with After Effects (via Cineware)
  Popular in broadcast/advertising VFX

Blender (open source):
  Full 3D pipeline: modeling, sculpting, rigging, animation, simulation, rendering
  Cycles (path tracer) + EEVEE (real-time preview renderer)
  Geometry Nodes: procedural modeling
  Used professionally by smaller studios, increasingly in film

3ds Max:
  Common in architectural visualization and games
  Less common in film VFX

Substance 3D Painter/Designer (Adobe):
  Industry standard for texture creation
  PBR texturing with procedural generators
  Used in games + VFX for PBR material authoring
```

### Rendering Engines

```
Arnold (Autodesk):
  Ray tracing renderer, industry standard in film VFX
  Integrated in Maya (Arnold for Maya)
  Scene-based, not viewport-based — submit jobs to farm

RenderMan (Pixar):
  Used in all Pixar/Disney films
  OSL (Open Shading Language) shaders
  XPU mode: CPU + GPU hybrid rendering

V-Ray (Chaos):
  Popular in VFX and architectural visualization
  Available for Maya, Houdini, 3ds Max, Cinema 4D, Blender
  
Redshift (Maxon):
  GPU-based biased renderer — fast, good quality tradeoff
  Popular when fast turnarounds needed

Karma (SideFX):
  Houdini's native renderer (XPU: CPU+GPU)
  Tight integration with Houdini simulations

Cycles (Blender):
  Open source path tracer
  Optix/CUDA/Metal GPU acceleration

Octane (OTOY):
  GPU-only unbiased renderer
  Spectral rendering, high quality

Mantra (SideFX legacy):
  Older Houdini renderer, being replaced by Karma
```

### Compositing

```
Nuke (Foundry):
  Industry standard compositing for film VFX
  Node-based workflow, 32-bit float color depth
  3D compositing, camera projection, particle system
  Used by: every major VFX studio
  Price: ~$3,000/yr

After Effects (Adobe):
  Industry standard for motion graphics and broadcast
  Layer-based (not node-based like Nuke)
  Plugin ecosystem: Element 3D, Trapcode Suite, Red Giant
  Not suitable for complex film VFX (use Nuke) but dominant in broadcast

DaVinci Resolve (Blackmagic):
  Industry standard for color grading
  Free version includes Fusion (node-based compositor like Nuke)
  Resolve Studio: $295 perpetual license
  Used for: final color grade, broadcast finishing

Flame (Autodesk):
  High-end broadcast compositing
  Used for commercials, TV, some film
```

---

## 11. Real-time vs Offline Rendering

```
Real-time (games, real-time pre-vis, virtual production):
  Budget: 16.67ms per frame (60fps) or 33.33ms (30fps)
  Techniques: rasterization + screen-space effects + limited ray tracing
  APIs: Vulkan, DirectX 12, Metal, OpenGL
  Engines: Unreal Engine 5 (Lumen GI, Nanite virtualized geometry)
           Unity (HDRP), Godot
  
Offline (film, TV, advertising, product visualization):
  Budget: seconds to hours per frame
  Techniques: full path tracing, volumetrics, high-poly geometry
  Software: Houdini + Arnold/RenderMan/Karma, Maya + Arnold
  
Virtual Production:
  LED volume stages (The Volume used in The Mandalorian)
  Unreal Engine renders real-time CGI background on LED wall
  Camera tracks real movement → parallax shift in background
  In-camera VFX: no green screen, final composite happens live
  Benefit: actors see real environment, practical lighting from LEDs
  
Game cinematics vs film:
  Game engine cutscenes: real-time → limited visual fidelity
  Pre-rendered cutscenes: offline rendered → film quality
  Blurring: Unreal 5 + photorealistic assets → near film quality in real-time
  Final Fantasy VII Rebirth: mix of real-time and pre-rendered cutscenes
```

---

## See Also

- [GPU Architecture](gpu-architecture.md) — Hardware that runs these pipelines (CUDA, RTX, Vulkan)
- [How a Computer Really Works](how-computers-work.md) — GPU in context of full system
- [Media Tools](../media/media-tools.md) — FFmpeg, VLC for video processing
- [AI Video Tools](../ai/ai-video-tools.md) — AI-powered video generation
