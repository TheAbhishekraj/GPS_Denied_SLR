#!/usr/bin/env python3
"""09b_evidence_digest.py — compact reading digest for one paper.

Reading a full workbook costs ~30,000 characters per paper, which does not scale
to 171 papers. This prints only the evidence an extractor actually needs, with
page citations, so every CSV field can be filled from a citable source:

    - identity block (from extracted_master_v2.csv: title, year, venue, qa_*)
    - sections detected, with pages
    - table / figure captions, with pages
    - ALL metric lines (keyword + number)
    - ALL numbered lines (table-row shaped)
    - OPENING  ~4,000 chars  -> abstract, problem setting, prior work
    - CLOSING  ~3,500 chars  -> discussion, limitations, future work
    - STATEMENT lines        -> sentences containing limit/future/drawback/fail

Usage:
    python 06_analysis/scripts/09b_evidence_digest.py REC_1573
    python 06_analysis/scripts/09b_evidence_digest.py REC_1573 --max 60
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WORKBOOKS = REPO / "06_analysis" / "output" / "workbooks"
MASTER_CSV = REPO / "02_data_processed" / "extracted_master_v2.csv"

STATEMENT_HINTS = (
    "limitation", "limited to", "future work", "drawback", "shortcoming",
    "fails", "fail to", "degrade", "difficult", "challeng", "we do not",
    "not been", "remains",
)


def master_row(pid: str) -> dict[str, str] | None:
    with MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["id"] == pid:
                return row
    return None


def split_workbook(text: str) -> dict[str, str]:
    """Carve the workbook into its titled blocks."""
    markers = [
        ("sections", "## 3. SECTIONS"),
        ("captions", "## 4. CAPTIONS"),
        ("metrics", "## 5. METRIC LINES"),
        ("numbered", "## 6. NUMBERED LINES"),
        ("body", "## 2. FULL PAGE-MARKED TEXT"),
    ]
    parts: dict[str, str] = {}
    positions = []
    for key, marker in markers:
        idx = text.find(marker)
        positions.append((idx, key))
    positions.sort()
    for i, (idx, key) in enumerate(positions):
        if idx < 0:
            parts[key] = ""
            continue
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        parts[key] = text[idx:end]
    return parts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--opening", type=int, default=4000)
    ap.add_argument("--closing", type=int, default=3500)
    ap.add_argument("--max-metrics", type=int, default=45)
    args = ap.parse_args()

    wb = WORKBOOKS / f"{args.id}.md"
    if not wb.exists():
        print(f"no workbook for {args.id}")
        return 2
    text = wb.read_text(encoding="utf-8")
    parts = split_workbook(text)
    rec = master_row(args.id) or {}

    print(f"===== DIGEST {args.id} =====")
    print(f"source PDF       : 05_papers_fulltext/{args.id}.pdf")
    print(f"title (master)   : {rec.get('title', 'NOT_REPORTED')}")
    print(f"year (master)    : {rec.get('year', 'NOT_REPORTED')}")
    print(f"venue (master)   : {rec.get('venue', 'NOT_REPORTED')}")
    print(f"doi (master)     : {rec.get('doi', 'NOT_REPORTED')}")
    print(f"qa_* (master)    : rigor={rec.get('qa_rigor')} "
          f"reporting={rec.get('qa_reporting')} baseline={rec.get('qa_baseline')} "
          f"repro={rec.get('qa_repro')} total={rec.get('qa_total')} "
          f"tier={rec.get('qa_tier')} citation={rec.get('citation_tier')}")
    print(f"master method    : {rec.get('primary_method')} / "
          f"{rec.get('method_category')}")
    print(f"master sensors   : {rec.get('sensor_list')}")
    print(f"master environ   : {rec.get('environment')} / "
          f"{rec.get('experiment_type')} / {rec.get('real_or_sim')}")
    print(f"master ate_rmse_m: {rec.get('ate_rmse_m')}")
    print(f"master metrics   : {rec.get('metrics_reported')}")
    print(f"platform         : {rec.get('platform_type')}")

    for key, label in (
        ("sections", "SECTIONS"),
        ("captions", "CAPTIONS"),
        ("metrics", "METRIC LINES"),
        ("numbered", "NUMBERED LINES"),
    ):
        block = parts.get(key, "")
        lines = [ln for ln in block.splitlines()[2:] if ln.strip()]
        print(f"\n----- {label} ({len(lines)}) -----")
        if key == "metrics" and len(lines) > args.max_metrics:
            head = lines[: args.max_metrics // 2]
            tail = lines[-(args.max_metrics // 2):]
            print("\n".join(head))
            print(f"... [{len(lines) - args.max_metrics} lines elided] ...")
            print("\n".join(tail))
        else:
            print("\n".join(lines))

    body_start = parts.get("body", "").find("### [[page 1]]")
    body = parts.get("body", "")[body_start:] if body_start >= 0 else ""
    print("\n----- OPENING -----")
    print(body[: args.opening])
    print("\n----- CLOSING -----")
    print(body[-args.closing:])

    print("\n----- STATEMENT LINES -----")
    seen = set()
    for line in body.splitlines():
        low = line.lower()
        if len(line) < 40 or len(line) > 400 or not any(h in low for h in STATEMENT_HINTS):
            continue
        key = line[:80]
        if key in seen:
            continue
        seen.add(key)
        print(f"- {line}")
    print(f"===== END {args.id} =====")
    return 0


if __name__ == "__main__":
    sys.exit(main())