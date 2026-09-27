# 03_extraction — Pipeline Extraction Mirror Directory

This directory serves as the **automated pipeline extraction mirror** for the systematic literature review:  
**"GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)"**.

---

## 1. Directory Structure

```text
03_extraction/
├── README.md                      # Directory manifest, schema specification, and pipeline guide (this file)
└── per_paper/                     # Per-paper individual markdown extractions
    ├── .gitkeep                   # Directory marker and synchronization note
    ├── QA_INDEX.md                # Quality appraisal scoring register
    └── REC_0001.md ... REC_1678.md# 288 individual paper extraction files
```

---

## 2. Governance & Synchronization with `_MANUAL/`

Per [`AGENTS.md`](file:///e:/GPS_Denied_SLR/AGENTS.md) and [`_PROJECT/MASTER_PROMPT_3.md`](file:///e:/GPS_Denied_SLR/_PROJECT/MASTER_PROMPT_3.md):
* **Primary Evidence Base:** [`_MANUAL/abhishek/per_paper/`](file:///e:/GPS_Denied_SLR/_MANUAL/abhishek/per_paper/) is the human-verified, frozen reference corpus (288 `REC_*.md` files hashed in [`FROZEN_MANIFEST_20260927.csv`](file:///e:/GPS_Denied_SLR/_MANUAL/abhishek/per_paper/FROZEN_MANIFEST_20260927.csv)).
* **Pipeline Mirror:** `03_extraction/per_paper/` mirrors the frozen manual corpus for ingestion by automated synthesis scripts (`06_analysis/scripts/`).
* **Synchronization Status (2026-09-27):** **100.0% synchronized.** All 288 `REC_*.md` files match their counterparts in `_MANUAL/abhishek/per_paper/` byte-for-byte with 0 cryptographic hash mismatches.

---

## 3. Extraction Corpus Denominator (279 vs. 288)

`03_extraction/per_paper/` holds exactly **288** `REC_*.md` files:
* **279 In-Corpus Papers:** Formally included in the synthesis corpus and represented as the 279 rows of [`02_data_processed/MASTER_EVIDENCE.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/MASTER_EVIDENCE.csv) and batches `BATCH_B01` to `BATCH_B28`.
* **9 Out-of-Corpus / Deferred Papers:**
  * 3 Screening-Excluded records extracted during preliminary evaluation (`REC_0053`, `REC_0693`, `REC_0866`).
  * 6 Deferred Include records (`REC_0023`, `REC_0035`, `REC_0244`, `REC_0363`, `REC_1217`, `REC_1667`).
  * Denominator Rule: The synthesis evidence denominator is always **279**, never 288.

---

## 4. Standard 18-Section Extraction Schema

Each extraction file follows the PRISMA 2020 quote-anchored schema defined in [`08_docs/EXTRACTION_SCHEMA_v1.md`](file:///e:/GPS_Denied_SLR/08_docs/EXTRACTION_SCHEMA_v1.md):

1. **YAML Header:** Paper ID, title, authors, year, venue, DOI, page count, extractor, status.
2. **Section 1: Bibliographic Metadata:** Full citation, affiliations, printed page ranges.
3. **Section 2: Problem Statement:** Core GPS-denied challenge addressed with verbatim quote.
4. **Section 3: Motivation:** Methodological justification and limitations of prior art.
5. **Section 4: GPS-Denied Context:** Specific denial mechanism (indoor, subterranean, foliage, RF jamming, spoofing).
6. **Section 5: Operational Environment:** Physical setting taxonomy (Indoor, Urban Canyon, Forest, Cave/Tunnel, Adversarial).
7. **Section 6: Platform Details:** UAV airframe classification (Quadrotor, Hexarotor, Fixed-Wing, Hybrid VTOL, Flapping MAV).
8. **Section 7: Sensor Modalities:** Exteroceptive (Vision, LiDAR, Radar, UWB) and Proprioceptive (IMU, Barometer, Magnetometer) sensors.
9. **Section 8: Sensor Fusion Category:** Coupling architecture (Loosely Coupled, Tightly Coupled, Ultra-Tightly Coupled).
10. **Section 9: Algorithmic Approach:** Core navigation pipeline (VIO, LIO, SLAM, EKF/UKF filter, Factor Graph, Deep Learning).
11. **Section 10: Validation Approach:** Real-world flight hardware vs. high-fidelity simulation.
12. **Section 11: Dataset Details:** Public benchmark datasets used (e.g., EuRoC, KITTI, SubT) or proprietary flight logs.
13. **Section 12: Performance Metrics:** Absolute Trajectory Error (ATE RMSE), Relative Pose Error (RPE drift %), update latency (Hz).
14. **Section 13: Headline Results:** Quantified localization accuracy and primary empirical findings.
15. **Section 14: Baseline Comparisons:** Quantitative benchmarks against established baselines (e.g., VINS-Mono, ORB-SLAM3).
16. **Section 15: Ablation Studies:** Component-level ablation or failure mode characterization.
17. **Section 16: Limitations Identified:** Operational boundaries, failure cases, compute limits.
18. **Section 17: Future Research Directions:** Next-generation research opportunities identified by the authors.
19. **Section 18: Quality Appraisal Scoring:** 10-point appraisal breakdown across Dimensions A–D per [`00_scope/SCOPE.md`](file:///e:/GPS_Denied_SLR/00_scope/SCOPE.md).

---

## 5. Archive History (Excluded Duplicates)

On 2026-09-27, three extraction files corresponding to byte-identical duplicate PDFs excluded per [`02_data_processed/pdf_removal_log.csv`](file:///e:/GPS_Denied_SLR/02_data_processed/pdf_removal_log.csv) were safely relocated via `git mv` into [`_ARCHIVE/legacy_03_extraction/`](file:///e:/GPS_Denied_SLR/_ARCHIVE/legacy_03_extraction/):
* `REC_1582.md` (duplicate of `REC_0274`)
* `REC_1688.md` (duplicate of `REC_1715`)
* `REC_1715.md` (duplicate of `REC_1688`)
