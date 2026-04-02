---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: fr
---

# 4.6 -- Base de donnees comme source de verite

## Contexte

Un fichier TASKS.md marche pour 10-20 taches. Au-dela, ca devient penible : pas de filtre, pas d'historique, pas de requetes, conflits de merge si plusieurs agents ecrivent. La solution : une base de donnees PostgreSQL comme source de verite.

Pourquoi PostgreSQL et pas SQLite ? Parce que votre agent tourne sur un VPS ou PostgreSQL est deja installe. Autant utiliser ce qui est la.

## Pourquoi DB > fichiers .md

| | Fichier .md | PostgreSQL |
|---|---|---|
| Filtre par statut/priorite | Manuel (grep) | `WHERE status = 'todo'` |
| Historique des changements | Git log (penible) | Colonne `updated_at` |
| Requetes complexes | Impossible | SQL standard |
| Acces concurrent | Conflits de merge | Transactions |
| Taches > 50 | Illisible | Pas de probleme |
| Backup | Avec le repo | pg_dump |

Le fichier .md reste utile comme vue (genere depuis la DB). Mais la source de verite est la base.

## Schema PostgreSQL

```sql
CREATE TABLE tasks (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    status      VARCHAR(20) DEFAULT 'todo' 
                CHECK (status IN ('todo', 'in_progress', 'done', 'blocked', 'cancelled')),
    priority    VARCHAR(10) DEFAULT 'medium'
                CHECK (priority IN ('high', 'medium', 'low')),
    project     VARCHAR(100),
    assigned_to VARCHAR(100),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    deadline    DATE,
    notes       TEXT
);

-- Index pour les requetes frequentes
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_project ON tasks(project);

-- Mise a jour automatique du updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

## Requetes utiles

### Taches prioritaires du jour

```sql
SELECT id, title, priority, deadline
FROM tasks
WHERE status IN ('todo', 'in_progress')
ORDER BY 
    CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
    deadline NULLS LAST;
```

### Taches en retard

```sql
SELECT id, title, deadline, 
       NOW()::date - deadline AS jours_retard
FROM tasks
WHERE status NOT IN ('done', 'cancelled')
  AND deadline < CURRENT_DATE
ORDER BY deadline;
```

### Resume de la semaine

```sql
SELECT status, COUNT(*) AS total
FROM tasks
WHERE updated_at >= NOW() - INTERVAL '7 days'
GROUP BY status
ORDER BY total DESC;
```

### Taches par projet

```sql
SELECT project, status, COUNT(*) AS total
FROM tasks
GROUP BY project, status
ORDER BY project, status;
```

## Script CLI : tasks.sh

Un script bash pour gerer les taches sans ouvrir psql a chaque fois.

```bash
#!/bin/bash
# tasks.sh — CLI pour la gestion des taches
# Usage : ./tasks.sh [commande] [arguments]

DB_NAME="${TASKS_DB:-cockpit}"
DB_USER="${TASKS_USER:-oa_admin}"

cmd_list() {
    local filter="${1:-all}"
    case "$filter" in
        todo|in_progress|done|blocked)
            psql -d "$DB_NAME" -U "$DB_USER" -c \
                "SELECT id, title, priority, deadline FROM tasks WHERE status = '$filter' ORDER BY priority, deadline NULLS LAST;"
            ;;
        urgent)
            psql -d "$DB_NAME" -U "$DB_USER" -c \
                "SELECT id, title, deadline FROM tasks WHERE status IN ('todo','in_progress') AND (priority = 'high' OR deadline <= CURRENT_DATE + 3) ORDER BY deadline NULLS LAST;"
            ;;
        *)
            psql -d "$DB_NAME" -U "$DB_USER" -c \
                "SELECT id, title, status, priority, deadline FROM tasks WHERE status NOT IN ('done','cancelled') ORDER BY priority, deadline NULLS LAST;"
            ;;
    esac
}

cmd_add() {
    local title="$1"
    local priority="${2:-medium}"
    local project="${3:-}"
    local deadline="${4:-}"
    
    # Utiliser des variables psql pour eviter l'injection SQL
    psql -d "$DB_NAME" -U "$DB_USER" \
        -v title="$title" \
        -v priority="$priority" \
        -v project="$project" \
        -v deadline="$deadline" \
        -c "INSERT INTO tasks (title, priority, project, deadline) VALUES (:'title', :'priority', NULLIF(:'project',''), NULLIF(:'deadline','')::date) RETURNING id, title;"
}

cmd_done() {
    local id="$1"
    # Valider que id est un entier
    if ! [[ "$id" =~ ^[0-9]+$ ]]; then
        echo "Erreur : id doit etre un entier" >&2
        return 1
    fi
    psql -d "$DB_NAME" -U "$DB_USER" -c \
        "UPDATE tasks SET status = 'done' WHERE id = $id RETURNING id, title, status;"
}

cmd_status() {
    local id="$1"
    local new_status="$2"
    if ! [[ "$id" =~ ^[0-9]+$ ]]; then
        echo "Erreur : id doit etre un entier" >&2
        return 1
    fi
    psql -d "$DB_NAME" -U "$DB_USER" \
        -v new_status="$new_status" \
        -c "UPDATE tasks SET status = :'new_status' WHERE id = $id RETURNING id, title, status;"
}

cmd_summary() {
    echo "=== Resume des taches ==="
    psql -d "$DB_NAME" -U "$DB_USER" -c \
        "SELECT status, COUNT(*) FROM tasks GROUP BY status ORDER BY COUNT(*) DESC;"
    echo ""
    echo "=== En retard ==="
    psql -d "$DB_NAME" -U "$DB_USER" -c \
        "SELECT id, title, deadline FROM tasks WHERE deadline < CURRENT_DATE AND status NOT IN ('done','cancelled') ORDER BY deadline;"
}

case "${1:-help}" in
    list)    cmd_list "$2" ;;
    add)     cmd_add "$2" "$3" "$4" "$5" ;;
    done)    cmd_done "$2" ;;
    status)  cmd_status "$2" "$3" ;;
    summary) cmd_summary ;;
    help)
        echo "Usage : tasks.sh <commande>"
        echo "  list [filtre]     — Lister (all/todo/in_progress/done/blocked/urgent)"
        echo "  add <titre> [priorite] [projet] [deadline]"
        echo "  done <id>         — Marquer comme terminee"
        echo "  status <id> <statut>"
        echo "  summary           — Resume global"
        ;;
    *)       echo "Commande inconnue : $1. Utilisez 'help'." ;;
esac
```

Rendez le executable : `chmod +x tasks.sh`

## Erreurs courantes

**Creer la DB trop tot.** Si vous avez 5 taches, un fichier TASKS.md suffit. Ne complexifiez pas sans raison.

**Pas de backup.** La DB est la source de verite mais elle n'est pas sauvegardee. Voir section 5.3 pour pg_dump automatise.

**Schema trop complexe.** Tags, sous-taches, dependances, commentaires, historique complet... Commencez avec le schema minimal. Ajoutez quand le besoin est reel.

**Pas de script CLI.** Vous ouvrez psql pour chaque operation. Friction = abandon. Le script reduit la friction a zero.

## Etapes

1. Creez la table avec le schema ci-dessus.
2. Migrez vos taches existantes (TASKS.md -> INSERT INTO).
3. Installez le script `tasks.sh`.
4. Testez : `./tasks.sh list`, `./tasks.sh add "Test" high`.
5. Ajoutez au system prompt : "Les taches sont dans PostgreSQL, table tasks."
6. Configurez pg_dump quotidien (section 5.3).

## Verification

- [ ] La table `tasks` existe avec le schema minimal.
- [ ] Le trigger `updated_at` fonctionne.
- [ ] Le script `tasks.sh` est executable et fonctionnel.
- [ ] L'agent sait interroger la table (instruction dans le system prompt).
- [ ] Un backup pg_dump est configure.
