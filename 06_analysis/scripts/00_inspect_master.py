#!/usr/bin/env python3
"""00_inspect_master.py — data-quality audit of extracted_master_v2.csv.

Written after an incidental finding: `venue` appeared to hold a single constant
value across all 171 rows, and PowerShell's console rendering inserted control
characters that made the value unreadable. Before relying on any master column as
an extraction prior, its real content must be visible and its informativeness
measured.

For every column this prints:
    - distinct value count (a constant column carries no information)
    - how many rows are empty / NOT_REPORTED
    - whether the raw value contains control characters (a sign of a mangled
      field rather than a real venue/author string)
    - the most common values

Read-only.

Usage:
    python 06_analysis/scripts/00_inspect_master.py
    python 06_analysis/scripts/00_inspect_master.py --col venue --rows 6
"""

from __future__ import annotations

import argparse
import csv
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MASTER_CSV = REPO / "02_data_processed" / "extracted_master_v2.csv"

EMPTY_TOKENS = {"", "not_reported", "n/a", "na", "none", "-", "nan", "null"}


def is_empty(value: str) -> bool:
    return value.strip().lower() in EMPTY_TOKENS


def control_chars(value: str) -> list[str]:
    bad = []
    for ch in value:
        if ch == "\t":
            continue
        if unicodedata.category(ch) in {"Cc", "Cf"}:
            bad.append(f"U+{ord(ch):04X}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--col", default=None, help="dump raw values of one column")
    ap.add_argument("--rows", type=int, default=8)
    args = ap.parse_args()

    with MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    n = len(rows)
    print(f"extracted_master_v2.csv: {n} rows x {len(fields)} columns")
    print(f"{'column':<20} {'distinct':>8} {'empty':>6} {'ctl':>4}  most common")
    print("-" * 100)
    for col in fields:
        values = [r.get(col, "") for r in rows]
        counts = Counter(values)
        distinct = len(counts)
        empty = sum(1 for v in values if is_empty(v))
        ctl = sum(1 for v in values if control_chars(v))
        top = counts.most_common(2)
        pretty = "  |  ".join(
            f"{repr(v)[:38]} x{c}" if len(repr(v)) > 3 else f"{v!r} x{c}"
            for v, c in top
        )
        print(f"{col:<20} {distinct:>8} {empty:>6} {ctl:>4}  {pretty[:70]}")

    if args.col:
        print(f"\n===== raw values of {args.col} =====")
        for r in rows[: args.rows]:
            print(f"{r['id']}: {r.get(args.col, '')!r}")

    print("\n===== columns that carry no information =====")
    dead = [
        c for c in fields
        if len(Counter(r.get(c, "") for r in rows)) == 1
        and not is_empty(rows[0].get(c, ""))
    ]
    print(f"  constant columns: {dead if dead else 'none'}")

    print("\n===== columns with control characters =====")
    ctl_cols = [
        c for c in fields
        if any(control_chars(r.get(c, "")) for r in rows)
    ]
    for c in ctl_cols:
        sample = next(r[c] for r in rows if control_chars(r.get(c, "")))
        print(f"  {c}: e.g. {sample!r}")
        print(f"       offending: {sorted(set(control_chars(sample)))}")
    if not ctl_cols:
        print("  none")

    print("\n===== spot rows =====")
    for r in rows[:3]:
        print(f"  {r['id']}: title={r['title'][:60]!r}")
        print(f"        authors={r['authors'][:60]!r}")
        print(f"        venue={r['venue']!r}  doi={r['doi']!r}  year={r['year']!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())