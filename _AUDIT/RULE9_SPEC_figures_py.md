# RULE 9 SPEC — `06_analysis/scripts/figures.py`

Status: **PROPOSED — AWAITING HUMAN APPROVAL. The script has NOT been written.**
Prepared: 2026-09-27T11:30Z by the Scribe session.
Governing rule: `.clinerules` Rule 9 — no new script without a written spec and
explicit approval.

---

## 1. Purpose

Generate the nine manuscript figures F1–F9 defined in `08_docs/MANUSCRIPT_SPEC.md`
from the frozen evidence base, deterministically and reproducibly, so that the
specification rule *"Every figure must regenerate from a script in
06_analysis/scripts/"* is satisfied and the `_PROJECT/PHASE_GATES.md` Phase 7
EXIT criterion ("every figure regenerates from a script") can be tested.
This is the last outstanding Phase 7 deliverable.

---

## 2. Design constraint that shapes the whole script (read first)

Measured state of the source at 2026-09-27T11:28Z:

| Column group | Status |
|---|---|
| `id`, `title`, `_source_pages` | populated 279 / 279 |
| `doi` | populated 32 / 279 (247 = NOT_REPORTED) |
| **all other 24 columns** | **NOT_REPORTED 279 / 279** |

Therefore **F2–F9 have no usable data yet.** The interpretive pass is still
running and `MASTER_EVIDENCE.csv` has not been re-populated.

The script must therefore support **two modes** and must never invent a value in
either:

| Mode | Behaviour |
|---|---|
| `--mode=placeholder` (default until Phase 7 substance lands) | draws figures that ARE derivable today (F1 PRISMA flow, plus a provenance panel), and for F2–F9 emits an explicit **"DATA NOT YET EXTRACTED"** placeholder image stating the measured `NOT_REPORTED` count for each required column. It must NOT silently omit a figure and must NOT render a zero-height bar. |
| `--mode=final` | requires that the governing column has at least one non-`NOT_REPORTED` value; otherwise the script **fails that figure with a non-zero exit code and a named reason** rather than drawing an empty chart. |

---

## 3. Inputs (measured row counts, 2026-09-27)

| Input | Rows | Columns | Use |
|---|---:|---:|---|
| `02_data_processed/MASTER_EVIDENCE.csv` | **279** | **28** | F2–F9 source (`year`, `sensors`, `method_category`, `environment`, `taxonomy_category`, `real_or_sim`, `country`, `metrics`, `headline_result`) |
| `02_data_processed/screening_results.csv` | **291** | — | F1 flow (full-text assessed; INCLUDE / EXCLUDE split) |
| `02_data_processed/screened_included_v2.csv` | **636** | — | F1 flow (title/abstract stage) |
| `02_data_processed/deduplicated_master.csv` | **1,716** | — | F1 flow (post-dedup) |
| `01_data_raw/ieee_xplore_20260615.csv` | **1,000** | — | F1 flow (identification) |
| `01_data_raw/scopus_20260615.csv` | **1,000** | — | F1 flow (identification) |
| `08_docs/ANCHOR_FREEZE_20260919.md` | 55 lines | — | F1 flow (frozen anchor values, incl. 288 PDFs) |
| `05_papers_fulltext/*.pdf` | **288** files | — | F1 flow (PDFs retrieved) |
| `02_data_processed/evidence_batches/BATCH_B*.csv` | **28** files / 279 id rows | 28 | optional batch-provenance panel |

All inputs are read-only. Frozen files are read, never written.

---

## 4. Outputs (file counts and rows)

| # | Output file | Type | Rows/points | Source |
|---|---|---|---:|---|
| F1 | `06_analysis/outputs/figures/F1_prisma_flow.png` | flow diagram | 6 stages | anchor freeze + CSVs + PDF listing |
| F2 | `.../F2_year_distribution.png` | bar | N distinct years | `year` |
| F3 | `.../F3_sensor_distribution.png` | bar | N sensors (multi-label) | `sensors` |
| F4 | `.../F4_method_category_distribution.png` | bar | <= 11 (schema enum) | `method_category` |
| F5 | `.../F5_environment_distribution.png` | bar | <= 6 (schema enum) | `environment` |
| F6 | `.../F6_taxonomy_pie.png` | pie | <= 3 (Core/Important/Peripheral) | `taxonomy_category` |
| F7 | `.../F7_real_vs_sim.png` | stacked bar | <= 4 (schema enum) | `real_or_sim` |
| F8 | `.../F8_geographic_distribution.png` | bar | N countries | `country` |
| F9 | `.../F9_metrics_scatter.png` | scatter | 1 point per (paper, metric) | `metrics` + `headline_result` |

Companion machine-readable tables:

| Output file | Rows |
|---|---:|
| `06_analysis/outputs/tables/F1_prisma_flow.csv` | 6 |
| `06_analysis/outputs/tables/F2..F9_*.csv` | one row per category/count, only when that figure succeeds |

Plus one run report: `06_analysis/outputs/figures/FIGURES_RUN_REPORT.md`
(per figure: source rows, NOT_REPORTED count, status DRAWN / PLACEHOLDER /
FAILED, output SHA256).

---

## 5. Side effects

1. Creates directory `06_analysis/outputs/figures/` if absent (currently absent).
2. Creates/overwrites the 9 PNGs, the companion CSVs and `FIGURES_RUN_REPORT.md`.
3. **Writes nothing else.** It must NOT write `02_data_processed/**`,
   `MASTER_EVIDENCE.csv`, `03_extraction/**`, `_MANUAL/**`, or any frozen file.
4. Reads, does not modify, the 288 PDFs.
5. No network access.

---

## 6. Interface

```
python 06_analysis/scripts/figures.py --mode=placeholder|final [--only F1,F3] [--dpi 300] [--seed 42]
```

| Flag | Default | Meaning |
|---|---|---|
| `--mode` | `placeholder` | as defined in section 2 |
| `--only` | all | comma-separated subset, e.g. `F1,F4` |
| `--dpi` | `300` | matplotlib savefig DPI |
| `--seed` | `42` | RNG seed for any jitter (F9); output must be byte-reproducible |

Exit codes: `0` = all requested figures drawn; `1` = one or more figures FAILED
(named in stdout and in the run report); `2` = input missing or unreadable.

Paths resolved repo-relative from the script location (no hardcoded absolute
paths).

---

## 7. Style requirements

- 300 DPI PNG, tight bounding box.
- Colourblind-safe palette (Okabe-Ito). No red/green-only encoding.
- Every axis labelled with units where units exist. No unit conversion anywhere
  (`08_docs/SYNTHESIS_METHOD.md` forbids it).
- Multi-label fields (`sensors`) labelled "multi-label, not mutually exclusive".
- Every figure carries its denominator in the title or caption, e.g. `(N = 279)`.
- Deterministic: same inputs produce byte-identical outputs.

---

## 8. Prohibitions (non-negotiable)

1. **No invented, imputed, estimated or rounded values.** Absent data stays
   absent. `NOT_REPORTED` is not a category to be plotted as zero.
2. **No pooling** of heterogeneous metrics, no unit conversion, no confidence
   intervals (`08_docs/SYNTHESIS_METHOD.md`).
3. **No silent omission.** A figure that cannot be drawn must appear in the run
   report as FAILED with a reason.
4. **No forbidden legacy numeric values** (Rule 5) in any figure, caption, axis
   label or companion CSV.
5. **No write outside `06_analysis/outputs/**`.**

---

## 9. Libraries

Confirmed present in `.venv` on 2026-09-27:

| Library | Version |
|---|---|
| matplotlib | 3.11.1 |
| pandas | 3.0.5 |
| numpy | 2.5.2 |

No new dependency is introduced.

---

## 10. Acceptance tests (to be run after approval)

| # | Test | Expected |
|---|---|---|
| 1 | `python 06_analysis/scripts/figures.py --mode=placeholder` | exit 0; 9 PNGs written; F2-F9 report `PLACEHOLDER` with `NOT_REPORTED = 279` |
| 2 | Re-run test 1 | identical SHA256 for every output (byte-reproducible) |
| 3 | `--mode=final --only F4` before Phase 7 substance | exit 1; named reason: `method_category has 0 non-NOT_REPORTED values` |
| 4 | Frozen-file check after both runs | `86DADC84...`, `A6489308...`, `15B26C59...` unchanged |
| 5 | Rule 5 scan of the run report and all CSVs | 0 forbidden values |

---

## 11. OPEN QUESTION FOR THE APPROVER

F2-F9 are meaningless until Phase 7 populates the 24 interpretive fields.

| Option | Description |
|---|---|
| **a** | Approve the spec as written; run `--mode=placeholder` now to get F1 and the provenance panel; run `--mode=final` after Phase 7. |
| **b** | Approve only F1 (PRISMA flow) now; defer the remainder of the spec until Phase 7 substance lands. |
| **c** | Reject and supply a different figure set. |

**Recommendation: (a)** — it closes F1 immediately, documents the honest
NOT_REPORTED state in a figure reviewers can see, and gives Phase 7 a ready-made
acceptance test.

---

END OF RULE 9 SPEC — awaiting "APPROVED" before any `.py` is written.

