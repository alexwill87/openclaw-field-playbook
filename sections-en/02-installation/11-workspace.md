---
status: complete
audience: both
chapter: 02
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 2.11 -- Workspace Structure

## Context

OpenClaw organizes its data in a workspace (`~/.openclaw/`). This folder is created automatically on first launch. Understanding its structure is essential for debugging, backup, and extending the system.

## Annotated Directory Tree

```
~/.openclaw/
├── workspace/                  # Main working directory
│   ├── knowledge/              # Knowledge base injected into context
│   │   ├── domain/             # Domain-specific knowledge
│   │   └── system/             # System knowledge (auto-updated)
│   ├── memory/                 # Persistent memory between sessions
│   │   ├── MEMORY.md           # Main memory file
│   │   └── *.md                # Thematic memory files
│   ├── sessions/               # Session history
│   │   └── YYYY-MM-DD/         # Organized by date
│   │       └── session-ID.json # Each session with context and exchanges
│   ├── skills/                 # Dynamically loaded capabilities
│   │   ├── builtin/            # Built-in skills (not modifiable)
│   │   └── custom/             # Your personalized skills
│   └── agents/                 # Agent definitions
│       ├── default.json        # Default agent
│       └── custom/             # Your personalized agents
├── config.json                 # Main configuration (section 12)
├── credentials.json            # Tokens and access (encrypted)
└── logs/                        # OpenClaw internal logs
    └── openclaw.log
```

## Role of Each Folder

### knowledge/

Contains documents that the agent can consult to answer questions. The `domain/` subfolder is yours: place your business documents, specifications, and internal guides there.

```bash
$ ls ~/.openclaw/workspace/knowledge/
```

### memory/

Persistent memory. The `MEMORY.md` file is read automatically at each session. Agents store what they need to remember between conversations there.

```bash
$ cat ~/.openclaw/workspace/memory/MEMORY.md
```

### sessions/

Complete history of each conversation. Useful for debugging and auditing. Old sessions can be archived.

### skills/

Skills are capabilities that the agent can invoke. The `custom/` folder allows you to add your own skills without touching built-in skills.

### agents/

Agent definitions with their system instructions, authorized skills, and parameters. The `default.json` file is used when no agent is specified.

## Permissions and Ownership

The entire `~/.openclaw/` folder must belong to your user:

```bash
$ ls -la ~/.openclaw/
```

If it doesn't:

```bash
$ sudo chown -R $USER:$USER ~/.openclaw/
```

## Backing Up the Workspace

The workspace contains valuable data (memory, knowledge, sessions). Include it in your backups:

```bash
$ tar -czf ~/backups/openclaw-workspace-$(date +%Y%m%d).tar.gz ~/.openclaw/workspace/
```

Do NOT back up `credentials.json` in an unencrypted backup.

## Common Mistakes

- **Modifying files in `builtin/`**: These files are overwritten with each update. Use the `custom/` folder for your changes.
- **Deleting `MEMORY.md`**: The agent loses all its memory. Back up this file regularly.
- **Workspace created by root**: If you accidentally ran `sudo openclaw`, files will belong to root. Fix this with `chown`.
- **Sessions taking up too much space**: After a few months, the `sessions/` folder can become large. Archive old sessions.

## Verification

```bash
$ ls -la ~/.openclaw/
$ ls -la ~/.openclaw/workspace/
$ cat ~/.openclaw/workspace/memory/MEMORY.md
```

Expected results:
- The folder exists and belongs to your user
- The subdirectories knowledge/, memory/, sessions/, skills/, agents/ exist
- MEMORY.md is readable

## Estimated Time

10 minutes (exploration and understanding).
