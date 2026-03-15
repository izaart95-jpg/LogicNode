# Basic Cybersecurity & Penetration Testing Tools

This document provides an overview of widely used cybersecurity, penetration testing, network analysis, and auditing tools. These tools are commonly used by security professionals, researchers, and ethical hackers for authorized testing and security assessments.

⚠️ Use these tools **only on systems you own or have explicit permission to test**.

---

## 1. Nmap

**Nmap (Network Mapper)** is a powerful open-source network scanning tool.

- Port scanning
- Service detection
- OS detection
- Scriptable scanning (NSE)
- Network discovery

Common uses:
- Finding open ports
- Identifying services
- Network inventory

---

## 2. Masscan

**Masscan** is a high-speed port scanner.

- Extremely fast (millions of packets per second)
- Asynchronous scanning
- Large-scale internet scanning

Used for:
- Rapid scanning of large IP ranges

---

## 3. Unicornscan

**Unicornscan** is an asynchronous TCP/UDP scanner.

- Advanced scanning techniques
- Custom packet crafting
- Banner grabbing

---

## 4. Wireshark

**Wireshark** is a graphical packet analyzer.

- Real-time traffic capture
- Protocol analysis
- Deep packet inspection
- Filtering system

Used for:
- Debugging network issues
- Traffic analysis
- Security investigations

---

## 5. tcpdump

**tcpdump** is a command-line packet capture tool.

- Lightweight
- Packet filtering
- PCAP file creation

Often used on:
- Servers
- Remote systems
- Embedded environments

---

## 6. Metasploit

**Metasploit Framework** is an exploitation framework.

- Exploit development
- Payload generation
- Post-exploitation modules
- Auxiliary scanning modules

Common uses:
- Vulnerability validation
- Controlled penetration testing

---

## 7. Burp Suite

**Burp Suite** is a web application security testing tool.

- Intercepting proxy
- Web vulnerability scanner
- Repeater & Intruder tools
- Session handling testing

Used for:
- Web application security testing

---

## 8. John the Ripper

**John the Ripper** is a password cracking tool.

- Offline hash cracking
- Multiple hash format support
- Wordlist and brute-force attacks

---

## 9. Hydra

**THC Hydra** is a network login cracker.

- Online brute-force attacks
- Supports many protocols (FTP, SSH, HTTP, etc.)
- Parallelized attacks

---

## 10. Aircrack-ng

**Aircrack-ng** is a Wi-Fi security auditing suite.

- WPA/WPA2 cracking
- Packet capture
- Deauthentication testing

---

## 11. Kismet

**Kismet** is a wireless network detector and sniffer.

- Passive Wi-Fi detection
- Hidden network discovery
- Wireless intrusion detection

---

## 12. Wifite

**Wifite** automates wireless auditing.

- Automated WPA/WEP testing
- Integrates with Aircrack-ng tools

---

## 13. Fern Wifi Cracker

**Fern Wifi Cracker** is a GUI-based wireless security tool.

- WEP/WPA cracking
- Network scanning
- MITM attack support

---

## 14. Bettercap

**Bettercap** is a network attack and monitoring framework.

- MITM attacks
- ARP spoofing
- DNS spoofing
- Packet sniffing

---

## 15. Arpwatch

**Arpwatch** monitors ARP activity on a network.

- Detects MAC/IP changes
- Identifies suspicious behavior

---

## 16. SQLMap

**SQLMap** automates SQL injection detection and exploitation.

- Database fingerprinting
- Data extraction
- Authentication bypass testing

---

## 17. Social-Engineer Toolkit (SET)

**SET** focuses on social engineering attacks.

- Phishing simulations
- Credential harvesting
- Attack simulations for awareness testing

---

## 18. Netcat

**Netcat (nc)** is a networking utility.

- TCP/UDP connections
- Port scanning
- Reverse shells
- File transfer

Often called:
"The Swiss Army Knife of Networking"

---

## 19. BloodHound

**BloodHound** analyzes Active Directory relationships.

- AD attack path mapping
- Privilege escalation analysis
- Graph-based visualization

---

## 20. Nikto

**Nikto** is a web server scanner.

- Detects outdated software
- Finds misconfigurations
- Identifies known vulnerabilities

---

## 21. CrackMapExec (CME)

**CrackMapExec** is a post-exploitation tool for Windows networks.

- SMB enumeration
- Credential validation
- Lateral movement support
- Active Directory auditing

---

## 22. Hashcat

**Hashcat** is a high-performance password recovery tool.

- GPU-accelerated cracking
- Supports many hash types
- Dictionary, rule-based, and brute-force modes

---

# Tool Categories Summary

## Network Scanning
- Nmap
- Masscan
- Unicornscan

## Packet Analysis
- Wireshark
- tcpdump

## Exploitation Frameworks
- Metasploit
- Bettercap

## Password Cracking
- John the Ripper
- Hashcat
- Hydra

## Wireless Auditing
- Aircrack-ng
- Kismet
- Wifite
- Fern Wifi Cracker

## Web Application Testing
- Burp Suite
- SQLMap
- Nikto
- OWASP ZAP

## Social Engineering
- Social-Engineer Toolkit

## Active Directory
- BloodHound
- CrackMapExec

## Networking Utilities
- Netcat
- Arpwatch

---

## 23. OWASP ZAP (Zed Attack Proxy)

**OWASP ZAP** is a free, open-source web application security scanner maintained by the OWASP Foundation.

- Intercepting proxy (like Burp Suite, but free)
- Automated vulnerability scanning
- Active and passive scanning modes
- API testing support
- Spidering/crawling
- Fuzzing
- WebSocket testing
- CI/CD integration via CLI/API

```bash
# Install
sudo apt install zaproxy
# Or download from https://www.zaproxy.org/download/

# Quick scan from CLI
zap-cli quick-scan --self-contained --start-options '-config api.disablekey=true' http://target.com
```

> **See Also:** [Web Application Security](web-application-security.md) for the full OWASP Top 10, OFFSEC certifications, and HackTheBox guide

---

# Final Note

These tools are powerful and widely used in:

- Ethical hacking
- Penetration testing
- Red teaming
- Blue team monitoring
- Security research

Always follow:
- Legal guidelines
- Organizational policies
- Responsible disclosure practices

Unauthorized use can result in serious legal consequences.