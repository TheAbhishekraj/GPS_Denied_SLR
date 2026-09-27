# _AUDIT — Cryptographic Audit Trail, Batch Reports & Governance Ledgers

This directory contains the normative **action ledgers**, **cryptographic batch merge reports**, **phase completion gates**, and **corpus integrity audit reports** for the systematic literature review:  
**"GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)"**.

---

## 1. Directory Structure & Key Artifacts

```text
_AUDIT/
├── README.md                           # Directory manifest and guide (this file)
├── action_log.md                       # Comprehensive append-only project action ledger
├── merge_log.csv                       # Cryptographic merge log for batches B01–B28
├── batch_B01_report.md ... B28         # Individual audit reports for each of the 28 batches
├── STATUS_REPORT_20260927.md           # Master status report and provenance audit
├── FINDINGS_20260927_CORPUS_INTEGRITY.md # Detailed analysis of the 279 synthesis corpus
├── PROJECT_COMPILATION_20260927.md     # Full project compilation, rule-checks, and recovery roadmap
├── INTERPRETIVE_PROGRESS.md            # Tracking sheet for qualitative extraction fields
├── RULE9_SPEC_figures_py.md            # Approved specification for synthesis figures generation
├── PHASE_6_COMPLETION.md               # Phase 6 extraction exit gate verification
├── PHASE_7_COMPLETION.md               # Phase 7 synthesis exit gate verification
├── PHASE_8_COMPLETION.md               # Phase 8 manuscript exit gate checklist
├── CORRECTION_REPORT.md                # Audit report on corrections applied post-audit
└── RECONCILIATION_REPORT_20260920.md   # Reconciliation report from 2026-09-20 session
```

---

## 2. Core Governance & Audit Ledgers

| Ledger / Report | Description |
| :--- | :--- |
| [`action_log.md`](file:///e:/GPS_Denied_SLR/_AUDIT/action_log.md) | Universal, append-only cryptographic event ledger recording every write, edit, and move. |
| [`merge_log.csv`](file:///e:/GPS_Denied_SLR/_AUDIT/merge_log.csv) | Records pre-merge hash, post-merge hash, row counts, and quarantine folders for batches B01–B28. |
| [`STATUS_REPORT_20260927.md`](file:///e:/GPS_Denied_SLR/_AUDIT/STATUS_REPORT_20260927.md) | In-depth audit report detailing active vs. legacy files and 100% synchronization status. |
| [`PROJECT_COMPILATION_20260927.md`](file:///e:/GPS_Denied_SLR/_AUDIT/PROJECT_COMPILATION_20260927.md) | Architectural compilation report establishing the Generation-2 baseline. |
| [`FINDINGS_20260927_CORPUS_INTEGRITY.md`](file:///e:/GPS_Denied_SLR/_AUDIT/FINDINGS_20260927_CORPUS_INTEGRITY.md) | Authoritative corpus reconciliation proving the 279 in-corpus denominator. |
| [`INTERPRETIVE_PROGRESS.md`](file:///e:/GPS_Denied_SLR/_AUDIT/INTERPRETIVE_PROGRESS.md) | Batch-by-batch audit tracking for manual interpretive fields. |
| [`RULE9_SPEC_figures_py.md`](file:///e:/GPS_Denied_SLR/_AUDIT/RULE9_SPEC_figures_py.md) | Approved specification for figures F2–F9 generation script. |

---

## 3. Extraction Batch Reports (B01–B28)

Contains 28 individual audit reports verifying each batch of papers extracted during Phase 6:
* [`batch_B01_report.md`](file:///e:/GPS_Denied_SLR/_AUDIT/batch_B01_report.md) through [`batch_B28_report.md`](file:///e:/GPS_Denied_SLR/_AUDIT/batch_B28_report.md)
* Total records extracted: **279** master evidence rows across 28 sequential batches.
