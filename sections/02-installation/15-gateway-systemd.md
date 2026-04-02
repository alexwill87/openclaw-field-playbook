---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.15 -- Gateway systemd

## Contexte

La gateway OpenClaw est le point d'entree HTTP du systeme. Elle doit tourner en permanence, redemarrer automatiquement en cas de crash et demarrer au boot du serveur. systemd est le gestionnaire de services standard de Linux -- c'est lui qui gere ca.

## Etape 1 : Creer le fichier de service

Creez `/etc/systemd/system/openclaw-gateway.service` :

```bash
$ sudo nano /etc/systemd/system/openclaw-gateway.service
```

Contenu :

```ini
[Unit]
Description=OpenClaw Gateway
Documentation=https://github.com/alexwill87/openclawfieldplaybook
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=deploy
Group=deploy
WorkingDirectory=/home/deploy
Environment=NODE_ENV=production
Environment=VAULT_ADDR=http://127.0.0.1:8200
Environment=VAULT_TOKEN=VOTRE_TOKEN_APPLICATIF_ICI

ExecStart=/home/deploy/.nvm/versions/node/v22.14.0/bin/node /home/deploy/.nvm/versions/node/v22.14.0/bin/openclaw gateway start
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -TERM $MAINPID

Restart=always
RestartSec=10
StartLimitIntervalSec=300
StartLimitBurst=5

StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw-gateway

# Securite
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/home/deploy

[Install]
WantedBy=multi-user.target
```

**IMPORTANT** : Adaptez les chemins selon votre installation :
- Remplacez `v22.14.0` par votre version Node.js exacte (`node --version`)
- Remplacez `VOTRE_TOKEN_APPLICATIF_ICI` par le token Vault cree en section 07
- Remplacez `deploy` par votre nom d'utilisateur si different

Pour trouver le chemin exact de node et openclaw :

```bash
$ which node
$ which openclaw
```

## Etape 2 : Activer et demarrer le service

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl enable openclaw-gateway
$ sudo systemctl start openclaw-gateway
```

## Etape 3 : Verifier le status

```bash
$ sudo systemctl status openclaw-gateway
```

Resultat attendu :

```
openclaw-gateway.service - OpenClaw Gateway
     Loaded: loaded (/etc/systemd/system/openclaw-gateway.service; enabled)
     Active: active (running) since ...
```

## Etape 4 : Consulter les logs

Logs en temps reel :

```bash
$ journalctl -u openclaw-gateway -f
```

Logs depuis le dernier demarrage :

```bash
$ journalctl -u openclaw-gateway -b
```

Logs des dernieres 100 lignes :

```bash
$ journalctl -u openclaw-gateway -n 100 --no-pager
```

## Etape 5 : Commandes de gestion courantes

| Action | Commande |
|--------|----------|
| Demarrer | `sudo systemctl start openclaw-gateway` |
| Arreter | `sudo systemctl stop openclaw-gateway` |
| Redemarrer | `sudo systemctl restart openclaw-gateway` |
| Recharger config | `sudo systemctl reload openclaw-gateway` |
| Status | `sudo systemctl status openclaw-gateway` |
| Desactiver au boot | `sudo systemctl disable openclaw-gateway` |
| Voir les logs | `journalctl -u openclaw-gateway -f` |

## Comportement de redemarrage automatique

La configuration prevoit :
- `Restart=always` : redemarre apres tout arret (crash, kill, etc.)
- `RestartSec=10` : attend 10 secondes avant de redemarrer
- `StartLimitBurst=5` et `StartLimitIntervalSec=300` : maximum 5 redemarrages en 5 minutes. Au-dela, systemd considere le service comme defaillant et arrete les tentatives.

Pour reinitialiser le compteur de tentatives :

```bash
$ sudo systemctl reset-failed openclaw-gateway
$ sudo systemctl start openclaw-gateway
```

## Erreurs courantes

- **"openclaw: command not found"** dans les logs : systemd ne charge pas `.bashrc`. Il faut utiliser le chemin ABSOLU vers node et openclaw. Pas de `nvm`, pas de `~`.
- **Permission denied** : L'utilisateur dans le fichier service n'a pas acces au dossier. Verifiez `User=` et `ReadWritePaths=`.
- **Service qui boucle (restart loop)** : Verifiez les logs (`journalctl`). Souvent un probleme de token Vault ou de connexion base de donnees.
- **"Start request repeated too quickly"** : Le service a crashe 5 fois en 5 minutes. Corrigez le probleme sous-jacent, puis `systemctl reset-failed`.

## Verification

```bash
$ sudo systemctl status openclaw-gateway
$ curl -s http://127.0.0.1:3000/health
$ journalctl -u openclaw-gateway -n 10 --no-pager
```

Resultats attendus :
- Status : active (running)
- Health endpoint retourne une reponse 200
- Pas d'erreur dans les 10 dernieres lignes de log

## Temps estime

10 minutes.
