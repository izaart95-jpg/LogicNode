# Media Processing Tools

A comprehensive guide to essential open-source media processing tools for video, audio, and image manipulation. This document covers FFmpeg for multimedia conversion and streaming, VLC for playback and transcoding, and GIMP for image editing, providing practical commands and workflows for each.

---

## Table of Contents

1. [Media Processing Overview](#1-media-processing-overview)
2. [FFmpeg](#2-ffmpeg)
3. [VLC Media Player](#3-vlc-media-player)
4. [GIMP (GNU Image Manipulation Program)](#4-gimp-gnu-image-manipulation-program)
5. [Comparison Table](#5-comparison-table)

---

## 1. Media Processing Overview

### 1.1 Codecs, Containers, and Formats

Understanding media processing starts with three core concepts:

- **Codec** (coder-decoder): The algorithm that compresses and decompresses media data. Examples: H.264, H.265 (HEVC), VP9, AV1 for video; AAC, MP3, Opus, FLAC for audio.
- **Container**: The file format that wraps encoded streams together. Examples: MP4 (.mp4), Matroska (.mkv), WebM (.webm), AVI (.avi), MOV (.mov).
- **Format**: Often used interchangeably with container, but can also refer to the overall specification including codec and container pairing.

A single container can hold multiple streams: video, audio, subtitles, and metadata.

### 1.2 Encoding vs Decoding vs Transcoding

- **Encoding**: Converting raw media into a compressed format using a codec (e.g., raw video to H.264).
- **Decoding**: Reversing the process, decompressing encoded media for playback or editing.
- **Transcoding**: Decoding from one codec and re-encoding into another (e.g., H.264 to H.265). This is the most common operation when converting between formats.
- **Remuxing**: Changing the container without re-encoding the streams (fast, lossless).

### 1.3 Common Quality Concepts

- **Bitrate**: Amount of data per second (higher = better quality, larger file).
- **CRF (Constant Rate Factor)**: Quality-based encoding where the encoder targets a perceptual quality level (lower = better quality).
- **Resolution**: Pixel dimensions (1920x1080, 3840x2160, etc.).
- **Frame rate**: Frames per second (24, 30, 60 fps).

---

## 2. FFmpeg

FFmpeg is the universal multimedia Swiss Army knife. It is a complete, cross-platform solution for recording, converting, and streaming audio and video.

- **Website**: https://ffmpeg.org
- **License**: LGPL / GPL
- **Platforms**: Linux, macOS, Windows, BSD

### 2.1 Installation

```bash
# Debian / Ubuntu
sudo apt install ffmpeg

# macOS (Homebrew)
brew install ffmpeg

# Windows (winget)
winget install ffmpeg

# Verify installation
ffmpeg -version
```

### 2.2 Core Concepts

FFmpeg operates on a pipeline model: **input -> decode -> filter -> encode -> output**.

- **Input** (`-i`): Source file or stream.
- **Output**: Destination file, stream, or device.
- **Codecs** (`-c:v` for video, `-c:a` for audio): Specify encoder/decoder.
- **Containers**: Determined by output file extension.
- **Filters** (`-vf` for video, `-af` for audio): Processing chains applied between decode and encode.

### 2.3 Essential Commands

```bash
# Convert format (MP4 to AVI)
ffmpeg -i input.mp4 output.avi

# Extract audio from video
ffmpeg -i video.mp4 -vn -acodec copy audio.aac

# Resize video to 720p
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4

# Compress video with CRF (lower = better quality, 18-28 typical range)
ffmpeg -i input.mp4 -crf 23 -preset medium output.mp4

# Create GIF from video
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" output.gif

# Concatenate files from a list
ffmpeg -f concat -i filelist.txt -c copy output.mp4

# Stream to RTMP server
ffmpeg -re -i input.mp4 -c copy -f flv rtmp://server/live/key

# Screen recording on Linux (X11)
ffmpeg -f x11grab -s 1920x1080 -i :0.0 output.mp4

# Cut/trim a clip (start at 1:00, duration 30 seconds)
ffmpeg -i input.mp4 -ss 00:01:00 -t 00:00:30 -c copy clip.mp4

# Extract frames as images
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.png

# Add subtitles (burn-in)
ffmpeg -i input.mp4 -vf "subtitles=subs.srt" output.mp4

# Two-pass encoding for target bitrate
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 output.mp4
```

### 2.4 Filters

FFmpeg has a powerful filter system for processing media streams:

- **scale**: Resize video (`-vf scale=1280:720`)
- **crop**: Crop video region (`-vf crop=640:480:100:50`)
- **overlay**: Overlay one video on another (picture-in-picture, watermarks)
- **drawtext**: Burn text onto video (`-vf "drawtext=text='Hello':fontsize=24:x=10:y=10"`)
- **eq**: Adjust brightness, contrast, saturation (`-vf eq=brightness=0.06:contrast=1.5`)
- **hue**: Adjust hue and saturation (`-vf hue=h=90:s=1`)
- **deinterlace**: Use `yadif` filter for interlaced sources (`-vf yadif`)
- **denoise**: Use `hqdn3d` or `nlmeans` for noise reduction

Filters can be chained with commas: `-vf "scale=1280:720,eq=brightness=0.1,drawtext=text='Test'"`.

### 2.5 Hardware Acceleration

FFmpeg supports GPU-accelerated encoding and decoding:

- **NVIDIA NVENC/NVDEC**: `-c:v h264_nvenc` (requires NVIDIA GPU + drivers)
- **Intel VAAPI**: `-vaapi_device /dev/dri/renderD128 -c:v h264_vaapi` (Linux)
- **Intel QSV**: `-c:v h264_qsv` (Quick Sync Video)
- **Apple VideoToolbox**: `-c:v h264_videotoolbox` (macOS)
- **AMD AMF**: `-c:v h264_amf` (Windows)

```bash
# NVIDIA NVENC encoding example
ffmpeg -i input.mp4 -c:v h264_nvenc -preset fast -cq 23 output.mp4

# VAAPI encoding example (Linux)
ffmpeg -vaapi_device /dev/dri/renderD128 -i input.mp4 \
  -vf 'format=nv12,hwupload' -c:v h264_vaapi output.mp4
```

### 2.6 Batch Processing

```bash
# Batch convert all MKV files to MP4
for f in *.mkv; do
  ffmpeg -i "$f" -c:v libx264 -crf 23 "${f%.mkv}.mp4"
done

# Batch extract audio from videos
for f in *.mp4; do
  ffmpeg -i "$f" -vn -acodec libmp3lame -q:a 2 "${f%.mp4}.mp3"
done

# Batch resize images
for f in *.png; do
  ffmpeg -i "$f" -vf scale=800:-1 "resized_$f"
done
```

---

## 3. VLC Media Player

VLC is a free and open-source cross-platform multimedia player and framework that plays most multimedia files as well as DVDs, Audio CDs, VCDs, and various streaming protocols.

- **Website**: https://www.videolan.org/vlc/
- **License**: GPL v2
- **Platforms**: Windows, macOS, Linux, Android, iOS

### 3.1 Key Features

- Plays virtually any audio/video format without installing extra codecs
- Built-in codec library (libavcodec, libavformat)
- Streaming support: HTTP, RTSP, RTP, MMS, HLS, DASH
- Transcoding and format conversion
- Subtitle support (SRT, ASS, SSA, embedded)
- Customizable skins and interface
- Extensions and plugin system
- No ads, no tracking, no spyware

### 3.2 CLI Usage

VLC provides a powerful command-line interface (`cvlc` for headless operation):

```bash
# Play a media file
vlc video.mp4

# Play without GUI (command line only)
cvlc audio.mp3

# Stream a file via HTTP
vlc input.mp4 --sout '#standard{access=http,mux=ts,dst=:8080}'

# Convert format (headless)
vlc -I dummy input.mp4 --sout '#transcode{vcodec=h264}:standard{access=file,dst=output.mp4}' vlc://quit

# Record screen on Linux
vlc screen:// --sout '#transcode{vcodec=h264}:standard{dst=recording.mp4}'

# Play a network stream
vlc rtsp://example.com/stream

# Play with specific subtitle file
vlc video.mp4 --sub-file subs.srt

# Loop playback
vlc --loop video.mp4
```

### 3.3 VLC as a Streaming Server

VLC can serve as a lightweight streaming server for local network distribution:

1. Open VLC and go to **Media > Stream**.
2. Add input source (file or capture device).
3. Select destination (HTTP, RTP, RTSP).
4. Configure transcoding options as needed.
5. Clients connect via `http://server-ip:port/`.

This is useful for quick ad-hoc streaming without setting up a dedicated media server.

### 3.4 Playlist and Media Library

- Supports M3U, XSPF, and PLS playlist formats
- Media library scans and indexes local media
- Metadata retrieval (album art, tags)
- Bookmarks for resuming playback

### 3.5 Extensions and Plugins

- VLC extensions are written in Lua
- Install from: https://addons.videolan.org
- Common extensions: subtitle downloaders, playlist parsers, streaming service integrations
- Custom interface skins available (VLC Skin Editor)

---

## 4. GIMP (GNU Image Manipulation Program)

GIMP is a free and open-source raster image editor used for image manipulation, retouching, editing, free-form drawing, and more. It is often considered the primary open-source alternative to Adobe Photoshop.

- **Website**: https://www.gimp.org
- **License**: GPL v3
- **Platforms**: Linux, macOS, Windows

### 4.1 Installation

```bash
# Debian / Ubuntu
sudo apt install gimp

# macOS (Homebrew)
brew install --cask gimp

# Fedora
sudo dnf install gimp

# Flatpak (cross-distribution)
flatpak install flathub org.gimp.GIMP
```

### 4.2 Core Tools

- **Selection tools**: Rectangle, ellipse, free select (lasso), fuzzy select (magic wand), by color, scissors (intelligent edges)
- **Paint tools**: Pencil, paintbrush, airbrush, ink, clone, heal, perspective clone
- **Transform tools**: Move, rotate, scale, shear, perspective, flip, cage transform, warp
- **Color tools**: Color balance, curves, levels, brightness-contrast, hue-saturation, threshold, posterize

### 4.3 Key Features

- **Layer-based editing with masks**: Non-destructive workflow using layer groups, blend modes, and layer masks for selective visibility.
- **Filters and effects**: Blur (Gaussian, motion, pixelize), sharpen (unsharp mask), distort (ripple, whirl, lens distortion), light effects (lens flare, lighting).
- **Color management**: ICC profile support, curves, levels, histograms, color picker.
- **Path tool**: Create and edit vector paths (Bezier curves) within GIMP for precise selections and shapes.
- **Plugin support**: Extensible through Script-Fu, Python-Fu, and third-party plugins.
- **File format support**: PSD, TIFF, PNG, JPEG, GIF, BMP, WebP, SVG, PDF, RAW (via UFRaw/darktable), and many more.

### 4.4 Scripting

GIMP supports two built-in scripting languages for automation:

**Script-Fu** (Scheme-based): Access via **Filters > Script-Fu > Console**.

**Python-Fu**: Access via **Filters > Python-Fu > Console**.

```python
# Python-Fu: batch resize images
import glob, os
for f in glob.glob("/path/to/images/*.jpg"):
    img = pdb.gimp_file_load(f, f)
    pdb.gimp_image_scale_full(img, 800, 600, INTERPOLATION_CUBIC)
    pdb.gimp_file_overwrite(img, img.active_drawable, f, f)
    pdb.gimp_image_delete(img)
```

```python
# Python-Fu: batch convert PNG to JPEG
import glob
for f in glob.glob("/path/to/images/*.png"):
    img = pdb.gimp_file_load(f, f)
    out = f.replace(".png", ".jpg")
    pdb.file_jpeg_save(img, img.active_drawable, out, out, 0.85, 0, 0, 0, "", 0, 0, 0, 2)
    pdb.gimp_image_delete(img)
```

### 4.5 GIMP vs Photoshop

| Feature | GIMP | Photoshop |
|---------|------|-----------|
| Price | Free (open source) | Subscription (~$20/month) |
| Platform | Linux, macOS, Windows | macOS, Windows |
| Non-destructive editing | Limited (via layers/masks) | Full (smart objects, adjustment layers) |
| RAW support | Via plugins (darktable, UFRaw) | Built-in (Camera RAW) |
| CMYK support | Limited (via plugin) | Full native support |
| Scripting | Script-Fu, Python-Fu | JavaScript, ExtendScript |
| Plugin ecosystem | G'MIC, Resynthesizer, community plugins | Vast commercial ecosystem |
| Performance (large files) | Moderate | Optimized |
| Learning resources | Community-driven | Extensive official + third-party |
| PSD compatibility | Partial (import/export) | Native |

### 4.6 Useful Plugins

- **G'MIC**: Massive collection of 500+ image processing filters and effects. Install from https://gmic.eu.
- **Resynthesizer**: Content-aware fill, texture synthesis, and smart removal of objects. Similar to Photoshop's Content-Aware Fill.
- **BIMP (Batch Image Manipulation Plugin)**: GUI-based batch processing for common operations.
- **Liquid Rescale**: Content-aware image resizing (seam carving).

---

## 5. Comparison Table

| Tool | Type | Open Source | Platform | Best For |
|------|------|-------------|----------|----------|
| FFmpeg | CLI multimedia framework | Yes (GPL/LGPL) | Linux, macOS, Windows | Video/audio conversion, streaming, batch processing |
| VLC | Media player + transcoder | Yes (GPL v2) | Linux, macOS, Windows, mobile | Universal playback, quick transcoding, streaming |
| GIMP | Image editor | Yes (GPL v3) | Linux, macOS, Windows | Photo editing, retouching, graphic design |

---

## See Also

- [media/mobile-creative-tools.md](mobile-creative-tools.md) - CapCut, Alight Motion, and mobile creative applications
