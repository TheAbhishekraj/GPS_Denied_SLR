# PREFLIGHT_FINDINGS.md
# Step 4 result: how many of the 171 papers report numeric ATE?

Date: 2026-09-17
Operator: AI (Cline), for A. Raj — **not yet human-verified**
Evidence: `pdf_numeric_probe_v1.csv`, `pdf_numeric_probe_v1.json`,
`PDF_NUMERIC_PROBE_REPORT.md` (all in this folder), produced by
`06_analysis/scripts/08_pdf_numeric_probe.py`, cross-checked by
`06_analysis/scripts/08b_ate_token_diagnostic.py`.

This memo lives in `06_analysis/output/` and not in `08_docs/` on purpose:
Check V4 of the verification protocol forbids the strings 1,692 / 1,700 /
1,719 / 2,000 / 281 / 1,332 / 495 / 98.4% anywhere under `08_docs`, and a probe
that quotes raw numbers out of 171 PDFs cannot promise to avoid them.

---

## 1. Headline

| Question | Answer |
|---|---|
| Papers that use the metric ATE at all | **6 / 171 (3.5%)** |
| Papers with ATE + numeric value + unit in text reach | 1 / 171 |
| Papers that use RMSE | 40 / 171 (23.4%) |
| Papers with RMSE + numeric value + unit in text reach | 20 / 171 (11.7%) |
| Papers with position / positioning / localization error + number + unit | 21 / 171 (12.3%) |
| Papers with **any** unit-anchored accuracy number | **44 / 171 (25.7%)** |
| Papers with no unit-anchored accuracy number at all | 127 / 171 (74.3%) |
| PDFs with a usable text layer | 170 / 171 |

The six genuine ATE papers, each confirmed by reading the match in context:

| id | context |
|---|---|
| REC_0035 | "average translation error (ATE) of Hector SLAM is 0.071 m" |
| REC_0041 | "positioning accuracy is represented by the RMSE of ATE", Table IV |
| REC_0502 | "we use the absolute trajectory error (ATE) metric" |
| REC_0951 | "TABLE IV ABLATION STUDY: ATE RMSE (M) / PROCESSING TIME (MS)" |
| REC_1217 | "Absolute Trajectory Error (ATE) and Relative Pose Error (RPE)" |
| REC_1573 | "Absolute Translational Error (ATE) is the accuracy metric" |

## 2. Warning: the original probe was wrong

The probe supplied in the task description
(`(ATE|RMSE|drift)[^\n]{0,40}\d`, case-insensitive) returns **167 / 171**.
That number is almost entirely false positives — it is matching the tail of
ordinary words followed by any digit:

- `ATE` inside estim**ate** / illustr**ate** / gener**ate** / approxim**ate** /
  calcul**ate** / coordin**ate** / upd**ate** / integr**ate** / accur**ate** /
  evalu**ate** (top offenders ranked in the diagnostic output),
- `cep` inside ex**cep**t / con**cep**t (145 / 171 "hits" for `cep`),
- hyphenated line breaks: `moder- ate`, `evalu- ate`,
- PDF ligatures: `con<U+FB02>ate`, `In<U+FB02>ate`, where the character before
  `ate` is not in `[A-Za-z]` and so defeats a naive character guard.

The corrected probe matches the acronyms case-sensitively (papers write `ATE`,
never `ate`) behind a word guard, which removes all of the above without losing
a genuine hit. **Do not cite 167 / 171 anywhere.** Use 6 / 171 for ATE.

This is not a parsing artifact: the median extractable text across the corpus is
about 34,000 characters and 170 / 171 PDFs parsed cleanly, so the scarcity of
ATE is a real property of this corpus.

## 3. Consequence for gate V9 — a decision is required

Gate V9 passes only if **≥ 5 `approach_family` values carry a numeric
`best_ate_rmse`**. With ATE used by 6 / 171 papers, the strict ATE form of V9
will fail. Three options:

| Option | What it means | Cost |
|---|---|---|
| **A. Re-scope V9 to any accuracy metric** (recommended) | Count a family as accuracy-bearing if `best_ate_rmse` **or** `other_metric_value` carries a unit-anchored number. 44 / 171 papers qualify, which is likely to clear 5 families. ATE stays a column, but the manuscript's accuracy section becomes "ATE where available; RMSE / position error otherwise". | one-line edit to the protocol; honest, keeps the accuracy story |
| **B. Keep V9 strict** | Extraction proceeds, V9 reports failure, and the manuscript is reframed as architectural / thematic per the confirmation checklist item 5. `best_ate_rmse` is `NOT_REPORTED` in 165+ rows. | manuscript loses its quantitative spine |
| **C. Neither — stop** | Do not spend the 6–10 h extraction run until A or B is chosen. | zero |

Option A is the recommendation because it is what the corpus can actually
support, and because it needs no change to the 63-column schema — the
`other_metric_name` / `other_metric_value` / `other_metric_unit` columns already
exist for exactly this purpose. **V9 must not be rescued by inventing ATE
values.** `NOT_REPORTED` is the correct value wherever a paper is silent.

## 4. Two defects in the delivered specification

1. **Column count.** Parts 3 and 4 both say `MASTER_EVIDENCE_V1.csv` has
   "66 columns", but the enumerated field list they give contains **63** field
   names. The files were written with the 63 enumerated names, verbatim, since
   inventing 3 extra columns would mean inventing schema. Either the label
   should read 63, or the 3 missing columns must be named.
2. **The probe regex** described in section 2.

## 5. Secondary parse risks for the extraction run

- `REC_0631` has only 2,129 extractable characters — it is the one PDF with a
  thin text layer and is the likely candidate for an OCR check or a
  `NOT_REPORTED`-only extraction.
- 0 PDFs failed to parse and 0 PDF ids are missing from
  `extracted_master_v2.csv`, so the join key is clean: 171 ids = 171 PDFs.
- Keyword proximity under-counts by construction: for REC_0041, REC_0951 and
  REC_1573 the ATE numbers sit in tables a full caption away from the word, so
  the extraction agent must read the tables rather than trust proximity. The
  probe is a floor for ATE papers (6) and a ceiling for nothing.

## 6. Status

Extraction agent **not started** — the confirmation checklist requires the probe
result first, and it is now back. Awaiting the A / B / C decision in section 3
before spending the 6–10 h run.