# Knowledge Base Skills

Skills designed to be both read and written by agents. Unlike typical skills that provide static guidance, knowledge base skills are living documents that agents update as they learn.

## When to Use This Pattern

Use a knowledge base skill when:

- Domain expertise accumulates over time (legal doctrines, API references, company policies)
- Agents should capture learnings for future sessions
- Content needs version control but also immediate availability
- The knowledge has natural structure that benefits from hierarchical organization

## Key Characteristics

| Aspect | Standard Skill | Knowledge Base Skill |
|--------|----------------|---------------------|
| **Updates** | Developer edits | Agents edit during work |
| **Location** | Plugin or `~/.claude/skills/` | `~/.claude/skills/` (symlinked) |
| **Reload** | May require restart | Hot reload (immediate) |
| **Self-documenting** | Optional | Required (maintenance guide) |

## Setup

### 1. Git Repository for Version Control

Keep the skill in a git repository for history and backup:

```
~/Projects/my-knowledge-base/
├── .git/
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       ├── maintaining.md
│       └── [domain folders]
└── README.md
```

### 2. Symlink to ~/.claude/skills/

Symlink the skill directory (not the repo root) for hot reload:

```bash
ln -s ~/Projects/my-knowledge-base/skills/my-skill ~/.claude/skills/my-skill
```

**Why symlink?**
- Edits apply immediately (no restart)
- Git tracks changes in the source repo
- Multiple skills can live in one repo

### 3. Self-Maintenance Guide

Every knowledge base skill needs a maintenance guide. Place `maintaining.md` at the skill root with:
- Content organization explanation
- Step-by-step for adding each content type
- Writing style guidelines
- Validation checklist

Link from SKILL.md:
```markdown
**Self-maintaining:** See [maintaining.md](./maintaining.md) when updating this knowledge base.
```

## Navigation Pattern

The folder structure encodes a knowledge hierarchy optimized for progressive context-building:

```
SKILL.md → topic/index.md → topic/subtopic.md
```

An agent traversing this path accumulates context progressively:
1. **SKILL.md** provides routing and skill-wide concepts
2. **topic/index.md** provides knowledge shared by all files in that folder
3. **topic/subtopic.md** provides specific details

This keeps the knowledge base DRY—shared concepts live in index files, not repeated in each child.

## Domains

Top-level folders under SKILL.md that are part of the knowledge hierarchy are called **domains**. Domains represent the primary organizational divisions of the knowledge base. Each skill defines its own domains based on its subject matter—there's no universal schema.

### Choosing Domains

Ask: What are the major categories of knowledge in this skill? Domains should be:
- **Mutually exclusive** — content belongs in one domain, not multiple
- **Collectively exhaustive** — together they cover the skill's scope
- **Meaningful to users** — reflect how practitioners think about the subject

### Example: Developer Skill (Toolchain-Centric)

A development knowledge base organized by language and tooling:

| Domain | Folder | Purpose |
|--------|--------|---------|
| **Python** | `python/` | Python project setup, style, async, testing |
| **TypeScript** | `typescript/` | TypeScript project setup, style, async, testing |
| **Publishing** | `publishing/` | Open source release guidance |
| **References** | `references/` | Third-party library documentation |

Domains are parallel—each language folder has similar structure. Knowledge doesn't build across domains; Python and TypeScript are independent.

### Example: Lawyer Skill (Layered)

A legal knowledge base with layered architecture:

| Domain | Folder | Purpose |
|--------|--------|---------|
| **Doctrine** | `law/` | What the law says (neutral, authoritative) |
| **Advocacy** | `advocacy/` | How to argue it (attack/defense patterns) |
| **Tasks** | Multiple folders | Specific deliverables and workflows |

Domains are layered—advocacy references doctrine, tasks reference both. Knowledge builds vertically, so DRY matters: update doctrine once, and advocacy/task content cross-references it.

### Domain Design Principles

**Flat/parallel domains** work when content areas are independent (languages, product lines, geographic regions). Each domain is self-contained.

**Layered domains** work when knowledge builds on itself (rules → interpretation → application). Lower layers are referenced by higher layers, reducing duplication.

## File Organization

### SKILL.md (Root)

The root index. Contains:
- Skill-wide principles and quick reference
- Links to all domains with descriptions

Target: Keep under 500 lines. Overflow to peer files or subfolders when necessary.

### Index Files (index.md)

Every folder has an `index.md` that:
- Describes the folder's scope
- Contains knowledge shared by ALL children
- Links to all files and subfolders within

Index files are not just routing—they contain substantive shared context that children build upon.

### Content Files

Specific topics that build on their parent index. An agent reading a content file should have already read the index.

### When to Split vs. Subfolder

As content grows beyond ~500 lines, ask: **Do these sections share common knowledge?**

| Scenario | Action |
|----------|--------|
| Sections are independent (no shared concepts) | Split into peer files in same folder |
| Sections share common concepts | Create subfolder; put shared concepts in `index.md`, specifics in child files |

The subfolder approach factors out common knowledge, keeping the knowledge base DRY.

## Exception Folders

Folders prefixed with `_` are **searchable but not navigable**. They contain resources useful for reference but not part of the main knowledge hierarchy.

| Folder | Purpose |
|--------|---------|
| `_resources/` | Long-form reference materials (e.g., full manual text) |
| `_research/` | Raw research, source files, works in progress |

**Navigation pattern for exception folders:** Use search tools (grep, glob) to find relevant content, then read specific files. Don't traverse hierarchically.

These folders may contain index files for discoverability, but agents aren't expected to read them as part of normal navigation.

## Link Formatting

Every link MUST provide context so an agent knows when to follow it. Links without context are useless for navigation.

### The Discoverability Principle

Just as SKILL.md frontmatter has a `description` field that enables skill discoverability, every outbound link needs a description that enables navigation discoverability. The agent reading a link should understand:
- What they'll find at the destination
- When/why they would want to go there

### Required Format for Index Links

SKILL.md and all index.md files must conclude with a **Links** section:

```markdown
## Links

- [Section 101 Eligibility](patent/section-101.md) - Alice/Mayo framework, abstract idea categories
- [Section 112 Disclosure](patent/section-112.md) - Enablement, written description, indefiniteness
```

Format: `[<informative name>](<path>) - <description for discoverability>`

The description should help an agent decide whether to follow the link given their current task.

### Inline Cross-References

For links within body text, the surrounding context provides the description:

```markdown
For the underlying legal framework, see [Section 101](../law/patent/section-101.md).
```

Cross-references are "see also" enrichment—the hierarchical structure remains primary for navigation.

## Content Style

Context is a valuable commodity. Every file an agent reads consumes context window; make that investment worthwhile.

### Information Density

Content files should be information-rich. State rules, frameworks, and guidance directly. Avoid filler, preamble, and meta-commentary about what you're about to say—just say it.

Every word must justify its place. If a sentence doesn't add information, delete it. If a paragraph restates what the heading already conveys, delete it.

### Structure

Use headings and subheadings to organize content. Prefer narrative paragraphs over bullet points—prose forces logical flow and precision. Bullets encourage fragmentation and padding.

No horizontal rules (`---`). Use headings to create visual separation.

Tables are appropriate for comparisons, quick reference, and structured data. Don't use tables for prose.

### Tone

Write with authority. State what is, not what "may be" or "could potentially be." Hedge only when genuine uncertainty exists.

Avoid AI tells: "delve," "tapestry," "multifaceted," "landscape," "Moreover" chains, "It's important to note."

## Architecture Patterns

Choose based on whether knowledge builds across domains or stays independent.

### Parallel Domains (Developer Skill)

For independent topic areas that share structure but not content:

```
developer/
├── SKILL.md
├── maintaining.md
├── python/                 # Language domain
│   ├── index.md
│   ├── project-setup.md
│   ├── style.md
│   └── async.md
├── typescript/             # Language domain (parallel structure)
│   ├── index.md
│   ├── project-setup.md
│   ├── style.md
│   └── async.md
├── publishing/             # Task domain
│   └── index.md
└── references/             # Third-party docs
    ├── claude-api/
    ├── openai-api/
    └── langchain/
```

**When to use:** Languages, product lines, geographic regions, client types—any case where domains are peers with no cross-referencing.

### Layered Domains (Lawyer Skill)

For knowledge that builds vertically—lower layers inform higher layers:

```
lawyer/
├── SKILL.md
├── maintaining.md
├── law/                    # Layer 1: DOCTRINE (foundational)
│   ├── index.md
│   ├── patent/
│   └── privacy/
├── advocacy/               # Layer 2: ARGUMENTS (references doctrine)
│   ├── index.md
│   ├── patent/
│   └── privacy/
├── writing/                # Layer 3: TASKS (references both)
│   ├── index.md
│   └── styles/
└── _resources/
    └── bluebook/
```

**When to use:** Legal analysis (rules → arguments → documents), compliance (regulations → policies → procedures), technical standards (specs → implementations → tests).

**Layer separation benefits:**
- Foundational knowledge written once, referenced by many
- Changes propagate naturally—update doctrine, advocacy stays current
- Clear separation of concerns: "what is" vs "how to apply" vs "what to produce"

## Example Index File

A properly structured index.md:

```markdown
# Patent Law

This folder covers patent law doctrine—the legal rules themselves, stated neutrally.

## Shared Concepts

Patent validity challenges arise under 35 U.S.C. §§ 101, 102, 103, and 112.
This folder focuses on § 101 (eligibility) and § 112 (disclosure) as the
primary invalidity grounds in software patent litigation.

[Any concepts that apply to ALL children go here]

## Links

- [Section 101 Eligibility](section-101.md) - Alice/Mayo two-step framework, abstract idea categories
- [Section 112 Disclosure](section-112.md) - Enablement (Wands factors), written description, indefiniteness
- [Claim Construction](claim-construction.md) - Phillips framework, intrinsic/extrinsic evidence hierarchy
```

## Conventions Summary

- Use lowercase with hyphens for folder and file names
- Every folder has an `index.md` (except exception folders)
- Exception folders start with `_`
- Links use relative paths
- Every link in index files includes a description
- SKILL.md and index.md files end with a `## Links` section
- Keep files under ~500 lines
- Prefer narrative paragraphs over bullets
- No horizontal rules—use headings instead

## Validation

Use `structure_validate.py --km` to validate knowledge base skills:

```bash
scripts/structure_validate.py --root /path/to/skill --km
```

This enables additional checks:
- Every folder has index.md
- Index files have ## Links sections with descriptions
- No horizontal rules in content
- Proper file naming (lowercase, hyphens)

See [advanced-tools.md](advanced-tools.md) for full validation options.

## Not Using Plugin Registration

Knowledge base skills should NOT be registered as plugins because:

1. **Plugin caching breaks edits** — plugins copy to cache, so edits to source don't apply
2. **No hot reload** — plugins require restart; standalone skills reload immediately
3. **Simpler paths** — agents edit `~/.claude/skills/my-skill/` directly

Keep the git repo for version control, symlink for access.

## Workflow Summary

```bash
# Initial setup
mkdir -p ~/Projects/my-knowledge-base/skills/my-skill
cd ~/Projects/my-knowledge-base && git init

# Create skill structure
# ... create SKILL.md, maintaining.md, domain folders with index.md files

# Symlink to make available
ln -s ~/Projects/my-knowledge-base/skills/my-skill ~/.claude/skills/my-skill

# Validate structure
scripts/structure_validate.py --root ~/.claude/skills/my-skill --km

# Agents edit directly, changes apply immediately
# Commit periodically to preserve history
cd ~/Projects/my-knowledge-base && git add -A && git commit -m "Update knowledge base"
```
