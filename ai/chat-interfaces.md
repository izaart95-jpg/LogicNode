# AI Chat Interfaces & Assistants

This document covers AI chat platforms — commercial assistants, free web interfaces, prompt engineering tools, and self-hosted chat UIs for running your own private AI.

---

## Table of Contents
1. [Commercial AI Assistants](#1-commercial-ai-assistants)
2. [Free & Open AI Chat Platforms](#2-free--open-ai-chat-platforms)
3. [Prompt Engineering & Community Platforms](#3-prompt-engineering--community-platforms)
4. [Self-Hosted Chat UIs](#4-self-hosted-chat-uis)
5. [Comparison Table](#5-comparison-table)
6. [Which Should You Use?](#6-which-should-you-use)

---

## 1. Commercial AI Assistants

### 1.1 ChatGPT (OpenAI)
- **Website:** https://chatgpt.com
- **Company:** OpenAI
- **Models:** GPT-4o, GPT-4o mini, o1, o3
- **Free Tier:** GPT-4o mini (unlimited), GPT-4o (rate-limited)
- **Paid:** Plus ($20/mo), Pro ($200/mo)

**Key Features:**
- Text, image, and file analysis
- Code interpreter (runs Python in sandbox)
- DALL·E image generation
- Web browsing
- Custom GPTs (create and share specialized chatbots)
- Voice mode (real-time conversation)
- Canvas (collaborative writing/code editing)
- Memory (remembers context across conversations)
- API: https://platform.openai.com

**API:**
```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

**Strengths:** Broadest feature set, best plugin ecosystem, voice mode, image generation
**Weaknesses:** Free tier rate-limited on best models, privacy concerns for sensitive data

---

### 1.2 Claude (Anthropic)
- **Website:** https://claude.ai
- **Company:** Anthropic
- **Models:** Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus
- **Free Tier:** Claude 3.5 Sonnet (rate-limited)
- **Paid:** Pro ($20/mo), Team ($25/user/mo)

**Key Features:**
- 200K context window (reads entire codebases, books)
- Artifacts (generates interactive code, documents, visualizations)
- Projects (organized workspaces with persistent context)
- File upload (PDF, code, images, CSV)
- Computer Use (experimental — controls desktop)
- Analysis mode (data analysis with charts)
- API: https://console.anthropic.com

**API:**
```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_KEY")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content[0].text)
```

**Strengths:** Best for long documents, coding, nuanced reasoning, safety
**Weaknesses:** No image generation, no voice mode, no web browsing (as of writing)

---

### 1.3 Gemini (Google)
- **Website:** https://gemini.google.com
- **Company:** Google DeepMind
- **Models:** Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0
- **Free Tier:** Gemini 1.5 Flash (generous limits)
- **Paid:** Google One AI Premium ($20/mo)

**Key Features:**
- Deep Google integration (Gmail, Drive, Docs, Maps)
- 1M+ token context window (Gemini 1.5 Pro)
- Multimodal (text, image, audio, video input)
- Google Search grounding
- Gems (custom AI personalities)
- API: https://aistudio.google.com

**Strengths:** Largest context window, Google ecosystem integration, multimodal
**Weaknesses:** Can be less precise than GPT-4o/Claude for complex reasoning

---

### 1.4 Copilot (Microsoft)
- **Website:** https://copilot.microsoft.com
- **Company:** Microsoft
- **Models:** GPT-4o (via OpenAI partnership)
- **Free Tier:** Yes (GPT-4o access)
- **Paid:** Pro ($20/mo)

**Key Features:**
- Web search integration (Bing)
- Image generation (DALL·E 3)
- Microsoft 365 integration (Word, Excel, PowerPoint)
- Copilot in Windows (system-level assistant)
- GitHub Copilot (code completion in IDEs)

---

### 1.5 Grok (xAI)
- **Website:** https://grok.x.ai
- **Company:** xAI (Elon Musk)
- **Models:** Grok-2, Grok-3
- **Free Tier:** Limited (via X/Twitter)
- **Paid:** X Premium+ ($16/mo), SuperGrok ($30/mo)

**Key Features:**
- Real-time X/Twitter data access
- Image generation (Aurora)
- DeepSearch (multi-step reasoning with citations)
- Less content restrictions than competitors
- API: https://console.x.ai

---

## 2. Free & Open AI Chat Platforms

### 2.1 DeepSeek
- **Website:** https://chat.deepseek.com
- **Company:** DeepSeek (China)
- **Models:** DeepSeek-V3, DeepSeek-R1 (reasoning)
- **Free Tier:** Free web chat (generous)
- **API:** Extremely cheap ($0.14/M input tokens for V3), OpenAI-compatible

**Key Features:**
- DeepSeek-R1: Open-weight reasoning model (competes with o1)
- Strong at math, coding, and Chinese/English
- Fully open-weight models (download and run locally)
- API: https://platform.deepseek.com

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DEEPSEEK_KEY",
    base_url="https://api.deepseek.com"
)
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

**Strengths:** Free chat, cheapest API, strong reasoning (R1), open-weight
**Weaknesses:** Censorship on some topics (Chinese regulation), occasional downtime

---

### 2.2 Qwen (Alibaba)
- **Website:** https://chat.qwen.ai
- **Company:** Alibaba Cloud
- **Models:** Qwen 2.5, Qwen-Max, QwQ (reasoning)
- **Free Tier:** Free web chat
- **API:** Free tier available

**Key Features:**
- Strong multilingual support (Chinese, English, and more)
- QwQ: Reasoning model (open-weight, competes with R1)
- Qwen 2.5 Coder: Specialized code model
- Open-weight models available on Hugging Face
- Multimodal (Qwen-VL for vision)

**Strengths:** Free, strong coding models, open-weight, good multilingual
**Weaknesses:** Less known in Western markets

---

### 2.3 Kimi (Moonshot AI)
- **Website:** https://kimi.moonshot.cn
- **Company:** Moonshot AI (China)
- **Models:** Kimi k1.5, Moonshot-v1
- **Free Tier:** Free web chat
- **Key Feature:** Very long context window (up to 2M tokens)

**Strengths:** Massive context window, free, good at document analysis
**Weaknesses:** Primarily Chinese-focused, English performance varies

---

### 2.4 ChatZ (chat.z.ai)
- **Website:** https://chat.z.ai
- **What it is:** Free multi-model AI chat interface
- **Free Tier:** Free access to multiple models
- **Features:** Switch between different AI models in one interface

---

### 2.5 MiniMax (Hailuo AI)
- **Website:** https://www.minimaxi.com / https://hailuoai.com
- **Company:** MiniMax (China)
- **Models:** MiniMax-Text-01, abab-series
- **Free Tier:** Free web chat (Hailuo AI)
- **Key Product:** **Hailuo AI Video** — text-to-video generation (competes with Runway, Kling)

**Key Features:**
- Text generation (strong multilingual)
- Video generation (Hailuo AI — free credits)
- Voice synthesis
- Music generation
- Large context window (4M tokens claimed on MiniMax-Text-01)
- API available

**Strengths:** Free video generation, large context, multimodal
**Weaknesses:** Less established outside China

---

### 2.6 Poe (Quora)
- **Website:** https://poe.com
- **Company:** Quora
- **What it is:** Multi-model chat platform — access GPT-4o, Claude, Gemini, Llama, and more from one interface
- **Free Tier:** Limited daily messages
- **Paid:** $20/mo (higher limits)
- **Features:** Create custom bots, share bots, API access

---

### 2.7 You.com
- **Website:** https://you.com
- **What it is:** AI search + chat platform
- **Free Tier:** Free (GPT-4o, Claude access)
- **Features:** Web search integration, multi-model, code generation

---

### 2.8 Perplexity AI
- **Website:** https://perplexity.ai
- **What it is:** AI-powered search engine with citations
- **Free Tier:** Free (limited Pro searches)
- **Paid:** Pro ($20/mo)
- **Strength:** Always cites sources, real-time web access

---

### 2.9 HuggingChat
- **Website:** https://huggingface.co/chat
- **What it is:** Open-source chat interface for Hugging Face models
- **Free Tier:** Free
- **Models:** Llama, Mistral, Qwen, Command R+, and more
- **Features:** Web search, tools, model switching

---

### 2.10 DuckDuckGo AI Chat
- **Website:** https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat
- **What it is:** Private AI chat (no data stored)
- **Free Tier:** Free
- **Models:** GPT-4o mini, Claude 3 Haiku, Llama, Mixtral
- **Strength:** Complete privacy — no conversations stored

---

## 3. Prompt Engineering & Community Platforms

### 3.1 FlowGPT
- **Website:** https://flowgpt.com
- **What it is:** Community platform for sharing and discovering AI prompts, characters, and chatbots
- **Free Tier:** Free to browse and use prompts
- **Features:**
  - Community-created prompt templates
  - Character/persona chat
  - Prompt marketplace
  - Bounties for prompt creation
  - Leaderboards

**Use Case:** Find optimized prompts for specific tasks, learn prompt engineering techniques, share your own prompts.

---

### 3.2 PromptHero
- **Website:** https://prompthero.com
- **What it is:** Search engine for AI prompts (text + image generation)
- **Features:** Prompt search, image prompt library, community

---

## 4. Self-Hosted Chat UIs

Run your own private AI chat interface connected to local models or external APIs.

### 4.1 LibreChat
- **Repository:** https://github.com/danny-avila/LibreChat
- **What it is:** Open-source ChatGPT-clone UI supporting multiple AI providers
- **License:** MIT

**Supported Backends:**
- OpenAI (GPT-4o, o1)
- Anthropic (Claude)
- Google (Gemini)
- Azure OpenAI
- Ollama (local models)
- Any OpenAI-compatible API (OpenRouter, Together, Groq, etc.)
- Plugins and tools support

```bash
# Docker deployment
git clone https://github.com/danny-avila/LibreChat.git
cd LibreChat
cp .env.example .env
# Edit .env with your API keys
docker compose up -d
# Access at http://localhost:3080
```

**Key Features:**
- Multi-model conversations
- User authentication and management
- Conversation search and export
- File uploads
- Plugin system
- Presets and prompt templates
- Mobile-friendly

**Best for:** Teams or individuals who want a unified private chat UI for all AI providers.

> **See Also:** [Docker Essentials](../devtools/docker-essentials.md) for Docker fundamentals and a detailed LibreChat Docker deployment walkthrough.

---

### 4.2 Open WebUI
- **Repository:** https://github.com/open-webui/open-webui
- **What it is:** Self-hosted ChatGPT-style interface, designed for Ollama
- **License:** MIT

```bash
# Run with Docker (connects to local Ollama)
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main

# Access at http://localhost:3000
```

**Key Features:**
- Beautiful UI (closest to ChatGPT)
- Ollama integration (auto-detects local models)
- OpenAI API support
- RAG (upload documents, chat with them)
- User management
- Voice input/output
- Model management and download
- Web search integration
- Image generation
- Pipelines (custom processing)

**Best for:** Running a private ChatGPT with local Ollama models.

---

### 4.3 text-generation-webui (oobabooga)
- **Repository:** https://github.com/oobabooga/text-generation-webui
- **What it is:** Gradio-based web UI for running LLMs locally
- **Features:** GGUF, GPTQ, AWQ, ExLlama support; character chat; extensions; training

---

### 4.4 SillyTavern
- **Repository:** https://github.com/SillyTavern/SillyTavern
- **What it is:** Frontend for LLM roleplay and character chat
- **Features:** Character cards, world info, group chats, TTS
- **Backends:** OpenAI, Claude, Ollama, KoboldCPP, and more

---

### 4.5 Chatbot UI
- **Repository:** https://github.com/mckaywrigley/chatbot-ui
- **What it is:** Open-source ChatGPT interface
- **Features:** Clean UI, OpenAI/Ollama support, conversation management

---

### 4.6 Big-AGI
- **Repository:** https://github.com/enricoros/big-AGI
- **What it is:** Feature-rich AI chat with multi-model support
- **Features:** Personas, code execution, image generation, voice, multi-chat

---

## 5. Comparison Table

### Commercial Assistants

| Platform | Free Tier | Best Model | Context Window | Image Gen | Web Search | Voice | API |
|----------|-----------|-----------|---------------|-----------|-----------|-------|-----|
| **ChatGPT** | GPT-4o mini + limited 4o | GPT-4o / o3 | 128K | ✅ DALL·E | ✅ | ✅ | ✅ |
| **Claude** | Sonnet (limited) | Opus / Sonnet | 200K | ❌ | ❌ | ❌ | ✅ |
| **Gemini** | Flash (generous) | 1.5 Pro / 2.0 | 1M+ | ✅ Imagen | ✅ | ✅ | ✅ |
| **Copilot** | GPT-4o | GPT-4o | 128K | ✅ DALL·E | ✅ Bing | ✅ | ✅ |
| **Grok** | Limited | Grok-3 | 128K | ✅ Aurora | ✅ X data | ✅ | ✅ |

### Free & Open Platforms

| Platform | Free Tier | Models | Open-Weight | API | Best For |
|----------|-----------|--------|------------|-----|----------|
| **DeepSeek** | Generous | V3, R1 | ✅ | ✅ (cheap) | Reasoning, code |
| **Qwen** | Free chat | 2.5, Max, QwQ | ✅ | ✅ | Multilingual, code |
| **Kimi** | Free chat | k1.5 | ❌ | ✅ | Long documents |
| **HuggingChat** | Free | Many | ✅ | Via HF | Open models |
| **DuckDuckGo AI** | Free | Multiple | N/A | ❌ | Privacy |
| **Perplexity** | Free + Pro | Multiple | N/A | ✅ | Search + citations |
| **Poe** | Limited | Multiple | N/A | ✅ | Multi-model |
| **FlowGPT** | Free | Community | N/A | ❌ | Prompts, characters |

### Self-Hosted UIs

| Platform | Backend Support | RAG | User Mgmt | Docker | Best For |
|----------|----------------|-----|-----------|--------|----------|
| **LibreChat** | All major APIs + Ollama | ✅ | ✅ | ✅ | Multi-provider unified UI |
| **Open WebUI** | Ollama + OpenAI API | ✅ | ✅ | ✅ | Local Ollama frontend |
| **text-gen-webui** | Local models (GGUF, GPTQ) | ❌ | ❌ | ✅ | Power users, model testing |
| **SillyTavern** | Many backends | ❌ | ❌ | ✅ | Roleplay, character chat |
| **Big-AGI** | Many APIs | ❌ | ❌ | ✅ | Feature-rich multi-chat |

---

## 6. Which Should You Use?

| Need | Recommended |
|------|------------|
| **Best overall assistant** | ChatGPT (Plus) or Claude (Pro) |
| **Best free assistant** | DeepSeek or Gemini |
| **Best for coding** | Claude or DeepSeek |
| **Best for research** | Perplexity (citations) or Gemini (long context) |
| **Best for privacy** | DuckDuckGo AI Chat or Ollama (local) |
| **Completely free, no limits** | DeepSeek chat + Pollinations API |
| **Self-hosted for team** | LibreChat + Ollama |
| **Self-hosted for personal** | Open WebUI + Ollama |
| **Best local model runner** | Ollama (easy) or llama.cpp (performance) |
| **Multi-model comparison** | Poe or OpenRouter |
| **Prompt engineering** | FlowGPT |
| **Cheapest API** | DeepSeek API or OpenRouter free models |

---

## See Also

- [AI Platforms & APIs](platforms-and-apis.md) — OpenRouter, Hugging Face, Pollinations, Runway ML, and inference tools
- [Penetration Testing Tools](../security/penetration-testing-tools.md) — Security tools that can integrate with AI
