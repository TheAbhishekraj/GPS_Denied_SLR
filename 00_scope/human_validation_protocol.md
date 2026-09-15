# Human Validation Protocol — AI Screening Agreement

## Purpose

This protocol provides the PRISMA-required evidence that AI eligibility screening was
validated against independent human judgment under
[screening criteria v2](./screening_criteria_v2.md).

## 1. Sampling

- Draw a stratified random sample of 10% of the screening corpus.
- Strata are the cross-product of AI decision (`INCLUDE`, `EXCLUDE`,
  `BORDERLINE_EXCLUDE`) and source database (`IEEE Xplore`, `Scopus`).
- Use a minimum of 100 papers and a maximum of 300 papers.
- Use the fixed seed `numpy.random.default_rng(42)`.
- Generate the reproducible sample and publish the selected records in
  [`08_docs/validation_sample.csv`](../08_docs/validation_sample.csv) using
  [`06_analysis/scripts/sample_validation.py`](../06_analysis/scripts/sample_validation.py).
- The sampler uses proportional allocation with largest-remainder rounding. Any
  remainder is assigned only to non-empty strata, and no paper can be sampled twice.

## 2. Reviewers

- Two independent, domain-literate human reviewers participate; at least one has
  systematic-review experience.
- Reviewers apply `screening_criteria_v2.md` blind to the AI decision.
- Each reviewer records a binary eligibility decision and criterion-level notes in
  the validation workbook or an equivalent signed data file.
- Disagreements are resolved by discussion. Unresolved cases go to a third
  adjudicator.
- The post-adjudication human decision is the reference standard.

## 3. Agreement statistics

Report in the manuscript and appendix:

- Cohen's kappa for Human 1 versus Human 2.
- Cohen's kappa for Human 1 versus AI.
- Cohen's kappa for Human 2 versus AI.
- Cohen's kappa for adjudicated human decision versus AI.
- Raw agreement and prevalence-adjusted kappa.
- Per-criterion confusion counts, including the criterion most often missed by AI.
- AI sensitivity and specificity against the adjudicated reference standard.

Interpretation:

- `kappa >= 0.80`: accept AI screening without further correction.
- `0.60 <= kappa < 0.80`: apply the error-model correction and re-screen.
- `kappa < 0.60`: re-calibrate the prompt and re-run screening from scratch.

## 4. Validation report

Complete [`08_docs/screening_validation_report.md`](../08_docs/screening_validation_report.md)
after both independent reviews and adjudication. Do not calculate agreement statistics
until reviewer decisions are complete.

## 5. Error-model correction

If `0.60 <= kappa < 0.80`:

1. Extract every false include and false exclude from the validation sample.
2. Classify each failure as criterion misapplication, missing abstract signal,
   prompt ambiguity, or LLM refusal/formatting.
3. Add explicit counter-examples for the top failure class to a versioned prompt v3.
4. Re-screen only the affected stratum, such as all borderline papers.
5. Record the change in
   [`03_prompts/SCREENING_PROMPT_CHANGELOG.md`](../03_prompts/SCREENING_PROMPT_CHANGELOG.md).

## 6. Extraction validation quality gate

Independently re-extract 20 core papers: 10 Core-tier papers and 10 additional
random core papers. Compare exact agreement for platform, environment, sensors,
algorithm family, metrics, and citation tier. Any field below 90% exact agreement
requires a schema revision before full extraction.
