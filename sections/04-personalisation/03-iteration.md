---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.3 -- Iteration : la premiere version ne sera pas la bonne

## Contexte

Votre premier system prompt sera mauvais. Pas parce que vous etes mauvais -- parce que personne ne sait ce qu'il veut d'un agent avant de l'avoir utilise. C'est normal. Le prompt se decouvre en l'utilisant, pas en y reflechissant.

Prevoyez 2-3 rounds d'iteration avant d'avoir un prompt qui sonne juste. Apres ca, des ajustements ponctuels quand le besoin change.

## Le processus d'iteration

### Round 1 : la version brute

Ecrivez votre premier prompt (voir section 4.1). Utilisez-le pendant 2-3 jours. Notez chaque friction :

- "Il repond trop long"
- "Il oublie que je veux du tutoiement"
- "Il propose des solutions Windows alors que je suis sur Linux"
- "Il me redemande le contexte a chaque fois"

### Round 2 : le prompt de correction

Utilisez ce pattern pour corriger :

```
Voici mon system prompt actuel :
[coller le prompt]

Problemes constates :
1. [friction 1]
2. [friction 2]
3. [friction 3]

Reecris le prompt en corrigeant ces problemes.
Garde la structure. Ne depasse pas 250 mots.
```

Relisez la proposition. Modifiez a la main ce qui ne colle pas. Testez 2-3 jours de plus.

### Round 3 : condenser

Apres le round 2, votre prompt fait probablement 400-500 mots. C'est trop. Chaque token compte.

Prompt de condensation :

```
Voici mon system prompt (480 mots).
Condense-le a 150 mots maximum.
Garde TOUTES les regles et interdictions.
Supprime les explications -- l'agent n'a pas besoin de comprendre pourquoi.
```

La regle : 150 mots > 500 mots. Un prompt court et precis bat un prompt long et detaille. Le modele n'a pas besoin de vos justifications -- il a besoin de vos instructions.

## Pourquoi condenser marche

Un prompt long cree du bruit. Le modele doit trier ce qui est important de ce qui est du remplissage. Plus c'est court, plus chaque mot pese.

Comparaison :

**Avant (68 mots) :**
```
Quand tu me proposes des solutions techniques, j'aimerais que tu prennes
en compte le fait que je travaille principalement sur des environnements
Linux Ubuntu, et que je n'ai generalement pas besoin de solutions qui
seraient specifiques a Windows ou macOS, sauf si je te le demande
explicitement dans ma question.
```

**Apres (12 mots) :**
```
Environnement : Linux Ubuntu. Pas de solutions Windows/macOS sauf demande.
```

Meme information. 5x moins de tokens.

## Quand arreter d'iterer

Arretez quand :

- Vous ne corrigez plus l'agent sur le ton ou le format.
- Les reponses sont utiles des la premiere fois dans 80%+ des cas.
- Vos corrections portent sur le fond (connaissance) pas la forme (comportement).

Si vous etes encore en train d'iterer apres 5 rounds, le probleme n'est probablement pas le prompt. C'est peut-etre le modele, l'outil, ou vos attentes.

## Erreurs courantes

**Ne jamais iterer.** Le premier jet reste en place pendant des mois. Le prompt accumule des instructions obsoletes et l'agent degrade progressivement.

**Iterer sans noter.** Vous changez le prompt "de memoire" sans avoir note les frictions. Vous corrigez un probleme et en creez un autre.

**Ajouter sans supprimer.** Chaque iteration ajoute des regles mais n'en retire jamais. Apres 5 rounds, le prompt fait 800 mots et se contredit.

## Etapes

1. Utilisez votre prompt actuel pendant 2-3 jours.
2. Notez chaque friction dans un fichier `prompt-feedback.md`.
3. Appliquez le prompt de correction (round 2).
4. Testez 2-3 jours.
5. Condensez a 150 mots (round 3).
6. Testez. Si ca tient, c'est bon.

## Verification

- [ ] Le prompt actuel a ete teste en conditions reelles (pas juste relu).
- [ ] Les frictions sont notees par ecrit, pas de memoire.
- [ ] Le prompt final fait moins de 200 mots.
- [ ] Aucune instruction ne contredit une autre.
- [ ] 80%+ des reponses sont utiles sans correction.
