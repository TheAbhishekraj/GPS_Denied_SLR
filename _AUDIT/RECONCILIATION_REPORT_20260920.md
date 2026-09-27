# RECONCILIATION & EXTRACTION AUDIT REPORT

**Date**: 2026-09-20  
**Scope**: Systematic Literature Review — GPS-Denied UAV Navigation  
**Audit Target**: Complete cross-verification of corpus across `MASTER_EVIDENCE.csv`, `03_extraction/per_paper/`, and `_MANUAL/abhishek/per_paper/`.

---

## 1. Corpus Inventory Summary

| Repository Component | File / Directory | Count | Status / Notes |
|---|---|:---:|---|
| **Raw Screening Pool** | `01_data_raw/*.csv` | 2,000 | Frozen (IEEE: 1,000, Scopus: 1,000) |
| **Deduplicated Corpus** | `02_data_processed/deduplicated_master.csv` | 1,716 | Frozen |
| **Title/Abstract Pass** | `02_data_processed/screening_results.csv` | 636 | Frozen |
| **Full-Text Included** | `02_data_processed/screening_results.csv` (INCLUDE) | 285 | Frozen (285 INCLUDE, 6 EXCLUDE) |
| **Safe Extraction Target** | `02_data_processed/MASTER_EVIDENCE.csv` | 279 | 6 deferred under audit integrity check |
| **Manual Extractions** | `_MANUAL/abhishek/per_paper/*.md` | 168 | 161 match Master; 7 extra/deferred; 163 are 18-sec |
| **Pipeline Extractions** | `03_extraction/per_paper/*.md` | 292 | 279 match Master; 13 extra/deferred; 30 are 18-sec |

---

## 2. Extraction Format & Quality Breakdown

### `_MANUAL/abhishek/per_paper/` (168 files total)
- **Standard 18-section template**: **163 files** (97.0%)
- **Legacy 16-section template**: **5 files** (`REC_1083`, `REC_1084`, `REC_1085`, `REC_1095`, `REC_1096`)
- **Coverage of 279 Master Included**: **161 / 279** (**57.7%**)

### `03_extraction/per_paper/` (292 files total)
- **Standard 18-section template**: **30 files** (10.3%)
- **Legacy machine template**: **261 files** (89.7%)
- **Coverage of 279 Master Included**: **279 / 279** (**100%**) *(deterministic / machine format)*

---

## 3. Batch-by-Batch Coverage in `_MANUAL/abhishek/per_paper`

| Batch | Range | Target Count | In `_MANUAL` | Status | Missing IDs in `_MANUAL` |
|---|---|:---:|:---:|:---:|---|
| **B01** | REC_0001 – REC_0033 | 10 | 10 | **COMPLETE** | None |
| **B02** | REC_0037 – REC_0080 | 10 | 10 | **COMPLETE** | None |
| **B03** | REC_0083 – REC_0209 | 10 | 10 | **COMPLETE** | None |
| **B04** | REC_0211 – REC_0271 | 10 | 10 | **COMPLETE** | None |
| **B05** | REC_0274 – REC_0343 | 10 | 10 | **COMPLETE** | None |
| **B06** | REC_0348 – REC_0411 | 10 | 10 | **COMPLETE** | None |
| **B07** | REC_0423 – REC_0485 | 10 | 10 | **COMPLETE** | None |
| **B08** | REC_0487 – REC_0579 | 10 | 10 | **COMPLETE** | None |
| **B09** | REC_0586 – REC_0690 | 10 | 10 | **COMPLETE** | None |
| **B10** | REC_0698 – REC_0776 | 10 | 10 | **COMPLETE** | None |
| **B11** | REC_0782 – REC_0861 | 10 | 10 | **COMPLETE** | None |
| **B12** | REC_0868 – REC_0939 | 10 | 10 | **COMPLETE** | None |
| **B13** | REC_0940 – REC_1002 | 10 | 10 | **COMPLETE** | None |
| **B14** | REC_1006 – REC_1049 | 10 | 9 | **PARTIAL** | `REC_1032` |
| **B15** | REC_1055 – REC_1085 | 10 | 10 | **COMPLETE** | None |
| **B16** | REC_1095 – REC_1106 | 10 | 10 | **COMPLETE** | None |
| **B17** | REC_1107 – REC_1135 | 10 | 2 | **PARTIAL** | `REC_1114`, `REC_1115`, `REC_1116`, `REC_1118`, `REC_1123`, `REC_1130`, `REC_1132`, `REC_1135` |
| **B18** | REC_1137 – REC_1165 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B19** | REC_1167 – REC_1190 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B20** | REC_1191 – REC_1232 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B21** | REC_1235 – REC_1270 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B22** | REC_1274 – REC_1302 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B23** | REC_1304 – REC_1330 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B24** | REC_1336 – REC_1393 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B25** | REC_1399 – REC_1435 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B26** | REC_1438 – REC_1474 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B27** | REC_1480 – REC_1587 | 10 | 0 | **EMPTY** | All 10 IDs |
| **B28** | REC_1608 – REC_1678 | 9 | 0 | **EMPTY** | All 9 IDs |
| **TOTAL** | | **279** | **161** | **57.7%** | **118 missing** |

---

## 4. Specific Action Punch List

1. **Immediate Gap in B14**: Complete `REC_1032.md` to bring B14 to 10/10.
2. **Immediate Gap in B17**: Complete the remaining 8 papers in B17 (`REC_1114` through `REC_1135`).
3. **Format Update in B15–B16**: Upgrade `REC_1083`, `REC_1084`, `REC_1085`, `REC_1095`, `REC_1096` from 16-section to the standardized 18-section template.
4. **Subsequent Batches**: Process batches B18 through B28 (109 papers) to reach 100% (279/279).
