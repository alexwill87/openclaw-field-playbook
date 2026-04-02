---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.16 -- Verification post-installation

## Contexte

Toutes les briques sont en place. Avant de passer au chapitre suivant, on verifie TOUT d'un coup. Si un point est rouge, le diagnostic par symptome vous dira quoi faire.

## Checklist des 10 points

Executez chaque commande. Tout doit reussir.

### 1. Docker fonctionne

```bash
$ docker ps
```

Attendu : au moins 2 conteneurs (vault, postgres) en etat "Up".

### 2. Vault est unseal et accessible

```bash
$ docker exec vault vault status | grep Sealed
```

Attendu : `Sealed          false`

### 3. Les secrets sont lisibles

```bash
$ docker exec vault vault kv get secret/openrouter
$ docker exec vault vault kv get secret/telegram
$ docker exec vault vault kv get secret/database
```

Attendu : chaque commande retourne les champs stockes.

### 4. PostgreSQL repond

```bash
$ docker exec postgres psql -U oa_admin -d oa_system -c "SELECT 'pg_ok';"
```

Attendu : `pg_ok`

### 5. Tailscale est connecte

```bash
$ tailscale status
```

Attendu : votre machine apparait comme connectee.

### 6. Node.js est la bonne version

```bash
$ node --version
```

Attendu : v22.x ou superieur.

### 7. OpenClaw est installe

```bash
$ openclaw --version
```

Attendu : numero de version affiche.

### 8. La gateway tourne

```bash
$ sudo systemctl status openclaw-gateway | grep Active
```

Attendu : `active (running)`

### 9. Le health check passe

```bash
$ ~/scripts/health-check.sh
```

Attendu : 0 echec.

### 10. openclaw doctor

```bash
$ openclaw doctor
```

Attendu : tous les checks verts.

## Script de verification rapide

Pour tout verifier en une commande :

```bash
$ check() { echo -n "$1: "; if eval "$2" > /dev/null 2>&1; then echo "OK"; else echo "ECHEC"; fi; }
$ echo "=== VERIFICATION COMPLETE ==="
$ check "1. Docker"      "docker ps"
$ check "2. Vault unseal" "docker exec vault vault status 2>/dev/null | grep 'Sealed.*false'"
$ check "3. Vault secret" "docker exec vault vault kv get -field=api_key secret/openrouter"
$ check "4. PostgreSQL"   "docker exec postgres psql -U oa_admin -d oa_system -c 'SELECT 1;'"
$ check "5. Tailscale"    "tailscale status"
$ echo -n "6. Node: "    && node --version
$ check "7. OpenClaw"     "openclaw --version"
$ check "8. Gateway"      "sudo systemctl is-active openclaw-gateway"
$ echo "=== FIN ==="
```

## Diagnostic par symptome

Si un point echoue, voici quoi faire :

| Point | Symptome | Diagnostic |
|-------|----------|------------|
| 1 | Docker ps erreur | `sudo systemctl start docker`. Si erreur persistante : `journalctl -u docker -n 50`. |
| 2 | Vault sealed | Normal apres redemarrage. Unseal avec 3 cles (section 07, etape 7). |
| 3 | Secret illisible | Token expire ? `docker exec vault vault token lookup`. Recreez si necessaire. |
| 4 | PostgreSQL ne repond pas | `docker logs postgres` pour voir l'erreur. Souvent un probleme de permissions sur `data/`. |
| 5 | Tailscale deconnecte | `sudo tailscale up`. Si erreur : `sudo systemctl restart tailscaled`. |
| 6 | Node version trop vieille | `nvm install --lts && nvm alias default lts/*`. |
| 7 | OpenClaw pas installe | `npm install -g @anthropic-ai/claude-code`. Verifiez le PATH nvm. |
| 8 | Gateway inactive | `journalctl -u openclaw-gateway -n 50`. Souvent un chemin incorrect dans le fichier service. |
| 9 | Health check echoue | Le script indique quel point echoue. Corrigez ce point specifique. |
| 10 | Doctor echoue | Suivez les instructions affichees par `openclaw doctor`. |

## Si tout est vert

Felicitations. Votre infrastructure est operationnelle. Passez aux sections suivantes (17, 18, 19) pour finaliser le workflow de developpement, puis au chapitre 3.

## Si un point reste rouge

Ne passez pas au chapitre suivant avec un point rouge. Chaque brique depend des precedentes. Un probleme non resolu ici deviendra un probleme plus gros plus tard.

## Temps estime

10 minutes (verification seule, sans correction).
