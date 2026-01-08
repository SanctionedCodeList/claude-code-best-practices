---
name: cc-dev
description: "Claude Code development guide: plugin authoring, context injection, session history, Python setup, and configuration. Five sub-skills for power users."
---

# CC Dev

Tools and guidance for Claude Code power users.

## Decision Tree

| What do you need? | Go to |
|-------------------|-------|
| **Author a plugin** | [plugin-authoring/](./plugin-authoring/index.md) |
| **Inject context (hooks, agents, MCP)** | [context-injection/](./context-injection/index.md) |
| **Search past sessions** | [sessions/](./sessions/index.md) |
| **Configure CLAUDE.md** | [claude-md/](./claude-md/index.md) |
| **Set up Python for agents** | [python-setup/](./python-setup/index.md) |

## Sub-Skills

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

This installs Python dependencies for the sessions sub-skill.
