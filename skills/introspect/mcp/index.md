# MCP Server Management

MCP servers are managed via the `claude mcp` CLI (the only area where CLI is appropriate, as it's an external tool).

## List Servers

```bash
python3 << 'EOF'
import sys; sys.path.insert(0, "scripts")
from introspect import list_mcp_servers

result = list_mcp_servers()
if result["success"]:
    print(result["output"])
else:
    print(f"Error: {result['error']}")
EOF
```

Or directly via CLI:

```bash
claude mcp list
```

## Add Server

Use the `claude mcp` CLI directly (not wrapped by introspect API):

```bash
# Basic
claude mcp add <name> <command> [args...]

# With scope
claude mcp add <name> <command> [args...] -s <scope>

# From JSON
claude mcp add-json <name> '{"command": "...", "args": [...]}'
```

Scopes: `user` (default), `project`, `local`

## Examples

```bash
# Simple server
claude mcp add my-server node /path/to/server.js

# With arguments
claude mcp add postgres-mcp npx @postgres/mcp --connection-string "..."

# Project scope
claude mcp add project-server ./run.sh -s project

# Import from Claude Desktop
claude mcp add-from-claude-desktop
```

## Remove Server

```bash
claude mcp remove <name>
claude mcp remove <name> -s project  # specific scope
```

## Configuration Files

See [config-locations.md](../references/config-locations.md) for MCP file paths.
