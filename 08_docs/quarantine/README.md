# 08_docs/quarantine — quarantined artifacts (RULINGS.md R5.1)

Files here were produced by the **Track B** agent (running `MASTER_PROMPT_v2.md`)
and are quarantined pending human review. They are **not** authoritative and must
not be fed into Track A's corpus.

| File | Bytes | Why quarantined |
|---|---:|---|
| `screening_prompts_v2_phase4_SUPERSEDED_20260915.jsonl` | 21,915,478 | Phase-4 prompt dump generated from the **superseded** criteria version. Superseded by the 1,719 prompts in `03_prompts/screening_prompts_v2/`, which embed the approved I1–I6 / E1–E8 criteria from `00_scope/screening_criteria_v2.md`. |
| `screening_prompts_v2_DRIFTED_phase4.jsonl` | 7,992,148 | Prompt dump that **drifted** from the approved criteria text (content no longer matches `screening_criteria_v2.md` verbatim). |

## Handling rules

1. **Do not delete** these while the two-track merge is unresolved; keep the
   original bytes for drift comparison.
2. **Do not commit them** — excluded via `.gitignore` (`08_docs/quarantine/*.jsonl`).
   They are 29.9 MB of derived, superseded text.
3. **Do not consume them** in Track A screening, extraction, or counting.
4. Disposition requires an owner decision (see CHANGELOG.md, 2026-09-15).

## Related

- Ruling: `RULINGS.md` R5.1 (Track B paused; Phase 2–3 outputs quarantined)
- **Phase 2–3 outputs moved here per R5.1:** `SEARCH_LOG_VERIFY.md` (from
  `01_data_raw/`), `DEDUP_VERIFY.md` (from `02_data_processed/`),
  `verify_phase2.py`, `verify_phase3.py` (from repo root). The two scripts are
  rejected as-is for hardcoded absolute paths (violates AGENT_RUNBOOK rule 3 and
  the Phase 13 "fresh clone -> identical outputs" gate). Their *findings* were
  independently re-verified from the raw data before quarantine and are recorded
  in CHANGELOG.md; quarantining the artifacts does not retract those findings.
- `phase4_prompts_v2.py` is **left at repo root but must not be run**: it embeds
  the superseded I1–I5/E1–E4 criteria and produced the `SUPERSEDED` dump above.
  Track A's generator is `06_analysis/scripts/05_generate_screening_prompts_v2.py`.
- Authoritative criteria: `00_scope/screening_criteria_v2.md`