# Exhaustive Deep Thematic Ingestion Report: GPS-Denied UAV Navigation (2013–2026)

**Corpus Scope:** 279 Gold-Standard Manually Verified Extractions  
**Data Sources:** `02_data_processed/MASTER_EVIDENCE.csv`, `06_analysis/outputs/quality_appraisal_scored.csv`, `06_analysis/outputs/inference_table.csv`  
**Quality Framework:** Plan-Do-Check-Act (PDCA) Multi-Tier Quality Screening  

---

## 1. Corpus Demographics & Historical Evolution (2013–2026)

The corpus of 279 papers spans 14 years of research into unmanned aerial vehicle (UAV) state estimation, localization, and navigation within Global Navigation Satellite System (GNSS)-denied environments.

### 1.1 Temporal Trajectory
The literature exhibits three distinct historical epochs:
1. **Pioneering Foundations (2013–2016; $n = 26$, 9.3%):** Focused primarily on basic single-sensor odometry (monocular visual odometry, early optical flow dead reckoning, and rudimentary filtering like Extended Kalman Filters).
2. **Algorithmic Maturation & Factor Graphs (2017–2021; $n = 79$, 28.3%):** Emergence of tightly coupled Visual-Inertial Odometry (VIO) using optimization backends (e.g., MSCKF, OKVIS, VINS-Mono, ORB-SLAM2) and early LiDAR odometry (LOAM).
3. **Multi-Modal, Swarm & Neural Era (2022–2026; $n = 174$, 62.4%):** Rapid escalation in hybrid multi-sensor architectures (LiDAR-Visual-Inertial-UWB), decentralized cooperative multi-UAV swarms, learned visual place recognition (SuperPoint/LightGlue cross-view matching), and 3D radiance field SLAM (3D Gaussian Splatting).

```
Year-by-Year Distribution (n = 279):
  2013: 1    (0.4%)   |
  2014: 1    (0.4%)   |
  2015: 6    (2.2%)   ||
  2016: 18   (6.5%)   |||||
  2017: 11   (3.9%)   |||
  2018: 27   (9.7%)   |||||||
  2019: 28   (10.0%)  |||||||
  2020: 3    (1.1%)   |
  2021: 10   (3.6%)   |||
  2022: 35   (12.5%)  |||||||||
  2023: 43   (15.4%)  |||||||||||
  2024: 7    (2.5%)   ||
  2025: 2    (0.7%)   |
  2026: 87   (31.2%)  ||||||||||||||||||||||
```

### 1.2 Geographic & Institutional Distribution
Research output is concentrated across several high-activity regional hubs:
- **China ($n = 28$ primary, plus institutional affiliations):** Tsinghua University, Beijing Institute of Technology, Northwestern Polytechnical University (NWPU), Beihang University.
- **United States ($n = 16$):** West Virginia University, Cal Poly Pomona, MIT/DARPA SubT contributors.
- **Singapore ($n = 9$):** National University of Singapore (TLAB, Temasek Laboratories).
- **Other Active Nations:** Taiwan ($n = 6$), Canada ($n = 6$), Australia ($n = 3$), Spain ($n = 3$), Finland ($n = 3$), India ($n = 3$), Iran ($n = 3$).

---

## 2. Quality Appraisal (QA) Tier Stratification

Every paper in the corpus was rigorously evaluated across four scoring dimensions:
- **Methodological Rigor (`qa_rigor`, 0–3):** Formulation soundness, noise modeling, theoretical convergence.
- **Reporting Quality (`qa_reporting`, 0–3):** Precision in reporting trajectory error (ATE, RMSE), drift rates, and operational parameters.
- **Baseline Comparative Rigor (`qa_baseline`, 0–2):** Controlled benchmarking against recognized open-source SOTA (e.g., ORB-SLAM3, VINS-Mono, FAST-LIO2).
- **Reproducibility (`qa_repro`, 0–1):** Availability of open-source repositories, publicly released datasets, or full hardware specs.

```
Quality Tier Breakdown:
┌───────────┬───────┬────────────┬────────────────────────────────────────────────────────┐
│ Tier      │ Count │ Percentage │ Description                                            │
├───────────┼───────┼────────────┼────────────────────────────────────────────────────────┤
│ Q-High    │ 3     │ 1.1%       │ Authoritative anchors; strict benchmarks, open baselines│
│ Q-Medium  │ 98    │ 35.1%      │ Solid technical rigor; complete experimental reporting │
│ Q-Low     │ 178   │ 63.8%      │ Exploratory or preliminary; lacks public baselines/code │
└───────────┴───────┴────────────┴────────────────────────────────────────────────────────┘

Component Score Statistics (Corpus Mean):
- Methodological Rigor:  1.48 / 3.0
- Reporting Clarity:     1.25 / 3.0
- Baseline Comparison:   1.06 / 2.0
- Reproducibility Score: 0.01 / 1.0 (Critical community gap: <2% provide open-source code/data)
- Composite QA Total:    3.81 / 8.0
```

### 2.1 The Three Authoritative Q-High Anchor Studies

1. **REC_0037 (2026) — Deep Cross-View Satellite Matching:**
   - **Method:** Visual place recognition matching onboard monocular video to geo-referenced satellite orthoimagery and Digital Elevation Models (DEM) via deep learned keypoints (SuperPoint / LightGlue) + EPnP pose recovery.
   - **Performance:** Mean horizontal localization error of **1.84 m** over multi-kilometer flight paths.
   - **Limitations Reported:** Z-axis deviation and vertical drift remain elevated due to DEM spatial resolution limits and monocular scale ambiguity.

2. **REC_0502 (2026) — `LD3DGS-SLAM` (Long-Distance 3D Gaussian Splatting SLAM):**
   - **Method:** Monocular camera + 200 Hz IMU fused with a 3D Gaussian Splatting map representation for real-time aerial radiance field rendering and tracking on DJI M100 and Phantom 4 RTK platforms.
   - **Performance:** **0.8 m** average localization error at high altitudes (100–500 m). Outperformed ORB-SLAM3 (RMSE **0.74 m** vs. ORB-SLAM3 **13.79 m** on eVTOL1-120; **0.49 m** vs. **3.83 m** on XAMIT-Loc300).
   - **Limitations Reported:** High GPU memory consumption; unrendered mode slightly outperforms rendering within localized effective map bounds (240–340 m).

3. **REC_1277 (2026) — `PG-TLNet` Physics-Guided Aeromagnetic Interference Compensation:**
   - **Method:** 5 scalar magnetometers + 1 vector magnetometer + IMU + current/voltage sensors fused via a physics-guided neural network compensating electromagnetic motor interference in GNSS-denied swarm flight.
   - **Performance:** Standard deviation of aeromagnetic error reduced from **179.99 nT** (Tolles-Lawson baseline) to **26.64 nT** (85.2% reduction); inference latency of **94 µs per sample**.
   - **Limitations Reported:** High-current surge events degrade the linear-nonlinear hybrid model; inter-UAV electromagnetic coupling in dense swarm formations is not explicitly accounted for.

---

## 3. Thematic Clustering by Algorithmic Paradigms

The 279 papers divide into seven distinct technological paradigms:

```
Methodological Taxa (n = 279):
1. Hybrid Multi-Sensor Fusion:              78 papers (28.0%)
2. Vision & Object / Cross-View / VPR:       50 papers (17.9%)
3. Cooperative Swarms & Multi-Agent SLAM:    49 papers (17.6%)
4. Visual-Inertial Odometry (VIO / VSLAM):   18 papers (6.5%)
5. LiDAR & LiDAR-Inertial SLAM (LIO):         7 papers (2.5%)
6. Ultra-Wideband (UWB) & Radio Ranging:      6 papers (2.1%)
7. Other Emergent & Physics-Guided Systems:  64 papers (22.9%)
   [Plus 7 Survey / Review articles for contextual baseline positioning]
```

### 3.1 Hybrid Multi-Sensor Fusion ($n = 78$)
- **Core Architectures:** Loosely coupled and tightly coupled Extended Kalman Filters (EKF), Unscented Kalman Filters (UKF), and factor graph optimization (FGO).
- **Sensor Configurations:** Visual-Inertial-LiDAR, Camera-IMU-Barometer-Magnetometer, and BIM/Digital-Twin-aided frameworks.
- **Key Trade-offs:** Highest absolute positioning accuracy and resilience against single-sensor failure; high computational overhead and non-trivial inter-sensor extrinsic/temporal calibration.

### 3.2 Vision-Based Localization & Cross-View Matching ($n = 50$)
- **Core Architectures:** Deep feature matching (SuperPoint, SuperGlue, LightGlue, LoFTR), template matching (MOGF, NCC), aerial-to-satellite cross-view localization, and YOLO object-level bounding box SLAM.
- **Key Trade-offs:** Zero-drift potential when registering against absolute georeferenced satellite/aerial maps; sensitivity to seasonal appearance changes, sun glint, perspective distortion, and high compute load.

### 3.3 Cooperative Multi-UAV Swarms & Distributed SLAM ($n = 49$)
- **Core Architectures:** Relative localization via inter-UAV visual detection, mutual UWB ranging, decentralized Dec-POMDP formation control, and aerial-ground (UAV-UGV) collaborative mapping.
- **Key Trade-offs:** Eliminates single-agent failure points and enables collaborative exploration of large environments; vulnerable to RF communication bandwidth saturation, packet loss, and inter-agent relative coordinate initialization.

### 3.4 Visual-Inertial Odometry (VIO) ($n = 18$)
- **Core Architectures:** Filter-based (MSCKF, adaptive $H_\infty$ AHCMSCKF) and keyframe optimization-based (ORB-SLAM, VINS-Mono adaptations).
- **Key Trade-offs:** Low SWaP (only requires camera + IMU); inevitable drift over long distances (typically 0.5%–2.5% of distance traveled) without loop closures or external anchors.

### 3.5 LiDAR & LiDAR-Inertial SLAM ($n = 7$)
- **Core Architectures:** Point-to-plane ICP, LOAM, PSS-LIO, spatial grid/shell feature extractors.
- **Key Trade-offs:** Direct metric 3D structural mapping invariant to ambient lighting changes; high payload weight, power consumption, and degeneracy in geometrically uniform corridors/tunnels.

### 3.6 Ultra-Wideband (UWB) & Radio Navigation ($n = 6$)
- **Core Architectures:** Time-Difference-of-Arrival (TDoA) and Two-Way Ranging (TWR) trilateration, dynamic anchor self-calibration, and GNSS-emulation transponders.
- **Key Trade-offs:** Bounded error (sub-meter or centimeter-level accuracy); requires pre-deployed infrastructure or moving anchor anchors, susceptible to non-line-of-sight (NLOS) multipath.

### 3.7 Emergent & Physics-Guided Paradigms ($n = 64$)
- **Core Architectures:** Geomagnetic navigation (PG-TLNet), quantum-enhanced sensor fusion, radar/Doppler odometry for visually degraded environments (smoke, dust, fog), and POMDP motion planners.

---

## 4. Operational Environments & Degradation Regimes

The corpus targets challenging environments where GNSS signals are degraded, blocked, or actively denied:

```
Operational Regimes:
- Mixed GNSS-Degraded & Open Transitions: 183 papers (65.6%)
- Indoor, Warehouses & Industrial Facilities: 60 papers (21.5%)
- Subterranean, Mines, Tunnels & Caves:       7 papers (2.5%)
- Forest & Dense Vegetative Canopy:           5 papers (1.8%)
- Urban Canyons & High-Rise Buildings:        4 papers (1.4%)
- GNSS Spoofed / Electronic Warfare:          2 papers (0.7%)
- Unreported / Generic:                      18 papers (6.5%)
```

---

## 5. Empirical Validation Fidelity & Sim-to-Real Gap

```
Empirical Evaluation Modes:
┌────────────────────────┬───────┬────────────┐
│ Mode                   │ Count │ Percentage │
├────────────────────────┼───────┼────────────┤
│ Real-World Flight Only │ 111   │ 39.8%      │
│ Both (Real + Sim)      │ 83    │ 29.7%      │
│ Simulation Only        │ 62    │ 22.2%      │
│ Dataset / Secondary    │ 7     │ 2.5%       │
│ Unreported / Review    │ 16    │ 5.7%       │
└────────────────────────┴───────┴────────────┘
```

- **Airframes:** Quadrotors and multi-rotors represent the vast majority, led by commercial DJI platforms (Matrice 100/300/600, Phantom 4 RTK, Mavic), alongside open-source Pixhawk/PX4 platforms and fixed-wing airframes ($n = 11$).
- **Embedded Compute:** Over 60% of real-time embedded deployments run on the NVIDIA Jetson family (Nano, TX2, Xavier NX, AGX Orin).
- **Public Benchmarking Deficit:** Over 90% of papers test exclusively on private, self-collected flight logs, highlighting a severe need for standardized open flight datasets.

---

## 6. Synthesis: The Core Physical Trade-Offs

1. **The Accuracy vs. SWaP-C Dilemma:** Multi-sensor LiDAR arrays deliver sub-decimeter accuracy but incur heavy payload (0.5–2.0 kg) and power draw (15–50 W), halving flight endurance. Lightweight monocular setups conform to micro-SWaP constraints (<100 g) but suffer cumulative dead-reckoning drift.
2. **The Metric Heterogeneity Gap:** Trajectory evaluations vary widely between absolute trajectory error (ATE RMSE in meters), drift percentage over distance traveled (0.5%–3.0%), and terminal position offset, impeding direct statistical pooling.
3. **The Sim-to-Real Transfer Disconnect:** Over 51% of the corpus does not demonstrate closed-loop autonomous flight in real physical hardware, operating either purely in simulation or executing offline state estimation on pre-recorded rosbags.
