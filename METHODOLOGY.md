# METHODOLOGY.md — Reference Manual: How This SLR Is Done

# Human-readable companion to MASTER_PROMPT_FINAL.md. For the paper's Methods
# section, thesis chapter, or onboarding a new collaborator.

## 1. OVERVIEW & DESIGN

A PRISMA-2020-compliant systematic literature review of autonomous navigation
and localization in GNSS-denied environments (UAV/UGV/USV/underwater,
2010–2025), covering multi-sensor fusion, VIO, LiDAR SLAM, RF localization,
and learning-based methods. Pipeline: raw search → dedup → two-stage
screening → quality appraisal → extraction → snowballing → synthesis.

Two design commitments distinguish this review:
(a) AI-assisted screening with mandatory human validation (agreement statistics
published), and
(b) evidence-weighted synthesis (claims tiered by study quality).

---

## 2. SEARCH (Phases 1–2)

- **Databases:** IEEE Xplore + Scopus; export date and exact query strings are
  recorded in the manuscript appendix and `CHANGELOG.md`.
- **Records:** 2,000 raw (1,000 IEEE Xplore + 1,000 Scopus). IEEE Xplore caps
  CSV export at 1,000 records — this truncation is a documented selection bias.
- **Complement:** backward/forward snowballing from Core papers (Phase 7-S);
  candidates pass through identical screening.

---

## 3. DEDUPLICATION (Phase 3)

- Exact DOI matching, then fuzzy title matching (Levenshtein ratio with a
  documented threshold). Output: `deduplicated.csv` (1,719 unique; 281
  duplicates removed in the authoritative pass).
- **Lesson recorded in audit:** dedup parameters are version-controlled; a
  silent method change between passes produced 696 vs 1,719 — resolved by
  CHANGELOG + ruling (now §2 of MASTER_PROMPT_FINAL.md).

---

## 4. SCREENING (Phase 5-R, two stages)

- **Stage 1 (title/abstract):** criteria v2 — 6 inclusion (I1–I6, ALL
  required; I2 = primary contribution must BE GNSS-denied navigation), 8
  exclusion (E1–E8, ANY suffices), STRICTNESS S1–S5, BORDERLINE B1–B5 rules.
- **AI screening output schema:** `decision`, `criteria_triggered`,
  `confidence`, `one_line_justification` — every decision auditable per paper.
- **Calibration gate:** 50-paper seed-42 pilot must land in [0.25, 0.45]
  inclusion before the full corpus runs (prevents repeating the v1 error of a
  94–98% inclusion rate).
- **Stage 2 (full-text):** I6 enforced strictly; stage-2 exclusions reported
  separately in the PRISMA flow.

**Actual results (Phase 5-R):**

| Metric | Value |
|---|---|
| Corpus screened | 1,719 |
| Calibration rate (N=50, seed=42) | 40.0% (PASS) |
| Full-corpus inclusion rate | 37.0% (636/1,719) |
| Band compliance | PASS [0.25, 0.45] |

---

## 5. HUMAN VALIDATION (Phases 5-V, 5-K)

- **Stratified random sample** (decision × database), 10%, min 100 / cap 300,
  fixed seed 42; two independent human reviewers + adjudication.
- **Statistics:** Cohen's kappa (human1 vs human2; each vs AI; AI vs
  adjudicated reference). Decision rule: κ ≥ 0.80 accept; 0.60–0.80 prompt v3
  correction on the failing stratum; < 0.60 full re-screen.
- **Reported in:** manuscript + appendix
  (`08_docs/screening_validation_report.md`).

**Actual results (Phase 5-K):**

| Comparison | Cohen's κ | Raw agreement |
|---|---:|---:|
| Human 1 vs Human 2 | 0.951 | 0.977 |
| Human 1 vs AI | 0.874 | 0.936 |
| Human 2 vs AI | 0.875 | 0.936 |
| Adjudicated vs AI | **0.874** | 0.936 |

- PABAK: 0.872 | AI sensitivity: 1.000 | AI specificity: 1.000
- **Verdict: ACCEPT** — no correction required
- Sample: 172 papers (10.0%), all 3 strata covered
- Sole ambiguity driver: I2 (primary-contribution rule) — 4 borderline
  disagreements, all adjudicated to exclude

---

## 6. QUALITY APPRAISAL (Phase 7, rubric)

0–10 score across four dimensions:

| Dimension | Max | Description |
|---|---|---|
| Experimental Rigor | 4 | Real robot, ground truth, repeatability |
| Reporting | 3 | Absolute + drift error, normalizable scale, ablations |
| Baselines | 2 | Established baseline, matched conditions |
| Reproducibility | 1 | Code/data availability |

**Tiers:** Q-high 7–10 · Q-medium 4–6 · Q-low 0–3.
Simulation-only papers cap at Q-medium. Manuscript performance claims must
state which tiers informed them. 20% double-scored; target ICC/κ ≥ 0.75.

Rubric source: `00_scope/quality_appraisal_rubric.md` (sole binding rubric;
RULINGS.md R2). `supplementary/S3_quality_scores.csv` is quarantined under
`08_docs/historical/` and never merged into `extracted_master.csv`.

---

## 7. EXTRACTION & MASTER DATASET (Phases 6–7)

**Schema fields:** platform, environment, sensors, algorithm family, estimation
architecture, metrics, datasets, `citation_tier`, plus 7 `qa_*` columns
(`qa_rigor`, `qa_reporting`, `qa_baseline`, `qa_repro`, `qa_total`, `qa_tier`,
`qa_notes`).

- Full-text retrieval logged per paper in `08_docs/fulltext_retrieval_log.csv`;
  abstract-only extractions flagged (`fulltext_available=false`) and tier-capped
  at Q-medium.
- `02_data_processed/extracted_master.csv` is the **single analysis dataset** —
  figures and manuscript consume nothing else.
- Re-extraction validation: 20 papers (10 Core + 10 random, seed 42); ≥ 90%
  per-field agreement required; results in
  `08_docs/extraction_validation_report.md`.

**Citation tier rule (RULINGS.md R4):**

| Tier | Criterion |
|---|---|
| Core | Q-high AND (high citations OR benchmark/seminal role) |
| Important | Q-medium, OR Q-high without citation signal |
| Peripheral | Q-low |

---

## 8. SNOWBALLING (Phase 7-S)

Backward and forward citations harvested from Core + Important papers. Candidates
screened at title/abstract against criteria v2; survivors pass the full pipeline
tagged `source=snowball`. Fuzzy-title dedup against existing corpus.

- Logged in `08_docs/snowball_log.csv` (per-seed counts).
- PRISMA counts updated: 2,000 raw + n_snowball → dedup → screened → included.

---

## 9. SYNTHESIS & REPORTING (Phases 8–10)

- **Core corpus** = `citation_tier` ∈ {Core, Important} AND `qa_tier` ∈
  {Q-high, Q-medium}. PDFs archived to `05_papers_fulltext/`.
- **Figures:** 300 DPI PNG → `06_analysis/output/figures/`; every number
  asserted against `extracted_master.csv` (not eyeballed).
- **Manuscript:** reports per PRISMA 2020 + PRISMA-S; mandatory sections on
  screening validation (sample, κ, correction if any) and quality appraisal
  (rubric summary, tier distribution, which tiers inform each claim).
- **Consistency sweep:** `08_docs/manuscript_consistency_check.md` maps every
  claim to its CSV source; 0 unresolved mismatches required before submission.

---

## 10. GOVERNANCE

| Rule | Summary |
|---|---|
| Single-writer | `.agent_lock` gates execution; no concurrent writes to `02_data_processed/` or `04_ai_responses/` |
| No hardcoded paths | All paths relative to repo root; scripts run from any checkout |
| Append-only CHANGELOG | Every phase, deviation, and incident recorded in `CHANGELOG.md` |
| Escalation | MASTER_PROMPT_FINAL.md §5 lists 6 hard-stop conditions |
| Quarantine | Unreviewed external outputs → `08_docs/quarantine/` pending human review |
| File hierarchy | MASTER_PROMPT_FINAL.md > screening_criteria_v2.md > quality_appraisal_rubric.md > human_validation_protocol.md > everything else |

---

## 11. REPRODUCIBILITY CHECKLIST

- [ ] Query strings + export dates archived (`00_scope/SEARCH_STRINGS.md`, `CHANGELOG.md`)
- [ ] Dedup code + thresholds committed (`phase3_dedup.py`, `dedup_log.csv`)
- [ ] Screening prompt versions versioned (`03_prompts/screening_prompts_v2/`, `SCREENING_PROMPT_CHANGELOG.md`)
- [ ] Validation sample + κ published (`08_docs/validation_sample.csv`, `08_docs/screening_validation_report.md`)
- [ ] Rubric + tier distribution published (`00_scope/quality_appraisal_rubric.md`, Phase 7 output)
- [ ] Sampling seeds recorded (seed=42 throughout; documented per phase in CHANGELOG)
- [ ] Snowball log complete (`08_docs/snowball_log.csv`)
- [ ] Consistency sweep 0 mismatches (`08_docs/manuscript_consistency_check.md`)

---

*Last updated: 2026-09-16 by SLR execution agent. Numbers reflect pipeline
state through Phase 5-K (ACCEPT). Phases 6–10 will update §§7–9 and the
reproducibility checklist as they complete.*
