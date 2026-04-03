---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit, claude-aurel]
lang: fr
---

# Adapter le playbook a un VPS existant

> Vous avez deja un serveur avec des services qui tournent. Cette section vous aide a diagnostiquer ce qui est deja en place et a adapter votre parcours.

---

## Diagnostic de l'existant

Copiez et executez ces commandes pour obtenir un etat des lieux rapide :

```bash
# Docker
docker --version

# Docker Compose
docker compose version

# Node.js (et methode d'installation)
node --version
command -v nvm && echo "installe via nvm" || echo "installation globale"

# Tailscale
tailscale status

# PostgreSQL (conteneur ou natif)
docker ps | grep postgres
psql --version

# Vault
vault status
docker ps | grep vault

# nginx
nginx -v

# Ports deja occupes par les services du playbook
ss -ltnp | grep -E ':(3007|5432|8065|8200|18789)'

# Services systemd OpenClaw existants
systemctl --user list-units --all | grep openclaw
sudo systemctl list-units --all | grep openclaw
```

Notez les resultats. Ils determinent quelles sections vous pouvez sauter et lesquelles vous devez adapter.

---

## Tableau de correspondance

Pour chaque composant existant, voici l'action a suivre :

| Composant | Deja installe ? | Action |
|-----------|-----------------|--------|
| Docker + Compose | Oui | Sautez section 2.4. Verifiez la version (>= 24). |
| Node.js (nvm) | Oui | Sautez section 2.5. Notez si c'est nvm ou global (impact section 2.15). |
| Node.js (global/apt) | Oui | Sautez section 2.5. Le wrapper systemd sera different (pas de nvm.sh). |
| Tailscale | Oui | Sautez section 2.3. Notez votre IP Tailscale. |
| PostgreSQL | Oui | Adaptez section 2.8 : creez une nouvelle base `oa_system` sans toucher a l'existant. |
| Vault | Oui | Sautez section 2.7 mais suivez l'etape "Stocker les secrets" (ajoutez les secrets OpenClaw). |
| nginx | Oui | Le playbook n'utilise pas nginx par defaut. Si vous voulez proxifier, voir la note ci-dessous. |

---

## Conflits de ports

Tableau des ports utilises par le playbook et comment reagir si ils sont deja pris :

| Port | Service | Si deja pris |
|------|---------|-------------|
| 5432 | PostgreSQL | Utilisez un port alternatif (ex: 5433) et adaptez les commandes |
| 8200 | Vault | Changez dans le docker-compose.yml de Vault |
| 8065 | Mattermost | Changez dans le docker-compose.yml de Mattermost |
| 18789 | OpenClaw Gateway | Changez dans la config OpenClaw |
| 3007 | Install Tracker | Changez dans docker-compose.yml du tracker |

---

## Services systemd existants (CRITIQUE)

Si vous avez deja eu une installation OpenClaw sur ce VPS, verifiez imperativement :

```bash
# Services systeme
sudo systemctl list-units --all | grep -i openclaw
sudo systemctl list-units --all | grep -i claw

# Services utilisateur
systemctl --user list-units --all | grep -i openclaw

# Si trouve, desactivez AVANT de continuer :
sudo systemctl stop openclaw-gateway
sudo systemctl disable openclaw-gateway
systemctl --user stop openclaw-gateway
systemctl --user disable openclaw-gateway
```

> **IMPORTANT** : ne pas desactiver les anciens services systemd avant de reinstaller est une source de bugs silencieux. Le nouveau service demarre, l'ancien aussi, et les deux se battent pour le meme port. (Reference : issue #30 -- ce probleme a coute 45 minutes de debug a Claude-Aurel.)

---

## Note sur nginx

Si vous utilisez deja nginx comme reverse proxy, vous pouvez proxifier le gateway OpenClaw :

```nginx
server {
    server_name openclaw.votre-domaine.com;
    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Verification

Apres avoir diagnostique et adapte, reprenez le playbook a la section qui correspond a votre premier composant manquant.

**Erreurs courantes :**
- Ne pas verifier les anciens services systemd
- Conflits de ports non detectes
- Version Docker trop ancienne (< 24)

---

[Contribuer a ce chapitre](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)
