---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2. Installation

> Du VPS vierge a une instance OpenClaw fonctionnelle. Etape par etape, sans rien supposer.

Ce chapitre couvre le parcours complet d'installation : preparation du serveur, mise en place de l'infrastructure (Docker, Vault, PostgreSQL), installation d'OpenClaw et de ses connexions, puis verification et automatisation du deploiement. C'est le chapitre le plus dense du playbook, avec 19 sections autonomes. A la fin, vous aurez un environnement de production fonctionnel et un script de deploiement idempotent.

Temps total estime : 3 a 5 heures pour une premiere installation complete. Les sections sont numerotees dans l'ordre logique d'execution. Certaines dependances importantes : Docker (04) avant Vault (07) et PostgreSQL (08), Vault (07) avant OpenRouter (13) et Telegram (14), Node.js (05) avant OpenClaw (10).

---

## Sommaire

### Avant de commencer

- **[Checklist pre-vol](00-preflight.md)**
  Tous les comptes, cles, decisions et budgets a preparer avant de lancer l'installation

### Partie A -- Preparation du serveur

- **2.1 -- [Prerequis](01-prerequis.md)**
  Inventaire complet de ce qu'il faut avant de commencer : materiel, logiciels, comptes et budget

- **2.2 -- [Securiser le VPS](02-securiser-vps.md)**
  Creer un utilisateur non-root, verrouiller SSH, configurer le pare-feu et les mises a jour automatiques

- **2.3 -- [Tailscale](03-tailscale.md)**
  Deployer un reseau prive mesh pour acceder au serveur sans exposer de ports publics

- **2.4 -- [Docker](04-docker.md)**
  Installer Docker Engine et Docker Compose, verifier que les conteneurs tournent correctement

- **2.5 -- [Node.js et PM2](05-nodejs-pm2.md)**
  Installer Node.js via nvm et configurer PM2 pour gerer les processus en arriere-plan

- **2.6 -- [Structure de dossiers](06-structure-dossiers.md)**
  Creer l'arborescence conventionnelle du projet pour que chaque fichier ait sa place

### Partie B -- Infrastructure et secrets

- **2.7 -- [HashiCorp Vault](07-vault.md)**
  Deployer un gestionnaire de secrets centralise pour ne jamais stocker de credentials en clair

- **2.8 -- [PostgreSQL](08-postgresql.md)**
  Lancer la base de donnees via Docker et la connecter a Vault pour les credentials

- **2.9 -- [Health check](09-health-check.md)**
  Ecrire un script qui verifie en une commande que toute l'infrastructure est operationnelle

### Partie C -- OpenClaw

- **2.10 -- [Installation OpenClaw](10-openclaw-install.md)**
  Telecharger, installer et lancer OpenClaw pour la premiere fois

- **2.11 -- [Workspace](11-workspace.md)**
  Comprendre et organiser la structure du workspace ou l'agent va operer

- **2.12 -- [Configuration OpenClaw](12-config-openclaw.md)**
  Remplir le fichier de configuration principal avec les valeurs adaptees a votre contexte

- **2.13 -- [OpenRouter](13-openrouter.md)**
  Connecter OpenClaw a plusieurs modeles IA via une API unique

- **2.14 -- [Telegram](14-telegram.md)**
  Creer un bot Telegram pour recevoir des notifications et envoyer des commandes a l'agent

- **2.15 -- [Gateway systemd](15-gateway-systemd.md)**
  Enregistrer la gateway comme service systeme pour qu'elle redemarre automatiquement

### Partie D -- Verification et deploiement

- **2.16 -- [Verification complete](16-verification-complete.md)**
  Passer la checklist post-installation pour confirmer que chaque composant fonctionne

- **2.17 -- [Git init](17-git-init.md)**
  Initialiser le depot Git et faire le premier commit pour versionner toute la configuration

- **2.18 -- [CLAUDE.md](18-claude-md.md)**
  Rediger le fichier de reference que les agents IA liront en ouvrant le repo

- **2.19 -- [Script de deploiement](19-script-deploy.md)**
  Construire un script deploy.sh idempotent qui reproduit l'installation en une commande

### Annexe

- **2.20 -- [Adapter pour un VPS existant](20-adapter-existant.md)**
  Diagnostiquer ce qui est deja en place et adapter le parcours d'installation

---

## Outil optionnel : Install Tracker

Pour suivre votre progression en temps reel, vous pouvez deployer le **Install Tracker** -- un cockpit minimal qui trace les phases, les decisions, les services et les actions.

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

[Contribuer a ce chapitre](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)
