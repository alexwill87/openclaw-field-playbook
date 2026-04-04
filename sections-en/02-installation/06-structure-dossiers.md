---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.6 -- Folder Structure

## Context

Before installing services, create a consistent folder hierarchy. This prevents the "files everywhere" effect that makes maintenance impossible. This convention is used throughout the playbook.

## Step 1: Create the Folder Structure

```bash
$ mkdir -p ~/docker/vault
$ mkdir -p ~/docker/postgres
$ mkdir -p ~/scripts
$ mkdir -p ~/backups/postgres
$ mkdir -p ~/backups/vault
$ mkdir -p ~/logs
```

## Resulting Folder Structure

```
~/
├── docker/
│   ├── vault/              # docker-compose.yml + Vault config
│   │   ├── docker-compose.yml
│   │   ├── config/
│   │   └── data/
│   └── postgres/           # docker-compose.yml + PostgreSQL data
│       ├── docker-compose.yml
│       └── data/
├── scripts/                # Custom scripts (health check, deploy, backup)
│   ├── health-check.sh
│   ├── deploy.sh
│   └── backup-postgres.sh
├── backups/                # Local backups
│   ├── postgres/           # SQL dumps
│   └── vault/              # Vault snapshots
├── logs/                   # Application logs (outside journalctl)
└── .openclaw/              # Created automatically by OpenClaw (section 11)
```

## Conventions

| Rule | Explanation |
|-------|-------------|
| `~/docker/<service>/` | Each Docker service gets its own subfolder |
| `docker-compose.yml` at the subfolder root | Run `docker compose up -d` from this folder |
| `~/scripts/` for custom scripts | All utility scripts go here, with `chmod +x` |
| `~/backups/` for local backups | Backup crons write here |
| No files at the root of `~` | Keep your home directory clean |

## Step 2: Make Scripts Executable

The folder is empty for now, but get into the habit:

```bash
$ chmod +x ~/scripts/*.sh 2>/dev/null || true
```

## Common Mistakes

- **Putting all docker-compose.yml files in the same place**: Each service gets its own folder. Otherwise volumes will mix.
- **Creating folders as root**: Create everything as `deploy` (your user). Otherwise Docker will hit permission issues.
- **Forgetting the backups folder**: Backups are configured in the following sections. The folder must exist.

## Verification

```bash
$ ls -la ~/docker/
$ ls -la ~/scripts/
$ ls -la ~/backups/
```

Expected results: the folders exist and belong to your user (not root).

## Estimated Time

5 minutes.
