---
name: plugin-authoring
description: "Guide for creating Claude Code plugins and marketplaces. Covers plugin structure, marketplace.json, distribution, and the plugin vs skill distinction."
---

# Plugin Authoring Guide

Create and distribute Claude Code plugins and marketplaces.

## Plugin vs Skill

| Concept | Plugin | Skill |
|---------|--------|-------|
| **Scope** | Claude Code only | Cross-platform (web, CLI, IDE) |
| **Activation** | Explicit install via `/plugin install` | Automatic based on task context |
| **Contains** | Commands, agents, skills, hooks, MCP servers | Single capability (SKILL.md + resources) |
| **Location** | `~/.claude/plugins/cache/` | `~/.claude/skills/` or within plugins |

**Key insight**: A plugin is a distribution package. Skills are capabilities that can live inside plugins or standalone.

## Plugin Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── marketplace.json     # Plugin manifest (required)
├── commands/                # Slash commands (optional)
│   └── my-command.md
├── agents/                  # Specialized agents (optional)
│   └── my-agent.md
├── skills/                  # Agent skills (optional)
│   └── my-skill/
│       └── SKILL.md
├── hooks/                   # Event handlers (optional)
│   └── hooks.json
├── .mcp.json               # MCP servers (optional)
├── install.sh              # Setup script (optional)
└── README.md
```

**Important**: All components live at plugin root, NOT inside `.claude-plugin/`. Only the manifest goes in `.claude-plugin/`.

## marketplace.json

The plugin manifest. Located at `.claude-plugin/marketplace.json`.

```json
{
  "name": "my-plugin-marketplace",
  "owner": {
    "name": "Your Name",
    "url": "https://github.com/you/my-plugin"
  },
  "metadata": {
    "description": "What this plugin does",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./",
      "description": "Plugin description for discovery",
      "strict": false,
      "skills": [
        "./skills/my-skill"
      ]
    }
  ]
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Marketplace identifier |
| `plugins` | Array of plugin definitions |
| `plugins[].name` | Plugin identifier (used in install command) |
| `plugins[].source` | Path to plugin root (usually `"./"`) |

### Optional Fields

| Field | Description |
|-------|-------------|
| `owner.name` | Author name |
| `owner.url` | Repository URL |
| `metadata.description` | Marketplace description |
| `metadata.version` | Semver version |
| `plugins[].description` | Plugin description |
| `plugins[].strict` | If true, requires separate plugin.json |
| `plugins[].skills` | Array of skill paths |
| `plugins[].keywords` | Search keywords |

## Single Plugin vs Marketplace

### Single Plugin Repository
One plugin, one repo. The marketplace.json defines that single plugin:

```json
{
  "name": "dev-browser-marketplace",
  "plugins": [{
    "name": "dev-browser",
    "source": "./",
    "skills": ["./skills/dev-browser"]
  }]
}
```

Install: `/plugin install owner/repo`

### Multi-Plugin Marketplace
One repo distributing multiple plugins from different sources:

```json
{
  "name": "scl-marketplace",
  "plugins": [
    {
      "name": "law-tools",
      "source": {"source": "github", "repo": "owner/law-tools"},
      "description": "Legal research toolkit"
    },
    {
      "name": "writing",
      "source": {"source": "github", "repo": "owner/writing"},
      "description": "Writing guidance"
    }
  ]
}
```

Add marketplace: `/plugin marketplace add owner/marketplace-repo`
Install plugin: `/plugin install law-tools@scl-marketplace`

## Installation Workflow

### For Users

```bash
# Add a marketplace (once)
/plugin marketplace add SanctionedCodeList/SCL_marketplace

# Install a plugin from that marketplace
/plugin install best-practices@scl-marketplace

# Or install directly from GitHub
/plugin install owner/repo
```

### Storage Locations

| Path | Purpose |
|------|---------|
| `~/.claude/plugins/known_marketplaces.json` | Registered marketplaces |
| `~/.claude/plugins/installed_plugins.json` | Installed plugin registry |
| `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` | Downloaded plugin code |
| `~/.claude/plugins/marketplaces/` | Cached marketplace repos |

## Strict Mode

The `strict` field controls manifest behavior:

| Value | Behavior |
|-------|----------|
| `false` (default) | marketplace.json entry IS the complete manifest |
| `true` | marketplace.json supplements a separate plugin.json |

Use `strict: false` for simple plugins. Use `strict: true` when you need a separate plugin.json with additional metadata.

## Plugin Components

### Slash Commands
Markdown files in `commands/` with frontmatter:

```markdown
---
name: my-command
description: "What this command does"
---

# My Command

Instructions for the command...
```

Invoked as `/my-command` in Claude Code.

### Agents
Markdown files in `agents/` defining specialized subagents:

```markdown
---
name: my-agent
description: "Specialized agent for X"
---

# My Agent

You are a specialized agent for...
```

### Skills
Directories in `skills/` with SKILL.md files. See the [skill-creator](../skill-creator/SKILL.md) sub-skill.

### Hooks
JSON configuration in `hooks/` for event handlers:

```json
{
  "hooks": [
    {
      "event": "on_message",
      "command": "./scripts/process.sh"
    }
  ]
}
```

### MCP Servers
Configure in `.mcp.json` at plugin root:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["./mcp/server.js"]
    }
  }
}
```

## Best Practices

### Naming
- Use lowercase with hyphens: `my-plugin`, not `MyPlugin`
- Plugin name should match the primary capability
- Marketplace name typically ends with `-marketplace`

### Structure
- Keep plugin focused on one domain
- Bundle related skills together
- Include install.sh for dependencies
- Add README.md for documentation

### Distribution
- Host on GitHub for easy installation
- Use semantic versioning
- Register with community marketplaces for discovery

## Example: Minimal Plugin

```
minimal-plugin/
├── .claude-plugin/
│   └── marketplace.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

**marketplace.json:**
```json
{
  "name": "minimal-plugin",
  "plugins": [{
    "name": "minimal-plugin",
    "source": "./",
    "description": "A minimal example plugin",
    "skills": ["./skills/my-skill"]
  }]
}
```

## References

- [Example marketplace.json](./references/example-marketplace-json.md)
- [Official Plugins](https://github.com/anthropics/claude-plugins-official) — Anthropic's curated list
- [Claude Code Docs](https://code.claude.com/docs/en/plugins) — Official documentation
