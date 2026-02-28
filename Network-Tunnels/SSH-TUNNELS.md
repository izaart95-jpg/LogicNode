# SSH Tunneling & Reverse Proxy Guide

## 1. What is SSH Tunneling?
SSH tunneling (SSH port forwarding) creates an encrypted tunnel between a local source and a remote destination. It is the gold standard for securely accessing internal services or exposing local ports to the internet without complex VPNs.

---

## 2. Remote Port Forwarding (Reverse Proxy)
This allows you to expose a local service (like a web server on port 8080) to the public internet using third-party relay servers.

### 🌐 Pinggy.io
Pinggy is a powerful tool for instant URLs. Use port **443** to bypass restrictive firewalls.

**Standard TCP Tunnel:**
```bash
ssh -p 443 -R0:localhost:8080 tcp@free.pinggy.io
```
**TLS Tunnel**
```bash 
ssh -p 443 -R0:localhost:8000 tls@free.pinggy.io
```

# Regional Servers (Lowest Latency):

##  Asia: ap.free.pinggy.io
```bash
ssh -p 443 -R0:localhost:8080 tcp@ap.free.pinggy.io
```
## Europe eu.free.pinggy.io
```bash
ssh -p 443 -R0:localhost:8080 tcp@eu.free.pinggy.io
```
## United States: us.free.pinggy.io
```bash
ssh -p 443 -R0:localhost:8080 tcp@us.free.pinggy.io
```

### Serveo.net
A simple, no-install reverse proxy.
```bash
ssh -R 80:localhost:3000 serveo.net
```

### Localhost.run
Gemini said
Here is the entire guide converted into a single, clean Markdown file contained within one code block.

Markdown
# SSH Tunneling & Reverse Proxy Guide

## 1. What is SSH Tunneling?
SSH tunneling (SSH port forwarding) creates an encrypted tunnel between a local source and a remote destination. It is the gold standard for securely accessing internal services or exposing local ports to the internet without complex VPNs.

---

## 2. Remote Port Forwarding (Reverse Proxy)
This allows you to expose a local service (like a web server on port 8080) to the public internet using third-party relay servers.

### 🌐 Pinggy.io
Pinggy is a powerful tool for instant URLs. Use port **443** to bypass restrictive firewalls.

**Standard TCP Tunnel:**
```bash
ssh -p 443 -R0:localhost:8080 tcp@free.pinggy.io
```
## TLS Tunnel (with HTTPS termination):
```bash
ssh -p 443 -R0:localhost:8000 tls@ap.free.pinggy.io
```
## Regional Servers (Lowest Latency):

Asia: ap.free.pinggy.io

Europe: eu.free.pinggy.io

United States: us.free.pinggy.io


### 🌐 Serveo.net
A simple, no-install reverse proxy.

```bash
ssh -R 80:localhost:3000 serveo.net
```
### 🌐 Localhost.run
Excellent for quick web hooks and testing.
```bash
# Basic usage
ssh -R 80:localhost:8080 nokey@localhost.run

# With TLS termination (Custom subdomain if available)
ssh -R 80:localhost:3000 yourapp.localhost.run
```
# Automation & "Silent" Connection
When scripts or automated tasks run SSH, you don't want the "Are you sure you want to continue connecting?" prompt or the connection to drop.
## Skip Host Verification (Auto-accept Prompt)
```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -R 80:localhost:8080 user@host.net
```
# Keep-Alive (Prevent Timeouts)
To ensure the tunnel doesn't close during inactivity:
```bash
ssh -o ServerAliveInterval=30 -R 80:localhost:8080 user@host.net
```
# The "All-in-One" Robust Command
Use this for the most stable, automated connection:
```bash
ssh -p 443 \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -o ServerAliveInterval=30 \
  -R0:localhost:8000 \
  tcp@free.pinggy.io
  ```

### Summary of Flags  

| Flag | Description |
| :--- | :--- |
| **-p** | Specifies the remote port (e.g., 443 for Pinggy) |
| **-R** | Remote forwarding (Expose local to world). |
| **-L** | Local forwarding (Bring remote to local). |
| **-o StrictHostKeyChecking=no** | Disables the "Trust this host?" prompt. |
| **-o UserKnownHostsFile=/dev/null** | Prevents saving the host key to your machine. |
| **-o ServerAliveInterval=30** | Sends a "heartbeat" every 30s to keep the tunnel alive. |