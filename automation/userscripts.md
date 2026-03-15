# Userscripts

Userscripts are small JavaScript programs that run in your browser on specific websites, modifying how pages look or behave. They are injected into pages after they load, using a browser extension as the host.

---

## Table of Contents
1. [How Userscripts Work](#1-how-userscripts-work)
2. [Userscript Managers](#2-userscript-managers)
3. [Writing a Userscript](#3-writing-a-userscript)
4. [Metadata Block Reference](#4-metadata-block-reference)
5. [GM_ API Reference](#5-gm_-api-reference)
6. [Finding & Installing Scripts](#6-finding--installing-scripts)
7. [Security Considerations](#7-security-considerations)

---

## 1. How Userscripts Work

```
Page loads in browser
        ↓
Userscript manager extension checks: does any installed script match this URL?
        ↓
Matching scripts injected into page context (isolated or page-level)
        ↓
Scripts run: modify DOM, intercept XHR, add UI elements, redirect URLs, etc.
        ↓
User sees modified page
```

Scripts run after the page's own JavaScript, in a sandboxed context. They can read and modify the DOM, intercept network requests, store persistent data via `GM_setValue`, and communicate cross-origin using `GM_xmlhttpRequest`.

---

## 2. Userscript Managers

| Manager | Browser | Notes |
|---------|---------|-------|
| **Tampermonkey** | Chrome, Firefox, Edge, Safari | Most popular, actively maintained |
| **Violentmonkey** | Chrome, Firefox, Edge | Open source, Tampermonkey-compatible |
| **Greasemonkey** | Firefox only | The original (2005), now less used |
| **Userscripts.app** | Safari (macOS/iOS) | Native Safari extension |

Install from browser extension stores. After installing, click a `.user.js` URL → manager prompts to install.

---

## 3. Writing a Userscript

### Minimal Script

```javascript
// ==UserScript==
// @name        My First Script
// @namespace   http://tampermonkey.net/
// @version     1.0
// @description Does something useful
// @author      You
// @match       https://example.com/*
// @grant       none
// ==/UserScript==

(function() {
    'use strict';
    document.title = "Modified by userscript";
    document.body.style.backgroundColor = "#1a1a2e";
})();
```

### Remove Ads / Paywalls

```javascript
// ==UserScript==
// @name        Element Remover
// @match       https://news-site.com/*
// @grant       none
// ==/UserScript==

(function() {
    // Remove elements immediately
    const remove = (selector) => {
        document.querySelectorAll(selector).forEach(el => el.remove());
    };

    // Run on load
    remove('.ad-container, .paywall-overlay, .subscribe-modal, #cookie-banner');

    // Also watch for dynamically injected elements
    const observer = new MutationObserver(() => {
        remove('.ad-container, .paywall-overlay, .subscribe-modal');
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
```

### Auto-Click / Form Filler

```javascript
// ==UserScript==
// @name        Auto Form Fill
// @match       https://site.com/checkout*
// @grant       none
// ==/UserScript==

(function() {
    window.addEventListener('load', () => {
        const fill = (selector, value) => {
            const el = document.querySelector(selector);
            if (el) {
                el.value = value;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        };

        fill('#first-name', 'John');
        fill('#email', 'john@example.com');
        fill('#zip', '12345');

        // Auto-submit after 500ms
        setTimeout(() => {
            const btn = document.querySelector('button[type=submit]');
            if (btn) btn.click();
        }, 500);
    });
})();
```

### XHR/Fetch Interceptor

```javascript
// ==UserScript==
// @name        API Response Logger
// @match       https://app.example.com/*
// @grant       none
// @run-at      document-start
// ==/UserScript==

(function() {
    // Intercept all fetch() calls
    const origFetch = window.fetch;
    window.fetch = async function(...args) {
        const response = await origFetch(...args);
        const clone = response.clone();
        clone.text().then(body => {
            console.log('[Intercepted]', args[0], body.substring(0, 500));
        });
        return response;
    };

    // Intercept XMLHttpRequest
    const origOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
        this.addEventListener('load', function() {
            console.log('[XHR]', method, url, this.responseText.substring(0, 200));
        });
        return origOpen.apply(this, arguments);
    };
})();
```

### Cross-Origin Request (using GM API)

```javascript
// ==UserScript==
// @name        Cross-Origin Fetcher
// @match       https://site.com/*
// @grant       GM_xmlhttpRequest
// @connect     api.external.com
// ==/UserScript==

GM_xmlhttpRequest({
    method: 'GET',
    url: 'https://api.external.com/data',
    headers: { 'Authorization': 'Bearer TOKEN' },
    onload: function(response) {
        const data = JSON.parse(response.responseText);
        console.log(data);
    }
});
```

---

## 4. Metadata Block Reference

```javascript
// ==UserScript==
// @name            Script Display Name
// @namespace       https://yoursite.com/        (unique ID for your scripts)
// @version         1.2.3
// @description     What the script does
// @author          Your Name
// @homepage        https://github.com/you/script
// @updateURL       https://raw.githubusercontent.com/.../script.user.js
// @downloadURL     https://raw.githubusercontent.com/.../script.user.js
// @icon            https://example.com/favicon.ico

// @match    https://example.com/*               (glob pattern — required)
// @match    https://*.example.com/*             (all subdomains)
// @match    *://example.com/*                   (http + https)
// @exclude  https://example.com/admin/*         (exclude these URLs)
// @include  /^https:\/\/example\.com\/.*$/      (regex match)

// @require  https://code.jquery.com/jquery-3.7.1.min.js   (load external JS)
// @resource STYLESHEET https://example.com/style.css       (load external resource)

// @run-at   document-start     (before page scripts — needed for intercepts)
// @run-at   document-body      (when body exists)
// @run-at   document-end       (after DOM, default)
// @run-at   document-idle      (after window.onload)

// @grant    none                     (run in page context, no GM API)
// @grant    GM_getValue              (persistent storage)
// @grant    GM_setValue
// @grant    GM_deleteValue
// @grant    GM_listValues
// @grant    GM_xmlhttpRequest        (cross-origin requests)
// @grant    GM_notification          (desktop notifications)
// @grant    GM_openInTab             (open new tab)
// @grant    GM_setClipboard          (write to clipboard)
// @grant    GM_addStyle              (inject CSS)
// @grant    GM_getResourceText       (access @resource files)
// @grant    unsafeWindow             (access page's actual window object)

// @noframes                          (don't run in iframes)
// @connect  api.example.com          (allow GM_xmlhttpRequest to this domain)
// ==/UserScript==
```

---

## 5. GM_ API Reference

```javascript
// Persistent key-value storage (survives page reload)
GM_setValue('key', value);              // Store (any JSON-serializable value)
const val = GM_getValue('key', default); // Retrieve (default if not set)
GM_deleteValue('key');
const keys = GM_listValues();           // Array of all stored keys

// Inject CSS
GM_addStyle(`
    .ad-banner { display: none !important; }
    body { font-family: 'Inter', sans-serif; }
`);

// Desktop notification
GM_notification({
    title: 'Script Alert',
    text: 'Something happened',
    image: 'https://example.com/icon.png',
    timeout: 3000,
    onclick: () => window.focus()
});

// Open new tab
GM_openInTab('https://example.com', {
    active: true,     // Focus the new tab
    insert: true      // Insert after current tab
});

// Clipboard
GM_setClipboard('text to copy', 'text');

// Cross-origin HTTP request (bypasses same-origin policy)
GM_xmlhttpRequest({
    method: 'POST',
    url: 'https://other-domain.com/api',
    headers: { 'Content-Type': 'application/json' },
    data: JSON.stringify({ key: 'value' }),
    responseType: 'json',
    onload: (res) => console.log(res.response),
    onerror: (err) => console.error(err)
});
```

---

## 6. Finding & Installing Scripts

**Script repositories:**
- **Greasy Fork:** https://greasyfork.org — largest collection, user ratings, reviews
- **OpenUserJS:** https://openuserjs.org — open source scripts
- **GitHub:** search `site:github.com userscript filetype:user.js`

**Popular scripts:**
- **uBlock Origin + uMatrix scripts** — additional filtering rules
- **YouTube enhancers** — sponsorblock integration, speed controls, download buttons
- **Return YouTube Dislike** — shows dislike count via API
- **Dark Reader userscript** — force dark mode on any site
- **Anti-Adblock Killer** — bypass adblock detection
- **Pixiv Downloader** — bulk download artwork
- **Steam Economy Enhancer** — price tools for Steam marketplace

**Installing a script:**
1. Install a manager (Tampermonkey recommended)
2. Click any `.user.js` link → manager prompts "Install"
3. Review the metadata and requested permissions before confirming

---

## 7. Security Considerations

```
Risks when installing userscripts:
  - Scripts run with your browser's full cookie access
  - A malicious script can: steal session cookies, log keystrokes,
    exfiltrate form data (passwords, credit cards), make requests as you
  
  Safe practices:
  ✓ Only install from Greasy Fork (reviewed) or trusted GitHub authors
  ✓ Read the script before installing — it's just JavaScript
  ✓ Check @grant permissions — why does a page restyler need GM_xmlhttpRequest?
  ✓ Check @updateURL — auto-updates can push malicious changes
  ✓ Use Violentmonkey which shows a diff on updates
  ✗ Never install from random paste sites or sketchy Discord links
  ✗ Never run scripts that request @grant unsafeWindow on banking/email sites
```

---

## See Also

- [Web Automation](web-automation.md) — Playwright, Puppeteer for server-side automation
- [Discord Quest Completer](discord-quest-completer.md) — browser automation for Discord
- [APIs & Resources](../devtools/apis-and-resources.md) — Working with web APIs directly
