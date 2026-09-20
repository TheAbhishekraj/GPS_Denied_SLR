# MASTER_EVIDENCE Validation Report
Generated: 2026-09-19T20:00:40Z
Scope: 02_data_processed/MASTER_EVIDENCE.csv vs 08_docs/EXTRACTION_SCHEMA_v1.md
Status: PASS

## Summary
| check | value |
|---|---|
| Rows | 279 |
| Expected | 279 |
| Structure | PASS |
| Duplicate IDs | 0 |
| Empty required fields | 0 |

## Structure detail
- Schema columns (ordered, 28): id, title, authors, year, venue, doi, problem, motivation, gps_denied_type, environment, platform, sensors, method_category, algorithm, real_or_sim, dataset, metrics, headline_result, baseline, ablation, limitations, future_work, taxonomy_category, contribution_type, country, funding, notes, _source_pages
- Header columns (ordered, 28): id, title, authors, year, venue, doi, problem, motivation, gps_denied_type, environment, platform, sensors, method_category, algorithm, real_or_sim, dataset, metrics, headline_result, baseline, ablation, limitations, future_work, taxonomy_category, contribution_type, country, funding, notes, _source_pages
- Header matches schema exactly (names and order).

## Notes
- Row count is informational at Phase 5 (master is empty by design);
  it becomes an EXIT condition (== 279) at Phase 6 close.
- Structure compares against EXTRACTION_SCHEMA_v1.md (the approved target schema).
