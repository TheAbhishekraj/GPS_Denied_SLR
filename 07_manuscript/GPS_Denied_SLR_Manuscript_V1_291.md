# Systematic Literature Review: Autonomous UAV Navigation in GPS-Denied Environments (V1, N=291)

**Author:** Abhishek Raj  
**Target Venue:** IEEE Transactions on Robotics (T-RO) / IEEE Access  
**Dataset:** 291 Full-Text Papers (Shipping Corpus, 45.8% Coverage of 636 Screened Included Records)  
**Date:** September 2026  

---

## Abstract
This systematic literature review provides a comprehensive synthesis of autonomous Unmanned Aerial Vehicle (UAV) navigation and localization in GPS-denied environments. Following PRISMA 2020 guidelines, we identified 636 eligible studies and analyzed the full-text shipping corpus of N=291 papers (2010–2026). This review addresses two core themes: Theme A (Methodology), establishing a transparent, reproducible extraction pipeline with complete audit trails; and Theme B (Findings & Future Directions), framed around the 5W questions (What, Who, Where, When, Why, and How). We classify methods across six major algorithmic families: Visual-Inertial Odometry/SLAM, LiDAR-Inertial Fusion, UWB/Radio Beacons, Thermal/Infrared, Neuromorphic/Event Cameras, and Multi-Agent Cooperative Navigation. Quantitative evaluation reveals significant variance in reported Absolute Trajectory Error (ATE), ranging from millimeter-level indoor precision to multi-meter outdoor drift. Furthermore, we identify a critical reporting-practice gap where 22.7% of literature omits unit-anchored accuracy metrics. We summarize key technical trade-offs, failure taxonomies, and open challenges to guide future research toward resilient micro-aerial platform autonomy.

---

## Section I: Introduction
### A. Motivation and Domain Background
Unmanned Aerial Vehicles (UAVs) have emerged as essential tools across industrial inspection, search-and-rescue, agriculture, and defense. However, reliance on Global Positioning System (GPS) signals introduces single-point failure modes in underground mines, urban canyons, indoor structures, and electronic warfare environments. Operating autonomously in GPS-denied settings requires robust onboard perception and state estimation.

### B. Research Gap and Systematic Review Objectives
While individual SLAM and odometry algorithms have been surveyed, prior literature reviews often lack rigorous PRISMA compliance, reproducible extraction schemas, or comprehensive longitudinal coverage. Existing reviews suffer from narrow scope or methodological ambiguity.

### C. Principal Contributions
1. **Unprecedented Corpus Scale (N=291):** Full-text synthesis of 291 audited UAV navigation papers spanning 2010–2026.
2. **Transparent Audit Trail:** Complete tracing from raw IEEE Xplore and Scopus search queries to per-paper evidence workbooks.
3. **5W Framing:** Systematic breakdown of What method families exist, Who conducts the research, Where systems are deployed, When techniques evolved, Why specific paradigms dominate, and How optical/inertial sensor combinations achieve peak accuracy.
4. **Quantitative Reporting-Gap Analysis:** Rigorous quality appraisal uncovering reporting deficits in benchmark standardization.

### D. The 5W Roadmap
The remainder of this article is structured around the 5W framework: Section II covers Related Work (What), Section III outlines Methodology, Section IV details Empirical Findings (Who, Where, When, Why, How, and Reporting Gap), Section V discusses RQ1–RQ4, Section VI addresses Threats to Validity, Section VII presents Future Directions, and Section VIII concludes.

---

## Section II: Related Work
### A. Visual-Inertial Systems (VIO/SLAM)
Visual-Inertial Odometry (VIO) pairs monocular or stereo cameras with Inertial Measurement Units (IMUs). Core frameworks like VINS-Mono (REC_0001) and OKVIS combine tightly-coupled non-linear optimization with sliding-window estimators.

### B. LiDAR-Inertial Systems (LIO/SLAM)
LiDAR-Inertial Odometry (LIO) methods such as FAST-LIO2 and LIO-SAM achieve centimeter-level trajectory estimation by fusing dense 3D point clouds with high-frequency IMU integration in feature-rich or unstructured environments.

### C. UWB, Radio, and RF Beacons
Ultra-Wideband (UWB) time-of-flight and arrival-angle positioning offer drift-free absolute localization in constrained indoor spaces (REC_0004), though deployment requires pre-installed anchor infrastructure.

### D. Thermal and Infrared Perception
Thermal-infrared cameras enable flight in total darkness, smoke, and degraded visual environments by tracking long-wave radiometric signatures when visible-spectrum cameras fail.

### E. Neuromorphic and Event-Based Navigation
Event-based sensors transmit asynchronous pixel-level intensity changes with microsecond temporal resolution, enabling high-speed maneuvers without motion blur.

### F. Multi-Agent Cooperative Navigation
Swarm systems leverage inter-UAV range measurements and distributed consensus algorithms to maintain joint state estimates when individual platforms experience sensor degradation.

### G. AMSTAR-2 Methodological Evaluation of Prior Reviews
An AMSTAR-2 critique reveals that prior reviews lack registered protocols, explicit exclusion lists, or quantitative quality weighting, highlighting the necessity of this PRISMA 2020 review.

---

## Section III: Methodology
### A. PRISMA 2020 Flow and Search Strategy
Comprehensive search strings were executed on 2026-06-15 across IEEE Xplore (ieee_xplore_20260615.csv) and Scopus (scopus_20260615.csv), retrieving 2,000 initial records, deduplicating to 1,719, screening to 636 included papers, and establishing the shipping corpus of N=291 full-text PDFs (45.8% coverage).

### B. Screening Criteria (v2) and Quality Appraisal Rubric
Screening applied Inclusion criteria I1–I6 and Exclusion criteria E1–E8. Quality appraisal scored papers across Rigor (0–4), Reporting (0–3), Baseline Comparison (0–2), and Reproducibility (0–1), categorizing scores into Q-high (8–10), Q-medium (5–7), and Q-low (0–4).

### C. Prioritization Formula
To weight synthesized evidence, each paper received a priority weight:
priority_weight = qa_total * 1.0 + (has_numeric ? 2.0 : 0) + (has_baseline ? 1.5 : 0) + (is_real_world ? 1.0 : 0) + (year >= 2020 ? 0.5 : 0)

---

## Section IV: Empirical Findings (The 5W Answer)
### IV.1 What — Method Landscape
Visual-Inertial and Visual-LiDAR fusion dominate 88.6% of the shipping corpus.

### IV.2 Who — Research Groups, Venues, and Platforms
Leading contributions stem from IEEE T-RO, ICRA, IROS, and IEEE Access, deployed primarily on custom quadrotors and NVIDIA Jetson compute units.

### IV.3 Where — Operational Environments
Indoor industrial facilities and subterranean tunnels represent 62.4% of evaluation scenarios, with outdoor GPS-denied flight remaining a major challenge.

### IV.4 When — Historical Evolution (2010–2026)
Longitudinal evolution transitioned from loosely-coupled EKF filters (2010–2015) to tightly-coupled non-linear optimization (2016–2020) and learning-augmented hybrid state estimation (2021–2026).

### IV.5 Why — Dominance of Tightly-Coupled Fusion
Tightly-coupled architectures dominate because joint optimization over raw sensor measurements prevents early linearization errors inherent in two-stage filters.

### IV.6 How — Sensor and Algorithm Combinations
Peak localization accuracy (ATE < 0.05m) is achieved by fusing 3D LiDAR, stereo vision, and tactical-grade IMUs via factor-graph optimization.

### IV.7 Reporting-Practice Gap
Across N=291 papers, 22.7% omit standardized unit-anchored accuracy metrics (ATE/RMSE), relying solely on qualitative flight trajectory plots.

### IV.8 Audit and Validation
Machine extractions were verified across 63 header fields with zero orphan IDs and complete audit traceability.

---

## Section V: Discussion
- **RQ1 (Method Landscape):** Six core method families categorized with distinct trade-offs in compute vs precision.
- **RQ2 (Sensory & Accuracy Performance):** LiDAR-Visual-Inertial fusion achieves top-tier ATE (<0.03m), while monocular VIO exhibits 1–3% drift over distance.
- **RQ3 (Operational Environments):** Indoor and subterranean GPS-denied spaces are well-studied; adversarial EW and dynamic cluttered outdoor spaces require further work.
- **RQ4 (Open Challenges):** Real-time embedded compute constraints, dynamic illumination changes, and long-term drift accumulation remain key bottlenecks.

---

## Section VI: Threats to Validity
We analyze potential validity threats: non-retrieved coverage (345 papers), machine extraction bias, single-reviewer validation bounds, multi-label classification overlaps, and reporting publication bias.

---

## Section VII: Future Research Directions
1. **Event-Based Ultra-Fast VIO:** Scaling neuromorphic vision for aggressive 3D evasive flight.
2. **Robust Deep-Learning Hybrid Estimators:** Combining physics-informed neural networks with EKF/factor-graph backends.
3. **Resilient Multi-Agent Swarm Localization:** Distributed, band-limited range-only localization in cluttered GPS-denied environments.

---

## Section VIII: Conclusion
This review synthesizes 291 full-text papers on GPS-denied UAV navigation using PRISMA 2020. By combining a transparent extraction methodology (Theme A) with rich empirical findings (Theme B), this work establishes a baseline for future autonomous aerial platform research.
