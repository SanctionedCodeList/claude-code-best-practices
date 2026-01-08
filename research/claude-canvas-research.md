# Claude Canvas Research

*Research date: 2026-01-07*

## Summary

Claude Canvas is a proof-of-concept plugin that gives Claude Code an "external monitor" - a separate tmux pane where it can spawn interactive TUIs (terminal user interfaces) for rich visual displays.

**Repository**: https://github.com/dvdsgl/claude-canvas
**Author**: David Siegel (@dvdsgl)
**Status**: Proof of concept, unsupported

## The Problem It Solves

Claude Code operates in a terminal, limited to text output. For tasks involving:
- Email composition and preview
- Calendar scheduling
- Flight booking comparisons
- Document editing with selection

...plain text is insufficient. Claude Canvas provides a visual "second screen" for structured interactions.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        tmux session                          │
│  ┌──────────────────────┐  ┌──────────────────────────────┐ │
│  │   Claude Code CLI    │  │     Canvas TUI (Ink/React)   │ │
│  │                      │  │                              │ │
│  │  - Runs commands     │  │  - Email preview             │ │
│  │  - Spawns canvases   │  │  - Calendar picker           │ │
│  │  - Sends IPC msgs    │  │  - Flight booking            │ │
│  │                      │  │  - Document editor           │ │
│  └──────────────────────┘  └──────────────────────────────┘ │
│           │                           │                      │
│           └───── Unix Socket IPC ─────┘                      │
│                 /tmp/canvas-{id}.sock                        │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

| Component | File | Purpose |
|-----------|------|---------|
| CLI | `src/cli.ts` | Commander-based CLI with `show`, `spawn`, `update`, `selection`, `content` commands |
| Terminal | `src/terminal.ts` | Detects tmux environment, spawns/reuses split panes |
| IPC Server | `src/ipc/server.ts` | Unix socket server for canvas-to-Claude communication |
| IPC Client | `src/ipc/client.ts` | Unix socket client for Claude-to-canvas communication |
| Canvas API | `src/api/canvas-api.ts` | High-level async functions like `pickMeetingTime()`, `editDocument()` |
| Canvases | `src/canvases/` | Ink (React for terminal) components |

## How It Works

### 1. Spawning a Canvas

```bash
bun run src/cli.ts spawn document --scenario email-preview --config '{
  "from": "david@example.com",
  "to": ["mark@example.com"],
  "subject": "Meeting next week",
  "content": "# Hello\n\nLooking forward to seeing you!"
}'
```

### 2. tmux Pane Management

The `terminal.ts` module:
- Detects if running inside tmux (required)
- Creates a new split pane at 67% width (2:1 ratio, Claude:Canvas)
- Tracks pane ID in `/tmp/claude-canvas-pane-id` for reuse
- Sends `Ctrl+C` to existing pane before reusing

### 3. IPC Communication

**Messages from Canvas to Claude:**
```typescript
{ type: "ready", scenario }        // Canvas initialized
{ type: "selected", data }         // User made a selection
{ type: "cancelled", reason? }     // User pressed Escape
{ type: "error", message }         // Something went wrong
{ type: "selection", data }        // Current text selection
{ type: "content", data }          // Current document content
```

**Messages from Claude to Canvas:**
```typescript
{ type: "update", config }  // Update canvas with new data
{ type: "close" }           // Request canvas to close
{ type: "ping" }            // Health check
{ type: "getSelection" }    // Request current selection
{ type: "getContent" }      // Request current content
```

### 4. Canvas Rendering

Canvases use **Ink** (React for terminals) with:
- Mouse support via ANSI escape sequences
- Keyboard input handling
- Responsive layouts based on terminal dimensions
- Scroll support for long content

## Canvas Types

### Document Canvas

**Scenarios:**
- `display` - Read-only markdown rendering
- `edit` - Editable with cursor and text selection
- `email-preview` - Email with headers (From, To, Cc, Bcc, Subject)

**Features:**
- Markdown rendering
- Mouse click-and-drag text selection
- Cursor navigation with arrow keys
- Scroll with Page Up/Down
- Selection reported via IPC

### Calendar Canvas

**Scenarios:**
- `display` - Show calendar events
- `meeting-picker` - Interactive time slot selection

**Features:**
- Event display with colors
- Time slot grid
- Mouse-based selection
- Returns selected time slot via IPC

### Flight Canvas

**Scenarios:**
- `booking` - Flight comparison and seat selection

**Features:**
- Flight list with tabs
- Seat map visualization
- Price comparison
- Selection returns flight + seat data

## High-Level API

For programmatic use within skills:

```typescript
import { pickMeetingTime, editDocument } from "./src/api";

// Spawn meeting picker and wait for user selection
const result = await pickMeetingTime({
  calendars: [...],
  slotGranularity: 30,
});

if (result.success && result.data) {
  console.log(`Selected: ${result.data.startTime}`);
}

// Edit a document and get selection
const docResult = await editDocument({
  content: "# My Document\n\nEdit me!",
  title: "Draft",
});

if (docResult.success && docResult.data) {
  console.log(`Selected text: ${docResult.data.selectedText}`);
}
```

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Bun** | Runtime (faster than Node, built-in TypeScript) |
| **Ink** | React renderer for terminal UIs |
| **tmux** | Terminal multiplexer for pane management |
| **Unix sockets** | IPC between Claude and canvas processes |
| **Commander** | CLI argument parsing |
| **React** | Component architecture for canvas UIs |

## Installation

```bash
# Add marketplace
/plugin marketplace add dvdsgl/claude-canvas

# Install plugin
/plugin install canvas@claude-canvas
```

## Requirements

- **Bun** - Runtime for executing canvas commands
- **tmux** - Required for pane spawning
- **Terminal with mouse support** - For click-based interactions

## Limitations

- Requires tmux (won't work in plain terminal)
- TUI-based, limited to terminal capabilities
- Proof of concept, not production-ready
- No persistence of canvas state across sessions

## Potential Improvements

- Browser-based canvas alternative (web UI instead of TUI)
- Persistent canvas sessions
- More canvas types (charts, diagrams, code diff viewers)
- Support for non-tmux environments (kitty splits, iTerm2 splits)

---

## Browser-Based Alternatives

Several projects provide similar "visual canvas" functionality but through browser interfaces rather than terminal TUIs.

### Layrr (Visual Claude)

**Repository**: https://github.com/thetronjohnson/visual-claude

A universal visual editor that works like Elementor or Framer but on any website.

**How it works:**
- Reverse proxy sits between browser and dev server
- JavaScript injected into pages provides editing interface
- WebSocket enables real-time communication
- Users select/drag/resize elements visually
- Changes sent to Claude Code which updates actual source code

**Key features:**
- Drag and resize with live preview (8-handle resize system)
- Framework-aware output (detects Tailwind, CSS, etc.)
- Design-to-code from uploaded images
- Natural language instructions for UI changes
- Works with any dev server (Vite, Next.js, webpack)

**Use case**: Visual WYSIWYG editing of live websites with AI-powered code updates.

### Claudia GUI

**Website**: https://claudia.so/

Desktop GUI wrapper for Claude Code built with Tauri 2 + React + Rust.

**Key features:**
- Session time travel with checkpoints and branching
- Visual timeline navigation
- Analytics dashboard for cost/token tracking
- MCP server management UI
- Project browser with smart search
- Custom AI agent visual editor

**Platforms**: macOS, Linux, Windows (AGPL license)

**Use case**: Full desktop GUI replacement for Claude Code CLI.

### Open Canvas (LangChain)

**Repository**: https://github.com/langchain-ai/open-canvas

Open source web app for document collaboration with AI agents, inspired by OpenAI Canvas.

**Key features:**
- Artifact versioning with time travel
- Dual-mode editing (code + markdown)
- Live markdown rendering
- Built-in memory system (reflection agents)
- Quick actions for one-click modifications
- Multiple LLM provider support

**Tech stack**: Next.js + LangGraph + Supabase

**Use case**: Document/code editing with AI assistance and version history.

### Claude Code Frontend Dev

**Repository**: https://github.com/hemangjoshi37a/claude-code-frontend-dev

Visual testing plugin that lets Claude "see" your UI.

**How it works:**
- Captures screenshots via Puppeteer/Playwright
- Claude 4.5 Sonnet analyzes UI visually
- Automatic testing on file changes
- Six specialized agents (coordinator, UX, tester, etc.)

**Key features:**
- 10 test categories (functional, a11y, performance, responsive, etc.)
- Multi-viewport screenshots
- Framework agnostic
- Pass/fail scoring with fix recommendations

**Use case**: Automated visual testing and UI verification.

### Claude Artifacts (Built-in)

Claude.ai's native artifact system for visual output.

**Capabilities:**
- Live preview panel alongside chat
- React component rendering
- HTML/CSS/JS webpage generation
- SVG and Mermaid diagrams
- Code with syntax highlighting

**Limitations:**
- No API calls or external data
- Static rendering only
- No server-side execution

**Relevant skills:**
- `artifacts-builder` - Build complex HTML artifacts
- `frontend-design` - Bold design decisions for React/Tailwind
- `canvas-design` - Visual art in PNG/PDF

### Comparison Matrix

| Tool | Type | Visual Output | AI Integration | Self-Hosted |
|------|------|---------------|----------------|-------------|
| **claude-canvas** | TUI (tmux) | Terminal UI | Claude Code | Yes |
| **Layrr** | Browser proxy | Live website | Claude Code | Yes |
| **Claudia GUI** | Desktop app | Native GUI | Claude Code | Yes |
| **Open Canvas** | Web app | Browser | Multiple LLMs | Yes |
| **Frontend Dev** | Plugin | Screenshots | Claude Code | Yes |
| **Claude Artifacts** | Web (claude.ai) | Browser | Claude | No |

### Key Differences

**claude-canvas (TUI)**:
- Pros: Works in any terminal, lightweight, tmux integration
- Cons: Limited to terminal capabilities, requires tmux

**Browser-based alternatives**:
- Pros: Rich UI, mouse interaction, familiar web interface
- Cons: Requires browser/server, more setup complexity

## Sources

- https://github.com/dvdsgl/claude-canvas
- https://x.com/dvdsgl/status/2008685488107139313
- https://github.com/thetronjohnson/visual-claude
- https://claudia.so/
- https://github.com/langchain-ai/open-canvas
- https://github.com/hemangjoshi37a/claude-code-frontend-dev
- https://claude-plugins.dev/
