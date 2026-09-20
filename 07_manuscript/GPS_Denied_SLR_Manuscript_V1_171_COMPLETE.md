# Autonomous UAV Navigation and Localization in GPS/GNSS-Denied Environments:
# A Systematic Literature Review of Sensor-Fusion Approaches

## Version-1 Full-Text Synthesis

**Review window:** 2010–2026  
**Screened-included set:** 636 studies  
**Version-1 full-text corpus:** 171 studies (26.9%)  
**Analysis date:** September 2026  

## Abstract

GPS/GNSS denial caused by indoor occlusion, urban canyons, underground
operation, foliage, jamming, or spoofing creates a fundamental localization
problem for autonomous unmanned aerial vehicles (UAVs). This systematic
literature review examines sensor-fusion approaches for navigation and
localization under such conditions. The protocol defines a 2010–2026 review
window, a UAV-focused population, multi-sensor interventions, localization and
robustness outcomes, and indoor, urban, underground, forest, maritime, and
electronic-warfare contexts. The review workflow screened 636 studies as
included and completed machine-assisted full-text extraction for 171 locally available
papers. The Version-1 full-text corpus is therefore an intermediate subset,
not the final complete review population. Descriptively, the extracted studies
are concentrated in visual-inertial odometry, visual-LiDAR-inertial fusion,
LiDAR-inertial odometry/SLAM, and radio-based positioning. Evaluation modality
counts are 22 real-world-only, 78 simulation-only, and 71 both real-world and
simulation studies. Quality appraisal assigns 38 studies to Q-high, 84 to
Q-medium, and 49 to Q-low using a 10-point rubric. The evidence supports a
strong role for complementary sensing but does not support a pooled accuracy
ranking because metrics, units, datasets, and reporting completeness are
heterogeneous and many numeric values are not reported in the structured table.
The main conclusions are consequently descriptive and should be updated when
additional full texts become available.

**Keywords:** UAV navigation; GNSS-denied; GPS-denied; visual-inertial
odometry; LiDAR-inertial odometry; SLAM; sensor fusion; systematic review.

## 1. Introduction

Reliable position estimation is a prerequisite for autonomous UAV flight.
When GPS or another GNSS service is unavailable, degraded, jammed, spoofed,
or unreliable because of indoor or built-up environments, a vehicle must
construct its state estimate from onboard sensing and prior information.
Failure can produce drift, loss of scale or observability, collision risk,
mission failure, or unsafe return behavior. The problem is particularly
difficult in texture-poor interiors, urban canyons, tunnels, mines, forests,
smoke or dust, and adversarial electronic environments.

Sensor fusion is central because no single sensing modality is reliable in all
of these conditions. Cameras provide geometric and semantic information but
are sensitive to illumination, texture, motion blur, and occlusion. Inertial
measurements provide high-rate short-term motion information but drift when
not corrected. LiDAR can provide range geometry in low-light or texture-poor
scenes, although it adds payload, power, and computational requirements.
Radio, UWB, radar, sonar, and map-based information can add complementary
constraints but may require infrastructure, environmental assumptions, or
additional calibration.

The review protocol addresses a gap in systematic comparison of these
configurations for UAV navigation in GPS/GNSS-denied environments. It asks:

**RQ1.** What sensor-fusion configurations are most commonly used?  
**RQ2.** What performance metrics and accuracy levels are achieved in different
environments?  
**RQ3.** What algorithmic approaches and comparative advantages are reported?  
**RQ4.** What limitations and future research directions remain?

This manuscript reports a **Version-1 full-text synthesis**. The canonical
screened-included set contains 636 papers, but only 171 corresponding PDFs
were locally available for structured full-text extraction at the time of
analysis. The conclusions therefore characterize the available full-text
subset and must not be generalized without qualification to all 636 included
records.

## 2. Methods

### 2.1 Review design and protocol

The review follows the repository research protocol
(`00_scope/research_protocol.md`). The population is UAVs, drones, and closely
related aerial autonomous systems. The intervention is multi-sensor fusion,
including combinations of vision, LiDAR, IMU, radar, UWB, and related aiding
sensors. Comparisons include baselines and, where reported, GPS-assisted or
alternative navigation conditions. Outcomes include localization accuracy,
trajectory error, drift, robustness, computational efficiency, and mission
success. The context includes indoor, urban canyon, underground, forest,
maritime, jamming, and spoofing environments.

### 2.2 Search and eligibility

The protocol specifies IEEE Xplore, Scopus, Web of Science, and supplementary
Google Scholar searching. Its principal search concepts combine GPS/GNSS
denial or indoor/underground navigation with localization, navigation, or
SLAM and UAV, drone, or robot terms. The publication window is 2010–2026.

Included studies are English-language, peer-reviewed journal or conference
papers that address GPS/GNSS-denied navigation, focus on UAVs/drones/robots,
present a sensor-fusion approach, and provide experimental validation or
simulation results. The protocol excludes purely theoretical work without
validation, GPS-only navigation, terrestrial-only vehicles, single-sensor-only
studies, non-English publications, and work published before 2010.

### 2.3 Selection and Version-1 corpus construction

The repository records 636 screened-included studies. The full-text corpus was constructed by
matching locally available PDF stems in `05_papers_fulltext/` to study IDs in
`screened_included_v2.csv`. This produced 171 matched records, equivalent to
26.9% of the screened-included set. The denominator for full-text coverage is
therefore the 636 included studies.

### 2.4 Data extraction

The authoritative table is
`02_data_processed/extracted_master_v2.csv`. It contains study identity,
authors, year, DOI, venue, full-text status, page count, platform type,
sensors, primary method, method category, environment, experiment type,
real/simulation status, reported metrics, ATE/RMSE field, application domain,
multi-agent status, notes, four quality components, total QA score, QA tier,
and citation tier.

Extraction was machine-assisted from PDF text using the repository Phase-7
runner. The resulting labels are suitable for a reproducible descriptive
baseline but are not equivalent to independent human coding. A 20-paper
stratified validation sample was generated in
`08_docs/extraction_validation_sample_v1.csv`; its human-review fields remain
to be completed unless subsequently updated.

### 2.5 Quality appraisal

Each extracted paper receives four components:

| Component | Range | Interpretation |
|---|---:|---|
| Experimental rigor | 0–4 | Design clarity, validation, ground truth, and repeatability |
| Reporting completeness | 0–3 | Metrics, scale, hardware/data, and failure reporting |
| Baseline fairness | 0–2 | Baseline presence and matched comparison |
| Reproducibility | 0–1 | Code, data, or sufficiently detailed parameters |
| **Total** | **0–10** | Sum of the four components |

The tiers are Q-high (8–10), Q-medium (5–7), and Q-low (0–4). A quality tier
is a reporting and evidence-quality indicator; it is not proof that the
proposed method is superior.

### 2.6 Synthesis

The synthesis is descriptive. Frequencies and cross-tabulations are reported
for methods, sensors, environments, applications, experiment modality, and QA
tier. Environment and sensor fields are multi-valued, so their frequency sums
can exceed 171. Because the extracted performance values use heterogeneous
metrics, units, datasets, and evaluation protocols, no pooled meta-analysis
or universal method ranking is attempted.

## 3. Results

### 3.1 Selection and corpus profile

| Stage | Records |
|---|---:|
| Screened-included studies | 636 |
| Full-text PDFs locally available and matched | 171 |
| Full-text coverage of included set | 26.9% |

The Version-1 corpus is thus a convenience-of-access subset of the included
set. It is appropriate for an interim synthesis and pipeline validation, but
not for final prevalence estimates over all included studies.

### 3.2 Publication years and platforms

The 171 extracted records span 2013–2026. The largest annual group in the
current corpus is 2026 (36 records), followed by 2018 (24), 2019 (21), and
2022 and 2023 (19 each). These counts should be interpreted as the temporal
distribution of the currently available PDFs, not as the publication trend of
the full 636-paper set.

The platform field identifies 95 records as UAV and 76 as multi-platform.
Because the latter label can represent papers whose text mentions or evaluates
more than one platform, it should not be read as evidence that 76 studies are
non-UAV studies.

### 3.3 Sensor configurations

| Sensor field | Papers |
|---|---:|
| IMU | 170 |
| 3-D LiDAR | 93 |
| Stereo camera | 87 |
| mmWave radar | 48 |
| Monocular camera | 46 |
| UWB | 46 |
| Sonar | 34 |
| Optical flow | 30 |
| 2-D LiDAR | 25 |
| Thermal camera | 23 |
| Depth camera | 6 |

These are multi-label counts. IMU appears in nearly all extracted records,
while cameras and LiDAR are frequent complementary sources. The presence of a
sensor in a paper does not establish that it was the primary source of
accuracy or that it was evaluated under the same conditions as another paper.

### 3.4 Algorithmic taxonomy

| Primary method | Papers |
|---|---:|
| Visual-LiDAR-inertial fusion | 73 |
| Visual-inertial odometry | 61 |
| LiDAR-inertial odometry/SLAM | 19 |
| Radio-based positioning | 9 |
| Thermal-inertial odometry | 4 |
| Visual SLAM | 3 |
| Hybrid inertial fusion | 2 |

The largest categories combine complementary geometric and inertial
information. Visual-inertial methods offer compact, high-rate estimation but
remain vulnerable to visual degradation and accumulated drift. LiDAR-inertial
methods provide direct geometric constraints and can be advantageous in
texture-poor or low-light settings, at the cost of payload and processing
requirements. Radio-based methods can provide global or infrastructure-linked
constraints, but their effectiveness depends on anchor placement, propagation,
or environmental availability. These are trade-offs represented in the
current records, not a universal performance ordering.

### 3.5 Environments and applications

| Environment label | Papers |
|---|---:|
| Adversarial/EW | 168 |
| Urban | 154 |
| Indoor | 144 |
| Underground/tunnel | 136 |
| Forest/canopy | 89 |
| Maritime/water | 66 |
| Mixed/unstructured | 1 |

The unusually high multi-label counts show why environment categories must not
be added as mutually exclusive classes. They reflect the labels produced by
the current extraction process and require human validation before being used
for precise prevalence claims.

Application labels are inspection (107), mapping/surveying (49),
search-and-rescue (11), general navigation (3), and defense/tactical (1).
Inspection and mapping are therefore the most frequent application labels in
the Version-1 table.

### 3.6 Evaluation modality and reported metrics

| Evaluation modality | Papers |
|---|---:|
| Simulation only | 78 |
| Real-world only | 22 |
| Both real-world and simulation | 71 |

The current corpus contains a substantial simulation component: 78
simulation-only records and 71 records reporting both types of evaluation.
This supports a recurring concern about transfer from controlled simulation
to physical flight, especially under illumination change, occlusion,
vibration, communication loss, and degraded sensing.

The structured metric labels occur as follows: ATE/RMSE (170), success rate
(150), computational latency (114), relative drift percentage (110), and RMSE
(45). These labels are multi-label. Although ATE/RMSE is frequently marked as
a reported metric, the numeric `ate_rmse_m` field is `NOT_REPORTED` or
otherwise unavailable for most records. Accordingly, this review does not
claim a pooled meter-level accuracy or rank methods by accuracy.

### 3.7 Quality appraisal

| QA tier | Papers |
|---|---:|
| Q-high | 38 |
| Q-medium | 84 |
| Q-low | 49 |
| **Total** | **171** |

Citation tiers are Core (35), Important (87), and Peripheral (49). The
Core/Important working subset therefore contains 122 records. The QA
distribution indicates that most currently extracted papers report enough
information to receive Q-high or Q-medium status under the repository rubric,
but the scores remain machine-assisted and pending sample-level human review.

### 3.8 Multi-agent systems

The extracted field identifies 85 multi-agent and 86 single-agent records.
Multi-agent status should be interpreted cautiously because terminology such as
swarm, cooperative, or multi-robot can be detected from text without proving
that scalable cooperative localization was experimentally demonstrated. The
key unresolved evidence needs are communication reliability, synchronization,
relative-observation quality, network scale, and failure recovery.

## 4. Discussion

### 4.1 RQ1: Sensor-fusion configurations

The Version-1 corpus is dominated by combinations of inertial sensing with
vision and/or LiDAR. IMU appears in 170 of 171 records, while 3-D LiDAR and
stereo cameras appear in 93 and 87 records, respectively. This pattern is
consistent with complementary observability: inertial data provide short-term
motion propagation, cameras provide visual constraints, and LiDAR provides
range geometry. Radio/UWB, radar, sonar, optical flow, thermal cameras, and
depth cameras occur less often but represent targeted responses to specific
failure modes or operational constraints.

The frequency pattern answers which configurations are common, but not which
configuration is best. A valid comparative answer requires matched datasets,
common ground truth, comparable trajectories, and consistent reporting of
compute and environmental conditions, which are not uniformly available in
the current table.

### 4.2 RQ2: Metrics and accuracy

The records report a heterogeneous collection of ATE, RMSE, relative drift,
success, and latency indicators. The distribution shows substantial attention
to trajectory and operational metrics, but the structured numeric field is
mostly missing or not reported. Differences in units, sequences, trajectories,
flight speed, map scale, ground-truth source, and failure definitions prevent
direct numerical pooling. The defensible conclusion is therefore that the
field commonly evaluates trajectory error, drift, success, and computation,
not that any one method achieves a universal accuracy level.

### 4.3 RQ3: Algorithmic approaches and comparative advantages

Visual-LiDAR-inertial fusion is the largest extracted method category, followed
by visual-inertial odometry. LiDAR-inertial and radio-based approaches form
smaller but technically important groups. Visual-inertial systems offer
compactness and high-rate updates; LiDAR-inertial systems can strengthen
geometric observability where visual texture is poor; radio-based systems can
provide external constraints where infrastructure is available. The
comparative advantage of each approach is conditional on environment, payload,
latency, calibration, and failure mode. The present evidence does not justify
declaring a universal winner.

### 4.4 RQ4: Limitations and future directions

The most important limitations are incomplete full-text availability,
heterogeneous evaluation, limited numeric reporting, and the simulation-to-real
gap. Future studies should report common benchmark sequences, sensor
calibration, synchronization, ground-truth source, trajectory length, runtime,
power or payload constraints, failure cases, and matched baseline conditions.
Field evaluations should include deliberate degradation, such as lighting
change, motion blur, dust, foliage, occlusion, magnetic or radio disturbance,
and communication loss. Multi-agent studies should report network scale,
bandwidth, latency, packet loss, synchronization, and recovery behavior.

## 5. Limitations and Threats to Validity

First, only 171 of 636 included papers had local PDFs at the time of
extraction. Access and retrieval availability can bias the Version-1 corpus
toward recent, open, or institutionally accessible work. Second, the
extraction is machine-assisted. Sensor, environment, method, and metric labels
may contain false positives or omissions; the 20-paper validation sample must
be manually completed before the results are treated as final coded evidence.
Third, the studies use incompatible datasets, hardware, trajectories, metrics,
and definitions of success, so pooled effect sizes and universal rankings are
not appropriate. Fourth, multi-label fields produce counts greater than the
number of papers and cannot be interpreted as mutually exclusive distributions.
Finally, the 2026 portion of the corpus and the retrieval state are time
sensitive and should be regenerated when the search or full-text set changes.

## 6. Conclusion

This Version-1 full-text synthesis establishes a reproducible baseline for
reviewing GPS/GNSS-denied UAV navigation. The available 171 records show a
strong concentration of visual-inertial and visual-LiDAR-inertial approaches,
frequent use of IMU, camera, and LiDAR sensing, and substantial reliance on
simulation or mixed evaluation. They also show that the literature commonly
reports trajectory, drift, success, and computational metrics but does not
provide a sufficiently uniform numeric basis for pooled accuracy ranking.

The conclusions are intentionally limited to the currently available
full-text subset. When additional PDFs arrive, the Phase-7 extraction runner,
validation sample, core subset, figures, synthesis matrices, and manuscript
must be regenerated. The final review should incorporate the enlarged corpus
and completed human validation.

## 7. Data and Code Availability

The analysis tables and scripts are stored in the repository. The principal
files are:

- `02_data_processed/extracted_master_v2.csv`
- `02_data_processed/screened_included_v2.csv`
- `02_data_processed/screened_included_v2_fulltext.csv`
- `02_data_processed/core_papers_v1.csv`
- `06_analysis/scripts/16_execute_phase7_extraction.py`
- `06_analysis/scripts/06_generate_figures_v2.py`
- `06_analysis/scripts/07_generate_synthesis.py`
- `08_docs/extraction_validation_sample_v1.csv`

Local PDFs are not assumed to be redistributable and may be gitignored or
subject to publisher access restrictions. Study-level DOI metadata should be
resolved against the master CSV and checked before submission.

## 8. Figure Captions

**Figure 1. Publication trends.** Annual distribution of records in the
Version-1 full-text corpus; this is not the trend for all 636 included records.

**Figure 2. Platform distribution.** Extracted platform labels, including
multi-platform records.

**Figure 3. Environment distribution.** Multi-label environment frequencies;
categories are not mutually exclusive.

**Figure 4. Method evolution.** Distribution of extracted primary methods by
publication year in the available full-text corpus.

**Figure 5. Sensor frequency.** Multi-label sensor frequencies, showing the
co-occurrence of inertial, camera, LiDAR, radio, radar, sonar, and related
modalities.

**Figure 6. Application domains.** Extracted application-domain labels.

**Figure 7. PRISMA-style flow.** Review-record counts from raw identification
through deduplication, inclusion, and Version-1 full-text extraction.

**Figure 8. Method-environment heatmap.** Descriptive co-occurrence of primary
method categories and environment labels.

**Figure 9. Research-maturity radar.** Descriptive quality and evaluation
dimensions for the available full-text corpus; not a causal or predictive
score.

## 9. Conflicts of Interest and Funding

No conflict-of-interest or funding information was supplied in the repository
materials used for this Version-1 synthesis. These statements require author
confirmation before submission.

## 10. References

The following verified methodological and benchmark references support the
review method and representative navigation baselines. Included-study
metadata remain in the authoritative extraction CSV.

1. M. J. Page et al., “The PRISMA 2020 statement: An updated guideline for
   reporting systematic reviews,” *BMJ*, vol. 372, p. n71, 2021,
   doi: 10.1136/bmj.n71.
2. M. L. Rethlefsen et al., “PRISMA-S: An extension to the PRISMA statement
   for reporting literature searches in systematic reviews,” *Syst. Rev.*,
   vol. 10, no. 1, p. 39, 2021.
3. C. Campos et al., “ORB-SLAM3: An accurate open-source library for visual,
   visual-inertial, and multimap SLAM,” *IEEE Trans. Robot.*, vol. 37,
   no. 6, pp. 1874–1890, 2021, doi: 10.1109/TRO.2021.3075644.
4. T. Qin, P. Li, and S. Shen, “VINS-Mono: A robust and versatile monocular
   visual-inertial state estimator,” *IEEE Trans. Robot.*, vol. 34, no. 4,
   pp. 1004–1020, 2018, doi: 10.1109/TRO.2018.2853729.
5. J. Zhang and S. Singh, “LOAM: Lidar odometry and mapping in real-time,”
   *Robotics: Science and Systems*, 2014, doi: 10.15607/RSS.2014.X.007.
6. W. Xu et al., “FAST-LIO2: Fast direct lidar-inertial odometry,”
   *IEEE Trans. Robot.*, vol. 38, no. 4, pp. 2053–2073, 2022,
   doi: 10.1109/TRO.2022.3141876.
7. T. Shan et al., “LIO-SAM: Tightly-coupled lidar inertial odometry via
   smoothing and mapping,” in *Proc. IEEE/RSJ IROS*, 2020, pp. 5135–5142,
   doi: 10.1109/IROS45743.2020.9341176.
8. M. Burri et al., “The EuRoC micro aerial vehicle datasets,” *Int. J.
   Robot. Res.*, vol. 35, no. 10, pp. 1157–1163, 2016,
   doi: 10.1177/0278364916652421.

## Appendix A. Reproducibility and Quality-Control Audit

| Check | Result |
|---|---|
| `extracted_master_v2.csv` row count = 171 | PASS |
| `screened_included_v2.csv` row count = 636 | PASS |
| Full-text subset row count = 171 | PASS |
| Full-text coverage = 171/636 = 26.9% | PASS |
| QA totals within 0–10 | PASS |
| QA tiers valid | PASS |
| QA counts = 38 / 84 / 49 | PASS |
| Experiment counts = 22 / 78 / 71 | PASS |
| Citation tiers = 35 / 87 / 49 | PASS |
| Core + Important = 122 | PASS |
| Human validation sample completed | REVIEW REQUIRED |
| Complete final-corpus claim justified | NO |

**Overall status: REVIEW REQUIRED.** The numerical Version-1 checks pass, but
human validation and additional full-text retrieval remain incomplete. The
manuscript is suitable as an intermediate synthesis and reproducibility
baseline, not as the final complete-corpus submission.
