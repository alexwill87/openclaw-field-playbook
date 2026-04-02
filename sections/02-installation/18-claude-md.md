---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.18 -- CLAUDE.md

## Contexte

`CLAUDE.md` est le fichier que tout agent IA lit en premier quand il travaille sur votre depot. C'est le contrat entre vous et l'agent : conventions, stack, commandes autorisees, regles. Sans ce fichier, l'agent improvise. Avec ce fichier, il suit VOS regles.

Ce fichier va a la racine du depot Git.

## Le fichier CLAUDE.md complet

Creez `CLAUDE.md` a la racine de votre depot :

```markdown
# CLAUDE.md -- Instructions pour les agents IA

## Identite du projet

- Nom : OA System
- Description : Infrastructure d'agents IA autonomes sur VPS
- Mainteneurs : [votre nom], agents OpenClaw
- Langue du code : anglais
- Langue de la documentation : francais
- Depot : prive

## Stack technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Runtime | Node.js | 22.x LTS |
| Base de donnees | PostgreSQL | 16 (Docker) |
| Secrets | HashiCorp Vault | 1.17 (Docker) |
| Process manager | PM2 | 5.x |
| Conteneurisation | Docker + Docker Compose v2 | 28.x |
| VPN | Tailscale | derniere |
| OS | Ubuntu | 24.04 LTS |

## Structure du depot

```
.
├── docker/           # Fichiers Docker Compose (pas de donnees)
├── scripts/          # Scripts bash utilitaires
├── CLAUDE.md         # Ce fichier
├── .gitignore        # Fichiers exclus du versionnement
└── README.md         # Documentation du projet
```

## Commandes courantes

```bash
# Deploiement
./scripts/deploy.sh

# Health check
./scripts/health-check.sh

# Backup base de donnees
./scripts/backup-postgres.sh

# Notification Telegram
./scripts/notify-telegram.sh "message"

# Logs gateway
journalctl -u openclaw-gateway -f

# Restart gateway
sudo systemctl restart openclaw-gateway
```

## Regles de code

1. Pas de secrets en dur dans le code. Tout passe par Vault.
2. Chaque script doit etre idempotent (executable plusieurs fois sans effet de bord).
3. Les commandes Docker utilisent `docker compose` (avec espace, pas tiret).
4. Les chemins sont absolus dans les scripts, relatifs dans le code applicatif.
5. Les logs vont dans ~/logs/ ou journalctl, jamais dans le depot Git.

## Regles de commit

- Format : `type: description courte`
- Types : feat, fix, docs, refactor, test, chore
- En anglais
- Une seule responsabilite par commit

## Ce qu'un agent NE DOIT PAS faire

- Modifier les fichiers dans /etc/ sans demander confirmation
- Supprimer des fichiers sans lister ce qui sera supprime
- Executer `rm -rf` sur quoi que ce soit
- Toucher aux unseal keys de Vault
- Committer des fichiers .env ou des credentials
- Faire `git push --force` sur main
- Modifier ce fichier (CLAUDE.md) sans approbation humaine

## Ce qu'un agent PEUT faire librement

- Lire n'importe quel fichier du depot
- Executer les scripts dans ~/scripts/
- Lire les secrets depuis Vault (en lecture seule)
- Creer des branches Git
- Faire des commits sur des branches (pas main directement)
- Consulter les logs
- Executer le health check

## Variables d'environnement

Les variables sont injectees via systemd ou Vault. Ne jamais les mettre dans .bashrc pour la production.

| Variable | Source | Description |
|----------|--------|-------------|
| VAULT_ADDR | systemd | URL de Vault |
| VAULT_TOKEN | systemd | Token applicatif Vault |
| NODE_ENV | systemd | production |
```

## Pourquoi ce fichier est important

Sans CLAUDE.md :
- L'agent peut tenter d'installer des paquets via `sudo apt install` alors que vous utilisez Docker
- L'agent peut creer des fichiers .env au lieu d'utiliser Vault
- L'agent peut faire `docker-compose` (tiret) au lieu de `docker compose` (espace)
- L'agent peut committer sur main sans branche

Avec CLAUDE.md :
- L'agent connait votre stack exacte
- L'agent respecte vos conventions
- L'agent sait ce qu'il peut et ne peut pas faire
- Moins de corrections manuelles

## Mise a jour

Ce fichier evolue avec le projet. Chaque fois que vous ajoutez un service, un script ou une regle, mettez CLAUDE.md a jour. C'est la source de verite pour les agents.

## Erreurs courantes

- **Ne pas creer le fichier** : L'agent fonctionne, mais fait des choix arbitraires. Le temps perdu en corrections depasse largement le temps de redaction.
- **Fichier trop long** : Gardez-le concis. Les agents ont un contexte limite. L'essentiel suffit.
- **Fichier obsolete** : Un CLAUDE.md qui decrit une stack qui a change est pire qu'aucun fichier. Maintenez-le.
- **Mettre des secrets dans CLAUDE.md** : Ce fichier est dans Git. Pas de tokens, pas de mots de passe.

## Verification

```bash
$ cat CLAUDE.md | head -5
$ git log --oneline CLAUDE.md
```

Resultats attendus :
- Le fichier existe et est lisible
- Il est versionne dans Git

## Temps estime

10 minutes.
