# GPS-Denied UAV Navigation SLR — Master Writing SOP V2
# Refined Binding Reference for Authors and AI Agents

**Document type:** Binding SOP — single source of truth
**Corpus target:** 330 PDFs (V2). Current: 171 (V1). Gap: 159.
**Venue style:** IEEE Transactions on Robotics / IEEE Access (IEEEtran)
**Reporting standard:** PRISMA 2020 + PRISMA-S (search extension)
**Secondary standards:** PRISMA-ScR, MOOSE, Cochrane Handbook, AMSTAR-2, IEEE Editorial Style
**Author:** Abhishek Raj
**Date:** 2026-09-17
**Supersedes:** MASTER_SLR_WRITING_SOP_AND_PROMPT_V1.md (had stale QA numbers 83/81/7, 71/93/7)
**Status:** Binding. Do not modify without version bump.

---

## SECTION 0 — LITERATURE REVIEW STANDARDS COMPLIANCE

| Standard | Role | Where applied |
|----------|------|---------------|
| **PRISMA 2020** | PRIMARY — full reporting checklist | §III Methods, Appendix A |
| **PRISMA-S** | PRIMARY — search reporting extension | §III.B Information sources |
| **PRISMA-A** | PRIMARY — abstract reporting | Abstract |
| **PRISMA-Flow** | PRIMARY — flow diagram | Figure 7, Table I |
| **PRISMA-ScR** | Referenced — scoping review extension | Justifies SLR vs ScR |
| **MOOSE** | Referenced — observational meta-analysis | Not applicable |
| **Cochrane Handbook** | Referenced — risk-of-bias | Rubric design, §III.H |
| **AMSTAR-2** | Referenced — critique prior reviews | §II Related Work |
| **IEEE Editorial Style Manual** | PRIMARY — prose, citations, units | Throughout |
| **IEEE Author Center** | PRIMARY — submission format | §VIII Production |
| **Vancouver / ICMJE** | Referenced — consistency | Citation style |

**Every PRISMA 2020 item must be ticked in Appendix A.**

**This review does NOT claim:**
- Meta-analysis (heterogeneous metrics)
- Scoping review (narrow RQs)
- Living review (single window)
- Umbrella review (primary studies only)

---

## SECTION 1 — HOW TO USE THIS FILE

Give this file to a writing agent with this instruction:

> Follow every rule. Do not invent numbers, DOIs, datasets, or performance
> values. Use only Canonical Numbers and CSVs listed under Authoritative
> Inputs. Treat the current 171-paper set as Version-1. Final corpus
> is 330 papers (Version-2). Stop downloading at 330.

### 1.1 Authoritative inputs

| File | Role |
|------|------|
| `02_data_processed/extracted_master_v2.csv` | All quantitative claims |
| `02_data_processed/screened_included_v2.csv` | 636 included records |
| `02_data_processed/deduplicated_master.csv` | 1,719 unique records |
| `02_data_processed/qa_distribution_v2.csv` | QA × citation breakdown |
| `00_scope/PROTOCOL.md` | RQ1–RQ4, PICOC |
| `00_scope/screening_criteria_v2.md` | I1–I6 / E1–E8 |
| `00_scope/quality_appraisal_rubric.md` | 0–10 rubric |
| `06_analysis/output/figures_v2/` | 9 figures @ 300 DPI |
| `08_docs/PDF_EXTRACTION_AUDIT_PROTOCOL.md` | Extraction verification |
| `08_docs/extraction_validation_status_v1.json` | Human validation status |

### 1.2 Forbidden legacy numbers

- 1,692 included papers
- 1,700 extracted rows
- 1,332 IMU papers (78%)
- 495 EW papers (29%)
- 98.4% inclusion rate

These belong only in a "superseded v1 screening" footnote.

---

## SECTION 2 — CANONICAL NUMBERS (V2)

### 2.1 Fixed upstream

| Symbol | Value | Meaning |
|--------|------:|---------|
| RAW | 2,000 | IEEE 1,000 + Scopus 1,000 |
| DEDUP | 1,719 | After dedup |
| DUPES | 281 | 14.1% removal |
| INCLUDED | 636 | Stage-1 v2 screening (37.0%) |
| EXCLUDED | 1,083 | v2 exclusions |
| WINDOW | 2010-01-01 → 2026-06-30 | Search window |

### 2.2 Corpus version

| Symbol | V1 | V2 target | Meaning |
|--------|----:|----------:|---------|
| FULLTEXT | 171 | **330** | PDFs extracted |
| COVERAGE | 26.9% | **51.9%** | FULLTEXT / 636 |
| NOT_RETRIEVED | 465 | **306** | No PDF |

### 2.3 Extraction output

| Symbol | V1 value | Meaning |
|--------|---------:|---------|
| Q-HIGH | **38** | qa_total ≥ 8 |
| Q-MED | **84** | qa_total 5–7 |
| Q-LOW | **49** | qa_total 0–4 |
| CORE | **35** | citation_tier = Core |
| IMPORTANT | **87** | citation_tier = Important |
| PERIPHERAL | **49** | citation_tier = Peripheral |
| CORE+IMP | **122** | Core ∪ Important |
| REAL | **22** | Real_World |
| SIM | **78** | Simulation |
| BOTH | **71** | Both |

**All values update when corpus grows. Recompute from CSV.**

---

## SECTION 3 — CORPUS VERSIONING AND STOP RULE

### 3.1 Why 330

| Corpus | Coverage | Reviewer signal | Cost |
|-------:|---------:|-----------------|------|
| 171 | 26.9% | "Insufficient" | Done |
| **330** | **51.9%** | **"Strong"** | +4 hrs downloads |
| 480 | 75% | "Comprehensive" | +10 hrs |
| 636 | 100% | Impossible (paywalls) | ~40 hrs |

### 3.2 STOP RULE

**Stop downloading at 330.** Do not exceed.

### 3.3 Version labels

| Label | N | Used in |
|-------|--:|---------|
| Version-1 (V1) | 171 | Current manuscript |
| Version-2 (V2) | 330 | Target manuscript |
| Version-3 (V3) | ≤636 | Only if reviewers require |

Every draft states version and N in: abstract, first Results paragraph, every figure caption. Do not mix versions.

---

## SECTION 4 — RESEARCH QUESTIONS AND PICOC

### RQ1
What localization and navigation methods have been proposed for UAVs in GPS-denied environments during 2010–2026?

### RQ2
Which sensor modalities and fusion strategies are most commonly used, and how has their prevalence changed over time?

### RQ3
In what operational environments have these methods been validated, and what is the real-world vs. simulation ratio?

### RQ4
What are the open research challenges, particularly for adversarial / EW scenarios?

### PICOC

| Element | Definition |
|---------|------------|
| Population | UAVs: fixed-wing, rotary, hybrid |
| Intervention | Localization without GPS/GNSS |
| Comparison | Method families, sensors, time periods |
| Outcome | Accuracy, drift, compute, validation, sensor load |
| Context | Indoor, urban, underground, forest, EW, maritime |

---

## SECTION 5 — BACKGROUND: HISTORY 2010–2026

(Introduction's historical narrative. Background context — do not assign corpus percentages unless computed from `year`.)

### 5.1 Why GPS denial became a problem

Denial occurs by:
- **Natural blockage:** indoor, underground, canopy, urban canyon
- **Degradation:** multipath, NLOS, ionospheric
- **Adversarial:** jamming, spoofing

2010–2018: indoor robotics dominated.
2022 onward: contested airspace, EW (Ukraine), alt-PNT.

### 5.2 Pre-2010 ancestry (background, not corpus)

| Lineage | Idea | Relevance |
|---------|------|-----------|
| Strapdown INS | Integrate IMU | Substrate of nearly all stacks |
| TERCOM (1960s–80s) | Terrain contour matching | Ancestor of DEM-relative nav |
| DSMAC (1980s) | Optical scene matching | Ancestor of visual geo-localization |
| Visual odometry | Camera-only motion | Basis of VIO |
| Early MAV indoor (2000s) | Optical flow, laser | Direct UAV precursor |

### 5.3 Era 1 — 2010–2013: Feasibility
Monocular/stereo VO, EKF fusion, optical flow, UWB labs. Limitations: scale drift, no outdoor geo-reference.

### 5.4 Era 2 — 2014–2016: SLAM usable
ORB-SLAM, LSD-SLAM, DSO, LOAM. EuRoC MAV benchmark released 2016.

### 5.5 Era 3 — 2017–2019: VIO substrate
Tight IMU-camera coupling. Filter (MSCKF) vs optimization (VINS-Mono, OKVIS, OpenVINS). Stereo for metric scale.

### 5.6 Era 4 — 2020–2021: LiDAR-inertial
FAST-LIO, LIO-SAM, ORB-SLAM3, thermal/event cameras. Jetson compute standard.

### 5.7 Era 5 — 2022–2023: Adversarial + learning
Jamming/spoofing as mission condition. DL odometry. NeRF. 5G. Swarm (mostly sim).

### 5.8 Era 6 — 2024–2026: Geo-localization
UAV-to-satellite cross-view, 3DGS SLAM, transformers, BIM/HD-map, dust/tunnel/maritime. Gap: sim-heavy.

### 5.9 Prior surveys

- Chang et al. 2023, RAS
- Jarraya et al. 2025, Satellite Navigation
- Cadena 2016 LiDAR-SLAM
- GNSS-denied UAV surveys 2020–2024

**This paper's difference:** PRISMA v2 screening (636), transparent subset (V1: 171 / V2: 330), documented 0–10 rubric, citation-tier weighting.

---

## SECTION 6 — MANUSCRIPT STRUCTURE

```
Title
Author block
Abstract (150–250 words, PRISMA-A)
Keywords (5–8)

I.   Introduction
     A. Operational motivation
     B. Historical evolution 2010–2026
     C. Gap vs prior surveys
     D. Numbered contributions
     E. Organisation

II.  Related Work
     A. Prior SLRs
     B. Canonical families

III. Review Protocol and Methods
     A. RQs and PICOC
     B. Information sources (PRISMA-S)
     C. Eligibility (I1–I6, E1–E8)
     D. Deduplication
     E. Screening (v2, band 25–45%)
     F. Full-text coverage
     G. Extraction schema
     H. Quality rubric 0–10
     I. Citation tiers
     J. Corpus versioning
     K. Reproducibility

IV.  Results
     A. PRISMA (Fig. 7)
     B. Publication trends (Fig. 1)
     C. Platforms (Fig. 2)
     D. Method taxonomy (Figs. 4, 8)
     E. Sensors (Fig. 5)
     F. Environments/apps (Figs. 3, 6)
     G. Real vs simulation
     H. Quality tiers
     I. Multi-agent
     J. Metrics honesty

V.   Discussion
     A–F (RQ1–RQ4 + sim-to-real + EW language)

VI.  Limitations
     A. Coverage
     B. Machine-assisted extraction
     C. Human validation status
     D. Databases
     E. Language
     F. Multi-label inflation

VII. Conclusion

Data availability
Conflicts / Funding
References (IEEE numbered)
Appendix A. PRISMA 2020 checklist
Appendix B. Search strings
Appendix C. QC audit
Appendix D. Version log
```

### Title

> Autonomous Navigation and Localization for Unmanned Aerial Vehicles in GPS-Denied Environments: A Systematic Literature Review

### Abstract formula

1. Context (1 sentence)
2. Objective (1)
3. Data sources (1)
4. Eligibility (1)
5. Methods (1–2)
6. Results with N (1–2)
7. Limitations (1)
8. Conclusions (1)

Must state: 2,000 → 1,719 → 636 → N, coverage %, PRISMA 2020.

### Keywords

`UAV`, `GPS-denied`, `GNSS-denied`, `visual-inertial odometry`, `LiDAR SLAM`, `sensor fusion`, `systematic literature review`, `PRISMA`, `electronic warfare`, `localization`

---

## SECTION 7 — STYLE SOP

1. **Traceability.** Every number with numerator/denominator: "38/171 (22.2%) were Q-high".
2. **Coverage honesty.** Always state N in every sentence about percentages.
3. **Tense.** Past for review methods; present for established science.
4. **Voice.** Impersonal; "we screened" sparing.
5. **No superlatives** without data.
6. **UNKNOWN/NOT_REPORTED** must be stated, never invented.
7. **Multi-label fields** captioned "not mutually exclusive".
8. **Heuristic extraction warning** in limitations.
9. **Version framing** in abstract, first Results para, every caption.
10. **Do not mix v1/v2 screening.**
11. **Paragraphs** 4–7 sentences, one idea.
12. **Acronyms** expanded at first use.
13. **Spelling** American English.
14. **Units** SI, thin space in LaTeX.
15. **Citations** IEEE numbered, [3]–[5] clusters.

---

## SECTION 8 — TABLES (mandatory)

### Table I — PRISMA flow

| Stage | n |
|-------|--:|
| Records identified | 2,000 |
| Duplicates removed | 281 |
| After dedup | 1,719 |
| Excluded at title/abstract | 1,083 |
| Included | 636 |
| Full texts not retrieved | 306 |
| **Full texts extracted (V2)** | **330** |

### Table II — Quality × citation tier

Regenerate from `qa_distribution_v2.csv`.

### Table III — Experiment type

Regenerate from CSV.

### Table IV — Method categories
Compute from `method_category`.

### Table V — Sensors (multi-label)
Split `sensor_list` on `;`.

### Table VI — Environments (multi-label)
Split `environment` on `;`.

### Table VII — Era × method
Group `year` into six eras, crosstab with `method_category`.

---

## SECTION 9 — FIGURES (mandatory)

All in `06_analysis/output/figures_v2/`, 300 DPI, colourblind-safe.

| Fig | File | Shows |
|-----|------|-------|
| 1 | fig01_publication_trends.png | Papers/year |
| 2 | fig02_platform_distribution.png | Platforms |
| 3 | fig03_environment_distribution.png | Environments |
| 4 | fig04_method_evolution.png | Methods over years |
| 5 | fig05_sensor_frequency.png | Sensors |
| 6 | fig06_application_domains.png | Applications |
| 7 | fig07_prisma_flow.png | PRISMA flow |
| 8 | fig08_method_environment_heatmap.png | Co-occurrence |
| 9 | fig09_research_maturity_radar.png | QA / maturity |

**Caption template:**
> Fig. 4. Evolution of primary method categories by publication year in the Version-2 full-text corpus (N = 330). Machine-assisted labels; not extrapolated to 636.

---

## SECTION 10 — BIBLIOGRAPHIC FORMAT (IEEE)

- In-text: [1], [2], [3]–[6]
- "Vanegas *et al.* [12] proposed…"
- No author–year format.

### BibTeX rules
- Every cited paper's DOI from master CSV.
- Full 330 in supplementary.
- Brace-protect `{UAV}`, `{GPS}`, `{GNSS}`, `{SLAM}`, `{IMU}`.
- No invented DOIs.
- PRISMA 2020: Page MJ et al., BMJ 2021;372:n71.
- PRISMA-S: Rethlefsen ML et al., Syst Rev 2021;10:39.

---

## SECTION 11 — LATEX PRODUCTION

```latex
\documentclass[journal]{IEEEtran}
\usepackage{cite}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath,amssymb}
\usepackage{url}
\usepackage{hyperref}
\usepackage[caption=false,font=footnotesize]{subfig}
\graphicspath{{../06_analysis/output/figures_v2/}}
```

Build:
```
pdflatex <file>.tex
bibtex   <file>
pdflatex <file>.tex
pdflatex <file>.tex
```

Prerequisite: MiKTeX or TeX Live.

Pre-flight: fonts embedded, no Type 3, US Letter, metadata correct.

---

## SECTION 12 — QUALITY CONTROL AUDIT (Appendix A)

Fill every draft. Any FAIL = not submission-ready.

| # | Check | Status |
|---|-------|--------|
| 1 | PRISMA numbers = 2000/1719/636/1083/N | PASS/FAIL |
| 2 | Coverage = N/636 with % | PASS/FAIL |
| 3 | No 1692/1700/1332/495 as current | PASS/FAIL |
| 4 | All % have num/denom | PASS/FAIL |
| 5 | Multi-label captions | PASS/FAIL |
| 6 | ATE not invented | PASS/FAIL |
| 7 | Human validation status stated | PASS/FAIL |
| 8 | DOIs of cited papers in CSV | PASS/FAIL |
| 9 | Figures 1–9 in order | PASS/FAIL |
| 10 | Evolution in Intro + Fig. 4 / Table VII | PASS/FAIL |
| 11 | Limitations include machine-assisted extraction | PASS/FAIL |
| 12 | Corpus version in abstract | PASS/FAIL |
| 13 | V1/V2 not mixed | PASS/FAIL |
| 14 | PDF audit log committed | PASS/FAIL |
| 15 | PRISMA 2020 27-item checklist complete | PASS/FAIL |
| 16 | PRISMA-S search items present | PASS/FAIL |
| 17 | STOP rule documented (330) | PASS/FAIL |

---

## SECTION 13 — PDF EXTRACTION AUDIT PROTOCOL

**Purpose:** Detect shallow/stubbed/fabricated extraction.
**Applies to:** `16_execute_phase7_extraction.py` output.
**Frequency:** After every re-extraction.

### Five checks

**Check 1 — PDF Open.** Every PDF opened with PyMuPDF; notes field has distinctive phrase. PASS: ≥95%.

**Check 2 — Field-Text Correlation.** Sample 20 (seed 42). Method/sensor labels appear in PDF. PASS: ≥90%.

**Check 3 — QA Justification.** qa_rigor ≥ 3 → ground-truth keyword. qa_baseline ≥ 1 → named baseline. PASS: all scored have trigger.

**Check 4 — Distribution.** Q-high 15–25%, Q-low 20–35%, Core 15–25%. PASS: bounds met.

**Check 5 — Manual 5-Paper Spot Check.** Open 5 random PDFs. PASS: ≥4/5 match.

**Report:** `08_docs/extraction_audit_report.md`

---

## SECTION 14 — HUMAN VALIDATION

| Audit | Human validation |
|-------|------------------|
| Automatic | Manual |
| Verifies PDFs read | Verifies labels correct |
| Detects fabrication | Detects bias |
| 2 min | 45 min |

**Status:** REVIEW REQUIRED (0/20 filled). Both required for publication.

---

## SECTION 15 — MASTER AGENT PROMPT

```
You are a senior robotics researcher writing a PRISMA 2020 + PRISMA-S
systematic literature review for IEEE T-RO / IEEE Access.

TOPIC
Autonomous navigation and localization for UAVs in GPS/GNSS-denied
environments (2010–2026).

BINDING DATA (V2)
- 2,000 raw (IEEE 1,000 + Scopus 1,000)
- 1,719 unique (281 duplicates removed, 14.1%)
- 636 included after v2 screening (37.0%)
- 1,083 excluded
- 171 V1 / 330 V2 PDFs (51.9% coverage). STOP at 330.
- QA: Q-high 38, Q-medium 84, Q-low 49
- Tiers: Core 35, Important 87, Peripheral 49
- Experiment: Real 22, Simulation 78, Both 71

NEVER: 1,692, 1,700, 1,332, 495, 98.4%.

AUTHORITATIVE FILE
02_data_processed/extracted_master_v2.csv is the ONLY source for counts.

TASK
Write a complete IEEE-style survey in Markdown.

STRUCTURE
Title; authors; PRISMA-A abstract (150-250 words); Keywords;
I Introduction with six-era evolution + gap + contributions;
II Related work;
III Methods (PICOC, RQ1-RQ4, I1-I6/E1-E8, dedup, screening, coverage,
  extraction, rubric, tiers, versioning, reproducibility);
IV Results (PRISMA, trends, platforms, methods, sensors, environments,
  real vs sim, quality, multi-agent, metrics honesty);
V Discussion (RQ1-RQ4 + sim-to-real + EW);
VI Limitations (coverage, machine-assisted extraction, validation status);
VII Conclusion; Data availability; References; Appendices A-D.

FIGURES (9, captions state N)
TABLES (I-VII)

STYLE
IEEE impersonal, past tense for methods, n/N stats, multi-label captions,
no superlatives, no fabricated citations, version framing mandatory.

OUTPUT
1) Full Markdown manuscript
2) Figure captions
3) Table sources
4) PRISMA 2020 27-item checklist
5) QC audit table filled
6) TODO_FROM_CSV for anything not computable
```

---

## SECTION 16 — RE-RUN POLICY (171 → 330)

1. Add PDFs to `05_papers_fulltext/`.
2. Run `16_execute_phase7_extraction.py`.
3. Run `17_audit_extraction.py --check=all`.
4. If PASS, proceed.
5. Recompute Tables II–VII.
6. Regenerate figures.
7. Replace N and coverage everywhere.
8. Delete V1 numbers.
9. Bump to V2.
10. Commit with tag `v2-corpus-330`.

---

## SECTION 17 — HUMAN TASKS OPEN

| Task | Status |
|------|--------|
| Download 159 more PDFs | OPEN |
| Fill 20-row validation sample | REVIEW REQUIRED |
| Install MiKTeX | PENDING |
| Compile PDF | PENDING |
| Language edit | HUMAN |
| Submit | HUMAN |

---

## SECTION 18 — CHEAT SHEET

**Target:** 330 PDFs. Current: 171. Gap: 159. STOP at 330.
**Standards:** PRISMA 2020 + PRISMA-S + PRISMA-A + IEEE Style.
**Format:** IEEE two-column IEEEtran, Markdown first.
**Story:** Indoor VO (2010) → VIO (2017) → LIO (2020) → EW + learning + geo (2022–2026).
**Never:** 1692, 1700, 1332, 495, invented ATE.

End of MASTER_SLR_WRITING_SOP_V2.md
