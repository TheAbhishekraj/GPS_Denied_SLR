# CORPUS_VERSION_LOG.md

Project: GPS_Denied_SLR  
Review type: PRISMA 2020 systematic literature review  
Topic: GPS-denied UAV navigation  
Target venues: IEEE T-RO / IEEE Access  
Last updated: 2026-09-17  
Maintainer: SLR automation pipeline  
Status: Phase 1 documentation complete; Phase 2 extraction audit pending

## 1. Purpose

This file tracks corpus versions, PDF counts, screening status, keyword taxonomy, extraction state, and audit state for the GPS_Denied_SLR review.

Rules:
- Append new versions; do not overwrite historical entries.
- Manuscript counts must match the latest audited corpus version.
- Deprecated pre-keyword-fix counts must not be cited in the manuscript, slides, audit reports, metadata, or commits.
- If keyword rules change again, create a new version snapshot instead of silently editing this file.

## 2. Version Summary

| Version | Status | PDFs on disk | Target | Screening priority list | Notes |
|---|---:|---:|---:|---:|---|
| V1 | Current working corpus | 171 | 330 | 300 records; ~133 marked done | HEAD `d3ad2496` or later; IEEE daily limit reached |
| V2 | Planned full corpus | 330 | 330 | Complete outstanding priority records | Add 159 PDFs after IEEE reset; re-extract; audit; manuscript V2 |

## 3. V1 Corpus Snapshot — 2026-09-17

- PDFs on disk: 171
- Target corpus: 330
- Remaining to target: 159
- Priority list: 300 papers
- Priority list marked done: ~133
- HEAD commit: `d3ad2496` or later
- Download status: IEEE daily limit HIT; blocked until midnight local time
- Extraction status: pre-audit; audit script not yet written
- Screening/taxonomy after keyword fix:
  - Q-high: 38, 22.2%
  - Q-medium: 84, 49.1%
  - Q-low: 49, 28.7%
  - Core: 35
  - Important: 87
  - Peripheral: 49
  - Real: 22
  - Sim: 78
  - Both: 71
- Internal consistency: quality tiers, relevance tiers, and real/sim/both each sum to 171 for V1.

## 4. V2 Target Snapshot — Planned

- PDFs on disk: 330
- Additional PDFs required: 159
- Screening priority list: 300 records; complete outstanding records
- Re-run extraction on full V2 corpus
- Run PDF extraction audit
- Update PRISMA counts and manuscript V2
- Rebuild tables and figures from V2 audited outputs only

## 5. Keyword and Taxonomy Change Control

- Counts above reflect the post-keyword-fix taxonomy.
- Pre-keyword-fix counts are deprecated and must not be cited.
- If keyword rules change again, create `V1.1` or `V2` snapshot.
- Do not hand-copy manuscript counts from old notes; use audit output.

## 6. Audit Requirements

- Audit script: `06_analysis/scripts/17_audit_extraction.py`
- Protocol: `08_docs/PDF_EXTRACTION_AUDIT_PROTOCOL.md`
- Audit inputs: V1 171 PDFs first; then V2 330 PDFs
- Audit outputs: pass/fail summary, missing extraction list, count reconciliation, taxonomy reconciliation
- Manuscript counts must be generated from audit output, not hand-copied.

## 7. Change History

| Date | Version | Change | Commit/Ref |
|---|---|---|---|
| 2026-09-17 | V1 | Phase 1 docs: SOP V2, extraction audit protocol, NEXT_STEPS_TO_330, CORPUS_VERSION_LOG; CHANGELOG entry appended | `d3ad2496` or later |
| 2026-09-17 | V1 | Keyword taxonomy fix; counts updated to Q-high 38, Q-medium 84, Q-low 49; Core 35, Important 87, Peripheral 49; Real 22, Sim 78, Both 71 | `d3ad2496` or later |
| 2026-09-17 | V1 | IEEE daily download limit reached; downloads paused until midnight local | `d3ad2496` or later |

## 8. Pre-Writing Checklist

Before writing abstract, PRISMA diagram, results tables, or response letters:
- Confirm corpus version.
- Confirm audit date and audit output path.
- Confirm all counts sum correctly.
- Confirm no deprecated pre-fix counts are present.
- Confirm V2 manuscript uses 330-corpus audited counts.
