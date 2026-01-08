# Library-Backed Skills

When a skill requires code beyond simple scripts—libraries, APIs, or complex functionality—the skill should live **in the library's repository**, not as a standalone skill.

## Repository Structure

Place skills in a `./skills` folder within the library repo:

```
my-library/
├── src/                    # Library source code
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       ├── install.sh      # Required for library-backed skills
│       └── references/
└── pyproject.toml          # or package.json
```

This ensures the skill stays in sync with the library it depends on.

## Language Preference

Prefer **Python** or **TypeScript** for functional components. These languages:
- Have strong LLM support (models write them well)
- Have mature package ecosystems
- Support both scripting and library patterns

## Agent Interaction Patterns

### Use APIs, Not CLIs

**Critical rule**: For libraries bundled with skills, agents should use the **Python/TypeScript API directly**, not CLI wrappers.

| Approach | When to Use |
|----------|-------------|
| Python/TS API via heredoc | Libraries we provide with the skill |
| CLI commands | External tools not bundled with the skill |

**Rationale**: LLMs are excellent at writing code. A well-structured API gives agents flexibility and composability. CLIs are rigid and require parsing string output.

**Bad** (CLI for bundled library):
```markdown
Run `my-tool convert --input file.pdf --output file.docx`
```

**Good** (API via heredoc):
```markdown
python3 << 'EOF'
from my_library import convert
convert("file.pdf", "file.docx", track_changes=True)
EOF
```

### Heredoc Execution Pattern

Instruct agents to execute code via heredocs with the appropriate runtime:

**Python:**
```bash
python3 << 'EOF'
from my_library import Document

doc = Document("input.docx")
doc.replace("old text", "new text")
doc.save("output.docx")
EOF
```

**TypeScript/Node:**
```bash
npx ts-node << 'EOF'
import { Document } from 'my-library';

const doc = new Document("input.docx");
doc.replace("old text", "new text");
doc.save("output.docx");
EOF
```

### File-Based Content Exchange

When agents need to provide content that:
- Must persist across operations
- Needs to be edited/refined
- Is large or complex

**Write to files** rather than passing inline:

```markdown
## Workflow

1. Write your content to `content.md`
2. Run the processor:

python3 << 'EOF'
from my_library import process
process(input_file="content.md", output_file="result.pdf")
EOF
```

This allows agents to:
- Edit the file iteratively
- Inspect intermediate results
- Recover from errors without re-entering content

### External State Management

For skills requiring persistent external state (browser sessions, servers, watchers):

1. **Provide a `start.sh` script** to launch the external process
2. **Document how to interact** with the running process
3. **Provide a `stop.sh` script** if cleanup is needed

```
my-skill/
├── SKILL.md
├── install.sh
├── start.sh      # Starts browser/server/watcher
└── stop.sh       # Cleanup (optional)
```

**SKILL.md example:**
```markdown
## Setup

1. Run `./install.sh` to install dependencies
2. Run `./start.sh` to start the browser session

The browser runs in the background. Interact via the API:

python3 << 'EOF'
from my_library import browser
browser.navigate("https://example.com")
browser.click("#submit")
EOF
```

## install.sh Requirements

Library-backed skills **must** include `install.sh`. Requirements:

| Requirement | Description |
|-------------|-------------|
| **Idempotent** | Safe to run multiple times |
| **User-space** | No sudo, install to user directories |
| **Clear output** | Exit 0 on success, non-zero on failure |
| **Informative errors** | Explain what failed and how to fix |

**Example:**
```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check Python version
python3 -c "import sys; assert sys.version_info >= (3, 10)" 2>/dev/null || {
    echo "Error: Python 3.10+ required"
    exit 1
}

# Install in user space
pip install --user -e "$SCRIPT_DIR/.."

echo "Installation complete"
```

## Summary

| Pattern | Implementation |
|---------|----------------|
| Skill location | `./skills` folder in library repo |
| Language | Python or TypeScript |
| Agent execution | Heredocs, not CLIs |
| Content exchange | Files, not inline |
| External state | `start.sh` / `stop.sh` |
| Dependencies | `install.sh` (required) |
