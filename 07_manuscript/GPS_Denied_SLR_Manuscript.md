# Autonomous Navigation and Localization for Unmanned Aerial Vehicles in GPS-Denied Environments: A Systematic Literature Review

**Author**: Advanced Autonomous Systems Research Group  
**Target Venue**: IEEE Transactions on Robotics / IEEE Access / Robotics and Autonomous Systems  
**Date**: September 2026  
**Repository**: [https://github.com/TheAbhishekraj/GPS_Denied_SLR](https://github.com/TheAbhishekraj/GPS_Denied_SLR)

---

## ABSTRACT

Unmanned Aerial Vehicles (UAVs) operating in complex, GPS-denied environments—such as indoor building structures, urban canyons, underground mining tunnels, forest canopies, and electronic warfare jamming zones—face critical state estimation and drift challenges. This Systematic Literature Review (SLR) provides a quantitative and qualitative synthesis of 1,692 included empirical studies selected from an initial pool of 2,000 raw records (1,000 IEEE Xplore, 1,000 Scopus) and 1,719 unique deduplicated papers following PRISMA 2020 guidelines. We present a multi-dimensional taxonomy covering platform types, sensor modalities, state estimation algorithms, operational environments, and evaluation metrics. Our findings reveal that while Visual-Inertial Odometry (VIO) and LiDAR SLAM remain foundational, hybrid deep learning-assisted dead-reckoning and multi-agent collaborative SLAM are rapidly growing solution paradigms. We highlight open challenges regarding Size, Weight, Power, and Cost (SWaP-C) constraints, sensor degradation under severe weather/lighting, and real-time edge processing, offering a strategic roadmap for future research.

**Keywords**: Unmanned Aerial Vehicles (UAVs), GPS-Denied Navigation, Sensor Fusion, Visual-Inertial Odometry (VIO), LiDAR SLAM, Swarm Robotics, Deep Learning Odometry.

---

## 1. INTRODUCTION

Unmanned Aerial Vehicles (UAVs) have transitioned from open-sky outdoor applications to complex, cluttered, and GNSS-denied environments. In scenarios such as search and rescue (SAR) inside collapsed structures, structural health inspection of penstocks and bridges, underground mining exploration, and military operations under active electronic jamming, reliance on Global Positioning System (GPS) signals is impossible due to signal attenuation, multi-path reflections, or active adversarial spoofing.

Achieving drift-free autonomous navigation without external position updates requires robust onboard multi-sensor fusion and real-time state estimation algorithms. Over the past decade, significant advancements have been made in Visual-Inertial Navigation Systems (VINS), 3D LiDAR SLAM, Ultra-Wideband (UWB) radio positioning, and deep neural network-aided odometry. However, researchers and practitioners face fragmented literature across robotics, control, computer vision, and aerospace engineering.

This systematic literature review addresses this gap by synthesizing 1,692 peer-reviewed empirical studies. The main contributions of this review are:
1. **PRISMA-Compliant Quantitative Dataset**: Analysis of 1,692 screened and extracted papers out of 1,719 deduplicated publications.
2. **Comprehensive Taxonomy**: Classification of hardware platforms, sensor suites, estimation architectures, and operational domains.
3. **Comparative Analysis of Core Frameworks**: Evaluation of filter-based VIO, optimization-based VIO, LiDAR-visual-inertial fusion, and radio-assisted localization.
4. **Open Challenges & Future Roadmap**: Identification of key bottlenecks in SWaP-C, resilience against sensor failure, and edge AI execution.

---

## 2. METHODOLOGY & PRISMA FLOW

This review was conducted in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) statement.

### 2.1 Research Questions
- **RQ1**: What are the primary sensor modalities and fusion architectures used for UAV navigation in GPS-denied environments?
- **RQ2**: How do state estimation algorithms perform across different operational scenarios (indoor, underground, urban canyon, adversarial)?
- **RQ3**: What are the main trade-offs between classical estimation techniques (EKF, Factor Graphs) and deep learning-based approaches?
- **RQ4**: What key open challenges hinder long-duration, fully autonomous GPS-denied flight?

### 2.2 Search Strategy and Data Sources
Searches were conducted across IEEE Xplore and Scopus databases for articles published between 2010 and 2026 using the core search query:
> `("GPS-denied" OR "GNSS-denied" OR "indoor navigation") AND ("UAV" OR "quadrotor" OR "drone") AND ("sensor fusion" OR "VIO" OR "SLAM")`

- **IEEE Xplore**: 1,000 records retrieved.
- **Scopus**: 1,000 records retrieved.
- **Total Initial Records**: 2,000 records.

### 2.3 PRISMA 2020 Flow Metrics
1. **Identification**: 2,000 raw records exported.
2. **Deduplication**: Individual per-source field standardization was performed (`01_deduplicate.py`), identifying 281 cross-database duplicate records (14.1% duplication rate), resulting in 1,719 unique papers (999 IEEE Xplore, 720 Scopus).
3. **Screening**: 1,719 papers evaluated against pre-defined inclusion/exclusion criteria.
   - **Included**: 1,692 empirical studies (98.4%).
   - **Excluded**: 27 non-empirical, orbital, or out-of-scope papers (1.6%).
4. **Data Extraction**: 1,700 paper responses processed into a structured JSON database and compiled into `extracted_master.csv`.

---

## 3. TAXONOMY OF SENSOR MODALITIES AND FUSION FRAMEWORKS

The primary sensor modalities and fusion frameworks identified across the 657 included studies are categorized below:

### 3.1 Visual-Inertial Navigation Systems (VINS)
Visual-Inertial Odometry (VIO) pairs high-frequency IMU acceleration/angular rate measurements with visual tracking from monocular, stereo, or event cameras.
- **Filter-Based VIO** (e.g., MSCKF, EKF-VIO): Computationally efficient, suitable for ultra-constrained micro aerial vehicles (MAVs).
- **Optimization-Based VIO** (e.g., OKVIS, VINS-Mono, ORB-SLAM3): Employs non-linear factor graph optimization over sliding keyframe windows, offering high accuracy at the cost of higher CPU/GPU overhead.

### 3.2 LiDAR SLAM and Visual-LiDAR-Inertial (VLI) Fusion
LiDAR sensors provide direct 3D range geometry independent of ambient illumination.
- **3D LiDAR SLAM** (e.g., LOAM, FAST-LIO, LIO-SAM): Delivers sub-centimeter mapping accuracy in complex structures but suffers under SWaP constraints on small UAVs.
- **Visual-LiDAR-Inertial Fusion**: Combines visual texture from RGB cameras, range point clouds from LiDAR, and high-rate IMU states for resilient performance in featureless or dynamic scenes.

### 3.3 Radio-Based & Infrastructure-Assisted Positioning
When onboard visual/LiDAR perception is degraded (e.g., heavy smoke or dark caverns), radio signals provide absolute local positioning:
- **Ultra-Wideband (UWB)**: Time-of-Flight (ToF) distance measurement offering 5–10 cm ranging precision when ground anchors are deployed.
- **WiFi / 5G Signals-of-Opportunity**: RSSI and Angle-of-Arrival (AoA) estimation for indoor warehouse navigation.

---

## 4. EXPERIMENTAL PERFORMANCE & ANALYSIS

### 4.1 Temporal Trends & Platform Distribution
Publication metrics demonstrate exponential growth from 2010 to 2025, driven by the miniaturization of sensors and solid-state LiDARs.
- **UAV Platform Share**: Multi-rotor quadrotors account for over 66% of target platforms due to hover capabilities, followed by fixed-wing and hybrid VTOL platforms.
- **Environment Breakdown**: Indoor warehouse/building navigation represents the largest single operational scenario, followed by subterranean tunnels and urban canyons.

### 4.2 Error Metrics and Benchmark Datasets
- **Primary Metric**: Absolute Trajectory Error Root Mean Square Error (ATE RMSE) is reported in 42% of quantitative papers.
- **Benchmark Datasets**: The EuRoC MAV, KITTI, TUM VI, and UZH-FPV datasets serve as standard benchmarks for evaluating VIO and SLAM resilience.

---

## 5. OPEN CHALLENGES AND FUTURE DIRECTIONS

1. **SWaP-C Bottlenecks**: High-end 3D LiDARs and GPU edge accelerators exceed the payload and battery capacity of sub-250g nano-drones.
2. **Perceptual Degradation**: Rapid motion blur, reflective glass walls, dynamic obstacles, and complete darkness degrade classical visual-inertial pipelines.
3. **Semantic SLAM & Digital Twins**: Transitioning from geometric point clouds to semantic graph maps (e.g., integrating BIM models for indoor localization).
4. **Multi-Agent Collaborative Resilience**: Decentralized swarm state estimation with intermittent, bandwidth-limited communication links.

---

## 6. CONCLUSION

This systematic literature review has analyzed 657 peer-reviewed empirical studies in GPS-denied UAV navigation. By establishing a quantitative taxonomy of sensors, algorithms, and operational scenarios, this study provides a foundation for researchers designing robust autonomous aerial platforms for GPS-denied environments.

---

## REFERENCES & REPOSITORY ACCESS
- **Master Dataset**: `02_data_processed/extracted_master.csv`
- **Publication Figures**: `06_analysis/output/figures/`
- **GitHub Repository**: [https://github.com/TheAbhishekraj/GPS_Denied_SLR](https://github.com/TheAbhishekraj/GPS_Denied_SLR)
