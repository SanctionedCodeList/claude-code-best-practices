# Skills Discovery

Discover available skills from all sources via the Python API. Read-only.

## List Skills

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import list_skills

result = list_skills()
for s in result["skills"]:
    print(f"[{s['source']}] {s['name']}: {s['description'][:50]}...")
EOF
```

## Skill Sources

| Source | Location | Scope |
|--------|----------|-------|
| User | `~/.claude/skills/` | All projects |
| Project | `.claude/skills/` | Current project |
| Plugin | Plugin install paths | Based on enabled plugins |

## Output Format

```python
{
    "name": "cc-dev",
    "description": "Claude Code development guide...",
    "source": "plugin:best-practices@scl-marketplace",  # or "user" or "project"
    "path": "/path/to/skill"
}
```

## Filter by Source

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import list_skills

result = list_skills()

# Only user skills
user_skills = [s for s in result["skills"] if s["source"] == "user"]

# Only plugin skills
plugin_skills = [s for s in result["skills"] if s["source"].startswith("plugin:")]

for s in user_skills:
    print(s["name"])
EOF
```

## Creating Skills

Skills are managed through plugins. For standalone skills, create in `~/.claude/skills/`:

```bash
mkdir -p ~/.claude/skills/my-skill
# Create SKILL.md with frontmatter
```

See [skill-creator](../../cc-dev/skill-creator/index.md) for full guidance.
