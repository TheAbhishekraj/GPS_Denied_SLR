### Table 1: Method Distribution and Validation Breakdown (N=1,700)

| Method | Total | Real-World | Simulation | Both | Real:Sim |
| --- | --- | --- | --- | --- | --- |
| Radio/Infrastructure (UWB/WiFi/5G) | 975 | 728 | 220 | 27 | 3.3:1 |
| Hybrid Classical-DL | 231 | 164 | 64 | 3 | 2.6:1 |
| LiDAR SLAM (LOAM/FAST-LIO2/LIO-SAM) | 146 | 125 | 17 | 4 | 7.4:1 |
| Filter-Based VIO (MSCKF/EKF) | 134 | 105 | 24 | 5 | 4.4:1 |
| Visual SLAM | 70 | 57 | 10 | 3 | 5.7:1 |
| Optimization-Based VIO (OKVIS/VINS-Mono/ORB-SLAM3) | 47 | 32 | 11 | 4 | 2.9:1 |
| Visual-LiDAR-Inertial Fusion (VLI) | 45 | 36 | 8 | 1 | 4.5:1 |
| Multi-Agent Collaborative SLAM | 26 | 14 | 11 | 1 | 1.3:1 |
| Deep Learning Odometry | 25 | 21 | 4 | 0 | 5.2:1 |
| Map-Based Localization | 1 | 0 | 1 | 0 | 0.0:1 |

*Real:Sim* = ratio of real-world to simulation experiments. Higher = more field-validated.


---

### Table 2: ATE_RMSE Performance by Primary Method (numeric metres, outliers >200 m excluded, N>=3)

| Method | Total | ATE Papers (m) | ATE Median | ATE Min | ATE Max |
| --- | --- | --- | --- | --- | --- |
| Radio/Infrastructure (UWB/WiFi/5G) | 975 | 112 | 5.000 m | 0.011 m | 200.000 m |
| Hybrid Classical-DL | 231 | 21 | 3.000 m | 0.024 m | 200.000 m |
| LiDAR SLAM (LOAM/FAST-LIO2/LIO-SAM) | 146 | 19 | 0.890 m | 0.010 m | 100.000 m |
| Filter-Based VIO (MSCKF/EKF) | 134 | 13 | 2.000 m | 0.089 m | 15.000 m |
| Visual-LiDAR-Inertial Fusion (VLI) | 45 | 11 | 2.600 m | 0.050 m | 10.000 m |
| Optimization-Based VIO (OKVIS/VINS-Mono/ORB-SLAM3) | 47 | 5 | 0.800 m | 0.500 m | 150.000 m |
| Visual SLAM | 70 | 5 | 0.290 m | 0.052 m | 5.360 m |
| Multi-Agent Collaborative SLAM | 26 | 3 | 8.000 m | 0.540 m | 48.200 m |

*ATE Median/Min/Max* computed only on papers reporting numeric ATE_RMSE in metres.
Values >200 m excluded as likely unit-mismatch artefacts from abstract-only extraction.
Methods with <3 valid ATE papers omitted from this table.


---

### Table 3: Sensor Modality Frequency (N=1,700, multi-label)

| Sensor | Papers | Pct |
| --- | --- | --- |
| IMU | 1332 | 78.4% |
| Monocular_Camera | 900 | 52.9% |
| LiDAR_3D | 328 | 19.3% |
| UWB | 134 | 7.9% |
| Stereo_Camera | 68 | 4.0% |
| Radar_mmWave | 61 | 3.6% |
| Sonar | 59 | 3.5% |
| Depth_Camera | 51 | 3.0% |
| LiDAR_2D | 45 | 2.6% |
| WiFi | 30 | 1.8% |
| Thermal_Camera | 20 | 1.2% |

IMU appears in **1332/1700 = 78.4%** of all papers.
