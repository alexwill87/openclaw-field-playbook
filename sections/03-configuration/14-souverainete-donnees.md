---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.14 -- Souverainete des donnees

## Contexte

Votre agent manipule vos emails, votre calendrier, vos taches, vos donnees clients. La question n'est pas SI ces donnees sont sensibles, mais OU elles vivent et QUI y a acces.

La souverainete des donnees n'est pas un sujet theorique. C'est une decision d'architecture qui impacte votre conformite legale, la confiance de vos clients, et votre capacite a changer de fournisseur.

## Ou vivent vos donnees

Trois modeles :

### Local

Toutes les donnees restent sur votre machine ou votre serveur.

```
+----------------------------+
|  VOTRE MACHINE / VPS       |
|                            |
|  SOUL.md                   |
|  USER.md                   |
|  CONSTITUTION.md           |
|  MEMORY.md                 |
|  knowledge/                |
|  skills/                   |
|  base de donnees locale    |
|                            |
+----------------------------+
      |
      | API calls (prompts)
      v
+----------------------------+
|  FOURNISSEUR LLM           |
|  (les prompts transitent,  |
|   pas les fichiers)        |
+----------------------------+
```

Avantages :
- Controle total
- Pas de dependance a un service tiers pour le stockage
- Conformite RGPD simplifiee

Inconvenients :
- Maintenance a votre charge (backup, securite, mises a jour)
- Acces limite a votre machine / reseau

### Cloud

Les donnees vivent chez un fournisseur cloud.

Avantages :
- Pas de maintenance infra
- Acces depuis n'importe ou
- Backup automatique

Inconvenients :
- Vos donnees sont chez un tiers
- Dependance au fournisseur (lock-in)
- Conformite RGPD plus complexe (selon la localisation des serveurs)

### Hybride (recommande)

Configuration et memoire en local. Services externes pour ce qui le necessite.

```
+----------------------------+    +---------------------------+
|  LOCAL                     |    |  CLOUD                    |
|                            |    |                           |
|  SOUL.md                   |    |  Calendrier (Google/O365) |
|  USER.md                   |    |  Email (fournisseur)      |
|  CONSTITUTION.md           |    |  CRM (si SaaS)            |
|  MEMORY.md                 |    |                           |
|  knowledge/                |    +---------------------------+
|  skills/                   |
|  vault (secrets)           |
|  logs                      |
|                            |
+----------------------------+
```

La regle : vos fichiers de configuration, votre memoire et vos secrets restent locaux. Les services externes sont accedes via API avec les droits minimaux necessaires.

## RGPD : ce que vous devez savoir

Si vous etes en Europe ou traitez des donnees de residents europeens, le RGPD s'applique.

### Points cles pour votre agent

**Base legale** : Vous devez avoir une base legale pour traiter les donnees via l'agent (interet legitime, consentement, execution d'un contrat).

**Minimisation** : L'agent ne doit acceder qu'aux donnees strictement necessaires. Pas de "on connecte tout au cas ou."

**Localisation** : Privilegiez les fournisseurs dont les serveurs sont en Europe. Si le fournisseur LLM est hors UE, les prompts transitent hors UE -- assurez-vous que les donnees personnelles sont anonymisees dans les prompts.

**Droit a l'effacement** : Si un client demande la suppression de ses donnees, elles doivent aussi disparaitre de knowledge/, MEMORY.md, et de tout fichier de l'agent.

**Registre des traitements** : Documentez quelles donnees l'agent traite, pourquoi, et ou elles sont stockees. Un fichier knowledge/legal/rgpd.md est un bon endroit.

### Checklist RGPD minimale

```markdown
## Registre des traitements -- Agent OpenClaw

| Donnee | Finalite | Base legale | Stockage | Duree |
|--------|----------|-------------|----------|-------|
| Emails clients | Triage et brouillons | Interet legitime | Local (48h cache) | 48h |
| Calendrier | Briefing quotidien | Interet legitime | API (pas de copie) | Session |
| Contacts clients | Contexte relation | Execution contrat | knowledge/ | Duree contrat |
| Notes de reunion | Memoire agent | Interet legitime | MEMORY.md | 2 semaines |
```

## Hebergement europeen recommande

Pour le VPS ou serveur local :
- OVH (France)
- Hetzner (Allemagne)
- Scaleway (France)
- Infomaniak (Suisse)

Pour les services cloud :
- Privilegiez les options avec datacenters en UE
- Verifiez les conditions de transfert hors UE
- Lisez les DPA (Data Processing Agreements)

## Etape par etape

1. Cartographiez ou vivent vos donnees aujourd'hui
2. Decidez du modele (local / cloud / hybride)
3. Assurez-vous que les fichiers de configuration sont en local
4. Stockez les secrets dans un vault, jamais en clair
5. Si RGPD applicable : creez le registre des traitements
6. Choisissez un hebergement europeen si possible
7. Documentez vos choix dans knowledge/legal/ ou knowledge/infra/

## Erreurs courantes

**Ignorer la question** : "Ce n'est qu'un agent, pas un service public." Votre agent traite potentiellement des donnees personnelles de vos clients. Le RGPD s'applique.

**Secrets en clair dans les fichiers** : Un token API dans SOUL.md ou dans un skill. Utilisez un vault.

**Pas de backup** : Votre configuration et knowledge/ representent des semaines de travail. Sauvegardez-les.

**Tout en cloud sans reflexion** : Pratique, mais vos donnees sont chez un tiers. Assurez-vous de comprendre les implications.

**Oublier le droit a l'effacement** : Un client demande la suppression de ses donnees. Vous les supprimez du CRM mais elles restent dans knowledge/clients/client-x.md et dans MEMORY.md.

## Verification

- [ ] Vous savez ou vivent chacune de vos donnees
- [ ] Les fichiers de configuration sont en local
- [ ] Les secrets sont dans un vault
- [ ] Si RGPD applicable : registre des traitements cree
- [ ] Hebergement europeen choisi (ou justification documentee si non)
- [ ] Procedure de suppression des donnees documentee
- [ ] Backup en place pour la configuration et knowledge/
