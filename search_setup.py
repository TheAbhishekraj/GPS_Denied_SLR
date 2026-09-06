"""
GPS-DENIED UAV SLR - SEARCH SETUP
Date: 2026-09-06
Current Time: 04:44 UTC
"""

import os
from datetime import datetime

# Create essential search templates
def create_templates():
    project = r"E:\GPS_Denied_SLR"
    scope = os.path.join(project, "00_scope")
    
    # Create search strings file
    strings = """# SEARCH STRINGS - GPS-DENIED UAV SLR
IEEE Xplore:
("GPS denied" OR "GNSS denied" OR "without GPS" OR "indoor navigation") AND (localization OR navigation OR SLAM) AND (UAV OR drone OR robot)

Scopus:
TITLE-ABS-KEY(("GPS denied" OR "GNSS denied" OR "without GPS" OR "indoor navigation") AND (localization OR navigation OR SLAM) AND (UAV OR drone OR robot))

Filters (both):
- Year: 2010-2025
- Language: English
- Types: Journals + Conference Papers"""

    # Create action checklist
    checklist = """# ACTION CHECKLIST - NEXT 60 MINUTES

## IMMEDIATE TASKS (0-30 min)
### IEEE Xplore Search
□ Go to ieeexplore.ieee.org
□ Institutional login
□ Advanced Search → Command Search
□ Paste IEEE string
□ Apply filters: 2010-2025, English
□ Export CSV → Save to: E:\\GPS_Denied_SLR\\01_data_raw\\ieee_xplore.csv

### Scopus Search
□ Go to scopus.com
□ Institutional login
□ Advanced Search
□ Paste Scopus string
□ Apply filters: 2010-2025, English
□ Export CSV → Save to: E:\\GPS_Denied_SLR\\01_data_raw\\scopus.csv

## PROCESSING (31-35 min)
□ Run deduplication: python deduplicate.py
□ Check output in 02_data_processed folder

## SETUP (36-60 min)
□ Review templates in 00_scope folder
□ Set up screening spreadsheet
□ Plan next steps

## FILE CHECK
□ ieee_xplore.csv in 01_data_raw
□ scopus.csv in 01_data_raw
□ deduplicated.csv in 02_data_processed
□ summary.txt in 02_data_processed"""

    # Create log template
    log = f"""SEARCH LOG - {datetime.now().strftime('%Y-%m-%d %H:%M')}

IEEE Xplore:
Date: __________
Results: __________
File: E:\\GPS_Denied_SLR\\01_data_raw\\ieee_xplore.csv

Scopus:
Date: __________
Results: __________
File: E:\\GPS_Denied_SLR\\01_data_raw\\scopus.csv

Deduplication:
Run Date: __________
Initial Count: __________
Final Count: __________
Duplicates Removed: __________"""

    # Save files
    os.makedirs(scope, exist_ok=True)
    
    files = {
        "search_strings.txt": strings,
        "checklist.txt": checklist,
        "search_log.txt": log
    }
    
    for filename, content in files.items():
        path = os.path.join(scope, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Created: {path}")
    
    return True

def main():
    print("GPS-DENIED UAV SLR - SEARCH SETUP")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Time: {datetime.now().strftime('%H:%M')} UTC")
    print("=" * 50)
    
    create_templates()
    
    print("\n" + "=" * 50)
    print("NEXT STEPS")
    print("=" * 50)
    print("1. Open: E:\\GPS_Denied_SLR\\00_scope\\checklist.txt")
    print("2. Follow the 60-minute action plan")
    print("3. Record results in search_log.txt")
    print("\nEstimated completion: 05:44 UTC")

if __name__ == "__main__":
    main()