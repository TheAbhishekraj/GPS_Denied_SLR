# PRISMA 2020 Checklist Mapping — GPS_Denied_SLR

Generated: 2026-09-27T11:32Z (Scribe session).
Scope: all 27 PRISMA 2020 items mapped to the file that evidences them and to
the manuscript section that must report them.
Required by: `08_docs/MANUSCRIPT_SPEC.md` ("Map every PRISMA item (1-27) to a
page in the manuscript. Store mapping in 08_docs/PRISMA_CHECKLIST.md").

**Status vocabulary:** `COMPLETE` = evidence exists on disk · `PARTIAL` =
evidence exists but is incomplete or not yet written up · `PENDING` = no
evidence yet.

**Headline:** 9 COMPLETE · 7 PARTIAL · 11 PENDING.

---

## A. Front matter

| # | PRISMA item | Evidence on disk | Manuscript location | Status |
|---|---|---|---|---|
| 1 | Title identifies the report as a systematic review | `00_scope/SCOPE.md` Q1 | Title page | **COMPLETE** |
| 2 | Abstract: structured summary (background, objectives, eligibility, sources, risk of bias, included studies, synthesis, limitations, funding, registration) | `07_manuscript/MANUSCRIPT_V2.md` §Abstract | Abstract | **PARTIAL** — draft abstract discloses the corpus and defers the synthesis, but funding and registration fields are absent |

## B. Introduction

| # | PRISMA item | Evidence on disk | Manuscript location | Status |
|---|---|---|---|---|
| 3 | Rationale in the context of existing knowledge | `00_scope/SCOPE.md` Q1-Q2 | §1 Introduction | **COMPLETE** (drafted) |
| 4 | Explicit statement of objectives / questions | `00_scope/SCOPE.md` Q2 — RQ1-RQ4 | §1 Introduction | **COMPLETE** |

## C. Methods

| # | PRISMA item | Evidence on disk | Manuscript location | Status |
|---|---|---|---|---|
| 5 | Eligibility criteria (I1-I7, E1-E7) | `00_scope/SCOPE.md` Q5, Q6 | §3.3 | **COMPLETE** |
| 6 | Information sources (all databases, last search date) | `00_scope/SCOPE.md` Q3 (IEEE Xplore, Scopus); `01_data_raw/ieee_xplore_20260615.csv` (1,000 rows) + `scopus_20260615.csv` (1,000 rows) — date in filename = 2026-06-15 | §3.2 | **COMPLETE** |
| 7 | Full search strategy for every source | `supplementary/S2_search_queries.txt` (2,193 bytes) | §3.2 / supplementary | **PARTIAL** — file exists; not yet verified to contain the complete, reproducible string for both databases including the 2010-2026 limit |
| 8 | Selection process: reviewers, independence, tools, disagreement resolution | `08_docs/SCREENING_INDEPENDENCE.md` — **Case C selected 2026-09-19**: single human reviewer assisted by AI; AI decision + confidence + criteria + justification recorded per record; human verified all AI decisions. Columns confirmed present in `screening_results.csv`: `ai_decision, ai_confidence, criteria_triggered, justification, decision, rule` | §3.4 | **COMPLETE** — the Case C disclosure sentence must be reproduced verbatim |
| 9 | Data collection process: reviewers, independence, tools, confirmation | `08_docs/EXTRACTION_SOP.md`; `08_docs/EXTRACTION_SCHEMA_v1.md`; 28 batches | §3.5 | **PARTIAL** — the batch workflow, schema and tools are documented, but **no reviewer-independence statement exists for extraction** (only for screening). Compare `SCREENING_INDEPENDENCE.md`, which has no extraction equivalent. Must be disclosed before submission |
| 10a | Outcomes: list and define all outcomes | `08_docs/EXTRACTION_SCHEMA_v1.md` — `metrics`, `headline_result`, `baseline` (quote-anchored) | §3.5, §4.5 | **COMPLETE** (defined; values pending) |
| 10b | Other variables: list and define | `08_docs/EXTRACTION_SCHEMA_v1.md` — remaining 25 columns incl. `sensors`, `method_category`, `environment`, `platform`, `real_or_sim` | §3.5 | **COMPLETE** (defined; values pending) |
| 11 | Study risk of bias assessment: method, assessors, independence | Rubric is in `00_scope/SCOPE.md` Q7 (0-10; dimensions A Experimental Rigor 0-4, B Reporting Completeness 0-3, C Baseline Fairness 0-2, D Reproducibility 0-1; tiers Q-high 8-10 / Q-medium 5-7 / Q-low 0-4; simulation-only capped at Q-medium; dual-appraiser on 20% with ICC(2,1) or weighted kappa >= 0.75) | §3.7 (to be added) | **PENDING** — see Open Finding P1. `03_extraction/per_paper/QA_INDEX.md` has a header and **0 data rows**; no paper has been scored |
| 12 | Effect measures for each outcome | `08_docs/SYNTHESIS_METHOD.md` — no pooling; metrics reported as printed (ATE, RMSE, relative drift); Rule E5 unit fidelity; Rule E6 ranges copied not averaged | §3.8 | **COMPLETE** — the decision *not* to compute pooled effect measures is itself documented and justified (heterogeneity, figure-only reporting) |
| 13 | Synthesis methods (13a eligibility, 13b preparation, 13c missing data, 13d synthesis method, 13e heterogeneity, 13f sensitivity) | `08_docs/SYNTHESIS_METHOD.md` — **FINAL, approved 2026-09-19**: structured narrative synthesis with descriptive tabulation; grouping by `taxonomy_category`, `method_category`, `environment`, `real_or_sim`; missing data stays NOT_REPORTED as a finding; no unit conversion, no imputation | §3.8 | **COMPLETE** (the method statement; the synthesis itself is PENDING) |

## D. Methods — items with no evidence yet

| # | PRISMA item | Status | Note |
|---|---|---|---|
| 14 | Reporting bias assessment (risk of bias due to missing results) | **PENDING** | No method documented. `00_scope/SCOPE.md` does not address reporting bias. Needed before submission |
| 15 | Certainty assessment (e.g. GRADE) | **PENDING** | No method documented. `SYNTHESIS_METHOD.md` does not mention certainty. Needed before submission, even if the answer is "not performed, with rationale" |

## E. Results

| # | PRISMA item | Evidence on disk | Manuscript location | Status |
|---|---|---|---|---|
| 16a | Study selection: numbers at every stage | `08_docs/ANCHOR_FREEZE_20260919.md`; re-measured 2026-09-27T13:10Z: raw 1,000 + 1,000 = 2,000; `deduplicated_master.csv` 1,716 rows; `screened_included_v2.csv` 636 rows; `screening_results.csv` 291 rows (285 INCLUDE / 6 EXCLUDE); `05_papers_fulltext/` 288 PDFs; `MASTER_EVIDENCE.csv` 279 rows = the extraction corpus = the union of BATCH_B01-B28 (both sets 279, verified identical) | §3.6, Fig. F1 | **COMPLETE** — note: `_MANUAL/abhishek/per_paper/` holds 288 `.md` files, of which 279 are in-corpus and 9 are out-of-corpus; the corpus denominator is 279, not 288 (see `_MANUAL/abhishek/per_paper/FROZEN.md` and `_AUDIT/FINDINGS_20260927_CORPUS_INTEGRITY.md`) |
| 16b | Study selection: excluded studies with reasons | `ANCHOR_FREEZE_20260919.md` "Excluded records" table gives all 6 with rule and reason (REC_0053, REC_0693, REC_0866 = E1 out of scope; REC_1582 = E2 duplicate of REC_0274; REC_1688 = E2 duplicate of REC_1715; REC_1715 = E2 duplicate of REC_1688). Verified identical to the 6 `decision = EXCLUDE` rows in `screening_results.csv`. `pdf_removal_log.csv` records the removed duplicate PDFs | §3.6 | **PARTIAL** — the 6 full-text exclusions are fully enumerated with reasons, but the **1,080 records excluded at title/abstract** (1,716 − 636) have no aggregated reason breakdown. `screening_results.csv` carries a `rule` column that would support one; it has not been tabulated |
| 17 | Study characteristics: cite each study and present its characteristics | `02_data_processed/MASTER_EVIDENCE.csv` (279 rows x 28 cols); **all 279** have an 18-section interpretive summary on disk, frozen by SHA256 | §4.1, supplementary T2 | **PENDING** — 24 of the 28 columns are `NOT_REPORTED` for all 279 rows. The extraction corpus reached 279 of 279 (100.0%) on 2026-09-27, but the summaries live in `_MANUAL/abhishek/per_paper/` and have not yet been merged back into `MASTER_EVIDENCE.csv` (task T2). Additionally `year` is missing for 279/279 and `doi` for 247/279 (findings D-4a/D-4b) |
| 18 | Risk of bias in each study | — | §4.6 | **PENDING** — no QA scores exist (see item 11) |
| 19 | Results of individual studies (summary statistics per study) | — | §4.2-4.5 | **PENDING** — `headline_result`, `metrics`, `baseline` are `NOT_REPORTED` 279/279 |
| 20a | Results of syntheses: characteristics of contributing studies | — | §4 | **PENDING** |
| 20b | Results of syntheses: summary estimates and heterogeneity | — | §4 | **PENDING** — by design no pooled estimate will be reported (`SYNTHESIS_METHOD.md`); ranges are reported as printed |
| 20c | Investigations of causes of heterogeneity | — | §4 | **PENDING** |
| 20d | Sensitivity analyses | — | §4 | **PENDING** |
| 21 | Reporting biases (risk of bias due to missing results) | — | §4 | **PENDING** |
| 22 | Certainty of evidence | — | §4 | **PENDING** |

## F. Discussion

| # | PRISMA item | Evidence on disk | Manuscript location | Status |
|---|---|---|---|---|
| 23a | General interpretation in the context of other evidence | — | §5 Discussion | **PENDING** |
| 23b | Limitations of the evidence included | `07_manuscript/MANUSCRIPT_V2.md` §6 items 1, 5, 6 | §6 | **PARTIAL** — drafted (interpretive fields empty, DOI coverage, no meta-analysis); will change once Phase 7 lands |
| 23c | Limitations of the review processes | `07_manuscript/MANUSCRIPT_V2.md` §6 items 2, 3, 4: six deferred records; single reviewer + AI (Case C); 28 spot-checks pending | §6 | **PARTIAL** — drafted; the pending spot-checks and the deferral of 6 records must remain in this section |
| 23d | Implications for practice, policy, future research | — | §5, §7 | **PENDING** |

## G. Other information

| # | PRISMA item | Evidence on disk | Manuscript location | Status |
|---|---|---|---|---|
| 24 | Registration and protocol: registration, protocol access, amendments | `00_scope/SCOPE.md` frozen 2026-09-19; SHA256 recorded in `00_scope/FROZEN.md` as `2126485248762E0DC9ECC4E96A07AE9BEAB3F4E380EC86CE3E9FD09C3370B861` and **re-verified MATCH on 2026-09-27**; no amendments recorded | §3.1 (states the protocol is frozen and was not modified) | **PARTIAL** — the protocol and its integrity are documented, but the manuscript does **not** state whether the review was prospectively registered (e.g. PROSPERO) or was not registered. Item 24 requires that statement explicitly |
| 25 | Support: financial and non-financial support; role of funders | — | Acknowledgements (to be added) | **PENDING** |
| 26 | Competing interests: declarations for all authors | — | Declarations (to be added) | **PENDING** |
| 27 | Availability of data, code and other materials | `06_analysis/scripts/` (7 scripts); `01_data_raw/` (frozen exports); `08_docs/ANCHOR_FREEZE_20260919.md`; `supplementary/` (S1-S8); repo `https://github.com/TheAbhishekraj/GPS_Denied_SLR` | Data availability statement (to be added) | **PARTIAL** — materials exist and are organised, but no data-availability statement has been written, and the PDF corpus cannot be redistributed (must be stated) |

---

## H. Open findings raised by this mapping

| ID | Finding | Severity | Action required |
|---|---|---|---|
| **P1** | `RULINGS.md` R2 declares `00_scope/quality_appraisal_rubric.md` to be *"the sole binding rubric"* with `qa_*` columns — but **that file does not exist**. `00_scope/` contains only `SCOPE.md` and `FROZEN.md`; the rubric content lives inside `SCOPE.md` Q7 instead. R2 also refers to `qa_*` columns in `extracted_master.csv`, a **superseded V1 artifact** outside the frozen corpus. | MEDIUM | Human ruling: create the rubric file, or amend R2 to point at `SCOPE.md` Q7 |
| **P2** | `08_docs/EXTRACTION_RULES.md` E11 requires unclear decisions to be logged in `_AUDIT/rules_log.md`. **That file does not exist.** No rule decision has ever been logged. | LOW | Create the file, or amend E11 |
| **P3** | `08_docs/MANUSCRIPT_SPEC.md` names `08_docs/PRISMA_FLOW.md` as the F1 source. **That file does not exist.** | LOW | Create it, or point F1 at the anchor freeze document |
| **P4** | No reviewer-independence statement exists for **extraction** (item 9), although one exists for screening (Case C). | MEDIUM | Human must confirm and disclose |
| **P5** | No method is documented for reporting-bias assessment (item 14) or certainty assessment (item 15). | MEDIUM | Human decision before submission |
| **P6** | The 1,080 title/abstract exclusions have no reason breakdown (item 16b), though `screening_results.csv.rule` would support one. | LOW | Tabulate from the `rule` column (write action, needs approval) |
| **P7** | Nine extraction files in `_MANUAL/abhishek/per_paper/` belong to records **outside** the frozen 279-paper corpus. Three of them (`REC_0053`, `REC_0693`, `REC_0866`) are records that screening **EXCLUDED**. Six (`REC_0023`, `REC_0035`, `REC_0244`, `REC_0363`, `REC_1217`, `REC_1667`) are deferral-set records. The directory therefore reads 288 files against a 279 corpus. | HIGH | Human ruling — see `_AUDIT/FINDINGS_20260927_CORPUS_INTEGRITY.md` findings C-1/C-2/C-3 |
| **P8** | ~~`REC_1453` is in the corpus but its recorded title is the literal string "Preprint not peer reviewed"~~ | ~~MEDIUM~~ | **RESOLVED 2026-09-27** — three-way identity check proved `REC_1453` is a peer-reviewed *Measurement* (Elsevier) 2026 article (`10.1016/j.measurement.2026.121787`). The corpus stays at 279 and the anchor is unchanged. The "Preprint" string is a metadata defect in `MASTER_EVIDENCE.csv` only → folded into P10 |
| **P9** | Five in-corpus files (`REC_1083`, `REC_1084`, `REC_1085`, `REC_1095`, `REC_1096`) use the superseded 17-heading legacy template and cite the retired `extracted_master_v2.csv`, so they cannot feed the same downstream fields as the other 283 in-corpus files. | LOW | Re-template, or mark `TEMPLATE: LEGACY` as a documented exception |
| **P10** | `MASTER_EVIDENCE.csv` metadata defects, measured across all 279 rows: `year` = NOT_REPORTED for **279 of 279**; `doi` = NOT_REPORTED for **247 of 279**; 15 titles longer than 180 characters (concatenated harvest artefacts); 2 titles containing the string "Preprint" (`REC_1118`, `REC_1453`). Every one of the 247 missing DOIs and the missing years is recoverable verbatim from `screening_results.csv`. | HIGH | Approve the T1 join script. `MASTER_EVIDENCE.csv` is writable under Rule 2; record before/after SHA256 |

---

## I. Summary

| Status | Count | Items |
|---|---:|---|
| **COMPLETE** | 9 | 1, 3, 4, 5, 6, 8, 10, 12, 13 |
| **PARTIAL** | 7 | 2, 7, 9, 16, 23, 24, 27 |
| **PENDING** | 11 | 11, 14, 15, 17, 18, 19, 20, 21, 22, 25, 26 |
| **TOTAL** | **27** | |

**Reading of the counts.** The 11 PENDING items are almost entirely downstream of
one blocker: merging the interpretive content back into `MASTER_EVIDENCE.csv`.
The extraction corpus reached **279 of 279 (100.0%)** on 2026-09-27, with all 279
summaries on disk in `_MANUAL/abhishek/per_paper/` and frozen by SHA256. Items
17-22 cannot be written until `MASTER_EVIDENCE.csv` carries the 24 interpretive
fields (task T2) and its `year`/`doi` metadata is repaired (tasks T1, finding
P10). Items 11 and 18 additionally require QA scores, of which 0 of 279 exist
(task T3). Items 25, 26 and the registration clause of 24 are author-supplied
and are the human's to provide.

**One HIGH-severity item gates the numbers in this table.** Finding P7 means the
extraction directory reads 288 files against a 279-paper corpus. Until the 9
out-of-corpus files are dispositioned, any count taken from the directory alone
is wrong. The corpus denominator used throughout this mapping is **279**, taken
from `MASTER_EVIDENCE.csv` and confirmed identical to the union of the 28 batch
CSVs. The frozen authority for the directory is
`_MANUAL/abhishek/per_paper/FROZEN_MANIFEST_20260927.csv`, whose recorded SHA256
values were all verified against disk.

**No PRISMA item is marked COMPLETE on the basis of a planned artefact.** Every
COMPLETE row cites a file that exists on disk and that was read while preparing
this mapping.

---

END OF PRISMA 2020 CHECKLIST MAPPING


