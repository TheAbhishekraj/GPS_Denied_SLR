# MASTER_PROMPT_v2.md — GPS_Denied_SLR Completion Kit (Tightened Screening + Validation)

> **Supersedes** MASTER_PROMPT.md. Use this for all work after 2026-09-15.
> Includes: screening_criteria_v2, human_validation_protocol, quality_appraisal_rubric,
> validate_screening.py.
>
> Target venue: IEEE T-RO (survey track) / IEEE Access / Robotics and Autonomous Systems
> Standard: PRISMA 2020
> Author: Abhishek Raj
> Repo: https://github.com/TheAbhishekraj/GPS_Denied_SLR

---

## 0. CRITICAL PROJECT STATE CHANGE

The previous screening run (v1 criteria) yielded 1,692 included papers — a **98.4%
inclusion rate**, far above PRISMA norms. Root cause: v1 criteria lacked a
"primary contribution" filter. Papers that merely *mention* GPS-denied as a
side-note were included.

**v2 fixes this** by adding rule **I2**: *the paper's primary claimed contribution
must be GNSS-denied navigation/localization. If removing the GPS-denied setting
would not change the paper's main claim, exclude it.*

**Target inclusion rate under v2: 25–45%** of 1,719 deduplicated papers
→ **≈430–775 included**.

**CONSEQUENCE**: Every downstream artifact that references "1,692 included"
(manuscript, LaTeX, figures, extraction CSVs) is now **provisional** and must be
regenerated after v2 screening completes. Do NOT patch numbers — regenerate
from the new screening results.

---

## 1. HOW TO USE

1. Open the phase you're on.
2. Copy the block between `>>> BEGIN PROMPT` and `<<< END PROMPT`.
3. Paste into your AI agent.
4. The agent MUST reply with a fully ticked CHECKLIST.
5. Any unticked box → `INCOMPLETE: <reason>` → STOP → fix → rerun.
6. Run the MANUAL VERIFICATION block yourself.
7. Commit → next phase.

Do NOT skip the **calibration gate** (Phase 5) or the **human validation gate**
(Phase 5b). They are blocking.

---

## 2. GLOBAL RULES (inject into every phase prompt)

```
GLOBAL RULES — read before answering any phase prompt.

1.  NEVER fabricate data. Unknown -> "UNKNOWN" or "PENDING".
2.  NEVER invent DOIs, authors, years, venues, registration IDs.
3.  ALWAYS print the CHECKLIST at the end, ticking [x] or [ ].
4.  If any box is [ ], print "INCOMPLETE: <reason>" and stop.
5.  ALWAYS report file path + byte size for every artifact written.
6.  ALWAYS cross-check against CANONICAL NUMBERS (§3). Mismatch = STOP.
7.  Every numeric claim must trace to a row in extracted_master.csv or a
    source table CSV. Cite the source path.
8.  Prefer reproducible, boring methods over clever, opaque ones.
9.  When blocked, ask exactly one clarifying question, then wait.
10. Commit after every completed phase: `git commit -m "phase-N: <summary>"`.
11. The agent MUST NOT proceed past Phase 5 or Phase 5b until the gate passes.
12. All inclusion decisions under v2 must cite the specific rule
    (I1..I5, E1..E4) that drove the decision.
```

---

## 3. CANONICAL NUMBERS — v2 (post-rescreen)

Some values are **fixed** (upstream of screening); some are **provisional**
(dependent on v2 screening outcomes).

### Fixed (upstream, do not change)

| Symbol | Value | Meaning |
|---|---|---|
| RAW | 2,000 | Initial records (IEEE 1,000 + Scopus 1,000) |
| DEDUP | 1,719 | After dedup (281 removed, 14.1%) |

### Provisional (fill after v2 screening)

| Symbol | Target / Rule | Meaning |
|---|---|---|
| INCLUSION_RATE | **0.25–0.45** | Required v2 inclusion rate |
| INCLUDED_V2 | `[430–775]` | Count after v2 screening |
| EXCLUDED_V2 | `[944–1,289]` | Count after v2 screening |
| CALIBRATION_N | 50 | Papers used for calibration gate |
| CALIBRATION_RATE | **0.20–0.50** | Acceptable calibration inclusion rate |
| HUMAN_SAMPLE_N | `[100–300]` | Stratified 10% validation sample |
| KAPPA_ACCEPT | **≥0.80** | Accept AI screening as-is |
| KAPPA_CORRECT | **0.60–0.80** | Apply error-model correction |
| KAPPA_REJECT | **<0.60** | Recalibrate and re-screen |
| EXTRACTED_V2 | `=INCLUDED_V2 + double_extractions` | Extracted rows |
| IMU_PCT_V2 | recomputed | % of extracted rows with IMU |
| EW_COUNT_V2 | recomputed | adversarial/EW environment count |
| MA_RATIO_V2 | recomputed | multi-agent real:sim ratio |

Do NOT hardcode INCLUDED_V2 = 1,692. That value is **obsolete**.

---

## PHASE 0 — Skeleton & Environment

>>> BEGIN PROMPT
You are completing Phase 0 (Skeleton & Environment) of a PRISMA 2020 SLR.

TASK:
1. Create folders under E:\GPS_Denied_SLR\:
   00_scope/ 01_data_raw/ 02_data_processed/ 03_prompts/ 04_ai_responses/
   05_papers_fulltext/ 06_analysis/output/figures_v2/ 06_analysis/output/tables/
   06_analysis/scripts/ 07_manuscript/ 08_docs/ 09_prompts/ supplementary/
   10_validation/
2. Write requirements.txt: pandas, numpy, matplotlib, seaborn, scikit-learn,
   python-Levenshtein, pyyaml, tqdm, python-dotenv, scikit-learn (for kappa).
3. Write .gitignore for: .venv/, __pycache__/, *.pyc, .DS_Store,
   05_papers_fulltext/*.pdf, .env.
4. Write 08_docs/FOLDER_GUIDE.md — one line per folder.

CHECKLIST:
[ ] 14 folders exist (incl. 10_validation/)
[ ] requirements.txt present with 10 packages
[ ] .gitignore covers .venv, pycache, PDFs, .env
[ ] FOLDER_GUIDE.md present
[ ] No placeholder data files created
<<< END PROMPT

**MANUAL VERIFICATION**
```powershell
Get-ChildItem "E:\GPS_Denied_SLR" -Directory | Select-Object Name
```

---

## PHASE 1 — Scope & Protocol (v2 criteria)

>>> BEGIN PROMPT
You are completing Phase 1 (Scope & Protocol, v2) of the SLR.

TASK: Write to 00_scope/:
1. PROTOCOL.md — RQ1-RQ4, PICOC, quality checklist (8-item),
   AND a pointer to screening_criteria_v2.md.
2. SEARCH_STRINGS.md — exact IEEE Xplore + Scopus queries, run date, counts.
3. REGISTRATION.md — OSF/Prospero ID or "UNREGISTERED" + justification.

ADDITIONALLY: Verify that screening_criteria_v2.md exists in 00_scope/ or
07_manuscript/. If missing, copy the user-provided version verbatim and
note the source. The key addition over v1 is:

  I2 (primary-contribution rule):
  "The paper's primary claimed contribution must be GNSS-denied
   navigation or localization. If removing the GPS-denied setting would
   not change the paper's main claim, the paper is EXCLUDED."

CONSTRAINTS:
- Do NOT fabricate a registration ID.
- Timeframe: 2010-01-01 to 2026-06-30. English only. Peer-reviewed only.

CHECKLIST:
[ ] PROTOCOL.md has RQ1-RQ4 + PICOC + 8-item quality checklist
[ ] SEARCH_STRINGS.md has both exact queries
[ ] REGISTRATION.md status explicit
[ ] screening_criteria_v2.md present with I2 rule verbatim
[ ] v1 vs v2 diff documented
[ ] Timeframe + language + peer-review stated
<<< END PROMPT

---

## PHASE 2 — Database Search (verify only)

>>> BEGIN PROMPT
You are completing Phase 2 (Database Search — verification only).

INPUTS: 01_data_raw/ieee_xplore_raw.csv, 01_data_raw/scopus_raw.csv
The search is already complete (2,000 records). You are VERIFYING only.

TASK:
1. Confirm both CSVs exist with 8 columns:
   id,title,abstract,authors,year,doi,venue,source.
2. Confirm 1,000 rows each (or state actual count).
3. Confirm zero empty titles.
4. Write 01_data_raw/SEARCH_LOG_VERIFY.md with date of verification.

CONSTRAINTS:
- Do NOT re-run searches. Do NOT invent missing rows.

CHECKLIST:
[ ] ieee_xplore_raw.csv row count reported
[ ] scopus_raw.csv row count reported
[ ] Both have 8 columns
[ ] Zero empty titles
[ ] SEARCH_LOG_VERIFY.md written with date + counts
<<< END PROMPT

---

## PHASE 3 — Deduplication (verify only)

>>> BEGIN PROMPT
You are completing Phase 3 (Deduplication — verification only).

INPUTS: 02_data_processed/deduplicated_master.csv, dedup_log.csv
The dedup is already complete (1,719 unique, 281 removed).

TASK:
1. Confirm deduplicated_master.csv = 1,719 rows.
2. Confirm dedup_log.csv = 281 rows, reasons only "DOI match" or "Title match".
3. Write 02_data_processed/DEDUP_VERIFY.md with counts + method recap.

CHECKLIST:
[ ] deduplicated_master.csv = 1,719 rows
[ ] dedup_log.csv = 281 rows
[ ] Reasons limited to DOI match / Title match
[ ] DEDUP_VERIFY.md written
<<< END PROMPT

---

## PHASE 4 — Screening Prompt Generation (v2)

>>> BEGIN PROMPT
You are completing Phase 4 (Screening Prompt Generation, v2).

INPUT: 02_data_processed/deduplicated_master.csv (1,719 rows)
OUTPUT: 03_prompts/screening_prompts_v2.jsonl (1,719 lines)

Each line: {"paper_id","title","abstract","prompt","schema","criteria_version":"v2"}.

Prompt template (do not alter):
"You are screening a paper for a PRISMA SLR on GPS-denied UAV navigation.
Apply criteria v2. Decide INCLUDE or EXCLUDE.

INCLUSION (ALL must hold):
 I1. UAV/drone platform (fixed-wing, rotorcraft, hybrid) OR a method
     explicitly transferable to UAVs.
 I2. The paper's PRIMARY claimed contribution is GNSS-denied navigation
     or localization. If removing the GPS-denied setting would not change
     the paper's main claim, EXCLUDE.
 I3. Quantitative localization results (ATE, RMSE, RPE, success rate,
     or equivalent) are reported.
 I4. English, peer-reviewed, 2010-01-01 to 2026-06-30.
 I5. Full text is available.

EXCLUSION (ANY triggers EXCLUDE):
 E1. Theoretical only — no experimental or simulated results.
 E2. GPS-augmented rather than GPS-denied (GPS is a fusion input, not
     the denied modality).
 E3. Non-UAV platform with no transferable result.
 E4. Quality score <= 2/8 (deferred to full-text stage).

Decision rule:
- If I1..I5 all clearly hold AND E1..E3 do not apply -> INCLUDE.
- If any of I1..I5 clearly fails OR E1..E3 applies -> EXCLUDE.
- If ambiguous -> BORDERLINE_EXCLUDE (counts as EXCLUDE for rate
  calculation; flagged for human review).

Return JSON: {decision: INCLUDE|EXCLUDE|BORDERLINE_EXCLUDE,
              rule_triggered: I1..I5|E1..E4,
              confidence: 0.0-1.0,
              one_line_justification: string}"

CONSTRAINTS:
- v2 criteria text must match 00_scope/screening_criteria_v2.md verbatim.
- BORDERLINE_EXCLUDE must be a valid decision value.

CHECKLIST:
[ ] screening_prompts_v2.jsonl = 1,719 lines
[ ] Every line has 6 keys incl. criteria_version="v2"
[ ] I1-I5 + E1-E4 all present in template
[ ] BORDERLINE_EXCLUDE included as decision value
[ ] Confidence field 0.0-1.0
[ ] No paper skipped
<<< END PROMPT

**MANUAL VERIFICATION**
```powershell
(Get-Content "E:\GPS_Denied_SLR\03_prompts\screening_prompts_v2.jsonl" | Measure-Object -Line).Lines
```

---

## PHASE 5 — Screening v2 + CALIBRATION GATE

**This phase has a HARD GATE. Do not proceed past it without passing calibration.**

>>> BEGIN PROMPT
You are completing Phase 5 (Screening v2 with Calibration Gate).

INPUT: 03_prompts/screening_prompts_v2.jsonl (1,719 lines)
OUTPUTS:
- 04_ai_responses/screening_calibration.jsonl  (50 lines, 50-paper subset)
- 04_ai_responses/screening_results_v2.jsonl   (1,719 lines, full run)
- 02_data_processed/screening_summary_v2.csv
- 02_data_processed/screening_audit_v2.csv
- 08_docs/CALIBRATION_REPORT.md

PROCEDURE:
STEP 1 (CALIBRATION):
1. Select 50 random papers with seed=42 from the 1,719.
2. Run the v2 screening prompt on these 50.
3. Compute inclusion rate on the 50.
4. If rate is within [0.20, 0.50] -> PROCEED to Step 2.
   If rate > 0.50 -> STOP. The v2 criteria are not tight enough.
      Report: "CALIBRATION FAILED: rate=X. Tighten I2 before proceeding."
   If rate < 0.20 -> STOP. Criteria may be too strict.
      Report: "CALIBRATION FAILED: rate=X. Loosen I2 before proceeding."

STEP 2 (FULL RUN):
1. Run v2 screening on all 1,719 papers.
2. Write screening_results_v2.jsonl (1,719 lines).
3. Write screening_summary_v2.csv (counts per decision + per rule_triggered).
4. Write screening_audit_v2.csv (all EXCLUDE + BORDERLINE_EXCLUDE rows).

POST-RUN AUDIT (print actual vs target):
  A. INCLUDE count           — must be in [430, 775]
  B. Inclusion rate          — must be in [0.25, 0.45]
  C. BORDERLINE_EXCLUDE count — report actual (flag if > 15% of total)
  D. Rule histogram          — which I/E rules fired most often
  E. Low-confidence (<0.6) rows flagged in `needs_human` column

CONSTRAINTS:
- Do NOT force INCLUDE rate into range by fudging decisions.
- If calibration fails, STOP and report. Do NOT proceed.
- Every decision must cite one rule (I1-I5 or E1-E4).

CHECKLIST:
[ ] Calibration run on 50 papers completed
[ ] Calibration inclusion rate in [0.20, 0.50]
[ ] Full run on 1,719 completed
[ ] screening_results_v2.jsonl = 1,719 lines
[ ] INCLUDE count in [430, 775]
[ ] Inclusion rate in [0.25, 0.45]
[ ] BORDERLINE_EXCLUDE count reported
[ ] Rule histogram generated
[ ] Low-confidence rows flagged
[ ] CALIBRATION_REPORT.md written with rate + verdict
<<< END PROMPT

**MANUAL VERIFICATION**
```powershell
$r = Import-Csv "E:\GPS_Denied_SLR\02_data_processed\screening_summary_v2.csv"
$r
# EXPECT: INCLUDE in [430,775], rate in [0.25,0.45]
```

**GATE**: If calibration fails, STOP. Do not proceed to Phase 5b.

---

## PHASE 5b — Human Validation (BLOCKING)

>>> BEGIN PROMPT
You are completing Phase 5b (Human Validation of AI Screening).

INPUTS: 04_ai_responses/screening_results_v2.jsonl, human_validation_protocol.md
OUTPUTS in 10_validation/:
- sample.csv                  (stratified sample, 100-300 papers)
- reviewer_A.csv              (reviewer A decisions)
- reviewer_B.csv              (reviewer B decisions)
- adjudicated.csv             (final ground-truth decisions)
- kappa_report.md             (Cohen's kappa + verdict)

PROCEDURE:
1. Draw stratified sample:
   - Strata: decision (INCLUDE, EXCLUDE, BORDERLINE_EXCLUDE) x year-bucket
   - Target: 10% of 1,719 ≈ 172 papers (floor 100, cap 300)
   - Fixed seed = 42
   - Write sample.csv with columns: paper_id, stratum, decision_ai, title, abstract
2. Instruct 2 human reviewers (this is a MANUAL step — you cannot do it).
   Provide reviewer_A.csv and reviewer_B.csv as blank templates with the
   same paper_id column.
   PAUSE here and tell the user: "Populate reviewer_A.csv and reviewer_B.csv
   with INCLUDE/EXCLUDE/BORDERLINE_EXCLUDE, then reply CONTINUE."
3. After reviewer files populated:
   a. Compute AI-vs-human kappa (AI vs adjudicated)
   b. Compute human-vs-human kappa (A vs B)
   c. Compute adjudication (disagreements resolved by a 3rd reviewer)
4. Apply decision rule:
   - kappa >= 0.80 -> "ACCEPT: use AI screening as-is"
   - 0.60 <= kappa < 0.80 -> "CORRECT: apply error-model correction"
     -> estimate per-stratum error rates, apply to full corpus
   - kappa < 0.60 -> "REJECT: recalibrate criteria, re-run Phase 5"
5. Write kappa_report.md with:
   - PRISMA-style validation table
   - Cohen's kappa (AI vs adjudicated) and (A vs B)
   - Verdict
   - If CORRECT verdict: the corrected inclusion count

CONSTRAINTS:
- Do NOT fabricate reviewer decisions.
- Do NOT proceed if verdict is REJECT — escalate to user.

CHECKLIST:
[ ] sample.csv written (100-300 rows, seed=42)
[ ] reviewer_A.csv template written
[ ] reviewer_B.csv template written
[ ] AI-vs-adjudicated kappa computed
[ ] Human-vs-human kappa computed
[ ] Verdict stated (ACCEPT/CORRECT/REJECT)
[ ] kappa_report.md includes PRISMA validation table
[ ] If CORRECT: corrected inclusion count reported
[ ] If REJECT: escalation message printed
<<< END PROMPT

**MANUAL STEP** — You must fill reviewer_A.csv and reviewer_B.csv.
Then reply CONTINUE.

---

## PHASE 6 — Extraction Prompt Generation (v2)

>>> BEGIN PROMPT
You are completing Phase 6 (Extraction Prompt Generation, v2).

INPUT: 04_ai_responses/screening_results_v2.jsonl (INCLUDE rows only)
OUTPUT: 03_prompts/extraction_prompts_v2.jsonl

MANDATORY SCHEMA FIELDS (20 — 17 v1 fields + 3 v2 QA placeholders):
paper_id, title, year, venue, doi,
platform_type, sensor_list, primary_method, method_category,
environment, experiment_type, metrics_reported,
ate_rmse_m, real_or_sim, application_domain,
multi_agent (bool), notes,
qa_total (int 0-10), qa_tier (Q-high|Q-medium|Q-low), qa_components (dict)

Enums:
- platform_type in {fixed_wing, rotor, hybrid, general, unknown}
- experiment_type in {real, sim, both, unknown}
- real_or_sim in {real, sim, both, unknown}
- multi_agent in {true, false, unknown}
- qa_tier in {Q-high, Q-medium, Q-low}

qa_components keys (per quality_appraisal_rubric.md):
  experimental_rigor (0-4), reporting_completeness (0-2),
  baseline_fairness (0-2), reproducibility (0-2). Sum = qa_total.

QA tiers:
- Q-high: qa_total >= 8
- Q-medium: qa_total 5-7
- Q-low: qa_total <= 4
- Simulation-only papers are CAPPED at Q-medium regardless of score.

CHECKLIST:
[ ] Line count = INCLUDED_V2 (from Phase 5)
[ ] All 20 fields per line
[ ] Enums constrained
[ ] QA rubric components documented
[ ] Simulation-only cap rule present
[ ] Prompt says "write UNKNOWN, never guess"
<<< END PROMPT

---

## PHASE 7 — Extraction Execution (v2) + QA Rubric Application

>>> BEGIN PROMPT
You are completing Phase 7 (Extraction Execution + QA Rubric, v2).

INPUT: 03_prompts/extraction_prompts_v2.jsonl
OUTPUTS:
- 02_data_processed/extracted_master_v2.csv
- 02_data_processed/EXTRACTION_NOTES_v2.md
- 02_data_processed/qa_distribution.csv

TASK:
1. Run extraction on every INCLUDED_V2 paper.
2. Apply quality_appraisal_rubric.md scoring per paper:
   - experimental_rigor (0-4): real robot +1, ground truth +1, repeatability +1,
     field environment +1
   - reporting_completeness (0-2): metrics defined +1, statistics reported +1
   - baseline_fairness (0-2): baseline given +1, equal conditions +1
   - reproducibility (0-2): code/data released +1, parameter disclosure +1
   - qa_total = sum (0-10)
   - qa_tier from rubric (simulation-only cap = Q-medium)
3. Write extracted_master_v2.csv with all 20 fields.
4. Write qa_distribution.csv: counts per tier + per component mean.
5. Document double-extractions in EXTRACTION_NOTES_v2.md.

POST-WRITE AUDIT (print actual):
  A. Row count = INCLUDED_V2 + double_extractions
  B. IMU coverage (recomputed — do NOT hardcode 78%)
  C. adversarial/EW count (recomputed)
  D. Multi-agent real:sim ratio (recomputed)
  E. Method category count (recomputed)
  F. QA distribution: n(Q-high) / n(Q-medium) / n(Q-low)

CONSTRAINTS:
- Do NOT reuse v1 numbers (1,332 / 78% / 495 / 1.3:1). Recomputed from v2 corpus.
- Every QA score must cite the paper evidence in the `notes` field.

CHECKLIST:
[ ] extracted_master_v2.csv row count = INCLUDED_V2 + doubles
[ ] All 20 fields present
[ ] qa_total in 0-10 for every row
[ ] qa_tier assigned for every row
[ ] Simulation-only cap enforced
[ ] qa_distribution.csv written
[ ] IMU/EW/MA recomputed (not hardcoded)
[ ] Double-extractions documented
<<< END PROMPT

**MANUAL VERIFICATION**
```powershell
$r = Import-Csv "E:\GPS_Denied_SLR\02_data_processed\extracted_master_v2.csv"
$r.Count
$r | Group-Object qa_tier | Select-Object Name, Count
```

---

## PHASE 7b — Extraction Validation Gate (20 papers, ≥90% agreement)

>>> BEGIN PROMPT
You are completing Phase 7b (Extraction Validation).

INPUTS: extracted_master_v2.csv, quality_appraisal_rubric.md
OUTPUTS in 10_validation/:
- extraction_validation_sample.csv  (20 random papers, seed=43)
- extraction_validation_results.csv (human-reviewed 20 papers)
- extraction_validation_report.md

PROCEDURE:
1. Draw 20 random papers (seed=43) from extracted_master_v2.csv.
2. Emit a template CSV with all 20 fields left blank for human review.
3. PAUSE. Ask user to fill extraction_validation_results.csv.
4. On CONTINUE: compute field-level agreement (AI vs human) across all fields.
5. Verdict:
   - Agreement >= 0.90 -> PASS
   - Agreement < 0.90  -> FAIL; identify fields with lowest agreement;
     re-run extraction with an amended prompt targeting those fields.
6. Write extraction_validation_report.md.

CHECKLIST:
[ ] Sample of 20 papers drawn (seed=43)
[ ] Blank template written
[ ] Field-level agreement computed
[ ] Verdict PASS/FAIL stated
[ ] If FAIL: failing fields identified + remediation plan
<<< END PROMPT

**MANUAL STEP** — Fill extraction_validation_results.csv.
Reply CONTINUE.

---

## PHASE 8 — PRISMA & Figures (regenerate from v2)

>>> BEGIN PROMPT
You are completing Phase 8 (PRISMA & Figures, v2).

INPUT: 02_data_processed/extracted_master_v2.csv
OUTPUTS in 06_analysis/output/figures_v2/ (9 PNGs, 300 DPI, >=2000 px wide):
  fig01_publication_trends.png
  fig02_platform_distribution.png
  fig03_environment_distribution.png
  fig04_method_evolution.png
  fig05_sensor_frequency.png
  fig06_application_domains.png
  fig07_prisma_flow.png
  fig08_method_environment_heatmap.png
  fig09_research_maturity_radar.png

ALSO: source CSV per figure in 06_analysis/output/tables/.
ALSO: qa-tier overlay on fig09 (radar) and fig03 (env distribution).

fig07 PRISMA numbers must reflect v2:
  2,000 -> 1,719 -> INCLUDED_V2 (excluded = 1,719 - INCLUDED_V2)
  -> EXTRACTED_V2

CONSTRAINTS:
- All numbers recomputed from extracted_master_v2.csv.
- Do NOT reuse 1,692.
- Colorblind-safe palette (Okabe-Ito).

CHECKLIST:
[ ] 9 PNGs present, all >= 300 DPI
[ ] PRISMA reflects INCLUDED_V2
[ ] Every figure has a source CSV
[ ] QA-tier overlay present on fig03 and fig09
[ ] Colorblind-safe palette confirmed
<<< END PROMPT

---

## PHASE 9 — Synthesis & Taxonomy (v2)

>>> BEGIN PROMPT
You are completing Phase 9 (Synthesis, v2).

INPUT: extracted_master_v2.csv
OUTPUTS in 06_analysis/output/tables/:
- taxonomy_matrix_v2.csv
- env_method_coverage_v2.csv
- sim_vs_real_v2.csv
- qa_by_method.csv
PLUS 06_analysis/SYNTHESIS_v2.md

SYNTHESIS_v2.md must state (with numerator + denominator):
- IMU universality — N_IMU / N_total = PCT
- Largest environment — N_env / N_total = PCT
- Deployment gap — multi-agent real:sim = R:1
- QA distribution — n(Q-high)/n(Q-medium)/n(Q-low)
- Every claim cites the CSV that produced it.

CONSTRAINTS:
- No number without source CSV path.
- Do NOT restate old values (1,332, 495, 1.3:1) — recompute.

CHECKLIST:
[ ] 4 CSVs present
[ ] SYNTHESIS_v2.md states all findings with num/denom
[ ] Zero claims without source
[ ] QA distribution reported
<<< END PROMPT

---

## PHASE 10 — Manuscript (v2)

>>> BEGIN PROMPT
You are completing Phase 10 (Manuscript, v2).

INPUTS: all v2 CSVs, figures_v2, references.bib
OUTPUTS:
- 07_manuscript/GPS_Denied_SLR_Manuscript_v3.md
- 07_manuscript/references.bib (updated)

STRUCTURE (mandatory):
  Abstract (<=250 words) + Keywords
  §1 Introduction
  §2 Methodology (PRISMA 2020, v2 criteria, human validation)
  §3 Taxonomy (with QA tiers)
  §4 Synthesis (recomputed findings)
  §5 Challenges
  §6 Maturity (with QA dimension)
  §7 Conclusion
  References

HARD RULES:
- §2 must describe the v2 criteria (I2 rule) and human validation protocol.
- Every number traces to a v2 CSV. No v1 numbers anywhere.
- Performance tables must state which QA tiers informed each claim
  (per quality_appraisal_rubric.md).
- Footer canonical numbers updated to v2 values.
- Zero orphan citations.

CHECKLIST:
[ ] All 7 numbered sections present
[ ] §2 describes v2 I2 rule + validation
[ ] Footer canonical numbers = v2
[ ] Every numeric claim has source
[ ] QA tiers cited in performance tables
[ ] Zero orphan citations
[ ] Abstract <= 250 words
<<< END PROMPT

---

## PHASE 11 — LaTeX Submission Package (v2)

>>> BEGIN PROMPT
You are completing Phase 11 (LaTeX Package, v2).

OUTPUTS in 07_manuscript/:
- GPS_Denied_SLR_IEEE_v2.tex  (\documentclass[journal]{IEEEtran})
- references.bib
- perf_tables.md  (>=3 tables, each with QA tier column)
- BUILD.md

POST-BUILD AUDIT:
  pdflatex -> bibtex -> pdflatex x2
  grep log for "undefined" -> must be 0
  grep log for "Overfull \hbox" -> must be < 5

CHECKLIST:
[ ] .tex uses IEEEtran journal class
[ ] Zero undefined citations
[ ] Zero undefined references
[ ] perf_tables.md has >=3 tables with QA tiers
[ ] BUILD.md lists exact commands
[ ] All 9 figures referenced
<<< END PROMPT

---

## PHASE 12 — Supplementary Materials (v2)

>>> BEGIN PROMPT
You are completing Phase 12 (Supplementary, v2).

OUTPUTS in supplementary/:
- S1_prisma_checklist.md
- S2_search_queries.txt
- S3_quality_scores.csv  (qa_* columns per included paper)
- S4_full_reference_list.bib
- S5_extracted_master_snapshot_v2.csv
- S6_screening_criteria_v2.md  (verbatim copy)
- S7_human_validation_report.md (from Phase 5b)
- S8_extraction_validation_report.md (from Phase 7b)

CHECKLIST:
[ ] S1-S8 all present
[ ] S3 = INCLUDED_V2 rows
[ ] S6 verbatim
[ ] S7 includes kappa + verdict
[ ] S8 includes field agreement
<<< END PROMPT

---

## PHASE 13 — Submission Prep (v2)

>>> BEGIN PROMPT
You are completing Phase 13 (Submission Prep, v2).

OUTPUTS in 08_docs/:
- SUBMISSION_CHECKLIST.md
- COVER_LETTER.md
- ARXIV_METADATA.md

GATES:
1. Plagiarism <15%
2. Reference check: 0 dangling
3. Numeric check: v2 canonical numbers match everywhere
4. Figure check: 9 figures @300 DPI
5. Reproducibility: fresh clone -> identical outputs
6. Language: Grammarly pass
7. PRISMA: 27 items
8. Format: venue page limit
9. Screening validation: kappa >= 0.60 (from Phase 5b)
10. Extraction validation: field agreement >= 0.90 (from Phase 7b)

CHECKLIST:
[ ] 10 gates listed with status
[ ] Cover letter <=400 words
[ ] arXiv categories filled
[ ] Internal gates verified
[ ] External gates PENDING flagged
<<< END PROMPT

---

## APPENDIX A — validate_screening.py

Save as `06_analysis/scripts/validate_screening.py`. Two commands:

```python
import argparse, csv, random, pathlib
from collections import Counter
from sklearn.metrics import cohen_kappa_score

ROOT = pathlib.Path(__file__).resolve().parents[2]

def cmd_sample(args):
    src = ROOT / "04_ai_responses/screening_results_v2.jsonl"
    rows = [eval(l) for l in src.read_text().splitlines() if l.strip()]
    random.seed(42)
    # Stratified: 10% per decision, floor 100, cap 300
    by_dec = {}
    for r in rows:
        by_dec.setdefault(r["decision"], []).append(r)
    n_total = len(rows)
    n_target = min(300, max(100, int(0.10 * n_total)))
    sample = []
    for dec, group in by_dec.items():
        k = max(1, int(round(n_target * len(group) / n_total)))
        sample += random.sample(group, min(k, len(group)))
    out = ROOT / "10_validation/sample.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["paper_id","stratum","decision_ai","title","abstract"])
        w.writeheader()
        for r in sample:
            w.writerow({"paper_id":r["paper_id"],"stratum":r["decision"],
                        "decision_ai":r["decision"],"title":r.get("title",""),
                        "abstract":r.get("abstract","")})
    print(f"Wrote {out} with {len(sample)} rows")
    inc = sum(1 for r in rows if r["decision"]=="INCLUDE")
    rate = inc / n_total
    print(f"Full corpus inclusion rate: {rate:.3f}")
    if rate > 0.55:
        print("WARNING: inclusion rate > 0.55 — criteria may be too loose.")

def cmd_kappa(args):
    a = {r["paper_id"]:r["decision"] for r in csv.DictReader(open(ROOT/"10_validation/reviewer_A.csv"))}
    b = {r["paper_id"]:r["decision"] for r in csv.DictReader(open(ROOT/"10_validation/reviewer_B.csv"))}
    adj = {r["paper_id"]:r["decision"] for r in csv.DictReader(open(ROOT/"10_validation/adjudicated.csv"))}
    ai = {r["paper_id"]:r["decision_ai"] for r in csv.DictReader(open(ROOT/"10_validation/sample.csv"))}
    ids = sorted(set(a) & set(b) & set(adj) & set(ai))
    k_hh = cohen_kappa_score([a[i] for i in ids], [b[i] for i in ids])
    k_ai = cohen_kappa_score([ai[i] for i in ids], [adj[i] for i in ids])
    print(f"Human-vs-human kappa: {k_hh:.3f}")
    print(f"AI-vs-adjudicated kappa: {k_ai:.3f}")
    if k_ai >= 0.80:   v = "ACCEPT"
    elif k_ai >= 0.60: v = "CORRECT (apply error-model correction)"
    else:              v = "REJECT (recalibrate criteria and re-screen)"
    print(f"Verdict: {v}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("sample")
    sp.add_parser("kappa")
    a = p.parse_args()
    {"sample":cmd_sample, "kappa":cmd_kappa}[a.cmd](a)
```

Run:
```powershell
python 06_analysis/scripts/validate_screening.py sample
python 06_analysis/scripts/validate_screening.py kappa
```

---

## APPENDIX B — One-Shot Verification (v2)

```python
# 06_analysis/scripts/99_verify_all_v2.py
import pandas as pd, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
em = pd.read_csv(ROOT/"02_data_processed/extracted_master_v2.csv")
sa = pd.read_csv(ROOT/"02_data_processed/screening_audit_v2.csv")
checks = []
def ck(n, cond, a, e): checks.append((n, "PASS" if cond else "FAIL", a, e))

inc = len(em) - int(em.get("is_double_extraction", pd.Series([0]*len(em))).sum())
ck("inclusion rate in [0.25,0.45]", 0.25 <= inc/1719 <= 0.45, round(inc/1719,3), "0.25-0.45")
ck("qa_total in 0-10", em.qa_total.between(0,10).all(), em.qa_total.min(), ">=0")
ck("qa_tier valid", em.qa_tier.isin(["Q-high","Q-medium","Q-low"]).all(), "-", "-")
ck("sim-only capped", ((em.real_or_sim!="sim") | (em.qa_tier!="Q-high")).all(), "-", "-")

for n,s,a,e in checks: print(f"[{s}] {n} actual={a} expected={e}")
sys.exit(0 if all(c[1]=="PASS" for c in checks) else 1)
```

---

## APPENDIX C — Escalation

If calibration (Phase 5) or kappa (Phase 5b) fails:
1. Print the failing metric (rate or kappa).
2. Print the v2 criteria text with the I2 rule highlighted.
3. Write `08_docs/BLOCKED_phaseN.md` with:
   - Failing metric + actual value
   - Suggested adjustment (tighten/loosen I2, add criterion)
   - Sample of borderline papers driving the failure
4. STOP. Await user instruction.

---

**End of MASTER_PROMPT_v2.md**
