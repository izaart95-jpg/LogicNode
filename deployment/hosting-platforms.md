# Hosting Platforms — Vercel, Netlify & Firebase Studio

Modern web hosting platforms combine Git-based deployments, serverless functions, edge computing, and global CDNs into streamlined developer workflows. Push your code and get a production-ready deployment in seconds.

---

## Table of Contents
1. [Modern Web Hosting Overview](#1-modern-web-hosting-overview)
2. [Vercel](#2-vercel)
3. [Netlify](#3-netlify)
4. [Firebase Studio](#4-firebase-studio)
5. [Comparison Table](#5-comparison-table)

---

## 1. Modern Web Hosting Overview

### Hosting Models

| Model | Description | Examples |
|-------|-------------|----------|
| **Static hosting** | Pre-built HTML/CSS/JS served from a CDN | GitHub Pages, Netlify, Vercel |
| **Serverless** | Backend functions that run on demand (no persistent server) | Vercel Functions, Netlify Functions, AWS Lambda |
| **Edge computing** | Code runs at CDN edge locations closest to users | Vercel Edge Runtime, Netlify Edge Functions, Cloudflare Workers |
| **Containers** | Full application packaged in Docker containers | Google Cloud Run, AWS ECS, Railway |
| **Traditional** | Long-running server (VPS or dedicated) | DigitalOcean, Linode, Hetzner |

### JAMstack Architecture

```
┌──────────────┐     Build        ┌──────────────┐     CDN         ┌──────────┐
│  Git Repo    │ ──────────────▶  │  Static      │ ─────────────▶  │  Users   │
│  (source)    │   (CI/CD)       │  Assets      │  (global edge)  │          │
└──────────────┘                  └──────────────┘                 └──────────┘
                                        │
                                  API calls at runtime
                                        │
                                  ┌─────▼──────┐
                                  │ Serverless  │
                                  │ Functions   │
                                  │ + APIs      │
                                  └────────────┘
```

**JAMstack** = **J**avaScript + **A**PIs + **M**arkup

- Pre-rendered pages for speed and security
- Dynamic features via APIs and serverless functions
- Git-based workflows: push triggers build and deploy

### CI/CD Integration

All modern platforms follow the same pattern:

```bash
# 1. Connect your Git repository (GitHub, GitLab, Bitbucket)
# 2. Configure build settings (framework auto-detected)
# 3. Every push to main → automatic production deployment
# 4. Every pull request → preview deployment with unique URL
```

---

## 2. Vercel

- **Website:** https://vercel.com
- **By:** Vercel Inc. (creators of Next.js)
- **Best for:** React, Next.js, and frontend frameworks
- **Free tier:** Hobby plan (personal, non-commercial)

### 2.1 Key Features

- **Optimized for Next.js** — ISR, Server Components, App Router, middleware
- **Edge Runtime** — run code at the edge (lightweight V8 isolates)
- **Serverless Functions** — Node.js, Python, Go, Ruby backends
- **Preview Deployments** — every PR gets a unique URL
- **Analytics** — Web Vitals, speed insights, audience metrics
- **Image Optimization** — automatic resizing, format conversion, lazy loading
- **Cron Jobs** — scheduled serverless function execution

### 2.2 Getting Started

```bash
# Install CLI
npm i -g vercel

# Deploy from project directory
cd my-project
vercel

# Deploy to production
vercel --prod

# Link to existing project
vercel link
```

### 2.3 GitHub Integration

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Vercel auto-detects the framework and configures build settings
4. Every push to `main` deploys to production
5. Every PR creates a preview deployment

### 2.4 Configuration (vercel.json)

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1"],
  "rewrites": [
    { "source": "/api/:path*", "destination": "/api/:path*" },
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "s-maxage=60" }
      ]
    }
  ],
  "crons": [
    { "path": "/api/cron/daily", "schedule": "0 8 * * *" }
  ]
}
```

### 2.5 Serverless Functions

```javascript
// api/hello.js — automatically becomes /api/hello
export default function handler(req, res) {
    const { name } = req.query;
    res.status(200).json({ message: `Hello, ${name || 'world'}!` });
}
```

```python
# api/hello.py — Python serverless function
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Hello from Python!"}).encode())
```

### 2.6 Environment Variables

```bash
# Add via CLI
vercel env add DATABASE_URL production
vercel env add API_KEY preview development

# Or in dashboard: Settings → Environment Variables
# Variables are encrypted and injected at build/runtime
```

### 2.7 Free Tier Limits

| Resource | Hobby (Free) | Pro ($20/mo) |
|----------|-------------|--------------|
| **Bandwidth** | 100 GB/mo | 1 TB/mo |
| **Serverless Execution** | 100 GB-hrs/mo | 1,000 GB-hrs/mo |
| **Builds** | 6,000 min/mo | 24,000 min/mo |
| **Concurrent Builds** | 1 | 12 |
| **Image Optimization** | 1,000 source images | 5,000 source images |
| **Team members** | 1 (personal) | Unlimited |
| **Commercial use** | No | Yes |

### 2.8 Supported Frameworks

Next.js, Nuxt, SvelteKit, Astro, Remix, Gatsby, Angular, Vue, React (CRA), Vite, Hugo, Jekyll, Eleventy, Docusaurus, and 30+ more with auto-detection.

---

## 3. Netlify

- **Website:** https://netlify.com
- **By:** Netlify Inc.
- **Best for:** Static sites, JAMstack, serverless backends
- **Free tier:** Starter plan

### 3.1 Key Features

- **Build Plugins** — extend the build process with community or custom plugins
- **Netlify Forms** — collect form submissions without backend code
- **Netlify Identity** — user authentication and management
- **Split Testing** — A/B test different branches
- **Large Media** — Git LFS-backed large file handling
- **Deploy Previews** — unique URL per pull request

### 3.2 Getting Started

```bash
# Install CLI
npm install netlify-cli -g

# Login
netlify login

# Initialize in project directory
cd my-project
netlify init

# Deploy (draft)
netlify deploy

# Deploy to production
netlify deploy --prod

# Local development server
netlify dev
```

### 3.3 Configuration (netlify.toml)

```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

# Redirect SPA routes
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# Custom headers
[[headers]]
  for = "/api/*"
  [headers.values]
    Cache-Control = "public, max-age=60"
    Access-Control-Allow-Origin = "*"

# Serverless function directory
[functions]
  directory = "netlify/functions"

# Branch deploy settings
[context.production]
  command = "npm run build:prod"

[context.deploy-preview]
  command = "npm run build:preview"
```

### 3.4 Netlify Functions (AWS Lambda)

```javascript
// netlify/functions/hello.js
exports.handler = async (event, context) => {
    const name = event.queryStringParameters?.name || 'world';
    return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: `Hello, ${name}!` })
    };
};
// Accessible at: /.netlify/functions/hello?name=Alice
```

### 3.5 Netlify Edge Functions (Deno)

```javascript
// netlify/edge-functions/geolocation.js
export default async (request, context) => {
    const country = context.geo?.country?.name || 'Unknown';
    return new Response(`Hello from ${country}!`, {
        headers: { 'Content-Type': 'text/plain' }
    });
};

export const config = { path: "/geo" };
```

### 3.6 Netlify Forms

```html
<!-- Add netlify attribute to any form — no backend needed -->
<form name="contact" method="POST" data-netlify="true">
    <input type="text" name="name" required />
    <input type="email" name="email" required />
    <textarea name="message"></textarea>
    <button type="submit">Send</button>
</form>
<!-- Submissions appear in Netlify dashboard -->
```

### 3.7 Free Tier Limits

| Resource | Starter (Free) | Pro ($19/mo) |
|----------|----------------|--------------|
| **Bandwidth** | 100 GB/mo | 1 TB/mo |
| **Build minutes** | 300 min/mo | 25,000 min/mo |
| **Serverless Functions** | 125K requests/mo | 2M requests/mo |
| **Edge Functions** | 3M invocations/mo | 6M invocations/mo |
| **Forms** | 100 submissions/mo | Unlimited |
| **Identity** | 1,000 users | Unlimited |
| **Concurrent builds** | 1 | 3 |
| **Team members** | 1 | Unlimited |

---

## 4. Firebase Studio

- **Website:** https://firebase.google.com
- **By:** Google
- **Type:** Cloud-based IDE and full-stack development platform
- **Best for:** Rapid prototyping, Firebase-integrated apps

### 4.1 Overview

Firebase Studio is Google's cloud-based development environment that combines an AI-powered IDE with the full Firebase ecosystem. It integrates Gemini AI for code assistance and allows developers to prototype, build, and deploy applications directly from the browser.

### 4.2 Key Features

- **Cloud-based IDE** — VS Code-like editor running in the browser
- **Gemini AI integration** — code suggestions, explanations, and debugging assistance
- **App prototyping** — generate app scaffolds from natural language descriptions
- **One-click deploy** — deploy directly to Firebase Hosting from the IDE
- **Firebase services** — integrated access to the full Firebase platform

### 4.3 Firebase Services Integration

| Service | Description |
|---------|-------------|
| **Firebase Hosting** | Fast, secure static + dynamic hosting with global CDN |
| **Cloud Firestore** | NoSQL document database with real-time sync |
| **Firebase Auth** | User authentication (email, Google, GitHub, phone, anonymous) |
| **Cloud Storage** | File storage for user-generated content (images, videos) |
| **Cloud Functions** | Serverless Node.js/Python backends triggered by events |
| **Firebase Realtime Database** | Low-latency JSON database for real-time apps |
| **Firebase Extensions** | Pre-built solutions (Stripe payments, image resize, email) |

### 4.4 Firebase Hosting Setup

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize project
firebase init hosting

# Deploy
firebase deploy --only hosting
```

### 4.5 Firebase Hosting Configuration

```json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      { "source": "/api/**", "function": "api" },
      { "source": "**", "destination": "/index.html" }
    ],
    "headers": [
      {
        "source": "**/*.@(js|css)",
        "headers": [{ "key": "Cache-Control", "value": "max-age=31536000" }]
      }
    ]
  }
}
```

### 4.6 Cloud Functions Example

```javascript
const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

// HTTP function
exports.api = functions.https.onRequest((req, res) => {
    res.json({ message: 'Hello from Firebase!' });
});

// Firestore trigger
exports.onUserCreate = functions.firestore
    .document('users/{userId}')
    .onCreate((snap, context) => {
        const user = snap.data();
        console.log(`New user: ${user.name}`);
        return admin.firestore().collection('stats').doc('users').update({
            count: admin.firestore.FieldValue.increment(1)
        });
    });
```

### 4.7 Project Setup in Firebase Studio

1. Open Firebase Studio from the Firebase Console
2. Create a new workspace or import from GitHub
3. Use Gemini to describe the app you want to build
4. Firebase Studio generates a project scaffold
5. Edit, test, and preview in the browser IDE
6. Deploy to Firebase Hosting with one click

---

## 5. Comparison Table

| Feature | Vercel | Netlify | Firebase Studio |
|---------|--------|---------|-----------------|
| **Best for** | Next.js, React apps | Static/JAMstack sites | Full-stack Firebase apps |
| **Free bandwidth** | 100 GB/mo | 100 GB/mo | 360 MB/day (10 GB/mo) |
| **Serverless functions** | Node, Python, Go, Ruby | Node (Lambda-based) | Node, Python (Cloud Functions) |
| **Edge functions** | Yes (Edge Runtime) | Yes (Deno-based) | No (CDN caching only) |
| **Database** | No (bring your own) | No (bring your own) | Firestore, Realtime Database |
| **Authentication** | No (bring your own) | Netlify Identity | Firebase Auth |
| **File storage** | No | Netlify Large Media | Cloud Storage |
| **Forms** | No | Built-in (free) | No (use Firestore) |
| **AI assistance** | v0 (AI UI generator) | No | Gemini integration |
| **Cloud IDE** | No | No | Yes (browser-based) |
| **Framework detection** | 30+ frameworks | 30+ frameworks | Firebase-focused |
| **Preview deploys** | Per PR | Per PR | Manual |
| **Custom domains** | Free | Free | Free |
| **SSL/TLS** | Automatic | Automatic | Automatic |
| **Git integration** | GitHub, GitLab, Bitbucket | GitHub, GitLab, Bitbucket | GitHub |
| **CLI** | `vercel` | `netlify` | `firebase` |

### Quick Decision Guide

| Scenario | Recommended Platform |
|----------|---------------------|
| Next.js application | **Vercel** (native support, ISR, edge) |
| Static site with forms | **Netlify** (built-in forms, identity) |
| Full-stack with database | **Firebase Studio** (Firestore, Auth, Functions) |
| A/B testing branches | **Netlify** (split testing) |
| AI-assisted prototyping | **Firebase Studio** (Gemini) |
| Multiple framework support | **Vercel** or **Netlify** (both auto-detect) |

---

## See Also

- [Cloud Platforms](cloud-platforms.md) — GCP, Google Colab, Kaggle, and more
- [Docker Essentials](../devtools/docker-essentials.md) — Containerized deployments and self-hosting
- [Tunneling Tools](../networking/tunneling-tools.md) — Expose local development servers publicly
- [APIs & Resources](../reference/apis-and-resources.md) — API services and developer tools
