# SYSTEMATIC LITERATURE REVIEW WORKFLOW
# GPS-Denied Navigation for UAVs using Multi-Sensor Fusion
# Project Setup: 2026-09-06

## PROJECT STRUCTURE OVERVIEW

```
E:\GPS_Denied_SLR\
├── 00_scope\                 # Project scope, protocol, research questions
├── 01_data_raw\             # Raw CSV exports from databases
├── 02_data_processed\       # Cleaned, deduplicated data
├── 03_prompts\              # AI prompts for screening/extraction
├── 04_ai_responses\         # AI screening and extraction outputs
├── 05_papers_fulltext\      # Downloaded PDFs of included papers
├── 06_analysis\             # Analysis scripts and results
├── 07_manuscript\           # SLR manuscript drafts
└── 08_docs\                 # Supporting documentation
```

## IMMEDIATE NEXT STEPS (NEXT 60 MINUTES)

### 1. DATABASE SEARCHES (30 minutes)
- **IEEE Xplore**: Use provided search string, filter 2010-2025, export CSV
- **Scopus**: Use provided search string, filter 2010-2025, export CSV

### 2. DATA PROCESSING (5 minutes)
- Run deduplication script: `python deduplicate.py`

### 3. PROJECT SETUP (25 minutes)
- Create all templates and scripts
- Set up screening and extraction workflows
- Prepare for next phase of SLR

## CURRENT STATUS
- ✅ Python environment ready (3.14.5)
- ✅ Required packages installed
- ✅ Project structure created
- ✅ Deduplication script ready
- ❌ Database searches pending