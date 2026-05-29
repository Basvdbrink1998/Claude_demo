# Forensic Intelligence Workshop — Storyline

## The Scenario

A financial crimes unit has received a whistleblower tip about irregular payments at a major US energy company. The tip is vague: *"money is moving in circles, and not all of it is what it looks like."*

You have been handed three data sources pulled from the company's systems:

- A **transaction export** covering 1999–2001
- **Internal emails** from executives and staff mentioning key entities
- A **summary of entity mentions** extracted from thousands of internal messages
- A **reference table** cross-referencing company names against the ICIJ Offshore Leaks database

None of the sources alone is conclusive. Your job is to connect them.

---

## The Data

| File | What it contains |
|------|-----------------|
| `data/structured/transactions.csv` | 2,000 wire transfers between Enron Corp, its executives, shell entities, and legitimate counterparties (1999–2001) |
| `data/structured/accounts.json` | Metadata for all 27 accounts in the transaction data: names, types, jurisdictions, opening dates |
| `data/structured/extracted_entities.csv` | 33 named entities (executives and special purpose vehicles) extracted from the Enron email corpus, with email frequency and sample context |
| `data/unstructured/emails/` | 100 real Enron emails mentioning key SPEs and individuals, organised by mailbox owner |
| `data/reference/icij_bridge.csv` | 371 matches between Enron entity names and records in the ICIJ Offshore Leaks database (Panama Papers, Paradise Papers, Pandora Papers, and others) |

The transaction data contains real Enron entity names and four embedded forensic patterns — hidden in a background of ~1,900 legitimate energy business transactions. Finding them is the goal of Step 1.

---

## Step 0 — Environment Setup

### How to run it

1. Clone this repo and open it in [Claude Code](https://claude.ai/code)
2. Copy the prompt below into the Claude Code chat and hit enter — Claude will install the
   required skills directly from the terminal

---

### Step 0 Prompt

```
Before we start, please set up my Claude Code environment by running the following commands:

claude plugins install frontend-design
claude plugins install playwright
npx antigravity-awesome-skills --claude
git clone https://github.com/coleam00/excalidraw-diagram-skill .claude/plugins/marketplaces/claude-plugins-official/external_plugins/excalidraw-diagram

These give us better UI generation, browser automation for testing the dashboard,
a large library of specialist skills, and architecture diagram generation.
```

---

*Continue to Step 1: Data Analysis →*

## Step 1 — Data Analysis with Claude

### How to run it

1. Clone this repo and open it in [Claude Code](https://claude.ai/code)
2. Copy the prompt below into the Claude Code chat and hit enter — Claude will read the files directly from the repo

---

### Step 1 Prompt

```
I'm investigating potential financial fraud at an energy company. The data is in the following files:

- data/structured/transactions.csv
- data/structured/accounts.json
- data/structured/extracted_entities.csv
- data/unstructured/emails/
- data/reference/icij_bridge.csv

Can you go through these and flag anything that looks suspicious? I'm particularly interested in unusual payment patterns and any links to offshore entities.
```

---

## Step 2 — Corporate Intelligence

### How to run it

1. Continue in the same Claude Code session from Step 1
2. Copy the prompt below into the chat and hit enter — Claude will search public registries,
   news archives, and OSINT databases directly from the web

---

### Step 2 Prompt

```
Based on what you just found, I want to dig deeper into the entities and individuals
that stood out. Before I go further I want to know more about who they actually are
in the real world.

For each flagged entity or person, can you search the web and find:
- Any company registration details (jurisdiction, incorporation date, registered agents)
- Names of directors, officers, or beneficial owners on public record
- Any appearances on sanctions lists, PEP databases, or regulatory watchlists
- Any news coverage linking them to litigation, enforcement actions, or fraud findings

Pull it together at the end — who sits at the centre of this network, and what does
the public record say about them?
```

---

## Step 3 — Investigation Dashboard

### How to run it

1. Continue in the same Claude Code session
2. Copy the prompt below into the chat and hit enter — Claude will scaffold and build a
   working web app directly in the repo

---

### Step 3 Prompt

```
Now I want to turn this investigation into something I can actually use day to day.

Build me a simple web dashboard for exploring the data we've been analysing. It should have:
- A search box where I can type an entity or person name and see related accounts and transactions
- A network graph showing how the entities connect to each other
- A transaction timeline for any selected entity, with dates on the x-axis and amounts on the y-axis

Use whatever stack makes sense — a FastAPI backend serving the data from the files in this
repo, with a single-page frontend to display everything.
```

---

### Follow-up prompts

Once the app is running, try these to extend it iteratively:

```
Add a sidebar that lists all transactions for the selected node, sorted by date,
with amounts colour-coded: green for inbound, red for outbound.
```

```
Add vertical reference lines on the timeline for key Enron events:
2001-08-14 (Skilling resignation), 2001-10-16 (earnings restatement),
2001-12-02 (bankruptcy filing).
```

```
Add a flag button on each node so I can mark entities as Suspicious, Verified, or
Needs Review. Save the flags to a local JSON file so they persist between sessions.
```
