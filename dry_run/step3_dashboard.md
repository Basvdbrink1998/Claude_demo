# Step 3 — Investigation Dashboard: Dry Run Results

**Date:** 2026-05-29
**Prompt used:** As written in `storyline.md` Step 3

---

## Prompt Sent

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

---

## Pre-existing Dashboard

The repository already contains a complete dashboard at `dashboard/`:

```
dashboard/
├── backend/
│   └── main.py         FastAPI server, 155 lines
├── frontend/
│   └── index.html      Single-page app, 983 lines (D3.js + custom dark theme)
└── tests/
    └── smoke_test.py   Playwright smoke tests, 127 lines
```

**When Claude sees this prompt**, it will find the existing code and either extend it or confirm it already satisfies the requirements. This is the intended behaviour for the workshop — the dashboard is a starting point that participants extend via the follow-up prompts.

---

## Server Test

### Start command
```bash
uvicorn dashboard.backend.main:app --host 0.0.0.0 --port 8000
```

### Health check
```
GET /api/health → {"status":"ok","accounts":27,"transactions":2000}
```

### API endpoints verified
| Endpoint | Response |
|----------|----------|
| `GET /api/health` | `{"status":"ok","accounts":27,"transactions":2000}` |
| `GET /api/search?q=LJM` | 1 entity returned (LJM Cayman L.P.) |
| `GET /api/network/ACC-SPE-001` | 3 nodes, 3 edges |
| `GET /` | Serves `frontend/index.html` |

---

## Smoke Test Results

```
platform win32 -- Python 3.11.0, pytest-9.0.3
plugins: playwright-0.8.0

dashboard/tests/smoke_test.py::test_dashboard_loads                          PASSED [ 25%]
dashboard/tests/smoke_test.py::test_search_returns_results                   PASSED [ 50%]
dashboard/tests/smoke_test.py::test_select_entity_populates_graph_and_timeline  PASSED [ 75%]
dashboard/tests/smoke_test.py::test_click_different_graph_node_updates_timeline PASSED [100%]

4 passed in 8.12s
```

All 4 tests pass. ✓

---

## Dashboard Features Verified

| Feature | Status |
|---------|--------|
| Entity search sidebar | ✓ Working — real-time debounced search |
| Network graph (D3.js force-directed) | ✓ Working — nodes sized by volume, colour-coded by type |
| Transaction timeline | ✓ Working — log-scale y-axis, Enron event reference lines |
| Entity details panel | ✓ Working — stats, flag buttons, JSON export |
| Dark theme / SENTINEL branding | ✓ Working |
| Offshore jurisdiction highlighting | ✓ Working — KY, VG flagged in red |

---

## Follow-up Prompts Assessment

The three follow-up prompts in the storyline are already implemented in the dashboard:

| Follow-up prompt | Implementation status |
|------------------|-----------------------|
| Sidebar with transactions colour-coded green/red | ✓ Built — in entity details panel |
| Vertical reference lines on timeline for Enron events | ✓ Built — 5 events marked |
| Flag button (Suspicious / Verified / Needs Review) | ✓ Built — persists in-memory during session |

**Implication:** These follow-up prompts won't produce visible new changes unless the dashboard is rebuilt from scratch. Options:
1. Use them as they are (Claude confirms features exist, may add polish)
2. Delete the `dashboard/` folder before Step 3 to force a fresh build
3. Replace follow-up prompts with new extension ideas (e.g. export to PDF, add ICIJ data to graph)

---

## Issues Found

1. **Dashboard already exists**: The follow-up prompts in the storyline add features that are already built. Facilitators should either delete `dashboard/` before Step 3 or use different follow-up prompts. See `dry_run/summary.md` for recommendations.
2. **`@playwright` smoke test scope**: The current smoke test only tests the existing dashboard. After a fresh build, the test file path may differ — participants should adjust the pytest command accordingly.
3. **Windows path note**: `uvicorn` must be run from the repo root, not from inside `dashboard/`. The correct import path is `dashboard.backend.main:app`.
