---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.6 -- Quand l'agent se trompe

## Contexte

Votre agent va se tromper. Pas "peut-etre" -- va. Les LLM hallucinent, sur-interpretent, appliquent le mauvais contexte. Ce n'est pas un defaut, c'est une propriete. La question n'est pas "comment empecher toute erreur" mais "comment detecter, corriger et prevenir".

## Types d'erreurs

### Hallucination factuelle

L'agent affirme quelque chose de faux avec assurance.

```
Agent : "Votre certificat SSL expire le 15 mai."
Realite : il expire le 15 juin.
```

### Sur-interpretation

L'agent interprete plus que ce que vous avez dit.

```
Vous : "Le deploy a plante."
Agent : "J'ai identifie le probleme : la base de donnees a manque de memoire,
        ce qui a cause un OOM kill du container, probablement lie a une fuite
        memoire dans le dernier commit."
Realite : c'etait une typo dans le docker-compose.yml.
```

### Mauvais contexte

L'agent applique une information d'un contexte a un autre.

```
Vous travaillez sur le projet A.
L'agent applique les regles du projet B.
```

### Execution incorrecte

L'agent fait la bonne chose mais mal.

```
Vous : "Backup la base."
Agent : pg_dump sans compression, dans le mauvais dossier.
```

## Protocole de correction

### 1. Diagnostic

Identifiez le type d'erreur. Utilisez ce prompt :

```
Tu viens de te tromper. Avant de corriger, reponds :
1. Quelle etait l'erreur exacte ?
2. Quel type : hallucination, sur-interpretation, mauvais contexte, execution incorrecte ?
3. Pourquoi l'erreur s'est-elle produite (d'apres toi) ?
```

### 2. Correction

Corrigez les degats d'abord, analysez apres.

- Si l'agent a modifie un fichier : `git diff` pour voir ce qui a change, `git checkout` si necessaire.
- Si l'agent a execute une commande : verifier l'impact (`docker ps`, `psql`, logs).
- Si l'agent a donne une mauvaise information : corrigez le fait dans la memoire.

### 3. Prevention

Apres correction, empecchez la recidive :

- **Hallucination** : ajoutez au prompt -- "Si tu n'es pas sur d'un fait, dis-le. Ne fabrique pas."
- **Sur-interpretation** : utilisez le prompt de Steinberg (voir ci-dessous).
- **Mauvais contexte** : clarifiez quel projet/contexte est actif.
- **Execution incorrecte** : mettez a jour le workflow dans WORKFLOWS.md.

## Le prompt de correction de Steinberg

Quand l'agent sur-interprete, utilisez ce recadrage :

```
Tu surinterpretes. Reformule ta reponse avec ce format :
1. Signal : qu'est-ce que tu as observe factuellement ?
2. Incertitude : qu'est-ce que tu ne sais PAS ?
3. Question pour moi : qu'est-ce que tu aurais besoin de savoir pour conclure ?
```

Exemple :

**Avant (sur-interpretation) :**
```
"Le deploy a plante a cause d'un OOM kill lie a une fuite memoire 
dans le dernier commit. Je recommande de profiler le code et 
d'augmenter la memoire du container."
```

**Apres (recadrage) :**
```
Signal : le container cockpit est passe de "Up" a "Exited" a 14h32.
Incertitude : je ne connais pas la cause. Ca peut etre OOM, erreur de config, 
ou probleme de runtime.
Question : peux-tu me montrer `docker logs cockpit --tail 50` et 
`dmesg | tail -20` pour que je diagnostique ?
```

La difference : le recadrage distingue ce que l'agent sait de ce qu'il suppose. Ca evite les fausses pistes.

## Quand l'erreur est grave

Si l'agent a cause des degats (donnees supprimees, service casse, information envoyee a tort) :

1. **Arreter l'agent.** Ne lui demandez pas de corriger seul.
2. **Evaluer les degats.** Manuellement.
3. **Restaurer si possible.** Backups, git, snapshots.
4. **Documenter l'incident.** Quoi, quand, pourquoi, comment eviter.
5. **Ajouter au boundary prompt.** L'action qui a cause le probleme rejoint la liste des interdictions.

## Erreurs courantes

**Blame l'agent.** L'erreur vient souvent de vos instructions, pas du modele. Prompt vague = reponse vague. Pas de boundary = pas de limite.

**Ignorer l'erreur.** "C'est pas grave, il a a peu pres compris." Les petites erreurs repetees deviennent des grosses erreurs.

**Corriger sans prevenir.** Vous corrigez le tir mais vous n'ajoutez pas de regle. La meme erreur revient la semaine suivante.

**Sur-corriger.** Apres une erreur, vous ajoutez 10 regles restrictives. L'agent devient inutilisable. Une regle ciblee suffit.

## Etapes

1. Quand l'agent se trompe, identifiez le type d'erreur.
2. Corrigez les degats (fichiers, DB, services).
3. Utilisez le prompt de recadrage si c'est de la sur-interpretation.
4. Ajoutez une regle de prevention (prompt, boundary, workflow).
5. Documentez l'incident si c'est une erreur grave.

## Verification

- [ ] Vous savez identifier le type d'erreur (hallucination, sur-interpretation, etc.).
- [ ] Le prompt de recadrage de Steinberg est dans vos notes/prompt.
- [ ] Les erreurs graves sont documentees avec les mesures de prevention.
- [ ] Le boundary prompt est mis a jour apres chaque incident.
- [ ] L'agent a la regle "Si tu n'es pas sur, dis-le" dans son system prompt.
