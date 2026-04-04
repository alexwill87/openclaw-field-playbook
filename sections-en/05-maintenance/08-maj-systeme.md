---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.8 -- System Updates

## Context

System updates are basic hygiene. Not doing them = accumulation of security vulnerabilities. Doing them carelessly = breaking production. The balance: regular, tested, documented.

## Ubuntu

### Security updates (weekly)

```bash
# See available updates
sudo apt update && apt list --upgradable

# Apply only security updates
sudo apt upgrade -y --only-upgrade

# Or for security only
sudo unattended-upgrade --dry-run  # see what would be done
sudo unattended-upgrade             # apply
```

### Major update (annual)

Ubuntu 24.04 LTS -> 26.04 LTS: do NOT do this on a Friday night.

1. Full Hetzner snapshot first.
2. Read the release notes.
3. Test on a test VPS if possible.
4. `do-release-upgrade` in screen/tmux (to survive an SSH disconnect).
5. Test all services after.

### Configure automatic updates

```bash
# Install
sudo apt install unattended-upgrades

# Configure: /etc/apt/apt.conf.d/50unattended-upgrades
# Keep only security updates
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};

# Enable email notifications (optional)
Unattended-Upgrade::Mail "your@email.com";

# Automatic reboot if needed (at 3 AM)
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "03:00";
```

## Docker

### Docker images

```bash
# See images and their dates
docker images --format "{{.Repository}}:{{.Tag}} {{.CreatedSince}}"

# Pull latest versions
docker compose pull

# Rebuild and restart
docker compose up -d --build

# Clean up old images
docker image prune -a --filter "until=720h"  # > 30 days
```

### Docker Engine

```bash
# Current version
docker version

# Update
sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io

# Verify after update
docker version
docker ps  # are containers still running?
```

Warning: a Docker Engine update can restart the daemon and thus stop all containers. Plan a maintenance window.

## Node.js

### With nvm (recommended)

```bash
# Current version
node -v

# List available versions
nvm ls-remote --lts

# Install a new version
nvm install 22  # for example

# Use the new version
nvm use 22

# Test your applications
cd /opt/cockpit && npm test

# If all is OK, set as default
nvm alias default 22
```

### With apt (if no nvm)

```bash
# Update via NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install nodejs
```

## Vault

```bash
# Current version
vault version

# Update
# Download the new version from releases.hashicorp.com
wget https://releases.hashicorp.com/vault/X.Y.Z/vault_X.Y.Z_linux_amd64.zip
unzip vault_X.Y.Z_linux_amd64.zip
sudo mv vault /usr/local/bin/vault

# Restart
sudo systemctl restart vault

# Verify
vault status
vault kv list secret/  # are secrets accessible?
```

Warning: ALWAYS read Vault's upgrade notes before updating. Some versions have breaking changes to the storage backend.

## When NOT to update

Do not update when:

1. **You are in critical production.** A client is waiting for a delivery in 2 hours. This is not the time.

2. **It's a Friday.** The Friday night outage gets fixed Monday morning. Update only Monday through Thursday.

3. **You don't have a recent backup.** No snapshot, no today's pg_dump = no update.

4. **The version is fresh.** Version X.0.0 just came out. Wait for X.0.1 or X.0.2. Let others break it in.

5. **Multiple updates at once.** Do not update Ubuntu, Docker, and Node.js on the same day. One change at a time.

6. **You don't understand the changelog.** If the breaking changes aren't clear, research before.

## Common mistakes

**Never update.** The server runs a 2-year-old version with known vulnerabilities. Security is debt that accumulates.

**Update everything at once.** If it breaks, you don't know what.

**No snapshot first.** The update breaks something. No rollback possible. 3 hours of debugging instead of 5 minutes of restore.

**Update without testing.** `apt upgrade -y` and move on. You discover the problem 2 days later.

## Steps

1. Plan a maintenance window (Tuesday or Wednesday, not Friday).
2. Take a Hetzner snapshot and pg_dump.
3. Update one component at a time.
4. Test each service after the update.
5. Document what was updated and when.

## Verification

- [ ] Ubuntu security updates are automatic (unattended-upgrades).
- [ ] Docker images are up to date (less than 30 days old).
- [ ] A snapshot exists before each major update.
- [ ] Updates are never done on Friday.
- [ ] Each update is followed by a service test.
