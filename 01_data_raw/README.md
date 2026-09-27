# 01_data_raw — Canonical Database Search Exports & Search Logs

This directory contains the immutable, primary **database search exports** and **search parameter logs** for the systematic literature review:  
**"GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)"**.

---

## 1. Directory Structure

```text
01_data_raw/
├── README.md                      # Directory manifest and guide (this file)
├── ieee_xplore_20260615.csv       # Primary export: 1,000 records from IEEE Xplore
├── scopus_20260615.csv            # Primary export: 1,000 records from Scopus
├── SEARCH_LOG.md                  # Comprehensive search log with query strings & timestamps
└── SEARCH_LOG_VERIFY.md           # Verification checklist confirming 2,000 canonical records
```

---

## 2. Primary Raw Data Catalog

These two CSV files represent **Tier-1 primary evidence** and are permanently read-only and immutable:

| File Link | Database | Search Date | Records | Size | SHA256 Hash |
| :--- | :--- | :---: | :---: | :---: | :--- |
| [`01_data_raw/ieee_xplore_20260615.csv`](file:///e:/GPS_Denied_SLR/01_data_raw/ieee_xplore_20260615.csv) | IEEE Xplore | 2026-06-15 | 1,000 | 2.24 MB | `FE374C9F2A405A0F0E07598979340AE971311B80BB20D8E121572D648CAA18F3` |
| [`01_data_raw/scopus_20260615.csv`](file:///e:/GPS_Denied_SLR/01_data_raw/scopus_20260615.csv) | Scopus | 2026-06-15 | 1,000 | 1.60 MB | `EF162F4F9525B6FC5CC617D1E3BADACD11F09B3E80FDFC488C4E37918BD524CB` |
| [`01_data_raw/SEARCH_LOG.md`](file:///e:/GPS_Denied_SLR/01_data_raw/SEARCH_LOG.md) | Search Log | 2026-06-15 | — | 2.5 KB | `7C3683515326A42C0A4F16FD254AB300F0E992003C966C54AFD834E11E859A24` |
| [`01_data_raw/SEARCH_LOG_VERIFY.md`](file:///e:/GPS_Denied_SLR/01_data_raw/SEARCH_LOG_VERIFY.md) | Verification | 2026-06-15 | — | 1.6 KB | `ED003EB3BE6D3E99F0CABBF0DF54CB0F8F59E463A827EDBDC80B294DA38E01CF` |

---

## 3. PRISMA 2020 Identification Totals

* Total records identified across both databases: **2,000**
* Duplicate records identified during Phase 2: **284**
* Unique deduplicated records entering Phase 3 screening: **1,716**
