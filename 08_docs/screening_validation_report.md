# Screening validation report (Phase 5-K)

Source worksheet: `validation_sample.csv` (172 adjudicated rows)

## Agreement statistics (protocol section 3)

| Comparison | Cohen's kappa | Raw agreement |
|---|---:|---:|
| Human 1 vs Human 2 | 0.951 | 0.977 |
| Human 1 vs AI | 0.874 | 0.936 |
| Human 2 vs AI | 0.875 | 0.936 |
| Adjudicated vs AI | 0.874 | 0.936 |

- Prevalence-adjusted kappa (PABAK), adjudicated vs AI: **0.872**
- AI sensitivity vs adjudicated reference: **1.000**
- AI specificity vs adjudicated reference: **1.000**

## Confusion counts (include vs not-include, AI vs adjudicated)

| | adjudicated include | adjudicated not-include |
|---|---:|---:|
| AI include | 64 | 0 |
| AI not-include | 0 | 108 |

## Decision-rule verdict (protocol section 3)

| kappa band | Action |
|---|---|
| >= 0.80 | accept AI screening without correction |
| 0.60 - 0.80 | apply error-model correction (protocol section 5) |
| < 0.60 | recalibrate prompt, re-run screening from scratch |

**Verdict: ACCEPT** - use AI screening as-is (AI-vs-adjudicated kappa=0.874).
