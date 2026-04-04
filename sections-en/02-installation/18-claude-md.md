---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.18 -- CLAUDE.md

## Context

`CLAUDE.md` is the file that every AI agent reads first when working on your repository. It's the contract between you and the agent: conventions, stack, authorized commands, rules. Without this file, the agent improvises. With this file, it follows YOUR rules.

This file goes in the root of your Git repository.

## The complete CLAUDE.md file

Create `CLAUDE.md` at the root of your repository:

```markdown
# CLAUDE.md -- Instructions for AI agents

## Project identity

- Name: OA System
- Description: Infrastructure for autonomous AI agents on VPS
- Maintainers: [your name], OpenClaw agents
- Code language: English
- Documentation language: French
- Repository: private

## Technical stack

| Component | Technology | Version |
|-----------|-------------|---------|
| Runtime | Node.js | 22.x LTS |
| Database | PostgreSQL | 16 (Docker) |
| Secrets | HashiCorp Vault | 1.17 (Docker) |
| Process manager | PM2 | 5.x |
| Containerization | Docker + Docker Compose v2 | 28.x |
| VPN | Tailscale | latest |
| OS | Ubuntu | 24.04 LTS |

## Repository structure

```
.
├── docker/           # Docker Compose files (no data)
├── scripts/          # Utility bash scripts
├── CLAUDE.md         # This file
├── .gitignore        # Files excluded from versioning
└── README.md         # Project documentation
```

## Common commands

```bash
# Deployment
./scripts/deploy.sh

# Health check
./scripts/health-check.sh

# Database backup
./scripts/backup-postgres.sh

# Telegram notification
./scripts/notify-telegram.sh "message"

# Gateway logs
journalctl -u openclaw-gateway -f

# Restart gateway
sudo systemctl restart openclaw-gateway
```

## Code rules

1. No hardcoded secrets in code. Everything goes through Vault.
2. Each script must be idempotent (executable multiple times without side effects).
3. Docker commands use `docker compose` (with space, not hyphen).
4. Paths are absolute in scripts, relative in application code.
5. Logs go in ~/logs/ or journalctl, never in the Git repository.

## Commit rules

- Format: `type: brief description`
- Types: feat, fix, docs, refactor, test, chore
- In English
- Single responsibility per commit

## What an agent MUST NOT do

- Modify files in /etc/ without asking for confirmation
- Delete files without listing what will be deleted
- Execute `rm -rf` on anything
- Touch Vault unseal keys
- Commit .env files or credentials
- Do `git push --force` on main
- Modify this file (CLAUDE.md) without human approval

## What an agent CAN do freely

- Read any file in the repository
- Execute scripts in ~/scripts/
- Read secrets from Vault (read-only)
- Create Git branches
- Make commits on branches (not main directly)
- Check logs
- Run health checks

## Environment variables

Variables are injected via systemd or Vault. Never put them in .bashrc for production.

| Variable | Source | Description |
|----------|--------|-------------|
| VAULT_ADDR | systemd | Vault URL |
| VAULT_TOKEN | systemd | Vault application token |
| NODE_ENV | systemd | production |
```

## Why this file is important

Without CLAUDE.md:
- The agent may attempt to install packages via `sudo apt install` when you use Docker
- The agent may create .env files instead of using Vault
- The agent may use `docker-compose` (hyphen) instead of `docker compose` (space)
- The agent may commit to main without a branch

With CLAUDE.md:
- The agent knows your exact stack
- The agent respects your conventions
- The agent knows what it can and cannot do
- Fewer manual corrections

## Updates

This file evolves with the project. Every time you add a service, a script, or a rule, update CLAUDE.md. It's the source of truth for agents.

## Common mistakes

- **Not creating the file**: The agent works, but makes arbitrary choices. Time lost in corrections far exceeds the time to write it.
- **File too long**: Keep it concise. Agents have limited context. The essentials are enough.
- **Obsolete file**: A CLAUDE.md that describes a stack that has changed is worse than no file at all. Maintain it.
- **Putting secrets in CLAUDE.md**: This file is in Git. No tokens, no passwords.

## Verification

```bash
$ cat CLAUDE.md | head -5
$ git log --oneline CLAUDE.md
```

Expected results:
- The file exists and is readable
- It is versioned in Git

## Estimated time

10 minutes.
