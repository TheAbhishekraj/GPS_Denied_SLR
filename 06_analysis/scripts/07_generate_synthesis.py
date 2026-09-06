#!/usr/bin/env python3
"""
07_generate_synthesis.py
========================
Generates SLR synthesis tables and taxonomy matrices from extracted_master.csv.

USAGE:
    python 06_analysis/scripts/07_generate_synthesis.py
"""

import pandas as pd
from pathlib import Path

PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
df = pd.read_csv(PROC_DIR / 'extracted_master.csv')

print("=" * 70)
print("GPS-DENIED SLR — STEP 7: GENERATE SYNTHESIS & TAXONOMY MATRICES")
print("=" * 70)

# 1. Method vs Venue Tier Cross-tabulation
ct_method_tier = pd.crosstab(df['primary_method'], df['venue_tier'], margins=True)
ct_method_tier.to_csv(PROC_DIR / 'synthesis_method_by_venue_tier.csv')
print("  ✓ Saved: synthesis_method_by_venue_tier.csv")

# 2. Core Papers Summary
core_df = df[df['citation_tier'] == 'Core'][['paper_number', 'title', 'first_author', 'year', 'venue', 'primary_method', 'sensors', 'performance_metric', 'performance_value', 'performance_unit', 'key_contribution']]
core_df.to_csv(PROC_DIR / 'core_papers_summary.csv', index=False)
print(f"  ✓ Saved: core_papers_summary.csv ({len(core_df)} Core papers)")

# 3. Overall Taxonomy Summary
taxonomy = df.groupby(['primary_method', 'experiment_type']).size().unstack(fill_value=0)
taxonomy.to_csv(PROC_DIR / 'synthesis_taxonomy_matrix.csv')
print("  ✓ Saved: synthesis_taxonomy_matrix.csv")

print("\n✅ Synthesis artifacts generated successfully!")
