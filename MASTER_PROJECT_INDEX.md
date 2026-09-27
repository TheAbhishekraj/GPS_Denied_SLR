# MASTER PROJECT INDEX & AUDIT MANIFEST
**Project:** GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)  
**Standard:** PRISMA 2020 & PRISMA-S Guidelines  
**Current Milestone:** Phase 6 COMPLETE (279/279 extracted & frozen) | Phase 7 PARTIAL | Phase 8 DRAFT  
**Author / Reviewer:** Abhishek Raj  
**Repository Root:** `E:\GPS_Denied_SLR`  
**Last Updated:** 2026-09-27  

---

## 1. Canonical PRISMA 2020 Metric Baseline

Every reported number across all manuscript drafts, tables, and scripts must reproduce these verified counts:

| Pipeline Stage | Value | Source File | Status |
| :--- | :---: | :--- | :--- |
| **Raw Harvested Records** | **2,000** | [`01_data_raw/ieee_xplore_20260615.csv`](file:///e:/GPS_Denied_SLR/01_data_raw/ieee_xplore_20260615.csv) (1,000)<br>[`01_data_raw/scopus_20260615.csv`](file:///e:/GPS_Denied_SLR/01_data_raw/scopus_20260615.csv) (1,000) | **FROZEN** |
| **Deduplicated Records** | **1,716** | [`02_data_processed/deduplicated_master.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/deduplicated_master.csv) | **FROZEN** |
| **Duplicate Records Dropped** | **280** | [`02_data_processed/dedup_log.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/dedup_log.csv) | **FROZEN** |
| **Title/Abstract Screened Included** | **636** | [`02_data_processed/screened_included_v2.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/screened_included_v2.csv) | **FROZEN** |
| **Full-Text Assessed Records** | **291** | [`02_data_processed/screening_results.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/screening_results.csv) (285 INCLUDE, 6 EXCLUDE) | **FROZEN** |
| **Full-Text PDF Corpus** | **288** | [`05_papers_fulltext/`](file:///e:/GPS_Denied_SLR/05_papers_fulltext/) (288 PDFs on disk, 1.54 GB) | **FROZEN** |
| **Final Synthesis Corpus** | **279** | [`02_data_processed/MASTER_EVIDENCE.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/MASTER_EVIDENCE.csv) (285 Include − 6 Deferred = 279 rows) | **LIVE MASTER** |
| **Extraction Batches** | **28** | [`02_data_processed/evidence_batches/`](file:///e:/GPS_Denied_SLR/02_data_processed/evidence_batches/) (B01–B27: 10 rows; B28: 9 rows) | **COMPLETE** |
| **Manual Extraction Evidence Base** | **288** | [`_MANUAL/abhishek/per_paper/`](file:///e:/GPS_Denied_SLR/_MANUAL/abhishek/per_paper/) (279 in-corpus + 9 out-of-corpus) | **FROZEN MANIFEST** |
| **Pipeline Extraction Mirror** | **288** | [`03_extraction/per_paper/`](file:///e:/GPS_Denied_SLR/03_extraction/per_paper/) (100% hash-synced with `_MANUAL/`) | **SYNCHRONIZED** |

---

## 2. Directory-by-Directory Audit & File Catalog

### 📁 `00_scope/` — Protocol & Research Scope
* **Purpose:** Defines the systematic review research questions, inclusion/exclusion criteria, multi-sensor operational taxonomy, and 10-point quality appraisal rubric.
* **Audit State:** Option 2 completed. Refrozen post-peer-audit revisions (incorporating verbatim PRISMA-S queries, partial 2026 window definition, and simulation score cap rules).

| File Link | Data / Lines | Size | SHA256 Hash | Status |
| :--- | :---: | :---: | :--- | :--- |
| [`00_scope/SCOPE.md`](file:///e:/GPS_Denied_SLR/00_scope/SCOPE.md) | 176 lines | 13.4 KB | `94E9E287D7BDA1D63224EF48B9C95D633CAB0828EAF2B9164CB092F0499664A4` | **FROZEN (V2.0)** |
| [`00_scope/FROZEN.md`](file:///e:/GPS_Denied_SLR/00_scope/FROZEN.md) | 11 lines | 573 B | `2289C3A87F1F4836549CF4CE0F089D1CA0136A03199F41EC9D97E4FF0907FE59` | **FROZEN RECORD** |

---

### 📁 `01_data_raw/` — Raw Bibliographic Exports
* **Purpose:** Holds untouched, verbatim exported search records from IEEE Xplore and Elsevier Scopus harvested on 2026-06-15, plus execution search logs.
* **Audit State:** Fully verified against canonical 2,000 raw harvest total.

| File Link | Records | Size | SHA256 Hash | Status |
| :--- | :---: | :---: | :--- | :--- |
| [`01_data_raw/ieee_xplore_20260615.csv`](file:///e:/GPS_Denied_SLR/01_data_raw/ieee_xplore_20260615.csv) | 1,000 | 2.24 MB | `FE374C9F2A405A0F0E07598979340AE971311B80BB20D8E121572D648CAA18F3` | **FROZEN RAW** |
| [`01_data_raw/scopus_20260615.csv`](file:///e:/GPS_Denied_SLR/01_data_raw/scopus_20260615.csv) | 1,000 | 1.60 MB | `EF162F4F9525B6FC5CC617D1E3BADACD11F09B3E80FDFC488C4E37918BD524CB` | **FROZEN RAW** |
| [`01_data_raw/SEARCH_LOG.md`](file:///e:/GPS_Denied_SLR/01_data_raw/SEARCH_LOG.md) | 50 lines | 2.46 KB | `7C3683515326A42C0A4F16FD254AB300F0E992003C966C54AFD834E11E859A24` | Search Execution Log |
| [`01_data_raw/SEARCH_LOG_VERIFY.md`](file:///e:/GPS_Denied_SLR/01_data_raw/SEARCH_LOG_VERIFY.md) | 48 lines | 1.63 KB | `ED003EB3BE6D3E99F0CABBF0DF54CB0F8F59E463A827EDBDC80B294DA38E01CF` | Harvest Verification |

---

### 📁 `01_corpus/` — Legacy Template Directory
* **Purpose:** Historical directory containing an early single template file.
* **Audit State:** Stale Generation-1 artifact. Candidate for consolidation into `_ARCHIVE/`.

| File Link | Lines | Size | SHA256 Hash | Status |
| :--- | :---: | :---: | :--- | :--- |
| [`01_corpus/MASTER_PAPER_TEMPLATE.md`](file:///e:/GPS_Denied_SLR/01_corpus/MASTER_PAPER_TEMPLATE.md) | 177 lines | 6.18 KB | `8FD24177FBE4B9F1506B6CFBA9B6FDF1B6DC9EEAE1A424033C0E56A21750C6A0` | Legacy Template |

---

### 📁 `02_data_processed/` — Processed Evidence & Screening Pipeline
* **Purpose:** Core pipeline datasets including deduplication, multi-stage screening results, master extraction table, and 28 sequential extraction batches.
* **Audit State:** Audited on 2026-09-27. Eight legacy files moved to `_ARCHIVE/legacy_02_data_processed/`. Comprehensive manifest added.

| File Link | Rows / Items | Size | SHA256 Hash | Status |
| :--- | :---: | :---: | :--- | :--- |
| [`02_data_processed/README.md`](file:///e:/GPS_Denied_SLR/02_data_processed/README.md) | 105 lines | 7.54 KB | `C002C685BF0B269372BA937DB7D01FC52D71CBA593AF90C8D47D648E7723FE78` | **Directory Manifest** |
| [`02_data_processed/MASTER_EVIDENCE.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/MASTER_EVIDENCE.csv) | **279** | 134 KB | `15B26C59DFAAAD0A62A3D473AC7EB4DFC0491A89B7B6D4D5CF78BB8FB512B2C6` | **LIVE MASTER** |
| [`02_data_processed/deduplicated_master.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/deduplicated_master.csv) | **1,716** | 2.51 MB | `A648930848EED1950A602EA5FA2F739CFDDB1C2BB1289F86B810211DB3D8649A` | **FROZEN ANCHOR** |
| [`02_data_processed/dedup_log.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/dedup_log.csv) | **280** | 34.8 KB | `F725F1A367FB47DE5969FFAF3EB4615B600F4937DC16F3DBD5A7129097C24F04` | **FROZEN AUDIT** |
| [`02_data_processed/screened_included_v2.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/screened_included_v2.csv) | **636** | 1.08 MB | `CD1B38745FF653BE3E23C62371B87A12861261BDC057F4F313645C4A79E93CED` | **FROZEN ANCHOR** |
| [`02_data_processed/screening_results.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/screening_results.csv) | **291** | 505 KB | `86DADC842AA590B03C0F5145FFCA5340800CB41AE505BC7AD1488CB40648F6D7` | **FROZEN ANCHOR** |
| [`02_data_processed/DEDUP_REPORT.md`](file:///e:/GPS_Denied_SLR/02_data_processed/DEDUP_REPORT.md) | 54 lines | 2.31 KB | `093992EB3364DAB9C14080524ECAA57D1B2640134D3330D72D1BF7A27AB74798` | Audit Log |
| [`02_data_processed/DEDUP_VERIFY.md`](file:///e:/GPS_Denied_SLR/02_data_processed/DEDUP_VERIFY.md) | 26 lines | 975 B | `CD9AAA38722E6A5BE2BD9244807C814908FDF287D5D4A65E21E64D7A73A8598E` | Audit Log |
| [`02_data_processed/pdf_removal_log.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/pdf_removal_log.csv) | **3** | 285 B | `A9CFF5BCAF9A69B510CE5189FFACD5440CEDA60793946E67A23DFD9A8E30972D` | Duplicate PDF Audit |
| [`02_data_processed/screening_spreadsheet.xlsx`](file:///e:/GPS_Denied_SLR/02_data_processed/screening_spreadsheet.xlsx) | — | 2.28 MB | `9C7F2E281F472210EC2BE6571C3A37AA12338DB2C1A04B4072D67850C7935CB8` | Working Spreadsheet |
| [`02_data_processed/evidence_batches/`](file:///e:/GPS_Denied_SLR/02_data_processed/evidence_batches/) | **28 Batches** | — | B01–B27: 10 rows each; B28: 9 rows (Total = 279 rows) | **Batch Processing** |

---

### 📁 `03_extraction/` — Pipeline Extraction Mirror
* **Purpose:** Pipeline extraction directory used by automated analysis scripts. Mirrors the frozen reference base in `_MANUAL/abhishek/per_paper/`.
* **Audit State:** Audited on 2026-09-27. Three duplicate PDF extractions moved to archive. 288 files synchronized with frozen reference corpus (288 of 288 SHA256 match, 0 mismatches).

| File Link | Items / Lines | Size | SHA256 Hash | Status |
| :--- | :---: | :---: | :--- | :--- |
| [`03_extraction/README.md`](file:///e:/GPS_Denied_SLR/03_extraction/README.md) | 68 lines | 4.88 KB | `77D15D6C401C60A89993E86262ACAEA4491B2020F4E526533C79A3BBDDA94577` | **Directory Manifest** |
| [`03_extraction/per_paper/`](file:///e:/GPS_Denied_SLR/03_extraction/per_paper/) | **288** `REC_*.md` | ~1.5 MB | 288 of 288 match [`_MANUAL/abhishek/per_paper/`](file:///e:/GPS_Denied_SLR/_MANUAL/abhishek/per_paper/) | **100% SYNCHRONIZED** |
| [`03_extraction/per_paper/.gitkeep`](file:///e:/GPS_Denied_SLR/03_extraction/per_paper/.gitkeep) | 4 lines | 249 B | `A3CE7A6783196EF9561E8BC1D50DF0813959A83ED5BCA2BAF7B2F6E1C8EF901B` | Directory Marker |
| [`03_extraction/per_paper/QA_INDEX.md`](file:///e:/GPS_Denied_SLR/03_extraction/per_paper/QA_INDEX.md) | 2 lines | 37 B | `59C204599311A6B7FA0AD51FBEA858AC5FA3004BAB7DC0FBFC89E2191566FAAC` | QA Register (Header) |

---

## 3. Relocated Legacy Archives: `_ARCHIVE/`

To prevent confusion with live PRISMA 2020 statistics, obsolete Generation-1 files have been safely relocated using `git mv` into [`_ARCHIVE/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/):

### Manifest: [`_ARCHIVE/README.md`](file:///e:/GPS_Denied_SLR/_ARCHIVE/README.md)

1. **[`_ARCHIVE/legacy_02_data_processed/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_02_data_processed/)** (8 items):
   - `summary.txt` (conflicting 2026-09-06 numbers)
   - `MASTER_EVIDENCE_V1.xlsx` (pre-reset Excel table)
   - `EXTRACTION_NOTES.md` & `EXTRACTION_NOTES_v2.md` (deprecated notes)
   - `V1_SCOPE_IDS.txt` & `PENDING_MASTER_EXTENSION_IDS.txt` (stale ID lists)
   - `retrieval_log.csv` & `pending_list.csv` (empty templates)
2. **[`_ARCHIVE/legacy_03_extraction/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_03_extraction/)** (3 items):
   - `REC_1582.md`, `REC_1688.md`, `REC_1715.md` (extractions for excluded duplicate PDFs)
3. **[`_ARCHIVE/legacy_03_prompts/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_03_prompts/)** (5,134 files, 65.6 MB):
   - Historical Generation-1 prompt store (`extraction_prompts/`, `screening_prompts/`, `.jsonl` streams)
   - Permanently resolves the Rule 5 count collision.
4. **[`_ARCHIVE/legacy_04_ai_responses/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_04_ai_responses/)** (5,142 files, 6.7 MB):
   - Historical Generation-1 raw LLM response dumps (`extraction/`, `screening/`, `.jsonl` streams)

---

## 4. Upcoming Folders to Review & Clean Up

| Directory | Items / Size | Current State | Planned Action |
| :--- | :---: | :--- | :--- |
| **`05_papers_fulltext/`** | 288 PDFs (1.54 GB) | Core frozen full-text PDF repository | Verify PDF integrity & presence |
| **`06_analysis/`** | 687 files (25.3 MB) | Live `scripts/` & `outputs/` vs legacy `output/` (singular) | Move legacy `output/` to `_ARCHIVE/` |
| **`07_manuscript/`** | 37 files (3.5 MB) | Live V2 manuscript vs legacy V1 / submitted | Archive legacy drafts, retain V2 |
| **`08_docs/`** | 10 files (40 KB) | Live PRISMA & extraction specifications | Keep and cross-reference |
| **`09_prompts/`** | 1 file (<1 MB) | Legacy PDCA prompt | Move to `_ARCHIVE/` |
| **`10_validation/`** | 8 files (260 KB) | Legacy 171-paper validation set | Move to `_ARCHIVE/` |
| **`supplementary/`** | 8 files (160 KB) | Legacy S1–S8 snapshots | Move to `_ARCHIVE/` |
| **`_AUDIT/`** | 55 files (350 KB) | Live audit ledger and batch reports | Clean up stray scratch scripts |
| **`_MANUAL/`** | 291 files (1.5 MB) | **FROZEN manual extraction evidence base** | Preserve and lock |
| **`_PROJECT/`** | 7 files (40 KB) | Governance & master prompts | Update and maintain |
| **47 `_QUARANTINE_*`** | ~17,800 files (~180 MB) | Cluttering the root directory | Consolidate into `_ARCHIVE/quarantines/` |
