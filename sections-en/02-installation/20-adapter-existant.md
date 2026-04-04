---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit, claude-aurel]
lang: en
---

# Adapting the playbook to an existing VPS

> You already have a server with services running. This section helps you diagnose what's already in place and adapt your path through the playbook.

---

## Diagnosing the current state

Copy and run these commands to get a quick inventory:

```bash
# Docker
docker --version

# Docker Compose
docker compose version

# Node.js (and installation method)
node --version
command -v nvm && echo "installe via nvm" || echo "installation globale"

# Tailscale
tailscale status

# PostgreSQL (container or native)
docker ps | grep postgres
psql --version

# Vault
vault status
docker ps | grep vault

# nginx
nginx -v

# Ports already in use by playbook services
ss -ltnp | grep -E ':(3007|5432|8065|8200|18789)'

# Existing OpenClaw systemd services
systemctl --user list-units --all | grep openclaw
sudo systemctl list-units --all | grep openclaw
```

Note the results. They determine which sections you can skip and which you need to adapt.

---

## Correspondence table

For each existing component, here's the action to take:

| Component | Already installed? | Action |
|-----------|-----------------|--------|
| Docker + Compose | Yes | Skip section 2.4. Verify version (>= 24). |
| Node.js (nvm) | Yes | Skip section 2.5. Note if it's nvm or global (affects section 2.15). |
| Node.js (global/apt) | Yes | Skip section 2.5. The systemd wrapper will be different (no nvm.sh). |
| Tailscale | Yes | Skip section 2.3. Note your Tailscale IP. |
| PostgreSQL | Yes | Adapt section 2.8: create a new `oa_system` database without touching the existing one. |
| Vault | Yes | Skip section 2.7 but follow the "Store secrets" step (add OpenClaw secrets). |
| nginx | Yes | The playbook doesn't use nginx by default. If you want to proxy, see the note below. |

---

## Port conflicts

Table of ports used by the playbook and how to respond if they're already in use:

| Port | Service | If already in use |
|------|---------|-------------|
| 5432 | PostgreSQL | Use an alternative port (e.g., 5433) and adapt the commands |
| 8200 | Vault | Change in Vault's docker-compose.yml |
| 8065 | Mattermost | Change in Mattermost's docker-compose.yml |
| 18789 | OpenClaw Gateway | Change in OpenClaw config |
| 3007 | Install Tracker | Change in tracker's docker-compose.yml |

---

## Existing systemd services (CRITICAL)

If you already had an OpenClaw installation on this VPS, verify absolutely:

```bash
# System services
sudo systemctl list-units --all | grep -i openclaw
sudo systemctl list-units --all | grep -i claw

# User services
systemctl --user list-units --all | grep -i openclaw

# If found, disable BEFORE continuing:
sudo systemctl stop openclaw-gateway
sudo systemctl disable openclaw-gateway
systemctl --user stop openclaw-gateway
systemctl --user disable openclaw-gateway
```

> **IMPORTANT**: failing to disable old systemd services before reinstalling is a source of silent bugs. The new service starts, the old one does too, and both fight over the same port. (Reference: issue #30 -- this problem cost Claude-Aurel 45 minutes of debugging.)

---

## Note on nginx

If you already use nginx as a reverse proxy, you can proxy the OpenClaw gateway:

```nginx
server {
    server_name openclaw.votre-domaine.com;
    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Verification

After diagnosing and adapting, resume the playbook at the section corresponding to your first missing component.

**Common errors:**
- Not checking old systemd services
- Port conflicts not detected
- Docker version too old (< 24)

---

[Contribute to this chapter](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)

---
