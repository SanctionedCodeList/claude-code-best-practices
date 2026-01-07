# Example marketplace.json Files

Real-world examples from production plugins.

## Single Plugin Repository

From `dev-browser` — a browser automation plugin:

```json
{
  "name": "dev-browser-marketplace",
  "owner": {
    "name": "Sawyer Hood",
    "email": "sawyerjhood@gmail.com"
  },
  "plugins": [
    {
      "name": "dev-browser",
      "source": "./",
      "description": "Browser automation skill with persistent page state and LLM-optimized DOM snapshots",
      "skills": ["./skills/dev-browser"]
    }
  ]
}
```

**Key points:**
- Marketplace name matches plugin name with `-marketplace` suffix
- Single plugin with `source: "./"` (same repo)
- Skills array points to skill directory

---

## Plugin with Multiple Skills

From `cc-dev` — this plugin:

```json
{
  "name": "claude-code-best-practices",
  "owner": {
    "name": "SanctionedCodeList",
    "url": "https://github.com/SanctionedCodeList/claude-code-best-practices"
  },
  "metadata": {
    "description": "Claude Code development tools and skills",
    "version": "0.1.0"
  },
  "plugins": [
    {
      "name": "cc-dev",
      "description": "Claude Code development guide: skill creation, plugin authoring, context injection, and power user tools",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/cc-dev"
      ]
    }
  ]
}
```

**Key points:**
- Uses metadata block for version tracking
- Owner URL points to GitHub repo
- `strict: false` means this manifest is complete (no separate plugin.json needed)

---

## Multi-Plugin Marketplace

From `scl-marketplace` — distributes plugins from multiple repos:

```json
{
  "name": "scl-marketplace",
  "owner": {
    "name": "SanctionedCodeList"
  },
  "metadata": {
    "description": "Professional-grade Claude Code plugins for legal, document, and office automation"
  },
  "plugins": [
    {
      "name": "law-tools",
      "source": {
        "source": "github",
        "repo": "SanctionedCodeList/law_tools"
      },
      "description": "Legal research toolkit with USPTO, court, SEC, and regulatory data connectors plus document drafting capabilities."
    },
    {
      "name": "writing",
      "source": {
        "source": "github",
        "repo": "SanctionedCodeList/writing"
      },
      "description": "Comprehensive writing guidance for professional documents with style guides and cognitive fluency techniques."
    },
    {
      "name": "office-bridge",
      "source": {
        "source": "github",
        "repo": "SanctionedCodeList/office-bridge"
      },
      "description": "Microsoft Office automation via Office.js add-ins for Word, Excel, and PowerPoint."
    },
    {
      "name": "python-docx-redline",
      "source": {
        "source": "github",
        "repo": "SanctionedCodeList/python-docx-redline"
      },
      "description": "Document creation, editing, and analysis with tracked changes support for .docx files."
    },
    {
      "name": "cc-dev",
      "source": {
        "source": "github",
        "repo": "SanctionedCodeList/claude-code-best-practices"
      },
      "description": "Claude Code development guide: skill creation, plugin authoring, context injection, and session history search."
    },
    {
      "name": "dev-browser",
      "source": {
        "source": "github",
        "repo": "SawyerHood/dev-browser"
      },
      "description": "Browser automation with persistent page state and LLM-optimized DOM snapshots."
    }
  ]
}
```

**Key points:**
- Each plugin has external source pointing to GitHub repo
- Source format: `{"source": "github", "repo": "owner/repo"}`
- No skills array needed — each repo defines its own skills
- Marketplace aggregates plugins from different authors

---

## Source Formats

### Local (same repo)
```json
"source": "./"
```

### GitHub
```json
"source": {
  "source": "github",
  "repo": "owner/repo-name"
}
```

### Local Directory (development)
```json
"source": {
  "source": "directory",
  "path": "/absolute/path/to/plugin"
}
```

---

## Validation Checklist

Before publishing, verify:

- [ ] `name` is lowercase with hyphens
- [ ] `plugins[].name` matches installation command
- [ ] `source` points to valid location
- [ ] `description` is concise but informative
- [ ] `skills` paths are correct (if specified)
- [ ] JSON is valid (no trailing commas)
