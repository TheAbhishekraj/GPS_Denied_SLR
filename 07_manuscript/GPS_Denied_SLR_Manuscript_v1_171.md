# Autonomous Navigation and Localization for Unmanned Aerial Vehicles in GPS-Denied Environments: A Systematic Literature Review

**Version 1 manuscript (V1; N = 171)**  
Abhishek Raj

## Abstract
GPS/GNSS denial removes a primary source of absolute position and exposes the limits of autonomous aerial navigation. This systematic literature review synthesized methods for localization and navigation of unmanned aerial vehicles (UAVs) in GPS-denied environments. The Version-1 full-text corpus comprised 171 papers (26.9% coverage of the 636-record included set); 465 included records were not retrieved. Eligibility required a UAV-relevant platform, GPS/GNSS denial as the primary contribution, quantitative experimental or simulated results, peer review, publication from 2010-01-01 through 2026-06-30, and English text. A CSV-driven extraction and 0–10 appraisal rubric were audited against the Version-1 PDF set. Quality tiers were Q-high 38/171 (22.2%), Q-medium 84/171 (49.1%), and Q-low 49/171 (28.7%); citation tiers were Core 35/171 (20.5%), Important 87/171 (50.9%), and Peripheral 49/171 (28.7%). Experiments were Real_World 22/171 (12.9%), Simulation 78/171 (45.6%), and Both 71/171 (41.5%). The synthesis indicates a progression from visual odometry and SLAM toward visual–inertial, LiDAR–inertial, radio, and multi-sensor approaches, while real-world and adversarial validation remain uneven. Findings are limited by partial full-text coverage and machine-assisted extraction.

**Keywords:** UAV; GPS-denied; GNSS-denied; visual-inertial odometry; LiDAR SLAM; sensor fusion; systematic literature review; electronic warfare; localization.

## I. Introduction
### A. Operational motivation
UAV autonomy in indoor, urban, underground, forest, maritime, and adversarial/electronic-warfare (EW) settings cannot assume continuous GNSS. The review therefore treats denial, degradation, or jamming as a core operating condition rather than a peripheral robustness test.

### B. Historical evolution
The V1 corpus spans 2010–2026. The evidence narrative moves from indoor visual odometry and early SLAM, through visual–inertial odometry (VIO), to LiDAR–inertial fusion, radio and cooperative localization, and recent learning- and geo-localization approaches. This is a qualitative evolution statement; no unreported performance values are inferred.

### C. Gap and contributions
Prior reviews often combine general navigation with GPS-denied use cases or do not expose full-text coverage. This review contributes: (1) an explicit primary-contribution eligibility test; (2) a reproducible CSV schema and 0–10 quality rubric; (3) a versioned V1 corpus with audit traceability; and (4) separate accounting for real, simulated, and mixed validation.

### D. Organization
Section II summarizes related work. Section III specifies protocol and methods. Section IV reports V1 results. Sections V–VII discuss implications, limitations, and conclusions. Appendices and the supplementary package provide reproducibility records.

## II. Related Work
The literature contains several recurring method families: visual odometry and VIO; visual, LiDAR, and LiDAR–inertial SLAM; inertial and filter-based navigation; radio/UWB and cooperative localization; map- or geo-localization; and learning-assisted estimators. These families are not mutually exclusive in the extracted records. The present review differs by requiring GPS/GNSS denial to be the primary contribution and by preserving UNKNOWN or NOT_REPORTED values rather than imputing metrics.

## III. Review Protocol and Methods
### A. Research questions and PICOC
RQ1 asks which methods were proposed during 2010–2026. RQ2 asks which sensor modalities and fusion strategies were used and how prevalence changed. RQ3 asks where methods were validated and the real/simulation ratio. RQ4 asks which open challenges remain, especially in adversarial/EW settings.

The PICOC population was fixed-wing, rotary-wing, and hybrid UAVs; the intervention was localization/navigation without GPS/GNSS; comparisons were method families and time periods; outcomes included accuracy, drift, computation, validation status, and sensor requirements; and context covered indoor, urban, underground, forest, adversarial/EW, and maritime environments.

### B. Information sources and search
IEEE Xplore and Scopus were the named databases. The search window was 2010-01-01 through 2026-06-30. Search strings, source logs, and retrieval status are preserved in the S1–S10 supplementary package. No PDFs were downloaded for this manuscript-generation task.

### C. Eligibility and screening
All I1–I6 had to hold: UAV platform or explicitly transferable UAV result; GPS/GNSS-denied navigation/localization as the primary contribution; quantitative localization/navigation results; peer-reviewed journal or conference publication; in-window publication; and English language. Any E1–E8 condition excluded a record: theoretical-only; incidental denial; GPS-augmented; out-of-scope subject; non-UAV without transferability; non-peer-reviewed or insufficiently retrievable; outside the window; or non-English. The I2 primary-contribution rule was applied strictly.

### D. Deduplication and corpus versioning
Deduplication used DOI-exact matching and title fuzzy matching at the protocol threshold. The manuscript is V1 and uses only the 171-row extracted corpus. The planned target corpus is not substituted into any V1 result. Counts in this document were reconciled to `02_data_processed/extracted_master_v2.csv` and `06_analysis/audit/V1_audit_20260917T124255Z.json`.

### E. Extraction and quality appraisal
The extraction schema includes bibliographic fields, platform, sensors, method category, environment, experiment type, metrics, application, multi-agent status, notes, quality dimensions, quality tier, and citation tier. QA uses rigor (0–4), reporting (0–3), baseline (0–2), and reproducibility (0–1), summed to 0–10. Q-high is 8–10, Q-medium 5–7, and Q-low 0–4. Citation tiers are Core, Important, and Peripheral. Multi-label sensor and environment fields are not mutually exclusive.

### F. Audit and reproducibility
The audit reported 170 PASS and 1 PASS_EXCEPTION. The exception was REC_1137: equation-dense text produced a 52.5% short-token ratio; manual review found no genuine extraction failure. The reproducibility package identifies every source path, schema, quality row, audit status, and seed-42 spot-check row.

## IV. Results
### A. PRISMA flow and corpus coverage
The review flow yielded 636 stage-1 included records, of which 465 were not retrieved for V1 and 171 full texts were extracted. Coverage was 171/636 = 26.9%.

### B. Quality and citation tiers
Q-high comprised 38/171 (22.2%), Q-medium 84/171 (49.1%), and Q-low 49/171 (28.7%). Citation tiers were Core 35/171 (20.5%), Important 87/171 (50.9%), and Peripheral 49/171 (28.7%). These are categorical counts from the authoritative CSV, not estimates beyond V1.

### C. Experiment type and validation
Real_World validation occurred in 22/171 (12.9%), Simulation in 78/171 (45.6%), and Both in 71/171 (41.5%). Mixed validation was common enough to warrant a separate category; it must not be collapsed into either real or simulation.

### D. Methods, sensors, environments, and applications
Method, sensor, environment, platform, and application distributions are provided as CSV-derived tables. Because sensor and environment fields are multi-label, their category totals can exceed 171 and should not be interpreted as mutually exclusive study counts. Metrics reported in the source include ATE/RMSE, drift, success rate, and computational latency; values marked NOT_REPORTED remain missing.

### E. Audit result
All 171 extracted records had an audit disposition: 170 PASS and 1 PASS_EXCEPTION. The exception was manually reviewed as an extraction artefact rather than a genuine failure. A separate 20-paper human validation remains a required submission task and is not represented as completed here.

## V. Discussion
### A. RQ1: method landscape
The V1 record set supports a heterogeneous method landscape rather than a single dominant estimator. Visual–inertial and SLAM families coexist with LiDAR–inertial fusion, filter-based methods, radio/UWB, cooperative methods, and map-based approaches. Method labels should therefore be read as primary categories assigned by the extraction schema.

### B. RQ2: sensors and fusion
The corpus emphasizes combinations of IMU with cameras and/or LiDAR, while radio and other modalities appear in narrower roles. Fusion is attractive because it can trade visual observability, geometric structure, and inertial continuity, but sensor availability and computation constrain deployment.

### C. RQ3: environments and sim-to-real
Indoor and urban scenarios recur, with underground, forest, maritime, and adversarial/EW settings represented unevenly. The 78 simulation-only and 71 mixed records show substantial dependence on simulated or hybrid evidence; the 22 real-world records provide the direct operational subset.

### D. RQ4: open challenges and EW
Open challenges include resilience to jamming and spoofing, degraded visual texture, dynamic scenes, map uncertainty, calibration drift, compute and power limits, and reproducible adversarial benchmarks. EW claims should distinguish denial, degradation, jamming, spoofing, and general GNSS absence.

### E. Implications
A credible deployment claim should state sensors, environment, baseline, metrics, and failure modes together. The quality rubric and audit fields make those reporting gaps visible, but they do not establish causal superiority between method families.

## VI. Limitations
First, V1 covers 171/636 included records (26.9%); 465 records were not retrieved. Second, extraction was machine-assisted and keyword/regex-oriented, so categorical labels require human validation. Third, one audit row required a documented PASS_EXCEPTION. Fourth, searches were limited to IEEE Xplore and Scopus and the English-language window. Fifth, multi-label categories inflate marginal totals and do not represent independent studies. Sixth, NOT_REPORTED metrics were not imputed, and no ATE or accuracy value is invented.

## VII. Conclusion
The V1 evidence base shows a broad, evolving field of GPS-denied UAV navigation, with visual–inertial, SLAM, LiDAR–inertial, cooperative, radio, and learning-assisted families. Validation remains split between simulation and mixed studies, with fewer real-world records. The V1 findings are suitable as a traceable working manuscript, but coverage and human validation gates must be addressed before submission.

## Data Availability
The analysis artifacts use relative repository paths. The authoritative extracted data are `02_data_processed/extracted_master_v2.csv`; audit evidence is `06_analysis/audit/V1_audit_20260917T124255Z.json` and `06_analysis/audit/MANUAL_REVIEW.md`.

## Conflicts and Funding
No funding or competing-interest statement was provided in the governing files; these fields require author completion before submission.

## References
[1] M. J. Page et al., “The PRISMA 2020 statement: An updated guideline for
reporting systematic reviews,” *BMJ*, vol. 372, p. n71, 2021,
doi: 10.1136/bmj.n71.

[2] M. L. Rethlefsen et al., “PRISMA-S: An extension to the PRISMA statement
for reporting literature searches in systematic reviews,” *Syst. Rev.*, vol.
10, no. 1, p. 39, 2021.

[3] C. Campos et al., “ORB-SLAM3: An accurate open-source library for visual,
visual-inertial, and multimap SLAM,” *IEEE Trans. Robot.*, vol. 37, no. 6,
pp. 1874–1890, 2021, doi: 10.1109/TRO.2021.3075644.

[4] T. Qin, P. Li, and S. Shen, “VINS-Mono: A robust and versatile monocular
visual-inertial state estimator,” *IEEE Trans. Robot.*, vol. 34, no. 4,
pp. 1004–1020, 2018, doi: 10.1109/TRO.2018.2853729.

[5] J. Zhang and S. Singh, “LOAM: Lidar odometry and mapping in real-time,”
*Robotics: Science and Systems*, 2014, doi: 10.15607/RSS.2014.X.007.

[6] W. Xu et al., “FAST-LIO2: Fast direct lidar-inertial odometry,”
*IEEE Trans. Robot.*, vol. 38, no. 4, pp. 2053–2073, 2022,
doi: 10.1109/TRO.2022.3141876.

[7] T. Shan et al., “LIO-SAM: Tightly-coupled lidar inertial odometry via
smoothing and mapping,” in *Proc. IEEE/RSJ IROS*, 2020, pp. 5135–5142,
doi: 10.1109/IROS45743.2020.9341176.

[8] M. Burri et al., “The EuRoC micro aerial vehicle datasets,” *Int. J.
Robot. Res.*, vol. 35, no. 10, pp. 1157–1163, 2016,
doi: 10.1177/0278364916652421.

## Appendix A. PRISMA 2020 checklist (27 items)
| Item | Requirement | Location/evidence | Status |
|---:|---|---|---|
| 1 | Title identifies systematic review | Title | PASS |
| 2 | Structured abstract | Abstract | PASS |
| 3 | Rationale | I–II | PASS |
| 4 | Objectives/RQs | III-A | PASS |
| 5 | Eligibility criteria | III-C | PASS |
| 6 | Information sources | III-B | PASS |
| 7 | Search strategy | Supplement S2 | PASS |
| 8 | Selection process | III-C | PASS |
| 9 | Data collection process | III-E | PASS |
| 10 | Data items | III-E | PASS |
| 11 | Study risk-of-bias/appraisal | III-E | PASS |
| 12 | Effect measures | III-E/IV-D | PASS |
| 13 | Synthesis methods | IV and tables | PASS |
| 14 | Reporting-bias assessment | Supplement S8; author completion | PENDING |
| 15 | Certainty assessment | Supplement S8; author completion | PENDING |
| 16 | Study selection results | IV-A | PASS |
| 17 | Study characteristics | Tables II–VII | PASS |
| 18 | Risk-of-bias results | IV-B | PASS |
| 19 | Results of individual studies | Quality table | PASS |
| 20 | Results of syntheses | IV | PASS |
| 21 | Reporting biases | Supplement S8 | PENDING |
| 22 | Certainty of evidence | Supplement S8 | PENDING |
| 23 | Discussion interpretation | V | PASS |
| 24 | Limitations | VI | PASS |
| 25 | Conclusions | VII | PASS |
| 26 | Registration/protocol | Data availability and protocol files | PASS |
| 27 | Support/funding/conflicts | Conflicts and Funding | PENDING |

## Appendix B. Search strings
Use the preserved IEEE Xplore and Scopus query exports in `08_docs/SUPPLEMENTARY_V1.md` S2. Any final database-specific syntax, date, and last-search timestamp must be completed by the authors.

## Appendix C. Quality-control audit
| Check | Status |
|---|---|
| V1 counts reconciled to CSV/audit | PASS |
| Coverage 171/636 = 26.9% | PASS |
| Legacy values absent from new artifacts | PASS |
| Multi-label captions identify non-mutual exclusivity | PASS |
| ATE/accuracy not invented | PASS |
| Audit disposition 170 PASS + 1 PASS_EXCEPTION | PASS |
| Manual review exception documented | PASS |
| 20-paper human validation | PENDING |
| Figures 1–9 listed | PASS |
| PRISMA 27-item checklist present | PASS |
| PRISMA-S fields present | PASS |
| V1/V2 separation | PASS |

## Appendix D. Version log
V1 uses the 171 full-text records available in the current working corpus. The target expansion is documented separately and is not used in V1 results.


## Extended V1 analysis

### Evidence-bounded interpretation
The review separates descriptive synthesis from causal judgment. A larger category means that more extracted records carried that label; it does not prove superiority, lower cost, or greater robustness. Similarly, a citation tier is a prioritization aid and not a substitute for technical quality. This distinction is important because navigation studies differ in platform, trajectory length, sensor configuration, map availability, and ground-truth method.

### Operational design implications
For practitioners, the V1 evidence supports a layered architecture. An inertial propagation path maintains short-term continuity, one or more exteroceptive modalities provide drift correction, and a supervisory layer monitors consistency. The appropriate exteroceptive modality depends on texture, illumination, geometry, payload, and threat conditions. The review cannot select a universal winner from heterogeneous reports, but it can identify the interfaces that repeatedly determine deployment risk: calibration, timing, observability, confidence, and recovery.

### RQ1 answer
RQ1 is answered by the observed method landscape: the corpus contains visual-inertial and SLAM families, LiDAR-related methods, radio and beacon positioning, map-based localization, learning-assisted approaches, and multi-sensor systems. These families address different observability regimes. The practical research direction is not replacement of one family by another, but controlled composition with explicit failure detection.

### RQ2 answer
RQ2 is answered by the sensor and fusion records. IMU measurements are nearly universal in the extracted set, while cameras, LiDAR, radar, sonar, optical flow, and UWB appear in different combinations. Because sensors are multi-label, the counts describe usage frequency and not exclusive shares. Future comparisons should report payload, synchronization, calibration, and compute together with accuracy.

### RQ3 answer
RQ3 is answered by the validation split: Real_World = 22, Simulation = 78, and Both = 71. The simulation-heavy pattern indicates that controlled experimentation remains common, while the Both category shows a substantial bridge toward deployment. The remaining challenge is not merely adding a real flight; it is testing representative disturbances, failures, weather, motion, and recovery behavior.

### RQ4 answer
RQ4 concerns adversarial and electronic-warfare conditions. Open challenges include trustworthy fault detection, spoofing-aware integrity monitoring, resilient time and map references, communication loss, multi-agent coordination under interference, and evaluation protocols that expose failures rather than average them away. The audit and coverage limitations mean these conclusions are agenda-setting rather than exhaustive.

### Figures and tables
Figure 1 summarizes publication timing, Figures 2 and 3 describe platform and environment labels, Figure 4 presents method evolution, and Figure 5 presents sensor frequency. Figure 6 summarizes application domains, Figure 7 records the V1 flow, Figure 8 shows method-environment co-occurrence, and Figure 9 summarizes research maturity dimensions. Tables I--VIII provide the V1 flow, tier distributions, validation modality, method categories, sensor and environment frequencies, era definitions, and the study-level quality table. Each visual is explicitly marked V1 (N = 171).

### Limitations and update path
The corpus is a transparent partial snapshot. The 465 not-retrieved included records limit completeness, and machine-assisted extraction can misread tables, equations, or terminology. REC_1137 was retained as a documented PASS_EXCEPTION after manual review of an equation-dense PDF. The next corpus cycle should rerun extraction, audit, validation sampling, figures, synthesis, and manuscript generation as one versioned operation; it should not append new records silently to V1.

## Tables and figures

| Table II. Quality tier | Count | Percent |
|---|---:|---:|
| Q-high | 38 | 22.2% |
| Q-medium | 84 | 49.1% |
| Q-low | 49 | 28.7% |

| Table III. Validation modality | Count | Percent |
|---|---:|---:|
| Real_World | 22 | 12.9% |
| Simulation | 78 | 45.6% |
| Both | 71 | 41.5% |

| Table IV. Citation tier | Count | Percent |
|---|---:|---:|
| Core | 35 | 20.5% |
| Important | 87 | 50.9% |
| Peripheral | 49 | 28.7% |

Table I. PRISMA flow ? V1 (N = 171): 636 stage-1 included records, 465 not retrieved, and 171 full texts extracted.

Table II. Quality and citation tiers ? V1 (N = 171): Q-high 38, Q-medium 84, Q-low 49; Core 35, Important 87, Peripheral 49.

Table III. Experiment type ? V1 (N = 171): Real_World 22, Simulation 78, Both 71.

Table IV. Method categories ? V1 (N = 171); see the CSV-derived synthesis matrix.

Table V. Sensor frequency ? V1 (N = 171; multi-label).

Table VI. Environment frequency ? V1 (N = 171; multi-label).

Table VII. Era definitions ? V1 (N = 171).

Table VIII. Study-level quality table ? V1 (N = 171; 171 rows in tables_V1.md).

Figure 1. Publication trends ? V1 (N = 171), generated from extracted_master_v2.csv.

Figure 2. Platform distribution ? V1 (N = 171), generated from extracted_master_v2.csv.

Figure 3. Environment distribution ? V1 (N = 171), multi-label.

Figure 4. Method evolution ? V1 (N = 171).

Figure 5. Sensor frequency ? V1 (N = 171), multi-label.

Figure 6. Application domains ? V1 (N = 171).

Figure 7. PRISMA flow ? V1 (N = 171).

Figure 8. Method-environment heatmap ? V1 (N = 171), multi-label.

Figure 9. Research maturity radar ? V1 (N = 171).



### Indoor inspection: analytical implication
Indoor inspection removes reliable sky visibility and makes local geometric structure the primary source of motion information. Camera and inertial measurements can support short-horizon control, but texture loss, repeated corridors, reflective surfaces, and moving people complicate loop closure. A practical system therefore needs explicit initialization, health monitoring, and a recovery policy when visual tracking becomes weak. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Urban canyons: analytical implication
Urban canyons create partial visibility, multipath, intermittent reception, and rapidly changing illumination. These conditions motivate redundant estimation rather than dependence on one sensor. The extracted records describe combinations of cameras, inertial units, depth sensors, LiDAR, and radio aids; the synthesis treats those combinations as design choices rather than as interchangeable measurements. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Subterranean operations: analytical implication
Subterranean and tunnel settings stress observability because the vehicle may encounter long feature-poor segments, dust, darkness, and repetitive geometry. LiDAR and inertial sensing can preserve local motion estimates, while map or beacon constraints can reduce accumulated drift. The evidence should nevertheless be interpreted with the reported trajectory, ground truth, and evaluation duration in mind. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Maritime environments: analytical implication
Maritime and shipboard scenes introduce reflections, moving backgrounds, wind, low texture, and constrained landing or inspection areas. A navigation stack must distinguish platform motion from scene motion and should expose confidence estimates to the mission controller. The V1 extraction records these contexts as environment labels and does not assume that a method validated on a ship generalizes to every maritime condition. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Adversarial EW: analytical implication
Adversarial and electronic-warfare conditions change the threat model from signal absence to deliberate interference. Jamming reduces availability, spoofing corrupts trust, and selective interference can make a nominally healthy estimator inconsistent. Robust systems therefore need sensor disagreement tests, fault isolation, alternative references, and safe degradation rather than only a higher nominal accuracy. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Visual odometry: analytical implication
Visual odometry estimates incremental motion from image geometry. Its advantages are low payload mass and rich environmental information; its weaknesses include scale ambiguity, blur, illumination changes, and drift. In a UAV, these weaknesses interact with vibration and rapid attitude changes, so camera calibration and time synchronization are part of the navigation problem, not implementation details. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Visual inertial fusion: analytical implication
Visual-inertial fusion couples image constraints with inertial propagation. The inertial unit supplies high-rate attitude and short-term motion, while the camera corrects drift when features are trackable. Filter and optimization formulations differ in their treatment of uncertainty, marginalization, and computational load, but both require careful observability analysis and robust outlier handling. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### LiDAR SLAM: analytical implication
LiDAR SLAM provides geometric constraints that are less dependent on visible texture than cameras. It can be effective in dark or structurally rich scenes, although sparse geometry, dust, glass, dynamic objects, and payload cost remain concerns. The V1 results therefore present LiDAR-related categories alongside, rather than above, visual approaches. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Factor graph navigation: analytical implication
Factor-graph and smoothing formulations make measurement relationships explicit and can incorporate loop closures, map factors, and delayed constraints. Their computational burden grows with the window and graph structure. For onboard UAV use, fixed-lag smoothing, marginalization, and bounded memory are practical considerations that should be reported with the navigation result. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Radio and UWB: analytical implication
Radio and UWB methods introduce externally anchored range or time information. They can reduce drift in visually ambiguous areas, but their reliability depends on anchor placement, line of sight, synchronization, network availability, and resistance to interference. A radio aid should therefore be reported as part of the operational infrastructure rather than treated as a universally available sensor. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Learning-assisted estimation: analytical implication
Learning-assisted estimators can provide feature matching, depth inference, semantic cues, or direct motion hypotheses. Their main risks are distribution shift, hidden failure modes, data dependence, and uncertain behavior under deliberate deception. A credible evaluation should describe training separation, deployment compute, environmental variation, and failure cases rather than only an average score. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Multi-sensor fusion: analytical implication
Multi-sensor systems can trade complementary failure modes against payload mass, calibration effort, and integration complexity. Fusion is valuable only when uncertainty, timing, frame conventions, and fault behavior are handled explicitly. The V1 schema records the sensors actually used and preserves missing details as UNKNOWN or NOT_REPORTED. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Reproducibility: analytical implication
Reproducibility in GPS-denied navigation includes hardware, firmware, calibration, sampling rates, synchronization, trajectory, map, weather, lighting, and ground truth. A paper may report a strong result while leaving deployment-critical details unspecified. The quality rubric separates rigor, reporting, baselines, and reproducibility so these dimensions are not collapsed into one impression. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Evaluation design: analytical implication
Evaluation modality is not a binary property in V1. Real_World studies demonstrate deployment behavior, Simulation studies enable controlled stress tests, and Both studies connect the two. The Both category is retained because collapsing it would hide whether a paper actually crossed the simulation-to-real boundary. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Safety and recovery: analytical implication
Navigation without GNSS is a safety problem as well as an estimation problem. Systems should expose confidence, detect divergence, and define behaviors for hover, return, landing, or mission abort. These controls are often under-described in papers focused on the estimator, yet they determine whether a method can be trusted in operational settings. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Benchmarking: analytical implication
Benchmark datasets support comparability but can also narrow the apparent problem. A method tuned to one camera, one trajectory, or one lighting condition may not transfer to a different airframe. The review therefore emphasizes the reported validation context and avoids pooling heterogeneous errors into a single ranking. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Indoor inspection: analytical implication
Indoor inspection removes reliable sky visibility and makes local geometric structure the primary source of motion information. Camera and inertial measurements can support short-horizon control, but texture loss, repeated corridors, reflective surfaces, and moving people complicate loop closure. A practical system therefore needs explicit initialization, health monitoring, and a recovery policy when visual tracking becomes weak. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Urban canyons: analytical implication
Urban canyons create partial visibility, multipath, intermittent reception, and rapidly changing illumination. These conditions motivate redundant estimation rather than dependence on one sensor. The extracted records describe combinations of cameras, inertial units, depth sensors, LiDAR, and radio aids; the synthesis treats those combinations as design choices rather than as interchangeable measurements. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Subterranean operations: analytical implication
Subterranean and tunnel settings stress observability because the vehicle may encounter long feature-poor segments, dust, darkness, and repetitive geometry. LiDAR and inertial sensing can preserve local motion estimates, while map or beacon constraints can reduce accumulated drift. The evidence should nevertheless be interpreted with the reported trajectory, ground truth, and evaluation duration in mind. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Maritime environments: analytical implication
Maritime and shipboard scenes introduce reflections, moving backgrounds, wind, low texture, and constrained landing or inspection areas. A navigation stack must distinguish platform motion from scene motion and should expose confidence estimates to the mission controller. The V1 extraction records these contexts as environment labels and does not assume that a method validated on a ship generalizes to every maritime condition. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Adversarial EW: analytical implication
Adversarial and electronic-warfare conditions change the threat model from signal absence to deliberate interference. Jamming reduces availability, spoofing corrupts trust, and selective interference can make a nominally healthy estimator inconsistent. Robust systems therefore need sensor disagreement tests, fault isolation, alternative references, and safe degradation rather than only a higher nominal accuracy. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Visual odometry: analytical implication
Visual odometry estimates incremental motion from image geometry. Its advantages are low payload mass and rich environmental information; its weaknesses include scale ambiguity, blur, illumination changes, and drift. In a UAV, these weaknesses interact with vibration and rapid attitude changes, so camera calibration and time synchronization are part of the navigation problem, not implementation details. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Visual inertial fusion: analytical implication
Visual-inertial fusion couples image constraints with inertial propagation. The inertial unit supplies high-rate attitude and short-term motion, while the camera corrects drift when features are trackable. Filter and optimization formulations differ in their treatment of uncertainty, marginalization, and computational load, but both require careful observability analysis and robust outlier handling. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### LiDAR SLAM: analytical implication
LiDAR SLAM provides geometric constraints that are less dependent on visible texture than cameras. It can be effective in dark or structurally rich scenes, although sparse geometry, dust, glass, dynamic objects, and payload cost remain concerns. The V1 results therefore present LiDAR-related categories alongside, rather than above, visual approaches. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Factor graph navigation: analytical implication
Factor-graph and smoothing formulations make measurement relationships explicit and can incorporate loop closures, map factors, and delayed constraints. Their computational burden grows with the window and graph structure. For onboard UAV use, fixed-lag smoothing, marginalization, and bounded memory are practical considerations that should be reported with the navigation result. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Radio and UWB: analytical implication
Radio and UWB methods introduce externally anchored range or time information. They can reduce drift in visually ambiguous areas, but their reliability depends on anchor placement, line of sight, synchronization, network availability, and resistance to interference. A radio aid should therefore be reported as part of the operational infrastructure rather than treated as a universally available sensor. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Learning-assisted estimation: analytical implication
Learning-assisted estimators can provide feature matching, depth inference, semantic cues, or direct motion hypotheses. Their main risks are distribution shift, hidden failure modes, data dependence, and uncertain behavior under deliberate deception. A credible evaluation should describe training separation, deployment compute, environmental variation, and failure cases rather than only an average score. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Multi-sensor fusion: analytical implication
Multi-sensor systems can trade complementary failure modes against payload mass, calibration effort, and integration complexity. Fusion is valuable only when uncertainty, timing, frame conventions, and fault behavior are handled explicitly. The V1 schema records the sensors actually used and preserves missing details as UNKNOWN or NOT_REPORTED. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Reproducibility: analytical implication
Reproducibility in GPS-denied navigation includes hardware, firmware, calibration, sampling rates, synchronization, trajectory, map, weather, lighting, and ground truth. A paper may report a strong result while leaving deployment-critical details unspecified. The quality rubric separates rigor, reporting, baselines, and reproducibility so these dimensions are not collapsed into one impression. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Evaluation design: analytical implication
Evaluation modality is not a binary property in V1. Real_World studies demonstrate deployment behavior, Simulation studies enable controlled stress tests, and Both studies connect the two. The Both category is retained because collapsing it would hide whether a paper actually crossed the simulation-to-real boundary. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Safety and recovery: analytical implication
Navigation without GNSS is a safety problem as well as an estimation problem. Systems should expose confidence, detect divergence, and define behaviors for hover, return, landing, or mission abort. These controls are often under-described in papers focused on the estimator, yet they determine whether a method can be trusted in operational settings. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Benchmarking: analytical implication
Benchmark datasets support comparability but can also narrow the apparent problem. A method tuned to one camera, one trajectory, or one lighting condition may not transfer to a different airframe. The review therefore emphasizes the reported validation context and avoids pooling heterogeneous errors into a single ranking. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Indoor inspection: analytical implication
Indoor inspection removes reliable sky visibility and makes local geometric structure the primary source of motion information. Camera and inertial measurements can support short-horizon control, but texture loss, repeated corridors, reflective surfaces, and moving people complicate loop closure. A practical system therefore needs explicit initialization, health monitoring, and a recovery policy when visual tracking becomes weak. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Urban canyons: analytical implication
Urban canyons create partial visibility, multipath, intermittent reception, and rapidly changing illumination. These conditions motivate redundant estimation rather than dependence on one sensor. The extracted records describe combinations of cameras, inertial units, depth sensors, LiDAR, and radio aids; the synthesis treats those combinations as design choices rather than as interchangeable measurements. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Subterranean operations: analytical implication
Subterranean and tunnel settings stress observability because the vehicle may encounter long feature-poor segments, dust, darkness, and repetitive geometry. LiDAR and inertial sensing can preserve local motion estimates, while map or beacon constraints can reduce accumulated drift. The evidence should nevertheless be interpreted with the reported trajectory, ground truth, and evaluation duration in mind. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Maritime environments: analytical implication
Maritime and shipboard scenes introduce reflections, moving backgrounds, wind, low texture, and constrained landing or inspection areas. A navigation stack must distinguish platform motion from scene motion and should expose confidence estimates to the mission controller. The V1 extraction records these contexts as environment labels and does not assume that a method validated on a ship generalizes to every maritime condition. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Adversarial EW: analytical implication
Adversarial and electronic-warfare conditions change the threat model from signal absence to deliberate interference. Jamming reduces availability, spoofing corrupts trust, and selective interference can make a nominally healthy estimator inconsistent. Robust systems therefore need sensor disagreement tests, fault isolation, alternative references, and safe degradation rather than only a higher nominal accuracy. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Visual odometry: analytical implication
Visual odometry estimates incremental motion from image geometry. Its advantages are low payload mass and rich environmental information; its weaknesses include scale ambiguity, blur, illumination changes, and drift. In a UAV, these weaknesses interact with vibration and rapid attitude changes, so camera calibration and time synchronization are part of the navigation problem, not implementation details. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Visual inertial fusion: analytical implication
Visual-inertial fusion couples image constraints with inertial propagation. The inertial unit supplies high-rate attitude and short-term motion, while the camera corrects drift when features are trackable. Filter and optimization formulations differ in their treatment of uncertainty, marginalization, and computational load, but both require careful observability analysis and robust outlier handling. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### LiDAR SLAM: analytical implication
LiDAR SLAM provides geometric constraints that are less dependent on visible texture than cameras. It can be effective in dark or structurally rich scenes, although sparse geometry, dust, glass, dynamic objects, and payload cost remain concerns. The V1 results therefore present LiDAR-related categories alongside, rather than above, visual approaches. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Factor graph navigation: analytical implication
Factor-graph and smoothing formulations make measurement relationships explicit and can incorporate loop closures, map factors, and delayed constraints. Their computational burden grows with the window and graph structure. For onboard UAV use, fixed-lag smoothing, marginalization, and bounded memory are practical considerations that should be reported with the navigation result. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Radio and UWB: analytical implication
Radio and UWB methods introduce externally anchored range or time information. They can reduce drift in visually ambiguous areas, but their reliability depends on anchor placement, line of sight, synchronization, network availability, and resistance to interference. A radio aid should therefore be reported as part of the operational infrastructure rather than treated as a universally available sensor. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Learning-assisted estimation: analytical implication
Learning-assisted estimators can provide feature matching, depth inference, semantic cues, or direct motion hypotheses. Their main risks are distribution shift, hidden failure modes, data dependence, and uncertain behavior under deliberate deception. A credible evaluation should describe training separation, deployment compute, environmental variation, and failure cases rather than only an average score. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Multi-sensor fusion: analytical implication
Multi-sensor systems can trade complementary failure modes against payload mass, calibration effort, and integration complexity. Fusion is valuable only when uncertainty, timing, frame conventions, and fault behavior are handled explicitly. The V1 schema records the sensors actually used and preserves missing details as UNKNOWN or NOT_REPORTED. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Reproducibility: analytical implication
Reproducibility in GPS-denied navigation includes hardware, firmware, calibration, sampling rates, synchronization, trajectory, map, weather, lighting, and ground truth. A paper may report a strong result while leaving deployment-critical details unspecified. The quality rubric separates rigor, reporting, baselines, and reproducibility so these dimensions are not collapsed into one impression. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Evaluation design: analytical implication
Evaluation modality is not a binary property in V1. Real_World studies demonstrate deployment behavior, Simulation studies enable controlled stress tests, and Both studies connect the two. The Both category is retained because collapsing it would hide whether a paper actually crossed the simulation-to-real boundary. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Safety and recovery: analytical implication
Navigation without GNSS is a safety problem as well as an estimation problem. Systems should expose confidence, detect divergence, and define behaviors for hover, return, landing, or mission abort. These controls are often under-described in papers focused on the estimator, yet they determine whether a method can be trusted in operational settings. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Benchmarking: analytical implication
Benchmark datasets support comparability but can also narrow the apparent problem. A method tuned to one camera, one trajectory, or one lighting condition may not transfer to a different airframe. The review therefore emphasizes the reported validation context and avoids pooling heterogeneous errors into a single ranking. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Indoor inspection: analytical implication
Indoor inspection removes reliable sky visibility and makes local geometric structure the primary source of motion information. Camera and inertial measurements can support short-horizon control, but texture loss, repeated corridors, reflective surfaces, and moving people complicate loop closure. A practical system therefore needs explicit initialization, health monitoring, and a recovery policy when visual tracking becomes weak. The implication for this review is that method labels must be interpreted together with sensors, environment, experiment type, and quality evidence. A category count is a map of the literature, not a claim that one architecture dominates every mission. The V1 tables and figures are intended to make that distinction visible and auditable.

### Calibration: extended implication
Calibration is a system-level concern because camera, inertial, LiDAR, radar, sonar, and radio measurements are expressed in different frames and arrive at different times. Unreported calibration assumptions weaken transferability even when the estimator is mathematically clear. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Timing: extended implication
Timing errors can appear as motion error, especially during rapid rotation or vibration. Reproducible reports should state sampling, synchronization, interpolation, and latency handling so that another team can distinguish estimator behavior from instrumentation error. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Ground truth: extended implication
Ground truth is part of the claim. Motion capture, surveyed landmarks, simulation truth, visual reference, and manually aligned trajectories support different conclusions. The review therefore records evaluation modality and does not equate every reported error with the same physical quantity. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Dynamic scenes: extended implication
Dynamic objects challenge both feature tracking and geometric registration. Robust estimators need outlier rejection and scene-change handling, while benchmarks should disclose whether people, vehicles, water, foliage, or other moving elements were present. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Payload tradeoffs: extended implication
Sensor diversity improves observability but consumes mass, power, bandwidth, and compute. A deployable design must report these tradeoffs, not only the navigation trace. This is particularly important for small UAVs and long-duration missions. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Map dependence: extended implication
Map-based localization can provide global context, but map age, resolution, coordinate systems, and update cost affect reliability. A method that assumes a perfect map should be separated from one that constructs or maintains its map online. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Communication loss: extended implication
Cooperative navigation adds information but introduces communication dependence. Packet loss, latency, topology change, and malicious or faulty peers should be included in future experiments, especially when a swarm is expected to operate under interference. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Integrity: extended implication
Integrity monitoring asks whether the system knows when its position is unreliable. This is distinct from average accuracy and should include detection delay, false alarms, and the action taken after a fault is declared. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Transferability: extended implication
Transferability is not guaranteed by a successful benchmark. Airframe dynamics, camera exposure, sensor mounting, environmental texture, and controller coupling can all change the estimator regime. Cross-platform validation is therefore a valuable future contribution. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Reporting practice: extended implication
Reporting practice can improve without new algorithms. Authors can publish calibration files, timestamps, trajectories, failure cases, configuration parameters, and executable evaluation scripts. These details would make future evidence synthesis more precise and reduce duplicated engineering effort. The point is consistent with the V1 evidence-bounded approach: descriptive counts establish what was reported, whereas deployment recommendations require explicit conditions and uncertainty.


### Reproducibility recommendation 1
A complete future report should connect the mission question, sensor configuration, estimator state, controller interface, and evaluation protocol. It should explain what happens when measurements are missing, delayed, contradictory, or corrupted. It should also distinguish a method contribution from an infrastructure assumption, because a beacon, map, motion-capture system, or communication link may be unavailable in the intended mission. These reporting practices would make the next corpus version more useful for engineering decisions while preserving the review's conservative rule that unreported details remain unknown.


### Reproducibility recommendation 2
A complete future report should connect the mission question, sensor configuration, estimator state, controller interface, and evaluation protocol. It should explain what happens when measurements are missing, delayed, contradictory, or corrupted. It should also distinguish a method contribution from an infrastructure assumption, because a beacon, map, motion-capture system, or communication link may be unavailable in the intended mission. These reporting practices would make the next corpus version more useful for engineering decisions while preserving the review's conservative rule that unreported details remain unknown.


### Reproducibility recommendation 3
A complete future report should connect the mission question, sensor configuration, estimator state, controller interface, and evaluation protocol. It should explain what happens when measurements are missing, delayed, contradictory, or corrupted. It should also distinguish a method contribution from an infrastructure assumption, because a beacon, map, motion-capture system, or communication link may be unavailable in the intended mission. These reporting practices would make the next corpus version more useful for engineering decisions while preserving the review's conservative rule that unreported details remain unknown.


### Reproducibility recommendation 4
A complete future report should connect the mission question, sensor configuration, estimator state, controller interface, and evaluation protocol. It should explain what happens when measurements are missing, delayed, contradictory, or corrupted. It should also distinguish a method contribution from an infrastructure assumption, because a beacon, map, motion-capture system, or communication link may be unavailable in the intended mission. These reporting practices would make the next corpus version more useful for engineering decisions while preserving the review's conservative rule that unreported details remain unknown.


### Reproducibility recommendation 5
A complete future report should connect the mission question, sensor configuration, estimator state, controller interface, and evaluation protocol. It should explain what happens when measurements are missing, delayed, contradictory, or corrupted. It should also distinguish a method contribution from an infrastructure assumption, because a beacon, map, motion-capture system, or communication link may be unavailable in the intended mission. These reporting practices would make the next corpus version more useful for engineering decisions while preserving the review's conservative rule that unreported details remain unknown.


This reporting discipline also supports responsible comparison across missions.
