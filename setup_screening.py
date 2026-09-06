"""
SETUP SCREENING - GPS-DENIED UAV SLR
Run after deduplicate.py
"""

import pandas as pd
import os

def main():
    project = r"E:\GPS_Denied_SLR"
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
    print("\nOpen the spreadsheet and begin screening!")

if __name__ == "__main__":
    main()