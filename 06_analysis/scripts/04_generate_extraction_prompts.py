#!/usr/bin/env python3
"""
04_generate_extraction_prompts.py
=================================
Generates data extraction prompts for INCLUDED papers only by merging
screened_included.csv with metadata from deduplicated.csv.

USAGE:
    python 04_generate_extraction_prompts.py

INPUT:
    - 02_data_processed/screened_included.csv
    - 02_data_processed/deduplicated.csv

OUTPUT:
    - 03_prompts/extraction_prompts/extraction_XXXXX_*.txt (one per included paper)
"""

import pandas as pd
from pathlib import Path

PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
PROMPT_DIR = Path('E:/GPS_Denied_SLR/03_prompts/extraction_prompts')

if PROMPT_DIR.exists():
    import shutil
    shutil.rmtree(PROMPT_DIR)
PROMPT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GPS-DENIED SLR — STEP 4: GENERATE EXTRACTION PROMPTS")
print("=" * 70)

df_inc = pd.read_csv(PROC_DIR / 'screened_included.csv')
df_dedup = pd.read_csv(PROC_DIR / 'deduplicated.csv')

print(f"\nLoaded {len(df_inc)} INCLUDED papers out of {len(df_dedup)} total papers.")
print(f"Generating rich extraction prompts...\n")

count = 0
for _, inc_row in df_inc.iterrows():
    p_num = int(inc_row['paper_number'])
    idx = p_num - 1
    
    if idx < 0 or idx >= len(df_dedup):
        continue
        
    dedup_row = df_dedup.iloc[idx]
    
    # Extract robust metadata
    title = dedup_row.get('Document Title')
    if pd.isna(title) or not str(title).strip():
        title = dedup_row.get('Title', 'Unknown Title')
        
    abstract = dedup_row.get('Abstract')
    if pd.isna(abstract) or not str(abstract).strip():
        abstract = 'NOT_AVAILABLE'
        
    year = dedup_row.get('Publication Year')
    if pd.isna(year):
        year = dedup_row.get('Year', 'Unknown Year')
    if isinstance(year, float):
        year = int(year)
        
    authors = dedup_row.get('Authors')
    if pd.isna(authors) or not str(authors).strip():
        authors = dedup_row.get('Author(s) ID', 'Unknown Authors')
        
    doi = dedup_row.get('DOI')
    if pd.isna(doi):
        doi = ''
        
    venue = dedup_row.get('Publication Title')
    if pd.isna(venue):
        venue = dedup_row.get('Source title', 'NOT_IN_ABSTRACT')

    prompt = f"""SYSTEMATIC REVIEW DATA EXTRACTION — PAPER #{p_num}

TITLE: {title}
AUTHORS: {authors}
YEAR: {year}
VENUE: {venue}
DOI: {doi}
ABSTRACT: {abstract}

SCREENED METADATA HINTS:
- Platform Hint: {inc_row.get('platform', 'Unknown')}
- Environment Hint: {inc_row.get('environment', 'Unknown')}
- Sensors Detected: {inc_row.get('sensors_detected', 'Unknown')}
- Method Hint: {inc_row.get('method_hint', 'Unknown')}
- Screening Reason: {inc_row.get('reason', '')}

=== EXTRACTION INSTRUCTIONS ===
Extract technical data fields from the title and abstract above. If a field is NOT mentioned, write "NOT_IN_ABSTRACT". Do NOT hallucinate.

=== OUTPUT FORMAT ===
Return ONLY valid JSON:

{{
  "paper_number": {p_num},
  "title": "{str(title).replace('\"', '\\\"')}",
  "authors": "{str(authors).replace('\"', '\\\"')}",
  "year": {year if str(year).isdigit() else 2024},
  "venue": "{str(venue).replace('\"', '\\\"')}",
  "doi": "{doi}",

  "platform": {inc_row.get('platform', '["UAV"]')},
  "environment": {inc_row.get('environment', '["Mixed"]')},

  "sensors": {inc_row.get('sensors_detected', '["IMU", "Camera"]')},

  "primary_method": "ONE of: Filter_Based_VIO, Optimization_Based_VIO, Visual_SLAM, LiDAR_SLAM, Visual_LiDAR_Inertial_Fusion, Radio_Based_Positioning, Deep_Learning_Odometry, Multi_Agent_Collaborative_SLAM, Map_Based_Localization, Hybrid_Classical_Learning, Unknown",

  "secondary_methods": {inc_row.get('method_hint', '[]')},

  "performance_metric": "ATE_RMSE or RPE or Absolute_Error or Relative_Error or Other or NOT_IN_ABSTRACT",
  "performance_value": "numerical value or NOT_IN_ABSTRACT",
  "performance_unit": "m or cm or mm or % or NOT_IN_ABSTRACT",
  "dataset_used": "EuRoC or KITTI or UZH_FPV or TUM or Custom or Public or NOT_IN_ABSTRACT",
  "experiment_type": "Real_World or Simulation or Both or NOT_IN_ABSTRACT",

  "key_contribution": "{str(inc_row.get('reason', 'Novel contribution to GPS-denied navigation.')).replace('\"', '\\\"')}",
  "problem_solved": "Addressing localization and state estimation drift in GNSS-denied environments.",
  "limitation_stated": "NOT_IN_ABSTRACT",

  "application_domain": ["Inspection", "Mapping", "SAR", "Agriculture", "Driving", "General"],

  "citation_tier": "Core" if {str(inc_row.get('confidence')) == 'High'} else "Important",
  "extraction_confidence": "{inc_row.get('confidence', 'High')}",
  "needs_full_text_reading": false
}}
"""

    safe_title = "".join(c if c.isalnum() or c in '-_' else '_' for c in str(title)[:40])
    filename = f"extraction_{p_num:05d}_{safe_title}.txt"

    with open(PROMPT_DIR / filename, 'w', encoding='utf-8') as f:
        f.write(prompt)

    count += 1
    if count % 50 == 0 or count == len(df_inc):
        print(f"  Generated {count}/{len(df_inc)} prompts...")

print(f"\n✅ Generated {count} rich extraction prompts in:")
print(f"   {PROMPT_DIR}")
print(f"\nNEXT STEP: Run AI Data Extraction to populate master database.")

