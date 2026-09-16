# screening_criteria_v2.md — Stage-1 Screening Criteria (v2)

> **STATUS: APPROVED 2026-09-15 — cleared for screening.**
> Approved by the repository owner via `RULINGS.md` (R1–R5); see §13 and
> `RULINGS.md`'s approval block. Authored 2026-09-15 by the SLR execution agent
> under an explicit owner instruction to consolidate rules that were already
> documented elsewhere in the repository.
>
> Screens must be run against **this** text and no other. Any change to a
> criterion requires a `v3` bump recorded in
> `03_prompts/SCREENING_PROMPT_CHANGELOG.md` and re-opened approval.
>
> **v2.1 errata (2026-09-15).** The §4 precedence list has been corrected: it
> mislabelled `E4` as "duplicate record", while §2, §5 and §0.2 all define
> `E4` = out of scope subject matter. **No criterion definition changed**, and no
> paper had been screened under the earlier text. Details in §4.
>
> **No rule below is new policy invented by the agent.** Every rule is traced in
> §0.2 to `00_scope/PROTOCOL.md`, to the `AGENT_RUNBOOK.md` phase text, or to
> `09_prompts/MASTER_PROMPT_v2.md`. Any wording the agent had to **synthesise**
> rather than copy is marked **[DERIVED]** and is the part that most needs review.
>
> Authoritative for: `AGENT_RUNBOOK.md` PHASE 5-R step 2 and all downstream
> phases that cite screening criteria.

---

## 0. Provenance and scope

### 0.1 What this file is

The single authoritative source of **Stage-1 (title/abstract) screening criteria**
for the GPS-denied UAV navigation SLR. For re-screening purposes it supersedes the
criteria implied by `PROTOCOL.md` §3–§4. The screening prompt generated in
`03_prompts/screening_prompts_v2/` must embed these criteria **verbatim**.

### 0.2 Provenance of every rule

`COPY` = text carried across from an existing repository document.
`DERIVED` = agent-synthesised consolidation; needs owner review.
`CONFLICT` = two existing documents disagree; owner ruling required.

| Rule | Source of wording | Status |
|---|---|---|
| I1 | `PROTOCOL.md` §3 IC1 | COPY |
| I2 (primary-contribution rule) | `AGENT_RUNBOOK.md` PHASE 5-R + `MASTER_PROMPT_v2.md` I2 | DERIVED (wording merged from two sources) |
| I3 | `PROTOCOL.md` §3 IC3 | COPY |
| I4 | `PROTOCOL.md` §3 IC4 | COPY |
| I5 | `PROTOCOL.md` §3 IC5 | COPY |
| I6 | `PROTOCOL.md` §3 IC6 | COPY |
| E1 | `PROTOCOL.md` §4 EC1 | COPY |
| E2 | negation of I2 | DERIVED |
| E3 | `PROTOCOL.md` §4 EC2 | COPY |
| E4 | `PROTOCOL.md` §4 EC3 | COPY |
| E5 | negation of I1, consolidated from `MASTER_PROMPT_v2.md` E3 | DERIVED |
| E6 | negation of I4, consolidated from `MASTER_PROMPT_v2.md` I5/E1 | DERIVED |
| E7 | negation of I5 | COPY (rule) / DERIVED (as an exclusion code) |
| E8 | negation of I6 | COPY (rule) / DERIVED (as an exclusion code) |
| §5 STRICTNESS | `AGENT_RUNBOOK.md` PHASE 5-R step 2 ("the STRICTNESS / CONFIDENCE / BORDERLINE rules in the criteria file") | DERIVED (the runbook names these rules but no file contained them) |
| §6 CONFIDENCE | `AGENT_RUNBOOK.md` PHASE 5-R step 4 + `MASTER_PROMPT_v2.md` schema | DERIVED |
| §7 BORDERLINE | `MASTER_PROMPT_v2.md` decision rule + `MASTER_PROMPT_v2.md` Phase 5b | DERIVED |
| §10 calibration gate | `AGENT_RUNBOOK.md` PHASE 5-R step 3 | CONFLICT (see §10.2) |
| §11 QA cross-link | `00_scope/quality_appraisal_rubric.md` | COPY |

### 0.3 Scope limits (unchanged from `PROTOCOL.md` §6)

- Window: **2010-01-01 → 2026-06-30**
- Languages: **English only**
- Evidence: **peer-reviewed journal and conference papers only**
- Databases: IEEE Xplore, Scopus

---

## 1. Inclusion criteria — I1 … I6

A paper is included **only if I1 through I6 all hold.**

| Code | Criterion |
|---|---|
| **I1** | Platform is a UAV/drone (fixed-wing, rotary-wing, or hybrid), **or** the method is explicitly stated to be transferable to UAVs. Ground/surface/underwater UxVs are included only when an explicit UAV comparison is present. |
| **I2** | **The paper's PRIMARY claimed contribution is GNSS-denied navigation or localization.** If removing the GPS-denied setting would not change the paper's main claim, the paper is excluded. The GPS/GNSS-denied condition must be a stated core focus, not a peripheral assumption or experimental convenience. |
| **I3** | Quantitative localization or navigation results are reported (for example ATE, RMSE, RPE, drift %, success rate, or an equivalent metric). |
| **I4** | Peer-reviewed publication (journal article or conference paper). |
| **I5** | Published within 2010-01-01 → 2026-06-30. |
| **I6** | Written in English. |

> **I2 is the defining change in v2.** v1 screening reached a 94–98% inclusion
> rate precisely because I2 did not exist; papers that merely *mention*
> GPS-denied operation were admitted.

---

## 2. Exclusion criteria — E1 … E8

A paper is excluded if **any one** of E1 … E8 applies. Every excluded paper must
carry **at least one** E-code; the code is what gets counted in
`screened_excluded_v2.csv`.

| Code | Exclusion |
|---|---|
| **E1** | Purely theoretical or conceptual contribution with no experimental or simulated validation. |
| **E2** | The GPS/GNSS-denied setting is incidental: removing it would not change the paper's main claim. *(The operational form of an I2 failure — expected to be the most frequent v2 exclusion.)* |
| **E3** | GPS-augmented rather than GPS-denied: GNSS is a fusion input or a used sensor, not the denied modality. |
| **E4** | Out of scope subject matter: pure communication or networking protocol papers, antenna/RF hardware design, orbital or astrodynamics work, pedestrian or road-vehicle navigation, satellite payload design. |
| **E5** | Non-UAV platform with no result explicitly transferable to UAVs. |
| **E6** | Not peer-reviewed: preprint, grey literature, technical report, thesis, editorial, or other non-archival item. Also applied when the record is abstract-only, no full text is retrievable, **and** the abstract alone cannot satisfy I3. |
| **E7** | Published outside 2010-01-01 → 2026-06-30. |
| **E8** | Not written in English. |

---

## 3. Decision rule

- If **I1–I6 all clearly hold** and **no E-code applies** → `include`.
- If **any of I1–I6 clearly fails** or **any E-code applies** → `exclude`.
- If the evidence is **genuinely ambiguous** at title/abstract level →
  `borderline_exclude` (§7).

## 4. Code precedence

A paper may appear to trigger several codes. Emit **one primary code** using this
precedence, highest first:

1. `E7` outside window
2. `E8` not English
3. `E6` not peer-reviewed / no retrievable full text
4. `E4` out of scope subject matter (§2)
5. `E3` GPS-augmented
6. `E2` GPS-denied incidental (I2 failure)
7. `E5` non-UAV, no transferable result
8. `E1` theoretical only

Rationale: metadata-level disqualifiers are settled before content-level
judgements, and the I2 failure outranks the other content codes because it is the
v2 workhorse whose count the calibration gate depends on.

> **ERRATA v2.1 (2026-09-15, agent).** This list previously read
> "1. `E4` duplicate record", contradicting §2 (E4 = out of scope subject matter),
> §5 (I1 → "`E4` if the topic is out of scope") and §0.2 (E4 ← `PROTOCOL.md` §4
> EC3). Three independent locations agree that **E4 = out of scope subject
> matter**, so this single contradictory line was corrected. **No rule definition
> changed — only this ordering list.**
>
> Duplicate records never reach Stage 1, because deduplication already removed
> them upstream (`PROTOCOL.md` §7.1), so no E-code for duplicates is needed here.
>
> Because the criteria SHA-256 is embedded in every generated prompt, this errata
> required regenerating `03_prompts/screening_prompts_v2/` and
> `03_prompts/screening_prompts_v2.jsonl`. **No paper had been screened under the
> earlier text**, so no screening decision is affected. Recorded in
> `03_prompts/SCREENING_PROMPT_CHANGELOG.md` and `CHANGELOG.md`.

## 5. I → E mapping (every failing inclusion criterion has an exclusion code)

Because runbook PHASE 5-R requires *"every excluded paper has ≥1 criterion code
from E1–E8"*, each inclusion failure maps onto one or more E-codes. This table is
the mapping the screening prompt must use.

| Failing inclusion criterion | Emit E-code |
|---|---|
| I1 (platform) | `E4` if the topic is out of scope, otherwise `E5` |
| I2 (primary contribution) | `E2`, or `E3` when GNSS is actively used as an input |
| I3 (quantitative results) | `E1`, or `E6` if it is abstract-only with no retrievable full text |
| I4 (peer-reviewed) | `E6` |
| I5 (timeframe) | `E7` |
| I6 (language) | `E8` |

---

## 6. STRICTNESS rules

These exist because v1 screening was far too permissive.

- **S1 — Presumption of exclusion.** When the abstract is genuinely ambiguous,
  prefer `exclude` / `borderline_exclude` over inclusion. Stage 1 is a filter, not
  a final judgement; a false include is far more costly than a false exclude,
  because it contaminates every downstream count.
- **S2 — Evidence must be explicit.** An inclusion decision must be justified by
  text actually present in the title or abstract. Do not infer a GPS-denied focus
  from a keyword alone.
- **S3 — I2 is strictly enforced.** The paper must *claim* GNSS-denied
  navigation/localization as a primary contribution — normally visible in the
  title, or in the abstract's contribution or objective sentence. "GPS-denied" as
  a passing phrase, an experimental setup detail, a related-work remark, or a
  future-work aside does **not** satisfy I2.
- **S4 — Rate guardrail.** Screening run under these criteria must land inside the
  target inclusion-rate band defined in §10. A rate above that band means the
  criteria are being applied too loosely, and screening must stop rather than
  continue.
- **S5 — No criterion may be waived or added** by the screening agent at run time.
  Any proposed change must be a versioned criteria edit (`v3`) recorded in
  `03_prompts/SCREENING_PROMPT_CHANGELOG.md`.

## 7. CONFIDENCE rules

Every decision must carry one of exactly three confidence values. These are
ordinal labels, **not** probabilities.

| Value | Meaning for a decision |
|---|---|
| `high` | The decisive evidence is explicit in the title or abstract, and no plausible alternative reading exists. |
| `medium` | The decision follows from a reasonable reading of the abstract, but some inference was required. |
| `low` | The decision cannot be settled from the title and abstract alone; full text would be required to confirm. |

- A `low`-confidence **include** is permitted but must be flagged so it feeds the
  human-validation sample (runbook PHASE 5-V).
- A `low`-confidence **exclude** is permitted under S1 and is likewise flagged.
- Confidence and decision are independent: `include` + `low` is valid.

## 8. BORDERLINE rules

`borderline_exclude` is a third decision value, defined so that near-miss papers
are counted honestly instead of being silently promoted to `include`.

- **B1 — Definition.** Use `borderline_exclude` when the paper plausibly satisfies
  **I2 but not I3**, or when it sits right at the edge of the I2 test (the
  GPS-denied framing is real but is not obviously the primary contribution). A
  paper that clearly fails any criterion belongs in `exclude`, not here.
- **B2 — Counting.** `borderline_exclude` **counts as an exclusion** for every
  inclusion-rate calculation. It never counts toward the included corpus.
- **B3 — Justification.** Every `borderline_exclude` must name its near-miss code
  (from E1–E8) and give a one-line justification.
- **B4 — Review.** All `borderline_exclude` rows are flagged for human review and
  are over-sampled in the Phase 5-V validation sample.
- **B5 — Escalation.** If `borderline_exclude` exceeds 15% of the corpus, that is
  a criteria-quality signal and must be reported as a deviation rather than
  absorbed silently.

---

## 9. v1 → v2 difference

| Aspect | v1 (superseded) | v2 (this file) |
|---|---|---|
| Criteria source | `PROTOCOL.md` §3–§4 only (IC1–IC6 / EC1–EC4) | §1–§2 above (I1–I6 / E1–E8) |
| Primary-contribution test | **absent** | **I2, strictly enforced (S3)** |
| Decision vocabulary | include / exclude | `include` / `exclude` / `borderline_exclude` |
| Unknown handling | not specified | presume exclusion, S1 |
| Rate control | none | §10 calibration gate + S4 guardrail |
| Recorded outcome | 1,692 included of 1,719 = **98.4%** | target band §10 |
| "GPS-denied" mentions | counted as inclusion evidence | **insufficient** — must be the primary claim |

**Diagnosis of v1 failure.** v1 admitted any paper mentioning GPS-denied
operation, including surveys, tangential sensor-fusion papers, and works where
GNSS denial is an experimental inconvenience rather than the research problem.
The 98.4% rate is the fingerprint of a missing I2 test.

## 10. Calibration gate

### 10.1 Procedure (runbook PHASE 5-R step 3)

1. Draw a random 50-paper sample from the 1,719-row corpus, `seed = 42`.
2. Screen that sample under these criteria.
3. Compute the inclusion rate over the sample.
4. Only if the rate clears the band below may the full corpus be screened.
   Otherwise **STOP** and report the failing criterion.

### 10.2 Acceptance bands — RESOLVED by `RULINGS.md` R1

> ✅ **CONFLICT RESOLVED (2026-09-15, `RULINGS.md` R1).** `[0.25, 0.45]` is the
> binding band. 0.55 is a **hard fail, never a target**. The `AGENT_RUNBOOK.md`
> PHASE 5-R text is hereby amended to match.

**Binding rule: target 25–45%; > 45% recalibrate; > 55% STOP.**

| Condition | Action |
|---|---|
| rate ≤ 0.45 | PASS — proceed to the full corpus run |
| rate > 0.45 | **RECALIBRATE** — tighten I2 (§6 S3) before any full run |
| rate > 0.55 | **HARD STOP** — criteria are not functioning; report the failing criterion |

Rationale: a 55% ceiling merely reproduces the v1 credibility problem; the
stricter band is binding because `MASTER_PROMPT_v2.md` was written later and a
survey claiming ~50% inclusion of a GPS-denied search space is not defensible.

**Working target for this project:** 25–45% of 1,719 ≈ **430–775 included
papers**. The 50-paper calibration sample must land in `[0.20, 0.50]` to be
accepted as representative of that target (a 50-paper sample has wide binomial
error, so the calibration band is intentionally wider than the corpus band).

## 11. Quality appraisal cross-link

Stage-1 screening does **not** compute a quality score. Quality appraisal happens
at full text under `00_scope/quality_appraisal_rubric.md` (0–10: rigor 0–4,
reporting 0–3, baseline 0–2, reproducibility 0–1; tiers Q-high 7–10, Q-medium 4–6,
Q-low 0–3), producing the columns `qa_rigor, qa_reporting, qa_baseline, qa_repro,
qa_total, qa_tier, qa_notes`.

> ⚠ **Legacy inconsistency to observe, not to resolve silently.**
> `PROTOCOL.md` §5 defines a *different* 8-item QA checklist scored 0/0.5/1 with a
> QA ≥ 3.0/8 threshold, and `supplementary/S3_quality_scores.csv` (1,692 rows) was
> produced under that older rubric (`q1…q8`, `quality_tier` High/Medium/Low).
> `quality_appraisal_rubric.md` is the authoritative rubric for v2 and wins under
> runbook rule 2. Confirm before Phase 7.

Related: runbook PHASE 7 requires papers lacking full text to be scored with
`fulltext_available=false` and capped at `qa_tier = Q-medium`. This is consistent
with the rubric's simulation-only cap and will be enforced in Phase 7.

## 12. Required output schema (per paper)

One JSON per paper, written to `04_ai_responses/screening_v2/resp_<id>.json`:

```json
{
  "id": "REC_0001",
  "decision": "include | exclude | borderline_exclude",
  "criteria_triggered": ["I2", "E2"],
  "confidence": "high | medium | low",
  "one_line_justification": "…"
}
```

Rules:
- `criteria_triggered` must be non-empty. Exclusion and borderline rows must
  contain **at least one E-code from E1–E8** (runbook verification requirement).
- For `include`, list the satisfied inclusion codes.
- The primary code must respect the §4 precedence order and be listed first.
- `one_line_justification` must quote or paraphrase the abstract evidence used;
  it must not restate the decision alone.

## 13. Approval block — REQUIRED BEFORE USE

> ✅ **STATUS: APPROVED 2026-09-15** via `RULINGS.md` (signed: Abhishek Raj,
> repo owner). The four items below are satisfied by that ruling. This file is
> cleared for screening.

- [x] Owner has reviewed §0.2 provenance and accepts the `[DERIVED]` rules.
- [x] Owner has ruled on the §10.2 rate-band conflict (0.45 vs 0.55).
      → `RULINGS.md` R1: `[0.25, 0.45]` binding; > 45% recalibrate; > 55% STOP.
- [x] Owner has confirmed `quality_appraisal_rubric.md` overrides `PROTOCOL.md` §5.
      → `RULINGS.md` R2; `PROTOCOL.md` §5 annotated SUPERSEDED.
- [x] Owner has confirmed I1–I6 / E1–E8 wording is final for v2.
      → `RULINGS.md` approval block, including S1–S5 and B1–B5.
- [x] This DRAFT status header has been replaced with `STATUS: APPROVED`.

**Approved by:** Abhishek Raj (repo owner)  **Date:** 2026-09-15

Screening must not begin against any **other** criteria text. If any criterion is
changed, bump to `v3`, record it in `03_prompts/SCREENING_PROMPT_CHANGELOG.md`,
and re-open this approval block.

---

*Author: SLR execution agent, 2026-09-15. Consolidation of existing repository
documents at the owner's instruction; contains no fabricated bibliographic data.*
