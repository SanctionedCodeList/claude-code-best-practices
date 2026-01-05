---
name: best-practices
description: "Claude Code best practices: skill creation guidance and session history search. Two sub-skills for power users."
---

# Best Practices

Tools and guidance for Claude Code power users.

## Decision Tree

| What do you need? | Go to |
|-------------------|-------|
| **Create a new skill** | [skill-creator/](./skill-creator/SKILL.md) |
| **Search past sessions** | [sessions/](./sessions/SKILL.md) |

## Sub-Skills

### skill-creator

Comprehensive guide for building effective Claude Code skills. Covers:
- Skill anatomy (SKILL.md, scripts/, references/)
- Progressive disclosure patterns
- Data model design for AI systems
- Validation and packaging tools

### sessions

Search and retrieve past Claude Code conversations. Features:
- Semantic search using embeddings
- Filtered message retrieval (by type, tool, position)
- Project-scoped session listing
- Metadata queries without loading full content

## Setup

Run the installer to set up dependencies:

```bash
./install.sh
```

This installs Python dependencies for the sessions sub-skill. The skill-creator sub-skill requires no setup.
