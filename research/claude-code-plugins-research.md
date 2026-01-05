# Claude Code Plugins Research

Research compiled for the plugin-authoring sub-skill.

## Official Documentation

- [Create plugins](https://code.claude.com/docs/en/plugins) — Main documentation
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference) — Technical specifications
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) — Marketplace creation
- [Discover Plugins](https://code.claude.com/docs/en/discover-plugins) — Installation guide

## Official Repositories

- [claude-code/plugins](https://github.com/anthropics/claude-code/tree/main/plugins) — Example plugins
- [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — Curated directory (29 plugins)

## Community Marketplaces

- [claudecodemarketplace.com](https://claudecodemarketplace.com/)
- [claude-plugins.dev](https://claude-plugins.dev/) — Registry
- [claude-code-marketplace](https://github.com/ananddtyagi/claude-code-marketplace)
- [marketplace](https://github.com/claude-market/marketplace) — Hand-curated

## Key Concepts

### Plugin vs Skill

| Concept | Plugin | Skill |
|---------|--------|-------|
| **Scope** | Claude Code only | Cross-platform |
| **Activation** | Explicit `/plugin install` | Automatic |
| **Contains** | Commands, agents, skills, hooks, MCP | Single capability |
| **Location** | `~/.claude/plugins/cache/` | `~/.claude/skills/` |

### Plugin Components

1. **Slash commands** — `commands/*.md` with frontmatter
2. **Agents** — `agents/*.md` for specialized subagents
3. **Skills** — `skills/*/SKILL.md` for capabilities
4. **Hooks** — `hooks/hooks.json` for event handlers
5. **MCP servers** — `.mcp.json` for external tools

### Directory Structure

```
plugin-name/
├── .claude-plugin/
│   └── marketplace.json     # Required
├── commands/                # Optional
├── agents/                  # Optional
├── skills/                  # Optional
├── hooks/                   # Optional
├── .mcp.json               # Optional
└── README.md
```

### marketplace.json Schema

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Author",
    "url": "https://github.com/..."
  },
  "metadata": {
    "description": "...",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./",
      "description": "...",
      "strict": false,
      "skills": ["./skills/..."]
    }
  ]
}
```

### Source Formats

Local (same repo):
```json
"source": "./"
```

GitHub:
```json
"source": {"source": "github", "repo": "owner/repo"}
```

Directory (development):
```json
"source": {"source": "directory", "path": "/path/to/plugin"}
```

### Installation Storage

| Path | Purpose |
|------|---------|
| `~/.claude/plugins/known_marketplaces.json` | Registered marketplaces |
| `~/.claude/plugins/installed_plugins.json` | Installed plugins |
| `~/.claude/plugins/cache/` | Downloaded code |
| `~/.claude/plugins/marketplaces/` | Cached repos |

### Strict Mode

- `strict: false` — marketplace.json IS the complete manifest
- `strict: true` — marketplace.json supplements separate plugin.json

## installed_plugins.json Format

```json
{
  "version": 2,
  "plugins": {
    "plugin-name@marketplace": [{
      "scope": "user",
      "installPath": "/path/to/...",
      "version": "unknown",
      "installedAt": "2025-12-31T18:30:26.863Z",
      "isLocal": true
    }]
  }
}
```

## known_marketplaces.json Format

```json
{
  "marketplace-name": {
    "source": {
      "source": "github",
      "repo": "owner/repo"
    },
    "installLocation": "/path/to/...",
    "autoUpdate": true
  }
}
```

## Requirements

- Claude Code version 1.0.33 or later
- GitHub access for remote plugins
- `gh` CLI for marketplace operations

## Third-Party Resources

- [Understanding Claude Code: Skills vs Commands vs Subagents vs Plugins](https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins)
- [Claude Skills Solve the Context Window Problem](https://tylerfolkman.substack.com/p/the-complete-guide-to-claude-skills)
