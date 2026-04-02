---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.4 -- AGENTS.md : le registre des agents

## Contexte

Quand vous n'avez qu'un seul agent, AGENTS.md semble superflu. Des que vous en avez deux, il devient indispensable.

AGENTS.md est le registre central. Il repond a trois questions :
- Quels agents existent ?
- Que fait chacun ?
- Dans quel ordre demarrent-ils ?

Meme avec un seul agent, AGENTS.md clarifie la boot sequence : l'ordre dans lequel l'agent lit ses fichiers de configuration au demarrage.

## Ce que AGENTS.md contient

- La liste des agents avec leur role
- Le modele utilise par chacun
- Les permissions de chaque agent
- La boot sequence (ordre de lecture des fichiers)
- Les dependances entre agents (si multi-agents)

## Boot sequence : l'ordre de lecture

Quand l'agent demarre une session, il lit ses fichiers de configuration dans un ordre precis. Cet ordre compte : les fichiers lus en premier ont plus de poids.

Sequence recommandee :

```
1. SOUL.md        -- Qui suis-je ?
2. USER.md        -- Pour qui je travaille ?
3. CONSTITUTION.md -- Quelles sont mes regles ?
4. AGENTS.md      -- Qui d'autre existe ? Quel est mon role specifique ?
5. MEMORY.md      -- Que s'est-il passe recemment ?
6. knowledge/     -- Que dois-je savoir de plus ?
```

Pourquoi cet ordre :
- L'identite (SOUL.md) cadre tout le reste
- Le profil utilisateur (USER.md) oriente les reponses
- Les regles (CONSTITUTION.md) definissent les limites
- Le registre (AGENTS.md) situe l'agent dans l'ensemble
- La memoire (MEMORY.md) donne le contexte recent
- Les connaissances (knowledge/) completent au besoin

## Etape par etape

### 1. Lister vos agents

Meme si vous n'en avez qu'un, documentez-le.

### 2. Definir le role de chacun

Un role = une phrase. Si vous avez besoin de plus, l'agent fait probablement trop de choses.

### 3. Assigner les permissions

Chaque agent a ses propres niveaux de la pyramide des droits (section 3.1).

### 4. Documenter la boot sequence

Listez l'ordre de lecture des fichiers pour chaque agent.

### 5. Definir les canaux de communication inter-agents

Si vous avez plusieurs agents, comment communiquent-ils ? Via des fichiers partages ? Via MEMORY.md ? Via un bus de messages ?

## Template AGENTS.md

```markdown
# AGENTS.md

## Agent principal

| Champ | Valeur |
|-------|--------|
| Nom | [Nom defini dans SOUL.md] |
| Role | [Role en une phrase] |
| Modele | [claude-opus-4 / claude-sonnet-4 / autre] |
| Workspace | [chemin du workspace] |
| Statut | actif |

### Permissions
- Lecture : tout
- Ecriture : MEMORY.md, knowledge/, brouillons
- Action externe : validation requise

### Boot sequence
1. SOUL.md
2. USER.md
3. CONSTITUTION.md
4. AGENTS.md
5. MEMORY.md
6. knowledge/*.md

---

## Agent secondaire (si applicable)

| Champ | Valeur |
|-------|--------|
| Nom | [Nom] |
| Role | [Role en une phrase] |
| Modele | [modele] |
| Workspace | [chemin du workspace] |
| Statut | actif / inactif |

### Permissions
- Lecture : [scope restreint]
- Ecriture : [scope restreint]
- Action externe : [regles specifiques]

### Boot sequence
1. SOUL.md (propre a cet agent)
2. USER.md (partage)
3. CONSTITUTION.md (propre a cet agent)
4. AGENTS.md (partage)
5. MEMORY.md (partage ou propre)

---

## Communication inter-agents

| De | Vers | Canal | Contenu |
|----|------|-------|---------|
| [Agent 1] | [Agent 2] | [MEMORY.md / fichier / API] | [Type d'information] |

## Notes
- [Regles supplementaires, contraintes, historique des changements]
```

## Erreurs courantes

**Pas de AGENTS.md avec un seul agent** : Vous pensez que c'est inutile. Puis vous ajoutez un deuxieme agent 3 mois plus tard et vous ne savez plus quelle est la boot sequence du premier.

**Boot sequence non documentee** : L'agent lit les fichiers dans un ordre par defaut qui peut ne pas correspondre a votre intention. Soyez explicite.

**Permissions identiques pour tous les agents** : Si deux agents ont les memes permissions, ils vont probablement se marcher dessus. Differenciez.

**Oublier le statut** : Un agent desactive mais encore dans AGENTS.md peut creer de la confusion. Marquez-le "inactif" ou supprimez-le.

## Verification

- [ ] Chaque agent a une entree dans AGENTS.md
- [ ] Role defini en une phrase par agent
- [ ] Modele specifie pour chaque agent
- [ ] Permissions explicites (lecture, ecriture, action externe)
- [ ] Boot sequence documentee
- [ ] Si multi-agents : canaux de communication definis
