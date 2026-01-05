# Context Window Management Research

Research on tools for managing Claude Code's context window across sessions.

## The Problem

Claude Code has a ~200K token context window. When it fills:
1. **Default behavior**: Auto-compacts (summarizes) the conversation
2. **Each compaction is lossy** - details get dropped
3. **After 2-3 compactions**: Working with summary-of-summary, hallucinations begin

## Approaches

### 1. Clear Strategy (Continuous Claude)

**Repo**: [parcadei/Continuous-Claude](https://github.com/parcadei/Continuous-Claude)

**Philosophy**: Clear, don't compact. Save state to files, wipe context, reload.

**How it works**:
- **Ledgers** (`thoughts/ledgers/CONTINUITY_*.md`) - In-session state surviving `/clear`
- **Handoffs** (`thoughts/shared/handoffs/`) - End-of-session documents for next session
- **Hooks** - Automate state save/load on lifecycle events
- **StatusLine** - Real-time context % display with color warnings

**Overhead**:
- Setup: `uv sync`, install hooks, configure per-project
- Runtime: Watch context %, save before clear, manage handoff files
- Context tax: ~1-2% for injected state on session start

**Best for**: Multi-session implementations, precise work, team handoffs

### 2. Loop Strategy (AnandChowdhary/continuous-claude)

**Repo**: [AnandChowdhary/continuous-claude](https://github.com/AnandChowdhary/continuous-claude)

**Philosophy**: Run Claude in a loop, each iteration creates a PR.

**How it works**:
- Each iteration: new branch → Claude generates commit → push → create PR
- `SHARED_TASK_NOTES.md` maintains continuity between iterations
- CI validates each PR before next iteration
- Human reviews/merges accumulated PRs

**Use case**: Large refactoring tasks (e.g., 0% to 80% test coverage across huge codebase)

**Best for**: Autonomous batch work, weekend refactoring runs

### 3. Development Kit (peterkrueck)

**Repo**: [peterkrueck/Claude-Code-Development-Kit](https://github.com/peterkrueck/Claude-Code-Development-Kit)

**Philosophy**: Orchestrated development environment through documentation + sub-agents + MCP.

**How it works**:
- **3-tier documentation system**: Foundation (CLAUDE.md) → Component (backend/CONTEXT.md) → Feature (api/CONTEXT.md)
- **Auto-loading**: Every command automatically loads critical docs via hooks
- **Sub-agent context injection**: All spawned agents receive core documentation automatically
- **MCP integration**: Context7 for library docs, Gemini for architecture consultation
- **Commands**: `/full-context`, `/code-review`, `/update-docs`

**Key insight**: Instead of managing context window, it structures documentation so the right context is always available. Sub-agents work in parallel with consistent knowledge.

**Best for**: Complex projects with multiple components, team environments

### 4. Smart Handoff Command

**Source**: [Smart Handoff Blog Post](https://blog.skinnyandbald.com/never-lose-your-flow-smart-handoff-for-claude-code/)

**Philosophy**: Generate optimized `/compact` message before compaction.

**How it works**:
- At ~70-80% context, run command
- Generates custom compaction prompt tuned to current goal
- Preserves direction + key details through compaction

**Best for**: Working with default compaction but optimizing what's preserved

## Comparison

| Approach | Overhead | Automation | Context Quality | Multi-Session |
|----------|----------|------------|-----------------|---------------|
| Default compaction | None | Full | Degrades | Poor |
| Clear Strategy | Medium | Partial (hooks) | Always fresh | Excellent |
| Loop Strategy | Low | Full | Fresh each iteration | N/A (single task) |
| Smart Handoff | Low | Manual trigger | Better compaction | Moderate |

## Official Feature Request

[Session Handoff Support (#11455)](https://github.com/anthropics/claude-code/issues/11455) - Requesting native handoff support in Claude Code CLI.

## Recommended Thresholds

From [Context Compaction Research](https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f):
- **85-90%**: Recommended threshold for action
- **95%**: Often too late
- Consider pruning old tool outputs before full compaction

## Our Assessment

For power_agents use case (multi-day development, complex implementations):
- **Continuous Claude** (Clear Strategy) is most relevant
- Loop Strategy useful for specific batch tasks
- Worth monitoring official feature request for native support
