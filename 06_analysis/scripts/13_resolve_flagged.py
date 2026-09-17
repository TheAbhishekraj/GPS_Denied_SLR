#!/usr/bin/env python3
"""13_resolve_flagged.py — definitively resolve the 6 identity-flag papers.

For each flagged id the audit v2 could not confirm (TITLE_ONLY / NO_EVIDENCE),
pull the PDF's own first-page title block and any DOI found in the first three
pages, side by side with the master row. That raw evidence is the basis for the
verdict, which is written by a human after reading this output.

Handles REC_0115's font-encoding defect by also decoding a Caesar shift of +29
(the rotation observed on its headline).

Usage:    python 06_analysis/scripts/13_resolve_flagged.py > 06_analysis/output/flagged_resolution.txt
"""

from __future__ import annotations

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
MASTER_CSV = REPO / "02_data_processed" / "extracted_master_v2.csv"
AUDIT_CSV = REPO / "06_analysis" / "output" / "pdf_identity_audit" / "identity_audit_v2.csv"

FLAGGED = [
    "REC_0023", "REC_0035", "REC_0053", "REC_0115", "REC_0274", "REC_1217",
    "REC_1667",
]

RE_DOI = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
RE_SHIFT = re.compile(r"^\s*(?:/RZ|&RPS|'DWD|)")  # observed scrambled starts


def caesar_decrypt(text: str, shift: int = 29) -> str:
    """Rotate ASCII letters back by `shift`. Only affects A-Z/a-z."""
    out = []
    for ch in text:
        if "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") - shift) % 26 + ord("A")))
        elif "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") - shift) % 26 + ord("a")))
        else:
            out.append(ch)
    return "".join(out)


def pdf_page1_raw(pid: str, pages: int = 3) -> str:
    pdf = PDF_DIR / f"{pid}.pdf"
    if not pdf.exists():
        return "[NO PDF]"
    with fitz.open(pdf) as doc:
        n = min(pages, doc.page_count)
        return "\n".join(doc[i].get_text() for i in range(n))


def clean(text: str) -> str:
    return "\n".join(ln.strip() for ln in text.splitlines() if ln.strip())


def head_block(text: str, max_lines: int = 10) -> str:
    """Upper part of the page: title + authors usually live above the abstract."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cap = min(max_lines, len(lines))
    return "\n".join(lines[:cap])


def main() -> int:
    master: dict[str, dict[str, str]] = {}
    with MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            master[row["id"]] = row

    print("FLAGGED-PAPER RESOLUTION EVIDENCE (from PDFs, not from the audit)")
    print("=" * 100)
    for pid in FLAGGED:
        raw = pdf_page1_raw(pid)
        also = caesar_decrypt(raw) if pid == "REC_0115" else ""
        dois = sorted(set(RE_DOI.findall(raw)))[:4]
        print(f"\n### {pid}")
        print(f"MASTER  title : {master[pid]['title']}")
        print(f"MASTER  year  : {master[pid]['year']}   doi: {master[pid]['doi']}")
        print("-" * 70)
        print("PDF FIRST PAGE (normalized):")
        print(head_block(clean(raw), 12))
        if also:
            print("\nPDF FIRST PAGE (Caesar -29 decoded):")
            print(head_block(clean(also), 12))
        print(f"\nPDF  DOI(s) in first {3} pages: {dois if dois else 'none found'}")
        print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())