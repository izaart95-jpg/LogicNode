# Version Control Platforms — Bitbucket, GitHub & GitLab

A reference for Git hosting platforms — features, CLI usage, REST APIs, CI/CD pipelines, and self-hosting options.

---

## Table of Contents
1. [Platform Comparison](#1-platform-comparison)
2. [Bitbucket](#2-bitbucket)
3. [GitHub](#3-github)
4. [GitLab](#4-gitlab)
5. [Git Essentials](#5-git-essentials)
6. [CI/CD Comparison](#6-cicd-comparison)

---

## 1. Platform Comparison

| Feature | Bitbucket | GitHub | GitLab |
|---------|-----------|--------|--------|
| **Owner** | Atlassian | Microsoft | GitLab Inc. |
| **Free private repos** | ✅ Unlimited | ✅ Unlimited | ✅ Unlimited |
| **Free tier CI/CD** | 50 min/month | 2,000 min/month | 400 min/month |
| **Self-hosted** | Bitbucket Server / Data Center (paid) | GitHub Enterprise (paid) | ✅ GitLab CE (free) |
| **Built-in CI/CD** | Bitbucket Pipelines | GitHub Actions | GitLab CI/CD |
| **Package registry** | ✅ | ✅ | ✅ |
| **Container registry** | ✅ | ✅ | ✅ |
| **Jira integration** | ✅ Native (Atlassian) | Plugin | Plugin |
| **Issue tracking** | Jira (native) | GitHub Issues | GitLab Issues |
| **Wiki** | ✅ | ✅ | ✅ |
| **Code review** | Pull Requests | Pull Requests | Merge Requests |
| **Best for** | Atlassian shops, Jira users | Open source, community | DevOps teams, self-hosting |

---

## 2. Bitbucket

- **Website:** https://bitbucket.org
- **Developer:** Atlassian
- **Git hosting:** Cloud (bitbucket.org) + self-hosted (Bitbucket Data Center)
- **Free tier:** Unlimited private repos, up to 5 users for free on Cloud

### Overview

Bitbucket is Atlassian's Git hosting platform — tightly integrated with Jira (issue tracking), Confluence (documentation), and Bamboo (CI/CD). The preferred choice for teams already using the Atlassian ecosystem. Supports Git and Mercurial (Mercurial support ended 2020, Git only now).

### Setup

```bash
# Clone a Bitbucket repo
git clone https://username@bitbucket.org/workspace/repo.git

# Or via SSH (recommended)
# 1. Add SSH key: Bitbucket → Personal Settings → SSH keys → Add key
git clone git@bitbucket.org:workspace/repo.git

# Set up credential helper (HTTPS)
git config --global credential.helper store
# First push will prompt for username + app password (not account password)
# Create app passwords: Bitbucket → Personal Settings → App passwords
```

### App Passwords

Bitbucket does not allow your account password for Git operations — you must create an App Password:

```
Bitbucket → Avatar → Personal Settings → App passwords → Create app password
Select scopes: Repositories (Read, Write), Pull requests (Read, Write)
Use: username + app_password as Git credentials
```

### Bitbucket Pipelines (CI/CD)

`bitbucket-pipelines.yml` in repo root:

```yaml
# Basic pipeline
image: node:20

pipelines:
  default:
    - step:
        name: Build and Test
        caches:
          - node
        script:
          - npm install
          - npm test

  branches:
    main:
      - step:
          name: Build
          script:
            - npm install
            - npm run build
      - step:
          name: Deploy
          deployment: production
          script:
            - pipe: atlassian/aws-s3-deploy:1.1.0
              variables:
                AWS_ACCESS_KEY_ID: $AWS_ACCESS_KEY_ID
                AWS_SECRET_ACCESS_KEY: $AWS_SECRET_ACCESS_KEY
                S3_BUCKET: my-bucket
                LOCAL_PATH: dist/

  pull-requests:
    '**':
      - step:
          name: PR Checks
          script:
            - npm install
            - npm test
            - npm run lint
```

### Bitbucket REST API v2

```bash
BASE="https://api.bitbucket.org/2.0"
AUTH="username:app_password"

# List repos in a workspace
curl -u "$AUTH" "$BASE/repositories/my-workspace"

# Get repo info
curl -u "$AUTH" "$BASE/repositories/workspace/repo-slug"

# List pull requests
curl -u "$AUTH" "$BASE/repositories/workspace/repo/pullrequests?state=OPEN"

# Create a pull request
curl -u "$AUTH" -X POST "$BASE/repositories/workspace/repo/pullrequests" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My PR",
    "source": {"branch": {"name": "feature-branch"}},
    "destination": {"branch": {"name": "main"}},
    "description": "PR description"
  }'

# Get pipeline runs
curl -u "$AUTH" "$BASE/repositories/workspace/repo/pipelines/?sort=-created_on"

# Trigger a pipeline
curl -u "$AUTH" -X POST "$BASE/repositories/workspace/repo/pipelines/" \
  -H "Content-Type: application/json" \
  -d '{"target": {"ref_type": "branch", "type": "pipeline_ref_target", "ref_name": "main"}}'
```

```python
# Python — using atlassian-python-api
pip install atlassian-python-api

from atlassian import Bitbucket

bb = Bitbucket(
    url="https://api.bitbucket.org",
    username="your_username",
    password="your_app_password"
)

# List repos
for repo in bb.get_repositories("workspace"):
    print(repo["slug"])

# Get pull requests
prs = bb.get_pullrequests("workspace", "repo-slug", state="OPEN")
for pr in prs:
    print(pr["id"], pr["title"])
```

### Branch Permissions

```
Repository Settings → Branch restrictions:
  - Require pull requests (no direct push to main)
  - Require minimum approvals (e.g., 2 reviewers)
  - Require passing builds before merge
  - Restrict who can push/merge
```

### Jira Integration

```
Link a Jira issue to a commit/PR by including the issue key in the message:
  git commit -m "PROJ-123 Fix authentication bug"
  # Branch named: feature/PROJ-123-fix-auth

Bitbucket automatically:
  - Links commits/PRs to the Jira issue
  - Shows deployment status in Jira
  - Allows transitioning Jira issues from PR merge
```

---

## 3. GitHub

- **Website:** https://github.com
- **Developer:** Microsoft
- **CLI:** `gh` — https://cli.github.com

### Key Features

- Largest developer community (100M+ developers)
- GitHub Actions (CI/CD) — 2,000 free minutes/month
- GitHub Pages — free static site hosting
- Packages — npm, Docker, Maven, NuGet registry
- Copilot — AI code completion
- Codespaces — cloud dev environments
- Security — Dependabot, code scanning, secret scanning

### GitHub CLI (`gh`)

```bash
# Install
brew install gh                    # macOS
winget install GitHub.cli          # Windows
sudo apt install gh                # Ubuntu

gh auth login

# Repo operations
gh repo create my-repo --public
gh repo clone owner/repo
gh repo fork owner/repo

# Pull requests
gh pr create --title "Fix bug" --body "Description" --base main
gh pr list
gh pr view 42
gh pr merge 42 --squash
gh pr checkout 42

# Issues
gh issue create --title "Bug report"
gh issue list --label bug
gh issue close 42

# Actions
gh workflow list
gh workflow run deploy.yml
gh run list
gh run view 12345

# Releases
gh release create v1.0.0 --notes "Initial release"
gh release upload v1.0.0 ./dist/*.tar.gz
```

### GitHub Actions

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

### GitHub REST API

```bash
# With gh CLI (authenticated)
gh api repos/owner/repo
gh api repos/owner/repo/pulls --method POST \
  --field title="PR title" \
  --field head="feature-branch" \
  --field base="main"

# Direct API (with token)
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/issues

# Create issue
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/issues \
  -d '{"title": "Bug", "body": "Description", "labels": ["bug"]}'
```

---

## 4. GitLab

- **Website:** https://gitlab.com
- **Self-hosted:** GitLab CE (Community Edition) — free
- **CLI:** `glab`

### Key Advantages

- **Best self-hosting:** GitLab CE is the most complete free self-hosted option
- **Built-in DevOps:** Issues → CI/CD → Container registry → Kubernetes → Monitoring all in one
- **Auto DevOps:** Detects your app type and configures CI/CD automatically

### Self-Hosting

```bash
# Docker Compose
version: '3.6'
services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    hostname: gitlab.example.com
    ports:
      - '80:80'
      - '443:443'
      - '22:22'
    volumes:
      - gitlab_config:/etc/gitlab
      - gitlab_logs:/var/log/gitlab
      - gitlab_data:/var/opt/gitlab
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.example.com'
        gitlab_rails['gitlab_shell_ssh_port'] = 22
```

### GitLab CI/CD

`.gitlab-ci.yml`:

```yaml
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20"

test:
  stage: test
  image: node:$NODE_VERSION
  cache:
    paths:
      - node_modules/
  script:
    - npm ci
    - npm test
  coverage: '/Coverage: \d+\.\d+/'

build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

deploy_staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - echo "Deploying to staging"
  only:
    - main
```

### GitLab REST API

```bash
# Personal access token required
TOKEN="your_token"
BASE="https://gitlab.com/api/v4"

# List projects
curl -H "PRIVATE-TOKEN: $TOKEN" "$BASE/projects"

# Create merge request
curl -X POST -H "PRIVATE-TOKEN: $TOKEN" \
  "$BASE/projects/PROJECT_ID/merge_requests" \
  --data "source_branch=feature&target_branch=main&title=My MR"

# Trigger pipeline
curl -X POST -H "PRIVATE-TOKEN: $TOKEN" \
  "$BASE/projects/PROJECT_ID/pipeline" \
  --data "ref=main"
```

---

## 5. Git Essentials

```bash
# --- Setup ---
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main

# --- Basic workflow ---
git init
git clone <url>
git status
git add .
git add -p                      # Interactive staging (review hunks)
git commit -m "message"
git push origin main
git pull

# --- Branching ---
git branch feature-x            # Create branch
git checkout -b feature-x       # Create + switch
git switch -c feature-x         # Modern syntax
git branch -d feature-x         # Delete branch (merged)
git branch -D feature-x         # Force delete
git merge feature-x             # Merge into current branch
git rebase main                 # Rebase current branch onto main

# --- Remote ---
git remote add origin <url>
git remote -v
git fetch origin                # Fetch without merging
git push -u origin feature-x    # Push + set upstream
git push --force-with-lease     # Safe force push

# --- History ---
git log --oneline --graph --all
git log -p                      # Show diffs
git blame file.txt              # Who wrote each line
git diff HEAD~1                 # Diff with previous commit
git show abc1234                # Show specific commit

# --- Undo ---
git restore file.txt            # Discard working dir changes
git restore --staged file.txt   # Unstage
git reset HEAD~1                # Undo last commit (keep changes)
git reset --hard HEAD~1         # Undo + discard changes
git revert abc1234              # Revert commit (safe, makes new commit)
git stash                       # Stash current changes
git stash pop                   # Apply stash

# --- Tags ---
git tag v1.0.0
git tag -a v1.0.0 -m "Release"
git push origin --tags
```

---

## 6. CI/CD Comparison

| Feature | Bitbucket Pipelines | GitHub Actions | GitLab CI/CD |
|---------|-------------------|----------------|-------------|
| **Free minutes/month** | 50 | 2,000 | 400 |
| **Config file** | `bitbucket-pipelines.yml` | `.github/workflows/*.yml` | `.gitlab-ci.yml` |
| **Self-hosted runners** | ✅ | ✅ | ✅ (GitLab Runner) |
| **Matrix builds** | ✅ | ✅ | ✅ |
| **Caching** | ✅ | ✅ | ✅ |
| **Artifacts** | ✅ | ✅ | ✅ |
| **Environments/deployments** | ✅ | ✅ | ✅ |
| **Reusable workflows** | ✅ (pipes) | ✅ (reusable workflows) | ✅ (includes) |
| **Marketplace** | Atlassian Pipes | GitHub Marketplace (20k+ actions) | No marketplace |
| **Best for** | Atlassian ecosystem | Open source, community | Self-hosted DevOps |

---

## See Also

- [Coding Agents](coding-agents.md) — AI coding tools that integrate with Git platforms
- [APIs & Resources](apis-and-resources.md) — REST API patterns, authentication
- [Docker Essentials](docker-essentials.md) — Containerization for CI/CD pipelines
- [Kubernetes](../deployment/kubernetes.md) — Container orchestration (deploy from CI/CD)
