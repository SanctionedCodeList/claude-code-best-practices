# Claude Code Official Memory Systems

Research from official Claude Code documentation.

---

## Memory Hierarchy

Claude Code uses a **four-tier system** (highest to lowest precedence):

| Priority | Type | Location | Shared? |
|----------|------|----------|---------|
| 1 | Enterprise | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Org-wide |
| 2 | Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team (git) |
| 3 | User | `~/.claude/CLAUDE.md` | Personal |
| 4 | Local | `./CLAUDE.local.md` | Personal (gitignored) |

### Loading Behavior

- Recursive discovery from cwd upward
- Subtree files loaded on-demand when working in those directories
- Import syntax: `@path/to/file` (max 5 hops)

---

## Modular Rules

For larger projects, use `.claude/rules/`:

```
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md
    ├── testing.md
    └── security.md
```

### Path-Specific Rules

```yaml
---
paths: src/api/**/*.ts
---
# API Rules - only loaded for matching files
```

---

## Session Persistence

### Resume Sessions

```bash
claude -c                    # Resume most recent
claude -r "session-name"     # Resume by name/ID
```

### Checkpointing

- Automatic checkpoint on each user prompt
- `/rewind` or `Esc+Esc` to restore
- Tracks file edits (not bash changes)
- 30-day retention (configurable via `cleanupPeriodDays`)

---

## Context Management

### Commands

| Command | Purpose |
|---------|---------|
| `/memory` | Edit CLAUDE.md files directly |
| `/compact [focus]` | Compress conversation |
| `/context` | Visualize token usage |
| `/clear` | Clear history |
| `/init` | Bootstrap CLAUDE.md |

### System Prompt

```bash
--append-system-prompt "..."   # Add to default (recommended)
--system-prompt "..."          # Replace entirely
--system-prompt-file path      # Load from file
```

---

## Prompt Caching

Automatic optimization for repeated memory content:

```bash
DISABLE_PROMPT_CACHING=1 claude  # Disable globally
```

---

## Configuration

Settings at multiple scopes:

- `.claude/settings.json` (project, shared)
- `.claude/settings.local.json` (project, personal)
- `~/.claude/settings.json` (user)

Key memory settings:

```json
{
  "cleanupPeriodDays": 30,
  "hooks": {
    "SessionStart": [...]
  }
}
```

---

## Key Commands Summary

| Command | Purpose |
|---------|---------|
| `/memory` | Edit memory files |
| `/init` | Bootstrap CLAUDE.md |
| `/compact` | Compress context |
| `/context` | Show token usage |
| `/rewind` | Restore previous state |
| `/clear` | Clear conversation |
| `/export` | Save conversation |

---

**Source:** https://code.claude.com/docs/
