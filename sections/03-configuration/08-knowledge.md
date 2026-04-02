---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.8 -- Le dossier knowledge/

## Contexte

knowledge/ est la memoire froide de l'agent. Le savoir qui ne change pas chaque semaine. Les references, les processus, les informations metier durables.

Contrairement a MEMORY.md (80 lignes, volatile), knowledge/ n'a pas de limite de taille globale. Mais chaque fichier doit rester lisible et cible : un fichier par sujet, 200 lignes max par fichier.

## Organisation par domaine

Structure recommandee :

```
knowledge/
  infra/
    stack-technique.md
    deploiement.md
    monitoring.md
  business/
    clients-principaux.md
    tarification.md
    processus-vente.md
  guides/
    onboarding-nouveau-client.md
    procedure-incident.md
    checklist-livraison.md
  contacts/
    equipe.md
    partenaires.md
```

Trois a quatre dossiers de premier niveau. Pas plus. Si vous avez besoin de plus, vous essayez probablement de documenter trop de choses.

## Regles d'organisation

### Un fichier par sujet

Mauvais :
```
knowledge/tout-sur-le-business.md  (300 lignes, 15 sujets)
```

Bon :
```
knowledge/business/tarification.md     (60 lignes)
knowledge/business/clients-principaux.md  (80 lignes)
knowledge/business/processus-vente.md     (70 lignes)
```

### Cross-reference plutot que duplication

Si le processus de deploiement mentionne le monitoring, ne recopiez pas la section monitoring. Faites une reference :

```markdown
## Deploiement
[...]
Pour le monitoring post-deploiement, voir [monitoring.md](../infra/monitoring.md).
```

La duplication cree des informations contradictoires des la premiere mise a jour oubliee.

### 200 lignes max par fichier

Au-dela de 200 lignes, le fichier couvre probablement plusieurs sujets. Decoupez.

### Noms de fichiers explicites

Le nom du fichier doit suffire a comprendre son contenu. Pas de `notes.md`, `divers.md`, `temp.md`.

## Exemples de bonne organisation

### Freelance / consultant

```
knowledge/
  clients/
    client-alpha.md        -- contexte, contacts, historique
    client-beta.md
  metier/
    tarifs-2026.md          -- grille tarifaire en vigueur
    modele-proposition.md   -- structure des propositions commerciales
  guides/
    onboarding-client.md    -- checklist premier contact a livraison
    facturation.md          -- processus de facturation
```

### Startup technique

```
knowledge/
  infra/
    architecture.md         -- schema de l'infra
    runbooks.md             -- procedures d'urgence
    secrets-management.md   -- ou sont les secrets, comment y acceder
  produit/
    roadmap-q2-2026.md      -- priorites produit du trimestre
    metriques.md            -- KPIs suivis, seuils d'alerte
  equipe/
    roles.md                -- qui fait quoi
    rituels.md              -- reunions, standups, retros
```

### Dirigeant PME

```
knowledge/
  business/
    offre-services.md       -- description de l'offre
    clients-top-10.md       -- 10 plus gros clients, contexte
    pipeline-commercial.md  -- opportunites en cours
  operations/
    processus-recrutement.md
    processus-achat.md
  legal/
    contrats-types.md       -- clauses standard, points d'attention
    rgpd.md                 -- obligations, registre des traitements
```

## Etape par etape

### 1. Creer la structure de dossiers

Commencez avec 3 dossiers maximum. Vous pourrez toujours en ajouter.

### 2. Migrer depuis MEMORY.md

Relisez MEMORY.md. Tout ce qui est stable depuis plus de 2 semaines devrait migrer dans knowledge/. Remplacez l'entree dans MEMORY.md par une reference :

```
Avant (MEMORY.md) :
- Processus de deploiement : build > test > staging > validation > prod

Apres (MEMORY.md) :
- Processus de deploiement documente dans knowledge/infra/deploiement.md
```

### 3. Documenter vos 5 sujets les plus frequents

Quels sont les 5 sujets sur lesquels vous expliquez les memes choses a chaque session ? Documentez-les dans knowledge/.

### 4. Mettre en place la revision trimestrielle

Chaque trimestre, parcourez knowledge/ :
- Supprimez les fichiers obsoletes
- Mettez a jour les informations perimees
- Fusionnez les fichiers trop petits, decoupez les trop gros

## Erreurs courantes

**knowledge/ vide** : L'agent repart de zero sur les sujets de fond a chaque session. Perte de temps massive.

**Un seul gros fichier** : `knowledge/everything.md` de 800 lignes. Impossible a maintenir, impossible a lire efficacement.

**Duplication** : La meme information dans 3 fichiers. A la premiere mise a jour, 2 fichiers sur 3 sont obsoletes.

**Fichiers orphelins** : Des fichiers que personne ne lit et que personne ne maintient. Si un fichier n'a pas ete utile en 3 mois, supprimez-le ou archivez-le.

**Noms vagues** : `notes.md`, `idees.md`, `a-traiter.md`. Des noms qui ne disent rien sur le contenu.

## Verification

- [ ] Le dossier knowledge/ existe avec une structure par domaine
- [ ] Chaque fichier traite un seul sujet
- [ ] Aucun fichier ne depasse 200 lignes
- [ ] Pas de duplication entre fichiers (cross-references a la place)
- [ ] Les noms de fichiers sont explicites
- [ ] Les 5 sujets les plus frequents sont documentes
- [ ] Une date de revision trimestrielle est planifiee
