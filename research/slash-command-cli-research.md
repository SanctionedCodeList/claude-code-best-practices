# Claude Code Slash Command & Configuration Introspection Research

## Summary

**Core Finding:** Slash commands (`/skills`, `/plugins`, `/config`, etc.) are TUI-exclusive features with no CLI access. However, configuration can be introspected via direct file access and the `claude mcp` subcommand.

---

## 1. Non-Interactive Slash Command Access

### What's NOT Possible

- No CLI flag or command invokes slash commands non-interactively
- The `--print` / `-p` flag runs Claude programmatically but does NOT execute slash commands
- `/skills`, `/plugins`, `/agents`, `/config`, `/mcp` are interactive-only

### What IS Possible

The `claude mcp` subcommand provides non-interactive MCP server management:

```bash
claude mcp list                           # List all configured MCP servers
claude mcp get <name>                     # Get specific server details
claude mcp add <name> <command> [args]    # Add new MCP server
claude mcp remove <name>                  # Remove MCP server
claude mcp add-json <name> '<json>'       # Add from JSON config
claude mcp add-from-claude-desktop        # Import from Claude Desktop
```

Scope flags: `-s user`, `-s project`, `-s local`

---

## 2. Configuration File Locations

### Settings Files (JSON)

| Scope | Location | Purpose |
|-------|----------|---------|
| User | `~/.claude/settings.json` | Global user preferences |
| Project (shared) | `.claude/settings.json` | Team-shared project settings |
| Project (local) | `.claude/settings.local.json` | Personal project settings |
| Comprehensive | `~/.claude.json` | Plugins, MCP state, OAuth, caches |
| Enterprise (macOS) | `/Library/Application Support/ClaudeCode/` | Managed policies |
| Enterprise (Linux) | `/etc/claude-code/` | Managed policies |

### MCP Configuration

| Scope | Location |
|-------|----------|
| Project | `.mcp.json` |
| User/Local | `~/.claude.json` → `mcpServers` key |

### Plugin & Skill Locations

| Type | Location |
|------|----------|
| Plugins | `~/.claude/plugins/` |
| Plugin cache | `~/.claude/plugins/cache/` |
| User skills | `~/.claude/skills/` |
| Project skills | `.claude/skills/` |
| User agents | `~/.claude/agents/` |
| Project agents | `.claude/agents/` |

---

## 3. Configuration Introspection Workarounds

### List Enabled Plugins

```bash
jq '.enabledPlugins // []' ~/.claude/settings.json
```

### List MCP Servers

```bash
claude mcp list
# or directly:
jq '.mcpServers // {}' ~/.claude.json
```

### Discover Skills

```bash
# User skills
find ~/.claude/skills -name "SKILL.md" 2>/dev/null

# Project skills
find .claude/skills -name "SKILL.md" 2>/dev/null
```

### Discover Agents

```bash
# User agents
ls ~/.claude/agents/*.md 2>/dev/null

# Project agents
ls .claude/agents/*.md 2>/dev/null
```

### Inspect Plugin Metadata

```bash
# List installed plugins
ls ~/.claude/plugins/

# Read plugin manifest
cat ~/.claude/plugins/<plugin-name>/.claude-plugin/plugin.json
```

### Dump Full Configuration

```bash
# Settings
cat ~/.claude/settings.json | jq .

# Comprehensive config (contains sensitive data like OAuth tokens)
cat ~/.claude.json | jq 'del(.oauthTokensByHost)'
```

---

## 4. Gaps & Missing Features

### No CLI Support For

1. **`claude plugins list`** - List installed/enabled plugins
2. **`claude skills list`** - List available skills
3. **`claude agents list`** - List available agents
4. **`claude config dump`** - Export full configuration
5. **`claude config get <key>`** - Query specific config values
6. **Slash command execution** - Any `/command` outside TUI

### Information Not Easily Accessible

- Which skills a plugin provides (requires parsing SKILL.md files)
- Runtime-computed configuration (merged settings, active hooks)
- Plugin tool availability (what tools each plugin injects)

---

## 5. Programmatic Access Options

### Agent SDK (Recommended)

Python and TypeScript SDKs provide full programmatic control:

```python
# Python example
from claude_code_sdk import query

result = await query(
    prompt="What plugins are available?",
    options={"allowedTools": ["Read", "Glob"]}
)
```

### Non-Interactive Claude Execution

```bash
# Run with prompt, get output
claude -p "List files in current directory"

# With specific options
claude --model opus -p "Analyze this code"
```

Note: This runs Claude but does NOT provide access to slash commands.

---

## 6. Recommendations for Self-Introspection

### For Claude to Introspect Its Own Configuration

Since slash commands aren't accessible programmatically, create tools/scripts that:

1. **Read configuration files directly:**
   ```bash
   cat ~/.claude/settings.json
   cat ~/.claude.json | jq 'del(.oauthTokensByHost)'
   ```

2. **Use `claude mcp list` for MCP servers**

3. **Scan skill/plugin directories:**
   ```bash
   find ~/.claude -name "SKILL.md" -o -name "plugin.json"
   ```

4. **Parse plugin manifests for capabilities:**
   ```bash
   for plugin in ~/.claude/plugins/*/; do
     echo "=== $(basename $plugin) ==="
     cat "$plugin/.claude-plugin/plugin.json" 2>/dev/null | jq -r '.name, .description'
   done
   ```

### Potential Enhancement: Custom Introspection Skill

Create a skill at `~/.claude/skills/introspect/SKILL.md` that:
- Reads and summarizes configuration files
- Lists available plugins, skills, agents
- Shows MCP server status
- Formats output for Claude consumption

---

## 7. Feature Requests

If CLI introspection is needed, these would be valuable additions:

1. `claude plugins list [--json]` - List plugins with status
2. `claude skills list [--json]` - List available skills
3. `claude config dump [--scope <scope>]` - Export configuration
4. `claude config get <key>` - Query specific values
5. `claude introspect` - Full system status dump

Consider submitting feature requests to: https://github.com/anthropics/claude-code/issues
