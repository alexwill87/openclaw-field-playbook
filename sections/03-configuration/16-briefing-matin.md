---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.16 -- Le briefing du matin (methode Steinberg)

## Contexte

Le briefing du matin est le test ultime de votre configuration. Si le briefing est bon, la configuration est bonne. S'il est generique, plat, ou hors sujet, le probleme est en amont : USER.md incomplet, calendrier non connecte, MEMORY.md vide.

Steinberg utilise le briefing comme diagnostic : "Montre-moi ton briefing, je te dirai ce qui manque dans ta config."

## Le prompt exact

```
Briefing du matin.

Sources :
- Calendrier : prochaines 24h
- Taches : cette semaine, non completees
- Email : recus depuis hier soir
- MEMORY.md : contexte actuel

Format :
1. FOCUS DU JOUR : la chose la plus importante aujourd'hui (1 phrase)
2. AGENDA : evenements de la journee avec contexte
3. A TRAITER : ce qui attend une action de ma part
4. SIGNAUX : ce que j'aurais pu rater
5. SUGGESTION : une action concrete que tu recommandes

Maximum 30 lignes. Pas de formules de politesse.
```

## Si c'est generique, le probleme est en amont

Un briefing generique ressemble a ca :

```
Bonjour ! Voici votre briefing.
Vous avez 4 reunions et 8 taches. Bonne journee !
```

Ce n'est pas un briefing. C'est un compteur. Les causes possibles :

| Symptome | Cause probable | Solution |
|---|---|---|
| Pas de contexte sur les reunions | USER.md sans interlocuteurs cles | Completer USER.md |
| Taches listees sans priorite | Systeme de taches non priorise | Prioriser les taches |
| Emails mentionnes sans triage | Regles de triage absentes | Definir les regles dans CONSTITUTION.md |
| Aucune suggestion pertinente | knowledge/ vide | Documenter les sujets recurrents |
| Aucun rappel de contexte | MEMORY.md vide | Routine de fin de session |

## Exemples de BONS briefings

### Alex -- consultante independante

```
FOCUS DU JOUR
Preparation du comite de pilotage ClientAlpha a 14h.

AGENDA
09:00  Standup equipe (routine, 15 min)
10:00-12:00  Bloc libre
  > Suggestion : finaliser les slides du copil
14:00-15:30  Copil ClientAlpha -- Marc, Sophie, Director Technique
  > Contexte : phase 2 du projet validee le 18/03.
    Budget restant : 45%. Sophie a signale un risque planning
    dans son email du 30/03. A adresser.
16:00  Call rapide avec comptable -- documents bilan

A TRAITER
- Repondre a Sophie (email du 30/03) : elle attend des clarifications
  sur le planning phase 2 AVANT le copil
- Facture mars ClientBeta : a envoyer avant vendredi

SIGNAUX
- Marc n'a pas repondu au dernier email (envoye il y a 5 jours).
  Inhabituel. A surveiller au copil.

SUGGESTION
Repondre a Sophie ce matin. Son point sur le planning sera
probablement souleve au copil. Mieux vaut avoir la reponse prete.
```

Pourquoi c'est bon : le focus est clair, le contexte du copil est complet (avec rappel du budget et du risque signale), les actions sont concretes et priorisees, le signal sur Marc est pertinent.

### Sam -- CTO startup

```
FOCUS DU JOUR
Release v2.4 prevue a 16h. Derniere fenetre avant le weekend.

AGENDA
09:00  Standup dev (routine)
09:30-12:00  Bloc code -- finir le fix #847
  > Le fix est a 80% (note session d'hier). Reste : tests d'integration.
12:30  Lunch with investor (informel, pas de prep requise)
14:00  Code review PR #312 avec Lea
  > PR ouverte depuis 3 jours. Lea attend le retour.
16:00  Fenetre de release v2.4
  > Checklist : fix #847 merge, tests green, staging OK

A TRAITER
- Valider la PR #312 (bloque Lea depuis 3 jours)
- Repondre au candidat backend (deadline reponse : demain)

SIGNAUX
- Le pipeline CI a eu 2 flaky tests hier soir (monitoring).
  Pas bloquant mais a surveiller avant la release.

SUGGESTION
Faire la code review #312 en premier ce matin.
Lea est bloquee et ca ne prend que 30 min.
Le fix #847 peut attendre 10h.
```

### Mira -- dirigeante PME

```
FOCUS DU JOUR
Signature contrat FournisseurY. Dernier jour de validite de l'offre.

AGENDA
08:30  Point RH avec Julie -- recrutement poste commercial
  > 3 candidats shortlistes. Julie attend votre avis pour
    passer aux entretiens finaux.
10:00  Reunion equipe commerciale (hebdo)
  > Pipeline : 2 prospects chauds (voir knowledge/business/pipeline.md)
11:30-14:00  Libre
14:00  Signature contrat FournisseurY (en visio)
  > Montant : 24 000 EUR/an. Negocie le 20/03.
    Conditions validees par le juridique le 27/03.
15:30  Call banque -- point tresorerie mensuel

A TRAITER
- Relire le contrat FournisseurY une derniere fois avant signature
- Valider les 3 candidats RH (Julie attend depuis 2 jours)

SIGNAUX
- Le prospect Gamma n'a pas donne suite depuis l'envoi de la
  proposition le 22/03 (10 jours). Relance a envisager.

SUGGESTION
Relire le contrat ce matin pendant le bloc libre.
Valider les candidats RH avant le point avec Julie a 08:30
(email de 5 min, elle aura les infos en main pour la reunion).
```

### Jordan -- developpeur freelance

```
FOCUS DU JOUR
Livraison module authentification pour ClientDelta (deadline demain).

AGENDA
09:00-12:00  Dev -- module auth ClientDelta
  > Avancement : 70%. Reste : tests unitaires + documentation API.
  > Note de session hier : le flow OAuth fonctionne, tests en cours.
14:00  Call ClientDelta -- point d'avancement
  > Lea (chef de projet) veut un statut. Avoir les tests passes
    AVANT le call si possible.
15:00-18:00  Dev -- continuer si necessaire

A TRAITER
- Facture ClientEpsilon : en retard de paiement (45 jours).
  Relance envoyee le 25/03, pas de reponse.
- Devis ClientZeta : demande recue hier, repondre d'ici vendredi.

SIGNAUX
- Le repo ClientDelta a une dependance (auth-lib) avec une
  CVE publiee hier. Severite moyenne. A evaluer.

SUGGESTION
Lancer les tests unitaires en premier ce matin.
S'ils passent, vous aurez du concret pour le call de 14h.
La documentation peut se faire apres.
```

## Exemples de MAUVAIS briefings

### Trop generique

```
Bonjour ! Vous avez une journee chargee avec 5 reunions
et 12 taches en attente. Je vous souhaite une excellente
journee productive !
```

Probleme : aucun contexte, aucune priorisation, aucune action concrete. L'agent ne connait pas assez le contexte (USER.md, knowledge/, MEMORY.md vides ou insuffisants).

### Trop long

```
[45 lignes detaillant chaque email recu, chaque tache,
chaque evenement avec 5 lignes de contexte chacun]
```

Probleme : le briefing est un rapport, pas un briefing. Si vous avez besoin de 5 minutes pour le lire, il est trop long. Maximum 30 lignes.

### Faux contexte

```
FOCUS : Preparer la presentation pour le board.
[Vous n'avez pas de board. L'agent invente.]
```

Probleme : l'agent "comble les trous" en inventant. CONSTITUTION.md doit interdire explicitement l'invention de faits.

## Etape par etape

1. Configurez le cron briefing-matin (section 3.15)
2. Utilisez le prompt exact ci-dessus
3. Lisez le premier briefing et evaluez :
   - Le focus est-il correct ?
   - Le contexte des reunions est-il pertinent ?
   - Les actions sont-elles concretes ?
   - La suggestion est-elle utile ?
4. Si non, identifiez la cause en amont (USER.md ? MEMORY.md ? sources ?)
5. Ajustez la config, pas le prompt
6. Reperez pendant 5 jours avant de considerer le briefing comme stable

## Erreurs courantes

**Ajuster le prompt au lieu de la config** : Le briefing est plat mais vous reecrivez le prompt 10 fois. Le probleme n'est pas le prompt. C'est que les sources sont vides.

**Briefing le weekend** : Si vous ne travaillez pas le weekend, desactivez le cron. Un briefing vide le samedi crée du bruit.

**Pas de section SIGNAUX** : Les signaux sont la valeur ajoutee de l'agent. Ce que VOUS auriez rate parce que c'est enfoui dans un email ou un calendrier. Sans cette section, l'agent est un simple lecteur de programme.

**Formules de politesse** : "Bonjour, j'espere que vous allez bien." Perte de place. Le briefing est un outil, pas une conversation.

## Verification

- [ ] Cron briefing-matin actif
- [ ] Prompt precis avec les 5 sections (focus, agenda, a traiter, signaux, suggestion)
- [ ] Maximum 30 lignes
- [ ] Le focus est specifique (pas generique)
- [ ] Le contexte des reunions croise USER.md et knowledge/
- [ ] Les suggestions sont concretes et actionnables
- [ ] Pas de formules de politesse
- [ ] Si le briefing est plat : diagnostic en amont (USER.md, MEMORY.md, sources)
