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
| `data/unstructured/emails/` | 100 real Enron emails, organised by mailbox subfolder (e.g. `emails/fastow/1`) — files have no extension |
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

### Expected output (Step 1)

A good Claude response will flag **four patterns** in the data:

1. **Structuring** — 14 payments to Chewco Investments L.P., all between $9,400–$9,999, described as "Management consulting fees". An email from Fastow explicitly instructs keeping wires "under the threshold".
2. **Round-trip transactions** — Money flows Enron → LJM Cayman → JEDI → Enron across three cycles (~$150M each). Labelled as "professional services" outbound and "investment return distributions" inbound.
3. **Southampton Place payments** — 9 escalating payments totalling ~$47M, culminating in a $26.8M single transfer on 2001-09-28 (65 days before bankruptcy).
4. **Quarter-end spikes** — 87 large transactions cluster on the last 2–3 days of each quarter ($276M total), consistent with earnings management.

If Claude finds all four, the data is working as intended.

---

## Step 2 — Corporate Intelligence

### How to run it

1. Continue in the **same** Claude Code session from Step 1 (Claude needs context from Step 1)
2. Copy the prompt below into the chat and hit enter — Claude will search public registries,
   news archives, and OSINT databases directly from the web

---

### Step 2 Prompt

```
Based on what you just found, I want to dig deeper into the entities and individuals
that stood out (in particular: LJM Cayman L.P., Chewco Investments L.P., JEDI Investments L.P.,
Andrew Fastow, and Michael Kopper). Before I go further I want to know more about who they
actually are in the real world.

For each flagged entity or person, can you search the web and find:
- Any company registration details (jurisdiction, incorporation date, registered agents)
- Names of directors, officers, or beneficial owners on public record
- Any appearances on sanctions lists, PEP databases, or regulatory watchlists
- Any news coverage linking them to litigation, enforcement actions, or fraud findings

Pull it together at the end — who sits at the centre of this network, and what does
the public record say about them?
```

---

### Expected output (Step 2)

A good Claude response will surface:

- **Andrew Fastow** at the centre — CFO who created and secretly controlled LJM, Chewco, and JEDI. Pleaded guilty 2004, sentenced to 6 years, forfeited $23.8M.
- **Michael Kopper** — nominee manager of Chewco, received $1.5M in undisclosed management fees. First Enron executive to plead guilty; disgorged $12M.
- **LJM Cayman L.P.** — Cayman Islands incorporation, named after Fastow's wife and sons. Used to absorb Enron's poorly performing assets off-balance-sheet.
- **Chewco** — failed the 3% independent equity rule; concealed $600M in debt, inflated earnings by ~$400M.
- **JEDI** — the CalPERS joint venture used as a money-circulation vehicle.

If Claude cites DOJ, SEC, or Wikipedia sources and identifies Fastow as the central figure, the step is working as intended.

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

Use the @frontend-design skill for the UI and @excalidraw-diagram to sketch the architecture
first. Build me a simple web dashboard for exploring the data we've been analysing. It should have:
- A search box where I can type an entity or person name and see related accounts and transactions
- A network graph showing how the entities connect to each other
- A transaction timeline for any selected entity, with dates on the x-axis and amounts on the y-axis

Use whatever stack makes sense — a FastAPI backend serving the data from the files in this
repo, with a single-page frontend to display everything. Once it's running, use @playwright
to write a quick smoke test that loads the dashboard and searches for an entity.
```

> **Note for facilitators:** A working dashboard already exists in the `dashboard/` folder of this repo. Claude will find it and confirm it runs rather than building from scratch. If you want the full vibe-coding experience, delete the `dashboard/` folder before running this step so Claude builds it live. Either way, the follow-up prompts below produce genuine new features.

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

```
Add a second API endpoint that reads data/reference/icij_bridge.csv and overlays
ICIJ Offshore Leaks matches on the network graph — show the number of ICIJ hits
as a badge on each node, and colour nodes red if any match is in a high-secrecy
jurisdiction (KY, VG, PMA, NIUE, SEY).
```

```
Add an export button that generates a case summary: a JSON file containing the
selected entity's details, all connected entities, the full transaction list,
and any flags set. Include a timestamp and case reference number.
```
