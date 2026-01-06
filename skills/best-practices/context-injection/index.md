# Context Injection Mechanisms

Claude Code provides five ways to inject context into conversations. Each serves different use cases.

## Overview

| Mechanism | Trigger | Use Case | Token Cost |
|-----------|---------|----------|------------|
| **Skills** | Automatic (LLM matches description) | Domain knowledge, workflows | Progressive (30-5K) |
| **Hooks** | Event-driven | Auto-inject git status, standards | Per-event |
| **Agents** | Spawned as subagents | Specialized workers | Isolated context |
| **Commands** | User invokes `/command` | On-demand actions | On-demand |
| **MCP Servers** | Tool calls | External APIs, persistent state | Per-call |

## Decision Tree

| You need... | Use |
|-------------|-----|
| Domain-specific guidance that activates automatically | Skills |
| Context injected at session start or before prompts | Hooks |
| Specialized worker with focused instructions | Agents |
| User-triggered workflow or shortcut | Commands |
| External tool integration or persistent data | MCP Servers |

---

## 1. Skills

Prompt templates injected on-demand when Claude determines relevance.

### How Selection Works

Claude uses **LLM reasoning** to select skills — no algorithmic matching:

1. All skill names/descriptions are formatted in the Skill tool's prompt
2. Claude matches descriptions to user intent via natural language
3. If matched, Claude invokes the Skill tool

**Implication:** Write precise, unique descriptions. Vague descriptions lead to wrong skill selection.

### Two-Message Injection Pattern

When a skill activates, Claude Code injects two messages:

1. **Visible metadata** — User sees "The skill is loading"
2. **Hidden instructions** — Full SKILL.md sent to API but hidden from UI

### Token Efficiency: Three-Tier Loading

| Phase | Token Cost | When Loaded |
|-------|-----------|-------------|
| Metadata | 30-50 tokens | Always (name + description) |
| Triggered | 500-5,000 tokens | When skill activates |
| Active | Variable | Supporting files on-demand |

### Best Practices

- Keep descriptions precise — Claude uses them for matching
- Minimize `allowed-tools` — Only include what's needed
- Use progressive disclosure — Load references on-demand
- Bundle scripts for deterministic tasks (PDF parsing, data sorting)

---

## 2. Hooks

Shell commands that run at lifecycle events and inject context.

### Hook Events

| Event | When | Injection Use Case |
|-------|------|-------------------|
| `SessionStart` | Session begins | Git status, TODO lists, project state |
| `UserPromptSubmit` | Before processing prompt | Sprint priorities, coding standards |
| `PreToolUse` | Before tool execution | Security checks, validation rules |
| `PostToolUse` | After tool execution | Formatting, logging |

### Configuration

In `.claude/settings.json` or plugin's `hooks/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "./scripts/load-context.sh"
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "cat ./project-standards.md"
          }
        ]
      }
    ]
  }
}
```

### Context Injection Methods

**Plain text stdout:**
```bash
#!/bin/bash
echo "Current sprint: Sprint 23"
echo "Focus: API refactoring"
cat ./coding-standards.md
```

**Structured JSON:**
```json
{
  "additionalContext": "Project uses TypeScript strict mode...",
  "continue": true
}
```

### Best Practices

- Use `SessionStart` for project context (git status, TODOs)
- Use `UserPromptSubmit` for always-applicable standards
- Keep output concise — every token counts
- Use `${CLAUDE_PLUGIN_ROOT}` for portable paths

---

## 3. Agents

Specialized subagents with focused system prompts.

### Structure

```
plugin-name/
└── agents/
    └── security-reviewer.md
```

### Agent Definition

```yaml
---
name: security-reviewer
description: Reviews code for OWASP vulnerabilities
allowed-tools: "Read,Grep,Glob"
---

# Security Review Agent

You are a security specialist. When reviewing code:
1. Check for injection vulnerabilities
2. Verify authentication patterns
3. Assess data validation
```

### When to Use

- Task requires specialized expertise
- Work can be delegated and summarized
- Isolated context prevents pollution of main conversation

### Invocation

- Claude spawns automatically based on task context
- Users invoke via `/agents` command
- Agents run with their own scoped context

---

## 4. Commands

Slash commands for explicit user control.

### Structure

```
plugin-name/
└── commands/
    └── review.md
```

### Command Definition

```yaml
---
description: Run comprehensive code review
---

# Code Review Workflow

1. Analyze the diff with `git diff`
2. Check each file for:
   - Type safety issues
   - Missing tests
   - Documentation gaps
3. Generate review summary
```

### When to Use

- User should explicitly trigger the action
- Workflow is too specific for automatic activation
- Action has side effects user should control

### Invocation

```
/plugin-name:review
```

---

## 5. MCP Servers

External tool integrations via Model Context Protocol.

### Configuration

In plugin's `.mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-memory"]
    }
  }
}
```

### When to Use

- Need persistent state across sessions
- Integrating external APIs or databases
- Tool requires runtime execution environment

---

## Comparison: Mechanisms vs CLAUDE.md

| Aspect | Injection Mechanisms | CLAUDE.md |
|--------|---------------------|-----------|
| **Loading** | On-demand or event-triggered | Always loaded at startup |
| **Scope** | Temporary, scoped | Persistent across sessions |
| **Control** | Plugin author | User/team |
| **Token cost** | Progressive (30-5000) | Full content always |
| **Sharing** | Via marketplace | Via git repository |

**Key insight:** CLAUDE.md is for persistent user preferences. Injection mechanisms are for on-demand, context-specific instructions.

---

## Example: SessionStart Context Injection

**hooks.json:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/inject-context.sh"
      }
    ]
  }
}
```

**inject-context.sh:**
```bash
#!/bin/bash

echo "## Project Context"
echo "- Framework: Next.js 14"
echo "- Current sprint: API v2 migration"
echo ""
echo "## Recent Changes"
git log --oneline -5
echo ""
echo "## Open Issues"
gh issue list --limit 3
```

---

## References

- [Hooks Documentation](https://code.claude.com/docs/en/hooks)
- [Skills Documentation](https://code.claude.com/docs/en/skills)
- [MCP Servers](https://code.claude.com/docs/en/mcp)
- [Example hook patterns](./references/hook-patterns.md)
