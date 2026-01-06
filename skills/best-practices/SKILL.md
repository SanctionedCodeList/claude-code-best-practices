---
name: best-practices
description: "Claude Code best practices: skill creation, plugin authoring, context injection, session history, Python setup, and configuration. Six sub-skills for power users."
---

# Best Practices

Tools and guidance for Claude Code power users.

## Decision Tree

| What do you need? | Go to |
|-------------------|-------|
| **Create a new skill** | [skill-creator/](./skill-creator/index.md) |
| **Author a plugin** | [plugin-authoring/](./plugin-authoring/index.md) |
| **Inject context (hooks, agents, MCP)** | [context-injection/](./context-injection/index.md) |
| **Search past sessions** | [sessions/](./sessions/index.md) |
| **Configure CLAUDE.md** | [claude-md/](./claude-md/index.md) |
| **Set up Python for agents** | [python-setup/](./python-setup/index.md) |

## Sub-Skills

### skill-creator

Comprehensive guide for building effective Claude Code skills. Covers:
- Skill anatomy (SKILL.md, scripts/, references/)
- Progressive disclosure patterns
- Data model design for AI systems
- Validation and packaging tools

### plugin-authoring

Guide for creating and distributing Claude Code plugins. Covers:
- Plugin vs skill distinction
- Directory structure and marketplace.json
- Single plugin vs multi-plugin marketplaces
- Installation workflow and storage locations

### context-injection

Guide to Claude Code's five context injection mechanisms. Covers:
- Skills, hooks, agents, commands, and MCP servers
- When to use each mechanism (decision tree)
- Token efficiency and progressive loading
- Hook patterns for common use cases

### sessions

Search and retrieve past Claude Code conversations. Features:
- Semantic search using embeddings
- Filtered message retrieval (by type, tool, position)
- Project-scoped session listing
- Metadata queries without loading full content

### claude-md

Guide for writing effective CLAUDE.md and AGENTS.md files. Covers:
- CLAUDE.md vs AGENTS.md (when to use which)
- File hierarchy and precedence
- Recommended sections (delegation, boundaries, writing style)
- Plugin issue reporting via git remote

### python-setup

Guide for configuring Python so Claude Code agents can reliably run scriptlets. Covers:
- Shell configuration (.zshenv vs .zshrc for non-interactive shells)
- pyenv/Homebrew PATH conflicts and resolution
- Heredoc syntax for Python scriptlets
- Package structure for agent-friendly libraries
- Troubleshooting common import failures

## Setup

Run the installer to set up dependencies:

```bash
./install.sh
```

This installs Python dependencies for the sessions sub-skill. The skill-creator sub-skill requires no setup.
