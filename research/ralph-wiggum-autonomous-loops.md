# Ralph Wiggum - Autonomous Loops for Claude Code

Research on the Ralph Wiggum technique for running Claude Code autonomously.

## What It Is

Ralph Wiggum is an autonomous loop technique that repeatedly feeds Claude Code the same prompt until a task is completed. Named after the Simpsons character who is "perpetually confused, always making mistakes, but never stops."

**Core philosophy:** "It's better to fail predictably than succeed unpredictably." — Geoffrey Huntley (creator)

At its core, Ralph Wiggum:
- Uses Claude Code's Stop hook to intercept session endings
- Re-injects the original prompt with exit code 2
- Lets Claude see previous work via git history and modified files
- Continues until a completion condition is met

## Sources

### Official
- [GitHub - anthropics/claude-code/plugins/ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)
- [claude-plugins-official/ralph-wiggum](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum)

### Community
- [Ralph Wiggum - Awesome Claude](https://awesomeclaude.ai/ralph-wiggum)
- [Ralph Wiggum: Autonomous Loops - Paddo.dev](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/)
- [The Ralph Wiggum Approach - DEV Community](https://dev.to/sivarampg/the-ralph-wiggum-approach-running-ai-coding-agents-for-hours-not-minutes-57c1)
- [Ralph Wiggum Plugin - APIdog](https://apidog.com/blog/ralph-wiggum-plugin-in-claude-code/)
- [Medium - Joe Njenga](https://medium.com/@joe.njenga/ralph-wiggum-claude-code-new-way-to-run-autonomously-for-hours-without-drama-095f47fbd467)
- [GitHub - frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code)

## Installation

```bash
/plugin install ralph-wiggum@claude-plugins-official
```

## Usage

```bash
/ralph-loop "Your task description" --max-iterations 50 --completion-promise "Task complete"
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `--max-iterations` | Safety limit on loop cycles |
| `--completion-promise` | String Claude outputs to signal task completion |

## When to Use

### Good Use Cases

- **Large migrations** — Test frameworks, dependencies, APIs
- **Repetitive refactoring** — Changes across many files
- **Iterative improvement** — Tasks where "keep trying" works better than one-shot
- **Complex multi-step tasks** — Where context continuity matters

### Considerations

| Factor | Impact |
|--------|--------|
| **Cost** | 50-iteration loop on large codebase: $50-100+ in API credits |
| **Subscription limits** | Burns through usage allocation faster |
| **Prompt quality** | Success depends on clear, specific prompts |

## How It Works

1. User starts loop with a task prompt
2. Claude Code attempts the task
3. When Claude tries to exit, the Stop hook intercepts
4. Exit code 2 blocks the stop and re-injects the prompt
5. Claude sees its previous work (git diff, modified files)
6. Loop continues until:
   - Max iterations reached, OR
   - Claude outputs the completion promise string

## Technical Implementation

The technique uses Claude Code's hook system:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "command": "exit 2"
    }]
  }
}
```

Exit code 2 signals "don't stop, continue with the same prompt."

## Related Concepts

- **Hooks** — Claude Code event handlers that enable this pattern
- **Git-based context** — Claude uses `git diff` to see its previous changes
- **Completion promises** — Specific strings that signal task completion
