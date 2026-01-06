# Advanced Skill Development Tools

This reference covers optional tooling for complex skill development: template composition and structure validation.

## Table of Contents

- [Template Build System](#template-build-system)
- [Structure Validation](#structure-validation)

## Template Build System

For skills with composable content (shared fragments, reusable sections), use Jinja2 templates:

```bash
scripts/build.py --root /path/to/skill           # Build all templates
scripts/build.py --root /path/to/skill --clean   # Clean rebuild
scripts/build.py --root /path/to/skill --check   # Check if rebuild needed (for CI)
```

**Convention:**
- Templates use `.md.j2` extension adjacent to their outputs
- `foo.md.j2` generates `foo.md` with an AUTO-GENERATED header
- Use `{% include 'path/to/fragment.md' %}` to compose content
- Files without `.j2` are editable directly

**Example structure:**
```
my-skill/
├── SKILL.md
├── styles/
│   └── formal.md           # Reusable style (editable)
├── structures/
│   ├── report.md.j2        # Template (edit this)
│   └── report.md           # Generated (don't edit)
└── _includes/
    └── citations.md        # Internal fragment
```

**Template example:**
```jinja
---
name: "report"
description: "Formal report structure"
---

# Report

{% include 'styles/formal.md' %}
{% include '_includes/citations.md' %}

## Structure
...
```

## Structure Validation

Validate skill structure for navigability and consistency:

```bash
scripts/structure_validate.py --root /path/to/skill              # Run all checks
scripts/structure_validate.py --root /path/to/skill --focus sub  # Check subdirectory
scripts/structure_validate.py --root /path/to/skill --graph      # Output mermaid diagram
scripts/structure_validate.py --root /path/to/skill -v           # Verbose with stats
```

**Checks performed:**
1. **Broken links** - Links to non-existent files
2. **Orphan files** - `.md` files with no incoming links
3. **Depth limits** - Files too deep in the hierarchy (default: 3 levels)
4. **Generated headers** - Files from `.j2` templates have AUTO-GENERATED headers
5. **File length** - Files exceeding recommended limits (warning: 300, error: 500 lines)

**Configuration via `.validate.json`:**
```json
{
  "max_depth": 3,
  "max_lines_warning": 300,
  "max_lines_error": 500,
  "excluded_patterns": ["_includes/", "assets/", "scripts/"],
  "known_issues": {
    "broken_links": ["reference/external/"],
    "long_files": ["reference/tables/"]
  }
}
```

**Best practices:**
- Keep files under 300 lines for readability and context efficiency
- Ensure all content files are reachable from SKILL.md
- Use `--graph` to visualize skill structure as a mermaid diagram
