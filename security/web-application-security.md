# Web Application Security

A comprehensive guide to web application security resources, training platforms, and certification paths. This document covers the OWASP project and its essential tools, OffSec's training methodology and certifications, and hands-on hacking platforms like HackTheBox for building practical offensive security skills.

> **Disclaimer:** All tools, techniques, and platforms described in this document are intended for **authorized security testing and educational purposes only**. Unauthorized access to computer systems is illegal. Always obtain explicit written permission before testing any system you do not own.

---

## Table of Contents

1. [OWASP (Open Web Application Security Project)](#1-owasp-open-web-application-security-project)
2. [OFFSEC (Offensive Security)](#2-offsec-offensive-security)
3. [HackTheBox](#3-hackthebox)
4. [Comparison Table](#4-comparison-table)
5. [See Also](#5-see-also)

---

## 1. OWASP (Open Web Application Security Project)

### 1.1 What is OWASP?

OWASP is a nonprofit foundation dedicated to improving the security of software. It operates as an open community where anyone can participate in projects, events, and discussions related to application security. OWASP produces freely available tools, documentation, standards, and methodologies used worldwide by developers, security professionals, and organizations.

- **Website:** https://owasp.org
- **Founded:** 2001
- **License:** All materials are free and open source
- **Community:** Hundreds of local chapters globally, annual conferences (AppSec Global, regional events)

### 1.2 OWASP Top 10 (2021)

The OWASP Top 10 is the most widely recognized awareness document for web application security. It represents a broad consensus about the most critical security risks.

| Rank | Category | Description |
|------|----------|-------------|
| A01 | **Broken Access Control** | Restrictions on authenticated users are not properly enforced, allowing access to unauthorized functions or data |
| A02 | **Cryptographic Failures** | Failures related to cryptography that lead to exposure of sensitive data (formerly Sensitive Data Exposure) |
| A03 | **Injection** | SQL, NoSQL, OS command, LDAP injection where untrusted data is sent as part of a command or query |
| A04 | **Insecure Design** | Missing or ineffective security controls due to flawed design patterns and architecture |
| A05 | **Security Misconfiguration** | Insecure default configs, incomplete setups, open cloud storage, verbose error messages, missing hardening |
| A06 | **Vulnerable and Outdated Components** | Using components with known vulnerabilities or unsupported/out-of-date software |
| A07 | **Identification and Authentication Failures** | Broken authentication, session management, and identity verification (formerly Broken Authentication) |
| A08 | **Software and Data Integrity Failures** | Code and infrastructure that does not protect against integrity violations (includes insecure deserialization) |
| A09 | **Security Logging and Monitoring Failures** | Insufficient logging, detection, monitoring, and active response to breaches |
| A10 | **Server-Side Request Forgery (SSRF)** | Application fetches remote resources without validating user-supplied URLs |

### 1.3 OWASP ZAP (Zed Attack Proxy)

ZAP is OWASP's flagship open-source web application security scanner. It acts as a man-in-the-middle proxy to intercept and inspect traffic between the browser and the target application.

**Installation:**

```bash
# Debian/Ubuntu
sudo apt install zaproxy

# Snap
sudo snap install zaproxy --classic

# Docker
docker pull ghcr.io/zaproxy/zaproxy:stable

# Download from official site
# https://www.zaproxy.org/download/
```

**Basic Automated Scan:**

```bash
# Quick scan against a target URL
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t https://target.example.com
```

**Authenticated Scan (CLI):**

```bash
# Full scan with authentication context
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py \
  -t https://target.example.com \
  -U username \
  -n context_file.context
```

**API Scan (OpenAPI/Swagger):**

```bash
# Scan an API defined by an OpenAPI spec
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-api-scan.py \
  -t https://target.example.com/openapi.json \
  -f openapi
```

**ZAP CLI Usage:**

```bash
# Start ZAP in daemon mode
zap.sh -daemon -port 8080 -config api.key=your-api-key

# Use the ZAP CLI client
zap-cli quick-scan --self-contained --start-options '-config api.key=12345' \
  http://target.example.com
```

### 1.4 OWASP Testing Guide

The OWASP Web Security Testing Guide (WSTG) is a comprehensive resource for testing web application security. It provides a framework of best practices and detailed test cases organized by category (authentication, authorization, session management, input validation, etc.). The current version is WSTG v4.2, available at https://owasp.org/www-project-web-security-testing-guide/.

### 1.5 OWASP ASVS (Application Security Verification Standard)

ASVS provides a basis for testing web application technical security controls and a list of requirements for secure development. It defines three verification levels:

- **Level 1:** Low-assurance applications (minimum baseline)
- **Level 2:** Applications containing sensitive data (recommended for most apps)
- **Level 3:** Critical applications (e.g., medical, military, financial infrastructure)

ASVS is commonly used for defining security requirements, guiding security architecture, and as a checklist for code reviews and penetration tests.

---

## 2. OFFSEC (Offensive Security)

### 2.1 Company Overview

OffSec (formerly Offensive Security) is a leading cybersecurity training and certification company known for its rigorous, hands-on approach to security education. Their motto "Try Harder" reflects a philosophy of persistence and independent problem-solving. OffSec maintains Kali Linux, the most widely used penetration testing distribution.

- **Website:** https://www.offsec.com
- **Founded:** 2007
- **Known for:** Performance-based certification exams (no multiple choice)

### 2.2 Key Certifications

#### OSCP (PEN-200) — Offensive Security Certified Professional

- The most recognized entry-level penetration testing certification
- Covers network enumeration, exploitation, privilege escalation, Active Directory attacks
- 24-hour hands-on exam: compromise machines in a lab environment
- Prerequisite: solid Linux, networking, and scripting fundamentals

#### OSWA (WEB-200) — Offensive Security Web Assessor

- Focused on web application security testing
- Covers common web vulnerabilities, authentication attacks, injection techniques
- Hands-on exam testing real web application exploitation

#### OSEP (PEN-300) — Offensive Security Experienced Penetration Tester

- Advanced penetration testing: evasion, custom exploits, advanced Active Directory
- Builds on OSCP with deeper exploitation techniques
- 48-hour exam scenario

#### OSED (EXP-301) — Offensive Security Exploit Developer

- Windows exploit development: buffer overflows, SEH, DEP/ASLR bypass, ROP chains
- Requires strong assembly and debugging knowledge
- 48-hour exam developing working exploits

### 2.3 Kali Linux

OffSec maintains Kali Linux, the industry-standard penetration testing Linux distribution. Kali comes pre-loaded with hundreds of security tools organized by category (information gathering, vulnerability analysis, exploitation, etc.). Available as ISO, VM, ARM images, WSL, Docker, and cloud marketplace images.

```bash
# Update Kali Linux
sudo apt update && sudo apt full-upgrade -y

# Install specific tool categories (metapackages)
sudo apt install kali-tools-web
sudo apt install kali-tools-exploitation
```

### 2.4 OffSec Proving Grounds

Proving Grounds is OffSec's practice lab environment with vulnerable machines for hands-on training:

- **PG Play:** Free tier with community-created machines
- **PG Practice:** Paid tier with OffSec-curated machines (retirement machines from OSCP labs)
- Machines range from beginner to advanced difficulty
- Walkthroughs available for completed machines

---

## 3. HackTheBox

### 3.1 Platform Overview

HackTheBox (HTB) is a gamified cybersecurity training platform offering vulnerable machines, challenges, and structured learning paths. It features CTF-style challenges alongside realistic enterprise-level scenarios, making it suitable for beginners through advanced practitioners.

- **Website:** https://www.hackthebox.com
- **Community:** 2M+ members
- **Content:** 500+ machines, 300+ challenges, endgame scenarios

### 3.2 Getting Started

```bash
# 1. Create an account at https://app.hackthebox.com

# 2. Download your VPN connection file from the platform
# Access -> OpenVPN -> Download VPN

# 3. Connect to the HTB network
sudo openvpn lab_username.ovpn

# 4. Verify connectivity
ping 10.10.10.x

# 5. Start with "Starting Point" machines (guided, beginner-friendly)
```

### 3.3 Machine Workflow

The standard approach to HTB machines follows a structured methodology:

1. **Enumerate:** Scan ports, identify services, discover directories and subdomains
2. **Exploit:** Identify vulnerabilities, develop or use exploits to gain initial access
3. **Escalate:** Enumerate the system internally, find privilege escalation vectors
4. **Submit Flags:** Retrieve user.txt and root.txt flag files, submit hashes on the platform

```bash
# Example initial enumeration
nmap -sC -sV -oN scan.txt 10.10.10.x
gobuster dir -u http://10.10.10.x -w /usr/share/wordlists/dirb/common.txt
```

### 3.4 Learning Tracks

| Track | Focus | Target Audience |
|-------|-------|-----------------|
| **Penetration Tester** | End-to-end pentesting methodology | Aspiring pentesters |
| **Bug Bounty Hunter** | Web vulnerability discovery and exploitation | Bug bounty hunters |
| **Red Team Operator** | Advanced adversary simulation, evasion, C2 | Experienced professionals |

### 3.5 HTB Academy

HTB Academy is the structured learning side of HackTheBox, offering module-based courses with theory, examples, and hands-on exercises. Modules range from fundamental topics (Linux, networking) to advanced topics (Active Directory, binary exploitation). Students earn "cubes" to unlock modules and can progress through guided skill paths.

### 3.6 Comparison with Other Platforms

| Feature | HackTheBox | TryHackMe | PortSwigger Web Security Academy |
|---------|-----------|-----------|----------------------------------|
| **Difficulty** | Intermediate to Advanced | Beginner to Intermediate | Beginner to Advanced (web only) |
| **Focus** | Full-spectrum pentesting | Guided learning, broad topics | Web application security |
| **Format** | Machines + Challenges | Rooms with step-by-step guides | Labs with detailed explanations |
| **Free Content** | Limited (retired machines) | Many free rooms | Fully free |
| **VPN Required** | Yes | Yes (or browser-based) | No (browser-based labs) |
| **Best For** | Skill sharpening, exam prep | Learning fundamentals | Deep web security knowledge |

---

## 4. Comparison Table

| Platform | Type | Certifications | Free Tier | Best For |
|----------|------|---------------|-----------|----------|
| **OWASP** | Community / Standards | N/A (provides standards) | Fully free | Developers, auditors, policy makers |
| **OWASP ZAP** | Web App Scanner | N/A | Fully free (open source) | Automated web security scanning |
| **OffSec** | Training / Certifications | OSCP, OSWA, OSEP, OSED | PG Play (limited) | Career pentesters, certification seekers |
| **HackTheBox** | Practice Platform | HTB CPTS, HTB CBBH | Limited free machines | Hands-on skill building, CTF practice |
| **TryHackMe** | Learning Platform | N/A | Many free rooms | Beginners, structured learning |
| **PortSwigger Academy** | Web Security Labs | N/A | Fully free | Web application security deep dive |

---

## 5. See Also

- [Penetration Testing Tools](penetration-testing-tools.md) — Core tools for network and application security testing
- [OPSEC and Proxies](opsec-and-proxies.md) — Operational security, anonymization, and proxy management
