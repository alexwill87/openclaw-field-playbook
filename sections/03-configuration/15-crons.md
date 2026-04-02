---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.15 -- Les crons : automatisations planifiees

## Contexte

Un agent reactif repond quand vous lui parlez. Un agent proactif agit sans que vous le demandiez, a des moments definis.

Les crons sont le mecanisme de proactivite. Un cron = une action planifiee qui se declenche a heure fixe. Le briefing du matin a 7h. Le recap du soir a 18h. Le triage email toutes les 2 heures. Le heartbeat qui verifie que tout fonctionne.

## Les 4 crons essentiels

### 1. Briefing matin

Le plus important. Detail complet dans la section 3.16.

```
openclaw cron add --name "briefing-matin" \
  --schedule "0 7 * * 1-5" \
  --prompt "Genere mon briefing du matin selon le format defini dans CONSTITUTION.md"
```

Declenchement : lundi au vendredi, 7h00.

### 2. Recap soir

Resume de la journee. Ce qui a ete fait, ce qui reste, ce qui a change.

```
openclaw cron add --name "recap-soir" \
  --schedule "0 18 * * 1-5" \
  --prompt "Resume de la journee : decisions prises, taches completees, 
  points en attente. Mets a jour MEMORY.md avec ce qui doit etre retenu."
```

Declenchement : lundi au vendredi, 18h00.

Le recap soir fait le lien avec le briefing du lendemain. Ce que le recap capture le soir, le briefing le presente le matin.

### 3. Triage email

Classement periodique des emails entrants.

```
openclaw cron add --name "triage-email" \
  --schedule "0 9,13,17 * * 1-5" \
  --prompt "Trie les emails recus depuis le dernier triage. 
  Classe en urgent/a-traiter/informatif. 
  Notifie-moi uniquement s'il y a des urgents."
```

Declenchement : 3 fois par jour (9h, 13h, 17h).

Note : ne triez pas toutes les 30 minutes. L'email n'est pas un chat. 3 fois par jour suffit pour la grande majorite des contextes.

### 4. Heartbeat

Verification que l'agent et ses connexions fonctionnent.

```
openclaw cron add --name "heartbeat" \
  --schedule "0 6 * * *" \
  --prompt "Verifie que toutes les connexions sont actives 
  (calendrier, email, taches). Signale uniquement les problemes."
```

Declenchement : tous les jours, 6h00 (avant le briefing).

Le heartbeat est silencieux quand tout va bien. Il ne vous notifie que si quelque chose est casse.

## Configuration

### Syntaxe cron

```
openclaw cron add --name "[nom]" \
  --schedule "[expression cron]" \
  --prompt "[instruction pour l'agent]"
```

Expressions cron courantes :

| Expression | Signification |
|---|---|
| `0 7 * * 1-5` | Lundi-vendredi a 7h |
| `0 7 * * *` | Tous les jours a 7h |
| `0 */2 * * 1-5` | Toutes les 2h, lun-ven |
| `0 9,13,17 * * 1-5` | 9h, 13h, 17h, lun-ven |
| `30 8 * * 1` | Lundi a 8h30 |

### Gestion des crons

```
openclaw cron list              # Voir tous les crons actifs
openclaw cron pause [nom]       # Mettre en pause
openclaw cron resume [nom]      # Reactiver
openclaw cron remove [nom]      # Supprimer
openclaw cron logs [nom]        # Voir les logs d'execution
```

## Commencer par UN seul cron

Regle de Steinberg appliquee aux crons : commencez par un seul. Le briefing matin.

Pourquoi :
- Vous validez que le mecanisme de cron fonctionne
- Vous verifiez que le prompt produit un resultat utile
- Vous ajustez l'heure et le contenu avant d'en ajouter d'autres
- Un cron mal configure qui tourne 3 fois par jour, c'est 3 fois plus de bruit qu'un seul

Ordre d'ajout recommande :

```
Semaine 1 : briefing matin
Semaine 2 : recap soir (si le briefing est valide)
Semaine 3 : triage email (si l'email est connecte)
Semaine 4 : heartbeat
```

## Etape par etape

1. Creez le cron "briefing-matin" avec le prompt de la section 3.16
2. Verifiez le premier briefing le lendemain matin
3. Ajustez le prompt si le resultat n'est pas satisfaisant
4. Vivez avec pendant 5 jours
5. Ajoutez le cron suivant seulement quand le premier est stable

## Erreurs courantes

**Trop de crons d'entree** : 8 crons des le premier jour. Vous etes noye de notifications. Commencez par 1.

**Crons trop frequents** : Triage email toutes les 15 minutes. L'agent consomme des tokens pour des resultats quasi identiques. Reduisez la frequence.

**Prompts de cron trop vagues** : "Fais un point." Un point sur quoi ? Avec quelles sources ? Quel format ? Soyez aussi precis dans un prompt de cron que dans une interaction directe.

**Ne pas lire les logs** : Un cron qui echoue silencieusement pendant 2 semaines. Verifiez les logs regulierement, au moins au debut.

**Pas de heartbeat** : Tout fonctionne jusqu'au jour ou le token API expire et le briefing est vide. Le heartbeat detecte les problemes avant qu'ils impactent votre travail.

## Verification

- [ ] Au moins 1 cron actif (briefing matin recommande)
- [ ] Le prompt du cron est precis et teste
- [ ] L'heure de declenchement correspond a votre rythme
- [ ] Les logs sont accessibles et verifies
- [ ] Pas plus de 2 crons actifs la premiere semaine
- [ ] Heartbeat prevu (meme s'il est ajoute plus tard)
