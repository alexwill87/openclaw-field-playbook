---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.14 -- Configuration bilingue

## Contexte

Si vous travaillez en francais et en anglais -- clients francophones, documentation en anglais, code en anglais, communications en francais -- votre agent doit savoir quand utiliser quelle langue. Sans instruction claire, il va basculer de facon impredictible.

## Les trois modes

### Mode 1 : francais uniquement

```
Langue : francais. Toujours.
Termes techniques en anglais quand il n'existe pas d'equivalent 
courant (deploy, commit, merge, container, endpoint).
Noms de commandes et de code en anglais (c'est du code, pas de la traduction).
```

Quand l'utiliser : usage personnel, equipe francophone, pas de clients anglophones.

### Mode 2 : anglais uniquement

```
Language: English. Always.
```

Quand l'utiliser : equipe internationale, documentation open source, clients anglophones.

### Mode 3 : bilingue contextuel

```
Langue par defaut : francais.
Bascule en anglais quand :
- Je redige de la documentation technique (README, API docs)
- Je prepare un message pour un client anglophone
- Je te dis "in English"
Retour au francais automatique a la conversation suivante.
```

Quand l'utiliser : contexte mixte, freelance international, projet open source avec equipe locale.

## Regles de basculement

Le basculement doit etre previsible. Definissez les declencheurs :

| Declencheur | Langue |
|---|---|
| Conversation directe | Francais |
| Ecrire un commit message | Anglais |
| Ecrire de la documentation code | Anglais |
| Ecrire un email client FR | Francais |
| Ecrire un email client EN | Anglais |
| Commenter du code | Anglais |
| Expliquer un concept | Francais |
| Nommer des variables/fonctions | Anglais |

### Prompt de basculement

```
Pour basculer la langue :
- "En anglais" ou "in English" -> bascule en anglais pour cette tache
- "En francais" -> retour au francais
- Quand j'ecris en anglais, reponds en anglais
- Quand j'ecris en francais, reponds en francais
- Par defaut : francais
```

## Modeles recommandes par langue

Tous les grands modeles (Claude, GPT-4, Gemini) gèrent bien le francais et l'anglais. Quelques nuances :

### Francais

- **Claude** : excellent en francais. Comprend les nuances, le tutoiement/vouvoiement, le registre.
- **GPT-4** : bon en francais, parfois des tournures un peu anglicisees.
- **Modeles open source (Mistral, LLaMA)** : Mistral, etant francais, est fort en francais. LLaMA est variable.

### Anglais

Tous les modeles sont excellents en anglais. Pas de difference significative pour un usage professionnel.

### Bilingue

Le facteur cle : la coherence du basculement. Claude et GPT-4 gerent bien le contexte bilingue si les regles sont claires dans le system prompt. Les modeles plus petits ont tendance a melanger.

## Les pieges du bilingue

### Le melange involontaire

L'agent commence en francais, met un terme anglais, puis continue en anglais. Ou l'inverse. Solution : regle explicite dans le system prompt.

```
Si tu bascules de langue en cours de reponse, signale-le.
Une reponse = une langue (sauf termes techniques).
```

### La traduction non demandee

Vous ecrivez en francais, l'agent traduit en anglais "pour etre plus precis". Solution :

```
Ne traduis jamais ma requete. Reponds dans la langue que j'utilise.
```

### Les termes techniques forces

L'agent traduit "container" en "conteneur", "deploy" en "deployer" (au lieu de "deployer", qui est acceptable en franglais technique). Solution :

```
Termes techniques gardes en anglais : deploy, commit, merge, push, pull, 
container, endpoint, token, API, CLI, pipeline, build, runtime.
```

## Erreurs courantes

**Pas de regle de langue.** L'agent choisit selon l'humeur du modele. Inconsistant.

**Forcer le 100% francais technique.** "Utilisez 'conteneur' au lieu de 'container'." Personne ne parle comme ca. Gardez les termes que votre equipe utilise au quotidien.

**Basculer sans contexte.** Vous dites "in English" mais oubliez de revenir en francais. L'agent continue en anglais pour les 10 prochaines requetes.

## Etapes

1. Decidez votre mode (1, 2, ou 3).
2. Listez les termes techniques a garder en anglais.
3. Definissez les declencheurs de basculement.
4. Ajoutez les regles au system prompt.
5. Testez avec 5 requetes dans chaque langue.

## Verification

- [ ] Le mode de langue est defini dans le system prompt.
- [ ] Les termes techniques a garder en anglais sont listes.
- [ ] Les declencheurs de basculement sont explicites.
- [ ] L'agent respecte la langue attendue (teste dans les deux langues).
- [ ] Pas de melange involontaire dans les reponses.
