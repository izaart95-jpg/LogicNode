# Cloud Platforms — GCP, Colab, Kaggle & Google Services

Cloud platforms provide on-demand computing, storage, and managed services that scale from free-tier experimentation to enterprise production workloads. This guide covers Google Cloud Console, notebook environments for machine learning, and Google API integrations for building automated workflows.

---

## Table of Contents
1. [Cloud Computing Overview](#1-cloud-computing-overview)
2. [Google Cloud Console](#2-google-cloud-console)
3. [Google Colab](#3-google-colab)
4. [Kaggle Notebooks](#4-kaggle-notebooks)
5. [Google Antigravity](#5-google-antigravity)
6. [Gmail API](#6-gmail-api)
7. [Comparison Table: Notebook Platforms](#7-comparison-table-notebook-platforms)

---

## 1. Cloud Computing Overview

### Service Models

| Model | What You Manage | What Provider Manages | Examples |
|-------|----------------|----------------------|----------|
| **IaaS** (Infrastructure) | OS, runtime, app, data | Servers, storage, networking | GCP Compute Engine, AWS EC2, Azure VMs |
| **PaaS** (Platform) | App and data only | OS, runtime, servers, scaling | Google Cloud Run, Heroku, App Engine |
| **SaaS** (Software) | Nothing (just use it) | Everything | Gmail, Google Docs, Slack |

```
┌────────────────────────────────────────────────────────┐
│                    YOU MANAGE ▲                         │
│                                                        │
│  IaaS          PaaS          SaaS                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ App      │  │ App      │  │          │              │
│  │ Runtime  │  │          │  │          │              │
│  │ OS       │  │          │  │  Fully   │              │
│  │----------│  │----------│  │  Managed │              │
│  │ Server   │  │ Server   │  │          │              │
│  │ Storage  │  │ Storage  │  │          │              │
│  │ Network  │  │ Network  │  │          │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│                                                        │
│                    PROVIDER MANAGES ▼                   │
└────────────────────────────────────────────────────────┘
```

### Major Cloud Providers

| Provider | Strengths | Free Tier |
|----------|-----------|-----------|
| **Google Cloud (GCP)** | ML/AI, BigQuery, Kubernetes (GKE) | $300 credit + always-free products |
| **Amazon Web Services (AWS)** | Largest ecosystem, broadest services | 12-month free tier + always-free |
| **Microsoft Azure** | Enterprise integration, .NET, hybrid cloud | $200 credit + always-free products |

---

## 2. Google Cloud Console

- **Website:** https://console.cloud.google.com
- **Free tier:** $300 credit for 90 days + always-free products

### 2.1 Key Services

| Service | Type | Description |
|---------|------|-------------|
| **Compute Engine** | IaaS | Virtual machines (VMs) with custom configurations |
| **Cloud Run** | PaaS | Serverless containers — deploy any Docker image |
| **Cloud Functions** | FaaS | Event-driven serverless functions (Node, Python, Go, Java) |
| **Cloud Storage** | Object | Scalable object storage (like AWS S3) |
| **BigQuery** | Data | Serverless data warehouse for analytics (SQL) |
| **Cloud SQL** | Database | Managed MySQL, PostgreSQL, SQL Server |
| **Firestore** | Database | NoSQL document database with real-time sync |
| **GKE** | Containers | Managed Kubernetes clusters |
| **Artifact Registry** | CI/CD | Store Docker images, npm packages, Python packages |
| **Cloud Build** | CI/CD | Automated build, test, and deploy pipelines |

### 2.2 gcloud CLI

```bash
# Install (Linux/macOS)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Or via apt (Debian/Ubuntu)
sudo apt install google-cloud-cli

# Authentication
gcloud auth login
gcloud auth application-default login

# Set project
gcloud config set project MY_PROJECT_ID

# List projects
gcloud projects list
```

### 2.3 Compute Engine (VMs)

```bash
# Create a VM
gcloud compute instances create my-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2404-lts-amd64 \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB

# SSH into VM
gcloud compute ssh my-vm --zone=us-central1-a

# List instances
gcloud compute instances list

# Stop / start / delete
gcloud compute instances stop my-vm --zone=us-central1-a
gcloud compute instances start my-vm --zone=us-central1-a
gcloud compute instances delete my-vm --zone=us-central1-a
```

### 2.4 Cloud Run (Serverless Containers)

```bash
# Deploy from source (auto-builds with Buildpacks)
gcloud run deploy my-service --source . --region=us-central1

# Deploy from Docker image
gcloud run deploy my-service \
  --image=gcr.io/MY_PROJECT/my-app:latest \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --cpu=1

# List services
gcloud run services list

# View logs
gcloud run services logs read my-service --region=us-central1
```

### 2.5 Cloud Functions

```bash
# Deploy an HTTP function (Python)
gcloud functions deploy myFunc \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point=main \
  --region=us-central1

# Deploy event-driven function (Cloud Storage trigger)
gcloud functions deploy processUpload \
  --runtime nodejs20 \
  --trigger-resource my-bucket \
  --trigger-event google.storage.object.finalize
```

```python
# main.py — Cloud Function
import functions_framework

@functions_framework.http
def main(request):
    name = request.args.get('name', 'World')
    return f'Hello, {name}!'
```

### 2.6 Cloud Storage

```bash
# Create bucket
gsutil mb gs://my-bucket-name

# Upload file
gsutil cp ./file.txt gs://my-bucket-name/

# Download file
gsutil cp gs://my-bucket-name/file.txt ./

# List contents
gsutil ls gs://my-bucket-name/

# Sync directory
gsutil rsync -r ./local-dir gs://my-bucket-name/remote-dir

# Make file public
gsutil acl ch -u AllUsers:R gs://my-bucket-name/file.txt
```

### 2.7 IAM and Service Accounts

```bash
# Create service account
gcloud iam service-accounts create my-sa \
  --display-name="My Service Account"

# Grant roles
gcloud projects add-iam-policy-binding MY_PROJECT \
  --member="serviceAccount:my-sa@MY_PROJECT.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# Create key file
gcloud iam service-accounts keys create key.json \
  --iam-account=my-sa@MY_PROJECT.iam.gserviceaccount.com

# Use in application
export GOOGLE_APPLICATION_CREDENTIALS="key.json"
```

### 2.8 Free Tier & Always-Free Products

| Product | Always-Free Limit |
|---------|-------------------|
| **Compute Engine** | 1 e2-micro VM (us-central1), 30 GB disk, 1 GB egress |
| **Cloud Storage** | 5 GB (US regions), 5,000 Class A ops, 50,000 Class B ops |
| **Cloud Functions** | 2M invocations/mo, 400K GB-seconds, 200K GHz-seconds |
| **Cloud Run** | 2M requests/mo, 360K vCPU-seconds, 180K GiB-seconds |
| **BigQuery** | 1 TB queries/mo, 10 GB storage |
| **Firestore** | 1 GiB storage, 50K reads, 20K writes, 20K deletes per day |
| **Artifact Registry** | 500 MB storage |

### 2.9 Billing Alerts

```bash
# Set up via CLI
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Monthly Budget" \
  --budget-amount=50 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100
```

---

## 3. Google Colab

- **Website:** https://colab.research.google.com
- **Type:** Free cloud-hosted Jupyter notebook environment
- **GPU:** T4 (free), A100 (Pro/Pro+)
- **Best for:** ML experimentation, data analysis, Python prototyping

### 3.1 Key Features

- **Free GPU/TPU access** — NVIDIA T4 GPU on free tier
- **Google Drive integration** — mount Drive as a filesystem
- **Pre-installed libraries** — NumPy, Pandas, TensorFlow, PyTorch, scikit-learn
- **Collaborative editing** — share and edit notebooks like Google Docs
- **pip installs** — install any Python package on the fly
- **GitHub integration** — open notebooks directly from GitHub

### 3.2 Basic Usage

```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Access files
import pandas as pd
df = pd.read_csv('/content/drive/MyDrive/data/dataset.csv')

# Check GPU availability
!nvidia-smi

# Check GPU in PyTorch
import torch
print(f"GPU available: {torch.cuda.is_available()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")
```

### 3.3 Installing Packages

```python
# Install packages (persist only during session)
!pip install transformers datasets accelerate

# Install specific version
!pip install torch==2.1.0

# Install from GitHub
!pip install git+https://github.com/user/repo.git
```

### 3.4 File Upload/Download

```python
from google.colab import files

# Upload files from local machine
uploaded = files.upload()

# Download files to local machine
files.download('output.csv')
```

### 3.5 Colab Pro / Pro+ Plans

| Feature | Free | Pro ($11.99/mo) | Pro+ ($49.99/mo) |
|---------|------|-----------------|-------------------|
| **GPU** | T4 (limited) | T4, V100, A100 | A100 (priority) |
| **TPU** | Limited | Standard | Priority |
| **RAM** | ~12.7 GB | Up to 32 GB | Up to 52 GB |
| **Session length** | ~12 hours | ~24 hours | ~24 hours |
| **Idle timeout** | 90 minutes | Longer | Background execution |
| **Storage** | 100 GB disk | 100 GB disk | 500 GB disk |

### 3.6 Tips and Workarounds

```python
# Prevent idle disconnect (run in browser console)
# document.querySelector("colab-toolbar-button#connect").click()

# Save checkpoints to Drive
import shutil
shutil.copy('model.pt', '/content/drive/MyDrive/checkpoints/model.pt')

# Use secrets (avoid hardcoding API keys)
from google.colab import userdata
api_key = userdata.get('OPENAI_API_KEY')

# System info
!cat /proc/cpuinfo | head -20
!free -h
!df -h
```

### 3.7 Limitations

- Sessions disconnect after idle timeout (90 min free, longer on Pro)
- Maximum session length ~12 hours (free) or ~24 hours (Pro)
- GPU availability not guaranteed on free tier
- No persistent environment — packages reinstall each session
- Limited terminal access

---

## 4. Kaggle Notebooks

- **Website:** https://www.kaggle.com
- **Type:** Free notebook environment for data science and ML
- **GPU:** NVIDIA P100 or T4, 30 hours/week
- **TPU:** Google TPU v3-8, 20 hours/week
- **Best for:** ML competitions, dataset exploration, learning

### 4.1 Key Features

- **Free GPU/TPU** — generous weekly quotas
- **Built-in datasets** — 50,000+ public datasets
- **Competitions** — ML competitions with prizes
- **Community** — notebooks, discussions, and leaderboards
- **Version control** — automatic versioning of notebook runs
- **Kaggle API** — programmatic access to datasets and competitions

### 4.2 GPU/TPU Usage

```python
# Check GPU
!nvidia-smi

# Enable GPU: Settings → Accelerator → GPU T4 x2 or P100
# Enable TPU: Settings → Accelerator → TPU v3-8
```

| Accelerator | Weekly Quota | Performance |
|-------------|-------------|-------------|
| **GPU P100** | 30 hours/week | 16 GB VRAM, good for training |
| **GPU T4 x2** | 30 hours/week | 2x 16 GB VRAM, inference-optimized |
| **TPU v3-8** | 20 hours/week | 128 GB HBM, great for large models |

### 4.3 Kaggle API

```bash
# Install
pip install kaggle

# Configure (place kaggle.json from account settings)
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Download competition data
kaggle competitions download -c titanic

# Download dataset
kaggle datasets download -d username/dataset-name

# Submit predictions
kaggle competitions submit -c titanic -f submission.csv -m "My submission"

# List competitions
kaggle competitions list

# Search datasets
kaggle datasets list -s "image classification"
```

### 4.4 Kaggle Notebooks vs Scripts

| Feature | Notebooks | Scripts |
|---------|-----------|---------|
| **Interface** | Interactive cells (Jupyter) | Single .py file |
| **Visualization** | Inline plots and tables | Output files only |
| **GPU/TPU** | Yes | Yes |
| **Collaboration** | Fork and modify | Fork and modify |
| **Output** | HTML render + files | Files only |
| **Best for** | Exploration, sharing | Production pipelines |

### 4.5 Kaggle vs Colab

| Feature | Kaggle Notebooks | Google Colab |
|---------|-----------------|--------------|
| **Free GPU** | P100/T4 x2 (30 hrs/week) | T4 (limited, variable) |
| **Free TPU** | TPU v3-8 (20 hrs/week) | Limited |
| **Datasets** | 50,000+ built-in | Mount from Drive |
| **Competitions** | Yes (prizes, leaderboards) | No |
| **Session limit** | 12 hours | 12 hours (free) |
| **Idle timeout** | 60 minutes | 90 minutes |
| **Persistent storage** | Kaggle Datasets | Google Drive |
| **Collaboration** | Forking model | Real-time (Google Docs) |
| **Internet access** | Optional (toggle) | Always on |
| **Package install** | Pre-session or !pip | !pip in cells |
| **Custom environments** | Docker images | Limited |
| **Best for** | Competitions, datasets | General ML, prototyping |

---

## 5. Google Antigravity

- **Website:** https://antigravity.google
- **By:** Google
- **Type:** AI-powered creative coding environment

### 5.1 Overview

Google Antigravity is an experimental platform from Google for AI-assisted creative coding. It provides an interactive environment where users can explore code generation and creative programming with AI guidance.

### 5.2 Key Features

- **AI-powered development** — use natural language to describe what you want to build
- **Interactive coding** — real-time feedback and visualization
- **Creative experiments** — designed for exploratory and creative coding projects
- **Browser-based** — no installation required

### 5.3 Use Cases

- Generative art and creative coding experiments
- Learning programming through AI-guided interaction
- Rapid prototyping of visual and interactive projects
- Exploring AI-assisted development workflows

---

## 6. Gmail API

- **Docs:** https://developers.google.com/workspace/gmail/api/guides
- **Type:** RESTful API for programmatic Gmail access
- **Auth:** OAuth 2.0
- **Rate limit:** 250 quota units/second per user

### 6.1 Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project (or select existing)
3. Enable the Gmail API: **APIs & Services > Enable APIs > Gmail API**
4. Create OAuth 2.0 credentials: **APIs & Services > Credentials > Create Credentials > OAuth client ID**
5. Download `credentials.json`

### 6.2 OAuth 2.0 Scopes

| Scope | Access Level |
|-------|-------------|
| `gmail.readonly` | Read messages and labels |
| `gmail.send` | Send email only |
| `gmail.modify` | Read, send, delete, modify messages and labels |
| `gmail.compose` | Create drafts and send |
| `gmail.labels` | Manage labels only |
| `gmail.metadata` | Read message metadata (headers, no body) |
| `mail.google.com` | Full access (all operations) |

### 6.3 Python Quickstart

```bash
pip install google-auth-oauthlib google-api-python-client
```

```python
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

service = get_service()
```

### 6.4 List Messages

```python
# List recent messages
results = service.users().messages().list(
    userId='me',
    maxResults=10,
    q='is:unread'  # Gmail search query syntax
).execute()

messages = results.get('messages', [])
for msg in messages:
    detail = service.users().messages().get(
        userId='me', id=msg['id']
    ).execute()
    headers = {h['name']: h['value'] for h in detail['payload']['headers']}
    print(f"From: {headers.get('From')}")
    print(f"Subject: {headers.get('Subject')}")
    print("---")
```

### 6.5 Send Email

```python
def send_email(to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent = service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()
    print(f"Message sent. ID: {sent['id']}")

send_email('recipient@example.com', 'Test Subject', 'Hello from the Gmail API!')
```

### 6.6 Search and Filter

```python
# Gmail search operators work in the API
queries = [
    'from:user@example.com',           # From specific sender
    'subject:invoice',                  # Subject contains
    'has:attachment filename:pdf',      # PDFs with attachments
    'after:2025/01/01 before:2025/06/01',  # Date range
    'is:unread label:inbox',            # Unread inbox messages
    'larger:5M',                        # Larger than 5MB
]

for q in queries:
    results = service.users().messages().list(userId='me', q=q, maxResults=5).execute()
    count = results.get('resultSizeEstimate', 0)
    print(f"Query '{q}': ~{count} results")
```

### 6.7 Batch Requests

```python
from googleapiclient.http import BatchHttpRequest

def callback(request_id, response, exception):
    if exception:
        print(f"Error for {request_id}: {exception}")
    else:
        headers = {h['name']: h['value'] for h in response['payload']['headers']}
        print(f"{request_id}: {headers.get('Subject', 'No subject')}")

batch = service.new_batch_http_request(callback=callback)

# Add multiple requests to batch
message_ids = ['msg_id_1', 'msg_id_2', 'msg_id_3']
for mid in message_ids:
    batch.add(service.users().messages().get(userId='me', id=mid))

batch.execute()
```

### 6.8 Rate Limits

| Quota | Limit |
|-------|-------|
| **Per user rate limit** | 250 quota units/second |
| **Daily usage limit** | 1,000,000,000 quota units/day |
| **messages.send** | 100 emails/day (trial), no hard limit (verified) |
| **messages.get** | 5 quota units per call |
| **messages.list** | 5 quota units per call |
| **messages.send** | 100 quota units per call |

---

## 7. Comparison Table: Notebook Platforms

| Feature | Google Colab | Kaggle Notebooks | Jupyter (Local) |
|---------|-------------|-----------------|-----------------|
| **Free GPU** | T4 (limited) | P100/T4 x2 (30 hrs/wk) | Your own hardware |
| **Free TPU** | Limited | TPU v3-8 (20 hrs/wk) | N/A |
| **Storage** | Google Drive (15 GB free) | 100 GB per notebook | Local disk |
| **RAM** | ~12.7 GB (free) | 16-30 GB | System RAM |
| **Datasets** | Upload or Drive | 50,000+ built-in | Local files |
| **Competitions** | No | Yes (prizes) | No |
| **Session limit** | ~12 hrs (free) | 12 hrs | Unlimited |
| **Collaboration** | Real-time (Docs-like) | Fork model | JupyterHub |
| **Internet** | Always on | Toggle on/off | Always on |
| **Custom packages** | !pip per session | !pip or Docker | Full control |
| **Version control** | Manual (Drive) | Automatic | Git |
| **Offline use** | No | No | Yes |
| **Best for** | Quick ML prototyping | Competitions, datasets | Production, privacy |

### Quick Decision Guide

| Scenario | Recommended Platform |
|----------|---------------------|
| ML competition | **Kaggle** (datasets + leaderboards) |
| Quick experiment with GPU | **Colab** (instant setup) |
| Large model training | **Colab Pro+** (A100) or **Kaggle** (T4 x2) |
| Production ML pipeline | **GCP** (Vertex AI, Cloud Run) |
| Data analysis with large datasets | **Kaggle** (built-in datasets) |
| Collaborative notebook | **Colab** (Google Docs-style sharing) |
| Privacy-sensitive data | **Jupyter Local** (data stays on your machine) |

---

## See Also

- [Hosting Platforms](hosting-platforms.md) — Vercel, Netlify, Firebase Studio for web deployment
- [AI Platforms & APIs](../ai/platforms-and-apis.md) — LLM APIs, AI services, model hosting
- [APIs & Resources](../reference/apis-and-resources.md) — Public APIs, developer tools, free resources
- [Docker Essentials](../devtools/docker-essentials.md) — Containerized deployments on cloud platforms
