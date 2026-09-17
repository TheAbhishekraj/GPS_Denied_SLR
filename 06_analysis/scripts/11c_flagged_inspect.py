#!/usr/bin/env python3
"""11c_flagged_inspect.py — dump the opening pages of flagged PDFs.

Used to resolve identity-audit flags by eye, and to detect text-layer damage
(a scrambled font map produces Caesar-shifted gibberish such as
`/RZ&RPSXWDWLRQDO'DWD)XVLRQ$SSURDFK8VLQJ` instead of
`Low Computational Data Fusion Approach Using`).

Prints, per id: page count, the first N characters of pages 1-2, and a
readability score = fraction of whitespace-separated tokens that look like
English words (>= 2 vowels, or a known common word). A score below ~0.55 means
the text layer is damaged and the PDF cannot be extracted without OCR.

Usage:
    python 06_analysis/scripts/11c_flagged_inspect.py --ids REC_0023,REC_0115
    python 06_analysis/scripts/11c_flagged_inspect.py --from-audit
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:  # pragma: no cover
    import fitz  # type: ignore

REPO = Path(__file__).resolve().parents[2]
PDF_DIR = REPO / "05_papers_fulltext"
AUDIT_CSV = (
    REPO / "06_analysis" / "output" / "pdf_identity_audit" / "identity_audit_v2.csv"
)

COMMON = {
    "the", "of", "and", "in", "for", "with", "a", "to", "on", "is", "are",
    "we", "this", "that", "as", "by", "an", "be", "it", "from", "or", "at",
    "our", "can", "has", "have", "not", "which", "using", "based", "system",
}


def readable(token: str) -> bool:
    t = token.lower()
    if t in COMMON:
        return True
    if len(t) < 3:
        return True
    letters = sum(c.isalpha() for c in t)
    if letters != len(t):
        return False
    return sum(1 for c in t if c in "aeiou") >= 2


def score(text: str) -> float:
    toks = [t for t in re.split(r"\s+", text) if len(t) >= 3]
    if not toks:
        return 0.0
    return sum(1 for t in toks if readable(t)) / len(toks)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default="")
    ap.add_argument("--from-audit", action="store_true")
    ap.add_argument("--chars", type=int, default=700)
    ap.add_argument("--out", default=None,
                    help="write UTF-8 to this path instead of stdout. Use this "
                         "rather than PowerShell '>' which emits UTF-16 and "
                         "null-pads every byte.")
    args = ap.parse_args()

    handle = None
    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = REPO / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        handle = out_path.open("w", encoding="utf-8", newline="\n")

    def say(line: str = "") -> None:
        if handle is None:
            print(line)
        else:
            handle.write(line + "\n")

    ids: list[str] = [x.strip() for x in args.ids.split(",") if x.strip()]
    if args.from_audit:
        with AUDIT_CSV.open(newline="", encoding="utf-8") as fh:
            ids = [
                r["id"] for r in csv.DictReader(fh)
                if r["verdict"] in ("TITLE_ONLY", "NO_EVIDENCE")
            ]
    if not ids:
        say("nothing to inspect; pass --ids or --from-audit")
        if handle:
            handle.close()
        return 2

    try:
        for pid in ids:
            pdf = PDF_DIR / f"{pid}.pdf"
            say("=" * 100)
            if not pdf.exists():
                say(f"{pid}: NO PDF")
                continue
            with fitz.open(pdf) as doc:
                pages = doc.page_count
                p1 = doc[0].get_text()
                p2 = doc[1].get_text() if pages > 1 else ""
            joined = p1 + "\n" + p2
            say(f"{pid}  pages={pages}  readability(p1-2)={score(joined):.2f}")
            say(f"--- page 1 (first {args.chars} chars) ---")
            say(p1[: args.chars])
            say(f"--- page 2 (first {args.chars // 2} chars) ---")
            say(p2[: args.chars // 2])
    finally:
        if handle is not None:
            handle.close()
            print(f"wrote {args.out} "
                  f"({(REPO / args.out if not Path(args.out).is_absolute() else Path(args.out)).stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())