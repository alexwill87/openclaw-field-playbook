---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.8 -- Mises a jour systeme

## Contexte

Les mises a jour systeme, c'est l'hygiene de base. Ne pas les faire = accumulation de failles de securite. Les faire n'importe comment = casser la production. L'equilibre : regulier, teste, documente.

## Ubuntu

### Mises a jour de securite (hebdomadaire)

```bash
# Voir les mises a jour disponibles
sudo apt update && apt list --upgradable

# Appliquer uniquement les mises a jour de securite
sudo apt upgrade -y --only-upgrade

# Ou pour les securite uniquement
sudo unattended-upgrade --dry-run  # voir ce qui serait fait
sudo unattended-upgrade             # appliquer
```

### Mise a jour majeure (annuelle)

Ubuntu 24.04 LTS -> 26.04 LTS : ne faites PAS ca un vendredi soir.

1. Snapshot Hetzner complet avant.
2. Lire les release notes.
3. Tester sur un VPS de test si possible.
4. `do-release-upgrade` en screen/tmux (pour survivre a une deconnexion SSH).
5. Tester tous les services apres.

### Configurer les mises a jour automatiques

```bash
# Installer
sudo apt install unattended-upgrades

# Configurer : /etc/apt/apt.conf.d/50unattended-upgrades
# Garder uniquement les mises a jour de securite
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};

# Activer les notifications par email (optionnel)
Unattended-Upgrade::Mail "votre@email.com";

# Reboot automatique si necessaire (a 3h du matin)
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "03:00";
```

## Docker

### Images Docker

```bash
# Voir les images et leurs dates
docker images --format "{{.Repository}}:{{.Tag}} {{.CreatedSince}}"

# Pull les dernieres versions
docker compose pull

# Rebuild et redemarrer
docker compose up -d --build

# Nettoyer les anciennes images
docker image prune -a --filter "until=720h"  # > 30 jours
```

### Docker Engine

```bash
# Version actuelle
docker version

# Mise a jour
sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io

# Verifier apres mise a jour
docker version
docker ps  # les containers tournent-ils encore ?
```

Attention : une mise a jour de Docker Engine peut redemarrer le daemon et donc arreter tous les containers. Planifiez une fenetre de maintenance.

## Node.js

### Avec nvm (recommande)

```bash
# Version actuelle
node -v

# Lister les versions disponibles
nvm ls-remote --lts

# Installer une nouvelle version
nvm install 22  # par exemple

# Utiliser la nouvelle version
nvm use 22

# Tester vos applications
cd /opt/cockpit && npm test

# Si tout est OK, definir comme defaut
nvm alias default 22
```

### Avec apt (si pas de nvm)

```bash
# Mettre a jour via NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install nodejs
```

## Vault

```bash
# Version actuelle
vault version

# Mise a jour
# Telecharger la nouvelle version depuis releases.hashicorp.com
wget https://releases.hashicorp.com/vault/X.Y.Z/vault_X.Y.Z_linux_amd64.zip
unzip vault_X.Y.Z_linux_amd64.zip
sudo mv vault /usr/local/bin/vault

# Redemarrer
sudo systemctl restart vault

# Verifier
vault status
vault kv list secret/  # les secrets sont-ils accessibles ?
```

Attention : lisez TOUJOURS les upgrade notes de Vault avant de mettre a jour. Certaines versions ont des breaking changes sur le storage backend.

## Quand NE PAS mettre a jour

Ne mettez pas a jour quand :

1. **Vous etes en production critique.** Un client attend un livrable dans 2 heures. Ce n'est pas le moment.

2. **C'est un vendredi.** La panne du vendredi soir se resout le lundi matin. Ne mettez a jour que du lundi au jeudi.

3. **Vous n'avez pas de backup recent.** Pas de snapshot, pas de pg_dump du jour = pas de mise a jour.

4. **La version est fraiche.** La version X.0.0 vient de sortir. Attendez X.0.1 ou X.0.2. Laissez les autres essuyer les platres.

5. **Plusieurs mises a jour en meme temps.** Ne mettez pas a jour Ubuntu, Docker et Node.js le meme jour. Un changement a la fois.

6. **Vous ne comprenez pas le changelog.** Si les breaking changes ne sont pas clairs, renseignez-vous avant.

## Erreurs courantes

**Ne jamais mettre a jour.** Le serveur tourne sur une version de 2 ans avec des failles connues. La securite est une dette qui s'accumule.

**Tout mettre a jour en meme temps.** Si ca casse, vous ne savez pas quoi.

**Pas de snapshot avant.** La mise a jour casse quelque chose. Pas de rollback possible. 3 heures de debug au lieu de 5 minutes de restauration.

**Mettre a jour sans tester.** `apt upgrade -y` et retour a autre chose. Vous decouvrez le probleme 2 jours plus tard.

## Etapes

1. Planifiez une fenetre de maintenance (mardi ou mercredi, pas vendredi).
2. Faites un snapshot Hetzner et un pg_dump.
3. Mettez a jour un composant a la fois.
4. Testez chaque service apres la mise a jour.
5. Documentez ce qui a ete mis a jour et la date.

## Verification

- [ ] Les mises a jour de securite Ubuntu sont automatiques (unattended-upgrades).
- [ ] Les images Docker sont a jour (moins de 30 jours).
- [ ] Un snapshot existe avant chaque mise a jour majeure.
- [ ] Les mises a jour ne sont jamais faites le vendredi.
- [ ] Chaque mise a jour est suivie d'un test des services.
