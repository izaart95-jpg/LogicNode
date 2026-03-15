# Kubernetes — Container Orchestration

Kubernetes (K8s) is the industry-standard open-source system for automating deployment, scaling, and management of containerized applications. Where Docker packages and runs individual containers, Kubernetes orchestrates fleets of them across clusters of machines.

> **See Also:** [Docker Essentials](docker-essentials.md) — Before learning Kubernetes, understanding Docker images, containers, and Compose is strongly recommended.

---

## Table of Contents
1. [What is Kubernetes?](#1-what-is-kubernetes)
2. [Core Concepts](#2-core-concepts)
3. [Architecture](#3-architecture)
4. [Installation](#4-installation)
5. [kubectl — The CLI](#5-kubectl--the-cli)
6. [Workloads](#6-workloads)
7. [Networking](#7-networking)
8. [Storage](#8-storage)
9. [Configuration & Secrets](#9-configuration--secrets)
10. [Helm — Package Manager](#10-helm--package-manager)
11. [Managed Kubernetes (Cloud)](#11-managed-kubernetes-cloud)
12. [Comparison Table](#12-comparison-table)

---

## 1. What is Kubernetes?

Kubernetes solves the operational problems that arise when running containers at scale:

- **Self-healing** — automatically restarts failed containers, replaces and reschedules them
- **Horizontal scaling** — scale workloads up or down based on load, manually or automatically
- **Rolling deployments** — update apps with zero downtime, roll back bad deploys instantly
- **Service discovery** — containers find each other by name, no hardcoded IPs
- **Load balancing** — distribute traffic across healthy container replicas automatically
- **Secret management** — store and inject passwords, tokens, and keys securely

```
Without Kubernetes (manual Docker):
  "Container died on server 3. SSH in. Restart it. Oh, server 3 is down. Find another server..."

With Kubernetes:
  Container dies → K8s detects it → schedules replacement on healthy node → done in seconds
```

**Docker vs Kubernetes:**

| Concern | Docker | Kubernetes |
|---------|--------|------------|
| Run a container | ✅ | Via Pod |
| Multi-container app | Compose | Deployment |
| Auto-restart on crash | Compose restart policy | ReplicaSet |
| Scale to 100 replicas | Manual | `kubectl scale --replicas=100` |
| Cross-machine scheduling | ❌ | ✅ |
| Rolling updates | ❌ | ✅ |
| Health checks + self-healing | ❌ | ✅ |

---

## 2. Core Concepts

### Pod
The smallest deployable unit in Kubernetes. A Pod wraps one or more containers that share network and storage. In practice, most Pods contain a single container.

```yaml
# Simplest possible Pod
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: app
      image: nginx:alpine
      ports:
        - containerPort: 80
```

### Deployment
Manages a ReplicaSet of identical Pods. Handles rolling updates and rollbacks. This is what you use for stateless apps.

### Service
A stable network endpoint for a set of Pods. Since Pod IPs change constantly, Services provide a fixed address/DNS name and load-balance across Pod replicas.

```
Service (stable IP: 10.96.1.5)
    ↓ load balances
Pod-a (10.244.1.2)
Pod-b (10.244.1.3)
Pod-c (10.244.2.1)
```

### Namespace
Virtual clusters within a physical cluster. Used to isolate environments (dev, staging, prod) or teams within the same cluster.

### ConfigMap & Secret
Store configuration data and sensitive values (passwords, tokens) separately from container images, injecting them as environment variables or files at runtime.

### Ingress
An HTTP/HTTPS router that exposes Services to the outside world. Maps hostnames and URL paths to backend Services.

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Kubernetes Cluster                                              │
│                                                                  │
│  ┌───────────────────────┐   ┌───────────────────────────────┐  │
│  │  Control Plane (Master)│   │  Worker Nodes                 │  │
│  │                       │   │                               │  │
│  │  kube-apiserver       │   │  ┌──────────────────────┐    │  │
│  │  (all requests go here)│   │  │ Node 1               │    │  │
│  │                       │   │  │  kubelet (agent)      │    │  │
│  │  etcd                 │   │  │  kube-proxy           │    │  │
│  │  (cluster state store) │   │  │  container runtime    │    │  │
│  │                       │   │  │  [Pod] [Pod] [Pod]    │    │  │
│  │  kube-scheduler       │   │  └──────────────────────┘    │  │
│  │  (assigns Pods→nodes) │   │                               │  │
│  │                       │   │  ┌──────────────────────┐    │  │
│  │  controller-manager   │   │  │ Node 2               │    │  │
│  │  (watches & reconciles)│   │  │  [Pod] [Pod]          │    │  │
│  └───────────────────────┘   │  └──────────────────────┘    │  │
│                               └───────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

kubectl (your CLI) ──────────────────▶ kube-apiserver
```

**Control Plane components:**

| Component | Role |
|-----------|------|
| **kube-apiserver** | Front door to the cluster — all kubectl commands hit this |
| **etcd** | Distributed key-value store holding all cluster state |
| **kube-scheduler** | Decides which node a new Pod should run on |
| **controller-manager** | Runs control loops (e.g., ensures desired replica count matches actual) |

**Worker Node components:**

| Component | Role |
|-----------|------|
| **kubelet** | Agent that runs on each node, manages Pods on that node |
| **kube-proxy** | Maintains network rules for Service routing |
| **Container runtime** | Actually runs containers (containerd, CRI-O) |

---

## 4. Installation

### Option 1: minikube (Local Development)

Runs a single-node Kubernetes cluster in a VM or container on your laptop. Best for learning and development.

```bash
# Install minikube (Linux)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# macOS
brew install minikube

# Start cluster (uses Docker driver by default)
minikube start

# Start with specific resources
minikube start --cpus=4 --memory=8g

# Check status
minikube status

# Open Kubernetes dashboard in browser
minikube dashboard

# Stop cluster
minikube stop

# Delete cluster
minikube delete
```

### Option 2: kind (Kubernetes in Docker)

Runs Kubernetes inside Docker containers. Fast to start, ideal for CI/CD and testing.

```bash
# Install kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Create cluster
kind create cluster

# Create cluster with config (multi-node)
cat > kind-config.yaml << 'EOF'
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
EOF
kind create cluster --config kind-config.yaml

# Delete cluster
kind delete cluster
```

### Option 3: k3s (Lightweight Kubernetes)

Minimal Kubernetes for edge, IoT, and resource-constrained environments. Single binary, ~70MB.

```bash
# Install k3s (single-node — control plane + worker)
curl -sfL https://get.k3s.io | sh -

# Check
sudo k3s kubectl get nodes

# Uninstall
/usr/local/bin/k3s-uninstall.sh
```

### Option 4: kubeadm (Production Multi-Node)

The official tool for bootstrapping production Kubernetes clusters.

```bash
# Install on all nodes (Ubuntu/Debian)
sudo apt update && sudo apt install -y apt-transport-https ca-certificates curl

curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key \
  | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' \
  | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update && sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# On the CONTROL PLANE node only:
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Set up kubeconfig (run as regular user after init)
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install a Pod network add-on (Flannel)
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

# On WORKER nodes — use the join command printed by kubeadm init:
sudo kubeadm join <control-plane-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

---

## 5. kubectl — The CLI

`kubectl` is the command-line tool for interacting with Kubernetes clusters. Install it separately from the cluster itself.

```bash
# Install kubectl (Linux)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl

# macOS
brew install kubectl

# Verify
kubectl version --client
```

### Essential Commands

```bash
# ── Cluster Info ──
kubectl cluster-info
kubectl get nodes
kubectl get nodes -o wide           # More detail (IPs, OS, kernel)
kubectl describe node <node-name>

# ── Namespaces ──
kubectl get namespaces
kubectl create namespace staging
kubectl config set-context --current --namespace=staging   # Switch default namespace

# ── Pods ──
kubectl get pods                        # Current namespace
kubectl get pods -A                     # All namespaces
kubectl get pods -o wide               # With node and IP info
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs <pod-name> -f              # Follow logs (tail -f)
kubectl logs <pod-name> -c <container>  # Specific container in multi-container Pod
kubectl exec -it <pod-name> -- bash     # Shell into a running Pod
kubectl exec -it <pod-name> -- sh       # If bash not available
kubectl delete pod <pod-name>

# ── Deployments ──
kubectl get deployments
kubectl describe deployment <name>
kubectl scale deployment <name> --replicas=5
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>          # Roll back one version
kubectl rollout undo deployment/<name> --to-revision=2

# ── Services ──
kubectl get services
kubectl describe service <name>
kubectl port-forward service/<name> 8080:80     # Access service locally

# ── Apply / Delete manifests ──
kubectl apply -f deployment.yaml
kubectl apply -f ./k8s/                         # Apply all YAML in directory
kubectl delete -f deployment.yaml
kubectl delete deployment <name>

# ── Get YAML of existing resources ──
kubectl get deployment <name> -o yaml
kubectl get pod <name> -o json

# ── Quick resource creation ──
kubectl create deployment nginx --image=nginx:alpine --replicas=3
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# ── Debugging ──
kubectl get events --sort-by=.lastTimestamp
kubectl top nodes                               # CPU/memory (requires metrics-server)
kubectl top pods
kubectl run debug --image=busybox --rm -it -- sh   # Temporary debug Pod
```

### kubeconfig and Contexts

`kubectl` uses a `~/.kube/config` file to store cluster credentials and contexts.

```bash
# View all contexts (clusters)
kubectl config get-contexts

# Switch context (cluster)
kubectl config use-context my-cluster

# View current context
kubectl config current-context

# Merge multiple kubeconfig files
KUBECONFIG=~/.kube/config:~/.kube/other-cluster kubectl config view --flatten > ~/.kube/merged
```

---

## 6. Workloads

### Deployment

Use for stateless applications (web servers, APIs). Manages a ReplicaSet with rolling update support.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1      # At most 1 Pod down during update
      maxSurge: 1            # At most 1 extra Pod during update
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
        - name: webapp
          image: myapp:v2.1
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"      # 0.1 CPU core guaranteed
              memory: "128Mi"
            limits:
              cpu: "500m"      # 0.5 CPU core maximum
              memory: "256Mi"
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
          env:
            - name: NODE_ENV
              value: "production"
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
```

### StatefulSet

Use for stateful applications (databases, message queues) that need stable network identities and persistent storage.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: "postgres"
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:16-alpine
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:              # Automatically creates PVC per replica
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

### DaemonSet

Runs exactly one Pod per node. Used for cluster-wide agents like log collectors, monitoring agents, or network plugins.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector
spec:
  selector:
    matchLabels:
      app: log-collector
  template:
    metadata:
      labels:
        app: log-collector
    spec:
      containers:
        - name: fluentd
          image: fluent/fluentd:v1.16
          volumeMounts:
            - name: varlog
              mountPath: /var/log
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
```

### Job & CronJob

```yaml
# Job — runs to completion once
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: myapp:v2.1
          command: ["python", "manage.py", "migrate"]
      restartPolicy: OnFailure

---
# CronJob — runs on a schedule
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-backup
spec:
  schedule: "0 2 * * *"       # Every night at 2 AM (cron syntax)
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: mybackup:latest
          restartPolicy: OnFailure
```

---

## 7. Networking

### Services

```yaml
# ClusterIP (default) — internal only
apiVersion: v1
kind: Service
metadata:
  name: webapp-svc
spec:
  selector:
    app: webapp
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP

---
# NodePort — exposes on every node's IP at a static port (30000-32767)
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080

---
# LoadBalancer — provisions a cloud load balancer (GKE, EKS, AKS)
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8080
```

### Ingress

An Ingress resource routes external HTTP/HTTPS traffic to internal Services based on hostname and path. Requires an Ingress Controller (nginx-ingress, Traefik, HAProxy) to be installed in the cluster.

```bash
# Install nginx-ingress controller (via Helm)
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp-svc
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-svc
                port:
                  number: 3000
  tls:
    - hosts:
        - app.example.com
      secretName: tls-secret    # Cert-manager populates this automatically
```

---

## 8. Storage

### PersistentVolume (PV) and PersistentVolumeClaim (PVC)

```yaml
# PersistentVolumeClaim — request storage
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce          # RWO = one node, RWX = many nodes
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard # Use default storage class
```

```yaml
# Use in a Deployment
spec:
  containers:
    - name: app
      image: myapp:latest
      volumeMounts:
        - name: data
          mountPath: /app/data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data-pvc
```

```bash
# Check storage classes available
kubectl get storageclasses

# Check PVC status
kubectl get pvc
kubectl describe pvc data-pvc
```

---

## 9. Configuration & Secrets

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_PORT: "8080"
  LOG_LEVEL: "info"
  config.yaml: |
    database:
      host: postgres
      port: 5432
```

```yaml
# Inject ConfigMap as env vars
envFrom:
  - configMapRef:
      name: app-config

# Mount ConfigMap as files
volumeMounts:
  - name: config
    mountPath: /etc/app
volumes:
  - name: config
    configMap:
      name: app-config
```

### Secret

```bash
# Create secret from command line (base64-encoded automatically)
kubectl create secret generic db-secret \
  --from-literal=password=supersecret \
  --from-literal=username=admin

# Create from file
kubectl create secret generic tls-secret \
  --from-file=tls.crt=cert.pem \
  --from-file=tls.key=key.pem

# View secret (values are base64)
kubectl get secret db-secret -o yaml
```

```yaml
# Inject secret as environment variable
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-secret
        key: password
```

> **Note:** Kubernetes Secrets are base64-encoded, not encrypted by default. For production, use external secret managers like HashiCorp Vault, AWS Secrets Manager, or enable etcd encryption at rest.

---

## 10. Helm — Package Manager

Helm is the package manager for Kubernetes. A Helm **chart** is a collection of YAML templates that can be parameterized and installed as a single unit.

```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Add a chart repository
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search for charts
helm search repo bitnami/postgres
helm search hub nginx

# Install a chart
helm install my-postgres bitnami/postgresql \
  --set auth.postgresPassword=secret \
  --namespace database --create-namespace

# Install with custom values file
helm install my-postgres bitnami/postgresql \
  -f my-values.yaml \
  --namespace database

# List installed releases
helm list -A

# Upgrade a release
helm upgrade my-postgres bitnami/postgresql -f updated-values.yaml

# Roll back a release
helm rollback my-postgres 1   # Revision number

# Uninstall
helm uninstall my-postgres --namespace database

# Render templates without installing (dry run)
helm template my-postgres bitnami/postgresql -f values.yaml
```

### Creating Your Own Chart

```bash
# Scaffold a new chart
helm create myapp

# Chart structure:
# myapp/
# ├── Chart.yaml          # Chart metadata
# ├── values.yaml         # Default values
# ├── templates/
# │   ├── deployment.yaml
# │   ├── service.yaml
# │   ├── ingress.yaml
# │   └── _helpers.tpl    # Template helpers
# └── charts/             # Sub-charts (dependencies)

# Package and push to registry
helm package myapp/
helm push myapp-0.1.0.tgz oci://registry.example.com/charts
```

---

## 11. Managed Kubernetes (Cloud)

All major cloud providers offer managed Kubernetes — they handle the control plane, upgrades, and infrastructure so you only manage workloads.

| Provider | Service | CLI Command |
|----------|---------|-------------|
| **Google Cloud** | GKE (Google Kubernetes Engine) | `gcloud container clusters create` |
| **Amazon AWS** | EKS (Elastic Kubernetes Service) | `eksctl create cluster` |
| **Microsoft Azure** | AKS (Azure Kubernetes Service) | `az aks create` |
| **DigitalOcean** | DOKS | `doctl kubernetes cluster create` |
| **Linode** | LKE | `linode-cli lke cluster-create` |

```bash
# GKE — create cluster and get credentials
gcloud container clusters create my-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type e2-standard-2

gcloud container clusters get-credentials my-cluster --zone us-central1-a
kubectl get nodes   # Now using GKE cluster

# EKS — create cluster (eksctl)
eksctl create cluster \
  --name my-cluster \
  --region us-east-1 \
  --nodegroup-name workers \
  --node-type t3.medium \
  --nodes 3

aws eks update-kubeconfig --name my-cluster --region us-east-1
kubectl get nodes

# AKS
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --node-vm-size Standard_B2s \
  --enable-addons monitoring \
  --generate-ssh-keys

az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
kubectl get nodes
```

---

## 12. Comparison Table

### Local Kubernetes Options

| Tool | Use Case | Speed | Multi-Node | Production-Like |
|------|----------|-------|-----------|-----------------|
| **minikube** | Learning, development | Moderate | Limited | Moderate |
| **kind** | CI/CD, testing | Fast | ✅ | Good |
| **k3s** | Edge, IoT, low resources | Fast | ✅ | Very Good |
| **kubeadm** | Production bootstrap | Slow (setup) | ✅ | Full |
| **Docker Desktop K8s** | Desktop dev (Mac/Win) | Easy | Single | Limited |

### Kubernetes vs Docker Compose

| Feature | Docker Compose | Kubernetes |
|---------|---------------|------------|
| **Multi-container apps** | ✅ | ✅ |
| **Cross-machine orchestration** | ❌ | ✅ |
| **Auto-healing** | Limited | ✅ |
| **Rolling updates** | ❌ | ✅ |
| **Horizontal auto-scaling** | ❌ | ✅ |
| **Production grade** | Small scale | Enterprise scale |
| **Learning curve** | Low | High |

### Quick Decision Guide

| Scenario | Recommendation |
|----------|---------------|
| Local dev + testing | **minikube** or **kind** |
| CI/CD pipelines | **kind** |
| Edge / Raspberry Pi | **k3s** |
| Self-hosted production | **kubeadm** + Flannel/Calico |
| Cloud production | **GKE / EKS / AKS** (managed) |
| Package existing apps for K8s | **Helm** |

---

## See Also

- [Docker Essentials](docker-essentials.md) — Containers, images, Compose — prerequisite knowledge for Kubernetes
- [Cloud Platforms](cloud-platforms.md) — GCP, Colab, cloud compute environments
- [Hosting Platforms](hosting-platforms.md) — Vercel, Netlify, Firebase for simpler deployments
