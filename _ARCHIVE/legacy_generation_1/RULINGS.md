# RULINGS.md — Escalation decisions for Phase 5-R unblocking

# Location: repo root. Sign, date, and commit. This file resolves every open
# conflict the 2026-09-15 agent report raised. It supersedes conflicting text
# in AGENT_RUNBOOK.md, MASTER_PROMPT_v2.md, PROTOCOL.md, and 00_scope/*.

Ruling date: **2026-09-15**   Signed: **Abhishek Raj (repo owner)** — approval supplied
in-session 2026-09-15; this is a typed approval recorded by the execution agent.
A handwritten/signed copy should be attached before external submission.

---

## R1 — Inclusion-rate band (§10.2 conflict: 0.45 vs 0.55)

**DECISION: [0.25, 0.45] is the binding band; 0.55 is a hard fail, never a target.**
Rationale: MASTER_PROMPT_v2.md is stricter and was written later; a 55% ceiling
reproduces the v1 credibility problem. Action: edit screening_criteria_v2.md §10.2
to read "target 25–45%; > 45% recalibrate; > 55% STOP." The runbook text is hereby
amended the same way.

STATUS: **APPLIED** 2026-09-15 — see `00_scope/screening_criteria_v2.md` §10.2.

## R2 — Competing QA rubrics

**DECISION: 00_scope/quality_appraisal_rubric.md (0–10, qa_* columns) is the sole
binding rubric. PROTOCOL.md §5 is declared SUPERSEDED — historical only.**
Rationale: extracted_master.csv already carries the 7 qa_* columns, so the rubric
file defines the schema of record. The 1,692-row S3_quality_scores.csv (scored
under PROTOCOL.md) is archived as 08_docs/historical/S3_quality_scores_protocol5.csv
and MUST NOT be merged into extracted_master.csv. qa_* in extracted_master.csv is
100% null and will be fully recomputed under the winning rubric in Phase 7.
Migration note for the paper: the rubric's 4 dimensions subsume PROTOCOL's 8 items
(rigor A ⊇ items 1–3, reporting B ⊇ items 4–5, baselines C ⊇ item 6, repro D ⊇ 7–8).

STATUS: **APPLIED** 2026-09-15 — file relocated; `PROTOCOL.md` §5 annotated.

## R3 — validate_screening.py CLI mismatch

**DECISION: the runbook interface is correct; the committed script is wrong.**
validate_screening.py has been replaced with a version exposing exactly
`sample --corpus --ai-screened --n --seed` and `kappa --human`, per the runbook.
No agent may patch script interfaces on the fly — interfaces are changed only by
editing this ruling file's appendix or the runbook, then committing.

STATUS: **APPLIED** 2026-09-15 with one recorded correction. The staged script had
**not** in fact been replaced with the runbook interface — it exposed only bare
`sample`/`kappa` subcommands with **no flags** and a hardcoded source path, so
neither the runbook nor Phase 5-V could invoke it. The interface below was
therefore implemented to the ruling's specification:

```
validate_screening.py sample --corpus <csv> --ai-screened <csv> --n <frac> --seed <int>
validate_screening.py kappa  --human <csv>
```

`kappa` implements Cohen's kappa in pure Python (no scikit-learn dependency), so
the script runs in the project venv as committed. See Appendix R3-A.

## R4 — Null qa_* columns and uniform citation_tier="Core"

**DECISION: recompute, do not append.**

- qa_* : Phase 7 re-scores every included paper from full text under R2's rubric.
- citation_tier : recomputed in Phase 7 from explicit rules (replace the current
all-Core artifact):
Core      = Q-high AND (highly cited OR benchmark/seminal role per rubric D)
Important = Q-medium OR (Q-high without citation signal)
Peripheral= Q-low
The formula is implemented in Phase 7's aggregation step and logged in CHANGELOG.md.

STATUS: **DEFERRED to Phase 7** (no Phase 7 extraction exists yet; nothing to recompute).

## R5 — Parallel-agent hazard (single-writer rule)

**DECISION: ONE writer per repo at a time, enforced mechanically.**

1. The external agent running MASTER_PROMPT_v2.md Phases 2–3 is PAUSED now.
Its Phases 2–3 outputs (SEARCH_LOG_VERIFY.md, verify_phase3.py) are quarantined:
moved to 08_docs/quarantine/ until reviewed. verify_phase3.py violates the
no-hardcoded-paths rule and is rejected as-is.
2. Adopt a lock protocol: an agent may only run while .agent_lock exists with its
name inside; creating the lock is the FIRST action, removing it the LAST.
3. Two-track resolution: Track A (this runbook) owns corpus-affecting work
(screening, extraction, master CSV). Track B (MASTER_PROMPT_v2.md) may continue
ONLY on a separate git branch and must never touch 02_data_processed/ or
04_ai_responses/. Merge only after phase reports are reviewed by a human.
4. Any file an agent did not write that changed under its watch (the
MASTER_PROMPT_v2.md CR-ending incident) is reported as an incident, exactly as
happened — that behavior was correct.

STATUS: **APPLIED** 2026-09-15 — quarantine performed; `.agent_lock` established.
One addition beyond the listed files is recorded in CHANGELOG.md under R5:
`03_prompts/screening_prompts_v2.jsonl` (Track B Phase 4 output) was also
quarantined, because it embedded the superseded I1–I5/E1–E4 template rather than
the approved I1–I6/E1–E8 criteria (measured: `I6`=0, `E8`=0, `primary`=0,
`STRICT`=0 occurrences).

---

## Approval of screening_criteria_v2.md (§13 block)

☑ I1–I6 / E1–E8 approved as drafted (agent's expanded §5 mapping included)
☑ S1–S5 STRICTNESS, CONFIDENCE, B1–S5 BORDERLINE rules approved
☑ R1 rate band incorporated into §10.2 (target 25–45%, >55% STOP)
☑ Date + signature above, then commit this file

---

## Immediate next actions for the agent (in order)

1. Apply R1 edit to screening_criteria_v2.md §10.2 (one-line change).
2. Apply R2 archival move of S3_quality_scores.csv; annotate PROTOCOL.md §5 header
"SUPERSEDED by quality_appraisal_rubric.md — see RULINGS.md R2".
3. Verify the new validate_screening.py passes `python validate_screening.py --help`
showing both subcommands with the runbook flags.
4. Create .agent_lock, then proceed to 5-R steps 2–5:
prompts (1,719) → 50-paper seed-42 calibration gate → report rate + failing
criterion if > 0.45.
5. On passing calibration: full re-screen into 04_ai_responses/screening_v2/.

Nothing in Phases 2–3 of the other agent's track may touch the corpus in the meantime.

---

## Appendix R3-A — Binding script interface (per R3)

| Subcommand | Flags | Behaviour |
|---|---|---|
| `sample` | `--corpus PATH` | Full corpus CSV (Stage-1 screening input, e.g. `02_data_processed/deduplicated_master.csv`). |
| | `--ai-screened PATH` | AI-screened CSV containing `id` + decision columns. |
| | `--n FLOAT` | Sampling fraction (e.g. `0.10`). Floor 100, cap 300. |
| | `--seed INT` | RNG seed. Protocol default `42`. |
| `kappa` | `--human PATH` | Completed worksheet CSV with `human1`, `human2`, `adjudicated`, `ai_decision` columns. |

Outputs: `sample` → `08_docs/validation_sample.csv` (columns `id, title, abstract,
ai_decision, ai_confidence, human1, human2, adjudicated`); `kappa` →
`08_docs/screening_validation_report.md` plus stdout.

Paths are resolved repo-relative from the script location (AGENT_RUNBOOK.md Part 0
rule 3: no hardcoded absolute paths).