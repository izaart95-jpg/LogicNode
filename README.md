<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=1A1A1A&center=true&vCenter=true&width=500&height=70&lines=LOGICNODE+SYSTEMS;LOGIC+IS+NOT+MAGIC;INDUSTRIAL+EFFICIENCY" alt="LogicNode Title" />

**A structured knowledge base covering systems fundamentals, networking, security, IoT, mobile development, dev tools, automation, deployment, and media.**

The philosophy is simple: **Logic is a tool, not a trick.** We build frameworks that prioritize predictability over "magic."

---

</div>

## 📂 Documentation Index

### Fundamentals
Core computer science and systems theory.

| Document | Description |
|----------|-------------|
| [Kernel Architecture](fundamentals/kernel-architecture.md) | Linux, Windows NT, and Darwin kernel internals — architecture, syscalls, debugging, compilation, tuning, security |
| [Operating Systems](fundamentals/operating-systems.md) | OS theory, chroot, proot, proot-distro, virtualization, namespaces, isolation mechanisms |
| [Linux Distributions](fundamentals/linux-distributions.md) | RHEL, Debian, Arch ecosystems — package managers, release cycles, use-case recommendations |
| [Network Protocols](fundamentals/network-protocols.md) | Complete protocol reference — OSI model, TCP/UDP/QUIC, HTTP, DNS, TLS, MQTT, BGP, WireGuard, and 80+ protocols |
| [Virtualization](fundamentals/virtualization.md) | WSL, QEMU/KVM, VirtualBox, VMware, Hyper-V — setup, usage, comparison |

### Networking
Network infrastructure, tunneling, and secure connectivity.

| Document | Description |
|----------|-------------|
| [SSH Tunneling](networking/ssh-tunneling.md) | Remote port forwarding, reverse proxies — Pinggy, Serveo, localhost.run |
| [VPN & ZTNA](networking/vpn-and-ztna.md) | Tailscale, WireGuard, OpenVPN, NetBird, ProtonVPN, Tor, Playit.gg |
| [Free DNS Services](networking/free-dns-services.md) | Dynamic DNS (No-IP, Dynu, DuckDNS, Cloudflare), free domains, DNS hosting |
| [Remote Access](networking/remote-access.md) | X11, VNC, RDP, SPICE, SSH basics, Win-KeX, VcXsrv, Parsec, AnyDesk, Sunshine+Moonlight, RustDesk, NoMachine, Guacamole, noVNC, xrdp |
| [Tunneling Tools](networking/tunneling-tools.md) | Ngrok, LocalXpose, Cloudflared — expose local services to the internet |
| [OnionShare](networking/onionshare.md) | Anonymous file sharing, receive mode, website hosting, and chat over Tor |

### Security
Offensive security tools, OSINT, reverse engineering, and threat intelligence.

| Document | Description |
|----------|-------------|
| [Penetration Testing Tools](security/penetration-testing-tools.md) | Nmap, Metasploit, Burp Suite, Hashcat, Aircrack-ng, OWASP ZAP, and 20+ more tools |
| [OSINT Platforms](security/osint-platforms.md) | Shodan, ZoomEye, Censys, Onyphe, CriminalIP — internet-wide scanning engines |
| [OSINT CLI Tools](security/osint-cli-tools.md) | GhostTrack, Holehe, PhoneInfoga, OnionSearch, and 15+ recon tools |
| [Web Application Security](security/web-application-security.md) | OWASP Top 10, ZAP, OFFSEC/OSCP certifications, HackTheBox platform |
| [Reverse Engineering](security/reverse-engineering.md) | x64dbg, Ghidra, Frida, IDA Pro — disassembly, debugging, dynamic instrumentation |
| [OPSEC & Proxies](security/opsec-and-proxies.md) | OPSEC fundamentals, ProxyChains, proxy sources, Camoufox, temp numbers & email |
| [Bootable USB Tools](security/bootable-usb-tools.md) | Rufus, Ventoy, BalenaEtcher — creating bootable drives for live OS and recovery |

### IoT
Microcontrollers and embedded systems.

| Document | Description |
|----------|-------------|
| [ESP32](iot/esp32.md) | Architecture, variants (S2/S3/C3/C6/H2), features, power modes, Arduino IDE & ESP-IDF setup |
| [ESP8266](iot/esp8266.md) | Wi-Fi microcontroller — modules, programming, comparison with ESP32 |
| [Arduino](iot/arduino.md) | Platform overview, boards (Uno/Nano/Mega/Due), programming model, IDE 2.x |
| [Espectre Project](iot/projects/espectre/) | ESP32 CSI motion detection — real-time WebSocket dashboard, ESPHome integration |

### Mobile
Android development, Termux, and mobile virtualization.

| Document | Description |
|----------|-------------|
| [Termux Setup](mobile/termux-setup.md) | Installation, package management, programming languages, SSH, APIs, Tmux, FFmpeg |
| [Linux on Android](mobile/linux-on-android.md) | Ubuntu via proot-distro with GUI (VNC + LXQt/LXDE) |
| [Desktop Environments](mobile/desktop-environments.md) | Installing XFCE, LXDE, LXQT, GNOME, KDE on headless systems + Termux X11 |
| [Environment Isolation](mobile/environment-isolation.md) | chroot vs proot vs proot-distro — comparison, usage, security warnings |
| [Termux Pentesting](mobile/termux-pentesting.md) | Kali NetHunter Rootless, Parrot OS, BlackArch on Android |
| [Emulators](mobile/emulators.md) | VPhone OS, VMOS, Winlator, Vectras VM, PPSSPP — Android virtualization |
| [Android Automation](mobile/android-automation.md) | ArduinoDroid, Tasker, MacroDroid — mobile programming and task automation |
| [Android System](mobile/android-system.md) | Shizuku, Phantom Process Killer fix, display density and smallest width configuration |

### AI
Artificial intelligence platforms, APIs, chat interfaces, and local inference.

| Document | Description |
|----------|-------------|
| [Platforms & APIs](ai/platforms-and-apis.md) | OpenRouter, Hugging Face, Pollinations, g4f, Groq, Runway ML, Ollama, llama.cpp — inference, APIs, creative tools |
| [Chat Interfaces](ai/chat-interfaces.md) | ChatGPT, Claude, DeepSeek, Qwen, Kimi, Gemini, FlowGPT, LibreChat, Open WebUI — assistants and self-hosted UIs |

### Dev Tools
Development environments, coding agents, terminals, and frameworks.

| Document | Description |
|----------|-------------|
| [Coding Agents](devtools/coding-agents.md) | Cursor, Claude Code, Windsurf, Kiro, Cline, and 15+ AI coding assistants — setup, features, comparison |
| [Editors & IDEs](devtools/editors-and-ides.md) | VSCode, code-server (self-hosted), Void Editor — configuration, extensions, remote development |
| [Terminal Tools](devtools/terminal-tools.md) | Tmux, Tabby — terminal multiplexing, modern terminals, configuration |
| [Docker Essentials](devtools/docker-essentials.md) | Containers, images, volumes, Compose, Dockerfile patterns, LibreChat Docker setup |
| [Figma](devtools/figma.md) | Design platform — dev mode, prototyping, plugins, Figma-to-code workflows |
| [Frameworks & Libraries](devtools/frameworks-and-libraries.md) | PyTorch, Mineflayer, minecraft-protocol, go-mc — ML training, game bot development |
| [APIs & Resources](devtools/apis-and-resources.md) | REST, GraphQL, API authentication, GitHub API, public APIs, rate limiting, MineSkin |

### Automation
Web scraping, browser automation, and workflow tools.

| Document | Description |
|----------|-------------|
| [Web Automation](automation/web-automation.md) | Playwright, Selenium, Puppeteer, CapMonster, 2Captcha, Camoufox — browser control and anti-bot |
| [Workflow Automation](automation/workflow-automation.md) | n8n, Tasker, MacroDroid — self-hosted workflows, Android automation |

### Deployment
Cloud platforms, hosting, and compute environments.

| Document | Description |
|----------|-------------|
| [Hosting Platforms](deployment/hosting-platforms.md) | Vercel, Netlify, Firebase Studio — static/serverless hosting, deployment workflows |
| [Cloud Platforms](deployment/cloud-platforms.md) | Google Cloud Console, Colab, Kaggle, Antigravity, Gmail API — cloud compute and APIs |
| [Kubernetes](deployment/kubernetes.md) | Architecture, kubectl, Deployments, Services, Ingress, Helm, GKE/EKS/AKS — container orchestration |

### Media
Media processing, creative tools, and image enhancement.

| Document | Description |
|----------|-------------|
| [Media Tools](media/media-tools.md) | FFmpeg, VLC, GIMP — media conversion, streaming, image editing, batch processing |
| [Mobile Creative Tools](media/mobile-creative-tools.md) | CapCut, Alight Motion, CPU-Z — mobile video editing, motion graphics, system info |
| [Image Upscalers](media/imgupscaler.md) | imgupscaler.com, Real-ESRGAN, Upscayl, Waifu2x — AI-based image and video upscaling |

### Mail
Email providers and clients for privacy-conscious communication.

| Document | Description |
|----------|-------------|
| [Email Providers](mail/email-providers.md) | ProtonMail, Tuta Mail — end-to-end encrypted email, zero-knowledge providers, Swiss and German jurisdiction |
| [Email Clients](mail/email-clients.md) | Thunderbird, Canary Mail — desktop and mobile clients, PGP setup, IMAP configuration, Proton Bridge |

### Streaming
Video platforms and anime streaming services.

| Document | Description |
|----------|-------------|
| [Video Platforms](streaming/video-platforms.md) | Dailymotion, EverythingMoe — general video hosting, API access, embedding, yt-dlp usage |
| [Anime Streaming](streaming/anime-streaming.md) | AnimePahe, AnimeKai, HiAnime, Toono, RareAnimes — platforms, features, download tips, comparison |

### Reference
Storage platforms, communities, and quick-reference directories.

| Document | Description |
|----------|-------------|
| [Archive.org](reference/archive-org.md) | Wayback Machine, Software Library, Books, audio/video archive, CDX API, upload via CLI |
| [MediaFire](reference/mediafire.md) | Free file hosting — sharing links, folder distribution, API access, CLI downloading |
| [Gofile](reference/gofile.md) | Anonymous unlimited-size file hosting — no account required, REST API, 10-day guest retention |
| [Mega.nz](reference/mega-nz.md) | Encrypted cloud storage — E2EE, 20 GB free, MEGAcmd CLI, Python SDK, security model |
| [Smash](reference/smash.md) | Large file transfer service — unlimited size, 14-day free link, email delivery, Node.js SDK |
| [Platforms & Communities](reference/platforms-and-communities.md) | Social platforms, cybersec news, threat intel orgs, conferences, underground forums |

---

## 📈 Repository Stats

| Metric | Value |
|--------|-------|
| **Total Documents** | 55 |
| **Categories** | 13 |
| **Topics Covered** | Kernels, OS Theory, Protocols, Virtualization, Networking, Security, Reverse Engineering, OPSEC, IoT, Mobile, AI, Coding Agents, Docker, Kubernetes, Automation, Deployment, Media, Email, File Storage, Video Streaming, Anime |

---

## 📝 Contributing

This is a living knowledge base. Documents are updated as new tools, techniques, and platforms emerge.

## ⚖️ Disclaimer

All security-related content is for **educational and authorized testing purposes only**. Always follow applicable laws and responsible disclosure practices.
