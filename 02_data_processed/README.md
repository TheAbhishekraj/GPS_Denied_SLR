# 02_data_processed — PRISMA 2020 Data Processing & Evidence Repository

This directory contains the core processed datasets, screening registers, and batch extraction manifests for the systematic literature review:  
**"GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)"**.

---

## 1. Directory Structure

```text
02_data_processed/
├── README.md                      # Directory guide, schema catalog, and cryptographic manifest (this file)
├── MASTER_EVIDENCE.csv            # LIVE: Final 279-paper multi-sensor extraction master (28 columns)
├── deduplicated_master.csv        # FROZEN: 1,716 unique records after cross-database deduplication
├── dedup_log.csv                  # FROZEN: 280 dropped duplicate records log
├── DEDUP_REPORT.md                # Deduplication audit report and metric breakdown
├── DEDUP_VERIFY.md                # Verification checklist and SHA256 audit for deduplication
├── screened_included_v2.csv       # FROZEN: 636 candidate records passing preliminary screening
├── screening_results.csv          # FROZEN: 291 records evaluated against full-text eligibility (285 INCLUDE, 6 EXCLUDE)
├── screening_spreadsheet.xlsx     # Working spreadsheet for screening evaluations
├── pdf_removal_log.csv            # Audit of 3 byte-identical duplicate PDFs excluded from corpus
└── evidence_batches/              # Batch extraction processing directory (28 batches)
    ├── BATCH_B01.csv ... BATCH_B28.csv       # 28 batch CSV tables (279 rows total)
    └── BATCH_B01_pages/ ... BATCH_B28_pages/ # Full-text page extraction snippets per batch
```

---

## 2. File Catalog & Cryptographic Manifest

All active core files have been audited and cryptographically verified:

| File | Type | Data Rows | Size | SHA256 Hash | Status |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **`MASTER_EVIDENCE.csv`** | CSV | **279** | 134,087 B | `15B26C59DFAAAD0A62A3D473AC7EB4DFC0491A89B7B6D4D5CF78BB8FB512B2C6` | **LIVE MASTER** |
| **`deduplicated_master.csv`** | CSV | **1,716** | 2,509,495 B | `A648930848EED1950A602EA5FA2F739CFDDB1C2BB1289F86B810211DB3D8649A` | **FROZEN ANCHOR** |
| **`dedup_log.csv`** | CSV | **280** | 34,801 B | `F725F1A367FB47DE5969FFAF3EB4615B600F4937DC16F3DBD5A7129097C24F04` | **FROZEN AUDIT** |
| **`DEDUP_REPORT.md`** | Markdown | — | 2,309 B | `093992EB3364DAB9C14080524ECAA57D1B2640134D3330D72D1BF7A27AB74798` | Audit Log |
| **`DEDUP_VERIFY.md`** | Markdown | — | 975 B | `CD9AAA38722E6A5BE2BD9244807C814908FDF287D5D4A65E21E64D7A73A8598E` | Audit Log |
| **`screened_included_v2.csv`** | CSV | **636** | 1,081,633 B | `CD1B38745FF653BE3E23C62371B87A12861261BDC057F4F313645C4A79E93CED` | **FROZEN ANCHOR** |
| **`screening_results.csv`** | CSV | **291** | 504,947 B | `86DADC842AA590B03C0F5145FFCA5340800CB41AE505BC7AD1488CB40648F6D7` | **FROZEN ANCHOR** |
| **`pdf_removal_log.csv`** | CSV | **3** | 285 B | `A9CFF5BCAF9A69B510CE5189FFACD5440CEDA60793946E67A23DFD9A8E30972D` | Audit Log |
| **`screening_spreadsheet.xlsx`** | XLSX | — | 2,279,257 B | `9C7F2E281F472210EC2BE6571C3A37AA12338DB2C1A04B4072D67850C7935CB8` | Working Data |

---

## 3. PRISMA 2020 Data Flow in this Directory

The files in this directory represent the quantitative stages of the PRISMA 2020 flow:

```
┌────────────────────────────────────────────────────────┐
│ Raw Harvest (01_data_raw/): 2,000 Records              │
│ (1,000 IEEE Xplore + 1,000 Scopus)                     │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ [Automated Deduplication]
┌────────────────────────────────────────────────────────┐
│ deduplicated_master.csv: 1,716 Unique Records          │
│ (280 Duplicate records documented in dedup_log.csv)    │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ [Title & Abstract Screening]
┌────────────────────────────────────────────────────────┐
│ screened_included_v2.csv: 636 Candidate Records        │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ [Full-Text Eligibility Screening]
┌────────────────────────────────────────────────────────┐
│ screening_results.csv: 291 Assessed Records            │
│ ├── 285 INCLUDED                                       │
│ └── 6 EXCLUDED (E1/E2/E4/E7)                           │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼ [Corpus Refinement & Deduplication]
┌────────────────────────────────────────────────────────┐
│ Corpus Denominator: 279 in-corpus papers               │
│ (285 Include - 6 Deferred records = 279 Final Corpus)  │
│ Stored in MASTER_EVIDENCE.csv & evidence_batches/      │
└────────────────────────────────────────────────────────┘
```

---

## 4. `evidence_batches/` Details

To ensure scalable, reproducible extraction without memory overruns, the 279 in-corpus papers are divided into **28 sequential batches**:
- **Batches B01 to B27:** Exactly 10 papers each (27 × 10 = 270 papers).
- **Batch B28:** Exactly 9 papers (270 + 9 = 279 papers).
- **Page Extraction Folders (`BATCH_BXX_pages/`):** Full-text page extractions corresponding to each paper in the batch, used by extraction scripts and human spot-check validators.

---

## 5. Archive History (Moved Legacy Files)

On 2026-09-27, the following 8 obsolete or conflicting Generation-1 (pre-reset) files were safely relocated using `git mv` to `_ARCHIVE/legacy_02_data_processed/` to preserve a clean PRISMA 2020 workspace:

1. `summary.txt` (Contained obsolete 2026-09-06 test numbers contradicting frozen deduplication).
2. `MASTER_EVIDENCE_V1.xlsx` (Pre-reset Generation-1 spreadsheet).
3. `EXTRACTION_NOTES.md` (Legacy notes citing deprecated 1,700-row extraction model).
4. `EXTRACTION_NOTES_v2.md` (Legacy notes citing 171-paper extraction subset).
5. `V1_SCOPE_IDS.txt` (Obsolete Generation-1 scope ID list).
6. `PENDING_MASTER_EXTENSION_IDS.txt` (Obsolete 121-paper extension tracking list).
7. `retrieval_log.csv` (Empty 0-row header template).
8. `pending_list.csv` (Empty 0-row header template).
