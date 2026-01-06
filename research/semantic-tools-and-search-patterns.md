# Semantic Tools and Search Patterns for AI Agents

Research on semantic alternatives to traditional bash tools and search strategies for AI coding agents.

## The Problem

Traditional tools have limitations for AI agents:

**grep limitations:**
- Requires agents to "guess all possible keywords"
- Returns "large, noisy blocks of code that pollute the context window"
- Multiple tool calls increase latency and token consumption
- No semantic understanding — matches text, not concepts

**Vector search limitations:**
- "Fuzziness becomes a liability when surgical precision is required"
- Surfaces incorrect lookalike functions
- Snippets arrive "decontextualized, shorn from their callers, tests, or configuration files"
- Embeddings can be stale in rapidly evolving repositories

## Two Schools of Thought

### 1. Vercel's "Less is More" Approach

Vercel removed 80% of their agent's tools and kept just **bash command execution**.

**Philosophy:** "The model makes better choices when we stop making choices for it."

**Their file system agent uses:**
- `grep` for pattern matching
- `cat` for reading files
- `ls` for directory listing
- `find` for file discovery

**Results:**
- 3.5x faster (77.4s vs 274.8s)
- 100% success rate (up from 80%)
- 37% fewer tokens
- 42% fewer steps

**Key insight:** "Grep is 50 years old and still does exactly what we need. We were building custom tools for what Unix already solves."

### 2. Semantic Enhancement Approach

Add semantic tools that complement (not replace) traditional tools.

**Cursor's hybrid approach:** "The agent uses both grep and semantic search together, with the combination producing superior outcomes."

**Results from semantic search:**
- 12.5% higher accuracy in answering codebase questions
- 2.6% code retention improvement on large codebases (1,000+ files)

## Semantic Tools

### mgrep (Mixedbread)

Semantic version of grep using natural language queries.

**Installation:**
```bash
npm install -g @mixedbread/mgrep
mgrep login
mgrep watch
```

**Claude Code integration:**
```bash
mgrep install-claude-code
```

**How it works:**
- Syncs local directories to cloud-backed search index
- Returns files with line numbers and similarity scores
- Multi-vector technology (every word as its own vector)

**Performance improvements:**
- 53% fewer tokens
- 48% faster responses
- 3.2x better quality responses

**Best use:** Semantic exploration ("where do we handle authentication?")

### osgrep

Open-source semantic grep for local code repositories.

**Key difference from grep:**
- Traditional grep matches exact strings/regex
- osgrep understands concepts — search for "authentication logic" and find `validateUserCredentials`

**Features:**
- Uses embeddings for semantic similarity
- Native plugin support for Claude Code
- 100% local operation

### CodeGrok MCP

MCP server for semantic code search.

**Features:**
- AST parsing + vector embeddings
- 10x better context efficiency claimed
- 100% local operation

### ast-grep

AST-based pattern matching (not semantic, but smarter than text grep).

**Use case:** Code searching, linting, rewriting at large scale using syntax tree patterns rather than text patterns.

## Anthropic's Recommendations

From the [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) blog:

### Agentic vs Semantic Search

> "Semantic search is usually faster than agentic search, but less accurate, more difficult to maintain, and less transparent. Start with agentic search, and only add semantic search if you need faster results."

**Agentic search:** Claude explores the codebase using tools (grep, file reads, etc.)
**Semantic search:** Pre-indexed vector embeddings queried by concept

### CLAUDE.md for Tool Documentation

Document your custom tools in CLAUDE.md:
- Tool names with usage examples
- Instruct Claude to run `--help` for documentation
- Frequently-used tools and their purposes

### The Explore-Plan-Code-Commit Pattern

1. **Explore** — Have Claude read files without coding
2. **Plan** — Use extended thinking ("think harder", "ultrathink")
3. **Code** — Implement with clear constraints
4. **Commit** — Let Claude handle git operations

### Extended Thinking Triggers

| Phrase | Effect |
|--------|--------|
| "think" | Basic extended thinking |
| "think hard" | More computation |
| "think harder" | Even more |
| "ultrathink" | Maximum computation |

## Best Practices for Code Retrieval

From research on agent-ready retrieval:

### Six Principles

1. **Return complete behavioral units** — Entire functions/classes, not snippets
2. **Preserve code adjacency** — Include callers, tests, configuration
3. **Prioritize precision over quantity** — Less noise, more signal
4. **Treat recent changes as primary relevance signals** — Fresh code matters more
5. **Provide explicit relevance justifications** — Why this result?
6. **Enable interactive, iterative retrieval loops** — Progressive discovery

### The Litmus Test

> "Can the system return the rate-limiting function, call sites, configuration, and tests as one cohesive package?"

## Recommended Approach

### For Most Use Cases

Start with Anthropic's recommendation: **agentic search first**.

```
Claude Code uses grep/find/cat → reads files → reasons about code
```

This is transparent, maintainable, and works well for most codebases.

### For Large Codebases (1,000+ files)

Add semantic search as complement:

```
Semantic tool (mgrep/osgrep) → finds relevant areas
grep → precise pattern matching
Claude → reasoning and implementation
```

### When to Use What

| Task | Tool |
|------|------|
| Find exact symbol/function name | `grep` |
| Find conceptually similar code | `mgrep` / semantic search |
| Explore unfamiliar codebase | Semantic search first, then grep |
| Refactoring known patterns | `grep` with `--replace` or `ast-grep` |
| Understanding code flow | Agentic exploration (let Claude navigate) |

## Tool Comparison

| Tool | Type | Local? | Best For |
|------|------|--------|----------|
| `grep` | Text pattern | Yes | Exact matches, symbols |
| `mgrep` | Semantic | Cloud | Conceptual discovery |
| `osgrep` | Semantic | Yes | Local semantic search |
| `ast-grep` | AST pattern | Yes | Syntax-aware refactoring |
| CodeGrok MCP | Semantic MCP | Yes | Claude Code integration |

## Sources

### Official
- [Claude Code Best Practices - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)

### Industry Approaches
- [We Removed 80% of Our Agent's Tools - Vercel](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)
- [Improving Agent with Semantic Search - Cursor](https://cursor.com/blog/semsearch)
- [Beyond Grep and Vectors - DEV Community](https://dev.to/akshat_ilen/beyond-grep-and-vectors-reimagining-code-retrieval-for-ai-agents-4pb2)

### Tools
- [mgrep - Mixedbread](https://elite-ai-assisted-coding.dev/p/mgrep-with-founding-engineer-rui)
- [osgrep](https://www.scriptbyai.com/osgrep-semantic-search/)
- [ast-grep](https://ast-grep.github.io/)
- [CodeGrok MCP](https://hackernoon.com/codegrok-mcp-semantic-code-search-that-saves-ai-agents-10x-in-context-usage)
