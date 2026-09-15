# Systematic Literature Review: Autonomous Navigation and Localization for UAVs in GPS-Denied Environments

![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue.svg)
![PRISMA 2020](https://img.shields.io/badge/standard-PRISMA%202020-orange.svg)
![Deduplicated](https://img.shields.io/badge/Unique%20Records-1%2C719-blue.svg)
![Included Papers](https://img.shields.io/badge/Included%20Studies-1%2C692-success.svg)
![Extracted Rows](https://img.shields.io/badge/Extracted%20Master-1%2C700-brightgreen.svg)
![Status](https://img.shields.io/badge/Submission-Ready%20(IEEEtran)-blueviolet.svg)

A systematic, reproducible literature review (SLR) compliant with PRISMA 2020 guidelines, synthesizing **1,692 peer-reviewed empirical studies** across 2010–2026 from IEEE Xplore and Elsevier Scopus. The review focuses on multi-sensor fusion, visual-inertial odometry (VIO), LiDAR SLAM, radio-frequency positioning, and hybrid learning-based architectures for uncrewed aerial vehicles (UAVs) operating in satellite-denied or degraded environments.

---

## 📌 Executive Summary & PRISMA 2020 Flow

```
   [Identification]   2,000 Initial Records (IEEE Xplore: 1,000 | Scopus: 1,000)
                              │
                              ▼
   [Deduplication]    1,719 Unique Records (281 duplicates removed, 14.1%)
                              │
                              ▼
   [Screening]        1,692 Included Studies (27 excluded: 8 theoretical, 11 GPS-augmented, 8 out-of-scope)
                              │
                              ▼
   [Extraction]       1,700 Extracted Rows (8 multi-experiment papers with dual evaluations)
```

| Metric | Canonical Value | Verification & Methodological Details |
| :--- | :--- | :--- |
| **Initial Search Records** | **2,000** | IEEE Xplore (1,000) + Scopus (1,000), 2010–2026 (`01_data_raw/`) |
| **Deduplicated Records** | **1,719** | Exact DOI + Levenshtein fuzzy title matching; 281 removed (14.1%) (`02_data_processed/deduplicated_master.csv`) |
| **Screened Included** | **1,692 (98.4%)** | Peer-reviewed empirical UAV localization studies (`04_ai_responses/screening_results.jsonl`) |
| **Screened Excluded** | **27 (1.6%)** | 8 theoretical surveys + 11 GPS-augmented + 8 out-of-scope (`02_data_processed/screening_audit.csv`) |
| **Extracted Master Rows** | **1,700** | Structured schema across 10 methods, 13 sensors, 7 environments (`02_data_processed/extracted_master.csv`) |
| **Multi-Experiment Papers**| **8** | Documented in `02_data_processed/EXTRACTION_NOTES.md` |
| **Publication Figures** | **9 (300 DPI)** | All >= 2000 px wide, colorblind-safe in `06_analysis/output/figures_v2/` |
| **Manuscript Package** | **Complete** | Markdown draft v2 + IEEEtran LaTeX (`07_manuscript/GPS_Denied_SLR_IEEE.tex`) |

---

## 🔬 Core Empirical Findings

1. **F1: Universal Inertial Substrate (IMU Ubiquity)**
   - The Inertial Measurement Unit (IMU) appears in **78.4% (1,332 / 1,700)** of all extracted papers. GPS-denied navigation has fundamentally converged around bounding and correcting inertial dead-reckoning drift.
2. **F2: Adversarial & EW Dominance**
   - Active Electronic Warfare (EW), GPS jamming, and contested airspace represent the **largest single environment category (495 papers, 29.1%)**, exceeding purely indoor operations (339 papers, 19.9%).
3. **F3: Multi-Agent Deployment Gap**
   - While single-agent VIO and LiDAR SLAM exceed a 4:1 real-world to simulation validation ratio, Multi-Agent Collaborative SLAM exhibits the lowest field ratio in the corpus at **1.3:1 (14 real-world : 11 simulation)**, constrained by communication dropouts and distributed compute burdens.

---

## 📁 Repository Structure

```
GPS_Denied_SLR/
├── 00_scope/                  # SLR Research protocol, PICOC table, search strings, registration
│   ├── PROTOCOL.md            # RQ1-RQ4, PICOC, 6 inclusion + 4 exclusion criteria, quality checklist
│   ├── SEARCH_STRINGS.md      # Verbatim IEEE Xplore and Scopus queries
│   └── REGISTRATION.md        # Protocol registration disclosure (unregistered + justification)
├── 01_data_raw/               # Canonical raw search data & logs
│   ├── ieee_xplore_raw.csv    # 1,000 raw IEEE records (canonical 8-column schema)
│   ├── scopus_raw.csv         # 1,000 raw Scopus records (canonical 8-column schema)
│   └── SEARCH_LOG.md          # Search execution details and parameters
├── 02_data_processed/         # Audited datasets & synthesis tables
│   ├── deduplicated_master.csv# 1,719 clean, unique records
│   ├── dedup_log.csv          # 281 removed duplicates with explicit match reasons
│   ├── DEDUP_REPORT.md        # Reproducible deduplication methodology and audit
│   ├── screening_audit.csv    # The 27 excluded papers with classified reason codes
│   ├── screening_summary.csv  # Screening breakdown counts and percentages
│   ├── extracted_master.csv   # 1,700 extracted rows with complete taxonomy
│   └── EXTRACTION_NOTES.md    # Documentation for the 8 double-extracted papers
├── 03_prompts/                # AI screening and data extraction prompts
│   ├── screening_prompts.jsonl# 1,719 screening prompt records
│   └── extraction_prompts.jsonl# 1,692 extraction prompt records (17 mandatory fields)
├── 04_ai_responses/           # AI response records
│   └── screening_results.jsonl# 1,719 screening decisions
├── 05_papers_fulltext/        # Full-text PDFs of core papers (gitignored)
├── 06_analysis/               # Analysis scripts, synthesis tables, and figures
│   ├── output/figures_v2/     # 9 publication-grade figures (300 DPI, colorblind-safe)
│   ├── output/tables/         # Machine-readable source CSVs for all 9 figures & matrices
│   ├── scripts/99_verify_all.py# End-to-end repository verification script
│   └── SYNTHESIS.md           # Quantitative synthesis with exact numerators/denominators
├── 07_manuscript/             # Submission manuscript and LaTeX package
│   ├── GPS_Denied_SLR_Manuscript_v2.md # Full Markdown manuscript draft (7 numbered sections)
│   ├── GPS_Denied_SLR_IEEE.tex# IEEEtran journal class submission package
│   ├── references.bib         # BibTeX references matching all manuscript citations
│   ├── perf_tables.md         # Quantitative ATE, SWaP-C, and Sim-to-Real benchmark tables
│   └── BUILD.md               # Exact pdflatex and bibtex compilation instructions
├── 08_docs/                   # Quality documentation & submission prep
│   ├── FOLDER_GUIDE.md        # Description of all repository folders
│   ├── SUBMISSION_CHECKLIST.md# 8-gate pre-flight submission audit
│   ├── COVER_LETTER.md        # Cover letter to IEEE T-RO Editor-in-Chief
│   └── ARXIV_METADATA.md      # arXiv cs.RO / cs.CV preprint metadata
└── supplementary/             # Formal supplementary artifacts (S1 through S5)
    ├── S1_prisma_checklist.md # Complete 27-item PRISMA 2020 compliance audit
    ├── S2_search_queries.txt  # Full search queries for both databases
    ├── S3_quality_scores.csv  # 8-item quality score for all 1,692 included papers
    ├── S4_full_reference_list.bib # Complete references
    └── S5_extracted_master_snapshot.csv # Frozen snapshot of extracted_master.csv
```

---

## 🚀 Quick Start & Verification

To verify complete repository consistency against canonical numbers:

```bash
python 06_analysis/scripts/99_verify_all.py
```

Expected output:
```
=======================================================
     GPS_Denied_SLR FINAL REPOSITORY VERIFICATION      
=======================================================
[PASS] raw=2000           actual=2000  expected=2000
[PASS] dedup=1719         actual=1719  expected=1719
[PASS] dedup_log=281      actual=281  expected=281
[PASS] excluded=27        actual=27  expected=27
[PASS] extracted=1700     actual=1700  expected=1700
[PASS] IMU~78%            actual=0.784  expected=0.78
[PASS] EW=495             actual=495  expected=495
[PASS] MA_Real=14         actual=14  expected=14
[PASS] MA_Sim=11          actual=11  expected=11
[PASS] methods=10         actual=10  expected=10
=======================================================
>>> ALL VERIFICATION CHECKS PASSED: REPOSITORY IS SUBMISSION-READY <<<
```

---

## 📜 Citation & Attribution

```bibtex
@article{Raj2026GPSDeniedSLR,
  author    = {Abhishek Raj},
  title     = {Autonomous Navigation and Localization for Unmanned Aerial Vehicles in {GPS}-Denied Environments: A Systematic Literature Review},
  journal   = {IEEE Transactions on Robotics (Submitted)},
  year      = {2026},
  url       = {https://github.com/TheAbhishekraj/GPS_Denied_SLR}
}
```
