# SYNTHESIS REPORT — GPS_Denied_SLR

Generated: 2026-09-19T20:35:00Z
Scope: 06_analysis/outputs/ derived from 02_data_processed/MASTER_EVIDENCE.csv
Method: 08_docs/SYNTHESIS_METHOD.md (structured narrative synthesis; no pooling)
Status: STRUCTURALLY COMPLETE — SUBSTANTIVELY EMPTY (interpretive pass not yet run)

## 1. Verified row count
- MASTER_EVIDENCE.csv rows: **279**
- Source: 02_data_processed/MASTER_EVIDENCE.csv (SHA256 recorded in _AUDIT/PHASE_6_COMPLETION.md)
- 279 = 285 INCLUDE − 6 deferred (REC_0023, REC_0035, REC_0244, REC_1217,
  REC_1667, REC_0363)
- PDFs on disk: 288 (05_papers_fulltext/, file listing)

## 2. Taxonomy breakdown
| field | value | count |
|---|---|---|
| taxonomy_category | NOT_REPORTED | 279 |
| method_category | NOT_REPORTED | 279 |
| environment | NOT_REPORTED | 279 |
| real_or_sim | NOT_REPORTED | 279 |

Source: 06_analysis/outputs/taxonomy_distribution.csv (4 data rows).
**No substantive distribution can be reported.** The Phase 6 run used the
deterministic extractor only (approved design): it populates `id`, `title`,
`doi`, `_source_pages` from each PDF and writes `NOT_REPORTED` for the other
24 fields. The interpretive pass (which reads the archived
BATCH_BXX_pages/REC_XXXX.txt text under EXTRACTION_RULES E1–E12) has not run.

This is reported as a finding, not smoothed over: per Rule 5, missing =
NOT_REPORTED, and per SYNTHESIS_METHOD an unreported value is itself the
finding. No value was inferred, estimated, imputed, or converted.

## 3. What IS populated (traceable)
| field | populated rows (of 279) | notes |
|---|---|---|
| id | 279 | from PDF filename |
| title | 279 | largest-font page-1 block |
| doi | 0 | NOT_REPORTED: these PDFs carry the DOI in a page footer, outside the page-1 header window used by the extractor |
| _source_pages | 279 | page-count range, physical numbering convention |

## 4. Key findings (from available data only)
1. Corpus mechanics are sound: 279/279 rows carry a title and a page range;
   0 duplicate IDs; 0 empty required fields (validate_master.py, Overall PASS).
2. Stage-1 screening titles and PDF page-1 titles agree for every batch
   spot-verified during extraction; 0 identity conflicts among the 279.
3. The 6 deferred IDs remain unresolved and unextracted by instruction.

## 5. Gaps (Section 17 inputs) — NOT DERIVABLE YET
Research-gap synthesis requires per-paper `limitations` / `future_work`
content, which is NOT_REPORTED for all 279 rows. No gap analysis is offered
rather than an invented one.

## 6. Best combinations and accuracy (Section 18 inputs) — NOT DERIVABLE YET
`headline_result`, `sensors`, `algorithm`, `baseline` are NOT_REPORTED for all
279 rows. No best-configuration or accuracy summary is offered.

## 7. Figures
Deferred by human decision (Rule 9 spec required for figures.py).
No figure was generated. F1–F9 remain outstanding; see
_AUDIT/PHASE_7_COMPLETION.md.

## 8. Method compliance
- No pooled effect sizes or confidence intervals: none computed.
- No unit conversion: nothing to convert (no metrics reported).
- NOT_REPORTED preserved as NOT_REPORTED throughout.
- Every number above traces to MASTER_EVIDENCE.csv, to a listing of
  05_papers_fulltext/, or to 06_analysis/outputs/*.csv.

## 9. What unblocks substantive synthesis
The interpretive pass: for each of the 279 rows, read
`02_data_processed/evidence_batches/BATCH_BXX_pages/REC_XXXX.txt` and populate
the 24 interpretive fields with verbatim quotes + page numbers per
EXTRACTION_RULES E1–E12, then re-run validate_master.py and regenerate these
outputs. Until then this report remains empty by design.
