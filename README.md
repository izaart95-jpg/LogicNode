<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=35&pause=1000&color=1A1A1A&center=true&vCenter=true&width=500&height=70&lines=LOGICNODE+SYSTEMS;LOGIC+IS+NOT+MAGIC;INDUSTRIAL+EFFICIENCY" alt="LogicNode Title" />

**A structured knowledge base covering systems fundamentals, networking, security, IoT, mobile development, dev tools, automation, deployment, and media.**

---

</div>

## 📂 Documentation Index

### Fundamentals
| Document | Description |
|----------|-------------|
| [How a Computer Really Works](fundamentals/how-computers-work.md) | Full vertical slice: electrons → transistors → Apple M-series → macOS → WiFi → TLS → WebKit → VP9 decode → GPU → LCD photons → AAC → speaker |
| [HTTP vs HTTPS & TLS/SSL](fundamentals/http-https-tls.md) | HTTP plaintext vs HTTPS, TLS 1.3 handshake, cipher suites, X.509 certificates, PKI, HSTS, CT logs, attacks |
| [CPU Architecture](fundamentals/cpu-architecture.md) | Pipeline, caches, OoO execution, branch prediction, NUMA, SIMD, privilege rings, interrupts, x86-64/ARM64/RISC-V |
| [GPU Architecture](fundamentals/gpu-architecture.md) | SM/warp model, rasterization, ray tracing, CUDA, TPU, Vulkan, OpenGL, GPU memory, driver stack |
| [Compilers & Interpreters](fundamentals/compilers-and-interpreters.md) | Assembly (x86-64, ARM64), assemblers, compiler stages, LLVM IR, JIT, historical languages |
| [Drivers & DLLs](fundamentals/drivers-and-dlls.md) | Device drivers, Windows DLLs, Linux .so, services, daemons, dynamic linker, graphics driver stack |
| [Linux Internals](fundamentals/linux-internals.md) | CFS scheduler, memory management, VFS, system calls, eBPF, cgroups, namespaces, boot process |
| [Kernel Architecture](fundamentals/kernel-architecture.md) | Linux, Windows NT, Darwin kernel internals — architecture, syscalls, debugging |
| [Operating Systems](fundamentals/operating-systems.md) | OS theory, chroot, proot, proot-distro, virtualization, namespaces |
| [Linux Distributions](fundamentals/linux-distributions.md) | RHEL, Debian, Arch — package managers, release cycles |
| [Network Protocols](fundamentals/network-protocols.md) | OSI model, TCP/UDP/QUIC, HTTP, DNS, TLS, MQTT, BGP, WireGuard, 80+ protocols |
| [Virtualization](fundamentals/virtualization.md) | WSL, QEMU/KVM, VirtualBox, VMware, Hyper-V |
| [Wine Compatibility Layer](fundamentals/wine-compatibility.md) | Wine architecture, DXVK, Proton, Lutris, Bottles, Winetricks, prefixes, macOS CrossOver/Whisky/GPTK |
| [File Systems](fundamentals/file-systems.md) | ext4, Btrfs, ZFS, XFS, NTFS, APFS, FAT32/exFAT, F2FS, tmpfs, FUSE, NFS, procfs — internals + commands |
| [Storage Technology](fundamentals/storage-technology.md) | NAND flash internals, SD cards, USB pendrives, RAM (DRAM/SRAM/DDR), USB protocol, Thunderbolt, NVMe |
| [CGI & VFX](fundamentals/cgi-vfx.md) | 3D pipeline, path tracing, PBR shaders, VFX production workflow, compositing, simulation, motion capture, software |

### Networking
| Document | Description |
|----------|-------------|
| [SSH Tunneling](networking/ssh-tunneling.md) | Remote port forwarding — Pinggy, Serveo, localhost.run |
| [VPN & ZTNA](networking/vpn-and-ztna.md) | Tailscale, WireGuard, OpenVPN, NetBird, ProtonVPN, Tor, Playit.gg |
| [Free DNS Services](networking/free-dns-services.md) | No-IP, Dynu, DuckDNS, Cloudflare dynamic DNS, free domains |
| [Remote Access](networking/remote-access.md) | X11, VNC, RDP, SPICE, Win-KeX, Parsec, AnyDesk, Sunshine+Moonlight, RustDesk, Guacamole |
| [Tunneling Tools](networking/tunneling-tools.md) | Ngrok, LocalXpose, Cloudflared |
| [OnionShare](networking/onionshare.md) | Anonymous file sharing, receive mode, website hosting, chat over Tor |

### Security
| Document | Description |
|----------|-------------|
| [Penetration Testing Tools](security/penetration-testing-tools.md) | Nmap, Metasploit, Burp Suite, Hashcat, Aircrack-ng, OWASP ZAP, 20+ tools |
| [OSINT Platforms](security/osint-platforms.md) | Shodan, ZoomEye, Censys, Onyphe, CriminalIP |
| [OSINT CLI Tools](security/osint-cli-tools.md) | GhostTrack, Holehe, PhoneInfoga, OnionSearch, 15+ tools |
| [Web Application Security](security/web-application-security.md) | OWASP Top 10, ZAP, OSCP, HackTheBox |
| [Reverse Engineering](security/reverse-engineering.md) | Ghidra, IDA Pro, x64dbg, radare2, Binary Ninja, GDB, LLDB, Frida, Windows PE tools |
| [Binary Analysis](security/binary-analysis.md) | angr, Qiling, PANDA, miasm, BAP, remill, MemProcFS, Kaitai, cemu, pefile, GoReSym, 20+ tools |
| [Exploit Development](security/exploit-development.md) | RPISEC MBE, HackSys HSEVD, exploitation techniques, mitigations and bypasses |
| [Offensive Frameworks](security/offensive-frameworks.md) | fsociety, AutoSploit, WinPwn, commix, SSRFmap, toxssin, moonwalk, SSH-Snake, AndroRAT, XAttacker |
| [Active Directory](security/active-directory.md) | AD exploitation cheat sheet — Kerberoasting, Pass-the-Hash, DCSync, lateral movement |
| [Network Analysis](security/network-analysis.md) | Zeek (formerly Bro) — traffic analysis, protocol logging, threat hunting |
| [Hacker Roadmap](security/hacker-roadmap.md) | sundowndev roadmap, Awesome Hacking, Arcanum AI Security Hub, 0xor0ne awesome-list |
| [OPSEC & Proxies](security/opsec-and-proxies.md) | OPSEC fundamentals, ProxyChains, Camoufox, temp numbers & email |
| [Bootable USB Tools](security/bootable-usb-tools.md) | Rufus, Ventoy, BalenaEtcher |
| [FingerprintJS](security/fingerprintjs.md) | Browser fingerprinting — signals, spoofing, anti-fingerprint defenses |

### IoT
| Document | Description |
|----------|-------------|
| [ESP32](iot/esp32.md) | Architecture, variants, power modes, Arduino IDE & ESP-IDF setup |
| [ESP8266](iot/esp8266.md) | WiFi microcontroller — modules, programming |
| [Arduino](iot/arduino.md) | Platform overview, boards, programming model, IDE 2.x |
| [Offensive Firmware](iot/offensive-firmware.md) | ESP32 Marauder, Bruce Firmware, GhostESP — WiFi/BT security tools, flashing, comparison |
| [Flipper Zero](iot/flipper-zero.md) | Hardware specs, Sub-GHz, RFID, NFC, IR, BadUSB, GPIO, custom firmware, ESP32 Dev Board |
| [LilyGo, STM32 & CNC](iot/lilygo-stm32-cnc.md) | T-Deck, T-Embed, STM32 family, G-code, CNC controllers, CAM software |
| [Espectre Project](iot/projects/espectre/) | ESP32 CSI motion detection — real-time WebSocket dashboard |

### Mobile
| Document | Description |
|----------|-------------|
| [Termux Setup](mobile/termux-setup.md) | Installation, package management, SSH, Tmux, FFmpeg |
| [Linux on Android](mobile/linux-on-android.md) | Ubuntu via proot-distro with GUI (VNC + LXQt/LXDE) |
| [Desktop Environments](mobile/desktop-environments.md) | XFCE, LXDE, LXQT, GNOME, KDE on headless + Termux X11 |
| [Environment Isolation](mobile/environment-isolation.md) | chroot vs proot vs proot-distro |
| [Termux Pentesting](mobile/termux-pentesting.md) | Kali NetHunter Rootless, Parrot OS, BlackArch on Android |
| [Emulators](mobile/emulators.md) | VPhone OS, VMOS, Winlator, Vectras VM, PPSSPP |
| [Android Automation](mobile/android-automation.md) | ArduinoDroid, Tasker, MacroDroid |
| [Android System](mobile/android-system.md) | Shizuku, Canta (rootless debloater), Phantom Process Killer fix |
| [Android Rooting](mobile/android-rooting.md) | Bootloader unlock, Magisk, KernelSU, APatch, TWRP, custom ROMs, Play Integrity bypass |

### AI
| Document | Description |
|----------|-------------|
| [Platforms & APIs](ai/platforms-and-apis.md) | OpenRouter, Hugging Face, Groq, Ollama, llama.cpp, Runway ML |
| [Chat Interfaces](ai/chat-interfaces.md) | ChatGPT, Claude, DeepSeek, Qwen, Gemini, LibreChat, Open WebUI |
| [AI Video Tools](ai/ai-video-tools.md) | Deep-Live-Cam, RuView — real-time face swap, video analysis |

### Dev Tools
| Document | Description |
|----------|-------------|
| [Coding Agents](devtools/coding-agents.md) | Cursor, Claude Code, Windsurf, Kiro, Cline, 15+ AI coding assistants |
| [Editors & IDEs](devtools/editors-and-ides.md) | VSCode, code-server, Void Editor |
| [Terminal Tools](devtools/terminal-tools.md) | Tmux, Tabby |
| [Docker Essentials](devtools/docker-essentials.md) | Containers, images, volumes, Compose, Dockerfile |
| [Figma](devtools/figma.md) | Design platform — dev mode, prototyping, plugins |
| [Frameworks & Libraries](devtools/frameworks-and-libraries.md) | PyTorch, Mineflayer, minecraft-protocol, go-mc |
| [APIs & Resources](devtools/apis-and-resources.md) | REST, GraphQL, GitHub API, public APIs, MineSkin |
| [Version Control](devtools/version-control.md) | Bitbucket, GitHub, GitLab — pipelines, REST APIs, CLI tools, self-hosting |

### Automation
| Document | Description |
|----------|-------------|
| [Web Automation](automation/web-automation.md) | Playwright, Selenium, Puppeteer, CapMonster, 2Captcha, Camoufox |
| [Workflow Automation](automation/workflow-automation.md) | n8n, Tasker, MacroDroid |
| [Discord Quest Completer](automation/discord-quest-completer.md) | Complete Discord Quests without installing games |
| [Userscripts](automation/userscripts.md) | Tampermonkey, Violentmonkey — write GM_ scripts, intercept XHR, modify pages |

### Deployment
| Document | Description |
|----------|-------------|
| [Hosting Platforms](deployment/hosting-platforms.md) | Vercel, Netlify, Firebase Studio |
| [Cloud Platforms](deployment/cloud-platforms.md) | Google Cloud, Colab, Kaggle, Antigravity |
| [Kubernetes](deployment/kubernetes.md) | Architecture, kubectl, Deployments, Services, Ingress, Helm, GKE/EKS/AKS |

### Media
| Document | Description |
|----------|-------------|
| [Creative Software](media/creative-software.md) | Blender (3D+render), DaVinci Resolve (color+edit), Photoshop, Premiere Pro, Filmora, CapCut desktop |
| [Media Tools](media/media-tools.md) | FFmpeg, VLC, GIMP |
| [Mobile Creative Tools](media/mobile-creative-tools.md) | CapCut, Alight Motion, CPU-Z |
| [Image Upscalers](media/imgupscaler.md) | imgupscaler.com, Real-ESRGAN, Upscayl, Waifu2x |

### Mail
| Document | Description |
|----------|-------------|
| [Email Providers](mail/email-providers.md) | ProtonMail, Tuta Mail |
| [Email Clients](mail/email-clients.md) | Thunderbird, Canary Mail, Proton Bridge |

### Streaming
| Document | Description |
|----------|-------------|
| [Movie Streaming](streaming/movie-streaming.md) | PRMovies, FMovies, Nunflix |
| [Video Platforms](streaming/video-platforms.md) | Dailymotion, EverythingMoe |
| [Anime Streaming](streaming/anime-streaming.md) | AnimePahe, AnimeKai, HiAnime, Toono, RareAnimes |
| [Manga Reading](streaming/manga-reading.md) | WeebCentral, MangaDex, Mihon/Tachiyomi |
| [Plex](streaming/plex.md) | Self-hosted media server — setup, Docker, transcoding |

### Minecraft
| Document | Description |
|----------|-------------|
| [Utility Clients](minecraft/utility-clients.md) | Meteor Client, Baritone |
| [Ghost Clients](minecraft/ghost-clients.md) | Vape, Raven B+, Hydrogen, Vestige |
| [Glazed Client](minecraft/glazed-client.md) | Glazed — injection-based paid client |
| [Servers](minecraft/servers.md) | FakePixel, 2b2t, Hypixel, MineMenClub |

### Torrenting
| Document | Description |
|----------|-------------|
| [BitTorrent Technology](torrenting/bittorrent-technology.md) | Protocol internals, info hashes, magnet links, DHT, PEX, piece selection, MSE encryption |
| [Torrent Sites](torrenting/torrent-sites.md) | TPB, 1337x, YTS, RARBG (dead), TorrentGalaxy, ETTV, Torlock, KAT, Torrends.to, Appdoze |
| [Deluge](torrenting/deluge.md) | BitTorrent client — daemon/client, Web UI, plugins, Docker, VPN binding |

### Reference
| Document | Description |
|----------|-------------|
| [Archive.org](reference/archive-org.md) | Wayback Machine, Software Library, CDX API, upload via CLI |
| [MediaFire](reference/mediafire.md) | Free file hosting — sharing, folder distribution, API |
| [Gofile](reference/gofile.md) | Anonymous unlimited-size hosting — REST API |
| [Mega.nz](reference/mega-nz.md) | Encrypted cloud storage — MEGAcmd CLI, Python SDK |
| [Smash](reference/smash.md) | Large file transfer — unlimited size, Node.js SDK |
| [URL Shorteners](reference/url-shorteners.md) | Shrink.pe, ShrinkEarn, self-hosting (YOURLS, Shlink, Kutt) |
| [Platforms & Communities](reference/platforms-and-communities.md) | Social platforms, cybersec news, threat intel, HL Gaming Official |

---

## 📈 Repository Stats

| Metric | Value |
|--------|-------|
| **Total Documents** | 105 |
| **Categories** | 18 |

---

## ⚖️ Disclaimer

All security-related content is for **educational and authorized testing purposes only**.
