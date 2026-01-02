# Claude Code Plugin Context Injection

How plugins inject custom instructions and context into Claude Code sessions.

---

## Key Insight: Plugins Don't Modify CLAUDE.md

Plugins **do not directly inject content into CLAUDE.md files**. Instead, they use five distinct mechanisms to supplement the conversation context:

1. **Skills** - Prompt templates injected on-demand
2. **Hooks** - Event-triggered context injection
3. **Agents** - Specialized subagents with custom prompts
4. **Commands** - User-invoked workflows
5. **MCP Servers** - External tool integrations

CLAUDE.md remains user/team-controlled, while plugins provide supplementary capabilities.

---

## 1. Skills: On-Demand Context Injection

Skills are the primary mechanism for injecting domain-specific instructions.

### Architecture

Skills are **not executable code** - they are prompt templates that inject instructions into conversation context when activated.

```
plugin-name/
└── skills/
    └── my-skill/
        ├── SKILL.md           # Instructions + frontmatter
        ├── scripts/           # Optional executables
        └── references/        # Documentation files
```

### SKILL.md Structure

```yaml
---
name: code-reviewer
description: Automated code review with best practices
allowed-tools: "Read,Glob,Grep"
model: sonnet  # Optional model override
---

# Code Review Instructions

When reviewing code, follow these steps:
1. Check for security vulnerabilities
2. Verify naming conventions
3. Assess test coverage
...
```

### Two-Message Injection Pattern

When a skill activates, Claude Code injects two messages:

1. **Visible metadata** (`isMeta: false`):
   ```xml
   <command-message>The "code-reviewer" skill is loading</command-message>
   ```

2. **Hidden instructions** (`isMeta: true`):
   - Full SKILL.md content (500-5,000 words)
   - Sent to Claude API but hidden from UI
   - Guides Claude's reasoning and behavior

### Token Efficiency: Three-Tier Loading

| Phase | Token Cost | When Loaded |
|-------|-----------|-------------|
| Metadata | 30-50 tokens | Always (name + description in system prompt) |
| Triggered | 500-5,000 tokens | When Claude determines relevance |
| Active | Variable | Supporting files accessed on-demand |

### Skill Selection

Claude uses **LLM reasoning** to select skills - no algorithmic matching:

1. All skill names/descriptions formatted in the Skill tool's prompt
2. Claude matches descriptions to user intent via natural language
3. If matched, Claude invokes the Skill tool

### Execution Context Modification

Skills can modify Claude's environment:

```yaml
allowed-tools: "Read,Write,Bash"  # Restricts available tools
model: opus                        # Overrides model selection
```

---

## 2. Hooks: Event-Triggered Injection

Hooks run shell commands at specific lifecycle events and can inject context.

### Hook Types for Context Injection

| Hook | When | Use Case |
|------|------|----------|
| `SessionStart` | Session begins | Load dev context, git status, TODO lists |
| `UserPromptSubmit` | Before processing prompt | Add sprint priorities, project standards |
| `PreToolUse` | Before tool execution | Security checks, validation |
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

**1. Plain text stdout** (simple):
```bash
#!/bin/bash
# load-context.sh
echo "Current sprint: Sprint 23"
echo "Focus: API refactoring"
cat ./coding-standards.md
```

**2. Structured JSON** (advanced):
```json
{
  "additionalContext": "Project uses TypeScript strict mode...",
  "continue": true
}
```

### How It Works

```
User types: "Write a new API endpoint"
     ↓
Hook runs: ./load-context.sh
     ↓
Output injected: [Project standards + conventions]
     ↓
Claude sees: [Injected context] + "Write a new API endpoint"
```

---

## 3. Agents: Specialized Subagents

Plugins can define specialized agents with focused system prompts.

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
...
```

### Invocation

- Claude can invoke agents automatically based on task context
- Users can invoke via `/agents` command
- Agents run with their own scoped context

---

## 4. Commands: User-Invoked Workflows

Slash commands provide explicit user control.

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

1. First, analyze the diff with `git diff`
2. Check each file for:
   - Type safety issues
   - Missing tests
   - Documentation gaps
3. Generate review summary
```

### Invocation

```
/plugin-name:review
```

---

## 5. MCP Servers: External Tools

MCP servers provide external tool integrations.

### Configuration

In plugin's `.mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

---

## Plugin Manifest

The `.claude-plugin/plugin.json` defines all components:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "agents": "./agents/",
  "commands": ["./commands/review.md"],
  "mcpServers": "./.mcp.json"
}
```

---

## Comparison: Plugin Context vs. CLAUDE.md

| Aspect | Plugins | CLAUDE.md |
|--------|---------|----------|
| **Loading** | On-demand (skills) or event-triggered (hooks) | Always loaded at startup |
| **Scope** | Temporary, scoped to skill/session | Persistent across all sessions |
| **Control** | Plugin author defines | User/team controls |
| **Token cost** | Progressive (30-5000 tokens) | Full content always loaded |
| **Sharing** | Via marketplace | Via git repository |
| **Modification** | Install/enable plugins | Edit files directly |

---

## Best Practices for Plugin Authors

### Skills

1. **Keep descriptions precise** - Claude uses them for matching
2. **Minimize allowed-tools** - Only include what's needed
3. **Use progressive disclosure** - Load supporting files on-demand
4. **Bundle scripts for deterministic tasks** - PDF parsing, data sorting

### Hooks

1. **Use SessionStart for context** - Git status, TODO lists, project state
2. **Use UserPromptSubmit for standards** - Always-applicable conventions
3. **Keep output concise** - Every token counts
4. **Use `${CLAUDE_PLUGIN_ROOT}`** - For portable paths

### General

1. **Don't duplicate CLAUDE.md** - Skills supplement, not replace
2. **Test token overhead** - Monitor context consumption
3. **Document clearly** - Users should understand what gets injected

---

## Example: SessionStart Context Injection

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

```bash
#!/bin/bash
# inject-context.sh

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

## Sources

- [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [Claude Code Plugins README](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)
- [Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Skills Documentation](https://code.claude.com/docs/en/skills.md)
- [Complete Guide to Claude Skills](https://tylerfolkman.substack.com/p/the-complete-guide-to-claude-skills)
