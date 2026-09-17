# PDF_NUMERIC_PROBE_REPORT.md

Pre-flight probe for `02_data_processed/MASTER_EVIDENCE_V1.csv`.

- PDFs scanned: `05_papers_fulltext/*.pdf` (n = 171)
- ID basis: `02_data_processed/extracted_master_v2.csv`
- All patterns are word-guarded (`(?<![A-Za-z\-])` + `\b`) so ordinary
  words such as estimate / illustrate / generate / except cannot fire.
- This is keyword proximity, **not** extraction. A number found near a
  metric word may belong to a related-work table comparing other systems.

## 1. Headline

- Papers that even mention **ATE**: 6 / 171 (3.5%)
- Papers with an **ATE + numeric value + unit**: 1 / 171 (0.6%)
- Papers that mention **RMSE**: 40 / 171 (23.4%)
- Papers with **RMSE + numeric value + unit**: 20 / 171 (11.7%)
- Papers that mention **RPE**: 2 / 171 (1.2%)
- Papers with **any** unit-anchored accuracy number: 44 / 171 (25.7%)

## 2. Full signal table

| Signal | PDFs | Share |
|---|---|---|
| mentions ATE | 6 | 3.5% |
| ATE + number + unit | 1 | 0.6% |
| mentions RMSE | 40 | 23.4% |
| RMSE + number + unit | 20 | 11.7% |
| mentions RPE | 2 | 1.2% |
| RPE + number + unit | 0 | 0.0% |
| drift + number + % or m | 2 | 1.2% |
| success rate + number + % | 7 | 4.1% |
| position / positioning / localization error + number + unit | 21 | 12.3% |
| any of the above numeric signals | 44 | 25.7% |
| NAIVE probe (ATE|RMSE|drift)[^\n]{0,40}\d - known inflated | 167 | 97.7% |
| PDFs with <3000 extractable chars | 1 | 0.6% |

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

- PDFs parsed: 171 / 171
- PDFs that failed to parse: 0
- PDF stems absent from `extracted_master_v2.csv`: 0
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
