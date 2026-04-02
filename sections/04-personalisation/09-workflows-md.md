---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.9 -- WORKFLOWS.md

## Contexte

Un workflow documente, c'est une routine que n'importe qui (vous, un autre dev, un autre agent) peut executer sans deviner les etapes. Si la procedure est dans votre tete, elle meurt quand vous changez d'outil ou quand vous oubliez.

WORKFLOWS.md est le fichier qui contient toutes vos procedures standardisees. L'agent le lit, l'execute, et le met a jour quand une etape change.

## Format standardise

Chaque workflow suit la meme structure :

```markdown
## [Nom du workflow]

**Declencheur :** Quand ce workflow se lance (manuellement, cron, evenement).
**Niveau de confiance :** 1 (dry run) / 2 (avec validation) / 3 (autonome)
**Derniere verification :** YYYY-MM-DD

### Prerequis
- [Ce qui doit etre vrai avant de commencer]
- [Acces necessaires]

### Etapes
1. [Action concrete avec la commande exacte]
2. [Action suivante]
3. [Action suivante]

### Verification
- [ ] [Comment savoir que ca a marche]
- [ ] [Test de validation]

### En cas d'erreur
- Si [erreur A] : [action corrective]
- Si [erreur B] : [action corrective]
- Si inconnu : arreter et signaler.
```

## Exemples concrets

### Deploiement cockpit

```markdown
## Deployer cockpit

**Declencheur :** Manuel, apres merge sur main.
**Niveau de confiance :** 2 (avec validation)
**Derniere verification :** 2026-03-28

### Prerequis
- Branch main a jour (git pull)
- Tests locaux passes
- Aucun deployment en cours

### Etapes
1. `cd /opt/cockpit && git pull origin main`
2. `docker compose build --no-cache`
3. `docker compose down && docker compose up -d`
4. Attendre 10 secondes.
5. `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000`
   Attendu : 200

### Verification
- [ ] curl retourne 200
- [ ] `docker ps` montre le container "Up"
- [ ] Les logs ne contiennent pas d'erreur : `docker logs cockpit --tail 20`

### En cas d'erreur
- Si build echoue : verifier les dependances dans package.json.
- Si le container ne demarre pas : `docker logs cockpit` pour diagnostic.
- Si curl retourne 502 : le service met du temps a demarrer, attendre 30s et retester.
- Si inconnu : rollback avec `git checkout HEAD~1 && docker compose up -d`
```

### Creer une tache

```markdown
## Creer une tache

**Declencheur :** Manuel.
**Niveau de confiance :** 3 (autonome)
**Derniere verification :** 2026-03-25

### Prerequis
- Acces PostgreSQL

### Etapes
1. `./tasks.sh add "Titre de la tache" [priority] [project] [deadline]`
2. Confirmer la creation : `./tasks.sh list todo`

### Verification
- [ ] La tache apparait dans la liste avec le bon statut et la bonne priorite.

### En cas d'erreur
- Si connexion PostgreSQL echoue : verifier que le service tourne (`systemctl status postgresql`).
```

### Rotation des secrets

```markdown
## Rotation des secrets

**Declencheur :** Mensuel (1er du mois) ou apres incident de securite.
**Niveau de confiance :** 2 (avec validation)
**Derniere verification :** 2026-03-01

### Prerequis
- Acces Vault
- Acces root/sudo
- Fenetre de maintenance (pas de deploiement en cours)

### Etapes
1. Generer le nouveau secret : `openssl rand -hex 32`
2. Stocker dans Vault : `vault kv put secret/[service] key=[nouveau_secret]`
3. Mettre a jour la config du service.
4. Redemarrer le service : `docker compose restart [service]`
5. Tester le service : `curl -s http://localhost:[port]/health`
6. Logger la rotation : `echo "$(date) [service] secret rotated" >> /var/log/secret-rotation.log`

### Verification
- [ ] Le service repond correctement avec le nouveau secret.
- [ ] L'ancien secret ne fonctionne plus.
- [ ] La rotation est loggee.

### En cas d'erreur
- Si le service ne demarre pas : restaurer l'ancien secret depuis Vault (version precedente).
- Si inconnu : ne pas continuer les autres rotations, diagnostiquer d'abord.
```

## Organiser le fichier

Un seul fichier WORKFLOWS.md avec une table des matieres :

```markdown
# WORKFLOWS.md

## Table des matieres
1. [Deployer cockpit](#deployer-cockpit)
2. [Creer une tache](#creer-une-tache)
3. [Rotation des secrets](#rotation-des-secrets)
4. [Health check quotidien](#health-check-quotidien)
5. [Backup base de donnees](#backup-base-de-donnees)
```

Quand le fichier depasse 500 lignes, decoupez en fichiers separes dans un dossier `workflows/`.

## Erreurs courantes

**Pas de section "En cas d'erreur".** Tout va bien jusqu'au jour ou ca casse. Sans procedure de rollback, vous improvisez sous stress.

**Commandes approximatives.** "Deployer le service" au lieu de la commande exacte. Si la commande n'est pas copiable-collable, elle n'est pas assez precise.

**Ne jamais mettre a jour.** Le workflow date de 6 mois, les chemins ont change, une etape a ete ajoutee a l'oral. Verifiez chaque workflow au moins une fois par mois.

## Etapes

1. Creez `WORKFLOWS.md` a la racine du projet.
2. Documentez votre workflow le plus frequent (celui que vous faites chaque jour).
3. Testez : donnez le workflow a l'agent et demandez-lui de l'executer en dry run.
4. Corrigez les etapes manquantes ou imprecises.
5. Ajoutez un workflow par semaine jusqu'a ce que vos routines principales soient couvertes.

## Verification

- [ ] WORKFLOWS.md existe et contient au moins 3 workflows.
- [ ] Chaque workflow suit le format standardise (prerequis, etapes, verification, erreur).
- [ ] Les commandes sont exactes et copiables-collables.
- [ ] Chaque workflow a ete teste en dry run par l'agent.
- [ ] La date de derniere verification est renseignee et recente (< 1 mois).
