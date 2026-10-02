# MASTER_EVIDENCE Audit Report

Generated (UTC): 2026-10-02T04:33:54Z
Scope: E:\GPS_Denied_SLR pipeline audit through 02_data_processed

## VERDICT: **FAIL**

### Blockers
- BLOCKER: 47 master rows carry wrong/empty titles (mangled extraction, e.g. "G","P","drones").

### Majors
- MAJOR: authors missing (NOT_REPORTED) in 279/279 rows.
- MAJOR: venue missing (NOT_REPORTED) in 279/279 rows.
- MAJOR: 3 placeholder/unassigned DOIs (REC_0064, REC_0391, REC_1637).
- MAJOR: 105 master titles differ from screening titles (incl. PDF-junk affixes).

### Minors
- MINOR: 28 evidence_batches CSVs are near-empty shells (0-3 filled cells each); they carry no extraction data.
- MINOR: screening_results.csv venue column is empty for all 279 rows; venue only recoverable from REC_*.md.
- MINOR: 6 INCLUDE records deferred from master: REC_0023, REC_0035, REC_0244, REC_0363, REC_1217, REC_1667.
- MINOR: BATCHED split is empty (0 rows); all 279 rows are MANUAL-origin.

## Phase 1 - Inventory
| metric | value |
|---|---|
| master_rows | 279 |
| master_cols | 28 |
| screening_rows | 291 |
| included_rows | 636 |
| dedup_rows | 1716 |
| batch_files | 28 |
| batch_total_rows | 279 |
| batch_unique_ids | 279 |
| manual_rec_files_count | 279 |
| primary_key | id |
| files_in_02_data_processed | 318 |

## Phase 2 - Structural
| check | value |
|---|---|
| duplicate master keys | 0 |
| empty master keys | 0 |
| header == EXTRACTION_SCHEMA_v1 | True |
| master not in included_v2 | 0 |
| included_v2 not in master | 357 |
| master not in screening | 0 |

## Phase 3 - Title integrity
- bad_count: **47**
- fixed (from screening_results.csv): **47**
- needs_human: **0**
- cross-check title diffs vs screening: **105**

| pid | reason | master_title | fixed_by | fixed_value |
|---|---|---|---|---|
| REC_0041 | short | G | screening_results.csv | UAV Navigation With Monocular Visual Inertial Odometry Under GNSS-Deni |
| REC_0095 | short | P | screening_results.csv | Cooperative Relative Localization for UAV Swarm in GNSS-Denied Environ |
| REC_0138 | short | A | screening_results.csv | Autonomous Exploration and Mapping System Using Heterogeneous UAVs and |
| REC_0211 | short | M | screening_results.csv | SIA-KalmanNet: A Structurally Integrated Attention Kalman Filter for M |
| REC_0343 | short | T | screening_results.csv | Vision-Aided Multi-UAV Autonomous Flocking in GPS-Denied Environment |
| REC_0347 | short | I | screening_results.csv | A Novel Three-Stage Robust Adaptive Filtering Algorithm for Visual-Ine |
| REC_0362 | short | A | screening_results.csv | Unmanned aerial vehicle relative navigation in GPS denied environments |
| REC_0369 | short | A | screening_results.csv | Autonomous Flight Control of a Nano Quadrotor Helicopter in a GPS-Deni |
| REC_0388 | short | I | screening_results.csv | Multi-UAV Cooperative Navigation Based on Multisource Information Fusi |
| REC_0391 | short | I | screening_results.csv | Multi-UAV Collaboration and IMU Fusion Localization Method in Partial  |
| REC_0489 | short | A | screening_results.csv | UAV Vision Aided INS/Odometer Integration for Land Vehicle Autonomous  |
| REC_0502 | short | W | screening_results.csv | LD3DGS-SLAM: Long-Distance Monocular SLAM With 3-D Gaussian Splatting  |
| REC_0503 | short | D | screening_results.csv | Decimeter-Accuracy Positioning for Drones Using Two-Stage Trilateratio |
| REC_0544 | short | K | screening_results.csv | Season-Invariant GNSS-Denied Visual Localization for UAVs |
| REC_0622 | short | T | screening_results.csv | Micro-Drone Ego-Velocity and Height Estimation in GPS-Denied Environme |
| REC_0631 | short | INVITED SPEAKER 1 | screening_results.csv | Invited Speaker 1: Navigation without GPS for Unmanned Aerial Vehicles |
| REC_0705 | short | U | screening_results.csv | Recursive Extended Finite-Memory Positioning Algorithm for Robust UAV  |
| REC_0713 | short | A | screening_results.csv | Autonomous UAV Pipeline Landing via Depth-LiDAR Fusion in GNSS-Denied  |
| REC_0719 | short | W | screening_results.csv | Autonomous landing of small unmanned aerial rotorcraft based on monocu |
| REC_0814 | short | S | screening_results.csv | Monocular Vision Aided Autonomous UAV Navigation in Indoor Corridor En |
| REC_0824 | short | F | screening_results.csv | A Homography-Based Visual Servo Control Approach for an Underactuated  |
| REC_0857 | short | R | screening_results.csv | SwarmRaft: Leveraging Consensus for Robust Drone Swarm Coordination in |
| REC_0951 | short | B | screening_results.csv | PSS-LIO A Computationally Efficient LiDAR-Inertial Odometry Framework  |
| REC_1019 | short | I | screening_results.csv | Multi-Sensor Fusion SLAM for Interceptor UAVs in GNSS-Denied Environme |
| REC_1032 | short | drones | screening_results.csv | Synchronized Multi-Directional FMCW mmWave Radar?Inertial Odometry: Ro |
| REC_1048 | short | sensors | screening_results.csv | Airspeed-Aided State Estimation Algorithm of Small Fixed-Wing UAVs in  |
| REC_1085 | short | aerospace | screening_results.csv | GNSS-Denied Semi-Direct Visual Navigation for Autonomous UAVs Aided by |
| REC_1095 | short | sensors | screening_results.csv | A multi-sensorial simultaneous localization and mapping (SLAM) system  |
| REC_1123 | short | I | screening_results.csv | A Novel Scene-Matching Positioning Approach for Low-Altitude UAVs Cons |
| REC_1135 | short | drones | screening_results.csv | UAV Localization in Low-Altitude GNSS-Denied Environments Based on POI |
| REC_1165 | short | U | screening_results.csv | UAV Localization in GPS-Denied Environments: A Review |
| REC_1186 | short | ScienceDirect | screening_results.csv | Landmarks based path planning for UAVs in GPS-denied areas |
| REC_1194 | short | drones | screening_results.csv | A Unmanned Aerial Vehicle (UAV)/Unmanned Ground Vehicle (UGV) Dynamic  |
| REC_1196 | short | sensors | screening_results.csv | Precision Landing of a Quadcopter Drone by Smartphone Video Guidance S |
| REC_1232 | short | drones | screening_results.csv | Range?Visual?Inertial Odometry with Coarse-to-Fine Image Registration  |
| REC_1250 | short | aerospace | screening_results.csv | Long-Distance GNSS-Denied Visual Inertial Navigation for Autonomous Fi |
| REC_1283 | short | sensors | screening_results.csv | Cooperative monocular-based SLAM for multi-UAV systems in GPS-denied e |
| REC_1286 | short | remote sensing | screening_results.csv | Hybrid camera array-based UAV auto-landing on moving UGV in GPS-denied |
| REC_1289 | short | aerospace | screening_results.csv | A Global ArUco-Based Lidar Navigation System for UAV Navigation in GNS |
| REC_1308 | short | U | screening_results.csv | Multi-sensor Data Fusion for Autonomous Unmanned Aerial Vehicle Naviga |
| REC_1316 | short | remote sensing | screening_results.csv | Automated Method for SLAM Evaluation in GNSS-Denied Areas |
| REC_1320 | short | sensors | screening_results.csv | Radar and visual odometry integrated system aided navigation for UAVS  |
| REC_1373 | short | sensors | screening_results.csv | Enabling UAV navigation with sensor and environmental uncertainty in c |
| REC_1402 | short | drones | screening_results.csv | Oxpecker: A Tethered UAV for Inspection of Stone-Mine Pillars |
| REC_1474 | short | U | screening_results.csv | Robust UAV-Satellite Imagery Alignment via Cross-Domain Descriptor Lea |
| REC_1587 | short | sensors | screening_results.csv | Landmark-Based Scale Estimation and Correction of Visual Inertial Odom |
| REC_1660 | short | sensors | screening_results.csv | A Novel Ranging and IMU-Based Method for Relative Positioning of Two-M |

## Phase 4 - Missing per column (NOT_REPORTED/empty)
| column | missing | of |
|---|---|---|
| authors | 279 | 279 |
| venue | 279 | 279 |
| dataset | 177 | 279 |
| funding | 143 | 279 |
| ablation | 91 | 279 |
| future_work | 56 | 279 |
| algorithm | 31 | 279 |
| country | 28 | 279 |
| metrics | 27 | 279 |
| limitations | 27 | 279 |
| method_category | 21 | 279 |
| headline_result | 19 | 279 |
| baseline | 18 | 279 |
| environment | 12 | 279 |
| real_or_sim | 9 | 279 |
| platform | 7 | 279 |
| sensors | 6 | 279 |
| _source_pages | 5 | 279 |
| gps_denied_type | 1 | 279 |
| contribution_type | 1 | 279 |

Fill table rows: 1254 (FILL=475, REPLACE=50, NEEDS_HUMAN=671).

## Phase 5 - Cross-source mismatches
| field | master vs screening |
|---|---|
| title | 105 |
| year | 0 |
| doi | 3 |
| authors | 279 |
| venue | 279 |

Batches: 28 overlapping columns; 1 non-empty mismatch columns.

## Phase 6 - Origin split
- MANUAL: **279**
- BATCHED: **0**
- UNASSIGNED: **0** []

## Phase 7 - Reconciliation
- 636 (title/abstract pass) - 345 (never full-text assessed) = 291 assessed.
- 291 = 285 INCLUDE + 6 EXCLUDE (REC_0053, REC_0693, REC_0866, REC_1582, REC_1688, REC_1715).
- 285 INCLUDE - 6 deferred (REC_0023, REC_0035, REC_0244, REC_0363, REC_1217, REC_1667) = 279 master rows.
- 288 PDFs = 279 in-corpus + 6 deferred + 3 duplicate-EXCLUDE.
- No pid dropped at merge: master is a strict subset of screening INCLUDE; 0 orphans.
- extraction mirror (03_extraction/per_paper): 289 files; _MANUAL REC files: 279.

## Phase 8 - Next actions
- Replace 47 mangled titles in master from screening_results.csv (see MASTER_FILL_TABLE.csv).
- Populate authors (279) from screening_results.csv and venue (188) from REC_*.md.
- Repair 3 placeholder DOIs from screening_results.csv.
- Review 58 remaining title mismatches (PDF-junk affixes) before any auto-replace.
- Resolve 671 NEEDS_HUMAN fill rows (no recoverable source).

