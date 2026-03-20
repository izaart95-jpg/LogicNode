# Creative Software

Reference guide for professional and consumer creative applications — 3D, video editing, color grading, photo editing, and content creation tools.

---

## Table of Contents
1. [Blender](#1-blender)
2. [DaVinci Resolve](#2-davinci-resolve)
3. [Adobe Photoshop](#3-adobe-photoshop)
4. [Adobe Premiere Pro](#4-adobe-premiere-pro)
5. [Filmora](#5-filmora)
6. [CapCut Desktop](#6-capcut-desktop)
7. [Software Comparison](#7-software-comparison)

---

## 1. Blender

- **Website:** https://blender.org
- **License:** GNU GPL v3 (free and open source forever)
- **Price:** Free
- **Platform:** Windows, macOS, Linux
- **Current version:** 4.x

### Overview

Blender is a complete open-source 3D suite covering the entire content creation pipeline: modeling, sculpting, rigging, animation, particle simulation, rendering (Cycles + EEVEE), compositing, and video editing — all in one application. Used in film VFX, game asset creation, architectural visualization, motion graphics, and scientific visualization.

### Interface Concepts

```
Blender uses an area-based interface — every area can show any editor type.
Right-click or edge-drag to split/merge areas.

Main editor types:
  3D Viewport:      Your primary working area — view and manipulate 3D objects
  Properties:       Object/scene/render/material/modifier settings
  Outliner:         Scene hierarchy (objects, collections, linked data)
  Timeline:         Animation keyframe overview
  Graph Editor:     FCurve animation curve editing
  Dope Sheet:       Keyframe management across all animated properties
  NLA Editor:       Non-Linear Animation — combine/reuse animation clips
  Shader Editor:    Node-based material creation (PBR materials)
  Compositor:       Node-based image compositing (post-processing)
  Geometry Nodes:   Procedural modeling and effects
  Sequencer:        Video editing / sequence editor
  UV Editor:        UV unwrap and texture coordinate editing
  Image Editor:     Texture painting, image reference
  Text Editor:      Write Python scripts / addons
  
Workspaces (tabs at top):
  Layout, Modeling, Sculpting, UV Editing, Texture Paint, Shading,
  Animation, Rendering, Compositing, Geometry Nodes, Scripting
```

### Essential Shortcuts (3D Viewport)

```
Navigation:
  Middle Mouse:     Orbit
  Shift+MMB:        Pan
  Scroll / Ctrl+MMB: Zoom
  Numpad 1/3/7:     Front/Right/Top orthographic views
  Numpad 5:         Toggle perspective/orthographic
  Numpad 0:         Camera view
  `/` (numpad):     Focus on selected (isolate)

Selection:
  Left Click:       Select
  Shift+Click:      Add to selection
  A:                Select all / deselect all
  B:                Box select (drag)
  C:                Circle select
  Ctrl+I:           Invert selection
  
Object mode (Tab to toggle edit):
  G:                Grab/move (then X/Y/Z to constrain axis, type number for amount)
  R:                Rotate (then X/Y/Z, type degrees)
  S:                Scale (then X/Y/Z, type factor)
  G X 5:            Move 5 units on X axis
  R Z 90:           Rotate 90° around Z
  S X 2:            Scale 2× on X
  Ctrl+A:           Apply transforms (freeze current state as default)
  Shift+D:          Duplicate (creates linked copy)
  Alt+D:            Duplicate linked (shares mesh data)
  M:                Move to collection
  H / Alt+H:        Hide / unhide selected
  
Edit mode (Tab):
  1/2/3:            Vertex / Edge / Face select mode
  E:                Extrude
  I:                Inset face
  Ctrl+R:           Loop cut (scroll to add more loops)
  K:                Knife tool
  F:                Fill (create face/edge between selected)
  Alt+Click:        Select edge/face loop
  Ctrl+B:           Bevel
  P:                Separate (to new object)
  Ctrl+J:           Join objects together (object mode)

Quick operations:
  Shift+A:          Add mesh/curve/light/camera/etc. (Add menu)
  X or Delete:      Delete
  F3:               Search for any operator by name
  Ctrl+Z / Ctrl+Y:  Undo / Redo
  N:                Toggle properties panel (right side)
  T:                Toggle toolbar (left side)
```

### Rendering

```
Two built-in renderers:

Cycles (Path Tracer):
  Physically accurate, ray-traced
  CPU or GPU (NVIDIA CUDA/OptiX, AMD HIP, Apple Metal)
  Use for: final renders, photorealistic results
  Slow on CPU, fast on modern GPU
  
  Settings: Properties → Render → Render Engine → Cycles
  Samples: higher = better quality, slower (start with 128, production: 512–2048)
  Denoising: ON (Intel OpenImageDenoise or NVIDIA OptiX) → clean result faster
  GPU: Properties → Preferences → System → CUDA/OptiX devices

EEVEE Next (Real-time):
  OpenGL-based rasterization
  Very fast (seconds per frame) 
  Not physically accurate but very good quality
  Use for: animation previews, stylized work, fast iterations
  EEVEE Next (4.2+): global illumination, better shadows

Enable GPU rendering in Cycles:
  Edit → Preferences → System → Cycles Render Devices
  Select your GPU (CUDA for NVIDIA, HIP for AMD, Metal for Apple Silicon)
  Render Properties → Device → GPU Compute

Render output:
  Properties → Output → set resolution, frame rate, output folder
  Render → Render Image (F12) — single frame
  Render → Render Animation (Ctrl+F12) — render all frames
  Output format: PNG for stills, FFmpeg Video for direct MP4, EXR for VFX
```

### Python Scripting

```python
import bpy

# Create a cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cube = bpy.context.active_object
cube.name = "MyCube"

# Apply material
mat = bpy.data.materials.new(name="RedMaterial")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1, 0, 0, 1)  # Red
bsdf.inputs["Roughness"].default_value = 0.3
cube.data.materials.append(mat)

# Keyframe animation
cube.location = (0, 0, 0)
cube.keyframe_insert(data_path="location", frame=1)
cube.location = (0, 0, 5)
cube.keyframe_insert(data_path="location", frame=50)

# Run render
bpy.context.scene.render.filepath = "/tmp/render_"
bpy.ops.render.render(animation=True)

# Access via Blender's Scripting workspace → Text Editor → Run Script
```

### Geometry Nodes

```
Procedural modeling system (Blender 3.0+):
  Node-based modifier that generates/transforms geometry
  Non-destructive — change parameters, geometry updates instantly
  
Example: scatter trees on a terrain
  Input (terrain mesh)
  → Distribute Points on Faces (density=100)
  → Instance on Points (tree mesh as instance)
  → Set Scale (random 0.5–1.5)
  → Output (trees scattered on terrain)

Used for: scatter systems, procedural buildings, data visualization,
          VFX effects, generative art
```

### Key Addons

```
Built-in (enable in Preferences → Add-ons):
  Node Wrangler:    Essential for shader/compositor node editing shortcuts
  LoopTools:        Useful mesh editing operations
  Bool Tool:        Boolean operations with shortcuts
  Import-Export:    FBX, OBJ, Alembic, USD formats
  Rigify:           Auto-generate animation rigs

Community (blender market, github):
  RetopoFlow:       Retopology tools
  Hard Ops/BoxCutter: Hard surface modeling
  Scatter:          Advanced scatter/instance systems
  True-Sky:         Realistic sky and atmosphere
```

---

## 2. DaVinci Resolve

- **Website:** https://www.blackmagicdesign.com/products/davinciresolve
- **Price:** Free (DaVinci Resolve) / $295 perpetual (DaVinci Resolve Studio)
- **Platform:** Windows, macOS, Linux
- **Used for:** Color grading (industry standard), video editing, audio (Fairlight), VFX (Fusion)

### Overview

DaVinci Resolve is the industry standard for professional color grading — used in virtually every Hollywood film. The free version is remarkably capable. Studio adds collaborative features, noise reduction, more effects, and GPU acceleration for specific tasks.

### Pages (Workspaces)

```
Media:     Import and organize footage (bins, metadata, proxies)
Cut:       Fast edit mode — smart timeline for quick assembly
Edit:      Full timeline-based editing (like Premiere)
Fusion:    Node-based compositing and VFX (like Nuke, included free!)
Color:     Professional color grading — Resolve's flagship page
Fairlight: Professional audio mixing and editing (like Pro Tools lite)
Deliver:   Export with codec/format settings

Workflow: Media → Cut/Edit → Fusion (VFX) → Color → Fairlight → Deliver
```

### Color Page — Core Concepts

```
Color grading tools (Color page):
  Wheels: Lift (shadows), Gamma (midtones), Gain (highlights)
    Drag center: saturation offset
    Drag wheel: hue rotation
    
  Curves:
    Custom curves: precise tone curve per channel
    Hue vs Sat: adjust saturation at specific hue (boost only skin tones)
    Hue vs Hue: shift a specific color to another hue
    Sat vs Sat: boost/reduce saturation based on existing saturation level
    
  Qualifiers: Select specific colors/luminance for isolated grading
    Key:  sample color → creates mask → grade only that selection
    Magic Mask: AI-based rotoscoping (Studio only)
    
  Scopes (essential for accurate color):
    Waveform: check exposure (no clipping)
    Vectorscope: check color balance (should be centered for neutral)
    Parade: RGB waveforms separately (check color cast)
    Histogram: overall tonal distribution
    
  Nodes (how grading is structured):
    Serial nodes: applied in sequence (left to right)
    Parallel nodes: applied simultaneously, blended
    Layer nodes: like layers in Photoshop
    
    Recommended node structure:
    [Input] → [Exposure/Balance] → [Creative Look] → [Output CST] → [Output]

Color Science:
  Color Space Transform (CST): convert between color spaces
    Camera RAW → DaVinci Wide Gamut → Rec.709 (for delivery)
    or use ACES (industry color pipeline for VFX)
  
  LUTs (Look-Up Tables): stored color transforms
    Technical LUT: camera log → display (e.g., BMPCC4K to Rec.709)
    Creative LUT: stylistic look (warm, cinematic, etc.)
    Apply: Clips/Gallery tab → Right-click → Apply LUT
```

### Edit Page

```
Import: Media Pool → drag footage to timeline
        or: Ctrl+I to import

Timeline operations:
  I / O:          In/Out points on source/timeline
  F9:             Insert edit
  F10:            Overwrite edit
  Ctrl+B:         Blade (cut) at playhead
  Shift+Click:    Trim edit (ripple or roll)
  Alt+Drag:       Slip clip (change start point without moving position)
  Ctrl+Shift+D:   Disable clip
  Alt+Backspace:  Ripple delete (remove clip + close gap)

Color matching (Edit page):
  Right-click clip → "Flag for Color Grading"
  Use remote grades to apply same grade to matching clips

Multicam editing:
  Create multicam clip from synced footage
  Edit → Show Multicam Viewer → angle switching live

Proxy workflow:
  File → Project Settings → Master Settings → Optimized Media → generate proxies
  Playback is smooth via proxies, final render uses original files
```

### Fusion (Compositing)

```
Fusion is a fully featured compositing system (included free in Resolve):
  Node-based: connect nodes with wires (like Nuke)
  
Common nodes:
  MediaIn:      Input footage from timeline
  Transform:    Position, rotation, scale
  Merge:        Composite two layers (like Nuke Merge/Over)
  Polygon:      Draw roto shapes for masking
  Text+:        Advanced text generator with animation
  ColorCorrector: Color adjustment in composite
  Blur:         Gaussian/directional blur
  3D:           3D scene setup (lights, materials, cameras)
  Particle:     Particle systems
  
Run Fusion per-clip: select clip → press Fusion page
```

### Deliver Page — Export

```
Common export settings:

H.264 MP4 (YouTube, social media):
  Format: MP4
  Video codec: H.264
  Quality: Restrict to 50,000 Kbps OR Quality 85
  Audio codec: AAC, 192 Kbps

ProRes (Apple editing):
  Format: QuickTime
  Codec: Apple ProRes 422 HQ or ProRes 4444

DNxHD (Avid editing):
  Format: MXF
  Codec: DNxHD/HR

H.265 HEVC (smaller file, wide device support):
  Format: MP4
  Codec: H.265 (HEVC), CRF 18–23

DPX/EXR sequence (VFX deliverables):
  Format: DPX or EXR sequence
  Each frame = one file (for VFX pipeline)
```

---

## 3. Adobe Photoshop

- **Website:** https://adobe.com/products/photoshop
- **Price:** $20.99/month (Photography plan includes Lightroom)
- **Platform:** Windows, macOS, iPad (limited)
- **AI features:** Generative Fill (Firefly AI), Neural Filters

### Core Concepts

```
Layers:
  Every edit lives on a layer — non-destructive by default
  Layer types: Pixel, Adjustment, Fill, Shape, Type, Smart Object
  Smart Objects: linked layer preserving original data — edits are reversible
  Layer masks: black = hide, white = show (grayscale = partial transparency)
  
Blend modes: how layers interact with layers below
  Normal:     Standard opacity
  Multiply:   Darkens (like ink on paper — multiply colors)
  Screen:     Lightens (like projecting slides)
  Overlay:    Increase contrast (combines Multiply + Screen)
  Soft Light: Subtle contrast
  Hard Light: Strong contrast
  Color:      Apply hue + saturation from top layer, keep luminance from below
  Luminosity: Apply luminance from top, keep color from below
  
Adjustments (always use Adjustment Layers, not direct adjustments):
  Curves:       Tone mapping (most powerful)
  Levels:       Set black/white point
  Hue/Saturation: Color shifts
  Color Balance: Shadow/midtone/highlight color cast
  Vibrance:     Saturation boost protecting skin tones
  Photo Filter: Warm/cool color casts
  Gradient Map: Map tones to gradient (creative effects)
```

### Essential Tools

```
Selection tools:
  Marquee (M):    Rectangle / ellipse selection
  Lasso (L):      Freehand, polygonal, magnetic lasso
  Quick Selection (W): Brush-paint selection that finds edges
  Magic Wand:     Select by color (with tolerance)
  Object Select:  AI-powered — click object, Photoshop selects it
  Select Subject: One-click AI subject selection (surprisingly accurate)
  Select → Select and Mask: Refine edges (especially hair/fur)

Brush tools:
  Brush (B):      Paint on current layer
  Eraser (E):     Erase (prefer layer mask instead — non-destructive)
  Clone Stamp (S): Copy pixels from one area to another
  Healing Brush (J): Clone + texture blending (remove blemishes)
  Spot Healing:   One-click remove small imperfections (AI fill)
  Content-Aware Fill: Ctrl+Shift+Delete → remove object, fill with AI

Transform:
  Ctrl+T:        Free Transform (scale, rotate, skew, warp)
  Edit → Transform → Perspective/Warp/Distort
  Edit → Puppet Warp: bend/twist image with pin-based control

Generative Fill (AI, requires internet):
  Select an area → Edit → Generative Fill → describe what to generate
  "replace with ocean", "remove person", "add mountains"
  Generates 3 variations, all as Smart Object layers
```

### Keyboard Shortcuts

```
Tools:
  V:     Move tool
  B:     Brush
  E:     Eraser
  M:     Marquee select
  L:     Lasso
  W:     Quick Select / Magic Wand
  C:     Crop
  T:     Type
  G:     Gradient / Paint Bucket
  I:     Eyedropper
  Z:     Zoom
  H:     Hand / Pan

Operations:
  Ctrl+Z:         Undo
  Ctrl+Alt+Z:     Step backward (multiple undos)
  Ctrl+J:         Duplicate layer
  Ctrl+E:         Merge down
  Ctrl+Shift+E:   Merge visible
  Ctrl+Shift+Alt+E: Stamp visible (merge to new layer, keep originals)
  Ctrl+D:         Deselect
  Ctrl+Shift+I:   Invert selection
  Ctrl+T:         Free Transform
  Ctrl+L:         Levels
  Ctrl+M:         Curves
  Ctrl+U:         Hue/Saturation
  Ctrl+Shift+Alt+S: Save for Web (legacy)
  Alt+Click layer mask: View mask as grayscale
  
Brush:
  [ / ]:         Decrease/increase brush size
  Shift+[ / ]:   Decrease/increase hardness
  0–9:           Set opacity (0=100%, 5=50%)
  Shift+0–9:     Set flow
```

### Non-Destructive Workflow

```
Best practice: NEVER edit pixels directly on the original layer.

1. Open image → Right-click layer → Convert to Smart Object
2. Apply filters → become Smart Filters (editable/deletable)
3. Use Adjustment Layers instead of Image → Adjustments
4. Use Layer Masks instead of Eraser

Smart Object benefits:
  Scale down and back up without quality loss
  Apply filters that remain editable
  Replace embedded image (Smart Object → Edit Contents)
  Linked Smart Objects: one file updates all instances

Camera RAW as filter:
  Filter → Camera Raw Filter → full RAW processing controls on any layer
  Non-destructive on Smart Objects
```

---

## 4. Adobe Premiere Pro

- **Website:** https://adobe.com/products/premiere
- **Price:** ~$22/month (or Creative Cloud All Apps ~$60/month)
- **Platform:** Windows, macOS
- **Integrates with:** After Effects, Audition, Photoshop, Frame.io

### Project Setup

```
New Project:
  File → New → Project
  Set: name, location, renderer (Mercury Playback Engine GPU Accelerated)
  
Sequence settings:
  File → New → Sequence → choose preset matching your footage
  OR: right-click footage → New Sequence from Clip (auto-matches)
  
  Key settings:
    Resolution: 1920×1080 (HD), 3840×2160 (4K)
    Frame rate: match your camera (24, 25, 29.97, 30, 60fps)
    Preview codec: set to match GPU for hardware acceleration
    
Import:
  Ctrl+I or Media Browser panel
  Drag folder → "Import all" folder structure
  Import as proxy: File → Link Media → generate proxies in background
```

### Timeline Editing

```
Essential shortcuts:

Navigation:
  Spacebar:      Play/pause
  J/K/L:         Rewind / Pause / Fast forward (tap multiple times for faster)
  Left/Right:    Step 1 frame
  Shift+Left/Right: Step 5 frames
  Home/End:      Go to start/end
  I / O:         Set In / Out point
  ; (semicolon): Insert edit
  . (period):    Overwrite edit
  
Timeline:
  V:             Selection tool
  C:             Razor (cut) tool
  B:             Ripple Edit tool (trim and shift remaining clips)
  N:             Rolling Edit (trim both sides of cut)
  Ctrl+Shift+D:  Apply default video transition (usually Cross Dissolve)
  Ctrl+K:        Cut at playhead
  Shift+Delete:  Ripple delete (remove + close gap)
  Ctrl+D:        Select duration (type to change)
  
  Alt+Drag:      Copy clip
  Ctrl+Drag:     Copy audio/video only (not linked)
  Hold Alt:      Break audio-video link temporarily
  Ctrl+L:        Link/unlink audio and video
  
Multi-camera:
  Sequence → Create Multi-Camera Source Sequence (sync by audio or timecode)
  Sequence → Multi-Camera → Enable (switch angles live during playback)
```

### Color Grading in Premiere

```
Lumetri Color panel (Window → Lumetri Color):
  Basic Correction:
    White Balance: temp (warm/cool) + tint (green/magenta)
    Tone: Exposure, Contrast, Highlights, Shadows, Whites, Blacks
    Saturation
    
  Creative: Film looks (LUTs), Vibrance, Faded Film
  Curves: Custom tone curves + Hue/Sat/Luma curves
  Color Wheels: Shadows/Midtones/Highlights per-color-wheel
  HSL Secondary: Isolate and grade specific colors
  Vignette: Edge darkening
  
Apply LUT:
  Basic Correction → Input LUT → browse .cube file
  Creative → Look → browse .cube file
  
Auto color match:
  Select clips → Color → Comparison View → Auto Match
  Premiere AI-matches multiple clips to reference shot
  
Send to DaVinci Resolve:
  File → Export → Final Cut Pro XML → import into Resolve
  Or use EDL (Edit Decision List) for simpler sequences
```

### Export

```
File → Export → Media (Ctrl+M):

YouTube / social:
  Format: H.264, Match Source - Adaptive High Bitrate
  Profile: High, Level 4.2
  VBR 2 pass: Target 8–15 Mbps (1080p), 35–50 Mbps (4K)
  
Broadcast master (prores):
  Format: QuickTime
  Codec: Apple ProRes 422 HQ
  
Archive (lossless):
  Format: DNxHR 444, or uncompressed

Add to Media Encoder queue:
  Click Queue (instead of Export) → Adobe Media Encoder
  Render in background while continuing to edit
  
Adobe Premiere Auto Reframe:
  Sequence → Auto Reframe Sequence → generates vertical/square versions automatically
  AI-detects subject, keeps them in frame while changing aspect ratio
```

---

## 5. Filmora

- **Website:** https://filmora.wondershare.com
- **Price:** $49.99/year or $79.99 perpetual (+ optional AI add-on)
- **Platform:** Windows, macOS, iOS, Android
- **Target:** Beginners to intermediate content creators

### Overview

Filmora is a consumer-focused video editor with an emphasis on accessibility and built-in effects. No steep learning curve — most features accessible via click-and-drag. Good choice for YouTubers, content creators, and beginners who want professional-looking results quickly.

### Key Features

```
Editing:
  Drag-and-drop timeline editing
  Magnetic timeline option (auto-snaps clips)
  Multi-track video and audio
  Speed ramping (variable speed with visual curve)
  Auto-beat sync: cut to music automatically
  Motion tracking: attach text/stickers to moving objects
  
Effects library (huge, built-in):
  Transitions: 100+ animated transitions
  Video effects: overlays, filters, LUTs, glitch effects
  Text templates: animated lower thirds, titles, openers
  Motion graphics elements: particles, light leaks, overlays
  
AI features:
  AI Auto Reframe: auto-crop for 9:16 (TikTok/Reels) from 16:9
  AI Audio Stretch: extend audio to match video length
  AI Noise Reduction: remove background noise from audio
  AI Speech Enhancement: boost vocal clarity
  AI Thumbnail Creator: generate YouTube thumbnail suggestions
  AI Copywriting: generate script/caption suggestions
  Smart Cutout: remove background without green screen
  
Audio tools:
  Beat detection: markers at music beats for cutting
  Audio ducking: auto-lower music when speech detected
  Audio visualizer: animated waveform visuals
  
Export:
  1-click export presets for YouTube, TikTok, Vimeo, Instagram
  Export up to 4K 60fps (full version)
  Direct upload to YouTube/TikTok from app
```

### Interface Overview

```
Panel layout:
  Left panel: Media library (imported clips, audio, effects)
  Preview: Split view (original vs edited)
  Right panel: Properties (selected clip controls)
  Bottom: Timeline
  
Import: File → Import / drag to media bin
  Supports: MP4, MOV, MKV, AVI, MP3, WAV, PNG, JPG, PSD, GIF
  
Basic edit workflow:
  1. Import footage → drag to timeline
  2. Trim: drag clip edges, or split with Ctrl+B then delete
  3. Add music: drag audio track under video
  4. Add title: Titles tab → drag template to timeline
  5. Color grade: Effects → Color → drag LUT to clip
  6. Export: Export button → choose preset
```

---

## 6. CapCut Desktop

- **Website:** https://www.capcut.com
- **Price:** Free (with paid Pro features)
- **Platform:** Windows, macOS, iOS, Android, Web
- **Owner:** ByteDance (TikTok parent company)

### Overview

CapCut started as a mobile-first TikTok editor but now has a full desktop version with surprisingly powerful features — all free. It's the go-to choice for TikTok, Instagram Reels, and YouTube Shorts creators. The AI features (especially background removal and auto-captions) are best-in-class for free software.

### Desktop Features

```
Editing:
  Multi-track timeline (full NLE features)
  Keyframe animation for all properties
  Speed curves (speed ramping like Premiere)
  Freeze frame: pause-on-beat effects
  
AI Tools (free):
  Auto Captions: speech-to-text → animated captions (remarkably accurate)
    Multiple styles (TikTok, podcast, minimal, etc.)
    Edit individual words, change colors, fix errors
  Background Removal: 1-click remove background (no green screen needed)
    Works on video too — not just photos
  Smart Cutout: trace custom mask around subject
  AI Color Match: match color grading of reference video/image
  Text to Speech: 50+ voices, multiple languages
  Auto Reframe: 16:9 → 9:16 with AI subject tracking
  AI Music: generate original background music by mood/genre/duration
  Noise Reduction: background audio suppression
  Auto Beat Sync: cuts sync to music beats automatically
  AI Script: generate video scripts from topic prompt
  
Effects library:
  Transitions, filters, stickers, text templates
  All built-in, massive selection optimized for short-form content
  
Templates:
  Browse trending TikTok/Reels template styles
  Drop your footage into pre-animated template → done

Pro features (paid):
  Commercial license for Pro effects
  Unlimited cloud storage
  4K+ export
  More AI generation credits
  
Export:
  Up to 4K (free), up to 8K (Pro)
  TikTok/Instagram/YouTube direct export presets
  Custom bitrate settings
```

### Privacy Note

```
CapCut is owned by ByteDance (TikTok parent).
Data handling concerns are similar to TikTok's.
For professional commercial work: use DaVinci Resolve (free) instead.
For personal/content creator work: CapCut is fine.
Some countries have restricted or banned TikTok/ByteDance apps — check your local regulations.
```

---

## 7. Software Comparison

| Software | Best For | Price | Skill Level | Platform |
|----------|---------|-------|-------------|---------|
| **Blender** | 3D, VFX, animation | Free | Intermediate-Pro | All |
| **DaVinci Resolve** | Color grading, professional edit | Free / $295 | Beginner-Pro | All |
| **Photoshop** | Photo editing, compositing, AI art | $21/mo | Beginner-Pro | Win/Mac |
| **Premiere Pro** | Professional video editing | $22/mo | Intermediate-Pro | Win/Mac |
| **Filmora** | Easy video editing, YouTube | $50/yr | Beginner | Win/Mac/Mobile |
| **CapCut** | Short-form content, TikTok | Free | Beginner | All |

### By Use Case

```
3D modeling / animation:        Blender
Color grading:                  DaVinci Resolve (industry standard)
Professional video editing:     Premiere Pro (Windows/Mac) or DaVinci Resolve (all OS)
Photo editing / retouching:     Photoshop
Quick YouTube/social video:     Filmora or CapCut
TikTok / Reels:                 CapCut
Free professional video:        DaVinci Resolve
Open source everything:         Blender + Kdenlive/Shotcut (video) + GIMP (photo)

Free alternatives to Adobe:
  Photoshop → GIMP (feature-complete), Krita (painting/illustration)
  Premiere   → DaVinci Resolve (better color), Kdenlive (Linux), Shotcut
  After Effects → Blender (compositor/motion), DaVinci Fusion (included in Resolve)
  Illustrator → Inkscape
```

---

## See Also

- [CGI & VFX](../fundamentals/cgi-vfx.md) — 3D pipeline concepts, rendering theory, VFX production
- [Media Tools](media-tools.md) — FFmpeg, VLC for video processing and conversion
- [Mobile Creative Tools](mobile-creative-tools.md) — CapCut mobile, Alight Motion deep dive
- [GPU Architecture](../fundamentals/gpu-architecture.md) — GPU acceleration for rendering and video encode
- [Storage Technology](../fundamentals/storage-technology.md) — Fast storage for video editing
