---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# Chapitre 2 -- Installation

> Du VPS vierge a une instance OpenClaw fonctionnelle. Etape par etape, sans rien supposer.

Ce chapitre est le plus dense du playbook. Il couvre 19 sections, de la preparation du serveur jusqu'au premier deploiement automatise. Chaque section est autonome : vous pouvez reprendre a n'importe quel point si une etape a deja ete faite.

Temps total estime : 3 a 5 heures pour une premiere installation complete.

---

## Sommaire

| #  | Section | Description | Temps estime |
|----|---------|-------------|--------------|
| 01 | [Prerequis](01-prerequis.md) | Materiel, logiciel, comptes, budget | 15 min |
| 02 | [Securiser le VPS](02-securiser-vps.md) | Utilisateur, SSH, pare-feu, mises a jour | 20 min |
| 03 | [Tailscale](03-tailscale.md) | Reseau prive mesh VPN | 10 min |
| 04 | [Docker](04-docker.md) | Docker Engine et Docker Compose | 10 min |
| 05 | [Node.js et PM2](05-nodejs-pm2.md) | Runtime Node via nvm, gestionnaire PM2 | 10 min |
| 06 | [Structure de dossiers](06-structure-dossiers.md) | Arborescence conventionnelle du projet | 5 min |
| 07 | [HashiCorp Vault](07-vault.md) | Gestion centralisee des secrets | 30 min |
| 08 | [PostgreSQL](08-postgresql.md) | Base de donnees via Docker | 15 min |
| 09 | [Health check](09-health-check.md) | Script de verification de l'infrastructure | 10 min |
| 10 | [Installation OpenClaw](10-openclaw-install.md) | Installation de l'outil principal | 15 min |
| 11 | [Workspace](11-workspace.md) | Structure du workspace OpenClaw | 10 min |
| 12 | [Configuration OpenClaw](12-config-openclaw.md) | Fichier de configuration commente | 15 min |
| 13 | [OpenRouter](13-openrouter.md) | Connexion multi-modeles IA | 10 min |
| 14 | [Telegram](14-telegram.md) | Bot de notification et commande | 10 min |
| 15 | [Gateway systemd](15-gateway-systemd.md) | Service systemd pour la gateway | 10 min |
| 16 | [Verification complete](16-verification-complete.md) | Checklist post-installation | 10 min |
| 17 | [Git init](17-git-init.md) | Depot Git et premier commit | 10 min |
| 18 | [CLAUDE.md](18-claude-md.md) | Fichier de reference pour agents IA | 10 min |
| 19 | [Script de deploiement](19-script-deploy.md) | Script deploy.sh idempotent | 15 min |

---

## Ordre recommande

Les sections sont numerotees dans l'ordre logique d'execution. Certaines dependances :

- La section 07 (Vault) doit etre faite avant 08 (PostgreSQL), 13 (OpenRouter) et 14 (Telegram)
- La section 04 (Docker) doit etre faite avant 07 (Vault) et 08 (PostgreSQL)
- La section 05 (Node.js) doit etre faite avant 10 (OpenClaw)
- La section 16 (Verification) suppose que toutes les sections precedentes sont terminees

## Outil optionnel : Install Tracker

Pour suivre votre progression en temps reel, vous pouvez deployer le **Install Tracker** — un cockpit minimal qui trace les phases, les decisions, les services et les actions.

```bash
cd tools/install-tracker
docker compose up -d
# Accessible sur http://localhost:3007
```

C'est optionnel. Le playbook fonctionne sans. Mais si vous voulez un tableau de bord visuel de votre installation, c'est pret en une commande. Details dans [tools/install-tracker/README.md](../../tools/install-tracker/README.md).

---

## Conventions dans ce chapitre

- Les commandes sont prefixees par `$` pour un utilisateur normal, `#` pour root
- Les blocs `IMPORTANT` signalent un risque de blocage
- Les blocs `VERIFICATION` indiquent comment confirmer que l'etape a fonctionne
- Les chemins sont relatifs au home de l'utilisateur (`~`) sauf indication contraire

---

*[Contribuer a ce chapitre](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)*
