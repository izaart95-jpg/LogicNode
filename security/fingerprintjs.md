# FingerprintJS — Browser Fingerprinting Library

FingerprintJS is an open-source JavaScript library that generates a unique visitor identifier based on browser and device attributes — without cookies or persistent storage. It is used both offensively (tracking users) and defensively (fraud detection, bot detection, security research).

- **Repository:** https://github.com/fingerprintjs/fingerprintjs
- **Website:** https://fingerprint.com
- **License:** MIT (open-source library), Commercial (Pro API)
- **Stars:** 22,000+
- **Maintained by:** Fingerprint Inc.

---

## Table of Contents
1. [What is Browser Fingerprinting?](#1-what-is-browser-fingerprinting)
2. [How FingerprintJS Works](#2-how-fingerprintjs-works)
3. [Signals Collected](#3-signals-collected)
4. [Installation & Basic Usage](#4-installation--basic-usage)
5. [Fingerprint Pro (Cloud API)](#5-fingerprint-pro-cloud-api)
6. [Defensive Use — Detection & Spoofing](#6-defensive-use--detection--spoofing)
7. [Security Research Applications](#7-security-research-applications)
8. [Privacy Implications](#8-privacy-implications)
9. [Comparison Table](#9-comparison-table)

---

## 1. What is Browser Fingerprinting?

Browser fingerprinting identifies users by collecting a combination of browser and device attributes that together form a unique profile. Unlike cookies:

- **No storage required** — fingerprint is computed from browser properties, nothing is written to disk
- **Survives cookie deletion** — clearing cookies does not change the fingerprint
- **Cross-incognito** — private browsing often doesn't change the fingerprint
- **Stateless on the client** — the server remembers you, not your browser

```
Traditional tracking:    Browser ←→ Server (via cookie ID stored in browser)
Fingerprint tracking:    Browser attributes → hash → Server recognizes the hash
```

**Legitimate uses:** Fraud detection, bot detection, account takeover prevention, rate limiting without login

**Privacy concern:** Cross-site tracking without user consent or knowledge, re-identification after cookie opt-out

---

## 2. How FingerprintJS Works

FingerprintJS collects dozens of browser attributes, hashes them together, and returns a `visitorId` — a stable identifier for the browser.

```
Browser signals → Collected by JS → Normalized → Hashed → visitorId (hex string)
```

The same browser on the same device returns the same `visitorId` consistently across visits. The identifier changes if the browser is significantly modified (major version update, hardware change, OS reinstall).

**Stability:** FingerprintJS prioritizes stability over uniqueness — it's designed to recognize returning visitors even when some attributes change (e.g., screen resolution change when connecting an external monitor).

---

## 3. Signals Collected

FingerprintJS collects attributes across multiple categories:

### Browser / JavaScript
- User-Agent string
- Browser language and accepted languages
- Timezone and timezone offset
- Session storage and local storage availability
- Do Not Track header
- JavaScript engine behavior (differences between V8, SpiderMonkey, etc.)
- Cookie support

### Hardware / Screen
- Screen resolution and color depth
- Available screen size (minus taskbar)
- Device pixel ratio (detects HiDPI/Retina)
- Device memory (approximate, via `navigator.deviceMemory`)
- Hardware concurrency (CPU core count)

### Canvas Fingerprint
- Renders a hidden canvas with text and shapes
- The pixel output differs slightly between GPU drivers, OS, and fonts
- SHA-256 hash of the pixel data becomes a stable signal

```javascript
// Canvas fingerprinting example (simplified)
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
ctx.textBaseline = 'top';
ctx.font = '14px Arial';
ctx.fillStyle = '#f60';
ctx.fillRect(125, 1, 62, 20);
ctx.fillStyle = '#069';
ctx.fillText('BrowserFingerprint', 2, 15);
// Hash the canvas data URL → unique per GPU/driver combination
const hash = sha256(canvas.toDataURL());
```

### WebGL
- GPU renderer string (reveals GPU model)
- GPU vendor string
- WebGL rendering differences

### Audio Context
- Renders an audio graph and measures the output
- Small numeric differences between audio hardware and OS reveal unique values

```javascript
// AudioContext fingerprinting (simplified)
const ctx = new AudioContext();
const oscillator = ctx.createOscillator();
const analyser = ctx.createAnalyser();
const gain = ctx.createGain();
gain.gain.value = 0;   // Silent — just measuring, not playing
oscillator.connect(analyser);
analyser.connect(gain);
gain.connect(ctx.destination);
oscillator.start(0);
// Capture analyser data → hash → GPU/audio hardware signal
```

### Fonts
- Detects installed fonts by measuring text rendering
- Font presence reveals OS, region, installed software

### Plugins and MIME Types
- List of installed browser plugins
- Supported MIME types

### Network
- IP address (server-side)
- Connection type (WiFi, cellular, wired via Network Information API)

---

## 4. Installation & Basic Usage

### npm

```bash
npm install @fingerprintjs/fingerprintjs
```

```javascript
import FingerprintJS from '@fingerprintjs/fingerprintjs';

// Initialize and get visitor ID
const fpPromise = FingerprintJS.load();

fpPromise
  .then(fp => fp.get())
  .then(result => {
    const visitorId = result.visitorId;
    console.log('Visitor ID:', visitorId);
    // visitorId: "a3b4c5d6e7f8..." (hex string, stable across visits)
  });
```

### CDN

```html
<script>
  // Initialize the agent at application startup.
  const fpPromise = import('https://openfpcdn.io/fingerprintjs/v4')
    .then(FingerprintJS => FingerprintJS.load())

  // Get the visitor identifier when you need it.
  fpPromise
    .then(fp => fp.get())
    .then(result => console.log(result.visitorId))
</script>
```

### Full Result Object

```javascript
fp.get().then(result => {
  console.log(result.visitorId);    // The stable visitor identifier
  console.log(result.confidence);   // { score: 0.995 } — confidence in stability
  console.log(result.components);   // All collected signals with their values
  /*
  components: {
    canvas: { value: "a1b2c3..." },
    webGlRenderer: { value: "ANGLE (NVIDIA GeForce RTX 3070...)" },
    fonts: { value: ["Arial", "Times New Roman", ...] },
    screenResolution: { value: [1920, 1080] },
    timezone: { value: "America/New_York" },
    ...
  }
  */
});
```

---

## 5. Fingerprint Pro (Cloud API)

The open-source library has ~60% accuracy. **Fingerprint Pro** is the commercial cloud version with 99.5% accuracy using additional server-side signals and ML models.

```bash
npm install @fingerprintjs/fingerprintjs-pro
```

```javascript
import FingerprintJS from '@fingerprintjs/fingerprintjs-pro';

const fpPromise = FingerprintJS.load({
  apiKey: 'YOUR_PUBLIC_API_KEY'
  // region: 'eu'  // for EU data residency
});

const result = await (await fpPromise).get();
console.log(result.requestId);  // Unique per request, used to query server API
console.log(result.visitorId);  // Stable visitor identifier
```

**Server-side verification:**

```python
import requests

# Verify a fingerprint server-side (never trust client-side alone)
def verify_fingerprint(request_id: str, visitor_id: str) -> dict:
    r = requests.get(
        f"https://api.fpjs.io/events/{request_id}",
        headers={"Auth-API-Key": "YOUR_SECRET_KEY"}
    )
    event = r.json()
    # Check if the visitor_id matches and request is not tampered
    products = event["products"]
    identification = products.get("identification", {}).get("data", {})
    return {
        "valid": identification.get("visitorId") == visitor_id,
        "bot": products.get("botd", {}).get("data", {}).get("bot", {}).get("result"),
        "vpn": products.get("vpn", {}).get("data", {}).get("result"),
        "ip": identification.get("ip")
    }
```

---

## 6. Defensive Use — Detection & Spoofing

### Detecting Fingerprinting on a Website

```javascript
// Check if a site is running FingerprintJS
// Open browser DevTools → Sources → search for "fingerprintjs" or "fpjs"
// Or: Network tab → look for requests to fpjs.io, fingerprint.com, or openfpcdn.io
```

### Anti-Fingerprinting Tools

| Tool | Method | Effectiveness |
|------|--------|--------------|
| **Brave Browser** | Randomizes canvas, WebGL, audio | High |
| **Tor Browser** | Standardizes all signals to same value | Very High |
| **Firefox (strict mode)** | Limits some signals | Medium |
| **Camoufox** | Anti-fingerprint Firefox fork | High |
| **Canvas Blocker (Firefox ext.)** | Injects noise into canvas | Medium-High |

```javascript
// Brave's canvas randomization approach (conceptual):
// Instead of blocking canvas, Brave adds per-session random noise to pixel values
// So every canvas read returns slightly different values each session
// → FingerprintJS gets a different hash each session → cannot track across sessions
```

### Testing Your Fingerprint

```
https://browserleaks.com/canvas    # Canvas fingerprint test
https://amiunique.org              # Uniqueness score
https://coveryourtracks.eff.org    # EFF's fingerprint test (Panopticlick)
https://demo.fingerprint.com       # Fingerprint Inc.'s own demo
```

### Spoofing with Puppeteer

For automated testing or research:

```javascript
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

// Stealth plugin patches:
// - navigator.webdriver = false
// - Canvas fingerprint randomization
// - WebGL vendor spoofing
// - Language and timezone consistency

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();

// Override canvas fingerprint manually
await page.evaluateOnNewDocument(() => {
  const originalGetContext = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function(type, ...args) {
    const ctx = originalGetContext.call(this, type, ...args);
    if (type === '2d') {
      const originalGetImageData = ctx.getImageData.bind(ctx);
      ctx.getImageData = function(...a) {
        const data = originalGetImageData(...a);
        // Add subtle noise to pixel values
        for (let i = 0; i < data.data.length; i += 4) {
          data.data[i] += Math.floor(Math.random() * 3) - 1;
        }
        return data;
      };
    }
    return ctx;
  };
});
```

---

## 7. Security Research Applications

### Bot Detection

FingerprintJS is widely used to distinguish human users from bots:

```javascript
// Server-side bot detection via Fingerprint Pro
const result = await verifyFingerprint(requestId, visitorId);
if (result.bot === "bad") {
  // Serve CAPTCHA or block request
}
```

### Account Takeover Prevention

```javascript
// Track which visitorIds have logged into an account
// Alert on login from new, unseen visitorId
async function checkLoginFingerprint(userId, visitorId) {
  const knownDevices = await db.getKnownDevices(userId);
  if (!knownDevices.includes(visitorId)) {
    await sendLoginAlert(userId, "New device detected");
    await db.addKnownDevice(userId, visitorId);
  }
}
```

### Rate Limiting Without Login

```javascript
// Rate limit anonymous users by fingerprint
const requests = new Map();
app.use('/api/search', async (req, res, next) => {
  const visitorId = req.headers['x-visitor-id'];  // Sent from client
  const count = (requests.get(visitorId) || 0) + 1;
  requests.set(visitorId, count);
  if (count > 10) return res.status(429).json({ error: 'Rate limited' });
  next();
});
```

---

## 8. Privacy Implications

Browser fingerprinting raises significant privacy concerns:

**No consent mechanism:** Unlike cookies, fingerprinting requires no opt-in and cannot be blocked by standard "refuse all cookies" flows.

**GDPR and ePrivacy Directive:** In the EU, fingerprinting for tracking purposes likely requires explicit consent under GDPR Article 6 and the ePrivacy Directive. Many sites use fingerprinting without disclosing it — this is a legal gray area actively being litigated.

**Re-identification:** If a user deletes cookies and clears local storage to "reset" their tracking, fingerprinting re-identifies them immediately on next visit.

**Cross-site tracking:** While the same-site policy limits cookies, fingerprinting works across any site that loads the same fingerprinting script.

---

## 9. Comparison Table

| Library | Open Source | Accuracy | Server-Side | Price | Use Case |
|---------|------------|----------|-------------|-------|---------|
| **FingerprintJS v4** | ✅ MIT | ~60% | No | Free | Client-side identification |
| **Fingerprint Pro** | ❌ (cloud) | 99.5% | ✅ | From $80/mo | Production fraud detection |
| **ClientJS** | ✅ MIT | ~50% | No | Free | Lightweight alternative |
| **CreepJS** | ✅ | Research | No | Free | Research, fingerprint testing |
| **Botd** | ✅ MIT | High (bots) | Optional | Free/Paid | Bot detection specifically |

---

## See Also

- [OPSEC & Proxies](opsec-and-proxies.md) — Camoufox, ProxyChains, anti-fingerprinting tools
- [Web Automation](../automation/web-automation.md) — Puppeteer Stealth, undetected-chromedriver, Camoufox
- [Penetration Testing Tools](penetration-testing-tools.md) — Tools for security testing and reconnaissance
