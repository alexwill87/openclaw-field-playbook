---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.7 -- MEMORY.md : la memoire collective

## Contexte

MEMORY.md est le fichier le plus vivant de votre configuration. Il change chaque jour. Il se compresse chaque semaine. Il est lu a chaque demarrage de session.

C'est la memoire tiede : ce qui s'est passe recemment et qui compte encore. Pas le passe lointain (knowledge/). Pas le present immediat (session). L'entre-deux.

## La regle des 80 lignes

Steinberg est catégorique : MEMORY.md ne doit jamais depasser 80 lignes.

Pourquoi 80 :
- En dessous de 80, l'agent traite chaque ligne comme importante
- Au-dessus de 80, l'agent commence a "survoler" et manque des informations
- 80 lignes = environ 2 minutes de lecture pour l'agent au demarrage

Ce n'est pas une suggestion. C'est une contrainte dure. Si MEMORY.md depasse 80 lignes, il faut compresser ou deplacer du contenu vers knowledge/.

## Structure recommandee

```markdown
# MEMORY.md

## Contexte actuel
- [Fait important 1 -- date]
- [Fait important 2 -- date]
- [Situation en cours]

## Decisions recentes
- [Decision 1 -- date -- raison]
- [Decision 2 -- date -- raison]

## En attente
- [Ce qui attend une reponse ou action]
- [Ce qui est bloque et pourquoi]

## Notes de session
- [Dernier fait marquant de la derniere session]
```

Quatre sections. Pas plus. Si vous avez besoin de plus de sections, c'est que du contenu devrait migrer vers knowledge/.

## Night consolidation (methode Steinberg)

Chaque soir (ou chaque matin avant le briefing), l'agent consolide MEMORY.md :

1. **Supprimer** ce qui n'est plus pertinent (decision executee, evenement passe)
2. **Compresser** ce qui peut l'etre (3 lignes sur le meme sujet = 1 ligne)
3. **Migrer** ce qui est devenu du savoir stable vers knowledge/
4. **Ajouter** ce qui a emerge pendant la journee

Prompt de consolidation :

```
Consolide MEMORY.md :
1. Supprime ce qui n'est plus pertinent (plus de 2 semaines, deja traite)
2. Compresse les entrees liees en une seule ligne
3. Si une information est devenue stable, migre-la vers knowledge/
4. Verifie que le total ne depasse pas 80 lignes
Montre-moi le diff avant de sauvegarder.
```

## L'oubli volontaire

L'oubli est une fonctionnalite, pas un bug. Un agent qui se souvient de tout est un agent qui ne sait pas ce qui compte.

Quand supprimer de MEMORY.md :
- La decision a ete executee et n'a plus d'impact
- L'evenement est passe et n'influence plus le present
- L'information a ete migree dans knowledge/
- Le fait est devenu obsolete (prix change, personne partie, projet annule)

Quand NE PAS supprimer :
- La decision impacte encore la semaine en cours
- L'information est necessaire pour le prochain briefing
- Le contexte est encore actif (negociation en cours, projet en phase critique)

## Memoire collective vs individuelle

Si vous avez plusieurs agents (section 3.17), MEMORY.md peut etre :
- **Partage** : tous les agents lisent le meme fichier. Plus simple. Risque de bruit.
- **Separe** : chaque agent a son MEMORY.md. Plus propre. Risque de desynchronisation.

Recommendation : commencez partage. Separéz quand le bruit devient un probleme.

## Template MEMORY.md

```markdown
# MEMORY.md
Derniere consolidation : [date]

## Contexte actuel
- [3-5 lignes max sur la situation generale]

## Decisions recentes
- [AAAA-MM-JJ] [Decision] -- [Raison en 5 mots]
- [AAAA-MM-JJ] [Decision] -- [Raison en 5 mots]

## En attente
- [Quoi] -- en attente de [qui/quoi] -- depuis [date]

## Notes
- [Fait marquant de la derniere session]
```

## Erreurs courantes

**MEMORY.md jamais nettoye** : Le fichier grossit jusqu'a 300 lignes. L'agent perd le signal. Consolidez au moins une fois par semaine.

**Tout garder "au cas ou"** : Si une information n'a pas ete utile depuis 2 semaines, elle n'est probablement plus pertinente. Supprimez ou migrez.

**Pas de dates** : Sans dates, impossible de savoir ce qui est recent. Chaque entree doit avoir une date.

**Doublons avec knowledge/** : "Processus de deploiement -- mis a jour le 15/03" dans MEMORY.md alors que le processus est deja dans knowledge/infra/. MEMORY.md pointe vers knowledge/, il ne duplique pas.

**Trop de sections** : 8 sections dans MEMORY.md = trop de structure. 4 sections suffisent. Si vous avez besoin de plus, c'est que du contenu appartient ailleurs.

## Verification

- [ ] MEMORY.md existe et fait moins de 80 lignes
- [ ] Chaque entree a une date
- [ ] La structure a 4 sections maximum
- [ ] Pas de doublons avec knowledge/
- [ ] Le prompt de consolidation est pret (ou automatise via cron)
- [ ] Vous savez ce qui doit etre supprime et ce qui doit etre garde
