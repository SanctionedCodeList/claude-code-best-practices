# Marketplace Management

Manage plugin marketplaces via the Python API.

## List Marketplaces

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import list_marketplaces

result = list_marketplaces()
for m in result["marketplaces"]:
    print(f"{m['name']}: {m['repo']}")
EOF
```

## Add Marketplace

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import add_marketplace

# Add from GitHub (owner/repo format)
result = add_marketplace("anthropics/claude-plugins-official")
if result["success"]:
    print(f"Added: {result['name']}")
else:
    print(f"Error: {result['error']}")
EOF
```

## Remove Marketplace

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import remove_marketplace

result = remove_marketplace("scl-marketplace")
print(result["message"])
EOF
```

## Update Marketplace

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import update_marketplace

result = update_marketplace("claude-plugins-official")
print(result["message"])
EOF
```

## Workflow: Install Plugin from New Marketplace

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import add_marketplace, install_plugin

# 1. Add the marketplace
add_marketplace("owner/marketplace-repo")

# 2. Install a plugin from it
install_plugin("plugin-name", "marketplace-name")
EOF
```

## Configuration Files

See [config-locations.md](../references/config-locations.md) for marketplace file paths.
