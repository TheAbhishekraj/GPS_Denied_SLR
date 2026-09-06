"""
GPS-DENIED SLR DEDUPLICATION
Run after downloading IEEE Xplore and Scopus CSV files.
"""

import pandas as pd
import os
from datetime import datetime

# PATHS
BASE = r"E:\GPS_Denied_SLR"
IEEE = os.path.join(BASE, "01_data_raw", "ieee_xplore.csv")
SCOPUS = os.path.join(BASE, "01_data_raw", "scopus.csv")
OUTPUT = os.path.join(BASE, "02_data_processed", "deduplicated.csv")

def deduplicate():
    print("GPS-DENIED SLR DEDUPLICATION")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Check files
    if not os.path.exists(IEEE):
        print(f"ERROR: IEEE CSV not found at:\n{IEEE}")
        print("\nDownload from IEEE Xplore with search:")
        print('("GPS-denied" OR "GNSS-denied" OR "GPS denied" ...)')
        print('AND ("localization" OR "navigation" OR "SLAM" ...)')
        print('AND ("UAV" OR "drone" OR "robot" ...)')
        print("Filters: 2010-2025, English")
        return
    
    if not os.path.exists(SCOPUS):
        print(f"ERROR: Scopus CSV not found at:\n{SCOPUS}")
        print("\nDownload from Scopus with search:")
        print('TITLE-ABS-KEY(("GPS-denied" OR "GNSS-denied" ...)')
        print('AND ("localization" OR "navigation" OR "SLAM" ...)')
        print('AND ("UAV" OR "drone" OR "robot" ...))')
        print("Filters: 2010-2025, English")
        return
    
    print("Loading data...")
    ieee_df = pd.read_csv(IEEE, encoding='utf-8')
    scopus_df = pd.read_csv(SCOPUS, encoding='utf-8')
    
    print(f"IEEE: {len(ieee_df)} records")
    print(f"Scopus: {len(scopus_df)} records")
    
    # Add source
    ieee_df['source'] = 'IEEE'
    scopus_df['source'] = 'Scopus'
    
    # Combine
    combined = pd.concat([ieee_df, scopus_df], ignore_index=True)
    print(f"Total: {len(combined)} records")
    
    # Remove exact duplicates
    initial = len(combined)
    combined = combined.drop_duplicates()
    print(f"Exact duplicates removed: {initial - len(combined)}")
    
    # Clean DOI for deduplication
    if 'DOI' in combined.columns:
        combined['doi_clean'] = combined['DOI'].astype(str).str.lower().str.strip()
        combined['doi_clean'] = combined['doi_clean'].replace(['nan', '', 'none'], pd.NA)
        
        # Keep first record per DOI
        mask = combined['doi_clean'].notna()
        with_doi = combined[mask].drop_duplicates(subset='doi_clean', keep='first')
        without_doi = combined[~mask]
        
        combined = pd.concat([with_doi, without_doi], ignore_index=True)
        combined = combined.drop(columns=['doi_clean'])
        print(f"After DOI deduplication: {len(combined)} records")
    
    # Clean title for deduplication
    if 'Title' in combined.columns:
        combined['title_clean'] = combined['Title'].astype(str).str.lower().str.strip()
        
        # Simple exact title match
        combined = combined.drop_duplicates(subset='title_clean', keep='first')
        combined = combined.drop(columns=['title_clean'])
        print(f"After title deduplication: {len(combined)} records")
    
    # Final stats
    total_removed = (len(ieee_df) + len(scopus_df)) - len(combined)
    print(f"\nTotal duplicates removed: {total_removed}")
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    combined.to_csv(OUTPUT, index=False, encoding='utf-8')
    print(f"\nSaved to: {OUTPUT}")
    
    # Summary
    summary = f"""
GPS-DENIED SLR DEDUPLICATION SUMMARY
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Original records:
  IEEE Xplore: {len(ieee_df)}
  Scopus: {len(scopus_df)}
  Total: {len(ieee_df) + len(scopus_df)}

After deduplication:
  Unique papers: {len(combined)}
  Duplicates removed: {total_removed}
  Duplicate rate: {(total_removed/(len(ieee_df)+len(scopus_df))*100):.1f}%

Source distribution:
"""
    for source, count in combined['source'].value_counts().items():
        summary += f"  {source}: {count}\n"
    
    summary_path = os.path.join(BASE, "02_data_processed", "summary.txt")
    with open(summary_path, 'w') as f:
        f.write(summary)
    
    print(f"Summary: {summary_path}")
    print("\nDeduplication complete!")
    print(f"Next: Screen {len(combined)} papers in 04_ai_responses\\screening\\")

if __name__ == "__main__":
    deduplicate()