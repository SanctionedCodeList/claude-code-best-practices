# Claude Code Memory Systems: Comprehensive Research

*Compiled: 2025-12-31*

---

## Executive Summary

This document consolidates research on memory and context management for Claude Code, covering official features, community solutions, and emerging architectures.

**Key Findings:**
- Claude Code uses a 4-tier CLAUDE.md hierarchy as primary memory
- Auto-compaction at ~155k tokens is a major pain point
- MCP servers provide extensible memory solutions
- Multi-tier memory (working/episodic/semantic) is the emerging pattern
- Titans architecture may fundamentally change AI memory in the future

---

## 1. Official Memory Systems

### CLAUDE.md Hierarchy

| Priority | Location | Scope |
|----------|----------|-------|
| 1 (Highest) | Enterprise policy paths | Org-wide |
| 2 | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team (git) |
| 3 | `~/.claude/CLAUDE.md` | Personal (all projects) |
| 4 | `./CLAUDE.local.md` | Personal (gitignored) |

**Loading behavior:**
- Recursive discovery from cwd upward
- Subtree files loaded on-demand
- Import syntax: `@path/to/file` (max 5 hops)

### Modular Rules

```
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md
    ├── testing.md
    └── security.md
```

Path-specific rules via YAML frontmatter:
```yaml
---
paths: src/api/**/*.ts
---
```

### Session Management

```bash
claude -c                    # Resume most recent
claude -r "session-name"     # Resume by name
```

- Checkpoints on each prompt (30-day retention)
- `/rewind` or `Esc+Esc` to restore
- Tracks file edits only (not bash)

### Context Commands

| Command | Purpose |
|---------|---------|
| `/memory` | Edit CLAUDE.md files |
| `/compact [focus]` | Compress conversation |
| `/context` | Visualize token usage |
| `/clear` | Clear history completely |
| `/init` | Bootstrap CLAUDE.md |

---

## 2. Context Management Challenges

### Pain Points (from Twitter/X research)

**Auto-compaction destroys context:**
> "The auto-compacting just obliterates important context, and I get anxious as I get close to the limit."

**Signal degradation:**
> "Each compaction is lossy. After several, you're working with a summary of a summary of a summary."

**Session amnesia:**
> "Every time you closed your laptop or switched machines, it forgot everything."

### Technical Details

- Auto-compact triggers at ~155k tokens
- Context windows: 200k standard, up to 1M enterprise
- Effective context (before degradation): 60k-120k for Sonnet

### Workarounds

**Proactive management:**
- Use `/clear` for new tasks, `/compact` for continuation
- Disable auto-compact: `/config` → disable autocompact
- Add to system prompt: "Never stop tasks early due to token budget concerns"

**The /page command:**
- Runs as subagent (doesn't consume context)
- Intelligently saves conversation state
- Combine with `-r` to fork threads

---

## 3. Multi-Tier Memory Architecture

### Emerging Pattern

| Tier | Purpose | Example |
|------|---------|---------|
| **Working** | Current session | Active conversation |
| **Episodic** | Important past interactions | Key decisions, architecture choices |
| **Semantic** | General knowledge over time | Coding patterns, preferences |

### Implementation Approaches

**CLAUDE.md layers:**
1. Global preferences (always loaded)
2. Project-specific instructions
3. Reference context files (mix and match)

**Context engineering strategies:**
1. **Writing** - Craft context that guides behavior
2. **Selecting** - Choose right information to include
3. **Compressing** - Reduce tokens while preserving meaning
4. **Isolating** - Segment context for different purposes

---

## 4. RAG for Code

### How It Works

1. **Index** - Chunk code, convert to embeddings
2. **Query** - Convert question to vector
3. **Retrieve** - Find semantically similar chunks
4. **Augment** - Add to prompt
5. **Generate** - LLM responds with grounded context

### Best Practices

- **Dual-model approach**: NLP embeddings + code embeddings
- **AST-aware chunking**: Functions, classes, methods (not arbitrary splits)
- **Natural language summaries**: 12% better retrieval than raw code
- **Metadata enrichment**: Include docstrings, comments, file paths

### Top Embedding Models

| Model | Best For |
|-------|----------|
| Voyage-3-large | Code semantic understanding |
| StarCoder | 80+ languages, open source |
| jina-embeddings-v2-base-code | Code-to-code similarity |
| all-MiniLM-L6-v2 | NL queries about code |

---

## 5. MCP Memory Servers

### Official

**@modelcontextprotocol/server-memory**
- Knowledge graph with entities, relations, observations
- JSON file storage
- `npm i @modelcontextprotocol/server-memory`

### Community Solutions

| Server | Storage | Best For |
|--------|---------|----------|
| MCP Memory Service (doobidoo) | SQLite-vec | Multi-tool context |
| Qdrant MCP | Vector DB | Code snippet search |
| Claude Context (Zilliz) | Vector DB | Codebase indexing (~40% token reduction) |
| Neo4j MCP | Graph DB | Entity relationships |
| Memory Graph (Redis) | Graph DB | Conversation graphs |

### Third-Party Tools

**Claude-mem** - Open-source cross-session memory
**Claude Diary** - Self-updating memory with reflection
**Depot Claude** - Session save/resume across machines
**Beads** - Context survival across compaction

---

## 6. Summarization Techniques

### Approaches

1. **Sliding window** - Keep last N messages verbatim, summarize older
2. **Key message preservation** - Pin critical messages, compress between
3. **Multi-level hierarchies** - Working → episodic → semantic
4. **Episodic memory systems** - Semantic search over history

### Performance

- **80-90% token cost reduction**
- **26% quality improvement** vs basic chat history
- Removes tool call details that bloat context

---

## 7. Future: Titans Architecture

Google's neural long-term memory architecture (research stage).

### Three-Layer Memory

| Layer | Function |
|-------|----------|
| Persistent | Fixed weights (task knowledge) |
| Long-term | Neural network that learns at test time |
| Core | Standard attention (short-term) |

### Key Innovation: "Surprise" Signal

- Expected input → low surprise → forget
- Unexpected input → high surprise → memorize

### Implications for AI Agents

- Memory inside model weights (no external DB)
- Long-running agents without context reset
- Learning user preferences over time
- 2M+ token context windows

**Status:** Research only. Community PyTorch implementations available.

---

## 8. Recommended Implementation

### Immediate (works today)

1. **Master CLAUDE.md patterns**
   - Use 4-tier hierarchy effectively
   - Modular rules for large projects
   - Import syntax for references

2. **Proactive context management**
   - `/compact` after major operations
   - `/clear` for new tasks
   - Disable auto-compact if problematic

3. **Add MCP memory server**
   - Start with official server-memory
   - Graduate to vector DB for large codebases

### Near-term

4. **Implement episodic memory**
   - Key decisions and architecture choices
   - Cross-session persistence

5. **RAG for large codebases**
   - When file-based memory is insufficient
   - Dual-model embedding approach

### Future

6. **Monitor Titans development**
   - May fundamentally change memory architecture
   - Community implementations available for experimentation

---

## 9. Quick Reference

### Commands

```bash
/memory          # Edit CLAUDE.md
/compact [focus] # Compress context
/context         # Show token usage
/clear           # Wipe completely
/init            # Bootstrap CLAUDE.md
/rewind          # Restore previous state
```

### Environment Variables

```bash
ENABLE_BACKGROUND_TASKS=1    # Async subagents
DISABLE_PROMPT_CACHING=1     # Disable caching
```

### Key Files

```
~/.claude/CLAUDE.md          # Global memory
./CLAUDE.md                  # Project memory
./CLAUDE.local.md            # Personal (gitignored)
.claude/rules/*.md           # Modular rules
.claude/settings.json        # Configuration
```

---

## Sources

### Official
- [Claude Code Memory Docs](https://code.claude.com/docs/en/memory)
- [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### Research
- [Titans Paper (arXiv)](https://arxiv.org/abs/2501.00663)
- [Google Titans + MIRAS Blog](https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/)

### Community
- [MCP Memory Service](https://github.com/doobidoo/mcp-memory-service)
- [lucidrains/titans-pytorch](https://github.com/lucidrains/titans-pytorch)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

### Twitter/X
- [@bcherny](https://x.com/bcherny/status/1977163445205450783) - Auto-compact at 155k
- [@avthars](https://x.com/avthars/status/1988678651160982012) - Context management tips
- [@AnkMister](https://x.com/AnkMister/status/1955890941300257000) - /page command
