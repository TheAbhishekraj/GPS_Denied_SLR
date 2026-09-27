# SEARCH_STRINGS.md — Database Query Documentation
# GPS_Denied_SLR | PRISMA 2020 | Author: Abhishek Raj

---

## IEEE Xplore Search

**Run Date:** 2026-06-15  
**Database:** IEEE Xplore (https://ieeexplore.ieee.org)  
**Result Count:** 1,000 records exported  
**Export Format:** CSV  
**Filters Applied:** Publication year: 2010–2026; Content type: Journals + Conferences; Access type: All  

**Exact Query String:**
```
("GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied" OR "GPS-degraded" OR "GPS free" OR "GPS-free" OR "navigation without GPS") AND ("UAV" OR "unmanned aerial vehicle" OR "drone" OR "quadrotor" OR "multirotor" OR "fixed-wing" OR "rotary-wing") AND ("localization" OR "navigation" OR "SLAM" OR "odometry" OR "positioning")
```

---

## Scopus Search

**Run Date:** 2026-06-15  
**Database:** Scopus (https://www.scopus.com)  
**Result Count:** 1,000 records exported  
**Export Format:** CSV  
**Filters Applied:** Publication year: 2010–2026; Document type: Article, Conference Paper; Language: English  

**Exact Query String:**
```
TITLE-ABS-KEY ( ( "GPS-denied" OR "GNSS-denied" OR "GPS denied" OR "GNSS denied" OR "GPS-degraded" OR "GPS-free" OR "navigation without GPS" ) AND ( "UAV" OR "unmanned aerial vehicle" OR "drone" OR "quadrotor" OR "multirotor" ) AND ( "localization" OR "navigation" OR "SLAM" OR "odometry" OR "sensor fusion" OR "positioning" ) )
```

---

## Search Log Summary

| Parameter | IEEE Xplore | Scopus |
|-----------|-------------|--------|
| Run date | 2026-06-15 | 2026-06-15 |
| Initial results | ~3,200 | ~4,100 |
| After year filter (2010–2026) | ~2,800 | ~3,800 |
| After document-type filter | 1,000 (exported cap) | 1,000 (exported cap) |
| Exported to CSV | `01_data_raw/ieee_xplore_raw.csv` | `01_data_raw/scopus_raw.csv` |

---

## Notes

- Both databases were searched on the same date (2026-06-15) to ensure temporal consistency.
- IEEE Xplore and Scopus both cap bulk exports at 2,000 records; 1,000 records were retrieved per database using relevance-sorted export.
- Records were exported with fields: title, abstract, authors, year, DOI, venue, source.
