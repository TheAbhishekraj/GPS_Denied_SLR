# SUBMISSION CHECKLIST — GPS_Denied_SLR

Updated: 2026-10-02T06:37:33Z
Audit basis: Station 9 / Gate 9.4 audit PASS (L5 18/18, L7 0, L2 0 genuine untraceable).

## Target venue
- Primary: **IEEE Access**
- Scope: SLR on GPS-denied UAV navigation, multi-sensor fusion (2010–2026).

## Corpus (locked canonical)
2,000 identified (IEEE 1,000 + Scopus 1,000) -> 1,716 after dedup
-> 636 screened -> 291 full-text -> 285 INCLUDE / 6 EXCLUDE -> 279 corpus (+6 deferred).

## Manuscript
| file | bytes | sha256 |
|---|---|---|
| 07_manuscript/MANUSCRIPT_V4.md | 49219 | `E5D470B6B5DC8E35A5EF99AB413E97DEEE7F4C97DDD6CCFD172BA34CF7D869DB` |
| 07_manuscript/references.bib (279 entries) | 93314 | `B64E0648D35415B743F37622A286F382E7B76594F471C53FEF27FF2A6C0220F8` |

## Figures (regenerated, traceable)
| # | figure | sha256 |
|---|---|---|
| F1 | PRISMA flow | `720586F3BB7901296039653D672214A4E71C2D3F122676019DC1983699628242` |
| F2 | Publications per year | `AB4AD9D0F3FAB064938630B554F08B611488E9DCAE89580BDFEAED73A8A4768F` |
| F3 | Sensor modality by epoch | `AA172246750860CD1EBF54095C316121043C389DBFD6BADAD76A4929E1AD6F0F` |
| F4 | Fusion-pair evolution | `D71865D4396825D45334AF2E76590F94876C4FA655E17F5A6442C4C99A581AF0` |
| F5 | Environment distribution | `0D9443D51E6C1FF3FA6CC82610AF299856E32CB3F35E0136E0F9BDC34917CA84` |
| F6 | Taxonomy distribution | `4F465363D94625FAF14022FAC21D412027FC07C42166AF6C6F68231F42E84FD4` |
| F7 | Validation fidelity | `63AF5E340D0E2B45CCFE6648F7EE2E7C6585669270CD2B73C7457EC0593C8A94` |
| F8 | Contributing countries | `07817BA091ACCF723932F0129B48CC47EB20F86BC83090EB8A8C2E2C4E18420C` |
| F9 | Limitation and future themes | `8A5F3CF04F37E649D62380FA611DF6389CA010C236AB833368ABD19C66F3478B` |

## Tables (manuscript, traced sources)
| # | table | source |
|---|---|---|
| T-II | Chronological publication trajectory | MASTER_EVIDENCE.csv year |
| T-III | Sensor modality frequency | RQ_DATA_ANALYTICS.json sensor_by_epoch |
| T-3 | Fusion-pair evolution | RQ_DATA_ANALYTICS.json fusion_pairs_by_epoch |
| T-IV | Environment categorization | RQ_DATA_ANALYTICS.json env_distribution |
| T-5 | Algorithmic family vs validation | RQ_DATA_ANALYTICS.json algo_families_vs_validation |
| T-6 | Q-High anchors (REC_0037/0502/1277) | MASTER_EVIDENCE.csv + quality_appraisal_scored.csv |
| T-7 | Limitations and future priorities | RQ_DATA_ANALYTICS.json limitation/future themes |

## Supplementary files
- S1 evidence matrix: 06_analysis/outputs/inference_table.csv
- S2 figure data tables: 06_analysis/outputs/tables/F1_data.csv ... F9_data.csv
- S3 PRISMA run report: 06_analysis/outputs/figures/FIGURES_RUN_REPORT.md
- S4 number trace: 08_docs/NUMBER_TRACE.md
- S5 inclusion/exclusion criteria: 00_scope/SCOPE.md
- S6 screening register: 02_data_processed/screening_results.csv (285 INCLUDE, 6 EXCLUDE)
- S7 PDF removal log: 02_data_processed/pdf_removal_log.csv

## Author contributions
[PENDING HUMAN CONFIRMATION] — placeholder.

## Conflict of interest
[PENDING HUMAN CONFIRMATION] — placeholder.

## Data availability
[PENDING HUMAN CONFIRMATION] — candidate statement: raw exports (01_data_raw/), screening results
(02_data_processed/screening_results.csv), the frozen anchor (08_docs/ANCHOR_FREEZE_20260919.md), per-batch page text
(02_data_processed/evidence_batches/BATCH_BXX_pages/), and all scripts (06_analysis/scripts/) are retained in the project repository.

## Known blockers before submission
- 5 extraction records flagged for re-extraction: REC_1083, REC_1084, REC_1085, REC_1095, REC_1096.
- 21 author name strings carry upstream encoding loss (diacritics replaced by "?") in references.bib.
- 91 of 279 bibliography entries have no venue in the corpus files (marked NOT_REPORTED).
- Final human proofread of MANUSCRIPT_V4.md.

## Attestation
- No submission made yet. Awaiting final human authorization.
