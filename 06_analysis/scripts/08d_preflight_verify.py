#!/usr/bin/env python3
"""08d_preflight_verify.py — one command to validate the pre-flight state.

Re-runs every check that can be evaluated BEFORE the extraction agent starts
(protocol steps 1-5), and prints a PASS/FAIL table. After extraction, run the
full `08_docs/MASTER_VERIFICATION_PROTOCOL.md` checks instead.

Checks
------
P1  The four governing files exist.
P2  MASTER_PAPER_TEMPLATE.md contains sections 0-15.
P3  MASTER_EXTRACTION_PROMPT.md contains STEP 1-7 and self-gates G1-G6.
P4  MASTER_VERIFICATION_PROTOCOL.md contains Check V1-V9.
P5  MASTER_EVIDENCE_V1.csv header has 63 columns, matches the prompt's field
    list exactly (names and order), no blanks, no duplicates, ends with \n.
P6  V4.1 forbidden-number scan over the evidence artifacts only. The as-written
    Check V4 cannot pass: it self-matches its own definition line and sweeps
    legacy files. See PREFLIGHT_FINDINGS.md section 7.
P7  The master CSV matches the canonical vectors and the audit of record.
P8  The probe scripts have been run and their outputs exist.

Usage:  python 06_analysis/scripts/08d_preflight_verify.py
Exit code 0 if all checks pass, 1 otherwise.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

TEMPLATE = REPO / "01_corpus" / "MASTER_PAPER_TEMPLATE.md"
PROMPT = REPO / "08_docs" / "MASTER_EXTRACTION_PROMPT.md"
PROTOCOL = REPO / "08_docs" / "MASTER_VERIFICATION_PROTOCOL.md"
EVIDENCE = REPO / "02_data_processed" / "MASTER_EVIDENCE_V1.csv"
MASTER = REPO / "02_data_processed" / "extracted_master_v2.csv"
AUDIT = REPO / "06_analysis" / "audit" / "V1_audit_20260917T124255Z.json"
PROBE_DIR = REPO / "06_analysis" / "output" / "pdf_numeric_probe_v1"
PER_PAPER = REPO / "03_extraction" / "per_paper"

CANON = {
    "qa_tier": {"Q-high": 38, "Q-medium": 84, "Q-low": 49},
    "citation_tier": {"Core": 35, "Important": 87, "Peripheral": 49},
    "real_or_sim": {"Real_World": 22, "Simulation": 78, "Both": 71},
}
CANON_AUDIT_DIST = {
    "citation_tier": {"Peripheral": 49, "Important": 87, "Core": 35},
    "qa_tier": {"Q-low": 49, "Q-medium": 84, "Q-high": 38},
    "real_or_sim": {"Simulation": 78, "Both": 71, "Real_World": 22},
}
FORBIDDEN = r"1,692|1,700|1,719|2,000|281|1,332|495|98\.4%"

results: list[tuple[str, bool, str]] = []


def check(cid: str, ok: bool, detail: str) -> None:
    results.append((cid, ok, detail))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def expected_columns() -> list[str]:
    """Enumerated column list from the master prompt.

    The declared count in the prose is parsed rather than hardcoded, so a stale
    literal cannot silently break this check. Callers must compare the declared
    count against the enumerated list: that mismatch was a real defect in the
    original spec ("66 columns" against 63 enumerated names).
    """
    text = read(PROMPT)
    m = re.search(r"\((\d+) comma-separated columns\):", text)
    if not m:
        raise SystemExit("P-err: no '(N comma-separated columns):' marker in prompt")
    declared = int(m.group(1))
    block = text[m.end():].split("(The agent must join")[0]
    names = [n.strip() for n in block.replace("\n", "").split(",") if n.strip()]
    if declared != len(names):
        raise SystemExit(
            f"P-err: prompt declares {declared} columns but enumerates {len(names)}"
        )
    return names


def main() -> int:
    # P1 -----------------------------------------------------------------
    missing = [p.name for p in (TEMPLATE, PROMPT, PROTOCOL, EVIDENCE)
               if not p.exists()]
    check("P1 governing files exist", not missing,
          "all 4 present" if not missing else f"missing {missing}")

    # P2 -----------------------------------------------------------------
    sections = re.findall(r"^## (\d+)\.", read(TEMPLATE), re.M)
    check("P2 template sections 0-15",
          sections == [str(i) for i in range(16)],
          f"{len(sections)} sections found")

    # P3 -----------------------------------------------------------------
    ptext = read(PROMPT)
    steps = re.findall(r"^## STEP (\d)", ptext, re.M)
    gates = re.findall(r"^G(\d):", ptext, re.M)
    check("P3 prompt STEP 1-7 + gates G1-G6",
          steps == [str(i) for i in range(1, 8)]
          and gates == ["1", "2", "3", "4", "5", "6"],
          f"steps={steps} gates={gates}")

    # P4 -----------------------------------------------------------------
    checks = re.findall(r"^## Check V(\d)", read(PROTOCOL), re.M)
    check("P4 protocol Check V1-V9",
          checks == [str(i) for i in range(1, 10)],
          f"found V{','.join(checks)}")

    # P5 -----------------------------------------------------------------
    raw = EVIDENCE.read_text(encoding="utf-8")
    rows = list(csv.reader(io.StringIO(raw)))
    header = rows[0] if rows else []
    problems = []
    if len(header) != 63:
        problems.append(f"{len(header)} cols, expected 63")
    if header != expected_columns():
        problems.append("does not match the prompt's field list")
    if any(not c.strip() for c in header):
        problems.append("blank column name")
    if len(header) != len(set(header)):
        problems.append("duplicate column name")
    if not raw.endswith("\n"):
        problems.append("no trailing newline: append would weld row 1 to header")
    check("P5 evidence CSV header", not problems,
          "63 cols, matches prompt, no blanks/dupes, ends with newline"
          if not problems else "; ".join(problems))

    # P6 -----------------------------------------------------------------
    targets = [EVIDENCE]
    if PER_PAPER.exists():
        targets += sorted(PER_PAPER.glob("*.md"))
    for extra in ("MASTER_EVIDENCE_VERIFY_SAMPLE.csv",
                  "MASTER_EVIDENCE_VERIFY_SAMPLE_DONE.csv",
                  "MASTER_VERIFICATION_REPORT.md"):
        p = REPO / "08_docs" / extra
        if p.exists():
            targets.append(p)
    hits = []
    for t in targets:
        for i, line in enumerate(read(t).splitlines(), 1):
            if re.search(FORBIDDEN, line):
                hits.append(f"{t.name}:{i}")
    check("P6 V4.1 forbidden numbers (evidence only)", not hits,
          f"0 matches across {len(targets)} target(s)"
          if not hits else f"{len(hits)} matches: {hits[:5]}")

    # P7 -----------------------------------------------------------------
    with MASTER.open(newline="", encoding="utf-8") as fh:
        mrows = list(csv.DictReader(fh))
    audit = json.loads(read(AUDIT))
    problems = []
    if len(mrows) != 171:
        problems.append(f"{len(mrows)} rows, expected 171")
    for col, want in CANON.items():
        got = Counter(r.get(col, "") for r in mrows)
        if any(got.get(k, 0) != v for k, v in want.items()):
            problems.append(f"{col}={dict(got)} want {want}")
    if audit.get("distribution") != CANON_AUDIT_DIST:
        problems.append("audit of record diverges from canonical vectors")
    check("P7 master CSV canonical + audit-aligned", not problems,
          "171 rows; all three vectors and the audit agree"
          if not problems else "; ".join(problems))

    # P8 -----------------------------------------------------------------
    probes = ["pdf_numeric_probe_v1.csv", "pdf_numeric_probe_v1.json",
              "PDF_NUMERIC_PROBE_REPORT.md", "PREFLIGHT_FINDINGS.md"]
    missing = [n for n in probes if not (PROBE_DIR / n).exists()]
    check("P8 probe outputs exist", not missing,
          "all 4 artifacts present" if not missing else f"missing {missing}")

    # report -------------------------------------------------------------
    width = max(len(c[0]) for c in results)
    print("=" * (width + 24))
    print(f"{'CHECK'.ljust(width)}  RESULT    DETAIL")
    print("=" * (width + 24))
    for cid, ok, detail in results:
        print(f"{cid.ljust(width)}  {'PASS' if ok else 'FAIL':<9} {detail}")
    print("=" * (width + 24))
    failed = [c[0] for c in results if not c[1]]
    print(f"{len(results) - len(failed)}/{len(results)} pre-flight checks pass")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    print("Pre-flight state is consistent. Next: resolve the gate-V9 scope")
    print("decision (PREFLIGHT_FINDINGS.md section 3), then run the extraction")
    print("agent on 08_docs/MASTER_EXTRACTION_PROMPT.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())