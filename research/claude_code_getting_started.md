# Claude Code: Getting Started Guide

**A Gentle Introduction for Lawyers**

---

## What You'll Need

- A Mac or Windows computer
- About 30 minutes for initial setup
- An Anthropic account ($20/month for Claude Pro, which includes Claude Code access)

We'll install three things: Node.js (runs Claude Code), Python (runs the legal research tools), and Claude Code itself. Don't worry if you've never used a "command line" before—this guide assumes you haven't.

---

## Part 1: Understanding the Basics

### What's a Command Line?

Your computer has two ways to interact with it:

1. **The visual way** — clicking icons, dragging files, using menus (what you're used to)
2. **The text way** — typing commands in a window (the command line)

The command line looks like a blank window where you type instructions. It might seem old-fashioned, but it's actually more powerful for certain tasks—like talking to AI.

Claude Code runs in the command line. You'll type requests, and it types back. Simple as that.

### Why the Command Line?

Browser-based AI (ChatGPT, Claude.ai) is sandboxed—it can't see your files or do things on your computer.

Command-line AI can. That's why Claude Code can:
- Read documents in your folders without uploading them
- Create and edit files directly
- Run searches across your entire project
- Remember context across sessions

---

## Part 2: Installation

### Step 1: Open the Terminal

**On Mac:**
- Press `Command + Space` to open Spotlight
- Type "Terminal" and press Enter
- A window with a text prompt appears—that's the command line

**On Windows:**
- Press `Windows + R`
- Type "cmd" and press Enter
- Or search for "Command Prompt" in the Start menu

### Step 2: Install Node.js

Claude Code requires a program called Node.js. Think of it as the engine that runs Claude Code.

Go to [nodejs.org](https://nodejs.org) and download the "LTS" version (the one that says "Recommended for Most Users"). Run the installer like any other program.

To verify it worked, type this in your terminal and press Enter:
```
node --version
```

You should see a version number like `v20.10.0`. If you see an error, the installation didn't complete—try restarting your terminal.

### Step 3: Install Python

Python is what powers the legal research tools—the connectors that query USPTO, CourtListener, SEC EDGAR, and other databases. Without Python, Claude Code still works, but it won't be able to pull live data from these sources.

**On Mac:**

Mac comes with an older Python, but we need a current version. The easiest approach:

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow "Download Python 3.12.x" button
3. Run the installer, accepting the defaults
4. **Important:** On the first installer screen, check the box that says "Add Python to PATH"

To verify it worked:
```
python3 --version
```

You should see `Python 3.12.x` or similar.

**On Windows:**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow "Download Python 3.12.x" button
3. Run the installer
4. **Critical:** On the first screen, check the box at the bottom that says **"Add python.exe to PATH"** before clicking Install
5. Click "Install Now"

To verify it worked, open a **new** Command Prompt window and type:
```
python --version
```

You should see `Python 3.12.x` or similar. If you see an error about Python not being found, the PATH wasn't set correctly—run the installer again and make sure to check that box.

**Why "Add to PATH" matters:** This lets your terminal find Python when Claude Code needs it. Skip this step, and the legal research tools won't work.

### Step 4: Install Claude Code

In your terminal, type:
```
npm install -g @anthropic-ai/claude-code
```

This tells your computer to download Claude Code and make it available everywhere. It may take a minute.

### Step 5: Start Claude Code

Type:
```
claude
```

The first time, it will ask you to log in to your Anthropic account. Follow the prompts—it will open a browser window for authentication.

Once logged in, you'll see a prompt waiting for your input. You're in.

---

## Part 3: Your First Session

### Navigating to a Folder

Claude Code works best when you point it at a specific folder of documents.

Before starting Claude, navigate to that folder in your terminal:

**On Mac:**
```
cd ~/Documents/SomeCase
```

**On Windows:**
```
cd C:\Users\YourName\Documents\SomeCase
```

The `cd` command means "change directory"—it's how you move around in the command line.

**Tip:** You can also drag a folder onto the terminal window to paste its path automatically.

### Asking Your First Question

Once Claude is running and you're in a folder with some documents, just type naturally:

```
What documents are in this folder?
```

Claude will list them. Then try:

```
Summarize the main arguments in the motion to dismiss.
```

Claude will find the relevant file, read it, and give you a summary.

### Watching It Work

You'll notice Claude shows you what it's doing:
- "Reading complaint.pdf..."
- "Searching for references to statute of limitations..."
- "Found 3 relevant sections..."

This transparency is intentional. You can see its reasoning, which helps you verify the output.

---

## Part 4: The Memory System

### What Claude Remembers (And Doesn't)

By default, Claude remembers everything within a session. Close the window, and it forgets.

But you can give Claude persistent memory using simple text files called "CLAUDE.md" files.

### Creating Your First Memory File

In your home folder, create a file called `CLAUDE.md` (in a hidden folder called `.claude`):

**The easy way:** Ask Claude to do it for you:
```
Create a CLAUDE.md file that remembers I prefer plain English, short sentences, and Bluebook citations.
```

Claude will create the file. From now on, every session starts by reading that file.

### What to Put in Memory Files

Think of it as onboarding a new associate—except you only do it once:

- **Writing style:** "Use plain English. Avoid legalese. Keep sentences short."
- **Citation format:** "Use Bluebook format for all citations."
- **Standard procedures:** "When I ask for research, start by checking if I have existing memos on the topic."
- **Preferences:** "Always include a one-paragraph executive summary at the top of memos."

### Project-Specific Memory

You can also create a `CLAUDE.md` file inside a specific project folder. Claude reads both:

1. Your global preferences (applies everywhere)
2. Project-specific context (applies only to this matter)

For example, a case folder might have:
```
This matter involves Client X v. Defendant Y.
Key dates: Complaint filed Jan 15, 2025. Answer due Feb 14, 2025.
Relevant jurisdiction: N.D. Cal.
Our theory of the case: ...
```

Claude reads this automatically when you work in that folder.

---

## Part 5: Skills — Teaching Claude Your Workflows

### What's a Skill?

A Skill is a text file that teaches Claude how to do a specific task your way. Think of it as a checklist or procedure manual that Claude follows.

### Creating Your First Skill

After Claude does something well, say:

```
That worked great. Can you save this as a Skill so you do it the same way next time?
```

Claude will create a Skill file capturing the workflow.

### Example: Office Action Response Skill

Imagine you've walked Claude through responding to a patent office action. The Skill might capture:

1. **Intake:** Parse the office action, identify rejection types (101, 102, 103, 112)
2. **Reference analysis:** Summarize each cited prior art reference
3. **Claim mapping:** Map claim elements to prior art teachings
4. **Response drafting:** Follow firm template, address each rejection in order

Next time you say "help me respond to this office action," Claude loads the Skill and follows the same process.

### The Recursive Learning Loop

Here's where it gets powerful: Claude can edit its own Skills.

1. You use a Skill
2. You correct Claude mid-task ("No, we always address the 103 rejection before the 102")
3. You say "Update the Skill with what you learned"
4. Claude edits the Skill file to incorporate your correction

Your institutional knowledge compounds. Every correction becomes permanent.

---

## Part 6: Installing the Legal Research Tools

This is where Python comes in. We've built a plugin called `law-tools` that gives Claude Code direct access to legal databases. Once installed, you can ask Claude to pull data from these sources, and it will query them directly.

### What's Included

The law-tools plugin connects to 18 data sources:

**Patent Data:** USPTO applications and prosecution history, USPTO publications, EPO, Google Patents, Japan Patent Office

**Litigation Data:** CourtListener (federal court dockets and opinions), Federal Rules of Civil/Criminal Procedure, USITC

**Regulatory Data:** Federal Register, SEC EDGAR, MPEP, U.S. Code, CFR, state statutes

**Legislative Data:** LegiScan (all 50 states), Texas Legislature

Many of these work without any API keys. Some (like USPTO's detailed application data) require free registration.

### Installing the Plugin

Inside Claude Code, type:
```
/plugin marketplace add SanctionedCodeList/law_tools
```

Then:
```
/plugin install law-tools@SanctionedCodeList
```

Claude will download the plugin. When it finishes, type `exit` to quit, then start Claude Code again with `claude`. The plugin activates on restart.

### Using It

Once installed, just describe what you need:

> "Search for Tesla's battery patents from 2023"

> "Pull the prosecution history for application 16/123,456"

> "Find recent Federal Register notices about AI regulation"

> "What does FRCP Rule 26 say about discovery scope?"

Claude automatically uses the right data source and returns the results.

### Optional: API Keys for More Access

Some data sources work better (or only work) with API keys. These are free to obtain:

| Service | Get a key at | What it unlocks |
|---------|--------------|-----------------|
| USPTO ODP | [developer.uspto.gov](https://developer.uspto.gov) | Full application data, prosecution history |
| EPO OPS | [developers.epo.org](https://developers.epo.org) | European patent data |
| CourtListener | [courtlistener.com](https://www.courtlistener.com) | Higher rate limits |

To add a key, create a file called `.env` in your home folder with:
```
USPTO_ODP_API_KEY=your-key-here
```

But start without keys—many features work fine without them.

---

## Part 7: Tips for Success

### Start Small
Don't try to revolutionize your practice on day one. Pick one small, non-confidential task and see how Claude handles it.

### Be Specific
"Research the statute of limitations for breach of contract in California" works better than "tell me about statutes of limitations."

### Correct It
When Claude gets something wrong, tell it specifically what was wrong and what you wanted instead. This is training data for your future Skills.

### Trust But Verify
Claude is powerful but not infallible. Verify citations, check quotes against sources, review reasoning. This is still a tool that augments your judgment—it doesn't replace it.

### Non-Confidential Only
Until your firm has approved specific AI tools for confidential work, stick to public filings, published opinions, regulatory materials, and other non-privileged information.

---

## Quick Reference

| To do this... | Type this... |
|--------------|--------------|
| Start Claude | `claude` |
| Go to a folder | `cd /path/to/folder` |
| Ask a question | Just type naturally |
| Exit Claude | `exit` or press `Ctrl+C` |
| Create a memory file | "Create a CLAUDE.md with my preferences" |
| Save a workflow | "Save this as a Skill" |
| Update a Skill | "Update the Skill with what you learned" |
| Add legal research tools | `/plugin marketplace add SanctionedCodeList/law_tools` |
| Install a plugin | `/plugin install law-tools@SanctionedCodeList` |

---

## Getting Help

**Within Claude:** Just ask. "How do I create a memory file?" or "What Skills do I have available?"

**Anthropic Documentation:** [docs.anthropic.com/claude-code](https://docs.anthropic.com/claude-code)

**From me:** Happy to walk through any of this in person. The learning curve is real, but so is the payoff.

---

## Next Steps

1. Install Node.js, Python, and Claude Code (20 minutes)
2. Start Claude Code and log in
3. Install the legal research plugin (Part 6)
4. Point Claude at a folder of non-confidential documents
5. Ask it to summarize something
6. Try a live query: "What does FRCP Rule 12(b)(6) say?"
7. Create a simple CLAUDE.md with your preferences

That's your first hour. After that, you'll have a feel for what it can do—and ideas for what to try next.
