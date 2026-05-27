# Forensic Intelligence Workshop — Claude Demo

## Workshop Overview

This interactive workshop demonstrates how Claude can support forensic and investigative workflows across three stages:

1. **Data Analysis** — linking structured and unstructured data sources
2. **Corporate Intelligence** — retrieving and synthesising information from the web
3. **Dashboard** — vibe-coding a live investigation dashboard

---

## Stage 1: Structured & Unstructured Data Analysis

### Goal
Show how Claude can ingest, cross-reference, and surface insights from mixed data formats — the kind of fragmented evidence typical in forensic investigations.

### Structured data examples
- Transaction records (CSV/Excel): dates, amounts, counterparties, account numbers
- Company registries (JSON/XML): directors, addresses, incorporation dates
- Customs/logistics data: shipment manifests, HS codes, origin/destination pairs

### Unstructured data examples
- Scanned documents (PDF): contracts, invoices, correspondence
- Email threads (plain text / .eml)
- Free-text case notes and interview summaries

### What to demonstrate
- Extract named entities (people, companies, addresses, dates, amounts) from PDFs and emails
- Reconcile them against structured records — flag matches, discrepancies, and gaps
- Build a simple entity graph: who is connected to whom, through which transactions or documents
- Summarise contradictions that would warrant further investigation

### Sample prompt patterns
```
Analyse the attached invoice PDF and the transactions CSV. 
Identify any invoices that have no matching transaction, and flag 
transactions above €50,000 that reference unknown counterparties.
```

```
From these email threads, extract every person, company, and date mentioned.
Cross-reference them with the company registry JSON and highlight
any directors that appear in the emails but are not in the registry.
```

---

## Stage 2: Corporate Intelligence (Web Research)

### Goal
Show how Claude with web access can enrich an investigation with open-source intelligence (OSINT) — publicly available corporate, financial, and reputational data.

### Topics to cover
- Looking up company ownership structures and UBOs (ultimate beneficial owners)
- Checking sanctions lists, PEP (politically exposed persons) databases, and adverse media
- Mapping subsidiaries, related entities, and known associates
- Verifying addresses, registration numbers, and incorporation details against public registries

### What to demonstrate
- Give Claude a company name and have it retrieve and summarise public filings, news, and registry data
- Chain lookups: start from one entity, discover related companies, then research those
- Produce a structured summary with sources cited, highlighting red flags

### Sample prompt patterns
```
Research [Company Name]. Find its registered address, directors, 
any known subsidiaries, and any adverse news or sanctions matches. 
Summarise findings with source links.
```

```
Starting from the director name [Full Name], identify all companies 
they are or were associated with, their registration statuses, 
and any public litigation or enforcement actions.
```

### Important notes
- Always cite sources; distinguish verified public records from news/commentary
- Note data freshness — registry data can lag weeks or months
- OSINT is a starting point, not a conclusion; flag items that need formal verification

---

## Stage 3: Vibe-Coding the Investigation Dashboard

### Goal
Live-code a simple web dashboard that ties stages 1 and 2 together — an interface investigators could use to query, visualise, and annotate findings.

### Features to build (iteratively)
1. **Entity search** — search by name, company, or transaction ID; show linked records
2. **Timeline view** — plot events and transactions on a chronological axis
3. **Network graph** — visualise entity relationships (people ↔ companies ↔ transactions)
4. **Flag & annotate** — mark entities or links as suspicious, verified, or needs review
5. **Export** — generate a case summary report (PDF or structured JSON)

### Suggested stack
- **Frontend**: plain HTML/CSS/JS or a lightweight framework (e.g. React + Vite)
- **Graph visualisation**: D3.js or Cytoscape.js
- **Backend / API**: FastAPI (Python) or Express (Node) — keep it minimal
- **Data store**: SQLite or in-memory JSON for the demo; easy to swap out later
- **Claude integration**: Anthropic SDK — stream responses for live analysis feel

### Vibe-coding approach
Start from a description of what you want, iterate with Claude, and ship incrementally:

```
Build a single-page app with a search box. When I type a company name, 
it calls a local FastAPI endpoint that returns related entities as JSON,
and renders them as nodes in a Cytoscape.js graph.
```

```
Add a sidebar that shows the raw evidence documents linked to a selected node,
with key passages highlighted based on why that entity was flagged.
```

---

## Running the Workshop

### Prerequisites
- Claude API key set as `ANTHROPIC_API_KEY`
- Python 3.11+ (for backend demo)
- Node 20+ (for frontend demo)
- Sample data files in `data/` (see below)

### Suggested session flow

| Time | Activity |
|------|----------|
| 0–15 min | Intro: forensic use case, what Claude can and cannot do |
| 15–40 min | Stage 1: live data analysis with sample files |
| 40–60 min | Stage 2: corporate intelligence lookups, OSINT demo |
| 60–90 min | Stage 3: vibe-coding the dashboard together |
| 90–100 min | Q&A and wrap-up |

### Sample data folder structure
```
data/
  structured/
    transactions.csv
    company_registry.json
  unstructured/
    invoices/        # PDF scans
    emails/          # .eml or .txt threads
    case_notes.txt
```

---

## Key Principles for Forensic AI Use

- **Claude as analyst, human as investigator** — Claude surfaces patterns; a human makes the call
- **Auditability** — log every prompt and response; the investigation record must be reproducible
- **Data minimisation** — only feed Claude the data relevant to the query; avoid uploading entire case files unnecessarily
- **No hallucination tolerance** — treat any factual claim Claude makes about real entities as a hypothesis to verify, not a finding
- **Legal and ethical boundaries** — OSINT only; no scraping of access-controlled systems, no personal data beyond what is legally permitted in your jurisdiction
