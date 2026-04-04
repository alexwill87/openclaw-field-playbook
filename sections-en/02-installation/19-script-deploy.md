---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.19 -- Deployment Script

## Context

The `deploy.sh` script automates the complete deployment: code pull, dependency installation, build, and service restart. It must be **idempotent**: executable multiple times in succession with no side effects. Whether the system is up to date or not, the final result is the same.

## The Complete Script

Create `~/scripts/deploy.sh`:

```bash
#!/bin/bash
set -euo pipefail

# === Configuration ===
PROJECT_DIR="$HOME/oa-system"
LOG_FILE="$HOME/logs/deploy.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# === Functions ===
log() {
  echo "[${TIMESTAMP}] $1" | tee -a "$LOG_FILE"
}

notify() {
  if [ -f "$HOME/scripts/notify-telegram.sh" ]; then
    "$HOME/scripts/notify-telegram.sh" "$1" 2>/dev/null || true
  fi
}

fail() {
  log "FAILURE: $1"
  notify "[OA Deploy] FAILURE: $1"
  exit 1
}

# === Pre-checks ===
log "=== Deployment started ==="

# Verify that the directory exists
[ -d "$PROJECT_DIR" ] || fail "Directory $PROJECT_DIR not found"

# Verify that Docker is running
docker info > /dev/null 2>&1 || fail "Docker is not running"

# Verify that Vault is unsealed
docker exec vault vault status 2>&1 | grep -q "Sealed.*false" || fail "Vault is sealed"

cd "$PROJECT_DIR"

# === Step 1: Git pull ===
log "Git pull..."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
  log "WARNING: current branch = $BRANCH (not main)"
fi

git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL" = "$REMOTE" ]; then
  log "Already up to date (commit: ${LOCAL:0:8}). Nothing to deploy."
  exit 0
fi

git pull origin "$BRANCH" || fail "git pull failed"
NEW_COMMIT=$(git rev-parse --short HEAD)
log "New commit: $NEW_COMMIT"

# === Step 2: Dependency installation ===
log "Installing npm dependencies..."
if [ -f "package.json" ]; then
  npm ci --production 2>&1 | tail -1 | tee -a "$LOG_FILE"
else
  log "No package.json, step skipped"
fi

# === Step 3: Build ===
log "Building..."
if [ -f "package.json" ] && grep -q '"build"' package.json; then
  npm run build 2>&1 | tail -5 | tee -a "$LOG_FILE"
else
  log "No build script, step skipped"
fi

# === Step 4: Docker Compose update (if necessary) ===
log "Checking Docker containers..."
for service_dir in docker/vault docker/postgres; do
  if [ -f "$HOME/$service_dir/docker-compose.yml" ]; then
    cd "$HOME/$service_dir"
    docker compose pull 2>/dev/null || true
    docker compose up -d 2>&1 | tee -a "$LOG_FILE"
    cd "$PROJECT_DIR"
  fi
done

# === Step 5: Gateway restart ===
# The playbook recommends systemd (section 2.15).
# If you are using PM2, replace this section with: pm2 reload all --update-env
log "Restarting gateway (systemd)..."
if sudo systemctl restart openclaw-gateway 2>&1; then
  log "Gateway restarted"
else
  log "WARNING: gateway restart failed"
  notify "[OA Deploy] FAILURE gateway restart on $NEW_COMMIT"
  exit 1
fi

# === Step 6: Health check ===
log "Post-deployment health check..."
sleep 5  # Allow services time to start

if "$HOME/scripts/health-check.sh" >> "$LOG_FILE" 2>&1; then
  log "Health check: OK"
  log "=== Deployment completed successfully ($NEW_COMMIT) ==="
  notify "[OA Deploy] Deployment successful: $NEW_COMMIT on $BRANCH"
else
  log "WARNING: health check has failures"
  notify "[OA Deploy] WARNING: $NEW_COMMIT deployed but health check failed"
  exit 1
fi
```

## Installation

```bash
$ chmod +x ~/scripts/deploy.sh
```

## Usage

```bash
$ ~/scripts/deploy.sh
```

The script:
1. Verifies prerequisites (Docker, Vault)
2. Pulls code from Git
3. Stops if nothing has changed (idempotent)
4. Installs dependencies (`npm ci`)
5. Builds the project if a build script exists
6. Updates Docker containers if necessary
7. Reloads PM2 processes
8. Restarts the gateway
9. Runs the health check
10. Notifies via Telegram

## Script Properties

| Property | Detail |
|----------|--------|
| Idempotent | If the code is already up to date, the script exits cleanly |
| Fail fast | `set -euo pipefail` stops the script at the first error |
| Logging | Each step is logged in `~/logs/deploy.log` |
| Notification | Telegram is notified on success or failure |
| Adaptable | Optional steps (build, PM2) are skipped if not applicable |

## Automatic Deployment via Git Hook (optional)

To trigger deployment automatically on every push:

Create `.git/hooks/post-receive` on the VPS (if you are using a bare repository):

```bash
#!/bin/bash
~/scripts/deploy.sh
```

Or use GitHub Actions to trigger the script via SSH.

## Common Errors

- **"npm ci" fails**: The `package-lock.json` file is missing or out of sync. Run `npm install` then commit the lock file.
- **Gateway won't restart**: Check the logs: `journalctl -u openclaw-gateway -n 20`. Often caused by an expired Vault token.
- **Script fails on first run**: The Git repository may not exist yet in `~/oa-system`. Create it first (section 17).
- **Permissions**: The script must be run by the `deploy` user, not root. Internal sudo commands (gateway restart) work thanks to the user's sudo rights.

## Verification

```bash
$ ~/scripts/deploy.sh
$ cat ~/logs/deploy.log | tail -20
```

Expected results:
- Script executes without error (or exits with "Already up to date")
- Log shows completed steps
- Telegram notification received (if configured)

## Estimated Time

15 minutes (creation and first test).
