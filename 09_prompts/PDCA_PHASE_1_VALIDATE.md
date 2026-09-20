# PDCA_PHASE_1_VALIDATE.md — Validate existing PDFs + extended retrieval

## ROLE
You are executing Phase 1 of a PDCA recovery cycle for GPS_Denied_SLR.
This phase is SELF-CONTAINED. Do NOT touch any other phase. Do NOT commit.

## CONTEXT
- HEAD = 60928c6 (post-rollback).
- Retrieval returned 47 log entries, only 30 PDFs on disk. The log lied once.
- Phase 7 needs >=40% full-text coverage; current = 4.7%. Pipeline BLOCKED.

## RULES (binding)
1. Create .agent_lock at start; remove at end.
2. No hardcoded absolute paths.
3. No fabrication. If a check fails, STOP, report actual vs expected.
4. Every output must include raw terminal output, not summaries.

## TASK DO-1 — Validate the 30 PDFs

For every file in 05_papers_fulltext/*.pdf:
1. Read the first 4 bytes. Valid PDF starts with `%PDF`.
2. If not `%PDF`, mark as FAKE and list the first 20 bytes as hex.
3. Write results to 08_docs/pdf_validation_phase1.csv with columns:
   filename, size_bytes, first_4_bytes_hex, is_valid_pdf (True/False)
4. Do NOT delete fakes yet — just report.

OUTPUT REQUEST (paste verbatim in report):
DO-1 RESULT:
Total .pdf files: __
Valid (%PDF header): __
Fake (HTML/JSON/other): __
Fake filenames: __

STOP-1: If fake count > 5, STOP. Report and await instruction.

## TASK DO-2 — Extended retrieval (Semantic Scholar + arXiv ID)

Run 06_analysis/scripts/07b_retrieve_extended.py.
If the script does not exist, STOP and report "07b script missing".

Before running, verify:
1. The script contains no hardcoded E:\ paths.
2. It reads 02_data_processed/screened_included_v2.csv.
3. It writes to 05_papers_fulltext/ and updates 08_docs/fulltext_retrieval_log.csv.

After running, report:
DO-2 RESULT:
New PDFs added: __
Total PDFs on disk: __
Coverage %: __ (of 636 included)
Runtime (minutes): __

STOP-2: If new PDFs < 10 AND Path C is anticipated, report and STOP. The
corpus may be <50 papers — a human must approve Path C on a tiny corpus.

## TASK — Final verification for Phase 1

Run and paste raw output:
(Get-ChildItem "05_papers_fulltext\*.pdf").Count
[math]::Round((Get-ChildItem "05_papers_fulltext\*.pdf" | Measure-Object Length -Sum).Sum / 1MB, 1)
Import-Csv "08_docs\fulltext_retrieval_log.csv" | Group-Object status | Select-Object Name, Count

## PHASE 1 REPORT TEMPLATE (paste as final answer)
=== PHASE 1 REPORT — Validate + Extend ===
Date: ____

DO-1 (validate PDFs):
Total .pdf files: __
Valid: __
Fake: __
Fake filenames: __

DO-2 (extended retrieval):
New PDFs: __
Total on disk: __
Coverage %: __
Runtime (min): __

FINAL STATE:
PDFs on disk: __
Total size (MB): __
Log status distribution:
<paste Group-Object output>

HALT TRIGGERED: <YES|NO>
Reason if YES: ____

Files written this phase:
- 08_docs/pdf_validation_phase1.csv
- 08_docs/fulltext_retrieval_log.csv (updated)
- CHANGELOG.md (Phase 1 entry)

Next phase requested: Phase 2 (Path decision)

## CHANGELOG ENTRY (append-only, dated)
Add: "PDCA Phase 1: validated N PDFs (F fakes), extended retrieval +M PDFs,
coverage X%. Halt trigger: Y/N."
