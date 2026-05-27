# Forensic Intelligence Workshop — Storyline

## The Scenario

A financial crimes unit has received a whistleblower tip about irregular payments at a major US energy company. The tip is vague: *"money is moving in circles, and not all of it is what it looks like."*

You have been handed three data sources pulled from the company's systems:

- A **transaction export** covering 1999–2001
- A **corporate email archive** with entity mentions extracted from thousands of internal messages
- A **reference table** cross-referencing company names against the ICIJ Offshore Leaks database

None of the sources alone is conclusive. Your job is to connect them.

---

## The Data

| File | What it contains |
|------|-----------------|
| `data/structured/transactions.csv` | 2,000 wire transfers between Enron Corp, its executives, shell entities, and legitimate counterparties (1999–2001) |
| `data/structured/accounts.json` | Metadata for all 27 accounts in the transaction data: names, types, jurisdictions, opening dates |
| `data/structured/extracted_entities.csv` | 33 named entities (executives and special purpose vehicles) extracted from the Enron email corpus, with email frequency and sample context |
| `data/reference/icij_bridge.csv` | 371 matches between Enron entity names and records in the ICIJ Offshore Leaks database (Panama Papers, Paradise Papers, Pandora Papers, and others) |

The transaction data contains real Enron entity names and four embedded forensic patterns — hidden in a background of ~1,900 legitimate energy business transactions. Finding them is the goal of Step 1.

---

## Step 1 — Data Analysis with Claude

### What you're trying to find

- Payments that are suspiciously close to a regulatory reporting threshold
- A company that receives money, passes it on, and sends it back — disguised as an investment return
- Recurring payments to offshore entities described as "consulting" or "advisory" fees
- A single very large payment made just before a major corporate event

### How to run it

1. Open [claude.ai](https://claude.ai) or your Claude environment
2. Attach the following files:
   - `data/structured/transactions.csv`
   - `data/structured/accounts.json`
   - `data/structured/extracted_entities.csv`
   - `data/reference/icij_bridge.csv`
3. Send the prompt below

---

### Step 1 Prompt

```
I'm investigating potential financial fraud at an energy company. The data is in the following files:

- data/structured/transactions.csv
- data/structured/accounts.json
- data/structured/extracted_entities.csv
- data/reference/icij_bridge.csv

Can you go through these and flag anything that looks suspicious? I'm particularly interested in unusual payment patterns and any links to offshore entities.
```

---

*Continue to Step 2: Corporate Intelligence →*
