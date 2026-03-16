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
| [Linux Internals](fundamentals/linux-internals.md) | Deep dive — CFS scheduler, memory management, VFS, system calls, eBPF, cgroups, namespaces, boot process |
| [Operating Systems](fundamentals/operating-systems.md) | OS theory, chroot, proot, proot-distro, virtualization, namespaces, isolation mechanisms |
| [Linux Distributions](fundamentals/linux-distributions.md) | RHEL, Debian, Arch ecosystems — package managers, release cycles, use-case recommendations |
| [Network Protocols](fundamentals/network-protocols.md) | Complete protocol reference — OSI model, TCP/UDP/QUIC, HTTP, DNS, TLS, MQTT, BGP, WireGuard, and 80+ protocols |
| [Virtualization](fundamentals/virtualization.md) | WSL, QEMU/KVM, VirtualBox, VMware, Hyper-V — setup, usage, comparison |
| [CPU Architecture](fundamentals/cpu-architecture.md) | Pipeline, caches, branch prediction, OoO execution, NUMA, SIMD, privilege rings, interrupts, x86-64/ARM64/RISC-V |
| [GPU Architecture](fundamentals/gpu-architecture.md) | SM/warp model, rasterization pipeline, ray tracing, CUDA, TPU, Vulkan, OpenGL, GPU memory, driver stack |
| [Compilers & Interpreters](fundamentals/compilers-and-interpreters.md) | Assembly language (x86-64, ARM64), assemblers, compiler stages, LLVM IR, JIT, historical languages |
| [Drivers & DLLs](fundamentals/drivers-and-dlls.md) | Device drivers, Windows DLLs, Linux .so, services, daemons, dynamic linker, graphics driver stack |

### Networking
Network infrastructure, tunneling, and secure connectivity.

| Document | Description |
|----------|-------------|
| [SSH Tunneling](networking/ssh-tunneling.md) | Remote port forwarding, reverse proxies — Pinggy, Serveo, localhost.run |
| [VPN & ZTNA](networking/vpn-and-ztna.md) | Tailscale, WireGuard, OpenVPN, NetBird, ProtonVPN, Tor, Playit.gg |
| [Free DNS Services](networking/free-dns-services.md) | Dynamic DNS (No-IP, Dynu, DuckDNS, Cloudflare), free domains, DNS hosting |
| [Remote Access](networking/remote-access.md) | X11, VNC, RDP, SPICE, SSH, Win-KeX, Parsec, AnyDesk, Sunshine+Moonlight, RustDesk, NoMachine, Guacamole |
| [Tunneling Tools](networking/tunneling-tools.md) | Ngrok, LocalXpose, Cloudflared — expose local services to the internet |
| [OnionShare](networking/onionshare.md) | Anonymous file sharing, receive mode, website hosting, and chat over Tor |

### Security
Offensive security tools, OSINT, reverse engineering, exploit development, and threat intelligence.

| Document | Description |
|----------|-------------|
| [Penetration Testing Tools](security/penetration-testing-tools.md) | Nmap, Metasploit, Burp Suite, Hashcat, Aircrack-ng, OWASP ZAP, and 20+ tools |
| [OSINT Platforms](security/osint-platforms.md) | Shodan, ZoomEye, Censys, Onyphe, CriminalIP — internet-wide scanning engines |
| [OSINT CLI Tools](security/osint-cli-tools.md) | GhostTrack, Holehe, PhoneInfoga, OnionSearch, and 15+ recon tools |
| [Web Application Security](security/web-application-security.md) | OWASP Top 10, ZAP, OFFSEC/OSCP certifications, HackTheBox |
| [Reverse Engineering](security/reverse-engineering.md) | Ghidra, IDA Pro, x64dbg, radare2, Binary Ninja, GDB, LLDB, Frida — full RE toolkit |
| [Binary Analysis](security/binary-analysis.md) | angr, Qiling, PANDA, miasm, BAP, remill, McSema, MemProcFS, Kaitai, cemu, pefile, GoReSym, garble, and 20+ tools |
| [Exploit Development](security/exploit-development.md) | RPISEC MBE course, HackSys HSEVD (Windows kernel), exploitation techniques, mitigations and bypasses |
| [Offensive Frameworks](security/offensive-frameworks.md) | fsociety, AutoSploit, WinPwn, commix, SSRFmap, fuxploider, toxssin, moonwalk, SSH-Snake, AndroRAT, XAttacker |
| [Active Directory](security/active-directory.md) | AD exploitation cheat sheet — enumeration, Kerberoasting, Pass-the-Hash, DCSync, lateral movement |
| [Network Analysis](security/network-analysis.md) | Zeek (formerly Bro) — network traffic analysis, protocol logging, threat hunting, scripting |
| [Hacker Roadmap](security/hacker-roadmap.md) | sundowndev roadmap, Awesome Hacking, Awesome Windows, Arcanum AI Security Hub, 0xor0ne awesome-list |
| [OPSEC & Proxies](security/opsec-and-proxies.md) | OPSEC fundamentals, ProxyChains, Camoufox, temp numbers & email |
| [Bootable USB Tools](security/bootable-usb-tools.md) | Rufus, Ventoy, BalenaEtcher — bootable drives for live OS and recovery |
| [FingerprintJS](security/fingerprintjs.md) | Browser fingerprinting — signals, spoofing, anti-fingerprint defenses, fraud detection |

### IoT
Microcontrollers and embedded systems.

| Document | Description |
|----------|-------------|
| [ESP32](iot/esp32.md) | Architecture, variants, power modes, Arduino IDE & ESP-IDF setup |
| [ESP8266](iot/esp8266.md) | Wi-Fi microcontroller — modules, programming, comparison with ESP32 |
| [Arduino](iot/arduino.md) | Platform overview, boards, programming model, IDE 2.x |
| [Espectre Project](iot/projects/espectre/) | ESP32 CSI motion detection — real-time WebSocket dashboard |

### Mobile
Android development, Termux, and mobile virtualization.

| Document | Description |
|----------|-------------|
| [Termux Setup](mobile/termux-setup.md) | Installation, package management, programming languages, SSH, Tmux, FFmpeg |
| [Linux on Android](mobile/linux-on-android.md) | Ubuntu via proot-distro with GUI (VNC + LXQt/LXDE) |
| [Desktop Environments](mobile/desktop-environments.md) | XFCE, LXDE, LXQT, GNOME, KDE on headless systems + Termux X11 |
| [Environment Isolation](mobile/environment-isolation.md) | chroot vs proot vs proot-distro — comparison, usage, security |
| [Termux Pentesting](mobile/termux-pentesting.md) | Kali NetHunter Rootless, Parrot OS, BlackArch on Android |
| [Emulators](mobile/emulators.md) | VPhone OS, VMOS, Winlator, Vectras VM, PPSSPP — Android virtualization |
| [Android Automation](mobile/android-automation.md) | ArduinoDroid, Tasker, MacroDroid — mobile programming and task automation |
| [Android System](mobile/android-system.md) | Shizuku, Canta (rootless debloater), Phantom Process Killer fix, display density |

### AI
Artificial intelligence platforms, APIs, chat interfaces, and local inference.

| Document | Description |
|----------|-------------|
| [Platforms & APIs](ai/platforms-and-apis.md) | OpenRouter, Hugging Face, Pollinations, g4f, Groq, Runway ML, Ollama, llama.cpp |
| [Chat Interfaces](ai/chat-interfaces.md) | ChatGPT, Claude, DeepSeek, Qwen, Kimi, Gemini, FlowGPT, LibreChat, Open WebUI |
| [AI Video Tools](ai/ai-video-tools.md) | Deep-Live-Cam (real-time face swap), RuView (AI video analysis) |

### Dev Tools
Development environments, coding agents, terminals, and frameworks.

| Document | Description |
|----------|-------------|
| [Coding Agents](devtools/coding-agents.md) | Cursor, Claude Code, Windsurf, Kiro, Cline, and 15+ AI coding assistants |
| [Editors & IDEs](devtools/editors-and-ides.md) | VSCode, code-server (self-hosted), Void Editor |
| [Terminal Tools](devtools/terminal-tools.md) | Tmux, Tabby — terminal multiplexing and modern terminals |
| [Docker Essentials](devtools/docker-essentials.md) | Containers, images, volumes, Compose, Dockerfile patterns |
| [Figma](devtools/figma.md) | Design platform — dev mode, prototyping, plugins |
| [Frameworks & Libraries](devtools/frameworks-and-libraries.md) | PyTorch, Mineflayer, minecraft-protocol, go-mc |
| [APIs & Resources](devtools/apis-and-resources.md) | REST, GraphQL, API authentication, GitHub API, public APIs, MineSkin |
| [Version Control](devtools/version-control.md) | Bitbucket, GitHub, GitLab — pipelines, REST APIs, CLI tools, self-hosting, Git essentials |

### Automation
Web scraping, browser automation, and workflow tools.

| Document | Description |
|----------|-------------|
| [Web Automation](automation/web-automation.md) | Playwright, Selenium, Puppeteer, CapMonster, 2Captcha, Camoufox |
| [Workflow Automation](automation/workflow-automation.md) | n8n, Tasker, MacroDroid — self-hosted workflows, Android automation |
| [Discord Quest Completer](automation/discord-quest-completer.md) | Complete Discord Quests without installing games — dummy process spoofing |

### Deployment
Cloud platforms, hosting, and compute environments.

| Document | Description |
|----------|-------------|
| [Hosting Platforms](deployment/hosting-platforms.md) | Vercel, Netlify, Firebase Studio — static/serverless hosting |
| [Cloud Platforms](deployment/cloud-platforms.md) | Google Cloud, Colab, Kaggle, Antigravity, Gmail API |
| [Kubernetes](deployment/kubernetes.md) | Architecture, kubectl, Deployments, Services, Ingress, Helm, GKE/EKS/AKS |

### Media
Media processing, creative tools, and image enhancement.

| Document | Description |
|----------|-------------|
| [Media Tools](media/media-tools.md) | FFmpeg, VLC, GIMP — media conversion, streaming, image editing |
| [Mobile Creative Tools](media/mobile-creative-tools.md) | CapCut, Alight Motion, CPU-Z — mobile video editing, motion graphics |
| [Image Upscalers](media/imgupscaler.md) | imgupscaler.com, Real-ESRGAN, Upscayl, Waifu2x |

### Mail
Email providers and clients for privacy-conscious communication.

| Document | Description |
|----------|-------------|
| [Email Providers](mail/email-providers.md) | ProtonMail, Tuta Mail — E2EE email, Swiss and German jurisdiction |
| [Email Clients](mail/email-clients.md) | Thunderbird, Canary Mail — PGP setup, IMAP configuration, Proton Bridge |

### Streaming
Video, anime, manga, and self-hosted media platforms.

| Document | Description |
|----------|-------------|
| [Movie Streaming](streaming/movie-streaming.md) | PRMovies, FMovies, Nunflix — free movie streaming, legal alternatives |
| [Video Platforms](streaming/video-platforms.md) | Dailymotion, EverythingMoe — video hosting, yt-dlp usage |
| [Anime Streaming](streaming/anime-streaming.md) | AnimePahe, AnimeKai, HiAnime, Toono, RareAnimes |
| [Manga Reading](streaming/manga-reading.md) | WeebCentral, MangaDex, Mihon/Tachiyomi — offline reading, AniList sync |
| [Plex](streaming/plex.md) | Self-hosted media server — library setup, Docker, transcoding, API |

### Minecraft
Clients, bots, and servers for Minecraft Java Edition.

| Document | Description |
|----------|-------------|
| [Utility Clients](minecraft/utility-clients.md) | Meteor Client, Baritone — Fabric utility mod, A* pathfinding bot |
| [Ghost Clients](minecraft/ghost-clients.md) | Vape, Raven B+, Hydrogen, Vestige — stealth PvP clients |
| [Glazed Client](minecraft/glazed-client.md) | Glazed — injection-based paid client, module list, multi-version support |
| [Servers](minecraft/servers.md) | FakePixel (free Hypixel alternative), 2b2t, Hypixel, MineMenClub |

### Torrenting
BitTorrent technology, torrent indexing sites, and download clients.

| Document | Description |
|----------|-------------|
| [BitTorrent Technology](torrenting/bittorrent-technology.md) | Protocol deep dive — .torrent structure, info hashes, magnet links, DHT, PEX, piece selection, choking, MSE encryption, BitTorrent v2 |
| [Torrent Sites](torrenting/torrent-sites.md) | TPB, 1337x, YTS, RARBG (dead — documented), Torlock, LimeTorrents, KickassTorrents, ETTV, TorrentGalaxy, Torrends.to, Appdoze |
| [Deluge](torrenting/deluge.md) | Deluge BitTorrent client — daemon/client architecture, Web UI, plugins, Docker, VPN kill switch, comparison with qBittorrent |

### Reference
Storage platforms, URL tools, communities, and quick-reference directories.

| Document | Description |
|----------|-------------|
| [Archive.org](reference/archive-org.md) | Wayback Machine, Software Library, Books, CDX API, upload via CLI |
| [MediaFire](reference/mediafire.md) | Free file hosting — sharing links, folder distribution, API |
| [Gofile](reference/gofile.md) | Anonymous unlimited-size file hosting — REST API, 10-day retention |
| [Mega.nz](reference/mega-nz.md) | Encrypted cloud storage — E2EE, MEGAcmd CLI, Python SDK |
| [Smash](reference/smash.md) | Large file transfer — unlimited size, 14-day free link, Node.js SDK |
| [URL Shorteners](reference/url-shorteners.md) | Shrink.pe, ShrinkEarn — earning-based shorteners, API, self-hosting (YOURLS, Shlink, Kutt) |
| [Platforms & Communities](reference/platforms-and-communities.md) | Social platforms, cybersec news, threat intel, Skype → Teams migration note, HL Gaming Official |

---

## 📈 Repository Stats

| Metric | Value |
|--------|-------|
| **Total Documents** | 93 |
| **Categories** | 15 |
| **Topics Covered** | Kernels, Linux Internals, CPU/GPU Architecture, Rasterization, Ray Tracing, CUDA, Compilers, Assembly, Drivers, DLLs, OS Theory, Protocols, Virtualization, Networking, Security, RE, Binary Analysis, Exploit Development, Active Directory, Offensive Frameworks, Network Analysis, Zeek, Fingerprinting, OPSEC, IoT, Mobile, Android Debloating, AI, Video AI, Coding Agents, Docker, Kubernetes, Automation, Deployment, Media, Email, File Storage, Video Streaming, Anime, Manga, Self-Hosted Media, Minecraft Clients, Minecraft Servers, URL Shorteners, Hacker Roadmap |

---

## 📝 Contributing

This is a living knowledge base. Documents are updated as new tools, techniques, and platforms emerge.

## ⚖️ Disclaimer

All security-related content is for **educational and authorized testing purposes only**. Always follow applicable laws and responsible disclosure practices.
