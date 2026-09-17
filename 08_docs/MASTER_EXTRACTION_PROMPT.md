# MASTER EXTRACTION PROMPT — Build MASTER_EVIDENCE_V1.csv and per-paper MDs

You are working in E:\GPS_Denied_SLR. Your job is to read 171 PDFs and produce
two artifacts:

1. `02_data_processed/MASTER_EVIDENCE_V1.csv` — one row per paper, 63 columns.
2. `03_extraction/per_paper/<id>.md` — one file per paper using the template
   at `01_corpus/MASTER_PAPER_TEMPLATE.md`.

## GOVERNING FILES — read before writing
- `01_corpus/MASTER_PAPER_TEMPLATE.md` — the per-paper template
- `02_data_processed/extracted_master_v2.csv` — categorical source (do not modify)
- `06_analysis/audit/V1_audit_20260917T124255Z.json` — audit truth
- `MASTER_SLR_WRITING_SOP_V2.md` — governing SOP
- `00_scope/PROTOCOL.md` — RQ1–RQ4
- `00_scope/screening_criteria_v2.md` — I1–I6 / E1–E8

## HARD CONSTRAINTS
- Do NOT modify extracted_master_v2.csv.
- Do NOT modify the stale drafts.
- Do NOT guess numeric values. If a paper does not report ATE / RMSE / drift,
  write NOT_REPORTED for the metric.
- Every numeric value must be traceable to a numbered table, a numbered figure,
  or a page. Record the source in `extraction_source`.
- Every `id` in the new CSV must match an existing `id` in extracted_master_v2.csv.
  If a PDF's id is not in the master CSV, STOP and report.

## CANONICAL NUMBERS (unchanged)
- N = 171; coverage 171/636 = 26.9%; not retrieved 465
- qa_tier: Q-high 38 | Q-medium 84 | Q-low 49
- citation_tier: Core 35 | Important 87 | Peripheral 49
- real_or_sim: Real_World 22 | Simulation 78 | Both 71
- Audit: 170 PASS + 1 PASS_EXCEPTION (REC_1137)

## FORBIDDEN IN ALL NEW OUTPUTS
1,692 — 1,700 — 1,719 — 2,000 — 281 — 1,332 — 495 — 98.4%

## OPERATOR NOTE — numeric-reporting expectation (added 2026-09-17)

A pre-flight probe of all 171 PDFs established the honest baseline for the
numeric columns. Read this before Step 2 and do not treat it as a target to hit:

- ~44 / 171 papers report any unit-anchored accuracy metric.
- ~127 / 171 papers report none.
- Only ~6 / 171 papers use the metric ATE at all.

Therefore, expecting roughly **44 (band 38–61) rows** to carry a value other
than `NOT_REPORTED` in at least one of: `best_ate_rmse`, `best_rpe`,
`drift_rate_pct`, `success_rate_pct`, `improvement_vs_baseline_pct`,
`other_metric_value`.

Hard rules:
- Do NOT widen a metric to reach a count. A number is only valid if it appears
  in the paper with a unit, traceable to a table, figure or page.
- Non-reporting is the expected outcome for the majority of rows and is itself
  a finding. `NOT_REPORTED` is a correct, complete answer.
- If you find yourself above ~61 numeric rows, re-check for invented or
  borrowed values (e.g. numbers copied from a related-work comparison of other
  systems into the paper's own `best_ate_rmse`).

Evidence for these expectations: `06_analysis/output/pdf_numeric_probe_v1/`.

## STEP 1 — Create the header CSV (once)

Create `02_data_processed/MASTER_EVIDENCE_V1.csv` with exactly this header row
(63 comma-separated columns):

id,authors,title,year,venue,venue_type,doi,url,abstract_summary,problem_setting,
historical_context,approach_family,named_method,core_idea,algorithmic_components,
fusion_strategy,learning_used,sensors_used,sensor_fusion_count,hardware_platform,
compute_onboard,flight_time_or_trajectory_length,environment_tested,
environment_category,real_or_sim,dataset_used,ground_truth_method,number_of_runs,
best_ate_rmse,best_ate_rmse_unit,best_rpe,best_rpe_unit,drift_rate_pct,
success_rate_pct,improvement_vs_baseline_pct,other_metric_name,other_metric_value,
other_metric_unit,baseline_compared,baseline_type,head_to_head_result,
claimed_novelty,failure_mode_1,failure_mode_2,failure_mode_3,stated_limitations,
stated_future_work,qa_rigor,qa_reporting,qa_baseline,qa_reproducibility,qa_total,
qa_tier,citation_tier,extraction_source,extractor,verified_by_human,
verifier_initials,verification_date,rq_relevance,manuscript_table,
manuscript_figure,notes

(The agent must join these into ONE line when writing the file.)

## STEP 2 — Process each PDF (171 iterations)

For each PDF in `05_papers_fulltext/*.pdf`:
1. Open with PyMuPDF; extract text.
2. Locate: abstract, introduction, methodology, experiments, results tables,
   discussion, limitations, future work.
3. Populate one row of MASTER_EVIDENCE_V1.csv per the schema.
4. Populate one `03_extraction/per_paper/<id>.md` per the template.
5. Copy qa_* and citation_tier verbatim from extracted_master_v2.csv. Do not
   recompute them.
6. Set extractor = "AI", verified_by_human = "N" on first pass.

Print progress every 10 papers. Log every PDF that fails to parse to
`08_docs/EXTRACTION_FAILURES.md` and continue.

## STEP 3 — Per-paper MD files

For every row written to the CSV, write the equivalent MD at
`03_extraction/per_paper/<id>.md` using MASTER_PAPER_TEMPLATE.md.

If a section of the paper is missing, write `NOT_REPORTED` or `NOT_STATED`
in the corresponding template field. Never leave a field blank.

## STEP 4 — Verification sample (agent produces, does not fill)

```powershell
$ev = Import-Csv 02_data_processed\MASTER_EVIDENCE_V1.csv
$sample = $ev | Get-Random -Count 34 -SetSeed 42
$sample | Export-Csv 08_docs\MASTER_EVIDENCE_VERIFY_SAMPLE.csv -NoTypeInformation
```

This produces a 34-row sample (20% of 171). Do not fill it.

## STEP 5 — Summary statistics (for the report)

After Step 2 completes, compute and print:
- total rows
- rows with best_ate_rmse != NOT_REPORTED
- rows with drift_rate_pct != NOT_REPORTED
- rows with baseline_compared != NONE_REPORTED
- distribution of approach_family
- distribution of environment_category
- distribution of real_or_sim
- distribution of rq_relevance
- top-10 most-cited named_method strings

## STEP 6 — Self-gates (must all pass before reporting done)

G1: MASTER_EVIDENCE_V1.csv has exactly 171 data rows (172 including header).
G2: Every id in MASTER_EVIDENCE_V1.csv exists in extracted_master_v2.csv.
G3: 171 files exist under 03_extraction/per_paper/.
G4: 08_docs/MASTER_EVIDENCE_VERIFY_SAMPLE.csv has 34 rows.
G5: Forbidden numbers appear 0 times in any new file.
G6: Every qa_total in the master CSV equals the corresponding qa_total in
    extracted_master_v2.csv.

If any gate fails, STOP and report which gate.

## STEP 7 — Report

Return a single block with:
- G1–G6 results
- The Step 5 summary statistics
- Paths to all created files
- Count of PDFs that failed to parse
- A short note on which column proved hardest to populate consistently

Begin with STEP 1. Do not skip any step.