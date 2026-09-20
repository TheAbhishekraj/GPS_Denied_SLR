# Extraction SOP — GPS_Denied_SLR (Phase 6 batch workflow)

Status: Phase 5 deliverable. Governs Phase 6 extraction batches.

## Scope
Batch workflow for Phase 6: extract all 285 INCLUDE papers into
MASTER_EVIDENCE.csv via small, auditable batches. No extraction is
performed in Phase 5; this SOP only defines how Phase 6 will run.

## Reference documents
- Schema: 08_docs/EXTRACTION_SCHEMA_v1.md (28 columns, quote rule,
  enum allowed-values, missing-data policy)
- Rules: 08_docs/EXTRACTION_RULES.md (E1-E12: no fabrication,
  quote anchoring, unit fidelity, baseline honesty, etc.)
- Manuscript target: 08_docs/MANUSCRIPT_SPEC.md

## Batch parameters
- Batch size: 10 papers
- Naming: BATCH_B01.csv through BATCH_B29.csv
  (285 papers = 28 full batches of 10 + 1 final batch of 5)
- Location: 02_data_processed/evidence_batches/
- Manual spot-check: 1 in 10 rows per batch, human-reviewed
- Merge cadence: after every batch
- Rollback: restore MASTER_EVIDENCE.csv from _QUARANTINE_<timestamp>/

## Scripts used at Phase 6 (deferred — to be written at Phase 6 start)
- phase4_batch_extract.py  (read screening_results.csv, filter INCLUDE,
  extract one batch of 10 IDs from PDFs into a BATCH_BXX.csv)
- merge_batch.py           (validate a batch against the schema, reject
  duplicate IDs / missing required fields, append to MASTER_EVIDENCE.csv,
  log to _AUDIT/merge_log.csv; never overwrite)

## Rule 9 note
Each Phase 6 script requires a written spec (purpose, inputs with row
counts, outputs with row counts, side effects) and explicit human
approval BEFORE it is written. No script is created speculatively.

## Governing rules
- .clinerules Rule 1  — read before write
- .clinerules Rule 3  — write commands need per-command approval
- .clinerules Rule 7  — one phase at a time; human marks PASS
- .clinerules Rule 9  — no new scripts without a spec

## Known pre-Phase-6 blocker
The on-disk MASTER_EVIDENCE.csv header currently uses legacy column
names and does NOT match EXTRACTION_SCHEMA_v1.md (6 columns renamed /
reordered). validate_master.py reports Structure: FAIL until the header
is migrated to the v1 schema. Header migration is a separate approved
action on the allowlisted MASTER_EVIDENCE.csv; it must be completed
before Phase 6 batch insertion begins.
