---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.12 -- Quand ajouter un deuxieme agent

## Contexte

Un agent, ca marche bien pour un contexte. Quand le contexte grossit trop -- trop de projets, trop de responsabilites, trop de contexte a maintenir -- la qualite des reponses baisse. C'est le signal qu'il est peut-etre temps d'ajouter un deuxieme agent.

## Signes qu'il est temps

1. **Le system prompt depasse 500 mots** et vous ne pouvez plus condenser sans perdre du contexte critique.

2. **Les domaines sont disjoints.** Votre agent gere a la fois l'infra et la communication client. Ce sont deux competences differentes avec des regles differentes.

3. **Les erreurs de contexte augmentent.** L'agent applique les regles du projet A au projet B. Il confond les clients. Il melange les workflows.

4. **Le cout tokens explose.** Trop de memoire, trop de contexte charge a chaque requete.

5. **Vous passez du temps a recadrer.** "Non, la c'est le projet X, pas Y." Si ca arrive plusieurs fois par semaine, le contexte est trop large.

## Comment structurer

### Option 1 : par domaine

```
Agent 1 : Infrastructure / DevOps
  - Gere : VPS, Docker, PostgreSQL, Vault, backups, monitoring
  - System prompt : technique, commandes, procedures

Agent 2 : Business / Communication
  - Gere : emails clients, documentation, planning, facturation
  - System prompt : ton professionnel, templates, regles business
```

### Option 2 : par projet

```
Agent 1 : Projet Cockpit
  - Gere : tout ce qui concerne cockpit (code, deploy, taches)
  - Contexte : stack cockpit, workflows cockpit

Agent 2 : Projet OpenClaw
  - Gere : redaction, structure, review
  - Contexte : plan du playbook, style guide
```

### Option 3 : par niveau de confiance

```
Agent 1 : Operations (niveau 1-2)
  - Peut agir (dans les limites)
  - Acces bash, Docker, PostgreSQL

Agent 2 : Conseil (niveau 0)
  - Lecture seule
  - Analyse, recommandations, redaction
  - Pas d'acces infrastructure
```

## Isolation

Chaque agent a son propre perimetre. Ne partagez pas tout.

### Ce qu'il faut separer

- **System prompt** : chaque agent a le sien, adapte a son domaine.
- **Memoire** : chaque agent a sa memoire. La memoire de l'agent infra ne contient pas le contexte client.
- **Acces** : l'agent business n'a pas acces a bash. L'agent infra n'a pas acces aux emails.
- **Boundaries** : adaptees au domaine de chaque agent.

### Ce qui peut etre partage

- **Taches** : si les deux agents travaillent sur les memes taches (table PostgreSQL commune).
- **Workflows transversaux** : deploiement qui implique code + infra.
- **Fichiers de reference** : CONSTITUTION.md, BOUNDARIES.md (avec des sections par agent).

### Structure de fichiers

```
~/.claude/
  agent-infra/
    system-prompt.md
    memory/
    boundaries.md
  agent-business/
    system-prompt.md
    memory/
    boundaries.md
  shared/
    CONSTITUTION.md
    TASKS (table PostgreSQL commune)
```

## Communication entre agents

Les agents ne se parlent pas directement. Vous etes le lien.

### Pattern recommande

```
1. Agent Infra detecte un probleme : "Le container cockpit redemarre en boucle."
2. Vous diagnostiquez avec Agent Infra.
3. Si le fix implique du code, vous passez a Agent Business/Code.
4. Vous revenez a Agent Infra pour deployer le fix.
```

### Ce qu'il ne faut PAS faire

- Faire passer des messages d'un agent a l'autre sans les relire. ("Agent 1 dit X, dis-le a Agent 2.") Vous perdez le controle.
- Donner aux deux agents acces au meme canal de communication. Confusion garantie.

## Erreurs courantes

**Ajouter un agent trop tot.** Vous avez 3 taches et 1 projet. Un seul agent suffit largement. N'ajoutez un agent que quand le premier sature.

**Pas d'isolation.** Les deux agents ont les memes acces et la meme memoire. Ils se marchent dessus.

**Trop d'agents.** 4 agents specialises pour un setup solo. Le temps passe a coordonner depasse le temps gagne. Pour la plupart des setups : 1 suffit, 2 maximum.

**Pas de convention de nommage.** Vous ne savez plus quel agent fait quoi. Nommez-les clairement : "agent-infra", "agent-content", pas "agent-1", "agent-2".

## Etapes

1. Identifiez les domaines disjoints dans votre usage actuel.
2. Evaluez : est-ce que la separation resout un probleme reel ?
3. Si oui, creez le deuxieme agent avec un system prompt minimal.
4. Definissez l'isolation (acces, memoire, boundaries).
5. Testez pendant 2 semaines avec les deux agents.
6. Evaluez : la qualite des reponses s'est-elle amelioree ?

## Verification

- [ ] Le besoin d'un deuxieme agent est justifie (au moins 2 signes de la liste).
- [ ] Chaque agent a son propre system prompt et sa propre memoire.
- [ ] Les acces sont separes (l'agent business n'a pas acces a bash, etc.).
- [ ] La communication passe par vous, pas entre agents.
- [ ] Le nombre total d'agents est inferieur ou egal a 2 (sauf besoin demontre).
