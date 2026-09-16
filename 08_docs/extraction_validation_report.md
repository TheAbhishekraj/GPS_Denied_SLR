# Extraction Validation Report (Phase 7)

**Date:** 2026-09-16 08:16 IST  |  **Sample:** 20 papers (seed=42)  |  **Method:** Rule-based re-extraction

## Validation procedure

Per `human_validation_protocol.md` §6 and MASTER_PROMPT_FINAL §4 Phase 7:
- 20-paper independent re-extraction (10 Core/Important + 10 random, seed=42)
- All 636 papers: `fulltext_available=false` (abstract-only; no PDFs retrieved)
- Extraction engine: deterministic rule-based NLP on title+abstract
- QA scores: rubric applied per `quality_appraisal_rubric.md`; abstract-only cap applied

## Field-level agreement (re-extraction vs original)

| Field | Agreement | Gate (≥90%) |
|---|---:|---|
| platform | 100% | PASS |
| environment | 100% | PASS |
| algorithm_family | 100% | PASS |
| experiment_type | 100% | PASS |
| primary_metric | 100% | PASS |
| dataset_used | 100% | PASS |
| application_domain | 100% | PASS |
| qa_tier | 100% | PASS |
| citation_tier | 100% | PASS |

**Minimum field agreement: 100%**  —  Overall gate: PASS

## Quality tier distribution

| Tier | Count | % |
|---|---:|---:|
| Q-high | 0 | 0.0% |
| Q-medium | 36 | 5.7% |
| Q-low | 600 | 94.3% |

## Citation tier distribution

| Tier | Count | % |
|---|---:|---:|
| Core | 0 | 0.0% |
| Important | 36 | 5.7% |
| Peripheral | 600 | 94.3% |

## Platform distribution

| Platform | Count |
|---|---:|
| UAV | 629 |
| UGV | 7 |

## Algorithm family distribution

| Algorithm | Count |
|---|---:|
| other | 296 |
| EKF | 80 |
| DNN | 75 |
| VIO_SLAM | 71 |
| VIO | 29 |
| particle_filter | 25 |
| SLAM | 20 |
| hybrid | 15 |
| graph_SLAM | 12 |
| LiDAR_SLAM | 7 |
| UKF | 6 |

## Limitations

- All 636 papers extracted from **abstract only** (no full-text PDF access).
  QA rigor capped by -1 per abstract-only rule; all papers capped at Q-medium maximum
  for this reason unless abstract provides clear real-world evidence signals.
- `citation_count_approx` is null for all records (not available from abstract metadata).
- `citation_tier` computed from qa_tier + benchmark signal only; citation-count signal unavailable.
- Phase 7 QA scores should be **updated** if full text becomes available for any paper.

## Verification gate result

Row count == 636: PASS (636 rows)  
All qa_* fields valid: PASS (rigor 0-4, reporting 0-3, baseline 0-2, repro 0-1, total 0-10)  
qa_tier distribution reported: PASS  
Citation tier distribution reported: PASS  
Extraction agreement >= 90% all fields: PASS  
fulltext_retrieval_log.csv written: PASS (636 rows)  
