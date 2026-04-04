---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.17 -- Initialize the Git Repo

## Context

Code, scripts, and configuration (excluding secrets) must be version-controlled in Git. This section creates the repository, configures the GitHub remote, and sets up a solid .gitignore to prevent committing secrets or unnecessary files.

## Step 1: Initialize the Repository

```bash
$ cd ~/
$ git init oa-system
$ cd oa-system
```

Or if you're working directly in your home directory:

```bash
$ cd ~/
$ git init
```

## Step 2: Configure Git

```bash
$ git config user.name "Your Name"
$ git config user.email "your-email@example.com"
$ git config init.defaultBranch main
```

## Step 3: Create the .gitignore

Create `.gitignore` at the root of the repository:

```gitignore
# === Secrets and credentials ===
.env
.env.*
*.key
*.pem
credentials.json
vault-keys.txt
unseal-keys.txt

# === Docker data ===
docker/vault/data/
docker/postgres/data/

# === Backups ===
backups/

# === Logs ===
logs/
*.log

# === Node.js ===
node_modules/
npm-debug.log*
.npm

# === OpenClaw ===
.openclaw/credentials.json
.openclaw/logs/
.openclaw/workspace/sessions/

# === OS ===
.DS_Store
Thumbs.db
*~
*.swp
*.swo

# === IDE ===
.vscode/settings.json
.idea/
*.sublime-workspace
```

## Step 4: Copy Files to Version Control

Files that MUST be in Git:

```bash
# Scripts
$ cp ~/scripts/*.sh ./scripts/

# Docker compose (without the data)
$ mkdir -p docker/vault docker/postgres
$ cp ~/docker/vault/docker-compose.yml ./docker/vault/
$ cp ~/docker/vault/config/vault.hcl ./docker/vault/config/
$ cp ~/docker/postgres/docker-compose.yml ./docker/postgres/

# Health check
$ cp ~/scripts/health-check.sh ./scripts/
```

Files that MUST NOT be in Git:
- Anything in `backups/`
- The `data/` folders of containers
- Any `.env` files or files containing secrets
- Vault unseal keys

## Step 5: Create the GitHub Remote

Create a repository on GitHub (private is recommended), then:

```bash
$ git remote add origin git@github.com:YOUR_USER/oa-system.git
```

If you're using HTTPS instead of SSH:

```bash
$ git remote add origin https://github.com/YOUR_USER/oa-system.git
```

## Step 6: First Commit

```bash
$ git add .
$ git status
```

Verify that NO secrets appear in the list of files to commit. If a sensitive file appears, add it to .gitignore and run `git reset HEAD <file>`.

```bash
$ git commit -m "feat: initialization of OA system - infrastructure and scripts"
$ git push -u origin main
```

## Step 7: Verify on GitHub

Go to your GitHub repository and verify:
- Files are present
- No secrets are visible
- The .gitignore works (no `data/`, no `backups/`)

## Common Errors

- **Committing secrets**: If this happens, the secret is compromised even if you remove it from the next commit (Git history preserves it). Change the secret immediately. Use `git-filter-repo` to purge the history if necessary.
- **"Permission denied (publickey)"**: Your SSH key is not configured on GitHub. Add it in GitHub > Settings > SSH Keys.
- **Private vs public repository**: For a production system, use a PRIVATE repository. The docker-compose.yml files can reveal your architecture.
- **Forgetting .gitignore before the first commit**: If `node_modules/` or `data/` has been committed, run `git rm -r --cached node_modules/` then re-commit.

## Verification

```bash
$ git status
$ git log --oneline
$ git remote -v
```

Expected results:
- Working tree clean (nothing to commit)
- At least one commit visible
- Remote points to your GitHub repository

## Estimated Time

10 minutes.
