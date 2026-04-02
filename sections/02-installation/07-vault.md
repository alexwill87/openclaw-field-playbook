---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.7 -- HashiCorp Vault

## Contexte

C'est la section la plus importante de tout le chapitre. Vault centralise TOUS les secrets : cles API, mots de passe base de donnees, tokens Telegram, etc.

**Pourquoi Vault et pas des fichiers .env ?**

| Critere | Fichiers .env | Vault |
|---------|---------------|-------|
| Versionnement | Risque de commit accidentel | Secrets jamais dans git |
| Rotation | Manuelle, oubliee | Programmable, automatisee |
| Audit | Aucun | Log de chaque acces |
| Acces granulaire | Tout ou rien | Politiques fines par chemin |
| Chiffrement au repos | Non | Oui (AES-256-GCM) |
| Multi-service | Copier le .env partout | API centralisee |

En resume : les fichiers .env sont une dette technique. Vault est un investissement.

## Etape 1 : Creer le fichier Docker Compose

```bash
$ mkdir -p ~/docker/vault/config
$ mkdir -p ~/docker/vault/data
```

Creez le fichier `~/docker/vault/docker-compose.yml` :

```yaml
version: "3.8"

services:
  vault:
    image: hashicorp/vault:1.17
    container_name: vault
    restart: unless-stopped
    ports:
      - "127.0.0.1:8200:8200"
    environment:
      VAULT_ADDR: "http://127.0.0.1:8200"
    cap_add:
      - IPC_LOCK
    volumes:
      - ./config:/vault/config:ro
      - ./data:/vault/data
    command: server -config=/vault/config/vault.hcl
    networks:
      - vault-net

networks:
  vault-net:
    driver: bridge
```

**IMPORTANT** : Le port est lie a `127.0.0.1`, pas a `0.0.0.0`. Vault n'est accessible que localement (et via Tailscale si configure).

## Etape 2 : Creer la configuration Vault

Creez le fichier `~/docker/vault/config/vault.hcl` :

```hcl
storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

api_addr = "http://127.0.0.1:8200"

ui = true

disable_mlock = true
```

Notes :
- `tls_disable = 1` : Acceptable car Vault est derriere Tailscale (chiffrement WireGuard). En production publique, activez TLS.
- `disable_mlock = true` : Necessaire dans Docker sans privileges supplementaires.
- `ui = true` : Interface web accessible sur http://127.0.0.1:8200/ui.

## Etape 3 : Mode dev vs production

| Mode | Utilisation | Persistance | Securite |
|------|------------|-------------|----------|
| Dev (`vault server -dev`) | Tests locaux | Non (memoire) | Token root connu |
| Production (ce qu'on fait ici) | VPS | Oui (fichier/consul) | Initialisation securisee |

Ce playbook utilise le **mode production**. Ne pas utiliser le mode dev sur un VPS.

## Etape 4 : Demarrer Vault

```bash
$ cd ~/docker/vault
$ docker compose up -d
```

Verifiez que le conteneur tourne :

```bash
$ docker ps | grep vault
```

## Etape 5 : Initialiser Vault

L'initialisation ne se fait qu'UNE SEULE FOIS. Elle genere les cles de dechiffrement (unseal keys) et le token root.

```bash
$ export VAULT_ADDR='http://127.0.0.1:8200'
$ docker exec vault vault operator init -key-shares=5 -key-threshold=3
```

Resultat : 5 unseal keys et 1 root token. Exemple de sortie :

```
Unseal Key 1: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Unseal Key 2: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Unseal Key 3: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Unseal Key 4: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Unseal Key 5: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Initial Root Token: hvs.XXXXXXXXXXXXXXXXXXXXXXXX
```

**SAUVEGARDEZ CES INFORMATIONS IMMEDIATEMENT.**

## Etape 6 : Sauvegarder les unseal keys HORS du VPS

Les unseal keys doivent etre stockees **en dehors du VPS**. Si quelqu'un compromet le VPS et possede les unseal keys, il peut dechiffrer tous les secrets.

Methode recommandee :
1. Copiez chaque cle dans un gestionnaire de mots de passe (1Password, Bitwarden, KeePass)
2. Distribuez les cles : 2 pour vous, 2 pour un co-admin, 1 dans un coffre physique
3. Le threshold est 3 : il faut 3 cles sur 5 pour dechiffrer. Aucune personne seule ne peut tout ouvrir.

**NE STOCKEZ PAS les unseal keys dans un fichier sur le VPS.**

## Etape 7 : Unseal (dechiffrer) Vault

Apres chaque redemarrage, Vault demarre en etat "sealed" (chiffre). Il faut 3 cles pour l'ouvrir :

```bash
$ docker exec vault vault operator unseal CLE_1_ICI
$ docker exec vault vault operator unseal CLE_2_ICI
$ docker exec vault vault operator unseal CLE_3_ICI
```

Verifiez l'etat :

```bash
$ docker exec vault vault status
```

Resultat attendu : `Sealed: false`

## Etape 8 : Se connecter avec le token root

```bash
$ docker exec vault vault login TOKEN_ROOT_ICI
```

Ou via variable d'environnement (plus pratique pour les scripts) :

```bash
$ export VAULT_TOKEN='TOKEN_ROOT_ICI'
```

## Etape 9 : Activer le moteur de secrets KV v2

KV (Key-Value) v2 permet le versionnement des secrets :

```bash
$ docker exec vault vault secrets enable -path=secret kv-v2
```

Verifiez :

```bash
$ docker exec vault vault secrets list
```

Vous devez voir `secret/` dans la liste.

## Etape 10 : Stocker les premiers secrets

Stockez vos secrets par categorie. Chaque commande cree ou met a jour un secret :

**Cle API OpenRouter :**

```bash
$ docker exec vault vault kv put secret/openrouter api_key="sk-or-VOTRE_CLE_ICI"
```

**Token Telegram :**

```bash
$ docker exec vault vault kv put secret/telegram bot_token="123456:ABC-DEF..." chat_id="VOTRE_CHAT_ID"
```

**Token GitHub :**

```bash
$ docker exec vault vault kv put secret/github token="ghp_VOTRE_TOKEN_ICI"
```

**Credentials base de donnees :**

```bash
$ docker exec vault vault kv put secret/database \
  host="127.0.0.1" \
  port="5432" \
  name="oa_system" \
  user="oa_admin" \
  password="MOT_DE_PASSE_FORT_ICI"
```

**Secret cockpit :**

```bash
$ docker exec vault vault kv put secret/cockpit \
  jwt_secret="GENERER_AVEC_openssl_rand_hex_32" \
  admin_password="MOT_DE_PASSE_ADMIN"
```

## Etape 11 : Lire un secret (verification)

```bash
$ docker exec vault vault kv get secret/openrouter
```

Resultat attendu : les champs `api_key` avec la valeur stockee.

## Etape 12 : Creer un token applicatif (pas le root token)

N'utilisez PAS le root token dans vos applications. Creez un token dedie :

```bash
$ docker exec vault vault token create \
  -display-name="openclaw-app" \
  -ttl=720h \
  -renewable=true \
  -policy=default
```

Notez le token genere. C'est celui que vous utiliserez dans la configuration OpenClaw.

## Etape 13 : Unseal apres redemarrage

Apres chaque redemarrage du VPS, Vault demarre en mode sealed. Vous devez l'unseal manuellement :

```bash
$ docker exec vault vault operator unseal
# Entrez la cle 1 quand demande
$ docker exec vault vault operator unseal
# Entrez la cle 2
$ docker exec vault vault operator unseal
# Entrez la cle 3
```

> **SECURITE : Ne jamais stocker les unseal keys dans un fichier sur le serveur.** Pas de script `vault-unseal.sh` avec les cles en clair. Les unseal keys doivent etre conservees hors du VPS (gestionnaire de mots de passe, coffre physique, ou KMS cloud). Un agent IA qui a acces aux unseal keys peut compromettre l'ensemble du systeme.

Pour les environnements de production, envisagez Vault auto-unseal avec un KMS cloud (AWS KMS, GCP Cloud KMS). C'est plus complexe a configurer mais elimine le besoin d'unseal manuel.

**IMPORTANT** : Ce script contient des unseal keys en clair. C'est un compromis entre securite et praticite. En environnement critique, preferez l'unseal manuel ou Vault auto-unseal avec un KMS cloud.

## Erreurs courantes

- **"server is not yet initialized"** : Vous n'avez pas fait l'etape 5 (init). L'initialisation ne se fait qu'une fois.
- **"Vault is sealed"** : Apres un redemarrage du conteneur ou du VPS, Vault est toujours sealed. Il faut unseal avec 3 cles.
- **Perdre les unseal keys** : Si vous perdez 3+ cles, vos secrets sont irrecuperables. Sauvegardez-les.
- **Utiliser le root token en production** : Le root token est tout-puissant. Creez des tokens dedies avec des politiques restreintes.
- **Vault qui crash au demarrage** : Verifiez les permissions sur `~/docker/vault/data/`. Le dossier doit appartenir a votre utilisateur.

## Verification

```bash
$ docker exec vault vault status
$ docker exec vault vault kv list secret/
$ docker exec vault vault kv get secret/openrouter
```

Resultats attendus :
- Status : Sealed = false, Initialized = true
- Liste des secrets : openrouter, telegram, github, database, cockpit
- Lecture d'un secret : valeur affichee correctement

## Temps estime

30 minutes (plus le temps de generer et sauvegarder les secrets).
