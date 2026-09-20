# Manuscript Specification — GPS_Denied_SLR

## Target venue
IEEE Transactions on Robotics (T-RO) or IEEE Access.

## Structure
1. Abstract (200 words max)
2. Introduction (1.5 pages)
3. Related Work (2 pages)
4. Methodology — PRISMA 2020 (1.5 pages)
5. Results (4 pages)
6. Discussion (2 pages)
7. Limitations (0.5 page)
8. Conclusion (0.5 page)
9. References (IEEE style)

## Required figures
| # | Figure | Source data |
|---|---|---|
| F1 | PRISMA flow diagram | 08_docs/PRISMA_FLOW.md |
| F2 | Publications per year | MASTER_EVIDENCE year column |
| F3 | Sensor distribution | MASTER_EVIDENCE sensors column |
| F4 | Method category distribution | MASTER_EVIDENCE method_category |
| F5 | Environment distribution | MASTER_EVIDENCE environment |
| F6 | Taxonomy pie (Core/Important/Peripheral) | MASTER_EVIDENCE taxonomy_category |
| F7 | Real vs Sim breakdown | MASTER_EVIDENCE real_or_sim |
| F8 | Geographic distribution | MASTER_EVIDENCE country |
| F9 | Performance metrics scatter (if applicable) | MASTER_EVIDENCE metrics + headline_result |

## Required tables
| # | Table | Source |
|---|---|---|
| T1 | Inclusion/exclusion criteria | 00_scope/ |
| T2 | Evidence matrix (all 285 papers) | MASTER_EVIDENCE |
| T3 | Method comparison summary | derived |
| T4 | Key results summary | derived |
| T5 | Excluded papers with reasons | screening_results.csv |

## Writing rules
- Every number in the text must appear in NUMBER_TRACE.md.
- No number may be a rounded version of another.
- No forbidden legacy numbers.
- Every claim must be defensible from MASTER_EVIDENCE.csv.
- Every figure must regenerate from a script in 06_analysis/scripts/.

## PRISMA 2020 checklist
Map every PRISMA item (1-27) to a page in the manuscript.
Store mapping in 08_docs/PRISMA_CHECKLIST.md.

## Citation style
IEEE numeric. Use the DOI where possible.

## Word limit
IEEE T-RO: 12 pages including references.
IEEE Access: 15 pages.

## Tone
Third person, past tense for methods, present tense for findings.
No first-person singular. Avoid "we believe".
