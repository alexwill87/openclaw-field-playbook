# FIELD-REPORTS.md — Correspondance issues terrain / sections du playbook

> Ce fichier connecte les issues GitHub (savoir terrain) aux sections du playbook (savoir formel).
> Mis a jour : avril 2026.

## Par section

| Section | Titre | Issues terrain |
|---------|-------|---------------|
| 2.02 | Securiser le VPS | #14 (UsePAM no risque sur Ubuntu) |
| 2.05 | Node.js et PM2 | #15 (version nvm hardcodee), #24 (nvm vs global), #12 (chemin Node) |
| 2.07 | Vault | #11 (unseal en clair), #21 (permission Docker volume), #22 (VAULT_ADDR HTTPS vs HTTP) |
| 2.08 | PostgreSQL | #13 (mot de passe en clair dans docker-compose) |
| 2.09 | Health check | #19 (script reference mais jamais cree) |
| 2.10 | Installation OpenClaw | #10 (CRITIQUE: mauvais package npm) |
| 2.12 | Config OpenClaw | #23 (syntaxe config set), #29 (registration modeles), #16 (noms modeles hardcodes), #34 (guide choix modele) |
| 2.13 | OpenRouter | #34 (openrouter/auto mauvais defaut), #32 (erreurs silencieuses), #16 (noms modeles), #26 (test sans canal) |
| 2.14 | Telegram | #28 (botToken pas token) |
| 2.15 | Gateway systemd | #12 (VAULT_TOKEN en clair), #25 (env file permissions), #30 (anciens services) |
| 2.16 | Verification complete | #26 (methode de test manquante) |
| 2.19 | Script deploy | #17 (faux succes), #18 (PM2 vs systemd) |
| 3.14 | Souverainete donnees | #20 (cles API en clair, workaround Vault) |
| 3.18 | Remote mode | #31 (connecter deux installations) |
| 4.01 | System prompt | #33 (cas terrain Aurel, workspace) |
| 4.02 | Personnalite et ton | #33 (spectrum proactif-passif) |
| 5.11 | En cas de panne | #32 (agent muet, erreurs LLM silencieuses) |

## Par issue

| Issue | Titre | Section(s) concernee(s) |
|-------|-------|-------------------------|
| #9 | Rapport terrain — premiere lecture agent | Toutes (chapitre 2) |
| #10 | Mauvais package npm | 2.10 |
| #11 | Vault unseal en clair | 2.07 |
| #12 | Chemin Node + VAULT_TOKEN | 2.05, 2.15 |
| #13 | PostgreSQL mot de passe | 2.08 |
| #14 | UsePAM no | 2.02 |
| #15 | Version nvm hardcodee | 2.05 |
| #16 | Noms modeles hardcodes | 2.12, 2.13 |
| #17 | deploy.sh faux succes | 2.19 |
| #18 | PM2 vs systemd | 2.19 |
| #19 | health-check.sh manquant | 2.09 |
| #20 | Cles API en clair | 3.14 |
| #21 | Vault Docker permissions | 2.07 |
| #22 | VAULT_ADDR HTTPS | 2.07 |
| #23 | openclaw config set syntaxe | 2.12 |
| #24 | nvm vs Node global | 2.05 |
| #25 | Gateway env permissions | 2.15 |
| #26 | Test modele sans canal | 2.13, 2.16 |
| #27 | Port conflict | 2.15 |
| #28 | Telegram botToken | 2.14 |
| #29 | Registration modeles | 2.12 |
| #30 | Anciens services systemd | 2.15 |
| #31 | Remote mode | 3.18 |
| #32 | Erreurs LLM silencieuses | 2.13, 5.11 |
| #33 | Chapter 4 cas Aurel | 4.01, 4.02 |
| #34 | Guide choix modele | 2.12, 2.13 |

## Regles de mise a jour

- Quand une issue est ouverte : ajouter une ligne dans les deux tableaux
- Quand une issue est corrigee et le contenu integre dans la section : la garder ici comme reference historique
- Format : numero d'issue cliquable, titre court, section(s) concernee(s)
