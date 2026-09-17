#!/usr/bin/env python3
"""08e_post_extraction_checks.py — runs Amendment V9.1 (a/b/c) and M1/M2/M3.

Implements, in Python, the post-extraction checks that
`08_docs/MASTER_VERIFICATION_PROTOCOL.md` specifies in PowerShell:

    V9.1a  family coverage with numeric data      (>= 5 families required)
    V9.1b  reporting-gap count                    (mandatory manuscript finding)
    V9.1c  reporting-gap by year                  (mandatory manuscript table)
    M1     44/127 split survives extraction       (expect 44 +/- 5)
    M2     family spread                          (alias of V9.1a)
    M3     5 random non-numeric papers to spot-read

The protocol names this script as the preferred way to run V9.1a because the
PowerShell form has a scalar/array hazard: `$withNum` produced by a `foreach`
statement (not a pipeline) collapses to a scalar for a single-element result,
so `.Count` yields `$null`, which is neither `-ge 1` nor `< 1`, and the family
is silently dropped. Python has no such hazard.

Why a unit anchor is required
-----------------------------
`metrics_reported` in extracted_master_v2.csv cannot be used as numeric
evidence. It claims `ATE_RMSE` for 170 / 171 rows, while the pre-flight probe
finds the metric ATE in only 6 papers and an ATE value in 1. A value counts
here only when it is a number with an explicit unit, or a `%` figure.

Usage:
    python 06_analysis/scripts/08e_post_extraction_checks.py
    python 06_analysis/scripts/08e_post_extraction_checks.py --json out.json
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVIDENCE_CSV = REPO / "02_data_processed" / "MASTER_EVIDENCE_V1.csv"
PER_PAPER = REPO / "03_extraction" / "per_paper"

NUMERIC_FIELDS = (
    "best_ate_rmse", "best_rpe", "drift_rate_pct", "success_rate_pct",
    "improvement_vs_baseline_pct", "other_metric_value",
)
UNIT = re.compile(
    r"^\s*\d+(?:\.\d+)?\s*(?:m\b|cm\b|mm\b|km\b|%|deg|°|rad\b)", re.I
)
BARE = re.compile(r"^\s*\d+(?:\.\d+)?\s*$")


def is_numeric(row: dict[str, str], field: str) -> bool:
    val = (row.get(field) or "").strip()
    if not val or val.upper() in ("NOT_REPORTED", "NONE_REPORTED"):
        return False
    if field in ("best_ate_rmse", "best_rpe", "other_metric_value"):
        return bool(UNIT.match(val)) or bool(BARE.match(val))
    return bool(re.match(r"^\s*\d+(?:\.\d+)?\s*%?\s*$", val)) or bool(UNIT.match(val))


def has_any_numeric(row: dict[str, str]) -> bool:
    return any(is_numeric(row, f) for f in NUMERIC_FIELDS)


def load() -> list[dict[str, str]]:
    with EVIDENCE_CSV.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def norm_year(raw: str) -> str:
    m = re.search(r"(19|20)\d{2}", raw or "")
    return m.group(0) if m else "UNKNOWN"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="also write the results as JSON here")
    args = ap.parse_args()

    if not EVIDENCE_CSV.exists():
        print(f"missing {EVIDENCE_CSV} — nothing to check")
        return 2
    rows = load()
    if not rows:
        print("MASTER_EVIDENCE_V1.csv has a header but no data rows")
        return 2

    n = len(rows)
    numeric = [r for r in rows if has_any_numeric(r)]
    non_numeric = [r for r in rows if not has_any_numeric(r)]
    report: dict[str, object] = {"n_rows": n}

    print("=" * 68)
    print(f"V9.1 — inference viability on {n} rows")
    print("=" * 68)

    # ---- V9.1a family coverage ------------------------------------------
    fams: dict[str, list[dict[str, str]]] = {}
    for r in rows:
        fams.setdefault((r.get("approach_family") or "NOT_REPORTED").strip(), []).append(r)
    print("\nV9.1a  family coverage with numeric data")
    print(f"  {'Family':<34}{'Papers':>7}{'Numeric':>9}")
    table = []
    for fam, group in sorted(
        fams.items(), key=lambda kv: (-sum(1 for r in kv[1] if has_any_numeric(r)), kv[0])
    ):
        k = sum(1 for r in group if has_any_numeric(r))
        table.append({"family": fam, "papers": len(group), "with_numeric": k})
        print(f"  {fam[:33]:<34}{len(group):>7}{k:>9}")
    fam_ok = sum(1 for t in table if t["with_numeric"] >= 1)
    verdict_a = "PASS" if fam_ok >= 5 else "FAIL"
    print(f"  families with >=1 numeric paper: {fam_ok}  -> V9.1a {verdict_a}")
    report["v9_1a"] = {
        "families": table, "families_with_numeric": fam_ok, "verdict": verdict_a,
    }

    # ---- V9.1b reporting gap --------------------------------------------
    pct_none = 100.0 * len(non_numeric) / n
    print("\nV9.1b  reporting gap")
    print(f"  with a unit-anchored accuracy metric: {len(numeric)} / {n} "
          f"({100 - pct_none:.1f}%)")
    print(f"  with none:                            {len(non_numeric)} / {n} "
          f"({pct_none:.1f}%)")
    print("  manuscript MUST state the 'with none' count verbatim.")
    report["v9_1b"] = {
        "with_numeric": len(numeric),
        "with_none": len(non_numeric),
        "pct_with_none": round(pct_none, 1),
        "manuscript_paragraph_required": True,
    }

    # ---- V9.1c by year ---------------------------------------------------
    years: dict[str, list[dict[str, str]]] = {}
    for r in rows:
        years.setdefault(norm_year(r.get("year", "")), []).append(r)
    print("\nV9.1c  reporting gap by year")
    print(f"  {'Year':<8}{'Papers':>7}{'Numeric':>9}{'Pct':>8}")
    ytable = []
    for year in sorted(years):
        g = years[year]
        k = sum(1 for r in g if has_any_numeric(r))
        pct = round(100.0 * k / len(g), 1) if g else 0.0
        ytable.append(
            {"year": year, "papers": len(g), "with_numeric": k, "pct_numeric": pct}
        )
        print(f"  {year:<8}{len(g):>7}{k:>9}{pct:>7}%")
    print("  manuscript MUST include this table in the reporting-practice subsection.")
    report["v9_1c"] = {"by_year": ytable}

    # ---- M1 44/127 split -------------------------------------------------
    print("\nM1  44/127 split survives extraction")
    lo, hi = 38, 61
    verdict_m1 = "PASS" if lo <= len(numeric) <= hi else "INVESTIGATE"
    print(f"  with numeric: {len(numeric)} / {n}   "
          f"(probe expectation 44, band {lo}-{hi})")
    print(f"  -> M1 {verdict_m1}")
    if len(numeric) < 44:
        print("  <44: extraction may be too strict — re-read the metric tables.")
    if len(numeric) > 60:
        print("  >60: extraction may be inventing values — spot-check 5 rows by hand.")
    report["m1"] = {
        "with_numeric": len(numeric), "band": [lo, hi], "verdict": verdict_m1,
    }

    # ---- M3 sample -------------------------------------------------------
    rng = random.Random(42)
    sample = rng.sample(non_numeric, min(5, len(non_numeric))) if non_numeric else []
    print("\nM3  5 random non-numeric papers for manual spot-read (seed 42)")
    for r in sample:
        md = PER_PAPER / f"{r['id']}.md"
        print(f"  {r['id']}  md={'yes' if md.exists() else 'MISSING'}  "
              f"{(r.get('title') or '')[:58]}")
    print("  For each: confirm best_ate_rmse is NOT_REPORTED, then check by eye")
    print("  that the paper genuinely reports no numeric accuracy.")
    report["m3"] = {"sample": [r["id"] for r in sample]}

    print("\n" + "=" * 68)
    print(f"V9.1a {verdict_a} | M1 {verdict_m1} | V9.1b/V9.1c are manuscript gates")
    print("=" * 68)

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"json: {args.json}")
    return 0 if (fam_ok >= 5 and verdict_m1 == "PASS") else 1


if __name__ == "__main__":
    sys.exit(main())