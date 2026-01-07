# Plugin Issue Reporting

How to enable agents to submit issues to the correct plugin repository automatically.

## The Problem

When Claude Code encounters a bug in a plugin/skill, it needs to submit an issue to the correct GitHub repository. Hardcoding repository URLs doesn't work because:

1. Plugins can be forked or installed from different sources
2. The same skill may exist in multiple repositories
3. Users may have local modifications

## The Solution

Use the plugin's git remote to determine the correct repository dynamically.

```bash
# SKILL_DIR is provided at the top of skill output as "Base directory for this skill:"
SKILL_DIR="<base directory from skill header>"
PLUGIN_ROOT=$(cd "$SKILL_DIR" && while [ ! -d .git ] && [ "$PWD" != "/" ]; do cd ..; done && pwd)
REPO=$(git -C "$PLUGIN_ROOT" remote get-url origin | sed -E 's#.*github\.com[:/]([^/]+/[^/.]+)(\.git)?$#\1#')

# Submit issue
gh issue create --repo "$REPO" --title "Bug: [description]" --body "## Problem
[Describe the issue]

## Steps to reproduce
[Minimal example]"

# Check existing issues first
gh issue list --repo "$REPO"
```

## How It Works

### Step 1: Get SKILL_DIR

When a skill runs, Claude Code outputs a header:

```
Base directory for this skill: /path/to/plugin/skills/my-skill
```

The agent extracts this path as `SKILL_DIR`.

### Step 2: Find PLUGIN_ROOT

Walk up the directory tree until finding a `.git` directory:

```bash
PLUGIN_ROOT=$(cd "$SKILL_DIR" && while [ ! -d .git ] && [ "$PWD" != "/" ]; do cd ..; done && pwd)
```

This handles nested skill structures like:
```
plugin-repo/           <- PLUGIN_ROOT (has .git)
├── skills/
│   └── my-skill/      <- SKILL_DIR
│       └── SKILL.md
└── .git/
```

### Step 3: Extract Repository

Parse the git remote URL to get `owner/repo`:

```bash
REPO=$(git -C "$PLUGIN_ROOT" remote get-url origin | sed -E 's#.*github\.com[:/]([^/]+/[^/.]+)(\.git)?$#\1#')
```

**Handles both URL formats:**

| Format | Example | Extracted |
|--------|---------|-----------|
| SSH | `git@github.com:owner/repo.git` | `owner/repo` |
| HTTPS | `https://github.com/owner/repo.git` | `owner/repo` |
| HTTPS (no .git) | `https://github.com/owner/repo` | `owner/repo` |

**Regex breakdown:**
- `.*github\.com` — Match anything up to github.com
- `[:/]` — Match `:` (SSH) or `/` (HTTPS) after github.com
- `([^/]+/[^/.]+)` — Capture two path segments: owner and repo name
- `(\.git)?$` — Optionally match `.git` suffix
- `\1` — Return the captured owner/repo

### Step 4: Submit Issue

Use GitHub CLI to create the issue:

```bash
gh issue create --repo "$REPO" --title "Bug: [description]" --body "..."
```

## Integration

Add this to your `~/.claude/CLAUDE.md`:

```markdown
## Plugin Feedback & Issues

When you encounter bugs or issues with a plugin/skill, submit issues to the correct repository by checking the plugin's git remote:

[code block from above]

This ensures issues go to the correct repository based on where the plugin was installed from, not a hardcoded default.
```

## Benefits

| Benefit | Description |
|---------|-------------|
| **Dynamic routing** | Issues go to the actual source repo, not a hardcoded default |
| **Fork-aware** | Works correctly with forked plugins |
| **Portable** | Handles SSH and HTTPS remote URLs |
| **Self-documenting** | Uses the same git remote the user cloned from |

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth login`)
- Plugin installed via git (has `.git` directory)
