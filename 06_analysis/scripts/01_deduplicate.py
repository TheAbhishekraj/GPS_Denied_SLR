#!/usr/bin/env python3
"""
01_deduplicate.py
=================
Combines all database exports and removes duplicates.

USAGE:
    python 01_deduplicate.py

INPUT:
    - 01_data_raw/ieee_xplore.csv
    - 01_data_raw/scopus.csv
    - 01_data_raw/wos.csv (if available)
    - 01_data_raw/acm.csv (if available)

OUTPUT:
    - 02_data_processed/deduplicated.csv
    - Console report with counts
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CONFIGURATION — EDIT THESE PATHS IF NEEDED
# ============================================================
RAW_DIR = Path('E:/GPS_Denied_SLR/01_data_raw')
PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
PROC_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GPS-DENIED SLR — STEP 1: DEDUPLICATION")
print("=" * 70)

# ============================================================
# LOAD DATABASE EXPORTS
# ============================================================
print("\n[1/4] Loading database exports...")

dfs = []

# IEEE Xplore
ieee_path = RAW_DIR / 'ieee_xplore.csv'
if ieee_path.exists():
    df_ieee = pd.read_csv(ieee_path)
    df_ieee['source'] = 'IEEE_Xplore'
    dfs.append(df_ieee)
    print(f"    ✓ IEEE Xplore: {len(df_ieee)} records")
else:
    print(f"    ✗ IEEE Xplore: {ieee_path} not found")

# Scopus
scopus_path = RAW_DIR / 'scopus.csv'
if scopus_path.exists():
    df_scopus = pd.read_csv(scopus_path)
    df_scopus['source'] = 'Scopus'
    dfs.append(df_scopus)
    print(f"    ✓ Scopus: {len(df_scopus)} records")
else:
    print(f"    ✗ Scopus: {scopus_path} not found")

# Web of Science (try CSV first, then BibTeX)
wos_path = RAW_DIR / 'wos.csv'
if wos_path.exists():
    df_wos = pd.read_csv(wos_path)
    df_wos['source'] = 'Web_of_Science'
    dfs.append(df_wos)
    print(f"    ✓ Web of Science: {len(df_wos)} records")
else:
    print(f"    ℹ Web of Science: {wos_path} not found (optional)")

# ACM DL
acm_path = RAW_DIR / 'acm.csv'
if acm_path.exists():
    df_acm = pd.read_csv(acm_path)
    df_acm['source'] = 'ACM_DL'
    dfs.append(df_acm)
    print(f"    ✓ ACM DL: {len(df_acm)} records")
else:
    print(f"    ℹ ACM DL: {acm_path} not found (optional)")

if not dfs:
    print("\n❌ ERROR: No database files found!")
    print(f"   Expected files in: {RAW_DIR}")
    print("   Please export your database results first.")
    exit(1)

# Combine
df_all = pd.concat(dfs, ignore_index=True)
print(f"\n{'=' * 70}")
print(f"TOTAL before deduplication: {len(df_all)}")
print(f"{'=' * 70}")

# ============================================================
# STANDARDIZE COLUMN NAMES
# ============================================================
print("\n[2/4] Standardizing column names...")

column_map = {
    'Document Title': 'Title',
    'Title': 'Title',
    'Authors': 'Authors',
    'Author(s)': 'Authors',
    'Publication Year': 'Year',
    'Year': 'Year',
    'Abstract': 'Abstract',
    'DOI': 'DOI',
    'Author Keywords': 'Keywords',
    'Index Keywords': 'Keywords',
    'IEEE Terms': 'IEEE_Terms',
}

for old_name, new_name in column_map.items():
    if old_name in df_all.columns and new_name not in df_all.columns:
        df_all.rename(columns={old_name: new_name}, inplace=True)

# Ensure required columns exist
for col in ['Title', 'Authors', 'Year', 'Abstract', 'DOI']:
    if col not in df_all.columns:
        df_all[col] = 'NOT_AVAILABLE'
        print(f"    ⚠ Column '{col}' not found — filled with 'NOT_AVAILABLE'")

print("    ✓ Column standardization complete")

# ============================================================
# DEDUPLICATE BY DOI
# ============================================================
print("\n[3/4] Removing duplicates by DOI...")

df_all['DOI_clean'] = df_all['DOI'].astype(str).str.lower().str.strip()
df_all['DOI_clean'] = df_all['DOI_clean'].replace(['nan', 'not_available', ''], np.nan)

before = len(df_all)
df_dedup = df_all.drop_duplicates(subset=['DOI_clean'], keep='first')
doi_dups = before - len(df_dedup)

print(f"    Duplicates removed by DOI: {doi_dups}")

# ============================================================
# DEDUPLICATE BY TITLE
# ============================================================
print("\n[4/4] Removing duplicates by title similarity...")

df_dedup['Title_clean'] = df_dedup['Title'].astype(str).str.lower().str.replace(r'[^\w\s]', '', regex=True).str.strip()

before = len(df_dedup)
df_dedup = df_dedup.drop_duplicates(subset=['Title_clean'], keep='first')
title_dups = before - len(df_dedup)

print(f"    Duplicates removed by title: {title_dups}")

# Clean up temporary columns
df_dedup = df_dedup.drop(columns=['DOI_clean', 'Title_clean'], errors='ignore')

# ============================================================
# SAVE AND REPORT
# ============================================================
output_path = PROC_DIR / 'deduplicated.csv'
df_dedup.to_csv(output_path, index=False)

print(f"\n{'=' * 70}")
print(f"DEDUPLICATION COMPLETE")
print(f"{'=' * 70}")
print(f"Records before:     {len(df_all)}")
print(f"Records after:      {len(df_dedup)}")
print(f"Total removed:      {doi_dups + title_dups}")
print(f"Removal rate:       {(doi_dups + title_dups) / len(df_all) * 100:.1f}%")
print(f"\nSource distribution:")
print(df_dedup['source'].value_counts().to_string())
print(f"\n✅ Saved: {output_path}")
print(f"\nNEXT STEP: Run 02_generate_prompts.py")
