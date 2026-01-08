# Debugging Claude Code

Techniques for debugging Claude Code behavior, configuration, and plugins.

## Debugging with dev-terminal

The most effective way to debug Claude Code from within Claude Code is using the **dev-terminal** skill. This allows one Claude instance to interact with another Claude Code instance through its TUI.

### Why dev-terminal?

- **Full access**: Interact with all Claude Code features, not just configuration APIs
- **Live observation**: Watch how Claude Code responds to inputs in real time
- **No fragile APIs**: Doesn't depend on internal JSON formats that may change

### Example workflow

1. Start a new Claude Code instance in a terminal session via dev-terminal
2. Send test prompts and observe behavior
3. Check configuration, run commands, or reproduce issues
4. Compare behavior across different configurations

```
User: Use dev-terminal to start a Claude Code instance and test how it handles [scenario]
```

## Configuration Reference

For understanding where Claude Code stores configuration files, see [config-locations.md](./references/config-locations.md).

**Note:** Configuration file formats are internal implementation details and may change between versions.

## Common Debugging Tasks

| Task | Approach |
|------|----------|
| Plugin not loading | Check `~/.claude/settings.json` for `enabledPlugins`, verify plugin path exists |
| Hook not firing | Add logging to hook script, check event name matches |
| Skill not matching | Review skill description and trigger phrases in SKILL.md |
| MCP server failing | Run `claude mcp list`, check server command manually |
| Session history issues | Use sessions sub-skill to search/retrieve past conversations |

## Logs and State

Claude Code doesn't maintain extensive logs by default. For debugging:

1. **Add logging hooks** - Use PostToolUse hooks to log tool calls (see context-injection)
2. **Session history** - Use the sessions sub-skill to review past conversations
3. **Configuration inspection** - Check the paths in config-locations.md
