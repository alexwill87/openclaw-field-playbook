---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.5 -- Comment les taches se font

## Contexte

Avoir un systeme de taches ne suffit pas. Ce qui compte, c'est le workflow : qui propose quoi, qui decide, qui execute. Si vous ne definissez pas ce workflow, l'agent va soit tout faire sans demander (dangereux), soit ne rien faire sans qu'on lui dise (inutile).

Le bon equilibre, selon le modele Steinberg : l'agent propose, vous decidez.

## Le workflow propose/decide

### 1. L'agent propose

L'agent analyse les taches en cours, les deadlines, le contexte. Il propose :

```
Bonjour. 3 taches prioritaires aujourd'hui :

1. [URGENT] Migration S3 — en retard de 2 jours. 
   Proposition : finir le script de transfert, tester, deployer.

2. [NORMAL] Doc API /users — pas de deadline, mais bloque l'onboarding dev.
   Proposition : generer le squelette depuis le code, vous completez.

3. [INFO] Certificat SSL expire dans 43 jours.
   Proposition : planifier le renouvellement pour semaine prochaine.

Quoi en premier ?
```

### 2. Vous decidez

Vous ne validez pas tout en bloc. Vous triez :

- "1 : oui, commence par le script."
- "2 : pas aujourd'hui."
- "3 : ajoute au planning semaine prochaine."

C'est du triage. L'agent fait le travail de preparation (analyser, prioriser, formuler). Vous gardez le jugement (decider, prioriser selon vos contraintes reelles).

### 3. L'agent execute et rend compte

Apres validation, l'agent execute et met a jour le statut :

```
Migration S3 : script de transfert termine. 
Test de restauration : OK (3 fichiers, 12s).
Statut mis a jour : in_progress -> done.

Prochaine tache ?
```

## Triage sans deleguer le jugement

Le piege : laisser l'agent decider de la priorite. Il n'a pas votre contexte complet. Il ne sait pas que le client X appelle demain, que vous etes fatigue, que le budget est serre.

Ce que l'agent peut faire :
- Ordonner par deadline.
- Signaler les retards.
- Identifier les dependances.
- Proposer un plan.

Ce que vous devez faire :
- Valider ou reordonner.
- Decider de reporter ou annuler.
- Juger de l'urgence reelle (pas la deadline theorique).

## Les taches nourrissent le briefing

Chaque tache terminee enrichit le contexte. Apres une semaine, votre agent peut dire :

```
Cette semaine : 8 taches terminees, 2 reportees, 1 bloquee.
Le pattern : les taches infra se terminent vite, les taches doc trainent.
Suggestion : bloquer 2h doc le jeudi.
```

Ce feedback n'est possible que si les taches sont tracees avec leur statut et leurs dates. Un fichier texte sans dates ne permet pas ca.

## Format minimal d'une tache

Pour que le workflow fonctionne, chaque tache a besoin de :

```
- Titre (quoi)
- Statut (todo / in_progress / done / blocked)
- Priorite (high / medium / low)
- Date de creation
- Date de deadline (optionnel)
- Notes (optionnel — contexte, blocages, decisions)
```

Pas besoin de plus au debut. Ajoutez des champs quand le besoin se manifeste, pas avant.

## Erreurs courantes

**L'agent decide seul.** Il ferme une tache, en ouvre une autre, change les priorites. Vous decouvrez les changements apres coup. Solution : regle dans le system prompt -- "Ne change jamais le statut d'une tache sans validation."

**Vous micro-managez.** Chaque sous-etape doit etre validee. L'agent passe plus de temps a attendre qu'a executer. Solution : definir des niveaux de confiance (voir section 4.11).

**Pas de rendu de compte.** L'agent execute mais ne dit pas ce qu'il a fait. Vous ne savez pas ou on en est. Solution : exiger un resume apres chaque tache completee.

## Etapes

1. Ajoutez cette regle au system prompt : "Propose les taches, ne les execute pas sans validation."
2. Demandez un briefing quotidien : "Quelles taches prioritaires aujourd'hui ?"
3. Pratiquez le triage : validez, reportez ou annulez chaque proposition.
4. Apres chaque execution, verifiez que le statut est mis a jour.
5. En fin de semaine, demandez un resume.

## Verification

- [ ] L'agent propose sans executer automatiquement.
- [ ] Vous validez chaque tache avant execution.
- [ ] Les statuts sont mis a jour apres chaque action.
- [ ] Un resume hebdomadaire est possible a partir des donnees.
- [ ] L'agent ne change jamais une priorite sans votre accord.
