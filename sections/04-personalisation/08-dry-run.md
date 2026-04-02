---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.8 -- Dry run avant confiance

## Contexte

Vous avez identifie une routine automatisable (section 4.7). Avant de la laisser tourner en autonome, vous la testez. Pas parce que vous ne faites pas confiance a l'agent -- parce que vous ne faites pas confiance a vos propres instructions.

Le dry run revele les trous dans vos procedures. Mieux vaut les decouvrir en mode test qu'en production.

## Les 3 niveaux de confiance

### Niveau 1 : lecture seule ("montre-moi")

L'agent execute la routine mais ne fait rien. Il affiche ce qu'il ferait.

```
Prompt : "Fais le health check en mode dry run. 
Montre-moi chaque commande que tu lancerais et ce que tu verifierais,
mais n'execute rien."
```

Resultat attendu :

```
Health check dry run :
1. Je lancerais : docker ps --format "{{.Names}} {{.Status}}"
   Je verifierais : tous les containers sont "Up"
2. Je lancerais : curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
   Je verifierais : code 200
3. Je lancerais : df -h /
   Je verifierais : usage < 80%
4. En cas de probleme, j'enverrais une alerte Telegram.

Aucune action executee. Mode dry run.
```

Vous validez : les commandes sont correctes ? Les seuils sont bons ? Il manque quelque chose ?

### Niveau 2 : action + validation ("fais et montre")

L'agent execute mais demande validation avant chaque action consequente.

```
Prompt : "Fais le health check. Execute les diagnostics.
Si tout est OK, dis-le. Si quelque chose est KO, montre-moi 
ce que tu ferais mais attends ma validation avant d'agir."
```

C'est le mode entrainement. L'agent fait le travail de diagnostic (sans risque), mais ne prend aucune action corrective sans votre feu vert.

### Niveau 3 : autonome ("fais tout")

L'agent execute la routine complete, prend les actions correctives si necessaire, et rend compte apres.

```
Prompt : "Health check quotidien. Si un service est down, 
redemarre-le. Si le disque depasse 80%, nettoie les logs > 30j. 
Envoie-moi le resume par Telegram."
```

Vous ne passez au niveau 3 que quand les niveaux 1 et 2 ont fonctionne sans probleme pendant au moins une semaine.

## Le calendrier de montee en confiance

| Semaine | Niveau | Ce que vous faites |
|---|---|---|
| 1 | Lecture seule | Verifiez chaque commande. Corrigez les procedures. |
| 2 | Action + validation | Laissez l'agent diagnostiquer. Validez les corrections. |
| 3 | Autonome avec rapport | L'agent agit seul mais vous lisez le rapport chaque jour. |
| 4+ | Autonome silencieux | L'agent agit seul et ne signale que les anomalies. |

Ce calendrier est un minimum. Pour les routines a risque (deploiement, suppression de donnees), doublez chaque phase.

## Prompt de test

Pour tester une routine avant de l'automatiser :

```
Je veux automatiser cette routine : [description].
Etapes prevues :
1. [etape 1]
2. [etape 2]
3. [etape 3]

Execute en mode dry run. Pour chaque etape :
- Montre la commande exacte.
- Dis ce que tu verifies.
- Dis ce que tu ferais si le resultat est anormal.
N'execute rien.
```

## Erreurs courantes

**Sauter directement au niveau 3.** "Ca a l'air simple, pas besoin de tester." Puis l'agent redemarre le mauvais container ou supprime les mauvais logs. Toujours tester.

**Rester bloque au niveau 1.** Vous faites des dry runs depuis 3 mois sans jamais passer a l'action. Le dry run est un outil de transition, pas un mode permanent.

**Ne pas documenter les decouvertes.** Le dry run revele que votre procedure oublie une etape. Vous corrigez a l'oral mais pas dans le workflow. La prochaine fois, meme erreur. Ecrivez les corrections dans WORKFLOWS.md (section 4.9).

## Etapes

1. Choisissez une routine identifiee en section 4.7.
2. Demandez un dry run (niveau 1).
3. Verifiez : commandes correctes ? Seuils bons ? Etapes manquantes ?
4. Corrigez la procedure si necessaire.
5. Passez au niveau 2 pendant une semaine.
6. Si tout est OK, passez au niveau 3.

## Verification

- [ ] Chaque nouvelle routine passe par le niveau 1 avant execution.
- [ ] Les decouvertes du dry run sont documentees dans WORKFLOWS.md.
- [ ] Le passage au niveau suivant est base sur au moins une semaine sans probleme.
- [ ] Les routines a risque ont un calendrier de montee en confiance double.
