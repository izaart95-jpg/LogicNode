# Hacker Roadmap & Security Resource Collections

A curated index of hacking roadmaps, awesome lists, and security resource hubs — for structured learning, tool discovery, and research reference.

---

## Table of Contents
1. [Hacker Roadmap — sundowndev](#1-hacker-roadmap--sundowndev)
2. [Awesome Hacking — Hack-with-Github](#2-awesome-hacking--hack-with-github)
3. [Awesome Windows — Hack-with-Github](#3-awesome-windows--hack-with-github)
4. [Arcanum AI Security Resource Hub](#4-arcanum-ai-security-resource-hub)
5. [0xor0ne Awesome List](#5-0xor0ne-awesome-list)
6. [Learning Path Recommendations](#6-learning-path-recommendations)

---

## 1. Hacker Roadmap — sundowndev

- **Repository:** https://github.com/sundowndev/hacker-roadmap
- **Stars:** 5k+
- **Type:** Structured visual roadmap for learning offensive security

### Overview

A guide for amateurs in pen testing and a summary of hacking tools to practice ethical hacking. The roadmap organizes the offensive security learning journey into phases, each with tool and concept recommendations.

### Roadmap Phases

```
Phase 1 — Foundations
  Linux CLI proficiency
  Networking fundamentals (TCP/IP, DNS, HTTP)
  Programming basics (Python, Bash)
  Web technologies (HTML, JS, HTTP headers)

Phase 2 — Reconnaissance
  Passive OSINT: WHOIS, DNS, social media footprinting
  Active scanning: Nmap, Masscan
  Service enumeration: Gobuster, ffuf, Nikto
  Subdomain enumeration: Amass, Subfinder

Phase 3 — Exploitation
  Web vulnerabilities: SQLi, XSS, SSRF, LFI/RFI
  Service exploitation: Metasploit, SearchSploit
  Password attacks: Hydra, Hashcat, John
  Buffer overflows and binary exploitation

Phase 4 — Post-Exploitation
  Privilege escalation: LinPEAS, WinPEAS, GTFOBins
  Lateral movement and pivoting
  Data exfiltration techniques
  Persistence mechanisms

Phase 5 — Advanced
  Active Directory attacks
  Kernel exploitation
  Custom exploit development
  Red team operations
```

### Tools Mapped in Roadmap

| Category | Tools |
|----------|-------|
| Scanning | Nmap, Masscan, Shodan |
| Web | Burp Suite, OWASP ZAP, SQLmap |
| Exploitation | Metasploit, ExploitDB |
| Password | Hydra, Hashcat, Medusa |
| Wireless | Aircrack-ng, Wifite |
| Forensics | Volatility, Autopsy |

---

## 2. Awesome Hacking — Hack-with-Github

- **Repository:** https://github.com/Hack-with-Github/Awesome-Hacking
- **Type:** Meta-list of awesome security lists
- **Stars:** 10k+

### Overview

A collection of awesome lists for hackers, pentesters, and security researchers — an index of other curated repositories organized by topic.

### Categories Covered

- Awesome Security — general security resources
- Awesome CTF — capture the flag resources and tools
- Awesome Malware Analysis — RE, sandboxes, YARA rules
- Awesome Pentest — penetration testing tools and resources
- Awesome Vulnerability Research
- Awesome Fuzzing
- Awesome Honeypots
- Awesome Incident Response
- Awesome PCAP Tools
- Awesome Threat Intelligence
- Awesome Web Hacking
- Awesome Linux Containers (security perspective)
- Awesome Reversing

---

## 3. Awesome Windows — Hack-with-Github

- **Repository:** https://github.com/Hack-with-Github/Windows
- **Type:** Windows hacking and exploitation resource collection
- **Stars:** 3k+

### What It Covers

A collection of resources for Windows exploitation, privilege escalation, and Windows internals for security researchers.

**Subcategories:**
- Windows exploitation techniques (kernel, user-mode)
- Windows privilege escalation checklists
- Windows persistence methods
- Active Directory attacks
- Windows malware analysis
- Windows security tools
- PowerShell for offense (PowerSploit, Nishang)
- Windows forensics
- Hypervisor/VM escape research

**Key referenced tools:**
- **Sysinternals Suite** — Process Monitor, Process Explorer, Autoruns, TCPView
- **PowerSploit** — PowerShell post-exploitation framework
- **Nishang** — PowerShell attack scripts and tools
- **WinPEAS** — Windows privilege escalation enumeration
- **SharpHound/BloodHound** — AD attack path enumeration
- **Mimikatz** — credential dumping
- **Empire** — post-exploitation C2 framework

---

## 4. Arcanum AI Security Resource Hub

- **Website:** https://arcanum-sec.github.io/ai-sec-resources/
- **Type:** Curated AI/ML security research resource hub

### Overview

A structured reference hub for AI security — covering adversarial attacks on ML models, LLM security (prompt injection, jailbreaks), AI red teaming, and ML model security research.

### Resource Categories

**LLM / Generative AI Security:**
- Prompt injection attack techniques and defenses
- Jailbreaking research and papers
- LLM red teaming methodologies
- RAG (Retrieval-Augmented Generation) attack surfaces
- Agent security — tool use exploitation, indirect prompt injection

**Adversarial Machine Learning:**
- Adversarial examples — crafting inputs that fool classifiers
- Evasion attacks (test time) vs. poisoning attacks (training time)
- Backdoor attacks in neural networks
- Robustness benchmarks and defenses

**Model Extraction & Privacy:**
- Model stealing attacks — reconstructing models via queries
- Membership inference attacks — determine if data was in training set
- Differential privacy techniques
- Federated learning security

**AI Red Teaming:**
- MITRE ATLAS framework (Adversarial Threat Landscape for AI Systems)
- Microsoft AI Red Team methodology
- OWASP Top 10 for LLMs
- Automated red teaming tools for LLMs

**Papers and Courses:**
- Foundational adversarial ML papers (Goodfellow et al., Carlini & Wagner)
- Recent LLM security research
- University courses on ML security

---

## 5. 0xor0ne Awesome List

- **Repository:** https://github.com/0xor0ne/awesome-list
- **Type:** Personal curated security awesome list
- **Focus:** Deep technical security — binary exploitation, RE, kernel, fuzzing, hardware

### Overview

A personal, opinionated collection of security resources with emphasis on low-level and advanced topics: binary exploitation, kernel security, hardware hacking, fuzzing, and vulnerability research.

### Key Sections

- **Binary Exploitation** — heap exploitation, ROP, kernel exploitation, browser pwn
- **Fuzzing** — AFL++, LibFuzzer, coverage-guided fuzzing, grammar fuzzing
- **Reverse Engineering** — static analysis, dynamic analysis, decompilers, emulators
- **Kernel Security** — Linux kernel exploitation, Windows kernel, mitigations
- **Hardware Security** — side-channel attacks, JTAG, firmware analysis, SoC security
- **CTF Resources** — writeup archives, challenge platforms
- **Malware Analysis** — sandboxes, YARA, IDA/Ghidra plugins
- **Network Security** — protocol fuzzing, ICS/SCADA security
- **Web Security** — advanced web exploitation, browser security

---

## 6. Learning Path Recommendations

### Beginner → CTF Player
```
1. OverTheWire Bandit (Linux basics)
2. OverTheWire Natas (web security)
3. PicoCTF (beginner CTF)
4. TryHackMe learning paths
5. HackTheBox Starting Point
```

### CTF → Penetration Tester
```
1. RPISEC MBE (binary exploitation)  ← see exploit-development.md
2. HackTheBox Pro Labs (network pentesting)
3. eLearnSecurity eCPPT or OSCP
4. Web: PortSwigger Web Security Academy (free)
5. AD: HackTheBox Pro Labs (Offshore, RastaLabs)
```

### Pentester → Security Researcher
```
1. Kernel exploitation (ret2usr, heap spray, SMEP/SMAP bypass)
2. Browser exploitation research
3. Fuzzing with AFL++ / LibFuzzer
4. CVE research — read patch diffs
5. Publish findings — write CVE reports, contribute to Metasploit
```

### Platforms

| Platform | Type | Cost |
|----------|------|------|
| **HackTheBox** | Machines, Pro Labs | Free + Pro |
| **TryHackMe** | Guided learning paths | Free + Premium |
| **PortSwigger Academy** | Web security labs | Free |
| **PentesterLab** | Web + code review | Free + Pro |
| **pwn.college** | Binary exploitation | Free |
| **exploit.education** | Exploit development VMs | Free |
| **Hack The Box CTF** | Competition CTFs | Free |
| **CTFtime** | CTF event tracker | Free |

---

## See Also

- [Exploit Development](exploit-development.md) — Binary exploitation, MBE, HSEVD
- [Offensive Frameworks](offensive-frameworks.md) — fsociety, AutoSploit, WinPwn, and more
- [Binary Analysis](binary-analysis.md) — angr, Qiling, radare2, reverse engineering tools
- [Penetration Testing Tools](penetration-testing-tools.md) — Nmap, Metasploit, Burp Suite
- [OSINT Platforms](osint-platforms.md) — Shodan, Censys, ZoomEye
