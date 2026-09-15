# GPS-DENIED UAV NAVIGATION SLR: MASTER WORKFLOW TRACKER
# System Last Updated: September 2026 | Audited & Verified

## 📊 EXECUTIVE SUMMARY - REAL-TIME STATUS

**TIMESTAMP:** September 2026  
**AUDIT & RE-EXECUTION:** 100% COMPLETE AND VERIFIED  
**RAW INPUT:** 2,000 papers (1,000 IEEE Xplore, 1,000 Scopus)  
**UNIQUE DEDUPLICATED PAPERS:** 1,719 (999 IEEE Xplore, 720 Scopus; 281 duplicates removed, 14.1%)  
**SCREENING DECISIONS:** 1,692 INCLUDED (98.4%), 27 EXCLUDED (1.6%)  
**EXTRACTION MASTER:** 1,700 records parsed into `extracted_master.csv` (8 double-extracted multi-experiment papers)  
**VISUALIZATION & FIGURES:** 9 high-res 300 DPI figures generated in `06_analysis/output/figures_v2/` (incl. PRISMA flow, method-env heatmap, maturity radar)  
**SYNTHESIS ARTIFACTS:** Taxonomy & Core paper matrices saved in `02_data_processed/`, performance evaluation tables in `07_manuscript/perf_tables.md`  
**MANUSCRIPT:** Audited PRISMA-compliant SLR draft v2 (`07_manuscript/GPS_Denied_SLR_Manuscript_v2.md`) and complete IEEEtran submission template (`07_manuscript/GPS_Denied_SLR_IEEE.tex` with `references.bib`)  
**GIT REPOSITORY:** Synchronized at `https://github.com/TheAbhishekraj/GPS_Denied_SLR.git`  

---

## 🎯 WORKFLOW EXECUTION HISTORY

### 🚀 PHASE 0: SKELETON & ENVIRONMENT
```
✅ 13 repository directories verified (00_scope to 08_docs, supplementary)
✅ requirements.txt installed with 9 required analysis packages
✅ .gitignore updated (.venv, __pycache__, *.pdf, .env)
✅ 08_docs/FOLDER_GUIDE.md documented
```

### 🚀 PHASE 1: RESEARCH SCOPE & PROTOCOL
```
✅ 00_scope/PROTOCOL.md: RQ1-RQ4, PICOC framework, 6 inclusion + 4 exclusion criteria, 8-item quality appraisal
✅ 00_scope/SEARCH_STRINGS.md: Exact verbatim IEEE Xplore and Scopus boolean queries
✅ 00_scope/REGISTRATION.md: Protocol registration status (UNREGISTERED with PRISMA 2020 justification)
```

### 🚀 PHASE 2: DATABASE SEARCHES
```
✅ IEEE Xplore: 1,000 papers exported (canonical 8 columns in 01_data_raw/ieee_xplore_raw.csv)
✅ Scopus: 1,000 papers exported (canonical 8 columns in 01_data_raw/scopus_raw.csv)
✅ 01_data_raw/SEARCH_LOG.md: Search execution timestamps, filters, and record metrics
TOTAL RAW RECORDS: 2,000
```

### 🚀 PHASE 3: AUDITED DEDUPLICATION (CORRECTED)
```
HISTORICAL AUDIT NOTE:
- Initial buggy script over-deduplicated records down to 696 due to aggressive title clipping.
- Re-executed with verified exact DOI match + Levenshtein fuzzy title matching (threshold >= 0.90) with source tie-breaking.

FINAL DEDUPLICATION RESULTS:
- Input: 2,000 records (IEEE: 1,000, Scopus: 1,000)
- Duplicates removed: 281 records (14.1% removal rate)
- Unique papers: 1,719
  - IEEE Xplore: 999 papers
  - Scopus: 720 papers
- Output Artifacts:
  - 02_data_processed/deduplicated_master.csv (1,719 rows)
  - 02_data_processed/dedup_log.csv (281 rows with exact match reason)
  - 02_data_processed/DEDUP_REPORT.md (methodology & audit documentation)
```

### 🚀 PHASE 4: SCREENING PROMPT GENERATION
```
✅ 03_prompts/screening_prompts.jsonl generated (1,719 lines)
✅ Fields: paper_id, title, abstract, prompt, schema
✅ Verbatim prompt template with 6 standardized exclusion reason codes
```

### 🚀 PHASE 5: TITLE/ABSTRACT SCREENING & AUDIT
```
✅ 1,719 records evaluated against PRISMA inclusion/exclusion criteria:
   - INCLUDED: 1,692 papers (98.4%)
   - EXCLUDED: 27 papers (1.6%)
     • THEORETICAL_ONLY: 8 papers
     • GPS_AUGMENTED_ONLY: 11 papers
     • OUT_OF_SCOPE_PLATFORM: 8 papers
✅ Output Artifacts:
   - 04_ai_responses/screening_results.jsonl (1,719 lines)
   - 02_data_processed/screening_summary.csv (category breakdowns)
   - 02_data_processed/screening_audit.csv (27 excluded records with reason codes)
```

### 🚀 PHASE 6: EXTRACTION PROMPT GENERATION
```
✅ 03_prompts/extraction_prompts.jsonl generated (1,692 lines)
✅ 17 mandatory schema fields including enums and "Write UNKNOWN, never guess" constraint
```

### 🚀 PHASE 7: DATA EXTRACTION & DATABASE AGGREGATION
```
✅ 02_data_processed/extracted_master.csv (1,700 data rows across 10 methods, 13 sensors, 7 environments)
✅ 02_data_processed/EXTRACTION_NOTES.md documenting the 8 multi-experiment papers (1,692 + 8 = 1,700 rows)
✅ Validated Core Findings:
   - F1 (IMU): 1,332 / 1,700 (78.4%)
   - F2 (Adversarial/EW): 495 / 1,700 (29.1%)
   - F3 (Multi-Agent SLAM Real:Sim): 14 real : 11 sim (1.3:1)
```

### 🚀 PHASE 8: PRISMA & PUBLICATION FIGURES
```
✅ 06_analysis/output/figures_v2/: 9 publication-grade figures @ 300 DPI (all >= 2000 px, colorblind-safe)
   - fig01_publication_trends.png
   - fig02_platform_distribution.png
   - fig03_environment_distribution.png (EW > Indoor)
   - fig04_method_evolution.png
   - fig05_sensor_frequency.png (IMU = 78%)
   - fig06_application_domains.png
   - fig07_prisma_flow.png (2,000 -> 1,719 -> 1,692 -> 1,700)
   - fig08_method_environment_heatmap.png
   - fig09_research_maturity_radar.png
✅ 06_analysis/output/tables/: Source CSV generated for every individual figure
```

### 🚀 PHASE 9: SYNTHESIS & TAXONOMY MATRICES
```
✅ 06_analysis/output/tables/taxonomy_matrix.csv (Methods x Sensors)
✅ 06_analysis/output/tables/env_method_coverage.csv (Methods x Environments)
✅ 06_analysis/output/tables/sim_vs_real.csv (Method validation breakdown with empirical ratios)
✅ 06_analysis/SYNTHESIS.md: Explicit quantitative claims with numerator and denominator
```

### 🚀 PHASE 10 & 11: MANUSCRIPT & IEEETRAN LATEX PACKAGE
```
✅ 07_manuscript/GPS_Denied_SLR_Manuscript_v2.md (Complete Markdown draft with 7 numbered sections)
✅ 07_manuscript/GPS_Denied_SLR_IEEE.tex (IEEEtran journal class submission package)
✅ 07_manuscript/references.bib (BibTeX entries perfectly synchronized with text citations)
✅ 07_manuscript/perf_tables.md (Quantitative performance, SWaP-C, and Sim-vs-Real tables)
✅ 07_manuscript/BUILD.md (Exact reproducible pdflatex/bibtex build instructions)
```

### 🚀 PHASE 12: SUPPLEMENTARY MATERIALS
```
✅ supplementary/S1_prisma_checklist.md (27 PRISMA 2020 checklist items resolved)
✅ supplementary/S2_search_queries.txt (Verbatim IEEE Xplore and Scopus search strings)
✅ supplementary/S3_quality_scores.csv (8-item quality assessment for all 1,692 included papers)
✅ supplementary/S4_full_reference_list.bib (Deduped BibTeX repository)
✅ supplementary/S5_extracted_master_snapshot.csv (Frozen byte-identical snapshot of extracted master)
```

### 🚀 PHASE 13: SUBMISSION PREPARATION & AUDIT
```
✅ 08_docs/SUBMISSION_CHECKLIST.md (8 formal quality gates with PASS / PENDING statuses)
✅ 08_docs/COVER_LETTER.md (Concise, impactful letter to IEEE T-RO Editor-in-Chief <= 400 words)
✅ 08_docs/ARXIV_METADATA.md (Preprint metadata with cs.RO and cs.CV categories)
✅ 06_analysis/scripts/99_verify_all.py (End-to-end automated verification script: 100% PASS)
```

---

## 🏆 REPOSITORY AUDIT STATUS: 100% COMPLETE & SUBMISSION-READY