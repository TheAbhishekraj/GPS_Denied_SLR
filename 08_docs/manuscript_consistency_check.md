# manuscript_consistency_check.md — Data Consistency Sweep
**Review Domain:** Autonomous Navigation & Localization for UAVs in GPS-Denied Environments  
**Unresolved Mismatches:** 0

---
## 1. Canonical Corpus Metrics Sweep

| Metric Domain | Claimed Value | CSV Source Path | Source Value | Status |
|---|---|---|---|---|
| Raw Database Records | 2,000 | `01_data_raw/SEARCH_LOG.md` | 2,000 | PASS |
| Deduplicated Records | 1,719 | `02_data_processed/deduplicated.csv` | 1,719 | PASS |
| Included SLR Papers | 636 | `02_data_processed/extracted_master.csv` | 636 | PASS |
| Excluded Records | 39 | `02_data_processed/screened_excluded.csv` | 39 | PASS |
| Extracted Dataset Rows | 636 | `02_data_processed/extracted_master.csv` | 636 | PASS |
| Core/Important Papers | 36 | `02_data_processed/core_papers.csv` | 36 | PASS |
| Snowball Seeds | 36 | `08_docs/snowball_log.csv` | 36 | PASS |

---
## 2. Validation & Quality Appraisal Mapping

| Phase / Stage | Validation Parameter | Result | Target Benchmark | Gate Status |
|---|---|---|---|---|
| Phase 5 Screening | Sample size / seed | 172 rows (seed=42) | N >= 100 | PASS |
| Phase 5 Screening | Inter-rater agreement (κ) | 0.874 | κ >= 0.80 | ACCEPT |
| Phase 7 Extraction | Validation sample size | 20 papers (seed=42) | N = 20 | PASS |
| Phase 7 Extraction | Field extraction agreement | 100% | 100% | PASS |
| Quality Appraisal | Q-high / Q-medium Papers | 36 papers | Inform headline claims | PASS |
| Quality Appraisal | Q-low Papers | 600 papers | Corpus statistics | PASS |

---
## 3. Verification Summary

**RESULT: PASS — 0 unresolved mismatches.** All manuscript metrics synchronized.