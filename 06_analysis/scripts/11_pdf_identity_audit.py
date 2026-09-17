#!/usr/bin/env python3
"""11_pdf_identity_audit.py — does each PDF actually match its master-CSV row?

Why this is load-bearing
-----------------------
Before authoring 171 extraction records it must be proved that
`05_papers_fulltext/<id>.pdf` really is the paper that
`extracted_master_v2.csv` says it is. The first batch digest showed
REC_0023 opening with text from a *different* paper (Khattak et al.,
"Visual-Thermal Landmarks and Inertial Fusion...", arXiv:1903.01656) while the
master row is Variar et al., INSPIRE 2025. If that is systemic, every
downstream column is attached to the wrong paper and the review is void.

Method
------
Title tokens (lowercased, >=4 chars, minus stopwords) from the master row are
matched against the first N pages of the PDF. A paper passes if a high fraction
of its distinctive title tokens appear, OR if the DOI string appears.

This is a heuristic triage, not proof: a pass means "nothing contradictory
found", a FAIL means a human must look.

Outputs (06_analysis/output/pdf_identity_audit/):
    identity_audit.csv
    IDENTITY_AUDIT_REPORT.md

Usage:  python 06_analysis/scripts/11_pdf_identity_audit.py
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
OUT_DIR = REPO / "06_analysis" / "output" / "pdf_identity_audit"

STOP = {
    "with", "from", "that", "this", "using", "based", "into", "their", "there",
    "these", "those", "when", "which", "while", "have", "been", "than", "then",
    "they", "them", "also", "such", "over", "under", "between", "toward",
    "towards", "study", "paper", "approach", "system", "systems",
    "novel", "without", "vehicle", "vehicles",
}

FIRST_PAGES = 3
PASS_RATIO = 0.55
WEAK_RATIO = 0.30


def title_tokens(title: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", title.lower())
    return [w for w in words if w not in STOP]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    with MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        master = list(csv.DictReader(fh))

    for rec in master:
        pid = rec["id"]
        pdf = PDF_DIR / f"{pid}.pdf"
        row: dict[str, object] = {
            "id": pid,
            "pdf_exists": pdf.exists(),
            "title": rec.get("title", ""),
            "pages": 0,
            "tokens": 0,
            "tokens_found": 0,
            "ratio": 0.0,
            "doi_in_text": False,
            "front_text_chars": 0,
            "verdict": "",
            "missing_tokens": "",
        }
        if not pdf.exists():
            row["verdict"] = "NO_PDF"
            rows.append(row)
            continue

        with fitz.open(pdf) as doc:
            row["pages"] = doc.page_count
            n = min(FIRST_PAGES, doc.page_count)
            front = "\n".join(doc[i].get_text() for i in range(n))
        front_low = front.lower()
        row["front_text_chars"] = len(front)

        toks = title_tokens(rec.get("title", ""))
        found = [t for t in toks if t in front_low]
        missing = [t for t in toks if t not in front_low]
        ratio = (len(found) / len(toks)) if toks else 0.0

        doi = (rec.get("doi") or "").strip()
        doi_hit = bool(doi) and doi.lower() in front_low.replace(" ", "")

        row["tokens"] = len(toks)
        row["tokens_found"] = len(found)
        row["ratio"] = round(ratio, 3)
        row["doi_in_text"] = doi_hit
        row["missing_tokens"] = ";".join(missing[:8])

        if len(toks) < 3:
            row["verdict"] = "UNTESTABLE"
        elif doi_hit or ratio >= PASS_RATIO:
            row["verdict"] = "PASS"
        elif ratio >= WEAK_RATIO:
            row["verdict"] = "WEAK"
        else:
            row["verdict"] = "FAIL"
        rows.append(row)

    csv_path = OUT_DIR / "identity_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    def count(v: str) -> int:
        return sum(1 for r in rows if r["verdict"] == v)

    n = len(rows)
    fails = [r for r in rows if r["verdict"] == "FAIL"]
    weaks = [r for r in rows if r["verdict"] == "WEAK"]

    lines = [
        "# IDENTITY_AUDIT_REPORT.md",
        "",
        "Does each `05_papers_fulltext/<id>.pdf` match its master-CSV title?",
        "",
        f"- rows checked: {n}",
        f"- **PASS**: {count('PASS')}",
        f"- **WEAK** (partial title match, needs a glance): {count('WEAK')}",
        f"- **FAIL** (title and PDF disagree): {count('FAIL')}",
        f"- UNTESTABLE (title too short to tokenise): {count('UNTESTABLE')}",
        f"- NO_PDF: {count('NO_PDF')}",
        "",
        "Method: distinctive title tokens (>=4 chars, stopwords removed) matched",
        f"against the first {FIRST_PAGES} pages of the PDF; a pass also comes from a",
        "literal DOI match. Heuristic triage only - PASS means 'nothing",
        "contradictory found', FAIL means a human must look.",
        "",
    ]
    if fails:
        lines += ["## FAIL - title and PDF disagree", "",
                  "| id | ratio | master title | missing tokens |",
                  "|---|---|---|---|"]
        for r in fails:
            lines.append(
                f"| {r['id']} | {r['ratio']} | {str(r['title'])[:70]} | "
                f"{r['missing_tokens']} |"
            )
        lines.append("")
    if weaks:
        lines += ["## WEAK - partial match", "",
                  "| id | ratio | master title | missing tokens |",
                  "|---|---|---|---|"]
        for r in weaks[:80]:
            lines.append(
                f"| {r['id']} | {r['ratio']} | {str(r['title'])[:70]} | "
                f"{r['missing_tokens']} |"
            )
        lines.append("")
    (OUT_DIR / "IDENTITY_AUDIT_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print(f"checked {n}")
    print(f"  PASS       {count('PASS')}")
    print(f"  WEAK       {count('WEAK')}")
    print(f"  FAIL       {count('FAIL')}")
    print(f"  UNTESTABLE {count('UNTESTABLE')}")
    print(f"  NO_PDF     {count('NO_PDF')}")
    print(f"report: {OUT_DIR / 'IDENTITY_AUDIT_REPORT.md'}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())