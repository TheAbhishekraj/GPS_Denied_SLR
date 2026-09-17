#!/usr/bin/env python3
"""09c_batch_digest.py — compact multi-paper digest for batch extraction.

`09b_evidence_digest.py` prints ~30k characters for one paper, which is right for
a careful single read but cannot drive a 171-paper run. This prints a *compact*
digest for several papers in one call, so a batch of ~10 papers fits in a single
reading pass. It trades the full page-marked text for the blocks that actually
decide field values:

    - the already-audited master-CSV columns (identity, categoricals, qa_*)
    - the abstract region (start of body)
    - table / figure captions
    - metric lines (keyword + number, the numeric evidence)
    - statement lines (limitation / failure / future-work sentences)

Everything printed keeps its page marker, so `extraction_source` stays citable.

Usage:
    python 06_analysis/scripts/09c_batch_digest.py --first 10
    python 06_analysis/scripts/09c_batch_digest.py --ids REC_0035 REC_0502
    python 06_analysis/scripts/09c_batch_digest.py --numeric --first 10
    python 06_analysis/scripts/09c_batch_digest.py --remaining --first 10
"""

from __future__ import annotations

import argparse
import csv
import sys
from importlib import import_module
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
digest = import_module("09b_evidence_digest")

REPO = Path(__file__).resolve().parents[2]
WORKBOOKS = REPO / "06_analysis" / "output" / "workbooks"
EVIDENCE_CSV = REPO / "02_data_processed" / "MASTER_EVIDENCE_V1.csv"
PROBE_CSV = (
    REPO / "06_analysis" / "output" / "pdf_numeric_probe_v1"
    / "pdf_numeric_probe_v1.csv"
)

CAPTION_CAP = 220
METRIC_CAP = 130
STATEMENT_CAP = 230


def clip(text: str, cap: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= cap else text[: cap - 1] + "\u2026"


def numeric_ids() -> list[str]:
    if not PROBE_CSV.exists():
        return []
    with PROBE_CSV.open(newline="", encoding="utf-8") as fh:
        return [
            r["id"] for r in csv.DictReader(fh)
            if r["any_accuracy_numeric"] == "True"
        ]


def done_ids() -> set[str]:
    if not EVIDENCE_CSV.exists():
        return set()
    with EVIDENCE_CSV.open(newline="", encoding="utf-8") as fh:
        return {r["id"] for r in csv.DictReader(fh)}


def all_ids() -> list[str]:
    with digest.MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        return [r["id"] for r in csv.DictReader(fh)]


def show(pid: str, max_captions: int, max_metrics: int, max_stmts: int,
         opening: int, out=None) -> None:
    def emit(line: str = "") -> None:
        if out is None:
            print(line)
        else:
            out.write(line + "\n")

    wb = WORKBOOKS / f"{pid}.md"
    if not wb.exists():
        emit(f"--- {pid}: NO WORKBOOK ---")
        return
    parts = digest.split_workbook(wb.read_text(encoding="utf-8"))
    rec = digest.master_row(pid) or {}

    emit(f"\n############ {pid} ############")
    emit(f"title   : {rec.get('title')}")
    emit(f"authors : {clip(str(rec.get('authors', '')), 160)}")
    emit(f"year    : {rec.get('year')}   venue: {rec.get('venue')}")
    emit(f"doi     : {rec.get('doi')}   domain: {rec.get('application_domain')}")
    emit(f"method  : {rec.get('primary_method')} / {rec.get('method_category')}")
    emit(f"platform: {rec.get('platform_type')}   multi_agent: {rec.get('multi_agent')}")
    emit(f"sensors : {rec.get('sensor_list')}")
    emit(f"environ : {rec.get('environment')} / {rec.get('experiment_type')} / "
         f"{rec.get('real_or_sim')}")
    emit(f"ate_rmse_m: {rec.get('ate_rmse_m')}   metrics: {rec.get('metrics_reported')}")
    emit(f"qa      : {rec.get('qa_rigor')}/{rec.get('qa_reporting')}/"
         f"{rec.get('qa_baseline')}/{rec.get('qa_repro')} = {rec.get('qa_total')} "
         f"{rec.get('qa_tier')} | {rec.get('citation_tier')}")
    emit(f"master_note: {clip(str(rec.get('notes', '')), 300)}")

    caps = [ln for ln in parts.get("captions", "").splitlines()[2:] if ln.strip()]
    emit(f"-- CAPTIONS ({len(caps)}) --")
    for ln in caps[:max_captions]:
        emit(f"  {clip(ln, CAPTION_CAP)}")

    mets = [ln for ln in parts.get("metrics", "").splitlines()[2:] if ln.strip()]
    emit(f"-- METRIC LINES ({len(mets)}) --")
    for ln in mets[:max_metrics]:
        emit(f"  {clip(ln, METRIC_CAP)}")

    body = parts.get("body", "")
    start = body.find("### [[page 1]]")
    body = body[start:] if start >= 0 else body
    emit("-- OPENING --")
    emit(clip(body[:opening], opening))

    emit("-- STATEMENTS --")
    seen: set[str] = set()
    shown = 0
    for line in body.splitlines():
        low = line.lower()
        if len(line) < 45 or len(line) > 320:
            continue
        if not any(h in low for h in digest.STATEMENT_HINTS):
            continue
        key = line[:70]
        if key in seen:
            continue
        seen.add(key)
        emit(f"  {clip(line, STATEMENT_CAP)}")
        shown += 1
        if shown >= max_stmts:
            break


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="*", default=None)
    ap.add_argument("--first", type=int, default=10)
    ap.add_argument("--numeric", action="store_true",
                    help="only papers the probe flagged as numeric")
    ap.add_argument("--remaining", action="store_true",
                    help="skip ids already committed to the evidence CSV")
    ap.add_argument("--captions", type=int, default=14)
    ap.add_argument("--metrics", type=int, default=14)
    ap.add_argument("--statements", type=int, default=7)
    ap.add_argument("--opening", type=int, default=1200)
    ap.add_argument("--out", default=None,
                    help="write UTF-8 to this path instead of stdout")
    args = ap.parse_args()

    if args.ids:
        ids = args.ids
    elif args.numeric:
        ids = numeric_ids()
    else:
        ids = all_ids()

    if args.remaining:
        done = done_ids()
        ids = [i for i in ids if i not in done]

    batch = ids[: args.first]
    handle = None
    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = REPO / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        handle = out_path.open("w", encoding="utf-8", newline="\n")

    def say(line: str) -> None:
        if handle is None:
            print(line)
        else:
            handle.write(line + "\n")

    try:
        say(f"batch of {len(batch)} (from {len(ids)} candidates; "
            f"{len(done_ids())} already committed)")
        for pid in batch:
            show(pid, args.captions, args.metrics, args.statements,
                 args.opening, handle)
        say(f"\nremaining after this batch: {len(ids) - len(batch)}")
    finally:
        if handle is not None:
            handle.close()
            size = Path(args.out).stat().st_size if Path(args.out).is_absolute() \
                else (REPO / args.out).stat().st_size
            print(f"wrote {args.out} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())