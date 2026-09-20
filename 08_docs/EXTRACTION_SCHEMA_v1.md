# Extraction Schema v1 — GPS_Denied_SLR

Frozen 2026-09-19. Do not modify without a new schema version.
Every row corresponds to one INCLUDE paper (285 total).
Every field marked QUOTE requires a verbatim quote + page number.

## Column definitions

| # | Column | Type | Required | PDF Source | Quote? |
|---|---|---|---|---|---|
| 1 | id | string | yes | filename REC_XXXX | no |
| 2 | title | string | yes | PDF page 1 | no |
| 3 | authors | string | yes | PDF page 1 | no |
| 4 | year | int | yes | PDF page 1 or venue | no |
| 5 | venue | string | yes | PDF header | no |
| 6 | doi | string | yes | PDF page 1 or metadata | no |
| 7 | problem | string | yes | Abstract + Intro | yes |
| 8 | motivation | string | yes | Intro | yes |
| 9 | gps_denied_type | enum | yes | Abstract or Intro | yes |
| 10 | environment | enum | yes | Experiments section | yes |
| 11 | platform | string | yes | Experiments section | yes |
| 12 | sensors | list | yes | Methods or System | yes |
| 13 | method_category | enum | yes | Methods | yes |
| 14 | algorithm | string | yes | Methods | yes |
| 15 | real_or_sim | enum | yes | Experiments | yes |
| 16 | dataset | string | yes | Experiments | yes |
| 17 | metrics | list | yes | Experiments | yes |
| 18 | headline_result | string | yes | Results or Abstract | yes |
| 19 | baseline | string | yes | Results | yes |
| 20 | ablation | string | optional | Results | yes |
| 21 | limitations | string | yes | Discussion or Conclusion | yes |
| 22 | future_work | string | optional | Conclusion | yes |
| 23 | taxonomy_category | enum | yes | Derived from method | no |
| 24 | contribution_type | enum | yes | Abstract | yes |
| 25 | country | string | optional | Affiliations | no |
| 26 | funding | string | optional | Acknowledgements | no |
| 27 | notes | string | optional | Anywhere | no |
| 28 | _source_pages | string | yes | Comma-separated page numbers | no |

## Allowed values

### gps_denied_type
- INDOOR
- URBAN_CANYON
- JAMMED
- GNSS_SPOOFED
- UNDERGROUND
- FOREST
- MIXED
- NOT_REPORTED

### environment
- INDOOR
- OUTDOOR_URBAN
- OUTDOOR_RURAL
- OUTDOOR_FOREST
- MIXED
- NOT_REPORTED

### method_category (single choice, highest-level technique)
- SLAM
- VIO
- UWB
- LIDAR
- OPTICAL_FLOW
- VISION_OBJECT
- PSEUDOLITE
- COOPERATIVE
- QUANTUM
- HYBRID
- OTHER

### real_or_sim
- REAL
- SIM
- BOTH
- NOT_REPORTED

### taxonomy_category (derived)
- CORE      (the paper's primary contribution is GPS-denied navigation)
- IMPORTANT (GPS-denied is a stated motivation, contribution is adjacent)
- PERIPHERAL (GPS-denied appears as use case, not central)

### contribution_type
- METHOD
- SYSTEM
- DATASET
- BENCHMARK
- SURVEY
- APPLICATION
- THEORY

## Quote anchoring rule
Every field marked QUOTE must contain:
  "<verbatim sentence or phrase from the PDF>" [p.N]
Not a paraphrase. Not a summary. The exact words.

If the field is not present in the PDF, write NOT_REPORTED.
Never leave blank. Never invent.

## Missing data policy
- If the PDF is unreadable: mark the entire row with status UNREADABLE.
- If a required field is not in the PDF: NOT_REPORTED.
- If a field appears in multiple places: use the most specific location
  (Methods > Abstract; Results > Discussion).

## Known open item (flagged at creation, 2026-09-19)
This schema has no quality-appraisal columns. The frozen
00_scope/SCOPE.md Q7 defines a 0-10 QA rubric (dimensions A-D,
Q-high/Q-medium/Q-low tiers, sim-only cap at Q-medium). Whether QA
scores are added to this schema (raising the column count above 28)
or stored in a separate appraisal file is a pending human decision.
Do not resolve silently.
