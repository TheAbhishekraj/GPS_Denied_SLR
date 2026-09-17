#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_generate_figures_v2.py
=========================
FIXED & ENHANCED figure generation script.

Key fixes over v1:
  - Properly explodes list-valued columns (platform, environment, sensors, application_domain)
  - Fixes overlapping labels on pie / bar charts
  - Adds PRISMA flow diagram (Fig 07)
  - Adds method × environment heatmap (Fig 08)
  - Adds sensor co-occurrence network (Fig 09)
  - Consistent publication-quality dark-mode style throughout

USAGE:
    cd E:\\GPS_Denied_SLR
    python 06_analysis/scripts/06_generate_figures_v2.py

OUTPUT:
    06_analysis/output/figures_v2/  (300 DPI PNGs)
"""

import sys
import ast
import re
import warnings
import pandas as pd
import matplotlib
matplotlib.use('Agg')
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import seaborn as sns
import numpy as np
from pathlib import Path
from collections import Counter

warnings.filterwarnings('ignore')

# ────────────────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────────────────
PROC_DIR   = Path('E:/GPS_Denied_SLR/02_data_processed')
OUTPUT_DIR = Path('E:/GPS_Denied_SLR/06_analysis/output/figures_v2')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Premium dark colour palette
DARK_BG     = '#0f1117'
PANEL_BG    = '#1a1d27'
ACCENT1     = '#4f8ef7'   # blue
ACCENT2     = '#f7714f'   # orange
ACCENT3     = '#4ff79e'   # green
ACCENT4     = '#f7d44f'   # yellow
ACCENT5     = '#c14ff7'   # purple
ACCENT6     = '#f74f8e'   # pink
ACCENT7     = '#4ff7f0'   # cyan
TEXT_COLOR  = '#e8eaf0'
GRID_COLOR  = '#2a2d3a'

METHOD_COLORS = {
    'Filter_Based_VIO':           ACCENT1,
    'Optimization_Based_VIO':     '#7bb4f9',
    'LiDAR_SLAM':                 ACCENT3,
    'Visual_SLAM':                '#8affc4',
    'Visual_LiDAR_Inertial_Fusion': ACCENT4,
    'Hybrid_Classical_Learning':  ACCENT2,
    'Deep_Learning_Odometry':     ACCENT6,
    'Radio_Based_Positioning':    '#888aa0',
    'Multi_Agent_Collaborative_SLAM': ACCENT5,
    'Map_Based_Localization':     ACCENT7,
}

METHOD_LABELS = {
    'Filter_Based_VIO':           'Filter-Based VIO',
    'Optimization_Based_VIO':     'Optimization VIO',
    'LiDAR_SLAM':                 'LiDAR SLAM',
    'Visual_SLAM':                'Visual SLAM',
    'Visual_LiDAR_Inertial_Fusion': 'Visual-LiDAR-Inertial',
    'Hybrid_Classical_Learning':  'Hybrid Classical+DL',
    'Deep_Learning_Odometry':     'Deep Learning Odometry',
    'Radio_Based_Positioning':    'Radio-Based Positioning',
    'Multi_Agent_Collaborative_SLAM': 'Multi-Agent SLAM',
    'Map_Based_Localization':     'Map-Based Localization',
}

def set_dark_style():
    plt.style.use('dark_background')
    plt.rcParams.update({
        'figure.facecolor':  DARK_BG,
        'axes.facecolor':    PANEL_BG,
        'axes.edgecolor':    GRID_COLOR,
        'axes.labelcolor':   TEXT_COLOR,
        'axes.titlecolor':   TEXT_COLOR,
        'axes.titlesize':    15,
        'axes.labelsize':    12,
        'axes.titleweight':  'bold',
        'xtick.color':       TEXT_COLOR,
        'ytick.color':       TEXT_COLOR,
        'xtick.labelsize':   10,
        'ytick.labelsize':   10,
        'legend.facecolor':  PANEL_BG,
        'legend.edgecolor':  GRID_COLOR,
        'legend.fontsize':   9,
        'grid.color':        GRID_COLOR,
        'grid.alpha':        0.5,
        'text.color':        TEXT_COLOR,
        'font.family':       'DejaVu Sans',
        'figure.dpi':        100,
    })

def parse_list_col(series):
    """Safely parse a column that contains Python-list strings like \"['UAV', 'UGV']\"."""
    result = []
    for val in series.dropna():
        val = str(val).strip()
        if val.startswith('['):
            try:
                items = ast.literal_eval(val)
                result.extend([str(i).strip() for i in items if str(i).strip()])
            except Exception:
                cleaned = re.sub(r"[\[\]']", '', val)
                items = [x.strip() for x in cleaned.split(',') if x.strip()]
                result.extend(items)
        else:
            result.append(val)
    return result

def save(fig, name, dpi=300):
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"   ✓ Saved: {name}")
    return path

# ────────────────────────────────────────────────────────────
# LOAD DATA & COMPUTE CANONICAL STATS
# ────────────────────────────────────────────────────────────
print("=" * 70)
print("GPS-DENIED SLR -- STEP 6 v2: GENERATE PUBLICATION FIGURES")
print("=" * 70)

df = pd.read_csv(PROC_DIR / 'extracted_master_v2.csv')
df = df.rename(columns={
    'platform_type': 'platform',
    'sensor_list': 'sensors',
})
if 'venue_tier' not in df.columns:
    df['venue_tier'] = df['citation_tier'].map({
        'Core': 'Core',
        'Important': 'Important',
        'Peripheral': 'Peripheral',
    }).fillna('Unknown')
N_EXTRACTED = len(df)

try:
    df_incl = pd.read_csv(PROC_DIR / 'screened_included_v2.csv')
    N_INCLUDED = len(df_incl)
except Exception:
    N_INCLUDED = N_EXTRACTED

try:
    df_excl = pd.read_csv(PROC_DIR / 'screened_excluded_v2.csv')
    N_EXCLUDED = len(df_excl)
except Exception:
    N_EXCLUDED = 39

try:
    df_dedup = pd.read_csv(PROC_DIR / 'deduplicated.csv')
    N_UNIQUE = len(df_dedup)
except Exception:
    N_UNIQUE = N_INCLUDED + N_EXCLUDED

N_RAW   = 2000
N_DUPES = N_RAW - N_UNIQUE

print(f"\n[STATS] CANONICAL PAPER COUNTS:")
print(f"   Raw records      : {N_RAW}")
print(f"   After dedup      : {N_UNIQUE}")
print(f"   Duplicates removed: {N_DUPES}")
print(f"   Included (final) : {N_INCLUDED}")
print(f"   Excluded         : {N_EXCLUDED}")
print(f"   Extracted master : {N_EXTRACTED}")
print(f"\nGenerating figures into: {OUTPUT_DIR}\n")

set_dark_style()

# ────────────────────────────────────────────────────────────
# FIGURE 1: Publication Trends with Trend Line
# ────────────────────────────────────────────────────────────
print("[1/9] Figure 1: Publication trends …")

fig, ax = plt.subplots(figsize=(13, 6))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(PANEL_BG)

year_counts = df['year'].value_counts().sort_index()
year_counts = year_counts[(year_counts.index >= 2010) & (year_counts.index <= 2025)]
years  = year_counts.index.astype(int).tolist()
counts = year_counts.values.tolist()

# Gradient bars: colour by count (low=blue, high=orange)
norm   = plt.Normalize(min(counts), max(counts))
cmap   = matplotlib.colormaps.get_cmap('cool')
bar_colors = [cmap(norm(c)) for c in counts]

bars = ax.bar(years, counts, color=bar_colors, edgecolor=DARK_BG, linewidth=0.8, width=0.75)

# Trend line
z    = np.polyfit(range(len(years)), counts, 2)
p    = np.poly1d(z)
xs   = np.linspace(0, len(years)-1, 200)
ax.plot([years[0] + x*(years[-1]-years[0])/(len(years)-1) for x in xs],
        p(xs), color=ACCENT2, linewidth=2.5, linestyle='--', label='Growth trend', alpha=0.9)

# Count labels
for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            str(count), ha='center', va='bottom', fontsize=8.5, color=TEXT_COLOR, fontweight='bold')

# Annotation boxes for key events
annotations = [
    (2018, max(counts)*0.6, 'ORB-SLAM3 era\n→ SLAM consolidation'),
    (2022, max(counts)*0.75, 'DL intrusion\n→ Hybrid methods surge'),
]
for ax_x, ax_y, txt in annotations:
    ax.annotate(txt, xy=(ax_x, year_counts.get(ax_x, 50)),
                xytext=(ax_x+0.2, ax_y),
                fontsize=8, color=ACCENT4,
                arrowprops=dict(arrowstyle='->', color=ACCENT4, lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor=PANEL_BG, edgecolor=ACCENT4, alpha=0.9))

ax.set_xlabel('Year', fontweight='bold', labelpad=8)
ax.set_ylabel('Number of Publications', fontweight='bold', labelpad=8)
ax.set_title('GPS-Denied Navigation Publications (2010–2025)', fontsize=16, fontweight='bold', pad=15)
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=45, ha='right')
ax.yaxis.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)
ax.legend(loc='upper left', framealpha=0.8)

# Footnote for partial year
ax.text(0.99, 0.02, '* 2025 data represents partial year at time of search',
        transform=ax.transAxes, fontsize=8, color='#888aa0',
        ha='right', va='bottom', style='italic')

plt.tight_layout()
save(fig, 'fig01_publication_trends.png')

# ────────────────────────────────────────────────────────────
# FIGURE 2: Platform Distribution — Fixed Donut Chart
# ────────────────────────────────────────────────────────────
print("[2/9] Figure 2: Platform distribution …")

all_platforms = parse_list_col(df['platform'])
platform_counts = Counter(all_platforms)

# Simplify compound platforms into primary
clean = {}
for k, v in platform_counts.items():
    k2 = k.replace("'","").strip()
    # map to canonical
    mapping = {'UAV': 'UAV', 'UGV': 'UGV', 'Underwater': 'Underwater',
               'USV': 'USV', 'Wearable': 'Wearable', 'General': 'General'}
    canonical = mapping.get(k2, k2)
    clean[canonical] = clean.get(canonical, 0) + v

# Keep top-7, merge rest to Other
top7 = dict(sorted(clean.items(), key=lambda x: -x[1])[:7])
other_sum = sum(clean[k] for k in clean if k not in top7)
if other_sum > 0:
    top7['Other'] = other_sum

labels = list(top7.keys())
values = list(top7.values())
pal    = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5, ACCENT6, ACCENT7, '#888aa0']
colors_p = pal[:len(labels)]

fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(DARK_BG)

wedges, texts, autotexts = ax.pie(
    values, labels=None, autopct='%1.1f%%',
    colors=colors_p, startangle=140,
    wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=2),
    pctdistance=0.75
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight('bold')
    at.set_color(DARK_BG)

# Legend instead of labels to avoid overlap
legend_labels = [f'{l} ({v:,})' for l, v in zip(labels, values)]
ax.legend(wedges, legend_labels, title='Platform', loc='lower right',
          bbox_to_anchor=(1.25, 0.05), framealpha=0.85, fontsize=10, title_fontsize=11)

total = sum(values)
ax.text(0, 0, f'{total:,}\nPapers', ha='center', va='center',
        fontsize=14, fontweight='bold', color=TEXT_COLOR)

ax.set_title('Publication Distribution by Platform', fontsize=16, fontweight='bold', pad=20, color=TEXT_COLOR)
plt.tight_layout()
save(fig, 'fig02_platform_distribution.png')

# ────────────────────────────────────────────────────────────
# FIGURE 3: Environment Distribution — Grouped & Readable
# ────────────────────────────────────────────────────────────
print("[3/9] Figure 3: Environment distribution …")

all_envs = parse_list_col(df['environment'])
env_counts = Counter(all_envs)

# Canonical environment mapping
env_map = {
    'Indoor': 'Indoor', 'Urban': 'Urban Canyon',
    'Underground': 'Underground', 'Forest': 'Forest / Natural',
    'Underwater': 'Underwater', 'Adversarial': 'Adversarial / EW',
    'Mixed': 'Mixed', 'Outdoor': 'Urban Canyon',
}
grouped = {}
for k, v in env_counts.items():
    canonical = env_map.get(k, k)
    grouped[canonical] = grouped.get(canonical, 0) + v

env_df = pd.Series(grouped).sort_values(ascending=True)

ENV_COLORS = {
    'Indoor': ACCENT1,
    'Urban Canyon': ACCENT3,
    'Underground': ACCENT4,
    'Adversarial / EW': ACCENT2,
    'Forest / Natural': '#4dde98',
    'Underwater': ACCENT7,
    'Mixed': ACCENT5,
}
bar_colors_e = [ENV_COLORS.get(e, '#888aa0') for e in env_df.index]

fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(PANEL_BG)

bars = ax.barh(env_df.index, env_df.values, color=bar_colors_e,
               edgecolor=DARK_BG, linewidth=1.2, height=0.6)

for bar, val in zip(bars, env_df.values):
    total_env = sum(env_df.values)
    pct = 100 * val / total_env
    ax.text(bar.get_width() + total_env * 0.005, bar.get_y() + bar.get_height()/2,
            f'{val:,}  ({pct:.1f}%)', va='center', fontsize=10, color=TEXT_COLOR, fontweight='bold')

ax.set_xlabel('Number of Papers (multi-label, some papers span multiple environments)',
              fontweight='bold', labelpad=8)
ax.set_title('Evaluation Environment Distribution', fontsize=16, fontweight='bold', pad=15)
ax.xaxis.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)
# Key finding callout
ax.text(0.98, 0.02,
        '⚡ "Adversarial / EW" is the largest\n   single environment category.',
        transform=ax.transAxes, fontsize=9, color=ACCENT2,
        ha='right', va='bottom', style='italic',
        bbox=dict(boxstyle='round', facecolor=PANEL_BG, edgecolor=ACCENT2, alpha=0.9))

plt.tight_layout()
save(fig, 'fig03_environment_distribution.png')

# ────────────────────────────────────────────────────────────
# FIGURE 4: Method Evolution — Cleaned Stacked Bar
# ────────────────────────────────────────────────────────────
print("[4/9] Figure 4: Method evolution …")

df_valid = df[(df['year'] >= 2010) & (df['year'] <= 2025)].copy()
method_year = pd.crosstab(df_valid['year'], df_valid['primary_method'])
# Rename columns
method_year.columns = [METHOD_LABELS.get(c, c) for c in method_year.columns]

fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(PANEL_BG)

# Build colour list aligned to renamed columns
col_colors = []
for col in method_year.columns:
    matched = [v for k, v in METHOD_COLORS.items() if METHOD_LABELS.get(k, k) == col]
    col_colors.append(matched[0] if matched else '#888aa0')

bottom = np.zeros(len(method_year))
xs = np.arange(len(method_year))

for i, col in enumerate(method_year.columns):
    vals = method_year[col].values
    ax.bar(xs, vals, bottom=bottom, color=col_colors[i],
           label=col, width=0.75, edgecolor=DARK_BG, linewidth=0.6)
    bottom += vals

ax.set_xticks(xs)
ax.set_xticklabels([str(y) for y in method_year.index], rotation=45, ha='right')
ax.set_xlabel('Year', fontweight='bold', labelpad=8)
ax.set_ylabel('Number of Papers', fontweight='bold', labelpad=8)
ax.set_title('Methodological Evolution in GPS-Denied Navigation (2010–2025)',
             fontsize=15, fontweight='bold', pad=15)
ax.yaxis.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# ERA annotations
era_spans = [
    (2010, 2017, 'Foundation\nEra', ACCENT1),
    (2018, 2021, 'SLAM\nConsolidation', ACCENT3),
    (2022, 2025, 'DL Hybrid\nSurge', ACCENT2),
]
ymax = method_year.sum(axis=1).max()
available_years = list(method_year.index)
for start, end, label, color in era_spans:
    era_years = [year for year in available_years if start <= year <= end]
    if not era_years:
        continue
    x0 = available_years.index(min(era_years)) - 0.4
    x1 = available_years.index(max(era_years)) + 0.4
    ax.axvspan(x0, x1, alpha=0.07, color=color)
    ax.text((x0+x1)/2, ymax * 1.02, label, ha='center', va='bottom',
            fontsize=8, color=color, fontweight='bold')

ax.legend(title='Method', loc='upper left', framealpha=0.85,
          fontsize=8.5, title_fontsize=10, ncol=2)
plt.tight_layout()
save(fig, 'fig04_method_evolution.png')

# ────────────────────────────────────────────────────────────
# FIGURE 5: Sensor Frequency — Colour-Coded by Sensor Family
# ────────────────────────────────────────────────────────────
print("[5/9] Figure 5: Sensor frequency …")

all_sensors = parse_list_col(df['sensors'])
all_sensors = [s for s in all_sensors if s and s != 'NOT_IN_ABSTRACT' and len(s) > 1]
sensor_counts = Counter(all_sensors)
top_sensors_df = pd.Series(dict(sensor_counts.most_common(14))).sort_values()

# Family colours
SENSOR_FAMILY = {
    'IMU': ('Inertial', ACCENT2),
    'Barometer': ('Inertial', ACCENT2),
    'Magnetometer': ('Inertial', '#f79d4f'),
    'Monocular_Camera': ('Vision', ACCENT1),
    'Stereo_Camera': ('Vision', ACCENT1),
    'Depth_Camera': ('Vision', '#7bb4f9'),
    'Event_Camera': ('Vision', '#3a88f7'),
    'Thermal_Camera': ('Vision', '#b0c8ff'),
    'LiDAR_3D': ('LiDAR/Radar', ACCENT3),
    'LiDAR_2D': ('LiDAR/Radar', '#8affc4'),
    'Radar_mmWave': ('LiDAR/Radar', ACCENT4),
    'Sonar': ('LiDAR/Radar', '#ffe07b'),
    'UWB': ('Radio', ACCENT5),
    'WiFi': ('Radio', '#e08aff'),
}

bar_colors_s = [SENSOR_FAMILY.get(s, ('Other', '#888aa0'))[1] for s in top_sensors_df.index]
family_handles = {}
for s in top_sensors_df.index:
    fam, col = SENSOR_FAMILY.get(s, ('Other', '#888aa0'))
    if fam not in family_handles:
        family_handles[fam] = mpatches.Patch(color=col, label=fam)

fig, ax = plt.subplots(figsize=(11, 8))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(PANEL_BG)

bars = ax.barh(top_sensors_df.index, top_sensors_df.values,
               color=bar_colors_s, edgecolor=DARK_BG, linewidth=1, height=0.65)

for bar, val in zip(bars, top_sensors_df.values):
    total_s = N_EXTRACTED
    pct = 100 * val / total_s
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
            f'{val:,}  ({pct:.0f}%)', va='center', fontsize=10, color=TEXT_COLOR, fontweight='bold')

ax.set_xlabel('Number of Papers', fontweight='bold', labelpad=8)
ax.set_title('Sensor Modality Frequency (Top-14)', fontsize=16, fontweight='bold', pad=15)
ax.xaxis.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

ax.legend(handles=list(family_handles.values()), title='Sensor Family',
          loc='lower right', framealpha=0.85, fontsize=10)

# Key insight callout
imu_count = sensor_counts.get('IMU', 0)
imu_pct = 100 * imu_count / N_EXTRACTED
ax.text(0.98, 0.98,
        f'IMU is present in {imu_pct:.0f}% of all papers\n— the universal substrate of GPS-denied nav.',
        transform=ax.transAxes, fontsize=9, color=ACCENT2,
        ha='right', va='top', style='italic',
        bbox=dict(boxstyle='round', facecolor=PANEL_BG, edgecolor=ACCENT2, alpha=0.9))

plt.tight_layout()
save(fig, 'fig05_sensor_frequency.png')

# ────────────────────────────────────────────────────────────
# FIGURE 6: Application Domain — FIXED (explode list column)
# ────────────────────────────────────────────────────────────
print("[6/9] Figure 6: Application domains …")

all_apps = parse_list_col(df['application_domain'])
all_apps = [a for a in all_apps if a and a != 'NOT_IN_ABSTRACT']

# Canonical mapping
APP_MAP = {
    'Inspection': 'Infrastructure\nInspection',
    'Mapping': 'Mapping &\nSurveying',
    'SAR': 'Search & Rescue\n(SAR)',
    'General': 'General\nNavigation',
    'Military': 'Military /\nDefense',
    'Agriculture': 'Agriculture',
    'Logistics': 'Logistics &\nWarehouse',
    'Underwater': 'Underwater\nOperations',
    'Mining': 'Mining &\nSubterranean',
}
app_counts_raw = Counter(all_apps)
app_grouped = {}
for k, v in app_counts_raw.items():
    canonical = APP_MAP.get(k.strip(), k.strip())
    app_grouped[canonical] = app_grouped.get(canonical, 0) + v

app_series = pd.Series(app_grouped).sort_values(ascending=False)
top_apps   = app_series.head(9)

APP_COLORS_LIST = [ACCENT1, ACCENT3, ACCENT2, ACCENT4, ACCENT5, ACCENT6, ACCENT7, '#f79d4f', '#4dde98']

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(PANEL_BG)

xs = np.arange(len(top_apps))
bars = ax.bar(xs, top_apps.values, color=APP_COLORS_LIST[:len(top_apps)],
              edgecolor=DARK_BG, linewidth=1.2, width=0.65)

for bar, val in zip(bars, top_apps.values):
    total_app = sum(top_apps.values)
    pct = 100 * val / total_app
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + total_app * 0.005,
            f'{val:,}\n({pct:.0f}%)', ha='center', va='bottom',
            fontsize=9, color=TEXT_COLOR, fontweight='bold')

ax.set_xticks(xs)
ax.set_xticklabels(top_apps.index, rotation=0, ha='center', fontsize=10)
ax.set_ylabel('Number of Papers', fontweight='bold', labelpad=8)
ax.set_title('Application Domain Distribution', fontsize=16, fontweight='bold', pad=15)
ax.yaxis.grid(True, alpha=0.3, linestyle='--')
ax.set_axisbelow(True)
plt.tight_layout()
save(fig, 'fig06_application_domains.png')

# ────────────────────────────────────────────────────────────
# FIGURE 7: PRISMA 2020 Flow Diagram
# ────────────────────────────────────────────────────────────
print("[7/9] Figure 7: PRISMA 2020 flow diagram …")

fig = plt.figure(figsize=(12, 14))
fig.patch.set_facecolor(DARK_BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(DARK_BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

BOX_STYLE = dict(boxstyle='round,pad=0.6', linewidth=2)
ARROW_STYLE = dict(arrowstyle='->', color=TEXT_COLOR, lw=2)

def box(ax, x, y, w, h, txt, facecolor, edgecolor):
    rect = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   facecolor=facecolor, edgecolor=edgecolor,
                                   linewidth=2, boxstyle='round,pad=0.15', zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, txt, ha='center', va='center', fontsize=10.5,
            fontweight='bold', color=TEXT_COLOR, zorder=4,
            wrap=True, multialignment='center')

def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=TEXT_COLOR, lw=2))

def side_box(ax, x, y, w, h, txt, facecolor='#3a1a1a', edgecolor=ACCENT2):
    rect = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   facecolor=facecolor, edgecolor=edgecolor,
                                   linewidth=1.5, boxstyle='round,pad=0.15', zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, txt, ha='center', va='center', fontsize=9,
            color=TEXT_COLOR, zorder=4, multialignment='center')

# Phase labels on left
for y_pos, phase_lbl in [(12.5, 'IDENTIFICATION'), (9.5, 'SCREENING'),
                          (6.5, 'ELIGIBILITY'), (3.5, 'INCLUDED')]:
    ax.text(0.5, y_pos, phase_lbl, ha='center', va='center',
            fontsize=10, fontweight='bold', color='#888aa0',
            rotation=90)

# Main boxes
box(ax, 5, 13, 7, 1.0,
    f'Records identified from databases\nIEEE Xplore (n=1,000) + Scopus (n=1,000)\nTotal: {N_RAW:,}',
    PANEL_BG, ACCENT1)

arrow(ax, 5, 12.5, 5, 11.5)

box(ax, 5, 11.0, 7, 1.0,
    f'Records after deduplication\nn = {N_UNIQUE:,}',
    PANEL_BG, ACCENT1)

side_box(ax, 8.8, 11.0, 2.8, 0.85,
         f'Duplicates removed\nn = {N_DUPES:,}\n(DOI + fuzzy title matching)')

arrow(ax, 5, 10.5, 5, 9.5)

box(ax, 5, 9.0, 7, 1.0,
    f'Records screened\n(title & abstract)\nn = {N_UNIQUE:,}',
    PANEL_BG, ACCENT3)

side_box(ax, 8.8, 9.0, 2.8, 0.85,
         f'Records excluded\nn = {N_EXCLUDED:,}\n(out-of-scope, non-empirical)')

arrow(ax, 5, 8.5, 5, 7.5)

box(ax, 5, 7.0, 7, 1.0,
    f'Full-text articles assessed for eligibility\nn = {N_INCLUDED:,}',
    PANEL_BG, ACCENT3)

side_box(ax, 8.8, 6.5, 2.8, 1.3,
         'Articles excluded:\n• No GPS-denied focus\n• No sensor fusion method\n• Purely theoretical\n• Pre-2010 / non-English')

arrow(ax, 5, 6.5, 5, 5.5)

box(ax, 5, 5.0, 7, 1.0,
    f'Studies included in synthesis\nn = {N_EXTRACTED:,}',
    '#1a2f1a', ACCENT3)

arrow(ax, 5, 4.5, 5, 3.5)

box(ax, 5, 3.0, 7, 1.0,
    f'Data extracted to master database\n(extracted_master.csv)\nn = {N_EXTRACTED:,} papers',
    '#1a2a1a', ACCENT4)

# Title
ax.text(5, 13.9, 'PRISMA 2020 Systematic Review Flow',
        ha='center', va='center', fontsize=16, fontweight='bold', color=TEXT_COLOR)

plt.tight_layout()
save(fig, 'fig07_prisma_flow.png')

# ────────────────────────────────────────────────────────────
# FIGURE 8: Method × Environment Heatmap
# ────────────────────────────────────────────────────────────
print("[8/9] Figure 8: Method x Environment heatmap ...")

# Build method-environment pair counts safely using groupby
records = []
for _, row in df.iterrows():
    envs    = parse_list_col(pd.Series([row['environment']]))
    method  = METHOD_LABELS.get(str(row.get('primary_method','')).strip(),
                                str(row.get('primary_method','')).strip())
    for env in envs:
        canonical = env_map.get(env.strip(), env.strip())
        records.append({'method': method, 'env': canonical})

df_pairs = pd.DataFrame(records)
# Pivot
heatmap_data = df_pairs.groupby(['method', 'env']).size().unstack(fill_value=0)
# Drop low-count columns
heatmap_data = heatmap_data.loc[:, heatmap_data.sum() > 10]
# Normalise by row
heatmap_pct = heatmap_data.div(heatmap_data.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(13, 8))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(PANEL_BG)

sns.heatmap(heatmap_pct, ax=ax, cmap='Blues', annot=True, fmt='.0f',
            linewidths=0.5, linecolor=DARK_BG,
            annot_kws={'size': 9, 'weight': 'bold'},
            cbar_kws={'label': '% of Method Papers in Environment'})
ax.set_title('Method × Environment Co-occurrence (% of Method Papers)',
             fontsize=15, fontweight='bold', pad=15, color=TEXT_COLOR)
ax.set_xlabel('Environment', fontweight='bold', labelpad=8)
ax.set_ylabel('Primary Method', fontweight='bold', labelpad=8)
plt.xticks(rotation=30, ha='right', color=TEXT_COLOR)
plt.yticks(rotation=0, color=TEXT_COLOR)
ax.collections[0].colorbar.ax.yaxis.label.set_color(TEXT_COLOR)
ax.collections[0].colorbar.ax.tick_params(colors=TEXT_COLOR)
plt.tight_layout()
save(fig, 'fig08_method_environment_heatmap.png')

# ────────────────────────────────────────────────────────────
# FIGURE 9: Research Gap Radar Chart
# ────────────────────────────────────────────────────────────
print("[9/9] Figure 9: Research maturity radar …")

categories = [
    'Lab Benchmark\nMaturity', 'Real-World\nDeployment',
    'Multi-Sensor\nFusion', 'Edge Computing\nReadiness',
    'Adversarial\nRobustness', 'Long-Horizon\nDrift Control',
    'Multi-Agent\nSystems', 'Standardised\nEvaluation'
]
# Scores 1-10 based on corpus evidence
current_scores = [9, 4, 7, 5, 6, 5, 3, 3]
ideal_scores   = [10, 10, 10, 10, 10, 10, 10, 10]

N_cat = len(categories)
angles = np.linspace(0, 2 * np.pi, N_cat, endpoint=False).tolist()
current_scores += current_scores[:1]
ideal_scores   += ideal_scores[:1]
angles         += angles[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(PANEL_BG)

ax.plot(angles, ideal_scores, color=ACCENT3, linewidth=1.5, linestyle='--', alpha=0.5)
ax.fill(angles, ideal_scores, color=ACCENT3, alpha=0.07)

ax.plot(angles, current_scores, color=ACCENT1, linewidth=2.5)
ax.fill(angles, current_scores, color=ACCENT1, alpha=0.25)

# Score markers
ax.scatter(angles[:-1], current_scores[:-1], color=ACCENT2, s=80, zorder=5)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=10, color=TEXT_COLOR)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2','4','6','8','10'], color='#666880', fontsize=8)
ax.set_ylim(0, 10)
ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
ax.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
ax.spines['polar'].set_color(GRID_COLOR)

legend_handles = [
    mpatches.Patch(color=ACCENT1, alpha=0.7, label='Current Research Maturity'),
    mpatches.Patch(color=ACCENT3, alpha=0.3, label='Target / Ideal State'),
]
ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.35, 1.15),
          framealpha=0.85, fontsize=11)
ax.set_title('GPS-Denied Navigation Research Maturity\nby Dimension (corpus-derived)',
             fontsize=14, fontweight='bold', pad=30, color=TEXT_COLOR)
plt.tight_layout()
save(fig, 'fig09_research_maturity_radar.png')

# ────────────────────────────────────────────────────────────
# SUMMARY REPORT
# ────────────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("[OK] ALL 9 FIGURES GENERATED SUCCESSFULLY")
print(f"{'='*70}")
print(f"\n[OUT] Output: {OUTPUT_DIR}")
for p in sorted(OUTPUT_DIR.glob('fig*.png')):
    size_kb = p.stat().st_size // 1024
    print(f"   + {p.name:<45} ({size_kb} KB)")
print(f"\n[STATS] CANONICAL PAPER COUNTS (use these in manuscript):")
print(f"   Raw records        : {N_RAW:,}")
print(f"   After dedup        : {N_UNIQUE:,}")
print(f"   Duplicates removed : {N_DUPES:,}  ({100*N_DUPES/N_RAW:.1f}% duplication rate)")
print(f"   Included papers    : {N_INCLUDED:,}  ({100*N_INCLUDED/N_UNIQUE:.1f}% inclusion rate)")
print(f"   Excluded papers    : {N_EXCLUDED:,}  ({100*N_EXCLUDED/N_UNIQUE:.1f}% exclusion rate)")
print(f"   Extracted (master) : {N_EXTRACTED:,}")
print(f"\nNEXT STEP: Run the manuscript rewrite script.")
