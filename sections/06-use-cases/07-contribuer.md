---
status: complete
audience: both
chapter: 06
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 07 -- Comment soumettre votre cas d'usage

**Pour qui :** toute personne ou equipe utilisant OpenClaw en situation reelle
**Temps requis :** 30 minutes a 1 heure
**Difficulte :** Debutant

---

## Pourquoi contribuer

Les cas d'usage sont la partie la plus utile de ce playbook. Chaque nouveau cas aide d'autres praticiens a :
- Evaluer si OpenClaw correspond a leur situation
- Gagner du temps en reutilisant une configuration testee
- Eviter les erreurs que d'autres ont deja faites

Votre experience, meme partielle, a de la valeur. Un cas d'usage n'a pas besoin d'etre parfait pour etre utile.

---

## Format standard

Chaque cas d'usage suit cette structure. Vous pouvez copier ce template directement.

```markdown
---
status: draft
audience: both
chapter: 06
last_updated: YYYY-MM
contributors: [votre-github-handle]
lang: fr
---

# XX -- [Titre du cas d'usage]

**Pour qui :** [profil en une ligne]
**Temps de mise en place :** [estimation]
**Difficulte :** Debutant / Intermediaire / Avance

---

## Contexte

Qui vous etes, ce que fait votre organisation, la taille de l'equipe.

## Probleme

Ce que vous deviez resoudre ou automatiser. Soyez specifique.

## Configuration

Votre infrastructure (serveur, OS, outils).
Vos agents (combien, quels roles).
Votre budget approximatif.

## Mise en place

Les etapes que vous avez suivies, dans l'ordre chronologique.

## Resultat

Ce qui a change concretement. Chiffres si possible (temps gagne, taux de reussite, couts).

## Lecons apprises

Ce que vous referiez differemment. Ce qui a mieux marche que prevu.

## Erreurs courantes

Les pieges que vous avez rencontres et comment les eviter.

## Template

Un prompt, une configuration, ou un snippet reutilisable par d'autres.

## Verification

Une checklist pour valider que la configuration fonctionne.
```

---

## Option 1 : Soumettre via Issue GitHub

C'est la methode la plus simple. Aucune connaissance de Git n'est requise.

1. Allez sur [github.com/alexwill87/openclawfieldplaybook/issues](https://github.com/alexwill87/openclawfieldplaybook/issues)
2. Cliquez sur **New Issue**
3. Choisissez le template **suggestion**
4. Dans le titre, ecrivez : `use-case: [votre titre]`
5. Dans le corps, collez le format standard ci-dessus et remplissez-le
6. Ajoutez le label `use-case`
7. Soumettez

Un agent IA analysera votre Issue et postera un commentaire. Un maintainer humain validera et integrera le cas dans le chapitre.

---

## Option 2 : Soumettre via Pull Request

Si vous etes a l'aise avec GitHub :

1. Forkez le repo [alexwill87/openclawfieldplaybook](https://github.com/alexwill87/openclawfieldplaybook)
2. Creez votre fichier dans `sections/06-use-cases/`
3. Nommez-le avec le prochain numero disponible : `XX-titre-court.md`
4. Utilisez le format standard ci-dessus
5. Ajoutez le frontmatter YAML avec `status: draft`
6. Committez avec un message clair : `feat: add use case for [votre titre]`
7. Ouvrez une Pull Request vers le repo principal

### Regles pour la PR :

- Un fichier par cas d'usage
- Le frontmatter YAML est obligatoire
- Le status initial est toujours `draft`
- Pas de donnees nominatives (clients, employeurs) sans leur accord
- Les montants et metriques peuvent etre approximatifs, indiquez-le si c'est le cas

---

## Ce qui rend un cas d'usage utile

| Critere | Bon exemple | Mauvais exemple |
|---------|-------------|-----------------|
| Specificite | "Nous avons reduit le temps de triage de 3h a 45min" | "Ca a bien marche" |
| Reproductibilite | Configuration complete avec system prompt | "On a configure un agent" |
| Honnetete | "L'agent se trompe sur 15% des cas, voici comment on gere" | "Ca marche parfaitement" |
| Template | Prompt copier-coller pret a l'emploi | Description vague du prompt |

---

## Ce que nous recherchons particulierement

Les cas d'usage suivants sont les plus demandes par la communaute. Si vous avez de l'experience dans l'un de ces domaines, votre contribution sera particulierement valorisee :

- Artisan / metiers manuels (devis, suivi chantier, relance client)
- Profession medicale (prise de rendez-vous, suivi patient, conformite)
- Association / ONG (gestion benevoles, communication, reporting)
- Enseignement (preparation de cours, suivi eleves, administration)
- Profession juridique (triage dossiers, recherche jurisprudentielle, conformite)
- Immobilier (gestion locative, relation proprietaires, suivi travaux)

---

## Apres la soumission

1. Un agent IA analyse votre contribution et poste un commentaire
2. Un maintainer humain relit le cas d'usage
3. Si des ajustements sont necessaires, ils sont demandes via commentaire
4. Le cas est merge avec le status `draft` puis passe en `review` puis `complete`
5. Le cas apparait dans le sommaire du chapitre 6

Temps de traitement habituel : 1 a 2 semaines.

---

## Questions frequentes

**Mon cas est trop simple, est-ce utile ?**
Oui. Les cas simples sont souvent les plus utiles car ils sont accessibles a davantage de personnes.

**Je ne peux pas partager les details de mon entreprise.**
Anonymisez. Remplacez les noms, les montants exacts, et les details sensibles par des valeurs generiques. Le format et l'experience sont ce qui compte.

**Mon cas d'usage n'a pas fonctionne.**
Partagez-le quand meme. Un echec documente est aussi utile qu'une reussite. Expliquez ce qui n'a pas marche et pourquoi.

**Je ne parle pas francais.**
Les contributions en anglais sont bienvenues. Un contributeur ou un agent se chargera de la traduction.

---

*Chaque cas d'usage soumis rend ce playbook plus utile pour le prochain praticien. Votre experience compte.*

*[Soumettre via Issue](https://github.com/alexwill87/openclawfieldplaybook/issues/new?template=suggestion.yml) -- [CONTRIBUTING.md](../../CONTRIBUTING.md)*
