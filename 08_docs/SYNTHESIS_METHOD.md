# Synthesis Method — GPS_Denied_SLR

> Status: FINAL — APPROVED 2026-09-19
> Approved by: Abhishek Raj
> Date: 2026-09-19

## Declared approach
Structured narrative synthesis with descriptive quantitative
tabulation. A classical statistical meta-analysis is NOT planned.

## Justification
1. High methodological heterogeneity across the corpus: platforms,
   sensor suites, environments (indoor / urban / subterranean /
   forest / adversarial), and evaluation protocols differ
   substantially between papers.
2. Metrics are not uniformly reported: different error definitions
   (ATE, RMSE, relative drift), different units, different
   trajectory lengths, and figure-only reporting (Rule E4) prevent
   valid effect-size pooling for most of the corpus.
3. PRISMA 2020 item 20b permits a structured narrative synthesis
   when meta-analysis is not feasible, provided the decision and
   rationale are reported in the manuscript Methods section.

## Synthesis structure (maps to RQ1-RQ4 in 00_scope/SCOPE.md)
1. Group papers by taxonomy_category, method_category, environment,
   and real_or_sim (columns 23, 13, 10, 15 of EXTRACTION_SCHEMA_v1).
2. Tabulate frequency distributions (figures F2-F8 of
   MANUSCRIPT_SPEC.md).
3. Within each group, narratively compare headline_results with
   their verbatim quotes and page citations; report ranges as
   printed (Rule E6). No pooling, no averaging across papers.
4. Where a subgroup of papers reports the same metric with the same
   unit on comparable platforms, a descriptive summary table
   (T4) may show printed ranges; each cell carries its source
   paper ID and page.

## What is forbidden in synthesis
- No pooled effect sizes or confidence intervals across papers.
- No conversion of units to force comparability (Rule E5).
- No imputation of missing metrics; NOT_REPORTED stays NOT_REPORTED
  and is itself reported as a finding.
- No forbidden legacy numbers anywhere in synthesis outputs.

## Outputs
- 06_analysis/outputs/inference_table.csv
- 06_analysis/outputs/taxonomy_distribution.csv
- 06_analysis/outputs/figures/*.png (F2-F9)
- 08_docs/SYNTHESIS_REPORT.md
Every number in these outputs traces to MASTER_EVIDENCE.csv rows,
which trace to PDF quotes and pages.
