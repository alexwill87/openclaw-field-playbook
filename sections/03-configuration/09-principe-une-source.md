---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.9 -- Une source a la fois (principe de Steinberg)

## Contexte

Vous avez configure l'agent. SOUL.md, USER.md, CONSTITUTION.md, MEMORY.md, knowledge/ -- tout est en place. Maintenant vous voulez connecter vos outils : calendrier, email, CRM, Notion, Slack, base de donnees, API metier...

Stop. Une source a la fois.

C'est le principe de Steinberg le plus contre-intuitif. L'instinct dit "tout connecter pour que l'agent ait une vue complete." L'experience dit "chaque source ajoutee augmente le bruit plus vite que le signal."

## Pourquoi une seule source a la fois

Chaque nouvelle connexion augmente trois choses :

**1. Le cout en tokens.** Chaque source injectee dans le contexte consomme de la fenetre. Calendrier + emails + taches + CRM = un contexte qui explose avant meme que vous ayez pose votre question.

**2. Le risque d'interpretation.** Plus l'agent a de sources, plus il fait de liens. Certains sont pertinents. D'autres sont des correlations fantomes. "Vous avez une reunion avec X et un email non lu de X, je deduis que..." -- non, pas forcement.

**3. Le bruit.** 50 emails non lus, 30 taches, 15 evenements calendrier. L'agent noie l'information importante dans la masse.

## La methode

### Connecter

Ajoutez UNE source. Calendrier d'abord (voir section 3.10).

### Valider

Vivez avec cette source pendant 3 a 5 jours. Posez la question :

```
Qu'est-ce qui a change depuis hier dans [source] ?
```

Si la reponse est utile et precise, la source apporte de la valeur. Si la reponse est vague ou bruitee, la configuration de la source doit etre affinee avant d'en ajouter une autre.

### Garder ou retirer

Regle de decision : **cette source ameliore-t-elle une decision que je dois prendre CETTE SEMAINE ?**

- Oui : garder
- "Ca pourrait etre utile un jour" : retirer
- "C'est interessant" : retirer

L'interessant est l'ennemi du pertinent.

## L'anti-pattern : le weekend de connexion

Scenario classique :

```
Vendredi soir : "Ce weekend, je connecte tout !"
Samedi : calendrier, email, Notion, CRM, Slack, base de donnees
Dimanche : "C'est genial, l'agent voit tout !"
Lundi matin : briefing de 45 lignes, 3 faux liens,
  2 actions suggerees a cote de la plaque
Lundi midi : "Cet outil ne marche pas."
```

Le probleme n'est pas l'outil. C'est que 6 sources connectees en 48h n'ont pas ete validees individuellement. Impossible de savoir laquelle cause le bruit.

## Ordre de connexion recommande

| Ordre | Source | Pourquoi maintenant |
|-------|--------|-------------------|
| 1 | Calendrier | Signal le plus fiable (section 3.10) |
| 2 | Taches | Complete le calendrier avec le non-planifie (section 3.11) |
| 3 | Email | La source la plus volumineuse, a ajouter apres maitrise des 2 premieres (section 3.12) |
| 4 | Outils metier | CRM, Notion, base de donnees -- selon votre besoin specifique |
| 5 | Messaging | Slack, Teams -- en dernier, le plus bruite |

Delai entre chaque ajout : minimum 3 jours, idealement 1 semaine.

## Etape par etape

1. Identifiez la source qui aurait le plus d'impact sur votre semaine
2. Connectez-la (voir les sections suivantes pour chaque type)
3. Utilisez-la pendant 3-5 jours
4. Evaluez avec la question "Qu'est-ce qui a change ?"
5. Si valide, passez a la suivante. Sinon, affinez d'abord.

## Erreurs courantes

**Tout connecter d'un coup** : Voir l'anti-pattern ci-dessus. Le bruit noie le signal.

**Garder une source inutile** : "J'ai connecte Slack mais je ne l'utilise jamais dans mes briefings." Deconnectez. Chaque source inutile consomme des tokens et ajoute du bruit.

**Connecter avant de configurer** : Ajouter l'email avant d'avoir un USER.md et un CONSTITUTION.md solides. L'agent va traiter vos emails sans comprendre vos priorites ni connaitre vos regles.

**Confondre "possible" et "utile"** : L'agent PEUT se connecter a 15 sources. Ca ne veut pas dire qu'il DOIT.

## Verification

- [ ] Vous avez identifie votre premiere source a connecter
- [ ] Vous avez un plan d'ajout progressif (une source a la fois)
- [ ] Vous connaissez la question de validation ("Qu'est-ce qui a change ?")
- [ ] Vous avez le critere de decision (ameliore une decision CETTE SEMAINE)
- [ ] Les fichiers de base (SOUL.md, USER.md, CONSTITUTION.md) sont en place AVANT la premiere connexion
