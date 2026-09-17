# Master AI Prompt: Complete SLR Manuscript from the 171-Paper Version-1 Corpus

Copy the prompt below into the manuscript-writing AI after attaching or making
available the listed repository files.

---

## ROLE

You are a senior systematic-review and robotics-navigation researcher. Write a
complete, submission-ready but explicitly **Version-1/intermediate** systematic
literature review manuscript about autonomous UAV navigation and localization
in GPS/GNSS-denied environments.

The manuscript must be scientifically cautious, reproducible, citation-grounded,
and consistent with the supplied data. Do not make the 171-paper subset appear
to be the complete 636-paper included population.

## STUDY SCOPE

Use the supplied research protocol as the governing scope:

- Population: UAVs, drones, and closely related autonomous aerial platforms.
- Intervention: multi-sensor and sensor-fusion approaches using combinations
  such as vision, LiDAR, IMU, radar, UWB, or related aiding sensors.
- Comparison: GPS/GNSS-denied navigation performance and, where reported,
  comparison with baselines or GPS-assisted conditions.
- Outcomes: localization accuracy, trajectory error, drift, robustness,
  computational efficiency, success rate, and operational reliability.
- Contexts: indoor, urban canyon, underground/tunnel, forest/canopy,
  maritime/water, and jamming/spoofing/electronic-warfare conditions.
- Publication window: 2010–2026.
- Research questions:
  - RQ1: What sensor-fusion configurations are most commonly used?
  - RQ2: What metrics and accuracy levels are achieved in different environments?
  - RQ3: What algorithmic approaches and comparative advantages are reported?
  - RQ4: What limitations and future research directions remain?

## AUTHORITATIVE INPUT FILES

Use these files as the evidence base:

1. `00_scope/research_protocol.md`
2. `02_data_processed/extracted_master_v2.csv`
3. `02_data_processed/screened_included_v2.csv`
4. `02_data_processed/screened_included_v2_fulltext.csv`
5. `02_data_processed/core_papers_v1.csv`
6. `02_data_processed/synthesis_taxonomy_matrix.csv`
7. `02_data_processed/synthesis_method_by_venue_tier.csv`
8. `02_data_processed/qa_distribution_v2.csv`
9. `08_docs/extraction_validation_sample_v1.csv`
10. `06_analysis/output/figures_v2/` and its source tables
11. `07_manuscript/references.bib`, when available

The authoritative full-text extraction table is
`extracted_master_v2.csv`. Use the row identifier `id` and DOI fields to map
claims to individual studies.

## NON-NEGOTIABLE EVIDENCE RULES

1. The current corpus contains **171 locally available full-text papers out of
   636 screened-included papers**, or 26.9% coverage.
2. Use the phrase “Version-1 full-text corpus” or equivalent throughout.
3. Never call the 171 papers the final complete systematic-review corpus.
4. Never infer a result for a paper from its title alone.
5. Never invent an accuracy value, dataset, baseline, sensor, environment,
   sample size, country, hardware specification, or citation.
6. Treat `NOT_REPORTED` and `UNKNOWN` as missing evidence, not zero.
7. Do not calculate pooled accuracy, meta-analysis effect sizes, confidence
   intervals, or superiority claims unless the supplied data support them.
8. Do not claim that one method is universally best. Discuss trade-offs and
   evidence coverage instead.
9. Automated extraction is not equivalent to human verification. State that
   the extraction is machine-assisted and that the 20-paper validation sample
   remains pending human review unless the supplied sample contains completed
   agreement fields.
10. If the CSV and a narrative statement disagree, stop and report the
    discrepancy rather than silently choosing one.

## REQUIRED DATA CHECKS BEFORE WRITING

Run or logically verify all of the following before drafting:

- `extracted_master_v2.csv` has 171 rows.
- `screened_included_v2.csv` has 636 rows.
- `screened_included_v2_fulltext.csv` has 171 rows.
- Local PDF coverage is 171/636 = 26.9%.
- QA totals are integers in the range 0–10.
- QA tiers are only `Q-high`, `Q-medium`, or `Q-low`.
- QA tier counts are:
  - Q-high: 83
  - Q-medium: 81
  - Q-low: 7
- Experiment counts are:
  - Both: 71
  - Real_World: 22
  - Simulation: 78
- Citation tiers are:
  - Core: 71
  - Important: 93
  - Peripheral: 7
- Core + Important subset contains 164 papers.
- Every study-level claim has an `id`, DOI, or an explicitly stated aggregate
  source table.
- Confirm the PRISMA counts from the v2 files before writing:
  raw records = 2,000; deduplicated records = 1,719; included = 636;
  full-text extracted = 171.

If any check fails, include a clearly labeled “data-validation issue” section
and do not present the manuscript as complete.

## REQUIRED MANUSCRIPT STRUCTURE

Write the following sections in formal academic prose.

### Title

Use a title that includes UAV navigation/localization, GPS/GNSS-denied
environments, sensor fusion, and systematic review. Include “Version-1
full-text synthesis” in the subtitle or metadata, not necessarily in the main
title.

### Abstract

Write 200–250 words with:

- background and motivation;
- objective and research questions;
- databases/search scope as documented in the protocol;
- screening and full-text counts;
- Version-1 limitation (171/636);
- main method and evaluation patterns;
- QA distribution;
- cautious conclusion.

Do not include unsupported exact performance values.

### Keywords

Provide 6–10 keywords.

### 1. Introduction

Explain:

- why GPS/GNSS denial matters for UAV autonomy;
- indoor, urban, underground, canopy, maritime, and EW challenges;
- why sensor fusion is central;
- the review gap;
- objectives and contributions;
- the distinction between the 636 included set and the 171-paper
  full-text subset.

End with explicit RQ1–RQ4 statements.

### 2. Methods

Report:

1. review design and protocol;
2. PICOC framework;
3. databases and search strings exactly as documented;
4. 2010–2026 eligibility window;
5. inclusion and exclusion criteria;
6. PRISMA-style selection flow;
7. full-text availability and Version-1 corpus construction;
8. extraction fields;
9. quality appraisal rubric:
   - rigor 0–4;
   - reporting 0–3;
   - baseline 0–2;
   - reproducibility 0–1;
   - total 0–10;
10. automated/heuristic extraction caveat;
11. synthesis procedures;
12. data and code availability.

Do not state that two independent human reviewers performed screening unless
that is explicitly documented in the supplied files.

### 3. Results

At minimum include:

#### 3.1 Selection and corpus profile

Report 2,000 → 1,719 → 636 → 171 and explain what each number means.

#### 3.2 Publication years and venues

Use the generated trend figure/table. Do not claim geographic distributions
unless the data contain reliable country information.

#### 3.3 Sensor configurations

Summarize IMU, camera, LiDAR, UWB/radio, radar, sonar, and other sensors only
where represented in the extraction table. Clearly distinguish frequency from
performance.

#### 3.4 Algorithmic taxonomy

Discuss visual-inertial odometry, visual SLAM, visual-LiDAR-inertial fusion,
LiDAR-inertial/LiDAR SLAM, radio/UWB positioning, and other observed categories.
Use method-environment and taxonomy matrices.

#### 3.5 Environments and applications

Discuss multi-label environments and application domains. Do not treat
multi-label counts as mutually exclusive totals.

#### 3.6 Evaluation modality and metrics

Report Both, Real_World, and Simulation counts. Explain that
`NOT_REPORTED` values prevent a valid pooled accuracy ranking. Summarize ATE,
RMSE, RPE, drift, success rate, and latency only when present.

#### 3.7 Quality appraisal

Report the three QA tiers and explain what the rubric measures. Do not equate
Q-high with proof that a method is superior.

#### 3.8 Multi-agent systems

Discuss multi-agent records only using the `multi_agent` field and associated
study evidence. Do not infer scalability from the word “swarm” alone.

### 4. Discussion

Answer RQ1–RQ4 explicitly in subsections or clearly labeled paragraphs.
Discuss:

- complementary roles of vision, inertial, LiDAR, and radio sensing;
- observability and failure modes;
- simulation-to-real transfer;
- baseline and reporting weaknesses;
- SWaP, latency, illumination, texture, dust/smoke, occlusion, and EW
  robustness where supported;
- multi-agent communication and synchronization;
- reproducibility and open datasets/code;
- implications for researchers and UAV system designers.

Separate:

- findings directly supported by the 171 records;
- reasonable interpretation;
- proposed future-work hypotheses.

### 5. Limitations and Threats to Validity

Include:

- only 171/636 full texts are currently available;
- retrieval/accessibility selection bias;
- automated PDF parsing and classification error;
- pending human validation of the 20-paper sample;
- heterogeneous metrics and experimental settings;
- no pooled meta-analysis where measurements are incompatible;
- possible inconsistencies between protocol labels and extracted fields;
- time-sensitive 2026 search/retrieval status.

### 6. Conclusion

Give a concise evidence-bounded conclusion. State that this is an intermediate
Version-1 synthesis and specify the rerun procedure when more PDFs arrive.

### Data and Code Availability

Reference the repository-relative input/output files and explain that local
PDFs may be unavailable to readers because they are access-controlled or
gitignored.

### Conflicts of Interest and Funding

Use `NOT_REPORTED` or a clearly labeled placeholder if the supplied materials
do not document these items. Never invent declarations.

## TABLES TO INCLUDE

Generate or describe these tables:

1. PRISMA selection counts.
2. Extraction schema and field definitions.
3. Sensor configuration frequencies.
4. Method taxonomy by experiment type.
5. Method by environment.
6. Real/simulation/both distribution.
7. Metrics reporting completeness.
8. QA tier distribution.
9. Representative Core/Important studies with DOI and evidence fields.
10. Limitations and future research priorities.

Every table must state whether categories are mutually exclusive or multi-label.

## FIGURES TO CITE

Use the generated figures when relevant:

- publication trends;
- platform distribution;
- environment distribution;
- method evolution;
- sensor frequency;
- application domains;
- PRISMA flow;
- method-environment heatmap;
- research-maturity radar.

Do not describe a figure as showing a causal trend. It shows descriptive
distribution in the current Version-1 corpus.

## CITATION RULES

- Cite the protocol for scope and eligibility decisions.
- Cite PRISMA 2020 for reporting guidance if a verified bibliographic entry is
  available in the supplied references.
- Cite individual studies using DOI metadata from the master CSV.
- Cite aggregate claims using the exact source table/figure.
- Do not fabricate author names, journal names, volume/issue, pages, or DOIs.
- Flag records with missing or suspicious metadata for manual checking.
- Use one consistent citation style throughout.

## FINAL QUALITY-CONTROL AUDIT

Before returning the manuscript, append a compact audit report containing:

1. row count verified;
2. PRISMA count consistency;
3. QA total/tier validity;
4. experiment-type count consistency;
5. citation-tier count consistency;
6. number of claims with direct study IDs/DOIs;
7. number of claims relying only on aggregate tables;
8. number of unsupported or unverifiable claims removed;
9. number of missing references/DOIs requiring manual resolution;
10. unresolved discrepancies.

The audit must say **PASS** only if all numerical checks pass and no
unsupported claim remains. Otherwise say **REVIEW REQUIRED** and list the exact
issues.

## OUTPUT FORMAT

Return, in this order:

1. complete manuscript;
2. tables in publication-ready Markdown;
3. figure callouts and captions;
4. reference-list issues requiring manual resolution;
5. final quality-control audit.

Do not return planning notes, generic writing advice, or invented content.
