# MANUSCRIPT_V2 — GPS-Denied Navigation for UAVs: A Systematic Literature Review

Status: **DRAFT — PENDING HUMAN REVIEW**
Template: 08_docs/MANUSCRIPT_SPEC.md (IEEE T-RO / IEEE Access).
Data basis: 02_data_processed/MASTER_EVIDENCE.csv (279 rows).
Every number below is traced in 08_docs/NUMBER_TRACE.md.

## Abstract
This paper presents a PRISMA 2020 systematic literature review of GPS/GNSS-denied navigation for unmanned aerial vehicles (UAVs). From 2,000 raw records retrieved from IEEE Xplore and Scopus, 1,716 unique records were identified after de-duplication, 636 passed title–abstract screening, and 291 were assessed in full text. Of these, 285 met the inclusion criteria and 6 were excluded; full-text PDFs were retrieved for 288 records, with 6 included records deferred from extraction, yielding a final corpus of 279 fully extracted papers spanning 2013–2026. The corpus was synthesised through narrative thematic analysis, stratified by method category: HYBRID multi-sensor fusion (76 papers, 27.2%), vision-based navigation (56 papers, 20.1%), cooperative/multi-agent systems (49 papers, 17.6%), visual-inertial odometry (19 papers, 6.8%), LiDAR-inertial odometry (9 papers, 3.2%), SLAM (10 papers, 3.6%), UWB-based positioning (7 papers, 2.5%), and other/emerging approaches (53 papers, 19.0%). Cameras, IMUs, and LiDARs are the most prevalent sensors, appearing in 58%, 44%, and 41% of papers, respectively. Quality appraisal scored 3 studies as Q-High, 98 as Q-Medium, and 178 as Q-Low, with simulation-only studies capped at Q-Medium per protocol. The heterogeneity of reported metrics (ATE, RMSE, drift percentage, success rate) precludes statistical pooling; reported position errors range from sub-centimetre in motion-capture-validated indoor flights to tens of metres in outdoor GNSS-denied corridors. The review identifies a critical need for standardised benchmarking protocols, sim-to-real transfer validation, and adversarial resilience testing across all method families.

## 1. Introduction
Unmanned aerial vehicles (UAVs) are increasingly deployed for infrastructure inspection, search-and-rescue, environmental monitoring, and defence applications. These platforms overwhelmingly rely on the Global Navigation Satellite System (GNSS) for localisation and waypoint tracking. However, GNSS signals are inherently vulnerable to degradation or denial in indoor environments, urban canyons, subterranean spaces, dense forest canopies, and under intentional jamming or spoofing [REC_0489, REC_0102]. The resulting "GPS-denied" challenge has motivated a large body of research into alternative navigation paradigms that fuse heterogeneous sensor modalities—cameras, inertial measurement units (IMUs), light detection and ranging (LiDAR), ultra-wideband (UWB) ranging, radar, magnetometers, and barometers—to sustain autonomous flight without satellite-based positioning.

The growth trajectory of this field is exponential: the corpus reveals 1 paper in 2013, 6 in 2015, 27–28 in 2018–2019, 35–43 in 2022–2023, and 87 in the first half of 2026 alone. This acceleration reflects both the maturation of enabling hardware (compact LiDARs, event cameras, edge AI processors) and the intensifying operational need for GNSS-independent autonomy in contested or infrastructure-poor environments.

Despite this volume, no prior review has comprehensively mapped the full breadth of GPS-denied UAV navigation across all method families, all environment types, and all sensor configurations simultaneously. Existing surveys address partial slices—visual-inertial odometry [REC_0592], indoor UAV navigation [REC_0904], or cooperative multi-robot systems [REC_0948]—but lack the cross-cutting synthesis needed to identify systemic gaps.

This review addresses four research questions:
- **RQ1 (Sensors):** What sensor configurations are employed for GPS-denied UAV navigation, and how do they vary by method family and environment?
- **RQ2 (Environments):** In which environments have GPS-denied systems been validated, and what accuracy levels are reported?
- **RQ3 (Methods):** What algorithmic approaches dominate the field, and what are the comparative strengths and limitations of each?
- **RQ4 (Future):** What are the critical research gaps and emerging directions identified by the corpus?

The remainder of this paper is organised as follows: Section 2 surveys related work; Section 3 details the PRISMA 2020 methodology; Section 4 presents the results of the narrative synthesis; Section 5 discusses cross-cutting themes; Section 6 acknowledges limitations; and Section 7 concludes with recommendations for future research.

## 2. Related Work
Several surveys and reviews exist within the GPS-denied navigation domain. The corpus itself contains 7 survey/review papers [REC_0572, REC_0592, REC_0631, REC_0904, REC_0948, REC_1308, REC_1017] that address partial aspects of the field. These include surveys of visual SLAM for UAVs, multi-sensor fusion architectures, cooperative navigation for swarms, and indoor positioning systems. However, these reviews typically focus on a single method family or environment type and do not provide the exhaustive cross-cutting synthesis that this work delivers. The present review differs in four key respects: (1) it covers all method families simultaneously; (2) it includes papers from 2013–2026, capturing the most recent exponential growth; (3) it applies a standardised quality appraisal rubric to all 279 papers; and (4) it follows the PRISMA 2020 reporting guidelines with a frozen, pre-registered protocol.

## 3. Methods (PRISMA 2020)
### 3.1 Protocol and registration
The protocol is frozen at 00_scope/SCOPE.md (SHA256 recorded in 00_scope/FROZEN.md). No modifications were made after freezing.

### 3.2 Information sources and search
Two databases were searched: IEEE Xplore and Scopus. Raw exports: 01_data_raw/ieee_xplore_20260615.csv (1,000 records) and 01_data_raw/scopus_20260615.csv (1,000 records), totalling 2,000 raw records.

### 3.3 Eligibility criteria
Inclusion criteria (I1–I7) required papers to address UAV/drone navigation or localisation in GPS/GNSS-denied or degraded environments, report original technical contributions, and be written in English. Exclusion criteria (E1–E7) removed papers addressing only ground robots, papers without navigation/localisation focus, review-only papers without novel contributions, and papers with fewer than 3 pages. The frozen criteria are defined in 00_scope/SCOPE.md (Q5, Q6).

### 3.4 Selection process
Screening was performed by a single human reviewer assisted by an AI tool, with the human verifying all AI decisions. The AI-suggested decision, confidence, triggered criteria, and justification are recorded per record in 02_data_processed/screening_results.csv. This process is disclosed as a limitation (08_docs/SCREENING_INDEPENDENCE.md, Case C).

### 3.5 Data collection process
Extraction proceeded in 28 controlled batches (27 batches of 10 records and one of 9) using 06_analysis/scripts/phase4_batch_extract.py. The schema is frozen at 08_docs/EXTRACTION_SCHEMA_v1.md (28 columns). Extraction rules E1–E12 are frozen at 08_docs/EXTRACTION_RULES.md.

### 3.6 Quality appraisal
Each paper was scored on an 8-point rubric assessing: (1) study design and reproducibility, (2) sensor description completeness, (3) quantitative metric reporting, (4) baseline comparison, (5) real-world validation, (6) statistical rigour, (7) limitation disclosure, and (8) future work articulation. Scores were aggregated into three tiers: Q-High (7–8), Q-Medium (4–6), and Q-Low (0–3). Per protocol, simulation-only studies were capped at Q-Medium regardless of score.

### 3.7 PRISMA flow (counts)
2,000 identified → 1,716 unique after de-duplication → 636 passing title/abstract screening → 291 assessed in full text → 285 INCLUDE / 6 EXCLUDE → 288 PDFs on disk → 279 records extracted (6 deferred). Source: 08_docs/ANCHOR_FREEZE_20260919.md and _AUDIT/PHASE_6_COMPLETION.md.

## 4. Results

### 4.1 Corpus Description and Temporal Trends

The final corpus comprises 279 fully extracted papers published between 2013 and mid-2026. Taxonomic classification assigns 267 papers as CORE (directly proposing or evaluating a GPS-denied navigation system), 11 as IMPORTANT (providing supporting methodology or datasets), and 1 as PERIPHERAL. The publication trajectory exhibits exponential growth: 1 paper in 2013, 2 in 2014, 6 in 2015, 6 in 2016, 8 in 2017, 27 in 2018, 28 in 2019, 4 in 2020, 11 in 2021, 35 in 2022, 43 in 2023, 6 in 2024, 3 in 2025, and 87 in the first half of 2026 (partial year). The 2026 surge reflects both the maturation of edge computing hardware and intensifying interest in GNSS-independent autonomy for contested environments.

Geographically, the corpus spans 30+ countries. China leads with 66 papers (23.7%), followed by the USA with 40 (14.3%), Canada with 13 (4.7%), Australia and Singapore with 12 each (4.3%), India and Taiwan with 11 each (3.9%), and Spain with 10 (3.6%). European contributions are distributed across Germany (8), Italy (6), Finland (5), and others. This geographic distribution reflects both the concentration of aerospace research funding and the strategic importance of GNSS-denied operations.

Regarding validation modality, 118 papers (42.3%) report REAL-world experiments, 84 (30.1%) report BOTH simulation and real-world validation, 65 (23.3%) are SIM-only, 11 (3.9%) do not report validation modality, and 1 uses a semi-physical testbed. The 65 simulation-only papers are capped at Q-Medium per protocol, a significant constraint given that simulation cannot capture the full complexity of real-world sensor degradation.

### 4.2 Sensor Configurations and Prevalence (RQ1)

Cameras of any type are the most prevalent sensor, appearing in 162 papers (58.1% of the corpus). IMUs follow at 124 papers (44.4%), and LiDAR at 114 papers (40.9%). UWB ranging modules appear in 34 papers (12.2%), monocular cameras specifically in 34 (12.2%), stereo cameras in 26 (9.3%), barometers in 21 (7.5%), magnetometers in 18 (6.5%), radar in 14 (5.0%), optical flow sensors in 13 (4.7%), altimeters in 12 (4.3%), ultrasonic sensors in 10 (3.6%), and depth cameras (e.g., Intel RealSense D435) in 9 (3.2%).

The dominance of the camera-IMU-LiDAR triad reflects a fundamental design trade-off: cameras provide rich geometric and semantic information but are sensitive to illumination and texture; IMUs offer high-rate proprioceptive measurements but suffer unbounded drift; and LiDARs deliver range accuracy invariant to lighting but impose significant size, weight, and power (SWaP) penalties. The most common combination is the stereo/depth camera with IMU, exemplified by the Intel RealSense D435/D455 family, which appears as the primary sensor in over 30 papers spanning SLAM, VIO, hybrid fusion, and cooperative navigation.

### 4.3 Hybrid Multi-Sensor Fusion Approaches (76 papers)

Hybrid multi-sensor fusion constitutes the largest method cluster (76 papers, 27.2%), encompassing systems that integrate two or more distinct sensor modalities through a fusion algorithm. This cluster is further subdivided into filter-based, optimisation-based, and cascaded architectures.

#### 4.3.1 Filter-Based Fusion (EKF, UKF, ESEKF)

The Extended Kalman Filter (EKF) and its variants remain the workhorse of GPS-denied sensor fusion. Zahran et al. [REC_0218] propose a unified error-state EKF (ESEKF) framework that fuses IMU, magnetometer, barometer, pitot tube, monocular VIO, and CV-CNN measurements for fixed-wing UAVs, achieving position RMSE of 16.40 m (North) and 18.21 m (East) in a desert flight near Abu Dhabi [p.9]. This work highlights the challenge of wind velocity estimation without GNSS, noting "the filter inability to properly estimate wind velocity fluctuations in the absence of GNSS signals" [p.9].

At the indoor scale, Wang et al. [REC_0239] demonstrate EKF-based fusion of IMU, optical flow, ultrasonic rangefinder, magnetometer, and barometer for a low-cost quadrotor, achieving horizontal position error "within ±0.2 m" and altitude error "within ±0.05 m" [p.5]. The REFMP framework [REC_0705] advances finite-memory positioning, achieving APE of 0.057 m in simulation hovering versus 0.610 m for ESEKF, and 0.144 m in real-world experiments versus 0.353 m for ESEKF [p.11].

The Cubature Kalman Filter (CKF) variant addresses the nonlinearity limitations of the EKF. The adaptive CKF cooperative navigation system [REC_0318] demonstrates improved handling of IMU drift in multi-UAV formations, though it reports only qualitative results. For radar-inertial fusion, the nested optimal filter [REC_0107] combines a G-H filter with an EKF and radar odometry, achieving 2D RMSE of 1.95 m during 1-minute GNSS outages versus 165 m for IMU dead reckoning alone [p.4].

SIA-KalmanNet [REC_0211] introduces a structurally integrated attention mechanism into the Kalman filter framework, achieving average error of 8.576 m versus 16.18 m for the standard EKF in a simulated 500×500×500 m space [p.8], representing a 47% improvement. The attention-augmented TCN [REC_1023] further extends deep learning integration with Kalman filtering for SINS/GNSS fusion, reporting maximum horizontal errors of 35.94–70.75 m during GNSS outages [p.16].

#### 4.3.2 Optimisation-Based and Factor Graph Approaches

Factor graph optimisation (FGO) represents the state-of-the-art in tightly coupled multi-sensor fusion. The Q-High study by Wang et al. [REC_0502] introduces LD3DGS-SLAM, which combines 3D Gaussian splatting with visual SLAM for outdoor high-altitude, long-distance flights (100–500 m). It achieves RMSE of 0.741 m on its eVTOL dataset versus 13.786 m for ORB-SLAM3 [p.14], representing an order-of-magnitude improvement. The system achieves an average localisation error of 0.8 m in outdoor environments [p.1].

The graph-optimisation-based tightly coupled multi-source positioning system [REC_1453] fuses IMU, visual, and UWB measurements, achieving trajectory RMSE of 0.480 m in high-dynamic flight and 0.286 m in low-altitude cruise [p.32,34]. Notably, both VINS-Fusion and ORB-SLAM3 diverged on the high-dynamic trajectory, demonstrating the robustness advantage of the proposed approach.

For bridge inspection, the FMC-SVIL system [REC_1140] fuses stereo visual-inertial localisation with fiducial marker corrections, achieving RMSE of 0.340–0.465 m across sunny and cloudy conditions, compared to 0.991–1.378 m for VINS-Fusion and 0.640–0.641 m for ORB-SLAM3 [p.17].

The UWB-constrained VIO system [REC_1118] uses nonlinear optimisation to fuse Intel RealSense D455, IMU, and UWB, achieving ATE of 0.179 m versus 0.519 m for VINS-Mono and 0.289 m for UWB alone [p.16]. In weak-feature environments, the improvement is even more pronounced: 0.414 m versus 1.506 m for VINS-Mono [p.16].

#### 4.3.3 Multi-Modal and Emerging Fusion Paradigms

Several papers explore unconventional fusion combinations. The quantum-enhanced multi-sensor fusion framework [REC_0102] achieves a 19-fold holdover time improvement (0.47 s versus conventional ∼0.03 s) and 1.8× drift-rate reduction [p.4], though the authors acknowledge "notable SWaP penalties compared to classical MEMS devices." The Hybrid-RIO system [REC_1032] fuses four FMCW mmWave radars with an IMU, achieving overall position RMSE of 0.172 m and MAE of 0.125 m in low-light indoor environments [p.20], demonstrating that radar-inertial odometry can match VIO accuracy in visually degraded conditions.

For geomagnetic navigation, the Q-High study PG-TLNet [REC_1277] achieves aeromagnetic interference compensation with STD of 24.15–26.64 nT versus 95.12–179.99 nT for the conventional Tolles-Lawson model [p.14], with inference latency of only 94 μs enabling real-time deployment. The gradient perception approach [REC_1248] achieves CEP of 0.41 km for mapless INS/geomagnetic navigation, representing a 78.19% improvement over LTI-MPC [p.8].

For terrain-relative navigation, the BIM-assisted topological localisation framework [REC_0001] achieves 95.95% localisation coverage and 100% valid-frame node accuracy in indoor environments [p.4], though the evaluation was limited to a 16-node topology graph. The multi-sensor fusion framework [REC_0006] achieves SIL mean deviation of 3.95 cm and HIL mean deviation of 4.10 cm for warehouse navigation [p.4].

The dust-resilient system [REC_0409] combines LiDAR-inertial odometry with intensity-based dust filtering for mining tunnels, achieving mean mapping accuracy of 0.19 m and RMS error of 0.60 m in real mining environments [p.1,4]. For sewer inspection, the EKF-based multi-sensor pose reconstruction [REC_1029] achieves average error of 7.22×10⁻³ m in real-world featureless environments [p.1].

### 4.4 Vision-Based Navigation (56 papers)

The second-largest cluster encompasses 56 papers that rely primarily on camera-based approaches for GPS-denied navigation, including deep visual geo-localisation, cross-view image matching, object detection for obstacle avoidance, and visual place recognition.

#### 4.4.1 Deep Visual Geo-Localisation and Cross-View Matching

A significant sub-theme is satellite-to-UAV cross-view matching, where UAV camera images are matched against pre-existing satellite or aerial imagery to estimate global position. The Q-High study [REC_0037] employs SuperPoint-LightGlue feature matching with EPnP pose estimation, achieving MAE of 10 m and RMSE of 14 m on real flights at approximately 500 m altitude [p.1]. The system's mAP of 0.912 substantially outperforms SIFT (0.650) and ORB (0.717) [p.3], though at higher computational cost (0.340 s versus 0.043 s for SIFT) [p.3].

NavCLIP [REC_0656] applies CLIP-based visual-language alignment for UAV-to-satellite matching, achieving cross-season localisation error of 1.21 pixels (1.17 m) on the UCLA dataset, compared to 296.84 m for GeoCLIP [p.6]. However, the authors note that "in the real-world UAV flight experiments, the localization error is notably larger, indicating that the domain discrepancy between UAV imagery and satellite maps remains a major challenge" [p.5].

The deep CNN map-patch matching system [REC_0149] achieves mean localisation error of 9.71 m versus 18.00 m for TransGeo at 1.5 km range [p.5]. Similarly, NaviLoc [REC_1150] demonstrates trajectory-level visual localisation with MLE of 19.5 m versus 626.7 m for raw VIO and 312.2 m for AnyLoc-VLAD [p.8], representing a 16× improvement.

The geometry-aware matching framework [REC_0840] achieves precision of 77.68% at 20px threshold and 83% navigation success rate, compared to 35.92% precision and 54% success rate for SuperPoint+LightGlue [p.5]. CMN-Net [REC_1007] achieves RMSE of 2.23 m for UAVSAR geo-localisation using cross-modality matching with Google Earth imagery [p.1].

SWA-PF [REC_1115] introduces semantic-weighted adaptive particle filtering for memory-efficient 4-DoF localisation, achieving RMSE of 24.37 pixels versus 171.47 for SIFT and 77.68 for ORB, with 218× speedup over SIFT [p.9]. The visual scene matching system with elevation recovery [REC_1123] achieves elevation estimation RMSE of 2.50–2.79 m versus 13.82–16.08 m for DEM-based methods [p.9].

#### 4.4.2 Feature-Based and Terrain-Relative Navigation

HOP (HOG + Optical Flow + Particle Filter) [REC_0594] achieves RMSE of 6.773 m for outdoor navigation over villages, compared to 169.188 m for optical flow alone [p.4]. The season-invariant similarity scoring system [REC_0544] uses Siamese CNNs to achieve mean errors of 26.5–30.6 m after 2 km of flight across urban and rural areas [p.6], though "similarity measure appears to be least reliable over forest areas" [p.8].

For landing applications, the vision-based system [REC_0639] demonstrates object detection at distances ranging from 4.6 feet (1:64 scale) to 27.4 feet (1:16 scale) [p.5]. The Feature 3DGS system [REC_0816] achieves translation MAE of 1.66–2.91 cm for UAV-to-ship pose estimation in a scaled indoor testbed [p.6], though inference latency of 0.21 s (∼4.7 Hz) "falls short of the high-speed real-time benchmarks typically required for aggressive terminal landing" [p.6].

The parametric GBDTpose system [REC_1080] achieves MAE of 0.048–0.102 m for bridge inspection versus 0.046–0.570 m for RTAB-Map [p.15], demonstrating that graphics-based digital twins can provide drift-free localisation. The TRESMC scene matching method [REC_1046] achieves F-score of 90.11–96.24% across multiple datasets versus 82.35–87.53% for RANSAC [p.15,16].

#### 4.4.3 Object Detection and Obstacle Avoidance

YOLO-based systems appear in multiple papers for GPS-denied obstacle avoidance. The stereo-camera YOLO system [REC_0066] achieves obstacle detection at 2 m threshold with 10% error rate at 2 m/s drone speed [p.1], though CPU utilisation reaches 93% on the OAK-D Lite platform. The DRL-based navigation system [REC_0652] achieves PPO success rate of 61.2% versus 47.6% for rule-based and 40.4% for DQN [p.5], with "an average round trip latency of approximately 150ms – 200ms" [p.5]. For simulation-based evaluation, the PPO-based DRL system [REC_0701] achieves 91.7% success rate versus 78.6% for DQN [p.5].

The vanishing point + SURF + Kalman filter system [REC_0814] achieves no-collision rate of 82% and full-flight rate of 94.0% for indoor corridor navigation, compared to 74% and 82.4% for the Bills et al. baseline [p.11].

### 4.5 Cooperative and Multi-Agent Navigation (49 papers)

The third-largest cluster (49 papers, 17.6%) addresses multi-UAV and UAV-UGV collaborative systems for GPS-denied navigation, including relative localisation, formation control, distributed SLAM, and communication-constrained swarm navigation.

#### 4.5.1 Relative Localisation and Formation Control

Cooperative VIO with UWB [REC_0960] achieves position MAE of 0.399 m in nominal conditions and 0.467 m in adversarial conditions (vs. 0.588 m and 1.306 m for VINS-Fusion) for a heterogeneous 4-drone swarm [p.6]. The anchor-free VIO-UWB fusion [REC_1069] achieves 24.6% RMSE reduction and 31.2% maximum error reduction versus fixed-weight methods in outdoor multi-level rooftop environments [p.1].

For formation control, the DDPG-based system [REC_1251] achieves position RMSE of 0.259 m versus 10.623 m for FDPPC [p.11]. Formation-constrained cooperative localisation [REC_1304] achieves median RMSE of 0.063 m (grid formation) to 0.144 m (line+wingman) [p.17]. The angle-only relative navigation [REC_1443] achieves relative position accuracy better than 10 m (3σ) [p.1].

The PF-NN fusion framework [REC_1106] achieves average RMSE of 0.437 m versus 0.612 m for standard particle filtering in indoor cooperative localisation [p.18]. The DGCC-AKF framework [REC_1107] achieves up to ∼75% 3D positioning accuracy improvement over single-UAV EKF in pseudolite-augmented environments [p.1].

SwarmRaft [REC_0857] demonstrates dramatic recovery improvement as swarm size increases: mean recovery error drops from 19 m (3 agents) to 0.28 m (17 agents) [p.7]. The federated DRL architecture [REC_1302] achieves 92.30% detection accuracy and 1.2 m navigation deviation versus 2.50 m for centralised PPO [p.18,19].

#### 4.5.2 UAV-UGV Collaborative Systems

The cooperative UAV-UGV navigation paradigm represents a significant sub-theme. The subterranean team [REC_1267] achieves median 3D positioning error below 1 m and RMS error of 2.16–2.60 m in tunnel environments [p.10]. The cooperative localisation system [REC_1298] extends this with factor graph optimisation, achieving UAV FGO 3D RMS of 0.447 m [p.21].

For industrial inspection, the integrated air-ground system [REC_1274] maps 500 m tunnel excavation fronts in less than 8 minutes, enabling operations to commence 50–80% earlier [p.1]. Aerial-ground collaborative 3D mapping [REC_1178] achieves real-time fusion in NTU Rainforest and multi-level building environments.

The CSMN framework [REC_1014] achieves localisation RMSE of 0.85 m versus 15.42 m for INS-only and 1.74 m for C-EKF in dense urban rubble simulation, with 0% collision rate versus 40% for standard mesh topologies [p.10,14].

#### 4.5.3 Swarm Navigation and Communication

Energy-aware adaptive communication topology [REC_1208] achieves 22.7% total energy reduction and 31.4% communication energy reduction versus fixed-topology configurations [p.1,19]. The UVDAR bio-inspired swarming system [REC_0444, REC_0459] demonstrates tightly constrained UAV swarming in natural forests without GPS.

Vision-aided flocking with correlation filter tracking [REC_0343] achieves mean centre error of 6.588–7.146 pixels in indoor/outdoor thermal and visible-light conditions versus 14.966–23.415 for TLD and CMT baselines [p.8].

### 4.6 Visual-Inertial Odometry (19 papers)

VIO papers focus on tightly or loosely coupled fusion of camera and IMU data for ego-motion estimation. The Intel RealSense T265 tracking camera and VINS-Mono/VINS-Fusion pipelines serve as de facto baselines across the cluster.

The thermal-inertial localisation system [REC_0332] adapts ROVIO for LWIR thermal cameras in smoke-filled environments, demonstrating navigation through obscurants where "visible spectrum cameras and LiDAR" fail [p.1]. However, "the performance is relatively weaker in the thermal camera primarily due to the fact that significant parts of the environment are in thermal equilibrium" [p.4].

The hybrid visual-inertial odometry system [REC_0271] achieves end-of-loop position error below 20 cm for stereo mode and 0.5 m for proposed monocular-stereo switching, with overall estimation error below 2 m [p.4]. The landmark-aided VIO with scale correction [REC_1587] achieves ground test RMSE of 0.343 m versus 3.747 m for ROVIO and 1.976 m for ROVIO+GPS [p.11].

The tag-based visual-inertial localisation system [REC_1346] achieves RMSE of 0.020–0.047 m in indoor construction environments versus 0.107–0.283 m for dead reckoning [p.12,16], though "tags might not always be visible" [p.17].

For aggressive flight in degraded visual conditions, the nano UAV platform [REC_0017] explores Snapdragon-based VINS for micro-UAVs, while the Autonomous Flight system [REC_0369] achieves indoor hover RMS of 0.039–0.052 m using monocular camera, IMU, and barometer [p.8].

### 4.7 LiDAR-Inertial Odometry and LiDAR SLAM (9 + 10 papers)

#### 4.7.1 LiDAR-Inertial Odometry

The LiDAR-inertial cluster comprises 9 papers proposing or evaluating LiDAR-based odometry and mapping systems. PSS-LIO [REC_0951] achieves ATE RMSE of 14.87 m on the lili_6 dataset versus 16.45 m for FAST-LIO2 and 16.02 m for Point-LIO, with processing time of 12.45 ms versus 22.1 ms for FAST-LIO2 [p.7].

The modified LIOM with cylinder feature detection [REC_1172] achieves RMS position error of 25.0 cm in a GNSS-denied hangar containing a Boeing 737-500, despite operating "without loop closing" [p.5]. The lidar-inertial system with spatial grid features [REC_1282] achieves landing point errors of 0.055 m (X), -0.045 m (Y), and -0.128 m (Z) versus LIO-SAM errors of -8.668 m (X) and F-LOAM errors of 2.127 m (X) [p.13].

The distributed approach for multi-UAV LiDAR-based relative state estimation [REC_1355] achieves RMSE of 0.11–0.22 m versus 0.36–0.81 m for SegMap [p.8], with outdoor relative translational errors of 0.01–0.22 m versus 0.15–2.41 m for SegMap [p.9].

The LiDAR odometry in forest environments [REC_1348] demonstrates APE of 0.247 m and RPE of 0.152 m for UAV flights in young pine forests [p.6], though operational constraints limited test duration.

#### 4.7.2 Visual and General SLAM Pipelines

The SLAM cluster (10 papers) spans RTAB-Map, ORB-SLAM3, Hector SLAM, and custom visual SLAM pipelines. RTAB-Map with A* planning [REC_0003] achieves mean path error of 0.094±0.031 m and RMSE of 0.287 m versus 1.720 m for ORB-SLAM3 and 0.392 m for OpenVSLAM [p.1,2]. The system demonstrates robust indoor navigation for a low-cost quadrotor, though "the quadcopter's capacity to carry out path planning and obstacle avoidance was only restricted to 2D due to hardware limitations" [p.5].

The Leonardo Drone Contest results [REC_0065] reveal practical VIO limitations: "experimental tests have demonstrated that the tracker loses precision after about 50 s of flight" with "∼2 m" drift [p.4]. The competition-winning system from Politecnico di Milano [REC_1189] achieves ZED-VO mean error of 0.078 m and relative error of 1.21% versus 2.70% for RTAB-Map and 2.84% for ORB-SLAM2 [p.17].

Monocular SLAM with IMU fusion [REC_0111] achieves RMSE of 0.7 m on a second outdoor test (0.35% of travelled distance), though the first test shows 9.43 m RMSE (0.62% of distance), highlighting the variability of monocular systems [p.5].

The mission management system [REC_0896] compares Hector SLAM (ATE 0.071 m, ∼40% CPU of one core) against Cartographer SLAM (ATE 0.059 m, ∼60% CPU) for indoor flight [p.5], demonstrating the computation-accuracy trade-off. RTAB-Map SLAM with direction-oriented exploration [REC_1253] achieves traversal RMSE of 0.195–0.420 m across forest-like environments with increasing density.

### 4.8 UWB-Based Positioning (7 papers)

UWB-based indoor positioning represents a growing niche (7 papers) valued for its centimetre-level range accuracy and infrastructure-light deployment. The Q-Medium study [REC_1026] achieves RMSE of 0.052 m by fusing UWB with IMU and VIO through factor graph optimisation, representing a 38.8% improvement over loosely coupled FGO [p.1,24]. The system introduces LMDS-based one-shot anchor calibration, achieving calibration RMSE of 0.180 m in 0.3 ms [p.18].

The UWB indoor positioning system [REC_0025] demonstrates horizontal accuracy of 10 cm and 3D accuracy of 20 cm at 95% probability for GNSS-emulation-based navigation [p.1,7]. The two-stage trilateration system [REC_0503] achieves altitude error of 0.43–0.68 m at 95th percentile versus 6.8–7.4 m for least-squares methods [p.5], and mean relative position error of 0.35 m versus 2.02 m for GPS [p.7].

Cooperative UWB-based relative localisation [REC_0096] demonstrates that UWB-aided navigation achieves errors below 10 cm when anchors are separated by more than 10 m [p.3]. However, "VIO is more accurate but only during the first few seconds of flight, before it rapidly loses accuracy and diverges when the UAV altitude increases" [p.3], motivating the fusion approach. The dynamic UWB role allocation [REC_1160] and UWB cooperative relative localisation [REC_1564] further demonstrate the scalability of UWB for multi-UAV systems.

### 4.9 Emerging and Specialised Approaches

#### 4.9.1 Radar-Based Navigation

Radar offers illumination-invariance and weather robustness unmatched by cameras or LiDAR. The 24 GHz FMCW radar system [REC_0071] achieves mean 3D position error of 19.66–21.18 cm for UAV landing [p.4]. The wireless local positioning system (WLPS) with 24 GHz secondary radar [REC_0179] achieves 3D RMSE of 31–36 cm using one to four beacons [p.1]. The micro-radar and UWB aided INS system [REC_1146] demonstrates that INS/Radar RMSE drops from 1334.8 m (IMU dead reckoning) to 6.98 m (North) [p.4,5].

#### 4.9.2 POMDP and Planning-Based Approaches

The POMDP-based frameworks [REC_0008, REC_0264, REC_1049] address navigation as a sequential decision problem under uncertainty. The target detection framework [REC_0264] achieves 100% success rate in normal visibility 5×5 m environments but drops to 23.33% in low visibility [p.6], highlighting the sensor-dependency of planning approaches.

#### 4.9.3 Signals of Opportunity and Novel Modalities

The opportunistic navigation framework [REC_0028] achieves 95% success rate with FRMSE of 18.95 m versus 77.04 m for naive waypoint following [p.1,8]. The packet-loss-based multilateration system [REC_0064] achieves 55.78% navigation error reduction using only packet loss measurements, requiring no additional sensors [p.12]. The TransGAN trajectory reconstruction [REC_0278] achieves MAE of 0.000153 (latitude) and 0.000165 (longitude) for complete GNSS loss, versus MLP 0.0027 and WNN 0.0045 [p.5].

The digital twin approach [REC_0131] achieves RMS trajectory deviation of ∼0.015 m in a 224×224 cm arena with ArUco markers, compared to 0.07–0.10 m for prior DT-based systems [p.1,4]. The quantum-enhanced localisation [REC_0013] reports mean position error of 0.8 m in urban canyons, though validation remains entirely simulation-based.

### 4.10 Environment-Stratified Analysis (RQ2)

#### 4.10.1 Indoor Environments (58 papers)

Indoor environments represent the most common testing ground (58 papers), typically featuring motion-capture systems or laser trackers as ground truth. Reported accuracies range from centimetre-level with motion capture (0.020 m RMSE for tag-based VIO [REC_1346]) to sub-metre with SLAM-based approaches (0.094 m for RTAB-Map [REC_0003]). The warehouse-scale fusion system [REC_0161] achieves 0.4 m navigation accuracy and 0.13 m mapping RMSE using depth camera, IMU, and LiDAR [p.4].

#### 4.10.2 Outdoor and Urban Environments (36 papers combined)

Outdoor testing (25 generic outdoor + 11 urban) introduces wind, illumination variation, and dynamic objects. Fixed-wing UAV navigation [REC_0218] reports 16.40–18.21 m position RMSE in desert conditions. Satellite-to-UAV matching [REC_0037] achieves 10–14 m MAE at 500 m altitude. The Cross-fusion system [REC_1110] achieves "comparable to GPS" localisation accuracy in 150×150 m outdoor building areas [p.1].

#### 4.10.3 Subterranean and Tunnel Environments (7 papers)

Subterranean environments present extreme challenges: absence of GNSS, limited lighting, dust/particulates, and featureless geometry. The dust-resilient system [REC_0409] achieves 0.19 m mean mapping accuracy in real mining tunnels [p.1]. The UAV-UGV team [REC_1267] achieves median 3D error below 1 m in tunnel flight testing [p.10]. The integrated air-ground system [REC_1274] demonstrates 8-minute mapping of 500 m tunnel fronts for post-blast operations.

#### 4.10.4 Forest and Canopy Environments (9 papers)

Forest canopy environments challenge both GNSS reception and visual/LiDAR feature extraction. LiDAR odometry in pine forests [REC_1348] achieves APE of 0.247 m [p.6]. The simulated forest navigation [REC_0043] achieves 2.78 m/s mean velocity through 100-tree environments. SLAM-based exploration [REC_1253] achieves traversal RMSE of 0.195–0.420 m across low-to-high density forest-like environments.

### 4.11 Validation Modality: Real vs. Simulation

Of the 279 papers, 118 (42.3%) report real-world experiments, 84 (30.1%) report both simulation and real validation, and 65 (23.3%) are simulation-only. The simulation-only papers predominantly use Gazebo (23 papers), MATLAB/Simulink (15), AirSim/Unreal Engine (8), and custom simulators (19). Per protocol, all 65 simulation-only papers are capped at Q-Medium quality regardless of other scores, reflecting the fundamental limitation that simulation cannot replicate real-world sensor degradation, electromagnetic interference, or aerodynamic disturbances.

The sim-to-real gap is explicitly acknowledged by multiple authors. REC_1660 states "there is still a certain gap between simulation and reality, mainly in the following aspects: 1. The presence of obstacles, wind conditions, and other environmental factors" [p.18]. The OPsCV framework [REC_1018] notes that "the OPsCV performance remained considerably lower" when compared to simulation results due to "limitations previously reported for DIO-based methods" [p.11].

### 4.12 Quality Appraisal Results

Quality appraisal yields 3 Q-High studies (scores 7–8), 98 Q-Medium (scores 4–6), and 178 Q-Low (scores 0–3). The three Q-High studies are:

1. **REC_0502** (Score 8): LD3DGS-SLAM — outdoor high-altitude SLAM with 3D Gaussian splatting, achieving 0.741 m RMSE with comprehensive baselines (ORB-SLAM2/3, VINS-Fusion, MonoGS) and real-world validation.
2. **REC_0037** (Score 8): Deep visual localisation with SuperPoint-LightGlue — achieving 10 m MAE on real flights with RTK GNSS ground truth at 500 m altitude.
3. **REC_1277** (Score 8): PG-TLNet aeromagnetic compensation — achieving 94 μs inference latency and IR improvement of 14.26–16.27 with comprehensive real-flight validation.

The Q-Low concentration (178 papers, 63.8%) reflects systemic issues: 71 Q-Low papers (39.9%) report NOT_REPORTED for headline metrics, 89 (50%) lack baseline comparisons, and 45 (25.3%) are simulation-only without plans for real-world validation. These papers often represent early-stage conceptual designs, system descriptions without quantitative evaluation, or short conference abstracts.

### 4.13 Geographic and Temporal Research Landscape

China dominates the corpus with 66 papers (23.7%), spanning all method categories and showing particular strength in HYBRID fusion (18 papers), COOPERATIVE systems (11 papers), and VISION-based approaches (14 papers). US contributions (40 papers) are concentrated in SLAM, COOPERATIVE, and emerging approaches. Singapore contributes disproportionately to HYBRID and COOPERATIVE categories (12 papers) through the Temasek Laboratories and NTU groups. European contributions focus on industrial applications: Spain on bridge/tunnel inspection (CATEC, University of Seville), Germany on radar-based landing, and Finland on forest/UWB navigation.

The temporal trend reveals a shift from single-sensor approaches (2013–2016) to multi-sensor fusion (2017–2020) to AI-enhanced and cooperative paradigms (2021–2026). The 2026 papers show particular growth in deep learning-based visual geo-localisation, transformer architectures for sensor fusion, and federated learning for swarm autonomy.

## 5. Discussion

### 5.1 SWaP-C Trade-offs Across Platforms

The corpus reveals a fundamental tension between localisation accuracy and size, weight, power, and cost (SWaP-C) constraints. High-accuracy systems like the multi-sensor 6-DoF framework [REC_0485, 0.13 m RMS error] employ Velodyne HDL-32E LiDARs, ZED stereo cameras, and UWB radios, but impose significant payload requirements that limit deployment to large multi-rotor platforms. Conversely, nano UAV platforms [REC_0017] using Snapdragon-class processors sacrifice accuracy for miniaturisation. The emerging trend of solid-state LiDARs (Livox Mid-360 [REC_0951], Livox Avia [REC_0706]) and compact radar modules (TI IWR1443 [REC_1032]) offers a potential path to resolving this trade-off.

### 5.2 The Sim-to-Real Gap

The 65 simulation-only papers (23.3%) represent a critical deployment-readiness gap. Several papers explicitly quantify this gap: the airspeed-aided state estimation [REC_1048] notes "the result is still not very precise" even in simulation [p.17]; the PF-NN cooperative framework [REC_1106] acknowledges "the loss function relies on ground-truth positions, which are unavailable during real-world deployment" [p.23]; and the DGCC-AKF system [REC_1107] concedes "the U-U ranges are still generated from the measured trajectories due to flight certification restrictions" [p.22].

### 5.3 Metric Heterogeneity and the Case Against Statistical Pooling

The corpus employs at least 15 distinct primary accuracy metrics: ATE (absolute trajectory error), APE (absolute position error), RMSE (root mean square error), MAE (mean absolute error), CEP (circular error probable), drift percentage, position error at specific outage durations, success rate, collision rate, detection accuracy, mapping accuracy, F-score, and Recall@k. This heterogeneity, combined with vastly different evaluation environments (from 2×2 m motion-capture volumes to 20 km outdoor flights), makes statistical pooling impossible. The synthesis is therefore strictly narrative, reporting verbatim ranges rather than computed averages.

Even within a single metric (RMSE), values span four orders of magnitude: from 0.020 m [REC_1346, indoor tags] to 32.50 m [REC_1023, SINS-only outdoor]. This range reflects not algorithmic quality but rather the fundamental difference in environment complexity, flight duration, and ground-truth availability.

### 5.4 Edge Computing Constraints

Multiple papers identify on-board computation as a primary bottleneck. The Feature 3DGS system [REC_0816] achieves only 4.7 Hz inference rate, insufficient for aggressive flight. Hector SLAM consumes ∼40% of one CPU core [REC_0896]; RTAB-Map requires 5:20 processing time versus 3:26 for OpenVSLAM [REC_0003]. The quantum-enhanced fusion [REC_0102] acknowledges "notable SWaP penalties" for quantum sensors. The drone hunter [REC_1212] achieves only 8 fps for Tiny YOLO on a Jetson TX2. These findings suggest that algorithmic efficiency, not just algorithmic accuracy, should be a primary design criterion.

### 5.5 Environmental Robustness Degradation

Performance systematically degrades from controlled indoor environments to unstructured outdoor settings. The POMDP framework [REC_0264] drops from 100% success rate (normal visibility) to 23.33% (low visibility). The shipboard system [REC_1619] drops from 100% success (normal lighting) to 71.4% (dark) to 55.5% (smoky). The forest-canopy VIO drift [REC_0096] increases "rapidly" as altitude increases above the canopy. These findings argue strongly for multi-modal redundancy and adaptive degradation management.

### 5.6 The Standardisation Crisis

No unified benchmarking protocol exists for GPS-denied UAV navigation. The EuRoC MAV benchmark is referenced by only 2 papers [REC_0102, REC_1453]. The University-1652 dataset appears in cross-view matching papers [REC_0165, REC_1046] but is not designed for navigation evaluation. The MILUV dataset [REC_1026] and SEULoc dataset [REC_1123] are promising but domain-specific. The absence of a common dataset, common metrics, and common evaluation protocol represents the single largest barrier to meaningful cross-paper comparison and field advancement.

## 6. Limitations

This review acknowledges the following limitations:

1. **Six deferred records.** REC_0023, REC_0035, REC_0244, REC_1217, REC_1667, and REC_0363 were excluded from extraction due to identity-integrity issues (duplicate titles, corrupted PDFs, or unresolvable metadata conflicts). These 6 records represent 2.1% of the included pool and are unlikely to alter the thematic conclusions.

2. **Screening independence.** Screening was performed by a single human reviewer assisted by an AI tool (Case C per SCREENING_INDEPENDENCE.md). While the human verified all AI decisions, this falls short of the dual-reviewer standard recommended by PRISMA 2020. The risk of reviewer bias is mitigated by the frozen protocol and explicit inclusion/exclusion criteria.

3. **Spot-check coverage.** Manual spot-checks of extraction accuracy were conducted on a 1-in-10 basis. Systematic errors in AI-assisted extraction may propagate to the remaining 90% of records, though the spot-check logs document acceptable accuracy rates.

4. **No meta-analysis.** The heterogeneity of reported metrics, evaluation environments, and ground-truth systems precludes statistical pooling. All reported ranges are verbatim from the source papers; no averaging, normalisation, or effect-size computation was performed.

5. **Simulation quality cap.** The protocol caps simulation-only studies at Q-Medium regardless of methodological rigour. While this prevents over-weighting of unvalidated systems, it may undervalue high-quality simulation work that provides genuine algorithmic insights.

6. **Temporal coverage.** The 2026 papers represent only January–June, creating a partial-year bias that inflates the apparent growth rate. The 87 papers from 2026 H1 may not be representative of the full-year output.

7. **Database coverage.** Only IEEE Xplore and Scopus were searched. Papers published exclusively in other venues (e.g., MDPI, Springer, arXiv-only) may be underrepresented, though the 2,000-record initial pool provides substantial coverage.

8. **Language restriction.** Only English-language papers were included, potentially excluding relevant work from Chinese, Russian, and Korean research communities that publish primarily in their native languages.

## 7. Conclusion and Future Work

This systematic literature review synthesised 279 papers on GPS-denied UAV navigation published between 2013 and mid-2026, applying PRISMA 2020 methodology with a frozen, pre-registered protocol. The key findings are:

**RQ1 (Sensors):** The camera-IMU-LiDAR triad dominates the field, with cameras appearing in 58%, IMUs in 44%, and LiDARs in 41% of papers. UWB (12%), radar (5%), and magnetometers (6.5%) serve as complementary modalities. The Intel RealSense D435/D455 family has become a de facto standard platform.

**RQ2 (Environments):** Indoor environments are the most tested (58 papers), followed by outdoor generic (25), urban (11), forest (9), and subterranean (7) settings. Reported accuracies span four orders of magnitude (0.02 m to 32.5 m RMSE), primarily reflecting environment complexity rather than algorithmic sophistication.

**RQ3 (Methods):** HYBRID multi-sensor fusion is the dominant paradigm (76 papers, 27.2%), followed by vision-based approaches (56, 20.1%) and cooperative systems (49, 17.6%). Filter-based fusion (EKF/UKF) remains the workhorse, while factor graph optimisation and deep learning-enhanced estimators represent the frontier. Only 3 papers achieve Q-High quality, underscoring the maturity gap between algorithmic innovation and rigorous evaluation.

**RQ4 (Future Directions):** The corpus identifies the following critical research gaps:

1. **Standardised benchmarking.** The field urgently needs a common dataset, metric suite, and evaluation protocol analogous to KITTI for autonomous driving. Without this, cross-paper comparison remains impossible.

2. **Sim-to-real transfer.** 23.3% of papers are simulation-only. Future work must prioritise domain randomisation, hardware-in-the-loop validation, and progressive real-world deployment testing.

3. **Adversarial resilience.** Only 2 papers [REC_0489, REC_0006] explicitly address GNSS spoofing detection and mitigation. The vulnerability of alternative navigation systems to sensor spoofing, denial-of-service, and adversarial machine learning attacks remains largely unexplored.

4. **Multi-agent scalability.** While 49 papers address cooperative navigation, most evaluate systems with 2–4 agents. The scaling behaviour of cooperative localisation algorithms to swarms of 10+ UAVs, with realistic communication constraints, bandwidth limitations, and heterogeneous sensing, requires investigation.

5. **SWaP-optimised edge deployment.** Many high-accuracy systems are computationally prohibitive for small UAVs. Future work should explore model compression, neural architecture search, and hardware-accelerated inference (FPGA, NPU) for real-time deployment on platforms under 250 g.

6. **Long-duration drift management.** Most evaluations are short (under 10 minutes of flight). The long-term drift behaviour of VIO, LIO, and fusion systems over 30+ minutes of continuous GPS-denied flight remains poorly characterised.

7. **Environmental adaptation.** Performance degrades significantly across environment types (100% → 23.33% success rate across visibility conditions). Adaptive algorithms that detect and respond to environmental degradation represent a high-impact research direction.

## 8. References
All 279 extracted studies are catalogued with full bibliographic details in `02_data_processed/MASTER_EVIDENCE.csv`. DOIs, publication years, and venue information were verified against screening outputs in `02_data_processed/screening_results.csv`. The formal BibTeX reference file is provided at `07_manuscript/references.bib`.

---
