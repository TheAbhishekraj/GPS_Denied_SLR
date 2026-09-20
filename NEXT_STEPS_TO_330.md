# NEXT_STEPS_TO_330.md
# Sequence from current state (171 PDFs) to submission-ready manuscript

**Current:** 171 PDFs, Version-1 extraction, manuscript V1 draft exists
**Target:** 330 PDFs, Version-2 extraction, submission-ready
**Time:** ~11 hours total (4 download + 7 compute/write)
**Date:** 2026-09-17

---

## STATE SNAPSHOT (start of this plan)

| Metric | Value |
|--------|------:|
| HEAD commit | `d3ad2496` (or later) |
| PDFs on disk | 171 |
| Priority rows done | ~133 / 300 |
| IEEE access | BLOCKED (daily limit) |
| Corpus version | V1 (N=171) |

---

## PHASE 1 — Save reference files (DONE)

- ✅ MASTER_SLR_WRITING_SOP_V2.md
- ✅ 08_docs/PDF_EXTRACTION_AUDIT_PROTOCOL.md
- ⏳ NEXT_STEPS_TO_330.md (this file)
- ⏳ 08_docs/CORPUS_VERSION_LOG.md
- ⏳ CHANGELOG.md (append)

---

## PHASE 2 — Write the audit script (15 min)

**Goal:** Implement `06_analysis/scripts/17_audit_extraction.py` per
`08_docs/PDF_EXTRACTION_AUDIT_PROTOCOL.md`.

**Task for agent:**
```
Write 06_analysis/scripts/17_audit_extraction.py implementing the 5 checks
in PDF_EXTRACTION_AUDIT_PROTOCOL.md.

Interface: python 17_audit_extraction.py --check=open|fields|qa|dist|all
Reads: extracted_master_v2.csv + 05_papers_fulltext/*.pdf
Writes: 08_docs/extraction_audit_report.md
Exit: 0 PASS, 1 FAIL
Uses PyMuPDF. No hardcoded paths.
```

**Verify:**
```powershell
python 06_analysis/scripts/17_audit_extraction.py --check=dist
```

**Expected:** Report written, exit code 0.

---

## PHASE 3 — Run audit on V1 corpus (5 min)

```powershell
python 06_analysis/scripts/17_audit_extraction.py --check=all
```

**Verify:**
```powershell
Get-Content "08_docs\extraction_audit_report.md"
```

**PASS criteria:** Overall verdict = PASS.

**If FAIL:** Fix script, re-run. Do not proceed.

---

## PHASE 4 — Wait for IEEE reset (until midnight)

**Test at 00:05:**
```powershell
Start-Process "E:\GPS_Denied_SLR\08_docs\priority_300_download.csv"
```

Open 1 `ieee_link`. Try to download the PDF.

**If PDF downloads:** proceed to Phase 5.
**If still blocked:** wait until 08:00 next morning.

---

## PHASE 5 — Download batch 1: +80 PDFs (2 hrs)

Work through priority rows **134 → 213**.

Per paper:
1. Click `ieee_link` in Excel
2. IEEE opens → PDF button
3. Drag PDF → `08_docs/downloads_staging/`
4. Type `Y` in `done_Y_N` column

**Sync every 40 papers:**
```powershell
python 06_analysis\scripts\15_sync_and_move.py
```

**Stop when total = 251.**

**Progress check:**
```powershell
(Get-ChildItem "05_papers_fulltext\*.pdf").Count
```

---

## PHASE 6 — Download batch 2: +79 PDFs (2 hrs, next day)

Work through priority rows **214 → 292**.

Same loop. **Stop when total = 330.**

**Sync:**
```powershell
python 06_analysis\scripts\15_sync_and_move.py
```

**Do NOT exceed 330.**

---

## PHASE 7 — Re-run Phase 7 extraction on 330 PDFs (30 min)

```powershell
python 06_analysis\scripts\16_execute_phase7_extraction.py
```

This regenerates:
- `02_data_processed/extracted_master_v2.csv` (330 rows)
- `02_data_processed/qa_distribution_v2.csv`

---

## PHASE 8 — Run audit on V2 corpus (5 min)

```powershell
python 06_analysis\scripts\17_audit_extraction.py --check=all
```

**PASS criteria:** Overall verdict = PASS.

**If FAIL:** Fix and re-run Phase 7.

---

## PHASE 9 — Manual 5-paper spot check (20 min)

```powershell
$r = Import-Csv "02_data_processed\extracted_master_v2.csv"
$r | Get-Random -Count 5 | Select-Object id, title, method_category, qa_total | Format-Table
```

For each:
1. Open the PDF
2. Compare CSV labels to paper content
3. Note any mismatch

**PASS criteria:** ≥ 4 of 5 match.

---

## PHASE 10 — Verify distribution (2 min)

```powershell
$r = Import-Csv "02_data_processed\extracted_master_v2.csv"
$r | Group-Object qa_tier | Select-Object Name, Count
$r | Group-Object citation_tier | Select-Object Name, Count
"Total: $($r.Count)"
```

**Expected on 330:**
- Q-high: 60–85 (18–25%)
- Q-medium: 140–180 (42–55%)
- Q-low: 65–110 (20–33%)
- Core: 50–80 (15–25%)
- Total: 330

---

## PHASE 11 — Regenerate figures (10 min)

```powershell
python 06_analysis\scripts\06_generate_figures_v2.py
```

All 9 figures regenerate with N = 330 labels.

**Verify:**
```powershell
Get-ChildItem "06_analysis\output\figures_v2\*.png" | Measure-Object
```
Expected: 9.

---

## PHASE 12 — Regenerate synthesis (10 min)

```powershell
python 06_analysis\scripts\07_generate_synthesis.py
```

Regenerates taxonomy matrices with 330-corpus numbers.

---

## PHASE 13 — Rewrite manuscript as V2 (2 hrs, agent)

Give the writing agent:
- `MASTER_SLR_WRITING_SOP_V2.md`
- `02_data_processed/extracted_master_v2.csv`
- `02_data_processed/qa_distribution_v2.csv`
- The 9 regenerated figures
- `08_docs/PDF_EXTRACTION_AUDIT_PROTOCOL.md`
- `08_docs/extraction_validation_status_v1.json`

Output: `GPS_Denied_SLR_Manuscript_V2_330_COMPLETE.md`

Abstract must state: N = 330, coverage = 51.9%, updated QA distribution.

---

## PHASE 14 — Convert to LaTeX (30 min)

**Install MiKTeX first** (Windows): https://miktex.org/download

```powershell
cd E:\GPS_Denied_SLR\07_manuscript
pandoc GPS_Denied_SLR_Manuscript_V2_330_COMPLETE.md `
  --from=gfm --to=latex --standalone `
  --variable=documentclass:IEEEtran `
  --variable=classoption:journal `
  -o GPS_Denied_SLR_Manuscript_V2_330_COMPLETE.tex

pdflatex GPS_Denied_SLR_Manuscript_V2_330_COMPLETE.tex
bibtex   GPS_Denied_SLR_Manuscript_V2_330_COMPLETE
pdflatex GPS_Denied_SLR_Manuscript_V2_330_COMPLETE.tex
pdflatex GPS_Denied_SLR_Manuscript_V2_330_COMPLETE.tex
```

**Verify:** 0 undefined refs in log.

---

## PHASE 15 — Human validation (45 min, human only)

Open `08_docs/extraction_validation_sample_v1.csv`.

For each of the 20 papers:
1. Open the PDF
2. Fill: `human_method_category`, `human_environment`, `human_real_or_sim`, `human_qa_total`
3. Compute agreement vs AI

**Target:** ≥ 90% agreement per field.

---

## PHASE 16 — Supplementary package (30 min, agent)

Build S1–S10:
- S1 PRISMA 2020 checklist (27 items)
- S2 search queries (IEEE + Scopus)
- S3 quality scores (330 rows)
- S4 full reference list (BibTeX)
- S5 extracted master snapshot
- S6 screening criteria v2 (verbatim)
- S7 screening validation report
- S8 extraction validation report
- S9 not-retrieved papers (306)
- S10 extraction audit report

---

## PHASE 17 — Submission prep (1 hr, human + agent)

Run 10 submission gates per SOP §12. Fill `SUBMISSION_CHECKLIST.md`.

Compile final PDF. Verify fonts, metadata, page limits.

---

## PHASE 18 — Submit

**Venue options:**
| Venue | Time | Fee |
|-------|------|-----|
| IEEE T-RO | 6–12 mo | Free |
| IEEE Access | 2–4 mo | ~$1,950 |
| Robotics and Autonomous Systems | 3–6 mo | Free |
| Drones (MDPI) | 2–3 mo | ~$2,600 |

**Steps:**
1. Post preprint to arXiv (get DOI for priority)
2. Submit via journal portal
3. Complete author forms
4. Tag repo: `git tag v2.0-submitted`

---

## TIMELINE

| Day | Task | Hours |
|-----|------|------:|
| Today | Files 3-5, audit script, run audit | 1 |
| Tomorrow | Download 80 PDFs | 2 |
| Day 3 | Download 79 PDFs | 2 |
| Day 3 | Re-extract + audit + verify | 1 |
| Day 4 | Rewrite manuscript | 2 |
| Day 4 | Human validation | 1 |
| Day 5 | LaTeX + supplementary + submit | 3 |

**Total: 5 days, ~12 hours active work.**

---

## STOP CONDITIONS

Pause and consult if any occur:

- Extraction audit FAILs twice
- Distribution outside bounds
- Spot-check match rate < 4/5
- PDF count exceeds 330
- Any QA count changes > 30% between runs
- IEEE access still blocked after 48 hours

Do not proceed to manuscript with an unaudited corpus.

---

## RE-RUN POLICY

If corpus grows beyond 330 later (reviewer request):

1. Add PDFs → `05_papers_fulltext/`
2. Run `16_execute_phase7_extraction.py`
3. Run `17_audit_extraction.py --check=all`
4. Recompute all tables
5. Regenerate figures
6. Bump version: V2 → V3
7. Log in `08_docs/CORPUS_VERSION_LOG.md`

---

## HUMAN TASKS CHECKLIST

- [ ] Save 5 reference files
- [ ] Wait for IEEE reset
- [ ] Download 159 PDFs
- [ ] Fill 20-paper human validation sample
- [ ] Install MiKTeX
- [ ] Language edit / IEEE English polish
- [ ] Submit to journal

End of NEXT_STEPS_TO_330.md
