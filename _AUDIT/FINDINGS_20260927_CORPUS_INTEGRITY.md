# CORPUS INTEGRITY FINDINGS — GPS_Denied_SLR

Generated: 2026-09-27T12:55Z (Scribe session).
Method: file-listing counts (Rule 4). Every number below is reproduced by
listing `_MANUAL/abhishek/per_paper/*.md`, reading `MASTER_EVIDENCE.csv`,
reading `screening_results.csv`, and reading the 28 batch CSVs. No number is
taken on trust from a prior log.

**Status: OPEN — awaiting human ruling. Nothing was changed on the basis of
these findings. No extraction file was moved, edited or deleted. The frozen
corpus files were not touched.**

---

## 1. Measured state

| Quantity | Value | How obtained |
|---|---:|---|
| `MASTER_EVIDENCE.csv` rows | 279 | CSV read |
| `screening_results.csv` rows | 291 (285 INCLUDE + 6 EXCLUDE) | CSV read |
| Unique ids across BATCH_B01..B28 | 279 | 28 CSV reads, de-duplicated |
| Are the 279 batch ids the same set as the 279 master ids? | **YES — identical** | set comparison |
| `_MANUAL/abhishek/per_paper/*.md` on disk | **288** | directory listing |
| Of those, in-corpus (id in the 279) | **279** | set intersection |
| Of those, out-of-corpus | **9** | set difference |
| In-corpus completion | **279 / 279 = 100.0%** | division |
| Files failing the 18-section template | 5 (legacy 17-heading template) | heading count |

Set arithmetic that closes exactly:
`279 (master) = 279 (in-corpus on disk) + 0 gaps`
`288 (on disk) = 279 (in-corpus) + 9 (out-of-corpus)`

**UPDATE 2026-09-27T13:10Z.** The two gaps open when this report was first
written were closed by the external writer at 13:04:58Z (commit `25877010`).
In-corpus coverage is now **279 of 279 = 100.0%**. Findings C-4 and C-5 below
are consequently RESOLVED; C-1, C-2, C-3 and C-6 remain open, and the new
findings D-2, D-3 and D-4 were added.

---

## 2. FINDING C-1 — nine extraction files exist for records outside the frozen corpus

None of the nine ids below appears in `MASTER_EVIDENCE.csv`, and none appears in
any of the 28 batch CSVs. All nine do appear in `screening_results.csv`, which is
how their status was determined.

| id | decision in `screening_results.csv` | added by commit | date | DOI |
|---|---|---|---|---|
| REC_0023 | INCLUDE (deferred) | 003bdca8 | 2026-09-20 | 10.1109/INSPIRE67328.2025.11300665 |
| REC_0035 | INCLUDE (deferred) | 003bdca8 | 2026-09-20 | 10.1109/WCSP49889.2020.9299710 |
| REC_0053 | **EXCLUDE** | 003bdca8 | 2026-09-20 | 10.1109/ICACCM61117.2024.11059131 |
| REC_0244 | INCLUDE (deferred) | 003bdca8 | 2026-09-20 | 10.1109/GLOBECOM59602.2025.11432122 |
| REC_0363 | INCLUDE (deferred) | 003bdca8 | 2026-09-20 | 10.1109/PLANS.2018.8373497 |
| REC_0693 | **EXCLUDE** | 003bdca8 | 2026-09-20 | — |
| REC_0866 | **EXCLUDE** | 003bdca8 | 2026-09-20 | — |
| REC_1217 | INCLUDE (deferred) | 78f00c5c | 2026-09-27 | — |
| REC_1667 | INCLUDE (deferred) | af3fff38 | 2026-09-27 | 10.1109/ICAR65334.2025.11338655 |

Two distinct defects are bundled here.

### FINDING C-2 — three files were extracted for records that screening EXCLUDED

`REC_0053`, `REC_0693`, `REC_0866` carry `decision = EXCLUDE` in the frozen
`screening_results.csv`. Extraction of an excluded record is a direct
inclusion-criteria conflict: whatever those three files say must not reach the
manuscript, and the PRISMA flow must not count them as included studies.

### FINDING C-3 — six files were extracted for DEFERRED records

The six ids `REC_0023, REC_0035, REC_0244, REC_0363, REC_1217, REC_1667` are
exactly `INCLUDE ids - MASTER_EVIDENCE ids`. They are the deferral set: included
at screening, but deliberately held out of the 279-paper extraction corpus.

`REC_1217` was already logged as OPEN FINDING B. This audit adds `REC_1667`
(committed 2026-09-27 in `af3fff38`) and confirms four further cases from
2026-09-20 in `003bdca8`.

**Why this matters.** The anchor is frozen at 279 extraction-target papers. Nine
extra files make the extraction directory look 286/279 complete. Anyone counting
the directory instead of the corpus would report the wrong denominator in the
PRISMA flow. This is the Rule 6 condition exactly: sources disagree, so halt and
report rather than guess.

**Options for the ruling (no option applied).**
 (a) Downgrade the nine files to a non-corpus side directory and state the 279
     corpus in the PRISMA flow.
 (b) Accept them as an expansion of the corpus to 288 targets and re-issue the
     anchor — this contradicts the frozen anchor and needs explicit approval.
 (c) Keep the files, add a header flag `CORPUS_STATUS: OUT_OF_CORPUS`, and
     exclude them from every count.

---

## 3. FINDING C-4 — RESOLVED 2026-09-27T13:04:58Z

Both outstanding in-corpus records were extracted by the external writer in
commit `25877010`.

| id | batch | SHA256 | sections | resolution |
|---|---|---|---|---|
| REC_1453 | B26 | `B25AE7272D3B8767C637283081D83E03D0EC4D7B9E6961970263E0570EF32697` | 18 | CLOSED |
| REC_1640 | B28 | `4A1FCC9730CF5B02BB4A6A20839223F25D05B9AE96F71256EA08340B3E6B3374` | 18 | CLOSED |

Both were identity-verified by three-way comparison of `MASTER_EVIDENCE.csv`
vs `screening_results.csv` vs the extraction file's YAML header. B26 is now
10/10 and B28 is 9/9. **In-corpus coverage: 279 of 279 = 100.0%.**

---

## 3b. FINDING C-5 — RESOLVED as a METADATA defect, not a screening defect

`REC_1453` was flagged because its `MASTER_EVIDENCE.csv` title read
`Preprint not peer reviewed`. The three-way comparison settles it:

| Source | REC_1453 title | DOI | Year |
|---|---|---|---|
| `MASTER_EVIDENCE.csv` | Preprint not peer reviewed | NOT_REPORTED | NOT_REPORTED |
| `screening_results.csv` | A Graph-Optimization-Based tightly coupled Multi-Source positioning method for UAVs in GNSS-Denied environments | 10.1016/j.measurement.2026.121787 | — |
| extraction file | A Graph-Optimization-Based Tightly Coupled Multi-Source Positioning Method for UAVs in GNSS-Denied Environments | 10.1016/j.measurement.2026.121787 | 2026 |

**Conclusion: the record is a legitimate peer-reviewed *Measurement* (Elsevier)
2026 article.** It satisfies SCOPE.md I3 and does not fall under E7. The corpus
stays at 279; the anchor does not change. The "Preprint" string was a harvest
artefact captured in `MASTER_EVIDENCE.csv` only.

`REC_1640` shows the same failure class: `MASTER_EVIDENCE.csv` holds a
duplicated title with the authors concatenated into it, while
`screening_results.csv` and the extraction file both agree.

This is a repair task in `MASTER_EVIDENCE.csv`, which Rule 2 lists as writable.
It is **not** a reason to reopen screening.

---

## 3c. NEW FINDINGS D-2, D-3, D-4 — metadata defects in MASTER_EVIDENCE.csv

Measured across all 279 rows on 2026-09-27.

| id | defect | count | fixable from |
|---|---|---:|---|
| **D-2** | `title` contains the string "Preprint" | 2 (`REC_1118`, `REC_1453`) | `screening_results.csv` |
| **D-3** | `title` longer than 180 characters (concatenated / duplicated harvest artefacts) | 15 (`REC_0008`, `REC_0037`, `REC_0084`, `REC_0345`, `REC_0469`, `REC_0840`, `REC_1049`, `REC_1067`, `REC_1146`, `REC_1216`, `REC_1348`, `REC_1459`, `REC_1463`, `REC_1640`, `REC_1642`) | `screening_results.csv` |
| **D-4a** | `year` = NOT_REPORTED | **279 of 279 (100%)** | `screening_results.csv` |
| **D-4b** | `doi` = NOT_REPORTED | **247 of 279 (88.5%)** | `screening_results.csv` — all 247 recoverable verbatim |

Severity: HIGH for the review's completeness, LOW for effort — every one of
these is a mechanical join, not a judgement call. The extraction files
themselves carry `year` and `doi` correctly, so no PDF needs re-reading.

Neither D-2 nor D-3 nor D-4 affects the anchor or the corpus count.

---

## 4. FINDING C-5 — SUPERSEDED, see section 3b

This section originally framed `REC_1453` as a possible screening defect
requiring a ruling. The three-way identity comparison in section 3b resolved it
as a metadata defect in `MASTER_EVIDENCE.csv` only. No ruling is needed and the
anchor does not change.

---

## 5. FINDING C-6 — five files use the superseded 17-heading legacy template

`REC_1083`, `REC_1084`, `REC_1085`, `REC_1095`, `REC_1096` carry these headings:

```
## 0. Identity
## Key findings (hand-readable)
## 1. Abstract summary  ... ## 15. Cross-references for the manuscript
```

The current standard, verified on the 283 files that are not on the legacy
template, is:

```
## 1. Bibliographic Metadata
## 2. Problem Statement
## 3. Motivation
## 4. GPS-Denied Context
## 5. Proposed Method
## 6. System Architecture
## 7. Experimental Setup
## 8. Key Quantitative Results
## 9. Ablation / Sensitivity
## 10. Stated Limitations
## 11. Future Work
## 12. Contribution Type
## 13. Taxonomy Category
## 14. Country / Funding
## 15. Notes
## 16. Source Page Index
## 17. Research Gap
## 18. Best Combination & Accuracy
```

Two problems beyond the heading names. The legacy template's heading
`## 13. Quality appraisal (verbatim from extracted_master_v2.csv)` points at
`extracted_master_v2.csv`, a superseded artifact outside the frozen corpus, so
those five files cite a source that the corpus no longer recognises. And the
legacy layout has no `## 18. Best Combination & Accuracy`, so the five files
cannot feed the same downstream fields as the other 283.

These five are in-corpus (all five are in `MASTER_EVIDENCE.csv`), so they are
real extractions on the wrong template, not out-of-corpus files.

**Options:** (a) re-template the five from their retained pdf-page sources,
(b) mark them `TEMPLATE: LEGACY` and handle them as a documented exception.

---

## 6. FINDING C-7 — the six full-text exclusions, for the record

`screening_results.csv` records exactly six `decision = EXCLUDE` rows. They are
listed here so the PRISMA flow's full-text exclusion box can be populated with
reasons without re-reading the frozen file.

| id | note |
|---|---|
| REC_0053 | **has an extraction file on disk — see C-2** |
| REC_0693 | **has an extraction file on disk — see C-2** |
| REC_0866 | **has an extraction file on disk — see C-2** |
| REC_1582 | no extraction file — correct |
| REC_1688 | no extraction file — correct |
| REC_1715 | no extraction file — correct |

Note the arithmetic: the anchor's "6" refers to these six *exclusions*, and the
deferral set is a separate six. Both happen to be six, which is why the two have
been conflated up to now. They are different sets with different memberships.

---

## 7. Rulings required

| # | Question | Recommended |
|---|---|---|
| C-1/C-2/C-3 | What happens to the 9 out-of-corpus extraction files, including the 3 for EXCLUDED records? | Option (a): move them out of `_MANUAL/abhishek/per_paper/` (Rule 2 permits writes under `_MANUAL/**`) and keep the 279 corpus intact. **Still OPEN.** Note: the directory is now frozen, so relocation requires a new freeze doc |
| C-4 | Extract the two remaining in-corpus records? | **CLOSED 2026-09-27T13:04:58Z** — both extracted in commit `25877010`, identity-verified. No action |
| C-5 | Keep `REC_1453` in the corpus? | **CLOSED as a metadata defect.** `REC_1453` is a peer-reviewed *Measurement* 2026 article; the corpus stays at 279; the anchor is unchanged. Repair belongs to T1 |
| C-6 | The 5 legacy-template files | **Still OPEN.** Option (a): re-template from pdf-page sources, or mark `TEMPLATE: LEGACY` |
| C-7 | No action — informational | — |
| **D-2/D-3/D-4** | Repair `title`, `doi` and `year` in `MASTER_EVIDENCE.csv` (2 corrupt titles, 15 over-long titles, 279 missing years, 247 missing DOIs, all recoverable from `screening_results.csv`) | **NEW.** Approve the T1 join script. `MASTER_EVIDENCE.csv` is writable under Rule 2; record before/after SHA256 |
| Prior A | `REC_1232` vs `REC_1235` duplicate identity (same DOI `10.3233/ATDE260245`) | **Unchanged — still open** |
| Prior B | `REC_1217` extracted despite deferral | Subsumed into C-1/C-3 |

---

## 8. What this session did NOT do

- Did not move, edit or delete any extraction file.
- Did not write to `01_data_raw/`, `05_papers_fulltext/`, or any frozen CSV.
- Did not start Phase 7 substance (the 24 interpretive fields in
  `MASTER_EVIDENCE.csv` remain `NOT_REPORTED` 279/279).
- Did not treat the 9 out-of-corpus files as corpus members in any count.
- Did not resolve the `REC_1232` / `REC_1235` duplicate.

Frozen-file integrity was re-verified while producing this report:
`screening_results.csv` `86DADC84...`, `deduplicated_master.csv` `A6489308...`,
`MASTER_EVIDENCE.csv` `15B26C59...`, `SCOPE.md` `21264852...` — all unchanged.

---

END OF CORPUS INTEGRITY FINDINGS — awaiting human ruling C-1..C-7.


