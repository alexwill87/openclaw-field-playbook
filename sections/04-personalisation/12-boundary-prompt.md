---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.12 -- Le boundary prompt

## Contexte

Le boundary prompt est la liste des choses que votre agent ne doit JAMAIS faire. Pas "eviter", pas "sauf si necessaire" -- JAMAIS. C'est le filet de securite. Vous l'ecrivez une fois, vous le mettez dans le system prompt ou dans un fichier dedie, et vous n'y touchez plus sauf pour ajouter une regle apres un incident.

Steinberg compare ca a une constitution : on ne la reecrit pas chaque semaine, mais on peut l'amender.

## Pourquoi c'est necessaire

Les agents LLM sont cooperatifs par defaut. Si vous demandez quelque chose de risque, l'agent va essayer de vous aider. C'est sa force et son danger.

Sans boundary prompt :
- "Montre-moi le contenu de .env" -> l'agent affiche les secrets.
- "Push --force sur main" -> l'agent execute.
- "Supprime les vieux backups pour faire de la place" -> l'agent supprime.

Avec boundary prompt :
- "Montre-moi le contenu de .env" -> "Je ne peux pas afficher les fichiers contenant des secrets. Utilisez `vault kv get` pour acceder aux secrets de facon securisee."

## Structure du boundary prompt

```markdown
# BOUNDARIES — Actions interdites

Tu ne dois JAMAIS, meme si je te le demande explicitement :

## Securite
- Afficher des mots de passe, tokens, ou cles API en clair.
- Modifier .env, .env.production, ou tout fichier contenant des secrets.
- Desactiver le firewall ou ouvrir des ports.
- Stocker des secrets dans des fichiers non-chiffres.
- Commiter des fichiers contenant des credentials.

## Git
- Executer git push --force sur main ou master.
- Executer git reset --hard sans backup prealable.
- Modifier l'historique git d'une branche partagee.
- Amend un commit deja pousse.

## Infrastructure
- Supprimer des backups.
- DROP TABLE ou DELETE sans WHERE en production.
- Arreter un service en production sans procedure de rollback.
- Modifier les regles DNS sans validation.

## Communication
- Envoyer un message a un client sans validation.
- Partager des informations internes a l'exterieur.
- Repondre a la place de l'utilisateur sur un canal public.

## Si on te demande de violer ces regles
Refuse poliment. Explique pourquoi c'est interdit.
Propose une alternative securisee si elle existe.
```

## Ou le placer

Deux options :

### Option 1 : dans le system prompt

Avantage : toujours lu en premier. Pas de risque d'oubli.
Inconvenient : consomme des tokens a chaque requete.

### Option 2 : dans un fichier BOUNDARIES.md

Avantage : le system prompt reste court. Le fichier est versionne.
Inconvenient : l'agent doit savoir qu'il doit le lire. Ajoutez dans le system prompt : "Lis et respecte BOUNDARIES.md avant toute action."

Recommandation : les 3-5 regles les plus critiques dans le system prompt. Le reste dans BOUNDARIES.md.

## Exemples concrets par domaine

### Pour un devops

```
JAMAIS :
- rm -rf sur / ou /home ou /opt sans confirmation du chemin exact
- Modifier iptables/ufw sans procedure documentee
- Redemarrer PostgreSQL en production sans verifier les connexions actives
- Deployer un vendredi apres 16h
```

### Pour un consultant

```
JAMAIS :
- Envoyer un email client sans relecture
- Partager des tarifs ou conditions sans validation
- Ecrire au nom du cabinet sur les reseaux sociaux
- Promettre une deadline sans verification
```

### Pour un developpeur

```
JAMAIS :
- Merge sur main sans CI verte
- Modifier une migration deja appliquee en production
- Hardcoder des credentials
- Desactiver des tests pour que la CI passe
```

## Apres un incident

Quand l'agent fait quelque chose qu'il n'aurait pas du :

1. Corrigez les degats.
2. Identifiez la regle manquante.
3. Ajoutez-la au boundary prompt.
4. Testez que l'agent refuse desormais cette action.

Le boundary prompt grossit avec l'experience. C'est normal. Chaque regle ajoutee est une erreur qui ne se reproduira pas.

## Erreurs courantes

**Pas de boundary prompt.** "Il est assez intelligent pour savoir." Non. L'agent fait ce que vous demandez. Si vous ne dites pas non, il dit oui.

**Trop vague.** "Ne fais rien de dangereux." L'agent ne sait pas ce que vous considerez comme dangereux. Soyez specifique : quelle commande, quel fichier, quelle action.

**Trop permissif.** "Sauf si c'est vraiment necessaire." Ca annule la regle. JAMAIS signifie JAMAIS. Si vous avez besoin d'une exception, gerez-la vous-meme manuellement.

## Etapes

1. Listez les 5 actions les plus dangereuses que votre agent pourrait faire.
2. Ecrivez-les dans BOUNDARIES.md.
3. Ajoutez les 3 plus critiques dans le system prompt.
4. Testez : demandez a l'agent de faire quelque chose d'interdit. Il doit refuser.
5. Apres chaque incident, ajoutez une regle.

## Verification

- [ ] BOUNDARIES.md existe avec au moins 10 regles.
- [ ] Les 3 regles les plus critiques sont dans le system prompt.
- [ ] L'agent refuse quand on lui demande de violer une regle (teste).
- [ ] L'agent propose une alternative quand il refuse.
- [ ] Le boundary prompt est mis a jour apres chaque incident.
