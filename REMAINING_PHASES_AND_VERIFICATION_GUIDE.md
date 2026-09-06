# GPS-Denied UAV Navigation SLR: Remaining Phases & Verification Guide

This document outlines the step-by-step roadmap for all remaining SLR phases (Phase 6 through Phase 10), including exact execution commands, input/output specifications, and automated verification scripts.

---

## 📊 Project Status Summary

| Phase | Description | Status | Output Artifact |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Project Setup & Protocol | ✅ Complete | Directory structure, protocol specs |
| **Phase 2** | Database Searches (IEEE & Scopus) | ✅ Complete | `01_data_raw/ieee_xplore.csv`, `scopus.csv` (2,000 papers) |
| **Phase 3** | Deduplication | ✅ Complete | `02_data_processed/deduplicated.csv` (696 unique papers) |
| **Phase 4** | Screening Prompt Generation | ✅ Complete | `03_prompts/screening_prompts/*.txt` (696 files) |
| **Phase 5** | Title/Abstract Screening & Parsing | ✅ Complete | `04_ai_responses/screening/resp_*.json` (696 files)<br>`02_data_processed/screened_included.csv` (657 included)<br>`02_data_processed/screened_excluded.csv` (39 excluded) |
| **Phase 6** | Extraction Prompt Generation | 🔜 Ready | `03_prompts/extraction_prompts/*.txt` (657 files) |
| **Phase 7** | Data Extraction & Database Creation | ⏳ Pending | `04_ai_responses/extraction/resp_*.json`<br>`02_data_processed/extracted_master.csv` |
| **Phase 8** | Citation Tier Selection & PDF Retrieval | ⏳ Pending | `02_data_processed/core_papers.csv`<br>`05_papers_fulltext/*.pdf` |
| **Phase 9** | Figure Generation & Data Analysis | ⏳ Pending | `06_analysis/output/figures/fig*.png` (6 figures) |
| **Phase 10**| SLR Manuscript Writing | ⏳ Pending | `07_manuscript/GPS_Denied_SLR_Manuscript.md` |

---

## 🚀 PHASE 6: Data Extraction Prompt Generation

### Goal
Generate structured data extraction prompts for each of the **657 INCLUDED papers** identified in Phase 5.

### Execution
Run the prompt generation script:
```bash
python E:\GPS_Denied_SLR\06_analysis\scripts\04_generate_extraction_prompts.py
```

### Inputs & Outputs
- **Input**: `E:\GPS_Denied_SLR\02_data_processed\screened_included.csv`
- **Output**: 657 text files in `E:\GPS_Denied_SLR\03_prompts\extraction_prompts\extraction_XXXXX_*.txt`

### Automated Verification Protocol
Run this snippet to verify prompt generation completion:
```python
import glob

prompts = glob.glob('E:/GPS_Denied_SLR/03_prompts/extraction_prompts/extraction_*.txt')
print(f"Extraction prompts found: {len(prompts)} / 657")
assert len(prompts) == 657, f"Expected 657 extraction prompts, but found {len(prompts)}"
print("✅ Phase 6 Verification Passed!")
```

---

## 🚀 PHASE 7: Structured Data Extraction & Parsing

### Goal
Extract technical taxonomies (platform types, environment classes, sensor suites, estimation algorithms, error metrics, datasets, application domains, and citation tiers) into JSON responses and aggregate into a master CSV database.

### Step-by-Step Procedure
1. **Process Extraction Prompts**:
   For each prompt in `03_prompts/extraction_prompts/`, generate structured JSON output and save to `04_ai_responses/extraction/resp_XXXXX.json`.
2. **Parse & Aggregate Master Database**:
   Run the parser script:
   ```bash
   python E:\GPS_Denied_SLR\06_analysis\scripts\05_parse_extraction.py
   ```

### Inputs & Outputs
- **Input**: `E:\GPS_Denied_SLR\04_ai_responses\extraction\resp_*.json` (657 files)
- **Output**: `E:\GPS_Denied_SLR\02_data_processed\extracted_master.csv`

### Automated Verification Protocol
```python
import glob, json, pandas as pd

responses = glob.glob('E:/GPS_Denied_SLR/04_ai_responses/extraction/resp_*.json')
assert len(responses) == 657, f"Missing JSON responses! Found {len(responses)}/657"

df = pd.read_csv('E:/GPS_Denied_SLR/02_data_processed/extracted_master.csv')
assert len(df) == 657, f"Master database row count mismatch! Expected 657, got {len(df)}"

print("✅ Phase 7 Verification Passed: Master extraction dataset is 100% complete.")
```


---

## 🚀 PHASE 8: Citation Prioritization & PDF Retrieval

### Goal
Filter top-tier papers ("Core" and "Important") for full-text PDF retrieval and detailed qualitative analysis.

### Execution Procedure
Run Python script to export high-priority papers:
```python
import pandas as pd

df = pd.read_csv('E:/GPS_Denied_SLR/02_data_processed/extracted_master.csv')
core_df = df[df['citation_tier'].isin(['Core', 'Important'])].copy()
core_df.to_csv('E:/GPS_Denied_SLR/02_data_processed/core_papers.csv', index=False)
print(f"Exported {len(core_df)} high-priority papers to core_papers.csv")
```

### Inputs & Outputs
- **Input**: `E:\GPS_Denied_SLR\02_data_processed\extracted_master.csv`
- **Output**: `E:\GPS_Denied_SLR\02_data_processed\core_papers.csv` and PDF files in `E:\GPS_Denied_SLR\05_papers_fulltext\`

### Verification Checklist
- PDF files stored in `05_papers_fulltext/` correspond to DOIs listed in `core_papers.csv`.
- Each core paper verified for full experimental evaluation.

---

## 🚀 PHASE 9: Publication Figure Generation & Analysis

### Goal
Generate high-resolution (300 DPI) publication-ready plots illustrating research trends, sensor usage, methodology evolution, and operational domains.

### Execution
Run figure generation script:
```bash
python E:\GPS_Denied_SLR\06_analysis\scripts\06_generate_figures.py
```

### Inputs & Outputs
- **Input**: `E:\GPS_Denied_SLR\02_data_processed\extracted_master.csv`
- **Output Directory**: `E:\GPS_Denied_SLR\06_analysis\output\figures\`
  - `fig01_publication_trends.png`
  - `fig02_platform_distribution.png`
  - `fig03_environment_breakdown.png`
  - `fig04_method_evolution.png`
  - `fig05_sensor_frequency.png`
  - `fig06_application_domains.png`

### Automated Verification Protocol
```python
from pathlib import Path

fig_dir = Path('E:/GPS_Denied_SLR/06_analysis/output/figures')
expected_files = [
    'fig01_publication_trends.png',
    'fig02_platform_distribution.png',
    'fig03_environment_breakdown.png',
    'fig04_method_evolution.png',
    'fig05_sensor_frequency.png',
    'fig06_application_domains.png'
]

for fig_name in expected_files:
    fig_path = fig_dir / fig_name
    assert fig_path.exists(), f"Missing figure: {fig_name}"
    assert fig_path.stat().st_size > 10000, f"Figure file is too small or corrupted: {fig_name}"

print("✅ Phase 9 Verification Passed: All 6 publication figures generated successfully.")
```

---

## 🚀 PHASE 10: Manuscript Writing & Submission Readiness

### Goal
Draft a comprehensive PRISMA-compliant SLR manuscript organizing technical insights into a structured survey paper.

### Outline & Content Breakdown
1. **Title & Abstract**: PRISMA 2020 compliant summary with key quantitative figures.
2. **PRISMA Flow Diagram**: 2,000 raw -> 1,304 deduplicated -> 696 screened -> 657 included -> core synthesis.
3. **Taxonomy & Sensor Fusion**: Monocular/Stereo VIO, LiDAR SLAM, Radar, UWB/Radio dead-reckoning.
4. **State Estimation Architectures**: EKF/UKF, Factor Graph Optimization, Deep Learning & Hybrid End-to-End frameworks.
5. **Operational Scenarios**: Tunnels, urban canyons, forest canopy, GPS jamming/spoofing environments.
6. **Open Challenges & Future Roadmap**: SWaP constraints, non-line-of-sight signal degradation, real-time edge AI, safety integrity.

### Inputs & Outputs
- **Inputs**: `extracted_master.csv`, core paper PDFs, generated figures.
- **Output**: `E:\GPS_Denied_SLR\07_manuscript\GPS_Denied_SLR_Manuscript.md` & LaTeX source files.

### Verification Checklist
- All numbers across PRISMA diagram, tables, and narrative match `extracted_master.csv`.
- Citations formatted in IEEE/MDPI style with valid DOIs.
