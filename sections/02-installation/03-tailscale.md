---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.3 -- Reseau prive Tailscale

## Contexte

Tailscale cree un reseau prive (VPN mesh) entre vos machines. Chaque machine recoit une IP privee (en 100.x.x.x). Le principe fondamental : **aucun service n'est expose sur l'IP publique du VPS**. Vault, PostgreSQL, OpenClaw -- tout passe par Tailscale.

Avantages :
- Zero configuration reseau complexe
- Chiffrement de bout en bout (WireGuard)
- Fonctionne meme derriere un NAT
- Gratuit jusqu'a 100 machines

## Etape 1 : Installer Tailscale sur le VPS

```bash
$ curl -fsSL https://tailscale.com/install.sh | sh
```

## Etape 2 : Demarrer et authentifier

```bash
$ sudo tailscale up
```

Cette commande affiche un lien d'authentification. Ouvrez ce lien dans votre navigateur et connectez-vous avec votre compte Tailscale.

## Etape 3 : Obtenir l'IP Tailscale

```bash
$ tailscale ip -4
```

Notez cette IP (format 100.x.x.x). C'est l'adresse que vous utiliserez pour tous les services.

## Etape 4 : Verifier la connexion

```bash
$ tailscale status
```

Vous devez voir votre VPS dans la liste des machines connectees.

## Etape 5 : Installer Tailscale sur votre machine locale

Installez Tailscale sur votre poste de travail egalement :
- **Mac** : `brew install tailscale` ou depuis le Mac App Store
- **Linux** : `curl -fsSL https://tailscale.com/install.sh | sh`
- **Windows** : Telechargez depuis tailscale.com

Puis `tailscale up` et authentifiez.

## Etape 6 : Tester la connectivite

Depuis votre machine locale :

```bash
$ ping VOTRE_IP_TAILSCALE_VPS
$ ssh deploy@VOTRE_IP_TAILSCALE_VPS
```

A partir de maintenant, utilisez toujours l'IP Tailscale pour vous connecter au VPS, pas l'IP publique.

## Etape 7 (optionnel) : Desactiver SSH sur l'IP publique

Si vous etes confiant que Tailscale fonctionne, vous pouvez restreindre SSH a Tailscale uniquement :

```bash
$ sudo ufw delete allow ssh
$ sudo ufw allow in on tailscale0 to any port 22
```

**IMPORTANT** : Ne faites ceci QUE si vous avez confirme que SSH via Tailscale fonctionne. Gardez la console VNC du fournisseur comme plan de secours.

## Principe d'architecture

A partir de cette etape, la regle est :

```
IP publique : RIEN d'expose (sauf SSH si necessaire)
IP Tailscale : TOUT passe par la
```

PostgreSQL ecoute sur 100.x.x.x:5432, pas sur 0.0.0.0.
Vault ecoute sur 100.x.x.x:8200, pas sur 0.0.0.0.
La gateway OpenClaw ecoute sur 100.x.x.x:3000, pas sur 0.0.0.0.

## Erreurs courantes

- **Oublier d'installer Tailscale sur la machine locale** : Sans Tailscale des deux cotes, pas de reseau prive.
- **Utiliser l'IP publique pour les services** : Tout le point de Tailscale est d'eviter ca. Si un service ecoute sur 0.0.0.0, corrigez pour ecouter sur l'IP Tailscale uniquement.
- **Tailscale qui se deconnecte** : Ajoutez `--ssh` a `tailscale up` pour maintenir la connexion, et activez le demarrage automatique : `sudo systemctl enable tailscaled`.

## Verification

```bash
$ tailscale status
$ tailscale ip -4
$ ping -c 3 $(tailscale ip -4)
```

Resultats attendus :
- Status montre la machine comme "active"
- IP en 100.x.x.x
- Ping repond sans perte

## Temps estime

10 minutes.
