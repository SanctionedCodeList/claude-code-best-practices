# Configuration File Locations

> **Warning: Internal Implementation Details**
>
> These file locations and formats are internal to Claude Code and may change without notice in future versions. Do not build automation that depends on these formats.
>
> **Last verified:** Claude Code v2.0.76

Complete reference for Claude Code configuration paths.

## Settings

| Scope | Path |
|-------|------|
| User | `~/.claude/settings.json` |
| Project (shared) | `.claude/settings.json` |
| Project (local) | `.claude/settings.local.json` |
| Comprehensive | `~/.claude.json` |

## Plugins

| Path | Purpose |
|------|---------|
| `~/.claude/plugins/installed_plugins.json` | Installed plugin registry |
| `~/.claude/plugins/known_marketplaces.json` | Known marketplaces |
| `~/.claude/plugins/cache/` | Downloaded plugin code |
| `~/.claude/plugins/marketplaces/` | Cloned marketplace repos |

## MCP

| Scope | Path |
|-------|------|
| Project | `.mcp.json` |
| User/Local | `~/.claude.json` → `mcpServers` |

## Skills & Agents

| Type | User | Project |
|------|------|---------|
| Skills | `~/.claude/skills/` | `.claude/skills/` |
| Agents | `~/.claude/agents/` | `.claude/agents/` |

## JSON Formats

### settings.json
```json
{"enabledPlugins": {"plugin@marketplace": true}, "hooks": {...}}
```

### installed_plugins.json
```json
{"version": 2, "plugins": {"id": [{"installPath": "...", "version": "..."}]}}
```

### known_marketplaces.json
```json
{"name": {"source": {"source": "github", "repo": "owner/repo"}, "installLocation": "..."}}
```

### .mcp.json
```json
{"mcpServers": {"name": {"command": "...", "args": [...], "env": {...}}}}
```
