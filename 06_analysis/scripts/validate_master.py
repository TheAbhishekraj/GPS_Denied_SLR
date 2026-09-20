#!/usr/bin/env python3
"""validate_master.py — Phase 5 EXIT-gate validator for MASTER_EVIDENCE.csv.

Reads:
  - 02_data_processed/MASTER_EVIDENCE.csv   (the evidence master; currently header-only)
  - 08_docs/EXTRACTION_SCHEMA_v1.md          (28-column target schema, required flags)

Writes:
  - _AUDIT/master_validation.md              (PASS/FAIL report; overwritten each run)

Side effects: creates/overwrites _AUDIT/master_validation.md only.
Stdlib only (csv, re, os, datetime). No third-party libraries.
Never modifies MASTER_EVIDENCE.csv or any frozen file.
"""
import csv
import os
import re
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MASTER = os.path.join(REPO, "02_data_processed", "MASTER_EVIDENCE.csv")
SCHEMA = os.path.join(REPO, "08_docs", "EXTRACTION_SCHEMA_v1.md")
OUT = os.path.join(REPO, "_AUDIT", "master_validation.md")
EXPECTED_ROWS = 279


def parse_schema(path):
    """Return (ordered column names, set of required column names) from the schema table."""
    cols = []
    required = set()
    row_re = re.compile(r"^\|\s*(\d+)\s*\|\s*([a-z_][a-z0-9_]*)\s*\|[^|]*\|\s*(yes|optional)\s*\|")
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = row_re.match(line.strip())
            if m:
                name = m.group(2)
                cols.append(name)
                if m.group(3) == "yes":
                    required.add(name)
    return cols, required


def main():
    schema_cols, required = parse_schema(SCHEMA)

    with open(MASTER, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = [r for r in reader if any(c.strip() for c in r)]
    header = rows[0] if rows else []
    data = rows[1:] if len(rows) > 1 else []

    n_rows = len(data)

    # --- structure check against schema ---
    missing_cols = [c for c in schema_cols if c not in header]
    extra_cols = [c for c in header if c not in schema_cols]
    structure_ok = (header == schema_cols)  # exact ordered match
    structure_status = "PASS" if structure_ok else "FAIL"

    # --- duplicate id check ---
    ids = []
    if "id" in header:
        id_idx = header.index("id")
        ids = [r[id_idx].strip() for r in data if len(r) > id_idx]
    dup_ids = sorted({i for i in ids if ids.count(i) > 1 and i != ""})
    n_dup = len(dup_ids)

    # --- empty required fields ---
    empty_required = 0
    empty_detail = []
    for r in data:
        for col in required:
            if col in header:
                ci = header.index(col)
                val = r[ci].strip() if len(r) > ci else ""
                if val == "":
                    empty_required += 1
                    rid = r[header.index("id")] if "id" in header and len(r) > header.index("id") else "?"
                    empty_detail.append((rid, col))

    overall = "PASS" if (structure_ok and n_dup == 0 and empty_required == 0) else "FAIL"

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = []
    lines.append("# MASTER_EVIDENCE Validation Report")
    lines.append("Generated: %s" % ts)
    lines.append("Scope: 02_data_processed/MASTER_EVIDENCE.csv vs 08_docs/EXTRACTION_SCHEMA_v1.md")
    lines.append("Status: %s" % overall)
    lines.append("")
    lines.append("## Summary")
    lines.append("| check | value |")
    lines.append("|---|---|")
    lines.append("| Rows | %d |" % n_rows)
    lines.append("| Expected | %d |" % EXPECTED_ROWS)
    lines.append("| Structure | %s |" % structure_status)
    lines.append("| Duplicate IDs | %d |" % n_dup)
    lines.append("| Empty required fields | %d |" % empty_required)
    lines.append("")
    lines.append("## Structure detail")
    lines.append("- Schema columns (ordered, %d): %s" % (len(schema_cols), ", ".join(schema_cols)))
    lines.append("- Header columns (ordered, %d): %s" % (len(header), ", ".join(header)))
    if missing_cols:
        lines.append("- MISSING from header: %s" % ", ".join(missing_cols))
    if extra_cols:
        lines.append("- EXTRA in header (not in schema): %s" % ", ".join(extra_cols))
    if structure_ok:
        lines.append("- Header matches schema exactly (names and order).")
    lines.append("")
    if dup_ids:
        lines.append("## Duplicate IDs")
        for d in dup_ids:
            lines.append("- %s" % d)
        lines.append("")
    if empty_detail:
        lines.append("## Empty required fields (first 50)")
        for rid, col in empty_detail[:50]:
            lines.append("- %s : %s" % (rid, col))
        lines.append("")
    lines.append("## Notes")
    lines.append("- Row count is informational at Phase 5 (master is empty by design);")
    lines.append("  it becomes an EXIT condition (== %d) at Phase 6 close." % EXPECTED_ROWS)
    lines.append("- Structure compares against EXTRACTION_SCHEMA_v1.md (the approved target schema).")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    # stdout summary
    print("Rows: %d" % n_rows)
    print("Expected: %d" % EXPECTED_ROWS)
    print("Structure: %s" % structure_status)
    print("Duplicate IDs: %d" % n_dup)
    print("Empty required fields: %d" % empty_required)
    print("Overall: %s" % overall)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
