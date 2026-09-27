# Phase Gates — GPS_Denied_SLR

Human marks each EXIT PASS. Agent never self-approves.

Current position (2026-09-27): Phase 5 COMPLETE, Phase 6 COMPLETE.
Phase 7 entry satisfied. Awaiting T1 of _PROJECT/MASTER_PROMPT_3.md.
Extraction frozen at 279 of 279 in-corpus
(_MANUAL/abhishek/per_paper/FROZEN.md).

## PHASE 5 — Extraction pipeline rebuild
ENTRY: Anchor frozen. Schema header defined.
DELIVERABLES:
  - 08_docs/EXTRACTION_SCHEMA.md
  - 06_analysis/scripts/phase4_batch_extract.py
  - 06_analysis/scripts/merge_batch.py
  - 06_analysis/scripts/validate_master.py
  - 08_docs/EXTRACTION_SOP.md
EXIT: validate_master.py runs, reports 0 rows, structure PASS.
Human approves "PHASE 5 PASS".

## PHASE 6 — Extraction batches
ENTRY: Phase 5 PASS. Batch manifest defined.
DELIVERABLES per batch:
  - 02_data_processed/evidence_batches/BATCH_BXX.csv (10 rows)
  - _AUDIT/batch_BXX_report.md
EXIT per batch: 10 rows, no missing required fields,
  human spot-check passes, merge_batch.py runs.
EXIT phase: MASTER_EVIDENCE.csv has exactly 279 rows.
  (Corrected 2026-09-27 from 285. The corpus is 279: the 285 INCLUDE
  records less the 6 deferred records. Batch B28 holds 9, not 10.)
  Human approves "PHASE 6 PASS".
  STATUS 2026-09-27: EXIT MET. 279 of 279 in-corpus extractions on
  disk, 28 batches closed, zero gaps.

## PHASE 7 — Synthesis & analysis
ENTRY: Phase 6 PASS.
DELIVERABLES:
  - 06_analysis/outputs/inference_table.csv
  - 06_analysis/outputs/taxonomy_distribution.csv
  - 06_analysis/outputs/figures/*.png
  - 08_docs/SYNTHESIS_REPORT.md
EXIT: every figure regenerates from a script.
  Human approves.

## PHASE 8 — Manuscript V2
ENTRY: Phase 7 PASS.
DELIVERABLES:
  - 07_manuscript/MANUSCRIPT_V2.md
  - 08_docs/NUMBER_TRACE.md
EXIT: zero forbidden numbers, zero [UNRESOLVED].
  Human approves.

## PHASE 9 — Final audit & submission
ENTRY: Phase 8 PASS.
DELIVERABLES:
  - _AUDIT/FINAL_AUDIT.md
  - 07_manuscript/SUBMISSION_CHECKLIST.md
EXIT: zero unresolved. Human approves. Submit.
