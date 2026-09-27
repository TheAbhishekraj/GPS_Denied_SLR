# GPS-Denied UAV Navigation: A Systematic Literature Review of Multi-Sensor Fusion, Vision-Based Localisation, and Cooperative Autonomy (2013–2026)

**Target Publication:** *IEEE Transactions on Robotics* / *IEEE Access*  
**Corpus Evidence Base:** `02_data_processed/MASTER_EVIDENCE.csv` ($n = 279$ peer-reviewed studies)  
**Quality Framework:** Plan-Do-Check-Act (PDCA) Multi-Tier Quality Screening (`06_analysis/outputs/quality_appraisal_scored.csv`)  
**Data Analytics Reference:** `06_analysis/outputs/RQ_DATA_ANALYTICS.json`  

---

## Abstract

The deployment of Unmanned Aerial Vehicles (UAVs) in Global Navigation Satellite System (GNSS)-denied environments represents one of the most formidable frontiers in modern robotics. Whether navigating subterranean mines, inspecting collapsed infrastructure, or operating within contested airspace, aerial platforms must execute high-frequency control and complex path planning in the complete absence of global positioning updates. This Systematic Literature Review (SLR) provides a comprehensive synthesis of 279 gold-standard, peer-reviewed empirical studies published between 2013 and 2026. Executed through a rigorous PRISMA 2020 protocol across IEEE Xplore and Scopus, this review investigates four fundamental dimensions of GPS-denied flight: (**RQ1**) the historical evolution of sensor modalities and fusion architectures; (**RQ2**) the empirical performance envelopes across extreme operational environments, including dense forest canopies and urban canyons; (**RQ3**) the validation fidelity of leading algorithmic paradigms, contrasting the maturity of LiDAR-inertial systems against the simulation dependency of cooperative swarms; and (**RQ4**) the systemic vulnerabilities imposed by Size, Weight, Power, and Cost (SWaP-C) constraints. Our chronological analysis exposes a paradigm shift from legacy ultrasonic odometry (2013–2016) to the contemporary dominance of lightweight solid-state LiDAR and Ultra-Wideband (UWB) networks (2022–2026). More critically, our quality appraisal reveals a profound reproducibility crisis: fewer than 2% of investigations provide open-source code and verifiable flight datasets. By aggressively avoiding artificial statistical pooling and relying exclusively on verbatim empirical metrics, this review dismantles the theoretical "Sim-to-Real" disconnect and defines a concrete, hardware-grounded roadmap toward certifiably autonomous, closed-loop aerial robotics.

**Index Terms**—UAV navigation, GNSS-denied localization, multi-sensor fusion, visual-inertial odometry, LiDAR SLAM, cooperative swarms, PRISMA systematic literature review.

---

## 1. Introduction

Over the past decade, Unmanned Aerial Vehicles (UAVs) have rapidly evolved from manually piloted platforms confined to open skies into highly autonomous agents tasked with penetrating the most challenging, inaccessible environments on Earth. Operational theaters such as subterranean cave networks, structurally compromised industrial facilities, dense urban canyons, and heavily foliated forests all share a critical, defining vulnerability: the absolute denial, severe degradation, or malicious spoofing of Global Navigation Satellite System (GNSS) signals. Stripped of global positioning tethers, a micro-aerial vehicle must rely entirely on its onboard suite of exteroceptive and proprioceptive sensors to estimate its six-degree-of-freedom (6-DoF) kinematic state, map unknown obstacles in real time, and execute aggressive, collision-free maneuvers.

The engineering reality of achieving sustained autonomous flight in these regimes is governed by brutal physical constraints. Micro- and small-UAVs are bound by unforgiving Size, Weight, Power, and Cost (SWaP-C) budgets. Every gram allocated to advanced compute modules (e.g., NVIDIA Jetson architectures) or active perception sensors (e.g., mechanical LiDAR) directly penalizes flight endurance, which typically hovers between 12 and 28 minutes. Simultaneously, the state estimation algorithms running on these processors face unrelenting environmental hostilities: dynamic illumination shifts that blind optical cameras, featureless corridors that induce geometric degeneracy in LiDAR scans, and rotor-induced downwash that violently agitates surrounding foliage.

While the academic literature addressing GPS-denied aerial navigation has exploded in volume, the secondary literature attempting to organize it remains fragmented. Existing survey articles are predominantly qualitative, heavily biased toward specific sensor silos (such as pure monocular vision), and critically lack transparent, reproducible data provenance. To resolve these ambiguities and establish a definitive baseline for the community, this systematic review conducts an exhaustive, data-grounded synthesis of 279 manually extracted, peer-reviewed publications spanning from the foundational efforts of 2013 through the swarm and neural paradigms of mid-2026.

### Research Questions
This review targets four primary research questions designed to dissect the architectural, environmental, algorithmic, and operational realities of GPS-denied flight:
* **RQ1 (Sensor Modalities & Fusion Trends):** Which sensor configurations dominate GPS-denied UAV navigation, and how have multi-sensor fusion paradigms shifted chronologically over the past decade?
* **RQ2 (Localization Accuracy & Operational Environments):** What are the true quantitative localization accuracy limits, drift rates, and robustness metrics achieved across distinct degradation regimes, including indoor warehouses, subterranean tunnels, and contested airspace?
* **RQ3 (Algorithmic Paradigms & Validation Fidelity):** Which algorithmic frameworks lead the state of the art, and how does the maturity of their physical flight validation compare against purely numerical simulation?
* **RQ4 (Systemic Limitations & Future Agenda):** What are the fundamental SWaP-C bottlenecks and perception vulnerabilities documented across the literature, and what open research priorities must be addressed to unlock certifiable real-world deployment?

---

## 2. Related Work & Systematic Positioning

Prior secondary literature has illuminated individual facets of UAV state estimation. However, a rigorous audit of the existing review articles identified within our screened corpus highlights severe methodological gaps:

Unlike preceding qualitative surveys, the present study asserts its authority through four methodological pillars:
1. It adheres strictly to the **PRISMA 2020** methodology, enforcing reproducible inclusion boundaries across IEEE Xplore and Scopus databases.
2. It evaluates every publication against an objective **Plan-Do-Check-Act (PDCA) Quality Appraisal** model, exposing the underlying rigor, baseline comparisons, and reproducibility of the field.
3. It completely forbids the artificial statistical pooling of heterogeneous metrics, reporting instead verifiable numerical performance ranges exactly as they appear in the primary literature.
4. It synthesizes cross-cutting physical trade-offs across a massive, manually verified 279-paper gold-standard evidence base.

---

## 3. Systematic Review Methodology

### 3.1 Literature Search Strategy & Information Sources
The literature search was executed on June 15, 2026, targeting the two premier indexing databases for robotics and aerospace engineering: **IEEE Xplore** and **Scopus**. The automated search retrieved exactly 2,000 raw candidate records, ensuring an exhaustively broad initial net.

### 3.2 Screening Protocol & Eligibility Criteria
Following automated cross-database deduplication, candidate records were screened against strict operational criteria (detailed in **[Insert Table I: Inclusion/exclusion criteria]**).

**Table I: Inclusion and Exclusion Criteria**
| Dimension | Inclusion Criteria | Exclusion Criteria |
|---|---|---|
| **Date** | Published 2010-01-01 to 2026-06-15 | Pre-2010 publications |
| **Language** | English | Non-English |
| **Document Type** | Peer-reviewed journal or full conference | Preprints, patents, theses, tutorials |
| **Topic** | GNSS-denied/degraded aerial navigation | GNSS-dependent systems |
| **Platform** | Unmanned Aerial Vehicles (UAVs) | Terrestrial (UGV) or underwater platforms |
| **Method** | Multi-sensor fusion (≥2 modalities) | Unassisted single-sensor odometry |
| **Validation** | Physical flight or high-fidelity simulation | Purely conceptual without empirical data |

Through multi-stage title, abstract, and full-text screening, exactly **279 studies** met all eligibility thresholds. 

The complete flow of information through the different phases of a systematic review is depicted in the PRISMA 2020 flow diagram (**[Insert Fig. 1: PRISMA flow diagram]**).

### 3.3 Data Extraction & PDCA Quality Appraisal
Data extraction captured operational environments, platform dynamics, sensor configurations, and verifiable performance outcomes. The full evidence matrix for all included studies is provided in **[Insert Table II: Evidence matrix (all 279 papers)]**.

Quality screening evaluated each study across Methodological Rigor, Reporting Quality, Baseline Comparative Rigor, and Reproducibility. Stratification yielded **3 Q-High studies (1.1%)**, **98 Q-Medium studies (35.1%)**, and **178 Q-Low studies (63.8%)**, establishing an average corpus composite quality score of 3.81 out of 8.0.

---

## 4. Systematic Results & Empirical Evidence Synthesis

### 4.1 Chronological & Geographic Trajectory
The temporal trajectory of the corpus illustrates a steady expansion that accelerated exponentially after 2021 (**[Insert Fig. 2: Publications per year]**). Geographically, research output is heavily concentrated across major robotics ecosystems in China, the United States, and Singapore.

### 4.2 RQ1 Synthesis: Sensor Modalities & Fusion Architectural Shifts
To answer **RQ1**, we analyzed the operational prevalence of primary sensor modalities (**[Insert Fig. 3: Sensor distribution]**) and fusion configurations across three historical epochs. 

**[Insert Table III: Method comparison summary (Evolution of Fusion Architectures)]**
**Table III: Method Comparison Summary**
| Multi-Sensor Pairing | 2013–2016 (%) | 2017–2021 (%) | 2022–2026 (%) | Overall Frequency |
|---|---|---|---|---|
| Camera + IMU | 34.6% | 27.8% | 23.0% | 25.4% |
| Camera + LiDAR | 15.4% | 16.5% | 17.2% | 16.8% |
| LiDAR + IMU | 15.4% | 8.9% | 17.2% | 14.7% |
| Camera + LiDAR + IMU | 7.7% | 5.1% | 10.3% | 8.6% |
| UWB + IMU | 0.0% | 7.6% | 10.9% | 9.0% |

**Key Findings for RQ1:**
1. **The Obsolescence of Ultrasonic Sensing vs. Rise of UWB:** In the foundational era (2013–2016), downward-facing sonars were prevalent (30.8%) for altitude hold. By 2022–2026, ultrasonic sensors almost vanished (0.6%), aggressively displaced by lightweight Time-of-Flight (ToF) LiDAR and Ultra-Wideband (UWB) networks.
2. **Solidification of Visual-Inertial & LiDAR-Inertial Couplings:** Camera + IMU remains the standard baseline pairing. However, LiDAR + IMU and triple-sensor arrays (Camera + LiDAR + IMU) grew five-fold in raw frequency after 2021, unlocked by the miniaturization of solid-state LiDAR scanners operating within strict micro-UAV payload allowances.

### 4.3 RQ2 Synthesis: Environmental Degradation Regimes & Metric Envelopes
To address **RQ2**, the corpus was categorized into operational environments (**[Insert Fig. 5: Environment distribution]**), extracting verifiable trajectory error metrics.

**[Insert Table IV: Key results summary by environment]**
**Table IV: Key Results Summary by Environmental Degradation Regime**
| Environment Category | Primary Degradation Stressor | Reported Accuracy Envelopes | Key Example Reference |
|---|---|---|---|
| Mixed / Outdoor Denied | GNSS dropouts, altitude variance | Horizontal RMSE: 0.10 m – 1.84 m | [REC_0037] |
| Indoor & Warehouses | Geometric symmetry, multipath | Mean path error: 0.039 m – 0.15 m | [REC_0028] |
| Urban Canyons | Multipath, structural shadow | Mean position error: 0.80 m – 2.0 m | [REC_0312] |
| Dense Forest Canopy | Dynamic foliage, non-rigid slip | Obstacle tracking FPS: 30–40 Hz | [REC_1253] |
| Subterranean/Tunnels | Zero illumination, airborne dust | 3D error: 0.05 m – 2.6 m | [REC_1267] |

Subterranean environments represent the most hostile operational regime, characterized by total darkness, suspended dust, and featureless cylindrical cross-sections that induce catastrophic geometric degeneracy.

### 4.4 RQ3 Synthesis: Algorithmic Paradigms & Validation Fidelity
To answer **RQ3**, we cross-tabulated algorithmic families (**[Insert Fig. 4: Method category distribution]**) against empirical validation fidelity (**[Insert Fig. 7: Real vs Sim breakdown]**). 

**Critical Algorithmic Insights:**
1. **The Swarm Sim-to-Real Disconnect:** While cooperative swarm navigation represents 17.6% of the literature, it suffers from the lowest physical flight-testing rate in the entire corpus: **49.0% of swarm studies rely entirely on numerical simulations**. Physical swarm validation remains stalled by inter-agent RF packet loss and aerodynamic downwash collisions.
2. **LiDAR SLAM Hardware Grounding:** Conversely, LiDAR-inertial SLAM exhibits the highest hardware validation fidelity: **85.7% of LiDAR studies execute physical flight tests**, driven by mature, robust open-source stacks.

### 4.5 The Three Q-High Benchmark Anchor Studies
Only 3 of the 279 studies (1.1%) met all criteria for **Q-High** classification, representing the absolute pinnacle of benchmarking, rigor, and reproducibility in the field:
1. **REC_0037 (2026):** Extracted deep learned descriptors (SuperPoint/LightGlue) between onboard monocular video and georeferenced satellite orthoimagery, achieving a mean horizontal error of 1.84 m across multi-kilometer flights.
2. **REC_0502 (2026):** Deployed 3D Gaussian Splatting combined with a 200 Hz IMU to achieve an unprecedented 0.80 m mean error at high altitudes, vastly outperforming ORB-SLAM3 baselines.
3. **REC_1277 (2026):** Utilized physics-guided neural networks (PG-TLNet) to compensate for aggressive aerodynamic and electromagnetic interference across a fixed-wing swarm, reducing magnetic interference standard deviation by 85.2%.

---

## 5. Discussion & Cross-Cutting Tensions

### 5.1 The Accuracy–SWaP–Compute Trilemma
The synthesis reveals that GPS-denied aerial navigation is governed by an inescapable physical trilemma. High-accuracy systems employing multi-beam LiDAR arrays achieve sub-decimeter accuracy but demand massive power (20–65 W) and decimate flight endurance. Conversely, ultra-lightweight nano-MAVs equipped with mere monocular cameras accumulate unbounded dead-reckoning drift, causing catastrophic localization divergence on extended flights. The intermediate solution—deep neural matching and radiance field rendering—eliminates drift but introduces severe compute latency bottlenecks, restricting closed-loop flight speeds.

### 5.2 Metric Heterogeneity & Non-Standardized Evaluation
A severe systemic weakness identified in the corpus is the extreme divergence in performance metric reporting. Over **90% of the corpus evaluates algorithms exclusively on private, self-collected flight sequences**, severely undermining comparative analysis. Furthermore, researchers arbitrarily alternate between reporting Absolute Trajectory Error (ATE), Relative Pose Error (RPE), or percentage drift, rendering direct algorithmic comparisons impossible without standardized benchmarks.

### 5.3 The Sim-to-Real Disconnect & Offline Trap
Over **51% of all studies in the corpus never execute closed-loop autonomous flight**. A widespread paradigm involves recording sensor rosbags during manual radio-controlled flight, executing SLAM estimation offline on desktop workstations, and reporting post-processed accuracy. This offline methodology dangerously ignores real-world compute latency, rotor vibration harmonics, and aerodynamic ground-effect disturbances.

---

## 6. RQ4 Synthesis: Technological Limitations & Future Research Agenda

To address **RQ4**, we systematically extracted and categorized the failure modes, technological limitations, and proposed future directions across all 279 studies. 

The top documented limitations revolve around visual degradation in extreme lighting, edge GPU thermal throttling, cumulative dead-reckoning drift in feature-sparse environments, and RF packet loss in multi-agent swarms.

### Strategic Future Research Directions:
1. **Neuromorphic & Bio-Inspired Event Sensing:** Integrating event-based neuromorphic cameras operating at microsecond temporal resolution offers a viable path toward blur-free state estimation under high-speed aggressive flight, defeating the limitations of standard CMOS sensors.
2. **Decentralized, Communication-Resilient Swarm SLAM:** Future swarm algorithms must implement communication-censored factor graphs, maintaining formation stability during extended RF dropouts by transmitting only high-information marginal keyframes.
3. **Physics-Informed Neural Network (PINN) Sensor Compensation:** Physics-guided neural models must be leveraged to predict and compensate for complex non-linear motor interference, thermal IMU bias drifts, and aerodynamic rotor downwash dynamics in real time.
4. **Community Standardization & Open-Source Verification:** The robotics community must urgently establish standardized aerial navigation benchmarks providing synchronous hardware data coupled with sub-millimeter motion-capture ground truth in hostile subterranean and canopy environments.

---

## 7. Conclusions

This systematic literature review provides the most comprehensive, data-grounded synthesis of GPS-denied UAV navigation conducted to date, analyzing 279 gold-standard peer-reviewed studies published between 2013 and mid-2026. By examining the corpus across four foundational research questions, we have mapped the operational obsolescence of legacy sensors, defined precise localization performance envelopes across hostile environments, exposed a profound simulation dependency in cooperative swarm literature, and articulated the systemic vulnerabilities imposed by strict SWaP-C budgets. 

By adhering strictly to transparent data extraction, avoiding artificial metric pooling, and grounding all findings in verifiable evidence, this review provides a definitive reference architecture for the next generation of resilient, certifiably autonomous aerial robotics.

---

## References

*(Full IEEE bibliographic citations mapped to all 279 in-corpus records; primary anchors and representative studies referenced directly via `07_manuscript/references.bib`).*
