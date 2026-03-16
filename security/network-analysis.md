# Network Analysis — Zeek (formerly Bro)

Network traffic analysis, intrusion detection, and protocol dissection tools.

---

## Table of Contents
1. [Zeek (formerly Bro)](#1-zeek-formerly-bro)
2. [Network Analysis Workflow](#2-network-analysis-workflow)
3. [Zeek Scripting](#3-zeek-scripting)
4. [Related Tools](#4-related-tools)

---

## 1. Zeek (formerly Bro)

- **Website:** https://zeek.org
- **Repository:** https://github.com/zeek/zeek
- **License:** BSD
- **Type:** Network security monitoring and traffic analysis framework
- **Language:** C++ (engine) + Zeek scripting language (analysis logic)

### Overview

Zeek (renamed from Bro in 2018) is a passive network traffic analyzer. Unlike IDS tools such as Snort or Suricata that match against rule signatures, Zeek generates structured logs describing all observed network activity — connections, DNS queries, HTTP requests, TLS certificates, file transfers, and more. Analysts use these logs for threat hunting, incident response, and forensics.

Zeek operates at the application layer, fully parsing dozens of protocols and producing rich structured output rather than raw packet captures.

### What Zeek Produces

```
Default log files generated per session:
  conn.log         — Every TCP/UDP/ICMP connection (duration, bytes, state)
  dns.log          — All DNS queries and responses
  http.log         — HTTP requests/responses (URI, method, status, user-agent)
  ssl.log          — TLS handshakes (cert subject, issuer, version, cipher)
  x509.log         — Certificate details
  files.log        — Files transferred (MD5/SHA1/SHA256 hashes)
  smtp.log         — Email headers and metadata
  ftp.log          — FTP commands
  ssh.log          — SSH connections (auth attempts, versions)
  dhcp.log         — DHCP leases
  kerberos.log     — Kerberos auth events
  rdp.log          — RDP sessions
  smb_files.log    — SMB file operations
  weird.log        — Protocol anomalies and unexpected behavior
  notice.log       — Policy violations and alerts (from scripts)
  intel.log        — Threat intelligence matches
```

### Installation

```bash
# Ubuntu/Debian
echo 'deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_22.04/ /' \
  | sudo tee /etc/apt/sources.list.d/zeek.list
curl -fsSL https://download.opensuse.org/repositories/security:zeek/xUbuntu_22.04/Release.key \
  | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/zeek.gpg > /dev/null
sudo apt update && sudo apt install zeek

# macOS
brew install zeek

# Verify
zeek --version
```

### Basic Usage

```bash
# Live capture on interface
sudo zeek -i eth0

# Analyze a PCAP file (offline)
zeek -r capture.pcap

# With specific scripts
zeek -r capture.pcap local     # Load default scripts from site/local.zeek
zeek -r capture.pcap policy/protocols/http/detect-sqli.zeek

# Output logs in current directory:
ls *.log
# conn.log  dns.log  http.log  ssl.log  files.log  ...

# JSON output (instead of TSV)
zeek -r capture.pcap LogAscii::use_json=T

# Read conn.log
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p proto duration
```

### Log Analysis with zeek-cut

```bash
# zeek-cut: extract specific fields from Zeek logs
zeek-cut -d '\t' id.orig_h id.resp_h id.resp_p duration < conn.log

# Top talkers by bytes
zeek-cut orig_bytes < conn.log | sort -n | tail -20

# All HTTP POST requests
zeek-cut method uri < http.log | grep POST

# Unique DNS queries
zeek-cut query < dns.log | sort -u

# TLS certificates
zeek-cut id.orig_h id.resp_h subject < ssl.log | head -30

# Find large file transfers
zeek-cut filename md5 total_bytes source < files.log | awk '$3 > 1000000'

# Connections to suspicious ports
zeek-cut id.orig_h id.resp_h id.resp_p < conn.log | awk '$3 == 4444'
```

### Key Use Cases

**Threat Hunting:**
```bash
# Long-duration connections (potential C2 beaconing)
zeek-cut id.orig_h id.resp_h duration < conn.log | awk '$3 > 3600' | sort -k3 -n

# DNS over unusual ports (DNS tunneling)
zeek-cut id.orig_h id.resp_p proto query < dns.log | awk '$2 != 53'

# HTTP with unusual user agents (malware)
zeek-cut id.orig_h user_agent < http.log | grep -v "Mozilla\|Chrome\|Safari"

# Self-signed or short-lived certs (phishing, C2)
zeek-cut id.orig_h id.resp_h subject not_valid_after < ssl.log
```

**Incident Response:**
```bash
# All activity from a specific IP
grep "10.0.0.55" conn.log | zeek-cut id.orig_h id.resp_h id.resp_p proto

# All DNS queries from a host
awk '/10.0.0.55/' dns.log | zeek-cut id.orig_h query qtype_name

# File hashes for threat intel lookup
zeek-cut md5 sha256 filename < files.log | grep -v "^-"
```

---

## 2. Network Analysis Workflow

```
1. Capture: tcpdump / Wireshark → save PCAP
   sudo tcpdump -i eth0 -w capture.pcap

2. Parse: zeek -r capture.pcap
   → Generates structured logs

3. Analyze: zeek-cut, grep, awk, or SIEM ingestion
   → Find anomalies, IOCs, traffic patterns

4. Correlate: Join logs across protocols
   → HTTP request + DNS query + conn timing

5. Alert: Zeek scripts / notice.log
   → Automated detection rules

6. Export: Feed into Elasticsearch/Splunk/SIEM
   → Persistent storage, dashboards
```

### With ELK Stack

```bash
# Install Filebeat Zeek module
# /etc/filebeat/modules.d/zeek.yml:
# - module: zeek
#   connection:
#     enabled: true
#     var.paths: ["/opt/zeek/logs/current/conn.log"]

# Zeek logs → Filebeat → Logstash → Elasticsearch → Kibana
```

---

## 3. Zeek Scripting

Zeek has its own event-driven scripting language for writing custom detection and analysis logic.

```zeek
# Detect connections to port 4444 and generate a notice
event connection_established(c: connection) {
    if (c$id$resp_p == 4444/tcp) {
        NOTICE([
            $note = Weird::Activity,
            $conn = c,
            $msg = fmt("Suspicious connection to port 4444 from %s", c$id$orig_h),
            $identifier = cat(c$id$orig_h)
        ]);
    }
}

# Track DNS queries to a watchlist
global suspect_domains: set[string] = {"evil.com", "malware.net"};

event dns_request(c: connection, msg: dns_msg, query: string, ...) {
    if (query in suspect_domains) {
        print fmt("DNS query to suspect domain: %s from %s", query, c$id$orig_h);
    }
}
```

---

## 4. Related Tools

| Tool | Type | Notes |
|------|------|-------|
| **Wireshark** | Interactive PCAP analysis | GUI, protocol dissection |
| **tcpdump** | CLI packet capture | Minimal, scriptable |
| **Suricata** | Signature-based IDS/IPS | Rules-based, high performance |
| **Snort** | Signature-based IDS | The original open IDS |
| **ntopng** | Network flow monitor | Web UI, traffic statistics |
| **Arkime (Moloch)** | PCAP indexing and search | Store/search full PCAP at scale |
| **NetworkMiner** | PCAP artifact extraction | Files, credentials, hosts |
| **RITA** | Zeek log analysis for C2 | Beaconing detection from conn.log |
| **Corelight** | Commercial Zeek | Zeek with support + sensors |

---

## See Also

- [Penetration Testing Tools](penetration-testing-tools.md) — Active scanning and exploitation
- [OSINT Platforms](osint-platforms.md) — Shodan, Censys — internet-wide visibility
- [VPN & ZTNA](../networking/vpn-and-ztna.md) — Network security and isolation
