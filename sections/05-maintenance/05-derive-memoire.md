---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.5 -- Derive de la memoire

## Contexte

La memoire de votre agent accumule des informations au fil du temps. Certaines deviennent obsoletes, d'autres se contredisent, d'autres encore sont devenues fausses sans que personne ne le remarque. C'est la derive de la memoire.

Steinberg compare ca a un bureau : si vous ne rangez jamais, les documents importants se perdent sous les papiers perimes.

## Symptomes de la derive

Vous avez un probleme de derive quand :

- L'agent mentionne un projet que vous avez termine il y a 2 mois.
- L'agent utilise un ancien workflow qui a ete remplace.
- L'agent donne des informations contradictoires dans deux reponses proches.
- L'agent "se souvient" d'une decision qui a ete annulee.
- L'agent repete une information en la formulant differemment a chaque fois (signe de redondance).

## Types de derive

### Obsolescence

L'information etait vraie mais ne l'est plus.

```
Memoire : "Le projet cockpit utilise Express.js"
Realite : vous avez migre vers Fastify il y a 3 semaines.
```

### Contradiction

Deux informations se contredisent.

```
Memoire fichier A : "Les backups sont quotidiens"
Memoire fichier B : "Les backups sont hebdomadaires"
```

### Inflation

La meme information est stockee sous 5 formes differentes. L'agent ne sait plus laquelle utiliser.

```
Fichier 1 : "L'utilisateur prefere le tutoiement"
Fichier 2 : "Utiliser tu, pas vous"
Fichier 3 : "Communication informelle, tutoyer"
```

### Hallucination memorisee

L'agent a un jour "invente" une information et l'a stockee comme un fait.

```
Memoire : "Le serveur a 16 Go de RAM"
Realite : il en a 8.
```

## Nettoyage periodique

### Frequence

- **Mensuel** : scan rapide (15 minutes).
- **Trimestriel** : nettoyage en profondeur (1 heure).
- **Apres chaque projet termine** : supprimer le contexte du projet.

### Prompt de scan

```
Lis tous tes fichiers de memoire et de contexte.
Pour chaque information factuelle, indique :
- [OK] : toujours vraie et utile
- [OBSOLETE] : n'est plus vraie
- [DOUTE] : tu n'es pas sur, a verifier avec moi
- [REDONDANT] : dit la meme chose qu'une autre entree

Liste les resultats. On nettoie ensemble.
```

### Processus de nettoyage

1. Lancez le prompt de scan.
2. Revoyez les resultats avec l'agent.
3. Supprimez les [OBSOLETE].
4. Fusionnez les [REDONDANT] en une seule entree.
5. Verifiez les [DOUTE] — corrigez ou supprimez.
6. Sauvegardez la version nettoyee.

## Night consolidation

Concept de Steinberg : a la fin de chaque journee (ou semaine), l'agent consolide ce qu'il a appris.

```
Resume de la journee :
- Quelles nouvelles informations as-tu apprises aujourd'hui ?
- Est-ce qu'elles contredisent quelque chose dans ta memoire ?
- Quelles informations en memoire sont confirmees par la journee ?

Propose les mises a jour de memoire necessaires.
```

Ca ne prend pas longtemps. 2 minutes en fin de journee. Mais ca empeche la derive de s'accumuler.

## Oubli volontaire

Parfois, la bonne action est de supprimer de la memoire. Pas parce que c'est faux, mais parce que ce n'est plus utile.

Candidats a l'oubli :

- Details d'un projet termine (garder uniquement les lessons learned).
- Decisions intermediaires qui ont ete remplacees par la decision finale.
- Contexte temporaire ("cette semaine je travaille sur X").
- Essais et erreurs documentes mais plus pertinents.

L'oubli volontaire reduit le bruit et le cout en tokens. Moins de memoire = lectures plus rapides = reponses plus precises.

## Erreurs courantes

**Ne jamais nettoyer.** La memoire grossit, les contradictions s'accumulent, la qualite des reponses baisse. Vous blamer l'agent alors que c'est la memoire qui est polluee.

**Tout supprimer.** Nettoyage radical : vous effacez toute la memoire. L'agent repart de zero et perd tout le contexte utile. Nettoyez chirurgicalement.

**Faire confiance au scan sans verifier.** L'agent dit [OK] sur une information obsolete parce qu'il ne sait pas qu'elle a change. Verifiez les faits critiques vous-meme.

**Pas de versioning de la memoire.** Vous supprimez une information et vous en avez besoin 2 semaines plus tard. Gardez un backup avant chaque nettoyage.

## Etapes

1. Lancez le prompt de scan sur votre memoire.
2. Revoyez les resultats : OBSOLETE, DOUTE, REDONDANT.
3. Sauvegardez la version actuelle de la memoire (backup).
4. Nettoyez : supprimez, fusionnez, corrigez.
5. Testez : l'agent donne-t-il des reponses plus precises ?
6. Planifiez le prochain nettoyage (mensuel).

## Verification

- [ ] Un scan de memoire a ete fait dans le dernier mois.
- [ ] Les informations obsoletes sont supprimees.
- [ ] Les redondances sont fusionnees en une seule entree.
- [ ] Un backup de la memoire existe avant chaque nettoyage.
- [ ] La night consolidation est pratiquee (quotidienne ou hebdomadaire).
