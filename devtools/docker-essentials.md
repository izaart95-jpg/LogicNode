# Docker Essentials — Containers, Images, Compose & Registry

Docker is the standard platform for building, shipping, and running applications inside lightweight, portable containers. Unlike virtual machines, containers share the host kernel and start in milliseconds, making them ideal for microservices, CI/CD pipelines, and reproducible development environments.

---

## Table of Contents
1. [What is Docker?](#1-what-is-docker)
2. [Installation](#2-installation)
3. [Core Concepts](#3-core-concepts)
4. [Essential Commands](#4-essential-commands)
5. [Dockerfile](#5-dockerfile)
6. [Docker Compose](#6-docker-compose)
7. [LibreChat Docker Setup (Worked Example)](#7-librechat-docker-setup-worked-example)
8. [Common Patterns](#8-common-patterns)
9. [Docker Registry](#9-docker-registry)
10. [Comparison Table](#10-comparison-table)

---

## 1. What is Docker?

### Containerization vs Virtualization

```
┌─────────────────────────────────────────────────────────────┐
│  Virtual Machines                 Containers                │
│                                                             │
│  ┌──────┐ ┌──────┐ ┌──────┐    ┌──────┐ ┌──────┐ ┌──────┐│
│  │ App  │ │ App  │ │ App  │    │ App  │ │ App  │ │ App  ││
│  │ Libs │ │ Libs │ │ Libs │    │ Libs │ │ Libs │ │ Libs ││
│  │ OS   │ │ OS   │ │ OS   │    └──┬───┘ └──┬───┘ └──┬───┘│
│  └──┬───┘ └──┬───┘ └──┬───┘       └────────┼────────┘     │
│     └────────┼────────┘             ┌───────▼───────┐      │
│       ┌──────▼──────┐               │ Container     │      │
│       │ Hypervisor  │               │ Runtime       │      │
│       └──────┬──────┘               └───────┬───────┘      │
│       ┌──────▼──────┐               ┌───────▼───────┐      │
│       │  Host OS    │               │  Host OS      │      │
│       └──────┬──────┘               │  (shared      │      │
│       ┌──────▼──────┐               │   kernel)     │      │
│       │  Hardware   │               └───────┬───────┘      │
│       └─────────────┘               ┌───────▼───────┐      │
│                                     │  Hardware     │      │
│  Each VM: full OS (GBs)            └───────────────┘      │
│  Containers: shared kernel (MBs)                           │
└─────────────────────────────────────────────────────────────┘
```

| Aspect | Virtual Machine | Container |
|--------|----------------|-----------|
| **Isolation** | Full OS kernel | Shared host kernel (namespaces, cgroups) |
| **Startup** | Minutes | Seconds / milliseconds |
| **Size** | GBs (full OS) | MBs (app + libs only) |
| **Performance** | Near-native (with KVM) | Native (no hypervisor overhead) |
| **Portability** | Heavy (VM images) | Lightweight (OCI images) |
| **Use case** | Full OS isolation, different kernels | Microservices, CI/CD, dev environments |

### Key Components

- **Docker Engine** — the daemon (`dockerd`) that builds and runs containers on Linux
- **Docker Desktop** — GUI application for Windows/macOS that bundles the engine, CLI, Compose, and a Linux VM
- **Image** — read-only template with filesystem layers (the blueprint)
- **Container** — running instance of an image (the process)
- **Volume** — persistent storage that survives container removal

---

## 2. Installation

### Linux (Debian/Ubuntu — Official Repo)

```bash
# Remove old versions
sudo apt remove docker docker-engine docker.io containerd runc

# Add Docker's official GPG key and repo
sudo apt update
sudo apt install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify
docker --version
docker run hello-world
```

### Linux (Fedora)

```bash
sudo dnf install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl enable --now docker
```

### Windows / macOS

Download **Docker Desktop** from https://www.docker.com/products/docker-desktop/ and follow the installer. On Windows, Docker Desktop uses WSL2 as its backend by default.

### Post-Install: Run Docker Without sudo

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker          # Apply immediately (or log out/in)
docker run hello-world # Should work without sudo
```

---

## 3. Core Concepts

### 3.1 Images

An image is a read-only, layered filesystem template. Each instruction in a Dockerfile creates a new layer.

```bash
# Pull an image from Docker Hub
docker pull nginx:1.25-alpine

# List local images
docker images

# Image naming convention
#   registry/repository:tag
#   docker.io/library/nginx:1.25-alpine   (fully qualified)
#   nginx:1.25-alpine                     (shorthand for Docker Hub)
#   nginx:latest                          (default tag if omitted)
#   ghcr.io/user/myapp:v2.1               (GitHub Container Registry)
```

### 3.2 Containers

A container is a running (or stopped) instance of an image.

```
Image ──► docker run ──► Container (running)
                              │
                    docker stop ──► Container (stopped)
                              │
                    docker rm  ──► (removed)
```

```bash
# Lifecycle
docker create --name myapp nginx      # Create (not started)
docker start myapp                     # Start
docker stop myapp                      # Graceful stop (SIGTERM)
docker kill myapp                      # Force stop (SIGKILL)
docker restart myapp                   # Stop + start
docker rm myapp                        # Remove (must be stopped)
docker rm -f myapp                     # Force remove (even if running)
```

### 3.3 Volumes

Volumes persist data beyond a container's lifecycle.

| Type | Syntax | Use Case |
|------|--------|----------|
| **Named volume** | `-v mydata:/app/data` | Database storage, shared data |
| **Bind mount** | `-v /host/path:/container/path` | Development (live code reload) |
| **tmpfs** | `--tmpfs /tmp` | Sensitive data that shouldn't persist |

```bash
# Create and use a named volume
docker volume create pgdata
docker run -d -v pgdata:/var/lib/postgresql/data postgres:16

# Bind mount (host directory into container)
docker run -d -v $(pwd)/src:/app/src node:20

# List / inspect / remove volumes
docker volume ls
docker volume inspect pgdata
docker volume rm pgdata
docker volume prune              # Remove all unused volumes
```

### 3.4 Networks

Docker networks control how containers communicate.

| Driver | Description |
|--------|-------------|
| **bridge** | Default. Containers on the same bridge can talk by name. |
| **host** | Container shares the host network stack (no isolation). |
| **none** | No networking at all. |
| **custom bridge** | User-defined bridge with DNS-based service discovery. |

```bash
# Create a custom network
docker network create mynet

# Run containers on the same network (they resolve each other by name)
docker run -d --name db --network mynet postgres:16
docker run -d --name app --network mynet -e DB_HOST=db myapp

# List / inspect / remove
docker network ls
docker network inspect mynet
docker network rm mynet
```

---

## 4. Essential Commands

### Container Operations

```bash
# Run a container (most common command)
docker run -d --name webapp -p 8080:80 -v ./html:/usr/share/nginx/html nginx:alpine
#  -d          Detached (background)
#  --name      Assign a name
#  -p 8080:80  Map host:container ports
#  -v          Mount volume or bind mount
#  --rm        Auto-remove on exit (useful for one-off tasks)
#  -e KEY=VAL  Set environment variable
#  -it         Interactive + TTY (for shells)

# Execute a command inside a running container
docker exec -it webapp sh
docker exec webapp cat /etc/nginx/nginx.conf

# View logs
docker logs webapp
docker logs -f webapp              # Follow (tail -f)
docker logs --tail 50 webapp       # Last 50 lines
docker logs --since 10m webapp     # Last 10 minutes

# List containers
docker ps                          # Running only
docker ps -a                       # All (including stopped)

# Inspect container details
docker inspect webapp
docker stats                       # Live resource usage

# Copy files between host and container
docker cp webapp:/etc/nginx/nginx.conf ./nginx.conf
docker cp ./index.html webapp:/usr/share/nginx/html/
```

### Image Operations

```bash
# Search Docker Hub
docker search python

# Pull / tag / push
docker pull python:3.12-slim
docker tag myapp:latest registry.example.com/myapp:v1.0
docker push registry.example.com/myapp:v1.0

# Build from Dockerfile
docker build -t myapp:latest .
docker build -t myapp:v2 -f Dockerfile.prod .

# Remove images
docker rmi nginx:alpine
docker image prune                 # Remove dangling images
docker image prune -a              # Remove all unused images
```

### System Cleanup

```bash
# Nuclear option: remove everything unused
docker system prune -a --volumes

# Individual cleanup
docker container prune             # Remove stopped containers
docker image prune -a              # Remove unused images
docker volume prune                # Remove unused volumes
docker network prune               # Remove unused networks

# Disk usage overview
docker system df
```

---

## 5. Dockerfile

### Basic Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (documentation only)
EXPOSE 8000

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Key Instructions

| Instruction | Purpose |
|-------------|---------|
| `FROM` | Base image (required, must be first) |
| `RUN` | Execute a command during build (creates a layer) |
| `COPY` | Copy files from host into the image |
| `ADD` | Like COPY, but also handles URLs and tar extraction |
| `WORKDIR` | Set the working directory for subsequent instructions |
| `EXPOSE` | Document which port the container listens on |
| `ENV` | Set environment variables |
| `CMD` | Default command when container starts (overridable) |
| `ENTRYPOINT` | Fixed command (arguments appended via CMD or CLI) |

### CMD vs ENTRYPOINT

```dockerfile
# CMD only — easily overridden
CMD ["python", "app.py"]
# docker run myapp                → python app.py
# docker run myapp bash           → bash (CMD replaced)

# ENTRYPOINT + CMD — fixed binary, flexible arguments
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run myapp                → python app.py
# docker run myapp test.py        → python test.py (CMD replaced)
```

### Multi-Stage Build

Produce minimal production images by discarding build dependencies:

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (only the output)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Result: final image contains only Nginx + static files, not Node.js or node_modules.

### .dockerignore

```
node_modules
.git
.env
*.log
dist
Dockerfile
docker-compose*.yml
.dockerignore
```

### Best Practices

- **Order matters for caching** — put infrequently changing layers (dependencies) before frequently changing ones (source code)
- **Use specific tags** — `python:3.12-slim` not `python:latest`
- **Combine RUN commands** — `RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*`
- **Use multi-stage builds** — keep production images small
- **Don't run as root** — add `RUN useradd app && USER app`
- **Use `-slim` or `-alpine` base images** — much smaller than defaults

---

## 6. Docker Compose

Docker Compose defines multi-container applications in a single YAML file.

### docker-compose.yml Structure

```yaml
services:
  webapp:
    build: .                          # Build from Dockerfile in current dir
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=postgres
    volumes:
      - ./src:/app/src                # Bind mount for development
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

### Compose Commands

```bash
# Start all services (detached)
docker compose up -d

# Start and rebuild images
docker compose up -d --build

# Stop and remove containers, networks
docker compose down

# Stop and also remove volumes (data loss!)
docker compose down -v

# View logs
docker compose logs
docker compose logs -f webapp        # Follow one service

# Execute command in running service
docker compose exec webapp sh
docker compose exec postgres psql -U admin myapp

# Scale a service
docker compose up -d --scale worker=3

# List running services
docker compose ps

# Pull latest images
docker compose pull
```

### Full Working Example: Node.js + PostgreSQL + Redis

```yaml
# docker-compose.yml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://admin:secret@db:5432/myapp
      REDIS_URL: redis://cache:6379
    volumes:
      - ./src:/app/src
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

```bash
docker compose up -d
# api starts after db is healthy and cache is running
```

---

## 7. LibreChat Docker Setup (Worked Example)

[LibreChat](https://github.com/danny-avila/LibreChat) is an open-source AI chat interface supporting multiple providers (OpenAI, Anthropic, Google, local models). Docker is the recommended deployment method.

### Step 1: Clone and Configure

```bash
git clone https://github.com/danny-avila/LibreChat.git
cd LibreChat

# Copy the example environment file
cp .env.example .env
```

### Step 2: Edit .env

```bash
# Open .env and configure API keys
nano .env

# Key settings:
#   OPENAI_API_KEY=sk-...
#   ANTHROPIC_API_KEY=sk-ant-...
#   GOOGLE_KEY=...
#   CREDS_KEY=<random 32-char string>
#   CREDS_IV=<random 16-char string>
#   JWT_SECRET=<random string>
```

### Step 3: Start with Docker Compose

```bash
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### Step 4: Access the UI

Open `http://localhost:3080` in your browser. Create an account and start chatting.

### Step 5: Customize Model Providers

Edit `librechat.yaml` to configure endpoints, model lists, and custom presets. See the [LibreChat docs](https://www.librechat.ai/docs/configuration/librechat_yaml) for the full configuration reference.

```bash
# Restart after config changes
docker compose restart
```

---

## 8. Common Patterns

### Running Databases

```bash
# PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=myapp \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine

# MongoDB
docker run -d --name mongo \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -v mongodata:/data/db \
  -p 27017:27017 \
  mongo:7

# Redis
docker run -d --name redis \
  -v redisdata:/data \
  -p 6379:6379 \
  redis:7-alpine --appendonly yes
```

### Reverse Proxy with Nginx

```yaml
# docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - certs:/etc/nginx/certs:ro
    depends_on:
      - webapp

  webapp:
    build: .
    expose:
      - "3000"     # Internal only, not published to host
```

```nginx
# nginx.conf
upstream webapp {
    server webapp:3000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://webapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Development Environment

```yaml
# docker-compose.dev.yml — mount source code, enable hot reload
services:
  app:
    build:
      context: .
      target: development            # Multi-stage: use dev stage
    volumes:
      - .:/app                        # Live code sync
      - /app/node_modules             # Exclude node_modules from bind mount
    ports:
      - "3000:3000"
      - "9229:9229"                   # Debugger port
    environment:
      NODE_ENV: development
    command: npm run dev
```

```bash
docker compose -f docker-compose.dev.yml up --build
```

---

## 9. Docker Registry

### Docker Hub

The default public registry. Images are pulled from here when no registry is specified.

```bash
# Login
docker login

# Push
docker tag myapp:latest username/myapp:v1.0
docker push username/myapp:v1.0

# Pull
docker pull username/myapp:v1.0
```

### GitHub Container Registry (ghcr.io)

```bash
# Login with a personal access token (PAT)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag and push
docker tag myapp:latest ghcr.io/username/myapp:v1.0
docker push ghcr.io/username/myapp:v1.0

# Pull (public images don't need login)
docker pull ghcr.io/username/myapp:v1.0
```

### Self-Hosted Registry

```bash
# Run a local registry
docker run -d -p 5000:5000 --name registry \
  -v regdata:/var/lib/registry \
  registry:2

# Push to it
docker tag myapp:latest localhost:5000/myapp:v1.0
docker push localhost:5000/myapp:v1.0

# List images in the registry
curl http://localhost:5000/v2/_catalog
```

---

## 10. Comparison Table

| Feature | Docker | Podman | LXC/LXD |
|---------|--------|--------|----------|
| **Type** | Application containers | Application containers | System containers |
| **Daemon** | Yes (`dockerd`) | Daemonless | Yes (`lxd`) |
| **Rootless** | Supported | Default | Supported |
| **CLI Compatibility** | — | `alias docker=podman` | Different CLI |
| **Compose** | `docker compose` | `podman-compose` / `podman compose` | — |
| **Kubernetes** | Via Docker Desktop | Native pod support | — |
| **Systemd in Container** | Difficult | Native support | Native (full init) |
| **OCI Compliant** | Yes | Yes | No (own format) |
| **Image Format** | OCI / Docker | OCI / Docker | Own images |
| **Init System** | Not typically | Not typically | Full init (systemd, etc.) |
| **Use Case** | App packaging, microservices | Same as Docker, rootless-first | Lightweight VMs, multi-tenant |
| **Platform** | Linux, Windows, macOS | Linux, macOS (via machine) | Linux |
| **Ecosystem** | Largest (Hub, Compose, Swarm) | Growing (compatible with Docker) | Smaller, Canonical-backed |
| **License** | Apache 2.0 | Apache 2.0 | Apache 2.0 / GPL |

**When to use which:**
- **Docker** — industry standard, best ecosystem, most documentation
- **Podman** — drop-in Docker replacement when daemonless/rootless is required
- **LXC/LXD** — when you need persistent system containers that behave like lightweight VMs

---

## See Also

- [Virtualization](../fundamentals/virtualization.md) — VMs, QEMU/KVM, VirtualBox, Hyper-V
- [Operating Systems](../fundamentals/operating-systems.md) — OS theory, chroot, namespaces
- [Tunneling Tools](../networking/tunneling-tools.md) — Expose Docker services with ngrok, Cloudflared
- [Remote Access](../networking/remote-access.md) — Access Docker hosts remotely
- [AI Chat Interfaces](../ai/chat-interfaces.md) — LibreChat, Open WebUI (commonly Docker-deployed)
- [APIs & Resources](../reference/apis-and-resources.md) — API keys for LibreChat configuration
