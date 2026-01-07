# Hook Patterns

Common patterns for using hooks to inject context.

## SessionStart: Project Context

Inject project state when a session begins.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "./scripts/session-context.sh"
      }
    ]
  }
}
```

```bash
#!/bin/bash
# session-context.sh

echo "## Git Status"
git status --short

echo ""
echo "## Recent Commits"
git log --oneline -5

echo ""
echo "## Current Branch"
git branch --show-current

echo ""
echo "## Open TODOs"
grep -r "TODO:" --include="*.ts" --include="*.py" -l 2>/dev/null | head -5
```

---

## SessionStart: Sprint Context

Load current sprint priorities.

```bash
#!/bin/bash
# sprint-context.sh

echo "## Current Sprint: Sprint 23"
echo "**Focus:** API v2 migration"
echo ""
echo "### Priorities"
echo "1. Complete auth endpoint migration"
echo "2. Update API documentation"
echo "3. Performance testing"

if [ -f "./SPRINT.md" ]; then
    echo ""
    cat ./SPRINT.md
fi
```

---

## UserPromptSubmit: Coding Standards

Inject standards before every prompt.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "cat ./STANDARDS.md"
          }
        ]
      }
    ]
  }
}
```

**STANDARDS.md:**
```markdown
## Coding Standards

- Use TypeScript strict mode
- All functions require JSDoc comments
- No `any` types without justification
- Tests required for new functionality
```

---

## UserPromptSubmit: Conditional Injection

Only inject for specific file types.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "\\.(tsx?|jsx?)$",
        "hooks": [
          {
            "type": "command",
            "command": "cat ./react-standards.md"
          }
        ]
      },
      {
        "matcher": "\\.py$",
        "hooks": [
          {
            "type": "command",
            "command": "cat ./python-standards.md"
          }
        ]
      }
    ]
  }
}
```

---

## PreToolUse: Security Check

Validate before dangerous operations.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/validate-command.sh"
          }
        ]
      }
    ]
  }
}
```

```bash
#!/bin/bash
# validate-command.sh

# Check for dangerous patterns
if echo "$CLAUDE_TOOL_INPUT" | grep -qE "(rm -rf|dd if=|mkfs|:(){:|format)"; then
    echo '{"error": "Potentially dangerous command detected"}'
    exit 1
fi

echo '{"continue": true}'
```

---

## PostToolUse: Logging

Log tool usage for audit.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/log-tool.sh"
          }
        ]
      }
    ]
  }
}
```

```bash
#!/bin/bash
# log-tool.sh

echo "$(date -Iseconds) | $CLAUDE_TOOL_NAME | $CLAUDE_SESSION_ID" >> ~/.claude/tool-audit.log
echo '{"continue": true}'
```

---

## Environment Variables

Available in hook scripts:

| Variable | Description |
|----------|-------------|
| `CLAUDE_PLUGIN_ROOT` | Plugin installation directory |
| `CLAUDE_SESSION_ID` | Current session identifier |
| `CLAUDE_TOOL_NAME` | Tool being invoked (PreToolUse/PostToolUse) |
| `CLAUDE_TOOL_INPUT` | Tool input JSON (PreToolUse) |
| `CLAUDE_TOOL_OUTPUT` | Tool output (PostToolUse) |

---

## Structured Output

Return JSON for advanced control:

```json
{
  "additionalContext": "Extra context to inject",
  "continue": true,
  "error": "Error message (stops execution)"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `additionalContext` | string | Text injected into conversation |
| `continue` | boolean | Whether to proceed with the action |
| `error` | string | Error message (blocks action) |

---

## Token Budget Tips

1. **Be concise** — Every token in hook output consumes context
2. **Filter output** — Use `head`, `grep`, `--limit` flags
3. **Cache expensive operations** — Don't run slow commands on every prompt
4. **Use matchers** — Only inject when relevant

```bash
# Bad: Full git log
git log

# Good: Limited, formatted output
git log --oneline -5
```
