---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit, claude-aurel]
lang: fr
---

# 3.18 -- Connecter deux installations OpenClaw (mode remote)

> Vous avez deux VPS avec OpenClaw, ou vous gerez l'installation d'un client. Voici comment les connecter pour surveiller, debugger ou collaborer a distance.

**Pour qui :** integrateur, equipe multi-sites, ou agent qui supervise un autre agent
**Prerequis :** deux installations OpenClaw fonctionnelles, idealement sur le meme reseau Tailscale
**Difficulte :** Intermediaire

---

## Contexte

OpenClaw supporte un mode `gateway.mode: "remote"` qui permet a un client de se connecter a une gateway distante via WebSocket. C'est une architecture client-serveur, pas une federation : un VPS est le maitre (il heberge la gateway), l'autre est le client (il se connecte a distance).

### Quand connecter deux installations

| Cas d'usage | Exemple |
|------------|---------|
| **Apprentissage** | Observer comment un agent plus mature fonctionne sur un autre VPS |
| **Debugging** | Diagnostiquer un probleme a distance sans se connecter en SSH |
| **Supervision** | Un VPS central surveille la sante de plusieurs installations |
| **Collaboration inter-agents** | Deux agents sur deux VPS separes partagent un canal de communication |

---

## Architecture

```
VPS A (gateway maitre)              VPS B (client remote)
   gateway.mode: "server"              gateway.mode: "remote"
   port 18789 (WebSocket)              gateway.remote.url
          ^                                    |
          |_________ Tailscale / SSH __________|
```

Le client remote ne lance PAS sa propre gateway. Il se connecte a la gateway du maitre et utilise ses commandes CLI a distance.

---

## Etapes

### 1. Cote gateway maitre (VPS A)

Creez un token d'authentification dedie pour la connexion remote. Ne reutilisez **jamais** le root token.

```bash
# Generer un token dedie
openclaw gateway token create --name "remote-vps-b" --scope read
```

Notez le token genere. Verifiez que la gateway ecoute sur le bon port :

```bash
# Verifier la configuration
cat ~/.openclaw/gateway.json
```

La configuration doit inclure :

```json
{
  "mode": "server",
  "port": 18789,
  "auth": {
    "tokens": [
      {
        "name": "remote-vps-b",
        "token": "ocgw_xxxxxxxxxxxxxxxxxx",
        "scope": "read"
      }
    ]
  }
}
```

### 2. Configuration du transport

Trois options, de la plus simple a la plus complexe :

#### Option A : Tailscale direct (recommande)

Si les deux VPS sont sur le meme reseau Tailscale, c'est le plus simple. Le trafic est deja chiffre point-a-point.

```bash
# Sur VPS B, verifier la connectivite
tailscale ping vps-a
```

L'URL remote sera : `ws://100.x.x.x:18789` (IP Tailscale du VPS A).

#### Option B : Tunnel SSH

Si vous n'avez pas Tailscale, un tunnel SSH fait le travail :

```bash
# Sur VPS B, creer le tunnel
ssh -N -L 18789:localhost:18789 user@vps-a-ip
```

L'URL remote sera : `ws://localhost:18789`.

Pour rendre le tunnel persistant, ajoutez-le dans un service systemd ou utilisez `autossh` :

```bash
# Installation d'autossh
sudo apt install autossh

# Tunnel persistant
autossh -M 0 -N -L 18789:localhost:18789 user@vps-a-ip \
  -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3"
```

#### Option C : WebSocket sur Internet (avance)

Si vous devez passer par Internet sans tunnel, utilisez **obligatoirement** TLS :

```bash
# Derriere un reverse proxy (Caddy, Nginx) avec certificat TLS
# L'URL sera : wss://gateway.votre-domaine.com
```

Ne jamais exposer `ws://` sur une IP publique sans TLS.

### 3. Cote client remote (VPS B)

Configurez le client pour se connecter a la gateway distante :

```bash
# Editer la configuration
nano ~/.openclaw/gateway.json
```

```json
{
  "mode": "remote",
  "remote": {
    "url": "ws://100.x.x.x:18789",
    "token": "ocgw_xxxxxxxxxxxxxxxxxx"
  }
}
```

Remplacez l'URL et le token par les valeurs de votre installation.

### 4. Verification

```bash
# Sur VPS B -- tester la connexion
openclaw gateway status

# Doit afficher : Connected to remote gateway at ws://100.x.x.x:18789

# Verifier la sante de l'installation distante
openclaw health

# Voir le statut detaille
openclaw status --deep
```

---

## Securite

| Regle | Pourquoi |
|-------|----------|
| **Token dedie** (pas le root token) | Limiter les degats en cas de fuite |
| **Scope `read` par defaut** | Le client observe mais ne modifie pas |
| **Tailscale ou tunnel SSH** | Chiffrement du transport obligatoire |
| **Jamais de `ws://` sur IP publique** | WebSocket en clair = credentials en clair |
| **Rotation du token reguliere** | Bonne pratique, surtout pour les installations client |

---

## Erreurs courantes

| Erreur | Cause | Solution |
|--------|-------|----------|
| `Connection refused` | La gateway maitre n'ecoute pas sur le bon port ou IP | Verifier `gateway.json` cote maitre et la connectivite reseau |
| `Authentication failed` | Token incorrect ou expire | Regenerer le token cote maitre, mettre a jour cote client |
| `ws:// blocked on non-loopback` | OpenClaw refuse les WebSocket non-TLS vers une IP distante | Utiliser Tailscale (considere loopback) ou un tunnel SSH |
| Le client lance sa propre gateway | `mode` est encore sur `server` au lieu de `remote` | Verifier `gateway.json` cote client : `"mode": "remote"` |
| `gateway.auth` vs `gateway.remote` | Confusion entre la config serveur et la config client | `auth` = cote maitre (qui recoit), `remote` = cote client (qui se connecte) |

---

## Template reutilisable

### Configuration maitre (VPS A)

```json
{
  "mode": "server",
  "port": 18789,
  "auth": {
    "tokens": [
      {
        "name": "remote-vps-b",
        "token": "REMPLACER_PAR_VOTRE_TOKEN",
        "scope": "read"
      }
    ]
  }
}
```

### Configuration client (VPS B)

```json
{
  "mode": "remote",
  "remote": {
    "url": "ws://TAILSCALE_IP_VPS_A:18789",
    "token": "REMPLACER_PAR_VOTRE_TOKEN"
  }
}
```

### Commande tunnel SSH (si pas Tailscale)

```bash
autossh -M 0 -N -L 18789:localhost:18789 user@VPS_A_IP \
  -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3"
```

### Commandes de verification

```bash
# Depuis VPS B
openclaw gateway status         # Etat de la connexion
openclaw health                 # Sante de l'installation distante
openclaw status --deep          # Statut detaille
```

---

## Verification

- [ ] Le token dedie est cree sur le VPS maitre (pas le root token)
- [ ] Le transport est chiffre (Tailscale, SSH tunnel, ou TLS)
- [ ] `openclaw gateway status` affiche "Connected" sur le client
- [ ] `openclaw health` renvoie un resultat depuis le client
- [ ] Le `ws://` n'est PAS expose sur une IP publique

---

*Cette section a ete redigee suite a l'experience de connexion entre VPS-Omar et VPS-Aurel (Pantheos). Issue [#31](https://github.com/alexwill87/openclaw-field-playbook/issues/31).*
