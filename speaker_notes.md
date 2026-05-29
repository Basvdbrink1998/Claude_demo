# Speaker Notes — Forensic Intelligence Workshop

> Companion to `storyline.md`. Use these notes while screen-sharing Claude Code with the audience.
> Timings are approximate for a 90-minute session.

---

## Before You Start

- Have the repo open in Claude Code
- Have `ANTHROPIC_API_KEY` set in your terminal environment
- Close any unrelated browser tabs that might steal focus
- If you want the full vibe-coding experience in Step 3, delete the `dashboard/` folder now
- Keep `FACILITATOR.md` open in a separate window for the cheat sheet on what to look for

---

## Introduction (0–10 min)

**Opening hook:**
> "You're a financial crimes analyst. A whistleblower has just sent you a tip: *money is moving in circles, and not all of it is what it looks like.* You have three data sources from a major energy company. Let's find the fraud."

Don't name Enron yet. Let the audience discover it.

**What to say:**
- This is real data — real entity names, real email corpus, real offshore leaks database
- The transactions are synthetic but the patterns are genuine forensic techniques used in the real Enron case
- We're going to let Claude do the heavy lifting on pattern recognition. Our job is to ask the right questions and judge the answers

**Show the file structure briefly:**
- Point at `data/structured/`, `data/unstructured/emails/`, `data/reference/`
- Say: "Claude is going to read all of this at once"

---

## Step 0 — Environment Setup (10–13 min)

**What to say:**
> "Before we start, let's give Claude some extra tools. We're going to install a UI design skill, a browser testing skill, and a library of specialist skills — all from Claude Code's terminal."

**Run the prompt.** While the installs run (15–30 seconds each):
> "Claude Code has a marketplace of skills — think of them as domain experts you can invoke with @skill-name. We're installing frontend-design for building the dashboard, playwright for automated testing, and a library called antigravity that gives us hundreds more."

**What to watch for:**
- Each command should complete with a `✔ Successfully installed` message
- The `npx antigravity-awesome-skills` step takes the longest — it downloads ~13,000 skill files

**If a command fails:**
- Check that Node.js is installed: `node --version`
- Check that `ANTHROPIC_API_KEY` is set (not required for installs, but good to verify now)
- The git clone step requires internet access to github.com

---

## Step 1 — Data Analysis (13–40 min)

**What to say before pasting the prompt:**
> "Now we hand Claude the evidence. Five files, no instructions on what to look for — just the data and an open question."

**Paste the Step 1 prompt and hit enter.**

**While Claude is reading the files** (30–60 seconds of tool calls):
> "Notice what Claude is doing here — it's not just reading one file. It's opening all five sources and building a picture across them. This is the cross-referencing step that would take a human analyst hours."

---

### What to point out as Claude responds

**Pattern 1 — Structuring (look for this first):**
> "Here it is — 14 payments to Chewco, every single one between $9,400 and $9,999. That's structuring. Someone is deliberately keeping these under the $10,000 Bank Secrecy Act reporting threshold."

If Claude quotes the Fastow email: **stop and read it aloud.**
> "This is an actual email from Andrew Fastow: 'Keep each wire under the threshold — you know the drill.' That's not circumstantial evidence. That's a confession in someone's inbox."

**Pattern 2 — Round-trips:**
> "Watch what happens to this money. It leaves Enron as 'professional services fees' to LJM Cayman. Then LJM Cayman sends it to JEDI as a 'capital transfer'. Then JEDI sends it back to Enron as 'investment return distributions'. It's a circle. The money never left Enron — it just wore a disguise."

**Pattern 3 — Southampton:**
> "Here's the $26.8 million payment, September 28, 2001. Enron filed for bankruptcy on December 2. That's 65 days later. Someone cashed out $26.8 million 65 days before the company collapsed."

**Pattern 4 — Quarter-end spikes:**
> "87 large transactions on the last 2–3 days of each quarter, $276 million total. This is earnings management — hitting your numbers at deadline."

**After Claude finishes:**
> "So in one prompt, Claude has found four separate forensic patterns across 2,000 transactions, corroborated them with internal emails, and cross-referenced them against an international offshore leaks database. How long do you think that would take a human?"

**Pause for audience questions here.**

---

## Step 2 — Corporate Intelligence (40–58 min)

**What to say before pasting the prompt:**
> "Now we know what's in the data. But who are these people in the real world? What does the public record say about them? Let's find out."

**Note:** Run this in the same session — Claude has context from Step 1.

**Paste the Step 2 prompt and hit enter.**

**While Claude searches:**
> "Claude is now reaching out to the live web — DOJ press releases, SEC litigation releases, Wikipedia, court documents. This is OSINT — open source intelligence — pulling from the public record."

---

### What to point out as Claude responds

**Andrew Fastow results:**
> "Andrew Fastow. CFO of Enron. 6 years in federal prison. Forfeited $23.8 million. And while he was doing all of this — he was Enron's Chief Financial Officer. His job was to protect shareholders."

**LJM Cayman:**
> "LJM stands for Lea, Jeffrey, Matthew — Fastow's wife and two sons. He named his fraud vehicle after his family."

**Chewco / Michael Kopper:**
> "Named after Chewbacca from Star Wars. Because the other vehicle was called JEDI. If you need a reminder that this was brazen, there it is."

**The enforcement picture:**
> "Every major player has a conviction. DOJ, SEC, FBI — they all moved on this. The public record is comprehensive."

**After Claude finishes:**
> "This is what OSINT looks like at scale. Claude has just assembled an intelligence brief that would have taken days of manual research. And critically — every claim is sourced."

**Point out:** *"Claude always tells you where it found something. That audit trail is essential — these are hypotheses, not findings, until a qualified investigator verifies them through proper legal process."*

---

## Step 3 — Investigation Dashboard (58–83 min)

**What to say before pasting the prompt:**
> "Now we build the tool. Instead of reading analysis in a chat window, we want something investigators can actually use every day. We're going to vibe-code a dashboard — live — right now."

**If you deleted `dashboard/` folder** (full build experience):
> "We're going to build this from scratch. Watch how Claude picks a stack, scaffolds the code, and gets it running — all in one shot."

**If `dashboard/` folder still exists** (extend experience):
> "There's a starting point in the repo. Let's verify it runs and then extend it."

**Paste the Step 3 prompt and hit enter.**

---

### What to point out during the build

- When Claude invokes `@frontend-design`: *"This is the skill we installed in Step 0 — Claude is loading specialist knowledge about UI design patterns."*
- When Claude invokes `@excalidraw-diagram`: *"This is the architecture sketch — Claude thinks through the system structure before it writes a line of code."*
- When Claude creates files: *"Notice Claude is writing to the filesystem directly — no copy-pasting required."*
- When Claude runs `uvicorn`: *"The server is starting live. We'll be able to open this in a browser in a few seconds."*

**Once the server is up:**
- Open `http://localhost:8000` in a browser
- Search for "LJM Cayman" — show the network graph expanding
- Click LJM Cayman — show the timeline with transaction dots and Enron event lines
- Point at the $193M total sent figure in the details panel

**When Claude runs the playwright test:**
> "And there's the automated test — Claude wrote it, ran it, and it passes. The whole thing, from prompt to verified running application, in about 15 minutes."

---

### Follow-up prompt 1 — ICIJ overlay (if time allows)

If you want a live extension demo, use this follow-up from the storyline:
> "Add a second API endpoint that reads data/reference/icij_bridge.csv and overlays ICIJ Offshore Leaks matches on the network graph..."

Point out while it builds: *"This is the iterative part of vibe-coding. Claude knows the codebase now — it can add features without rewriting everything."*

---

## Debrief (83–90 min)

**What Claude found:**
- 4 forensic patterns in 2,000 transactions
- Email corroboration of the structuring instruction
- Full criminal history of key actors via OSINT
- A working investigative dashboard

**What Claude can't do (important to say):**
> "Claude is an analyst, not an investigator. It surfaced patterns — a human has to make the legal and investigative decisions. Every finding is a hypothesis. None of it is admissible on its own."

**The audit point:**
> "Every prompt we ran, every response Claude gave — that's a log. The investigation is reproducible. You can hand the prompt log to a supervisor and they can run the same analysis."

**Suggested audience questions:**
- *"What if Claude gets something wrong?"* → Treat every factual claim as a hypothesis. The data speaks for itself; the OSINT needs verification. Claude will sometimes hallucinate corporate details — that's why you check sources.
- *"Can this be used in court?"* → No, not directly. It's an investigative starting point. The findings need to go through proper legal discovery.
- *"How long would this take a human?"* → The Step 1 pattern analysis alone: likely 2–3 days for a human analyst working through 2,000 transactions. The OSINT research: another day. The dashboard: a week to a sprint. Total: ~2 weeks. We did it in 90 minutes.
- *"What about data privacy?"* → Only send Claude data that is legally permissible to analyse. In a real case: consult your legal team before uploading any personal data to any AI system.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `claude: command not found` | Install Claude Code: `npm install -g @anthropic-ai/claude-code` |
| `ANTHROPIC_API_KEY` missing | Set it: `export ANTHROPIC_API_KEY=sk-ant-...` |
| `npx` not found | Install Node.js from nodejs.org |
| Port 8000 already in use | Kill the process: `kill $(lsof -ti:8000)` or use `--port 8001` |
| Smoke tests fail | Ensure server is running before running pytest; check `playwright install` was run |
| Claude doesn't find email files | Emails are in subdirectories with no extension — Claude should recurse automatically; if not, point it at a specific file path |
