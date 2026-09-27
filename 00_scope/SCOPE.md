# SCOPE: GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)

## Q1. Review title & Scope Rationale
**Title:** GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)

**Terminology Rationale:** Throughout this review, "GPS-denied" is employed as the standard, established umbrella terminology in aerospace and robotics literature. It encompasses broader GNSS-denied operational conditions (loss, degradation, jamming, spoofing, or multipath attenuation of GPS, GLONASS, Galileo, and BeiDou signals in indoor, subterranean, urban canyon, canopy, and contested environments).

---

## Q2. Research Questions & Operational Definitions

### Research Questions
- **RQ1 (Sensors & Trends):** Which sensor-fusion configurations (camera, LiDAR, IMU, radar, UWB, barometer, ultrasonic) are most commonly used for GPS-denied UAV navigation, and how has their prevalence shifted between 2010 and 2026?
- **RQ2 (Accuracy & Environments):** What localization accuracy and robustness metrics are reported across different GPS-denied environments (indoor, urban canyon, subterranean, forest, adversarial), and how do they vary by environment and platform?
- **RQ3 (Algorithmic Approaches & Validation):** Which algorithmic approaches (VIO, SLAM, LIO, filter-based fusion, learning-based methods) dominate the literature, and how do they compare on validation type (real flight vs. simulation) and reported performance?
- **RQ4 (Limitations & Adversarial Conditions):** What limitations and future research directions are identified in the corpus, particularly regarding adversarial conditions, electronic warfare (jamming/spoofing), and resource-constrained edge platforms?

### Operational Taxonomies & Coding Rules
- **Sensor Modalities:**
  - *Proprioceptive:* Inertial Measurement Units (IMU/INS: gyroscopes, accelerometers).
  - *Exteroceptive:* Optical cameras (monocular, stereo, RGB-D, event cameras), LiDAR (2D, 3D mechanical, solid-state), Radar (mmWave, FMCW), Ultra-Wideband (UWB RF ranging), Acoustic/Ultrasonic altimeters, Barometric pressure altimeters, Magnetometers.
- **Sensor Fusion Categories:**
  - *Loosely Coupled:* Independent estimation per sensor followed by state-level filtering.
  - *Tightly Coupled:* Joint optimization or filtering directly over raw sensor measurements (e.g., visual feature tracks + IMU pre-integration).
  - *Optimization-Based / Factor Graph:* Non-linear least-squares smoothing over sliding windows or full graphs.
  - *Filter-Based:* Extended Kalman Filter (EKF), Unscented Kalman Filter (UKF), Multi-State Constraint Kalman Filter (MSCKF), Particle Filter (PF).
  - *Multi-label rule:* Hybrid architectures (e.g., tightly coupled VIO front-end with pose graph optimization back-end) are coded hierarchically with primary front-end and back-end labels recorded.
- **Environment Taxonomy:**
  - *Indoor:* Structured buildings, corridors, rooms, warehouses.
  - *Urban Canyon:* High-rise city corridors, multipath-heavy urban environments.
  - *Subterranean:* Tunnels, mines, caves, culverts, underground structures.
  - *Forest / Vegetated:* Natural canopy, agricultural orchards, unstructured outdoor clutter.
  - *Adversarial / Contested:* RF jamming, GPS spoofing, cyber-physical electronic warfare environments.
  - *Open / Transition:* Open outdoor areas transitioning into GPS-denied zones.
- **Platform Taxonomy:**
  - Multi-rotor (quadrotor, hexarotor, octocopter), Fixed-wing, Hybrid VTOL, Flapping-wing / Micro-Air-Vehicle (MAV).
- **Reported Accuracy & Robustness Metrics:**
  - Absolute Trajectory Error (ATE / RMSE in meters), Relative Pose Error (RPE / drift per meter or % distance traveled), Success/Failure Rate, Update Latency / Frame Rate (Hz).

---

## Q3. Databases Searched & Full Search Strategy

### Information Sources
Searches were conducted across two primary indexing databases in engineering and applied sciences:
1. **IEEE Xplore** (`ieeexplore.ieee.org`)
2. **Scopus** (`scopus.com`)

### Full Search Strings & Parameters (Executed: 2026-06-15)

#### 1. IEEE Xplore
- **Search Query:**
  ```text
  ("GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied" OR "GPS-degraded" OR "GPS free" OR "GPS-free" OR "navigation without GPS") AND ("UAV" OR "unmanned aerial vehicle" OR "drone" OR "quadrotor" OR "multirotor" OR "fixed-wing" OR "rotary-wing") AND ("localization" OR "navigation" OR "SLAM" OR "odometry" OR "positioning")
  ```
- **Applied Filters:** Publication Year: 2010–2026; Content Type: Conference Publications, Journals; Language: English.
- **Yield:** ~3,200 initial hits; ~2,800 after document/language filters; **1,000** exported (relevance-ranked standard harvest cap).
- **Raw Export:** `01_data_raw/ieee_xplore_20260615.csv` (28 fields, 2,244,035 bytes).

#### 2. Scopus
- **Search Query:**
  ```text
  TITLE-ABS-KEY ( ( "GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied" OR "GPS-degraded" OR "GPS-free" OR "navigation without GPS" ) AND ( "UAV" OR "unmanned aerial vehicle" OR "drone" OR "quadrotor" OR "multirotor" ) AND ( "localization" OR "navigation" OR "SLAM" OR "odometry" OR "sensor fusion" OR "positioning" ) )
  ```
- **Applied Filters:** Publication Year: 2010–2026; Document Type: Conference Paper, Article; Language: English.
- **Yield:** ~4,100 initial hits; ~3,800 after document/language filters; **1,000** exported (relevance-ranked standard harvest cap).
- **Raw Export:** `01_data_raw/scopus_20260615.csv` (8 normalized fields, 1,598,838 bytes).

**Total Harvested Corpus:** Exactly **2,000 raw records** (1,000 IEEE + 1,000 Scopus) logged in `01_data_raw/SEARCH_LOG.md`.

---

## Q4. Search Window & Temporal Coverage
- **Search Execution Date:** **2026-06-15**.
- **Search Window:** **2010-01-01 to 2026-06-15** (inclusive).
- **Partial Year Clarification (2026):** Because searches were executed on 2026-06-15, literature indexed for 2026 represents a partial year (January 1 through mid-June 2026). In all temporal trend analyses and synthesis reports, 2026 data is explicitly reported as partial and not annualized to prevent skewed growth inferences.

---

## Q5. Inclusion Criteria (Operational Definitions)
- **I1 (Date):** Published between 2010-01-01 and 2026-06-15.
- **I2 (Language):** Written and published in English.
- **I3 (Document Type):** Peer-reviewed original journal article or full conference proceeding.
- **I4 (Primary Topic):** Addresses GPS/GNSS-denied, degraded, or contested aerial navigation as the central research focus (defined by title, abstract, keywords, and explicit problem statement; not merely passing mention as peripheral context).
- **I5 (Platform Focus):** Focuses explicitly on Unmanned Aerial Vehicles (UAVs / drones / UAS / MAVs).
- **I6 (Multi-Sensor Fusion):** Implements or evaluates an integrated multi-sensor navigation solution fusing measurements from at least two distinct sensing modalities (e.g., IMU + Camera, IMU + LiDAR, Camera + LiDAR, Radar + IMU, UWB + IMU, or IMU + Barometer). Single-sensor-only approaches (e.g., pure standalone monocular vision without inertial or external aiding) are excluded.
- **I7 (Empirical Validation):** Presents empirical quantitative validation via physical real-world UAV flight tests, ground robot flight-surrogate experiments, or high-fidelity simulation.

---

## Q6. Exclusion Criteria
- **E1 (No Validation):** Purely conceptual, tutorial, or theoretical papers lacking experimental or simulation results.
- **E2 (GPS-Dependent):** Systems requiring active, uninterrupted nominal GNSS signals (GPS-denial is not the core operational setting).
- **E3 (Non-UAV Platforms):** Purely terrestrial unmanned ground vehicles (UGVs), underwater/marine autonomous vehicles (AUVs), spacecraft, or non-aerial robotics with no UAV applicability or testing.
- **E4 (Single-Sensor):** Single-sensor navigation methods lacking multi-sensor fusion.
- **E5 (Non-English):** Publications in languages other than English.
- **E6 (Pre-2010):** Articles published prior to 2010-01-01.
- **E7 (Non-Peer-Reviewed):** Unrefereed preprints (e.g., arXiv/TechRxiv preprints unless published in a peer-reviewed venue), trade magazines, white papers, industry marketing material, patents, books, book chapters, dissertations, theses, extended abstracts, and conference summaries.
- **E8 (Duplicates):** Duplicate records identified during cross-database deduplication (IEEE Xplore vs. Scopus).
- **E9 (Retractions):** Formally retracted articles.
- **E10 (No Extractable Data):** Papers lacking extractable localization accuracy, error metrics, or quantitative performance data.

---

## Q7. Quality Appraisal Framework (0–10 Scale)

Quality appraisal is scored on a 10-point scale across four defined methodological dimensions:

### Dimensions
- **A. Experimental Rigor (0–4 points):**
  - `+2`: Real-world experimental flight tests conducted on a physical UAV platform.
  - `+1`: Ground-truth reference comparison (RTK-GPS, motion capture [Vicon/OptiTrack], total station, or high-precision survey-grade map).
  - `+1`: Repeatability reporting: Multiple experimental flight runs with variance, standard deviation, or confidence intervals reported. *(Note: Code/dataset release is scored strictly under Dimension D to avoid double-counting).*
- **B. Reporting Completeness (0–3 points):**
  - `+1`: Quantitative trajectory error reported (Absolute Trajectory Error [ATE / RMSE] AND relative drift / odometry error).
  - `+1`: Detailed operational environment parameters reported (trajectory length, flight duration, and spatial scale).
  - `+1`: Robustness characterization reported (failure modes, edge cases, latency, or component ablation analysis).
- **C. Baseline Fairness (0–2 points):**
  - `+1`: Direct quantitative comparison against at least one established benchmark/baseline algorithm (e.g., VINS-Mono, ORB-SLAM3, LIO-SAM, standard EKF).
  - `+1`: Baseline evaluated under matched experimental flight conditions or identical benchmark sensor datasets (not unverified copied figures).
- **D. Reproducibility (0–1 point):**
  - `+1`: Public release of open-source codebase, raw flight dataset, or full hardware/sensor bill-of-materials and calibration specs.

### Quality Tiers
- **Q-High:** Score 8–10 points.
- **Q-Medium:** Score 5–7 points.
- **Q-Low:** Score 0–4 points.

### Simulation Cap Policy Rule
Simulation-only papers cannot be classified as **Q-High** regardless of total raw points. If a simulation-only study receives a raw score of 8–10 points, its tier classification is capped at **Q-Medium (capped)**, while the raw numerical score is preserved in data extraction logs for audit transparency.

### Appraisal Procedure & Inter-Rater Reliability
Calibration is performed on an initial dual-appraiser sample of 20% of eligible studies. Inter-rater agreement is measured via weighted Cohen's Kappa ($\kappa \ge 0.75$) or Intraclass Correlation Coefficient (ICC(2,1) $\ge 0.75$). Any scoring discrepancies are resolved by consensus with reference to verbatim evidence quotes.

---

## Q8. Venue Inclusion & Exclusion

### Included Venues
Peer-reviewed journals and conference proceedings indexed in IEEE Xplore, Scopus, or Web of Science within robotics, aerospace, autonomous systems, and sensor fusion. Representative examples:
- *IEEE Transactions on Robotics (T-RO)*
- *IEEE Robotics and Automation Letters (RA-L)*
- *IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*
- *IEEE International Conference on Robotics and Automation (ICRA)*
- *Journal of Field Robotics (JFR)*
- *GPS Solutions (Springer)*
- *Navigation: Journal of the Institute of Navigation (ION)*
- *Sensors (MDPI)*
- *IEEE Sensors Journal*
- *Drones / Aerospace (MDPI)*

### Excluded Venues
- Predatory or non-indexed journals (defined as journals not indexed in IEEE Xplore, Scopus, Web of Science, or DOAJ for open-access venues).
- Unindexed workshops, non-peer-reviewed symposium presentations, and vendor white papers.
- Venues strictly outside robotics, aerospace, sensing, and navigation disciplines.

---

## Q9. Language Filter
English language only.

---

## Q10. Document Types
- **Included:** Peer-reviewed journal articles and full peer-reviewed conference proceeding papers.
- **Excluded:** Books, edited volumes, book chapters, master's theses, doctoral dissertations, letters to the editor, editorials, conference extended abstracts without peer review, and non-refereed preprints.

---

## Q11. Synthesis & Review Workflow Alignment
The protocol directly guides the PRISMA 2020 systematic review pipeline:
1. **Deduplication:** Automated cross-database matching (DOI, normalized title Levenshtein distance $\ge 0.95$, publication year) in `02_data_processed/deduplicated_master.csv`.
2. **Screening:** Title/abstract screening followed by full-text eligibility appraisal against criteria I1–I7 and E1–E10 in `02_data_processed/screening_results.csv`.
3. **Data Extraction:** Standardized 18-section structured evidence extraction per paper with exact verbatim quote anchoring (`08_docs/EXTRACTION_SCHEMA_v1.md`).
4. **Synthesis:** Narrative synthesis grouped by sensor combination and algorithm paradigm, supported by multi-dimensional comparative taxonomy tables and performance distributions (`08_docs/SYNTHESIS_METHOD.md`).
