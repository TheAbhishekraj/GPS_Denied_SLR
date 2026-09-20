# BATCH B02 - Extraction Report

Generated: 2026-09-19T19:52:00Z
Status: EXTRACTED - merged after verification

## Reviewed artifact hash (merge hash-guard)
```
BATCH_B02.csv SHA256: BE407226698C6FD212219D4003E4834DFB098569511987195A32F09FEDF1DE55
```

## Verification
| check | expected | observed | result |
|---|---|---|---|
| data rows | 10 | 10 | PASS |
| header == EXTRACTv1 schema | match | match | PASS |
| rows missing id/title/_source_pages | 0 | 0 | PASS |
| text files in _pages/ | 10 | 10 | PASS |

## IDs
REC_0037, REC_0041, REC_0043, REC_0057, REC_0064, REC_0065, REC_0066, REC_0071, REC_0077, REC_0080

## Notes
- doi NOT_REPORTED where the DOI sits in a page footer outside the page-1 header window.
- Interpretive fields NOT_REPORTED by design; filled in the interpretive pass from _pages/ text.
- Spot-check: PENDING HUMAN REVIEW (D3).