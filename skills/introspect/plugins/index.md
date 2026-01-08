# Plugin Management

Manage Claude Code plugins programmatically via the Python API.

## List Plugins

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import list_plugins

result = list_plugins()
for p in result["plugins"]:
    status = "enabled" if p["enabled"] else "disabled"
    print(f"{p['id']}: {status} (v{p['version']})")
EOF
```

## Enable/Disable

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import enable_plugin, disable_plugin

# Enable
result = enable_plugin("dev-browser@scl-marketplace")
print(result["message"])

# Disable
result = disable_plugin("writing@scl-marketplace")
print(result["message"])
EOF
```

## Install Plugin

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import install_plugin

result = install_plugin("pyright-lsp", "claude-plugins-official")
if result["success"]:
    print(f"Installed: {result['installPath']}")
else:
    print(f"Error: {result['error']}")
EOF
```

## Remove Plugin

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import remove_plugin

# Remove from registry only
result = remove_plugin("writing@scl-marketplace")

# Remove and delete cached files
result = remove_plugin("writing@scl-marketplace", delete_cache=True)
EOF
```

## Update Plugin

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import update_plugin

result = update_plugin("dev-browser@scl-marketplace")
print(result["message"])
EOF
```

## Health Check

Find orphaned or broken plugin installations:

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import check_plugin_health, remove_plugin, disable_plugin

result = check_plugin_health()
if result["healthy"]:
    print("All plugins healthy")
else:
    for issue in result["issues"]:
        print(f"✘ {issue['plugin_id']}: {issue['message']}")
        print(f"  → {issue['suggestion']}")
EOF
```

Issue types detected:
- `missing_path` - Install directory doesn't exist
- `missing_marketplace` - Marketplace not in known_marketplaces.json
- `plugin_not_in_marketplace` - Plugin removed from marketplace
- `enabled_but_not_installed` - Enabled in settings but not installed

## Plugin ID Format

`<plugin-name>@<marketplace-name>` (e.g., `dev-browser@scl-marketplace`)

## Configuration Files

See [config-locations.md](../references/config-locations.md) for plugin file paths.
