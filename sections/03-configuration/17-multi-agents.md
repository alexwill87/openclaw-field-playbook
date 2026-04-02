---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.17 -- Architecture multi-agents

## Contexte

Un seul agent couvre 90% des besoins. Ce chapitre est pour les 10% restants.

NE COMMENCEZ PAS PAR LA. Si vous lisez cette section avant d'avoir un agent principal stable et utile pendant au moins 4 semaines, fermez cette page et revenez plus tard.

Le multi-agents resout un probleme precis : un seul agent ne peut pas tout faire bien. Pas parce qu'il manque de capacite, mais parce que des roles differents demandent des postures, des permissions et des connaissances differentes.

## Quand un seul agent ne suffit plus

Signes qu'il est temps de passer au multi-agents :

- SOUL.md contient des instructions contradictoires ("sois direct" ET "sois diplomatique selon le contexte")
- CONSTITUTION.md a des regles qui s'appliquent a certaines taches mais pas d'autres
- knowledge/ melange des domaines qui n'ont rien a voir (infra technique ET communication client)
- L'agent change de "personnalite" selon le sujet, et le resultat est inconsistant

Signes que ce n'est PAS le moment :

- Vous n'avez pas encore de briefing matin stable
- USER.md n'est pas complet
- Vous n'avez connecte aucune source
- Vous utilisez l'agent moins de 5 fois par semaine

## Agents specialises

Le modele recommande : un agent principal (generaliste) et des agents specialises (experts dans un domaine).

### Exemples d'architecture

**Freelance technique** :
```
Agent principal : "Axel" -- gestion quotidienne, briefing, triage
Agent dev : "K8" -- code, infrastructure, deployments
```

**Dirigeant PME** :
```
Agent principal : "Clara" -- briefing, email, agenda
Agent commercial : "Hugo" -- CRM, pipeline, relances
Agent ops : "Max" -- facturation, fournisseurs, logistique
```

**Equipe produit** :
```
Agent principal : "PM" -- priorisation, roadmap, communication
Agent technique : "Dev" -- code review, monitoring, alertes
Agent data : "Ana" -- metriques, rapports, A/B tests
```

### Quand ajouter un agent specialise

Regle : ajoutez un agent specialise quand une ACTIVITE recurrente necessite :
- Un ton different de l'agent principal
- Des permissions differentes
- Des connaissances specifiques que l'agent principal n'a pas besoin de charger a chaque session

Si les trois criteres ne sont pas reunis, un seul agent avec un knowledge/ bien organise suffit.

## Isolation des workspaces

Chaque agent a son propre workspace avec ses propres fichiers de configuration :

```
workspaces/
  principal/
    SOUL.md              -- personnalite de l'agent principal
    USER.md              -- partage (symlink)
    CONSTITUTION.md      -- regles de l'agent principal
    MEMORY.md            -- memoire de l'agent principal
    knowledge/           -- connaissances generales
  dev/
    SOUL.md              -- personnalite de l'agent dev
    USER.md              -- partage (symlink)
    CONSTITUTION.md      -- regles de l'agent dev
    MEMORY.md            -- memoire de l'agent dev
    knowledge/           -- connaissances techniques
  commercial/
    SOUL.md              -- personnalite de l'agent commercial
    USER.md              -- partage (symlink)
    CONSTITUTION.md      -- regles de l'agent commercial
    MEMORY.md            -- memoire de l'agent commercial
    knowledge/           -- connaissances business
```

Regles d'isolation :

| Fichier | Partage ? | Raison |
|---------|-----------|--------|
| SOUL.md | Non | Chaque agent a sa propre identite |
| USER.md | Oui (symlink) | Vous etes la meme personne pour tous |
| CONSTITUTION.md | Non | Chaque agent a ses propres regles |
| AGENTS.md | Oui (symlink) | Registre central de tous les agents |
| MEMORY.md | Selon le cas | Partage si besoin de contexte croise |
| knowledge/ | Non | Chaque agent a ses propres connaissances |

## Communication inter-agents

Les agents ne se parlent pas directement. Ils communiquent via des artefacts partages.

### Via MEMORY.md partage

Le plus simple. Un seul MEMORY.md lu par tous les agents.

```
Agent principal note dans MEMORY.md :
"2026-04-01 -- Client Alpha a demande un changement de scope. A evaluer."

Agent dev lit MEMORY.md au demarrage et voit la note.
```

Avantage : simple. Inconvenient : MEMORY.md grossit vite avec plusieurs agents qui ecrivent.

### Via fichiers de liaison

Chaque agent ecrit dans un fichier de sortie que les autres peuvent lire.

```
workspaces/shared/
  principal-output.md    -- ce que l'agent principal veut communiquer
  dev-output.md          -- ce que l'agent dev veut communiquer
  commercial-output.md   -- ce que l'agent commercial veut communiquer
```

Avantage : chaque agent controle ce qu'il partage. Inconvenient : plus de fichiers a gerer.

### Via AGENTS.md

Le registre AGENTS.md definit les canaux de communication :

```markdown
## Communication

| De | Vers | Canal | Quand |
|----|------|-------|-------|
| Principal | Dev | shared/principal-output.md | Quand un sujet technique emerge |
| Dev | Principal | shared/dev-output.md | Apres chaque deploiement |
| Commercial | Principal | shared/commercial-output.md | Quand un deal avance/recule |
```

## Etape par etape

### 1. Validez que c'est necessaire

Relisez les criteres ci-dessus. Si votre agent principal fonctionne bien, n'ajoutez pas de complexite.

### 2. Identifiez le premier agent specialise

Un seul. Pas trois d'un coup. Quel domaine beneficierait le plus d'un agent dedie ?

### 3. Creez le workspace

Copiez la structure. Creez SOUL.md et CONSTITUTION.md specifiques. Liez USER.md et AGENTS.md.

### 4. Definissez la communication

Comment les agents echangent-ils ? MEMORY.md partage ou fichiers de liaison ?

### 5. Testez pendant 2 semaines

Avant d'ajouter un troisieme agent, le deuxieme doit etre stable.

### 6. Documentez dans AGENTS.md

Mettez a jour le registre central avec le nouvel agent.

## Erreurs courantes

**Commencer par le multi-agents** : Vous n'avez meme pas un agent qui fonctionne et vous en deployez trois. Resultats garantis : confusion, tokens gaspilles, abandon.

**Agents qui se chevauchent** : L'agent principal et l'agent commercial traitent tous les deux les emails clients. Qui a raison ? Definissez des perimetres exclusifs.

**Trop d'agents** : 5 agents pour un solo entrepreneur. La gestion des agents devient un travail a plein temps. 2-3 agents maximum pour la plupart des contextes.

**Pas d'isolation** : Tous les agents partagent tout. L'agent dev a acces aux negociations commerciales. L'agent commercial peut deployer du code. Isolez les workspaces.

**Communication non definie** : Les agents ne savent pas ce que les autres ont fait. Pas de fichier partage, pas de MEMORY.md commun. Chaque agent travaille dans sa bulle.

**Oublier de mettre a jour AGENTS.md** : Vous ajoutez un agent mais AGENTS.md n'est pas mis a jour. Les autres agents ne savent pas qu'il existe.

## Verification

- [ ] L'agent principal est stable depuis au moins 4 semaines
- [ ] Le besoin multi-agents est justifie (3 criteres reunis)
- [ ] Maximum 1 agent specialise ajoute a la fois
- [ ] Chaque agent a son workspace isole
- [ ] USER.md et AGENTS.md sont partages (symlinks)
- [ ] SOUL.md et CONSTITUTION.md sont propres a chaque agent
- [ ] La communication inter-agents est definie et documentee
- [ ] AGENTS.md est a jour avec tous les agents
- [ ] 2 semaines de test avant d'ajouter un agent supplementaire
