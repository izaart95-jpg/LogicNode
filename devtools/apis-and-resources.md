# APIs & Developer Resources

A comprehensive guide to APIs — what they are, how they work, types, authentication methods, useful public APIs, and real-world examples for developers and hackers.

---

## Table of Contents
1. [What is an API?](#1-what-is-an-api)
2. [API Types](#2-api-types)
3. [Authentication Methods](#3-authentication-methods)
4. [HTTP Methods & Status Codes](#4-http-methods--status-codes)
5. [Data Formats](#5-data-formats)
6. [Working with APIs (Tools & Examples)](#6-working-with-apis-tools--examples)
7. [GitHub API — Deep Reference](#7-github-api--deep-reference)
8. [Useful Public APIs](#8-useful-public-apis)
9. [API Discovery & Collections](#9-api-discovery--collections)
10. [Rate Limiting & Best Practices](#10-rate-limiting--best-practices)
11. [Building Your Own API](#11-building-your-own-api)

---

## 1. What is an API?

**API** (Application Programming Interface) is a set of rules and endpoints that allows software to communicate with other software. Instead of using a GUI, you send structured requests (usually HTTP) and get structured responses (usually JSON).

```
┌──────────┐     HTTP Request      ┌──────────┐     Query      ┌──────────┐
│  Client   │ ──────────────────▶  │   API    │ ────────────▶  │ Database │
│  (you)    │                      │  Server  │                │ / Service│
│           │ ◀──────────────────  │          │ ◀────────────  │          │
│           │     JSON Response    │          │    Results     │          │
└──────────┘                      └──────────┘                └──────────┘
```

**Real-world analogy:** A restaurant menu is an API. You (client) read the menu (documentation), place an order (request), and the kitchen (server) returns your food (response). You don't need to know how the kitchen works.

---

## 2. API Types

### 2.1 REST (Representational State Transfer)

The most common API architecture. Uses standard HTTP methods on resource URLs.

**Principles:**
- **Stateless** — each request contains all info needed; server stores no session
- **Resource-based** — URLs represent resources (`/users`, `/posts/123`)
- **HTTP methods** — GET (read), POST (create), PUT (update), DELETE (remove)
- **JSON responses** — standard data format

```bash
# REST examples
GET    https://api.example.com/users          # List users
GET    https://api.example.com/users/42       # Get user 42
POST   https://api.example.com/users          # Create user
PUT    https://api.example.com/users/42       # Update user 42
PATCH  https://api.example.com/users/42       # Partial update
DELETE https://api.example.com/users/42       # Delete user 42
```

**Characteristics:**
| Aspect | REST |
|--------|------|
| Protocol | HTTP/HTTPS |
| Data Format | JSON (usually), XML |
| Stateless | ✅ |
| Caching | ✅ Built-in (HTTP cache headers) |
| Best For | CRUD apps, web/mobile backends, public APIs |

---

### 2.2 GraphQL

Query language for APIs — client specifies exactly what data it needs. Single endpoint.

```graphql
# Single endpoint: POST https://api.example.com/graphql

# Query — get only what you need
query {
  user(id: 42) {
    name
    email
    posts {
      title
      createdAt
    }
  }
}

# Response — exactly what you asked for
{
  "data": {
    "user": {
      "name": "Alice",
      "email": "alice@example.com",
      "posts": [
        { "title": "Hello World", "createdAt": "2025-01-15" }
      ]
    }
  }
}
```

```bash
# GraphQL via curl
curl -X POST https://api.example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: 42) { name email } }"}'
```

| Aspect | GraphQL |
|--------|---------|
| Protocol | HTTP (POST to single endpoint) |
| Data Format | JSON |
| Over-fetching | ❌ (client picks fields) |
| Under-fetching | ❌ (nested queries in one request) |
| Best For | Complex data relationships, mobile apps, dashboards |
| Used By | GitHub (v4), Shopify, Spotify, Facebook |

---

### 2.3 gRPC (Google Remote Procedure Call)

Binary protocol using Protocol Buffers (protobuf). Extremely fast.

```protobuf
// user.proto — define the service
syntax = "proto3";

service UserService {
  rpc GetUser (UserRequest) returns (UserResponse);
  rpc ListUsers (Empty) returns (stream UserResponse);  // streaming!
}

message UserRequest {
  int32 id = 1;
}

message UserResponse {
  int32 id = 1;
  string name = 2;
  string email = 3;
}
```

| Aspect | gRPC |
|--------|------|
| Protocol | HTTP/2 |
| Data Format | Protobuf (binary) |
| Streaming | ✅ (unary, server, client, bidirectional) |
| Performance | ⚡ Much faster than REST/GraphQL |
| Code Generation | ✅ Auto-generate client/server code |
| Best For | Microservices, real-time, IoT, internal APIs |
| Used By | Google, Netflix, Dropbox, Kubernetes |

---

### 2.4 WebSocket

Persistent, bidirectional connection. Server can push data to client in real time.

```javascript
// Client
const ws = new WebSocket('wss://api.example.com/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({ subscribe: 'btc-usd' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Price:', data.price);  // real-time updates
};
```

| Aspect | WebSocket |
|--------|-----------|
| Protocol | WS / WSS (over TCP) |
| Connection | Persistent, bidirectional |
| Best For | Chat, live feeds, gaming, trading, notifications |
| Used By | Binance, Discord, Slack, multiplayer games |

---

### 2.5 SOAP (Simple Object Access Protocol)

Legacy XML-based protocol. Still used in enterprise/banking/government.

```xml
<!-- SOAP Request -->
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetUser xmlns="http://example.com/users">
      <UserId>42</UserId>
    </GetUser>
  </soap:Body>
</soap:Envelope>
```

| Aspect | SOAP |
|--------|------|
| Protocol | HTTP, SMTP, TCP |
| Data Format | XML |
| Best For | Enterprise, banking, legacy systems |
| Status | Legacy — avoid for new projects |

---

### 2.6 Webhooks

**Reverse API** — the server calls YOUR endpoint when something happens. Event-driven.

```
Normal API:  Client ──polls──▶ Server   "Any new data?"  (wasteful)
Webhook:     Server ──pushes──▶ Client   "Here's new data!" (efficient)
```

```bash
# GitHub webhook sends POST to your server when a push happens:
# POST https://yourserver.com/webhook
{
  "action": "push",
  "repository": { "full_name": "user/repo" },
  "commits": [{ "message": "fix bug", "author": "alice" }]
}
```

**Common webhook providers:** GitHub, Stripe, Slack, Discord, Twilio, PayPal, Shopify

---

### 2.7 Server-Sent Events (SSE)

One-way stream from server to client over HTTP. Simpler than WebSocket for read-only feeds.

```bash
# Server sends events as text/event-stream
curl https://api.example.com/stream

data: {"price": 42000, "asset": "BTC"}

data: {"price": 42050, "asset": "BTC"}

data: {"price": 42030, "asset": "BTC"}
```

```javascript
const source = new EventSource('https://api.example.com/stream');
source.onmessage = (event) => console.log(JSON.parse(event.data));
```

| Used By | OpenAI (streaming responses), live sports, stock tickers |

---

### API Types Comparison

| Type | Format | Direction | Real-time | Complexity | Best For |
|------|--------|-----------|-----------|------------|----------|
| **REST** | JSON | Request-Response | ❌ | Low | CRUD, public APIs |
| **GraphQL** | JSON | Request-Response | ❌ (subscriptions exist) | Medium | Complex queries |
| **gRPC** | Protobuf | Bidirectional stream | ✅ | Medium | Microservices, speed |
| **WebSocket** | Any | Bidirectional | ✅ | Medium | Chat, live data |
| **SOAP** | XML | Request-Response | ❌ | High | Enterprise legacy |
| **Webhooks** | JSON | Server→Client push | ✅ (event-driven) | Low | Event notifications |
| **SSE** | Text | Server→Client stream | ✅ | Low | Live feeds |

---

## 3. Authentication Methods

### 3.1 API Key

Simplest method. Pass a key in header or query parameter.

```bash
# In header (preferred)
curl https://api.example.com/data \
  -H "Authorization: Bearer sk-abc123"

# Or custom header
curl https://api.example.com/data \
  -H "X-API-Key: sk-abc123"

# In query param (less secure — visible in logs)
curl "https://api.example.com/data?api_key=sk-abc123"
```

### 3.2 OAuth 2.0

Industry standard for delegated authorization. User grants limited access to third-party apps.

**Flows:**
| Flow | Use Case |
|------|----------|
| **Authorization Code** | Web apps (most common, most secure) |
| **Authorization Code + PKCE** | Mobile/SPA apps |
| **Client Credentials** | Server-to-server (no user involved) |
| **Device Code** | CLI tools, smart TVs |

```
Authorization Code Flow:

1. App redirects user → Provider login page
   GET https://provider.com/oauth/authorize?
     client_id=YOUR_ID&
     redirect_uri=https://yourapp.com/callback&
     response_type=code&
     scope=read:user

2. User logs in, grants permission → redirected back with code
   https://yourapp.com/callback?code=AUTHORIZATION_CODE

3. App exchanges code for token (server-side)
   POST https://provider.com/oauth/token
   { client_id, client_secret, code, redirect_uri, grant_type: "authorization_code" }

4. Provider returns access_token + refresh_token

5. App uses token for API calls
   GET https://api.provider.com/user
   Authorization: Bearer ACCESS_TOKEN
```

### 3.3 JWT (JSON Web Token)

Self-contained token with encoded payload. Server can verify without database lookup.

```
Header.Payload.Signature

eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0MiwiZXhwIjoxNzA0MDY3MjAwfQ.signature_here

# Decoded payload:
{
  "user_id": 42,
  "exp": 1704067200,
  "iat": 1703980800
}
```

```bash
curl https://api.example.com/protected \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..."
```

### 3.4 Basic Auth

Username:password encoded in Base64. Simple but use HTTPS only.

```bash
# Explicit
curl -u username:password https://api.example.com/data

# Same as:
curl https://api.example.com/data \
  -H "Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ="
```

### 3.5 HMAC (Hash-based Message Authentication Code)

Sign requests with a shared secret. Used by AWS, Stripe.

```python
import hmac, hashlib, time

secret = b"your_secret_key"
timestamp = str(int(time.time()))
message = f"GET/api/data{timestamp}".encode()
signature = hmac.new(secret, message, hashlib.sha256).hexdigest()

# Send:
# X-Timestamp: 1704067200
# X-Signature: a1b2c3d4...
```

### Auth Methods Comparison

| Method | Security | Complexity | Stateless | Best For |
|--------|----------|-----------|-----------|----------|
| **API Key** | Medium | Low | ✅ | Public APIs, dev tools |
| **OAuth 2.0** | High | High | ✅ | Third-party access, social login |
| **JWT** | High | Medium | ✅ | Session tokens, microservices |
| **Basic Auth** | Low | Low | ✅ | Internal/quick testing |
| **HMAC** | Very High | High | ✅ | Financial APIs, AWS |

---

## 4. HTTP Methods & Status Codes

### Methods

| Method | Purpose | Idempotent | Safe | Body |
|--------|---------|-----------|------|------|
| **GET** | Read resource | ✅ | ✅ | ❌ |
| **POST** | Create resource | ❌ | ❌ | ✅ |
| **PUT** | Replace resource | ✅ | ❌ | ✅ |
| **PATCH** | Partial update | ❌ | ❌ | ✅ |
| **DELETE** | Remove resource | ✅ | ❌ | Optional |
| **HEAD** | Headers only (no body) | ✅ | ✅ | ❌ |
| **OPTIONS** | Supported methods (CORS preflight) | ✅ | ✅ | ❌ |

### Status Codes

| Code | Meaning | Common Use |
|------|---------|------------|
| **200** | OK | Successful GET/PUT/PATCH |
| **201** | Created | Successful POST |
| **204** | No Content | Successful DELETE |
| **301** | Moved Permanently | URL changed |
| **302** | Found (Temporary Redirect) | OAuth redirects |
| **304** | Not Modified | Cached response valid |
| **400** | Bad Request | Invalid input |
| **401** | Unauthorized | Missing/invalid auth |
| **403** | Forbidden | Valid auth, no permission |
| **404** | Not Found | Resource doesn't exist |
| **405** | Method Not Allowed | Wrong HTTP method |
| **409** | Conflict | Resource conflict (duplicate) |
| **422** | Unprocessable Entity | Validation failed |
| **429** | Too Many Requests | Rate limited |
| **500** | Internal Server Error | Server bug |
| **502** | Bad Gateway | Upstream server error |
| **503** | Service Unavailable | Server overloaded/maintenance |

---

## 5. Data Formats

### JSON (JavaScript Object Notation)
The standard for modern APIs.

```json
{
  "id": 42,
  "name": "Alice",
  "email": "alice@example.com",
  "roles": ["admin", "user"],
  "profile": {
    "avatar": "https://example.com/avatar.jpg",
    "bio": null
  },
  "active": true
}
```

### XML
Legacy, still used in SOAP and some enterprise APIs.

```xml
<user>
  <id>42</id>
  <name>Alice</name>
  <email>alice@example.com</email>
</user>
```

### Protocol Buffers (Protobuf)
Binary, used by gRPC. Smaller and faster than JSON.

### YAML
Used in configs, sometimes in API specs (OpenAPI/Swagger).

### Common Headers

```bash
Content-Type: application/json          # Request body format
Accept: application/json                # Desired response format
Authorization: Bearer <token>           # Auth
User-Agent: MyApp/1.0                   # Client identifier
X-Request-ID: uuid-here                 # Request tracking
Cache-Control: no-cache                 # Caching behavior
```

---

## 6. Working with APIs (Tools & Examples)

### 6.1 curl (Command Line)

```bash
# GET
curl https://api.github.com/users/torvalds

# GET with headers
curl -H "Authorization: Bearer TOKEN" https://api.example.com/me

# POST with JSON body
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# PUT
curl -X PUT https://api.example.com/users/42 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Updated"}'

# DELETE
curl -X DELETE https://api.example.com/users/42

# Verbose (see headers)
curl -v https://api.example.com/data

# Save response
curl -o response.json https://api.example.com/data

# Follow redirects
curl -L https://short.url/abc

# POST form data
curl -X POST https://api.example.com/upload \
  -F "file=@photo.jpg" \
  -F "description=My photo"

# Pretty print JSON (pipe to jq)
curl -s https://api.github.com/users/torvalds | jq .
```

### 6.2 HTTPie (Friendlier curl)

```bash
# Install
pip install httpie

# GET
http https://api.github.com/users/torvalds

# POST
http POST https://api.example.com/users name=Alice email=alice@example.com

# With auth
http -A bearer -a TOKEN https://api.example.com/me

# Download
http --download https://example.com/file.zip
```

### 6.3 Python (requests)

```python
import requests

# GET
r = requests.get('https://api.github.com/users/torvalds')
print(r.json()['name'])  # Linus Torvalds

# POST
r = requests.post('https://api.example.com/users',
    json={'name': 'Alice', 'email': 'alice@example.com'},
    headers={'Authorization': 'Bearer TOKEN'}
)
print(r.status_code)  # 201

# Error handling
r = requests.get('https://api.example.com/data')
r.raise_for_status()  # Raises HTTPError for 4xx/5xx

# Session (reuse connection + auth)
session = requests.Session()
session.headers.update({'Authorization': 'Bearer TOKEN'})
r = session.get('https://api.example.com/me')
```

### 6.4 JavaScript (fetch)

```javascript
// GET
const res = await fetch('https://api.github.com/users/torvalds');
const user = await res.json();
console.log(user.name);

// POST
const res = await fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer TOKEN'
  },
  body: JSON.stringify({ name: 'Alice', email: 'alice@example.com' })
});
```

### 6.5 GUI Tools

| Tool | Type | Free | Notes |
|------|------|------|-------|
| **Postman** | Desktop/Web | ✅ (limited) | Most popular, collections, environments |
| **Insomnia** | Desktop | ✅ | Clean UI, GraphQL support |
| **Bruno** | Desktop | ✅ (open source) | Git-friendly, offline-first |
| **Hoppscotch** | Web | ✅ (open source) | Postman alternative in browser |
| **Thunder Client** | VS Code extension | ✅ | Lightweight, in-editor |
| **RapidAPI (Paw)** | macOS | 💰 | Native macOS, beautiful |

---

## 7. GitHub API — Deep Reference

GitHub has one of the best documented and most useful public APIs.

- **REST API (v3):** `https://api.github.com`
- **GraphQL API (v4):** `https://api.github.com/graphql`
- **Docs:** https://docs.github.com/en/rest

### 7.1 API Discovery Endpoint

The root endpoint returns all available API URLs — a self-documenting map of the entire API:

```bash
curl https://api.github.com
```

```json
{
  "current_user_url": "https://api.github.com/user",
  "current_user_authorizations_html_url": "https://github.com/settings/connections/applications{/client_id}",
  "authorizations_url": "https://api.github.com/authorizations",
  "code_search_url": "https://api.github.com/search/code?q={query}{&page,per_page,sort,order}",
  "commit_search_url": "https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}",
  "emails_url": "https://api.github.com/user/emails",
  "emojis_url": "https://api.github.com/emojis",
  "events_url": "https://api.github.com/events",
  "feeds_url": "https://api.github.com/feeds",
  "followers_url": "https://api.github.com/user/followers",
  "following_url": "https://api.github.com/user/following{/target}",
  "gists_url": "https://api.github.com/gists{/gist_id}",
  "hub_url": "https://api.github.com/hub",
  "issue_search_url": "https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}",
  "issues_url": "https://api.github.com/issues",
  "keys_url": "https://api.github.com/user/keys",
  "label_search_url": "https://api.github.com/search/labels?q={query}&repository_id={repository_id}{&page,per_page}",
  "notifications_url": "https://api.github.com/notifications",
  "organization_url": "https://api.github.com/orgs/{org}",
  "organization_repositories_url": "https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}",
  "organization_teams_url": "https://api.github.com/orgs/{org}/teams",
  "public_gists_url": "https://api.github.com/gists/public",
  "rate_limit_url": "https://api.github.com/rate_limit",
  "repository_url": "https://api.github.com/repos/{owner}/{repo}",
  "repository_search_url": "https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}",
  "current_user_repositories_url": "https://api.github.com/user/repos{?type,page,per_page,sort}",
  "starred_url": "https://api.github.com/user/starred{/owner}{/repo}",
  "starred_gists_url": "https://api.github.com/gists/starred",
  "topic_search_url": "https://api.github.com/search/topics?q={query}{&page,per_page}",
  "user_url": "https://api.github.com/users/{user}",
  "user_organizations_url": "https://api.github.com/user/orgs",
  "user_repositories_url": "https://api.github.com/users/{user}/repos{?type,page,per_page,sort}",
  "user_search_url": "https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"
}
```

**How to read the template URLs:**
- `{user}` — replace with actual username
- `{owner}/{repo}` — replace with owner and repo name
- `{?page,per_page,sort}` — optional query parameters
- `{&page,per_page,sort,order}` — additional optional query parameters
- `{/gist_id}` — optional path segment

### 7.2 Public Endpoints (No Auth Required)

```bash
# ── User Info ──
curl -s https://api.github.com/users/torvalds | jq .
curl -s https://api.github.com/users/torvalds/repos?sort=stars | jq '.[].name'
curl -s https://api.github.com/users/torvalds/followers | jq '.[].login'
curl -s https://api.github.com/users/torvalds/following | jq '.[].login'
curl -s https://api.github.com/users/torvalds/gists | jq .
curl -s https://api.github.com/users/torvalds/starred | jq '.[].full_name'
curl -s https://api.github.com/users/torvalds/events/public | jq '.[].type'
curl -s https://api.github.com/users/torvalds/received_events/public | jq .

# ── Repository Info ──
curl -s https://api.github.com/repos/torvalds/linux | jq '{stars: .stargazers_count, forks: .forks_count, language: .language}'
curl -s https://api.github.com/repos/torvalds/linux/commits | jq '.[0].commit.message'
curl -s https://api.github.com/repos/torvalds/linux/commits?per_page=5 | jq '.[].commit.message'
curl -s https://api.github.com/repos/torvalds/linux/languages | jq .
curl -s https://api.github.com/repos/torvalds/linux/contributors?per_page=5 | jq '.[].login'
curl -s https://api.github.com/repos/torvalds/linux/tags | jq '.[0:5] | .[].name'
curl -s https://api.github.com/repos/torvalds/linux/branches | jq '.[].name'
curl -s https://api.github.com/repos/torvalds/linux/topics | jq .
curl -s https://api.github.com/repos/microsoft/vscode/releases/latest | jq '{tag: .tag_name, date: .published_at}'

# ── Repo Contents (browse files via API) ──
curl -s https://api.github.com/repos/torvalds/linux/contents/ | jq '.[].name'
curl -s https://api.github.com/repos/torvalds/linux/contents/README | jq .
# File content is base64-encoded in .content field

# ── Repo README (rendered) ──
curl -s -H "Accept: application/vnd.github.html" \
  https://api.github.com/repos/torvalds/linux/readme

# ── Search ──
# Repos by stars
curl -s "https://api.github.com/search/repositories?q=stars:>100000&sort=stars" | jq '.items[].full_name'

# Repos by language + topic
curl -s "https://api.github.com/search/repositories?q=language:python+topic:ai&sort=stars" | jq '.items[0:5] | .[].full_name'

# Users by location
curl -s "https://api.github.com/search/users?q=location:japan+followers:>1000" | jq '.items[].login'

# Code search (find files across all repos)
curl -s "https://api.github.com/search/code?q=filename:docker-compose.yml+org:google" | jq '.items[0:3] | .[].repository.full_name'

# Issues/PRs
curl -s "https://api.github.com/search/issues?q=repo:torvalds/linux+is:issue+is:open&per_page=5" | jq '.items[].title'

# Topics
curl -s "https://api.github.com/search/topics?q=machine-learning" | jq '.items[0:5] | .[].name'

# Commits
curl -s "https://api.github.com/search/commits?q=author:torvalds+repo:torvalds/linux" \
  -H "Accept: application/vnd.github.cloak-preview+json" | jq '.items[0].commit.message'

# ── Organization ──
curl -s https://api.github.com/orgs/google | jq '{name: .name, repos: .public_repos, members: .public_members_url}'
curl -s "https://api.github.com/orgs/google/repos?sort=stars&per_page=10" | jq '.[].full_name'
curl -s https://api.github.com/orgs/google/members | jq '.[].login'

# ── Miscellaneous ──
curl -s https://api.github.com/emojis | jq 'keys[0:10]'                    # All emojis
curl -s https://api.github.com/rate_limit | jq .rate                       # Rate limit status
curl -s https://api.github.com/events | jq '.[0:3] | .[].type'            # Real-time public activity
curl -s https://api.github.com/gitignore/templates | jq .                  # .gitignore templates
curl -s https://api.github.com/gitignore/templates/Python | jq .source     # Python .gitignore
curl -s https://api.github.com/licenses | jq '.[].key'                    # Available licenses
curl -s https://api.github.com/licenses/mit | jq .body                    # MIT license text
curl -s https://api.github.com/meta | jq .                                # GitHub IP ranges, SSH keys
```

### 7.3 Authenticated Endpoints

Create a personal access token at: https://github.com/settings/tokens

```bash
TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
AUTH="-H \"Authorization: Bearer $TOKEN\""

# ── Your Profile ──
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user/emails
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user/repos
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user/starred
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user/followers
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user/following
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user/keys
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/user/orgs
curl -H "Authorization: Bearer $TOKEN" https://api.github.com/notifications

# ── Create a Repo ──
curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/user/repos \
  -d '{
    "name": "my-new-repo",
    "description": "Created via API",
    "private": false,
    "auto_init": true
  }'

# ── Delete a Repo ──
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO

# ── Update Repo ──
curl -X PATCH -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO \
  -d '{"description": "Updated via API", "has_issues": true}'

# ── Create an Issue ──
curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO/issues \
  -d '{"title": "Bug report", "body": "Something is broken", "labels": ["bug"]}'

# ── Comment on Issue ──
curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO/issues/1/comments \
  -d '{"body": "Working on this!"}'

# ── Star / Unstar a Repo ──
curl -X PUT -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/user/starred/torvalds/linux
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/user/starred/torvalds/linux

# ── Follow / Unfollow a User ──
curl -X PUT -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/user/following/torvalds
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/user/following/torvalds

# ── Create a Gist ──
curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/gists \
  -d '{
    "description": "My gist",
    "public": true,
    "files": {
      "hello.py": { "content": "print(\"Hello from API!\")" },
      "notes.md": { "content": "# Notes\n\nCreated via GitHub API" }
    }
  }'

# ── Create / Update File in Repo ──
# Content must be base64-encoded
curl -X PUT -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO/contents/hello.txt \
  -d '{
    "message": "Create hello.txt via API",
    "content": "'$(echo -n "Hello World" | base64)'"
  }'

# ── Add SSH Key ──
curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/user/keys \
  -d '{"title": "My Laptop", "key": "ssh-ed25519 AAAA..."}'

# ── Create Webhook ──
curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO/hooks \
  -d '{
    "name": "web",
    "active": true,
    "events": ["push", "pull_request"],
    "config": {
      "url": "https://yourserver.com/webhook",
      "content_type": "json",
      "secret": "your-webhook-secret"
    }
  }'

# ── Create a Pull Request ──
curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO/pulls \
  -d '{
    "title": "My Feature",
    "body": "Description of changes",
    "head": "feature-branch",
    "base": "main"
  }'
```

### 7.4 GitHub GraphQL API (v4)

Single endpoint, requires auth. Much more powerful for complex queries.

```bash
# Basic query — your profile + top repos
curl -X POST https://api.github.com/graphql \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { viewer { login name repositories(first: 5, orderBy: {field: STARGAZERS, direction: DESC}) { nodes { name stargazerCount description } } } }"
  }'

# Query any user with nested data
curl -X POST https://api.github.com/graphql \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { user(login: \"torvalds\") { name bio repositories(first: 3, orderBy: {field: STARGAZERS, direction: DESC}) { nodes { name stargazerCount forkCount languages(first: 3) { nodes { name } } } } followers { totalCount } } }"
  }'
```

**GraphQL Explorer (interactive):** https://docs.github.com/en/graphql/overview/explorer

### 7.5 GitHub API Rate Limits

| Auth Level | Requests/Hour | Search Requests/Min |
|------------|--------------|---------------------|
| **No auth** | 60 | 10 |
| **Personal token** | 5,000 | 30 |
| **GitHub App** | 15,000+ | 30 |

```bash
# Check your remaining limits
curl -s https://api.github.com/rate_limit | jq '.rate'
# With auth:
curl -s -H "Authorization: Bearer $TOKEN" https://api.github.com/rate_limit | jq '.resources'
```

### 7.6 Pagination

GitHub returns max 100 items per page. Use `Link` header for navigation.

```bash
# First page, 100 items
curl -s "https://api.github.com/users/torvalds/repos?per_page=100&page=1"

# Check Link header for next page
curl -sI "https://api.github.com/users/torvalds/repos?per_page=10" | grep -i link
# Link: <https://api.github.com/users/...?per_page=10&page=2>; rel="next", ...

# Python pagination
import requests

def get_all_pages(url, headers=None):
    results = []
    while url:
        r = requests.get(url, headers=headers)
        results.extend(r.json())
        url = r.links.get('next', {}).get('url')
    return results

repos = get_all_pages('https://api.github.com/users/torvalds/repos?per_page=100')
```

---

## 8. Useful Public APIs

### 8.1 Master List

📚 **https://github.com/public-apis/public-apis** — The definitive collection of **1,400+ free public APIs**, categorized by topic: animals, anime, anti-malware, art, books, business, calendar, cloud, cryptocurrency, data, design, dictionaries, documents, email, entertainment, environment, events, finance, food, games, geocoding, government, health, jobs, machine learning, music, news, open data, open source, patent, personality, phone, photography, programming, science, security, shopping, social, sports, test data, text analysis, tracking, transportation, URL shorteners, vehicle, video, weather.

### 8.2 No Auth Required (Just Call Them)

| API | Endpoint | Returns |
|-----|----------|---------|
| **IP Info** | `https://ipinfo.io/json` | Your IP, location, ISP |
| **IP API** | `http://ip-api.com/json` | IP geolocation |
| **Dog Pictures** | `https://dog.ceo/api/breeds/image/random` | Random dog image |
| **Cat Facts** | `https://catfact.ninja/fact` | Random cat fact |
| **Bored API** | `https://bored-api.appbrewery.com/random` | Random activity suggestion |
| **Advice Slip** | `https://api.adviceslip.com/advice` | Random advice |
| **Joke API** | `https://v2.jokeapi.dev/joke/Any` | Random joke |
| **Useless Facts** | `https://uselessfacts.jsph.pl/api/v2/facts/random` | Random useless fact |
| **Lorem Picsum** | `https://picsum.photos/400/300` | Random placeholder image |
| **HTTPBin** | `https://httpbin.org/get` | Echo your request back |
| **JSON Placeholder** | `https://jsonplaceholder.typicode.com/posts` | Fake REST API for testing |
| **Pokemon API** | `https://pokeapi.co/api/v2/pokemon/pikachu` | Pokemon data |
| **Open Trivia** | `https://opentdb.com/api.php?amount=10` | Quiz questions |
| **Numbers API** | `http://numbersapi.com/42` | Fun facts about numbers |
| **ISS Location** | `http://api.open-notify.org/iss-now.json` | Current ISS position |
| **Sunrise/Sunset** | `https://api.sunrise-sunset.org/json?lat=36.72&lng=-4.42` | Sun times |
| **Exchange Rates** | `https://open.er-api.com/v6/latest/USD` | Currency exchange rates |
| **Country Info** | `https://restcountries.com/v3.1/name/japan` | Country data |
| **University List** | `http://universities.hipolabs.com/search?country=japan` | Universities by country |
| **GitHub API** | `https://api.github.com/users/torvalds` | GitHub user data |
| **Open Meteo** | `https://api.open-meteo.com/v1/forecast?latitude=35.68&longitude=139.76&current=temperature_2m` | Weather forecast |

```bash
# Try them all
curl -s https://ipinfo.io/json | jq .
curl -s https://dog.ceo/api/breeds/image/random | jq .message
curl -s https://v2.jokeapi.dev/joke/Programming | jq .
curl -s https://jsonplaceholder.typicode.com/posts/1 | jq .
curl -s https://pokeapi.co/api/v2/pokemon/charizard | jq '{name: .name, hp: .stats[0].base_stat}'
curl -s http://api.open-notify.org/iss-now.json | jq .iss_position
curl -s https://open.er-api.com/v6/latest/USD | jq '.rates.EUR'
curl -s https://restcountries.com/v3.1/name/japan | jq '.[0] | {name: .name.common, capital: .capital[0], population}'
```

### 8.3 Gaming & Minecraft APIs

| API | Endpoint | Description |
|-----|----------|-------------|
| **MineSkin** | `https://api.mineskin.org` | Generate Minecraft skins from URLs/uploads |
| **Mojang API** | `https://api.mojang.com/users/profiles/minecraft/{username}` | UUID lookup |
| **Mojang Session** | `https://sessionserver.mojang.com/session/minecraft/profile/{uuid}` | Full profile + skin |
| **Crafatar** | `https://crafatar.com/avatars/{uuid}` | Minecraft avatar images |
| **MC Server Status** | `https://api.mcsrvstat.us/3/{ip}` | Minecraft server status |
| **PokeAPI** | `https://pokeapi.co/api/v2/` | Complete Pokemon database |

**MineSkin (https://mineskin.eu):**

MineSkin generates valid Minecraft skin data (texture value + signature) that can be used in plugins, launchers, and NPC systems. It handles the Mojang signing process for you.

```bash
# Generate skin from a URL (returns signed texture data)
curl -X POST https://api.mineskin.org/generate/url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/skin.png",
    "variant": "classic",
    "name": "my-skin",
    "visibility": 0
  }'

# Response includes:
# - data.texture.value — base64 texture (use in game)
# - data.texture.signature — Mojang-signed signature
# - data.uuid — temporary profile UUID

# Get skin data by ID
curl -s https://api.mineskin.org/get/id/12345 | jq .

# Get skin by UUID
curl -s https://api.mineskin.org/get/uuid/069a79f444e94726a5befca90e38aaf5 | jq .

# List skins
curl -s "https://api.mineskin.org/get/list/1?size=20" | jq .

# Upload skin file directly
curl -X POST https://api.mineskin.org/generate/upload \
  -F "file=@skin.png" \
  -F "variant=classic"

# Rate limit: ~1 request per minute for free tier
# Auth: optional API key for higher limits
# Docs: https://docs.mineskin.org
```

**Use cases for MineSkin:**
- Custom NPC skins in Bukkit/Spigot plugins
- Custom launcher skin previews
- Skin-based avatar systems
- Server shop/cosmetic plugins

**Mojang API Examples:**

```bash
# Username → UUID
curl -s https://api.mojang.com/users/profiles/minecraft/Notch | jq .
# {"name":"Notch","id":"069a79f444e94726a5befca90e38aaf5"}

# UUID → Profile (includes skin/cape texture data)
curl -s https://sessionserver.mojang.com/session/minecraft/profile/069a79f444e94726a5befca90e38aaf5 | jq .
# The .properties[0].value is base64 — decode it:
curl -s https://sessionserver.mojang.com/session/minecraft/profile/069a79f444e94726a5befca90e38aaf5 | \
  jq -r '.properties[0].value' | base64 -d | jq .

# Blocked servers (SHA1 hashes)
curl -s https://sessionserver.mojang.com/blockedservers | head -5

# Bulk username → UUID (POST, up to 10 names)
curl -X POST https://api.mojang.com/profiles/minecraft \
  -H "Content-Type: application/json" \
  -d '["Notch", "jeb_", "Dinnerbone"]'
```

**Crafatar (avatar images — no API key needed):**

```bash
# Avatar (face)
https://crafatar.com/avatars/069a79f444e94726a5befca90e38aaf5?size=128

# Head (3D rendered)
https://crafatar.com/renders/head/069a79f444e94726a5befca90e38aaf5

# Body (full 3D render)
https://crafatar.com/renders/body/069a79f444e94726a5befca90e38aaf5

# Skin file
https://crafatar.com/skins/069a79f444e94726a5befca90e38aaf5

# Cape
https://crafatar.com/capes/069a79f444e94726a5befca90e38aaf5

# Options: ?size=128&overlay (adds hat layer)
```

**Minecraft Server Status:**

```bash
# Check any MC server
curl -s https://api.mcsrvstat.us/3/hypixel.net | jq '{online: .online, players: .players, version: .version, motd: .motd.clean}'
curl -s https://api.mcsrvstat.us/3/play.example.com:25565 | jq .

# Bedrock servers
curl -s https://api.mcsrvstat.us/bedrock/3/play.example.com | jq .

# Server icon
https://api.mcsrvstat.us/icon/hypixel.net
```

**Free Fire APIs:**

Unofficial developer APIs for Garena Free Fire — player stats, profiles, and redeem codes.

**FreeFire-Api (0xMe)**

- **Repository:** https://github.com/0xMe/FreeFire-Api
- **Language:** Python + Flask
- **Type:** Internal Free Fire API client using Protocol Buffers

Interacts with Free Fire's internal game servers using compiled protobuf schemas and encrypted requests — the same protocol the official client uses. Requires account credentials per server region.
```bash
git clone https://github.com/0xMe/FreeFire-Api.git
cd FreeFire-Api
pip install -r requirements.txt
# Add credentials to ./Configuration/AccountConfiguration.json
python app.py   # Starts Flask API on :5000
```

**Endpoints (examples):**
- `GET /get_player_stats?server=ind&uid=11959685790&matchmode=RANKED&gamemode=br`
- Player profile, rank, guild, personal show data, pet info

**Supported regions:** IND, BR, US, SG, RU, ID, TW, VN, TH, ME, PK, CIS, BD, NA

**Note:** Uses your own FF account credentials to authenticate requests. Marked "OLD SOURCE BUT WORKING" by the author — treat as research/educational.

---

**HL Gaming Free Fire Redeem Codes (dlt source)**

- **dlt source:** https://dlthub.com/context/source/hl-gaming-free-fire-redeem-codes
- **Type:** dlt (data load tool) pipeline source for Free Fire redeem codes

A `dlt` pipeline source that fetches active Free Fire redeem codes from HL Gaming Official's API. Useful for building bots or dashboards that automatically surface valid redeem codes.
```python
import dlt
from hl_gaming_free_fire_redeem_codes import hl_gaming_free_fire_redeem_codes_source

pipeline = dlt.pipeline(
    pipeline_name="ff_redeem_codes",
    destination="duckdb",
    dataset_name="freefire"
)

source = hl_gaming_free_fire_redeem_codes_source()
load_info = pipeline.run(source)
print(load_info)
# Loads active redeem codes into local DuckDB
```

**Use case:** schedule this pipeline (cron/Airflow/n8n) to refresh a codes database, then surface them via a bot or website automatically.

### 8.4 AI & ML APIs

| API | Auth | Endpoint | Description |
|-----|------|----------|-------------|
| **Pollinations Text** | ❌ | `https://text.pollinations.ai/{prompt}` | Free AI text |
| **Pollinations Image** | ❌ | `https://image.pollinations.ai/prompt/{prompt}` | Free AI images |
| **Hugging Face** | API Key | `https://api-inference.huggingface.co/models/` | 200,000+ models |
| **OpenRouter** | API Key | `https://openrouter.ai/api/v1/chat/completions` | Multi-model gateway |
| **Groq** | API Key | `https://api.groq.com/openai/v1/chat/completions` | Ultra-fast inference |
| **Together AI** | API Key | `https://api.together.xyz/v1/chat/completions` | Open-source models |

```bash
# Pollinations (no key!)
curl "https://text.pollinations.ai/Explain%20APIs%20in%20one%20sentence"
curl "https://image.pollinations.ai/prompt/cute%20robot%20coding" -o robot.jpg

# Hugging Face (free API key)
curl https://api-inference.huggingface.co/models/gpt2 \
  -H "Authorization: Bearer hf_xxxxx" \
  -d '{"inputs": "The meaning of life is"}'

# OpenRouter (OpenAI-compatible format, many models)
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer sk-or-xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"model": "meta-llama/llama-3-8b-instruct:free", "messages": [{"role": "user", "content": "Hello"}]}'
```

### 8.5 Weather APIs

```bash
# Open-Meteo (free, no key, generous limits)
curl -s "https://api.open-meteo.com/v1/forecast?latitude=35.68&longitude=139.76&current=temperature_2m,wind_speed_10m,weather_code&daily=temperature_2m_max,temperature_2m_min&timezone=auto" | jq .

# wttr.in (terminal weather — beautiful)
curl wttr.in
curl wttr.in/Tokyo
curl wttr.in/Tokyo?format=3        # Compact: Tokyo: ⛅️ +15°C
curl wttr.in/Tokyo?format=j1       # JSON format
curl wttr.in/Moon                   # Moon phase
curl "wttr.in/:help"               # All format options
```

### 8.6 Security & OSINT APIs

| API | URL | Description | Auth |
|-----|-----|-------------|------|
| **Shodan** | `https://api.shodan.io` | Internet-connected device search | API Key |
| **VirusTotal** | `https://www.virustotal.com/api/v3` | Malware/URL scanning | API Key (free) |
| **Have I Been Pwned** | `https://haveibeenpwned.com/api/v3` | Breach checking | API Key |
| **AbuseIPDB** | `https://api.abuseipdb.com/api/v2` | IP reputation | API Key (free) |
| **URLScan** | `https://urlscan.io/api/v1` | URL analysis | API Key (free) |
| **SecurityTrails** | `https://api.securitytrails.com/v1` | DNS/domain intelligence | API Key |
| **Censys** | `https://search.censys.io/api` | Internet asset discovery | API Key |
| **GreyNoise** | `https://api.greynoise.io/v3` | IP threat intelligence | API Key (free) |
| **IPQualityScore** | `https://ipqualityscore.com/api` | Fraud detection | API Key (free) |

```bash
# Shodan — search internet-connected devices
curl "https://api.shodan.io/shodan/host/8.8.8.8?key=YOUR_KEY" | jq .
curl "https://api.shodan.io/shodan/host/search?key=YOUR_KEY&query=apache+country:US" | jq .

# VirusTotal — scan URLs and files
curl -X POST "https://www.virustotal.com/api/v3/urls" \
  -H "x-apikey: YOUR_KEY" \
  -d "url=https://example.com"
# Scan file
curl -X POST "https://www.virustotal.com/api/v3/files" \
  -H "x-apikey: YOUR_KEY" \
  -F "file=@suspicious.exe"

# AbuseIPDB — check IP reputation
curl "https://api.abuseipdb.com/api/v2/check?ipAddress=8.8.8.8&maxAgeInDays=90" \
  -H "Key: YOUR_KEY" -H "Accept: application/json" | jq .

# URLScan — analyze a URL
curl -X POST "https://urlscan.io/api/v1/scan/" \
  -H "API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "visibility": "public"}'
```

### 8.7 Fake/Testing APIs

| API | URL | Purpose |
|-----|-----|---------|
| **JSONPlaceholder** | `https://jsonplaceholder.typicode.com` | Fake REST API (posts, comments, users, todos, albums, photos) |
| **ReqRes** | `https://reqres.in/api` | Fake users API with real HTTP responses |
| **HTTPBin** | `https://httpbin.org` | Echo service (test headers, methods, auth, redirects, cookies) |
| **DummyJSON** | `https://dummyjson.com` | 150+ dummy products, users, carts, recipes |
| **MockAPI** | `https://mockapi.io` | Create your own fake API endpoint |
| **Beeceptor** | `https://beeceptor.com` | Mock server + request inspection |
| **Webhook.site** | `https://webhook.site` | Instant webhook endpoint for testing |

```bash
# JSONPlaceholder — full CRUD simulation
curl -s https://jsonplaceholder.typicode.com/posts | jq '.[0:3]'
curl -s https://jsonplaceholder.typicode.com/posts/1 | jq .
curl -s https://jsonplaceholder.typicode.com/posts/1/comments | jq '.[0:2]'
curl -s https://jsonplaceholder.typicode.com/users | jq '.[0].name'
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","body":"Hello","userId":1}' | jq .

# DummyJSON — rich fake data
curl -s https://dummyjson.com/products | jq '.products[0]'
curl -s https://dummyjson.com/products/search?q=phone | jq '.products[].title'
curl -s https://dummyjson.com/users | jq '.users[0] | {firstName, email}'
curl -s https://dummyjson.com/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"username":"emilys","password":"emilyspass"}' | jq .token

# HTTPBin — see what your request looks like
curl -s https://httpbin.org/get | jq .
curl -s https://httpbin.org/ip | jq .
curl -s https://httpbin.org/headers | jq .
curl -s https://httpbin.org/user-agent | jq .
curl -X POST https://httpbin.org/post -d "key=value" | jq .
curl https://httpbin.org/status/418    # I'm a teapot ☕
curl https://httpbin.org/delay/3       # Delayed response (3s)
curl https://httpbin.org/redirect/3    # Chain of 3 redirects
curl -u user:pass https://httpbin.org/basic-auth/user/pass  # Test basic auth
curl https://httpbin.org/image/png -o test.png              # Test image download
```

### 8.8 Crypto & Finance APIs

```bash
# CoinGecko (free, no key)
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd" | jq .
curl -s "https://api.coingecko.com/api/v3/coins/bitcoin" | jq '{price: .market_data.current_price.usd, market_cap: .market_data.market_cap.usd}'
curl -s "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10" | jq '.[].name'

# Exchange Rates (free, no key)
curl -s "https://open.er-api.com/v6/latest/USD" | jq '.rates | {EUR, GBP, JPY}'

# Binance (no key for public endpoints)
curl -s "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT" | jq .
curl -s "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT" | jq '{price: .lastPrice, volume: .volume, change: .priceChangePercent}'
```

---

## 9. API Discovery & Collections

| Resource | URL | Description |
|----------|-----|-------------|
| **Public APIs** | https://github.com/public-apis/public-apis | 1,400+ free APIs, categorized |
| **RapidAPI Hub** | https://rapidapi.com/hub | Marketplace of 40,000+ APIs |
| **API List** | https://apilist.fun | Curated public API collection |
| **Any API** | https://any-api.com | API documentation aggregator |
| **Postman Collections** | https://www.postman.com/explore | Community API collections |
| **APIs.guru** | https://apis.guru | OpenAPI spec directory |
| **Free APIs** | https://free-apis.github.io | Categorized free APIs |
| **Public API Lists** | https://publicapis.dev | Searchable API directory |
| **DevResources** | https://devresources.info | Developer tools & APIs |
| **No-Auth APIs** | https://mixedanalytics.com/blog/list-actually-free-open-no-auth-needed-apis/ | APIs that truly need no auth |

---

## 10. Rate Limiting & Best Practices

### Understanding Rate Limits

```bash
# Most APIs return rate limit info in response headers:
X-RateLimit-Limit: 60          # Max requests per window
X-RateLimit-Remaining: 45      # Requests left
X-RateLimit-Reset: 1704067200  # Unix timestamp when limit resets
Retry-After: 30                # Seconds to wait (on 429)
```

### Handling Rate Limits in Code

```python
import requests
import time

def api_call_with_retry(url, headers=None, max_retries=3):
    for attempt in range(max_retries):
        r = requests.get(url, headers=headers)

        if r.status_code == 429:  # Rate limited
            retry_after = int(r.headers.get('Retry-After', 60))
            print(f"Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            continue

        r.raise_for_status()
        return r.json()

    raise Exception("Max retries exceeded")


# Exponential backoff
import random

def api_call_backoff(url, headers=None, max_retries=5):
    for attempt in range(max_retries):
        r = requests.get(url, headers=headers)
        if r.status_code == 429:
            wait = (2 ** attempt) + random.uniform(0, 1)  # 1s, 2s, 4s, 8s, 16s
            print(f"Rate limited. Backoff: {wait:.1f}s")
            time.sleep(wait)
            continue
        r.raise_for_status()
        return r.json()
    raise Exception("Max retries exceeded")
```

### Best Practices

1. **Cache responses** — don't re-fetch data that hasn't changed (use `ETag`, `If-Modified-Since`)
2. **Respect rate limits** — check headers, implement exponential backoff
3. **Use pagination** — don't fetch all data at once (`?page=1&per_page=100`)
4. **Handle errors gracefully** — check status codes, parse error messages
5. **Never hardcode API keys** — use environment variables or secret managers
6. **Prefer webhooks over polling** — let the server notify you
7. **Read the docs** — every API is different, read before coding
8. **Use SDKs when available** — official libraries handle auth, pagination, retries
9. **Set User-Agent** — some APIs require/prefer a custom User-Agent
10. **Use HTTPS** — never send credentials over plain HTTP

```bash
# Store API keys in environment variables
export GITHUB_TOKEN="ghp_xxxxx"
export OPENAI_API_KEY="sk-xxxxx"

# Use in curl
curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user

# .env file (for applications)
echo "GITHUB_TOKEN=ghp_xxxxx" >> .env
echo ".env" >> .gitignore   # NEVER commit .env!

# In Python
import os
token = os.environ.get('GITHUB_TOKEN')
```

---

## 11. Building Your Own API

### Quick API with Python (Flask)

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        abort(404)
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data:
        abort(400)
    user = {"id": len(users) + 1, "name": data['name'], "email": data.get('email', '')}
    users.append(user)
    return jsonify(user), 201

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    global users
    users = [u for u in users if u['id'] != id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Quick API with Node.js (Express)

```javascript
const express = require('express');
const app = express();
app.use(express.json());

let users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
];

app.get('/api/users', (req, res) => res.json(users));
app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});
app.post('/api/users', (req, res) => {
  const user = { id: users.length + 1, name: req.body.name };
  users.push(user);
  res.status(201).json(user);
});
app.delete('/api/users/:id', (req, res) => {
  users = users.filter(u => u.id !== parseInt(req.params.id));
  res.status(204).send();
});

app.listen(3000, () => console.log('API running on :3000'));
```

### Expose Your API to the Internet

```bash
# Use tunneling tools (see tunneling-tools.md for full details)
ngrok http 5000
loclx tunnel http --to 5000
cloudflared tunnel --url http://localhost:5000

# Your local API is now accessible at a public URL!
```

---

## See Also

- [AI Platforms & APIs](../ai/platforms-and-apis.md) — AI-specific APIs (OpenRouter, Hugging Face, Pollinations)
- [Tunneling Tools](../networking/tunneling-tools.md) — Ngrok, LocalXpose, Cloudflared for exposing local APIs
- [SSH Tunneling](../networking/ssh-tunneling.md) — SSH-based tunneling for API access
- [Network Protocols](../fundamentals/network-protocols.md) — HTTP, TCP, UDP protocol details
- [Platforms & Communities](platforms-and-communities.md) — Developer resources
