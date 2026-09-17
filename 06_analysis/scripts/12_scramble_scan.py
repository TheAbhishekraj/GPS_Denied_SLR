#!/usr/bin/env python3
"""12_scramble_scan.py — find PDFs whose text layer is character-shifted.

Discovery: REC_0115 extracts as `/RZ&RPSXWDWLRQDO'DWD)XVLRQ$SSURDFK8VLQJ`,
which is `Low Computational Data Fusion Approach Using` put through a Caesar
shift of +29 on the byte value (mod 128):

    '/' 0x2F + 29 = 0x4C 'L'
    'R' 0x52 + 29 = 0x6F 'o'
    'Z' 0x5A + 29 = 0x77 'w'
    0x03 + 29     = 0x20 ' '

This is a font-encoding failure, not a wrong file: the PDF *is* the right paper,
but naive extraction yields gibberish, so every field derived from it would be
wrong. This script scans every PDF for the defect and reports the shift that
restores readable English, so damaged papers are recovered instead of being
silently mis-extracted.

Method: readability = fraction of whitespace tokens that look like English
(>= 2 vowels, all letters, or a common stopword). Score pages 1-2 raw; if the
score is below THRESHOLD, brute-force shifts 1..94 and report the best.

Read-only. Writes a CSV and prints a summary.

Usage:
    python 06_analysis/scripts/12_scramble_scan.py
    python 06_analysis/scripts/12_scramble_scan.py --out 06_analysis/output/x.csv
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
DEFAULT_OUT = REPO / "06_analysis" / "output" / "scramble_scan.csv"

THRESHOLD = 0.55          # below this, the text layer is considered damaged
MAX_FRONT_PAGES = 2

COMMON = {
    "the", "of", "and", "in", "for", "with", "a", "to", "on", "is", "are",
    "we", "this", "that", "as", "by", "an", "be", "it", "from", "or", "at",
    "our", "can", "has", "have", "not", "which", "using", "based", "system",
    "abstract", "introduction", "paper", "present", "results", "method",
}


def readable(token: str) -> bool:
    t = token.lower()
    if t in COMMON:
        return True
    if len(t) < 3:
        return True
    if not t.isalpha():
        return False
    return sum(1 for c in t if c in "aeiou") >= 2


def readability(text: str) -> float:
    toks = [t for t in re.split(r"\s+", text) if len(t) >= 3]
    if not toks:
        return 0.0
    return sum(1 for t in toks if readable(t)) / len(toks)


def shift_text(text: str, amount: int, modulus: int = 128) -> str:
    """Caesar-shift every code point below `modulus` by `amount`."""
    out = []
    for ch in text:
        code = ord(ch)
        if code < modulus:
            out.append(chr((code + amount) % modulus))
        else:
            out.append(ch)
    return "".join(out)


def front_text(doc) -> tuple[str, int]:
    pages = min(MAX_FRONT_PAGES, doc.page_count)
    parts = [doc[i].get_text() for i in range(pages)]
    return "\n".join(parts), doc.page_count


def investigate(text: str) -> tuple[float, int, float]:
    """Return (raw_score, best_shift, best_shift_score)."""
    raw = readability(text)
    best_shift, best_score = 0, raw
    if raw < THRESHOLD:
        for amount in range(1, 95):
            score = readability(shift_text(text, amount))
            if score > best_score:
                best_shift, best_score = amount, score
    return raw, best_shift, best_score


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        rec: dict[str, object] = {
            "id": pdf.stem,
            "raw_score": 0.0,
            "scrambled": False,
            "best_shift": 0,
            "best_shift_score": 0.0,
        }
        try:
            with fitz.open(pdf) as doc:
                text, _ = front_text(doc)
        except Exception as exc:  # noqa: BLE001 - log, don't fail the scan
            rec["scrambled"] = None
            rec["best_shift"] = f"parse error: {type(exc).__name__}"
            rows.append(rec)
            continue
        raw, shift, score = investigate(text)
        rec["raw_score"] = round(raw, 4)
        rec["best_shift_score"] = round(score, 4)
        rec["scrambled"] = raw < args.threshold and shift > 0
        rec["best_shift"] = shift
        rows.append(rec)

    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    n = len(rows)
    bad = [r for r in rows if r["scrambled"]]
    print(f"scanned: {n} pdfs")
    print(f"scrambled: {len(bad)}")
    for r in bad[:30]:
        print(f"  {r['id']}: raw={r['raw_score']} shift={r['best_shift']} "
              f"score={r['best_shift_score']}")
    print(f"wrote: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())