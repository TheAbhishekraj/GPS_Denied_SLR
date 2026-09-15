# Quality Appraisal Rubric — GNSS-Denied Navigation SLR

**Applied at:** full-text stage (Stage 2) for every included paper  
**Output:** `quality_score` fields in `02_data_processed/extracted_master.csv`; synthesis is weighted by quality tier

## Scoring (0–10 total)

### A. Experimental Rigor (0–4)

| Points | Criterion |
|---:|---|
| +2 | Real-world experiments on a physical robot/vehicle, not only simulation |
| +1 | Ground-truth comparison against a reference such as RTK-GPS on open runs, motion capture, total station, or a survey-grade map |
| +1 | Repeatability evidence: multiple runs/trials with variance, or public dataset/code |

### B. Reporting Completeness (0–3)

| Points | Criterion |
|---:|---|
| +1 | Reports absolute position error (RMSE/ATE) **and** relative drift (%) |
| +1 | Reports trajectory length, duration, and environment scale |
| +1 | Reports failure modes or ablation analysis |

### C. Baseline Fairness (0–2)

| Points | Criterion |
|---:|---|
| +1 | Compares against at least one established baseline, such as ORB-SLAM3, VINS-Mono, LIO-SAM, or EKF |
| +1 | Baselines are re-implemented or run under matched conditions, rather than copied numbers |

### D. Reproducibility (0–1)

| Points | Criterion |
|---:|---|
| +1 | Code, dataset, or sufficient implementation detail is released |

## Quality tiers

| Tier | Score | Use in synthesis |
|---|---:|---|
| Q-high | 7–10 | Weighted evidence; eligible for Core tier |
| Q-medium | 4–6 | Included in synthesis and flagged in tables |
| Q-low | 0–3 | Reported in corpus statistics; excluded from headline performance claims |

Simulation-only papers can reach Q-medium at best: dimension A is capped at 2/4,
so the maximum tier is Q-medium even if dimensions B–D are perfect.

## Appraisal procedure

Two appraisers independently score 20% of papers. Report ICC(2,1) or weighted
Cohen's kappa, with a target of at least 0.75, before one appraiser proceeds solo.
Resolve disagreements by discussion and document the final score and rationale in
the appraisal worksheet. Apply the final score to every included paper at Stage 2.

The required output columns in `extracted_master.csv` are:

`qa_rigor, qa_reporting, qa_baseline, qa_repro, qa_total, qa_tier, qa_notes`

Performance claims must state: **“N papers (Q-high/Q-medium) informed each claim.”**
Q-low papers remain in PRISMA corpus statistics but are excluded from headline
performance claims.
