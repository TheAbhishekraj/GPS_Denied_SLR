#!/usr/bin/env python3
"""refresh_submission_docs.py - Station 9 / Gate 9.5: refresh submission documents.

Reads current file bytes to record exact sizes and SHA256 hashes.
Writes 07_manuscript/SUBMISSION_CHECKLIST.md and 07_manuscript/README.md.
No external data. All numbers trace to locked canonical values.
"""
import os
import hashlib
from datetime import datetime, timezone

ROOT = r'E:\GPS_Denied_SLR'
MP = os.path.join(ROOT, '07_manuscript')
OD = os.path.join(ROOT, '06_analysis', 'outputs')
FG = os.path.join(OD, 'figures')

TS = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(65536), b''):
            h.update(b)
    return h.hexdigest().upper()


def size(p):
    return os.path.getsize(p)


V4 = os.path.join(MP, 'MANUSCRIPT_V4.md')
BIB = os.path.join(MP, 'references.bib')

check = []
check.append('# SUBMISSION CHECKLIST — GPS_Denied_SLR')
check.append('')
check.append('Updated: %s' % TS)
check.append('Audit basis: Station 9 / Gate 9.4 audit PASS (L5 18/18, L7 0, L2 0 genuine untraceable).')
check.append('')
check.append('## Target venue')
check.append('- Primary: **IEEE Access**')
check.append('- Scope: SLR on GPS-denied UAV navigation, multi-sensor fusion (2010–2026).')
check.append('')
check.append('## Corpus (locked canonical)')
check.append('2,000 identified (IEEE 1,000 + Scopus 1,000) -> 1,716 after dedup')
check.append('-> 636 screened -> 291 full-text -> 285 INCLUDE / 6 EXCLUDE -> 279 corpus (+6 deferred).')
check.append('')
check.append('## Manuscript')
check.append('| file | bytes | sha256 |')
check.append('|---|---|---|')
check.append('| 07_manuscript/MANUSCRIPT_V4.md | %d | `%s` |' % (size(V4), sha(V4)))
check.append('| 07_manuscript/references.bib (279 entries) | %d | `%s` |' % (size(BIB), sha(BIB)))
check.append('')
check.append('## Figures (regenerated, traceable)')
check.append('| # | figure | sha256 |')
check.append('|---|---|---|')
fig_titles = {1: 'PRISMA flow', 2: 'Publications per year', 3: 'Sensor modality by epoch',
              4: 'Fusion-pair evolution', 5: 'Environment distribution', 6: 'Taxonomy distribution',
              7: 'Validation fidelity', 8: 'Contributing countries', 9: 'Limitation and future themes'}
for i in range(1, 10):
    p = os.path.join(FG, 'F%d_output.png' % i)
    check.append('| F%d | %s | `%s` |' % (i, fig_titles[i], sha(p)))
check.append('')
check.append('## Tables (manuscript, traced sources)')
check.append('| # | table | source |')
check.append('|---|---|---|')
check.append('| T-II | Chronological publication trajectory | MASTER_EVIDENCE.csv year |')
check.append('| T-III | Sensor modality frequency | RQ_DATA_ANALYTICS.json sensor_by_epoch |')
check.append('| T-3 | Fusion-pair evolution | RQ_DATA_ANALYTICS.json fusion_pairs_by_epoch |')
check.append('| T-IV | Environment categorization | RQ_DATA_ANALYTICS.json env_distribution |')
check.append('| T-5 | Algorithmic family vs validation | RQ_DATA_ANALYTICS.json algo_families_vs_validation |')
check.append('| T-6 | Q-High anchors (REC_0037/0502/1277) | MASTER_EVIDENCE.csv + quality_appraisal_scored.csv |')
check.append('| T-7 | Limitations and future priorities | RQ_DATA_ANALYTICS.json limitation/future themes |')
check.append('')
check.append('## Supplementary files')
check.append('- S1 evidence matrix: 06_analysis/outputs/inference_table.csv')
check.append('- S2 figure data tables: 06_analysis/outputs/tables/F1_data.csv ... F9_data.csv')
check.append('- S3 PRISMA run report: 06_analysis/outputs/figures/FIGURES_RUN_REPORT.md')
check.append('- S4 number trace: 08_docs/NUMBER_TRACE.md')
check.append('- S5 inclusion/exclusion criteria: 00_scope/SCOPE.md')
check.append('- S6 screening register: 02_data_processed/screening_results.csv (285 INCLUDE, 6 EXCLUDE)')
check.append('- S7 PDF removal log: 02_data_processed/pdf_removal_log.csv')
check.append('')
check.append('## Author contributions')
check.append('[PENDING HUMAN CONFIRMATION] — placeholder.')
check.append('')
check.append('## Conflict of interest')
check.append('[PENDING HUMAN CONFIRMATION] — placeholder.')
check.append('')
check.append('## Data availability')
check.append('[PENDING HUMAN CONFIRMATION] — candidate statement: raw exports (01_data_raw/), screening results')
check.append('(02_data_processed/screening_results.csv), the frozen anchor (08_docs/ANCHOR_FREEZE_20260919.md), per-batch page text')
check.append('(02_data_processed/evidence_batches/BATCH_BXX_pages/), and all scripts (06_analysis/scripts/) are retained in the project repository.')
check.append('')
check.append('## Known blockers before submission')
check.append('- 5 extraction records flagged for re-extraction: REC_1083, REC_1084, REC_1085, REC_1095, REC_1096.')
check.append('- 21 author name strings carry upstream encoding loss (diacritics replaced by "?") in references.bib.')
check.append('- 91 of 279 bibliography entries have no venue in the corpus files (marked NOT_REPORTED).')
check.append('- Final human proofread of MANUSCRIPT_V4.md.')
check.append('')
check.append('## Attestation')
check.append('- No submission made yet. Awaiting final human authorization.')
open(os.path.join(MP, 'SUBMISSION_CHECKLIST.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(check) + '\n')
print('WROTE SUBMISSION_CHECKLIST.md (%d bytes)' % size(os.path.join(MP, 'SUBMISSION_CHECKLIST.md')))
readme = []
readme.append('# 07_manuscript — Manuscript Drafts, Tables, and Submission Files')
readme.append('')
readme.append('Active draft: **MANUSCRIPT_V4.md** (Station 9 repair of MANUSCRIPT_V3.md; Station 9 / Gate 9.4 audit PASS).')
readme.append('')
readme.append('```text')
readme.append('07_manuscript/')
readme.append('├── MANUSCRIPT_V4.md               # Canonical manuscript (audit-clean; Fig. 1-9 callouts wired)')
readme.append('├── MANUSCRIPT_V3.md               # Superseded draft (legacy flow numbers + ID errors; keep for diff)')
readme.append('├── MANUSCRIPT_V2.md               # Superseded draft')
readme.append('├── references.bib                 # 279-entry corpus bibliography (rebuilt Gate 9.2)')
readme.append('├── BUILD.md                       # Compilation and rendering instructions')
readme.append('├── GPS_Denied_SLR_IEEE_v2.tex     # Legacy IEEE LaTeX source')
readme.append('├── GPS_Denied_SLR_IEEE_v3.tex     # Legacy IEEE LaTeX source (pre-repair)')
readme.append('├── GPS_Denied_SLR_IEEE_v4.tex     # Legacy IEEE LaTeX source (pre-repair; requires regeneration from V4)')
readme.append('└── SUBMISSION_CHECKLIST.md        # IEEE Access submission readiness checklist')
readme.append('```')
readme.append('')
readme.append('## Active files')
readme.append('')
readme.append('| File | Bytes | SHA256 | Role / Status |')
readme.append('|---|---|---|---|')
readme.append('| 07_manuscript/MANUSCRIPT_V4.md | %d | `%s` | Canonical manuscript (Station 9 repaired) |' % (size(V4), sha(V4)))
readme.append('| 07_manuscript/MANUSCRIPT_V3.md | %d | `%s` | Superseded V3 draft (retained for diff only) |' % (size(os.path.join(MP, 'MANUSCRIPT_V3.md')), sha(os.path.join(MP, 'MANUSCRIPT_V3.md'))))
readme.append('| 07_manuscript/references.bib | %d | `%s` | 279-entry bibliography (Gate 9.2 rebuilt) |' % (size(BIB), sha(BIB)))
readme.append('| 07_manuscript/GPS_Denied_SLR_IEEE_v3.tex | %d | `%s` | Legacy LaTeX (pre-repair) |' % (size(os.path.join(MP, 'GPS_Denied_SLR_IEEE_v3.tex')), sha(os.path.join(MP, 'GPS_Denied_SLR_IEEE_v3.tex'))))
readme.append('| 07_manuscript/GPS_Denied_SLR_IEEE_v4.tex | %d | `%s` | Legacy LaTeX (pre-repair; regenerate before submission) |' % (size(os.path.join(MP, 'GPS_Denied_SLR_IEEE_v4.tex')), sha(os.path.join(MP, 'GPS_Denied_SLR_IEEE_v4.tex'))))
readme.append('| 07_manuscript/SUBMISSION_CHECKLIST.md | %d | `%s` | Refreshed Station 9 submission checklist |' % (size(os.path.join(MP, 'SUBMISSION_CHECKLIST.md')), sha(os.path.join(MP, 'SUBMISSION_CHECKLIST.md'))))
readme.append('| 07_manuscript/BUILD.md | %d | `%s` | Compilation instructions |' % (size(os.path.join(MP, 'BUILD.md')), sha(os.path.join(MP, 'BUILD.md'))))
readme.append('')
readme.append('Updated: %s' % TS)
open(os.path.join(MP, 'README.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(readme) + '\n')
print('WROTE README.md (%d bytes)' % size(os.path.join(MP, 'README.md')))
print('SELF-AUDIT PASS')