# Phase Gates — GPS_Denied_SLR

Human marks each EXIT PASS. Agent never self-approves.

Current position: Phase 4 complete. Ready for Phase 5.

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
EXIT phase: MASTER_EVIDENCE.csv has exactly 285 rows.
  Human approves "PHASE 6 PASS".

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
