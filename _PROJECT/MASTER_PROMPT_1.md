# MASTER_PROMPT_1 — Correction & File Hygiene

One-time run. Supersedes any earlier correction prompt.
Executes after governance installation. Stops before Phase 5.

================================================================
ROLE
================================================================
You are a file-hygiene agent for a PRISMA 2020 SLR project.
You fix two specific files and verify the anchor. You do not
extract, analyze, synthesize, or start any phase.

================================================================
PROJECT ROOT
================================================================
E:\GPS_Denied_SLR

================================================================
BINDING RULES
================================================================
Read .clinerules first and follow it. It overrides conflicting
instructions.

================================================================
ALLOWLIST FOR THIS RUN
================================================================
  _AUDIT/**
  08_docs/ANCHOR_FREEZE_20260919.md
  _PROJECT/MASTER_PROMPT.txt
  _QUARANTINE_CORRECTION_<timestamp>/**

Do not write anything else. Do not touch 01_data_raw/,
02_data_processed/, or 05_papers_fulltext/.

================================================================
FORBIDDEN NUMBERS
================================================================
Five legacy numeric strings must never appear in any live file.
They are documented by category only (see Section 5 of the
installation report for their identity).
If you find them in a live file, report line number and halt.

================================================================
TASK 0 — VERIFY SCHEMA AND RULES FILES EXIST
================================================================
Confirm these exist and report SHA256:
  08_docs/EXTRACTION_SCHEMA_v1.md
  08_docs/EXTRACTION_RULES.md
  08_docs/MANUSCRIPT_SPEC.md

If any is missing, STOP and report. Do not proceed.
(Added 2026-09-19 per coverage audit.)

================================================================
TASK 1 — VERIFY GOVERNANCE FILES EXIST
================================================================
Confirm these exist and report SHA256:
  .clinerules
  _PROJECT/MASTER_PROMPT.txt
  _PROJECT/PROJECT_CHARTER.md
  _PROJECT/END_GOAL.md
  _PROJECT/PHASE_GATES.md
  _PROJECT/MASTER_PROMPT_1.md
  _PROJECT/MASTER_PROMPT_2.md

================================================================
TASK 2 — VERIFY ANCHOR
================================================================
Read-only checks:
  - PDF count in 05_papers_fulltext/ (expect 288)
  - Row count of 01_data_raw/ieee_xplore_20260615.csv (expect 1000)
  - Row count of 01_data_raw/scopus_20260615.csv (expect 1000)
  - Row count of 02_data_processed/screening_results.csv (expect 291)
  - Decision breakdown: INCLUDE 285 / EXCLUDE 6
  - SHA256 of screening_results.csv
    (expect 86DADC842AA590B03C0F5145FFCA5340800CB41AE505BC7AD1488CB40648F6D7)

Report each result. Halt on any mismatch.

================================================================
TASK 3 — FIX 08_docs/ANCHOR_FREEZE_20260919.md
================================================================
The file contains the five forbidden legacy numbers at line 90
(literal values). This violates Rule 5.

Steps:
  1. Copy the current file to:
     _QUARANTINE_CORRECTION_<timestamp>/ANCHOR_FREEZE_before.md
     Record its SHA256.
  2. Rewrite the file with this content (the forbidden-value
     line replaced by a category reference; nothing else changes):

---BEGIN NEW CONTENT---
# Anchor Freeze — 2026-09-19

## Frozen counts
| Stage | Value |
|---|---|
| Raw records identified | 2,000 (IEEE 1,000 + Scopus 1,000) |
| Duplicates removed | 284 |
| Unique records after dedup | 1,716 |
| Records passing title/abstract | 636 |
| Full-text records assessed | 291 |
| PDFs on disk | 288 |
| PDFs pending retrieval | 3 (duplicate EXCLUDEs, not restored) |
| Studies INCLUDE | 285 |
| Studies EXCLUDE | 6 (3 x E1, 3 x E2) |

## Excluded records
| ID | Rule | Reason |
|---|---|---|
| REC_0053 | E1 | Out of scope |
| REC_0693 | E1 | Out of scope |
| REC_0866 | E1 | Out of scope |
| REC_1582 | E2 | Duplicate of REC_0274 |
| REC_1688 | E2 | Duplicate of REC_1715 |
| REC_1715 | E2 | Duplicate of REC_1688 |

## Removed duplicate PDFs
| Removed | Canonical | SHA256 prefix |
|---|---|---|
| REC_1582.pdf | REC_0274.pdf | 4D3DCB09 |
| REC_1688.pdf | REC_1715.pdf | 41AE7D59 |
| REC_1715.pdf | REC_1688.pdf | 41AE7D59 |

## File hashes (SHA256)
| File | SHA256 |
|---|---|
| 01_data_raw/ieee_xplore_20260615.csv | FE374C9F2A405A0F0E07598979340AE971311B80BB20D8E121572D648CAA18F3 |
| 01_data_raw/scopus_20260615.csv | EF162F4F9525B6FC5CC617D1E3BADACD11F09B3E80FDFC488C4E37918BD524CB |
| 02_data_processed/deduplicated_master.csv | A648930848EED1950A602EA5FA2F739CFDDB1C2BB1289F86B810211DB3D8649A |
| 02_data_processed/screened_included_v2.csv | CD1B38745FF653BE3E23C62371B87A12861261BDC057F4F313645C4A79E93CED |
| 02_data_processed/screening_results.csv | 86DADC842AA590B03C0F5145FFCA5340800CB41AE505BC7AD1488CB40648F6D7 |

## PRISMA flow
2,000 -> 1,716 -> 636 -> 291 -> 285 INCLUDE / 6 EXCLUDE

## Freeze rules
1. No count changes without a new freeze doc.
2. No decision changes without a new freeze doc.
3. No PDF removed without a new freeze doc.
4. Every extraction batch reconciles against this freeze.
5. Five legacy numeric strings are deprecated and must not
   appear in any live file. Their values are on record in
   _AUDIT/INSTALLATION_REPORT.md only. Do not reproduce them.

## Next phase
Phase 5 — Extraction pipeline rebuild. Target: 285 INCLUDE papers.
---END NEW CONTENT---

  3. Record the new SHA256.
  4. Log both hashes in _AUDIT/action_log.md.

================================================================
TASK 4 — FIX _PROJECT/MASTER_PROMPT.txt
================================================================
The file contains the five forbidden legacy numbers at line 46
(literal values). This violates Rule 5.

Steps:
  1. Copy the current file to:
     _QUARANTINE_CORRECTION_<timestamp>/MASTER_PROMPT_before.txt
     Record its SHA256.
  2. In the current file, replace the FORBIDDEN NUMBERS section
     with:

FORBIDDEN NUMBERS
Five legacy numeric strings are deprecated and must never appear
in any live file. Their values are on record in
_AUDIT/INSTALLATION_REPORT.md only. Do not reproduce them.
If found in a live file, report line number and halt.

  3. Do not change anything else in the file.
  4. Record the new SHA256.
  5. Log both hashes in _AUDIT/action_log.md.

================================================================
TASK 5 — SCAN FOR REMAINING OCCURRENCES
================================================================
Scan every live file (excluding _QUARANTINE_* folders and
_AUDIT/INSTALLATION_REPORT.md) for the five forbidden numeric
strings.

List every match with: file path, line number, snippet.

Expected result: zero matches in live files.

If matches remain, halt and report.

================================================================
TASK 6 — WRITE CORRECTION REPORT
================================================================
Write _AUDIT/CORRECTION_REPORT.md containing:
  - Timestamp
  - Anchor verification results (Task 2)
  - Files fixed (Task 3, Task 4) with before/after SHA256
  - Quarantine folder path
  - Forbidden-number scan results (Task 5)
  - Confirmation that nothing outside the allowlist was written
  - Confirmation that no analysis script was run

================================================================
TASK 7 — STOP
================================================================
Do not run Phase 5.
Do not run MASTER_PROMPT_2.md.
Do not run any Python script.

Report only:
  "CORRECTION COMPLETE. AWAITING PHASE 5 APPROVAL."

================================================================
END OF MASTER_PROMPT_1
================================================================
