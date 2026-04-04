# Process de maintenance du site web

Ce document décrit le process complet pour maintenir, mettre à jour et auditer le site www.openclawfieldplaybook.com.

Il est conçu pour être suivi par un humain ou un agent IA.

---

## 1. Modifier du contenu

### Ajouter ou modifier une section

1. Éditer le fichier `.md` dans `sections/`
2. Respecter le format standard (frontmatter YAML + Contexte/Étapes/Erreurs/Template/Vérification)
3. Rebuild le site : `python .github/scripts/build_site.py`
4. Vérifier la page générée localement
5. Commit + push sur `main`
6. Le workflow GitHub Actions rebuild automatiquement si les paths `sections/**` changent

### Ajouter une page utilitaire

1. Ajouter une fonction `build_xxx_page()` dans `.github/scripts/build_site.py`
2. L'appeler dans le `main`
3. L'ajouter dans `build_sidebar()` au bon endroit
4. Mettre à jour le compteur `Utility pages` dans le résumé

### Mettre à jour le sitemap

Le sitemap n'est PAS généré automatiquement. Après avoir ajouté des pages :
```bash
ls *.html | sed 's|^|https://www.openclawfieldplaybook.com/|' > /tmp/urls.txt
# Puis mettre à jour sitemap.xml manuellement
```

---

## 2. Auditer le site

### Audit rapide (5 minutes)

```bash
# Vérifier que le build passe
python .github/scripts/build_site.py

# Compter les pages
ls *.html | wc -l

# Vérifier les liens cassés dans les HTML
grep -rh 'href="[^"]*\.html"' *.html | grep -oP 'href="([^"]+)"' | sort -u | while read link; do
  file=$(echo $link | sed 's/href="//;s/"//')
  [ ! -f "$file" ] && echo "LIEN CASSÉ: $file"
done

# Vérifier que le sitemap est à jour
diff <(ls *.html | sort) <(grep -oP '[^/]+\.html' sitemap.xml | sort)
```

### Audit complet (Lighthouse)

Depuis un navigateur avec Chrome DevTools :
1. Ouvrir https://www.openclawfieldplaybook.com/
2. F12 → onglet Lighthouse
3. Cocher : Performance, Accessibility, Best Practices, SEO
4. Lancer l'audit
5. Objectifs : Performance > 90, Accessibility > 90, SEO > 90

Ou via l'API PageSpeed Insights :
```
https://pagespeed.web.dev/analysis?url=https://www.openclawfieldplaybook.com/
```

### Audit SEO

Vérifier :
- [ ] `robots.txt` présent et correct
- [ ] `sitemap.xml` à jour avec toutes les pages
- [ ] Meta description sur chaque page (dans le template)
- [ ] OG tags présents (og:title, og:description)
- [ ] Pas de pages orphelines (toutes accessibles depuis la sidebar)

---

## 3. Process de déploiement

### Déploiement automatique

Le workflow `.github/workflows/deploy-playbook.yml` se déclenche quand :
- Un push sur `main` modifie `sections/**`, `index_template.html`, `assets/**`, ou le build script

Il rebuild le `index.html` et les pages de chapitre, puis commit le résultat.

### Déploiement manuel

```bash
# 1. Build
python .github/scripts/build_site.py

# 2. Vérifier
ls *.html | wc -l  # Doit correspondre au total attendu

# 3. Commit + push
git add -A
git commit -m "build: regenerate site"
git push

# 4. Vérifier le deploy
gh run list --limit 1
```

### GitHub Pages

- Source : branche `main`, dossier `/` (racine)
- Domaine custom : `www.openclawfieldplaybook.com` (CNAME)
- HTTPS : automatique via GitHub

---

## 4. Google Search Console

### Première configuration (à faire par Alex)

1. Aller sur https://search.google.com/search-console/
2. Se connecter avec alexwillemetz@gmail.com
3. Ajouter la propriété `https://www.openclawfieldplaybook.com/`
4. Méthode de vérification : fichier HTML ou DNS
5. Une fois vérifié, soumettre le sitemap : `https://www.openclawfieldplaybook.com/sitemap.xml`

### Suivi régulier

- Vérifier l'indexation (combien de pages indexées)
- Regarder les requêtes de recherche qui amènent du trafic
- Corriger les erreurs de couverture signalées

---

## 5. Checklist de maintenance mensuelle

- [ ] Vérifier que le build passe sans erreur
- [ ] Vérifier les liens cassés
- [ ] Mettre à jour le sitemap si nouvelles pages
- [ ] Lancer un audit Lighthouse (objectif > 90 sur les 4 catégories)
- [ ] Vérifier Google Search Console (erreurs, indexation)
- [ ] Mettre à jour les dépendances (Python markdown, etc.)
- [ ] Traiter les issues ouvertes sur GitHub
- [ ] Vérifier les commentaires giscus non répondus
- [ ] Mettre à jour la page Écosystème si nouveaux projets

---

## 6. Checklist avant publication majeure

Avant de publier un changement important (nouveau chapitre, nouvelle fonctionnalité) :

- [ ] Contenu relu (accents, liens, cohérence)
- [ ] Build passe sans erreur
- [ ] Pages générées vérifiées visuellement (au moins la nouvelle + index)
- [ ] Sitemap mis à jour
- [ ] Commit message clair et descriptif
- [ ] Issues liées fermées
- [ ] Email de notification envoyé aux contributeurs si pertinent

---

*Ce document est destiné à un futur agent de maintenance. Il doit pouvoir suivre ces étapes sans supervision.*
