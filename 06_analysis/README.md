# 06_analysis — Quantitative Analysis & Synthesis Pipeline

This directory holds the active **analysis scripts** and **Phase 7 synthesis output tables** for the systematic literature review:  
**"GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)"**.

---

## 1. Directory Structure

```text
06_analysis/
├── README.md                      # Directory manifest and script guide (this file)
├── outputs/                       # Active Generation-2 Phase 7 synthesis tables
│   ├── evidence_matrix.csv        # 279 rows: Evidence matrix (byte-identical to MASTER_EVIDENCE.csv)
│   ├── inference_table.csv        # 279 rows: Structured inference and synthesis table
│   └── taxonomy_distribution.csv  # 4 rows: Core vs. adjacent taxonomy distributions
└── scripts/                       # Active pipeline execution scripts
    ├── 01_dedup.py                # Automated DOI and fuzzy-title cross-database deduplication
    ├── 02_screen.py               # Two-stage screening evaluator
    ├── merge_batch.py             # Phase 6 batch merger with SHA256 integrity checks
    ├── pdf_text.py                # PDF full-text extraction utility
    ├── phase4_batch_extract.py    # Batch text extraction processor
    └── validate_master.py         # Standard library CSV schema and integrity validator
```

---

## 2. Active Output Tables Catalog

All active output files in `06_analysis/outputs/` have been audited and verified:

| File Link | Rows | Size | SHA256 Hash | Role / Status |
| :--- | :---: | :---: | :--- | :--- |
| [`06_analysis/outputs/evidence_matrix.csv`](file:///e:/GPS_Denied_SLR/06_analysis/outputs/evidence_matrix.csv) | **279** | 134,087 B | `15B26C59DFAAAD0A62A3D473AC7EB4DFC0491A89B7B6D4D5CF78BB8FB512B2C6` | Evidence Matrix (matches `MASTER_EVIDENCE.csv`) |
| [`06_analysis/outputs/inference_table.csv`](file:///e:/GPS_Denied_SLR/06_analysis/outputs/inference_table.csv) | **279** | 64,824 B | `2344A340ED06F9DDDFBCEAB7D2D3D3262CBA73AFA927C72B9331359DBBD4C842` | Inference Synthesis Table |
| [`06_analysis/outputs/taxonomy_distribution.csv`](file:///e:/GPS_Denied_SLR/06_analysis/outputs/taxonomy_distribution.csv) | **4** | 182 B | `954898BE6434E398FD477FDC3EB70C8BF6DBF38AA3902CC6AE8D064A89B7B122` | Taxonomy Distribution Breakdown |

---

## 3. Pipeline Scripts Catalog

| Script | Purpose |
| :--- | :--- |
| [`scripts/01_dedup.py`](file:///e:/GPS_Denied_SLR/06_analysis/scripts/01_dedup.py) | Executes automated deduplication across IEEE Xplore and Scopus raw exports. |
| [`scripts/02_screen.py`](file:///e:/GPS_Denied_SLR/06_analysis/scripts/02_screen.py) | Implements eligibility screening evaluation against I1–I7 and E1–E10 criteria. |
| [`scripts/merge_batch.py`](file:///e:/GPS_Denied_SLR/06_analysis/scripts/merge_batch.py) | Merges sequential batch CSVs into `MASTER_EVIDENCE.csv` with strict cryptographic pre-merge checks. |
| [`scripts/pdf_text.py`](file:///e:/GPS_Denied_SLR/06_analysis/scripts/pdf_text.py) | Extracts and indexes full-text sections from local PDF files. |
| [`scripts/phase4_batch_extract.py`](file:///e:/GPS_Denied_SLR/06_analysis/scripts/phase4_batch_extract.py) | Generates batch CSV manifests and source page text snippets. |
| [`scripts/validate_master.py`](file:///e:/GPS_Denied_SLR/06_analysis/scripts/validate_master.py) | Phase 5/6 exit-gate validator enforcing zero-fabrication and schema compliance. |

*(Note: `figures.py` specification is approved in `_AUDIT/RULE9_SPEC_figures_py.md` and will be implemented during Task T5).*

---

## 4. Archive History (Legacy Gen-1 Relocation)

On 2026-09-27, the following obsolete Generation-1 files were moved to [`_ARCHIVE/legacy_06_analysis/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_06_analysis/) to eliminate the confusion between singular `output/` and live plural `outputs/`:
* `output/` (singular, 673 files: legacy `figures_v1/`, `figures_v2/`, old tables, workbooks)
* `audit/` (3 files: `MANUAL_REVIEW.md`, `V1_audit_*.csv/json` from old 171-paper run)
* `SYNTHESIS.md` & `SYNTHESIS_v2.md` (citing deprecated 1,700-row pre-reset numbers)
