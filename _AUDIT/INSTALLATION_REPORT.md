# INSTALLATION REPORT — Governance Files
Generated: 2026-09-19T17:16:00Z
Scope: E:\GPS_Denied_SLR (governance installation task)
Status: PASS (2 findings reported below, no action taken on them)

## 1. Old files quarantined
Quarantine folder: E:\GPS_Denied_SLR\_QUARANTINE_INSTRUCTIONS_20260919_171403\

| file | original_path | quarantine_path | sha256 | timestamp |
|---|---|---|---|---|
| .clinerules | E:\GPS_Denied_SLR\.clinerules | _QUARANTINE_INSTRUCTIONS_20260919_171403\.clinerules.old | 95DFFA567AF782221B14F7FD53E063687DB869072CEDAE7FB4D0B7DC3C61B2FF | 2026-09-19T17:14:03Z |
| MASTER_PROMPT.txt | E:\GPS_Denied_SLR\_PROJECT\MASTER_PROMPT.txt | _QUARANTINE_INSTRUCTIONS_20260919_171403\MASTER_PROMPT.txt.old | 48C146D01B37EA12F6EE3278028B0CF67067B81792BFC715DBBE27EC890ADAE6 | 2026-09-19T17:14:03Z |

Manifest: _QUARANTINE_INSTRUCTIONS_20260919_171403\OLD_INSTRUCTION_HASHES.csv
Originals deleted after verified copy (explicitly approved in task, Step 1).
No other file was deleted or moved.

## 2. New files created
| file | sha256 |
|---|---|
| E:\GPS_Denied_SLR\.clinerules | CFD479AF38855BEEFA065CC1F09FE5FCBA1E06E2F87083B85CF971EF7570AF4C |
| E:\GPS_Denied_SLR\_PROJECT\MASTER_PROMPT.txt | 601FEC279E7AAB9E4AAA4CBDBE6CB7D353E4FF68DE371A81AFA5243ED70601D0 |
| E:\GPS_Denied_SLR\_PROJECT\PROJECT_CHARTER.md | FA873A3482FE3C93AF5C595C4FFDCAA9C7D8EC06C7F7E88C2F5EE9D699DFD9E7 |
| E:\GPS_Denied_SLR\_PROJECT\END_GOAL.md | 080C293C63FE078BF8BD035F76DAFA1B882DB666EBBA63A64F7BEFCDC7A65A15 |
| E:\GPS_Denied_SLR\_PROJECT\PHASE_GATES.md | DD226076A60057C7FDEEEF0D863998A51EA402C2ACAA767971B8CEB037ED41C4 |
| E:\GPS_Denied_SLR\_PROJECT\MASTER_PROMPT_1.md | 5F485FF7609225F1C7B458DC7B8D78B04D80BB3280F1D53ECCCDDD52703E20E3 |
| E:\GPS_Denied_SLR\_PROJECT\MASTER_PROMPT_2.md | 16D0DB55433990176EC79462F3F9775C9E4377DA0DF59744A22E0218B6605DB3 |

All content written byte-for-byte as specified in the task
(MASTER_PROMPT_1.md and MASTER_PROMPT_2.md created as placeholders
per Steps 7-8: "Full content will be provided by the human.").

## 3. Hash verification of frozen anchor files (read-only)
| file | result |
|---|---|
| 01_data_raw\ieee_xplore_20260615.csv | MATCH FE374C9F2A405A0F0E07598979340AE971311B80BB20D8E121572D648CAA18F3 |
| 01_data_raw\scopus_20260615.csv | MATCH EF162F4F9525B6FC5CC617D1E3BADACD11F09B3E80FDFC488C4E37918BD524CB |
| 02_data_processed\deduplicated_master.csv | MATCH A648930848EED1950A602EA5FA2F739CFDDB1C2BB1289F86B810211DB3D8649A |
| 02_data_processed\screened_included_v2.csv | MATCH CD1B38745FF653BE3E23C62371B87A12861261BDC057F4F313645C4A79E93CED |
| 02_data_processed\screening_results.csv | MATCH 86DADC842AA590B03C0F5145FFCA5340800CB41AE505BC7AD1488CB40648F6D7 |

## 4. Findings — forbidden numbers in live files (Rule 5: report and halt)
| id | file | line | severity | evidence | rule | proposed_fix |
|---|---|---|---|---|---|---|
| F-01 | 08_docs\ANCHOR_FREEZE_20260919.md | 90 | HIGH | line lists the five forbidden legacy numbers by literal value | Rule 5 | Flagged for MASTER_PROMPT_1 correction run (Step 3 of that prompt). Not touched — file is outside this task's allowlist and no fix content was provided. |
| F-02 | _PROJECT\MASTER_PROMPT.txt | 46 | LOW | FORBIDDEN NUMBERS section lists the forbidden values; content is verbatim per Step 3 of the task ("EXACTLY this content") | Rule 5 vs task Step 3 conflict | Human decision: keep verbatim (documents the ban) or replace values with a redaction token. |

Note: an automated scan also matched the bare digits 4-9-5 inside an
IEEE raw CSV row (01_data_raw\ieee_xplore_20260615.csv:882). That is
paper content inside a frozen raw export, not a legacy count. Logged
for completeness; no action proposed or taken.

## 5. Allowlist confirmation
Written: .clinerules, _PROJECT\* (6 files), _AUDIT\INSTALLATION_REPORT.md,
_AUDIT\action_log.md (append), _QUARANTINE_INSTRUCTIONS_20260919_171403\*.
All within the task allowlist (_PROJECT/**, _AUDIT/**,
_QUARANTINE_INSTRUCTIONS_<timestamp>/**, .clinerules).
Nothing written to 01_data_raw/, 02_data_processed/, or
05_papers_fulltext/.

## 6. No-analysis confirmation
No analysis script was run. No Python was executed. The only commands
used were directory listings, file copies, SHA256 hashing, and text
scans (read-only), plus the two approved deletes after verified copies.
