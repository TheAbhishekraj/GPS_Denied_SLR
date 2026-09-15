# Autonomous Navigation and Localization for UAVs in GPS-Denied Environments: A Systematic Literature Review

**Author**: Abhishek Raj, Advanced Autonomous Systems Research Group
**Target Venue**: IEEE T-RO / IEEE Access / RAS
**Date**: September 2026
**Repository**: https://github.com/TheAbhishekraj/GPS_Denied_SLR
**Figures**: 06_analysis/output/figures_v2/ (9 figures, 300 DPI)

---

## ABSTRACT

Reliable autonomous operation of UAVs where satellite navigation is unavailable -- collapsed buildings, mines, contested EW, urban canyons, forests -- is one of robotics' most consequential unsolved challenges. This SLR synthesizes **1,692 peer-reviewed empirical studies** (2,000 initial -> 1,719 dedup -> 1,692 included), PRISMA 2020, 2010-2026, IEEE Xplore + Scopus. Three structural findings: (1) **IMU is the universal substrate** (78%, 1,332/1,700); (2) **adversarial/EW denial is the largest environment category**; (3) **a persistent simulation-to-deployment gap** unchanged over 16 years.

**Keywords**: UAV, GPS-Denied Navigation, GNSS-Denied Localization, Sensor Fusion, VIO, LiDAR SLAM, Dead Reckoning, Multi-Agent SLAM, Deep Learning Odometry, PRISMA.

---

## 1. INTRODUCTION

### 1.1 The Problem
UAVs are now expected to operate where GPS is unavailable: post-earthquake SAR, deep mines, urban canyons, active EW. In each case, the challenge is operational, not cosmetic -- unlocalizable UAVs cannot report survivor positions, maintain structural-inspection precision, or survive jamming.

### 1.2 Why This Review, Why Now
No prior survey covers the full multi-sensor, multi-platform landscape with PRISMA methodology, and none covers 2022-2026 when DL began integrating with geometric pipelines.

### 1.3 Central Argument
GPS-denied navigation has reached benchmark maturity while deployment remains unsolved. Closing the gap needs better evaluation standards, honest failure reporting, and stressed-environment validation.

### 1.4 Contributions
1. PRISMA-compliant dataset: 1,692 from 1,719 dedup (2,000 initial).
2. Multi-dimensional taxonomy: 10 methods, 13 sensors, 7 environments, 3 experiment types.
3. Three novel corpus-level findings: IMU 78%, EW dominance, quantified sim-to-deploy gap.
4. Five prioritized research directions.

---

## 2. METHODOLOGY AND PRISMA FLOW

### 2.1 Research Questions
| RQ | Question |
|---|---|
| RQ1 | Sensor modalities & fusion architectures; evolution 2010-2026? |
| RQ2 | Algorithm performance across environments? |
| RQ3 | Classical vs DL trade-offs? |
| RQ4 | Structural gaps limiting operational impact? |

### 2.2 Search Strategy
- IEEE Xplore: 1,000 records (GPS-denied OR GNSS-denied + UAV/drone + fusion/SLAM/VIO)
- Scopus: 1,000 records (equivalent TITLE-ABS-KEY)
- Timeframe: Jan 2010 - Jun 2026; English peer-reviewed only

### 2.3 PRISMA 2020 Flow (fig07_prisma_flow.png)
| Stage | Count | Notes |
|---|---|---|
| Initial | 2,000 | IEEE 1,000; Scopus 1,000 |
| After dedup | **1,719** | 281 removed (14.1%) |
| After screening | **1,692** | 27 excluded (1.6%) |
| Extracted | **1,700** | extracted_master.csv |

27 exclusions: 8 theoretical-only, 11 GPS-augmented, 8 out-of-scope platforms.

### 2.4 PICOC
Population: UAVs (fixed-wing/rotor/hybrid). Intervention: GPS/GNSS-denied methods. Comparison: baseline vs alternative. Outcome: accuracy, drift, compute, robustness. Context: indoor/outdoor/underground/adversarial/mixed.

### 2.5 Quality Checklist (8 items)
Problem statement; sensor config; quantitative results; baseline comparison; real-world/HIL validation; statistical treatment; reproducibility; limitations. Score >=5 included; 3-4 noted; <=2 excluded (8 of 27).

---

## 3. TAXONOMY OF SENSORS AND ESTIMATION FRAMEWORKS

### 3.1 IMU -- The Universal Substrate
IMU appears in **1,332/1,700 papers = 78%** (fig05). It is rarely the primary method but underlies every high-performing approach. GPS-denied navigation is fundamentally the problem of correcting IMU drift.

### 3.2 Visual-Inertial (VINS)
- **Filter-based** (MSCKF, EKF-VIO): 10-50 ms/frame, dominant on MAVs; long-horizon linearization error.
- **Optimization-based** (OKVIS, VINS-Mono, ORB-SLAM3): 0.03-0.15 m ATE on EuRoC vs 0.08-0.25 m filter; 3-10x compute. ORB-SLAM3 and VINS-Mono appear as baselines in >40% of VIO papers.

### 3.3 LiDAR SLAM & VLI Fusion
- **3D LiDAR** (LOAM, FAST-LIO2, LIO-SAM): sub-decimeter; FAST-LIO2 <0.1 m ATE real-time on embedded CPU. SWaP: VLP-16 = 830 g / 8 W.
- **Solid-state (2020+)**: Livox/Hesai; LiDAR SLAM papers +47% 2020-2023 (fig04).
- **VLI Fusion**: 38 papers; ATE <0.05 m typical; needs GPU + calibration.

### 3.4 Radio / Infrastructure-Assisted
Numerically the largest primary category.
- **UWB**: <10 cm with >=4 anchors; 14 papers on multi-UAV cooperative.
- **WiFi/5G**: 0.5-2 m; <12% address temporal fingerprint drift.
Corpus split: infra-based dominates indoor industrial; outdoor/military/SAR nearly exclude it.

### 3.5 Deep Learning & Hybrid
| Approach | Real-world | Sim |
|---|---|---|
| Hybrid Classical-Learning | 164 | 64 |
| Deep Learning Odometry | 21 | 4 |

Hybrids outperform pure DL 8:1 in real-world. End-to-end (DeepVO) fails to generalize; learned sub-modules (SuperPoint, NetVLAD) succeed.

### 3.6 Additional Modalities
- **Event cameras**: only **1 paper** as primary -- surprising given microsecond latency, <5 g, <2 W.
- **Barometers**: 23% (vertical drift aid).
- **Magnetometers**: 18% (indoor steel distortion limits).
- **Acoustic/sonar**: 9% (close-range avoidance).

---

## 4. SYNTHESIS AND ANALYSIS

### 4.1 Three Waves (fig01)
- **W1 (2010-2017)**: 17-50/yr. EKF, particle filter, VO, grid LiDAR. EuRoC released 2016.
- **W2 (2018-2022)**: 87-124/yr. ORB-SLAM3, LIO-SAM, FAST-LIO2 crystallize graph SLAM.
- **W3 (2023-2025)**: 154-336/yr. DL hybrids + new domains (agri, maritime, DARPA SubT). 2025 partial.

### 4.2 Platform & Environment
- fig02: UAVs 50.7%; General 33.6%.
- fig03: **Adversarial/EW = 495 papers (29%)** vs Indoor 339 (20%). GPS-denied is a contested-operations literature, not primarily an indoor one.

### 4.3 Simulation-to-Deployment Gap
| Method | Real | Sim | Ratio |
|---|---|---|---|
| Filter VIO | 105 | 24 | 4.4:1 |
| LiDAR SLAM | 125 | 17 | 7.4:1 |
| Multi-Agent SLAM | 14 | 11 | **1.3:1** |
| DL Odometry | 21 | 4 | 5.3:1 |
| Hybrid CL | 164 | 64 | 2.6:1 |

<8% of "real-world" papers use genuine operational environments. Multi-Agent SLAM (1.3:1) has the **lowest real-world dominance** ratio in the corpus — nearly equal real and simulation validation — signalling the field has not yet committed to field deployment for this method.

### 4.4 Application Domains (fig06)
| Domain | Papers | % |
|---|---|---|
| SAR/Disaster | 287 | 16.9% |
| Military/EW | 312 | 18.4% |
| Infrastructure | 198 | 11.6% |
| Agriculture | 143 | 8.4% |
| General/Benchmark | 760 | 44.7% |

---

## 5. OPEN CHALLENGES AND FUTURE DIRECTIONS

### 5.1 The Benchmark Illusion
EuRoC/KITTI/TUM-VI/UZH-FPV dominate. 0.05 m ATE on smooth EuRoC may fail in a 500 m dusty mine shaft. **Action**: build GDSEB (underground >200 m, EW spoofing, dynamic scenes, illumination gradients).

### 5.2 SWaP-C Tiers
- T1 (>2 kg, >50 W): full VLI + 3D LiDAR.
- T2 (0.5-2 kg, 10-50 W): VIO + solid-state LiDAR.
- T3 (<500 g, <10 W): filter VIO or UWB-IMU. **Only T3 is truly mass-deployable**, yet corpus is T1/T2-dominated.

### 5.3 Evaluation Standards Crisis
Seven metrics in use (ATE, RMSE, RPE, success rate, rate, CPU/mem, robustness). ATE RMSE reported in only 42% of quantitative papers. Need ImageNet-style canonical protocol.

### 5.4 DL vs Geometric -- False Dichotomy
Best systems combine both. Highest-leverage DL insertion points: feature extraction (SuperPoint), place recognition (NetVLAD), dynamic masking.

### 5.5 Multi-Agent -- The Underdeveloped Frontier
Only 26 papers (14 real + 11 sim + 1 both) vs 134 for Filter VIO alone. Highest-leverage open frontier in 2026. Open problems: bandwidth-efficient map sharing; relative pose without shared map; fusion under comms dropout.

---

## 6. RESEARCH MATURITY (fig09)

| Dimension | Score |
|---|---|
| Lab Benchmark | 9/10 |
| Real-World Deploy | 4/10 |
| Multi-Sensor Fusion | 7/10 |
| Edge Compute | 5/10 |
| Adversarial Robustness | 6/10 |
| Long-Horizon Drift | 5/10 |
| Multi-Agent | 3/10 |
| Standardised Eval | 3/10 |

---

## 7. CONCLUSION

Three corpus-level findings unique to this review:
1. **IMU universal**: 78% use IMU as fusion input. GPS-denied navigation = correcting IMU drift.
2. **Adversarial dominates**: largest environment (495, 29%). Not primarily indoor.
3. **Deployment gap is structural**: sim-to-deploy ratio hasn't improved; Multi-Agent SLAM worst.

Closing requires culture shift: stressed-env evaluation, honest drift reporting, community-enforced protocols, field deployment as publication standard.

---

## REFERENCES (key)

- [Campos2021] ORB-SLAM3, IEEE T-RO 2021
- [Qin2018] VINS-Mono, IEEE T-RO 2018
- [Zhang2014] LOAM, RSS 2014
- [Xu2022] FAST-LIO2, IEEE T-RO 2022
- [Shan2020] LIO-SAM, IROS 2020
- [Burri2016] EuRoC, IJRR 2016
- [Geiger2012] KITTI, CVPR 2012
- [DeTone2018] SuperPoint, CVPRW 2018
- [Arandjelovic2016] NetVLAD, CVPR 2016
- [Wang2017] DeepVO, ICRA 2017
- [Prisma2020] PRISMA 2020, BMJ 2021

**Dataset**: 02_data_processed/extracted_master.csv (1,700)
**Figures**: 06_analysis/output/figures_v2/ (9, 300 DPI)
**GitHub**: https://github.com/TheAbhishekraj/GPS_Denied_SLR

---
CANONICAL NUMBERS: Raw=2,000 | Dedup=1,719 | Included=1,692 | Excluded=27 | Extracted=1,700
Next: (1) inline citations; (2) LaTeX; (3) performance tables; (4) plagiarism check
