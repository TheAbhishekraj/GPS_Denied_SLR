# MASTER_PAPER_TEMPLATE.md
# Canonical per-paper summary template for GPS_Denied_SLR V1

Purpose: every paper in the V1 corpus (N = 171) is rendered into this template
as a standalone file at `03_extraction/per_paper/<id>.md`. This template is
also the column plan for `02_data_processed/MASTER_EVIDENCE_V1.csv`.

Rules:
- Every field is filled. If the paper does not report it, write `NOT_REPORTED`.
- Never guess. If a value is paraphrased from a figure without a table, mark
  `extraction_source` with the figure number and note the uncertainty in `notes`.
- `[id]` is the join key to `extracted_master_v2.csv`. Do not rename it.

---

## 0. Identity

| Field | Value |
|---|---|
| id | `[REC_XXXX]` |
| authors | `[full author list, comma-separated, initials + surname]` |
| title | `[exact title]` |
| year | `[YYYY]` |
| venue | `[journal / conference full name]` |
| venue_type | `[journal / conference / preprint / thesis]` |
| doi | `[DOI or NOT_REPORTED]` |
| url | `[URL or NOT_REPORTED]` |

## 1. Abstract summary

Two to four sentences. Own words. Must preserve any numeric claim the abstract
itself makes (e.g., "reports 0.3 m ATE"). Do not add interpretation.

> [abstract_summary]

## 2. Problem setting

What denial scenario does the paper address? Choose one and expand:
- GNSS absence (urban canyon, indoor, tunnel, forest, underground, maritime)
- GNSS jamming
- GNSS spoofing
- Degraded GNSS (intermittent, multipath)
- Adversarial / electronic warfare
- General GNSS-denied assumption (no specific scenario)

> [problem_setting — 2–3 sentences]

## 3. Historical context

Where does this paper sit in the 2010–2026 timeline? What prior work does it
build on, cite, or explicitly replace? Name 2–4 prior methods the paper itself
mentions (e.g., ORB-SLAM, VINS-Mono, LIO-SAM, Cartographer). This becomes the
input to the evolution narrative.

> [historical_context — 3–5 sentences]

## 4. Methodology (summarized)

- **Approach family:** [VIO / LiDAR-inertial / filter / factor-graph / radio /
  map-based / learning-assisted / hybrid / other]
- **Named method:** [specific method name if any, else NOT_REPORTED]
- **Core idea (2 sentences):** [core_idea]
- **Algorithmic components:** [list 3–6 components: e.g., "MSCKF filter,
  loop closure, IMU preintegration, map-based correction"]
- **Fusion strategy:** [loosely-coupled / tightly-coupled / switchable /
  NOT_REPORTED]
- **Any learning used:** [none / feature learning / depth / policy / other]

## 5. Sensors and hardware

| Field | Value |
|---|---|
| sensors_used | [IMU; Monocular_Camera; Stereo_Camera; LiDAR; Radar; UWB; Barometer; Magnetometer; Optical_Flow; Sonar; GPS_(for init only); Other] |
| sensor_fusion_count | [integer] |
| hardware_platform | [specific airframe, e.g., DJI M300, custom quadrotor, simulator] |
| compute_onboard | [Jetson Xavier / NUC / Raspberry Pi / offboard / simulation-only / NOT_REPORTED] |
| flight_time_or_trajectory_length | [value + unit, or NOT_REPORTED] |

## 6. Experimental setup

| Field | Value |
|---|---|
| environment_tested | [verbatim from paper: e.g., "indoor warehouse", "urban canyon", "tunnel", "simulation only"] |
| environment_category | [Indoor / Urban / Underground / Forest / Maritime / Adversarial_EW / Mixed / Simulation_Only] |
| real_or_sim | [Real_World / Simulation / Both] |
| dataset_used | [name, or "custom", or NOT_REPORTED] |
| ground_truth_method | [motion capture / RTK / surveyed landmarks / simulation truth / manual / NOT_REPORTED] |
| number_of_runs | [integer or NOT_REPORTED] |

## 7. Reported performance (numeric, verbatim)

Only fill what the paper actually reports. If the paper reports a table, cite it.
If it reports only a figure, note "from Fig. X". If nothing numeric is reported,
mark every value `NOT_REPORTED`.

| Metric | Value | Unit | Source (table/figure/section) |
|---|---|---|---|
| best_ate_rmse | | m | |
| best_rpe | | m or deg | |
| drift_rate | | % of distance | |
| success_rate | | % | |
| improvement_vs_baseline | | % | |
| other_metric_name | | | |

## 8. Baseline comparison

| Field | Value |
|---|---|
| baseline_compared | [name(s), or NONE_REPORTED] |
| baseline_type | [classical / learned / ablation-only / none] |
| head_to_head_result | [paper's method wins / loses / comparable / NOT_REPORTED] |

## 9. Novelty claim (verbatim from paper)

Extract the authors' own contribution statement. Quote if under 30 words; else
paraphrase and mark `[paraphrase]`.

> [claimed_novelty]

## 10. Reported failure modes

List conditions under which the paper itself says the method fails or degrades.

- [failure_mode_1]
- [failure_mode_2]
- [failure_mode_3 if any]

## 11. Stated limitations (authors' own)

Quote or paraphrase the "Limitations" / "Discussion" section. If none stated,
write `NOT_STATED`.

> [stated_limitations]

## 12. Stated future work

Quote or paraphrase the "Future work" section. If none, `NOT_STATED`.

> [stated_future_work]

## 13. Quality appraisal (from extracted_master_v2.csv)

| Dimension | Score | Max |
|---|---|---|
| qa_rigor | | 4 |
| qa_reporting | | 3 |
| qa_baseline | | 2 |
| qa_reproducibility | | 1 |
| **qa_total** | | **10** |
| qa_tier | [Q-high / Q-medium / Q-low] | |
| citation_tier | [Core / Important / Peripheral] | |

## 14. Extraction provenance

| Field | Value |
|---|---|
| extraction_source | [pages / tables / sections used] |
| extractor | [AI / AR / other] |
| verified_by_human | [Y / N] |
| verifier_initials | [ ] |
| verification_date | [ ] |
| notes | [any caveat about uncertain extraction] |

## 15. Cross-references for the manuscript

- Which RQ does this paper inform? [RQ1 / RQ2 / RQ3 / RQ4 / multiple]
- Which manuscript table will cite it? [Table II / III / IV / V / …]
- Which manuscript figure will cite it? [Fig. 1 / 2 / …]

---

End of template. Populate one file per paper at `03_extraction/per_paper/<id>.md`.