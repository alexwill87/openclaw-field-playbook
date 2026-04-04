---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.1 -- Ecrire votre system prompt

## Contexte

Le system prompt est le texte le plus important de votre setup. C'est la premiere chose que l'agent lit a chaque conversation. Il definit qui il est, ce qu'il sait faire, et comment il doit se comporter.

Un bon system prompt = un agent utile des la premiere reponse.
Un mauvais system prompt = des corrections permanentes.

## Structure recommandee

Un system prompt efficace suit cet ordre :

### 1. Mission (2-3 phrases)

Qui est l'agent, pour qui il travaille, quel est son role principal.

```
Tu es l'assistant technique de [votre nom], freelance devops.
Tu geres l'infrastructure VPS, les deployments, et le suivi des taches.
Tu communiques en francais, termes techniques en anglais.
```

### 2. Contexte (ce qu'il doit savoir)

Les faits permanents. Pas les details qui changent chaque semaine -- ceux-la vont dans la memoire.

```
Stack : Ubuntu 24.04, Docker, PostgreSQL, Node.js, Vault.
VPS : Hetzner Paris, IP fixe.
Projets actifs : cockpit, openclaw-playbook.
```

### 3. Outils et acces

Ce que l'agent peut utiliser. Pas la doc complete -- juste la liste et les limites.

```
Tu as acces a : bash, fichiers locaux, git, Docker, PostgreSQL, Vault.
Tu n'as PAS acces a : email, Stripe, DNS.
```

### 4. Regles de comportement

Les contraintes non negociables.

```
- Ne jamais push --force sur main.
- Ne jamais modifier .env sans validation explicite.
- Toujours creer un commit separe, jamais amend sauf demande explicite.
- Pas de fichiers markdown sauf demande explicite.
```

### 5. Ton et format

Comment il parle. Court et precis. Voir section 4.2 pour les details.

```
- Francais. Termes techniques en anglais.
- Reponses courtes sauf si je demande un detail.
- Pas d'emojis.
```

## Erreurs courantes

**Trop long.** Chaque token du system prompt est envoye a chaque requete. 500 mots = ~700 tokens. A 1000 requetes/mois, ca chiffre. Visez 150-300 mots.

**Trop vague.** "Sois utile et professionnel" ne dit rien. "Reponds en 3 phrases max sauf si je demande plus" dit tout.

**Trop de contexte volatil.** Le system prompt est pour les regles permanentes. Les projets en cours, les deadlines, les etats -- ca va dans la memoire ou les fichiers de contexte.

**Pas de regles negatives.** Dire ce que l'agent NE doit PAS faire est aussi important que dire ce qu'il doit faire. Sinon il improvise, et l'improvisation coute cher.

## Template complet

```markdown
# System Prompt — [Votre nom / projet]

## Mission
Tu es [role] de [qui]. Tu [responsabilite principale].

## Contexte
- Stack : [technologies]
- Infra : [provider, localisation]
- Projets : [liste]

## Outils
Tu as acces a : [liste].
Tu n'as PAS acces a : [liste].

## Regles
- [Regle 1 — la plus critique]
- [Regle 2]
- [Regle 3]
- Ne JAMAIS [interdit critique].

## Ton
- [Langue]. Termes techniques en anglais.
- [Style : court/long, formel/direct]
- [Format prefere : bullet points, prose, code]
```

## Cas terrain : workspace Aurel (VPS Pantheos)

L'agent Aurel utilise un systeme de fichiers complementaires au system prompt qui merite d'etre documente comme pattern reutilisable :

| Fichier | Role | Contenu cle |
|---------|------|-------------|
| `SOUL.md` | Boussole morale | Mission, valeurs, 4 principes fondateurs, limites inviolables |
| `IDENTITY.md` | Identite operationnelle | 3 roles integres (Majordome, Ingenieur, Premier Ministre), signature de communication |
| `USER_PROFILE.md` | Contexte utilisateur | Qui est l'utilisateur, horaires, budget, contraintes |
| `AGENTS.md` | Manifeste agent | Regles comportementales, memoire, proactivite, fleet de 8 agents |
| `mode_DEV.md` / `mode_ARCHI.md` | Modes operationnels | DEV = execution, ARCHI = gouvernance |

**Pourquoi ca marche** : le system prompt reste court (~200 mots) et pointe vers ces fichiers. Chaque fichier a un perimetre precis. Quand une regle change, on modifie un seul fichier sans toucher au system prompt.

**Pattern "Last Word Rule"** (extrait du SOUL.md d'Aurel) : l'humain a toujours le dernier mot. Si l'agent est en desaccord, il exprime sa position une fois, puis execute la decision humaine sans resistance passive. Ce pattern evite les boucles de negociation agent-humain.

> **Recommandation** : commencez avec un system prompt simple (template ci-dessus). Quand il depasse 300 mots, eclatez-le en fichiers thematiques. Voir section 4.11 pour les niveaux de confiance dans CONSTITUTION.md.

## Etapes

1. Ecrivez une premiere version en suivant la structure ci-dessus.
2. Testez avec 5 requetes typiques de votre usage quotidien.
3. Notez ou l'agent repond mal -- c'est un trou dans le prompt.
4. Ajustez. Voir section 4.3 pour le processus d'iteration.

## Verification

- [ ] Le prompt fait moins de 300 mots.
- [ ] La mission est claire en 2 phrases.
- [ ] Les regles incluent au moins 2 interdictions explicites.
- [ ] Le ton est defini de facon actionnable (pas "sois professionnel").
- [ ] Teste avec 5 requetes reelles -- les reponses sont correctes sans correction.
