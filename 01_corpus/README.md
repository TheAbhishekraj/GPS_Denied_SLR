# 01_corpus — Corpus Architecture & Master Paper Extraction Template

This directory establishes the standardized extraction architecture and master template for individual study evidence synthesis in the systematic literature review:  
**"GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)"**.

---

## 1. Directory Structure

```text
01_corpus/
├── README.md                      # Directory manifest and usage guide (this file)
└── MASTER_PAPER_TEMPLATE.md       # Standardized 18-section paper extraction template
```

---

## 2. Template Specification

| File Link | Size | SHA256 Hash | Purpose |
| :--- | :---: | :--- | :--- |
| [`01_corpus/MASTER_PAPER_TEMPLATE.md`](file:///e:/GPS_Denied_SLR/01_corpus/MASTER_PAPER_TEMPLATE.md) | 6.2 KB | `F0F862BD8CFBB448F1A896B83A1A6BBF9F8B1526CA6ED2BDB4F339A41BBB75BD` | The normative 18-section markdown schema governing all per-paper extraction files in `_MANUAL/abhishek/per_paper/` and `03_extraction/per_paper/`. |

---

## 3. The 18 Standard Extraction Sections

Every extracted paper in the review adheres to the following structure:
1. Paper Identification & Metadata
2. Problem Statement & Operational Scenario
3. UAV Platform & System Hardware Configuration
4. Sensor Suite Architecture (Modalities, Rates, Specs)
5. Multi-Sensor Fusion Algorithm & Estimation Framework
6. GPS-Degraded / GPS-Denied Trigger & Transition Management
7. Environmental & Operational Conditions (Lighting, Degradation, Dynamics)
8. Experimental Validation & Benchmarking
9. Performance Metrics & Quantitative Outcomes
10. Failure Modes, Edge Cases & Limitations
11. Computational Complexity & Real-Time Feasibility
12. Quality Appraisal & Risk of Bias (0–10 Scale)
13. Verbatim Key Evidence Quotes & Citations
14. Alignment with Review Research Questions (Q1–Q8)
15. Key Takeaways & Conceptual Contribution
16. Synthesis Categorization & Taxonomy Placement
17. Reviewer Confidence Score & Extraction Audit Trail
18. Bibliographic Reference Entry
