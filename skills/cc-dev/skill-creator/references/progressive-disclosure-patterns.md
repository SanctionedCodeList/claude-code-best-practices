# Progressive Disclosure Patterns

This reference covers patterns for organizing skill content to minimize context usage while maintaining discoverability.

## Table of Contents

- [Design Patterns](#design-patterns)
- [Multi-file Skill Index](#multi-file-skill-index)
- [Guidelines](#guidelines)

## Design Patterns

### Pattern 1: High-level Guide with References

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

Claude loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

### Pattern 2: Domain-specific Organization

For skills with multiple domains, organize content by domain to avoid loading irrelevant context:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, Claude only reads sales.md.

Similarly, for skills supporting multiple frameworks or variants, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When the user chooses AWS, Claude only reads aws.md.

### Pattern 3: Conditional Details

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads REDLINING.md or OOXML.md only when the user needs those features.

## Multi-file Skill Index

For skills with branching workflows, specializations, or conditional content, end SKILL.md with an index of supplementary files. This gives agents a clear map of available documentation they can load on-demand.

**Format:** Place the index at the end of SKILL.md with relative links and brief descriptions:

```markdown
## Additional References

- [aws.md](references/aws.md) - AWS-specific deployment patterns and IAM configuration
- [gcp.md](references/gcp.md) - GCP-specific deployment patterns and service accounts
- [azure.md](references/azure.md) - Azure-specific deployment patterns and RBAC setup
- [troubleshooting.md](references/troubleshooting.md) - Common errors and resolution steps
```

### Recursive Structure

This pattern applies recursively. SKILL.md indexes top-level sections, each section indexes its subsections, and so on:

```
complex-skill/
├── SKILL.md                    # Core workflow + index of top-level sections
└── references/
    ├── deployment.md           # Deployment overview + index of providers
    │   └── providers/
    │       ├── aws.md          # AWS details + index of services
    │       │   └── services/
    │       │       ├── lambda.md
    │       │       └── ecs.md
    │       └── gcp.md
    └── monitoring.md           # Monitoring overview + index of tools
        └── tools/
            ├── datadog.md
            └── cloudwatch.md
```

Each file contains its own index at the end, linking to the next level down. This allows agents to navigate hierarchically—reading only the path from root to the specific information needed, without loading irrelevant branches.

This allows an agent to:
1. Read SKILL.md to understand the core workflow
2. Identify which specialization or branch applies to the current task
3. Navigate down the hierarchy, loading only relevant files at each level
4. Arrive at the specific information needed with minimal context pollution

## Guidelines

- **Structure longer reference files** - For files longer than 100 lines, include a table of contents at the top so Claude can see the full scope when previewing.
- **Avoid duplication** - Information should live in either SKILL.md or references files, not both.
- **Keep SKILL.md lean** - Move detailed information to references files; keep only essential procedural instructions and workflow guidance in SKILL.md.
