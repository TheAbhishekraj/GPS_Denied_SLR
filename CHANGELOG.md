# CHANGELOG.md

Append-only audit trail for the GPS_Denied_SLR phase pipeline.

Entry format: phase, timestamp, inputs (with row counts), outputs (with counts),
verification status, deviations. Newest entries appended at the bottom.

---

## 2026-09-15 — PHASE 5-R — STEP 1 ONLY — **BLOCKED (STOP-and-ask triggered)**

| Field | Value |
|---|---|
| Phase | 5-R (re-screening with criteria v2) |
| Timestamp | 2026-09-15 |
| Status | **BLOCKED at step 1**; steps 2–5 NOT executed |
| Inputs read | `02_data_processed/deduplicated.csv` — 1,719 rows × 62 cols |
| | `02_data_processed/deduplicated_master.csv` — 1,719 rows × 8 cols |
| | `08_docs/restart_backup_20260906_181323/deduplicated.csv` — 696 rows (stale backup, 2026-09-06) |
| Outputs written | none (no screening artifacts produced) |
| Verification | NOT RUN — phase incomplete, so the phase gate cannot be evaluated |
| Deviations | Runbook step 1 assumed `deduplicated.csv` = 696 rows; actual = 1,719 rows. STOP-and-ask executed. |

### Step 1 findings (read + report, per runbook)

Authoritative corpus resolved by owner ruling to **1,719 rows**.

| Check | Result |
|---|---|
| `02_data_processed/deduplicated.csv` | 1,719 rows × 62 cols (merged IEEE + Scopus export schema) |
| `02_data_processed/deduplicated_master.csv` | 1,719 rows × 8 cols (`id,title,abstract,authors,year,doi,venue,source`) |
| Canonical id | `REC_0001` … `REC_1719`, 1,719 unique |
| Source split | IEEE_Xplore 999 + Scopus 720 = 1,719 |
| Year range | 2010–2026 (inside the 2010-01-01 → 2026-06-30 window) |
| Null titles / abstracts | 0 / 0 (both screening inputs are complete) |
| Null DOI | 33 (in `deduplicated.csv`); 1,686 DOIs present in both files |
| **Row-order alignment** | **1,719 / 1,719 titles match at identical row index** |
| Title-set overlap | 1,718 unique + 1 duplicated title present identically in both files |
| DOI overlap | 1,686 / 1,686 — master DOIs are a complete subset of the raw file |

**Consequence:** the positional `iloc[i]` join used by the existing pipeline
scripts is safe for this corpus, and `deduplicated_master.csv` (canonical `id`)
joined positionally to `deduplicated.csv` (rich metadata) is the sanctioned
screening input.

### The 696-row file (not authoritative)

`08_docs/restart_backup_20260906_181323/deduplicated.csv` is a stale restart
backup dated 2026-09-06, using the IEEE-only export schema (`Document Title`,
`Publication Title`). 695 of its 696 titles appear in the 1,719-row corpus and
1 title is orphaned, so it is a superseded snapshot, not an alternative corpus.
The same backup folder carries `screening_prompts/…_00001–00696_*.txt` and
`screening_responses/resp_00001.json…`, i.e. the output layout that runbook
phase 5-R describes — evidence the runbook was authored against that older state.

### Blocking conflict recorded (runbook Part 0 rule 2: report, do not silently resolve)

Phase 5-R step 2 requires `00_scope/screening_criteria_v2.md` (stated to contain
inclusion I1–I6, exclusion E1–E8, plus STRICTNESS / CONFIDENCE / BORDERLINE
rules). **That file does not exist anywhere in the repository.** Three competing
criteria rule sets are currently in play:

1. Runbook Part 0 rule 2 → `00_scope/screening_criteria_v2.md` (I1–I6, E1–E8) — **missing**.
2. `00_scope/PROTOCOL.md` §3–§5 → IC1–IC6, EC1–EC4, 8-item QA checklist (QA ≥ 3.0/8.0) — exists, 6 inclusion + 4 exclusion.
3. `09_prompts/MASTER_PROMPT_v2.md` → I1–I5, E1–E4, `BORDERLINE_EXCLUDE`, confidence 0.0–1.0 — exists, differs from both.

Steps 2–5 are blocked pending an owner ruling, because runbook rule 1 forbids the
agent from authoring or "improving" criteria on its own initiative.

---

## 2026-09-15 — PHASE 5-R — STEP 2 PREREQUISITE — criteria draft authored

| Field | Value |
|---|---|
| Phase | 5-R (step 2 prerequisite only) |
| Timestamp | 2026-09-15 |
| Status | **DRAFT authored — awaiting owner approval (§13); screening still NOT started** |
| Inputs read | `00_scope/PROTOCOL.md`, `00_scope/quality_appraisal_rubric.md`, `00_scope/human_validation_protocol.md`, `AGENT_RUNBOOK.md`, `09_prompts/MASTER_PROMPT_v2.md` |
| Output written | `00_scope/screening_criteria_v2.md` — 15,741 bytes, 244 lines |
| Verification | 14 sections (§0–§13); I1–I6 and E1–E8 each exactly 1 definition row; STRICTNESS/CONFIDENCE/BORDERLINE all present; EOF newline present; 0 mojibake; CRLF consistent |
| Deviations | File did not exist, so it was agent-authored under explicit owner instruction. Marked `STATUS: DRAFT`, with per-rule provenance (`COPY` / `[DERIVED]` / `CONFLICT`) in §0.2. |
| Owner ruling applied | 1,719-row corpus is authoritative (resolves the step-1 STOP). |

### What the draft contains

- I1–I6 inclusion (I2 = primary-contribution rule, verbatim from the runbook).
- E1–E8 exclusion, with §5 mapping every failing inclusion criterion to an E-code
  so the runbook's "≥1 code from E1–E8" verification can actually be satisfied.
- §6 STRICTNESS (S1–S5), §7 CONFIDENCE (high/medium/low), §8 BORDERLINE (B1–B5) —
  the three rule groups the runbook names but that existed in no file.
- §12 output schema matching the runbook's per-paper JSON.
- §13 unsigned approval block gating all screening.

### Open items escalated (not resolved silently)

1. **Rate-band conflict (§10.2):** runbook allows ≤ 0.55, `MASTER_PROMPT_v2.md`
   caps at 0.45. Draft adopts the runbook band; either must be ruled binding.
2. **Two competing QA rubrics (§11):** `quality_appraisal_rubric.md` (0–10, 7 qa_*
   columns) vs `PROTOCOL.md` §5 (8-item, 0/0.5/1, threshold 3.0/8.0 — the rubric
   that actually produced `supplementary/S3_quality_scores.csv`, 1,692 rows).
3. **Named-file mismatch:** runbook PHASE 5-V invokes
   `validate_screening.py sample --corpus … --ai-screened … --n … --seed …`, but
   the committed `06_analysis/scripts/validate_screening.py` (7,771 B) exposes
   `sample` with no `--corpus/--ai-screened` flags and reads a fixed v1 path. No
   version of that script supports the documented CLI.
4. **Phase 7 QA columns already exist as all-null:** `extracted_master.csv`
   (1,700 rows) has `qa_rigor/reporting/baseline/repro/total/tier/notes` columns
   but every value is `NaN`, and `citation_tier` is uniformly `Core`. Phase 7 must
   recompute all 7 columns, not append them.
5. **Stale backup vs runbook:** `08_docs/restart_backup_20260906_181323/` contains
   `screening_prompts/` and `screening_responses/resp_00001.json` — the exact
   output layout runbook phase 5-R specifies — indicating the runbook was written
   against the 696-row era.
6. **Untracked `extract_master_v2.py` (2,057 B, repo root):** not created by this
   agent; contains mojibake-encoded text and would corrupt `MASTER_PROMPT_v2.md`
   if run. Left untouched; flagged for owner deletion.

---

## 2026-09-15 — INCIDENT — `MASTER_PROMPT_v2.md` encoding corruption; restored

| Field | Value |
|---|---|
| Type | File-integrity incident (external writer) |
| Timestamp | Detected and corrected 2026-09-15 (file mtime of bad write: 22:47:52) |
| Affected file | `09_prompts/MASTER_PROMPT_v2.md` |
| Committed good state | blob `70a9edb` (commit `19fcf33`), 29,584 B in blob, LF, UTF-8 BOM |
| Bad worktree state | 31,280 B, **no BOM**, **1,700 CRs = 856 CRLF + 844 lone CRs**, 0 bare LF, no trailing newline |
| Action taken | `git checkout -- 09_prompts/MASTER_PROMPT_v2.md` → restored |
| Post-restore hash | worktree `70a9edb8e07973202421d45a982174ee8bde31c1` == `HEAD:09_prompts/MASTER_PROMPT_v2.md` ✓ |
| Post-restore profile | 30,441 B, BOM present, 857 CRLF, 0 lone CR, trailing newline, 857 lines, 0 mojibake |
| Data loss | **None.** Line-by-line comparison showed all 857 lines textually identical; only line 1 (BOM) and line-ending encoding differed. |

### Why this is recorded

An external writer — not this agent — rewrote `MASTER_PROMPT_v2.md` after commit
`19fcf33`, stripping the UTF-8 BOM and emitting 844 lines terminated with a lone
CR instead of CRLF. The corruption was benign in content but would have produced
mis-diffing (`git diff` reported all 857 lines changed) and inconsistent rendering.

This matches the same external actor that produced the mojibake-laden
`extract_master_v2.py`. Enforcement note: the repo runs with `core.autocrlf=true`,
so any external editor must preserve BOM + CRLF or content-level diffs become
unreviewable.

### Also observed (same external actor, same window)

- `verify_phase2.py` (untracked, 1,157 B) appeared. It writes
  `01_data_raw/SEARCH_LOG_VERIFY.md` and asserts both raw CSVs have exactly 1,000
  rows and 8 expected columns — i.e. `MASTER_PROMPT_v2.md` PHASE 2.
  **Note:** it hardcodes absolute `E:\GPS_Denied_SLR\...` paths, violating
  `AGENT_RUNBOOK.md` Part 0 rule 3 ("NO HARDCODED PATHS"). Not reviewed or
  endorsed by this agent; left untracked.
- `extract_master_v2.py` is no longer present in the working tree (removed by the
  external actor). Nothing was committed from it.