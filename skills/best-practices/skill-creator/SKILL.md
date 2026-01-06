---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
license: Complete terms in LICENSE.txt
---

# Skill Creator

This skill provides guidance for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

- **High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.
- **Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.
- **Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

## Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
├── install.sh (optional) - Dependency installation script
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): Contains `name` and `description` fields. These are the only fields that Claude reads to determine when the skill gets used, thus it is very important to be clear and comprehensive in describing what the skill is, and when it should be used.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

### install.sh (optional)

If a skill requires software dependencies (Python packages, Node modules, etc.), include an `install.sh` script at the skill's root. SKILL.md should instruct the agent to run this script before proceeding:

```markdown
Before using this skill, run the installation script: `./install.sh`
```

**Requirements for install.sh:**
- **Idempotent**: Safe to run multiple times
- **User-space only**: Install to user directories, never globally (no sudo)
- **Cross-platform**: Handle platform differences internally
- **Clear exit status**: Must exit with success (0) or failure (non-zero) so the agent knows whether to proceed
- **Informative errors**: Always output clear error messages on failure so agents or users can diagnose and resolve issues

### Bundled Resources (optional)

#### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Issue reporting**: If scripts contain non-trivial logic that may have bugs, include where to report issues in SKILL.md

#### References (`references/`)

Documentation and reference material intended to be loaded as needed into context.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: Database schemas, API documentation, domain knowledge, company policies
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md

#### Assets (`assets/`)

Files not intended to be loaded into context, but used within the output Claude produces.

- **When to include**: When the skill needs files for the final output (templates, images, icons, fonts)
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

### What to Not Include in a Skill

Do NOT create extraneous documentation or auxiliary files like README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md, etc. The skill should only contain information needed for an AI agent to do the job.

## Progressive Disclosure

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (unlimited)

**Keep SKILL.md body under 500 lines.** Split content into separate files when approaching this limit. Reference split files from SKILL.md with clear guidance on when to read them.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details to reference files.

For detailed patterns and examples, see [progressive-disclosure-patterns.md](references/progressive-disclosure-patterns.md).

## Skill Creation Process

Skill creation involves these steps:

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill (run init_skill.py)
4. Edit the skill (implement resources and write SKILL.md)
5. Package the skill (run package_skill.py)
6. Iterate based on real usage

Follow these steps in order, skipping only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood.

To create an effective skill, understand concrete examples of how the skill will be used. Ask questions like:

- "What functionality should the skill support?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

Analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

**Examples:**
- `pdf-editor` skill: A `scripts/rotate_pdf.py` script avoids rewriting the same code each time
- `frontend-webapp-builder` skill: An `assets/hello-world/` template provides reusable boilerplate
- `big-query` skill: A `references/schema.md` file documents table schemas to avoid rediscovery

### Step 3: Initializing the Skill

Skip this step if the skill already exists.

When creating a new skill from scratch, run the `init_skill.py` script:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:
- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

### Step 4: Edit the Skill

Remember that the skill is being created for another instance of Claude to use. Include information that would be beneficial and non-obvious.

#### Learn Proven Design Patterns

Consult these guides based on your skill's needs:

- **Multi-step processes**: See [workflows.md](references/workflows.md) for sequential workflows and conditional logic
- **Specific output formats or quality standards**: See [output-patterns.md](references/output-patterns.md) for template and example patterns
- **Testable code examples**: See [testable-code-examples.md](references/testable-code-examples.md) for validating code snippets
- **Data models and structured output**: See [data-models.md](references/data-models.md) for schema design best practices

#### Start with Reusable Skill Contents

Begin implementation with the reusable resources identified in Step 2. This may require user input (e.g., brand assets, documentation).

Added scripts must be tested by actually running them. Delete any example files and directories not needed for the skill.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

##### Frontmatter

Write the YAML frontmatter with `name` and `description`:

- `name`: The skill name
- `description`: This is the primary triggering mechanism for your skill.
  - Include both what the Skill does and specific triggers/contexts for when to use it
  - Include all "when to use" information here—not in the body (the body is only loaded after triggering)

Do not include any other fields in YAML frontmatter.

##### Body

Write instructions for using the skill and its bundled resources.

**Issue reporting for functional code**: If the skill includes scripts or libraries, include a section specifying where to report issues (e.g., GitHub repository URL).

### Step 5: Packaging a Skill

Once development is complete, package into a distributable .skill file:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script will:

1. **Validate** the skill (frontmatter, naming, structure, description quality)
2. **Package** the skill if validation passes, creating a .skill file (a zip with .skill extension)

If validation fails, fix errors and run again.

### Step 6: Iterate

After testing the skill, users may request improvements.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

## Advanced Tools

For complex skills with composable content or validation needs, see [advanced-tools.md](references/advanced-tools.md) for:
- Template build system (Jinja2 for shared fragments)
- Structure validation (link checking, orphan detection, depth limits)

## Reporting Issues

If you encounter bugs with the skill creation tools, or want to request new features:

```bash
# Report a bug
gh issue create --repo SanctionedCodeList/claude-code-best-practices --title "Bug: [description]" --body "## Problem\n[Describe the issue]\n\n## Script affected\n[e.g., init_skill.py, package_skill.py]\n\n## Error message\n[Include any error output]\n\n## Steps to reproduce\n[How to trigger it]"

# Check existing issues first
gh issue list --repo SanctionedCodeList/claude-code-best-practices
```

## Additional References

- [workflows.md](references/workflows.md) - Sequential workflows and conditional logic patterns
- [output-patterns.md](references/output-patterns.md) - Template and example patterns for output quality
- [testable-code-examples.md](references/testable-code-examples.md) - Validating code snippets in documentation
- [progressive-disclosure-patterns.md](references/progressive-disclosure-patterns.md) - Patterns for organizing content to minimize context usage
- [data-models.md](references/data-models.md) - Data model design and structured output best practices
- [advanced-tools.md](references/advanced-tools.md) - Template build system and structure validation
