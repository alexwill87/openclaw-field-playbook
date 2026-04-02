---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.10 -- Calendrier d'abord, toujours (principe de Steinberg)

## Contexte

Si vous ne connectez qu'une seule source, connectez le calendrier. C'est la premiere connexion, sans exception.

Steinberg est formel : le calendrier est le signal le plus honnete de votre vie professionnelle. Pas ce que vous dites que vous faites. Pas ce que vous aimeriez faire. Ce que vous faites REELLEMENT.

## Les 4 raisons de commencer par le calendrier

### 1. Le calendrier ne ment pas

Vos emails sont bruyants. Vos taches sont incompletes. Votre CRM est desynchronise. Mais votre calendrier reflete vos engagements reels. Si c'est dans le calendrier, ca va se passer (ou ca aurait du).

### 2. Le calendrier donne le tempo

Un agent qui connait votre calendrier sait :
- Que vous etes en reunion de 10h a 11h (ne pas deranger)
- Que vous avez une presentation client a 14h (preparer le contexte)
- Que votre apres-midi est libre (moment ideal pour du travail de fond)
- Que demain est charge (compresser le briefing)

### 3. Le calendrier connecte les personnes

Chaque evenement du calendrier implique des personnes. L'agent croise ces personnes avec USER.md (interlocuteurs cles) et knowledge/ (contexte client). Le briefing passe de "Vous avez 4 reunions" a "Vous voyez Marc de ClientAlpha a 14h -- rappel : la proposition tarifaire est en attente depuis le 25/03."

### 4. Le calendrier est peu bruyant

Contrairement aux emails (50/jour) ou aux messages (200/jour), le calendrier genere 5 a 15 evenements par jour. Peu de volume, forte pertinence.

## Configuration

### Via skill

```
openclaw skill add calendar
```

L'agent va :
1. Vous demander le fournisseur (Google Calendar, Outlook, CalDAV)
2. Configurer l'authentification
3. Definir la portee (lecture seule recommandee au debut)
4. Creer le skill dans votre workspace

### Portee recommandee

| Droit | Recommandation |
|-------|----------------|
| Lecture des evenements | Oui |
| Lecture des participants | Oui |
| Lecture des descriptions | Oui |
| Creation d'evenements | Non (ajoutez plus tard si besoin) |
| Modification d'evenements | Non |
| Suppression d'evenements | Non |

Commencez en lecture seule. Ajoutez les droits d'ecriture apres 2 semaines d'utilisation si necessaire.

## Validation

Le test de validation est simple :

```
Montre-moi mes prochaines 48h.
```

L'agent doit afficher :
- Les evenements dans l'ordre chronologique
- Les participants de chaque reunion
- Les creneaux libres
- Les evenements qui meritent une preparation

Si l'affichage est correct et les croisements pertinents (lien avec les interlocuteurs de USER.md), la connexion est validee.

### Ce qui rend un briefing calendrier UTILE

```
MERCREDI 2 AVRIL

09:00-09:30  Standup equipe
  > RAS -- routine hebdomadaire

10:00-11:00  Point projet Alpha avec Marc (ClientAlpha)
  > Preparation : la proposition tarifaire envoyee le 25/03
    n'a pas encore recu de retour. Sujet probable.

11:00-14:00  Bloc libre
  > Suggestion : traiter les 3 emails en attente de reponse

14:00-15:00  Entretien recrutement -- Lea Martin (poste dev backend)
  > CV dans knowledge/recrutement/lea-martin.md

15:30-16:00  Call investisseur -- Fonds Epsilon
  > Contexte : second call. Le premier etait le 18/03.
    Notes dans MEMORY.md.
```

### Ce qui rend un briefing calendrier INUTILE

```
Vous avez 4 reunions demain : standup, point projet,
entretien, call. Bonne journee !
```

Si votre briefing ressemble au deuxieme exemple, le probleme n'est pas le calendrier. C'est que USER.md et knowledge/ sont trop vides pour que l'agent fasse des croisements.

## Etape par etape

1. Connectez le calendrier en lecture seule
2. Testez avec "Montre-moi mes prochaines 48h"
3. Verifiez que les croisements avec USER.md fonctionnent
4. Vivez avec pendant 5 jours avant d'ajouter une autre source
5. Ajoutez les droits d'ecriture seulement si necessaire

## Erreurs courantes

**Connecter l'email avant le calendrier** : L'email est bruyant, le calendrier est structure. Inversez l'ordre et vous deboguerez le bruit email sans le repere du calendrier.

**Ignorer les participants** : Le calendrier sans croisement avec les interlocuteurs cles est un simple agenda. La valeur vient du lien entre l'evenement et le contexte.

**Donner les droits d'ecriture immediatement** : L'agent cree un evenement par erreur, vous avez un "Revue strategie Q3" dans votre calendrier un samedi. Commencez en lecture.

**Ne pas remplir USER.md avant** : Le calendrier sans contexte = une liste d'evenements. Le calendrier avec USER.md = un briefing intelligent.

## Verification

- [ ] Calendrier connecte en lecture seule
- [ ] Test "Montre-moi mes prochaines 48h" reussi
- [ ] Les participants sont croises avec les interlocuteurs cles de USER.md
- [ ] Les creneaux libres sont identifies
- [ ] Le briefing est contextualise (pas une simple liste)
- [ ] 5 jours d'utilisation avant d'ajouter une autre source
