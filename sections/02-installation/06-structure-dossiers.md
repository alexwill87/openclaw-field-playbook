---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.6 -- Structure de dossiers

## Contexte

Avant d'installer les services, on cree une arborescence coherente. Ca evite l'effet "fichiers partout" qui rend la maintenance impossible. Cette convention est utilisee dans tout le playbook.

## Etape 1 : Creer l'arborescence

```bash
$ mkdir -p ~/docker/vault
$ mkdir -p ~/docker/postgres
$ mkdir -p ~/scripts
$ mkdir -p ~/backups/postgres
$ mkdir -p ~/backups/vault
$ mkdir -p ~/logs
```

## Arborescence resultante

```
~/
├── docker/
│   ├── vault/              # docker-compose.yml + config Vault
│   │   ├── docker-compose.yml
│   │   ├── config/
│   │   └── data/
│   └── postgres/           # docker-compose.yml + donnees PostgreSQL
│       ├── docker-compose.yml
│       └── data/
├── scripts/                # Scripts maison (health check, deploy, backup)
│   ├── health-check.sh
│   ├── deploy.sh
│   └── backup-postgres.sh
├── backups/                # Sauvegardes locales
│   ├── postgres/           # Dumps SQL
│   └── vault/              # Snapshots Vault
├── logs/                   # Logs applicatifs (hors journalctl)
└── .openclaw/              # Cree automatiquement par OpenClaw (section 11)
```

## Conventions

| Regle | Explication |
|-------|-------------|
| `~/docker/<service>/` | Chaque service Docker a son propre sous-dossier |
| `docker-compose.yml` a la racine du sous-dossier | On lance `docker compose up -d` depuis ce dossier |
| `~/scripts/` pour les scripts maison | Tout script utilitaire va ici, avec `chmod +x` |
| `~/backups/` pour les sauvegardes locales | Les crons de backup ecrivent ici |
| Pas de fichiers a la racine de `~` | Gardez le home propre |

## Etape 2 : Rendre les scripts executables

Pour l'instant le dossier est vide, mais prenez l'habitude :

```bash
$ chmod +x ~/scripts/*.sh 2>/dev/null || true
```

## Erreurs courantes

- **Mettre tous les docker-compose.yml au meme endroit** : Chaque service a son dossier. Sinon les volumes se melangent.
- **Creer les dossiers en root** : Creez tout en tant que `deploy` (votre utilisateur). Sinon les permissions bloqueront Docker.
- **Oublier le dossier backups** : Les sauvegardes sont configurees dans les sections suivantes. Le dossier doit exister.

## Verification

```bash
$ ls -la ~/docker/
$ ls -la ~/scripts/
$ ls -la ~/backups/
```

Resultats attendus : les dossiers existent et appartiennent a votre utilisateur (pas a root).

## Temps estime

5 minutes.
