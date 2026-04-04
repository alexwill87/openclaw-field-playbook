---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit, claude-aurel]
lang: en
---

# Pre-flight checklist -- Get everything ready before you start

This page exists because we got tired of discovering a prerequisite in section 13 that we could have prepared beforehand. Everything that follows must be ready BEFORE you run the first command in chapter 2.

Total preparation time: approximately 30 minutes.

---

## 1. Accounts to create

Create these accounts now. Not "later". Now.

| # | Service | Sign-up URL | What to note | Estimated time |
|---|---------|-------------|--------------|----------------|
| 1 | **Hetzner** or **OVH** (VPS) | [hetzner.com/cloud](https://www.hetzner.com/cloud) / [ovh.com/vps](https://www.ovhcloud.com/fr/vps/) | Account credentials, server IP once ordered | 10 min |
| 2 | **Tailscale** | [login.tailscale.com/start](https://login.tailscale.com/start) | Account created (sign in via Google, GitHub, or Microsoft) | 2 min |
| 3 | **OpenRouter** | [openrouter.ai](https://openrouter.ai) | API key (format `sk-or-v1-...`). Go to Settings > API Keys after signing up | 5 min |
| 4 | **Telegram** (bot) | In the Telegram app, search for `@BotFather` and send `/newbot` | Bot token (format `123456789:ABCDef...`), bot username | 5 min |
| 5 | **GitHub** | [github.com/signup](https://github.com/signup) | Credentials. Also generate a Personal Access Token (Settings > Developer settings > Tokens) | 5 min |

**Telegram tip**: After creating the bot, send it a message in Telegram. You'll need this later to retrieve your `chat_id`.

---

## 2. Information to collect

Before touching the server, gather these items:

### Your current public IP

```bash
$ curl -4 ifconfig.me
```

Note it down. You'll need it to configure the VPS firewall.

### Your SSH public key

Check if you already have one:

```bash
$ cat ~/.ssh/id_ed25519.pub
```

If the file doesn't exist, create a key:

```bash
$ ssh-keygen -t ed25519 -C "your-email@example.com"
```

Accept the default path, set a passphrase. Copy the contents of `~/.ssh/id_ed25519.pub`.

### A strong password for PostgreSQL

Generate one with:

```bash
$ openssl rand -base64 24
```

Note it in a password manager (1Password, Bitwarden, KeePass). You'll store it in Vault in section 07.

### A name for your agent

This is the name that will appear in `SOUL.md` -- the identity of your AI agent. Examples: `Atlas`, `Vigil`, `Sentinel`. Choose something short and memorable.

### The email address of the primary user

It will be used in `USER.md` to identify the instance owner. Use an email address you actually check.

---

## 3. Decisions to make BEFORE you start

Don't discover these choices in the middle of installation. Decide now.

| Decision | Options | Recommendation |
|----------|---------|-----------------|
| Vault or .env files? | Vault (production) / .env (prototype) | Vault if multi-user, .env if solo |
| PM2 or systemd? | PM2 (if already using) / systemd (native Ubuntu) | systemd for newcomers |
| Which LLM model by default? | Claude Sonnet / Haiku / Mistral / Gemini | Claude Sonnet 4 via OpenRouter |
| PostgreSQL or SQLite? | PostgreSQL (recommended) / SQLite (lightweight) | PostgreSQL |
| Mattermost or not? | Yes (structured communication) / No (email/Telegram sufficient) | Not required at the start |

**Vault vs .env**: If you're alone and this is a prototype, `.env` is enough to get started. But if other people or agents access the secrets, Vault is the investment that avoids technical debt. The playbook documents both approaches, but the following sections use Vault by default.

**PM2 vs systemd**: PM2 is convenient if you come from the Node.js world. systemd is native to Ubuntu, requires no additional installation, and integrates better with system logs. If you have no preference, use systemd.

**LLM model**: Claude Sonnet 4 offers the best balance of accuracy/cost for complex tasks. Haiku 3.5 is the fast, economical fallback. You can change it anytime via OpenRouter.

---

## 4. Estimated budget

| Item | Monthly cost | Notes |
|------|-------------|-------|
| VPS (Hetzner CPX21) | ~5-8 EUR/month | 4 CPU, 8 GB RAM, 80 GB SSD |
| OpenRouter API key | ~10-30 EUR/month | Depends on usage. Set an alert at 10 EUR and a limit at 30 EUR |
| Domain (optional) | ~10 EUR/year | If you want a custom domain |
| **Total** | **~15-40 EUR/month** | |

The most variable item is OpenRouter. An active agent using Claude Sonnet consumes more than a dormant agent on Haiku. Monitor your OpenRouter dashboard in the first few weeks.

---

## 5. Estimated time

| Phase | Duration |
|-------|----------|
| Account creation (this page) | 30 minutes |
| Complete installation (chapter 2, sections 01-19) | 3-5 hours |
| Configuration (chapter 3) | 2-3 hours |
| Customization (chapter 4) | Ongoing |

Plan a half-day for chapters 2 and 3. Don't start at 11 PM on a Sunday night.

---

## Quick checklist

Check off each point before moving to section 01:

- [ ] VPS account created and server ordered
- [ ] Tailscale account created
- [ ] OpenRouter account created and API key noted
- [ ] Telegram bot created and token noted
- [ ] GitHub account created
- [ ] SSH key generated (or existing key located)
- [ ] PostgreSQL password generated
- [ ] Vault vs .env decision made
- [ ] PM2 vs systemd decision made
- [ ] Monthly budget estimated and validated

All checked? Move to **[2.1 -- Prerequisites](01-prerequis.md)**.

---
