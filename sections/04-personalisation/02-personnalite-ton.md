---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.2 -- Personnalite et ton

## Contexte

Le ton de votre agent n'est pas un detail cosmetique. C'est ce qui fait la difference entre un outil que vous utilisez avec plaisir et un outil que vous subissez. Un agent trop verbeux, vous arretez de lire. Trop sec, vous n'avez pas le contexte. Trop formel, ca sonne faux.

Le but : que la reponse de l'agent ressemble a ce qu'un collegue competent vous dirait.

## Les axes de personnalite

### Direct vs diplomatique

**Direct** : "Ce script a un bug ligne 12. Le fix : [code]."
**Diplomatique** : "J'ai remarque un point d'attention a la ligne 12 qui pourrait potentiellement causer un souci..."

Pour un usage technique quotidien, direct gagne. Toujours.

### Humoristique vs professionnel

L'humour dans un agent technique est un piege. Ca marche la premiere fois, ca fatigue a la centieme. Si vous en voulez, dosez : une remarque legere quand ca va bien, zero humour quand ca casse.

### Court vs detaille

La regle d'or : court par defaut, detaille sur demande.

Mauvais : `"communication detaillee"`
Bon : `"3 phrases max sauf si je demande plus"`
Encore mieux : `"1 ligne pour la reponse, bloc code si necessaire, explication uniquement si je dis 'explique'"`

### Tutoiement vs vouvoiement

Votre agent, votre choix. Mais soyez explicite :

```
Tutoie-moi. Pas de "vous", pas de formules de politesse.
```

ou

```
Vouvoiement. Ton professionnel mais pas distant.
```

Si vous ne precisez pas, l'agent va alterner et ca sonne inconsistant.

## Formuler de facon actionnable

Le probleme avec les instructions vagues, c'est que le modele les interprete a sa facon. Et chaque modele les interprete differemment.

| Vague (inutile) | Actionnable (efficace) |
|---|---|
| "Sois concis" | "3 phrases max sauf demande explicite" |
| "Communication directe" | "Pas de formules de politesse. Commence par la reponse." |
| "Ton professionnel" | "Pas d'emojis. Pas d'exclamations. Francais standard." |
| "Sois utile" | (ne rien ecrire -- c'est le comportement par defaut) |
| "Adapte-toi a mon style" | "Phrase courte. Bullet points pour les listes. Code inline pour les commandes." |

## Exemples concrets de configuration

### Profil tech / devops

```
Ton : direct, technique. Pas de formules de politesse.
Reponse courte par defaut (1-3 phrases + code si applicable).
Si je pose une question oui/non, reponds oui ou non d'abord, puis justifie.
Tutoie-moi.
Pas d'emojis.
```

### Profil consultant / client-facing

```
Vouvoiement. Ton professionnel mais accessible.
Quand je prepare un email client, propose une version diplomate.
Pour le travail interne, reponse directe et courte.
```

### Profil creatif

```
Tutoie-moi. Ton decontracte.
Propose des alternatives quand je demande un avis.
Si une idee est mauvaise, dis-le franchement avec une meilleure suggestion.
```

## Erreurs courantes

**Empiler les adjectifs.** "Sois professionnel, chaleureux, concis, detaille quand il faut, humoristique mais pas trop." Le modele ne sait pas prioriser. Choisissez 2-3 traits, pas 7.

**Copier le ton d'un autre.** Le prompt de quelqu'un d'autre ne sonnera pas juste pour vous. Partez de vos propres conversations : comment parlez-vous a un collegue de confiance ? C'est votre ton.

**Oublier le format.** Le ton, ce n'est pas que les mots. C'est aussi : bullet points vs prose, blocs de code vs inline, headers vs texte continu. Precisez le format autant que le vocabulaire.

## Adapter le ton par canal

Un agent utilise souvent plusieurs canaux. Le ton doit s'adapter :

| Canal | Ton recommande | Exemple |
|-------|----------------|---------|
| Telegram | Court, direct, 1-3 phrases | "Deploiement OK. Zero erreur." |
| Email | Structure, professionnel | Objet + contexte + action demandee |
| Terminal / CLI | Technique, minimal | Commande + resultat attendu |
| Rapport / bilan | Detaille, avec tableaux | Sections, metriques, recommandations |

Precisez dans le system prompt : `"Sur Telegram : max 3 phrases. Par email : structure complete."` Sans cette precision, l'agent ecrit des paves sur Telegram et des telegrammes par email.

## Cas terrain : le spectrum proactif-passif (Aurel)

L'agent Aurel definit explicitement son positionnement sur le spectrum passif-proactif dans son IDENTITY.md. Ce parametrage a un impact direct sur le ton :

- **Mode passif** : repond uniquement aux questions. Ton factuel, bref.
- **Mode proactif** : propose des actions, alerte sur les problemes, envoie un briefing matin. Ton plus engage.

Le piege : un agent configure "proactif" avec un ton "minimal" cree une dissonance. Il envoie des alertes mais sans assez de contexte pour agir. Alignez le ton avec le niveau de proactivite.

## Etapes

1. Relisez vos 10 dernieres conversations avec votre agent.
2. Notez chaque fois ou le ton vous a gene (trop long, trop formel, trop vague).
3. Formulez 3-5 instructions actionnables qui corrigent ces problemes.
4. Ajoutez-les au system prompt, section Ton.
5. Testez sur 5 requetes. Ajustez.

## Verification

- [ ] Le ton est defini en instructions actionnables, pas en adjectifs.
- [ ] Le choix tutoiement/vouvoiement est explicite.
- [ ] La longueur par defaut des reponses est specifiee.
- [ ] Le format (bullets, prose, code) est precise.
- [ ] Teste sur 5 requetes -- le ton est consistant.
