"""
Forensic Intelligence Dashboard — FastAPI backend
Run: uvicorn dashboard.backend.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json
import csv
from pathlib import Path
from collections import defaultdict

app = FastAPI(title="Forensic Intelligence Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "structured"
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


def _load():
    with open(DATA_DIR / "accounts.json") as f:
        accounts = json.load(f)
    accounts_by_id = {a["account_id"]: a for a in accounts}

    transactions = []
    with open(DATA_DIR / "transactions.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["amount"] = float(row["amount"])
            transactions.append(row)

    connections: dict[str, set] = defaultdict(set)
    txns_by_account: dict[str, list] = defaultdict(list)
    for t in transactions:
        s, r = t["sender_account_id"], t["receiver_account_id"]
        connections[s].add(r)
        connections[r].add(s)
        txns_by_account[s].append(t)
        txns_by_account[r].append(t)

    return accounts, accounts_by_id, transactions, dict(connections), dict(txns_by_account)


ACCOUNTS, ACCOUNTS_BY_ID, TRANSACTIONS, CONNECTIONS, TXNS_BY_ACCOUNT = _load()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    html = FRONTEND_DIR / "index.html"
    if not html.exists():
        raise HTTPException(status_code=500, detail="Frontend not found")
    return FileResponse(str(html))


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "accounts": len(ACCOUNTS),
        "transactions": len(TRANSACTIONS),
    }


@app.get("/api/search")
def search(q: str = Query(default="")):
    q_lower = q.strip().lower()
    if not q_lower:
        return {"results": ACCOUNTS}
    results = [
        a for a in ACCOUNTS
        if q_lower in a["holder_name"].lower() or q_lower in a["account_id"].lower()
    ]
    return {"results": results}


@app.get("/api/entity/{account_id}")
def get_entity(account_id: str):
    account = ACCOUNTS_BY_ID.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    txns = TXNS_BY_ACCOUNT.get(account_id, [])
    sent = [t for t in txns if t["sender_account_id"] == account_id]
    received = [t for t in txns if t["receiver_account_id"] == account_id]

    return {
        "account": account,
        "stats": {
            "total_sent": sum(t["amount"] for t in sent),
            "total_received": sum(t["amount"] for t in received),
            "transaction_count": len(txns),
            "sent_count": len(sent),
            "received_count": len(received),
        },
    }


@app.get("/api/network/{account_id}")
def get_network(account_id: str):
    if account_id not in ACCOUNTS_BY_ID:
        raise HTTPException(status_code=404, detail="Account not found")

    connected_ids = CONNECTIONS.get(account_id, set())
    all_ids = {account_id} | connected_ids

    nodes = []
    for aid in all_ids:
        acc = ACCOUNTS_BY_ID.get(aid)
        if not acc:
            continue
        txns = TXNS_BY_ACCOUNT.get(aid, [])
        nodes.append({
            **acc,
            "transaction_count": len(txns),
            "total_volume": sum(t["amount"] for t in txns),
            "is_center": aid == account_id,
        })

    # Aggregate edges between nodes in this subgraph
    edge_map: dict[tuple, dict] = defaultdict(lambda: {"count": 0, "total": 0.0})
    for t in TRANSACTIONS:
        s, r = t["sender_account_id"], t["receiver_account_id"]
        if s in all_ids and r in all_ids:
            key = (min(s, r), max(s, r))
            edge_map[key]["count"] += 1
            edge_map[key]["total"] += t["amount"]

    edges = [{"source": k[0], "target": k[1], **v} for k, v in edge_map.items()]
    return {"nodes": nodes, "edges": edges}


@app.get("/api/timeline/{account_id}")
def get_timeline(account_id: str):
    if account_id not in ACCOUNTS_BY_ID:
        raise HTTPException(status_code=404, detail="Account not found")

    txns = TXNS_BY_ACCOUNT.get(account_id, [])
    result = sorted(
        [
            {**t, "direction": "sent" if t["sender_account_id"] == account_id else "received"}
            for t in txns
        ],
        key=lambda x: x["date"],
    )
    return {"transactions": result}
