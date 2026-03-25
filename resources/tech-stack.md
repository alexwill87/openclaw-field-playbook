---
status: complete
audience: both
last_updated: 2026-03
contributors: [alexwill87]
---

# Tech Stack — The OpenClaw Field Playbook

> This file documents the environment used to build and run this project.  
> Reference for contributors who want to replicate the setup.

---

## Agents

| Agent | Role |
|-------|------|
| OpenClaw | Primary agent framework — all automation runs through OpenClaw |
| Aurel | Alex's named OpenClaw instance — handles GitHub, content generation, scheduling |
| Sub-agents | Planned — specialised agents for specific domains (content, research, infra) |

---

## LLMs in use

| Model | Provider | Primary use |
|-------|----------|-------------|
| Claude Sonnet 4.6 | Anthropic | Primary reasoning, writing, code review |
| Gemini Flash 3.0 | Google | Fast tasks, high-volume operations |
| Mistral | Mistral AI | French-language content, EU-hosted |
| OpenAI GPT | OpenAI | Fallback, comparison testing |

---

## Infrastructure

| Component | Technology | Notes |
|-----------|------------|-------|
| Primary server | Hetzner VPS | Ubuntu 24, EU-hosted |
| Network | Tailscale | Zero-trust mesh, secure remote access |
| OS | Ubuntu 24 LTS | OpenClaw runs natively |
| DNS | Cloudflare (planned) | Domain management |

---

## Domains

| Domain | Status | Purpose |
|--------|--------|---------|
| openclawfieldplaybook.com | Active | Primary site and brand |
| openclawfieldbook.com | Active | Redirect to main domain |

---

## Collaboration tools

| Tool | Use |
|------|-----|
| GitHub | Repository, Issues, Pull Requests, Actions |
| GitHub Actions | AI review automation, weekly digest, PDF export |
| Notion | Internal notes, project planning |
| Claude (Anthropic) | Co-author of this playbook |

---

## Why this stack

- **Hetzner + Ubuntu** — EU-hosted, RGPD-compliant, full control
- **Tailscale** — secure access to the VPS without exposing ports publicly
- **Multi-LLM** — different models for different tasks; no single-provider dependency
- **GitHub-native** — all collaboration happens in the open, version-controlled

---

## For contributors

You do not need this exact stack to contribute. You need:
- A GitHub account (for Issues and PRs)
- A text editor (for Markdown)
- OpenClaw running (for testing prompts and configs in the playbook)

If you want to replicate Alex's full setup, start with [Chapter 2 — Installation](../sections/02-installation/README.md).
