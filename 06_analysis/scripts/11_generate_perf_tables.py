#!/usr/bin/env python3
"""
11_generate_perf_tables.py
===========================
Generates performance and synthesis tables for Phase 9/10 manuscript integration:
- 07_manuscript/perf_summary.csv
- 07_manuscript/perf_tables.md

Derives every summary metric directly from 02_data_processed/extracted_master.csv.
"""

import os
import pandas as pd
from pathlib import Path

PROC_DIR = Path('02_data_processed')
MANFLOW_DIR = Path('07_manuscript')

def generate_perf_tables():
    df = pd.read_csv(PROC_DIR / 'extracted_master.csv')
    
    # 1. Summary by Algorithm Family
    algo_summary = df.groupby('algorithm_family').agg(
        total_papers=('id', 'count'),
        real_world=('experiment_type', lambda x: (x == 'real_world').sum()),
        simulation=('experiment_type', lambda x: (x == 'simulation').sum()),
        q_medium=('qa_tier', lambda x: (x == 'Q-medium').sum()),
        q_low=('qa_tier', lambda x: (x == 'Q-low').sum())
    ).reset_index().sort_values('total_papers', ascending=False)

    algo_summary.to_csv(MANFLOW_DIR / 'perf_summary.csv', index=False)
    print(f"Saved {MANFLOW_DIR / 'perf_summary.csv'}")

    # 2. Build Markdown Performance & Synthesis Tables
    md = []
    md.append("# Systematic Review Synthesis Tables (Canonical Dataset: N = 636)\n")
    md.append("## Table 1: State Estimation Algorithm Family Distribution & Empirical Validation\n")
    md.append("| Algorithm Family | Total Papers | Real-World Validation | Simulation Only | Q-medium Tier | Q-low Tier |")
    md.append("|---|---|---|---|---|---|")
    
    for _, row in algo_summary.iterrows():
        md.append(f"| {row['algorithm_family']} | {row['total_papers']} | {row['real_world']} | {row['simulation']} | {row['q_medium']} | {row['q_low']} |")

    md.append("\n---\n")
    md.append("## Table 2: Operational Environment Breakdown by Platform Type\n")
    md.append("| Environment | UAV | UGV | Total |")
    md.append("|---|---|---|---|")
    
    env_ct = pd.crosstab(df['environment'], df['platform'])
    for env, row in env_ct.iterrows():
        uav = row.get('UAV', 0)
        ugv = row.get('UGV', 0)
        md.append(f"| {env} | {uav} | {ugv} | {uav + ugv} |")

    md.append("\n---\n")
    md.append("## Table 3: Application Domain Breakdown\n")
    md.append("| Application Domain | Paper Count | Percentage (%) |")
    md.append("|---|---|---|")
    app_summary = df['application_domain'].value_counts()
    for domain, count in app_summary.items():
        pct = (count / len(df)) * 100
        md.append(f"| {domain} | {count} | {pct:.1f}% |")

    md_path = MANFLOW_DIR / 'perf_tables.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
        
    print(f"Saved {md_path}")
    return True

if __name__ == '__main__':
    generate_perf_tables()
