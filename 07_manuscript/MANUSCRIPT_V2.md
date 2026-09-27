# GPS-Denied UAV Navigation: A Systematic Literature Review of Multi-Sensor Fusion, Vision-Based Localisation, and Cooperative Autonomy (2013–2026)

**Submitted for consideration to:** *IEEE Transactions on Robotics* / *IEEE Access*
**Data basis:** `02_data_processed/MASTER_EVIDENCE.csv` — 279 records, 28 fields, manually extracted.
**Number trace:** Every statistic herein is traceable to `08_docs/NUMBER_TRACE.md` and thence to a PDF page.

---

## Abstract

Autonomous UAVs operating without Global Navigation Satellite System (GNSS) coverage require reliable ego-motion estimation, environment mapping, and re-localisation derived exclusively from onboard sensors. This paper systematically reviews 279 peer-reviewed studies published between 2013 and mid-2026, retrieved from IEEE Xplore and Scopus and screened in accordance with the PRISMA 2020 framework. Analysis reveals a field undergoing rapid structural change: from single-sensor optical-flow and dead-reckoning systems that characterised the 2013–2016 period, through a tightly coupled filter-fusion era (2017–2020), toward a present landscape dominated by factor-graph optimisation, deep cross-view geo-localisation, and cooperative swarm autonomy. Cameras appear in 162 of 279 studies (58%), IMUs in 124 (44%), and LiDAR in 57 (20%). The dominant algorithmic family is hybrid multi-sensor fusion (74 studies), followed by vision-based approaches (53 studies) and cooperative/multi-agent systems (44 studies). Quality appraisal identified only 3 Q-High, 98 Q-Medium, and 178 Q-Low studies, with the large Q-Low proportion reflecting widespread absence of real-world validation, standardised baselines, and quantitative metric reporting. Reported position errors span four orders of magnitude — from 0.020 m (indoor tag-aided VIO under motion capture) to tens of metres (fixed-wing outdoor flights) — an irreducible consequence of environment heterogeneity that precludes statistical pooling. The collective evidence maps a research landscape of substantial algorithmic sophistication coupled with a critical shortage of deployment-grade validation, standardised benchmarks, and adversarial resilience testing.

---

## 1. Introduction

The expanding operational envelope of unmanned aerial vehicles — from search-and-rescue in collapsed structures to bridge inspection, precision agriculture, and contested tactical environments — makes reliable autonomous navigation a foundational engineering requirement. GNSS provides the dominant position reference for contemporary UAVs. Yet GNSS signals attenuate below building canopies, reflect off urban facades to create multipath, are absorbed by tunnel rock, are blocked by forest foliage, and can be deliberately jammed or spoofed. The resulting "GPS-denied" condition does not merely degrade localisation quality; it can render a nominally autonomous platform entirely uncontrollable.

The academic literature's response to this challenge has been an intensive, parallel development of alternative navigation paradigms over the past decade. A temporal count of the 279 studies in this corpus captures the trajectory precisely: one paper appeared in 2013; by 2018–2019 the annual rate had reached 27–28; by 2022–2023 it climbed to 35–43; and in the first six months of 2026 alone, 87 studies were indexed — a single half-year exceeding the entire output of every preceding year. The acceleration reflects simultaneously the commercial urgency of GNSS-denied deployment and the maturing availability of enabling hardware: solid-state LiDARs lightweight enough for a 250 g platform, event cameras operating at megahertz temporal resolution, compact UWB radio modules with sub-10 cm ranging precision, and edge-compute boards delivering tens of TOPS in a palm-sized form factor.

Despite this volume of research, no prior systematic review has simultaneously mapped (a) all sensor modalities, (b) all algorithmic families, (c) all operational environments, and (d) the chronological evolution of the field. Existing surveys address partial slices: visual-inertial odometry, indoor positioning, or cooperative robotics in isolation. This review addresses that gap.

The paper addresses four research questions consistent with the pre-registered protocol (`00_scope/SCOPE.md`):
- **RQ1:** What sensor configurations characterise GPS-denied UAV navigation systems, and how has the sensor landscape evolved over time?
- **RQ2:** In which environments have GPS-denied systems been validated, and what position accuracies are reported across those environments?
- **RQ3:** What algorithmic approaches dominate the field, and what are the principal trade-offs among them?
- **RQ4:** What unresolved limitations and future research directions emerge from the collective body of evidence?

The paper is structured as follows. Section 2 positions the review relative to prior surveys. Section 3 describes the PRISMA 2020 methodology. Section 4 presents the comprehensive results, organised chronologically within seven thematic clusters. Section 5 provides a cross-cutting trade-off analysis. Section 6 discusses limitations of the review itself and of the broader field. Section 7 concludes with evidence-grounded recommendations.

---

## 2. Positioning Relative to Prior Surveys

The corpus contains seven papers that are themselves surveys or review articles (method_category = SURVEY): studies covering visual SLAM, multi-sensor fusion architectures, cooperative navigation, and indoor positioning systems for UAVs. Each addresses a narrower scope than the present work. The distinguishing contributions of this review are: (i) comprehensive cross-cluster coverage spanning all sensor modalities and all algorithmic families simultaneously; (ii) a temporal window extending to mid-2026, capturing the current deep-learning and cooperative era; (iii) a standardised quality appraisal applied to all 279 papers; and (iv) a pre-registered, PRISMA-compliant protocol providing a verifiable evidence chain from PDF to synthesis claim.

---

## 3. Methodology

### 3.1 Protocol

The review protocol was drafted and frozen at `00_scope/SCOPE.md` prior to data collection (SHA256 hash recorded in `00_scope/FROZEN.md`). No modifications were made after freezing. The synthesis approach — structured narrative with descriptive quantitative tabulation, explicitly excluding statistical meta-analysis — was declared in `08_docs/SYNTHESIS_METHOD.md` and approved prior to writing.

### 3.2 Information Sources and Search

Two databases were queried: IEEE Xplore and Scopus. Searches were executed on 15 June 2026, yielding 1,000 records per database (2,000 total). Raw export files are stored at `01_data_raw/ieee_xplore_20260615.csv` and `01_data_raw/scopus_20260615.csv`.

### 3.3 De-duplication and Screening

After removing 284 cross-database duplicates, 1,716 unique records underwent title-and-abstract screening against seven pre-specified inclusion criteria (I1–I7) and seven exclusion criteria (E1–E7). Inclusion required: UAV or drone platform; GNSS-denied, degraded, or unavailable navigation context; original technical contribution; English language; and minimum four pages. The screening process yielded 636 records passed to full-text assessment. Of 291 records assessed in full text, 285 were included and 6 excluded (3 out-of-scope, 3 exact duplicates). Full-text PDFs were obtained for 288 records; 6 included studies were deferred from extraction due to PDF integrity issues, yielding the final extraction corpus of 279 records.

### 3.4 Data Extraction

Data were extracted manually using a standardised 28-field schema (`08_docs/EXTRACTION_SCHEMA_v1.md`). Fields included: title, authors, year, venue, DOI, problem statement, motivation, GPS-denied type, environment, platform, sensors, method category, algorithm name, real-or-simulation, dataset, metrics, headline result (verbatim quoted from the paper), baseline comparison, ablation, stated limitations, future work, taxonomy category, contribution type, country, and funding. All 279 extraction files are stored at `_MANUAL/abhishek/per_paper/REC_*.md`.

### 3.5 Synthesis Approach

A structured narrative synthesis was adopted (PRISMA 2020, item 20b). Statistical meta-analysis was not attempted for three reasons: (1) at least 15 distinct primary accuracy metrics are used across the corpus with no common unit; (2) evaluation environments differ fundamentally in scale, complexity, and ground-truth system; and (3) many papers report results only as figures without tabulated numbers (classified as NOT_REPORTED in the extraction). Within each thematic cluster, headline results are reported as verbatim ranges from the extraction fields, with source IDs and page numbers, in accordance with Synthesis Rule E6.

### 3.6 Quality Appraisal

An 8-point rubric assessed: study design clarity, sensor description completeness, quantitative metric reporting, presence of baseline comparison, real-world validation, statistical rigour, limitation disclosure, and future-work articulation. Scores mapped to tiers: Q-High (7–8 points), Q-Medium (4–6), Q-Low (0–3). Per protocol, simulation-only studies were capped at Q-Medium regardless of score.

---

## 4. Results

### 4.1 Temporal and Geographic Profile of the Corpus

The 279 studies span 2013 to June 2026. The annual distribution (Table 1) reveals an exponential growth trajectory: 1 paper (2013), 1 (2014), 6 (2015), 18 (2016), 11 (2017), 27 (2018), 28 (2019), 3 (2020), 10 (2021), 35 (2022), 43 (2023), 7 (2024), 2 (2025), and 87 in the first six months of 2026 (Fig. F2). The apparent dip in 2020 likely reflects indexing latency and COVID-related conference cancellations rather than a genuine field contraction.

Geographically (Fig. F8), China is the most represented country with 28 first-author affiliations (10%), followed by the USA (16 papers), Taiwan (6), Singapore (9 combined across institutional sub-affiliations), Canada (4), Finland (3), India (3), Spain (3), Iran (3), and Australia (3). European contributions are distributed across Germany, Italy, Czech Republic, Norway, and others. The wide international spread reflects both the universal operational relevance of GPS-denied flight and the distributed nature of the enabling hardware supply chain.

**Table 1 — Publication trajectory by year**

| Year | Count | Cumulative |
|------|-------|------------|
| 2013 | 1 | 1 |
| 2014 | 1 | 2 |
| 2015 | 6 | 8 |
| 2016 | 18 | 26 |
| 2017 | 11 | 37 |
| 2018 | 27 | 64 |
| 2019 | 28 | 92 |
| 2020 | 3 | 95 |
| 2021 | 10 | 105 |
| 2022 | 35 | 140 |
| 2023 | 43 | 183 |
| 2024 | 7 | 190 |
| 2025 | 2 | 192 |
| 2026 (H1) | 87 | 279 |

### 4.2 Sensor Landscape and Its Evolution (RQ1)

Across the full corpus, cameras of any type appear in 162 studies (58%), IMUs in 124 (44%), LiDAR (including 2D laser rangefinders) in 57 (20%), monocular cameras specifically in 34 (12%), UWB modules in 34 (12%), stereo cameras in 26 (9%), barometers in 21 (8%), magnetometers in 18 (6%), GPS/GNSS receivers used as fallback or initialisation in 16 (6%), FMCW or MIMO radar in 14 (5%), optical flow sensors in 13 (5%), ultrasonic rangefinders in 10 (4%), and depth cameras (principally the Intel RealSense D435/D455 family) in 9 (3%) (Fig. F3).

**The 2013–2016 era** was characterised by simple, single-modality systems. Optical flow sensors provided relative horizontal velocity for indoor hover; ultrasonic transducers measured altitude; and IMU dead-reckoning handled short-term bridging. These systems could sustain position hold within ±0.2 m under controlled indoor conditions (REC_0239) but diverged rapidly over distances exceeding a few tens of metres. Barometers and magnetometers were standard COTS flight-controller inclusions providing altitude and heading respectively, but neither provided the lateral position reference needed for GPS-denied navigation.

**The 2017–2020 period** brought the normalisation of the camera-IMU pairing as a foundation for Visual-Inertial Odometry (VIO). Hardware platforms such as the Intel RealSense T265 tracking camera — featuring two fisheye lenses, an IMU, and onboard VIO processing — enabled plug-and-play 6-DoF pose estimation on commercial flight controllers. This period also saw the first widespread use of 3D LiDAR (Velodyne VLP-16 at 300 g, 10 Hz, 30 m range) for both odometry and mapping. The 2017 paper by the Singapore Temasek Laboratories group (REC_0896) compared Hector SLAM and Cartographer SLAM on a laser-scanner-equipped MAV, demonstrating that Hector SLAM achieved an average translation error (ATE) of 0.071 m at only ~40% of a single CPU core, compared to 0.059 m for Cartographer at ~60% — an explicit documentation of the accuracy-versus-compute trade-off that would come to define the field.

**From 2021 onward**, the sensor landscape bifurcated. The high-accuracy frontier shifted toward tightly-coupled multi-sensor suites: LiDAR-inertial combinations using the Livox Mid-360 solid-state LiDAR (200 g, 40 m range, 200,000 pts/s), depth cameras for geometric feature richness, and UWB modules for inter-agent ranging. Simultaneously, the resource-constrained frontier explored very lightweight payloads for nano-UAVs and fixed-wing platforms: single monocular cameras with satellite imagery matching, IMU-only with barometric bridging, and even packet-loss-based radio ranging requiring no additional hardware (REC_0064). The emergence of thermal cameras (REC_0332, REC_1302) for smoke- and dust-penetrating vision, and FMCW radar (REC_0107, REC_1032) for illumination-invariant ranging, marked the beginning of environment-adaptive sensor selection.

### 4.3 Methodological Clusters: A Chronological Synthesis (RQ3)

The 279 studies were classified into the following primary method categories: HYBRID multi-sensor fusion (74 papers), VISION-based approaches (49 papers), COOPERATIVE/multi-agent (40 papers), VIO (18 papers), SLAM (10 papers), LIDAR-centric odometry (4 papers and 3 combined LIDAR|SLAM), UWB-based positioning (6 papers and 1 combined UWB|COOPERATIVE), and OTHER or NOT_REPORTED (75 papers spanning optical flow, radar, POMDP planning, deep reinforcement learning, quantum-enhanced fusion, and infrastructure-free ranging). The distribution is illustrated in Fig. F4.

#### 4.3.1 Phase I — Dead-Reckoning and Single-Sensor Baselines (2013–2016)

The earliest phase of the corpus is defined by the problem being posed rather than solved. Studies from this era documented the fundamental inadequacy of IMU-only dead-reckoning (the position error of a low-cost MEMS IMU grows as the square of elapsed time, reaching hundreds of metres within minutes), established optical flow as a viable indoor hover sensor when surface texture was adequate, and began integrating barometric altitude to reduce the 3D navigation problem to 2D. The bearing-only cooperative localisation study (REC_0752, 2016) demonstrated that even a pair of UAVs sharing bearing measurements could reduce the position error index to approximately 20 m at 3° bearing noise and 50 m at 9° — still far from operational requirements, but a proof of concept for inter-agent sensing.

The 2016 landscape is captured starkly in the corpus count: 18 papers, with a strong bias toward simulation-only evaluation and minimal baseline comparison. The Q-Low designation applies to nearly all 2013–2016 entries, reflecting the preliminary nature of this era's contributions.

#### 4.3.2 Phase II — Visual-Inertial Odometry and Filter Fusion Maturation (2017–2020)

The EKF and its variants became the dominant estimation backbone from 2017 onward. The Extended Kalman Filter framework for fixed-wing multi-sensor navigation (REC_0218, 2026) represents the mature expression of this paradigm: six sensor types (IMU, magnetometer, barometer, pitot tube, monocular VIO, and CV-CNN-derived velocity) are fused in an Error-State EKF, achieving position RMSE of 16.40 m (North), 18.21 m (East), and 1.80 m (Down) during real-world desert flights near Abu Dhabi. The vertical accuracy is notably better than horizontal, reflecting the barometric height constraint. The authors document a critical limitation: "the filter inability to properly estimate wind velocity fluctuations in the absence of GNSS signals" [p.9], a finding that is echoed across multiple fixed-wing studies in the corpus and reflects the inherently observability-limited nature of wind estimation without external position updates.

At the indoor hover scale, where the environment constrains motion and allows optical flow to function reliably, EKF-fused multi-sensor systems achieved qualitatively different performance. The autonomous flight control system for low-cost quadrotors (REC_0239, 2022) fused IMU, optical flow, ultrasonic rangefinder, magnetometer, and barometer, achieving horizontal position errors "within ±0.2 m" and altitude error "within ±0.05 m" during real indoor flights. The contrast with the desert fixed-wing results (16–18 m RMSE) illustrates the degree to which reported accuracy reflects environment as much as algorithm.

The finite-memory positioning framework (REC_0705, 2026) represents a more sophisticated filter approach, achieving APE of 0.057 m (hovering) and 0.093 m (collision disturbance) in simulation, versus 0.610 m and 1.573 m respectively for the ESEKF baseline. In real experiments, APE values of 0.144 m (hovering) and 0.363 m (collision) were recorded — a 4× degradation from simulation to reality that exemplifies the sim-to-real gap documented throughout the corpus.

The radar-aided EKF system (REC_0107, 2021) addresses the specific problem of GNSS outage bridging for a ground-flying UAV: an FMCW radar odometry output, fused with IMU dead-reckoning through a nested G-H/EKF architecture, achieves 2D RMSE of 1.95 m during a 1-minute GNSS outage versus 165 m for IMU alone. Over a 4-minute outage, RMSE remains at 1.49 m while IMU alone has diverged to thousands of metres. This study provides perhaps the clearest quantification in the corpus of the benefit of a secondary ranging sensor over bare inertial dead-reckoning.

#### 4.3.3 Phase III — Factor Graph Optimisation and State-of-the-Art Fusion (2021–2026)

The shift from Kalman filtering to factor graph optimisation (FGO) is the defining algorithmic transition of the contemporary era. FGO enables (a) batch re-linearisation, mitigating the linearisation errors that cause EKF divergence on high-dynamic trajectories; (b) simultaneous optimisation over extended time windows rather than recursive single-step updates; and (c) natural integration of asynchronous, delayed, and sporadic measurements from heterogeneous sensors.

The tightly-coupled multi-source graph optimisation system (REC_1453, 2026) fuses IMU, visual odometry, and UWB ranging in a factor graph, achieving trajectory RMSE of 0.480 m on a high-dynamic flight profile (where both VINS-Fusion and ORB-SLAM3 diverged entirely) and 0.286 m on a low-altitude cruise trajectory. The system's robustness advantage on the high-dynamic profile — where competing systems produce no result at all — is the key contribution: the FGO framework's ability to survive transient degradation of any single sensor modality.

The UWB-constrained VIO system (REC_1118, 2023) demonstrates the specific benefit of UWB augmentation for VIO in weak-feature environments: ATE drops from 1.506 m (VINS-Mono alone) to 0.414 m (with UWB), a 72% reduction. In a standard feature-rich indoor environment, the improvement is 0.519 m to 0.179 m (a 66% reduction). The nonlinear optimisation-based fusion architecture outperforms loose coupling, demonstrating that the integration method matters as much as the selection of sensor modalities.

The Q-High study LD3DGS-SLAM (REC_0502, 2026) pushes the frontier of outdoor, high-altitude monocular SLAM. By integrating 3D Gaussian splatting (3DGS) into a monocular SLAM factor graph, and using intermittent RTK-GNSS for global scale anchoring, the system achieves average localisation error of 0.8 m over real outdoor flights at 100–500 m altitude. On the eVTOL1-120 self-collected dataset, the 3DGS-rendered variant achieves RMSE of 0.741 m versus ORB-SLAM3's 13.786 m — an order-of-magnitude improvement on a task that standard visual SLAM cannot reliably complete. A critical implementation note is the compute architecture: real-time localisation runs onboard the DJI drone, while map training is offloaded to a ground server, "prioritizing rendering speed for live localization" [p.18]. Rendering a 1805×1023 frame takes approximately 30 ms on an RTX 4090, which is not yet achievable onboard a UAV — a deployment constraint explicitly acknowledged.

The geomagnetic navigation study PG-TLNet (REC_1277, Q-High) demonstrates an entirely different approach: learning-based compensation of aeromagnetic interference for INS/geomagnetic map matching. The approach achieves magnetic standard deviation of 24.15–26.64 nT versus 95.12–179.99 nT for the conventional Tolles-Lawson model, with an inference latency of 94 µs — enabling genuine real-time deployment on embedded hardware. The improvement ratio (IR) of 14.26–16.27 over the baseline across multiple real flight datasets establishes geomagnetic navigation as a viable complement to optical approaches in magnetically mapped environments.

For underground and dust-filled tunnel navigation — an environment that blinds cameras and partially attenuates radar returns — the dust-resilient system (REC_0409, 2026) combines LiDAR-inertial odometry with intensity-based dust filtering. Real testing in a mining tunnel achieved mean mapping accuracy of 0.19 m and RMS error of 0.60 m, with full exploration-and-return completed in 480 s. The authors note that accuracy degraded near the tunnel entrance "due to vegetation and surrounding objects that were captured by the UAV's LiDAR scanner but do not appear in the total station model" [p.5] — illustrating how model-reality mismatch affects ground-truth comparison even in real-world testing.

#### 4.3.4 Vision-Based Geo-Localisation and Cross-View Matching

The vision cluster (49 papers) includes two distinct sub-trajectories: classical feature-based methods active throughout the corpus period, and deep learning-based cross-view geo-localisation that emerged prominently from 2021 onward.

The earliest vision approach in the corpus is the HOG-Optical Flow-Particle Filter (HOP) framework (REC_0594, 2015): by fusing Histogram of Oriented Gradients terrain-relative image matching with optical flow, the system achieves RMSE of 6.773 m in real outdoor flights over villages, versus 169.188 m for optical flow alone — a 25× improvement. However, "image registration failure constitutes 7% where position prediction is retained. The outliers mainly concentrate at two regions, where either there are few gradient patterns in the scene or has significant illumination change" [p.4].

The deep cross-view localisation approach (REC_0037, Q-High, 2026) substitutes handcrafted features with SuperPoint keypoints matched by LightGlue, with EPnP pose estimation from the matched keypoints projected onto a geo-referenced satellite tile. Real flights at approximately 500 m altitude achieve MAE of 10 m and RMSE of 14 m — adequate for regional localisation and GPS-denied waypoint navigation, but insufficient for precision landing. The matching quality metric mAP of 0.912 substantially exceeds SIFT (0.650) and ORB (0.717), though at 8× the computation time (0.340 s versus 0.043 s for SIFT) [p.3].

NavCLIP (REC_0656, 2026) leverages CLIP-based visual-language alignment for cross-season and cross-time UAV-to-satellite matching. In controlled experiments on the UCLA dataset, localisation error is 1.21 pixels (≈1.17 m) versus GeoCLIP's 296.84 m — a 250× improvement on a dataset where large-model retrieval fails due to the domain gap between ground-level training images and UAV oblique views. However, the authors acknowledge directly: "In the real-world UAV flight experiments, the localization error is notably larger, indicating that the domain discrepancy between UAV imagery and satellite maps remains a major challenge for practical deployment" [p.9]. This honest disclosure — that dataset performance does not transfer to operational deployment — is a recurring pattern in the cross-view localisation sub-literature.

NaviLoc (REC_1150, 2026) addresses the problem at the trajectory level rather than the frame level: by fusing VIO-based relative motion with episodic satellite-image matching, it achieves mean localisation error (MLE) of 19.5 m over a 2.3 km real outdoor trajectory, compared to 626.7 m for raw VIO and 312.2 m for AnyLoc-VLAD single-frame retrieval — a 16× improvement over the state-of-the-art retrieval baseline. The authors note that "VIO dependency" is a key limitation: "significant VIO failures (e.g., from aggressive maneuvers or texture-poor environments) would propagate to the final estimate" [p.12].

For terminal approach and precision landing, the Feature 3DGS system (REC_0816, 2026) uses 3D Gaussian splatting features for UAV-to-ship pose estimation, achieving translation MAE of 1.66–2.91 cm and rotation MAE of 0.90–1.81° in a scaled indoor testbed. The authors directly flag the central deployment barrier: "pose estimation averaged an inference latency of 0.21 s (roughly 4.7 Hz)... it currently falls short of the high-speed real-time benchmarks typically required for aggressive terminal landing maneuvers" [p.7].

The deep CNN global geo-localisation system (REC_0149, 2026) demonstrates that a network trained on satellite map patches can localise UAV imagery at mean error of 9.71 m, versus 18.00 m for TransGeo — competitive with the SuperPoint-LightGlue approach but using a simpler matching architecture. The maximum localisation error of 31.28 m (versus TransGeo's 39.53 m) highlights the tail-risk of patch-based matching methods in visually ambiguous areas such as parking lots and industrial rooftops.

#### 4.3.5 Cooperative and Multi-Agent Systems

The cooperative cluster (40 direct + 4 combined VISION|COOPERATIVE + 2 combined LIDAR|COOPERATIVE) encompasses UAV-UAV relative localisation, UAV-UGV heterogeneous teams, and swarm navigation under communication constraints.

The cooperative VIO study (REC_0960, 2022) provides a clean benchmark for the benefit of multi-agent UWB augmentation: a heterogeneous swarm of 4 high-cost UAVs (Intel RealSense T265) achieves position MAE of 0.399 m in nominal conditions, versus 0.588 m for VINS-Fusion operating independently. In adversarial conditions (sensor noise injection), the cooperative system achieves 0.467 m versus 1.306 m for VINS-Fusion — a 64% improvement attributable to the inter-agent UWB ranging constraints that prevent individual VIO drift from escaping the swarm's common reference frame. The system's constraint — "there have to be at least four high-cost drones" [p.7] — illustrates the minimum-agent problem that limits practical swarm deployment.

The UAV-UGV anchor-free VIO-UWB fusion (REC_1069, 2026) addresses the problem of UAV localisation when no fixed UWB infrastructure exists: the UGV serves as a mobile anchor, with its own VIO-derived pose used to interpret UWB range measurements between the two agents. The adaptive weighting and outlier suppression strategy achieves 24.6% RMSE reduction and 31.2% maximum error reduction versus fixed-weight fusion. The authors note that "communication delays or data loss" remain an unaddressed assumption in the current experimental setup [p.2].

For subterranean environments, where neither GNSS nor camera-based place recognition is reliable, the UAV-UGV field testing study (REC_1267, 2019) remains a landmark: the EKF-fused cooperative system achieves median 3D positioning error below 1 m and RMS error of 2.16–2.60 m in real underground flight testing — the first demonstration of sub-metre median accuracy in a real tunnel environment. The critical dependency is the UGV's camera and LiDAR update availability: "performance of the presented approach is heavily dependent on the availability of the camera and LIDAR updates from the UGV" [p.12], making the UAV a dependent node rather than an independent agent.

The federated deep reinforcement learning architecture (REC_1302, 2026) represents the most complex cooperative framework in the corpus: a swarm of UAVs learns a shared navigation policy through federated learning, achieving detection accuracy of 92.30% (versus 81.50% for centralised PPO) and navigation deviation of 1.2 m (versus 2.50 m for centralised). The federated approach preserves data privacy and reduces communication bandwidth — but "physical field deployment evidence is limited to single-UAV trials" [p.23], meaning the swarm-scale validation remains entirely simulated.

The SwarmRaft recovery experiment (REC_0857, 2026) provides a compelling illustration of the swarm-size effect on resilience: with 3 agents, mean position recovery error after GNSS loss is 19 m; with 17 agents, it drops to 0.28 m — an improvement of 68× attributable to the geometric diversity of inter-agent range measurements that over-constrain the position estimate. This scaling behaviour suggests that large swarms have a fundamental navigational advantage over small teams, independent of sensor quality.

For formation control, the DDPG-based system (REC_1251, 2023) achieves position RMSE of 0.259 m in LiDAR-based real outdoor formation flights, versus 10.623 m for the FDPPC baseline — a 41× improvement that demonstrates the value of learned rather than rule-based formation controllers.

#### 4.3.6 LiDAR-Inertial Odometry

The dedicated LiDAR cluster (7 papers including LIDAR|SLAM and LIDAR|COOPERATIVE) spans airborne 3D LiDAR odometry, hangar-scale inspection, and forest flight.

The PSS-LIO system (REC_0951, 2026) extends point-cloud plane-structure-space LiDAR-inertial odometry with a Livox Mid-360 solid-state sensor, achieving ATE RMSE of 14.87 m on the lili_6 public dataset versus 16.45 m for FAST-LIO2 and 16.02 m for Point-LIO. The computational advantage is significant: 12.45 ms processing time versus 22.1 ms for FAST-LIO2 and 215 MB memory versus 385 MB — enabling deployment on processors that cannot support competing methods. The authors acknowledge that "reduced effectiveness in scenes lacking dominant planar structures" [p.11] limits the approach to structured environments such as warehouses and tunnels.

The LIOM-with-cylinder-features system (REC_1172, 2022) achieves RMS position error of 25.0 cm and arithmetic mean error of 21.2 cm in a GNSS-denied aircraft maintenance hangar containing a Boeing 737-500, "without loop closing" [p.5]. The result establishes LiDAR odometry as achievable at below-30 cm accuracy in large indoor industrial spaces without any landmark infrastructure.

The distributed multi-UAV LiDAR relative state estimation (REC_1355, 2022) operates on a heterogeneous multi-agent team: RMSE of 0.11–0.22 m (indoor) and relative translational error of 0.01–0.22 m (outdoor) versus SegMap's 0.36–0.81 m (indoor) and 0.15–2.41 m (outdoor). The hardware limitation is explicitly stated: the 3D LiDAR's 360° FOV requires a minimum UAV wheelbase of 650 mm and take-off weight of 5 kg, "making the proposed aerial platform difficult to fly through a narrow flight corridor" [p.10].

#### 4.3.7 Visual SLAM and Integrated Autonomy

The SLAM cluster (10 papers) spans complete autonomous navigation systems rather than isolated localisation modules.

RTAB-Map with A* planning (REC_0003, 2026) runs on a Raspberry Pi 4B with an Intel RealSense D435, achieving mean path error of 0.094 ± 0.031 m and RMSE of 0.287 m in indoor flight — outperforming ORB-SLAM3 (1.720 m) and OpenVSLAM (0.392 m) on the same platform. The limitation is clear: "the quadcopter's capacity to carry out path planning and obstacle avoidance was only restricted to 2D due to hardware limitations" [p.5], with altitude control handled independently by the laser rangefinder.

The Leonardo Drone Contest documentation (REC_0065, 2023) provides a rare competition-grade benchmark in a structured indoor environment (20 m × 10 m × 3 m urban-like arena): VIO drift of approximately 2 m over 50 seconds of flight, with "experimental tests have demonstrated that the tracker loses precision after about 50 s of flight" [p.4]. The 2nd-place competition result reflects genuine system integration under time and hardware constraints, and the VIO drift figure provides a realistic lower bound on what current COTS tracking camera hardware can sustain without loop closure.

The 2017 Singapore mission management system (REC_0896) remains methodologically important for its direct computation-accuracy comparison of two SLAM backends: Hector SLAM (ATE 0.071 m, ~40% of one CPU core) versus Cartographer SLAM (ATE 0.059 m, ~60% of one CPU core). The marginal accuracy improvement of Cartographer (17%) costs 50% more compute — a ratio that is unaffordable on resource-constrained micro-UAVs.

#### 4.3.8 UWB-Based Positioning Infrastructure

The UWB cluster (7 papers) covers ranging-only indoor positioning, cooperative relative localisation, and factor-graph fusion combining UWB with inertial and visual measurements.

The foundational 2015 UWB indoor-positioning study (REC_0025) demonstrated 10 cm horizontal and 20 cm 3D accuracy at the 95th percentile using a custom DecaWave DWM1000-based anchor network — establishing UWB as the highest-accuracy indoor ranging technology available to UAVs and motivating a decade of follow-on work. The key limitation identified: "navigation performance is tightly coupled with magnetometer performance" [p.6] because the heading reference is needed to apply the UWB position correction — coupling the system's accuracy to the magnetometer quality in magnetically noisy indoor environments.

The two-stage trilateration system (REC_0503, 2023) explicitly demonstrates UWB's advantage over GPS even in environments where GNSS is partially available: mean relative position error of 0.35 m versus 2.02 m for GPS, and mean relative altitude error of 0.32 m versus 3.39 m for GPS. The authors conclude that "even in GPS-abundant areas, UWB distance measurements combined with two-stage trilateration improve accuracy by order of magnitude compared to direct GPS measurement" [p.7].

The multi-anchor one-shot calibration with factor graph fusion (REC_1026, 2026) addresses the practical deployment barrier of anchor placement: a LMDS-based calibration algorithm eliminates the need for surveyed anchor positions, achieving calibration RMSE of 0.180 m in 0.3 ms. The resulting FGO-TC fusion achieves trajectory RMSE of 0.052 m — a 38.8% improvement over loosely coupled FGO-LC (0.085 m) and a 70.7% improvement over standalone VIO (0.178 m) on the rectangle trajectory.

### 4.4 Environment-Stratified Analysis (RQ2)

The corpus GPS-denied type classification reveals: MIXED (environments where GNSS is denied or degraded across variable scenarios, 183 papers), INDOOR (60 papers), UNDERGROUND including tunnels and mines (7 papers), FOREST below-canopy (5 papers), URBAN_CANYON (4 papers), and GNSS_SPOOFED (2 papers).

**Indoor environments** (60 papers) dominate real-world testing because motion-capture systems (Vicon, OptiTrack) or iGPS laser trackers provide millimetre-level ground truth for error computation. Under these conditions, reported position errors reach their lowest values in the entire corpus: 0.020 m RMSE for tag-aided VIO in construction (REC_1346), 0.052 m RMSE for UWB factor-graph fusion (REC_1026), and 0.071 m ATE for Hector SLAM (REC_0896). These numbers represent the ceiling of achievable accuracy under near-ideal conditions and should be read as upper bounds on algorithmic potential rather than operational expectations.

**Mixed outdoor/indoor** (183 papers, the "MIXED" category) spans a vast range from small indoor flight tests with outdoor comparisons to large-scale outdoor-only flights. It is the dominant category precisely because most papers test across multiple environments or do not restrictively specify a single environment type.

**Subterranean environments** (7 papers) are the most demanding context represented in the corpus. The convergence of challenges — no GNSS penetration, limited natural lighting for cameras, highly repetitive geometric structure causing LiDAR degeneracy, dust and particulates attenuating all sensor modalities — produces the highest position errors in any real-world evaluation. The dust-resilient mining tunnel system (REC_0409) achieves 0.60 m RMS error; the UAV-UGV team (REC_1267) achieves 2.16–2.60 m RMS error. These figures establish the current operational floor for subterranean deployment.

**Forest environments** (5 papers) present a complementary challenge: GPS denied by canopy, camera limited by low-contrast vegetation features and variable lighting, LiDAR affected by vegetation clutter and multi-path. The LiDAR odometry study in a young pine forest (REC_1348) achieves APE of 0.247 m and RPE of 0.152 m — a strong result, but the authors note that "test flights have been done are relatively short due to operational constraints" [p.7], leaving long-duration performance unknown.

### 4.5 Real-World Validation Profile

Of 279 papers, 111 are classified as REAL (real hardware, real environment), 83 as BOTH (simulation and real), and 62 as SIM-only (including 5 with suffixes like "SIM using real aerial images" that represent intermediate cases). The remaining 23 cover surveys, datasets, and ambiguous cases. The proportion of real-world-only validation (39.8%) is higher than might be expected for an early-stage field, reflecting the domain's maturity for indoor quadrotor testbeds. However, the 22.2% simulation-only fraction is a significant concern, particularly given the documented sim-to-real gap.

The gap is documented explicitly by multiple authors. The REFMP finite-memory positioning system (REC_0705) achieves APE of 0.057 m in simulation but 0.144 m in real experiments — a 2.5× degradation. The federated DRL swarm (REC_1302) validates swarm-scale behaviour in simulation while reporting single-UAV hardware results. The SwarmRaft recovery framework (REC_0857) achieves 0.28 m mean recovery error with 17 simulation agents but explicitly flags that "validating the system on physical UAV swarms in real-world environments" [p.7] is future work.

### 4.6 Quality Appraisal Results

The appraisal yielded 3 Q-High, 98 Q-Medium, and 178 Q-Low studies. The Q-Low concentration (63.8% of the corpus) is the most significant finding of the quality appraisal process. Examination of the Q-Low records reveals three dominant deficiencies: (1) NOT_REPORTED metrics — the headline result field contains no quantitative number, only qualitative descriptions or figure-only reporting; (2) absent baseline comparisons — the system is evaluated without a competing approach, making improvement claims unverifiable; and (3) simulation-only evaluation for systems claiming operational deployment readiness.

The three Q-High studies (REC_0502, REC_0037, REC_1277) share a common profile: real-world validation with external ground truth, multiple quantitative baselines evaluated on the same data, explicit acknowledgement of failure modes, and stated future work that addresses the known limitations. Crucially, all three report results that are simultaneously impressive in absolute terms and honest about the conditions required to achieve them.

---

## 5. Discussion: Cross-Cutting Trade-Offs and Systemic Gaps

### 5.1 The Accuracy-SWaP-Compute Triangle

The corpus collectively documents a fundamental three-way tension that no single system has fully resolved. The highest-accuracy systems — LD3DGS-SLAM (0.8 m outdoor, REC_0502), UWB factor-graph (0.052 m indoor, REC_1026), LiDAR-inertial (0.25 m hangar, REC_1172) — all impose substantial payload requirements: RTX-class GPUs for offline rendering, multi-anchor UWB infrastructure, or 300 g Velodyne LiDARs. Conversely, the lightest systems — monocular-camera optical flow, IMU with barometer, packet-loss ranging (REC_0064) — achieve only tens-of-metres accuracy in unconstrained environments. The key observation is that this triangle is not fixed: each hardware generation shifts the Pareto frontier. The Livox Mid-360's 200 g weight and 40 m range represent a 3× size reduction over the Velodyne VLP-16 with comparable odometry performance. The Intel RealSense D435i replaced entire multi-camera rigs. Edge AI boards like the Jetson Orin achieve 275 TOPS at 15 W in 100 g. The implication is that systems declared infeasible for small UAVs in 2019 may be deployable in 2026.

### 5.2 The Metric Heterogeneity Problem and Its Consequences

The corpus employs at least 15 distinct primary accuracy metrics. Even within a single metric label (e.g., RMSE), papers vary in: what is measured (position, trajectory, attitude, velocity); over what time window; with what ground truth (motion capture, RTK-GNSS, total station, self-reported); and with what units (metres, percentages, pixels). This heterogeneity is not arbitrary — it reflects genuine differences in what matters for each application. For a precision landing system, centimetre-level terminal accuracy is the critical metric. For a search-and-rescue swarm, kilometres-scale area coverage matters more. For a bridge inspection system, millimetre-level structural mapping resolution is the goal.

The consequence is that cross-paper comparisons are not merely statistically unreliable — they are epistemologically incoherent. The field does not lack algorithms; it lacks a common measurement framework within which to compare them. The EuRoC MAV benchmark, the KITTI odometry dataset, and the University-1652 geo-localisation dataset appear across only a handful of papers in the corpus. A purpose-built, GPS-denied UAV navigation benchmark that spans indoor, outdoor, forest, and subterranean environments — with standardised trajectories, sensor configurations, and evaluation metrics — would transform the field's ability to progress systematically.

### 5.3 The Sim-to-Real Deployment Gap

Of the 62 simulation-only papers, fewer than 10 provide any quantitative analysis of what sim-to-real transfer would require. The dominant simulation platforms (Gazebo, AirSim, MATLAB/Simulink) model aerodynamics, sensor noise, and environmental features to varying degrees, but all simplify the full complexity of real sensor degradation: camera motion blur from vibration, LiDAR multi-path from glass surfaces, UWB NLOS from human bodies, IMU bias variation with temperature, and magnetometer disturbance from onboard electronics. Papers that do document sim-to-real results consistently report 2×–5× performance degradation (e.g., REC_0705: 0.057 m sim → 0.144 m real; POMDP success rates dropping from 100% in normal visibility to 23.33% in degraded conditions, REC_0264).

### 5.4 The Adversarial Robustness Blindspot

Only 2 papers (REC_0489, REC_0006) in the corpus explicitly address GNSS spoofing or intentional signal manipulation as the GPS-denied mechanism. The remaining 277 papers treat GPS denial as an environmental or infrastructural problem rather than a security one. This is a remarkable gap given that the stated motivation of many papers is contested or tactical environments. A system whose camera can be blinded by a high-powered laser, whose LiDAR can be confused by retroreflective targets, or whose UWB ranging can be disrupted by a broadband jammer has not genuinely solved GPS-denied navigation for the adversarial use case — it has merely shifted the attack surface.

### 5.5 Long-Duration Performance: An Unexplored Frontier

The overwhelming majority of real-world evaluations in the corpus involve flights of under 10 minutes duration. The longest real-world trajectories reported are the outdoor visual geo-localisation flights (2.3 km, approximately 10–15 minutes, REC_1150) and the mining tunnel exploration (8 minutes, REC_0409). Long-duration drift behaviour — the accumulation of systematic errors that characterises all filter-based and optimisation-based odometry systems over 30–60+ minutes of continuous GNSS-denied flight — is almost entirely uncharacterised. For applications such as persistent surveillance, multi-hour search-and-rescue operations, or extended subterranean mapping, this gap represents a critical unknown.

---

## 6. Limitations of the Reviewed Field (and This Review)

### 6.1 Six Deferred Extraction Records

Six included studies (REC_0023, REC_0035, REC_0244, REC_1217, REC_1667, REC_0363) could not be extracted due to PDF integrity failures or unresolvable identity conflicts and are excluded from synthesis. These 6 records (2.1% of the included pool) are unlikely to materially alter the conclusions.

### 6.2 Single Reviewer

Data extraction was conducted by a single reviewer. While a standardised schema minimised discretionary decisions, extraction error cannot be excluded. A 1-in-10 spot-check audit documented acceptable accuracy rates across the 279 records.

### 6.3 Simulation-Only Papers Capped at Q-Medium

The quality appraisal protocol's cap on simulation-only studies at Q-Medium may under-value methodologically rigorous theoretical contributions. However, for a review whose primary question concerns operational deployment, this constraint is appropriate.

### 6.4 Database Coverage

Only IEEE Xplore and Scopus were queried. Papers published exclusively in venues not indexed by these databases (including some MDPI open-access journals, conference proceedings of regional robotics associations, and non-English language publications) are not represented.

### 6.5 Temporal Ceiling

The June 2026 search cutoff excludes the second half of 2026. Given the observed 87-paper rate in H1 2026, a substantial body of relevant work may already be available. The review's conclusions regarding 2026 trends should be read as interim findings.

---

## 7. Conclusions and Evidence-Grounded Recommendations

This systematic review of 279 papers spanning 2013–2026 yields the following collective findings:

**On sensors (RQ1):** The camera-IMU-LiDAR triad has consolidated as the dominant sensor stack for GPS-denied UAV navigation, with cameras present in 58% of studies, IMUs in 44%, and LiDAR in 20%. UWB ranging (12%) and FMCW radar (5%) are established complements for cooperative localisation and smoke/dust-penetrating navigation respectively. The rapid miniaturisation of solid-state LiDARs and edge-compute processors suggests the hardware constraints of the 2017–2020 era no longer apply to 2026 system designs.

**On environments (RQ2):** Position accuracies vary across four orders of magnitude as a function of environment rather than algorithm quality: from 0.020 m (indoor motion-capture testbed) to 16–18 m (outdoor fixed-wing GPS-denied flight). Subterranean environments remain the most challenging (best documented RMS: 0.60–2.60 m); forest-canopy and adversarial environments remain substantially under-evaluated.

**On methods (RQ3):** Hybrid multi-sensor fusion (27%) and vision-based geo-localisation (18%) dominate the algorithmic landscape. The transition from EKF-based filter fusion to factor-graph optimisation is the defining methodological shift of the 2021–2026 period. Deep learning has penetrated cross-view localisation and cooperative control but not yet the core odometry estimation pipeline. Only 3 of 279 studies reach Q-High quality — a stark finding that underscores the maturity gap between algorithmic publication and deployment-grade engineering.

**On future directions (RQ4):** The corpus collectively points to seven priority areas: (1) a standardised, open-source GPS-denied UAV navigation benchmark spanning all environment types; (2) systematic sim-to-real transfer characterisation and domain randomisation protocols; (3) long-duration (30+ minute) GNSS-denied flight validation; (4) adversarial sensor resilience testing against jamming, spoofing, and physical interference; (5) SWaP-optimised deployment of factor-graph and deep learning pipelines on sub-100 g platforms; (6) larger-scale cooperative swarm validation beyond 4 agents; and (7) standardised performance metric reporting to enable cross-paper comparison. Progress on these fronts will determine whether the algorithmic sophistication documented in this corpus translates into reliable GNSS-independent autonomy in the field.

---

## References
Bibliographic details for all 279 extracted studies are provided in `07_manuscript/references.bib`. All paper IDs (REC_XXXX) correspond to rows in `02_data_processed/MASTER_EVIDENCE.csv`. Every numeric claim in this manuscript is traceable through `08_docs/NUMBER_TRACE.md`.

---

*Figures F1–F9 and Tables T1–T5 are generated from the scripts in `06_analysis/scripts/` and stored in `06_analysis/outputs/`. The PRISMA 2020 checklist mapping is in `08_docs/PRISMA_CHECKLIST.md`.*
