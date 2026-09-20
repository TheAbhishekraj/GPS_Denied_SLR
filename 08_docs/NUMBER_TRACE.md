# NUMBER_TRACE — GPS_Denied_SLR

Generated: 2026-09-19T20:40:00Z
Scope: every number appearing in 07_manuscript/MANUSCRIPT_V2.md
Rule: no number without a source file + row/line. Zero exceptions.

| # | number in manuscript | where used | source file | row / line | verification |
|---|---|---|---|---|---|
| 1 | 2,000 | Abstract; Methods 3.6; Conclusion | 01_data_raw/ieee_xplore_20260615.csv + 01_data_raw/scopus_20260615.csv | 1,000 rows + 1,000 rows (row count) | Import-Csv Measure-Object = 1000 each |
| 2 | 1,000 (IEEE) | Abstract; Methods 3.2 | 01_data_raw/ieee_xplore_20260615.csv | data rows | row count = 1000 |
| 3 | 1,000 (Scopus) | Abstract; Methods 3.2 | 01_data_raw/scopus_20260615.csv | data rows | row count = 1000 |
| 4 | 1,716 | Abstract; Methods 3.6; Conclusion | 02_data_processed/deduplicated_master.csv | data rows | row count = 1716; also 08_docs/ANCHOR_FREEZE_20260919.md line 8 |
| 5 | 636 | Abstract; Methods 3.6; Conclusion | 02_data_processed/screened_included_v2.csv | data rows | row count = 636; ANCHOR_FREEZE line 9 |
| 6 | 291 | Abstract; Methods 3.6; Conclusion | 02_data_processed/screening_results.csv | data rows | row count = 291; ANCHOR_FREEZE line 10 |
| 7 | 285 | Abstract; Methods 3.3/3.6; Results 4.1; Limitations 2; Conclusion | 02_data_processed/screening_results.csv | decision = INCLUDE | Group-Object decision = 285; ANCHOR_FREEZE line 13 |
| 8 | 6 (EXCLUDE) | Abstract; Methods 3.3 | 02_data_processed/screening_results.csv + 02_data_processed/pdf_removal_log.csv | decision = EXCLUDE (6); removal log rows 2-4 | Group-Object decision = 6; ANCHOR_FREEZE line 14 |
| 9 | 3 (E1) / 3 (E2) | Abstract; Methods 3.3 | 08_docs/ANCHOR_FREEZE_20260919.md | lines 19-21 (E1 x3), 22-24 (E2 x3) | matches pdf_removal_log decisions |
| 10 | 288 (PDFs) | Abstract; Methods 3.6 | 05_papers_fulltext/ | *.pdf file listing | Get-ChildItem -Filter *.pdf = 288 |
| 11 | 279 | Abstract; Methods 3.6; Results 4.1; Limitations 1-2; Conclusion | 02_data_processed/MASTER_EVIDENCE.csv | data rows | row count = 279; _AUDIT/PHASE_6_COMPLETION.md |
| 12 | 28 (batches) | Methods 3.5 | _AUDIT/PHASE_6_COMPLETION.md | batch manifest table (28 rows) | 28 BATCH_BXX.csv files on disk |
| 13 | 27 x 10 + 1 x 9 | Methods 3.5 | _AUDIT/PHASE_6_COMPLETION.md | batch manifest row counts | B01-B27 = 10 rows, B28 = 9 rows; 27*10+9 = 279 |
| 14 | 28 (columns) | Methods 3.5 | 08_docs/EXTRACTION_SCHEMA_v1.md | column table rows 1-28 | header comparison = exact match |
| 15 | 0 duplicate IDs | Results 4.1 | _AUDIT/master_validation.md | "Duplicate IDs" row | validate_master.py output |
| 16 | 0 empty required fields | Results 4.1 | _AUDIT/master_validation.md | "Empty required fields" row | validate_master.py output |
| 17 | 6 (deferred) | Abstract; Methods 3.6; Limitations 2 | _AUDIT/PHASE_6_COMPLETION.md | deferred IDs section | REC_0023, REC_0035, REC_0244, REC_1217, REC_1667, REC_0363 |
| 18 | 279/279 NOT_REPORTED (per field) | Results 4.2-4.5 | 06_analysis/outputs/taxonomy_distribution.csv | 4 data rows, count = 279 each | Export-Csv of Group-Object on MASTER |
| 19 | 24 (interpretive fields) | Limitations 1 | 08_docs/EXTRACTION_SCHEMA_v1.md | 28 columns − 4 deterministic (id,title,doi,_source_pages) | arithmetic on schema table; 28−4 = 24 |
| 20 | 0 data rows (QA_INDEX) | Results 4.6 | 03_extraction/per_paper/QA_INDEX.md | header only | file content check |

## Notes
- Every count above was obtained by listing files or counting CSV rows during
  the 2026-09-19 run; no count is quoted from memory.
- Counts 11, 12, 13, 17 changed relative to the pre-deferral plan (285 → 279)
  because 6 INCLUDE records were deferred for identity audit. The frozen anchor
  (285/6) is unchanged; the difference is disclosed in Methods 3.6 and
  Limitations 2.
- No forbidden legacy number appears in the manuscript or in this trace.
