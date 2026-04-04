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
| Gemini 2.5 Flash | Tres rapide, grande fenetre | Variable en qualite | ~0.10$/M tokens |

### Tableau de decision par profil

| Profil | Modele recommande | Provider | Cout estime/jour | Notes |
|--------|-------------------|----------|-------------------|-------|
| Solo budget serre | `google/gemini-2.5-flash` | Google direct ou OpenRouter | ~0.50 EUR | Bon rapport qualite/prix |
| Solo qualite | `anthropic/claude-sonnet-4` | Anthropic direct | ~2-5 EUR | Meilleur raisonnement |
| Multi-modele | Modele explicite via OpenRouter | OpenRouter | Variable | **Jamais `auto`** |
| Production fiable | 1 primaire + 2 fallbacks | Mix | Variable | Tester chaque modele avant deploy |

### Regles de choix

1. **Ne jamais utiliser `openrouter/auto` en production.** Le routage automatique choisit un modele different a chaque appel, ce qui cause des incompatibilites (ex : certains modeles exigent `reasoning: true`). Resultat : erreurs 400 silencieuses, agent percu comme "endormi". Cas reel : 11.6% d'erreurs sur un VPS en avril 2026.
2. **Toujours tester le modele avant de configurer un canal.** Envoyez un message test via l'API et verifiez la reponse (section 2.13).
3. **Verifier la compatibilite reasoning.** Certains modeles exigent `reasoning: true` et retournent une erreur 400 silencieuse si desactive.
4. **Documenter les fallbacks.** Au moins 2 fallbacks de providers differents pour eviter les pannes totales.
5. **Monitorer.** Verifier periodiquement les sessions JSONL pour detecter les erreurs silencieuses (`grep "stopReason.*error"` — voir section 5.11).

Recommandation : Claude Sonnet en defaut, Haiku en fallback, Gemini Flash en fallback secondaire.

## Enregistrement des modeles dans `agents.defaults.models`

En plus de la configuration du modele principal, OpenClaw a besoin que les modeles soient enregistres dans la section `agents.defaults.models` pour que les agents puissent les utiliser. Ajoutez cette section dans `~/.openclaw/config.json` :

```json
"agents": {
  "defaults": {
    "models": [
      {
        "id": "anthropic/claude-sonnet-4",
        "provider": "openrouter",
        "role": "primary"
      },
      {
        "id": "anthropic/claude-haiku-4-5",
        "provider": "openrouter",
        "role": "fallback"
      }
    ]
  }
}
```

Ou via la CLI :

```bash
$ openclaw config set agents.defaults.models --strict-json '[{"id":"anthropic/claude-sonnet-4","provider":"openrouter","role":"primary"},{"id":"anthropic/claude-haiku-4-5","provider":"openrouter","role":"fallback"}]'
```

> **Sans cette etape**, les agents OpenClaw ne sauront pas quel modele utiliser et echoueront avec une erreur de type "no model configured for agent".

## Syntaxe de `openclaw config set`

Si vous preferez configurer via la CLI plutot qu'en editant le JSON a la main, voici la syntaxe de `openclaw config set` :

**Strings** (guillemets obligatoires pour les valeurs contenant des espaces ou caracteres speciaux) :

```bash
$ openclaw config set instance_name "oa-paris"
$ openclaw config set model.default_model "anthropic/claude-sonnet-4"
```

**Booleans** :

```bash
$ openclaw config set vault.enabled true
$ openclaw config set database.ssl false
```

**Nombres** :

```bash
$ openclaw config set model.temperature 0.3
$ openclaw config set model.max_tokens 8192
```

**Objets JSON** (utilisez `--strict-json` pour passer un objet complet) :

```bash
$ openclaw config set model --strict-json '{"provider":"openrouter","default_model":"anthropic/claude-sonnet-4","fallback_model":"anthropic/claude-haiku-4-5","temperature":0.3,"max_tokens":8192}'
```

**Lister la configuration actuelle** :

```bash
$ openclaw config get
$ openclaw config get model.default_model
```

> **Piege courant :** Si vous oubliez les guillemets autour d'une string contenant `/` (comme `anthropic/claude-sonnet-4`), le shell peut l'interpreter differemment. Encadrez toujours les valeurs de guillemets.

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
