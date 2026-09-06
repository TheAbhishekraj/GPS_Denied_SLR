# SYSTEMATIC LITERATURE REVIEW WORKFLOW
# GPS-Denied Navigation for UAVs using Multi-Sensor Fusion
# Project Setup: 2026-09-06

## PROJECT STRUCTURE OVERVIEW

```
E:\GPS_Denied_SLR\
├── 00_scope\                 # Project scope, protocol, research questions
├── 01_data_raw\             # Raw CSV exports from databases (2,000 papers)
├── 02_data_processed\       # Cleaned, deduplicated data (696 papers), screening & extraction masters
├── 03_prompts\              # AI prompts for screening (696) and extraction (657)
├── 04_ai_responses\         # AI screening (696) and extraction (657) JSON outputs
├── 05_papers_fulltext\      # Downloaded PDFs of included core papers
├── 06_analysis\             # Analysis scripts, figure generation, synthesis matrices
├── 07_manuscript\           # SLR manuscript drafts
└── 08_docs\                 # Supporting documentation
```

## CURRENT STATUS & SUMMARY

- ✅ Phase 1: Project Setup & Environment Ready
- ✅ Phase 2: Database Searches (2,000 raw papers: 1,000 IEEE Xplore, 1,000 Scopus)
- ✅ Phase 3: Deduplication (1,304 duplicates removed, 696 unique papers)
- ✅ Phase 4: Screening Prompt Generation (696 screening prompts created)
- ✅ Phase 5: AI Screening & Parsing (100% processed: 657 INCLUDED, 39 EXCLUDED)
- ✅ Phase 6: Extraction Prompt Generation (657 rich prompts generated)
- ✅ Phase 7: AI Data Extraction & Parsing (657 extractions complete -> `extracted_master.csv`)
- ✅ Phase 8: PRISMA & Visualization Generation (6 high-res figures generated in 300 DPI)
- ✅ Phase 9: Synthesis & Taxonomy Matrices Generated (`synthesis_taxonomy_matrix.csv`, `core_papers_summary.csv`)
- 🔜 Phase 10: SLR Synthesis Manuscript Writing & Final Paper Publication
