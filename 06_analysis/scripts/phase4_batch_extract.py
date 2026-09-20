#!/usr/bin/env python3
"""phase4_batch_extract.py v1.0 - per-batch deterministic extractor (Phase 6).

Rule 9 spec approved 2026-09-19, with human amendment: also writes per-paper
page-marked text files so the interpretive pass never re-opens a PDF.

INPUTS (read-only):
  02_data_processed/screening_results.csv   (291 rows -> INCLUDE = 285)
  05_papers_fulltext/REC_XXXX.pdf
  06_analysis/scripts/pdf_text.py           (page-marked text helper)
  08_docs/EXTRACTION_SCHEMA_v1.md           (28-column order)

HARD SKIP LOGIC (no flag can override):
  DEFERRED = REC_0023, REC_0035, REC_0244, REC_1217, REC_1667, REC_0363
  SAFE = INCLUDE minus DEFERRED = 279 -> BATCH_B01..BATCH_B28 (27x10 + 1x9)

OUTPUTS (only when NOT --dry-run):
  a. evidence_batches/BATCH_BXX.csv - 28 cols in schema order; deterministic
     fields filled from the PDF (id, title, doi, _source_pages); ALL other
     fields NOT_REPORTED (filled by the interpretive pass). No value is ever
     invented: no inference, no substitution from other files.
  b. evidence_batches/BATCH_BXX_pages/REC_XXXX.txt - full [p.N] text from
     pdf_text.py. Archived to _QUARANTINE_BATCH_PAGES_<ts>/ after merge.

SIDE EFFECTS: writes only the batch CSV, its _pages/ folder, and one
_AUDIT/action_log.md line. NEVER touches MASTER_EVIDENCE.csv.

CLI: python phase4_batch_extract.py --batch B01 [--dry-run] [--force]
Exit: 0 ok / 1 error / 2 usage.
"""
import argparse
import csv
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCREEN = os.path.join(REPO, "02_data_processed", "screening_results.csv")
PDF_DIR = os.path.join(REPO, "05_papers_fulltext")
BATCH_DIR = os.path.join(REPO, "02_data_processed", "evidence_batches")
PDFTEXT = os.path.join(REPO, "06_analysis", "scripts", "pdf_text.py")
LOG = os.path.join(REPO, "_AUDIT", "action_log.md")

SCHEMA_COLS = [
    "id", "title", "authors", "year", "venue", "doi", "problem", "motivation",
    "gps_denied_type", "environment", "platform", "sensors", "method_category",
    "algorithm", "real_or_sim", "dataset", "metrics", "headline_result",
    "baseline", "ablation", "limitations", "future_work", "taxonomy_category",
    "contribution_type", "country", "funding", "notes", "_source_pages",
]
DETERMINISTIC = ("id", "title", "doi", "_source_pages")

DEFERRED = {
    "REC_0023", "REC_0035", "REC_0244", "REC_1217", "REC_1667", "REC_0363",
}
BATCH_SIZE = 10
DOIPAT = re.compile(r"10\.\d{4,9}/[^\s\]\[<>\"{}|]+")


def load_safe_ids():
    """INCLUDE ids from screening, minus DEFERRED, sorted."""
    if not os.path.isfile(SCREEN):
        sys.stderr.write("phase4: missing %s\n" % SCREEN)
        sys.exit(1)
    inc = []
    with open(SCREEN, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if (r.get("decision") or "").strip().upper() == "INCLUDE":
                inc.append(r["id"].strip())
    return inc, sorted(i for i in inc if i not in DEFERRED)


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def batch_plan(safe):
    """Return {'B01': [ids...], ...} with the last batch holding the remainder."""
    plan, k = {}, 1
    for c in chunks(safe, BATCH_SIZE):
        plan["B%02d" % k] = c
        k += 1
    return plan

def extract(path):
    """Deterministic fields from one PDF. Returns (title, doi, pages, err)."""
    try:
        import fitz
    except Exception as exc:
        return None, None, None, "fitz unavailable: %s" % exc
    try:
        d = fitz.open(path)
        if d.needs_pass or d.is_encrypted:
            d.close()
            return None, None, None, "encrypted"
        if d.page_count <= 0:
            d.close()
            return None, None, None, "no_pages"
        page = d.load_page(0)
        spans = []
        for b in page.get_text("dict").get("blocks", []):
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    t = s["text"].strip()
                    if t:
                        spans.append((round(s["size"], 1), round(s["origin"][1], 1), t))
        if not spans:
            d.close()
            return None, None, None, "no_text"
        mx = max(s[0] for s in spans)
        big = sorted([s for s in spans if s[0] >= mx - 1.5], key=lambda x: x[1])
        title = re.sub(r"\s+", " ", " ".join(s[2] for s in big)).strip()
        dois = DOIPAT.findall(page.get_text("text")[:600])
        doi = dois[0].rstrip(".,;)") if dois else None
        pages = d.page_count
        d.close()
        return title, doi, pages, None
    except Exception as exc:
        return None, None, None, "%s: %s" % (type(exc).__name__, exc)


def run(args):
    inc, safe = load_safe_ids()
    plan = batch_plan(safe)
    if args.batch not in plan:
        sys.stderr.write("phase4: unknown batch %r (valid: B01..B%02d)\n" % (args.batch, len(plan)))
        sys.exit(2)
    ids = plan[args.batch]

    print("batch      : %s" % args.batch)
    print("safe total : %d (INCLUDE %d - deferred %d)" % (len(safe), len(inc), len(DEFERRED)))
    print("batches    : %d" % len(plan))
    print("batch rows : %d (expected)" % len(ids))
    print("planned IDs:")
    missing = []
    for i in ids:
        ok = os.path.isfile(os.path.join(PDF_DIR, i + ".pdf"))
        if not ok:
            missing.append(i)
        print("  %s  pdf=%s" % (i, "ok" if ok else "MISSING"))
    if missing:
        sys.stderr.write("phase4: missing PDFs for %s\n" % ", ".join(missing))
        return 1

    if args.dry_run:
        print("DRY-RUN: no files written.")
        return 0

    out_csv = os.path.join(BATCH_DIR, "BATCH_%s.csv" % args.batch)
    out_pages = os.path.join(BATCH_DIR, "BATCH_%s_pages" % args.batch)
    if os.path.exists(out_csv) and not args.force:
        sys.stderr.write("phase4: %s exists; refusing to overwrite (needs --force + approval)\n" % out_csv)
        return 1
    os.makedirs(out_pages, exist_ok=True)

    rows = []
    for i in ids:
        path = os.path.join(PDF_DIR, i + ".pdf")
        title, doi, pages, err = extract(path)
        if err:
            sys.stderr.write("phase4: %s extraction error: %s\n" % (i, err))
            return 1
        r = subprocess.run([sys.executable, PDFTEXT, path], capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            sys.stderr.write("phase4: pdf_text.py failed for %s (exit %d)\n" % (i, r.returncode))
            return 1
        with open(os.path.join(out_pages, i + ".txt"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(r.stdout)
        row = {c: "NOT_REPORTED" for c in SCHEMA_COLS}
        row["id"] = i
        row["title"] = title if title else "NOT_REPORTED"
        row["doi"] = doi if doi else "NOT_REPORTED"
        row["_source_pages"] = "1..%d (physical)" % pages
        rows.append(row)

    with open(out_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=SCHEMA_COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write("%s | PHASE6 | EXTRACT | %s | rows: %d | pages: %s | deterministic=id,title,doi,_source_pages; rest NOT_REPORTED\n"
                 % (ts, out_csv, len(rows), out_pages))

    print("WROTE %s (%d rows)" % (out_csv, len(rows)))
    print("WROTE %s (%d text files)" % (out_pages, len(rows)))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Phase 6 batch extractor (deterministic fields only)")
    ap.add_argument("--batch", required=True, help="batch id, e.g. B01")
    ap.add_argument("--dry-run", action="store_true", help="plan only, write nothing")
    ap.add_argument("--force", action="store_true", help="allow overwrite of an existing batch CSV")
    args = ap.parse_args()
    if not re.fullmatch(r"B\d{2}", args.batch):
        sys.stderr.write("usage: --batch must look like B01\n")
        sys.exit(2)
    sys.exit(run(args))


if __name__ == "__main__":
    main()

