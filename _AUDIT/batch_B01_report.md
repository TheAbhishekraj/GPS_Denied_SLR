# BATCH B01 — Extraction Report

Generated: 2026-09-19T19:20:00Z
Phase: 6 (extraction batches)
Status: EXTRACTED — AWAITING HUMAN APPROVAL TO MERGE
Spot-check: PENDING HUMAN REVIEW (D3 — 1-in-10 manual spot-check deferred)

## Batch identity
| field | value |
|---|---|
| batch | B01 |
| records | 10 (of 279 SAFE; 285 INCLUDE − 6 deferred) |
| extractor | 06_analysis/scripts/phase4_batch_extract.py (sha256 B959445C7EC6216C0A5E3C0CF433F2AF20AC6392152A2651E97B9B80B00120A2) |
| CLI | `--batch B01` (exit 0) |

## Reviewed artifact hash (read by merge_batch.py — amendment 2)
```
BATCH_B01.csv SHA256: 9E9E95BCACBC6A548B1CF65F8EDDFBEDDED309AFB903AC8E2E2B0749555D7457
```
`merge_batch.py --batch B01 --commit` will abort with HASH_MISMATCH unless the
batch file is byte-identical to this hash.

## Verification results
| check | expected | observed | result |
|---|---|---|---|
| data rows in BATCH_B01.csv | 10 | 10 | PASS |
| header == EXTRACTION_SCHEMA_v1.md (28 cols, exact order) | match | match | PASS |
| rows missing id / title / _source_pages | 0 | 0 | PASS |
| text files in BATCH_B01_pages/ | 10 | 10 | PASS |
| extractor exit code | 0 | 0 | PASS |

## IDs in this batch
REC_0001, REC_0003, REC_0006, REC_0008, REC_0010, REC_0013, REC_0017,
REC_0022, REC_0025, REC_0028

## Field population (by design)
- Filled from the PDF: `id`, `title`, `doi` (where a page-1 DOI exists),
  `_source_pages`.
- All other 24 fields: `NOT_REPORTED` — to be filled by the interpretive
  pass from `BATCH_B01_pages/REC_XXXX.txt` under EXTRACTION_RULES E1–E12.
- No value was inferred, converted, or substituted from another file.

## Notes / warnings
- `doi` is NOT_REPORTED for all 10 rows: these IEEE conference PDFs carry the
  DOI in a page footer, which the page-1 header region does not expose. The
  interpretive pass may capture it from the archived page text.
- Stage-1 screening titles and PDF page-1 titles agree for all 10 IDs — no
  identity conflict in this batch.
- Spot-check (D3) deferred: every batch is logged "spot-check pending human review".
