# IDENTITY_AUDIT_REPORT.md

Does each `05_papers_fulltext/<id>.pdf` match its master-CSV title?

- rows checked: 171
- **PASS**: 170
- **WEAK** (partial title match, needs a glance): 1
- **FAIL** (title and PDF disagree): 0
- UNTESTABLE (title too short to tokenise): 0
- NO_PDF: 0

Method: distinctive title tokens (>=4 chars, stopwords removed) matched
against the first 3 pages of the PDF; a pass also comes from a
literal DOI match. Heuristic triage only - PASS means 'nothing
contradictory found', FAIL means a human must look.

## WEAK - partial match

| id | ratio | master title | missing tokens |
|---|---|---|---|
| REC_0115 | 0.429 | Low Computational Data Fusion Approach Using INS and UWB for UAV Navig | navigation;tasks;gps-denied;environments |
