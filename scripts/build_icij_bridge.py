#!/usr/bin/env python3
"""
Build a reference bridge between Enron entities and the ICIJ Offshore Leaks database.

Download the ICIJ bulk data from: https://offshoreleaks.icij.org/pages/database
Unzip and point --icij-nodes at the nodes-entities.csv file.

The script does a case-insensitive substring search across entity names,
then writes a filtered CSV to data/reference/icij_bridge.csv for use in
cross-dataset forensic analysis during the workshop.

Usage:
    python scripts/build_icij_bridge.py --icij-nodes /path/to/nodes-entities.csv
"""

import csv
import argparse
from pathlib import Path

# Terms to search for in the ICIJ nodes data.
# Includes Enron SPE names plus associated offshore jurisdictions and individuals.
SEARCH_TERMS = [
    "LJM",
    "Chewco",
    "JEDI",
    "Enron",
    "Fastow",
    "Kopper",
    "Southampton",
    "Whitewing",
    "Osprey",
    "Marlin",
    "Talon",
    "Timberwolf",
    "Raptor",
    "Glisan",
    "Belden",
]

# Columns to retain from the ICIJ dataset (subset for readability)
KEEP_COLUMNS = [
    "node_id",
    "name",
    "jurisdiction",
    "jurisdiction_description",
    "countries",
    "sourceID",
    "valid_until",
    "note",
]


def search_icij(nodes_file: str, search_terms: list[str], output_path: str) -> int:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    matches = []
    total   = 0

    with open(nodes_file, 'r', encoding='utf-8', errors='replace') as f:
        reader  = csv.DictReader(f)
        headers = reader.fieldnames or []
        out_fields = [c for c in KEEP_COLUMNS if c in headers] + ["matched_term"]

        for row in reader:
            total += 1
            name = (row.get("name") or "").lower()

            for term in search_terms:
                if term.lower() in name:
                    matches.append({**row, "matched_term": term})
                    break

    print(f"Scanned {total:,} ICIJ nodes — {len(matches)} matched.")

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(matches)

    print(f"Bridge table written → {output_path}")

    # Print a quick breakdown by source dataset
    by_source: dict[str, int] = {}
    for m in matches:
        src = m.get("sourceID", "unknown")
        by_source[src] = by_source.get(src, 0) + 1

    if by_source:
        print("\nMatches by source dataset:")
        for src, count in sorted(by_source.items(), key=lambda x: -x[1]):
            print(f"  {src}: {count}")

    return len(matches)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Cross-reference Enron entities against the ICIJ Offshore Leaks database'
    )
    parser.add_argument(
        '--icij-nodes', required=True,
        help='Path to nodes-entities.csv from the ICIJ bulk download'
    )
    parser.add_argument(
        '--output', default='data/reference/icij_bridge.csv',
        help='Output path (default: data/reference/icij_bridge.csv)'
    )
    args = parser.parse_args()

    n = search_icij(args.icij_nodes, SEARCH_TERMS, args.output)

    if n == 0:
        print(
            "\nNo matches found. Check that --icij-nodes points at nodes-entities.csv "
            "(not the edges or addresses file)."
        )


if __name__ == '__main__':
    main()
