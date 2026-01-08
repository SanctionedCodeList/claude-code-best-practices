# Artifacts Implementation Research

*Research date: 2026-01-07*

## Summary

This research examines how Anthropic (Claude Artifacts), OpenAI (ChatGPT Canvas), and Google (Gemini Canvas) implement their live code preview/artifacts systems, including rendering engines, widget libraries, and sandboxing techniques.

---

## Claude Artifacts (Anthropic)

### Rendering Engine

**react-runner** - A lightweight library for executing dynamic React code in the browser.

From reverse engineering the JS bundle, Claude uses react-runner to render dynamic React components. Unlike Sandpack (CodeSandbox), react-runner is simpler and doesn't include a full npm/bundler environment.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    claude.ai                             │
│  ┌─────────────────────┐                                │
│  │   Chat Interface    │                                │
│  │                     │  window.postMessage()          │
│  │   <antArtifact>     │ ──────────────────────────────►│
│  │   XML in response   │                                │
│  └─────────────────────┘                                │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│            claudeusercontent.com (iframe)                │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Sandboxed Environment               │   │
│  │                                                  │   │
│  │  • react-runner executes JSX                    │   │
│  │  • DOMPurify sanitizes HTML                     │   │
│  │  • Pre-bundled libraries available              │   │
│  │  • CSP restricts to cdnjs.cloudflare.com        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Security Model

- **Iframe isolation** on separate domain (`claudeusercontent.com`)
- **Full-site process isolation** protects main browsing session
- **Content Security Policy (CSP)** restricts network to `cdnjs.cloudflare.com`
- **DOMPurify** for HTML sanitization

### Available Libraries

| Library | Version | Import Example |
|---------|---------|----------------|
| **React** | 18.x | Built-in |
| **Tailwind CSS** | 3.x | Class-based styling |
| **shadcn/ui** | Latest | `import { Button } from '@/components/ui/button'` |
| **Lucide React** | 0.263.1 | `import { Camera } from 'lucide-react'` |
| **Recharts** | Latest | `import { LineChart } from 'recharts'` |
| **D3** | Latest | `import * as d3 from 'd3'` |
| **Three.js** | r128 | `import * as THREE from 'three'` |
| **Lodash** | Latest | `import _ from 'lodash'` |
| **MathJS** | Latest | `import * as math from 'mathjs'` |
| **Plotly** | Latest | `import * as Plotly from 'plotly'` |
| **PapaParse** | Latest | CSV processing |
| **SheetJS** | Latest | Excel (XLSX, XLS) processing |
| **Chart.js** | Latest | Alternative charting |
| **Tone.js** | Latest | Audio synthesis |

### Additional Dependencies (from bundle analysis)

- **Radix UI Primitives** - Accessible component primitives (foundation for shadcn)
- **React Hot Loader** - Live reloading
- **React Zoom Pan Pinch** - Interactive canvas manipulation

### Artifact Types

| Type | MIME Type | Description |
|------|-----------|-------------|
| React | `application/vnd.ant.react` | JSX components |
| HTML | `text/html` | Single-file webpages |
| SVG | `image/svg+xml` | Vector graphics |
| Code | `application/vnd.ant.code` | Syntax-highlighted code |
| Markdown | `text/markdown` | Documents |
| Mermaid | `application/vnd.ant.mermaid` | Diagrams |

### Restrictions

- No API calls or external data fetching (sandbox blocks network)
- External scripts limited to `cdnjs.cloudflare.com` CDN
- No web images (use `/api/placeholder/width/height` instead)
- Certain Three.js features unavailable (OrbitControls, CapsuleGeometry)
- No zod, react-hook-form, or other unlisted libraries

---

## ChatGPT Canvas (OpenAI)

### Rendering Engine

**Unknown** - OpenAI has not publicly documented the rendering engine.

There's "clearly some kind of optional build step used to compile React JSX to working code, but the details are opaque."

### Architecture

Less documented than Claude, but known features:

- Sandbox environment for code execution
- JSX compilation step (specific compiler unknown)
- CDN library imports supported (specific CDNs undocumented)
- Error detection with "Fix bug" auto-repair feature

### Available Features

| Feature | Status |
|---------|--------|
| HTML rendering | Yes |
| React/JSX rendering | Yes |
| CDN library imports | Yes (undocumented which) |
| npm packages | "All npm packages and many JavaScript libraries will work" |
| Network access | Configurable (off by default for enterprise) |
| Python execution | Yes |
| o1 model support | Yes |

### Security Model

- Sandbox environment
- Enterprise admins can control:
  - Whether code execution is available
  - Network access permissions

### Key Differences from Claude

- **Python execution** - Canvas can run Python, Claude Artifacts cannot
- **Network access** - Configurable, not strictly blocked
- **Model flexibility** - Works with o1 model
- **Less documented** - Technical details remain opaque

---

## Gemini Canvas (Google)

### Rendering Engine

**Unknown** - Google has not publicly documented implementation details.

### Architecture

- Real-time collaborative workspace
- Live preview for React and HTML
- Code editor with diff view for changes
- 1M token context window (Pro/Ultra)

### Available Features

| Feature | Status |
|---------|--------|
| HTML generation | Yes |
| React generation | Yes |
| JavaScript generation | Yes |
| Live preview | Yes |
| Change tracking | Yes (per-turn diffs) |

### Noted Capabilities

"Not only does it generate the code, but it also provides a live preview so you can see the design come to life instantly."

### Missing Documentation

Google has not disclosed:
- Rendering engine
- Available libraries
- Sandboxing implementation
- CDN restrictions

---

## Comparison Matrix

| Feature | Claude Artifacts | ChatGPT Canvas | Gemini Canvas |
|---------|------------------|----------------|---------------|
| **Rendering engine** | react-runner | Unknown | Unknown |
| **Primary framework** | React | React | React |
| **Styling** | Tailwind CSS | Unknown | Unknown |
| **Component library** | shadcn/ui + Radix | Unknown | Unknown |
| **Icons** | Lucide React | Unknown | Unknown |
| **Charts** | Recharts, D3, Plotly | Unknown | Unknown |
| **3D** | Three.js (r128) | Unknown | Unknown |
| **Python** | No | Yes | Unknown |
| **Network access** | Blocked (CSP) | Configurable | Unknown |
| **CDN whitelist** | cdnjs.cloudflare.com | "Various" | Unknown |
| **Open documentation** | Partially reverse-engineered | Minimal | Minimal |

---

## Open Source Alternatives

### Sandpack (CodeSandbox)

**Most popular for building artifact-like features.**

```bash
npm install @codesandbox/sandpack-react
```

Features:
- Full npm dependency support
- Hot module reloading
- Node.js support via Nodebox
- Multiple file support
- Error overlays

Used by: LlamaCoder, Together AI artifacts clone, many tutorials

### react-runner

**Lighter alternative (what Claude uses).**

```bash
npm install react-runner
```

Features:
- Simple API
- TypeScript support
- Server-side rendering
- Smaller bundle than Sandpack

### react-live

**Popular for documentation/playgrounds.**

Similar to react-runner but older, requires manual function binding.

### claude-artifact-runner

**Drop-in local runner for Claude artifacts.**

```bash
npx run-claude-artifact my-app.tsx
```

Pre-bundles all Claude artifact dependencies (shadcn, Recharts, Lucide, etc.)

---

## Key Insights

### Why shadcn/ui?

1. **Copy-paste model** - Components are local files, not npm imports
2. **AI-optimized** - Explicitly designed to be "AI-Ready: Open code for LLMs to read, understand, and improve"
3. **Radix foundation** - Accessible primitives already work
4. **Tailwind integration** - No CSS-in-JS complexity

### Why Tailwind?

1. **Utility classes** - Deterministic, predictable output
2. **No build step** - Classes work immediately
3. **Constraint system** - Prevents arbitrary values
4. **Training data** - Massive corpus for LLMs

### Why iframe isolation?

1. **Security** - Malicious code can't access parent session
2. **CSP enforcement** - Network restrictions
3. **Process isolation** - Browser-level sandboxing
4. **Domain separation** - Cookie/storage isolation

---

## Building Your Own

### Minimal Stack (Claude-like)

```
react-runner + Tailwind CDN + shadcn components
```

### Full-Featured Stack (Sandpack-based)

```
Sandpack + custom dependency list + iframe wrapper
```

### Security Considerations

1. Use iframe with `sandbox` attribute
2. Host on separate domain/subdomain
3. Implement CSP headers
4. Sanitize HTML with DOMPurify
5. Limit network access

---

## Sources

### Claude Artifacts
- https://www.reidbarber.com/blog/reverse-engineering-claude-artifacts
- https://simonwillison.net/2024/Oct/23/claude-artifact-runner/
- https://github.com/claudio-silva/claude-artifact-runner
- https://gist.github.com/dedlim/6bf6d81f77c19e20cd40594aa09e3ecd

### OpenAI Canvas
- https://help.openai.com/en/articles/9930697-what-is-the-canvas-feature-in-chatgpt-and-how-do-i-use-it
- https://simonwillison.net/2025/jan/25/openai-canvas-gets-a-huge-upgrade/
- https://openai.com/index/introducing-canvas/

### Google Gemini Canvas
- https://gemini.google/overview/canvas/
- https://workspaceupdates.googleblog.com/2025/03/introducing-canvas-for-the-gemini-app.html

### Rendering Libraries
- https://www.npmjs.com/package/react-runner
- https://github.com/nihgwu/react-runner
- https://sandpack.codesandbox.io/
- https://github.com/codesandbox/sandpack

### Open Source Implementations
- https://docs.together.ai/docs/how-to-build-a-claude-artifacts-clone-with-llama-31-405b
- https://github.com/langchain-ai/open-canvas
