const express = require('express');
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3007;
const DB_PATH = process.env.DB_PATH || path.join(__dirname, 'data', 'tracker.db');

// Ensure data directory exists
fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });

const db = new Database(DB_PATH);
db.pragma('journal_mode = WAL');

// ============================================================
// SCHEMA
// ============================================================
db.exec(`
  CREATE TABLE IF NOT EXISTS phases (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    "order" INTEGER NOT NULL,
    status TEXT DEFAULT 'todo' CHECK(status IN ('todo','en_cours','fait','skip')),
    started_at TEXT,
    finished_at TEXT,
    notes TEXT DEFAULT ''
  );

  CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    choice TEXT,
    reason TEXT,
    alternatives TEXT,
    phase_id TEXT,
    created_at TEXT DEFAULT (datetime('now'))
  );

  CREATE TABLE IF NOT EXISTS services (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    port INTEGER,
    url TEXT,
    access_type TEXT DEFAULT 'localhost' CHECK(access_type IN ('public','tailscale','localhost')),
    status TEXT DEFAULT 'not_installed' CHECK(status IN ('running','stopped','not_installed')),
    docker_container TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
  );

  CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    result TEXT DEFAULT 'success' CHECK(result IN ('success','failure','warning','info')),
    details TEXT,
    phase_id TEXT,
    created_at TEXT DEFAULT (datetime('now'))
  );
`);

// Seed default phases if empty
const count = db.prepare('SELECT COUNT(*) as c FROM phases').get();
if (count.c === 0) {
  const phases = [
    ['phase-00', 'Phase 0 — Securisation VPS', 0],
    ['phase-01', 'Phase 1 — Docker & infra', 1],
    ['phase-02', 'Phase 2 — Vault & PostgreSQL', 2],
    ['phase-03', 'Phase 3 — Installation OpenClaw', 3],
    ['phase-04', 'Phase 4 — Connexions (OpenRouter, Telegram)', 4],
    ['phase-05', 'Phase 5 — Schema DB', 5],
    ['phase-06', 'Phase 6 — Agent principal', 6],
    ['phase-07', 'Phase 7 — Workspace & knowledge', 7],
    ['phase-08', 'Phase 8 — Communication', 8],
    ['phase-09', 'Phase 9 — Cockpit', 9],
    ['phase-10', 'Phase 10 — Git & deploy', 10],
  ];
  const insert = db.prepare('INSERT INTO phases (id, name, "order") VALUES (?, ?, ?)');
  for (const p of phases) insert.run(...p);
}

// ============================================================
// MIDDLEWARE
// ============================================================
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ============================================================
// API — PHASES
// ============================================================
app.get('/api/phases', (req, res) => {
  const rows = db.prepare('SELECT * FROM phases ORDER BY "order"').all();
  res.json(rows);
});

app.patch('/api/phases/:id', (req, res) => {
  const { status, notes } = req.body;
  const phase = db.prepare('SELECT * FROM phases WHERE id = ?').get(req.params.id);
  if (!phase) return res.status(404).json({ error: 'Phase not found' });

  if (status) {
    const now = new Date().toISOString();
    if (status === 'en_cours' && phase.status === 'todo') {
      db.prepare('UPDATE phases SET status = ?, started_at = ? WHERE id = ?').run(status, now, req.params.id);
    } else if (status === 'fait' || status === 'skip') {
      db.prepare('UPDATE phases SET status = ?, finished_at = ? WHERE id = ?').run(status, now, req.params.id);
    } else {
      db.prepare('UPDATE phases SET status = ? WHERE id = ?').run(status, req.params.id);
    }
  }
  if (notes !== undefined) {
    db.prepare('UPDATE phases SET notes = ? WHERE id = ?').run(notes, req.params.id);
  }

  // Log the action
  db.prepare('INSERT INTO actions (action, result, details, phase_id) VALUES (?, ?, ?, ?)')
    .run(`Phase ${req.params.id} -> ${status || 'updated'}`, 'info', notes || '', req.params.id);

  res.json(db.prepare('SELECT * FROM phases WHERE id = ?').get(req.params.id));
});

// ============================================================
// API — DECISIONS
// ============================================================
app.get('/api/decisions', (req, res) => {
  res.json(db.prepare('SELECT * FROM decisions ORDER BY created_at DESC').all());
});

app.post('/api/decisions', (req, res) => {
  const { question, choice, reason, alternatives, phase_id } = req.body;
  const result = db.prepare(
    'INSERT INTO decisions (question, choice, reason, alternatives, phase_id) VALUES (?, ?, ?, ?, ?)'
  ).run(question, choice, reason, alternatives, phase_id);
  res.status(201).json({ id: result.lastInsertRowid });
});

// ============================================================
// API — SERVICES
// ============================================================
app.get('/api/services', (req, res) => {
  res.json(db.prepare('SELECT * FROM services ORDER BY name').all());
});

app.put('/api/services/:id', (req, res) => {
  const { name, port, url, access_type, status, docker_container } = req.body;
  const now = new Date().toISOString();
  db.prepare(`
    INSERT INTO services (id, name, port, url, access_type, status, docker_container, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
      name=excluded.name, port=excluded.port, url=excluded.url,
      access_type=excluded.access_type, status=excluded.status,
      docker_container=excluded.docker_container, updated_at=excluded.updated_at
  `).run(req.params.id, name, port, url, access_type || 'localhost', status || 'not_installed', docker_container, now);
  res.json(db.prepare('SELECT * FROM services WHERE id = ?').get(req.params.id));
});

// ============================================================
// API — ACTIONS LOG
// ============================================================
app.get('/api/actions', (req, res) => {
  const limit = parseInt(req.query.limit) || 50;
  res.json(db.prepare('SELECT * FROM actions ORDER BY created_at DESC LIMIT ?').all(limit));
});

app.post('/api/actions', (req, res) => {
  const { action, result, details, phase_id } = req.body;
  const r = db.prepare(
    'INSERT INTO actions (action, result, details, phase_id) VALUES (?, ?, ?, ?)'
  ).run(action, result || 'success', details, phase_id);
  res.status(201).json({ id: r.lastInsertRowid });
});

// ============================================================
// API — STATE (export/import complet)
// ============================================================
app.get('/api/state', (req, res) => {
  res.json({
    phases: db.prepare('SELECT * FROM phases ORDER BY "order"').all(),
    decisions: db.prepare('SELECT * FROM decisions ORDER BY created_at').all(),
    services: db.prepare('SELECT * FROM services ORDER BY name').all(),
    actions: db.prepare('SELECT * FROM actions ORDER BY created_at DESC LIMIT 100').all(),
    exported_at: new Date().toISOString(),
  });
});

app.post('/api/state', (req, res) => {
  const { phases, decisions, services } = req.body;
  const tx = db.transaction(() => {
    if (phases) {
      for (const p of phases) {
        db.prepare(`
          INSERT INTO phases (id, name, "order", status, started_at, finished_at, notes)
          VALUES (?, ?, ?, ?, ?, ?, ?)
          ON CONFLICT(id) DO UPDATE SET
            status=excluded.status, started_at=excluded.started_at,
            finished_at=excluded.finished_at, notes=excluded.notes
        `).run(p.id, p.name, p.order, p.status, p.started_at, p.finished_at, p.notes);
      }
    }
    if (decisions) {
      for (const d of decisions) {
        db.prepare('INSERT INTO decisions (question, choice, reason, alternatives, phase_id) VALUES (?, ?, ?, ?, ?)')
          .run(d.question, d.choice, d.reason, d.alternatives, d.phase_id);
      }
    }
    if (services) {
      for (const s of services) {
        db.prepare(`
          INSERT INTO services (id, name, port, url, access_type, status, docker_container, updated_at)
          VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
          ON CONFLICT(id) DO UPDATE SET
            name=excluded.name, port=excluded.port, url=excluded.url,
            access_type=excluded.access_type, status=excluded.status,
            docker_container=excluded.docker_container, updated_at=excluded.updated_at
        `).run(s.id, s.name, s.port, s.url, s.access_type, s.status, s.docker_container);
      }
    }
  });
  tx();
  res.json({ ok: true });
});

// ============================================================
// START
// ============================================================
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Install Tracker running on port ${PORT}`);
  console.log(`UI: http://localhost:${PORT}`);
  console.log(`API: http://localhost:${PORT}/api/state`);
});
