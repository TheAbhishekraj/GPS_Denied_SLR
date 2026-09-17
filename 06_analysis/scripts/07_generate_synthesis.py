#!/usr/bin/env python3
"""
07_generate_synthesis.py
========================
Generates SLR synthesis tables and taxonomy matrices from extracted_master_v2.csv.

USAGE:
    python 06_analysis/scripts/07_generate_synthesis.py
"""

import sys
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
df = pd.read_csv(PROC_DIR / 'extracted_master_v2.csv')
df = df.rename(columns={
    'sensor_list': 'sensors',
})
df['venue_tier'] = df['citation_tier']
df['first_author'] = df['authors'].fillna('UNKNOWN').str.split(';').str[0]
df['paper_number'] = df['id']
df['performance_metric'] = df['metrics_reported']
df['performance_value'] = df['ate_rmse_m']
df['performance_unit'] = 'mixed_or_not_reported'
df['key_contribution'] = df['notes']

print("=" * 70)
print("GPS-DENIED SLR — STEP 7: GENERATE SYNTHESIS & TAXONOMY MATRICES")
print("=" * 70)

# 1. Method vs Venue Tier Cross-tabulation
ct_method_tier = pd.crosstab(df['primary_method'], df['venue_tier'], margins=True)
ct_method_tier.to_csv(PROC_DIR / 'synthesis_method_by_venue_tier.csv')
print("  ✓ Saved: synthesis_method_by_venue_tier.csv")

# 2. Core Papers Summary
core_df = df[df['citation_tier'].isin(['Core', 'Important'])][['paper_number', 'title', 'first_author', 'year', 'venue', 'primary_method', 'sensors', 'performance_metric', 'performance_value', 'performance_unit', 'key_contribution']]
core_df.to_csv(PROC_DIR / 'core_papers_summary.csv', index=False)
print(f"  ✓ Saved: core_papers_summary.csv ({len(core_df)} Core/Important papers)")

# 3. Overall Taxonomy Summary
taxonomy = df.groupby(['primary_method', 'experiment_type']).size().unstack(fill_value=0)
taxonomy.to_csv(PROC_DIR / 'synthesis_taxonomy_matrix.csv')
print("  ✓ Saved: synthesis_taxonomy_matrix.csv")

print("\n✅ Synthesis artifacts generated successfully!")
