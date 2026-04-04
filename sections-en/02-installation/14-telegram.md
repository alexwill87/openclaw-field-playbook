---
---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.14 -- Telegram Connection

## Context

Telegram serves as a notification and command channel for OpenClaw. The system sends alerts (failed health checks, deployment completion, critical errors) and can receive simple commands via the bot.

## Step 1: Create the bot with @BotFather

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Give it a name: `OA System Bot` (or whatever you prefer)
4. Give it a username: `oa_system_bot` (must be unique and end with `bot`)
5. BotFather gives you a token (format: `123456789:ABCDefGhIJKlmnoPQRSTuvwxyz`)

Copy this token.

## Step 2: Store the token in Vault

```bash
$ docker exec vault vault kv put secret/telegram bot_token="123456789:ABCDefGhIJKlmnoPQRSTuvwxyz"
```

## Step 3: Get your chat_id

The chat_id identifies the conversation where the bot will send messages. To find it:

1. Send any message to your bot in Telegram
2. Call the Telegram API:

```bash
$ BOT_TOKEN=$(docker exec vault vault kv get -field=bot_token secret/telegram)
$ curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getUpdates" | python3 -m json.tool
```

3. In the response, look for `"chat": {"id": 123456789}`. This number is your chat_id.

## Step 4: Store the chat_id in Vault

Update the Telegram secret with the chat_id:

```bash
$ docker exec vault vault kv put secret/telegram \
  bot_token="123456789:ABCDefGhIJKlmnoPQRSTuvwxyz" \
  chat_id="YOUR_CHAT_ID"
```

## Step 5: Test message sending

```bash
$ BOT_TOKEN=$(docker exec vault vault kv get -field=bot_token secret/telegram)
$ CHAT_ID=$(docker exec vault vault kv get -field=chat_id secret/telegram)

$ curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"[OA System] Notification test -- installation successful.\"}"
```

Verify that the message arrives in Telegram.

## Step 6: Configuration in OpenClaw

The `notifications.telegram` section in `~/.openclaw/config.json` (section 12) should be:

```json
"notifications": {
  "telegram": {
    "enabled": true,
    "vault_path": "secret/telegram"
  }
}
```

OpenClaw will automatically read `bot_token` and `chat_id` from Vault.

> **Pay attention to the field name:** The field in Vault must be called `bot_token` (with underscore), not `token` or `botToken`. If you stored the token under a different name, OpenClaw won't find it. Verify with: `docker exec -e VAULT_ADDR=http://127.0.0.1:8200 vault vault kv get secret/telegram`.

## Notification sending utility script

Create `~/scripts/notify-telegram.sh` to send notifications from any script:

```bash
#!/bin/bash
# Usage: ./notify-telegram.sh "Your message here"

MESSAGE="${1:-Test}"
BOT_TOKEN=$(docker exec vault vault kv get -field=bot_token secret/telegram 2>/dev/null)
CHAT_ID=$(docker exec vault vault kv get -field=chat_id secret/telegram 2>/dev/null)

if [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
  echo "Error: unable to read Telegram credentials from Vault"
  exit 1
fi

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"${MESSAGE}\", \"parse_mode\": \"Markdown\"}" > /dev/null

echo "Notification sent."
```

```bash
$ chmod +x ~/scripts/notify-telegram.sh
$ ~/scripts/notify-telegram.sh "Hello from the VPS"
```

## Common errors

- **"Unauthorized"**: The token is invalid. Verify that it's copied correctly, without spaces.
- **"Bad Request: chat not found"**: You didn't send a message to the bot before calling getUpdates. The bot cannot initiate a conversation.
- **Negative chat_id**: This is normal for groups. For a private chat, the chat_id is a positive number.
- **getUpdates returns an empty array**: Send a message to the bot and try again immediately. Updates expire after 24 hours.

## Verification

```bash
$ ~/scripts/notify-telegram.sh "[OA] Telegram verification OK"
```

Expected result: message received in Telegram.

## Estimated time

10 minutes.
