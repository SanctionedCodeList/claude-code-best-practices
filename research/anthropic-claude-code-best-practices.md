# Anthropic's Official Claude Code Best Practices

Compiled from [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) on the Anthropic Engineering blog.

## Setup & Configuration

### CLAUDE.md Files

Special files that Claude automatically incorporates into conversations.

**What to include:**
- Bash commands for building, testing, linting
- Code style guidelines
- Testing instructions
- Repository etiquette
- Environment setup

**Where to place:**
- Repo root (most common)
- Parent directories
- Home folder (`~/.claude/CLAUDE.md`) for global settings
- Child directories for specific contexts

**Tips:**
- Use `#` key to have Claude automatically add documentation
- Add emphasis keywords like "IMPORTANT" for critical instructions
- Iterate on content like you would any prompt

### Permission Management

Four methods to customize allowed tools:
1. Select "Always allow" when prompted
2. Use `/permissions` command
3. Edit `.claude/settings.json` manually
4. Use `--allowedTools` CLI flag for session-specific

### Custom Slash Commands

Store prompt templates in `.claude/commands/` as Markdown files.

```markdown
# .claude/commands/fix-lint.md
Fix all linting errors in $ARGUMENTS
```

Use `$ARGUMENTS` keyword to pass parameters.

Personal commands go in `~/.claude/commands/`.

## Effective Workflows

### Explore-Plan-Code-Commit

1. **Explore** — Have Claude read files without coding first
2. **Plan** — Create documentation of the plan before implementation
3. **Code** — Implement with clear constraints
4. **Commit** — Let Claude handle git operations

### Extended Thinking Triggers

Use these phrases to increase Claude's computation time:

| Phrase | Effect |
|--------|--------|
| "think" | Basic extended thinking |
| "think hard" | More computation |
| "think harder" | Even more |
| "ultrathink" | Maximum computation |

Use for complex reasoning, debugging, or architectural decisions.

### Test-Driven Development

1. Write tests first based on input/output pairs
2. Confirm tests fail before implementing
3. Have Claude commit tests separately
4. Implement code iteratively
5. Use independent subagents to verify implementations don't overfit

### Visual Iteration

1. Provide design mocks or screenshots (paste, drag-drop, or file path)
2. Have Claude implement the design
3. Take screenshots of the result
4. Iterate 2-3 times for polish

### Safe YOLO Mode

```bash
claude --dangerously-skip-permissions
```

**Only use in:**
- Containers without internet access
- Isolated environments
- When you accept the security risks

Bypasses permission checks for faster iteration.

## Tool Integration

### Bash Tools

Claude inherits your shell environment.

**Document in CLAUDE.md:**
- Tool names with usage examples
- Instruct Claude to run `--help` for documentation
- Frequently-used tools and their purposes

### MCP Servers

Configure in:
- Project settings
- Global config
- Checked-in `.mcp.json` files

Use `--mcp-debug` flag when troubleshooting.

### GitHub CLI

Install `gh` for Claude to:
- Manage issues
- Create pull requests
- Handle comments
- Read repository metadata

## Context Management

### Specificity Matters

> "Provide clear, detailed instructions. Specify edge cases, patterns to follow, and constraints upfront rather than relying on inference."

Bad: "Fix the bug"
Good: "Fix the null pointer exception in `parseConfig()` by adding validation for empty input arrays"

### Visual Resources

Share screenshots, diagrams, and images through:
- Clipboard paste
- Drag-drop
- File paths

Claude excels with visual reference points.

### File References

Use tab-completion to reference files and folders accurately.

### URL Fetching

- Paste URLs for Claude to fetch and read
- Use `/permissions` to allowlist domains
- Avoid repeated permission prompts

### Course Correction

- **Plan before coding** — Reduce wasted effort
- **Press Escape** — Interrupt phases mid-execution
- **Double-tap Escape** — Edit previous prompts
- **Ask Claude to undo** — Revert changes
- **Use `/clear` frequently** — Reset context between tasks

## Advanced Patterns

### Checklists for Complex Tasks

Use Markdown files or GitHub issues as working scratchpads:
- Multi-step migrations
- Lint fix campaigns
- Build script modifications

Have Claude work through items systematically.

### Data Input Methods

1. Copy-paste directly
2. Pipe into Claude: `cat foo.txt | claude`
3. Tell Claude to pull data via bash/MCP/slash commands
4. Have Claude read files and fetch URLs

### Headless Mode Automation

```bash
claude -p "Your prompt here"
```

Use cases:
- CI pipelines
- Pre-commit hooks
- Infrastructure scripts
- Large-scale migrations (fan out across repos)

Output options:
- `--output-format stream-json` for structured output

### Multi-Claude Workflows

Run multiple instances in parallel:

**Patterns:**
- One writes code, another reviews
- Separate git checkouts per task
- Lightweight git worktrees for isolation

**Coordination:**
- Shared scratchpads or working files
- Consistent naming conventions
- One terminal tab per worktree

```bash
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
```

### Subagents

Use subagents early to:
- Verify details
- Preserve main context
- Parallelize research

Subagents run in isolated context windows and return only relevant information.

## Search Strategy

### Agentic vs Semantic Search

> "Semantic search is usually faster than agentic search, but less accurate, more difficult to maintain, and less transparent."

**Recommendation:** Start with agentic search (Claude explores using tools). Only add semantic search if you need faster results.

**Agentic search:** Claude uses grep, file reads, and exploration
**Semantic search:** Pre-indexed vector embeddings

## Git Workflows

Claude can:
- Search git history
- Write commit messages
- Handle complex operations (rebases, merges)
- Create PRs and respond to review comments
- Fix build failures

## Jupyter Notebooks

Claude works well with notebooks:
- Request aesthetic improvements
- Interpret outputs including images
- Fast data exploration cycles

## Source

[Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) — Anthropic Engineering Blog
