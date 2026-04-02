---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.6 -- Les trois zones de memoire

## Contexte

Un agent sans memoire est un agent amnesique. Chaque session repart de zero. Vous repetez les memes choses. Il pose les memes questions.

Un agent avec trop de memoire est un agent noye. Il melange le contexte d'il y a 6 mois avec celui d'aujourd'hui. Il cite des decisions obsoletes. Il traite comme actuel ce qui ne l'est plus.

La solution de Steinberg : trois zones de memoire, chacune avec sa portee et ses regles.

## Les trois zones

```
+--------------------------------------------------+
|                                                  |
|  MEMOIRE CHAUDE (session)                        |
|  Duree : cette conversation                      |
|  Taille : illimitee (dans la fenetre de contexte)|
|  Contenu : tout ce qui se dit maintenant         |
|  Disparait : a la fin de la session              |
|                                                  |
+--------------------------------------------------+
          |
          | Ce qui merite d'etre retenu
          v
+--------------------------------------------------+
|                                                  |
|  MEMOIRE TIEDE (MEMORY.md)                       |
|  Duree : jours a semaines                        |
|  Taille : 80 lignes max                          |
|  Contenu : faits recents, decisions, contexte    |
|  Nettoyage : compression reguliere               |
|                                                  |
+--------------------------------------------------+
          |
          | Ce qui est durable et structure
          v
+--------------------------------------------------+
|                                                  |
|  MEMOIRE FROIDE (knowledge/)                     |
|  Duree : mois a indefini                         |
|  Taille : illimitee (un fichier par sujet)       |
|  Contenu : savoirs stables, references, guides   |
|  Nettoyage : revision trimestrielle              |
|                                                  |
+--------------------------------------------------+
```

## Memoire chaude : la session

C'est la conversation en cours. Tout ce que vous dites, tout ce que l'agent repond, reste accessible pendant la session.

**Ce qui y va** : tout. Questions, reponses, reflexions, essais, erreurs.

**Ce qui en sort** : rien automatiquement. A la fin de la session, tout disparait SAUF ce que vous ou l'agent decidez de sauvegarder dans MEMORY.md ou knowledge/.

**Piege** : croire que l'agent "se souviendra" demain de ce que vous avez dit aujourd'hui. Sans sauvegarde explicite, la memoire chaude est volatile.

Bonne pratique en fin de session :

```
Qu'est-ce qui merite d'etre retenu de cette session ?
Mets a jour MEMORY.md.
```

## Memoire tiede : MEMORY.md

Le tampon entre le present et le durable. 80 lignes maximum (regle de Steinberg). Contient le contexte recent necessaire pour que l'agent soit pertinent des l'ouverture de la prochaine session.

**Ce qui y va** :
- Decisions prises cette semaine
- Faits recents importants
- Contexte en cours (projet, negociation, evenement)
- Notes temporaires a ne pas oublier

**Ce qui n'y va PAS** :
- Des connaissances stables (ca va dans knowledge/)
- Des informations personnelles permanentes (ca va dans USER.md)
- Des regles de fonctionnement (ca va dans CONSTITUTION.md)
- Des taches (ca va dans le systeme de taches)

Detail dans la section 3.7.

## Memoire froide : knowledge/

Le savoir durable. Structure par domaine. Un fichier par sujet. Pas de limite de taille globale, mais chaque fichier doit rester lisible (200 lignes max par fichier recommande).

**Ce qui y va** :
- Processus documentes
- Informations metier stables
- References techniques
- Guides et procedures
- Profils de clients ou partenaires durables

**Ce qui n'y va PAS** :
- Du contexte temporaire (ca va dans MEMORY.md)
- Des opinions ou preferences (ca va dans USER.md)
- Des regles agent (ca va dans CONSTITUTION.md)

Detail dans la section 3.8.

## Pourquoi separer

**Raison 1 : le cout en tokens.** Tout ce que l'agent lit au demarrage consomme des tokens. MEMORY.md (80 lignes) est lu a chaque session. knowledge/ est lu a la demande ou selon la boot sequence. Melanger les deux = charger 500 lignes de connaissances stables a chaque session, meme quand elles ne sont pas pertinentes.

**Raison 2 : le bruit.** Un agent qui lit 200 lignes de contexte au demarrage va perdre le signal. Les informations recentes (MEMORY.md) doivent etre separees des connaissances de fond (knowledge/) pour que l'agent sache ce qui est ACTUEL.

**Raison 3 : la maintenance.** MEMORY.md se compresse chaque semaine. knowledge/ se revise chaque trimestre. Deux rythmes differents pour deux types d'information differents.

**Raison 4 : la pertinence.** Quand l'agent lit "Decision du 28/03 : on reporte le lancement a avril" dans MEMORY.md, il sait que c'est recent et actionnable. Quand il lit "Processus de lancement produit" dans knowledge/, il sait que c'est une reference stable.

## Diagramme de decision

```
Une information arrive. Ou la stocker ?

Est-ce que ca concerne UNIQUEMENT cette session ?
  OUI --> Ne rien faire. Memoire chaude.
  NON --> continuer

Est-ce que ca va changer dans les 2 prochaines semaines ?
  OUI --> MEMORY.md (memoire tiede)
  NON --> continuer

Est-ce que c'est un savoir stable et reutilisable ?
  OUI --> knowledge/ (memoire froide)
  NON --> continuer

Est-ce que c'est une information sur MOI qui ne change pas souvent ?
  OUI --> USER.md
  NON --> continuer

Est-ce que c'est une regle de fonctionnement de l'agent ?
  OUI --> CONSTITUTION.md
  NON --> Probablement pas necessaire de le stocker.
```

## Erreurs courantes

**Tout dans MEMORY.md** : Le fichier grossit, depasse 80 lignes, l'agent perd le signal. MEMORY.md est un tampon, pas une base de donnees.

**Rien dans knowledge/** : Vous repetez les memes explications a chaque session parce que l'agent n'a pas de reference durable.

**Pas de nettoyage** : MEMORY.md contient des notes de 3 mois. knowledge/ contient des fichiers obsoletes. La memoire non entretenue est pire que pas de memoire.

**Confusion memoire chaude / tiede** : "Je te l'ai dit tout a l'heure" -- oui, en session. Mais sans sauvegarde dans MEMORY.md, demain c'est oublie.

## Verification

- [ ] Vous comprenez la difference entre les 3 zones
- [ ] MEMORY.md existe et fait moins de 80 lignes
- [ ] Le dossier knowledge/ est cree avec au moins un fichier
- [ ] Vous avez une routine de fin de session ("Mets a jour MEMORY.md")
- [ ] Les informations sont dans la bonne zone (pas de taches dans USER.md, pas de connaissances stables dans MEMORY.md)
