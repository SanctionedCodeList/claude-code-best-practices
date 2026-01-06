# Gastown: Multi-Agent Orchestration for Claude Code

Research on Gastown (also "Gas Town"), Steve Yegge's multi-agent orchestrator built on Beads.

## What It Is

Gastown is a workspace manager that coordinates 20-30+ AI coding agents working on software projects simultaneously. It's described as "Kubernetes for agents" — an industrialized coding factory with multiple levels of agents supervising other agents.

**Creator:** Steve Yegge (Sourcegraph)
**Built on:** Beads (git-backed issue tracker)
**UI:** tmux-based
**Language:** Go

**Core insight:** Claude Code sessions are ephemeral "cattle." Work should live in git (via Beads), where it survives crashes, compaction, and restarts. Agents check their "hook" on wake-up and execute whatever work is there.

## The GUPP Principle

> **Gastown Universal Propulsion Principle:** "If there is work on your hook, YOU MUST RUN IT."

All workers have persistent identities in Beads. When a session ends and restarts, the agent checks its hook and continues where it left off. This eliminates dependency on persistent command streams.

## Architecture

### The Seven Roles

| Role | Level | Purpose |
|------|-------|---------|
| **Mayor** | Town | AI coordinator, your primary interface. Concierge and chief-of-staff |
| **Deacon** | Town | Daemon beacon. Runs patrols in a loop, propagates "do your job" signals downward |
| **Dogs** | Town | Deacon's crew for maintenance, cleanup, handyman work |
| **Boot** | Town | Special dog awakened every 5 min to check on the Deacon |
| **Witness** | Rig | Per-project monitor tracking worker health, detecting stuck processes |
| **Polecats** | Rig | Ephemeral workers that spawn, work, produce MRs, then disappear |
| **Refinery** | Rig | Merge queue processor handling code review and integration |
| **Crew** | Rig | Long-lived named agents you work with directly (design, back-and-forth) |
| **Overseer** | — | You. The human. Has an inbox and can send/receive town mail |

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Town** | Your HQ workspace (e.g., `~/gt`). Manages all rigs |
| **Rig** | A project (git repo) under Gas Town management |
| **Hook** | Where work assignments hang. Agents check their hook on wake |
| **Convoy** | A tracked unit of work spanning multiple issues |

### Two-Tier Beads Structure

```
Town Level (orchestration)
├── Patrols, releases, code review waves
├── Cross-rig coordination
└── Town mail/events

Rig Level (project work)
├── Features, bug fixes
├── Polecat work items
└── Merge requests
```

## MEOW: Molecular Expression Of Work

The algebra governing work state:

| Phase | Name | Storage | Behavior |
|-------|------|---------|----------|
| **Ice-9** | Formula | `.beads/formulas/` | Source template, composable |
| **Solid** | Protomolecule | `.beads/` | Frozen, reusable template |
| **Liquid** | Mol | `.beads/` | Persistent flowing work |
| **Vapor** | Wisp | `.beads/` (ephemeral) | Transient work for patrols |

### Operators

| Operator | Transformation | Purpose |
|----------|---------------|---------|
| `cook` | Formula → Protomolecule | Expand macros, flatten |
| `pour` | Protomolecule → Mol | Instantiate persistently |
| `wisp` | Protomolecule → Wisp | Ephemeral instantiation |
| `squash` | Mol/Wisp → Digest | Compress to record |
| `burn` | Wisp → ∅ | Discard without recording |

## Formula System

Formulas define structured workflows with dependencies:

```toml
formula = "shiny"
description = "Design before code, review before ship"

[[steps]]
id = "design"
description = "Think about architecture"

[[steps]]
id = "implement"
needs = ["design"]
```

Formulas compose via `extends` and `aspects`. When poured into molecules, steps become individual beads. If a polecat crashes after step 2 of 5, the next agent picks up at step 3.

## Commands

### For Humans

```bash
gt start              # Start Gas Town daemon + agents
gt status             # Town overview
gt mayor attach       # Enter Mayor session
gt <role> attach      # Jump into agent sessions
gt shutdown           # Graceful shutdown
gt doctor             # Health check
```

### For Work Coordination

```bash
gt convoy create "Feature X" issue-123 issue-456    # Track work
gt convoy list                                       # Dashboard
gt sling issue-123 myproject                         # Assign to worker
gt mail inbox                                        # Check messages
```

### For Configuration

```bash
gt rig add <path>             # Add project to Gas Town
gt config agent list          # List all agents
gt config agent set <name>    # Create custom agent
gt config default-agent       # Set town default
```

## Prerequisites

- **Go 1.23+**
- **Git 2.25+** (worktree support)
- **Beads (bd)** — Required, git-backed issue tracker
- **tmux 3.0+** — Recommended for full experience
- **Claude Code CLI**

## Installation

```bash
go install github.com/steveyegge/gastown/cmd/gt@latest
```

## The Eight Stages of AI-Assisted Development

Yegge's framework for developer evolution:

| Stage | Description |
|-------|-------------|
| 1 | Zero/near-zero AI — maybe code completions |
| 2 | Coding agent in IDE, permissions on |
| 3 | Agent in IDE, YOLO mode (permissions off) |
| 4 | In IDE, wide agent fills screen |
| 5 | CLI, single agent, YOLO |
| 6 | CLI, multi-agent (3-5 parallel instances) |
| 7 | 10+ agents, hand-managed |
| 8 | Building your own orchestrator |

**Warning:** Gastown requires Stage 7+ experience. It's "an industrialized coding factory manned by superintelligent chimpanzees" that can "wreck your shit in an instant."

## Graceful Degradation

Gastown degrades gracefully:
- Every worker can operate independently
- Works in "no-tmux" mode with naked Claude Code sessions
- Can run subsets of roles as needed
- Slower but still functional without full stack

## Dashboard

Web-based monitoring at `localhost:8080`:
- Convoy tracking with progress bars
- Active polecat sessions
- Refinery merge queue status
- Auto-refresh every 10 seconds

**Status indicators:**
- Green: Complete or active (< 1 min)
- Yellow: Stale (1-5 min)
- Red: Stuck (> 5 min)
- Gray: Waiting (no assignee)

## Relationship to Other Systems

| System | Relationship |
|--------|--------------|
| **Beads** | Required foundation — all work state lives in Beads |
| **Kubernetes** | Similar concepts: cattle vs pets, declarative state, self-healing |
| **Temporal** | Similar workflow orchestration, but Gastown is lighter weight |
| **Ralph Wiggum** | Simpler approach — just a bash loop. Gastown is full orchestration |

## Key Insights

### Work Philosophy

> "Work becomes fluid, an uncountable that you sling around freely, like slopping shiny fish into wooden barrels at the docks. Most work gets done; some work gets lost. Fish fall out of the barrel."

### Cost Warning

> "Gas Town is expensive as hell. You won't like Gas Town if you ever have to think, even for a moment, about where money comes from."

### The Vision

> "You are a Product Manager, and Gas Town is an Idea Compiler. You just make up features, design them, file the implementation plans, and then sling the work around to your polecats and crew."

## Sources

### Official
- [GitHub - steveyegge/gastown](https://github.com/steveyegge/gastown)
- [Gastown - Claude Code Plugins](https://claudecodeplugins.io/plugins/gastown/)

### Steve Yegge (Creator)
- [Welcome to Gas Town](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) — Comprehensive introduction (34 min read)

### Community
- [Hacker News Discussion](https://news.ycombinator.com/item?id=46458936)
- [ASCII News Coverage](https://ascii.co.uk/news/article/news-20260102-190a5f9f/steve-yegge-releases-gas-town-multi-agent-orchestrator-for-c)

## Status

- **Age:** ~3 weeks (as of Jan 2026)
- **Maturity:** "100% vibe coded" — author has never looked at the code
- **Recommendation:** Stage 7+ developers only
