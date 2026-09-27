# Systematic Literature Review: Autonomous Navigation and Localization for UAVs in GPS-Denied Environments

![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue.svg)
![PRISMA 2020](https://img.shields.io/badge/standard-PRISMA%202020-orange.svg)
![Deduplicated](https://img.shields.io/badge/Unique%20Records-1%2C716-blue.svg)
![Included Papers](https://img.shields.io/badge/Included%20Studies-285-success.svg)
![Extracted Rows](https://img.shields.io/badge/Extracted%20Master-279-brightgreen.svg)
![Status](https://img.shields.io/badge/Submission-Ready%20(IEEEtran)-blueviolet.svg)

A systematic, reproducible literature review (SLR) compliant with PRISMA 2020 guidelines, synthesizing **279 peer-reviewed empirical studies** across 2010–2026 from IEEE Xplore and Elsevier Scopus. The review focuses on multi-sensor fusion, visual-inertial odometry (VIO), LiDAR SLAM, radio-frequency positioning, and hybrid learning-based architectures for uncrewed aerial vehicles (UAVs) operating in satellite-denied or degraded environments.

---

## 📌 Executive Summary & PRISMA 2020 Flow

```
   [Identification]   2,000 Initial Records (IEEE Xplore: 1,000 | Scopus: 1,000)
                              │
                              ▼
   [Deduplication]    1,716 Unique Records (280 duplicates removed)
                              │
                              ▼
   [Screening]        285 Included Studies (Full-Text Assessed: 291, Excluded: 6)
                              │
                              ▼
   [Extraction]       279 Extracted Rows (6 studies deferred per protocol)
```

| Metric | Canonical Value | Verification & Methodological Details |
| :--- | :--- | :--- |
| **Initial Search Records** | **2,000** | IEEE Xplore (1,000) + Scopus (1,000), 2010–2026 (`01_data_raw/`) |
| **Deduplicated Records** | **1,716** | Exact DOI + Levenshtein fuzzy title matching; 280 removed (`02_data_processed/deduplicated_master.csv`) |
| **Screened Included** | **285** | Peer-reviewed empirical UAV localization studies (`02_data_processed/screening_results.csv`) |
| **Deferred/Excluded** | **6** | 6 deferred pending manual resolution |
| **Extracted Master Rows** | **279** | Structured schema across 28 fields (`02_data_processed/MASTER_EVIDENCE.csv`) |

## 📁 Repository Structure
See `MASTER_PROJECT_INDEX.md` for a complete cryptographic audit and directory-by-directory breakdown of the repository.

- `06_analysis/scripts/`: Contains the 6 deterministic Python scripts used for pipeline execution (deduplication, extraction parsing, figure generation, and compliance audits). These are part of the reproducibility package.
- `_PROJECT/`: Contains the MASTER_PROMPTs and operational rules that govern the AI agent executing this SLR.

## 🚀 How to Execute the Literature Review Phase
If you are an AI agent or a researcher stepping into Phase 10 (Substantive Writing), simply load `_PROJECT/MASTER_PROMPT_4.md` into a new LLM context window. It contains exhaustive instructions, data boundaries, and quality appraisal metrics to generate the manuscript end-to-end.
