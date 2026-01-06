# Multi-Agent Orchestration Patterns for Claude Code

Research on patterns, tools, and best practices for running multiple Claude Code agents in parallel.

## Why Multi-Agent?

Anthropic's research found that "a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2%."

**Key benefits:**
- Parallelization — work on multiple tasks simultaneously
- Context isolation — each agent gets a fresh 200k token window
- Specialization — agents can focus on specific domains
- Throughput — 2.8-4.4x speed improvement reported

## The Core Loop

From Anthropic's Claude Agent SDK:

```
gather context → take action → verify work → repeat
```

Subagents use isolated context windows and only send relevant information back to the orchestrator, making them ideal for tasks requiring sifting through large amounts of information.

## Proven Patterns

### 1. The 3 Amigo Agents Pattern

**Source:** George Vetticaden

Three specialized agents working in sequence:

| Agent | Role | Output |
|-------|------|--------|
| **PM Agent** | Requirements, PRDs, architecture | 8 specification documents |
| **UX Agent** | Prototypes, design system, components | 8 design artifacts |
| **Claude Code** | Implementation | Working MVP |

**Key insight:** Each agent builds on the previous one's work. The PM Agent's specifications become the UX Agent's design requirements. Progressive refinement creates rich, multi-layered context.

**Results:** "Transforming weeks of AI development into hours" — 3-hour implementation of enterprise-grade multi-agent health system.

### 2. Orchestrator/Worker Pattern

**Source:** Anthropic's multi-agent research

```
Meta-Agent (Orchestrator)
    ├── Worker Agent 1 (Frontend)
    ├── Worker Agent 2 (Backend)
    ├── Worker Agent 3 (Testing)
    └── Worker Agent 4 (Docs)
```

**Key principle:** The meta-agent "doesn't write code — it manages other agents." It breaks requirements into independent, parallelizable tasks with dependency tracking via topological sorting.

### 3. Shared Planning Document Pattern

**Source:** Multi-agent architecture article

Four specialized Claude Code agents run in separate VSCode terminals with distinct roles. Coordination happens through a simple shared planning document that acts as their communication hub.

**Why it works:** Mirrors how high-performing human teams operate — clear roles, shared context, regular communication, built-in quality checks.

### 4. Scout Pattern

**Source:** Jesse Vincent via Simon Willison

> "Send out a scout" — Hand the AI agent a task just to find out where the sticky bits are. Give the agent a genuinely difficult task against a large codebase, with no intention of actually landing its code, just to get ideas from which files it modifies and how it approaches the problem.

**Use case:** Exploration and proof of concept before committing to an approach.

### 5. Assembly Line Pattern (Sequential Handoffs)

One agent's output becomes the next agent's input:

```
Planning Agent → Implementation Agent → Review Agent → Iteration Agent
```

**Key insight:** Automates entire lifecycles. Each stage has clear inputs and outputs.

## Creating Subagents

### File Structure

```
~/.claude/agents/          # User-level agents
./.claude/agents/          # Project-level agents
```

Or use `/agents` command during a Claude Code session.

### Basic Agent Definition

```yaml
---
name: senior-engineer
description: Takes lightly specified tickets, discovers context, plans sanely, ships code with tests
model: opus
---

# Agent Behavior

## operating principles
- Emphasize reuse over invention
- Keep changes reversible
- Ship with tests

## working loop
1. Analyze requirements
2. Discover existing patterns
3. Plan implementation
4. Execute with tests
5. Review own work
```

### Specialist Agent Examples

| Agent | Focus |
|-------|-------|
| **Product Manager** | User stories, acceptance criteria, PRDs |
| **UX Designer** | All user states (loading, empty, error, success), accessibility |
| **Code Reviewer** | Blockers, high-priority issues, actionable improvements |
| **Security Auditor** | CVE scanning, vulnerability analysis |

## Coordination Strategies

### File Locking

Prevent simultaneous modification of interdependent files:

```python
# Redis-based lock with timeout
lock = redis.SET(f"lock:{filepath}", agent_id, nx=True, ex=300)
```

### Conflict Prevention

- Analyze import/export relationships between files
- Check for shared critical dependencies before parallel work
- Prevent simultaneous modification of interdependent files

### Resource Management

| Resource | Threshold |
|----------|-----------|
| CPU | 80% before halting new agents |
| Memory | 85% before rejecting spawns |
| Per-agent limits | 2GB memory max |

### Communication Hub Options

1. **Shared markdown file** — Simple, works as crude shared memory
2. **Beads** — Git-backed issue tracker (survives compaction)
3. **Redis queue** — Task distribution for 10+ agents
4. **memory.md** — Continuity layer for multi-session projects

## Infrastructure Options

### Simple (Terminal Windows)

```bash
# Terminal 1: Frontend agent
claude --resume session-frontend

# Terminal 2: Backend agent
claude --resume session-backend

# Terminal 3: Testing agent
claude --resume session-testing
```

### Git Worktrees (Isolation)

```bash
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
# Run separate agents in each worktree
```

### Docker Containers (Blast Radius)

Limit damage from agent mistakes:
```yaml
resources:
  cpu_quota: 50000
  memory_max: 2GB
```

### Orchestration Tools

| Tool | Description |
|------|-------------|
| **Gastown** | Steve Yegge's 20-30 agent orchestrator built on Beads |
| **Claude-Flow** | MCP-based swarm intelligence with AgentDB memory |
| **Agentrooms** | Routes tasks to specialists via @mentions |

## Claude-Flow Details

Enterprise orchestration platform with:

- **Hive-Mind mode** — Complex projects with persistent SQLite memory
- **25 Claude Skills** — Activate via natural language
- **AgentDB** — Semantic vector search (96x faster than baseline)
- **100+ MCP tools** — Direct Claude Code integration

**Installation:**
```bash
npm install -g @anthropic-ai/claude-code
npx claude-flow@alpha init --force
claude mcp add claude-flow npx claude-flow@alpha mcp start
```

**Performance claims:** 84.8% SWE-Bench solve rate, 32.3% token reduction.

## Best Practices

### Task Selection for Parallelization

**Good candidates:**
- Research and proof of concepts
- Knowledge retrieval / codebase exploration
- Low-stakes maintenance (deprecation warnings, test fixes)
- Well-specified implementation work

**Poor candidates:**
- Tasks with unclear requirements
- Highly interdependent changes
- Work requiring deep context continuity

### Quality Safeguards

1. **Version control agent definitions** — Treat like code
2. **Create evaluation suites** — Monitor for consistency
3. **Maintain clear handoff artifacts** — Debug trail between agents
4. **Document output file locations** — Audit trail for synthesis failures

### The Bottleneck

> "The bottleneck isn't agent output speed—it's review capacity."

Parallelization succeeds when tasks genuinely operate independently of primary cognitive focus. Don't parallelize if you can't review the output.

### Cost Management

> "Chaining agents, especially in a loop, will increase your token usage significantly. This means you'll hit the usage caps on plans like Claude Pro/Max much faster."

**Trade-off:** Dramatically increased output and velocity at the cost of higher usage.

**Approximate costs (heavy usage):**
- API: ~$50/day
- Infrastructure: ~$20/day

### Handling Non-Determinism

LLM variability means workflow changes ripple unpredictably. Requires:
- Low cost-of-failure mindset
- Creative engineering for graceful failure handling
- "Taking more shots on goal"

## Evolution Stages

Steve Yegge's framework for developer AI evolution:

| Stage | Description | Agents |
|-------|-------------|--------|
| 1-4 | IDE-based, permissions evolving | 1 |
| 5 | CLI, single agent, YOLO | 1 |
| 6 | CLI, multi-agent (3-5 parallel) | 3-5 |
| 7 | 10+ agents, hand-managed | 10+ |
| 8 | Building your own orchestrator | 20-30+ |

**Warning:** Stage 7+ is "an industrialized coding factory manned by superintelligent chimpanzees" — requires experienced agent-wrangling skills.

## Sources

### Patterns & Tutorials
- [Multi-Agent Orchestration: Running 10+ Claude Instances](https://dev.to/bredmond1019/multi-agent-orchestration-running-10-claude-instances-in-parallel-part-3-29da)
- [Embracing Parallel Coding Agents - Simon Willison](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/)
- [How to Use Claude Code Subagents - Zach Wills](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development)
- [The 3 Amigo Agents Pattern - George Vetticaden](https://medium.com/@george.vetticaden/the-3-amigo-agents-the-claude-code-development-pattern-i-discovered-while-implementing-anthropics-67b392ab4e3f)

### Tools
- [Claude-Flow](https://github.com/ruvnet/claude-flow) — Swarm orchestration with MCP
- [Gastown](https://github.com/steveyegge/gastown) — Multi-agent workspace manager
- [Claude Code Agentrooms](https://claudecode.run/) — @mention-based coordination

### Official
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [Andrew Ng's Claude Code Course](https://x.com/AndrewYNg) — Anthropic partnership
