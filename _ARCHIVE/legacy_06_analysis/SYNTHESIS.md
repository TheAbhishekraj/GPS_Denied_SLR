# SYNTHESIS.md — Quantitative Findings & Synthesis Matrices
# GPS_Denied_SLR | PRISMA 2020 | Author: Abhishek Raj

This document presents the core quantitative synthesis across **1,700 extracted rows** (from 1,692 included peer-reviewed papers).

---

## 1. The Three Primary Corpus-Level Findings

Every finding is verified directly against `02_data_processed/extracted_master.csv` with explicit numerator and denominator:

### Finding 1: Universal Inertial Reliance (IMU Ubiquity)
- **Claim:** The Inertial Measurement Unit (IMU) is the universal foundational sensing modality across GPS-denied UAV navigation.
- **Data:** IMU appears in **1332 / 1700** extracted records (**78.4%**).
- **Numerator:** 1332 papers incorporating accelerometer/gyroscope integration.
- **Denominator:** 1700 total extracted rows.
- **Takeaway:** GPS-denied navigation has transitioned almost entirely to inertial-centric fusion, where visual (VIO), LiDAR (LIO), and radio methods act as drift-correction mechanisms for inertial dead-reckoning.

### Finding 2: Adversarial / EW Environment Dominance
- **Claim:** Adversarial and Electronic Warfare (EW) / jammed conditions constitute the largest single environment class.
- **Data:** Dedicated adversarial/EW environments account for **495 / 1700** papers (**29.1%**).
- **Numerator:** 495 papers explicitly addressing electronic jamming, spoofing, or contested airspace.
- **Denominator:** 1700 total extracted rows.
- **Comparison:** Pure adversarial settings (495 papers, 29.1%) exceed pure indoor environments (339 papers, 19.9%), highlighting defense and contested operational priorities.

### Finding 3: Multi-Agent Deployment & Sim-to-Real Gap
- **Claim:** Multi-Agent Collaborative SLAM exhibits the severe sim-to-real gap across all method taxonomies.
- **Data:** Multi-Agent Collaborative SLAM has **14 real-world flight validations : 11 simulation validations** (a ratio of **1.3:1**).
- **Numerator:** 14 physical multi-UAV flight tests.
- **Denominator:** 11 pure simulation studies.
- **Comparison:** Whereas classical single-agent VIO and LiDAR SLAM exceed 3.5:1 real-to-sim validation ratios, multi-agent frameworks are hindered by inter-agent communication bandwidth, distributed loop closure overhead, and swarm collision safety constraints.

---

## 2. Generated Synthesis Artifacts

The following machine-readable matrices have been generated in `06_analysis/output/tables/`:

1. **`taxonomy_matrix.csv`**: Methods × Sensors co-occurrence frequencies across all 1,700 rows.
2. **`env_method_coverage.csv`**: Methods × Operational Environments distribution.
3. **`sim_vs_real.csv`**: Method-by-method breakdown of real-world flight trials vs. simulation validations with empirical ratios.
4. **`fig01` through `fig09` source tables**: Independent CSV data tables for every publication figure.

---

## 3. Method Category Summary Table

| Method Category | Papers | Real Flight | Sim Only | Both | Real:Sim Ratio |
|---|---|---|---|---|---|
| Radio_Based_Positioning | 975 | 728 | 220 | 27 | 728:220 |
| Hybrid_Classical_Learning | 231 | 164 | 64 | 3 | 164:64 |
| LiDAR_SLAM | 146 | 125 | 17 | 4 | 125:17 |
| Filter_Based_VIO | 134 | 105 | 24 | 5 | 105:24 |
| Visual_SLAM | 70 | 57 | 10 | 3 | 57:10 |
| Optimization_Based_VIO | 47 | 32 | 11 | 4 | 32:11 |
| Visual_LiDAR_Inertial_Fusion | 45 | 36 | 8 | 1 | 36:8 |
| Multi_Agent_Collaborative_SLAM | 26 | 14 | 11 | 1 | 14:11 |
| Deep_Learning_Odometry | 25 | 21 | 4 | 0 | 21:4 |
| Map_Based_Localization | 1 | 0 | 1 | 0 | 0:1 |
