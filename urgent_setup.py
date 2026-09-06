"""
GPS-DENIED UAV SLR - 60 MINUTE ACTION PLAN
Current UTC: 04:47, September 6, 2026
"""

import os
from datetime import datetime

def create_action_plan():
    """Create 60-minute action plan for SLR"""
    project = r"E:\GPS_Denied_SLR"
    scope = os.path.join(project, "00_scope")
    
    # Create urgent action checklist
    checklist = f"""# 60-MINUTE ACTION PLAN - GPS-DENIED UAV SLR
# Start Time: 04:47 UTC, September 6, 2026
# Target Completion: 05:47 UTC

## MINUTES 0-15: IEEE XPLORE SEARCH
□ Open: ieeexplore.ieee.org
□ Institutional login
□ Advanced Search → Command Search
□ Paste this string:
  ("GPS denied" OR "GNSS denied" OR "without GPS" OR "indoor navigation") AND (localization OR navigation OR SLAM) AND (UAV OR drone OR robot)
□ Filters: 2010-2025, English
□ Export CSV → Save to: E:\\GPS_Denied_SLR\\01_data_raw\\ieee_xplore.csv
□ Record results: ______ papers

## MINUTES 16-30: SCOPUS SEARCH
□ Open: scopus.com
□ Institutional login
□ Advanced Search
□ Paste this string:
  TITLE-ABS-KEY(("GPS denied" OR "GNSS denied" OR "without GPS" OR "indoor navigation") AND (localization OR navigation OR SLAM) AND (UAV OR drone OR robot))
□ Filters: 2010-2025, English
□ Export CSV → Save to: E:\\GPS_Denied_SLR\\01_data_raw\\scopus.csv
□ Record results: ______ papers

## MINUTES 31-35: DEDUPLICATION
□ Open terminal in E:\\GPS_Denied_SLR
□ Run: python deduplicate.py
□ Check output in 02_data_processed folder
□ Record: ______ unique papers after deduplication

## MINUTES 36-45: SCREENING SETUP
□ Run: python setup_screening.py
□ Open screening_spreadsheet.xlsx
□ Review criteria in 00_scope folder
□ Prepare for screening

## MINUTES 46-60: BEGIN SCREENING
□ Start title/abstract screening
□ Screen first 50 papers
□ Mark: I (Include), E (Exclude), M (Maybe)
□ Document exclusion reasons
□ Save progress

## FILE CHECKLIST
□ E:\\GPS_Denied_SLR\\01_data_raw\\ieee_xplore.csv
□ E:\\GPS_Denied_SLR\\01_data_raw\\scopus.csv
□ E:\\GPS_Denied_SLR\\02_data_processed\\deduplicated.csv
□ E:\\GPS_Denied_SLR\\02_data_processed\\screening_spreadsheet.xlsx
□ E:\\GPS_Denied_SLR\\00_scope\\search_log.txt

## TROUBLESHOOTING
- Search fails → Use shorter string
- No results → Check year filter
- Export fails → Try smaller batches
- Script fails → Check Python installation

## COMPLETION STATUS
Start: 04:47 UTC
Current: ______ UTC
Progress: ______%
Estimated Finish: ______ UTC"""

    # Create search strings file
    search_strings = """# DATABASE SEARCH STRINGS

## IEEE XPLORE (copy-paste)
("GPS denied" OR "GNSS denied" OR "without GPS" OR "indoor navigation") AND (localization OR navigation OR SLAM) AND (UAV OR drone OR robot)

## SCOPUS (copy-paste)
TITLE-ABS-KEY(("GPS denied" OR "GNSS denied" OR "without GPS" OR "indoor navigation") AND (localization OR navigation OR SLAM) AND (UAV OR drone OR robot))

## FILTERS (apply to both)
- Year: 2010-2025
- Language: English
- Document Types: Journal Articles + Conference Papers

## EXPECTED RESULTS
IEEE Xplore: 200-500 papers
Scopus: 300-700 papers
After deduplication: 400-800 unique papers"""

    # Save files
    os.makedirs(scope, exist_ok=True)
    
    with open(os.path.join(scope, "60min_plan.txt"), "w", encoding="utf-8") as f:
        f.write(checklist)
    
    with open(os.path.join(scope, "search_strings_short.txt"), "w", encoding="utf-8") as f:
        f.write(search_strings)
    
    print("✓ Created: E:\\GPS_Denied_SLR\\00_scope\\60min_plan.txt")
    print("✓ Created: E:\\GPS_Denied_SLR\\00_scope\\search_strings_short.txt")

def create_setup_screening():
    """Create screening setup script"""
    script = '''"""
SETUP SCREENING - GPS-DENIED UAV SLR
Run after deduplicate.py
"""

import pandas as pd
import os

def main():
    project = r"E:\\GPS_Denied_SLR"
    processed = os.path.join(project, "02_data_processed")
    
    # Check for deduplicated file
    dedup_file = os.path.join(processed, "deduplicated.csv")
    if not os.path.exists(dedup_file):
        print("ERROR: Run deduplicate.py first")
        return
    
    # Load data
    df = pd.read_csv(dedup_file, encoding='utf-8')
    print(f"Loaded {len(df)} papers")
    
    # Add screening columns
    df['screening_status'] = 'Pending'
    df['include_exclude'] = ''
    df['exclusion_reason'] = ''
    df['screening_notes'] = ''
    
    # Save screening spreadsheet
    output = os.path.join(processed, "screening_spreadsheet.xlsx")
    df.to_excel(output, index=False)
    print(f"✓ Created: {output}")
    print(f"✓ Ready to screen {len(df)} papers")
    print("\\nOpen the spreadsheet and begin screening!")

if __name__ == "__main__":
    main()'''
    
    script_path = os.path.join(r"E:\GPS_Denied_SLR", "setup_screening.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
    
    print(f"✓ Created: {script_path}")
    return script_path

def main():
    print("GPS-DENIED UAV SLR - URGENT SETUP")
    print(f"Current UTC: {datetime.utcnow().strftime('%H:%M')}")
    print(f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    # Create action plan
    create_action_plan()
    
    # Create screening script
    create_setup_screening()
    
    print("\n" + "=" * 60)
    print("READY FOR 60-MINUTE WORK SESSION")
    print("=" * 60)
    print("\nIMMEDIATE ACTION REQUIRED:")
    print("1. Open: E:\\GPS_Denied_SLR\\00_scope\\60min_plan.txt")
    print("2. Follow step-by-step plan")
    print("3. Start with IEEE Xplore search")
    print("4. Complete within 60 minutes")
    
    print("\nESTIMATED TIMELINE:")
    print("04:47-05:02 UTC - IEEE Xplore search")
    print("05:02-05:17 UTC - Scopus search")
    print("05:17-05:22 UTC - Deduplication")
    print("05:22-05:32 UTC - Screening setup")
    print("05:32-05:47 UTC - Begin screening")
    
    print("\nGOAL: Complete database searches and start screening")
    print("Expected: 400-800 papers ready for screening")

if __name__ == "__main__":
    main()