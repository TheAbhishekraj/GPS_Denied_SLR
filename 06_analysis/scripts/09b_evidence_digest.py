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
import re
import sys
import unicodedata
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


def ascii_safe(text: str) -> str:
    """Make PDF text printable on a cp1252 console.

    PDFs carry fi/fl ligatures (U+FB01/U+FB02), Greek letters and math symbols.
    Printing them raw yields mojibake such as `∩¼éight`, which is unreadable and
    can hide a real word. Map the common ligatures first, then transliterate.
    """
    for src, dst in (
        ("\ufb00", "ff"), ("\ufb01", "fi"), ("\ufb02", "fl"),
        ("\ufb03", "ffi"), ("\ufb04", "ffl"), ("\u2013", "-"),
        ("\u2014", "-"), ("\u2212", "-"), ("\u00d7", "x"),
    ):
        text = text.replace(src, dst)
    return unicodedata.normalize("NFKD", text).encode(
        "ascii", "replace"
    ).decode("ascii")


def emit(text: str) -> None:
    print(ascii_safe(text))


def main() -> int:
    # Windows consoles default to cp1252; PDF text carries ligatures and Greek
    # letters, so force UTF-8 on stdout and transliterate before printing.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+", help="one or more paper ids")
    ap.add_argument("--opening", type=int, default=4000)
    ap.add_argument("--closing", type=int, default=3500)
    ap.add_argument("--max-metrics", type=int, default=45)
    ap.add_argument("--max-captions", type=int, default=40)
    ap.add_argument("--slim", action="store_true",
                    help="batch mode: 700/500 windows, 12 metrics, 10 captions")
    args = ap.parse_args()
    if args.slim:
        args.opening, args.closing = 700, 500
        args.max_metrics, args.max_captions = 12, 10

    rc = 0
    for pid in args.ids:
        rc |= digest(pid, args)
    return rc


def digest(pid: str, args: argparse.Namespace) -> int:
    wb = WORKBOOKS / f"{pid}.md"
    if not wb.exists():
        emit(f"no workbook for {pid}")
        return 2
    text = wb.read_text(encoding="utf-8")
    parts = split_workbook(text)
    rec = master_row(pid) or {}

    emit(f"===== DIGEST {pid} =====")
    emit(f"title            : {rec.get('title') or 'NOT_REPORTED'}")
    emit(f"authors          : {rec.get('authors') or 'NOT_REPORTED'}")
    emit(f"year/venue/doi   : {rec.get('year')} | {rec.get('venue')} | "
         f"{rec.get('doi')}")
    emit(f"qa (master)      : rigor={rec.get('qa_rigor')} "
         f"reporting={rec.get('qa_reporting')} baseline={rec.get('qa_baseline')} "
         f"repro={rec.get('qa_repro')} total={rec.get('qa_total')} "
         f"tier={rec.get('qa_tier')} citation={rec.get('citation_tier')}")
    emit(f"master method    : {rec.get('primary_method')} / "
         f"{rec.get('method_category')}")
    emit(f"master sensors   : {rec.get('sensor_list')}")
    emit(f"master environ   : {rec.get('environment')} / "
         f"{rec.get('experiment_type')} / {rec.get('real_or_sim')}")
    emit(f"master ate_rmse_m: {rec.get('ate_rmse_m')}")
    emit(f"master metrics   : {rec.get('metrics_reported')}")
    emit(f"platform/app     : {rec.get('platform_type')} / "
         f"{rec.get('application_domain')} / multi_agent={rec.get('multi_agent')}")
    emit(f"pdf pages        : {rec.get('pdf_pages')}")

    for key, label, cap in (
        ("sections", "SECTIONS", 30),
        ("captions", "CAPTIONS", args.max_captions),
        ("metrics", "METRIC LINES", args.max_metrics),
        ("numbered", "NUMBERED LINES", 20),
    ):
        block = parts.get(key, "")
        lines = [ln for ln in block.splitlines()[2:] if ln.strip()]
        emit(f"\n----- {label} ({len(lines)}) -----")
        if len(lines) > cap:
            head = lines[: cap // 2]
            tail = lines[-(cap // 2):]
            emit("\n".join(head))
            emit(f"... [{len(lines) - cap} lines elided] ...")
            emit("\n".join(tail))
        else:
            emit("\n".join(lines))

    body_start = parts.get("body", "").find("### [[page 1]]")
    body = parts.get("body", "")[body_start:] if body_start >= 0 else ""

    # Limitations / future work live BEFORE the reference list. Cut the
    # bibliography out of the closing window and out of the statement scan,
    # otherwise the digest's most useful sections are buried in citations.
    refs = None
    for m in re.finditer(r"(?mi)^\s*(references|bibliography|reference list)\s*$",
                         body):
        refs = m.start()
    main_body = body[:refs] if refs is not None else body

    emit("\n----- OPENING -----")
    emit(body[: args.opening])
    emit("\n----- CLOSING (references excluded) -----")
    emit(main_body[-args.closing:])

    emit("\n----- STATEMENT LINES -----")
    seen = set()
    for line in main_body.splitlines():
        line = " ".join(line.split())
        low = line.lower()
        if len(line) < 40 or len(line) > 400 or not any(
            h in low for h in STATEMENT_HINTS
        ):
            continue
        key = line[:80]
        if key in seen:
            continue
        seen.add(key)
        emit(f"- {line}")
        if len(seen) >= 6:
            break
    emit(f"===== END {pid} =====")
    return 0


if __name__ == "__main__":
    sys.exit(main())