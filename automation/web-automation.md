# Web Automation — Playwright, Selenium, Puppeteer & CAPTCHA Solving

Web automation enables programmatic control of web browsers for testing, scraping, and task automation. Modern frameworks provide headless execution, network interception, screenshot capture, and anti-detection capabilities for robust browser-driven workflows.

---

## Table of Contents
1. [Browser Automation Overview](#1-browser-automation-overview)
2. [Playwright](#2-playwright)
3. [Selenium](#3-selenium)
4. [Puppeteer](#4-puppeteer)
5. [CAPTCHA Solving Services](#5-captcha-solving-services)
6. [Anti-Detection](#6-anti-detection)
7. [Comparison Table](#7-comparison-table)

---

## 1. Browser Automation Overview

### What It Is

Browser automation is the practice of controlling a web browser programmatically — clicking buttons, filling forms, navigating pages, and extracting data without human interaction.

### Common Use Cases

- **Testing** — end-to-end (E2E) test suites for web applications
- **Scraping** — extracting data from JavaScript-rendered pages that simple HTTP requests cannot handle
- **Task automation** — form submissions, report generation, monitoring dashboards
- **Screenshot & PDF generation** — capturing visual snapshots of web pages
- **Performance monitoring** — measuring page load times and resource usage

### Headless vs Headed Mode

| Mode | Description | Use Case |
|------|-------------|----------|
| **Headless** | No visible browser window; runs in background | CI/CD, servers, scraping at scale |
| **Headed** | Full browser UI visible | Debugging, development, demos |

```bash
# Most frameworks default to headless; pass a flag for headed mode
# Playwright: headless=False
# Selenium: no special flag (headed by default)
# Puppeteer: headless: false
```

### WebDriver vs CDP (Chrome DevTools Protocol)

| Protocol | How It Works | Used By |
|----------|-------------|---------|
| **WebDriver** | W3C standard; sends commands via HTTP to a driver binary (chromedriver, geckodriver) | Selenium, early Playwright |
| **CDP** | Direct WebSocket connection to browser's DevTools; lower-level, faster | Puppeteer, Playwright (Chromium), Selenium 4 (optional) |

CDP offers finer control — network interception, console access, performance tracing — while WebDriver provides cross-browser standardization.

---

## 2. Playwright

- **Website:** https://playwright.dev
- **By:** Microsoft
- **Languages:** Python, Node.js, Java, .NET
- **Browsers:** Chromium, Firefox, WebKit (Safari engine)
- **License:** Apache 2.0

### 2.1 Installation

```bash
# Python
pip install playwright
playwright install

# Node.js
npm init playwright@latest
# Or manually:
npm install playwright
npx playwright install
```

### 2.2 Key Features

- **Auto-wait** — automatically waits for elements to be actionable before interacting
- **Network interception** — mock API responses, block resources, modify requests
- **Screenshots & PDF** — full-page or element-level capture
- **Video recording** — record browser sessions as video files
- **Tracing** — capture detailed execution traces for debugging
- **Multi-browser** — single API for Chromium, Firefox, and WebKit
- **Mobile emulation** — simulate devices, geolocation, permissions
- **Codegen** — generate test scripts by recording browser actions

### 2.3 Python Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://example.com")
    page.screenshot(path="screenshot.png")

    # Interact with elements
    page.fill("#search", "automation")
    page.click("button[type='submit']")

    # Wait for navigation
    page.wait_for_load_state("networkidle")

    # Extract text
    title = page.text_content("h1")
    print(title)

    browser.close()
```

### 2.4 Async API

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```

### 2.5 Network Interception

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Block images and CSS for faster scraping
    page.route("**/*.{png,jpg,jpeg,gif,css}", lambda route: route.abort())

    # Mock an API response
    page.route("**/api/data", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"mocked": true}'
    ))

    page.goto("https://example.com")
    browser.close()
```

### 2.6 Codegen & Trace Viewer

```bash
# Record actions and generate code automatically
playwright codegen https://example.com

# Record a trace for debugging
# In code: browser.new_context(record_video_dir="videos/")

# View traces
playwright show-trace trace.zip
```

---

## 3. Selenium

- **Website:** https://www.selenium.dev
- **By:** Selenium Project (open source)
- **Languages:** Python, Java, C#, Ruby, JavaScript
- **Browsers:** Chrome, Firefox, Edge, Safari, Opera
- **License:** Apache 2.0

### 3.1 Installation

```bash
# Python
pip install selenium

# WebDriver management (auto-downloads drivers)
pip install webdriver-manager

# Node.js
npm install selenium-webdriver
```

### 3.2 WebDriver Setup

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Auto-manage chromedriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Or specify manually
# driver = webdriver.Chrome(service=Service("/path/to/chromedriver"))
```

### 3.3 Python Example

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://example.com")

element = driver.find_element(By.CSS_SELECTOR, "h1")
print(element.text)

# Fill a form
search = driver.find_element(By.NAME, "q")
search.send_keys("automation")
search.send_keys(Keys.RETURN)

driver.quit()
```

### 3.4 Selenium 4 Features

- **Relative locators** — find elements relative to others (`above`, `below`, `near`, `to_left_of`, `to_right_of`)
- **Chrome DevTools access** — network interception, performance metrics via CDP
- **New window/tab management** — `driver.switch_to.new_window('tab')`
- **Element screenshots** — capture individual elements

```python
from selenium.webdriver.support.relative_locator import locate_with

# Find input below a label
email_input = driver.find_element(
    locate_with(By.TAG_NAME, "input").below({By.ID: "email-label"})
)
```

### 3.5 Waits

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Implicit wait (global timeout)
driver.implicitly_wait(10)

# Explicit wait (condition-based)
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "result"))
)

# Fluent wait (custom polling)
wait = WebDriverWait(driver, 30, poll_frequency=2,
                     ignored_exceptions=[NoSuchElementException])
element = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
```

### 3.6 Selenium Grid

Selenium Grid enables parallel test execution across multiple machines and browsers.

```bash
# Start hub
java -jar selenium-server-4.x.jar hub

# Start node
java -jar selenium-server-4.x.jar node --detect-drivers true

# Or use Docker
docker run -d -p 4442-4444:4442-4444 --name selenium-hub selenium/hub:4.x
docker run -d --link selenium-hub:hub selenium/node-chrome:4.x
docker run -d --link selenium-hub:hub selenium/node-firefox:4.x
```

```python
from selenium import webdriver

options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
)
```

---

## 4. Puppeteer

- **Website:** https://pptr.dev
- **By:** Google
- **Language:** Node.js (TypeScript support)
- **Browsers:** Chrome, Chromium (Firefox experimental)
- **Protocol:** CDP (Chrome DevTools Protocol)
- **License:** Apache 2.0

### 4.1 Installation

```bash
npm install puppeteer
# Downloads a compatible Chromium automatically

# Or use puppeteer-core (no bundled browser)
npm install puppeteer-core
```

### 4.2 Basic Example

```javascript
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('https://example.com');
    await page.screenshot({ path: 'screenshot.png' });

    // Extract text
    const title = await page.$eval('h1', el => el.textContent);
    console.log(title);

    await browser.close();
})();
```

### 4.3 Form Filling & Navigation

```javascript
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto('https://example.com/login');

    // Fill form
    await page.type('#username', 'myuser');
    await page.type('#password', 'mypass');
    await page.click('#login-btn');

    // Wait for navigation
    await page.waitForNavigation();

    // Generate PDF
    await page.pdf({ path: 'page.pdf', format: 'A4' });

    await browser.close();
})();
```

### 4.4 SPA Crawling & Network Interception

```javascript
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Intercept network requests
    await page.setRequestInterception(true);
    page.on('request', request => {
        if (request.resourceType() === 'image') {
            request.abort();  // Block images for speed
        } else {
            request.continue();
        }
    });

    // Capture API responses
    page.on('response', async response => {
        if (response.url().includes('/api/')) {
            console.log(await response.json());
        }
    });

    await page.goto('https://example.com', { waitUntil: 'networkidle0' });
    await browser.close();
})();
```

### 4.5 Puppeteer vs Playwright

| Feature | Puppeteer | Playwright |
|---------|-----------|------------|
| **Browsers** | Chrome/Chromium only | Chromium, Firefox, WebKit |
| **Languages** | Node.js | Node.js, Python, Java, .NET |
| **Protocol** | CDP | CDP + custom protocols |
| **Auto-wait** | Manual waits needed | Built-in auto-wait |
| **Mobile** | Chrome emulation | Full device emulation |
| **Parallelism** | Manual | Browser contexts (isolated) |
| **Maintained by** | Google | Microsoft |

---

## 5. CAPTCHA Solving Services

### 5.1 CapMonster

- **Website:** https://capmonster.cloud
- **Type:** Automated (AI-based) CAPTCHA solving
- **Variants:** CapMonster Cloud (API) and CapMonster 2 (local software)
- **Supported CAPTCHAs:** reCAPTCHA v2/v3, hCaptcha, FunCaptcha, GeeTest, image CAPTCHA, Turnstile

```python
import requests

task = {
    "clientKey": "YOUR_API_KEY",
    "task": {
        "type": "RecaptchaV2TaskProxyless",
        "websiteURL": "https://example.com",
        "websiteKey": "SITE_KEY"
    }
}
response = requests.post("https://api.capmonster.cloud/createTask", json=task)
task_id = response.json()["taskId"]

# Poll for result
import time
while True:
    result = requests.post("https://api.capmonster.cloud/getTaskResult", json={
        "clientKey": "YOUR_API_KEY",
        "taskId": task_id
    }).json()
    if result["status"] == "ready":
        token = result["solution"]["gRecaptchaResponse"]
        break
    time.sleep(2)
```

**CapMonster Cloud vs CapMonster 2:**

| Feature | CapMonster Cloud | CapMonster 2 |
|---------|-----------------|--------------|
| **Deployment** | SaaS API | Local Windows software |
| **Speed** | Fast (distributed) | Depends on hardware |
| **Pricing** | Per-solve (from $0.6/1000) | One-time license |
| **Internet** | Required | Optional (local solving) |

### 5.2 2Captcha

- **Website:** https://2captcha.com
- **Type:** Human-powered + AI hybrid CAPTCHA solving
- **Supported CAPTCHAs:** reCAPTCHA v2/v3, hCaptcha, text CAPTCHA, image CAPTCHA, FunCaptcha, Turnstile, audio CAPTCHA
- **Pricing:** Per-solve basis (from $1.00-$2.99 per 1000 solves depending on type)

```bash
pip install 2captcha-python
```

```python
from twocaptcha import TwoCaptcha

solver = TwoCaptcha('YOUR_API_KEY')

# Solve reCAPTCHA v2
result = solver.recaptcha(
    sitekey='SITE_KEY',
    url='https://example.com'
)
print(result['code'])  # CAPTCHA token to submit

# Solve hCaptcha
result = solver.hcaptcha(
    sitekey='SITE_KEY',
    url='https://example.com'
)

# Solve image CAPTCHA
result = solver.normal('captcha.png')
```

### 5.3 Integration with Browser Automation

```python
from playwright.sync_api import sync_playwright
from twocaptcha import TwoCaptcha

solver = TwoCaptcha('YOUR_API_KEY')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/protected")

    # Extract sitekey from page
    sitekey = page.get_attribute('[data-sitekey]', 'data-sitekey')

    # Solve CAPTCHA via service
    result = solver.recaptcha(sitekey=sitekey, url=page.url)

    # Inject token into page
    page.evaluate(f'document.getElementById("g-recaptcha-response").value = "{result["code"]}"')
    page.click("#submit")

    browser.close()
```

---

## 6. Anti-Detection

Browser automation is often detected and blocked by websites. Anti-detection techniques help bypass these protections.

### 6.1 Camoufox

Anti-fingerprint Firefox browser designed for web automation. See [security/opsec-and-proxies.md](../security/opsec-and-proxies.md) for detailed proxy and OPSEC configuration.

```bash
pip install camoufox
playwright install firefox
```

```python
from camoufox.sync_api import Camoufox

with Camoufox(humanize=True) as page:
    page.goto("https://example.com")
    page.screenshot(path="screenshot.png")
```

### 6.2 undetected-chromedriver

Drop-in replacement for Selenium's chromedriver that patches detection mechanisms.

```bash
pip install undetected-chromedriver
```

```python
import undetected_chromedriver as uc

driver = uc.Chrome()
driver.get("https://example.com")
print(driver.page_source)
driver.quit()
```

### 6.3 Puppeteer Stealth

```bash
npm install puppeteer-extra puppeteer-extra-plugin-stealth
```

```javascript
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin());

puppeteer.launch({ headless: true }).then(async browser => {
    const page = await browser.newPage();
    await page.goto('https://example.com');
    await browser.close();
});
```

### 6.4 Fingerprint Considerations

Websites detect automation through browser fingerprinting. Key vectors:

| Vector | What Is Checked | Mitigation |
|--------|----------------|------------|
| **navigator.webdriver** | `true` when automated | Stealth plugins override to `false` |
| **Canvas** | Unique rendering fingerprint | Noise injection, Camoufox |
| **WebGL** | GPU renderer string, hashing | Spoofing via browser patches |
| **Fonts** | Installed font enumeration | Limit font exposure |
| **User-Agent** | Browser/OS identification | Rotate realistic UA strings |
| **Screen resolution** | Viewport and screen size | Set realistic dimensions |
| **Timezone** | Must match IP geolocation | Set via browser launch args |
| **WebRTC** | Leaks real IP behind proxy | Disable or patch |

---

## 7. Comparison Table

| Feature | Playwright | Selenium | Puppeteer |
|---------|-----------|----------|-----------|
| **Language Support** | Python, Node.js, Java, .NET | Python, Java, C#, Ruby, JS | Node.js |
| **Browsers** | Chromium, Firefox, WebKit | Chrome, Firefox, Edge, Safari | Chrome, Chromium |
| **Protocol** | CDP + custom | WebDriver (W3C) | CDP |
| **Headless** | Yes (default) | Yes | Yes (default) |
| **Auto-Wait** | Built-in | Manual (explicit/implicit waits) | Manual |
| **Network Interception** | Native | Selenium 4 (CDP) | Native |
| **Screenshots** | Full page + element | Full page + element | Full page + element |
| **PDF Generation** | Yes | No (native) | Yes |
| **Video Recording** | Built-in | No | Manual (screencast) |
| **Parallel Execution** | Browser contexts | Selenium Grid | Incognito contexts |
| **Mobile Emulation** | Full device profiles | Basic resize | Chrome emulation |
| **Code Generation** | `playwright codegen` | Selenium IDE | Chrome Recorder |
| **Speed** | Fast | Moderate | Fast |
| **Community** | Growing rapidly | Largest (established) | Large |
| **Best For** | Cross-browser testing, modern apps | Legacy support, enterprise | Chrome-specific, quick scripts |

### Quick Decision Guide

| Scenario | Recommended Tool |
|----------|-----------------|
| New E2E testing project | **Playwright** |
| Cross-browser testing (including Safari) | **Playwright** |
| Enterprise with existing Java/C# stack | **Selenium** |
| Chrome-only quick automation | **Puppeteer** |
| Legacy test suite maintenance | **Selenium** |
| Web scraping with anti-detection | **Playwright** + Camoufox or **undetected-chromedriver** |

---

## See Also

- [OPSEC & Proxies](../security/opsec-and-proxies.md) — Camoufox, proxy rotation, anti-fingerprinting
- [Frameworks & Libraries](../devtools/frameworks-and-libraries.md) — Testing frameworks and dev tools
- [Workflow Automation](workflow-automation.md) — n8n, Tasker, automated pipelines
