---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.12 -- Configuration initiale OpenClaw

## Contexte

Le fichier `~/.openclaw/config.json` est le centre de controle d'OpenClaw. Chaque champ affecte le comportement du systeme. Cette section detaille un fichier de configuration complet et commente.

## Fichier de configuration complet

Creez ou editez `~/.openclaw/config.json` :

```json
{
  // --- Identification ---
  "instance_name": "oa-paris",
  "environment": "production",

  // --- Modele IA ---
  "model": {
    "provider": "openrouter",
    "default_model": "anthropic/claude-sonnet-4",
    "fallback_model": "anthropic/claude-haiku-4-5",
    "temperature": 0.3,
    "max_tokens": 8192
  },

  // --- Connexion Vault ---
  "vault": {
    "enabled": true,
    "address": "http://127.0.0.1:8200",
    "token_env": "VAULT_TOKEN",
    "secret_prefix": "secret"
  },

  // --- Base de donnees ---
  "database": {
    "type": "postgresql",
    "vault_path": "secret/database",
    "pool_size": 10,
    "ssl": false
  },

  // --- Gateway ---
  "gateway": {
    "host": "127.0.0.1",
    "port": 3000,
    "cors_origins": []
  },

  // --- Notifications ---
  "notifications": {
    "telegram": {
      "enabled": true,
      "vault_path": "secret/telegram"
    }
  },

  // --- Logging ---
  "logging": {
    "level": "info",
    "file": "~/.openclaw/logs/openclaw.log",
    "max_size_mb": 50,
    "max_files": 5
  },

  // --- Workspace ---
  "workspace": {
    "path": "~/.openclaw/workspace",
    "auto_save_memory": true,
    "session_retention_days": 30
  },

  // --- Securite ---
  "security": {
    "allowed_commands": ["git", "npm", "node", "docker", "docker compose"],
    "blocked_paths": ["/etc/shadow", "/root"],
    "require_confirmation_for": ["rm", "drop", "delete", "truncate"]
  }
}
```

> **Les noms de modeles OpenRouter changent regulierement.** Avant de configurer, verifiez les noms actuels sur [openrouter.ai/models](https://openrouter.ai/models). Les noms ci-dessus etaient valides en avril 2026.

**Note** : JSON ne supporte pas les commentaires. Retirez les lignes `//` dans le fichier final, ou utilisez un pre-processeur JSON5. Les commentaires ci-dessus sont pour la documentation uniquement.

## Explication champ par champ

### instance_name

Identifiant unique de cette instance. Utile si vous avez plusieurs VPS. Apparait dans les logs et les notifications.

### model

| Champ | Description |
|-------|-------------|
| `provider` | Service d'acces aux modeles. `openrouter` permet de changer de modele sans changer de provider. |
| `default_model` | Modele utilise par defaut. Claude Sonnet 4 offre le meilleur rapport qualite/prix. |
| `fallback_model` | Modele de repli si le principal est indisponible ou trop lent. Haiku est rapide et pas cher. |
| `temperature` | 0 = deterministe, 1 = creatif. 0.3 est un bon equilibre pour du code. |
| `max_tokens` | Longueur maximale de la reponse. 8192 est suffisant pour la plupart des taches. |

### vault

| Champ | Description |
|-------|-------------|
| `enabled` | Active la recuperation des secrets depuis Vault. |
| `address` | URL locale de Vault. Ne changez pas sauf si Vault est sur une autre machine. |
| `token_env` | Variable d'environnement contenant le token Vault. Definie dans le fichier systemd (section 15). |
| `secret_prefix` | Prefixe du chemin KV. `secret` correspond a `vault kv get secret/...`. |

### database

| Champ | Description |
|-------|-------------|
| `vault_path` | Chemin Vault ou sont stockes les credentials PostgreSQL. |
| `pool_size` | Nombre de connexions simultanees. 10 est suffisant pour un usage moderé. |
| `ssl` | Desactive car la connexion est locale (meme machine, via 127.0.0.1). |

### security

| Champ | Description |
|-------|-------------|
| `allowed_commands` | Commandes systeme que l'agent peut executer. Ajoutez selon vos besoins. |
| `blocked_paths` | Chemins que l'agent ne peut ni lire ni ecrire. |
| `require_confirmation_for` | Commandes qui necessitent une confirmation manuelle avant execution. |

## Connexion a Vault

Pour que la configuration fonctionne, le token Vault doit etre disponible en variable d'environnement :

```bash
$ export VAULT_TOKEN="votre-token-applicatif"
```

Pour rendre ca permanent, ajoutez a `~/.bashrc` :

```bash
export VAULT_TOKEN="votre-token-applicatif"
```

Ou mieux : utilisez le fichier systemd (section 15) pour injecter la variable.

## Choix du modele

| Modele | Forces | Faiblesses | Cout approx. |
|--------|--------|------------|--------------|
| Claude Sonnet 4 | Meilleur raisonnement, code de qualite | Plus lent, plus cher | ~3$/M tokens entree |
| Claude Haiku 3.5 | Rapide, pas cher | Moins precis sur les taches complexes | ~0.25$/M tokens |
| Mistral Large | Bon en francais | Moins bon en code | ~2$/M tokens |
| Gemini 2.0 Flash | Tres rapide, grande fenetre | Variable en qualite | ~0.10$/M tokens |

Recommandation : Claude Sonnet en defaut, Haiku en fallback.

## Erreurs courantes

- **JSON invalide** : Retirez les commentaires `//` du fichier. Validez avec `jq . ~/.openclaw/config.json`.
- **Vault token absent** : L'erreur apparait au demarrage d'OpenClaw. Verifiez `echo $VAULT_TOKEN`.
- **Modele introuvable** : Verifiez le nom exact du modele sur openrouter.ai/models.
- **Pool size trop grand** : PostgreSQL a un nombre limite de connexions (100 par defaut). 10 est raisonnable.

## Verification

```bash
$ cat ~/.openclaw/config.json | python3 -m json.tool
$ openclaw doctor
```

Resultats attendus :
- JSON valide (pas d'erreur de parsing)
- Doctor : configuration valide

## Temps estime

15 minutes.
