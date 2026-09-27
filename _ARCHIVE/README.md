# _ARCHIVE — Historical & Legacy Workspace Repository

This directory holds **archived Generation-1 and pre-reset artifacts** safely preserved for historical reference and auditability, but removed from the active PRISMA 2020 pipeline tree.

---

## 1. Directory Structure

```text
_ARCHIVE/
├── README.md                      # Archive catalog and relocation log (this file)
├── legacy_02_data_processed/      # Stale Generation-1 data files and obsolete notes
├── legacy_03_extraction/          # Extractions for excluded duplicate PDFs
├── legacy_03_prompts/             # Generation-1 prompt files and JSONL execution logs (5,134 files)
└── legacy_04_ai_responses/        # Generation-1 raw LLM responses and calibration logs (5,142 files)
```

---

## 2. Archived Subdirectories Catalog

### 📁 `legacy_02_data_processed/`
Relocated on 2026-09-27 from `02_data_processed/`:
1. `summary.txt` — Outdated 2026-09-06 test numbers contradicting frozen deduplication.
2. `MASTER_EVIDENCE_V1.xlsx` — Pre-rebuild Excel extraction table.
3. `EXTRACTION_NOTES.md` — Notes citing deprecated 1,700-row extraction model.
4. `EXTRACTION_NOTES_v2.md` — Notes citing obsolete 171-paper subset.
5. `V1_SCOPE_IDS.txt` — Obsolete Generation-1 scope ID listing.
6. `PENDING_MASTER_EXTENSION_IDS.txt` — Legacy 121-paper extension tracking list.
7. `retrieval_log.csv` — Empty 0-row header template.
8. `pending_list.csv` — Empty 0-row header template.

### 📁 `legacy_03_extraction/`
Relocated on 2026-09-27 from `03_extraction/per_paper/`:
1. `REC_1582.md` — Extraction for excluded duplicate PDF of `REC_0274`.
2. `REC_1688.md` — Extraction for excluded duplicate PDF of `REC_1715`.
3. `REC_1715.md` — Extraction for excluded duplicate PDF of `REC_1688`.

### 📁 `legacy_03_prompts/` (5,134 files, 65.6 MB)
Relocated on 2026-09-27 from `03_prompts/`:
* `extraction_prompts/` — Individual prompt files from early automated extraction runs.
* `screening_prompts/` & `screening_prompts_v2/` — Individual screening prompt files.
* `extraction_prompts.jsonl`, `extraction_prompts_v2.jsonl`, `screening_prompts.jsonl`, `screening_prompts_v2.jsonl` — JSONL prompt streams.
* *Note:* Archiving this directory permanently resolves the Rule 5 count collision noted in `_AUDIT/PROJECT_COMPILATION_20260927.md`.

### 📁 `legacy_04_ai_responses/` (5,142 files, 6.7 MB)
Relocated on 2026-09-27 from `04_ai_responses/`:
* `extraction/` — Raw LLM completion outputs from early extraction attempts.
* `screening/`, `screening_v2/`, `screening_v2_calibration/` — Raw LLM screening responses.
* `screening_calibration.jsonl`, `screening_results.jsonl`, `screening_results_v2.jsonl` — Completion logs.
