# Step 1 — Data Analysis: Dry Run Results

**Date:** 2026-05-29
**Prompt used:** As written in `storyline.md` Step 1

---

## Prompt Sent

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

## Simulated Claude Response

*The following reflects what Claude actually surfaces when analysing the data files in this repo.*

---

### Data Overview

| Source | Contents |
|--------|----------|
| `transactions.csv` | 2,000 wire transfers, 1999–2001, between 27 accounts |
| `accounts.json` | 27 accounts: 1 corporate (Enron Corp), 6 executive personal accounts, 10 shell entities (SPEs), 10 legitimate external counterparties |
| `extracted_entities.csv` | 33 named entities extracted from the Enron email corpus, with email frequency counts |
| `emails/` | 100 real Enron emails, organised by mailbox (no file extension — numbered files e.g. `fastow/1`, `fastow/2`) |
| `icij_bridge.csv` | 371 matches between Enron entity names and ICIJ Offshore Leaks records |

---

### Flagged Pattern 1 — Structuring (Chewco)

**Finding:** 14 payments from Enron Corp to **Chewco Investments L.P.** all fall just below the $10,000 reporting threshold. All are described as "Management consulting fees".

| Date | Amount | Description |
|------|--------|-------------|
| 2001-07-16 | $9,457.65 | Management consulting fees |
| 2001-07-17 | $9,485.17 | Management consulting fees |
| 2001-07-17 | $9,593.17 | Management consulting fees |
| 2001-07-23 | $9,630.63 | Management consulting fees |
| 2001-07-31 | $9,579.40 | Management consulting fees |
| … (9 more) | $9,xxx.xx | Management consulting fees |

**Why suspicious:** 14 consecutive payments to the same counterparty, each landing between $9,400–$9,999, is a textbook structuring pattern — deliberately staying below the $10,000 Bank Secrecy Act reporting threshold to avoid Currency Transaction Reports.

**Email corroboration:** A January 2001 email from Andrew Fastow (fastow/1) explicitly instructs: *"the Chewco management fee invoices for October through December need to go out this week. Keep each wire under the threshold — you know the drill."*

---

### Flagged Pattern 2 — Round-Trip Transactions (Enron → LJM → JEDI → Enron)

**Finding:** Money flows in a full circle across three entities over three cycles.

**Cycle structure:**
1. Enron Corp → LJM Cayman L.P. (labelled "Professional services" or "Restructuring advisory")
2. LJM Cayman L.P. → JEDI Investments L.P. (labelled "Partnership capital transfer")
3. JEDI Investments L.P. → Enron Corp (labelled "Investment return distribution")

| Leg | Count | Total |
|-----|-------|-------|
| Enron → LJM Cayman | 11 txns | $193,923,999 |
| LJM Cayman → JEDI | 3 txns | $155,879,000 |
| JEDI → Enron | 3 txns | $151,058,000 |

**Why suspicious:** Money leaving Enron as "professional services" returns 12–18 days later as "investment return distributions" via two intermediate entities — both of which are Enron-controlled SPEs. This is a classic round-trip designed to disguise debt as equity and inflate reported income.

**Email corroboration:** A November 2000 email from Jeff Skilling to Ken Lay (skilling/1): *"The JEDI Partners vehicle has been particularly useful in absorbing the merchant investments that we can't hold on the balance sheet… I don't see any reason to disclose the full structure in the annual report."*

---

### Flagged Pattern 3 — Southampton Place Payments

**Finding:** Enron Corp made 9 escalating payments to **Southampton Place L.P.**, culminating in a single $26.8M transfer on 2001-09-28 — 65 days before bankruptcy.

| Date | Amount |
|------|--------|
| 1999-08-17 | $304,507 |
| 2000-01-14 | $685,937 |
| 2000-01-17 | $1,000,000 |
| 2000-03-12 | $5,000,000 |
| 2000-04-13 | $7,000,000 |
| 2000-12-19 | $6,000,000 |
| 2001-04-12 | $110,860 |
| 2001-05-28 | $654,917 |
| **2001-09-28** | **$26,800,000** |

**Why suspicious:** The $26.8M figure matches the publicly documented "Southampton buyout" — a payment made to wind down an SPE that secretly enriched Fastow and Kopper. The timing (September 2001, as SEC scrutiny was mounting) is notable.

---

### Flagged Pattern 4 — Quarter-End Transaction Spikes

**Finding:** 87 transactions cluster on the last 2–3 days of each calendar quarter, with a combined value of $276.6M. The average quarter-end transaction is significantly larger than the daily average.

**Why suspicious:** Quarter-end spikes are a known indicator of "earnings management" — booking large transactions in the final hours of a reporting period to hit targets. This is especially significant given Enron's later admission of widespread earnings manipulation.

---

### ICIJ Offshore Leaks Cross-Reference

Every major SPE entity appears in the ICIJ Offshore Leaks database, with matches across multiple offshore secrecy jurisdictions:

| Entity | ICIJ Matches | Jurisdictions |
|--------|-------------|---------------|
| Marlin | 117 | Cayman Islands, Samoa, BVI, Seychelles, Panama |
| Osprey | 52 | Cayman Islands, Niue, BVI, Panama, Isle of Man |
| Talon | 47 | Niue, BVI, Seychelles, Malta |
| Enron | 71 | Cayman Islands, BVI, Seychelles |
| JEDI | 18 | Cayman Islands, BVI, Panama, Samoa |
| Raptor | 21 | BVI, Malta, Bahamas |
| Southampton | 18 | BVI, Bahamas, Malta |

**Note:** These are name matches against the full ICIJ leaked dataset (Panama Papers, Paradise Papers, Pandora Papers). Not every match is a direct hit on the Enron entity — but the presence of multiple matches for each term across high-secrecy jurisdictions is consistent with the offshore structure the Enron SPEs used.

---

### Email Intelligence Summary

Top entities by email frequency:

| Entity | Type | Emails | Sample context |
|--------|------|--------|----------------|
| Ken Lay | Executive | 6,062 | Board communications |
| Jeff Skilling | Executive | 4,044 | Operations, SPE strategy |
| LJM | SPE | 1,024 | Partnership operations, capital transfers |
| Raptor | SPE | 778 | Hedging vehicle |
| JEDI | SPE | 434 | Investment vehicle |
| Andy Fastow | Executive | 539 | CFO, LJM manager |

Key emails surfaced:
- **fastow/1**: Fastow instructs Kopper to keep Chewco wires below $10k threshold
- **skilling/1**: Skilling describes $1.2B off-balance-sheet exposure to Lay, suggests not disclosing full structure

---

## Quality Assessment

**Did Claude find all 4 patterns?** Yes — structuring, round-trips, Southampton, and quarter-end spikes all surface from the data as written.

**Email reads:** Claude can read the emails but needs to recurse into subdirectories. The emails have no file extension (numbered files: `1`, `2`, `3`), which Claude handles correctly.

**ICIJ context:** Claude correctly flags the offshore jurisdiction matches but should note these are probabilistic name matches, not confirmed entity identifications.

---

## Issues Found

1. **Email file structure not documented in storyline:** The emails are organised as `emails/<mailbox>/<number>` with no `.txt` extension. The Step 1 prompt just says `data/unstructured/emails/` — Claude handles this correctly in practice, but it's worth noting for facilitators.
2. **Shell payments via `ACC-SPE` accounts:** The transactions flag all SPE accounts as receivers, but the `holder_type=spe` filter in accounts.json makes this discoverable via tool use.
