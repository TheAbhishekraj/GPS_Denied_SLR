# Systematic Literature Review: Autonomous Navigation & Localization in GNSS-Denied Environments

![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue.svg)
![Screening Progress](https://img.shields.io/badge/Screening-100%25%20Complete-brightgreen.svg)
![Included Papers](https://img.shields.io/badge/Included%20Papers-657-success.svg)
![Excluded Papers](https://img.shields.io/badge/Excluded%20Papers-39-important.svg)

A systematic, reproducible literature review (SLR) focusing on multi-sensor fusion, visual-inertial state estimation, LiDAR SLAM, radio-frequency localization, and learning-based navigation for uncrewed aerial (UAV), ground (UGV), and surface (USV) vehicles operating in satellite-denied or degraded environments.

---

## 📌 Executive Summary & PRISMA Metrics

| Metric | Value | Description / Source |
| :--- | :--- | :--- |
| **Initial Search Records** | **2,000** | IEEE Xplore (1,000) + Scopus (1,000) (2010–2026) |
| **Deduplicated Dataset** | **696** | 1,304 duplicate records removed via DOI & Fuzzy Title Matching |
| **Title/Abstract Screened**| **696 / 696 (100%)** | AI-assisted screening with validated JSON schemas |
| **Included Papers** | **657 (94.4%)** | Primary empirical studies meeting all 6 inclusion criteria |
| **Excluded Papers** | **39 (5.6%)** | Excluded literature reviews, GNSS-centric, or non-empirical work |
| **Repository Status** | **Phase 5 Complete**| Ready for Phase 6 (Data Extraction Prompt Generation) |

---

## 📁 Repository Structure

```
GPS_Denied_SLR/
├── 00_scope/                  # SLR Research protocol, inclusion/exclusion criteria, & scoping docs
├── 01_data_raw/              # Raw CSV database exports (IEEE Xplore & Scopus)
├── 02_data_processed/        # Cleaned datasets (`deduplicated.csv`, `screened_included.csv`, `screened_excluded.csv`)
├── 03_prompts/               # AI prompts (`screening_prompts/`, `extraction_prompts/`)
├── 04_ai_responses/          # Structured JSON outputs (`screening/resp_*.json`, `extraction/`)
├── 05_papers_fulltext/       # Downloaded full-text PDFs for Core papers
├── 06_analysis/              # Python data analysis scripts and output figures
│   ├── output/figures/       # High-resolution (300 DPI) publication figures
│   └── scripts/              # Pipeline execution scripts (01 through 06)
├── 07_manuscript/            # PRISMA 2020 SLR manuscript drafts & LaTeX source
├── 08_docs/                  # Project documentation & backup snapshots
├── check_screening_progress.py# Verification script for AI screening completion
├── MASTER_WORKFLOW_TRACKER.md# Real-time workflow tracker
└── REMAINING_PHASES_AND_VERIFICATION_GUIDE.md # Execution and verification guide for Phases 6–10
```

---

## ⚙️ Workflow Pipeline & Phase Overview

### Completed Phases
- **Phase 1: Project Setup & Research Protocol** ✅
  Established directory structure, Python virtual environment, and 6 inclusion / 9 exclusion criteria.
- **Phase 2: Database Searches** ✅
  Retrieved 1,000 records from IEEE Xplore and 1,000 records from Scopus (2010–2026).
- **Phase 3: Deduplication** ✅
  Applied automated DOI exact matching and Levenshtein title fuzzy matching (`01_deduplicate.py`), reducing 2,000 records to 696 unique papers.
- **Phase 4: Prompt Generation** ✅
  Generated 696 structured screening prompt files (`02_generate_prompts.py`).
- **Phase 5: Title/Abstract Screening** ✅
  Screened all 696 papers, outputting JSON response files (`04_ai_responses/screening/resp_*.json`) and parsed master lists (`03_parse_screening.py`).

### Pending Phases (Detailed in `REMAINING_PHASES_AND_VERIFICATION_GUIDE.md`)
- **Phase 6**: Extraction Prompt Generation for 657 Included Papers (`04_generate_extraction_prompts.py`)
- **Phase 7**: Data Extraction & Master Database Aggregation (`05_parse_extraction.py`)
- **Phase 8**: Citation Prioritization & PDF Retrieval (`core_papers.csv`)
- **Phase 9**: Publication Figure Generation (`06_generate_figures.py`)
- **Phase 10**: SLR Manuscript Preparation (`07_manuscript/`)

---

## 🚀 Quick Start & Execution Commands

### Environment Setup
```bash
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Reproduce Data Processing & Verification

1. **Verify Screening Progress**:
   ```bash
   python check_screening_progress.py
   ```

2. **Parse AI Screening Responses**:
   ```bash
   python 06_analysis/scripts/03_parse_screening.py
   ```

3. **Generate Data Extraction Prompts (Phase 6)**:
   ```bash
   python 06_analysis/scripts/04_generate_extraction_prompts.py
   ```

4. **Aggregate Extracted Master Database (Phase 7)**:
   ```bash
   python 06_analysis/scripts/05_parse_extraction.py
   ```

5. **Generate Publication Figures (Phase 9)**:
   ```bash
   python 06_analysis/scripts/06_generate_figures.py
   ```

---

## 📜 Citation & License

If using this dataset, prompt framework, or analysis scripts, please cite:

```bibtex
@misc{gps_denied_slr_2026,
  author = {Abhishek Raj},
  title = {Systematic Literature Review: Autonomous Navigation and Localization in GNSS-Denied Environments},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/TheAbhishekraj/GPS_Denied_SLR}}
}
```
