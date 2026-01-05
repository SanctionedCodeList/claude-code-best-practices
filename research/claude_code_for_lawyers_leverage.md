# Claude Code for Lawyers: The Leverage Case

**Draft v1 — December 2025**

---

## The Elevator Pitch

Lawyers understand leverage. It's why you hire associates, use templates, build precedent banks.

Claude Code is a new kind of leverage. It reads your files, queries databases, drafts documents—and learns how you work. Every correction becomes a Skill it follows forever. Every workflow you teach it is a tool you never have to build again.

It's not just an AI assistant. It's a force multiplier that makes other force multipliers.

**The only AI tool you need—because it makes other AI tools.**

---

## What Is Claude Code?

Claude Code is a command-line application from Anthropic that runs on your computer. Unlike ChatGPT or Claude.ai in your browser, it has two critical additional capabilities:

1. **It reads and writes files on your computer.** No uploading documents one at a time. Point it at a folder of discovery materials, prosecution files, or case law—it searches and finds what it needs.

2. **It runs commands on your computer.** It can execute code, query APIs, manage files, and produce actual artifacts—not just chat responses.

Think of 2022-2024 as the years of "prompt engineering"—being clever with your prompts. Then 2024-2025 became about "context engineering"—feeding the right documents at the right time. Claude Code obsoletes both. It's smart enough to figure out what you're asking and find what it needs to answer.

---

## The Five Dimensions of Leverage

### 1. Time Leverage
Do in hours what used to take days. Pull a prosecution history, synthesize 50 documents, draft a memo—in one session. When I say "pull the prosecution history for application 16/123,456," Claude Code generates a few lines of code, executes them, and synthesizes the results. No manual website navigation or copy-pasting.

### 2. Knowledge Leverage
Every correction you make can become a Skill. Your expertise compounds. The AI gets better at being *you*. When I ask Claude Code to draft an office action response, it doesn't start from scratch—it loads my skill, follows my workflow, and produces output in my style.

### 3. Tool Leverage
Need a tool that doesn't exist? Describe it. Claude Code builds it. No developers, no vendors, no six-month procurement cycle. A lawyer with zero coding background can build internal tools for their practice.

### 4. Scale Leverage
Subagents. Claude Code can spawn copies of itself to research in parallel. Imagine reviewing a complaint, generating a list of research topics, then having ten concurrent research threads running simultaneously—each producing its own memo to be synthesized later. One lawyer managing a digital research team.

### 5. Learning Leverage
You're not learning a product that will be obsolete in 18 months. You're learning to work with AI agents—a skill that transfers to whatever comes next. NYSBA is already teaching CLEs on this. The ABA's duty of technological competence is rising.

---

## The Memory System: CLAUDE.md

Claude Code has a layered memory system that persists across sessions. These are plain Markdown files that Claude reads at the start of every conversation.

### Three Levels of Memory

```
~/.claude/CLAUDE.md          # Global: applies to everything you do
~/Projects/case-x/CLAUDE.md  # Project: applies to this matter
~/Projects/case-x/.claude/   # Local settings and context
```

**Global CLAUDE.md** contains instructions that always apply—your preferred writing style, common procedures, paths to your tools and resources.

**Project CLAUDE.md** contains matter-specific context—the parties, key dates, relevant authorities, special instructions for this engagement.

### What Goes in CLAUDE.md

Think of it as onboarding a new associate, except you only have to do it once:

- **General procedures**: "For any research request, first check the case file for existing memos."
- **Style preferences**: "Use plain English. Avoid legalese. Follow Garner's principles."
- **Resource locations**: "Prior art searches are in /prior-art/. Client communications are in /correspondence/."
- **Decision frameworks**: "When presenting options, always include pros/cons and a recommendation."

The key insight: Claude reads these files automatically. You don't have to repeat yourself every session.

---

## Skills: Institutional Knowledge in AI-Followable Format

Skills are reusable workflow templates—institutional knowledge captured in a format the AI can follow. They're Markdown files with a specific structure that Claude discovers and loads when relevant.

### Anatomy of a Skill

```
office-action-response/
├── SKILL.md                 # Core instructions
├── references/
│   ├── claim-mapping.md     # How to map claims to references
│   ├── rejection-types.md   # 101, 102, 103, 112 responses
│   └── style-guide.md       # Firm writing standards
└── assets/
    └── response-template.docx
```

The **SKILL.md** file contains:
- **Frontmatter**: Name and description (triggers when Claude should use it)
- **Workflow**: Step-by-step procedure
- **References**: Pointers to detailed guidance loaded only when needed

### Example Skills for Legal Practice

**Office Action Response**
- Intake: Parse the office action, identify rejection types
- Reference Analysis: Summarize each cited reference
- Claim Mapping: Map claim elements to prior art teachings
- Response Assembly: Draft arguments using firm templates

**Legal Memorandum**
- Issue Identification: Parse the question presented
- Research: Query relevant databases
- Analysis: Apply CREAC structure
- Drafting: Follow firm style guide

**Citation Verification**
- Extract all citations from draft
- Verify quotes appear verbatim in source
- Flag discrepancies with specific locations
- Produce verification spreadsheet

### The Recursive Loop

Here's where the magic happens: **Claude can edit its own Skills.**

The workflow:
1. Ask Claude to do a task
2. Correct it as you go
3. When you're happy, say "update the skill based on what you learned"
4. Claude edits the SKILL.md to incorporate your corrections

Your institutional knowledge compounds. Every correction becomes permanent. The AI gets better at being your firm.

---

## Tool Libraries: Querying External Data

Skills tell Claude *how* to do things. Tool libraries give Claude *access* to things.

These are Python packages that let Claude query external data sources. I've built clients for:

- **USPTO & EPO**: Patent applications, prosecution history, assignments
- **CourtListener**: Federal court dockets and opinions
- **SEC EDGAR**: Company filings, exhibits, ownership reports
- **Federal Register**: Proposed rules, final rules, notices
- **USC & CFR**: Statutory and regulatory text

When I say "pull the prosecution history for application 16/123,456," Claude writes Python code like:

```python
from law_tools.uspto import get_prosecution_history
history = get_prosecution_history("16/123,456")
```

It executes the code, gets the results, and synthesizes them—no manual navigation.

### Why This Matters

Traditional legal AI (Harvey, CoCounsel) is a black box. You pay for access to their system. They decide what data sources to include.

With Claude Code + tool libraries, **you control the stack**. You decide which databases to query. You see exactly what code runs. You can extend it when you need new sources.

---

## Plugin Frameworks: Extending Capabilities

Beyond individual tool libraries, Claude Code supports plugin architectures that bundle multiple capabilities together.

### What Plugins Provide

- **Document processing**: Read and write Word, PowerPoint, PDF
- **Browser automation**: Navigate websites, fill forms, extract data
- **Specialized workflows**: Citation checking, contract analysis, regulatory tracking

### Example: The law-tools Plugin

```
law-tools/
├── servers/
│   └── python/
│       └── reference_mcp/      # Data connectors
│           ├── uspto.py        # Patent data
│           ├── courtlistener.py # Case law
│           ├── sec_edgar.py    # SEC filings
│           └── federal_register.py
└── skills/
    └── legal/
        ├── research/           # Research workflows
        ├── writing/            # Drafting skills
        └── bluebook/           # Citation format
```

The plugin bundles:
1. **Data connectors** for querying legal databases
2. **Skills** for legal workflows (research, drafting, citation)
3. **Reference materials** (Bluebook rules, style guides)

When you install the plugin, Claude gains all these capabilities at once.

---

## Getting Started: The First Hour

### Installation
```bash
npm install -g @anthropic-ai/claude-code
claude
```

### First Session
1. Navigate to a folder with some documents
2. Ask Claude to summarize them
3. Ask a follow-up question that requires synthesis
4. Watch it search, read, and respond

### First CLAUDE.md
Create `~/.claude/CLAUDE.md` with basic preferences:
```markdown
# My Preferences

## Writing Style
- Plain English, no legalese
- Short sentences, active voice
- Cite sources with pinpoint citations

## When I Ask for Research
- Start by checking if I have existing memos on the topic
- Note any jurisdictional limitations
- Flag areas of uncertainty
```

### First Skill
After Claude does something well, say:
> "That worked great. Can you create a skill that captures this workflow so you do it the same way next time?"

Claude will create a SKILL.md file you can refine over time.

---

## Confidentiality: The Essential Caveat

**I only use these tools for non-confidential matters.**

- Public patent prosecution
- Published court filings
- Regulatory research
- Publicly available company information

Anything involving privileged or sensitive client information stays off cloud-based AI systems.

The good news: a surprising amount of legal work involves public records. Patent prosecution, regulatory compliance, litigation involving public filings—there's substantial leverage available without touching confidential material.

For confidential work, the same skills and workflows can eventually run on on-premise or zero-data-retention systems. The investment in learning the paradigm transfers.

---

## The Bottom Line

Claude Code isn't a chatbot. It's not another AI product to evaluate against Harvey or CoCounsel.

It's infrastructure. A platform for building exactly the AI tools your practice needs.

- **Skills** capture your institutional knowledge
- **Tool libraries** connect to your data sources
- **CLAUDE.md** remembers your preferences
- **The recursive loop** compounds your investment

The question isn't whether to learn this. It's whether to learn it now, while you're ahead of the curve, or later, when everyone else has caught up.

The NYSBA is already teaching CLEs on "agentic AI and vibe coding for lawyers." The bar is rising. The tools are here.

Roll up your sleeves.

---

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Skills Specification](https://agentskills.io)
- [NYSBA CLE: Agentic AI and Vibe Coding for Lawyers](https://nysba.org/products/agentic-ai-and-vibe-coding-for-lawyers/)
- [Anthropic: How Teams Use Claude Code](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code)
