# PDF_NUMERIC_PROBE_REPORT.md

Pre-flight probe for `02_data_processed/MASTER_EVIDENCE_V1.csv`.

- PDFs scanned: `05_papers_fulltext/*.pdf` (n = 291)
- ID basis: `02_data_processed/extracted_master_v2.csv`
- All patterns are word-guarded (`(?<![A-Za-z\-])` + `\b`) so ordinary
  words such as estimate / illustrate / generate / except cannot fire.
- This is keyword proximity, **not** extraction. A number found near a
  metric word may belong to a related-work table comparing other systems.

## 1. Headline

- Papers that even mention **ATE**: 16 / 291 (5.5%)
- Papers with an **ATE + numeric value + unit**: 3 / 291 (1.0%)
- Papers that mention **RMSE**: 96 / 291 (33.0%)
- Papers with **RMSE + numeric value + unit**: 45 / 291 (15.5%)
- Papers that mention **RPE**: 3 / 291 (1.0%)
- Papers with **any** unit-anchored accuracy number: 88 / 291 (30.2%)

## 2. Full signal table

| Signal | PDFs | Share |
|---|---|---|
| mentions ATE | 16 | 5.5% |
| ATE + number + unit | 3 | 1.0% |
| mentions RMSE | 96 | 33.0% |
| RMSE + number + unit | 45 | 15.5% |
| mentions RPE | 3 | 1.0% |
| RPE + number + unit | 0 | 0.0% |
| drift + number + % or m | 8 | 2.7% |
| success rate + number + % | 7 | 2.4% |
| position / positioning / localization error + number + unit | 42 | 14.4% |
| any of the above numeric signals | 88 | 30.2% |
| NAIVE probe (ATE|RMSE|drift)[^\n]{0,40}\d - known inflated | 287 | 98.6% |
| PDFs with <3000 extractable chars | 1 | 0.3% |

## 3. Why the naive probe must not be used

`08b_ate_token_diagnostic.py` measured what the naive pattern actually
matches. Almost every hit came from the tail of an ordinary word
(`ATE` inside estim-ate, illustr-ate, gener-ate, approxim-ate,
calcul-ate, coordin-ate, upd-ate, integr-ate, accur-ate, evalu-ate), or
from `cep` inside ex-cept / con-cept. The naive count is therefore
useless as an estimate of metric reporting and is kept only as a
cautionary baseline.

Two further leaks survived the first, case-insensitive character guard
and had to be closed explicitly:

1. Hyphenated line breaks, where the preceding character is a space
   rather than the hyphen - `moder- ate`, `evalu- ate`.
2. PDF ligatures, where the preceding character is U+FB01/U+FB02 and so
   is not in `[A-Za-z]` - `con\ufb02ate`, `In\ufb02ate`.

Both are closed by matching the acronyms case-sensitively. Papers write
`ATE`, never `ate`, so no genuine hit is lost.

## 4. Reconciliation

- PDFs parsed: 291 / 291
- PDFs that failed to parse: 0
- PDF stems absent from `extracted_master_v2.csv`: 120
- PDFs with a thin text layer: 1. The median
  extractable text across the corpus is about 34,000 characters, so the
  text layer is healthy and the low ATE count is a property of the
  corpus, not a parsing artifact.

## 5. Consequence for gate V9

Gate V9 in `08_docs/MASTER_VERIFICATION_PROTOCOL.md` requires at least 5
`approach_family` values carrying a numeric `best_ate_rmse`. ATE is used
by only a handful of papers, so the strict form of V9 is very likely to
fail. Two honest responses exist:

1. Re-scope V9 to any unit-anchored accuracy metric
   (`best_ate_rmse` **or** `other_metric_value`). 44 / 171 papers carry
   such a number, so this is likely to clear 5 families and keeps a
   quantitative section in the manuscript.
2. Keep V9 strict, let it fail, and reframe the manuscript as an
   architectural / thematic SLR per the confirmation checklist.

See `PREFLIGHT_FINDINGS.md` section 3. Do not fill `best_ate_rmse` by
guesswork to rescue V9; write `NOT_REPORTED` and let V9 report the truth.

## 6. Files

- `pdf_numeric_probe_v1.csv` - per-PDF flags and first matched snippet,
  for manual spot-reading of any flag that looks wrong.
- `pdf_numeric_probe_v1.json` - aggregate counts, machine-readable.
- `06_analysis/scripts/08b_ate_token_diagnostic.py` - the diagnostic that
  exposed the false positives and confirmed text-layer health.
- `PREFLIGHT_FINDINGS.md` - decision memo: what the probe means for
  gate V9, the six genuine ATE papers, and the two spec defects found.
