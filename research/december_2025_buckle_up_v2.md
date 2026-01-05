# December 2025 - Buckle Up

Hey team,

Yesterday, Andrej Karpathy—former Director of AI at Tesla, OpenAI founding team member, and the guy who coined the term "vibe coding"—[posted this](https://x.com/karpathy/status/2004607146781278521):

> "I've never felt this much behind as a programmer. The profession is being dramatically refactored... I have a sense that I could be 10X more powerful if I just properly string together what has become available over the last ~year and a failure to claim the boost feels decidedly like skill issue... Clearly some powerful alien tool was handed around except it comes with no manual and everyone has to figure out how to hold it and operate it, while the resulting magnitude 9 earthquake is rocking the profession."

That post got 4.3 million views in 10 hours. It resonated because it captured something true.

If Andrej Karpathy—one of the most accomplished AI researchers alive—feels behind, what does that tell us? It tells us that what's happening right now is real, it's fast, and nobody has it fully figured out yet.

As we head into 2026, I want to share three observations about where we are.

---

## 1. AI Progress Accelerated Through 2025

You've heard me cite [METR's research](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) before—they measure how long an AI agent can work autonomously on a task. The trend has been exponential, with capability doubling roughly every 7 months since 2019.

But here's the update: **in 2024-2025, that rate accelerated to doubling every 4 months.**

To put concrete numbers on it:
- **2022 (ChatGPT launch):** 36 seconds of autonomous task completion
- **Today (GPT-5.1-Codex-Max):** 2 hours and 42 minutes

And models are consistently landing *ahead* of the predicted curve—hitting expected capability levels 1-3 months earlier than forecast.

[Epoch AI confirms this](https://epoch.ai/data-insights/ai-capabilities-progress-has-sped-up). Their Capabilities Index shows the rate of frontier improvement nearly doubled—from about 8 points/year before April 2024 to 15 points/year after. They attribute this to reasoning models and reinforcement learning breakthroughs.

If the accelerated trend holds, we should see agents capable of full-day autonomous work by late 2026, and week-long projects by 2027. If it *continues* to accelerate—which the data suggests it might—those timelines compress further.

![METR: AI task completion capability has grown exponentially, from seconds in 2020 to hours in 2025](metr_chart.png)

![Epoch AI: The rate of capability improvement nearly doubled after April 2024](epoch_ai_chart.png)

---

## 2. AI Is Now Pushing Frontiers—Not Just Passing Tests

This is the development I think most people are missing.

Yes, AI systems are acing exams. In July 2025, [Gemini with Deep Think achieved gold-medal level at the International Mathematical Olympiad](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/)—solving five of six problems perfectly, scoring 35 out of 42 points. OpenAI matched that exact score. Just one year earlier, these systems achieved silver. The year before that, they couldn't compete at all.

![DeepMind's IMO achievement: From formal mathematics with specialist systems to informal mathematics with general reasoning](deepmind_imo.png)

But here's what matters more than the medal: **AI has crossed from solving known problems to contributing to unknown frontiers.**

[AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/), DeepMind's evolutionary coding agent, discovered a new construction for the finite field Kakeya conjecture. That result was good enough to inspire **Terence Tao**—the Fields Medalist, arguably the world's greatest living mathematician—to write a new theoretical paper based on the insight.

An AI produced a result that a Fields Medalist found worthy of building upon.

[AlphaProof proved a PhD student's lemma](https://www.nature.com/articles/d41586-025-03585-5) in under a minute—a lemma the student had been stuck on for weeks. It then disproved another lemma, exposing a bug in a definition.

Google's [AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/) helped Stanford researchers identify drug candidates for liver fibrosis. At Imperial College London, researchers working on antimicrobial resistance found it produced **in days the same hypothesis their team took years to develop**.

[AlphaFold](https://deepmind.google/blog/alphafold-five-years-of-impact/), which won the Nobel Prize in Chemistry last year, now has a database of over 200 million predicted protein structures used by 3.5 million researchers worldwide.

This isn't "AI getting better at tests." This is AI beginning to do real research. And if it can contribute novel insights to mathematics, drug discovery, and protein science, it can contribute novel insights to legal analysis. The question isn't *whether*—it's *when* and *how well*.

---

## 3. You Can Access This Now Through Coding Agents

Here's the practical part.

The most capable AI systems available today aren't ChatGPT-style chatbots. They're **coding agents**—tools originally built for software developers that turn out to be useful for far more than coding.

I've been using [Claude Code](https://claude.ai/claude-code), Anthropic's command-line agent powered by Opus 4.5. It's what Karpathy was talking about when he mentioned "agents, subagents, their prompts, contexts, memory, modes, permissions, tools, plugins, skills, hooks, MCP, LSP, slash commands, workflows, IDE integrations."

Why coding agents? Because coders have been the early adopters, the guinea pigs. They've pushed these tools harder and faster than any other profession. The result is that coding agents can:

- **Hold context across extended work sessions.** Unlike chatbots that forget what you discussed, these agents remember yesterday's conversation and build on it today.
- **Work with files and documents.** They read, analyze, and produce actual artifacts—not just chat responses.
- **Execute multi-step workflows.** Research a question, synthesize findings, draft a memo, refine based on feedback—in one session.
- **Use tools.** Search databases, browse the web, run calculations, interact with APIs.

For legal work specifically: I've used Claude Code to research complex regulatory questions, produce memo-quality analysis, automate document generation that reasons about edge cases, and manage multi-file projects with consistency across documents.

### What This Looks Like in Practice

A caveat first: **I only use these tools for non-confidential matters**—public patent prosecution, published court filings, regulatory research. Anything involving privileged or sensitive client information stays off cloud-based AI systems. That said, a surprising amount of legal work involves public records, and that's where these tools shine.

Two concepts from the coding world translate directly to legal practice: **Skills** and **tool libraries**.

**Skills** are reusable workflow templates—institutional knowledge captured in a format the AI can follow. I've built skills for USPTO Office Action responses that walk through intake, reference analysis, claim mapping, and response assembly. I have skills for legal memoranda that encode the CREAC structure as a repeatable process. I have patent prosecution workflows for analyzing file histories and verifying priority chains, and citation verification routines that check whether quotes actually appear in cited sources.

When I ask Claude Code to draft an office action response, it doesn't start from scratch. It loads the skill, follows the workflow, and produces consistent output.

**Tool libraries** are Python packages that let the agent query external data sources. I've built clients that pull patent applications and prosecution history from USPTO and EPO, federal court dockets and opinions from CourtListener, company filings from SEC EDGAR, proposed rules from the Federal Register, and statutory text from USC and CFR.

The agent writes and runs Python code to query these APIs. When I say "pull the prosecution history for application 16/123,456," it generates a few lines of code, executes them, and synthesizes the results—no manual website navigation or copy-pasting.

This isn't theoretical. This is my actual workflow for non-confidential research and drafting. The tools exist now; they just require some setup and experimentation.

The [ABA's 2025 report](https://www.americanbar.org/groups/law_practice/resources/law-technology-today/2025/the-legal-industry-report-2025/) shows AI use among legal professionals increased 315% from 2023 to 2024. But most implementations are still incremental—faster document review, quicker research. The firms seeing transformative results are the ones who've rethought workflows from first principles.

**My suggestion:** Install Claude Code this week. Spend an hour with it. Don't try to accomplish anything specific—just explore what it can do. Build intuition for where it's strong and where it's weak. The learning curve is real, but so is the capability.

---

## Looking Ahead to 2026

Based on the trend data, I expect 2026 to bring:

- **Agents capable of 4-6 hour autonomous work sessions** becoming standard
- **AI-native legal practices**—firms built from the ground up around AI workflows—winning significant market share
- **Serious pressure on the billable hour model** as productivity gains make time-based billing increasingly absurd
- **Stricter enforcement of "technological competence"** requirements by bar associations

The [Takeoff Speeds model](https://www.lesswrong.com/posts/jLEcddwp4RBTpPHHq/takeoff-speeds-update-crunch-time-1), updated with recent data, now predicts AI capable of full economic automation around 2030—a decade earlier than previous estimates. Whether that's good or bad depends largely on how we prepare.

Preparation starts with awareness. And awareness starts with actually using the tools.

Buckle up. 2026 is going to be a ride.

— Parker

---

**Sources:**

*AI Progress:*
- [METR: Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)
- [Epoch AI: AI Capabilities Progress Has Sped Up](https://epoch.ai/data-insights/ai-capabilities-progress-has-sped-up)

*AI Research Breakthroughs:*
- [Gemini Deep Think Achieves IMO Gold Medal](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/)
- [AlphaEvolve: Evolutionary Coding Agent](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
- [Nature: Mathematicians Put AlphaProof to the Test](https://www.nature.com/articles/d41586-025-03585-5)
- [Google: AI Co-Scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- [AlphaFold: Five Years of Impact](https://deepmind.google/blog/alphafold-five-years-of-impact/)

*Legal Profession:*
- [American Bar Association: The Legal Industry Report 2025](https://www.americanbar.org/groups/law_practice/resources/law-technology-today/2025/the-legal-industry-report-2025/)

*Other:*
- [Karpathy on X (Dec 26, 2025)](https://x.com/karpathy/status/2004607146781278521)
- [LessWrong: Takeoff Speeds Update](https://www.lesswrong.com/posts/jLEcddwp4RBTpPHHq/takeoff-speeds-update-crunch-time-1)
