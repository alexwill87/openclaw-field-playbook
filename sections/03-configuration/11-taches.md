---
status: complete
audience: both
chapter: 03
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 3.11 -- Taches : la pression invisible

## Contexte

Le calendrier montre ce qui est PLANIFIE. Les taches montrent ce qui est REEL mais pas encore planifie.

C'est la pression invisible : les choses que vous devez faire mais qui n'ont pas de creneau. Le rapport a finir. La relance a envoyer. Le bug a corriger. Ces elements ne sont pas dans le calendrier, mais ils pesent sur chaque decision de priorisation.

Un agent qui voit votre calendrier mais pas vos taches croit que vos creneaux libres sont vraiment libres. Ils ne le sont pas.

## Calendrier + taches = vision complete

| Calendrier | Taches |
|---|---|
| Ce qui a une date et une heure | Ce qui a une deadline (ou pas) |
| Engagements avec d'autres | Engagements avec vous-meme |
| Planifie | Non planifie mais reel |
| Visible par les autres | Souvent prive |

L'agent a besoin des deux pour produire un briefing utile. "Vous avez 2h libres cet apres-midi" est incomplet si vous avez 5 taches urgentes en retard.

## Connexion

### Via base de donnees

```
openclaw skill add tasks --source db
```

L'agent se connecte a votre base de donnees de taches (Supabase, PostgreSQL, SQLite). Avantage : controle total, pas de dependance a un service tiers.

### Via outil externe

```
openclaw skill add tasks --source todoist
openclaw skill add tasks --source notion
openclaw skill add tasks --source linear
```

L'agent se connecte a votre outil de taches existant. Avantage : pas besoin de migrer.

### Portee : cette semaine, pas la wishlist

Regle critique : l'agent ne doit voir que les taches de CETTE SEMAINE. Pas le backlog de 200 items. Pas la wishlist. Pas les "un jour peut-etre".

Pourquoi : un agent qui voit 200 taches les traite toutes comme potentiellement pertinentes. Il mentionne des taches de basse priorite dans le briefing. Il suggere de traiter des items vieux de 3 mois. Le bruit noie le signal.

Configuration recommandee :

```markdown
## Portee des taches
- Taches avec deadline cette semaine
- Taches marquees "urgent" ou "haute priorite"
- Taches assignees a moi (pas celles que j'ai deleguees)
- Maximum : 15 taches visibles a la fois
```

## Etape par etape

### 1. Identifier votre source de taches

Ou sont vos taches aujourd'hui ? Un outil ? Plusieurs ? Des post-its ? Un fichier texte ?

Si elles sont dispersees, consolidez-les d'abord dans un seul endroit avant de connecter l'agent.

### 2. Connecter en lecture seule

Comme pour le calendrier, commencez en lecture. L'agent voit les taches, les mentionne dans le briefing, mais ne les modifie pas.

### 3. Definir la portee

Configurez le filtre : cette semaine + urgentes uniquement.

### 4. Valider l'integration calendrier + taches

```
Montre-moi ma journee avec mes taches en attente.
```

L'agent doit :
- Afficher le calendrier (reunions, blocs)
- Lister les taches pertinentes
- Suggerer quand traiter les taches dans les creneaux libres

### 5. Ajouter les droits d'ecriture (optionnel)

Apres validation, vous pouvez autoriser l'agent a :
- Marquer une tache comme terminee (apres votre confirmation)
- Ajouter une tache (issue d'un email ou d'une reunion)
- Modifier la priorite (avec notification)

## Erreurs courantes

**Connecter toutes les taches** : 200 taches dans le contexte = briefing inutile. Filtrez a cette semaine.

**Pas de priorite** : Si toutes les taches ont la meme priorite, l'agent ne peut pas trier. Priorisez vos taches dans votre outil AVANT de connecter l'agent.

**Taches dans MEMORY.md** : "Finir le rapport pour vendredi" dans MEMORY.md au lieu du systeme de taches. MEMORY.md n'est pas une todo list. Les taches vont dans le systeme de taches.

**Taches dupliquees** : La meme tache dans Notion ET dans MEMORY.md. L'agent la compte deux fois.

**Connecter les taches avant le calendrier** : Les taches sans calendrier sont une liste flottante. Connectez le calendrier d'abord (section 3.10).

## Verification

- [ ] Source de taches identifiee et consolidee
- [ ] Connexion en lecture seule etablie
- [ ] Portee definie (cette semaine + urgentes)
- [ ] Maximum 15 taches visibles
- [ ] Test "ma journee avec mes taches" reussi
- [ ] Integration calendrier + taches validee
- [ ] Pas de taches dans MEMORY.md (elles sont dans le systeme de taches)
