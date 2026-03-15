# HTTP vs HTTPS — and the TLS/SSL Stack

A focused deep dive into how HTTP and HTTPS differ, what TLS actually does at every step, and the full certificate trust chain.

---

## Table of Contents
1. [HTTP — The Naked Protocol](#1-http--the-naked-protocol)
2. [HTTPS — HTTP Inside TLS](#2-https--http-inside-tls)
3. [What TLS Actually Protects](#3-what-tls-actually-protects)
4. [SSL vs TLS — Version History](#4-ssl-vs-tls--version-history)
5. [TLS 1.3 Handshake — Step by Step](#5-tls-13-handshake--step-by-step)
6. [TLS 1.2 Handshake — Legacy](#6-tls-12-handshake--legacy)
7. [Certificates & the Trust Chain](#7-certificates--the-trust-chain)
8. [Cipher Suites](#8-cipher-suites)
9. [Certificate Authorities & PKI](#9-certificate-authorities--pki)
10. [HSTS, HPKP & Certificate Transparency](#10-hsts-hpkp--certificate-transparency)
11. [Common Attacks & Mitigations](#11-common-attacks--mitigations)
12. [Inspecting TLS in Practice](#12-inspecting-tls-in-practice)

---

## 1. HTTP — The Naked Protocol

HTTP is a text-based request/response protocol. Every byte travels in plain text. No encryption, no integrity, no authentication.

### What an HTTP Request Looks Like on the Wire

```
Client → Server (plain text, anyone can read this):

GET /login HTTP/1.1
Host: bank.example.com
Cookie: session=abc123; user=alice
User-Agent: Mozilla/5.0

[blank line ends headers]
```

```
Server → Client (plain text):

HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: session=abc123; Path=/

<form action="/submit-password">
<input name="password" type="password">
```

### Who Can Read This

```
Your device → WiFi router → ISP → backbone routers → destination server

Every hop can read ALL of it:
  Your WiFi router operator
  Your ISP (and anyone they share with)
  Every transit router (~10–20 hops across the internet)
  Any attacker on your local network (ARP poisoning)
  Any BGP hijacker

What they see:
  ✓ Every URL (full path: /account?token=xyz)
  ✓ Every cookie → session hijacking
  ✓ Every form submission (passwords, card numbers)
  ✓ Every response (your private data)
  ✓ They can modify responses: inject ads, malware, redirect to phishing
```

---

## 2. HTTPS — HTTP Inside TLS

HTTPS is HTTP with a TLS layer inserted between TCP and HTTP ( S = Secure). The HTTP protocol itself is unchanged — same headers, methods, status codes. TLS wraps it in an encrypted tunnel.

```
HTTP stack:          HTTPS stack:
  HTTP                 HTTP
  TCP                  TLS   ← inserted here
  IP                   TCP
  Physical             IP
                       Physical
```

### What the Wire Looks Like

```
HTTP wire:
  47 45 54 20 2f 61 63 63 6f 75 6e 74 ...
  G  E  T     /  a  c  c  o  u  n  t    ← fully readable

HTTPS wire (TLS record):
  17 03 03 00 45 a3 f8 2c 9d 1b 44 e7 ...
  ↑  ↑  ↑  ↑  ↑  └──────────────────── encrypted payload
  │  │  │  └──── length (2 bytes)
  │  │  └─────── TLS version (0x03 0x03 = TLS 1.2 record layer)
  │  └────────── legacy (03 = TLS 1.x family)
  └───────────── record type: 0x17 = application data

Without session keys: computationally indistinguishable from random noise.
```

### What HTTPS Guarantees

```
Confidentiality:
  Nobody in the path can read plaintext content.
  ISP sees: "device connected to IP 142.250.x.x"
  ISP cannot see: URL path, cookies, form data, response body.
  Note: ISP still sees the domain via SNI and DNS (unless DoH used).

Integrity:
  Every TLS record has an authentication tag (AEAD).
  Any modification to ciphertext is detected and rejected.
  Attacker cannot inject, delete, or reorder bytes.
  This is a cryptographic guarantee — not "probably safe."

Server Authentication:
  Certificate proves you're talking to the real server.
  Browser verifies: cert is for "bank.example.com",
                    signed by a trusted CA, not expired, not revoked.
  Without this: encrypted tunnel to an impersonator = still dangerous.

Client Authentication (optional — mTLS):
  Server verifies client's certificate too.
  Used in: API-to-API, zero-trust networks.
  Not used in: normal browser HTTPS (password authentication instead).
```

---

## 3. What TLS Actually Protects

```
                          HTTP     HTTPS
──────────────────────────────────────────────────
Destination IP            plain    plain   ISP always sees IP
Destination port          plain    plain   443 = clearly HTTPS
Domain (SNI in handshake) plain    plain*  Sent before encryption
DNS query                 plain    plain** Unless DoH/DoT used
URL path (/login?x=y)     plain    ✓ enc
HTTP headers              plain    ✓ enc
Cookies                   plain    ✓ enc
Request/response body     plain    ✓ enc
Data volume / timing      plain    plain   Traffic analysis still possible

*  ECH (Encrypted Client Hello) encrypts SNI — not yet universal (2026)
** Use DNS-over-HTTPS (DoH) or DNS-over-TLS (DoT) to hide DNS queries
```

---

## 4. SSL vs TLS — Version History

"SSL" and "TLS" are used interchangeably in conversation but are distinct protocols. SSL is entirely dead.

| Version | Year | Status | Reason |
|---------|------|--------|--------|
| SSL 1.0 | 1994 | Never released | Severe vulns found internally |
| SSL 2.0 | 1995 | Dead | DROWN attack, MD5 weakness |
| SSL 3.0 | 1996 | Dead (RFC 7568, 2015) | POODLE attack |
| TLS 1.0 | 1999 | Dead (RFC 8996, 2021) | BEAST, POODLE-TLS, RC4 |
| TLS 1.1 | 2006 | Dead (RFC 8996, 2021) | No meaningful improvements |
| TLS 1.2 | 2008 | Current (still ~40% of traffic) | Safe if properly configured |
| TLS 1.3 | 2018 | Current — use this | All legacy algorithms removed |

**TLS 1.3 key improvements over 1.2:**
- Handshake: 1 RTT (vs 2 RTT) — 0-RTT for resumption
- Removed: RSA key exchange (no PFS), CBC mode, RC4, DES, 3DES, MD5, SHA-1
- All cipher suites are AEAD — no separate MAC
- Certificate is now encrypted in the handshake
- Perfect Forward Secrecy is mandatory (ephemeral DH always)

---

## 5. TLS 1.3 Handshake — Step by Step

TLS 1.3 completes in **1 RTT**. Here is exactly what is exchanged:

```
CLIENT                                          SERVER
──────────────────────────────────────────────────────────────────

→ ClientHello
    TLS versions: [1.3, 1.2]
    Client random: 32 random bytes (nonce)
    Cipher suites: [AES_256_GCM_SHA384, AES_128_GCM_SHA256, CHACHA20_POLY1305]
    Extensions:
      key_share:    x25519 public key A = a × G
                    (a = client's random private scalar,
                     G = Curve25519 base point)
      server_name:  "bank.example.com"  ← still plaintext (SNI)
      alpn:         ["h3", "h2", "http/1.1"]
      signature_algs: [rsa_pss_sha256, ecdsa_secp256r1_sha256]

← ServerHello
    Chosen cipher: TLS_AES_256_GCM_SHA384
    key_share: x25519 public key B = b × G
               (b = server's random private scalar)

── SHARED SECRET DERIVED ──────────────────────────────────────────
    Client computes: K = a × B = a × (b × G) = ab × G
    Server computes: K = b × A = b × (a × G) = ab × G
    Same K. Eavesdropper cannot compute without knowing a or b.
    
    HKDF derivation from K:
      handshake_secret → client_hs_key, server_hs_key
    Everything below is encrypted.
──────────────────────────────────────────────────────────────────

← {EncryptedExtensions}   [encrypted with server_hs_key]
    ALPN selected: h2

← {Certificate}           [encrypted — cert is private in TLS 1.3]
    Leaf cert: CN=bank.example.com, SANs, pubkey, signed by intermediate CA
    Intermediate cert: signed by root CA
    (Root cert NOT sent — client already has it in trust store)

← {CertificateVerify}     [encrypted]
    Signature = Sign(server_private_key, Hash(all_handshake_messages))
    Proves server possesses the private key matching the certificate.

← {Finished}              [encrypted]
    HMAC over entire handshake transcript.
    Proves no tampering with any message.

CLIENT VERIFIES:
    1. Cert chain: leaf → intermediate → root (in system trust store)
    2. Leaf cert CN/SAN matches "bank.example.com"
    3. Not expired
    4. Not revoked (OCSP check)
    5. CertificateVerify signature valid with cert's public key
    6. Finished HMAC matches

→ {Finished}              [encrypted with client_hs_key]
    Client's HMAC. Server verifies.

── APPLICATION KEYS DERIVED ───────────────────────────────────────
    master_secret → client_app_key, server_app_key
    Separate keys per direction. Independent nonce counter per key.
──────────────────────────────────────────────────────────────────

→ {GET /account HTTP/1.1...}   [encrypted with client_app_key]
← {HTTP/1.1 200 OK...}         [encrypted with server_app_key]

Total: 1 RTT before application data.
TLS 1.2 for comparison: 2 RTT.
```

### 0-RTT Resumption

```
Returning connection (server issued a session ticket last time):

→ ClientHello + EarlyData
    psk_identity: ticket from previous session
    binder: HMAC proving PSK possession
    early_data: HTTP request already appended (before server responds!)

← ServerHello + accept_early_data

Data arrives at server before full handshake completes.
0 additional RTT for data.

Caveat: 0-RTT is replayable (same request can be replayed by attacker).
Used only for safe/idempotent requests (GET, not POST).
```

---

## 6. TLS 1.2 Handshake — Legacy

TLS 1.2 requires **2 RTT** before data flows. Still ~40% of HTTPS traffic.

```
CLIENT                                          SERVER
──────────────────────────────────────────────────────────────────

→ ClientHello
    Random, cipher suites, extensions

← ServerHello            ─── RTT 1 begins ───
    Chosen cipher suite, server random

← Certificate            [PLAINTEXT — cert is visible to any observer]
    Full cert chain in clear

← ServerKeyExchange      (only for ECDHE/DHE suites)
    Server's ephemeral DH public key, signed with cert private key

← ServerHelloDone

→ ClientKeyExchange      ─── RTT 1 ends ───
    Client's ephemeral DH public key (ECDHE)
    OR: RSA-encrypted pre-master secret (no PFS — avoid)

→ ChangeCipherSpec        (legacy signal: switching to encrypted now)
→ Finished                HMAC of handshake transcript

← ChangeCipherSpec
← Finished               ─── RTT 2 ───

→ Application Data        ─── RTT 2 ends — data flows ───

Why 2 RTT: server must receive client's DH key (RTT 1 end)
           before both sides can derive keys and send Finished (RTT 2).

TLS 1.3 fix: client sends its DH key share in the FIRST ClientHello.
             Server can derive keys and send Finished in one flight.
             Client sends data in next flight. Saves 1 RTT.
```

---

## 7. Certificates & the Trust Chain

### X.509 Certificate Structure

```
A TLS certificate (ASN.1/DER encoded):

Version:            3 (X.509 v3)
Serial Number:      unique CA-assigned integer
Signature Algorithm: sha256WithRSAEncryption OR ecdsa-with-SHA256
Issuer:             CN=DigiCert TLS RSA SHA256 2020 CA1, O=DigiCert Inc
Validity:
  Not Before:       2024-01-15 00:00:00 UTC
  Not After:        2025-01-15 23:59:59 UTC
Subject:            CN=bank.example.com
Public Key:         EC P-256 public key (65 bytes)

Extensions:
  Subject Alternative Names:
    DNS: bank.example.com
    DNS: www.bank.example.com
    DNS: api.bank.example.com   ← cert covers all these names
  Key Usage: digitalSignature
  Extended Key Usage: serverAuth
  Basic Constraints: CA:FALSE    ← leaf cert, cannot sign other certs
  OCSP URL: http://ocsp.digicert.com
  CT SCTs: [proof this cert is in Certificate Transparency logs]

Signature: [CA's ECDSA/RSA signature over all fields above]
  Anyone can verify: hash(fields) → verify with CA's public key → valid
```

### The Three-Level Trust Chain

```
Root CA  (self-signed, pre-installed in your OS)
  └── Intermediate CA  (signed by Root CA)
        └── Leaf Certificate  (signed by Intermediate CA, held by server)

Verification:
  leaf.signature → verify with intermediate CA's pubkey → valid?
  intermediate.signature → verify with root CA's pubkey → valid?
  root → is it in my trust store? → YES → chain trusted.

Why three levels:
  Root CA private key is offline (HSM in a vault, air-gapped).
  Intermediate CA is online and does the actual daily signing.
  If intermediate is compromised: revoke it, root untouched.
  If root is compromised: catastrophic — everything collapses.

Trust stores:
  macOS:   Keychain → System Roots (~170 root CAs)
  Windows: certmgr → Trusted Root CAs
  Firefox: ships its own store (independent of OS)
  Chrome:  uses OS store on macOS/Windows

Any of the ~170 root CAs can issue a cert for ANY domain.
This is PKI's central weakness. (See DigiNotar attack in §11.)

Certificate types:
  DV (Domain Validated):   prove you control the domain. Free (Let's Encrypt).
                           Issued in seconds. No human review.
  OV (Organization Validated): domain + org identity verified. Days.
  EV (Extended Validation): thorough legal/org verification. Now useless —
                             Chrome and Firefox removed the green bar in 2019.
                             Looks identical to DV in modern browsers.
```

---

## 8. Cipher Suites

A cipher suite = key exchange + authentication + symmetric cipher + hash, packaged as a named identifier.

### TLS 1.3 Suites (only 5, all strong)

```
TLS_AES_256_GCM_SHA384
TLS_AES_128_GCM_SHA256          ← Most common
TLS_CHACHA20_POLY1305_SHA256    ← Preferred on mobile (no AES hardware)
TLS_AES_128_CCM_SHA256
TLS_AES_128_CCM_8_SHA256

Key exchange: always ECDHE (x25519 or P-256) — ephemeral, always PFS
Auth:         always certificate (RSA-PSS or ECDSA)
Cipher:       AES-GCM or ChaCha20-Poly1305 — both AEAD
MAC:          embedded in AEAD — no separate step

TLS 1.3 eliminated the entire category of bad cipher suites.
You cannot configure a weak TLS 1.3 suite — there are none.
```

### TLS 1.2 Suite Naming

```
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
 │    │     │        │   │   │   │
 │    │     │        │   │   │   └── PRF/HMAC hash
 │    │     │        │   │   └────── Mode (GCM)
 │    │     │        │   └────────── Key size
 │    │     │        └────────────── Cipher (AES)
 │    │     └─────────────────────── Auth (RSA cert)
 │    └───────────────────────────── Key exchange (ECDHE = PFS)
 └────────────────────────────────── Protocol

Strong (use):
  TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
  TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
  TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256

Weak (disable):
  TLS_RSA_WITH_AES_128_CBC_SHA       ← RSA key exchange = no PFS
  TLS_RSA_WITH_3DES_EDE_CBC_SHA      ← SWEET32 (64-bit block)
  *_WITH_RC4_*                       ← RC4 broken
  *_EXPORT_*                         ← Deliberately crippled (FREAK)
  *_anon_*                           ← No auth at all
```

### AES-GCM Internals

```
AES-GCM = AES in Counter Mode + GHASH authentication:

Encryption (CTR mode):
  ciphertext[i] = plaintext[i] XOR AES_K(nonce || counter++)
  counter increments for each 16-byte block
  parallelizable — blocks are independent

Authentication (GHASH):
  auth_tag = GHASH(H, AAD, ciphertext)
    H = AES_K(0)  ← hash subkey derived once
    AAD = TLS record header (authenticated but not encrypted)
    Result: 128-bit tag appended to ciphertext

Verification:
  Receiver recomputes auth_tag, compares in constant time.
  One flipped bit → completely different tag → rejected.

Critical: never reuse (key + nonce) pair.
          TLS uses a counter nonce, incrementing per record — safe.
          Reuse = catastrophic (key recovery possible).

Hardware: AES-NI + PCLMULQDQ instructions on x86/ARM
  Intel/AMD: AES-128-GCM at ~1 byte/clock cycle (~3 GB/s per core)
  Apple M-series: dedicated AES hardware → ~50 GB/s
```

---

## 9. Certificate Authorities & PKI

### Domain Validation (DV) — How It Works

```
ACME protocol (RFC 8555) — used by Let's Encrypt and others:

Challenge types:

HTTP-01:
  CA says: "serve this token at http://yourdomain.com/.well-known/acme-challenge/TOKEN"
  CA fetches it → proves you control port 80 on that domain
  Cannot issue wildcard certs (*.domain.com)

DNS-01:
  CA says: "add TXT record: _acme-challenge.yourdomain.com = TOKEN"
  CA queries DNS → proves you control DNS for the domain
  CAN issue wildcard certs
  Works for internal/non-public domains

TLS-ALPN-01:
  CA connects to your :443 server
  Verifies a specially crafted certificate via TLS
  Proves you control TLS on the domain
```

### Let's Encrypt — Free Automated Certs

```bash
# certbot (standard)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Certs at:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem

# Auto-renewal (added by certbot automatically)
sudo certbot renew --dry-run

# acme.sh (lightweight, no root required)
curl https://get.acme.sh | sh
acme.sh --issue -d yourdomain.com --webroot /var/www/html
acme.sh --install-cert -d yourdomain.com \
  --fullchain-file /etc/nginx/ssl/fullchain.pem \
  --key-file /etc/nginx/ssl/key.pem \
  --reloadcmd "systemctl reload nginx"
```

### Nginx TLS Configuration (Modern)

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # TLS versions
    ssl_protocols TLSv1.2 TLSv1.3;

    # Cipher suites (TLS 1.2 only — TLS 1.3 suites are auto)
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;  # Let client choose (TLS 1.3 handles this)

    # Session resumption
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;        # Disable tickets (PFS concern)

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 1.1.1.1 valid=300s;
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;   # Redirect HTTP → HTTPS
}
```

---

## 10. HSTS, HPKP & Certificate Transparency

### HSTS — HTTP Strict Transport Security

```
Problem: User types "bank.com" → browser tries HTTP first
         SSL stripping attack: MITM intercepts HTTP, strips the 301 redirect,
         serves fake HTTP page. User never reaches HTTPS.

Header (sent over HTTPS):
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

Effect:
  Browser records: "bank.com must be HTTPS for the next year"
  Even typing http:// → browser internally converts to https://
  Before making any HTTP connection — no window for stripping

preload directive:
  Submit to https://hstspreload.org
  Chrome/Firefox/Safari ship with a hardcoded list of HSTS-preloaded domains
  First visit: already HTTPS — SSL stripping impossible from day one

max-age guideline:
  Start with max-age=300 (5 minutes) for testing
  Increase to max-age=31536000 (1 year) + preload once stable
  Warning: if you ever need to drop HTTPS, you're locked in for max-age seconds
```

### Certificate Transparency (CT)

```
Problem: rogue CA issues cert for google.com without Google's knowledge
         Traditional PKI: no mechanism to detect this

CT solution:
  All publicly trusted CAs must log every issued cert to public CT logs
  CT log = append-only Merkle tree (tampering detectable)
  Cert includes SCTs (Signed Certificate Timestamps) = proof it was logged
  Browser checks for valid SCTs → rejects certs not in logs (Chrome since 2018)

Effect:
  Anyone can monitor CT logs for their own domains
  Rogue cert issued → visible in CT within minutes → domain owner alerted
  DigiNotar-style attacks now detectable in near real-time

Check your domain:
  https://crt.sh/?q=yourdomain.com
  Shows every cert ever issued for your domain
  Check for unexpected issuances
```

### HPKP (Deprecated)

```
HTTP Public Key Pinning: removed from Chrome 2017, Firefox 2018.
Was: pin specific public key hashes in response header.
Failed: one misconfiguration = permanent lockout from your own site.
Replacement: CT handles the same threat more safely.
```

---

## 11. Common Attacks & Mitigations

### SSL Stripping

```
Attack:
  MITM between client and server.
  Client requests http://bank.com → MITM intercepts.
  MITM forwards to bank.com over HTTPS, strips HTTPS from response.
  Client communicates over HTTP with MITM, MITM forwards over HTTPS to server.
  Client never sees the padlock.

Mitigation:
  HSTS: browser refuses all HTTP connections to the domain.
  HSTS Preload: even first visit uses HTTPS — no initial HTTP request.
```

### POODLE (2014, CVE-2014-3566)

```
Affects: SSL 3.0 (and TLS 1.0 in some implementations)
Attack: padding oracle on CBC mode → leak plaintext one byte at a time
Fix: disable SSL 3.0 and TLS 1.0 (done by all browsers 2020–2021)
     Use AEAD ciphers (mandatory in TLS 1.3)
```

### HEARTBLEED (2014, CVE-2014-0160)

```
Not a protocol flaw — OpenSSL implementation bug in Heartbeat extension.
Client: "echo back 64KB of data"
Bug: OpenSSL didn't validate requested length vs actual data.
Server returned 64KB of its own memory: private keys, passwords, session tokens.
Fix: patch OpenSSL. ~200,000 servers reportedly still unpatched as of 2024.
```

### BEAST (2011)

```
Affects: TLS 1.0, CBC mode, specific browser/server combos
Attack: chosen plaintext IV prediction in CBC → decrypt session cookies
Fix: TLS 1.1+ with explicit random IVs, or TLS 1.3
```

### FREAK / Logjam (2015)

```
Attack: MITM downgrades cipher suite to "EXPORT" grade
        (512-bit RSA/DH — deliberately weakened for US 1990s export law)
        512-bit RSA factorable in hours
Fix: disable all EXPORT cipher suites (done everywhere)
```

### Certificate Misissuance

```
DigiNotar (2011):
  Dutch CA hacked → attacker issued cert for *.google.com
  Used to intercept traffic of ~300,000 Iranians
  DigiNotar removed from all trust stores immediately
  Company went bankrupt within weeks

Symantec (2017):
  Issued thousands of invalid certs (including for google.com)
  Google distrusted all Symantec-issued certs (sunset complete 2018)
  ~1% of all HTTPS sites had to replace their certs

CT prevents future large-scale misissuance from going undetected.
```

### renegotiation Attack (CVE-2009-3555)

```
Flaw in TLS renegotiation: attacker could inject data at start of TLS session.
Fix: RFC 5746 (Secure Renegotiation extension) — deployed 2010.
TLS 1.3 removed renegotiation entirely.
```

---

## 12. Inspecting TLS in Practice

### openssl s_client

```bash
# Full handshake inspection
openssl s_client -connect google.com:443 -servername google.com

# Key output lines:
# Protocol  : TLSv1.3
# Cipher    : TLS_AES_256_GCM_SHA384
# Server public key is 256 bit (ECDSA P-256)

# Force specific TLS version
openssl s_client -connect google.com:443 -tls1_3
openssl s_client -connect google.com:443 -tls1_2

# View certificate details
openssl s_client -connect google.com:443 2>/dev/null \
  | openssl x509 -text -noout

# Check expiry
openssl s_client -connect google.com:443 2>/dev/null \
  | openssl x509 -noout -dates

# Check specific cipher support
openssl s_client -connect google.com:443 \
  -cipher 'ECDHE-RSA-AES128-GCM-SHA256' 2>/dev/null | grep Cipher
```

### nmap SSL scan

```bash
# Enumerate all TLS versions and cipher suites
nmap --script ssl-enum-ciphers -p 443 google.com

# Output:
# TLSv1.2:
#   TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
# TLSv1.3:
#   TLS_AES_128_GCM_SHA256 (ecdh_x25519) - A
# Least strength: A
```

### testssl.sh (comprehensive audit)

```bash
git clone https://github.com/drwetter/testssl.sh.git && cd testssl.sh

# Full scan: TLS versions, ciphers, cert, HSTS, vulnerabilities
./testssl.sh google.com

# Checks: BEAST, POODLE, HEARTBLEED, ROBOT, FREAK, LOGJAM,
#         DROWN, TICKETBLEED, SWEET32, and more

# Online equivalent: https://www.ssllabs.com/ssltest/
```

### Browser DevTools

```
Chrome / Safari: DevTools → Security tab
  → Shows: TLS 1.3, X25519, AES_128_GCM, cert validity

Firefox: padlock → Connection Secure → More Information
  → TLS version, cipher suite, certificate chain

Check for rogue certs on your domain:
  https://crt.sh/?q=yourdomain.com
  (shows every cert ever issued for your domain via CT logs)
```

### Wireshark TLS Decryption (with session keys)

```bash
# Chrome/Firefox write session keys when SSLKEYLOGFILE is set
export SSLKEYLOGFILE=~/tls_session_keys.log
google-chrome &

# In Wireshark:
# Edit → Preferences → Protocols → TLS
# Set "(Pre)-Master-Secret log filename" to ~/tls_session_keys.log
# Now Wireshark decrypts TLS traffic in real time

# This works because you have the session keys.
# Passive eavesdroppers without keys see only ciphertext.
```

---

## Quick Reference

```
HTTP:   port 80, plain text, no security
HTTPS:  port 443, HTTP inside TLS

TLS 1.3:  use this (1 RTT, AEAD only, PFS mandatory)
TLS 1.2:  acceptable if configured correctly
TLS ≤1.1: dead, broken, disabled everywhere

TLS protects:  URL path, headers, cookies, body
TLS exposes:   destination IP, domain (SNI), traffic timing

Free certs:    Let's Encrypt (certbot, acme.sh, caddy auto)
Check your TLS: ssllabs.com or testssl.sh
Check for rogue certs: crt.sh
Force HTTPS:   HSTS header → preload list (hstspreload.org)
CT monitoring: crt.sh alerts for your domain

Session keys stored? → MITM possible (debugging proxies, Wireshark)
Session keys ephemeral (TLS 1.3 ECDHE)? → Perfect Forward Secrecy
```

---

## See Also

- [Network Protocols](network-protocols.md) — TCP, DNS, HTTP/2, QUIC, full stack
- [How a Computer Really Works](how-computers-work.md) — TLS in full networking context
- [Web Application Security](../security/web-application-security.md) — HTTPS in security context
- [Penetration Testing Tools](../security/penetration-testing-tools.md) — Burp Suite TLS interception
- [OPSEC & Proxies](../security/opsec-and-proxies.md) — Privacy beyond HTTPS (DoH, VPN)
