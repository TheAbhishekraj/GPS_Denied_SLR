#!/usr/bin/env python3
"""09_build_workbooks.py — per-paper extraction workbook builder.

Implements Step 2.1 of `08_docs/MASTER_EXTRACTION_PROMPT.md` ("Open with
PyMuPDF; extract text") in a form that makes reading 171 papers tractable and
auditable. For each PDF it writes `06_analysis/output/workbooks/<id>.md` with:

  1. HEADER    - id, pages, characters, thin-text flag, evidence counts
  2. TEXT      - full page-marked text, so every field can be traced to a page
  3. SECTIONS  - auto-detected section headings with page numbers
  4. CAPTIONS  - table / figure captions with page numbers
  5. METRICS   - lines carrying a metric keyword AND a number, with page cites
  6. NUMBERED  - lines shaped like table rows, so results tables are findable

A `workbook_index.csv` summarises what each PDF yielded, which drives batch
planning and the M3 reporting-gap spot-check.

Workbooks are NOT deliverables. They carry verbatim paper text, including
whatever numbers a paper happens to use, so they live under
`06_analysis/output/` and sit deliberately outside the Amendment V4.1 sweep
(which covers only `02_data_processed/MASTER_EVIDENCE_V1.csv`,
`03_extraction/per_paper/*.md` and `07_manuscript/*V1_171_EVIDENCE*`). They are
raw input, not result. Do not cite them; cite the paper's page / table / figure.

Usage:
    python 06_analysis/scripts/09_build_workbooks.py              # all PDFs
    python 06_analysis/scripts/09_build_workbooks.py REC_0035     # one or more
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
OUT_DIR = REPO / "06_analysis" / "output" / "workbooks"

THIN_CHARS = 3000

# Section headings seen across this corpus. Matched at line start; numbering,
# all-caps and single-letter drops (A B S T R A C T) are tolerated.
SECTION_PATTERNS = [
    ("abstract", r"^a\s?b\s?s\s?t\s?r\s?a\s?c\s?t\b"),
    ("introduction", r"^(?:i|1|1\.)\s*\.?\s*introduction\b"),
    ("related_work", r"^(?:related\s+work|ii\s*\.?\s*related|2\s*\.?\s*related)\b"),
    ("method", r"^(?:iii|3|iv|4)\s*\.?\s*(?:method|methodolog|approach|system|"
               r"proposed|materials\s+and\s+methods)\w*|^methodolog\w*"),
    ("experiments", r"^(?:v|5|vi|6)\s*\.?\s*(?:experiment|evaluation|result|"
                    r"validation|field\s+test)\w*|^experiment\w*"),
    ("results", r"^results?\b"),
    ("discussion", r"^discussion\b"),
    ("conclusion", r"^conclusion\w*|^conclusions?\b"),
    ("limitations", r"^limitation\w*"),
    ("future_work", r"^future\s+work\b|^conclusions?\s+and\s+future\b"),
    ("references", r"^references\b|^bibliography\b"),
    ("acknowledgement", r"^acknowledg\w*"),
]
RE_SECTIONS = [(name, re.compile(pat, re.I)) for name, pat in SECTION_PATTERNS]

RE_CAPTION = re.compile(r"^(table|fig(?:ure)?)\s*[IVXLC0-9]+\s*[:.\-]?\s*(.*)$", re.I)
RE_METRIC = re.compile(
    r"\b(ATE|RMSE|RPE|drift|accuracy|error|success\s+rate|improvement|"
    r"precision|recall|flight\s+time|trajectory\s+length|duration)\b",
    re.I,
)
RE_NUMBER = re.compile(r"\d")
RE_DECIMAL = re.compile(r"(\d+(?:\.\d+)?\s*%|\d+\.\d+)")
RE_MULTI_NUMBERS = re.compile(r"(?:\d+(?:\.\d+)?[^\n\d]{0,12}){3,}")


def load_master_ids() -> set[str]:
    with MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        return {row["id"] for row in csv.DictReader(fh)}


def page_texts(pdf: Path) -> list[str]:
    with fitz.open(pdf) as doc:
        return [page.get_text() for page in doc]


def clean(text: str) -> str:
    """Collapse runs of spaces, keep line breaks so table rows survive."""
    out = []
    for line in text.splitlines():
        collapsed = re.sub(r"[ \t\u00a0]+", " ", line).strip()
        if collapsed:
            out.append(collapsed)
    return "\n".join(out)


def detect_sections(pages: list[str]) -> list[tuple[int, str, str]]:
    found: list[tuple[int, str, str]] = []
    for pno, text in enumerate(pages, start=1):
        for line in clean(text).splitlines():
            if not line or len(line) > 90:
                continue
            for name, pat in RE_SECTIONS:
                if pat.search(line):
                    found.append((pno, name, line))
                    break
    return found


def detect_captions(pages: list[str]) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for pno, text in enumerate(pages, start=1):
        lines = clean(text).splitlines()
        for i, line in enumerate(lines):
            if not RE_CAPTION.match(line):
                continue
            caption = line
            # Captions are frequently split; join the following short line.
            if len(lines) > i + 1 and len(lines[i + 1]) < 90:
                caption = f"{line} {lines[i + 1]}"
            found.append((pno, caption))
    return found


def detect_metric_lines(pages: list[str]) -> list[tuple[int, str]]:
    return [
        (pno, line)
        for pno, text in enumerate(pages, start=1)
        for line in clean(text).splitlines()
        if RE_METRIC.search(line) and RE_NUMBER.search(line)
    ]


def detect_numbered_lines(pages: list[str]) -> list[tuple[int, str]]:
    return [
        (pno, line)
        for pno, text in enumerate(pages, start=1)
        for line in clean(text).splitlines()
        if len(RE_DECIMAL.findall(line)) >= 2 or RE_MULTI_NUMBERS.search(line)
    ]


def build_one(pdf: Path) -> dict[str, object]:
    pid = pdf.stem
    pages = page_texts(pdf)
    cpages = [clean(t) for t in pages]
    chars = sum(len(t) for t in cpages)

    sections = detect_sections(pages)
    captions = detect_captions(pages)
    metrics = detect_metric_lines(pages)
    numbered = detect_numbered_lines(pages)

    lines = [
        f"# WORKBOOK {pid}",
        "",
        "Machine-built extraction workbook. NOT a deliverable. Do not cite this",
        "file; cite the paper's page / table / figure in `extraction_source`.",
        "",
        f"- source: `05_papers_fulltext/{pid}.pdf`",
        f"- pages: {len(pages)}",
        f"- extractable characters: {chars}",
        f"- thin text layer (<{THIN_CHARS} chars): "
        f"{'YES - suspect image-only PDF' if chars < THIN_CHARS else 'no'}",
        f"- metric lines: {len(metrics)}",
        f"- captions: {len(captions)}",
        f"- numbered lines: {len(numbered)}",
        "",
        "## 3. SECTIONS",
        "",
    ]
    lines += [f"- p{p} [{n}] {ln}" for p, n, ln in sections] or ["- NOT_DETECTED"]

    lines += ["", "## 4. CAPTIONS", ""]
    lines += [f"- p{p}: {c}" for p, c in captions] or ["- NOT_DETECTED"]

    lines += ["", "## 5. METRIC LINES (keyword + number)", ""]
    lines += [f"- p{p}: {ln}" for p, ln in metrics] or ["- NONE"]

    lines += ["", "## 6. NUMBERED LINES (table-row shaped)", ""]
    lines += [f"- p{p}: {ln}" for p, ln in numbered] or ["- NONE"]

    lines += ["", "## 2. FULL PAGE-MARKED TEXT", ""]
    for pno, text in enumerate(cpages, start=1):
        lines += [f"### [[page {pno}]]", "", text or "(no extractable text)", ""]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{pid}.md").write_text("\n".join(lines), encoding="utf-8")

    return {
        "id": pid,
        "pages": len(pages),
        "chars": chars,
        "thin_text": chars < THIN_CHARS,
        "n_sections": len(sections),
        "n_captions": len(captions),
        "n_metric_lines": len(metrics),
        "n_numbered_lines": len(numbered),
        "section_names": ";".join(sorted({s[1] for s in sections})),
    }


def main(argv: list[str]) -> int:
    master_ids = load_master_ids()
    all_pdfs = sorted(PDF_DIR.glob("*.pdf"))
    wanted = set(argv[1:])
    if wanted:
        all_pdfs = [p for p in all_pdfs if p.stem in wanted]
        missing = sorted(wanted - {p.stem for p in all_pdfs})
        if missing:
            print(f"no such PDF: {', '.join(missing)}")
            return 2

    rows: list[dict[str, object]] = []
    failed: list[str] = []
    for i, pdf in enumerate(all_pdfs, start=1):
        if pdf.stem not in master_ids:
            failed.append(f"{pdf.stem}: id not in extracted_master_v2.csv")
            continue
        try:
            rows.append(build_one(pdf))
        except Exception as exc:  # noqa: BLE001 - log and continue
            failed.append(f"{pdf.stem}: {type(exc).__name__}: {exc}")
        if i % 25 == 0:
            print(f"  workbooks: {i} / {len(all_pdfs)}")

    if rows:
        idx = OUT_DIR / "workbook_index.csv"
        fresh_ids = {str(r["id"]) for r in rows}
        existing: list[dict[str, object]] = []
        if idx.exists():
            with idx.open(newline="", encoding="utf-8") as fh:
                existing = [r for r in csv.DictReader(fh) if r["id"] not in fresh_ids]
        merged = sorted(existing + rows, key=lambda r: str(r["id"]))
        with idx.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(merged)
        print(f"index rows: {len(merged)} -> {idx}")

    print(f"workbooks written: {len(rows)} / {len(all_pdfs)}")
    print(f"workbook dir: {OUT_DIR}")
    if failed:
        print(f"FAILURES ({len(failed)}):")
        for f in failed:
            print(f"  {f}")
    print(f"workbooks with zero metric lines: "
          f"{sum(1 for r in rows if int(r['n_metric_lines']) == 0)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))