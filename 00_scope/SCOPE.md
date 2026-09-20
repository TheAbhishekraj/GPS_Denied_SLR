# SCOPE: GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)

## Q1. Review title
GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)

## Q2. Research questions (list them)
RQ1. Which sensor-fusion configurations (camera, LiDAR, IMU, radar, UWB, barometer, ultrasonic) are most commonly used for GPS-denied UAV navigation, and how has their prevalence shifted between 2010 and 2026?

RQ2. What localization accuracy and robustness metrics are reported across different GPS-denied environments (indoor, urban canyon, subterranean, forest, adversarial), and how do they vary by environment and platform?

RQ3. Which algorithmic approaches (VIO, SLAM, LIO, filter-based fusion, learning-based methods) dominate the literature, and how do they compare on validation type (real flight vs simulation) and reported performance?

RQ4. What limitations and future research directions are identified in the corpus, particularly regarding adversarial and electronic-warfare conditions?

## Q3. Databases searched (name every one)
IEEE Xplore and Scopus.

## Q4. Search window (start year – end year)
2010 to 2026 (inclusive).

## Q5. Inclusion criteria (list them)
I1. Published 2010–2026 (inclusive).
I2. English language.
I3. Peer-reviewed journal articles or conference papers.
I4. Addresses GPS/GNSS-denied navigation as the primary topic (not incidental).
I5. Focuses on UAVs / drones / unmanned aerial systems.
I6. Presents a multi-sensor fusion approach.
I7. Includes experimental validation or simulation results.

## Q6. Exclusion criteria (list them)
E1. Purely theoretical with no validation.
E2. GPS-based navigation only (denial is not the setting).
E3. Terrestrial vehicles only (no UAV focus).
E4. Single-sensor approaches only.
E5. Non-English publications.
E6. Published before 2010.
E7. Non-peer-reviewed (preprints, blogs, white papers).

## Q7. Quality appraisal approach (max points, dimensions, tier cutoffs)
Quality appraisal scale: 0 to 10 points across 4 dimensions.

A. Experimental Rigor (0–4)
   +2  Real-world experiments on physical platform (not sim only)
   +1  Ground-truth comparison (RTK-GPS, motion capture, total station, or survey-grade map)
   +1  Repeatability evidence: multiple runs with variance, or public dataset / code

B. Reporting Completeness (0–3)
   +1  Reports absolute position error (RMSE / ATE) AND relative drift
   +1  Reports trajectory length, duration, and environment scale
   +1  Reports failure modes or ablation analysis

C. Baseline Fairness (0–2)
   +1  Compares against at least one established baseline (e.g., ORB-SLAM3, VINS-Mono, LIO-SAM, EKF)
   +1  Baselines re-implemented or run under matched conditions (not copied numbers)

D. Reproducibility (0–1)
   +1  Code, dataset, or sufficient implementation detail released

Quality tiers:
  Q-high    qa_total 8–10
  Q-medium  qa_total 5–7
  Q-low     qa_total 0–4

Policy rule: simulation-only papers are capped at Q-medium regardless of score.

Appraisal procedure: two appraisers independently score 20% of papers; target ICC(2,1) or weighted Cohen's kappa >= 0.75 before one appraiser proceeds solo.

## Q8. Venues to include or exclude
INCLUDE:
  - Peer-reviewed journals and conferences in robotics, navigation, aerospace, and autonomous systems.
  - Examples (representative, not exhaustive):
      IEEE Transactions on Robotics
      IEEE Robotics and Automation Letters (RA-L)
      IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)
      IEEE International Conference on Robotics and Automation (ICRA)
      Journal of Field Robotics
      GPS Solutions
      Navigation (ION)
      Sensors (MDPI)
      IEEE Sensors Journal
      Aerospace / Drones (MDPI)
  - Any Scopus- or IEEE-indexed venue in these domains.

EXCLUDE:
  - Predatory or non-indexed journals.
  - Non-peer-reviewed sources: blogs, white papers, vendor documentation, unrefereed preprints.
  - Venues outside the robotics / navigation / aerospace / autonomous-systems domains.

## Q9. Language filter
English only.

## Q10. Document types (journal / conference / both)
Peer-reviewed journal articles and conference papers only.

Excludes: books, book chapters, theses, dissertations, editorials, letters to the editor, and unrefereed preprints.
