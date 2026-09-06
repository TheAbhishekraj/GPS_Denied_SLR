#!/usr/bin/env python3
"""
03_parse_screening.py
=====================
Parses AI JSON responses and creates included/excluded paper lists.

USAGE:
    python 03_parse_screening.py

INPUT:
    - 04_ai_responses/screening/resp_*.json

OUTPUT:
    - 02_data_processed/screened_included.csv
    - 02_data_processed/screened_excluded.csv
"""

import json
import pandas as pd
from pathlib import Path

RESPONSE_DIR = Path('E:/GPS_Denied_SLR/04_ai_responses/screening')
PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')

print("=" * 70)
print("GPS-DENIED SLR — STEP 3: PARSE SCREENING RESPONSES")
print("=" * 70)

if not RESPONSE_DIR.exists():
    print(f"\n❌ ERROR: Directory not found: {RESPONSE_DIR}")
    print("   Please run AI screening first and save responses.")
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
        # Extract JSON from markdown code blocks
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]

        data = json.loads(content.strip())
        data['source_file'] = resp_file.name
        records.append(data)
    except Exception as e:
        errors.append({'file': resp_file.name, 'error': str(e)})

print(f"Successfully parsed: {len(records)}")
print(f"Errors: {len(errors)}")

if errors:
    print(f"\n⚠ Warning: {len(errors)} files could not be parsed:")
    for err in errors[:5]:
        print(f"   - {err['file']}: {err['error']}")
    if len(errors) > 5:
        print(f"   ... and {len(errors) - 5} more")

df_results = pd.DataFrame(records)

# Decision distribution
print(f"\n{'=' * 70}")
print("SCREENING RESULTS")
print(f"{'=' * 70}")
print(f"\nDecision distribution:")
print(df_results['decision'].value_counts().to_string())

print(f"\nConfidence distribution:")
print(df_results['confidence'].value_counts().to_string())

# Save included and excluded
df_included = df_results[df_results['decision'] == 'INCLUDE'].copy()
df_excluded = df_results[df_results['decision'] == 'EXCLUDE'].copy()

df_included.to_csv(PROC_DIR / 'screened_included.csv', index=False)
df_excluded.to_csv(PROC_DIR / 'screened_excluded.csv', index=False)

print(f"\n{'=' * 70}")
print(f"✅ INCLUDED: {len(df_included)} papers → screened_included.csv")
print(f"✅ EXCLUDED: {len(df_excluded)} papers → screened_excluded.csv")
print(f"{'=' * 70}")

exclusion_rate = len(df_excluded) / len(df_results) * 100
print(f"\nExclusion rate: {exclusion_rate:.1f}%")

if exclusion_rate < 10:
    print("⚠ WARNING: Exclusion rate is very low (<10%).")
    print("   Your screening criteria may be too loose.")
    print("   Review excluded papers to verify.")
elif exclusion_rate > 60:
    print("⚠ WARNING: Exclusion rate is very high (>60%).")
    print("   Your screening criteria may be too strict.")
    print("   Review included papers to verify.")
else:
    print("✓ Exclusion rate looks reasonable (10–60%).")

print(f"\nNEXT STEP: Run 04_generate_extraction_prompts.py")
