#!/usr/bin/env python3
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHECKLIST = os.path.join(REPO, "07_manuscript", "SUBMISSION_CHECKLIST.md")

content = """# SUBMISSION CHECKLIST — GPS_Denied_SLR

Status: **[READY FOR HUMAN REVIEW]**

## Target venue
- Primary: IEEE Transactions on Robotics (T-RO) **[PENDING HUMAN CONFIRMATION]**
- Alternative: IEEE Access **[PENDING HUMAN CONFIRMATION]**
- Source: 08_docs/MANUSCRIPT_SPEC.md

## Word count estimate
- MANUSCRIPT_V2.md is structurally complete and fully populated with Phase 7 extraction outputs.
- Target per spec: T-RO 12 pages incl. references; IEEE Access 15 pages

## Figure list
| # | figure | status |
|---|---|---|
| F1 | PRISMA flow diagram | GENERATED (08_docs/PRISMA_FLOW.md) |
| F2 | Publications per year | GENERATED (figures.py) |
| F3 | Sensor distribution | GENERATED (figures.py) |
| F4 | Method category distribution | GENERATED (figures.py) |
| F5 | Environment distribution | GENERATED (figures.py) |
| F6 | Taxonomy pie (Core/Important/Peripheral) | GENERATED (figures.py) |
| F7 | Real vs Sim breakdown | GENERATED (figures.py) |
| F8 | Geographic distribution | GENERATED (figures.py) |
| F9 | Performance metrics scatter | GENERATED (figures.py) |

## Table list
| # | table | status |
|---|---|---|
| T1 | Inclusion/exclusion criteria | SOURCE AVAILABLE (00_scope/SCOPE.md) |
| T2 | Evidence matrix (279 rows) | GENERATED (06_analysis/outputs/inference_table.csv) |
| T3 | Method comparison summary | GENERATED |
| T4 | Key results summary | GENERATED |
| T5 | Excluded papers with reasons | 02_data_processed/screening_results.csv (6 EXCLUDE) |

## Supplementary files
- S1 evidence matrix: 06_analysis/outputs/inference_table.csv
- S2 PRISMA flow: 08_docs/PRISMA_FLOW.md
- S3 pending/removal log: 02_data_processed/pdf_removal_log.csv
- S4 inclusion/exclusion criteria: 00_scope/SCOPE.md

## Author contributions
[PENDING HUMAN CONFIRMATION] — placeholder.

## Conflict of interest
[PENDING HUMAN CONFIRMATION] — placeholder.

## Data availability
[PENDING HUMAN CONFIRMATION] — candidate statement: raw exports
(01_data_raw/), screening results (02_data_processed/screening_results.csv),
the frozen anchor (08_docs/ANCHOR_FREEZE_20260919.md), per-batch page text
(02_data_processed/evidence_batches/BATCH_BXX_pages/), and all scripts
(06_analysis/scripts/) are retained in the project repository.

## PRISMA checklist mapping
- 08_docs/PRISMA_CHECKLIST.md is complete. PRISMA item 8
(selection process) satisfied by 08_docs/SCREENING_INDEPENDENCE.md (Case C).

## Known blockers before submission
1. 28 batch spot-checks pending.
2. Final human proofread of MANUSCRIPT_V2.md.

## Attestation
- No submission made yet. Awaiting final human authorization.
"""
with open(CHECKLIST, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated SUBMISSION_CHECKLIST.md")
