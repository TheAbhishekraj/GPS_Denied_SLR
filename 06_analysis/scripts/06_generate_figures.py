#!/usr/bin/env python3
"""
06_generate_figures.py
======================
Generates all publication-ready figures from master database.

USAGE:
    python 06_generate_figures.py

INPUT:
    - 02_data_processed/extracted_master.csv

OUTPUT:
    - 06_analysis/output/figures/fig*.png (300 DPI)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from collections import Counter

# ============================================================
# CONFIGURATION
# ============================================================
PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
OUTPUT_DIR = Path('E:/GPS_Denied_SLR/06_analysis/output/figures')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(PROC_DIR / 'extracted_master.csv')

print("=" * 70)
print("GPS-DENIED SLR — STEP 6: GENERATE FIGURES")
print("=" * 70)
print(f"\nLoaded {len(df)} papers from extracted_master.csv")
print("Generating figures...\n")

# Set publication style
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 100

# Colorblind-friendly palette
colors = sns.color_palette("colorblind", 10)

# ============================================================
# FIGURE 1: Publication Trends Over Time
# ============================================================
print("[1/6] Figure 1: Publication trends...")

fig, ax = plt.subplots(figsize=(10, 6))

if 'year' in df.columns:
    year_counts = df['year'].value_counts().sort_index()
    # Filter to valid years
    year_counts = year_counts[(year_counts.index >= 2010) & (year_counts.index <= 2025)]

    bars = ax.bar(year_counts.index.astype(str), year_counts.values, 
                  color=colors[0], edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Year', fontweight='bold')
    ax.set_ylabel('Number of Publications', fontweight='bold')
    ax.set_title('GPS-Denied Localization Publications (2010–2025)', fontweight='bold')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                ha='center', va='bottom', fontsize=8)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig01_publication_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Saved: fig01_publication_trends.png")
else:
    print("    ⚠ Skipped: 'year' column not found")

# ============================================================
# FIGURE 2: Platform Distribution (Pie Chart)
# ============================================================
print("[2/6] Figure 2: Platform distribution...")

fig, ax = plt.subplots(figsize=(8, 8))

if 'platform' in df.columns:
    platform_counts = df['platform'].value_counts()

    wedges, texts, autotexts = ax.pie(
        platform_counts.values, 
        labels=platform_counts.index, 
        autopct='%1.1f%%', 
        colors=colors[:len(platform_counts)],
        startangle=90, 
        textprops={'fontsize': 10}
    )
    ax.set_title('Distribution by Platform', fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig02_platform_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Saved: fig02_platform_distribution.png")
else:
    print("    ⚠ Skipped: 'platform' column not found")

# ============================================================
# FIGURE 3: Environment Distribution (Horizontal Bar)
# ============================================================
print("[3/6] Figure 3: Environment distribution...")

fig, ax = plt.subplots(figsize=(10, 6))

if 'environment' in df.columns:
    env_counts = df['environment'].value_counts()

    ax.barh(env_counts.index, env_counts.values, 
            color=colors[1], edgecolor='black', linewidth=0.5)
    ax.set_xlabel('Number of Papers', fontweight='bold')
    ax.set_title('Evaluation Environment Distribution', fontweight='bold')
    ax.invert_yaxis()

    for i, v in enumerate(env_counts.values):
        ax.text(v + 1, i, str(v), va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig03_environment_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Saved: fig03_environment_distribution.png")
else:
    print("    ⚠ Skipped: 'environment' column not found")

# ============================================================
# FIGURE 4: Method Evolution Over Time (Stacked Bar)
# ============================================================
print("[4/6] Figure 4: Method evolution...")

fig, ax = plt.subplots(figsize=(12, 7))

if 'year' in df.columns and 'primary_method' in df.columns:
    df_valid = df[(df['year'] >= 2010) & (df['year'] <= 2025)]
    method_year = pd.crosstab(df_valid['year'], df_valid['primary_method'])

    method_year.plot(kind='bar', stacked=True, ax=ax, colormap='tab10', width=0.8)
    ax.set_xlabel('Year', fontweight='bold')
    ax.set_ylabel('Number of Papers', fontweight='bold')
    ax.set_title('Method Evolution Over Time', fontweight='bold')
    ax.legend(title='Method', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig04_method_evolution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Saved: fig04_method_evolution.png")
else:
    print("    ⚠ Skipped: required columns not found")

# ============================================================
# FIGURE 5: Sensor Usage Frequency
# ============================================================
print("[5/6] Figure 5: Sensor frequency...")

fig, ax = plt.subplots(figsize=(10, 8))

if 'sensors' in df.columns:
    all_sensors = []
    for sensors in df['sensors'].dropna():
        if isinstance(sensors, str):
            # Parse various formats
            sensor_list = [s.strip().strip("'\"[]") for s in sensors.replace(';', ',').split(',')]
            all_sensors.extend([s for s in sensor_list if s and s != 'NOT_IN_ABSTRACT'])

    if all_sensors:
        sensor_counts = Counter(all_sensors)
        top_sensors = dict(sensor_counts.most_common(15))

        ax.barh(list(top_sensors.keys()), list(top_sensors.values()), 
                color=colors[2], edgecolor='black', linewidth=0.5)
        ax.set_xlabel('Number of Papers', fontweight='bold')
        ax.set_title('Top-15 Sensor Usage Frequency', fontweight='bold')
        ax.invert_yaxis()

        for i, (k, v) in enumerate(top_sensors.items()):
            ax.text(v + 1, i, str(v), va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'fig05_sensor_frequency.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("    ✓ Saved: fig05_sensor_frequency.png")
    else:
        print("    ⚠ Skipped: no sensor data found")
else:
    print("    ⚠ Skipped: 'sensors' column not found")

# ============================================================
# FIGURE 6: Application Domain Distribution
# ============================================================
print("[6/6] Figure 6: Application domains...")

fig, ax = plt.subplots(figsize=(10, 6))

if 'application_domain' in df.columns:
    app_counts = df['application_domain'].value_counts()

    ax.bar(range(len(app_counts)), app_counts.values, 
           color=colors[3], edgecolor='black', linewidth=0.5)
    ax.set_xticks(range(len(app_counts)))
    ax.set_xticklabels(app_counts.index, rotation=45, ha='right')
    ax.set_ylabel('Number of Papers', fontweight='bold')
    ax.set_title('Application Domain Distribution', fontweight='bold')

    for i, v in enumerate(app_counts.values):
        ax.text(i, v + 1, str(v), ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig06_application_domains.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    ✓ Saved: fig06_application_domains.png")
else:
    print("    ⚠ Skipped: 'application_domain' column not found")

# ============================================================
# DONE
# ============================================================
print(f"\n{'=' * 70}")
print("ALL FIGURES GENERATED")
print(f"{'=' * 70}")
print(f"Output directory: {OUTPUT_DIR}")
print(f"\nFiles created:")
for f in sorted(OUTPUT_DIR.glob('fig*.png')):
    print(f"   ✓ {f.name}")
print(f"\nNEXT STEP: Review figures visually, then begin manuscript writing.")
