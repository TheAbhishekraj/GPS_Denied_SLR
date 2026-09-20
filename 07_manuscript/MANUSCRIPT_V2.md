# MANUSCRIPT_V2 — GPS-Denied Navigation for UAVs: A Systematic Literature Review

Status: **DRAFT — NOT FINAL** (overnight run, 2026-09-19). Requires human review.
Template: 08_docs/MANUSCRIPT_SPEC.md (IEEE T-RO / IEEE Access).
Data basis: 02_data_processed/MASTER_EVIDENCE.csv (279 rows).
Every number below is traced in 08_docs/NUMBER_TRACE.md.
Values not yet extracted are marked **[UNRESOLVED]**; none are estimated.

## Abstract
This review reports a PRISMA 2020 systematic literature review of GPS/GNSS-denied
navigation for unmanned aerial vehicles (UAVs). Screening 2,000 raw records from
IEEE Xplore and Scopus yielded 1,716 unique records, 636 records passing
title/abstract screening, and 291 records assessed in full text. Of these, 285
were included and 6 excluded (3 under E1, 3 under E2). Full text was retrieved
for 288 records; 6 INCLUDE records were deferred from extraction pending an
identity-integrity audit (see Limitations). Extraction populated 279 records
across 28 fields in 28 controlled batches. Quantitative synthesis of sensor
configurations, methods, environments, and reported accuracy is **[UNRESOLVED]**
pending the interpretive extraction pass; this draft therefore reports the
review's protocol, corpus, and administrative results, and does not yet report
substantive performance findings.

## 1. Introduction
UAVs depend on GNSS for localisation, yet GNSS is unreliable or unavailable in
indoor spaces, urban canyons, subterranean settings, forest canopies, and under
jamming or spoofing. The literature proposes multi-sensor fusion to sustain
navigation in these conditions. This review maps that literature under a
pre-registered protocol (00_scope/SCOPE.md, frozen 2026-09-19).

Research questions (RQ1–RQ4) are as defined in 00_scope/SCOPE.md. Answers to
RQ1–RQ3, which require the extracted sensor/method/metric fields, are
**[UNRESOLVED]** in this draft. RQ4 (limitations and future directions) is
**[UNRESOLVED]** pending Section-17 synthesis.

## 2. Related Work
Systematic reviews and surveys exist for visual-inertial odometry and for
indoor UAV navigation; these were screened as part of the 636-record pool.
Their comparative content is **[UNRESOLVED]** in this draft pending extraction
of the `contribution_type` and `method_category` fields.

## 3. Methods (PRISMA 2020)
### 3.1 Protocol and registration
The protocol is frozen at 00_scope/SCOPE.md (SHA256 recorded in
00_scope/FROZEN.md). The protocol was not modified after freezing.

### 3.2 Information sources and search
Two databases were searched: IEEE Xplore and Scopus. Raw exports:
01_data_raw/ieee_xplore_20260615.csv (1,000 records) and
01_data_raw/scopus_20260615.csv (1,000 records).

### 3.3 Eligibility criteria
Inclusion I1–I7 and exclusion E1–E7 are as defined in 00_scope/SCOPE.md
(Q5, Q6); the frozen anchor records 6 exclusions (3 E1, 3 E2).

### 3.4 Selection process
Screening was performed by a single human reviewer assisted by an AI tool,
with the human verifying all AI decisions; the AI-suggested decision, confidence,
triggered criteria, and justification are recorded per record in
02_data_processed/screening_results.csv. This is disclosed as a limitation
(08_docs/SCREENING_INDEPENDENCE.md, Case C, selected 2026-09-19).

### 3.5 Data collection process
Extraction proceeded in 28 controlled batches (27 batches of 10 records and one
of 9) using 06_analysis/scripts/phase4_batch_extract.py, with per-batch
verification and append-only merges through 06_analysis/scripts/merge_batch.py
and validation by 06_analysis/scripts/validate_master.py. The schema is frozen
at 08_docs/EXTRACTION_SCHEMA_v1.md (28 columns). Extraction rules E1–E12 are
frozen at 08_docs/EXTRACTION_RULES.md.

### 3.6 PRISMA flow (counts)
2,000 identified → 1,716 unique after de-duplication → 636 passing
title/abstract screening → 291 assessed in full text → 285 INCLUDE / 6 EXCLUDE
→ 288 PDFs on disk → 279 records extracted (6 deferred). Source:
08_docs/ANCHOR_FREEZE_20260919.md and _AUDIT/PHASE_6_COMPLETION.md.

## 4. Results
### 4.1 Corpus description
The extracted evidence base contains 279 records (285 INCLUDE − 6 deferred).
Source: 02_data_processed/MASTER_EVIDENCE.csv. All 279 rows carry a title and a
page range; validation reports 0 duplicate IDs and 0 empty required fields
(_AUDIT/master_validation.md).

### 4.2 Year distribution
**[UNRESOLVED]** — the `year` field is NOT_REPORTED for 279/279 records
(deterministic extraction populated only id, title, doi, _source_pages).

### 4.3 Sensor configurations (RQ1)
**[UNRESOLVED]** — `sensors` is NOT_REPORTED for 279/279 records.

### 4.4 Methods and algorithms (RQ3)
**[UNRESOLVED]** — `method_category` and `algorithm` are NOT_REPORTED for
279/279 records (06_analysis/outputs/taxonomy_distribution.csv).

### 4.5 Environments and accuracy (RQ2)
**[UNRESOLVED]** — `environment`, `metrics`, and `headline_result` are
NOT_REPORTED for 279/279 records. No accuracy value is reported here; none was
extracted yet, and none has been inferred, converted, or averaged
(08_docs/SYNTHESIS_METHOD.md forbids pooling and unit conversion).

### 4.6 Quality appraisal
**[UNRESOLVED]** — the QA rubric is defined in 00_scope/SCOPE.md (Q7) and the
QA index file exists at 03_extraction/per_paper/QA_INDEX.md (header only,
0 data rows).

## 5. Discussion
Substantive discussion of sensor-fusion trade-offs and performance is
**[UNRESOLVED]** and cannot be written without the interpretive extraction pass.
This draft deliberately contains no invented comparative claims.

## 6. Limitations
1. **Interpretive fields empty.** All 24 interpretive fields are NOT_REPORTED for
   all 279 records; the extraction run captured bibliographic identity only.
2. **Six deferred records.** REC_0023, REC_0035, REC_0244, REC_1217, REC_1667 and
   REC_0363 are excluded from extraction pending an identity-integrity audit;
   their PDFs' content does not match their corpus metadata. The corpus is
   therefore reported as 279 extracted of 285 INCLUDE.
3. **Screening independence.** Single reviewer with AI assistance (Case C),
   disclosed per PRISMA 2020 item 8.
4. **Spot-checks pending.** The 1-in-10 manual spot-check was deferred; all 28
   batch reports carry "spot-check pending human review".
5. **DOI coverage.** `doi` is NOT_REPORTED wherever the DOI lies in a page footer
   outside the page-1 header window used by the extractor.
6. **No meta-analysis.** Heterogeneous metrics and figure-only reporting preclude
   pooling; a structured narrative synthesis is planned
   (08_docs/SYNTHESIS_METHOD.md).

## 7. Conclusion
This draft establishes the review protocol, the audited corpus
(2,000 → 1,716 → 636 → 291 → 285/6), and a verified 279-record extraction
substrate. Substantive conclusions are **[UNRESOLVED]** pending the interpretive
pass. No submission is made and no phase is marked complete.

## 8. References
**[UNRESOLVED]** — IEEE-style references require per-record bibliographic
extraction (authors, venue, year, DOI), which is not yet populated. Reference
list to be generated from MASTER_EVIDENCE.csv after the interpretive pass.

---
DRAFT ONLY. Not final. Not approved. Not submitted.

