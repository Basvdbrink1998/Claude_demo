#!/usr/bin/env python3
"""
Generate a synthetic Enron-era financial transaction dataset.

Embeds four forensic patterns that participants must discover:
  1. Structuring  — 14 transfers to Chewco just below the $10k reporting threshold
  2. Round-trips  — Enron → LJM Cayman → JEDI → Enron (debt disguised as equity)
  3. Shell payments — recurring "consulting" payments to Cayman/BVI entities
  4. Quarter-end spikes — large transfers on the last 2-3 days of each quarter

Outputs:
  data/structured/transactions.csv          — workshop version (no flag column)
  data/structured/transactions_facilitator.csv — facilitator key (with flag_type)
  data/structured/accounts.json             — all account/entity metadata

Usage:
    python scripts/generate_transactions.py
    python scripts/generate_transactions.py --seed 42 --num-transactions 2000
"""

import random
import json
import csv
import uuid
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Entity definitions
# ---------------------------------------------------------------------------

ENRON_EXECUTIVES = [
    {"name": "Andrew Fastow",   "role": "CFO",              "company": "Enron Corp"},
    {"name": "Michael Kopper",  "role": "Managing Director", "company": "Enron Corp"},
    {"name": "Ben Glisan",      "role": "Treasurer",         "company": "Enron Corp"},
    {"name": "Kevin Hannon",    "role": "COO",               "company": "Enron Broadband Services"},
    {"name": "Timothy Belden",  "role": "Head of Trading",   "company": "Enron Energy Services"},
    {"name": "Lou Pai",         "role": "CEO",               "company": "Enron Energy Services"},
]

SHELL_ENTITIES = [
    {"name": "LJM Cayman L.P.",          "jurisdiction": "KY", "type": "spe"},
    {"name": "LJM2 Co-Investment L.P.",   "jurisdiction": "KY", "type": "spe"},
    {"name": "Chewco Investments L.P.",   "jurisdiction": "KY", "type": "spe"},
    {"name": "JEDI Partners L.P.",        "jurisdiction": "KY", "type": "spe"},
    {"name": "Southampton Place L.P.",    "jurisdiction": "KY", "type": "spe"},
    {"name": "Talon LLC",                 "jurisdiction": "TX", "type": "raptor"},
    {"name": "Timberwolf LLC",            "jurisdiction": "TX", "type": "raptor"},
    {"name": "Whitewing Associates L.P.", "jurisdiction": "KY", "type": "spe"},
    {"name": "Osprey Trust",              "jurisdiction": "VG", "type": "spe"},
    {"name": "Marlin Water Trust",        "jurisdiction": "VG", "type": "spe"},
]

LEGITIMATE_COUNTERPARTIES = [
    {"name": "Citibank N.A.",             "jurisdiction": "US"},
    {"name": "JP Morgan Chase",           "jurisdiction": "US"},
    {"name": "Deutsche Bank AG",          "jurisdiction": "DE"},
    {"name": "Barclays PLC",              "jurisdiction": "GB"},
    {"name": "Portland General Electric", "jurisdiction": "US"},
    {"name": "Dabhol Power Company",      "jurisdiction": "IN"},
    {"name": "Azurix Corp",               "jurisdiction": "US"},
    {"name": "Enron Pipeline Company",    "jurisdiction": "US"},
    {"name": "Wessex Water Services",     "jurisdiction": "GB"},
    {"name": "EOTT Energy Partners",      "jurisdiction": "US"},
]

LEGITIMATE_DESCRIPTIONS = [
    "Gas supply contract payment",
    "Pipeline maintenance services",
    "Energy trading settlement",
    "Quarterly service fee",
    "Equipment lease payment",
    "IT infrastructure services",
    "Regulatory compliance fee",
    "Transmission tariff payment",
    "Natural gas procurement",
    "Power purchase agreement",
    "Capacity reservation charge",
    "Balancing charge adjustment",
    "Interconnection fee",
    "Fuel supply agreement",
]

SHELL_DESCRIPTIONS = [
    "Management consulting fees",
    "Advisory services Q{}",
    "Partnership distribution",
    "Investment management fee",
    "Strategic advisory retainer",
    "Professional services",
    "Equity contribution",
    "Capital distribution",
    "Restructuring advisory",
    "Financial consulting services",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def make_id() -> str:
    return str(uuid.uuid4())[:12].upper()


def build_accounts(executives, shells, legit) -> list[dict]:
    accounts = [
        {
            "account_id":   "ACC-ENR-001",
            "holder_name":  "Enron Corp",
            "holder_type":  "company",
            "jurisdiction": "US",
            "account_type": "corporate_checking",
            "opened_date":  "1996-01-01",
        }
    ]

    for i, exc in enumerate(executives, 1):
        year  = random.randint(1995, 1999)
        month = random.randint(1, 12)
        accounts.append({
            "account_id":   f"ACC-EXE-{i:03d}",
            "holder_name":  exc["name"],
            "holder_type":  "individual",
            "jurisdiction": "US",
            "account_type": "personal",
            "opened_date":  f"{year}-{month:02d}-01",
            "employer":     exc["company"],
        })

    for i, shell in enumerate(shells, 1):
        year  = random.randint(1997, 1999)
        month = random.randint(1, 12)
        accounts.append({
            "account_id":   f"ACC-SPE-{i:03d}",
            "holder_name":  shell["name"],
            "holder_type":  "company",
            "jurisdiction": shell["jurisdiction"],
            "account_type": "corporate_checking",
            "opened_date":  f"{year}-{month:02d}-01",
        })

    for i, cp in enumerate(legit, 1):
        accounts.append({
            "account_id":   f"ACC-EXT-{i:03d}",
            "holder_name":  cp["name"],
            "holder_type":  "company",
            "jurisdiction": cp["jurisdiction"],
            "account_type": "corporate_checking",
            "opened_date":  "1990-01-01",
        })

    return accounts


def _find(accounts, substring):
    return next(a for a in accounts if substring in a["holder_name"])


# ---------------------------------------------------------------------------
# Transaction generators
# ---------------------------------------------------------------------------

def gen_legitimate(accounts, n, start, end) -> list[dict]:
    enron = _find(accounts, "Enron Corp")
    legit = [a for a in accounts if a["account_id"].startswith("ACC-EXT")]

    rows = []
    for _ in range(n):
        cp        = random.choice(legit)
        amount    = round(random.uniform(10_000, 2_000_000), 2)
        outbound  = random.random() < 0.55
        rows.append({
            "transaction_id":    make_id(),
            "date":              random_date(start, end).strftime("%Y-%m-%d"),
            "amount":            amount,
            "currency":          "USD",
            "sender_account_id": enron["account_id"] if outbound else cp["account_id"],
            "sender_name":       enron["holder_name"] if outbound else cp["holder_name"],
            "receiver_account_id": cp["account_id"] if outbound else enron["account_id"],
            "receiver_name":     cp["holder_name"] if outbound else enron["holder_name"],
            "description":       random.choice(LEGITIMATE_DESCRIPTIONS),
            "transaction_type":  "wire_transfer",
            "flag_type":         None,
        })
    return rows


def gen_structuring(accounts) -> list[dict]:
    """14 transfers to Chewco just below the $10k cash-reporting threshold."""
    enron  = _find(accounts, "Enron Corp")
    chewco = _find(accounts, "Chewco")
    base   = datetime(2001, 7, 8)

    rows = []
    for _ in range(14):
        amount = round(random.uniform(9_100, 9_850), 2)
        date   = base + timedelta(days=random.randint(0, 50))
        rows.append({
            "transaction_id":      make_id(),
            "date":                date.strftime("%Y-%m-%d"),
            "amount":              amount,
            "currency":            "USD",
            "sender_account_id":   enron["account_id"],
            "sender_name":         enron["holder_name"],
            "receiver_account_id": chewco["account_id"],
            "receiver_name":       chewco["holder_name"],
            "description":         "Management consulting fees",
            "transaction_type":    "wire_transfer",
            "flag_type":           "structuring",
        })
    return rows


def gen_round_trips(accounts) -> list[dict]:
    """Three full round-trips: Enron → LJM Cayman → JEDI → Enron."""
    enron = _find(accounts, "Enron Corp")
    ljm   = _find(accounts, "LJM Cayman")
    jedi  = _find(accounts, "JEDI")

    trips = [
        (datetime(2000, 9, 29), 50_000_000.00),
        (datetime(2001, 3, 29), 72_500_000.00),
        (datetime(2001, 6, 28), 38_200_000.00),
    ]

    rows = []
    for base_date, amount in trips:
        # Leg 1: Enron → LJM (quarter-end, labelled "equity contribution")
        rows.append({
            "transaction_id":      make_id(),
            "date":                base_date.strftime("%Y-%m-%d"),
            "amount":              amount,
            "currency":            "USD",
            "sender_account_id":   enron["account_id"],
            "sender_name":         enron["holder_name"],
            "receiver_account_id": ljm["account_id"],
            "receiver_name":       ljm["holder_name"],
            "description":         "Equity contribution",
            "transaction_type":    "wire_transfer",
            "flag_type":           "round_trip_leg1",
        })

        # Leg 2: LJM → JEDI (3–7 days later, small "fee" skimmed)
        d2 = base_date + timedelta(days=random.randint(3, 7))
        rows.append({
            "transaction_id":      make_id(),
            "date":                d2.strftime("%Y-%m-%d"),
            "amount":              round(amount * 0.97, 2),
            "currency":            "USD",
            "sender_account_id":   ljm["account_id"],
            "sender_name":         ljm["holder_name"],
            "receiver_account_id": jedi["account_id"],
            "receiver_name":       jedi["holder_name"],
            "description":         "Partnership capital transfer",
            "transaction_type":    "wire_transfer",
            "flag_type":           "round_trip_leg2",
        })

        # Leg 3: JEDI → Enron (10–21 days later, amount slightly reduced)
        d3 = d2 + timedelta(days=random.randint(10, 21))
        rows.append({
            "transaction_id":      make_id(),
            "date":                d3.strftime("%Y-%m-%d"),
            "amount":              round(amount * 0.94, 2),
            "currency":            "USD",
            "sender_account_id":   jedi["account_id"],
            "sender_name":         jedi["holder_name"],
            "receiver_account_id": enron["account_id"],
            "receiver_name":       enron["holder_name"],
            "description":         "Investment return distribution",
            "transaction_type":    "wire_transfer",
            "flag_type":           "round_trip_leg3",
        })

    return rows


def gen_shell_payments(accounts, n) -> list[dict]:
    """Recurring consulting / advisory payments to offshore shells."""
    enron  = _find(accounts, "Enron Corp")
    shells = [a for a in accounts if a["account_id"].startswith("ACC-SPE")]
    start  = datetime(1999, 1, 1)
    end    = datetime(2001, 11, 15)

    rows = []
    for i in range(n):
        shell  = random.choice(shells)
        # Mix of mid-range and suspiciously round amounts
        if random.random() < 0.4:
            amount = round(random.randint(1, 15) * 1_000_000, 2)
        else:
            amount = round(random.uniform(50_000, 750_000), 2)

        desc = random.choice(SHELL_DESCRIPTIONS)
        if '{}' in desc:
            desc = desc.format(random.randint(1, 4))

        rows.append({
            "transaction_id":      make_id(),
            "date":                random_date(start, end).strftime("%Y-%m-%d"),
            "amount":              amount,
            "currency":            "USD",
            "sender_account_id":   enron["account_id"],
            "sender_name":         enron["holder_name"],
            "receiver_account_id": shell["account_id"],
            "receiver_name":       shell["holder_name"],
            "description":         desc,
            "transaction_type":    "wire_transfer",
            "flag_type":           "shell_payment",
        })
    return rows


def gen_southampton(accounts) -> list[dict]:
    """The $26.8M Southampton payout — real Enron scandal figure."""
    enron       = _find(accounts, "Enron Corp")
    southampton = _find(accounts, "Southampton")

    return [{
        "transaction_id":      make_id(),
        "date":                "2001-09-28",
        "amount":              26_800_000.00,
        "currency":            "USD",
        "sender_account_id":   enron["account_id"],
        "sender_name":         enron["holder_name"],
        "receiver_account_id": southampton["account_id"],
        "receiver_name":       southampton["holder_name"],
        "description":         "Partnership buy-out settlement",
        "transaction_type":    "wire_transfer",
        "flag_type":           "high_value_shell",
    }]


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

FIELDS = [
    "transaction_id", "date", "amount", "currency",
    "sender_account_id", "sender_name",
    "receiver_account_id", "receiver_name",
    "description", "transaction_type",
]


def write_transactions(transactions: list[dict], path: str, include_flags: bool) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fields = FIELDS + (["flag_type"] if include_flags else [])
    sorted_txns = sorted(transactions, key=lambda x: x["date"])

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(sorted_txns)

    print(f"{'[facilitator] ' if include_flags else ''}Wrote {len(transactions):,} transactions → {path}")


def write_accounts(accounts: list[dict], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, indent=2)
    print(f"Wrote {len(accounts)} accounts → {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description='Generate synthetic Enron transaction dataset')
    parser.add_argument('--seed',             type=int, default=42)
    parser.add_argument('--num-transactions', type=int, default=2000,
                        help='Total transaction count (default: 2000)')
    args = parser.parse_args()

    random.seed(args.seed)

    accounts = build_accounts(ENRON_EXECUTIVES, SHELL_ENTITIES, LEGITIMATE_COUNTERPARTIES)

    start = datetime(1999, 1, 1)
    end   = datetime(2001, 11, 30)

    # Reserve slots for the suspicious patterns
    n_suspicious = 14 + 9 + 45 + 1   # structuring + round-trips + shells + southampton
    n_legit      = max(100, args.num_transactions - n_suspicious)

    transactions = (
        gen_legitimate(accounts, n_legit, start, end)
        + gen_structuring(accounts)
        + gen_round_trips(accounts)
        + gen_shell_payments(accounts, 45)
        + gen_southampton(accounts)
    )

    random.shuffle(transactions)

    write_transactions(transactions, 'data/structured/transactions.csv',             include_flags=False)
    write_transactions(transactions, 'data/structured/transactions_facilitator.csv', include_flags=True)
    write_accounts(accounts, 'data/structured/accounts.json')

    # Summary for facilitator
    counts: dict[str, int] = {}
    for t in transactions:
        k = t.get('flag_type') or 'legitimate'
        counts[k] = counts.get(k, 0) + 1

    print("\nTransaction breakdown (facilitator view):")
    for k, v in sorted(counts.items()):
        marker = "  *** " if k != "legitimate" else "      "
        print(f"{marker}{k}: {v}")


if __name__ == '__main__':
    main()
