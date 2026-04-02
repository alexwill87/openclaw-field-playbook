---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.11 -- Structure du workspace

## Contexte

OpenClaw organise ses donnees dans un workspace (`~/.openclaw/`). Ce dossier est cree automatiquement au premier lancement. Comprendre sa structure est essentiel pour le debug, la sauvegarde et l'extension du systeme.

## Arborescence commentee

```
~/.openclaw/
├── workspace/                  # Repertoire de travail principal
│   ├── knowledge/              # Base de connaissances injectee dans le contexte
│   │   ├── domain/             # Connaissances specifiques au domaine
│   │   └── system/             # Connaissances systeme (mises a jour auto)
│   ├── memory/                 # Memoire persistante entre sessions
│   │   ├── MEMORY.md           # Fichier principal de memoire
│   │   └── *.md                # Fichiers de memoire thematiques
│   ├── sessions/               # Historique des sessions
│   │   └── YYYY-MM-DD/         # Organise par date
│   │       └── session-ID.json # Chaque session avec contexte et echanges
│   ├── skills/                 # Competences chargees dynamiquement
│   │   ├── builtin/            # Skills integrées (non modifiables)
│   │   └── custom/             # Vos skills personnalisees
│   └── agents/                 # Definitions d'agents
│       ├── default.json        # Agent par defaut
│       └── custom/             # Vos agents personnalises
├── config.json                 # Configuration principale (section 12)
├── credentials.json            # Tokens et acces (chiffre)
└── logs/                       # Logs internes OpenClaw
    └── openclaw.log
```

## Role de chaque dossier

### knowledge/

Contient les documents que l'agent peut consulter pour repondre. Le sous-dossier `domain/` est le votre : mettez-y vos documents metier, specifications, guides internes.

```bash
$ ls ~/.openclaw/workspace/knowledge/
```

### memory/

Memoire persistante. Le fichier `MEMORY.md` est lu automatiquement a chaque session. Les agents y stockent ce qu'ils doivent retenir entre les conversations.

```bash
$ cat ~/.openclaw/workspace/memory/MEMORY.md
```

### sessions/

Historique complet de chaque conversation. Utile pour le debug et l'audit. Les vieilles sessions peuvent etre archivees.

### skills/

Les skills sont des capacites que l'agent peut invoquer. Le dossier `custom/` vous permet d'ajouter vos propres skills sans toucher aux skills integrées.

### agents/

Definitions d'agents avec leurs instructions systeme, skills autorisees et parametres. Le fichier `default.json` est utilise quand aucun agent n'est specifie.

## Droits et propriete

Tout le dossier `~/.openclaw/` doit appartenir a votre utilisateur :

```bash
$ ls -la ~/.openclaw/
```

Si ce n'est pas le cas :

```bash
$ sudo chown -R $USER:$USER ~/.openclaw/
```

## Sauvegarder le workspace

Le workspace contient des donnees precieuses (memoire, knowledge, sessions). Incluez-le dans vos sauvegardes :

```bash
$ tar -czf ~/backups/openclaw-workspace-$(date +%Y%m%d).tar.gz ~/.openclaw/workspace/
```

Ne sauvegardez PAS `credentials.json` dans un backup non chiffre.

## Erreurs courantes

- **Modifier les fichiers dans `builtin/`** : Ces fichiers sont ecrases a chaque mise a jour. Utilisez le dossier `custom/` pour vos modifications.
- **Supprimer `MEMORY.md`** : L'agent perd toute sa memoire. Sauvegardez ce fichier regulierement.
- **Workspace cree par root** : Si vous avez lance `sudo openclaw` par erreur, les fichiers appartiendront a root. Corrigez avec `chown`.
- **Sessions qui prennent trop de place** : Apres quelques mois, le dossier `sessions/` peut peser lourd. Archivez les vieilles sessions.

## Verification

```bash
$ ls -la ~/.openclaw/
$ ls -la ~/.openclaw/workspace/
$ cat ~/.openclaw/workspace/memory/MEMORY.md
```

Resultats attendus :
- Le dossier existe et appartient a votre utilisateur
- Les sous-dossiers knowledge/, memory/, sessions/, skills/, agents/ existent
- MEMORY.md est lisible

## Temps estime

10 minutes (exploration et comprehension).
