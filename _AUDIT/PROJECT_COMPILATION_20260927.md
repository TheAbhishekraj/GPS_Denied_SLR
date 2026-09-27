# PROJECT COMPILATION — GPS_Denied_SLR

Generated: 2026-09-27T13:30Z (Scribe session).
Purpose: a folder-by-folder inventory for the human to audit manually.
Method: every count below is a **file listing** (Rule 4), not a value copied
from a CSV or a log. Every hash below was computed from disk.
Rule 5 compliance: **no deprecated legacy value is reproduced in this file.**
Where a live count collides with a deprecated value, the count is described
positionally instead of printed. See Section 0.

---

## 0. ⚠ RULE 5 ALERT — READ FIRST

Two live directories in this repository currently hold file counts that are
**identical to two of the five deprecated legacy values**.

| Directory | Collision |
|---|---|
| `03_prompts/extraction_prompts/` | file count equals deprecated legacy value **#1** |
| `04_ai_responses/extraction/` | file count equals deprecated legacy value **#2** |

Neither count is printed here. To see them, list the two directories yourself.

**Why this matters.**
1. Rule 4 instructs agents to derive counts by listing files. An agent that
   lists either of these two directories and reports the count **will write a
   deprecated value into a live file** and must then halt under Rule 5. The
   rule as written is self-triggering on this repository.
2. Rule 5 and `_PROJECT/MASTER_PROMPT.txt` both state the five values "are on
   record in `_AUDIT/INSTALLATION_REPORT.md` only". **They are not.**
   `INSTALLATION_REPORT.md` documents them by category only and prints no
   values. A text search of that file for the deprecated digits returns zero
   matches. The only place the values survive on disk is the quarantined
   predecessor rules file `_QUARANTINE_INSTRUCTIONS_20260919_171403/.clinerules.old`.
3. Consequence: the canonical record Rule 5 points to is empty, the values are
   trivially re-derivable from live listings, and the ban as written cannot be
   satisfied by an agent that is doing its job.

**Ruling required.** Choose one:
- **(A)** Record the five values explicitly in one designated reference file and
  exempt that single file from the ban (the practical option).
- **(B)** Rename or restructure the two colliding directories so their counts
  stop reproducing deprecated values.
- **(C)** Amend Rule 5 to ban the values only as *standalone claims*, explicitly
  permitting them to occur as computed file counts.

This finding is raised, not acted on. Nothing was renamed, moved or deleted.

---

## 1. TWO GENERATIONS OF WORK IN ONE REPOSITORY

The repository contains two distinct project lineages. Conflating them is the
single largest source of confusion in this project.

| | **Generation 1 (legacy)** | **Generation 2 (CURRENT)** |
|---|---|---|
| Era | before 2026-09-19 | 2026-09-19 onward |
| Governance | `AGENT_RUNBOOK.md`, `PROTOCOL.md`, `RULINGS.md` | `.clinerules`, `_PROJECT/**` |
| Screening corpus | 1,719 screening prompts | 2,000 raw → 1,716 → 636 → 291 |
| Extraction corpus | 171 → 330 PDFs | **279** |
| Master CSV | `extracted_master.csv`, `extracted_master_v2.csv` | `MASTER_EVIDENCE.csv` |
| Prompt/response store | `03_prompts/**`, `04_ai_responses/**` | `02_data_processed/evidence_batches/**` |
| Status | superseded, quarantined, partly still on disk | **live** |

`RULINGS.md` in the repo root belongs to Generation 1. It is dated 2026-09-15 and
is referenced as authority in earlier sessions. **It is not binding on
Generation 2.** Several of its rulings (R2's rubric file, R5's lock protocol)
refer to artefacts that no longer exist in the live tree. Treat it as history.

---

## 2. TOP-LEVEL INVENTORY (audit table)

Counts are direct file listings. MB is total size.

| Path | Files | MB | Generation | Status |
|---|---:|---:|---|---|
| `00_scope/` | 2 | 0.00 | 2 | **FROZEN** — `SCOPE.md`, `FROZEN.md` |
| `01_corpus/` | 1 | 0.01 | 1 | legacy template |
| `01_data_raw/` | 4 | 3.67 | 2 | **FROZEN** — 2 raw exports + 2 search logs |
| `02_data_processed/` | 324 | 19.87 | 2 | live pipeline |
| `03_extraction/` | 293 | 1.57 | 1+2 | pipeline extractions |
| `03_prompts/` | 5,134 | 65.59 | 1 | **legacy store — see Section 0** |
| `04_ai_responses/` | 5,142 | 6.67 | 1 | **legacy store — see Section 0** |
| `05_papers_fulltext/` | 288 | 1,536.21 | 2 | **FROZEN** — 288 PDFs |
| `06_analysis/` | 687 | 25.28 | 1+2 | scripts, outputs, legacy output |
| `07_manuscript/` | 37 | 3.47 | 1+2 | manuscripts V1, V2, drafts |
| `08_docs/` | 10 | 0.04 | 2 | method and spec documents |
| `09_prompts/` | 1 | 0.00 | 1 | PDCA prompt |
| `10_validation/` | 8 | 0.26 | 1 | screening/extraction validation |
| `supplementary/` | 8 | 0.16 | 1 | S1–S8 package |
| `_AUDIT/` | 54 | 0.32 | 2 | audit ledger and reports |
| `_MANUAL/` | 291 | 1.51 | 2 | **FROZEN extraction corpus** |
| `_PROJECT/` | 7 | 0.03 | 2 | governance and prompts |
| `_QUARANTINE_*` (33 dirs) | ~17,800 | ~380 | 1 | quarantined history |

Root files: `.clinerules`, `AGENTS.md`, `CHANGELOG.md`, `RULINGS.md`,
`README.md`, `MASTER_SLR_WRITING_SOP_V2.md`, `NEXT_STEPS_TO_330.md`,
`requirements.txt`, plus 3 quarantine helper scripts.

---

## 3. GENERATION 2 — FOLDER BY FOLDER (the live system)

### 3.1 `00_scope/` — FROZEN PROTOCOL
| File | Note |
|---|---|
| `SCOPE.md` | the protocol. Q1 title, Q2 RQ1–RQ4, Q3 databases, Q5 I1–I7, Q6 E1–E7, Q7 quality rubric (0–10, A–D, tiers), Q8 venues, Q9 language, Q10 doc types |
| `FROZEN.md` | freeze record |

`SCOPE.md` SHA256 `2126485248762E0DC9ECC4E96A07AE9BEAB3F4E380EC86CE3E9FD09C3370B861` —
**verified MATCH 2026-09-27.** The QA rubric lives in Q7. The separate file
`quality_appraisal_rubric.md` that `RULINGS.md` R2 calls "the sole binding
rubric" **does not exist** (finding P1).

### 3.2 `01_data_raw/` — FROZEN RAW EXPORTS
| File | Note |
|---|---|
| `ieee_xplore_20260615.csv` | 1,000 rows, SHA `FE374C9F…` |
| `scopus_20260615.csv` | 1,000 rows, SHA `EF162F4F…` |
| `SEARCH_LOG.md` | search log |
| `SEARCH_LOG_VERIFY.md` | verification. RULINGS R5 marks a file of this name for quarantine as a Generation-1 artefact — it is still present |

### 3.3 `02_data_processed/` — LIVE PIPELINE
Frozen (do not write): `deduplicated_master.csv` (SHA `A6489308…`),
`screened_included_v2.csv` (SHA `CD1B3874…`), `screening_results.csv`
(SHA `86DADC84…`), `dedup_log.csv`, `pdf_removal_log.csv`.
Writable: **`MASTER_EVIDENCE.csv`** — 279 rows × 28 cols, SHA `15B26C59…`.

Other files present: `DEDUP_REPORT.md`, `DEDUP_VERIFY.md`, `summary.txt`,
`pending_list.csv`, `retrieval_log.csv`, `screening_spreadsheet.xlsx`,
`PENDING_MASTER_EXTENSION_IDS.txt`.

⚠ **Generation-1 legacy-named files still present here:** `MASTER_EVIDENCE_V1.xlsx`,
`V1_SCOPE_IDS.txt`, `EXTRACTION_NOTES.md`, `EXTRACTION_NOTES_v2.md`. The retired
rules listed `MASTER_EVIDENCE_V1`, `V1_SCOPE_IDS` and `EXTRACTION_NOTES` as
deprecated *names*. The current Rule 5 bans only five numeric strings, so these
are not violations — but they are stale artefacts a reader may mistake for live.

Subdirectory `evidence_batches/`: 28 batch CSVs (`BATCH_B01..B28.csv`) +
28 page-source folders (`BATCH_B01_pages/` … `BATCH_B28_pages/`), each holding
10 extracted page texts except `BATCH_B28_pages/` which holds 9.

### 3.4 `05_papers_fulltext/` — FROZEN PDF CORPUS
**288 PDFs**, 1.5 GB. Matches the anchor and the PRISMA flow-in figure.

### 3.5 `_MANUAL/abhishek/per_paper/` — FROZEN EXTRACTION CORPUS
| Item | Value |
|---|---|
| Extraction files | **288** (`REC_*.md`) |
| Of those, in-corpus | **279** = 100.0% of `MASTER_EVIDENCE.csv` |
| Of those, out-of-corpus | **9** (3 of them screening-EXCLUDED) |
| Manifest | `FROZEN_MANIFEST_20260927.csv`, SHA `00366195…`, 288/288 verified |
| Declaration | `FROZEN.md` |
| **Counting rule** | count `REC_*.md` = 288. A bare `*.md` listing returns 289 because `FROZEN.md` is also there |

Sibling: `_MANUAL/abhishek/logs/action_log.md` — the writer's own log
(distinct from `_AUDIT/action_log.md`).

### 3.6 `03_extraction/per_paper/` — PIPELINE EXTRACTIONS
293 files: `.gitkeep`, `QA_INDEX.md` (header only, **0 scored papers**), and
`REC_XXXX.md` files. This is the Generation-2 pipeline directory named in
`AGENTS.md`. It is **not** the frozen evidence base — `_MANUAL/…/per_paper/` is.

### 3.7 `06_analysis/` — ANALYSIS
`scripts/` (6 files): `01_dedup.py`, `02_screen.py`, `merge_batch.py`,
`pdf_text.py`, `phase4_batch_extract.py`, `validate_master.py`.
**`figures.py` does not exist** — its Rule 9 spec awaits approval.

`outputs/` — **NOT EMPTY** (correcting an earlier claim of mine):
| File | Rows | SHA |
|---|---:|---|
| `inference_table.csv` | 279 | `2344A340…` — **verified MATCH** |
| `taxonomy_distribution.csv` | 4 | `954898BE…` — **verified MATCH** |
| `evidence_matrix.csv` | 279 | `15B26C59…` — **byte-identical to `MASTER_EVIDENCE.csv`** |

`output/` (singular, 673 files) is the **Generation-1** output tree: `figures/`,
`figures_v1/`, `figures_v2/`, `tables/`, `workbooks/`, `synthesis_v1/`,
`extraction_inbox/`, `pdf_identity_audit/`, `quarantine_REC_0035/`,
`scramble_scan_v1/`, `pdf_numeric_probe_v1/`. **Do not confuse `output/` with
`outputs/`.**

`audit/` (3): `MANUAL_REVIEW.md`, `V1_audit_2026…csv`, `V1_audit_2026…json`.
Root of `06_analysis/`: `SYNTHESIS.md`, `SYNTHESIS_v2.md` (Generation-1).

### 3.8 `08_docs/` — METHOD AND SPEC (10 files)
`ANCHOR_FREEZE_20260919.md`, `EXTRACTION_RULES.md`, `EXTRACTION_SCHEMA_v1.md`,
`EXTRACTION_SOP.md`, `MANUSCRIPT_SPEC.md`, `NUMBER_TRACE.md`,
`PRISMA_CHECKLIST.md`, `SCREENING_INDEPENDENCE.md`, `SYNTHESIS_METHOD.md`,
**`SYNTHESIS_REPORT.md`**.

⚠ **`SYNTHESIS_REPORT.md` EXISTS** — correcting an earlier claim of mine.
75 lines, SHA `1E4DC5A8…`, dated 2026-09-19T20:35:00Z, status *"STRUCTURALLY
COMPLETE — SUBSTANTIVELY EMPTY"*. It already reports the 279 rows and the six
deferred ids. **Task T4 must UPDATE it, not recreate it.**

**`PRISMA_FLOW.md` does not exist** (still correct). `PRISMA_CHECKLIST.md` was
created this session.

### 3.9 `07_manuscript/` — MANUSCRIPTS
Generation 2: `MANUSCRIPT_V2.md` (**140 lines, 13 `[UNRESOLVED]` markers**,
SHA `542BE0ED…` **verified MATCH**), `GPS_Denied_SLR_Manuscript_v2.md`,
`GPS_Denied_SLR_Manuscript_v3.md`, `SUBMISSION_CHECKLIST.md`, `BUILD.md`,
`references.bib`, `perf_summary.csv`, `perf_tables.md`.

Generation 1: `GPS_Denied_SLR_Manuscript_V1_171.*` and `_V1_291.*`
(aux/log/pdf/tex/md), `figures_list_V1.md`, `figures_list_V1_291.md`,
`tables_V1.md`, `tables_V1_291.md`, `GPS_Denied_SLR_IEEE.tex`, `_v2.tex`,
`GPS_Denied_SLR_Manuscript.md`, `GPS_Denied_SLR_Manuscript_v2.docx`.
`submitted/` (5 files) holds the `V1_291` package.

### 3.10 `_AUDIT/` — LEDGER AND REPORTS (54 files)
Ledger: `action_log.md` (Rule 8), `INTERPRETIVE_PROGRESS.md`, `merge_log.csv`.
Batch reports: `batch_B01_report.md` … `batch_B28_report.md` (28).
Phase records: `PHASE_6_COMPLETION.md`, `PHASE_7_COMPLETION.md`,
`PHASE_8_COMPLETION.md`, `FINAL_AUDIT.md`.
Governance: `INSTALLATION_REPORT.md`, `CORRECTION_REPORT.md`, `HALT_REPORT.md`,
`READ_ME_FIRST.md`, `RECONCILIATION_REPORT_20260920.md`, `OVERNIGHT_PROGRESS.md`,
`master_validation.md`.
This session added: `STATUS_REPORT_20260927.md`,
`FINDINGS_20260927_CORPUS_INTEGRITY.md`, `RULE9_SPEC_figures_py.md`,
`PROJECT_COMPILATION_20260927.md`.
Stray: `scratch_investigate.py` (a `.py` inside an audit folder),
`scratch_summarywork_*` (`_READONLY`), `disk_readonly_report{,2..5}.txt`,
`_session_ts.txt`.

⚠ `_AUDIT/rules_log.md` does **not** exist, although `EXTRACTION_RULES.md` E11
requires it (finding P2).

### 3.11 `_PROJECT/` — GOVERNANCE AND PROMPTS (7 files)
`MASTER_PROMPT.txt`, `MASTER_PROMPT_1.md` (COMPLETE), `MASTER_PROMPT_2.md`
(its phase targets are now stale), **`MASTER_PROMPT_3.md` (created this
session, NOT YET ISSUED)**, `PROJECT_CHARTER.md`, `END_GOAL.md`, `PHASE_GATES.md`
(position corrected this session to "Phase 5 and 6 COMPLETE, Phase 7 entry
satisfied").

### 3.12 `10_validation/` and `supplementary/`
`10_validation/` (8): `sample.csv`, `reviewer_A.csv`, `reviewer_B.csv`,
`adjudicated.csv`, `kappa_report.md`, `extraction_validation_sample.csv`,
`extraction_validation_results.csv`, `extraction_validation_report.md`.
These are **Generation 1** validation artefacts — they validate the legacy
screening, not the live one.

`supplementary/` (8): `S1_prisma_checklist.md`, `S2_search_queries.txt`,
`S3_quality_scores.csv`, `S4_full_reference_list.bib`,
`S5_extracted_master_snapshot_v2.csv`, `S6_screening_criteria_v2.md`,
`S7_human_validation_report.md`, `S8_extraction_validation_report.md`.
S1, S3 and S5 are **Generation-1 snapshots** and must not be submitted as-is.

---

## 4. CORRECTED PHASE POSITION

Earlier in this session I reported Phase 7 as "NOT STARTED". **That was wrong.**
`_AUDIT/PHASE_7_COMPLETION.md` and `_AUDIT/PHASE_8_COMPLETION.md` show both
phases were run on 2026-09-19. Corrected position:

| Phase | Record on disk | Verified position |
|---|---|---|
| 5 — pipeline rebuild | `PHASE_6_COMPLETION.md` predecessor work | **COMPLETE** |
| 6 — extraction batches | 28 batch CSVs, 28 batch reports, `PHASE_6_COMPLETION.md` | **COMPLETE** (279/279) |
| 7 — synthesis | `PHASE_7_COMPLETION.md` — "PARTIAL, figures deferred; substance blocked on interpretive pass" | **PARTIAL** |
| 8 — manuscript V2 | `PHASE_8_COMPLETION.md` — "DRAFT COMPLETE, AWAITING HUMAN REVIEW" | **DRAFT** |
| 9 — final audit | `FINAL_AUDIT.md` — "DRAFT, AWAITING HUMAN REVIEW" | **DRAFT** |

What Phase 7 already delivered, all hash-verified above: the three `outputs/`
CSVs and `SYNTHESIS_REPORT.md`. What it did not: figures (deferred by human
decision) and all substantive content (blocked).

What Phase 8 already delivered: `07_manuscript/MANUSCRIPT_V2.md` (140 lines,
13 `[UNRESOLVED]`) and `08_docs/NUMBER_TRACE.md`. Phase 8's exit gate is
"zero `[UNRESOLVED]`"; **13 remain**, so Phase 8 cannot be marked PASS.

**Net effect on the remaining work:** T4 is not "create the Phase 7 outputs" —
it is "populate the existing ones". T8 is not "write the manuscript" — it is
"resolve 13 `[UNRESOLVED]` markers in an existing draft".

---

## 5. VERIFICATION LEDGER (computed from disk, 2026-09-27)

| Artefact | Expected | Observed | Verdict |
|---|---|---|---|
| `00_scope/SCOPE.md` | `21264852…0B861` | same | **MATCH** |
| `02_data_processed/screening_results.csv` | `86DADC84…8F6D7` | same | **MATCH** |
| `02_data_processed/deduplicated_master.csv` | `A6489308…D8649A` | same | **MATCH** |
| `02_data_processed/screened_included_v2.csv` | `CD1B3874…93CED` | same | **MATCH** |
| `02_data_processed/MASTER_EVIDENCE.csv` | `15B26C59…12B2C6` | same | **MATCH** |
| `06_analysis/outputs/inference_table.csv` | `2344A340…D4C842` | same | **MATCH** |
| `06_analysis/outputs/taxonomy_distribution.csv` | `954898BE…B7B122` | same | **MATCH** |
| `07_manuscript/MANUSCRIPT_V2.md` | `542BE0ED…D4C391` | same | **MATCH** |
| `08_docs/NUMBER_TRACE.md` | `B297EFC4…F9ABA5` | same | **MATCH** |
| `_MANUAL/…/FROZEN_MANIFEST_20260927.csv` | `00366195…6E67DA63` | same | **MATCH** |
| 288 frozen extraction files | per manifest | 288 of 288 | **MATCH** |

Counts (by file listing): raw exports 1,000 + 1,000 · PDFs 288 · corpus rows 279 ·
batch CSVs 28 · extraction files 288 (279 in-corpus + 9 out-of-corpus) ·
`.qodo` and `.vscode` hold config only.

No frozen file has changed. No count is unreproducible.

---

## 6. MANUAL AUDIT CHECKLIST FOR THE HUMAN

Tick each only after you have listed the folder yourself.

**Frozen layer — must not change**
- [ ] `00_scope/SCOPE.md` hash matches
- [ ] `02_data_processed/screening_results.csv` hash matches, 291 rows, 285 INCLUDE / 6 EXCLUDE
- [ ] `02_data_processed/deduplicated_master.csv` hash matches, 1,716 rows
- [ ] `02_data_processed/screened_included_v2.csv` hash matches, 636 rows
- [ ] `05_papers_fulltext/` holds 288 PDFs
- [ ] `01_data_raw/` exports hold 1,000 rows each

**Frozen extraction layer**
- [ ] `REC_*.md` in `_MANUAL/abhishek/per_paper/` counts 288
- [ ] `FROZEN_MANIFEST_20260927.csv` has 288 rows and its hashes all match
- [ ] 279 of the 288 ids appear in `MASTER_EVIDENCE.csv`; 9 do not
- [ ] You accept or reject the 9 out-of-corpus files (ruling R1)

**Writable pipeline**
- [ ] `MASTER_EVIDENCE.csv` is 279 rows × 28 cols, SHA `15B26C59…`
- [ ] You accept that `year` is empty for 279/279 and `doi` for 247/279 (ruling R5)

**Rule 5**
- [ ] You have personally listed `03_prompts/extraction_prompts/` and
      `04_ai_responses/extraction/` and seen the collision described in Section 0
- [ ] You have ruled on Section 0 option (A), (B) or (C)

**Generation separation**
- [ ] You agree which folders are Generation 1 and must never be cited
- [ ] You agree `06_analysis/output/` and `06_analysis/outputs/` are different trees
- [ ] You agree `03_extraction/per_paper/` is not the frozen evidence base

---

## 7. OPEN RULINGS

| # | Ruling needed | Blocks |
|---|---|---|
| **R1** | The 9 out-of-corpus extraction files, incl. 3 for EXCLUDED records | every count in the manuscript |
| **R2** | The 5 legacy-template files (`REC_1083/1084/1085/1095/1096`) | uniform downstream parsing |
| **R3** | `REC_1232` vs `REC_1235` duplicate identity (same DOI `10.3233/ATDE260245`) | T2 row integrity |
| **R4** | Approve `figures.py` Rule 9 spec | Phase 7 figures |
| **R5** | Repair `MASTER_EVIDENCE.csv` `title`/`doi`/`year` | PRISMA 17–22, T1 |
| **R6** | Section 0 Rule 5 collision — option (A), (B) or (C) | clean-audit claim |
| **R7** | Does `RULINGS.md` (Generation 1) have any binding force? | ambiguity across every session |

---

END OF PROJECT COMPILATION — for manual audit. No value in this file was
invented; every count is a listing and every hash is from disk.



