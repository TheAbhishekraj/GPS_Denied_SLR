# SEARCH_LOG.md — Database Search Execution Log
# GPS_Denied_SLR | PRISMA 2020 | Author: Abhishek Raj

---

## Search Record 1: IEEE Xplore

| Field | Value |
|-------|-------|
| **Date** | 2026-06-15 |
| **Database** | IEEE Xplore (ieeexplore.ieee.org) |
| **Query** | `("GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied" OR "GPS-degraded" OR "GPS free" OR "GPS-free" OR "navigation without GPS") AND ("UAV" OR "unmanned aerial vehicle" OR "drone" OR "quadrotor" OR "multirotor" OR "fixed-wing" OR "rotary-wing") AND ("localization" OR "navigation" OR "SLAM" OR "odometry" OR "positioning")` |
| **Filters** | Year: 2010–2026; Content type: Journals + Conferences; Language: English |
| **Initial hits** | ~3,200 |
| **After filters** | ~2,800 |
| **Exported** | 1,000 (relevance-sorted export cap) |
| **Output file** | `01_data_raw/ieee_xplore_20260615.csv` |
| **File size** | 2,244,035 bytes |
| **Columns** | 28 columns — native IEEE Xplore export schema: Document Title, Authors, Author Affiliations, Publication Title, Date Added To Xplore, Publication Year, Volume, Issue, Start Page, End Page, Abstract, ISSN, ISBNs, DOI, Funding Information, PDF Link, Author Keywords, IEEE Terms, Mesh_Terms, Article Citation Count, Patent Citation Count, Reference Count, License, Online Date, Issue Date, Meeting Date, Publisher, Document Identifier |
| **source value** | IEEE |

---

## Search Record 2: Scopus

| Field | Value |
|-------|-------|
| **Date** | 2026-06-15 |
| **Database** | Scopus (scopus.com) |
| **Query** | `TITLE-ABS-KEY ( ( "GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied" OR "GPS-degraded" OR "GPS-free" OR "navigation without GPS" ) AND ( "UAV" OR "unmanned aerial vehicle" OR "drone" OR "quadrotor" OR "multirotor" ) AND ( "localization" OR "navigation" OR "SLAM" OR "odometry" OR "sensor fusion" OR "positioning" ) )` |
| **Filters** | Year: 2010–2026; Document type: Article, Conference Paper; Language: English |
| **Initial hits** | ~4,100 |
| **After filters** | ~3,800 |
| **Exported** | 1,000 (relevance-sorted export cap) |
| **Output file** | `01_data_raw/scopus_20260615.csv` |
| **File size** | 1,598,838 bytes |
| **Columns** | id, title, abstract, authors, year, doi, venue, source |
| **source value** | Scopus |

---

## Totals

| Metric | Value |
|--------|-------|
| Total raw records | 2,000 |
| IEEE Xplore | 1,000 |
| Scopus | 1,000 |
| Combined RAW canonical number | 2,000 ✓ |
