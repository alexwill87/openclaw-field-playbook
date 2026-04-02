---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 2.1 -- Prerequis materiel et logiciel

## Contexte

Avant de toucher au serveur, il faut savoir ce qu'on achete, ce qu'on cree comme comptes et combien ca coute. Cette section liste tout ce qui est necessaire AVANT de commencer l'installation.

## Prerequis materiel : le VPS

Configuration minimale testee et validee :

| Ressource | Minimum | Recommande |
|-----------|---------|------------|
| CPU | 4 vCPU | 6 vCPU |
| RAM | 8 Go | 16 Go |
| Stockage | 80 Go SSD | 160 Go NVMe |
| Bande passante | 20 To/mois | Illimite |
| Localisation | Europe (RGPD) | Europe (RGPD) |

Fournisseurs testes :

- **Hetzner** (recommande) : CPX31 a environ 15 EUR/mois. Excellent rapport qualite/prix. Datacenters en Allemagne et Finlande.
- **OVH** : VPS Essential a environ 12 EUR/mois. Datacenters en France. Latence plus faible depuis la France.

## Systeme d'exploitation

**Ubuntu 24.04 LTS** -- c'est la seule version testee dans ce playbook. Les commandes sont ecrites pour Ubuntu/Debian. Si vous utilisez autre chose, adaptez.

## Comptes a creer

Creez ces comptes AVANT de commencer l'installation :

| Service | URL | Pourquoi | Gratuit ? |
|---------|-----|----------|-----------|
| Hetzner ou OVH | hetzner.com / ovh.com | Heberger le VPS | Non |
| Tailscale | tailscale.com | VPN mesh prive | Oui (jusqu'a 100 machines) |
| GitHub | github.com | Depot de code, CI/CD | Oui |
| OpenRouter | openrouter.ai | Acces multi-modeles IA | Credits a l'usage |
| Telegram | telegram.org | Notifications et commandes | Oui |
| HashiCorp Cloud (optionnel) | cloud.hashicorp.com | Backup Vault cloud | Tier gratuit |

## Budget mensuel estime

| Poste | Cout |
|-------|------|
| VPS (Hetzner CPX31) | 15 EUR |
| OpenRouter (usage modere) | 5-20 EUR |
| Nom de domaine (optionnel) | 1 EUR |
| **Total** | **21-36 EUR/mois** |

Le cout OpenRouter depend fortement du modele utilise et du volume de requetes. Claude Sonnet coute environ 3$/M tokens en entree. Haiku est 10x moins cher.

## Logiciels sur votre machine locale

Sur votre poste de travail (pas le VPS), vous aurez besoin de :

- Un terminal SSH (Terminal natif sur Mac/Linux, Windows Terminal + OpenSSH sur Windows)
- Git
- Un editeur de texte (VS Code recommande, avec l'extension Remote-SSH)
- Tailscale installe localement

## Competences attendues

Ce playbook suppose que vous savez :

- Ouvrir un terminal et taper des commandes
- Vous connecter en SSH a un serveur
- Lire un message d'erreur en anglais

Si vous ne savez pas faire ca, commencez par un tutoriel SSH basique avant de continuer.

## Erreurs courantes

- **Prendre un VPS avec 2 Go de RAM** : Vault + PostgreSQL + Node.js + Docker saturent rapidement. 8 Go est le strict minimum.
- **Oublier de creer le compte OpenRouter avant** : L'installation d'OpenClaw demande une cle API des le debut.
- **Choisir un datacenter hors Europe** : Si vos donnees sont europeennes, la localisation du serveur importe (RGPD).

## Verification

Avant de passer a la section suivante, confirmez :

- [ ] VPS commande et accessible (vous avez l'IP et le mot de passe root)
- [ ] Comptes Tailscale, GitHub, OpenRouter crees
- [ ] SSH fonctionne depuis votre poste local vers le VPS
- [ ] Ubuntu 24.04 LTS installe sur le VPS

## Temps estime

15 minutes (hors creation de comptes et commande VPS).
