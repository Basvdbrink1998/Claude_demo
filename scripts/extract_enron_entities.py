#!/usr/bin/env python3
"""
Extract named entities from the Enron email corpus.
Scans for known executives, SPEs, and dollar amounts, then writes a CSV
that the transaction generator uses as seeds.

Usage:
    python scripts/extract_enron_entities.py --enron-dir /path/to/maildir
    python scripts/extract_enron_entities.py --enron-dir /path/to/maildir --output data/structured/extracted_entities.csv
"""

import os
import re
import csv
import email
import argparse
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Known Enron entities — real names from the scandal
# ---------------------------------------------------------------------------

EXECUTIVES = {
    "Kenneth Lay":     "executive",
    "Ken Lay":         "executive",
    "Jeffrey Skilling":"executive",
    "Jeff Skilling":   "executive",
    "Andrew Fastow":   "executive",
    "Andy Fastow":     "executive",
    "Michael Kopper":  "executive",
    "Rebecca Mark":    "executive",
    "Lou Pai":         "executive",
    "Greg Whalley":    "executive",
    "Richard Causey":  "executive",
    "Mark Frevert":    "executive",
    "Ben Glisan":      "executive",
    "Sherron Watkins": "executive",
    "Kevin Hannon":    "executive",
    "Timothy Belden":  "executive",
    "David Delainey":  "executive",
}

SPECIAL_PURPOSE_ENTITIES = {
    "LJM Cayman":          "spe",
    "LJM2":                "spe",
    "LJM":                 "spe",
    "Chewco":              "spe",
    "JEDI":                "spe",
    "Raptor":              "spe",
    "Talon LLC":           "spe",
    "Timberwolf":          "spe",
    "Whitewing":           "spe",
    "Condor":              "spe",
    "Southampton":         "spe",
    "Bobcat":              "spe",
    "Pronghorn":           "spe",
    "Fishtail":            "spe",
    "Braveheart":          "spe",
    "Osprey":              "spe",
    "Marlin":              "spe",
}

ALL_ENTITIES = {**EXECUTIVES, **SPECIAL_PURPOSE_ENTITIES}

AMOUNT_RE = re.compile(r'\$\s?([\d,]+(?:\.\d{2})?)\s?(?:million|MM|M\b)?', re.IGNORECASE)


def parse_email_file(path: Path) -> dict | None:
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            msg = email.message_from_file(f)

        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body += part.get_payload(decode=False) or ''
        else:
            body = msg.get_payload(decode=False) or ''

        return {
            'subject': msg.get('subject', ''),
            'date':    msg.get('date', ''),
            'from':    msg.get('from', ''),
            'body':    str(body),
        }
    except Exception:
        return None


def extract_context(text: str, entity: str, window: int = 100) -> str:
    idx = text.lower().find(entity.lower())
    if idx == -1:
        return ''
    start = max(0, idx - window)
    end   = min(len(text), idx + len(entity) + window)
    return text[start:end].replace('\n', ' ').strip()


def scan_corpus(enron_dir: str) -> dict:
    results = defaultdict(lambda: {
        'entity_type':       '',
        'email_count':       0,
        'amounts_mentioned': [],
        'sample_context':    '',
    })

    email_files = [
        f for f in Path(enron_dir).rglob('*')
        if f.is_file() and not f.suffix
    ]

    print(f"Scanning {len(email_files):,} email files...")

    for i, fpath in enumerate(email_files):
        if i % 5000 == 0:
            print(f"  {i:,} / {len(email_files):,}")

        parsed = parse_email_file(fpath)
        if not parsed:
            continue

        full_text = f"{parsed['subject']} {parsed['body']}"

        for entity, etype in ALL_ENTITIES.items():
            if entity.lower() in full_text.lower():
                rec = results[entity]
                rec['entity_type'] = etype
                rec['email_count'] += 1

                if not rec['sample_context']:
                    rec['sample_context'] = extract_context(full_text, entity)

                amounts = AMOUNT_RE.findall(full_text)
                rec['amounts_mentioned'].extend(amounts[:3])

    return results


def write_output(results: dict, output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    rows = [
        (name, rec) for name, rec in results.items()
        if rec['email_count'] > 0
    ]
    rows.sort(key=lambda x: -x[1]['email_count'])

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'entity_name', 'entity_type', 'email_count',
            'amounts_mentioned', 'sample_context',
        ])
        writer.writeheader()

        for name, rec in rows:
            writer.writerow({
                'entity_name':       name,
                'entity_type':       rec['entity_type'],
                'email_count':       rec['email_count'],
                'amounts_mentioned': ' | '.join(dict.fromkeys(rec['amounts_mentioned']))[:200],
                'sample_context':    rec['sample_context'][:300],
            })

    print(f"Wrote {len(rows)} entities → {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract named entities from the Enron email corpus')
    parser.add_argument('--enron-dir', required=True,
                        help='Path to the Enron maildir root')
    parser.add_argument('--output', default='data/structured/extracted_entities.csv',
                        help='Output CSV path (default: data/structured/extracted_entities.csv)')
    args = parser.parse_args()

    results = scan_corpus(args.enron_dir)
    write_output(results, args.output)


if __name__ == '__main__':
    main()
