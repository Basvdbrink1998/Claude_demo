# Forensic Intelligence Workshop — Facilitator Notes

> **Keep this file out of participants' Claude Code sessions.** It contains answer-key information that would be auto-loaded if present in a CLAUDE.md file. Share only verbally or after the debrief.

---

## The Investigation Narrative

> A financial crimes unit has received a whistleblower tip about irregular payments at an energy company. They have three data sources: a transaction export, a corporate email archive, and a public offshore leaks database. None of the sources alone is conclusive. The task is to connect them.

Participants will discover (in order):

1. A cluster of transfers just below the $10,000 reporting threshold going to an entity called *Chewco Investments L.P.*
2. Emails in which a senior executive discusses "partnership arrangements" with offshore vehicles around the same dates
3. Three large transfers that leave Enron Corp, pass through *LJM Cayman* and *JEDI Partners*, and return — debt disguised as equity
4. A $26.8M payment to *Southampton Place L.P.* three days before the company's collapse
5. All of the above entities appearing in the ICIJ Offshore Leaks database

This is not fiction — these are the real Enron SPEs, real executive names, and real forensic patterns from the scandal.

---

## Embedded Forensic Patterns (Answer Key)

| Pattern | Description | Count |
|---------|-------------|-------|
| `structuring` | Transfers to Chewco of $9,100–$9,850 (just below $10k threshold) | 14 |
| `round_trip_leg1/2/3` | Enron → LJM Cayman → JEDI → Enron (3 full cycles) | 9 |
| `shell_payment` | Consulting/advisory fees to Cayman/BVI shells | 45 |
| `high_value_shell` | $26.8M to Southampton Place on 2001-09-28 | 1 |
| `legitimate` | Normal energy business transactions | ~1,931 |

The `data/structured/transactions_facilitator.csv` file contains a `flag_type` column labelling every row — use it to verify what Claude finds vs. what exists.

---

## Debrief Guidance

After participants have run Step 1, walk through:

- Which patterns did Claude surface unprompted?
- Which required more specific follow-up prompts?
- Any false positives (legitimate transactions flagged)?
- Any false negatives (embedded patterns missed)?

This gap between "what Claude found" and "what we know exists" is the core forensic AI lesson: Claude surfaces hypotheses, investigators verify them.
