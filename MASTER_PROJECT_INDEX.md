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
| **Full-Text PDF Corpus** | **288** | [`05_papers_fulltext/`](file:///e:/GPS_Denied_SLR/05_papers_fulltext/) (288 PDFs on disk, 1.50 GB) | **FROZEN** |
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

### 📁 `05_papers_fulltext/` — Full-Text PDF Corpus
* **Purpose:** Complete collection of full-text research paper PDFs corresponding to the screening corpus.
* **Audit State:** Audited on 2026-09-27. Stale empty directory removed. Manifest added.

| File Link | Items | Size | SHA256 Hash | Status |
| :--- | :---: | :---: | :--- | :--- |
| [`05_papers_fulltext/README.md`](file:///e:/GPS_Denied_SLR/05_papers_fulltext/README.md) | 22 lines | 1.15 KB | `F4DE108422A1E2752178229F84B0661159C2D32EC3628F50B6AE21B9720BA78D` | **Directory Manifest** |
| [`05_papers_fulltext/`](file:///e:/GPS_Denied_SLR/05_papers_fulltext/) | **288** PDFs | **1.50 GB** | All 288 PDFs verified present on local disk | **FROZEN PDF CORPUS** |

---

### 📁 `06_analysis/` — Analysis Scripts & Phase 7 Synthesis Tables
* **Purpose:** Pipeline analysis scripts and quantitative output tables for PRISMA 2020 synthesis.
* **Audit State:** Audited on 2026-09-27. Moved 673 legacy output files and pre-reset synthesis drafts to archive. Manifest added.

| File Link | Items / Lines | Size | SHA256 Hash | Status |
| :--- | :---: | :---: | :--- | :--- |
| [`06_analysis/README.md`](file:///e:/GPS_Denied_SLR/06_analysis/README.md) | 55 lines | 3.53 KB | `DFF99A156527C6392EBA8DF0B7E8CE129AE9F0580A586B90CCE86E6DDF2D6C8E` | **Directory Manifest** |
| [`06_analysis/outputs/evidence_matrix.csv`](file:///e:/GPS_Denied_SLR/06_analysis/outputs/evidence_matrix.csv) | **279** rows | 134 KB | `15B26C59DFAAAD0A62A3D473AC7EB4DFC0491A89B7B6D4D5CF78BB8FB512B2C6` | Evidence Matrix (Live) |
| [`06_analysis/outputs/inference_table.csv`](file:///e:/GPS_Denied_SLR/06_analysis/outputs/inference_table.csv) | **279** rows | 64.8 KB | `2344A340ED06F9DDDFBCEAB7D2D3D3262CBA73AFA927C72B9331359DBBD4C842` | Inference Synthesis Table |
| [`06_analysis/outputs/taxonomy_distribution.csv`](file:///e:/GPS_Denied_SLR/06_analysis/outputs/taxonomy_distribution.csv) | **4** rows | 182 B | `954898BE6434E398FD477FDC3EB70C8BF6DBF38AA3902CC6AE8D064A89B7B122` | Taxonomy Breakdown |
| [`06_analysis/scripts/`](file:///e:/GPS_Denied_SLR/06_analysis/scripts/) | **6** scripts | ~30 KB | 6 core Python scripts (`01_dedup.py`, `merge_batch.py`, etc.) | **Pipeline Scripts** |

### 📁 `07_manuscript/` — Manuscript Drafts, Tables, and Submission Files
* **Purpose:** Live Generation-2 manuscript drafts, performance tables, IEEE LaTeX template, and submission checklists.
* **Audit State:** Audited on 2026-09-27. Relocated 24 legacy Generation-1 files (`submitted/`, `V1_171.*`, `V1_291.*`, old figures/tables) to `_ARCHIVE/legacy_07_manuscript/`.

| File Link | Size | SHA256 Hash | Role / Status |
| :--- | :---: | :--- | :--- |
| [`07_manuscript/README.md`](file:///e:/GPS_Denied_SLR/07_manuscript/README.md) | 2.5 KB | `CDF8D74E21A2214FC0A1C5F6787C4B290FE4F4DA185EC2978F90DBAC5F25AC3E` | **Directory Manifest** |
| [`07_manuscript/MANUSCRIPT_V2.md`](file:///e:/GPS_Denied_SLR/07_manuscript/MANUSCRIPT_V2.md) | 7.3 KB | `542BE0ED72D6CED9AA58FE1D0C95ADA4015AABAF058B2DC169EB313D56D4C391` | **Canonical Active Draft** (13 unresolved markers) |
| [`07_manuscript/GPS_Denied_SLR_Manuscript_v2.md`](file:///e:/GPS_Denied_SLR/07_manuscript/GPS_Denied_SLR_Manuscript_v2.md) | 10.8 KB | `7423A55018B58F6EF77724110323BFEBFE6520E8D342AD93586341AE6C12FCCB` | Manuscript text draft v2 |
| [`07_manuscript/GPS_Denied_SLR_Manuscript_v3.md`](file:///e:/GPS_Denied_SLR/07_manuscript/GPS_Denied_SLR_Manuscript_v3.md) | 6.5 KB | `B7C6A3F64023EBEE88A3CFB241F3E0205DCD20013E62E38C389F77547DCF632F` | Manuscript text draft v3 |
| [`07_manuscript/GPS_Denied_SLR_IEEE_v2.tex`](file:///e:/GPS_Denied_SLR/07_manuscript/GPS_Denied_SLR_IEEE_v2.tex) | 3.2 KB | `02CF0DE1CFD13C29BF4B056139A3E638B0CD9D5C4070AC0ACB20B6A90B8AD680` | IEEE-format LaTeX template |
| [`07_manuscript/references.bib`](file:///e:/GPS_Denied_SLR/07_manuscript/references.bib) | 4.6 KB | `19F4ED3311010EAF3B10970FEE8216ED5BBA1B92791284DCA1843D0C86459BE3` | Master BibTeX bibliography |
| [`07_manuscript/perf_summary.csv`](file:///e:/GPS_Denied_SLR/07_manuscript/perf_summary.csv) | 921 B | `9DAECB658F8F3A6856AFFC7BD77C35BCF009C0DF0E74B8F2A5D7A27F97DE5222` | Extracted performance summary |
| [`07_manuscript/perf_tables.md`](file:///e:/GPS_Denied_SLR/07_manuscript/perf_tables.md) | 958 B | `26CA25F0F245C2A156067CF18DE4A2D760D9689EB1E1FB8C4112888C82CCAD05` | Performance tables |
| [`07_manuscript/SUBMISSION_CHECKLIST.md`](file:///e:/GPS_Denied_SLR/07_manuscript/SUBMISSION_CHECKLIST.md) | 3.2 KB | `DB018A93D1AA6CCCC5531819F75FF10C6B79F235A9EB6D31E53459413DBF68FD` | Submission checklist |
| [`07_manuscript/BUILD.md`](file:///e:/GPS_Denied_SLR/07_manuscript/BUILD.md) | 248 B | `E321505B20F861E3EACF34BECA4B9CE481217C8681A9D7996B94E20584A8D901` | Build guide |

### 📁 `08_docs/` — PRISMA 2020 Protocol, Extraction Schema & Methodology Specifications
* **Purpose:** Core normative methodology specifications, 28-column extraction schema, and PRISMA 2020 checklists.
* **Audit State:** Audited on 2026-09-27. All 10 active specification documents verified and cataloged. Manifest added.

| File Link | Size | SHA256 Hash | Role / Status |
| :--- | :---: | :--- | :--- |
| [`08_docs/README.md`](file:///e:/GPS_Denied_SLR/08_docs/README.md) | 2.8 KB | `F14D8BF2D867E926186DDEB16BFAC2B3F9560ACAFCFDA4ED68DF51CA31EA0E1A` | **Directory Manifest** |
| [`08_docs/ANCHOR_FREEZE_20260919.md`](file:///e:/GPS_Denied_SLR/08_docs/ANCHOR_FREEZE_20260919.md) | 2.1 KB | `D165BB14A6C932A74479A0BFA2C4477694A13CFA80AD6CC382FF4DB43A91607C` | Anchor Freeze Hashes |
| [`08_docs/EXTRACTION_RULES.md`](file:///e:/GPS_Denied_SLR/08_docs/EXTRACTION_RULES.md) | 1.6 KB | `684ED59DB69C4ACA29822B75374163499880BC885DFD2A4CDD4B2B81DAC14C56` | Rules E1–E6: Verbatim extraction rules |
| [`08_docs/EXTRACTION_SCHEMA_v1.md`](file:///e:/GPS_Denied_SLR/08_docs/EXTRACTION_SCHEMA_v1.md) | 3.7 KB | `876D42D237AFC21BB9B07D53552813DFBC872AC42A4E16B294ADF35B36E4A81B` | 28-Column Master Evidence Schema |
| [`08_docs/EXTRACTION_SOP.md`](file:///e:/GPS_Denied_SLR/08_docs/EXTRACTION_SOP.md) | 2.3 KB | `AF916B13FC9B4EF9C8C8C383734D50D3462AA14180E86C8D10065379B7D44D8A` | Extraction Standard Operating Procedure |
| [`08_docs/MANUSCRIPT_SPEC.md`](file:///e:/GPS_Denied_SLR/08_docs/MANUSCRIPT_SPEC.md) | 2.1 KB | `FEA98930115ABD7FE039DEB44DF9EFA99E083D7332DBD933625C556A157D7B5B` | Manuscript Tables T1–T8 & Figures F1–F9 Spec |
| [`08_docs/NUMBER_TRACE.md`](file:///e:/GPS_Denied_SLR/08_docs/NUMBER_TRACE.md) | 3.9 KB | `B297EFC4EA60D98561A5B09952637EAEB2E8BCF3C8E66557FA56609725F9ABA5` | Cryptographic Number Trace |
| [`08_docs/PRISMA_CHECKLIST.md`](file:///e:/GPS_Denied_SLR/08_docs/PRISMA_CHECKLIST.md) | 16.0 KB | `AAA45B5A1CA2AC68666F8688CB9258CD5D875B93852D1699F9A834FA02DC6C36` | 27-Item PRISMA 2020 Compliance Checklist |
| [`08_docs/SCREENING_INDEPENDENCE.md`](file:///e:/GPS_Denied_SLR/08_docs/SCREENING_INDEPENDENCE.md) | 2.4 KB | `2266FB177877B395408BA5A3C40892F20BC973BF74A392996B41894960EFD5D3` | Reviewer Screening Independence Protocol |
| [`08_docs/SYNTHESIS_METHOD.md`](file:///e:/GPS_Denied_SLR/08_docs/SYNTHESIS_METHOD.md) | 2.3 KB | `8B4867009FABD5F28481C583602A6E0A576D88254E94F75B37110B783305DB09` | PRISMA 2020 Synthesis Methodology |
| [`08_docs/SYNTHESIS_REPORT.md`](file:///e:/GPS_Denied_SLR/08_docs/SYNTHESIS_REPORT.md) | 3.7 KB | `1E4DC5A86C23C1FA9A90546D228CAED9BEA6D554E7F766BD600B84E6E788AAD5` | Phase 7 Synthesis Report (279 papers) |

### 📁 `09_prompts/` — Execution Prompts Directory
* **Purpose:** Directory for operational prompts. (Active execution prompts are centrally located in `_PROJECT/`).
* **Audit State:** Audited on 2026-09-27. Relocated obsolete `PDCA_PHASE_1_VALIDATE.md` to `_ARCHIVE/legacy_09_prompts/`.

| File Link | Size | SHA256 Hash | Role / Status |
| :--- | :---: | :--- | :--- |
| [`09_prompts/README.md`](file:///e:/GPS_Denied_SLR/09_prompts/README.md) | 520 B | `3A820D5DAB0E8D067BF929DE62FACA8D23A7116AD34FD6B87FFA086CED07B085` | **Directory Manifest & Pointer to `_PROJECT/`** |

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
5. **[`_ARCHIVE/legacy_06_analysis/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_06_analysis/)** (678 items):
   - `output/` (singular, 673 files: legacy `figures_v1/`, `figures_v2/`, old tables, workbooks)
   - `audit/` (3 files: `MANUAL_REVIEW.md`, `V1_audit_*.csv/json` from old 171-paper run)
   - `SYNTHESIS.md` & `SYNTHESIS_v2.md` (citing deprecated 1,700-row pre-reset numbers)
6. **[`_ARCHIVE/legacy_07_manuscript/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_07_manuscript/)** (24 items):
   - `submitted/` directory (5 legacy files: `GPS_Denied_SLR_Manuscript_V1_291.*`, `figures_list_V1_291.md`, `tables_V1_291.md`)
   - `GPS_Denied_SLR_Manuscript_V1_171.*` (7 files: `.tex`, `.pdf`, `.md`, `.aux`, `.log`, and `_COMPLETE.*` variants)
   - `GPS_Denied_SLR_Manuscript_V1_291.*` (6 files: `.tex`, `.pdf`, `.md`, `.aux`, `.log`, `.out`)
   - `GPS_Denied_SLR_Manuscript_v1_171.md`
   - `GPS_Denied_SLR_Manuscript_v2.docx` (stale binary export)
   - `GPS_Denied_SLR_IEEE.tex` & `GPS_Denied_SLR_Manuscript.md` (unversioned legacy drafts)
   - `tables_V1.md`, `tables_V1_291.md`, `figures_list_V1.md`, `figures_list_V1_291.md`
7. **[`_ARCHIVE/legacy_09_prompts/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_09_prompts/)** (1 item):
   - `PDCA_PHASE_1_VALIDATE.md` (historical PDCA prompt referencing obsolete numbers)
8. **[`_ARCHIVE/legacy_10_validation/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_10_validation/)** (8 items):
   - `adjudicated.csv`, `extraction_validation_results.csv`, `extraction_validation_sample.csv`, `reviewer_A.csv`, `reviewer_B.csv`, `sample.csv`, `kappa_report.md`, `extraction_validation_report.md` (172-paper validation data from deprecated 1,700-row run)
9. **[`_ARCHIVE/legacy_supplementary/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_supplementary/)** (8 items):
   - `S1_prisma_checklist.md`, `S2_search_queries.txt`, `S3_quality_scores.csv` (172 rows), `S4_full_reference_list.bib`, `S5_extracted_master_snapshot_v2.csv` (172 rows), `S6_screening_criteria_v2.md`, `S7_human_validation_report.md`, `S8_extraction_validation_report.md`

---

## 4. Upcoming Folders to Review & Clean Up

| Directory | Items / Size | Current State | Planned Action |
| :--- | :---: | :--- | :--- |
| **`_AUDIT/`** | 55 files (350 KB) | Live audit ledger and batch reports | Clean up stray scratch scripts, add manifest |
| **`_MANUAL/`** | 291 files (1.5 MB) | **FROZEN manual extraction evidence base** | Preserve and lock |
| **`_PROJECT/`** | 7 files (40 KB) | Governance & master prompts | Update and maintain |
| **47 `_QUARANTINE_*`** | ~17,800 files (~180 MB) | Cluttering the root directory | Consolidate into `_ARCHIVE/quarantines/` |

