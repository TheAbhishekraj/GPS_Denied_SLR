#!/usr/bin/env python3
"""09_build_evidence_workbooks.py — page-marked evidence workbook per paper.

The extraction agent must fill 63 columns per paper with a citable source. Raw
`get_text()` output has no page numbers and no structure, so a value cannot be
traced to "p. 7, Table III". This script builds one workbook per PDF that keeps
the page anchors and pre-locates the evidence.

Per paper, `06_analysis/output/workbooks/<id>.md` contains, in this order:

    ## 1. IDENTITY            master-CSV categorical fields (citable, audited)
    ## 2. FULL PAGE-MARKED TEXT   every page, prefixed `### [[page N]]`
    ## 3. SECTIONS            heading -> page map, so a field cites a section
    ## 4. CAPTIONS            table / figure captions with page + number
    ## 5. METRIC LINES        every line carrying a metric keyword + number
    ## 6. NUMBERED LINES      table-row-shaped lines, for reading results tables

Blocks 3-6 are navigation aids. Block 2 is the evidence; every value in the
final CSV must be traceable to a page in block 2, normally via a caption or
section found in block 3 or 4.

The metric patterns are the same word-guarded, case-sensitive ones that the
pre-flight probe (`08_pdf_numeric_probe.py`) was verified against, so the
workbook and the probe agree on what counts as a metric hit.

Read-only with respect to the PDFs; writes only under 06_analysis/output/.

Usage:
    python 06_analysis/scripts/09_build_evidence_workbooks.py
    python 06_analysis/scripts/09_build_evidence_workbooks.py --limit 3
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
MASTER_CSV = REPO / "02_data_processed" / "extracted_master_v2.csv"
OUT_DIR = REPO / "06_analysis" / "output" / "workbooks"

# --- metric patterns (identical to the verified probe) --------------------
GUARD = r"(?<![A-Za-z\-])"
NUM = r"(\d+(?:\.\d+)?)"
LEN_UNIT = r"(km|cm|mm|m)\b"
ANG_UNIT = r"(deg|degree|°|rad|%)"

METRIC_PATTERNS = (
    ("ATE", re.compile(GUARD + rf"ATE\b[^\n]{{0,50}}?{NUM}\s*{LEN_UNIT}")),
    ("RMSE", re.compile(GUARD + rf"RMSE\b[^\n]{{0,50}}?{NUM}\s*{LEN_UNIT}")),
    ("RPE", re.compile(
        GUARD + rf"RPE\b[^\n]{{0,50}}?{NUM}\s*(?:{LEN_UNIT}|{ANG_UNIT})")),
    ("drift", re.compile(
        GUARD + rf"drift\b[^\n]{{0,60}}?{NUM}\s*(?:%|m)\b", re.I)),
    ("success rate", re.compile(
        GUARD + rf"success\s+rate[^\n]{{0,50}}?{NUM}\s*%", re.I)),
    ("position error", re.compile(
        rf"(?<![A-Za-z\-])(?:position|positioning|localization|localisation)"
        rf"\s+error[^\n]{{0,50}}?{NUM}\s*{LEN_UNIT}",
        re.I)),
)
KEYWORD_ANY = re.compile(
    GUARD + r"(?:ATE|RMSE|RPE|CEP)\b|drift|"
    r"error[- ]?(?:cm|mm|m)\b|"
    r"success\s+rate|error\s*[=:]\s*\d",
    re.I,
)

SECTION_PATTERNS = (
    "abstract", "introduction", "related work", "literature review",
    "background", "problem formulation", "system overview", "methodology",
    "method", "approach", "system design", "implementation", "experiment",
    "experimental setup", "evaluation", "results", "discussion", "limitation",
    "conclusion", "future work", "ablation",
)
RE_SECTION = re.compile(
    r"^\s*(?:\d+\.?\d*\.?\s*)?("
    + "|".join(re.escape(s) for s in SECTION_PATTERNS)
    + r")\b[:.\s]",
    re.I,
)
# Fallback: roman-numeral headings ("IV. SIMULATION RESULTS") and short
# title-like lines do not match RE_SECTION above, yet they are exactly the
# headings an extractor needs for page citations.
RE_SECTION_ANY = re.compile(
    r"\b(" + "|".join(re.escape(s) for s in SECTION_PATTERNS) + r")\b", re.I
)


def is_sectionish(line: str) -> bool:
    """True when a short line looks like a section heading."""
    if len(line) < 4 or line.endswith(","):
        return False
    if RE_SECTION.match(line) and len(line) < 55:
        return True
    return len(line) < 40 and bool(RE_SECTION_ANY.search(line))
RE_CAPTION = re.compile(
    r"^\s*(table|tab\.|figure|fig\.|figures|tables)\s*"
    r"([IVXLC]+|\d+[a-z]?)\s*[:.]\s*(.+)",
    re.I,
)
RE_NUMBERED = re.compile(r"^\s*[\dIVX][\d.,)\s]")


def load_master() -> dict[str, dict[str, str]]:
    with MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        return {row["id"]: row for row in csv.DictReader(fh)}


def build_pages(pdf: Path) -> list[str]:
    with fitz.open(pdf) as doc:
        return [page.get_text() for page in doc]


def identity_block(rec: dict[str, str] | None) -> list[str]:
    if not rec:
        return ["_id absent from extracted_master_v2.csv_"]
    keys = (
        "id", "title", "authors", "year", "venue", "doi", "source",
        "fulltext_available", "pdf_pages", "platform_type", "sensor_list",
        "primary_method", "method_category", "environment", "experiment_type",
        "real_or_sim", "metrics_reported", "ate_rmse_m", "application_domain",
        "multi_agent", "qa_rigor", "qa_reporting", "qa_baseline", "qa_repro",
        "qa_total", "qa_tier", "citation_tier",
    )
    out = []
    for key in keys:
        val = (rec.get(key) or "").strip() or "NOT_REPORTED"
        out.append(f"- **{key}**: {val}")
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="only first N PDFs")
    args = ap.parse_args()

    master = load_master()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if args.limit:
        pdfs = pdfs[: args.limit]

    failures: list[str] = []
    no_metrics: list[str] = []
    built = 0

    for pdf in pdfs:
        pid = pdf.stem
        try:
            pages = build_pages(pdf)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{pid}: {type(exc).__name__}: {exc}")
            continue

        body = "\n".join(
            f"### [[page {i}]]\n{text}" for i, text in enumerate(pages, start=1)
        )

        sections: list[str] = []
        captions: list[str] = []
        metrics: list[str] = []
        numbered: list[str] = []
        for pno, text in enumerate(pages, start=1):
            for raw in text.splitlines():
                line = " ".join(raw.split())
                if not line:
                    continue
                if is_sectionish(line):
                    sections.append(f"- p.{pno}: {line}")
                m = RE_CAPTION.match(line)
                if m:
                    kind = m.group(1).lower()
                    kind = "Table" if kind.startswith("tab") else "Figure"
                    captions.append(
                        f"- p.{pno}: {kind} {m.group(2)}: {m.group(3)[:220]}"
                    )
                if KEYWORD_ANY.search(line) and re.search(r"\d", line):
                    metrics.append(f"- p.{pno}: {line[:260]}")
                if RE_NUMBERED.match(line) and re.search(r"\d\.\d|\d,\d", line):
                    numbered.append(f"- p.{pno}: {line[:220]}")

        if not metrics:
            no_metrics.append(pid)

        blocks = [
            f"# WORKBOOK {pid}",
            "",
            "Generated by `06_analysis/scripts/09_build_evidence_workbooks.py`.",
            f"Source: `05_papers_fulltext/{pid}.pdf` ({len(pages)} pages).",
            "Every extracted value must be traceable to a page shown here.",
            "",
            "## 1. IDENTITY",
            "",
            *identity_block(master.get(pid)),
            "",
            "## 2. FULL PAGE-MARKED TEXT",
            "",
            body,
            "",
            "## 3. SECTIONS",
            "",
            *(sections or ["- none detected"]),
            "",
            "## 4. CAPTIONS",
            "",
            *(captions or ["- none detected"]),
            "",
            "## 5. METRIC LINES",
            "",
            *(metrics or ["- none detected"]),
            "",
            "## 6. NUMBERED LINES",
            "",
            *(numbered or ["- none detected"]),
            "",
        ]
        (OUT_DIR / f"{pid}.md").write_text("\n".join(blocks), encoding="utf-8")
        built += 1
        if built % 20 == 0:
            print(f"  {built}/{len(pdfs)} workbooks")

    print(f"workbooks written: {built} -> {OUT_DIR}")
    print(f"pdfs with no metric line: {len(no_metrics)}")
    if no_metrics:
        print(f"  {', '.join(no_metrics[:20])}")
    if failures:
        print(f"FAILED TO PARSE ({len(failures)}):")
        for f in failures:
            print(f"  {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
