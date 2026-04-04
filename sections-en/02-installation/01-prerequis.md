---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.1 -- Hardware and Software Prerequisites

## Context

Before touching the server, you need to know what you're buying, what accounts you're creating, and how much it costs. This section lists everything that is necessary BEFORE you start the installation.

## Hardware Prerequisites: The VPS

Tested and validated minimum configuration:

| Resource | Minimum | Recommended |
|-----------|---------|------------|
| CPU | 4 vCPU | 6 vCPU |
| RAM | 8 GB | 16 GB |
| Storage | 80 GB SSD | 160 GB NVMe |
| Bandwidth | 20 TB/month | Unlimited |
| Location | Europe (GDPR) | Europe (GDPR) |

Tested providers:

- **Hetzner** (recommended): CPX31 at approximately 15 EUR/month. Excellent value for money. Datacenters in Germany and Finland.
- **OVH**: VPS Essential at approximately 12 EUR/month. Datacenters in France. Lower latency from France.

## Operating System

**Ubuntu 24.04 LTS** -- this is the only version tested in this playbook. The commands are written for Ubuntu/Debian. If you use something else, adapt accordingly.

## Accounts to Create

Create these accounts BEFORE you start the installation:

| Service | URL | Why | Free? |
|---------|-----|-----|-------|
| Hetzner or OVH | hetzner.com / ovh.com | Host the VPS | No |
| Tailscale | tailscale.com | Private mesh VPN | Yes (up to 100 machines) |
| GitHub | github.com | Code repository, CI/CD | Yes |
| OpenRouter | openrouter.ai | Multi-model AI access | Pay-as-you-go credits |
| Telegram | telegram.org | Notifications and commands | Yes |
| HashiCorp Cloud (optional) | cloud.hashicorp.com | Cloud Vault backup | Free tier |

## Estimated Monthly Budget

| Item | Cost |
|-------|------|
| VPS (Hetzner CPX31) | 15 EUR |
| OpenRouter (moderate usage) | 5-20 EUR |
| Domain name (optional) | 1 EUR |
| **Total** | **21-36 EUR/month** |

The OpenRouter cost depends heavily on the model used and the volume of requests. Claude Sonnet costs approximately 3$/M input tokens. Haiku is 10x cheaper.

## Software on Your Local Machine

On your workstation (not the VPS), you will need:

- An SSH terminal (native Terminal on Mac/Linux, Windows Terminal + OpenSSH on Windows)
- Git
- A text editor (VS Code recommended, with the Remote-SSH extension)
- Tailscale installed locally

## Expected Skills

This playbook assumes you know how to:

- Open a terminal and type commands
- Connect via SSH to a server
- Read an error message in English

If you don't know how to do these things, start with a basic SSH tutorial before continuing.

## Common Mistakes

- **Getting a VPS with 2 GB of RAM**: Vault + PostgreSQL + Node.js + Docker saturate quickly. 8 GB is the bare minimum.
- **Forgetting to create the OpenRouter account beforehand**: The OpenClaw installation requires an API key from the start.
- **Choosing a datacenter outside Europe**: If your data is European, the server location matters (GDPR).

## Verification

Before moving to the next section, confirm:

- [ ] VPS ordered and accessible (you have the IP and root password)
- [ ] Tailscale, GitHub, OpenRouter accounts created
- [ ] SSH works from your local machine to the VPS
- [ ] Ubuntu 24.04 LTS installed on the VPS

## Estimated Time

15 minutes (excluding account creation and VPS ordering).
