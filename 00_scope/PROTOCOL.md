# PROTOCOL.md — SLR Research Protocol
# GPS_Denied_SLR: Autonomous Navigation and Localization for UAVs in GPS-Denied Environments
# PRISMA 2020 Compliant | Author: Abhishek Raj | Target: IEEE Transactions on Robotics / IEEE Access

---

## 1. Research Questions

| ID | Research Question |
|----|------------------|
| **RQ1** | What localization and navigation methods have been proposed for UAVs in GPS-denied environments during 2010–2026? |
| **RQ2** | Which sensor modalities and fusion strategies are most commonly used, and how has their prevalence changed over time? |
| **RQ3** | In what operational environments (indoor, urban, adversarial/EW, underground, forest, underwater) have these methods been validated, and what is the real-world vs. simulation experiment ratio? |
| **RQ4** | What are the open research challenges and future directions in GPS-denied UAV navigation, particularly for adversarial/electronic-warfare scenarios? |

---

## 2. PICOC Framework

| Element | Definition |
|---------|-----------|
| **Population** | Unmanned Aerial Vehicles (UAVs/drones): fixed-wing, rotary-wing (multirotor), and hybrid platforms |
| **Intervention** | Localization and navigation methods operating without GPS/GNSS signals (denied, degraded, or jammed) |
| **Comparison** | Comparison across method categories (SLAM, VIO, filter-based, learning-based, radio-based, etc.) and across time periods (2010–2026) |
| **Outcome** | Localization accuracy (m/cm), drift rate (%), computational cost, real-world validation status, sensor requirements |
| **Context** | GPS-denied operational environments: indoor, urban canyons, underground, forest, adversarial/EW, underwater |

---

## 3. Inclusion Criteria (ALL must be satisfied)

| # | Criterion |
|---|-----------|
| **IC1** | Platform is a UAV/drone (fixed-wing, rotary-wing, or hybrid); ground/surface/underwater UxVs included only if UAV platform comparison is explicitly present |
| **IC2** | GPS/GNSS denied, degraded, or jammed is a **core focus** of the paper (not a peripheral assumption) |
| **IC3** | Presents experimental or simulation results with quantitative localization/navigation metrics |
| **IC4** | Peer-reviewed publication (journal article or conference paper) |
| **IC5** | Published between 2010-01-01 and 2026-06-30 |
| **IC6** | Written in English |

---

## 4. Exclusion Criteria (ANY is sufficient)

| # | Criterion |
|---|-----------|
| **EC1** | Purely theoretical contribution with no experimental or simulation validation |
| **EC2** | GPS/GNSS used as primary navigation sensor (GPS-augmented systems excluded) |
| **EC3** | Paper is out of scope (pure communication, hardware design, orbit mechanics, pedestrian navigation) |
| **EC4** | Duplicate after deduplication stage |

---

## 5. Quality Assessment Checklist (8 items, each scored 0/0.5/1)

> ⚠ **SUPERSEDED by `00_scope/quality_appraisal_rubric.md` — see `RULINGS.md` R2.**
> This 8-item 0/0.5/1 checklist is **historical only**. The binding rubric is
> `quality_appraisal_rubric.md` (0–10 scale: rigor 0–4, reporting 0–3, baseline
> 0–2, reproducibility 0–1; tiers Q-high 7–10 / Q-medium 4–6 / Q-low 0–3),
> producing the `qa_rigor, qa_reporting, qa_baseline, qa_repro, qa_total,
> qa_tier, qa_notes` columns. Migration equivalence: dimension A ⊇ items 1–3,
> B ⊇ items 4–5, C ⊇ item 6, D  items 7–8. The QA ≥ 3.0/8.0 threshold below is
> **not** in force. Do not score any v2 paper with this checklist.

| # | Quality Item |
|---|-------------|
| **QA1** | Clear statement of GPS-denied/GNSS-denied motivation and problem scope |
| **QA2** | Reproducible description of the proposed method/algorithm |
| **QA3** | Real-world or high-fidelity simulation experimental validation |
| **QA4** | Quantitative performance metrics reported (e.g., RMSE, ATE, drift %) |
| **QA5** | Comparison with at least one baseline or prior method |
| **QA6** | Discussion of limitations or failure modes |
| **QA7** | Sensor hardware specified (model or class) |
| **QA8** | Dataset/environment described with sufficient detail for reproducibility |

*Minimum quality threshold for inclusion: QA-score ≥ 3.0 / 8.0*

---

## 6. Search Timeframe

- **Start:** 2010-01-01
- **End:** 2026-06-30
- **Databases:** IEEE Xplore, Scopus

---

## 7. Screening Process

1. **Deduplication:** DOI-exact match + Levenshtein title fuzzy match (≥ 0.90 threshold)
2. **Title/Abstract Screening:** Applied per IC1–IC6 and EC1–EC4
3. **Double-extraction:** 8 papers received dual extraction (inter-rater reliability check)

---

## 8. PRISMA Flow Numbers

| Stage | Count |
|-------|-------|
| Records identified (IEEE 1,000 + Scopus 1,000) | 2,000 |
| Duplicates removed | 281 (14.1%) |
| Records screened | 1,719 |
| Records excluded after screening | 27 |
| Records included | 1,692 |
| Rows in extracted_master.csv (incl. 8 double-extractions) | 1,700 |
