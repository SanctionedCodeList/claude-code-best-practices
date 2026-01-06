# Sessions

Search and read Claude Code session histories with a context-efficient API.

## Setup

Before using, run the install script:

```bash notest
./install.sh
```

This installs the `cc-best-practices` package and syncs the session index. Run it:
- First time to set up
- Periodically to index new sessions
- After any errors (ensures clean state)

Index location: `~/.claude/session-index/`

## API

Four operations: `search`, `meta`, `read`, and `list_sessions`.

All operations are accessed via Python heredoc scripts:

```bash notest
python3 <<'EOF'
from cc_best_practices.sessions import search, meta, read, list_sessions, sync
# ... your code here
EOF
```

### search(query, limit?, project?)

Semantic search across all sessions.

```python fixture:indexed_sessions
results = sessions.search("authentication", limit=5)
assert isinstance(results, list)
# Each result has: session_id, project, score, summary, first_message, start_time, message_count
if results:
    assert "session_id" in results[0]
    assert "score" in results[0]
```

### meta(session_id)

Get session statistics without loading message content.

```python fixture:indexed_sessions
info = sessions.meta(indexed_sessions["session_id"])
assert info is not None
assert "message_counts" in info
assert "tools_used" in info
assert "summaries" in info
# message_counts breaks down by type
assert "user" in info["message_counts"]
assert "assistant" in info["message_counts"]
assert "tool_use" in info["message_counts"]
```

### read(session_id, types?, tools?, first?, last?, offset?, limit?)

Read session messages with filtering.

**Message types:**
- `user` - User text prompts (not tool results)
- `assistant` - Claude text responses (not thinking/tools)
- `thinking` - Extended thinking blocks
- `tool_use` - Tool invocations
- `tool_result` - Tool responses
- `summary` - Session summaries

Python API:

```python fixture:indexed_sessions
session_id = indexed_sessions["session_id"]

# Read only user messages
user_msgs = sessions.read(session_id, types=["user"])
assert all(m["type"] == "user" for m in user_msgs)

# Read only tool calls
tools = sessions.read(session_id, types=["tool_use"])
assert all(m["type"] == "tool_use" for m in tools)
assert all("tool_name" in m for m in tools)

# Filter by specific tools
edits = sessions.read(session_id, types=["tool_use"], tools=["Edit"])
assert all(m["tool_name"] == "Edit" for m in edits)

# Positional filters
first_3 = sessions.read(session_id, first=3)
assert len(first_3) <= 3

last_2 = sessions.read(session_id, last=2)
assert len(last_2) <= 2
```

### list_sessions(project?, limit?)

List recent sessions.

```python fixture:indexed_sessions
recent = sessions.list_sessions(limit=10)
assert isinstance(recent, list)
if recent:
    assert "session_id" in recent[0]
    assert "project" in recent[0]
    assert "start_time" in recent[0]
```

## Usage Patterns

### Quick Session Overview

Get summaries + stats without loading messages:

```python fixture:indexed_sessions
info = sessions.meta(indexed_sessions["session_id"])
# Low context cost - just metadata
print(f"Project: {info['project']}")
print(f"Messages: {info['message_counts']}")
print(f"Tools: {info['tools_used']}")
print(f"Summaries: {info['summaries']}")
```

### Conversation Compression

For large sessions, load strategically to minimize context:

```python fixture:indexed_sessions
session_id = indexed_sessions["session_id"]

# Step 1: Get metadata to understand scope
info = sessions.meta(session_id)

# Step 2: Load summaries (if any)
summaries = sessions.read(session_id, types=["summary"])

# Step 3: First few user prompts (understand the task)
first_prompts = sessions.read(session_id, types=["user"], first=3)

# Step 4: Last few exchanges (see the resolution)
final_exchange = sessions.read(session_id, types=["user", "assistant"], last=4)

# Now you have: metadata + summaries + beginning + end
# Much smaller than loading the entire session
```

### Audit File Changes

Find what files were modified in a session:

```python fixture:indexed_sessions
session_id = indexed_sessions["session_id"]

# Get all Write and Edit tool calls
file_changes = sessions.read(session_id, types=["tool_use"], tools=["Write", "Edit"])

for change in file_changes:
    tool = change["tool_name"]
    file_path = change["input"].get("file_path", "unknown")
    print(f"{tool}: {file_path}")
```

### Review Commands Run

See bash commands and their outputs:

```python fixture:indexed_sessions
session_id = indexed_sessions["session_id"]

# Get Bash tool calls
commands = sessions.read(session_id, types=["tool_use"], tools=["Bash"])
for cmd in commands:
    print(f"Command: {cmd['input'].get('command', '')[:100]}")
```

### Understand Reasoning

Read Claude's thinking process for complex decisions:

```python fixture:indexed_sessions
session_id = indexed_sessions["session_id"]

thinking = sessions.read(session_id, types=["thinking"])
for thought in thinking:
    # Thinking blocks can be long - truncate for preview
    preview = thought["content"][:200] + "..." if len(thought["content"]) > 200 else thought["content"]
    print(preview)
```

### Full Dialogue (No Tools)

Read the conversation without tool noise:

```python fixture:indexed_sessions
session_id = indexed_sessions["session_id"]

dialogue = sessions.read(session_id, types=["user", "assistant"])
for msg in dialogue:
    role = "User" if msg["type"] == "user" else "Claude"
    content = msg["content"][:100] if msg["content"] else ""
    print(f"{role}: {content}")
```

### Learning From Past Sessions

Find how similar problems were solved before:

```python fixture:indexed_sessions
# Search for relevant past work
results = sessions.search("JWT token validation", limit=3)

for r in results:
    print(f"Session: {r['session_id']}")
    print(f"Project: {r['project']}")
    print(f"Score: {r['score']}")
    print(f"Summary: {r['summary']}")
    print()
```

### Continue Previous Work

Resume where a session left off:

```python fixture:indexed_sessions
# List recent sessions for the current project
recent = sessions.list_sessions(project="test", limit=5)

if recent:
    # Get the most recent session
    latest = recent[0]
    session_id = latest["session_id"]

    # Load the last few messages to understand state
    context = sessions.read(session_id, types=["user", "assistant"], last=6)

    # Now you have context to continue
```

### Cross-Session Pattern Search

Find patterns across multiple sessions:

```python fixture:indexed_sessions
# Find all sessions involving a topic
results = sessions.search("authentication", limit=10)

# Collect approaches used across sessions
for r in results:
    info = sessions.meta(r["session_id"])
    tools = info["tools_used"]
    print(f"{r['project']}: {tools}")
```

### Paginated Reading

For very large sessions, read in chunks:

```python fixture:indexed_sessions
session_id = indexed_sessions["session_id"]

page_size = 20
offset = 0

while True:
    page = sessions.read(session_id, offset=offset, limit=page_size)
    if not page:
        break
    # Process this page
    print(f"Read {len(page)} messages starting at {offset}")
    offset += page_size
```

## Index Maintenance

Run `./install.sh` to sync new sessions (incremental, fast).

Force full rebuild if index seems corrupted:

```bash notest
python3 <<'EOF'
from cc_best_practices.sessions import sync
stats = sync(force=True, verbose=True)
print(stats)
EOF
```

## Reporting Issues

Report bugs at: https://github.com/SanctionedCodeList/claude-code-best-practices/issues
