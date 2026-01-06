# Beads: Git-Backed Task Tracking for AI Agents

Research on Beads, a distributed issue tracker designed specifically for AI coding agents.

## What It Is

Beads is a git-backed graph issue tracker that provides persistent, structured memory for AI coding agents. Created by Steve Yegge at Sourcegraph, it replaces markdown plans with a queryable, dependency-aware task system.

**Core insight:** Markdown plans don't work for AI agents. They create hundreds of decaying plan files, lose context across sessions, and can't be queried. Beads externalizes task state to git, where it survives compaction.

**The name:** Issues linked together by dependencies, "like beads on a chain, which agents can follow to get tasks done in the right order."

## The Problem It Solves

### The Dementia Problem

AI agents have no memory between sessions (which last ~10 minutes). When they wake up, they only know what they find on disk. This causes:

1. **Plan explosion** — Agents create nested 6-phase plans, then create more 6-phase plans inside those, leading to hundreds of markdown files
2. **Context loss** — After compaction, agents forget where they were in the hierarchy
3. **False completion** — Agents declare "DONE!" when they've only finished a subset of nested phases
4. **Reconstruction overhead** — Agents must re-parse dozens of markdown files to figure out "what next?"

### Why Markdown Plans Fail

- **Text, not structured data** — Requires parsing/interpretation, stealing GPU cycles
- **Not queryable** — Can't build work queues, audit work, or track dependencies
- **Bit-rot** — Agents rarely update plans as they work
- **No linking** — Plans form a work graph but aren't connected in queryable form

## Architecture

### Three-Component System

| Component | Purpose |
|-----------|---------|
| **SQLite Database** (`beads.db`) | Local storage for issues, statuses, priorities, relationships |
| **JSON-L Format** (`issues.jsonl`) | Text-based export committed to Git |
| **Two-Way Sync** | Background daemon synchronizes database ↔ Git file |

### Why Git-Backed?

- **Survives compaction** — If it's in git, agents can find it
- **Versioned** — Nothing is ever lost; can reconstruct from history
- **Branchable** — Multi-agent/multi-branch workflows work naturally
- **Self-healing** — Corrupted databases can be rebuilt from git history

### Collision-Free IDs

Hash-based identifiers (e.g., `bd-a1b2`) prevent merge conflicts in multi-agent workflows.

## Installation

```bash
# npm
npm install -g @beads/bd

# Homebrew
brew install steveyegge/beads/bd

# Go
go install github.com/steveyegge/beads/cmd/bd@latest
```

Initialize in project:
```bash
bd init
bd setup claude  # Configure for Claude Code
```

## Core Commands

| Command | Purpose |
|---------|---------|
| `bd init` | Initialize tracking system |
| `bd ready` | List unblocked tasks (no incomplete dependencies) |
| `bd create <title>` | Create issue with type (`-t epic/task`), priority (`-p`) |
| `bd dep add <child> <parent>` | Link task dependencies |
| `bd dep tree` | Display hierarchical project structure |
| `bd show <id>` | Display task details and history |
| `bd update <id>` | Change status or properties |
| `bd close <id>` | Mark issue complete |
| `bd compact` | Summarize old closed issues (semantic memory decay) |
| `bd list` | View all issues |

## Task Structure

### Hierarchical IDs

Supports nested IDs for structured epics:
- `bd-a3f8` — Epic level
- `bd-a3f8.1` — Task level
- `bd-a3f8.1.1` — Subtask level

### Four Dependency Types

1. **Blocks** — Task A must complete before Task B
2. **Related** — Tasks are connected but independent
3. **Parent-child** — Hierarchical containment
4. **Discovered-from** — Provenance tracking (where did this task come from?)

### Three-Field Task Content

| Field | Purpose |
|-------|---------|
| **Description** | Implementation mechanics (file paths, code snippets, steps) |
| **Design** | Architectural context and decision rationale |
| **Notes** | Source document references as fallback |

## Workflow Patterns

### Basic Agent Loop

```
1. Query `bd ready` for actionable tasks
2. Select highest-priority available task
3. Update status: `bd update <id> --status in_progress`
4. Complete work
5. Mark complete: `bd close <id>`
6. Return to step 1
```

### Five-Stage Pipeline (from JX0.ca)

1. **Brainstorming** — Collaborative dialogue producing design documents
2. **Planning** — Converting designs into detailed implementation plans
3. **Plan-to-Epic** — Creating beads epics with structured tasks
4. **Execution** — Autonomous task implementation via subagents
5. **Completion** — Verification and closure

### Automatic Dependency Detection

The `plan-to-epic` workflow automatically infers dependencies through file overlap detection — if Task 5 modifies files that Task 3 also changes, Task 5 depends on Task 3.

## Integration

### Claude Code

- Marketplace plugin available
- Point CLAUDE.md at beads with one line
- Agents "instantly become good at long-horizon planning"

### MCP Server

```bash
pip install beads-mcp
```

Works with Sourcegraph Amp and any MCP-enabled agent.

### Stealth Mode

```bash
bd init --stealth
```

Local-only tracking on shared projects without committing to main repository.

## Key Benefits

| Benefit | Description |
|---------|-------------|
| **Context efficiency** | Agents query only needed info vs. loading entire spec files |
| **Explicit dependencies** | Relationships stored structurally, no ambiguity |
| **Persistent memory** | Task state survives session restarts |
| **Self-healing** | Database corruption recoverable from git history |
| **Agent-native** | JSON output, queryable, structured — how agents think |

## Sources

### Official
- [GitHub - steveyegge/beads](https://github.com/steveyegge/beads)
- [Beads - Claude Skills](https://claude-plugins.dev/skills/@steveyegge/beads/beads)

### Steve Yegge (Creator)
- [Introducing Beads: A coding agent memory system](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a) — Origin story, the dementia problem, why markdown plans fail
- [The Beads Revolution](https://steve-yegge.medium.com/the-beads-revolution-how-i-built-the-todo-system-that-ai-agents-actually-want-to-use-228a5f9be2a9) — Self-healing, MCP integration, community adoption

### Community
- [Solving Agent Context Loss - JX0.ca](https://jx0.ca/solving-agent-context-loss) — Five-stage pipeline, three-field task structure
- [Beads: Git-Friendly Issue Tracker - Better Stack](https://betterstack.com/community/guides/ai/beads-issue-tracker-ai-agents/) — Installation guide, workflow patterns
- [Beads: Memory for Coding Agents - Paddo.dev](https://paddo.dev/blog/beads-memory-for-coding-agents/)

## Stats (as of research date)

- **GitHub Stars:** 8.5k+
- **Forks:** 519
- **Language:** Go (93.9%)
- **Contributors:** 121
- **Releases:** 60+

## Quotes

> "Markdown plans may reasonably model how humans work, but they don't work well for AIs." — Steve Yegge

> "Your markdown plans form a work graph, but they aren't linked together in a queryable, reified form." — Steve Yegge

> "The AIs love it. Go ahead, ask them. Point your favorite coding agent at my GitHub repo and ask them, would this be useful?" — Steve Yegge

> "By externalizing task state, developers eliminate session boundaries as obstacles." — JX0.ca
