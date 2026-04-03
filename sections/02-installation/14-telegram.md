---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.14 -- Connexion Telegram

## Contexte

Telegram sert de canal de notification et de commande pour OpenClaw. Le systeme envoie des alertes (health check en echec, deploiement termine, erreur critique) et peut recevoir des commandes simples via le bot.

## Etape 1 : Creer le bot avec @BotFather

1. Ouvrez Telegram et cherchez `@BotFather`
2. Envoyez `/newbot`
3. Donnez un nom : `OA System Bot` (ou ce que vous voulez)
4. Donnez un username : `oa_system_bot` (doit etre unique et finir par `bot`)
5. BotFather vous donne un token (format : `123456789:ABCDefGhIJKlmnoPQRSTuvwxyz`)

Copiez ce token.

## Etape 2 : Stocker le token dans Vault

```bash
$ docker exec vault vault kv put secret/telegram bot_token="123456789:ABCDefGhIJKlmnoPQRSTuvwxyz"
```

## Etape 3 : Obtenir votre chat_id

Le chat_id identifie la conversation ou le bot enverra les messages. Pour le trouver :

1. Envoyez un message quelconque a votre bot dans Telegram
2. Appelez l'API Telegram :

```bash
$ BOT_TOKEN=$(docker exec vault vault kv get -field=bot_token secret/telegram)
$ curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getUpdates" | python3 -m json.tool
```

3. Dans la reponse, cherchez `"chat": {"id": 123456789}`. Ce nombre est votre chat_id.

## Etape 4 : Stocker le chat_id dans Vault

Mettez a jour le secret Telegram avec le chat_id :

```bash
$ docker exec vault vault kv put secret/telegram \
  bot_token="123456789:ABCDefGhIJKlmnoPQRSTuvwxyz" \
  chat_id="VOTRE_CHAT_ID"
```

## Etape 5 : Tester l'envoi de message

```bash
$ BOT_TOKEN=$(docker exec vault vault kv get -field=bot_token secret/telegram)
$ CHAT_ID=$(docker exec vault vault kv get -field=chat_id secret/telegram)

$ curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"[OA System] Test de notification -- installation reussie.\"}"
```

Verifiez que le message arrive dans Telegram.

## Etape 6 : Configuration dans OpenClaw

La section `notifications.telegram` dans `~/.openclaw/config.json` (section 12) doit etre :

```json
"notifications": {
  "telegram": {
    "enabled": true,
    "vault_path": "secret/telegram"
  }
}
```

OpenClaw lira automatiquement `bot_token` et `chat_id` depuis Vault.

> **Attention au nom du champ :** Le champ dans Vault doit s'appeler `bot_token` (avec underscore), pas `token` ni `botToken`. Si vous avez stocke le token sous un autre nom, OpenClaw ne le trouvera pas. Verifiez avec : `docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv get secret/telegram`.

## Script utilitaire d'envoi

Creez `~/scripts/notify-telegram.sh` pour envoyer des notifications depuis n'importe quel script :

```bash
#!/bin/bash
# Usage : ./notify-telegram.sh "Votre message ici"

MESSAGE="${1:-Test}"
BOT_TOKEN=$(docker exec vault vault kv get -field=bot_token secret/telegram 2>/dev/null)
CHAT_ID=$(docker exec vault vault kv get -field=chat_id secret/telegram 2>/dev/null)

if [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
  echo "Erreur : impossible de lire les credentials Telegram depuis Vault"
  exit 1
fi

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"${MESSAGE}\", \"parse_mode\": \"Markdown\"}" > /dev/null

echo "Notification envoyee."
```

```bash
$ chmod +x ~/scripts/notify-telegram.sh
$ ~/scripts/notify-telegram.sh "Hello depuis le VPS"
```

## Erreurs courantes

- **"Unauthorized"** : Le token est invalide. Verifiez qu'il est bien copie, sans espaces.
- **"Bad Request: chat not found"** : Vous n'avez pas envoye de message au bot avant d'appeler getUpdates. Le bot ne peut pas initier une conversation.
- **chat_id negatif** : C'est normal pour les groupes. Pour un chat prive, le chat_id est un nombre positif.
- **getUpdates retourne un tableau vide** : Envoyez un message au bot et reessayez immediatement. Les updates expirent apres 24h.

## Verification

```bash
$ ~/scripts/notify-telegram.sh "[OA] Verification Telegram OK"
```

Resultat attendu : message recu dans Telegram.

## Temps estime

10 minutes.
