# FOLDER_GUIDE.md — GPS_Denied_SLR Repository Structure

| Folder | Purpose |
|--------|---------|
| `00_scope/` | Research protocol, PICOC table, inclusion/exclusion criteria, search strings, registration |
| `01_data_raw/` | Raw CSV exports from IEEE Xplore (1,000) and Scopus (1,000); search log |
| `02_data_processed/` | Deduplicated master (1,719), screening decisions, extracted_master.csv (1,700 rows) |
| `03_prompts/` | AI screening prompts (JSONL, 1,719 lines) and extraction prompts |
| `04_ai_responses/` | Raw AI JSON outputs for screening and extraction passes |
| `05_papers_fulltext/` | Downloaded PDFs of core included papers (gitignored) |
| `06_analysis/` | Python analysis scripts, generated figures (300 DPI), tables, synthesis matrices |
| `06_analysis/output/figures_v2/` | 9 publication-quality PNG figures at 300 DPI |
| `06_analysis/output/tables/` | Machine-readable CSV/Markdown table outputs |
| `06_analysis/scripts/` | Reproducible Python analysis and figure-generation scripts |
| `07_manuscript/` | SLR manuscript drafts (Markdown + LaTeX IEEEtran), BibTeX references |
| `08_docs/` | Supporting documentation, workflow trackers, folder guides |
| `09_prompts/` | Additional / versioned prompt templates |
| `supplementary/` | Supplementary artifacts: PRISMA checklist, screening spreadsheet, taxonomy matrix |
