# FINAL AUDIT - GPS_Denied_SLR (DRAFT)

Generated: 2026-09-19T20:45:00Z
Status: DRAFT - AWAITING HUMAN REVIEW

## 1. Final row count
| item | value |
|---|---|
| MASTER_EVIDENCE.csv rows | 279 |
| Expected (285 INCLUDE - 6 deferred) | 279 |
| Match | YES |

## 2. SHA256 ledger
| file | sha256 |
|---|---|
| 02_data_processed/MASTER_EVIDENCE.csv | 15B26C59DFAAAD0A62A3D473AC7EB4DFC0491A89B7B6D4D5CF78BB8FB512B2C6 |
| 02_data_processed/screening_results.csv | 86DADC842AA590B03C0F5145FFCA5340800CB41AE505BC7AD1488CB40648F6D7 |
| 02_data_processed/deduplicated_master.csv | A648930848EED1950A602EA5FA2F739CFDDB1C2BB1289F86B810211DB3D8649A |
| 07_manuscript/MANUSCRIPT_V2.md | 542BE0ED72D6CED9AA58FE1D0C95ADA4015AABAF058B2DC169EB313D56D4C391 |
| 08_docs/SYNTHESIS_REPORT.md | 1E4DC5A86C23C1FA9A90546D228CAED9BEA6D554E7F766BD600B84E6E788AAD5 |
| .clinerules (post-amendment) | F7EA28F2E89B12FFE683A934EC4AADFDE43F73AB1424499DD041672C8CCB69D2 |

Frozen-file integrity: screening_results.csv and deduplicated_master.csv are unchanged from their frozen values (86DADC84... / A6489308...).

## 3. Script run log (2026-09-19)
| time (UTC) | script | result |
|---|---|---|
| 18:48 | validate_master.py | Rows 0, Structure PASS |
| 19:51 | validate_master.py + merge_batch.py B01 | 10 rows, PASS |
| 19:50-19:52 | merge_batch.py B01 | master 0 -> 10 |
| 19:52 | merge_batch.py B02 | master 10 -> 20 |
| 19:55 | merge_batch.py B03-B05 | master 50 |
| 19:58 | merge_batch.py B06-B09 | master 90 |
| 20:02 | merge_batch.py B10-B13 | master 130 |
| 20:12 | merge_batch.py B17-B19 | master 190 |
| 20:16 | merge_batch.py B20-B22 | master 220 |
| 20:20 | merge_batch.py B23-B25 | master 250 |
| 20:25 | merge_batch.py B26-B28 | master 279 |
| 20:45 | validate_master.py (final) | Rows 279, Structure PASS, Overall PASS |

## 4. Validator output (final)
```
Rows: 279
Expected: 285
Structure: PASS
Duplicate IDs: 0
Empty required fields: 0
Overall: PASS
```

## 5. Unresolved items
1. Six deferred IDs: REC_0023, REC_0035, REC_0244, REC_1217, REC_1667, REC_0363 (identity conflict; not extracted).
2. All 24 interpretive fields NOT_REPORTED for 279/279 records - interpretive pass not run.
3. 13 [UNRESOLVED] markers in MANUSCRIPT_V2.md (Results 4.2-4.6, Discussion, References).
4. Figures F1-F9 not generated (Rule 9 spec required for figures.py).
5. doi NOT_REPORTED wherever the DOI is in a page footer.
6. validate_master.py hard-codes Expected: 285 (now 279); script not modified (Rule 9).
7. Two tool timeouts occurred during batch runs; state re-verified, no partial merge.

## 6. Forbidden-number scan
- Patterns scanned: the four forbidden formatted strings.
- Hits in new outputs: 0 (expected 0).

## 7. Pending human actions
1. Spot-check 1 paper per batch (28 checks) - DEFERRED by D3.
2. Resolve the 6 deferred IDs.
3. Review MANUSCRIPT_V2.md (draft, not final).
4. Approve or reject synthesis outputs.
5. Decide on the interpretive extraction pass (unblocks all substance).
6. Final submission approval - NOT performed.

## 8. Compliance attestation
- No frozen file modified. No anchor count changed.
- No phase marked PASS by the agent.
- No submission made.
- No write outside the allowlist.
- No fabricated value: absent data is NOT_REPORTED or [UNRESOLVED].