# Claude Code Best Practices

**Build effective Claude Code skills with proper structure and progressive disclosure.**

A plugin providing guidance, templates, and tools for creating professional-grade Claude Code skills.

---

## 🚀 Installation

### Option 1: Via SCL Marketplace (Recommended)

Install all SCL plugins at once:

```bash
claude plugins add SanctionedCodeList/SCL_marketplace
```

### Option 2: Standalone Installation

```bash
claude plugins add SanctionedCodeList/claude-code-best-practices
```

### Verify Installation

```bash
claude plugins list
# Should show: best-practices
```

### Try It Out

Start Claude Code and ask:

```
> Help me create a skill for generating API documentation
```

Claude will use the skill-creator skill to guide you through the process.

---

## What's Included

### Skill Creator Skill

The `skill-creator` skill provides step-by-step guidance for building effective Claude Code skills:

| Phase | What Happens |
|-------|--------------|
| **1. Understand** | Gather concrete examples of how the skill will be used |
| **2. Plan** | Identify reusable scripts, references, and assets |
| **3. Initialize** | Generate skill directory structure with templates |
| **4. Edit** | Implement SKILL.md and bundled resources |
| **5. Package** | Validate and create distributable .skill file |
| **6. Iterate** | Refine based on real usage |

---

## Key Concepts

### Progressive Disclosure

Skills use a three-level loading system to manage context efficiently:

| Level | When Loaded | Size Target |
|-------|-------------|-------------|
| **Metadata** | Always in context | ~100 words |
| **SKILL.md body** | When skill triggers | <5k words |
| **Bundled resources** | As needed | Unlimited |

### Skill Anatomy

```
my-skill/
├── SKILL.md           # Required: frontmatter + instructions
├── install.sh         # Optional: dependency installation
├── scripts/           # Executable code for deterministic tasks
├── references/        # Documentation loaded on-demand
└── assets/            # Files used in output (templates, images)
```

### Freedom Calibration

Match specificity to task fragility:

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** | Multiple valid approaches | Text-based instructions |
| **Medium** | Preferred pattern exists | Pseudocode with parameters |
| **Low** | Fragile, must be exact | Specific scripts |

---

## Creating a Skill

### Step 1: Initialize

```bash
# In Claude Code, ask:
> Create a new skill called "api-docs" for generating API documentation
```

The skill-creator will generate:

```
api-docs/
├── SKILL.md
├── scripts/
│   └── example.py
├── references/
│   └── example.md
└── assets/
    └── example.txt
```

### Step 2: Edit SKILL.md

The frontmatter is critical for triggering:

```yaml
---
name: api-docs
description: >
  Generate API documentation from code. Use when users ask to
  document APIs, create endpoint references, or generate OpenAPI specs.
---

# API Documentation Generator

## Workflow

1. Analyze source code for endpoints
2. Extract parameters and return types
3. Generate markdown documentation
...
```

### Step 3: Add Resources

| Directory | Purpose | Example |
|-----------|---------|---------|
| `scripts/` | Reusable code | `extract_endpoints.py` |
| `references/` | On-demand docs | `openapi-spec.md` |
| `assets/` | Output templates | `doc-template.md` |

### Step 4: Package

```bash
> Package the api-docs skill
```

Creates `api-docs.skill` for distribution.

---

## Best Practices

### Do

- Keep SKILL.md under 500 lines
- Put detailed content in `references/` files
- Use concrete examples over abstract explanations
- Test scripts before including them
- Include both `content` and `activeForm` for todos

### Don't

- Create README.md, CHANGELOG.md, or other auxiliary files
- Duplicate content between SKILL.md and references
- Include user-facing documentation (skills are for AI agents)
- Add complexity for hypothetical future needs

---

## Structured Output Design

When skills instruct LLMs to produce JSON:

| Guideline | Reason |
|-----------|--------|
| Keep under 30 fields | Performance degrades above this |
| Put reasoning before conclusions | Prevents short-circuiting |
| Use prose for analysis | AI reads prose fine |
| Limit nesting to 3 levels | Deep nesting causes failures |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not triggering | Check `description` in frontmatter covers the use case |
| Context too large | Move content to `references/` for on-demand loading |
| Scripts failing | Test scripts independently before packaging |
| Validation errors | Run packaging script to see specific issues |

---

## Links

- [GitHub](https://github.com/SanctionedCodeList/claude-code-best-practices)
- [SCL Marketplace](https://github.com/SanctionedCodeList/SCL_marketplace)
