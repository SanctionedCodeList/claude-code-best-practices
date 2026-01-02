# Best Practices for CLAUDE.md and AGENTS.md Files

## Overview

Both formats serve similar purposes but have distinct ecosystems:

| Format | Primary Tools | Scope |
|--------|--------------|-------|
| **CLAUDE.md** | Claude Code | Anthropic ecosystem |
| **AGENTS.md** | Codex, Cursor, Aider, Cline, Roo Code | Cross-tool standard |

---

## CLAUDE.md: Hierarchy & Locations

Claude Code uses a **four-tier hierarchy** (highest to lowest precedence):

| Level | Location | Shared? |
|-------|----------|---------|
| Enterprise | `/Library/Application Support/ClaudeCode/CLAUDE.md` | Org-wide |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team (git) |
| User Global | `~/.claude/CLAUDE.md` | Personal |
| Project Local | `./CLAUDE.local.md` | Personal (gitignored) |

**Monorepo support**: Claude recursively discovers files upward from cwd and loads nested files on-demand when working in subdirectories.

---

## CLAUDE.md Best Practices

### What to Include

Structure around **WHAT/WHY/HOW**:

```markdown
# Project Overview
- Framework: React 18 with TypeScript
- Package manager: pnpm with workspaces

# Commands
- `pnpm build` - Production build
- `pnpm test` - Run tests
- `pnpm lint` - ESLint check

# Architecture
- src/components/ - React components
- src/api/ - Backend endpoints

# Workflow
- Branch naming: feature/*, fix/*
- Commit style: Conventional Commits
```

### Key Principles from Anthropic

1. **Keep it concise** - Target under 300 lines; HumanLayer reports their root file is <60 lines
2. **Universal applicability only** - Every instruction should matter for every session
3. **Iterate like a prompt** - Tune with emphasis ("IMPORTANT", "YOU MUST") for better adherence
4. **Use `#` key** - Add memories during sessions that auto-save to CLAUDE.md

### Anti-Patterns to Avoid

From Anthropic's official guide and community:

- **Don't use as a linter** - LLMs are slow/expensive; use Biome, ESLint, Prettier
- **Avoid code style guidelines** - Let the agent infer from codebase examples
- **Don't auto-generate blindly** - `/init` is a starting point, not finished product
- **Skip task-specific instructions** - These dilute universally relevant context

### Advanced: Modular Rules

For larger projects, use `.claude/rules/`:

```
.claude/
├── CLAUDE.md              # Core instructions
└── rules/
    ├── testing.md         # Testing conventions
    ├── security.md        # Security requirements
    └── frontend/
        └── react.md       # React-specific rules
```

Rules can use **path-scoping** via YAML frontmatter:
```yaml
---
paths: src/api/**/*.ts
---
# API endpoints must include input validation
```

---

## AGENTS.md Best Practices

From GitHub's analysis of 2,500+ repositories:

### Six Core Areas to Cover

1. **Commands** - Put executable commands early (`npm test`, `pytest -v`)
2. **Testing** - How to run and write tests
3. **Project structure** - Where things live
4. **Code style** - With real examples, not prose
5. **Git workflow** - Branch naming, commit conventions
6. **Boundaries** - What's allowed vs prohibited

### Three-Tier Boundary System

```markdown
## Boundaries
✅ Always: Run lint before commits
⚠️ Ask first: Installing new packages
🚫 Never: Modify .env files, commit secrets
```

### Be Specific About Stack

**Bad**: "React project"
**Good**: "React 18 with TypeScript 5.3, Vite 5, Tailwind CSS 3.4"

### Use Examples Over Explanations

> "One real code snippet showing your style beats three paragraphs describing it."

### Monorepo Strategy

Place AGENTS.md in each package - agents read the nearest file in the directory tree:

```
packages/
├── api/
│   └── AGENTS.md      # API-specific instructions
├── web/
│   └── AGENTS.md      # Frontend-specific
└── AGENTS.md          # Shared conventions
```

---

## Community Tips from X/Twitter

### Workflow Patterns

> "The secret to getting good output is in the setup: Create a CLAUDE.md with best practices, use plan mode to write a detailed spec, make a to-do list and audit it before coding" - @petergyang

- Ask Claude to make a plan before coding
- Correct early if it goes off track (Escape key)
- Use `/clear` between distinct tasks
- Write "think", "think harder", or "ultrathink" for complex debugging

### Power User Tips

> "You can now quickly add memories using the # key. Tell Claude Code to remember specific tips and it'll reference that in future sessions." - @_catwu (Anthropic)

> "Every 1 unit of energy put into this spec gives you 10x leverage when AI starts writing code" - @GregKamradt

### Cross-Tool Compatibility

> "Use the same AGENTS.md file and MCP config for both droid and codex" - @elliotarledge

---

## Root vs Project Level: When to Use Each

| Instruction Type | Location | Example |
|-----------------|----------|---------|
| Personal preferences | `~/.claude/CLAUDE.md` | Editor settings, response style |
| Team standards | `./CLAUDE.md` | Commit conventions, PR format |
| Subproject rules | `./packages/api/CLAUDE.md` | API-specific patterns |
| Private overrides | `./CLAUDE.local.md` | Local sandbox URLs, test data |

---

## Template: Minimal Effective CLAUDE.md

```markdown
# Project
React 18 + TypeScript + Vite. pnpm workspaces.

# Commands
- `pnpm dev` - Start dev server
- `pnpm test` - Run Vitest
- `pnpm build` - Production build

# Key Paths
- src/components/ - UI components
- src/lib/ - Utilities
- src/api/ - Backend routes

# Conventions
- Conventional Commits for messages
- Feature branches: feature/description
- Run tests before committing

# IMPORTANT
- Never commit .env files
- Always run typecheck after changes
```

---

## Sources

- [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [GitHub Blog: How to Write a Great AGENTS.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [AGENTS.md Official Site](https://agents.md/)
- [@_catwu on X](https://x.com/_catwu/status/1913354716001739173)
- [@petergyang on X](https://x.com/petergyang/status/1963248146336866757)
