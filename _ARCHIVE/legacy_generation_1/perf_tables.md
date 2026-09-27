# Performance Tables with Quality Appraisal Tiers

## Table 1: Visual-Inertial Odometry / SLAM Systems
| Method | Sensors | ATE RMSE (m) | Environment | QA Tier |
|---|---|---|---|---|
| VIO-Baseline | Mono-Camera + IMU | 0.12 | Indoor | Q-high |
| Stereo-VIO | Stereo-Camera + IMU | 0.08 | Urban | Q-high |
| Thermal-VIO | Thermal + IMU | 0.25 | Underground | Q-medium |

## Table 2: LiDAR-Inertial SLAM Systems
| Method | Sensors | ATE RMSE (m) | Environment | QA Tier |
|---|---|---|---|---|
| LIO-SAM | 3D LiDAR + IMU | 0.04 | Forest | Q-high |
| FAST-LIO2 | 3D LiDAR + IMU | 0.03 | Indoor/Outdoor | Q-high |
| Lightweight-LIO | 2D LiDAR + IMU | 0.15 | Indoor | Q-medium |

## Table 3: UWB & Radio-Assisted Localization Systems
| Method | Sensors | ATE RMSE (m) | Environment | QA Tier |
|---|---|---|---|---|
| UWB-IMU Fusion | UWB + IMU | 0.18 | Indoor Arena | Q-medium |
| RF-TPOA | RF Beacons + IMU | 0.35 | Industrial | Q-low |
