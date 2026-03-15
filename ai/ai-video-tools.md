# AI Video Tools — Deep-Live-Cam & RuView

This document covers AI-powered video analysis and manipulation tools — real-time face swapping for content creation and AI-assisted video review systems.

> **Ethical Notice:** Real-time face swap and deepfake technologies carry significant ethical responsibilities. Creating content that impersonates real people without consent, spreads misinformation, or constitutes harassment is harmful and in many jurisdictions illegal. Use these tools for legitimate creative, research, and entertainment purposes only. Always disclose AI-generated content.

---

## Table of Contents
1. [Deep-Live-Cam](#1-deep-live-cam)
2. [RuView](#2-ruview)
3. [Related Tools](#3-related-tools)

---

## 1. Deep-Live-Cam

- **Repository:** https://github.com/hacksider/Deep-Live-Cam
- **License:** Custom (non-commercial use)
- **Stars:** 45,000+
- **Language:** Python
- **Purpose:** Real-time face swap on webcam feed and video files using a single source image

### Overview

Deep-Live-Cam performs real-time face replacement using a single reference photo. Unlike older deepfake methods requiring large training datasets, it uses **inswapper** (InsightFace) to swap faces in a single inference step — making it usable live on a webcam without GPU training.

### Key Features

- **Single image source:** One photo of the target face is all that's needed
- **Real-time processing:** Works on live webcam at ~10–30 FPS depending on hardware
- **Video file processing:** Process pre-recorded video files frame by frame
- **GPU acceleration:** CUDA (NVIDIA), CoreML (Apple Silicon), DirectML (Windows GPU)
- **Face detection:** Automatically detects and replaces faces in frame
- **Mouth mask:** Preserves natural mouth movements for more realistic results
- **Many faces mode:** Swap all detected faces simultaneously

### Requirements

```
Python 3.10
GPU strongly recommended:
  NVIDIA: CUDA 11.8+ with cuDNN
  Apple Silicon: CoreML backend
  CPU: Works but very slow (~2 FPS)
RAM: 8 GB minimum, 16 GB recommended
VRAM: 4 GB+ for GPU processing
```

### Installation

```bash
# Clone repository
git clone https://github.com/hacksider/Deep-Live-Cam.git
cd Deep-Live-Cam

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Download required models (auto on first run, or manually):
# Models download to: ./models/
# inswapper_128_fp16.onnx (~256 MB)
# GFPGANv1.4.pth (~332 MB) — face enhancement
```

### Running

```bash
# Launch with GUI
python run.py

# GUI steps:
# 1. Click "Select a face" → choose your source image (one clear face photo)
# 2. Click "Select a target" → choose target video or webcam
# 3. For webcam: select your camera device from dropdown
# 4. Click "Live" to start real-time preview
# 5. Adjust settings (mouth mask, face enhancer, etc.)

# Headless / CLI mode
python run.py \
  --source path/to/source_face.jpg \
  --target path/to/target_video.mp4 \
  --output path/to/output.mp4 \
  --frame-processor face_swapper face_enhancer

# Webcam to virtual camera output (for streaming/video calls)
python run.py \
  --source face.jpg \
  --target 0 \                      # 0 = first webcam
  --output-video-name output.mp4    # Also streams to virtual cam if configured
```

### CLI Options

```bash
python run.py --help

# Key flags:
--source SOURCE           # Source face image path
--target TARGET           # Target video/image path or webcam index (0, 1, 2...)
--output OUTPUT           # Output path
--frame-processor         # face_swapper, face_enhancer (can combine both)
--keep-fps                # Match output FPS to input
--keep-frames             # Keep extracted frames after processing
--skip-audio              # Drop audio from output
--many-faces              # Process all faces in frame, not just the first
--mouth-mask              # Preserve original mouth region
--video-encoder           # libx264, libx265, libvpx-vp9
--video-quality           # 0–51 (CRF, lower = better quality)
--max-memory              # Limit VRAM usage in GB
--execution-provider      # cuda, coreml, directml, cpu
--execution-threads       # Number of parallel threads
```

### GPU Setup

```bash
# NVIDIA CUDA
pip uninstall onnxruntime
pip install onnxruntime-gpu

# Run with CUDA
python run.py --execution-provider cuda ...

# Apple Silicon (CoreML)
pip uninstall onnxruntime
pip install onnxruntime-silicon

python run.py --execution-provider coreml ...

# Check available providers
python -c "import onnxruntime; print(onnxruntime.get_available_providers())"
```

### Virtual Camera Integration (for Video Calls)

To use Deep-Live-Cam output as a webcam in Zoom, Teams, OBS, or browsers:

```bash
# Linux: Install v4l2loopback
sudo apt install v4l2loopback-dkms
sudo modprobe v4l2loopback

# macOS: Install OBS Virtual Camera or CamTwist
# Windows: OBS Virtual Camera or ManyCam

# Then pipe Deep-Live-Cam output to the virtual camera device
# OBS approach: run Deep-Live-Cam in window → window capture in OBS → OBS Virtual Camera
```

### Performance Benchmarks (approximate)

| Hardware | FPS (Real-time) |
|----------|----------------|
| NVIDIA RTX 4090 | ~30 FPS |
| NVIDIA RTX 3080 | ~20 FPS |
| NVIDIA RTX 3060 | ~12 FPS |
| Apple M2 Pro | ~15 FPS |
| Apple M1 | ~8 FPS |
| CPU only | 1–3 FPS |

---

## 2. RuView

- **Repository:** https://github.com/ruvnet/RuView
- **Author:** ruvnet
- **Language:** Python
- **Purpose:** AI-powered video analysis — automated scene understanding, object detection, content summarization, and review generation from video files

### Overview

RuView uses vision AI models to analyze video content and generate structured descriptions, summaries, and reviews. It processes video frames through large language models and computer vision systems to produce human-readable analysis of video content.

### Key Features

- **Scene analysis:** Automatically identifies and describes scenes in video
- **Content summarization:** Generates text summaries of video content
- **Object and action detection:** Identifies objects, people, and actions in frames
- **Review generation:** Produces structured reviews of content using LLM
- **Batch processing:** Analyze multiple videos programmatically
- **Configurable frame sampling:** Control how many frames per second are analyzed

### Installation

```bash
# Clone
git clone https://github.com/ruvnet/RuView.git
cd RuView

# Install dependencies
pip install -r requirements.txt

# Configure API keys (RuView uses OpenAI Vision API by default)
cp .env.example .env
# Edit .env:
# OPENAI_API_KEY=sk-...
```

### Basic Usage

```bash
# Analyze a video file
python ruview.py --video path/to/video.mp4

# With specific output format
python ruview.py \
  --video path/to/video.mp4 \
  --output review.md \
  --format markdown

# Control frame sampling rate
python ruview.py \
  --video path/to/video.mp4 \
  --fps 1             # Analyze 1 frame per second
  --max-frames 100    # Cap at 100 frames total
```

### Python API

```python
from ruview import VideoAnalyzer

analyzer = VideoAnalyzer(api_key="your_openai_key")

# Analyze video
result = analyzer.analyze(
    video_path="video.mp4",
    sample_rate=1,           # 1 frame per second
    generate_summary=True,
    generate_review=True
)

print(result.summary)      # Text summary of the video
print(result.scenes)       # List of detected scene descriptions
print(result.review)       # Full AI-generated review
print(result.objects)      # Detected objects and people

# Save results
result.save("analysis.json")
```

### Use Cases

- **Content moderation:** Automatically screen uploaded videos for policy violations
- **Video indexing:** Generate searchable metadata from video archives
- **Accessibility:** Auto-generate descriptions for video content
- **Research:** Analyze large video datasets without watching each one
- **Content review workflows:** First-pass automated review before human review

### Supported Models

RuView supports multiple vision backends:

```python
# OpenAI GPT-4 Vision (default)
analyzer = VideoAnalyzer(model="gpt-4-vision-preview")

# Claude claude-sonnet-4-20250514 Vision
analyzer = VideoAnalyzer(
    model="claude-sonnet-4-20250514",
    provider="anthropic",
    api_key="sk-ant-..."
)

# Local model via Ollama (llava)
analyzer = VideoAnalyzer(
    model="llava",
    provider="ollama",
    base_url="http://localhost:11434"
)
```

---

## 3. Related Tools

### Other Face Swap / Deepfake Tools

| Tool | Repo | Type | GPU Required |
|------|------|------|-------------|
| **Deep-Live-Cam** | hacksider/Deep-Live-Cam | Real-time webcam | Recommended |
| **Rope** | Hillobar/Rope | Video file processing | Yes |
| **FaceFusion** | facefusion/facefusion | Advanced, multi-face | Yes |
| **SimSwap** | neuralchen/SimSwap | Research-grade | Yes |

### Other AI Video Analysis Tools

| Tool | Purpose |
|------|---------|
| **Twelve Labs** | Video understanding API (commercial) |
| **AssemblyAI** | Video transcription + analysis |
| **AWS Rekognition Video** | Object/face detection in video |
| **Google Video Intelligence** | Scene detection, label detection |

---

## See Also

- [Platforms & APIs](platforms-and-apis.md) — Ollama, Replicate, and AI inference platforms
- [Chat Interfaces](chat-interfaces.md) — GPT-4, Claude Vision for image/video analysis
- [Web Automation](../automation/web-automation.md) — Browser automation that complements video tools
- [Media Tools](../media/media-tools.md) — FFmpeg for video processing and format conversion
