# Supplementary Material — V1 (N = 171)

## S1. Package manifest — V1 (N = 171)
This package is tied to `02_data_processed/extracted_master_v2.csv`, `06_analysis/audit/V1_audit_20260917T124255Z.json`, `06_analysis/audit/V1_audit_20260917T124255Z.csv`, and `06_analysis/audit/MANUAL_REVIEW.md`.

## S2. Search strategy and PRISMA-S fields — V1 (N = 171)
Sources: IEEE Xplore and Scopus. Search window: 2010-01-01 through 2026-06-30. Record the complete database-specific strings, interface versions, search dates, and export formats before submission. No PDFs were downloaded during manuscript generation.

## S3. Eligibility and screening codes — V1 (N = 171)
I1–I6 and E1–E8 are reproduced from `00_scope/screening_criteria_v2.md`. The strict I2 primary-contribution test is binding. Stage-1 screening is separate from quality appraisal.

## S4. Extraction data dictionary — V1 (N = 171)
Fields: id, title, authors, year, DOI, venue, source, fulltext availability, pages, platform, sensors, primary method, method category, environment, experiment type, real/simulation label, metrics, ATE RMSE, application, multi-agent, notes, four QA dimensions, QA total/tier, QA notes, and citation tier.

## S5. Study-level quality and citation table — V1 (N = 171)
The complete 171-row table is in `07_manuscript/tables_V1.md`, Table VIII. QA dimensions follow the 0–10 rubric; no score is imputed outside the CSV.

## S6. Audit reconciliation — V1 (N = 171)
Audit disposition: 170 PASS + 1 PASS_EXCEPTION. REC_1137 was manually reviewed because equation-dense notation caused a short-token flag; disposition is PASS_EXCEPTION, with no genuine extraction failure.

## S7. Human-validation status — V1 (N = 171)
The governing SOP marks the 20-paper human validation as REVIEW REQUIRED. It is not represented as complete. The five-row seed-42 spot check is an audit reproducibility sample, not a substitute for the 20-paper validation.

## S8. Reporting-bias and certainty plan — V1 (N = 171)
Reporting-bias assessment and certainty-of-evidence grading require author completion. The package preserves NOT_REPORTED values and does not fabricate effect estimates. Complete these fields before submission.

## S9. Reproducibility and rendering instructions — V1 (N = 171)
Use relative repository paths. Recompute all derived tables from the authoritative CSV, verify totals against the audit JSON, render figures at the venue-required resolution, and run the submission checklist. Do not replace V1 counts with target-corpus values.

## S10. Audit report and manual review record — V1 (N = 171)
The audit JSON/CSV and manual review record are the source of truth for PDF-open status, field consistency, QA consistency, and the documented PASS_EXCEPTION. This section is the supplementary audit record, not a claim of completed human validation.
