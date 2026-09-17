#!/usr/bin/env python3
"""
17_audit_extraction.py — V1 extraction integrity audit (two-layer).

Layer 1 (PDF text):  reads 05_papers_fulltext/REC_XXXX.pdf via PyMuPDF,
                     computes n_chars / n_tokens / non-ASCII / short-token.
Layer 2 (CSV data):  audits 02_data_processed/extracted_master_v2.csv for
                     required-field population, QA sum consistency,
                     pdf_pages vs actual, fulltext_available vs disk,
                     and id ↔ PDF filename 1:1.

Outputs (with --apply): 06_analysis/audit/V1_audit_<UTC>.{csv,json}
Exit codes: 0 clean or dry-run, 1 FAILs present, 2 fatal setup error.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

# ------------------------------------------------------------------ setup
try:
    import pymupdf as fitz          # PyMuPDF >= 1.24
except ImportError:
    try:
        import fitz                 # older name
    except ImportError:
        print("[fatal] PyMuPDF not installed. Run: pip install pymupdf",
              file=sys.stderr)
        sys.exit(2)

REPO_ROOT   = Path(r"E:\GPS_Denied_SLR")
EXTRACT_CSV = REPO_ROOT / "02_data_processed" / "extracted_master_v2.csv"
PDF_DIR     = REPO_ROOT / "05_papers_fulltext"
AUDIT_DIR   = REPO_ROOT / "06_analysis" / "audit"

EXPECTED_ROWS  = 171
FORBIDDEN_ROWS = {1692, 1700, 1332}      # legacy pipeline counts — hard flag

# Thresholds
MIN_CHARS     = 2000
MAX_NONASCII  = 0.30
MAX_SHORTTOK  = 0.50

# Required CSV fields (empty / NOT_REPORTED / N/A → WARN)
REQUIRED_FIELDS = (
    "id", "title", "year", "doi",
    "platform_type", "sensor_list", "primary_method", "method_category",
    "environment", "experiment_type", "real_or_sim",
    "qa_total", "qa_tier", "citation_tier",
)

# Closed vocabularies
VOCAB = {
    "real_or_sim":   {"Real_World", "Simulation", "Both"},
    "qa_tier":       {"Q-high", "Q-medium", "Q-low"},
    "citation_tier": {"Core", "Important", "Peripheral"},
}

# QA sub-score bounds (from qa_notes string: Rigor/4, Reporting/3, Baseline/2, Repro/1)
QA_BOUNDS = {"qa_rigor": 4, "qa_reporting": 3, "qa_baseline": 2, "qa_repro": 1}

EMPTY_TOKENS = {"", "NOT_REPORTED", "N/A", "NA", "None", "Unknown", "null"}

# ------------------------------------------------------------------ exceptions
# Rows whose FAIL classification is a known false positive. Each entry MUST
# have a reason and MUST be echoed in 06_analysis/audit/MANUAL_REVIEW.md.
# These do NOT silently pass — they surface as PASS_EXCEPTION in every report.
MANUAL_EXCEPTIONS: dict[str, str] = {
    "REC_1137":
        "High short-token ratio (52.5%) due to equation-dense mathematical "
        "notation; text integrity confirmed by manual inspection. 26,871 chars, "
        "non-ASCII within bounds.",
}

# ------------------------------------------------------------------ types
@dataclass
class Row:
    paper_id: str
    status: str                  # PASS | WARN_* | FAIL_*
    issues: str                  # pipe-joined
    pdf_exists: bool
    pdf_bytes: int
    pdf_pages_actual: int
    pdf_pages_csv: int
    pages_match: bool
    text_chars: int
    text_tokens: int
    nonascii_ratio: float
    shorttok_ratio: float
    text_status: str             # PASS | FAIL_EMPTY | FAIL_SHORT | FAIL_OCR
    missing_fields: str          # pipe-joined
    qa_consistent: bool
    qa_sum: int
    qa_total_csv: int
    fulltext_consistent: bool

# ------------------------------------------------------------------ helpers
def _load_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        rdr = csv.DictReader(f)
        return rdr.fieldnames or [], list(rdr)

def _is_empty(v) -> bool:
    return (v is None) or (str(v).strip() in EMPTY_TOKENS)

def _to_int(v) -> int:
    try:
        return int(str(v).strip())
    except Exception:
        return -1

def _metrics(text: str) -> tuple[int, int, float, float]:
    n = len(text)
    if n == 0:
        return 0, 0, 0.0, 0.0
    nonascii = sum(1 for c in text if ord(c) > 127)
    tokens = re.findall(r"\S+", text)
    ntok = len(tokens)
    short = sum(1 for t in tokens if len(t) <= 2)
    return n, ntok, nonascii / n, (short / ntok if ntok else 0.0)

def _classify_text(n_chars: int, na: float, st: float) -> tuple[str, str]:
    if n_chars == 0:        return "FAIL_EMPTY", "0 chars extracted"
    if n_chars < MIN_CHARS: return "FAIL_SHORT", f"{n_chars} chars < {MIN_CHARS}"
    if na > MAX_NONASCII:   return "FAIL_OCR",   f"non-ASCII {na:.1%}"
    if st > MAX_SHORTTOK:   return "FAIL_OCR",   f"short-token {st:.1%}"
    return "PASS", ""

def _pdf_text(path: Path) -> tuple[str, int]:
    """Return (concatenated text, page count)."""
    try:
        doc = fitz.open(str(path))
        pages = doc.page_count
        chunks = [doc.load_page(i).get_text("text") for i in range(pages)]
        doc.close()
        return "\n".join(chunks), pages
    except Exception as e:
        return f"__PDF_READ_ERROR__:{e}", -1

# ------------------------------------------------------------------ main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path, default=EXTRACT_CSV)
    ap.add_argument("--pdf-dir", type=Path, default=PDF_DIR)
    ap.add_argument("--min-chars", type=int, default=MIN_CHARS)
    ap.add_argument("--apply", action="store_true",
                    help="Write CSV+JSON report. Otherwise dry-run.")
    ap.add_argument("--inspect", action="store_true",
                    help="Print CSV schema + first row, then exit.")
    args = ap.parse_args()

    # ---- load CSV
    if not args.csv.is_file():
        print(f"[fatal] extraction CSV not found: {args.csv}", file=sys.stderr)
        return 2
    cols, rows = _load_csv(args.csv)
    print(f"[csv] {args.csv}")
    print(f"[csv] {len(rows)} data rows, {len(cols)} columns")

    if args.inspect:
        if rows:
            print("\n[inspect] first row:")
            for k, v in rows[0].items():
                vs = (v[:120] + "…") if isinstance(v, str) and len(v) > 120 else v
                print(f"  {k}: {vs!r}")
        return 0

    # ---- row-count guards
    if len(rows) in FORBIDDEN_ROWS:
        print(f"[fatal] row count {len(rows)} matches FORBIDDEN legacy count "
              f"{sorted(FORBIDDEN_ROWS)}. Refusing to audit.", file=sys.stderr)
        return 2
    if len(rows) != EXPECTED_ROWS:
        print(f"[warn] row count {len(rows)} != V1 expected {EXPECTED_ROWS}")

    # ---- PDF inventory
    pdfs = {p.stem: p for p in args.pdf_dir.glob("*.pdf")} if args.pdf_dir.is_dir() else {}
    print(f"[pdfs] {len(pdfs)} PDFs under {args.pdf_dir}")

    # ---- audit loop
    out: list[Row] = []
    for i, r in enumerate(rows, 1):
        issues: list[str] = []
        pid = str(r.get("id", "")).strip()

        # -------- Layer 1: PDF text quality
        pdf = pdfs.get(pid)
        pdf_exists = pdf is not None
        pdf_bytes = pdf.stat().st_size if pdf_exists else 0
        pages_actual = -1
        text_chars = text_tokens = 0
        na = st = 0.0
        text_status = "PASS"

        if pdf_exists:
            text, pages_actual = _pdf_text(pdf)
            if text.startswith("__PDF_READ_ERROR__"):
                text_status = "FAIL_EMPTY"
                issues.append(f"pdf_read_error: {text.split(':', 1)[1][:60]}")
            else:
                text_chars, text_tokens, na, st = _metrics(text)
                text_status, reason = _classify_text(text_chars, na, st)
                if text_status != "PASS":
                    issues.append(f"{text_status}: {reason}")
        else:
            text_status = "FAIL_EMPTY"
            issues.append("pdf_missing_on_disk")

        # -------- Layer 2a: required fields
        missing = [f for f in REQUIRED_FIELDS if _is_empty(r.get(f))]
        if missing:
            issues.append("missing_fields:" + ",".join(missing))

        # -------- Layer 2b: closed vocabularies
        for field, allowed in VOCAB.items():
            val = str(r.get(field, "")).strip()
            if val and val not in allowed:
                issues.append(f"vocab:{field}={val!r}")

        # -------- Layer 2c: QA sum consistency
        qa_vals = {k: _to_int(r.get(k)) for k in QA_BOUNDS}
        qa_out_of_bounds = [k for k, v in qa_vals.items()
                            if v < 0 or v > QA_BOUNDS[k]]
        qa_sum = sum(v for v in qa_vals.values() if v >= 0)
        qa_total_csv = _to_int(r.get("qa_total"))
        qa_consistent = (qa_sum == qa_total_csv) and not qa_out_of_bounds
        if qa_out_of_bounds:
            issues.append("qa_bounds:" + ",".join(qa_out_of_bounds))
        if qa_sum != qa_total_csv:
            issues.append(f"qa_sum_mismatch: parts={qa_sum} total={qa_total_csv}")

        # -------- Layer 2d: pdf_pages consistency
        pages_csv = _to_int(r.get("pdf_pages"))
        pages_match = (pages_csv == pages_actual) if pages_actual >= 0 else False
        if pdf_exists and not pages_match:
            issues.append(f"pages_mismatch: csv={pages_csv} actual={pages_actual}")

        # -------- Layer 2e: fulltext_available vs disk
        ft = str(r.get("fulltext_available", "")).strip().lower()
        fulltext_consistent = (
            (ft in {"true", "1", "yes"} and pdf_exists) or
            (ft in {"false", "0", "no"} and not pdf_exists)
        )
        if not fulltext_consistent:
            issues.append(f"fulltext_flag: flag={ft!r} pdf_on_disk={pdf_exists}")

        # -------- roll-up status
        if not pdf_exists:
            status = "FAIL_MISSING_PDF"
        elif text_status != "PASS" and pid in MANUAL_EXCEPTIONS:
            status = "PASS_EXCEPTION"
            issues.append(f"exception: {MANUAL_EXCEPTIONS[pid][:80]}")
        elif text_status != "PASS":
            status = text_status.replace("FAIL_", "FAIL_TEXT_")
        elif not qa_consistent:
            status = "FAIL_QA"
        elif missing:
            status = "WARN_FIELD"
        elif not pages_match or not fulltext_consistent:
            status = "WARN_META"
        elif issues:
            status = "WARN_VOCAB"
        else:
            status = "PASS"

        out.append(Row(
            paper_id=pid, status=status, issues="|".join(issues) or "",
            pdf_exists=pdf_exists, pdf_bytes=pdf_bytes,
            pdf_pages_actual=pages_actual, pdf_pages_csv=pages_csv,
            pages_match=pages_match,
            text_chars=text_chars, text_tokens=text_tokens,
            nonascii_ratio=round(na, 4), shorttok_ratio=round(st, 4),
            text_status=text_status,
            missing_fields="|".join(missing),
            qa_consistent=qa_consistent, qa_sum=qa_sum, qa_total_csv=qa_total_csv,
            fulltext_consistent=fulltext_consistent,
        ))
        if i % 25 == 0:
            print(f"  ...audited {i}/{len(rows)}")

    # ---- summary
    counts = Counter(x.status for x in out)
    total = len(out)
    print("\n=== AUDIT SUMMARY ===")
    order = ["PASS", "PASS_EXCEPTION", "WARN_FIELD", "WARN_META", "WARN_VOCAB",
             "FAIL_MISSING_PDF", "FAIL_TEXT_EMPTY", "FAIL_TEXT_SHORT",
             "FAIL_TEXT_OCR", "FAIL_QA"]
    for k in order:
        c = counts.get(k, 0)
        if c:
            print(f"  {k:<20} {c:>5}  ({c/total*100:5.1f}%)")
    print(f"  {'TOTAL':<20} {total:>5}")

    fails = [x for x in out if x.status.startswith("FAIL")]
    warns = [x for x in out if x.status.startswith("WARN")]
    if fails:
        print(f"\n[fails] {len(fails)} row(s); first 10:")
        for x in fails[:10]:
            print(f"  {x.paper_id:<12} {x.status:<20} {x.issues[:90]}")
    if warns:
        print(f"\n[warns] {len(warns)} row(s); first 5:")
        for x in warns[:5]:
            print(f"  {x.paper_id:<12} {x.status:<20} {x.issues[:90]}")

    # ---- vocabulary / QA roll-ups
    print("\n=== ROLL-UPS ===")
    ft_ok = sum(1 for x in out if x.fulltext_consistent)
    pg_ok = sum(1 for x in out if x.pages_match)
    qa_ok = sum(1 for x in out if x.qa_consistent)
    print(f"  fulltext_available consistent : {ft_ok}/{total}")
    print(f"  pdf_pages matches actual      : {pg_ok}/{total}")
    print(f"  QA sub-scores sum to qa_total : {qa_ok}/{total}")

    # ---- citation_tier / qa_tier distributions (cross-check vs known V1 numbers)
    tier_ct = Counter(str(r.get("citation_tier", "")).strip() for r in rows)
    qa_ct   = Counter(str(r.get("qa_tier", "")).strip() for r in rows)
    ros_ct  = Counter(str(r.get("real_or_sim", "")).strip() for r in rows)
    print(f"  citation_tier: {dict(tier_ct)}")
    print(f"  qa_tier      : {dict(qa_ct)}")
    print(f"  real_or_sim  : {dict(ros_ct)}")

    if not args.apply:
        print("\n[dry-run] no files written. Re-run with --apply to save report.")
        return 0 if not fails else 1

    args.out_dir = AUDIT_DIR
    args.out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    csv_path  = args.out_dir / f"V1_audit_{ts}.csv"
    json_path = args.out_dir / f"V1_audit_{ts}.json"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(out[0]).keys()))
        w.writeheader()
        for x in out:
            w.writerow(asdict(x))

    json_path.write_text(json.dumps({
        "generated_utc": ts,
        "csv_source":    str(args.csv),
        "pdf_dir":       str(args.pdf_dir),
        "expected_rows": EXPECTED_ROWS,
        "thresholds":    {"min_chars": args.min_chars,
                          "max_nonascii": MAX_NONASCII,
                          "max_shorttok": MAX_SHORTTOK},
        "counts":        dict(counts),
        "total":         total,
        "distribution":  {"citation_tier": dict(tier_ct),
                          "qa_tier":       dict(qa_ct),
                          "real_or_sim":   dict(ros_ct)},
        "rows":          [asdict(x) for x in out],
    }, indent=2), encoding="utf-8")

    print(f"\n[apply] wrote:\n  {csv_path}\n  {json_path}")
    return 0 if not fails else 1

if __name__ == "__main__":
    raise SystemExit(main())
