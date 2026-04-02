---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.11 -- La confiance est une configuration

## Contexte

La confiance envers votre agent n'est pas un sentiment. C'est une configuration. Chaque action a un niveau de risque, et chaque niveau de risque a des regles. Si vous ne les ecrivez pas, vous allez osciller entre trop de confiance ("fais tout") et pas assez ("montre-moi tout").

Steinberg propose une pyramide : plus l'action est risquee, plus le controle est strict.

## La pyramide des droits

### Niveau 0 : lecture seule

L'agent peut lire mais ne peut rien modifier.

Actions : consulter des fichiers, lire des logs, afficher des statuts, faire des calculs.

Controle : aucun necessaire. Risque zero.

```
Exemples :
- cat, ls, docker ps, git log
- SELECT sur la base de donnees
- Lire la documentation
```

### Niveau 1 : actions reversibles

L'agent peut agir, mais l'action est facilement annulable.

Actions : creer des fichiers, ecrire dans un fichier temporaire, creer une branche git, ajouter une tache.

Controle : l'agent agit et rend compte. Vous verifiez apres.

```
Exemples :
- git checkout -b feature/xxx
- Creer un fichier dans /tmp
- INSERT dans la table tasks
- Ecrire un brouillon
```

### Niveau 2 : actions consequentes

L'agent peut agir mais demande validation avant.

Actions : modifier des fichiers de config, deployer un service, modifier la base de donnees, envoyer un message.

Controle : l'agent propose l'action exacte et attend un "go" explicite.

```
Exemples :
- docker compose restart
- UPDATE/DELETE sur la base de donnees
- Modifier .env ou docker-compose.yml
- git push
- Envoyer un message Telegram a un tiers
```

### Niveau 3 : actions interdites

L'agent ne peut JAMAIS faire ca, meme avec validation.

Actions : supprimer des donnees de production irrecuperable, push --force sur main, modifier les secrets sans procedure, exposer des credentials.

Controle : interdit dans le boundary prompt (section 4.12). L'agent doit refuser meme si vous le demandez.

```
Exemples :
- DROP TABLE en production
- git push --force origin main
- Afficher un mot de passe en clair dans les logs
- Modifier les regles de firewall
- Supprimer un backup
```

## Ecrire les niveaux dans CONSTITUTION.md

Creez un fichier `CONSTITUTION.md` qui definit les niveaux de facon explicite :

```markdown
# CONSTITUTION.md — Niveaux de confiance

## Niveau 0 : lecture seule (libre)
- Lire tout fichier du projet
- Consulter les logs
- Requetes SELECT sur la base
- Afficher les statuts

## Niveau 1 : reversible (agir + rendre compte)
- Creer des fichiers non-critiques
- Creer des branches git
- Ajouter des taches
- Generer des brouillons

## Niveau 2 : consequent (demander avant)
- Modifier des fichiers de configuration
- Deployer un service
- Modifier la base de donnees (UPDATE, DELETE)
- Push sur une branche
- Envoyer des communications

## Niveau 3 : interdit (refuser toujours)
- DROP TABLE / DELETE sans WHERE
- Push --force sur main
- Modifier les secrets hors procedure
- Exposer des credentials
- Supprimer des backups
- Modifier le firewall
```

Ajoutez dans le system prompt :

```
Lis et respecte CONSTITUTION.md pour les niveaux de confiance.
```

## Faire evoluer les niveaux

Les niveaux ne sont pas figes. Quand un workflow a ete teste et fonctionne bien pendant un mois, vous pouvez baisser son niveau de controle :

- Deploiement cockpit : niveau 2 -> niveau 1 (apres 10 deploiements reussis).
- Rotation secrets : reste niveau 2 (risque inherent, pas de raccourci).
- Health check : niveau 1 -> niveau 0 equivalent (cron automatique).

Documentez chaque changement de niveau avec la date et la raison dans CONSTITUTION.md.

## Erreurs courantes

**Pas de niveaux definis.** L'agent improvise. Parfois il demande, parfois il agit. Inconsistant et stressant.

**Tout au niveau 2.** Chaque action demande validation. Vous passez votre temps a valider des trucs sans risque. Fatigue decisionnelle.

**Niveaux mais pas appliques.** CONSTITUTION.md existe mais le system prompt n'y fait pas reference. L'agent ne le lit pas.

**Baisser le niveau trop vite.** Un workflow fonctionne 3 fois et vous le passez en autonome. 3 reussites ne prouvent pas la fiabilite. Minimum 10 executions sans probleme.

## Etapes

1. Listez les 10 actions les plus frequentes de votre agent.
2. Classez chacune dans un niveau (0, 1, 2, 3).
3. Creez `CONSTITUTION.md` avec cette classification.
4. Ajoutez la reference dans le system prompt.
5. Testez pendant 2 semaines : l'agent respecte-t-il les niveaux ?
6. Ajustez si necessaire.

## Verification

- [ ] CONSTITUTION.md existe avec les 4 niveaux definis.
- [ ] Chaque action frequente est classee dans un niveau.
- [ ] Le system prompt reference CONSTITUTION.md.
- [ ] Le niveau 3 contient au moins 5 interdictions explicites.
- [ ] Les changements de niveau sont dates et justifies.
