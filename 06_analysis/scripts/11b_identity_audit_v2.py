#!/usr/bin/env python3
"""11b_identity_audit_v2.py — identity audit that actually identifies.

Why v1 was not good enough
--------------------------
`11_pdf_identity_audit.py` matched >=55% of the master title's tokens against
the first 3 PDF pages and reported 170 PASS / 0 FAIL. It passed REC_0023, whose
PDF is Khattak et al. (arXiv:1903.01656, "Visual-Thermal Landmarks and Inertial
Fusion...") while the master row is Variar et al. (INSPIRE 2025,
DOI 10.1109/INSPIRE67328.2025.11300665). The title "Autonomous Aerial Navigation
in GPS-Denied Environments" shares almost every token with any paper in this
field, so token overlap is a *topical* test, not an identity test. v1's PASS
verdicts are therefore not evidence of identity.

Identity evidence used here, strongest first
--------------------------------------------
1. DOI            - literal match on the DOI string, all pages, normalised.
2. Author surname - surname found in the author block (pages 1-2 only, so the
                    reference list cannot be mistaken for the author block).
                    The page limit matters: searching all pages for a name like
                    "Wang" would match half the bibliographies.
3. Title tokens   - full-text ratio, reported but never sufficient on its own.

Verdicts
--------
    DOI_MATCH      definitive identity
    SURNAME_MATCH  strong identity
    TITLE_ONLY     inconclusive -> a human must look
    NO_EVIDENCE    no identity evidence at all -> assume wrong PDF
    NO_PDF         file missing

PASS = DOI_MATCH or SURNAME_MATCH. Every other verdict is listed in the report
with the PDF's own opening line so the wrong file can be identified by eye.

Usage:  python 06_analysis/scripts/11b_identity_audit_v2.py
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
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
    "towards", "study", "paper", "approach", "system", "systems", "novel",
    "without", "for", "and", "the", "via",
}

# Unicode repair so "GPS–denied" (en dash) and "conﬂate" (ligature) compare.
TRANS = {
    0x2010: 0x2D, 0x2011: 0x2D, 0x2012: 0x2D, 0x2013: 0x2D, 0x2014: 0x2D,
    0x2212: 0x2D,
}

AUTHOR_PAGES = 2      # author block only; keeps bibliographies out of the test
TITLE_RATIO = 0.70


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.translate(TRANS).lower()
    text = text.replace("\ufb01", "fi").replace("\ufb02", "fl")
    return re.sub(r"\s+", " ", text)


def title_tokens(title: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", norm(title))
    return [w for w in words if w not in STOP]


def surnames(authors: str) -> list[str]:
    """Surnames = last >=4-char alpha token of each author segment.

    Initial-only authors ("B. R", "J. J") are dropped because they cannot
    identify anything. Master author strings are sometimes truncated, so an
    empty result is normal and falls through to the DOI / title tests.
    """
    out: list[str] = []
    for segment in re.split(r"[;,]", authors or ""):
        seg = norm(segment)
        if not seg:
            continue
        toks = re.findall(r"[a-z][a-z\-']+", seg)
        if not toks:
            continue
        last = toks[-1]
        if len(last) >= 4 and last not in STOP:
            out.append(last)
    return sorted(set(out))


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
            "master_year": rec.get("year", ""),
            "master_doi": rec.get("doi", ""),
            "pdf_pages": 0,
            "detected_headline": "",
            "doi_match": False,
            "surnames_tested": 0,
            "surnames_found": 0,
            "surnames_hit": "",
            "title_tokens": 0,
            "title_ratio": 0.0,
            "verdict": "",
        }
        if not pdf.exists():
            row["verdict"] = "NO_PDF"
            rows.append(row)
            continue

        with fitz.open(pdf) as doc:
            row["pdf_pages"] = doc.page_count
            full = "\n".join(p.get_text() for p in doc)
            front_n = min(AUTHOR_PAGES, doc.page_count)
            front = "\n".join(doc[i].get_text() for i in range(front_n))
            first = doc[0].get_text() if doc.page_count else ""

        full_n = norm(full)
        front_norm = norm(front)

        # detected headline: skip journal stamps and DOI lines to reach the title
        head = ""
        for ln in [x.strip() for x in first.splitlines() if x.strip()][:14]:
            low = ln.lower()
            if low.startswith("arxiv:") or "doi" in low or "preprint" in low:
                continue
            if "issn" in low or "ieee access" in low or "received" in low:
                continue
            if len(ln) < 12:
                continue
            head = ln[:110]
            break
        row["detected_headline"] = head

        # 1. DOI, all pages
        doi = norm((rec.get("doi") or "").strip())
        if doi and doi not in ("not_reported", "nan"):
            row["doi_match"] = doi.replace(" ", "") in full_n.replace(" ", "")

        # 2. author block, pages 1-2 only
        sur = surnames(rec.get("authors", ""))
        hit = [s for s in sur if s in front_norm]
        row["surnames_tested"] = len(sur)
        row["surnames_found"] = len(hit)
        row["surnames_hit"] = ";".join(hit[:6])

        # 3. title tokens, full text
        toks = title_tokens(rec.get("title", ""))
        found = [t for t in toks if t in full_n]
        row["title_tokens"] = len(toks)
        row["title_ratio"] = round(len(found) / len(toks), 3) if toks else 0.0

        if row["doi_match"]:
            row["verdict"] = "DOI_MATCH"
        elif hit:
            row["verdict"] = "SURNAME_MATCH"
        elif toks and row["title_ratio"] >= TITLE_RATIO:
            row["verdict"] = "TITLE_ONLY"
        else:
            row["verdict"] = "NO_EVIDENCE"
        rows.append(row)

    csv_path = OUT_DIR / "identity_audit_v2.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    def count(v: str) -> int:
        return sum(1 for r in rows if r["verdict"] == v)

    n = len(rows)
    ok = count("DOI_MATCH") + count("SURNAME_MATCH")
    bad = [r for r in rows if r["verdict"] in ("NO_EVIDENCE", "TITLE_ONLY")]
    untested = [r for r in rows if r["surnames_tested"] == 0]

    lines = [
        "# IDENTITY_AUDIT_REPORT_V2.md",
        "",
        "Identity audit on DOI + author surname, not title tokens.",
        "",
        f"- rows checked: {n}",
        f"- **DOI_MATCH** (definitive): {count('DOI_MATCH')}",
        f"- **SURNAME_MATCH** (strong): {count('SURNAME_MATCH')}",
        f"- TITLE_ONLY (inconclusive, needs eyes): {count('TITLE_ONLY')}",
        f"- NO_EVIDENCE (presumed wrong PDF): {count('NO_EVIDENCE')}",
        f"- NO_PDF: {count('NO_PDF')}",
        f"- **identity-confirmed (DOI or surname): {ok} / {n}**",
        f"- rows with no testable author surname: {len(untested)}",
        "",
        "A DOI match is definitive. A surname match is strong but not absolute",
        "(a wrong-but-related paper can share an author). TITLE_ONLY means the",
        "title tokens are present but neither the DOI nor any author surname was,",
        "which cannot distinguish identity and must be resolved by hand.",
        "",
        "## Why v1 was wrong",
        "",
        "v1 reported 170 PASS / 0 FAIL and passed REC_0023, whose PDF is",
        "Khattak et al. (arXiv:1903.01656) while the master row is Variar et al.",
        "(INSPIRE 2025, DOI 10.1109/INSPIRE67328.2025.11300665). The master title",
        "shares 5 of 5 tokens with the Khattak paper's front matter, so a",
        "token-overlap test cannot separate the two. v1 verdicts are superseded.",
        "",
    ]
    if bad:
        lines += [
            "## Not identity-confirmed",
            "",
            "`detected_headline` is the PDF's own opening line, so the file can be",
            "identified without opening it.",
            "",
            "| id | verdict | doi? | surnames | title ratio | master title | detected headline |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in bad:
            lines.append(
                f"| {r['id']} | {r['verdict']} | {r['doi_match']} | "
                f"{r['surnames_found']}/{r['surnames_tested']} | "
                f"{r['title_ratio']} | {str(r['title'])[:52]} | "
                f"{str(r['detected_headline'])[:52]} |"
            )
        lines.append("")
    (OUT_DIR / "IDENTITY_AUDIT_REPORT_V2.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print(f"checked {n}")
    print(f"  DOI_MATCH     {count('DOI_MATCH')}")
    print(f"  SURNAME_MATCH {count('SURNAME_MATCH')}")
    print(f"  TITLE_ONLY    {count('TITLE_ONLY')}")
    print(f"  NO_EVIDENCE   {count('NO_EVIDENCE')}")
    print(f"  NO_PDF        {count('NO_PDF')}")
    print(f"  identity-confirmed: {ok} / {n}")
    print(f"  no testable surname: {len(untested)}")
    print(f"report: {OUT_DIR / 'IDENTITY_AUDIT_REPORT_V2.md'}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())