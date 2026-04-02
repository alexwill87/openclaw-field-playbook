---
status: complete
audience: both
chapter: 05
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 5.7 -- Mettre a jour les integrations

## Contexte

Les API changent. Les outils evoluent. Un endpoint qui marchait hier retourne une erreur 404 demain. Votre agent utilise des integrations (Telegram, Vault, PostgreSQL, Docker, GitHub) et chacune peut casser independamment.

L'enjeu : adapter sans tout casser.

## Quand une API change

### Signaux d'alerte

- L'agent recoit des erreurs 4xx/5xx sur un endpoint qu'il utilisait.
- Un email de l'editeur annonce un changement (deprecation notice).
- Une commande CLI ne fonctionne plus apres une mise a jour.
- Les resultats ont change de format (JSON avec des champs differents).

### Processus de mise a jour

1. **Identifier** : quel endpoint/commande a change.
2. **Lire la doc** : changelog, migration guide, nouvelle API.
3. **Tester en isolation** : appeler la nouvelle version manuellement avant de l'integrer.
4. **Mettre a jour le workflow** : modifier WORKFLOWS.md avec la nouvelle commande/endpoint.
5. **Tester le workflow complet** : dry run avec l'agent.
6. **Deployer** : mettre a jour en production.

### Template de mise a jour

```markdown
## Mise a jour integration : [nom]

Date : YYYY-MM-DD
Raison : [deprecation / bug / nouvelle feature]

### Avant
- Endpoint : [ancien]
- Commande : [ancienne]
- Format : [ancien]

### Apres
- Endpoint : [nouveau]
- Commande : [nouvelle]
- Format : [nouveau]

### Impact
- Workflows affectes : [liste]
- Scripts a modifier : [liste]

### Test
- [ ] Appel manuel OK
- [ ] Dry run agent OK
- [ ] Production OK
```

## Adapter sans casser

### Regle 1 : jamais en production d'abord

Testez toujours en isolation. Un `curl` manuel, un script de test, un environnement de staging. Jamais directement dans le workflow de production.

### Regle 2 : garder l'ancien en fallback

Ne supprimez pas l'ancienne integration tant que la nouvelle n'est pas validee en production pendant au moins une semaine.

```bash
# Exemple : nouveau endpoint Telegram
NEW_URL="https://api.telegram.org/bot${TOKEN}/sendMessage"
OLD_URL="https://api.telegram.org/bot${TOKEN}/sendMessage"  # meme dans ce cas

# Tester le nouveau
if ! curl -s -f "$NEW_URL" -d "chat_id=$CHAT_ID&text=test" > /dev/null; then
    echo "Nouveau endpoint KO, fallback sur l'ancien"
    curl -s "$OLD_URL" -d "chat_id=$CHAT_ID&text=test"
fi
```

### Regle 3 : un changement a la fois

Ne mettez pas a jour Telegram, Docker, et l'API GitHub le meme jour. Si quelque chose casse, vous ne saurez pas quoi. Un changement, un test, une validation.

## Skills a jour

Si votre agent utilise des skills (MCP, plugins, extensions) :

### Verifier les skills disponibles

```
Liste toutes tes skills/outils disponibles.
Pour chacun, dis-moi :
- Nom
- Derniere utilisation
- Est-ce qu'il fonctionne encore ? (teste)
```

### Mettre a jour une skill

1. Verifiez la version actuelle.
2. Lisez le changelog de la nouvelle version.
3. Mettez a jour dans un environnement de test.
4. Testez les fonctionnalites que vous utilisez.
5. Deployez en production.

### Supprimer les skills inutilisees

Chaque skill est un point de maintenance. Si vous ne l'utilisez plus depuis 2 mois, desactivez-la. Ca reduit la surface d'attaque et simplifie le debug.

## Erreurs courantes

**Ignorer les deprecation notices.** "Ca marche encore, je verrai plus tard." Puis l'API coupe l'ancien endpoint un dimanche soir.

**Mettre a jour en aveugle.** `pip install --upgrade` ou `npm update` sans lire le changelog. Breaking change surprise.

**Pas de fallback.** L'ancien est supprime, le nouveau ne marche pas. Vous etes coince.

**Oublier de mettre a jour les workflows.** L'integration est mise a jour mais WORKFLOWS.md reference encore l'ancienne commande. L'agent utilise l'ancien workflow et ca plante.

## Etapes

1. Listez toutes les integrations de votre agent.
2. Pour chacune, notez la version actuelle et la date de derniere verification.
3. Abonnez-vous aux changelogs/release notes des outils critiques.
4. Quand une mise a jour est necessaire, suivez le processus ci-dessus.
5. Mettez a jour WORKFLOWS.md apres chaque changement.

## Verification

- [ ] La liste des integrations est documentee avec les versions.
- [ ] Chaque integration a ete testee dans le dernier mois.
- [ ] Les deprecation notices sont suivies.
- [ ] WORKFLOWS.md est a jour apres chaque changement d'integration.
- [ ] Un fallback existe pour les integrations critiques.
