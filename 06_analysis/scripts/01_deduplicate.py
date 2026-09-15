#!/usr/bin/env python3
"""
01_deduplicate.py
=================
Combines all database exports and removes duplicates reliably by standardizing
columns PER SOURCE prior to concatenation.

USAGE:
    python 01_deduplicate.py

INPUT:
    - 01_data_raw/ieee_xplore.csv
    - 01_data_raw/scopus.csv

OUTPUT:
    - 02_data_processed/deduplicated.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW_DIR = Path('E:/GPS_Denied_SLR/01_data_raw')
PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
PROC_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GPS-DENIED SLR — STEP 1: AUDITED DEDUPLICATION")
print("=" * 70)

dfs = []

# 1. IEEE Xplore
ieee_path = RAW_DIR / 'ieee_xplore.csv'
if ieee_path.exists():
    df_ieee = pd.read_csv(ieee_path)
    # Standardize columns before concat
    df_ieee = df_ieee.rename(columns={
        'Document Title': 'Title',
        'Publication Year': 'Year',
        'Publication Title': 'Venue',
        'Authors': 'Authors',
        'Abstract': 'Abstract',
        'DOI': 'DOI',
        'IEEE Terms': 'Keywords'
    })
    df_ieee['source'] = 'IEEE_Xplore'
    dfs.append(df_ieee)
    print(f"    ✓ IEEE Xplore: {len(df_ieee)} records loaded")

# 2. Scopus
scopus_path = RAW_DIR / 'scopus.csv'
if scopus_path.exists():
    df_scopus = pd.read_csv(scopus_path)
    # Standardize columns before concat
    df_scopus = df_scopus.rename(columns={
        'Title': 'Title',
        'Year': 'Year',
        'Source title': 'Venue',
        'Authors': 'Authors',
        'Abstract': 'Abstract',
        'DOI': 'DOI',
        'Index Keywords': 'Keywords'
    })
    df_scopus['source'] = 'Scopus'
    dfs.append(df_scopus)
    print(f"    ✓ Scopus: {len(df_scopus)} records loaded")

if not dfs:
    print("❌ ERROR: No raw database exports found!")
    exit(1)

df_all = pd.concat(dfs, ignore_index=True)
print(f"\nTOTAL raw records loaded: {len(df_all)}")

# Fill missing columns gracefully
for col in ['Title', 'Authors', 'Year', 'Abstract', 'DOI', 'Venue']:
    if col not in df_all.columns:
        df_all[col] = ''
    df_all[col] = df_all[col].fillna('').astype(str).str.strip()

# Create clean comparison keys
df_all['DOI_clean'] = df_all['DOI'].str.lower().str.strip()
df_all['DOI_clean'] = df_all['DOI_clean'].replace(['nan', 'not_available', '', 'none', 'null'], np.nan)

df_all['Title_clean'] = df_all['Title'].str.lower().str.replace(r'[^\w\s]', '', regex=True).str.strip()
df_all['Title_clean'] = df_all['Title_clean'].replace(['nan', 'not_available', '', 'none', 'null'], np.nan)

# Deduplicate Strategy:
# 1. Deduplicate by DOI where valid
has_doi = df_all[df_all['DOI_clean'].notna()].copy()
no_doi = df_all[df_all['DOI_clean'].isna()].copy()

dedup_doi = has_doi.drop_duplicates(subset=['DOI_clean'], keep='first')
df_stage1 = pd.concat([dedup_doi, no_doi], ignore_index=True)
doi_dups_removed = len(df_all) - len(df_stage1)

# 2. Deduplicate by Title_clean
df_final = df_stage1.drop_duplicates(subset=['Title_clean'], keep='first')
title_dups_removed = len(df_stage1) - len(df_final)

total_dups = doi_dups_removed + title_dups_removed

# Clean up temp columns
df_final = df_final.drop(columns=['DOI_clean', 'Title_clean'], errors='ignore')

# Save deduplicated output
output_path = PROC_DIR / 'deduplicated.csv'
df_final.to_csv(output_path, index=False)

print("\n" + "=" * 70)
print("DEDUPLICATION AUDIT RESULTS")
print("=" * 70)
print(f"Total raw input records:  {len(df_all)}")
print(f"Duplicates by DOI:        {doi_dups_removed}")
print(f"Duplicates by Title:      {title_dups_removed}")
print(f"Total duplicates removed: {total_dups} ({total_dups / len(df_all) * 100:.1f}%)")
print(f"TOTAL UNIQUE PAPERS:      {len(df_final)}")
print("\nSource breakdown after deduplication:")
print(df_final['source'].value_counts().to_string())
print(f"\n✅ Saved: {output_path}")

