FROZEN UTC: 2026-09-27T13:10:00Z
DIRECTORY: _MANUAL/abhishek/per_paper/
EXTRACTION FILES AT FREEZE: 288 (files matching REC_XXXX.md)
DIRECTORY ALSO HOLDS: FROZEN.md (this file) and FROZEN_MANIFEST_20260927.csv
COUNTING RULE: the extraction count is the number of files matching
  REC_*.md. A bare listing of *.md returns 289, because it also counts
  this FROZEN.md. Always count REC_*.md. Verified 2026-09-27: REC_*.md
  = 288, *.md = 289, non-REC .md = {FROZEN.md}.
MANIFEST: _MANUAL/abhishek/per_paper/FROZEN_MANIFEST_20260927.csv
MANIFEST SHA256: 00366195381CF421700070D24D705E9CAA091F212DB445276D8E75864E67DA63
MANIFEST SELF-CHECK: 288 of 288 recorded SHA256 values verified against disk, 0 mismatches

CORPUS STATUS
  Anchor corpus (MASTER_EVIDENCE.csv, 279 rows): 279 of 279 extracted = 100.0%
  Out-of-corpus files present in this directory: 9
  Directory total: 279 + 9 = 288

FREEZE RULES FOR THIS DIRECTORY
  1. No file in this directory may be edited, renamed, moved or deleted
     without a new freeze document and explicit human approval.
  2. Every extraction file is identified by its recorded SHA256 in
     FROZEN_MANIFEST_20260927.csv. A hash mismatch means the file
     changed after this freeze: halt and report (Rule 6).
  3. New extraction files may only be added by a process that also
     appends to FROZEN_MANIFEST_20260927.csv and logs to
     _AUDIT/action_log.md.
  4. This freeze covers the manuscript's extraction evidence base.
     Any count quoted in the manuscript must be reproducible from
     FROZEN_MANIFEST_20260927.csv by counting REC_*.md files in this
     directory. Count REC_*.md, never *.md.

CORPUS BOUNDARY — READ THIS BEFORE QUOTING ANY COUNT
  This directory holds 288 files but the extraction corpus is 279.
  The 9 out-of-corpus files are, by id and screening decision:
    REC_0053  EXCLUDE   (E1, out of scope)      <- extracted despite exclusion
    REC_0693  EXCLUDE   (E1, out of scope)      <- extracted despite exclusion
    REC_0866  EXCLUDE   (E1, out of scope)      <- extracted despite exclusion
    REC_0023  INCLUDE   (deferred)
    REC_0035  INCLUDE   (deferred)
    REC_0244  INCLUDE   (deferred)
    REC_0363  INCLUDE   (deferred)
    REC_1217  INCLUDE   (deferred)
    REC_1667  INCLUDE   (deferred)
  None of the nine appears in MASTER_EVIDENCE.csv or in any
  BATCH_B01-B28 manifest. The corpus denominator is 279, never 288.
  Full detail: _AUDIT/FINDINGS_20260927_CORPUS_INTEGRITY.md

KNOWN DEFECTS CARRIED INTO THIS FREEZE
  D-1 (5 files) REC_1083, REC_1084, REC_1085, REC_1095, REC_1096 use the
      superseded 17-heading legacy template and cite the retired
      extracted_master_v2.csv. All five are in-corpus.
  D-2 (2 files) REC_1118, REC_1453 have "Preprint" in the title field of
      MASTER_EVIDENCE.csv. For REC_1453 the underlying record is a
      legitimate peer-reviewed article (Measurement, 2026,
      10.1016/j.measurement.2026.121787) and the extraction file carries
      the correct title; MASTER_EVIDENCE.csv holds the corrupt string.
      REC_1118 is the same class of defect, unresolved.
  D-3 (15 files) Titles longer than 180 characters, i.e. concatenated or
      duplicated harvest artefacts, in MASTER_EVIDENCE.csv. Includes
      REC_1640, REC_1459, REC_1463, REC_1348, REC_1216, REC_1146,
      REC_1067, REC_1049, REC_0840, REC_0469, REC_0345, REC_0084,
      REC_0037, REC_0008, REC_1642.
  D-4 MASTER_EVIDENCE.csv reports year = NOT_REPORTED for 279 of 279 rows
      and doi = NOT_REPORTED for 247 of 279 rows. All 247 DOIs are
      recoverable verbatim from screening_results.csv.
      These are metadata gaps, not content gaps: the extraction files
      themselves carry year and doi correctly.

SCOPE OF WHAT IS FROZEN
  Frozen: the 288 extraction files, by SHA256, as listed in the manifest.
  Not frozen by this document: MASTER_EVIDENCE.csv (a writable pipeline
  file) and the batch manifests. Defects D-2, D-3 and D-4 live in
  MASTER_EVIDENCE.csv and are therefore repairable under Rule 2 with
  approval and a logged before/after hash.
