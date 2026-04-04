---
---
status: complete
audience: both
chapter: 04
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 4.6 -- Database as source of truth

## Context

A TASKS.md file works for 10-20 tasks. Beyond that, it becomes painful: no filtering, no history, no queries, merge conflicts if multiple agents write to it. The solution: a PostgreSQL database as the source of truth.

Why PostgreSQL and not SQLite? Because your agent runs on a VPS where PostgreSQL is already installed. Might as well use what's already there.

## Why DB > .md files

| | .md file | PostgreSQL |
|---|---|---|
| Filter by status/priority | Manual (grep) | `WHERE status = 'todo'` |
| Change history | Git log (painful) | `updated_at` column |
| Complex queries | Impossible | Standard SQL |
| Concurrent access | Merge conflicts | Transactions |
| Tasks > 50 | Unreadable | No problem |
| Backup | With the repo | pg_dump |

The .md file remains useful as a view (generated from the DB). But the source of truth is the database.

## PostgreSQL schema

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

-- Index for frequent queries
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_project ON tasks(project);

-- Automatic update of updated_at
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

## Useful queries

### Priority tasks for the day

```sql
SELECT id, title, priority, deadline
FROM tasks
WHERE status IN ('todo', 'in_progress')
ORDER BY 
    CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
    deadline NULLS LAST;
```

### Overdue tasks

```sql
SELECT id, title, deadline, 
       NOW()::date - deadline AS jours_retard
FROM tasks
WHERE status NOT IN ('done', 'cancelled')
  AND deadline < CURRENT_DATE
ORDER BY deadline;
```

### Weekly summary

```sql
SELECT status, COUNT(*) AS total
FROM tasks
WHERE updated_at >= NOW() - INTERVAL '7 days'
GROUP BY status
ORDER BY total DESC;
```

### Tasks by project

```sql
SELECT project, status, COUNT(*) AS total
FROM tasks
GROUP BY project, status
ORDER BY project, status;
```

## CLI script: tasks.sh

A bash script to manage tasks without opening psql every time.

```bash
#!/bin/bash
# tasks.sh — CLI for task management
# Usage : ./tasks.sh [command] [arguments]

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
    
    # Use psql variables to avoid SQL injection
    psql -d "$DB_NAME" -U "$DB_USER" \
        -v title="$title" \
        -v priority="$priority" \
        -v project="$project" \
        -v deadline="$deadline" \
        -c "INSERT INTO tasks (title, priority, project, deadline) VALUES (:'title', :'priority', NULLIF(:'project',''), NULLIF(:'deadline','')::date) RETURNING id, title;"
}

cmd_done() {
    local id="$1"
    # Validate that id is an integer
    if ! [[ "$id" =~ ^[0-9]+$ ]]; then
        echo "Error: id must be an integer" >&2
        return 1
    fi
    psql -d "$DB_NAME" -U "$DB_USER" -c \
        "UPDATE tasks SET status = 'done' WHERE id = $id RETURNING id, title, status;"
}

cmd_status() {
    local id="$1"
    local new_status="$2"
    if ! [[ "$id" =~ ^[0-9]+$ ]]; then
        echo "Error: id must be an integer" >&2
        return 1
    fi
    psql -d "$DB_NAME" -U "$DB_USER" \
        -v new_status="$new_status" \
        -c "UPDATE tasks SET status = :'new_status' WHERE id = $id RETURNING id, title, status;"
}

cmd_summary() {
    echo "=== Task summary ==="
    psql -d "$DB_NAME" -U "$DB_USER" -c \
        "SELECT status, COUNT(*) FROM tasks GROUP BY status ORDER BY COUNT(*) DESC;"
    echo ""
    echo "=== Overdue ==="
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
        echo "Usage : tasks.sh <command>"
        echo "  list [filter]     — List (all/todo/in_progress/done/blocked/urgent)"
        echo "  add <title> [priority] [project] [deadline]"
        echo "  done <id>         — Mark as complete"
        echo "  status <id> <status>"
        echo "  summary           — Global summary"
        ;;
    *)       echo "Unknown command: $1. Use 'help'." ;;
esac
```

Make it executable: `chmod +x tasks.sh`

## Common mistakes

**Creating the DB too early.** If you have 5 tasks, a TASKS.md file is sufficient. Don't add complexity without reason.

**No backup.** The DB is the source of truth but it's not backed up. See section 5.3 for automated pg_dump.

**Schema too complex.** Tags, subtasks, dependencies, comments, full history... Start with the minimal schema. Add when the need is real.

**No CLI script.** You open psql for each operation. Friction = abandonment. The script reduces friction to zero.

## Steps

1. Create the table with the schema above.
2. Migrate your existing tasks (TASKS.md -> INSERT INTO).
3. Install the `tasks.sh` script.
4. Test: `./tasks.sh list`, `./tasks.sh add "Test" high`.
5. Add to system prompt: "Tasks are in PostgreSQL, tasks table."
6. Configure daily pg_dump (section 5.3).

## Checklist

- [ ] The `tasks` table exists with the minimal schema.
- [ ] The `updated_at` trigger works.
- [ ] The `tasks.sh` script is executable and functional.
- [ ] The agent knows how to query the table (instruction in system prompt).
- [ ] A pg_dump backup is configured.
