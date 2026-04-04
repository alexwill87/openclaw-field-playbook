---
---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 5.10 -- Monitoring and Alerts

## Context

Monitoring answers a simple question: is everything running? And if not, since when and why? Without monitoring, you discover outages when your users write to you. With monitoring, you discover them before they do.

Three levels. Start with the first one. Move up when the need arises.

## Level 1: Simple (cron + Telegram)

This is the health check from section 5.1 on a cron, with Telegram alerts. Zero additional infrastructure.

### What it covers

- Services up/down.
- Disk space.
- PostgreSQL accessible.
- SSL certificates valid.

### What it doesn't cover

- Metric history (no graphs).
- Response time.
- Application metrics (requests/second, errors).
- Monitoring from outside (if the server goes down completely, the cron won't run).

### Setup

See section 5.1. Summary:

```bash
# Cron every 4 hours
0 */4 * * * /opt/scripts/health-check.sh --quiet

# Telegram alert if KO
```

Setup time: 30 minutes.
Cost: 0 EUR.

## Level 2: Intermediate (Uptime Kuma)

Uptime Kuma is a self-hosted monitoring tool. Web interface, history, multiple notifications.

### Installation

```bash
# Via Docker (the recommended method)
docker run -d \
  --name uptime-kuma \
  --restart unless-stopped \
  -p 3001:3001 \
  -v uptime-kuma-data:/app/data \
  louislam/uptime-kuma:1

# Or in docker-compose.yml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - uptime-kuma-data:/app/data

volumes:
  uptime-kuma-data:
```

### Configuration

1. Open `http://your-ip:3001`.
2. Create an admin account.
3. Add monitors:

| Type | URL/Command | Interval |
|---|---|---|
| HTTP | `http://localhost:3000` (cockpit) | 60s |
| HTTP | `http://localhost:8080` (API) | 60s |
| TCP | `localhost:5432` (PostgreSQL) | 120s |
| HTTP Keyword | `https://your-domain.com` + expected keyword | 300s |

4. Configure notifications: Telegram, email, or Slack.

### What it adds

- Uptime history (graphs).
- Average response time.
- Flexible notifications (multi-channel).
- Public status page (optional).
- Monitoring from the same server (limitation: if the server goes down, Uptime Kuma goes down too).

Setup time: 1 hour.
Cost: 0 EUR (self-hosted).

## Level 3: Advanced (Grafana + Prometheus)

For those who need detailed metrics, custom dashboards, and distributed monitoring.

### Stack

```
Prometheus: collects metrics (CPU, RAM, disk, requests).
Node Exporter: exposes system metrics for Prometheus.
Grafana: displays dashboards.
AlertManager: manages alerts.
```

### Installation (Docker Compose)

```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro

  grafana:
    image: grafana/grafana
    ports:
      - "3002:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=changeme

volumes:
  prometheus-data:
  grafana-data:
```

### When it's justified

- You manage 3+ services with SLAs.
- You need to correlate CPU/memory/network with application performance.
- You have a team that consults the dashboards.
- You charge uptime to your clients.

### When it's over-engineering

- You're alone with 2 containers.
- Nobody looks at the dashboards.
- A cron + Telegram is enough for your use case.

Setup time: 4-8 hours.
Cost: 0 EUR (self-hosted) + maintenance time.

## Recommendation

**Start with level 1.** Always. It takes 30 minutes and covers 80% of needs.

Move to level 2 when:
- You want uptime history.
- You have 5+ services to monitor.
- You want a status page.

Move to level 3 when:
- You have SLAs to meet.
- You need fine-grained metrics (p99 latency, throughput).
- You manage multiple servers.

Most solo setups will never need level 3.

## Common Mistakes

**Installing Grafana + Prometheus for 2 containers.** Over-engineering. You spend more time maintaining the monitoring than maintaining the application.

**No external monitoring.** All your monitoring runs on the same server. If the server goes down, the monitoring goes down too. Level 1 solution: a free external service (UptimeRobot, Hetrixtools) for basic pings.

**Too many alerts.** You receive 20 alerts per day. You ignore them all. You end up ignoring the real outage. Adjust thresholds to alert only on real problems.

**No alerts at all.** Monitoring is running, logs are filling up, but nobody is notified. Monitoring without alerts is monitoring without value.

## Steps

1. Install level 1 (section 5.1: health-check.sh + cron + Telegram).
2. Use it for 2 weeks.
3. Evaluate: is it enough?
4. If not, install Uptime Kuma (level 2).
5. Add a free external ping to cover complete server failure.

## Verification

- [ ] Monitoring is active (minimum level 1).
- [ ] Alerts are working (tested with a simulated outage).
- [ ] Number of alerts per day is reasonable (< 3 in normal times).
- [ ] External monitoring pings your server.
- [ ] You know within 5 minutes if a service is down.
