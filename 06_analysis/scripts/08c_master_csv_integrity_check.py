#!/usr/bin/env python3
"""08c_master_csv_integrity_check.py — is extracted_master_v2.csv still canonical?

Gate G2/G6 and Check V5/V7 of the master protocol all lean on
`02_data_processed/extracted_master_v2.csv` being the frozen categorical source.
`git status` reports this file as modified in the working tree, and the diff is a
*content* change (QA subscores), not a line-ending change. That means the
canonical vectors quoted in MASTER_EXTRACTION_PROMPT.md might no longer hold.

This script answers, without modifying anything:

  1. Does the committed (HEAD) copy match the canonical vectors?
  2. Does the working-tree copy match the canonical vectors?
  3. Which rows differ between the two, and in which columns?

Canonical vectors under test:
  N = 171
  qa_tier:       Q-high 38 | Q-medium 84 | Q-low 49
  citation_tier: Core 35 | Important 87 | Peripheral 49
  real_or_sim:   Real_World 22 | Simulation 78 | Both 71
  170 PASS + 1 PASS_EXCEPTION (REC_1137)

Usage:  python 06_analysis/scripts/08c_master_csv_integrity_check.py
"""

from __future__ import annotations

import csv
import io
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REL = "02_data_processed/extracted_master_v2.csv"
CANON = {
    "rows": 171,
    "qa_tier": {"Q-high": 38, "Q-medium": 84, "Q-low": 49},
    "citation_tier": {"Core": 35, "Important": 87, "Peripheral": 49},
    "real_or_sim": {"Real_World": 22, "Simulation": 78, "Both": 71},
}


def load_rows(text: str) -> list[dict[str, str]]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return list(csv.DictReader(io.StringIO(text)))


def git_show(rel: str) -> str:
    out = subprocess.run(
        ["git", "--no-pager", "show", f"HEAD:{rel}"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        check=True,
    )
    return out.stdout


def report(label: str, rows: list[dict[str, str]]) -> bool:
    ok = True
    print(f"\n=== {label} ===")
    print(f"rows: {len(rows)}  (canonical {CANON['rows']})", end="")
    if len(rows) != CANON["rows"]:
        print("   <-- MISMATCH")
        ok = False
    else:
        print("   OK")

    for col in ("qa_tier", "citation_tier", "real_or_sim"):
        got = Counter(r.get(col, "") for r in rows)
        want = CANON[col]
        same = all(got.get(k, 0) == v for k, v in want.items()) and \
            all(k in want for k in got)
        flag = "OK" if same else "<-- MISMATCH"
        print(f"{col}: {dict(got)}  want {want}  {flag}")
        if not same:
            ok = False
    return ok


def main() -> int:
    committed = load_rows(git_show(REL))
    working = load_rows(Path(REPO / REL).read_text(encoding="utf-8"))

    ok_committed = report("HEAD (committed) copy", committed)
    ok_working = report("Working-tree copy", working)

    by_id_c = {r["id"]: r for r in committed}
    by_id_w = {r["id"]: r for r in working}

    ids_only_committed = sorted(set(by_id_c) - set(by_id_w))
    ids_only_working = sorted(set(by_id_w) - set(by_id_c))
    print(f"\nids only in HEAD: {len(ids_only_committed)} {ids_only_committed[:10]}")
    print(f"ids only in working tree: {len(ids_only_working)} "
          f"{ids_only_working[:10]}")

    cols = list(committed[0].keys()) if committed else []
    changed_cols: Counter[str] = Counter()
    changed_ids: list[str] = []
    for pid in sorted(set(by_id_c) & set(by_id_w)):
        diffs = [c for c in cols if by_id_c[pid].get(c) != by_id_w[pid].get(c)]
        if diffs:
            changed_ids.append(pid)
            for c in diffs:
                changed_cols[c] += 1

    print(f"\nrows whose content changed HEAD -> working tree: "
          f"{len(changed_ids)}")
    print("columns touched (count of rows):")
    for col, n in changed_cols.most_common():
        print(f"  {col:<28} {n}")

    for pid in changed_ids[:3]:
        print(f"\nsample diff {pid}:")
        for col in cols:
            a, b = by_id_c[pid].get(col), by_id_w[pid].get(col)
            if a != b:
                print(f"  {col}: {a!r} -> {b!r}")

    print("\n=== VERDICT ===")
    if ok_committed and not ok_working:
        print("HEAD matches the canonical vectors; the working tree does NOT.")
        print("The working tree has been altered after the audit. Extraction must")
        print("NOT proceed until this is resolved: G6/V5 reconcile qa_total against")
        print("this file, so every qa_* value copied from it would be unaudited.")
        return 1
    if ok_committed and ok_working:
        print("Both copies match the canonical vectors; the edit is benign for the")
        print("tier distributions. Still confirm the QA subscores are intended,")
        print("because qa_total is copied verbatim into the evidence CSV.")
        return 0
    print("The committed copy ALSO diverges from the canonical vectors. The")
    print("canonical numbers in MASTER_EXTRACTION_PROMPT.md are stale and must be")
    print("re-derived from the file of record before extraction.")
    return 1


if __name__ == "__main__":
    sys.exit(main())