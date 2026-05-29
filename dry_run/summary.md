# Dry Run Summary

**Date:** 2026-05-29
**Repo:** Claude demo (Forensic Intelligence Workshop)

---

## Overall Result: PASS with minor improvements needed

All core mechanics work. The data tells a coherent story. The dashboard runs cleanly. Three issues require attention before a live workshop.

---

## Step Results

| Step | Result | Notes |
|------|--------|-------|
| Step 0 — Environment Setup | ✓ PASS | All 4 commands succeed |
| Step 1 — Data Analysis | ✓ PASS | Claude finds all 4 forensic patterns |
| Step 2 — Corporate Intelligence | ✓ PASS | Web search returns real enforcement records |
| Step 3 — Dashboard | ✓ PASS (4/4 tests) | But follow-up prompts add features already built |

---

## Issues and Recommendations

### Issue 1 — Step 3 follow-up prompts are pre-implemented (MEDIUM)

**Problem:** The three follow-up prompts in Step 3 (coloured sidebar, Enron event lines, flag buttons) are already built in `dashboard/frontend/index.html`. A participant running them will get Claude confirming they exist rather than building them.

**Options:**
- **Option A (Recommended for demos):** Delete `dashboard/` before Step 3 to force a fresh build. Claude will build the dashboard from scratch and the follow-up prompts will produce genuine incremental additions.
- **Option B (Recommended for workshops):** Keep the dashboard and replace the follow-up prompts with genuinely new features — e.g. adding the ICIJ data as a second node layer in the graph, or exporting a case summary as JSON/PDF.
- **Option C:** Frame Step 3 explicitly as "here's what Claude already built — let's extend it further" with new prompts.

---

### Issue 2 — Step 1 email file structure not documented (LOW)

**Problem:** The Step 1 prompt lists `data/unstructured/emails/` but doesn't mention that emails are organised by mailbox subfolder with no file extension (e.g. `emails/fastow/1`). Claude handles this correctly in practice, but facilitators should know what to expect.

**Fix:** Add a note to the Data table in Step 1 mentioning the subfolder structure.

---

### Issue 3 — Step 2 continuity assumption (LOW)

**Problem:** The Step 2 prompt opens with "Based on what you just found" — valid in a single session but fragile if participants close and reopen Claude Code between steps.

**Fix:** Add the key entity names as a parenthetical fallback so Step 2 works even in a fresh session.

---

## What Works Well

- **Step 0 is bulletproof** — all install commands succeed without error
- **Step 1 data is rich** — Claude finds structuring, round-trips, Southampton, quarter-end spikes, and email corroboration all in one pass
- **The Fastow email (fastow/1) is a smoking gun** — "Keep each wire under the threshold — you know the drill" is a powerful live demo moment
- **The Skilling email (skilling/1) adds a second thread** — $1.2B off-balance-sheet exposure, deliberate non-disclosure to investors
- **ICIJ cross-reference is visually impressive** — every SPE entity has offshore jurisdiction matches
- **All 4 smoke tests pass** — the dashboard is production-ready
- **The Southampton $26.8M payment is dateable** — 65 days before bankruptcy is a concrete, quotable finding

---

## Suggested Workshop Timing

| Step | Suggested time |
|------|---------------|
| Intro + data walkthrough | 10 min |
| Step 0 (live) | 3 min |
| Step 1 (live) | 20–25 min |
| Step 2 (live) | 15 min |
| Step 3 (live) | 20–25 min |
| Debrief | 10 min |
| **Total** | **~85 min** |
