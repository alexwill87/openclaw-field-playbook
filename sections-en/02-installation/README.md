---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2. Installation

> From a bare VPS to a working OpenClaw instance. Step by step, assuming nothing.

This chapter covers the complete installation journey: server preparation, infrastructure setup (Docker, Vault, PostgreSQL), OpenClaw installation and integrations, then verification and deployment automation. It's the densest chapter of the playbook, with 19 standalone sections. By the end, you'll have a functional production environment and an idempotent deployment script.

Estimated total time: 3 to 5 hours for a first complete installation. Sections are numbered in logical execution order. Some important dependencies: Docker (04) before Vault (07) and PostgreSQL (08), Vault (07) before OpenRouter (13) and Telegram (14), Node.js (05) before OpenClaw (10).

---

## Table of Contents

### Before You Start

- **[Preflight Checklist](00-preflight.md)**
  All accounts, keys, decisions, and budgets to prepare before launching the installation

### Part A -- Server Preparation

- **2.1 -- [Prerequisites](01-prerequis.md)**
  Complete inventory of what you need before starting: hardware, software, accounts, and budget

- **2.2 -- [Secure the VPS](02-securiser-vps.md)**
  Create a non-root user, lock down SSH, configure the firewall, and enable automatic updates

- **2.3 -- [Tailscale](03-tailscale.md)**
  Deploy a private mesh network to access your server without exposing public ports

- **2.4 -- [Docker](04-docker.md)**
  Install Docker Engine and Docker Compose, verify that containers run correctly

- **2.5 -- [Node.js and PM2](05-nodejs-pm2.md)**
  Install Node.js via nvm and configure PM2 to manage background processes

- **2.6 -- [Folder Structure](06-structure-dossiers.md)**
  Create the conventional project directory tree so every file has its place

### Part B -- Infrastructure and Secrets

- **2.7 -- [HashiCorp Vault](07-vault.md)**
  Deploy a centralized secrets manager so credentials are never stored in plain text

- **2.8 -- [PostgreSQL](08-postgresql.md)**
  Launch the database via Docker and connect it to Vault for credential management

- **2.9 -- [Health Check](09-health-check.md)**
  Write a script that verifies in one command that all infrastructure is operational

### Part C -- OpenClaw

- **2.10 -- [OpenClaw Installation](10-openclaw-install.md)**
  Download, install, and launch OpenClaw for the first time

- **2.11 -- [Workspace](11-workspace.md)**
  Understand and organize the workspace structure where the agent will operate

- **2.12 -- [OpenClaw Configuration](12-config-openclaw.md)**
  Fill in the main configuration file with values suited to your context

- **2.13 -- [OpenRouter](13-openrouter.md)**
  Connect OpenClaw to multiple AI models via a single API

- **2.14 -- [Telegram](14-telegram.md)**
  Create a Telegram bot to receive notifications and send commands to the agent

- **2.15 -- [Gateway systemd](15-gateway-systemd.md)**
  Register the gateway as a system service so it restarts automatically

### Part D -- Verification and Deployment

- **2.16 -- [Complete Verification](16-verification-complete.md)**
  Run through the post-installation checklist to confirm each component works

- **2.17 -- [Git Init](17-git-init.md)**
  Initialize the Git repository and make the first commit to version your configuration

- **2.18 -- [CLAUDE.md](18-claude-md.md)**
  Write the reference file that AI agents will read when opening the repository

- **2.19 -- [Deployment Script](19-script-deploy.md)**
  Build an idempotent deploy.sh script that reproduces the installation in one command

### Appendix

- **2.20 -- [Adapt for an Existing VPS](20-adapter-existant.md)**
  Diagnose what's already in place and adapt the installation journey

---

## Optional Tool: Install Tracker

To track your progress in real time, you can deploy the **Install Tracker** -- a minimal cockpit that logs phases, decisions, services, and actions.

```bash
cd tools/install-tracker
docker compose up -d
# Accessible on http://localhost:3007
```

It's optional. The playbook works without it. But if you want a visual dashboard of your installation, it's ready in one command. Details in [tools/install-tracker/README.md](../../tools/install-tracker/README.md).

---

## Conventions in This Chapter

- Commands are prefixed with `$` for a regular user, `#` for root
- `IMPORTANT` blocks signal a risk of blocking issues
- `VERIFICATION` blocks show how to confirm the step worked
- Paths are relative to the user's home (`~`) unless otherwise stated

---

[Contribute to this chapter](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)

---
