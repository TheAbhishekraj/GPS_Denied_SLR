# GPS-DENIED NAVIGATION FOR UAVs SYSTEMATIC LITERATURE REVIEW
# Research Protocol Document
# Date: 2026-09-06
# Version: 1.0

## 1. RESEARCH CONTEXT

### 1.1 Problem Statement
GPS/GNSS-denied environments present significant challenges for UAV navigation. Indoor spaces, urban canyons, underground facilities, and jamming scenarios require alternative navigation solutions using sensor fusion approaches.

### 1.2 Research Gap
Existing literature reviews on GPS-denied navigation lack systematic analysis of multi-sensor fusion approaches specifically for UAV platforms, particularly comparing performance across different sensor combinations and environments.

## 2. RESEARCH OBJECTIVES

### 2.1 Primary Objective
To systematically review and synthesize current research on GPS-denied navigation technologies for UAVs using multi-sensor fusion approaches (2010-2026).

### 2.2 Specific Objectives
1. Identify and classify sensor fusion approaches for GPS-denied UAV navigation
2. Analyze performance metrics and accuracy across different environments
3. Compare algorithmic approaches (SLAM, VIO, LIO, etc.)
4. Identify current limitations and future research directions

## 3. PICOC FRAMEWORK

| Component | Description |
|-----------|-------------|
| **Population** | Unmanned Aerial Vehicles (UAVs), drones, autonomous robots |
| **Intervention** | Multi-sensor fusion approaches (Vision + LiDAR + IMU + Radar) |
| **Comparison** | GPS-based vs. GPS-denied navigation performance |
| **Outcomes** | Localization accuracy, robustness, computational efficiency |
| **Context** | Indoor, underground, urban canyon, jamming environments |

## 4. RESEARCH QUESTIONS

### RQ1: What sensor fusion configurations are most commonly used for GPS-denied UAV navigation?
### RQ2: What performance metrics and accuracy levels are achieved in different GPS-denied environments?
### RQ3: What are the main algorithmic approaches and their comparative advantages?
### RQ4: What are the current limitations and future research directions in this field?

## 5. INCLUSION AND EXCLUSION CRITERIA

### 5.1 Inclusion Criteria
- Published between 2010-2026
- English language
- Peer-reviewed journals or conference proceedings
- Addresses GPS/GNSS-denied navigation
- Focuses on UAVs/drones/robots
- Presents sensor fusion approach
- Includes experimental validation or simulation results

### 5.2 Exclusion Criteria
- Purely theoretical without validation
- Focuses only on GPS-based navigation
- Terrestrial vehicles only
- Single sensor approaches only
- Non-English publications
- Pre-2010 publications

## 6. SEARCH STRATEGY

### 6.1 Databases
1. IEEE Xplore
2. Scopus
3. Web of Science
4. Google Scholar (supplementary)

### 6.2 Search Strings
**IEEE Xplore:**
```
("GPS denied" OR "GNSS denied" OR "without GPS" OR "indoor navigation" OR "underground navigation") AND (localization OR navigation OR SLAM) AND (UAV OR drone OR robot)
```

**Scopus:**
```
TITLE-ABS-KEY(("GPS denied" OR "GNSS denied" OR "without GPS" OR "indoor navigation" OR "underground navigation") AND (localization OR navigation OR SLAM) AND (UAV OR drone OR robot))
```

### 6.3 Timeframe
2010-2026

## 7. METHODOLOGY

### 7.1 Study Selection Process
1. **Identification**: Database searches and export to CSV
2. **Screening**: Title/abstract screening using inclusion/exclusion criteria
3. **Eligibility**: Full-text screening of selected papers
4. **Inclusion**: Final selection for data extraction

### 7.2 Quality Assessment
Using 10-point checklist assessing:
- Research design clarity
- Experimental methodology
- Validation approach
- Results reporting
- Limitations discussion

### 7.3 Data Extraction
Structured extraction using predefined template covering:
- Bibliographic information
- Research context
- Technical approach
- Experimental setup
- Results and metrics
- Limitations and future work

## 8. DATA SYNTHESIS

### 8.1 Descriptive Analysis
- Publication trends (year, source, country)
- Sensor configuration frequencies
- Algorithm distribution
- Environment types

### 8.2 Thematic Analysis
- Sensor fusion approaches
- Performance characteristics
- Technical challenges
- Research gaps

## 9. TIMELINE

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| **Phase 1** | Week 1-2 | Protocol development, database searches |
| **Phase 2** | Week 3-4 | Screening and study selection |
| **Phase 3** | Week 5-6 | Data extraction and quality assessment |
| **Phase 4** | Week 7-8 | Data analysis and synthesis |
| **Phase 5** | Week 9-10 | Manuscript writing and revision |

## 10. ETHICAL CONSIDERATIONS

- Proper citation and acknowledgment of all sources
- No plagiarism - all sources properly referenced
- Transparent reporting of methods and findings
- Declaration of any conflicts of interest

## 11. DISSEMINATION PLAN

- Submission to relevant robotics/navigation journals
- Conference presentation
- Open access publication where possible
- Data and tools shared via GitHub

---
*Protocol approved: 2026-09-06*