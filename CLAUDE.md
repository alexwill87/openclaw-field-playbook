# CLAUDE.md -- Instructions pour les agents Claude Code

Ce fichier est lu automatiquement par tout agent Claude Code qui ouvre ce repository.

---

## Contexte du projet

Ce repository contient le **OpenClaw Field Playbook**, un guide de terrain open-source pour installer, configurer et operer OpenClaw en entreprise. Il est ecrit par des praticiens, pour des praticiens -- entrepreneurs, equipes techniques, et agents IA.

Le playbook couvre le parcours complet : comprendre ce qu'est OpenClaw, l'installer, le configurer pour son contexte, le personnaliser, et le maintenir dans le temps.

- **Repo GitHub :** github.com/alexwill87/openclawfieldplaybook
- **Site :** www.openclawfieldplaybook.com
- **Licence :** Creative Commons Attribution 4.0

---

## Structure du repository

```
MANIFESTE.md              <- Constitution du projet. A lire en premier.
PLAYBOOK.md               <- Document assemble depuis sections/. Ne pas editer directement.
CONTRIBUTING.md            <- Guide de contribution (3 niveaux : T1, T2, T3)
ROADMAP.md                 <- Feuille de route du projet
sections/                  <- Contenu canonique, organise par chapitre
  00-reading-guide.md
  01-definition/
  02-installation/
  03-configuration/
  04-personalisation/
  05-maintenance/
  06-use-cases/
  07-localisation/
_project/                  <- Fichiers de suivi interne (scores, qualite)
resources/                 <- Ressources complementaires
assets/                    <- Images et fichiers statiques
website/                   <- Site web (GitHub Pages)
```

`PLAYBOOK.md` est assemble a partir des fichiers dans `sections/`. Toujours editer les fichiers sources dans `sections/`, jamais `PLAYBOOK.md` directement.

---

## Langue

Le contenu est redige en **francais**. Les termes techniques anglais sont conserves tels quels (API, VPS, webhook, system prompt, knowledge base, etc.). Les cles YAML, les noms de fichiers, et les blocs de code utilisent l'anglais comme reference universelle.

---

## Comment contribuer

Trois niveaux de contribution, documentes dans `CONTRIBUTING.md` :

| Niveau | Portee | Processus |
|--------|--------|-----------|
| **T3** | Corrections (typos, liens, exemples) | Issue ou PR directe, merge rapide |
| **T2** | Nouvelles sections, reecritures, cas d'usage | Issue d'abord, puis PR, review par maintainer |
| **T1** | Structure des 7 chapitres | Issue `governance`, decision du fondateur uniquement |

---

## Regles pour l'agent

1. **Lire `MANIFESTE.md` en premier.** C'est le document d'autorite sur l'intention et la structure du projet.

2. **Preferer `sections/` a `PLAYBOOK.md`.** Les fichiers dans `sections/` sont la source de verite. `PLAYBOOK.md` est un document derive.

3. **Ne pas modifier la structure T1.** Les 7 chapitres (Definition, Installation, Configuration, Personalisation, Maintenance, Use Cases, Localisation) sont fixes. Proposer des changements de structure via une Issue `governance`.

4. **Issues `governance` = decision humaine.** Ne pas tenter de resoudre automatiquement les Issues etiquetees `governance`. Elles requierent une decision du fondateur.

5. **Ecrire en francais.** Garder les termes techniques anglais. Ne pas traduire les noms de fichiers, les cles YAML, ou les commandes.

6. **Respecter le format standard par section :**
   - Frontmatter YAML (`status`, `audience`, `chapter`, `last_updated`, `contributors`)
   - Sections : Contexte / Etapes / Erreurs courantes / Template / Verification

7. **Utiliser le frontmatter YAML pour le routage.** Les champs `status` (draft/review/complete), `audience` (human/agent/both), et `chapter` determinent le traitement de chaque section.

8. **Ne pas generer de contenu speculatif.** Chaque affirmation doit etre basee sur une experience reelle ou explicitement etiquetee comme une recommandation.

---

## Utilisation comme runbook par un agent

Ce repository peut etre clone par un agent Claude Code sur un VPS pour guider une installation OpenClaw. L'agent peut :

1. Cloner le repo : `git clone https://github.com/alexwill87/openclawfieldplaybook.git`
2. Lire les sections du **chapitre 2 (Installation)** comme un runbook
3. Executer les commandes decrites etape par etape
4. Documenter les resultats de chaque etape dans un fichier de log
5. Passer au **chapitre 3 (Configuration)** une fois l'installation validee
6. Utiliser les **cas d'usage du chapitre 6** pour adapter la configuration au contexte specifique

L'agent doit toujours verifier les prerequis avant d'executer une commande et ne jamais sauter une etape de verification.

---

## Commandes utiles

### Assembler le playbook depuis les sections

```bash
# Concatener toutes les sections dans l'ordre
cat sections/00-reading-guide.md > PLAYBOOK.md
for dir in sections/0{1..7}*/; do
  for f in "$dir"*.md; do
    echo -e "\n---\n" >> PLAYBOOK.md
    cat "$f" >> PLAYBOOK.md
  done
done
```

### Tester les liens internes

```bash
# Verifier les liens Markdown casses (necessite markdown-link-check)
npx markdown-link-check sections/**/*.md
```

### Valider le frontmatter YAML

```bash
# Verifier que chaque fichier .md dans sections/ a un frontmatter valide
for f in sections/**/*.md; do
  head -1 "$f" | grep -q "^---" || echo "Frontmatter manquant: $f"
done
```

---

## Contacts

- **Fondateur :** Alex Willemetz (@alexwill87)
- **Issues :** github.com/alexwill87/openclawfieldplaybook/issues
- **Contributions :** voir `CONTRIBUTING.md`
