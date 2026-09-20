# Anchor Freeze — 2026-09-19

## Frozen counts
| Stage | Value |
|---|---|
| Raw records identified | 2,000 (IEEE 1,000 + Scopus 1,000) |
| Duplicates removed | 284 |
| Unique records after dedup | 1,716 |
| Records passing title/abstract | 636 |
| Full-text records assessed | 291 |
| PDFs on disk | 288 |
| PDFs pending retrieval | 3 (duplicate EXCLUDEs, not restored) |
| Studies INCLUDE | 285 |
| Studies EXCLUDE | 6 (3 x E1, 3 x E2) |

## Excluded records
| ID | Rule | Reason |
|---|---|---|
| REC_0053 | E1 | Out of scope |
| REC_0693 | E1 | Out of scope |
| REC_0866 | E1 | Out of scope |
| REC_1582 | E2 | Duplicate of REC_0274 |
| REC_1688 | E2 | Duplicate of REC_1715 |
| REC_1715 | E2 | Duplicate of REC_1688 |

## Removed duplicate PDFs
| Removed | Canonical | SHA256 prefix |
|---|---|---|
| REC_1582.pdf | REC_0274.pdf | 4D3DCB09 |
| REC_1688.pdf | REC_1715.pdf | 41AE7D59 |
| REC_1715.pdf | REC_1688.pdf | 41AE7D59 |

## File hashes (SHA256)
| File | SHA256 |
|---|---|
| 01_data_raw/ieee_xplore_20260615.csv | FE374C9F2A405A0F0E07598979340AE971311B80BB20D8E121572D648CAA18F3 |
| 01_data_raw/scopus_20260615.csv | EF162F4F9525B6FC5CC617D1E3BADACD11F09B3E80FDFC488C4E37918BD524CB |
| 02_data_processed/deduplicated_master.csv | A648930848EED1950A602EA5FA2F739CFDDB1C2BB1289F86B810211DB3D8649A |
| 02_data_processed/screened_included_v2.csv | CD1B38745FF653BE3E23C62371B87A12861261BDC057F4F313645C4A79E93CED |
| 02_data_processed/screening_results.csv | 86DADC842AA590B03C0F5145FFCA5340800CB41AE505BC7AD1488CB40648F6D7 |

## PRISMA flow
2,000 -> 1,716 -> 636 -> 291 -> 285 INCLUDE / 6 EXCLUDE

## Freeze rules
1. No count changes without a new freeze doc.
2. No decision changes without a new freeze doc.
3. No PDF removed without a new freeze doc.
4. Every extraction batch reconciles against this freeze.
5. Five legacy numeric strings are deprecated and must not
   appear in any live file. Their values are on record in
   _AUDIT/INSTALLATION_REPORT.md only. Do not reproduce them.

## Next phase
Phase 5 — Extraction pipeline rebuild. Target: 285 INCLUDE papers.
