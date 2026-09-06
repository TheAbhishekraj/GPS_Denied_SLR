#!/usr/bin/env python3
"""
05_parse_extraction.py
======================
Parses extraction JSON responses into master database.

USAGE:
    python 05_parse_extraction.py

INPUT:
    - 04_ai_responses/extraction/resp_*.json

OUTPUT:
    - 02_data_processed/extracted_master.csv
    - Console summary statistics
"""

import json
import pandas as pd
from pathlib import Path

RESPONSE_DIR = Path('E:/GPS_Denied_SLR/04_ai_responses/extraction')
PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')

print("=" * 70)
print("GPS-DENIED SLR — STEP 5: PARSE EXTRACTION RESPONSES")
print("=" * 70)

if not RESPONSE_DIR.exists():
    print(f"\n❌ ERROR: Directory not found: {RESPONSE_DIR}")
    print("   Please run AI extraction first and save responses.")
    exit(1)

records = []
errors = []

resp_files = sorted(RESPONSE_DIR.glob('resp_*.json'))
print(f"\nFound {len(resp_files)} response files")
print("Parsing...\n")

for resp_file in resp_files:
    with open(resp_file, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]

        data = json.loads(content.strip())
        records.append(data)
    except Exception as e:
        errors.append({'file': resp_file.name, 'error': str(e)})

print(f"Successfully parsed: {len(records)}")
print(f"Errors: {len(errors)}")

if errors:
    print(f"\n⚠ Warning: {len(errors)} files could not be parsed")
    for err in errors[:3]:
        print(f"   - {err['file']}")

df_db = pd.json_normalize(records)

# Save master database
output_path = PROC_DIR / 'extracted_master.csv'
df_db.to_csv(output_path, index=False)

print(f"\n{'=' * 70}")
print(f"✅ MASTER DATABASE SAVED")
print(f"{'=' * 70}")
print(f"   Path: {output_path}")
print(f"   Papers: {len(df_db)}")

# Summary statistics
print(f"\n{'=' * 70}")
print("SUMMARY STATISTICS")
print(f"{'=' * 70}")

print(f"\n📊 Platform distribution:")
if 'platform' in df_db.columns:
    print(df_db['platform'].value_counts().head(10).to_string())

print(f"\n📊 Environment distribution:")
if 'environment' in df_db.columns:
    print(df_db['environment'].value_counts().head(10).to_string())

print(f"\n📊 Primary method distribution:")
if 'primary_method' in df_db.columns:
    print(df_db['primary_method'].value_counts().head(10).to_string())

print(f"\n📊 Citation tier distribution:")
if 'citation_tier' in df_db.columns:
    print(df_db['citation_tier'].value_counts().to_string())

print(f"\n📊 Extraction confidence:")
if 'extraction_confidence' in df_db.columns:
    print(df_db['extraction_confidence'].value_counts().to_string())

print(f"\n{'=' * 70}")
print("NEXT STEPS:")
print("  1. Manually verify 20 random extractions")
print("  2. Select 50-100 Core papers (citation_tier = 'Core')")
print("  3. Download full PDFs for Core papers only")
print("  4. Run 06_generate_figures.py")
print(f"{'=' * 70}")
