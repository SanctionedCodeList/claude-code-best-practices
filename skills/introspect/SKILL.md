---
name: introspect
description: "Introspect and manage Claude Code configuration programmatically. Use when checking installed plugins, viewing enabled/disabled status, listing available skills, managing MCP servers, or adding/removing plugin marketplaces. Provides API access to configuration that normally requires the interactive TUI."
---

# Introspect

View and manage Claude Code configuration without the interactive TUI.

## Setup

Run the install script to verify dependencies:

```bash
./install.sh
```

## Decision Tree

| What do you need? | Go to |
|-------------------|-------|
| **View or manage MCP servers** | [mcp/](./mcp/index.md) |
| **View, install, or manage plugins** | [plugins/](./plugins/index.md) |
| **Discover available skills** | [skills-view/](./skills-view/index.md) |
| **Add or manage marketplaces** | [marketplaces/](./marketplaces/index.md) |

## Usage Pattern

Import and call functions via heredoc:

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, "scripts")
from introspect import list_plugins, enable_plugin

# List all plugins
result = list_plugins()
for p in result["plugins"]:
    status = "enabled" if p["enabled"] else "disabled"
    print(f"{p['id']}: {status}")
EOF
```

## API Reference

| Function | Purpose |
|----------|---------|
| `list_plugins()` | List installed plugins with enabled status |
| `enable_plugin(id)` | Enable a plugin |
| `disable_plugin(id)` | Disable a plugin |
| `install_plugin(name, marketplace)` | Install from marketplace |
| `remove_plugin(id, delete_cache=False)` | Remove plugin |
| `update_plugin(id)` | Update to latest |
| `check_plugin_health()` | Find orphaned/broken plugins |
| `list_skills()` | Discover available skills |
| `list_marketplaces()` | List known marketplaces |
| `add_marketplace(repo)` | Add from GitHub |
| `remove_marketplace(name)` | Remove marketplace |
| `update_marketplace(name)` | Pull latest |
| `list_mcp_servers()` | List MCP servers |

## Configuration Files

See [references/config-locations.md](./references/config-locations.md) for file paths.

## Reporting Issues

If you encounter bugs with the introspect API:

```bash
gh issue create --repo SanctionedCodeList/claude-code-best-practices \
  --title "Bug: introspect [description]" \
  --body "## Problem\n[Describe]\n\n## Function\n[e.g., list_plugins]\n\n## Error\n[Output]"
```
