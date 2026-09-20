#!/usr/bin/env python3
"""merge_batch.py v1.0 - validate one batch CSV and append it to MASTER_EVIDENCE.csv.

Rule 9 spec approved 2026-09-19, with human amendment: before appending, read
_AUDIT/batch_BXX_report.md, extract the SHA256 recorded there for BATCH_BXX.csv,
recompute the current hash, and abort with HASH_MISMATCH if they differ.

INPUTS (read-only):
  evidence_batches/BATCH_BXX.csv            (10 rows; 9 in the final batch)
  _AUDIT/batch_BXX_report.md                (carries the reviewed SHA256)
  08_docs/EXTRACTION_SCHEMA_v1.md           (28-column order)
  02_data_processed/screening_results.csv   (ID / decision checks)
  02_data_processed/MASTER_EVIDENCE.csv     (read for validation)

HARD GUARDS (no flag can override):
  - abort if batch hash != hash recorded in batch_BXX_report.md (HASH_MISMATCH)
  - abort if any row id is DEFERRED, not INCLUDE, or already in the master
  - abort if batch row count is not the expected count
  - abort if any required column is empty (NOT_REPORTED is a valid value)

OUTPUTS (only with --commit):
  MASTER_EVIDENCE.csv  appended (never overwritten), +N rows
  _AUDIT/merge_log.csv appended
  _AUDIT/action_log.md appended
  _QUARANTINE_<timestamp>/MASTER_EVIDENCE.before_<batch>.csv (pre-append backup)

CLI: python merge_batch.py --batch B01 [--commit] [--partial]
Exit: 0 ok / 1 error / 2 usage.
"""
import argparse
import csv
import hashlib
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BATCH_DIR = os.path.join(REPO, "02_data_processed", "evidence_batches")
MASTER = os.path.join(REPO, "02_data_processed", "MASTER_EVIDENCE.csv")
SCREEN = os.path.join(REPO, "02_data_processed", "screening_results.csv")
AUDIT = os.path.join(REPO, "_AUDIT")
LOG = os.path.join(AUDIT, "action_log.md")
MERGE_LOG = os.path.join(AUDIT, "merge_log.csv")
VALIDATOR = os.path.join(REPO, "06_analysis", "scripts", "validate_master.py")

SCHEMA_COLS = [
    "id", "title", "authors", "year", "venue", "doi", "problem", "motivation",
    "gps_denied_type", "environment", "platform", "sensors", "method_category",
    "algorithm", "real_or_sim", "dataset", "metrics", "headline_result",
    "baseline", "ablation", "limitations", "future_work", "taxonomy_category",
    "contribution_type", "country", "funding", "notes", "_source_pages",
]
REQUIRED = set(SCHEMA_COLS)
DEFERRED = {"REC_0023", "REC_0035", "REC_0244", "REC_1217", "REC_1667", "REC_0363"}
BATCHES_TOTAL = 28
LAST_BATCH_ROWS = 9
NORMAL_BATCH_ROWS = 10


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()


def recorded_hash(report_path):
    if not os.path.isfile(report_path):
        return None, "report missing: %s" % report_path
    txt = open(report_path, encoding="utf-8", errors="replace").read()
    nums = re.findall(r"\b([0-9A-Fa-f]{64})\b", txt)
    if not nums:
        return None, "no SHA256 found in report"
    return nums[-1].upper(), None


def read_batch(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        r = csv.DictReader(fh)
        return r.fieldnames, list(r)


def master_ids():
    if not os.path.isfile(MASTER):
        return set()
    with open(MASTER, newline="", encoding="utf-8-sig") as fh:
        return {(row.get("id") or "").strip() for row in csv.DictReader(fh)}


def screening_decisions():
    d = {}
    with open(SCREEN, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            d[row["id"].strip()] = (row.get("decision") or "").strip().upper()
    return d

def main():
    ap = argparse.ArgumentParser(description="merge one validated batch into MASTER_EVIDENCE.csv")
    ap.add_argument("--batch", required=True)
    ap.add_argument("--commit", action="store_true", help="actually append (default: dry-run)")
    ap.add_argument("--partial", action="store_true", help="allow the final short batch")
    args = ap.parse_args()
    if not re.fullmatch(r"B\d{2}", args.batch):
        sys.stderr.write("usage: --batch must look like B01\n")
        sys.exit(2)

    batch_csv = os.path.join(BATCH_DIR, "BATCH_%s.csv" % args.batch)
    report = os.path.join(AUDIT, "batch_%s_report.md" % args.batch)
    if not os.path.isfile(batch_csv):
        sys.stderr.write("merge: missing %s\n" % batch_csv)
        return 1

    cur = sha256_file(batch_csv)
    rec, err = recorded_hash(report)
    print("batch        : %s" % args.batch)
    print("batch sha256 : %s" % cur)
    if err:
        print("ABORT: %s" % err)
        return 1
    print("report sha256: %s" % rec)
    if rec != cur:
        print("ABORT: HASH_MISMATCH - batch changed since review")
        return 1

    cols, rows = read_batch(batch_csv)
    if cols != SCHEMA_COLS:
        print("ABORT: column mismatch vs EXTRACTION_SCHEMA_v1")
        return 1

    expected = LAST_BATCH_ROWS if args.batch == "B%02d" % BATCHES_TOTAL else NORMAL_BATCH_ROWS
    if len(rows) != expected and not (args.partial and len(rows) == LAST_BATCH_ROWS):
        print("ABORT: expected %d rows, found %d" % (expected, len(rows)))
        return 1

    dec = screening_decisions()
    have = master_ids()
    problems = []
    for row in rows:
        i = (row.get("id") or "").strip()
        if i in DEFERRED:
            problems.append("%s: DEFERRED id" % i)
        if dec.get(i) != "INCLUDE":
            problems.append("%s: screening decision != INCLUDE (%s)" % (i, dec.get(i)))
        if i in have:
            problems.append("%s: already present in MASTER_EVIDENCE.csv" % i)
        for c in REQUIRED:
            if not (row.get(c) or "").strip():
                problems.append("%s: empty required field %s" % (i, c))
    if problems:
        print("ABORT: validation problems")
        for p in problems:
            print("  - %s" % p)
        return 1

    print("validation   : PASS (%d rows)" % len(rows))
    before = sha256_file(MASTER) if os.path.isfile(MASTER) else "MISSING"
    print("master before: %s" % before)
    if not args.commit:
        print("DRY-RUN: no files written.")
        return 0

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    qdir = os.path.join(REPO, "_QUARANTINE_%s" % ts)
    os.makedirs(qdir, exist_ok=True)
    shutil.copy2(MASTER, os.path.join(qdir, "MASTER_EVIDENCE.before_%s.csv" % args.batch))

    with open(MASTER, "a", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=SCHEMA_COLS, lineterminator="\r\n").writerows(rows)

    after = sha256_file(MASTER)
    new_hdr = not os.path.exists(MERGE_LOG)
    with open(MERGE_LOG, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new_hdr:
            w.writerow(["timestamp", "batch", "rows", "master_before", "master_after", "quarantine"])
        w.writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    args.batch, len(rows), before, after, qdir])

    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write("%s | PHASE6 | MERGE | %s | rows: +%d | master %s -> %s | quarantine: %s\n"
                 % (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    batch_csv, len(rows), before[:12], after[:12], qdir))

    print("master after : %s" % after)
    print("quarantine   : %s" % qdir)

    if os.path.isfile(VALIDATOR):
        r = subprocess.run([sys.executable, VALIDATOR], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        print("--- validate_master.py ---")
        print(r.stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())

