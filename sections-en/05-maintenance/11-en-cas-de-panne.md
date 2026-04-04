---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.11 -- In case of outage

## Context

An outage happens. The reflex: don't panic, diagnose, fix, prevent. This guide gives you a diagnostic table by symptom for the most common outages.

## Reflex in case of outage

1. **Don't touch everything at once.** One diagnosis at a time.
2. **Note the time.** When it started. To correlate logs.
3. **Check the simplest thing first.** Is the server up? Is the service running? Is disk space full?

## Diagnostic table

### The site/service is not responding

| Diagnostic | Command | Fix |
|---|---|---|
| The container is stopped | `docker ps -a` | `docker compose up -d` |
| The port is not exposed | `ss -tlnp \| grep PORT` | Check docker-compose.yml ports |
| Nginx is not proxying | `nginx -t && systemctl status nginx` | Fix the config, `systemctl restart nginx` |
| The service crashes on startup | `docker logs CONTAINER --tail 50` | Read the error, fix, rebuild |
| DNS does not point | `dig your-domain.com` | Check DNS config |

**Prevention:** automated health check (section 5.1) + monitoring (section 5.10).

### The server is inaccessible via SSH

| Diagnostic | Command | Fix |
|---|---|---|
| The server is down | Hetzner Cloud console | Reboot from console |
| SSH is blocked by firewall | Hetzner console > rescue mode | `ufw allow 22` |
| Disk full (SSH cannot create a session) | Hetzner console | Rescue mode, mount disk, free space |
| Wrong SSH key | From your machine: `ssh -vvv user@ip` | Check authorized_keys |

**Prevention:** never modify ufw/iptables without confirmed SSH rule. Snapshot before network changes.

### The database is not responding

| Diagnostic | Command | Fix |
|---|---|---|
| PostgreSQL is stopped | `systemctl status postgresql` | `systemctl start postgresql` |
| Too many connections | `psql -c "SELECT count(*) FROM pg_stat_activity;"` | Identify ghost connections, increase max_connections |
| Disk full | `df -h /var/lib/postgresql` | Free space (logs, tmp) |
| Corruption | PostgreSQL logs | Restore from last backup (section 5.3) |
| Wrong password (after rotation) | `psql -U oa_admin -d cockpit` | Check secret in Vault, fix |

**Prevention:** PostgreSQL monitoring + daily tested backup.

### The disk is full

| Diagnostic | Command | Fix |
|---|---|---|
| Identify what takes space | `du -sh /* \| sort -rh \| head -10` | See below |
| Docker logs | `du -sh /var/lib/docker/containers/` | Configure rotation (section 5.2) |
| System logs | `journalctl --disk-usage` | `journalctl --vacuum-size=200M` |
| Old backups | `du -sh /var/backups/` | Delete oldest, keep 7 days |
| Unused Docker images | `docker system df` | `docker system prune -a --filter "until=720h"` |
| Temporary files | `du -sh /tmp/` | `rm -rf /tmp/old-*` (with discretion) |

**Prevention:** alert at 80% disk usage in health check. Log rotation configured.

### A container keeps restarting in a loop

| Diagnostic | Command | Fix |
|---|---|---|
| Startup error | `docker logs CONTAINER --tail 100` | Read the error, fix |
| Missing dependency | `docker logs CONTAINER 2>&1 \| grep -i "error\|fatal"` | npm install, pip install, etc. |
| Missing environment variable | `docker inspect CONTAINER \| jq '.[0].Config.Env'` | Add to .env or docker-compose.yml |
| Port already in use | `ss -tlnp \| grep PORT` | Stop the other service or change port |
| OOM Kill | `dmesg \| grep -i oom` | Increase memory or optimize app |

**Prevention:** `restart: unless-stopped` in docker-compose.yml + health check + logs.

### The agent is no longer working

| Diagnostic | Command | Fix |
|---|---|---|
| Invalid/expired API key | Test a direct API call | Renew the key |
| Rate limit reached | Check response headers | Wait or change plan |
| API service down | Check status.anthropic.com (or equivalent) | Wait |
| Broken configuration | Read .claude/ or equivalent | Restore from backup |
| Deprecated model | Read error logs | Change model in config |

**Prevention:** fallback on another configured model (section 5.13). Budget and rate limits monitored.

## After the outage

1. **Document.** What, when, cause, fix, duration.
2. **Prevent.** Add a check to the health check, a rule to the boundary prompt, a workflow to WORKFLOWS.md.
3. **Test the prevention.** Simulate the outage again and verify that monitoring detects it.

### Post-mortem template

```markdown
## Incident — YYYY-MM-DD

**Symptom:** [what was observed]
**Start:** HH:MM — **End:** HH:MM — **Duration:** X min
**Cause:** [root cause]
**Fix:** [what was done]
**Impact:** [who/what was affected]
**Prevention:** [measure added to prevent recurrence]
```

## Common mistakes

**Panicking and touching everything.** You change 3 configs at once. Now you have 4 problems instead of one.

**No recent backup.** Recovery is impossible or too old. See section 5.3.

**Not documenting.** The same outage comes back 3 months later and you forgot the fix.

**Fixing without understanding.** "I rebooted and it works." Until next time. Identify the root cause.

## Checklist

- [ ] You can diagnose the 6 scenarios above.
- [ ] The diagnostic commands are tested and work on your setup.
- [ ] A post-mortem template exists.
- [ ] Past outages are documented.
- [ ] Each outage generated a prevention measure.

---
