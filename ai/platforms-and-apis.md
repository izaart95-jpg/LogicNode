# AI Platforms, APIs & Creative Tools

This document covers AI model hosting platforms, API aggregators, free inference endpoints, and AI-powered creative tools — essential for developers, researchers, and builders integrating AI into projects.

---

## Table of Contents
1. [API Aggregators & Routers](#1-api-aggregators--routers)
2. [Model Hosting & Inference](#2-model-hosting--inference)
3. [Free & Open Inference](#3-free--open-inference)
4. [AI Creative & Media Tools](#4-ai-creative--media-tools)
5. [Local AI Inference](#5-local-ai-inference)
6. [Comparison Table](#6-comparison-table)
7. [Pricing & Free Tier Summary](#7-pricing--free-tier-summary)
8. [Getting Started Examples](#8-getting-started-examples)

---

## 1. API Aggregators & Routers

These platforms provide a **single API endpoint** that routes requests to many different AI models and providers.

### 1.1 OpenRouter
- **Website:** https://openrouter.ai
- **What it is:** Unified API gateway to 200+ models from OpenAI, Anthropic, Google, Meta, Mistral, and open-source providers
- **Pricing:** Pay-per-token, varies by model. Some models are **free** (rate-limited)
- **API:** OpenAI-compatible (`/v1/chat/completions`)
- **Key Feature:** Single API key → access GPT-4o, Claude, Gemini, Llama, Mixtral, etc.

**Why use it:**
- Don't need separate accounts for every provider
- Automatic fallback between providers
- Compare models easily
- Some free models available (e.g., free Llama, Mistral variants)

```python
import requests

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_OPENROUTER_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "meta-llama/llama-3.1-70b-instruct:free",
        "messages": [{"role": "user", "content": "Hello!"}]
    }
)
print(response.json()["choices"][0]["message"]["content"])
```

**Free Models on OpenRouter (rate-limited):**
- `meta-llama/llama-3.1-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`
- `google/gemma-2-9b-it:free`
- `qwen/qwen-2.5-7b-instruct:free`
- Check current free models: https://openrouter.ai/models?q=free

---

### 1.2 g4f (GPT4Free)
- **Website:** https://g4f.ai / https://github.com/xtekky/gpt4free
- **What it is:** Open-source library that provides free access to AI models through reverse-engineered and public provider endpoints
- **Pricing:** Free
- **Language:** Python
- **Models:** GPT-4, GPT-3.5, Claude, Gemini, and others through various providers

> ⚠️ **Legal Notice:** g4f uses unofficial API endpoints. Reliability varies. Providers can break at any time. Not recommended for production use. Review terms of service for each provider.

```python
import g4f

response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response)
```

**Key Features:**
- No API key required for many providers
- OpenAI-compatible API server mode
- Web UI included
- Provider rotation and fallback

```bash
# Install
pip install g4f

# Run local API server (OpenAI-compatible)
g4f api

# Run web UI
g4f gui
```

---

## 2. Model Hosting & Inference

### 2.1 Hugging Face
- **Website:** https://huggingface.co
- **What it is:** The largest open-source AI model hub — hosting, training, datasets, and inference
- **Models:** 500,000+ models (text, image, audio, video, multimodal)
- **Free Tier:** Free Inference API (rate-limited), free model hosting, free Spaces

**Core Services:**

| Service | Description | Free? |
|---------|-------------|-------|
| **Hub** | Host and share models, datasets, Spaces | ✅ |
| **Inference API** | Run any hosted model via API | ✅ (rate-limited) |
| **Inference Endpoints** | Dedicated GPU inference | 💰 Pay-per-hour |
| **Spaces** | Host Gradio/Streamlit apps | ✅ (CPU), 💰 (GPU) |
| **Datasets** | 100,000+ datasets | ✅ |
| **Transformers** | Python library for model loading | ✅ Open source |
| **GGUF/GPTQ/AWQ Models** | Quantized models for local inference | ✅ |

```python
# Free Inference API
from huggingface_hub import InferenceClient

client = InferenceClient(token="hf_YOUR_TOKEN")
response = client.text_generation(
    "Explain quantum computing",
    model="meta-llama/Llama-3.1-8B-Instruct"
)
print(response)
```

```bash
# Download a model
pip install huggingface_hub
huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf
```

**Why it matters:** Hugging Face is the GitHub of AI. Most open-source models are hosted here. If you work with AI, you will use Hugging Face.

---

### 2.2 Replicate
- **Website:** https://replicate.com
- **What it is:** Run open-source AI models in the cloud via simple API
- **Pricing:** Pay-per-second of compute
- **Models:** Llama, Stable Diffusion, Whisper, and thousands more
- **API:** REST + Python/JS SDKs

```python
import replicate

output = replicate.run(
    "meta/llama-2-70b-chat",
    input={"prompt": "What is quantum computing?"}
)
print(output)
```

---

### 2.3 Together AI
- **Website:** https://www.together.ai
- **What it is:** Fast inference and fine-tuning for open-source models
- **Free Tier:** $1 free credit on signup
- **Models:** Llama, Mixtral, Qwen, Code Llama, and more
- **API:** OpenAI-compatible

---

### 2.4 Groq
- **Website:** https://groq.com
- **What it is:** Ultra-fast inference using custom LPU (Language Processing Unit) hardware
- **Free Tier:** Free API access (rate-limited)
- **Speed:** Fastest available inference (500+ tokens/sec for Llama 3)
- **API:** OpenAI-compatible

```python
from groq import Groq

client = Groq(api_key="YOUR_KEY")
response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

### 2.5 Fireworks AI
- **Website:** https://fireworks.ai
- **What it is:** Fast inference platform for open models
- **Free Tier:** Free credits on signup
- **API:** OpenAI-compatible
- **Models:** Llama, Mixtral, Qwen, function-calling models

---

### 2.6 Cerebras
- **Website:** https://cerebras.ai
- **What it is:** AI inference on custom wafer-scale chips
- **Free Tier:** Free API (rate-limited)
- **Speed:** Extremely fast inference (competes with Groq)
- **API:** OpenAI-compatible

---

## 3. Free & Open Inference

### 3.1 Pollinations AI
- **Website:** https://pollinations.ai
- **What it is:** Free, open-source AI generation platform — text, images, audio, code
- **Pricing:** Completely free, no API key required
- **API:** REST endpoints, no auth needed

**Text Generation:**
```bash
curl "https://text.pollinations.ai/What%20is%20Linux?"
```

**Image Generation:**
```bash
# Returns image directly
curl "https://image.pollinations.ai/prompt/A%20cyberpunk%20city" --output image.jpg
```

**Key Features:**
- No API key, no signup, no rate limits (fair use)
- Text, image, and code generation
- OpenAI-compatible chat endpoint
- Great for prototyping and education

```python
import requests

# Text
response = requests.get("https://text.pollinations.ai/Explain DNS in one paragraph")
print(response.text)

# Image (returns PNG)
img = requests.get("https://image.pollinations.ai/prompt/A%20futuristic%20server%20room")
with open("output.png", "wb") as f:
    f.write(img.content)
```

---

### 3.2 Hugging Face Inference API
- Free tier with rate limits
- Access to thousands of models
- See section 2.1 above

---

### 3.3 Google AI Studio (Gemini)
- **Website:** https://aistudio.google.com
- **Free Tier:** Free Gemini API access (rate-limited)
- **Models:** Gemini 1.5 Flash, Gemini 1.5 Pro
- **API:** Google AI SDK + OpenAI-compatible

---

## 4. AI Creative & Media Tools

### 4.1 Runway ML
- **Website:** https://runwayml.com
- **What it is:** AI-powered creative suite for video, image, and media generation
- **Key Product:** **Gen-3 Alpha** — text-to-video and image-to-video generation

**Features:**
| Tool | Function |
|------|----------|
| **Gen-3 Alpha** | Text/image to video generation |
| **Inpainting** | Remove/replace objects in images |
| **Motion Brush** | Add motion to static images |
| **Super Slow Motion** | AI frame interpolation |
| **Background Removal** | Automatic subject isolation |
| **Text to Image** | Generate images from prompts |
| **Upscaling** | AI image resolution enhancement |
| **Audio Cleanup** | Remove background noise |

**Pricing:**
- Free Tier: 125 credits (limited generation)
- Basic: $12/month (625 credits)
- Standard: $28/month (2250 credits)

**Use Cases:**
- Film and video production
- Content creation
- Social media
- Advertising
- Art and design

---

### 4.2 Stability AI
- **Website:** https://stability.ai
- **Products:** Stable Diffusion (image), Stable Video Diffusion, Stable Audio
- **Open Source:** Core models are open-weight
- **API:** https://platform.stability.ai
- **Free Tier:** Free credits on signup

---

### 4.3 ElevenLabs
- **Website:** https://elevenlabs.io
- **What it is:** AI voice synthesis and cloning
- **Free Tier:** 10,000 characters/month
- **Features:** Text-to-speech, voice cloning, audio dubbing

---

### 4.4 Suno AI
- **Website:** https://suno.com
- **What it is:** AI music generation
- **Free Tier:** 10 songs/day
- **Features:** Text-to-music, lyrics generation

---

### 4.5 Leonardo AI
- **Website:** https://leonardo.ai
- **What it is:** AI image generation platform
- **Free Tier:** 150 tokens/day
- **Features:** Image generation, fine-tuning, canvas editor

---

### 4.6 Ideogram
- **Website:** https://ideogram.ai
- **What it is:** AI image generation (strong text rendering)
- **Free Tier:** Free daily generations
- **Strength:** Best at rendering text within images

---

### 4.7 Flux (by Black Forest Labs)
- **Website:** https://blackforestlabs.ai
- **What it is:** Open-weight image generation model
- **Models:** FLUX.1 [dev], FLUX.1 [schnell], FLUX.1 [pro]
- **Free:** Dev and Schnell models are open
- **Available on:** Hugging Face, Replicate, ComfyUI

---

### 4.8 Kling AI
- **Website:** https://klingai.com
- **What it is:** Text/image to video generation (by Kuaishou)
- **Free Tier:** Free daily credits
- **Strength:** High-quality video generation

---

## 5. Local AI Inference

Tools for running AI models on your own hardware.

### 5.1 Ollama
- **Website:** https://ollama.com
- **What it is:** Run LLMs locally with a single command
- **Platform:** macOS, Linux, Windows
- **API:** OpenAI-compatible (`/v1/chat/completions`)

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Download and run models
ollama pull llama3.1
ollama pull mistral
ollama pull qwen2.5
ollama pull codellama
ollama pull gemma2

# Run interactively
ollama run llama3.1

# Serve API
ollama serve
# API available at http://localhost:11434

# List models
ollama list

# API usage
curl http://localhost:11434/v1/chat/completions \
  -d '{
    "model": "llama3.1",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

**Model Library:** https://ollama.com/library
- Llama 3.1, Mistral, Qwen 2.5, Gemma 2, CodeLlama, Phi-3, DeepSeek, StarCoder, and 100+ more

---

### 5.2 llama.cpp
- **Repository:** https://github.com/ggerganov/llama.cpp
- **What it is:** High-performance C/C++ inference engine for LLMs
- **Format:** GGUF (quantized models)
- **Platform:** CPU (any), GPU (CUDA, Metal, Vulkan, ROCm, SYCL)
- **Key Feature:** Runs models on consumer hardware, from phones to servers

```bash
# Build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release

# Run model
./build/bin/llama-cli \
  -m models/llama-3.1-8b-q4_k_m.gguf \
  -p "Explain Linux in simple terms" \
  -n 256

# Run server (OpenAI-compatible API)
./build/bin/llama-server \
  -m models/llama-3.1-8b-q4_k_m.gguf \
  --host 0.0.0.0 --port 8080
```

**Quantization Levels:**
| Quantization | Size Reduction | Quality | Speed |
|-------------|---------------|---------|-------|
| Q8_0 | ~50% | Excellent | Moderate |
| Q6_K | ~60% | Very Good | Good |
| Q5_K_M | ~65% | Good | Good |
| Q4_K_M | ~70% | Good | Fast |
| Q3_K_M | ~75% | Decent | Fast |
| Q2_K | ~80% | Low | Fastest |

**Recommendation:** Q4_K_M offers the best balance of quality and speed for most users.

---

### 5.3 LM Studio
- **Website:** https://lmstudio.ai
- **What it is:** Desktop GUI for downloading and running LLMs locally
- **Platform:** macOS, Linux, Windows
- **Features:** Model browser (Hugging Face), chat UI, local server
- **API:** OpenAI-compatible
- **Best for:** Users who want a GUI experience

---

### 5.4 LocalAI
- **Website:** https://localai.io
- **Repository:** https://github.com/mudler/LocalAI
- **What it is:** Drop-in OpenAI API replacement, runs locally
- **Features:** Text, image, audio, embeddings — all local
- **API:** OpenAI-compatible

---

### 5.5 vLLM
- **Repository:** https://github.com/vllm-project/vllm
- **What it is:** High-throughput LLM serving engine
- **Key Feature:** PagedAttention for efficient memory management
- **Best for:** Production deployments, high-concurrency serving
- **API:** OpenAI-compatible

---

### 5.6 Jan
- **Website:** https://jan.ai
- **What it is:** Open-source alternative to ChatGPT that runs fully offline
- **Platform:** macOS, Linux, Windows
- **Features:** Chat UI, model management, local API, extensions

---

## 6. Comparison Table

### API Providers & Aggregators

| Platform | Free Tier | Models | API Compatible | Best For |
|----------|-----------|--------|---------------|----------|
| **OpenRouter** | Some free models | 200+ | OpenAI | Multi-provider access |
| **g4f** | Free | Many | OpenAI | Experimentation |
| **Hugging Face** | Rate-limited API | 500K+ | HF / OpenAI | Open-source models |
| **Groq** | Rate-limited | ~20 | OpenAI | Speed |
| **Cerebras** | Rate-limited | ~10 | OpenAI | Speed |
| **Together AI** | $1 credit | 100+ | OpenAI | Open model fine-tuning |
| **Fireworks AI** | Free credits | 50+ | OpenAI | Fast open model serving |
| **Pollinations** | Fully free | Several | REST | No-key prototyping |
| **Replicate** | Pay-per-second | 1000+ | REST | Run any model |
| **Google AI Studio** | Rate-limited | Gemini | Google / OpenAI | Gemini access |

### Local Inference

| Tool | GUI | API | GPU Required | Best For |
|------|-----|-----|-------------|----------|
| **Ollama** | No (CLI) | OpenAI-compat | Optional | Easy local LLMs |
| **llama.cpp** | No (CLI) | OpenAI-compat | Optional | Maximum performance |
| **LM Studio** | Yes | OpenAI-compat | Optional | Desktop users |
| **LocalAI** | No | OpenAI-compat | Optional | Self-hosted API |
| **Jan** | Yes | OpenAI-compat | Optional | Offline ChatGPT |
| **vLLM** | No | OpenAI-compat | Yes (GPU) | Production serving |

### Creative AI Tools

| Platform | Type | Free Tier | Strength |
|----------|------|-----------|----------|
| **Runway ML** | Video/Image | 125 credits | Best text-to-video |
| **Stability AI** | Image/Video/Audio | Free credits | Open-weight models |
| **ElevenLabs** | Voice | 10K chars/mo | Voice cloning |
| **Suno** | Music | 10 songs/day | Text-to-music |
| **Leonardo AI** | Image | 150 tokens/day | Image generation |
| **Ideogram** | Image | Free daily | Text in images |
| **Flux** | Image | Open models | Open-weight quality |
| **Kling AI** | Video | Free credits | Video generation |
| **Pollinations** | Text/Image | Unlimited | Zero-friction |

---

## 7. Pricing & Free Tier Summary

### Completely Free (No Payment Required)
- **Pollinations AI** — text + image generation, no key needed
- **g4f** — open-source, community providers
- **DuckDuckGo AI Chat** — free, private (limited models)
- **Hugging Face Inference API** — rate-limited
- **Groq** — rate-limited free tier
- **Cerebras** — rate-limited free tier
- **Ollama / llama.cpp** — run on your hardware

### Free Credits on Signup
- **Together AI** — $1 credit
- **Fireworks AI** — free credits
- **Replicate** — free credits
- **Stability AI** — free credits
- **Google AI Studio** — generous free tier

### Pay-Per-Use (No Subscription)
- **OpenRouter** — pay per token
- **Replicate** — pay per second

---

## 8. Getting Started Examples

### Fastest Free Text Generation (No Key)
```bash
# Pollinations — zero setup
curl "https://text.pollinations.ai/What%20is%20a%20kernel?"
```

### Fastest Free Image Generation (No Key)
```bash
curl "https://image.pollinations.ai/prompt/A%20hacker%20terminal%20with%20green%20text" -o image.jpg
```

### Fastest Local Setup
```bash
# Ollama — one command
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama3.1
```

### OpenRouter Multi-Model Access
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## See Also

- [AI Chat Interfaces](chat-interfaces.md) — ChatGPT, Claude, DeepSeek, Kimi, and self-hosted UIs
- [Network Protocols](../fundamentals/network-protocols.md) — HTTP/REST/gRPC protocols used by AI APIs
