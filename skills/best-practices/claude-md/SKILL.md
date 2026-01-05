---
name: claude-md
description: "Guide for writing effective CLAUDE.md and AGENTS.md files. Covers file hierarchy, recommended sections, and plugin issue reporting."
---

# CLAUDE.md & AGENTS.md Guide

Configure Claude Code and other AI coding assistants with persistent instructions.

## CLAUDE.md vs AGENTS.md

| File | Ecosystem | Tools |
|------|-----------|-------|
| **CLAUDE.md** | Anthropic | Claude Code |
| **AGENTS.md** | Cross-tool standard | Cursor, Codex, Aider, Cline, Roo Code |

Use CLAUDE.md for Claude Code-specific features. Use AGENTS.md for instructions that should work across multiple AI coding tools.

## CLAUDE.md Hierarchy

Claude Code loads instructions from multiple locations in this order (later files override earlier):

| Priority | Location | Scope | Git |
|----------|----------|-------|-----|
| 1 | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Enterprise/org-wide | No |
| 2 | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project (team) | Yes |
| 3 | `~/.claude/CLAUDE.md` | User global | No |
| 4 | `./CLAUDE.local.md` | Project local (personal) | No (gitignore) |

**Typical setup:**
- **User global** (`~/.claude/CLAUDE.md`): Personal preferences, delegation style, writing conventions
- **Project** (`./CLAUDE.md`): Tech stack, testing commands, code style, team conventions

## Best Practices

### Length
- Keep under 300 lines (some recommend under 60)
- Include only universally applicable instructions
- Move specialized content to project-level files

### Structure
Organize by concern:

```markdown
# Global Instructions

## Approach
[How to work: planning, thinking, tools]

## Context Management
[Timeouts, polling, output verbosity]

## Boundaries
[Always/ask first/never rules]

## Writing Style
[Documentation, comments, communication]
```

### Iteration
Treat CLAUDE.md like a prompt—iterate based on results:
- Use emphasis for critical rules: "IMPORTANT:", "YOU MUST", "NEVER"
- Add the `#` key during sessions to capture learnings as memories
- Review and consolidate periodically

## Recommended Sections

### Delegation & Subagents
```markdown
## Delegation

Act as a manager of subagents. Delegate to conserve context and increase speed.

**When to delegate:**
- Research, exploration, information gathering
- File searches across large codebases
- Independent subtasks

**Run subagents in parallel** when tasks are independent.

**Subagent output pattern:** Return only:
- Success/failure status
- Brief summary
- File paths to detailed results
```

### Boundaries
```markdown
## Boundaries

**Always:**
- Run tests/typecheck after code changes
- Commit frequently with clear messages

**Ask first:**
- Deleting files or significant refactors
- Installing new dependencies

**Never:**
- Commit secrets or credentials
- Skip tests to save time
- Make changes outside requested scope
```

### Plugin Issue Reporting
```markdown
## Plugin Feedback & Issues

Submit issues to the correct repository by checking the plugin's git remote:

\`\`\`bash
SKILL_DIR="<base directory from skill header>"
PLUGIN_ROOT=$(cd "$SKILL_DIR" && while [ ! -d .git ] && [ "$PWD" != "/" ]; do cd ..; done && pwd)
REPO=$(git -C "$PLUGIN_ROOT" remote get-url origin | sed -E 's#.*github\.com[:/]([^/]+/[^/.]+)(\.git)?$#\1#')

gh issue create --repo "$REPO" --title "Bug: [description]" --body "## Problem
[Describe the issue]

## Steps to reproduce
[Minimal example]"
\`\`\`
```

See [plugin-issue-reporting.md](./references/plugin-issue-reporting.md) for details on how this works.

## Complete Example

See [example-claude-md.md](./references/example-claude-md.md) for a complete working example covering:
- Delegation patterns
- Approach and planning
- Context management
- Boundaries
- Professional writing style
- Decision-making responses

## References

- [Example CLAUDE.md](./references/example-claude-md.md) — Complete working example
- [Plugin Issue Reporting](./references/plugin-issue-reporting.md) — Git remote solution for agents
