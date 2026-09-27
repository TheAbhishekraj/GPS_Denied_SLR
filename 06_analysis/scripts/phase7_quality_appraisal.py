#!/usr/bin/env python3
"""
phase7_quality_appraisal.py
Implements heuristic quality appraisal based on SCOPE.md Q7.
Reads: 02_data_processed/MASTER_EVIDENCE.csv
Writes: 06_analysis/outputs/quality_appraisal_scored.csv
"""

import os
import csv
import re
import hashlib
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MASTER_CSV = os.path.join(REPO, "02_data_processed", "MASTER_EVIDENCE.csv")
OUTPUT_CSV = os.path.join(REPO, "06_analysis", "outputs", "quality_appraisal_scored.csv")
LOG = os.path.join(REPO, "_AUDIT", "action_log.md")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()

def contains_keywords(text, keywords):
    text_lower = str(text).lower()
    return any(kw in text_lower for kw in keywords)

def score_paper(row):
    # Dimension A: Experimental Rigor (0-4)
    a_score = 0
    real_sim = str(row.get('real_or_sim', '')).strip().upper()
    if real_sim in ['REAL', 'BOTH']:
        a_score += 2
        
    combo_text = f"{row.get('metrics','')} {row.get('environment','')} {row.get('platform','')} {row.get('sensors','')}"
    if contains_keywords(combo_text, ['rtk', 'vicon', 'optitrack', 'motion capture', 'ground truth']):
        a_score += 1
        
    metrics_headline = f"{row.get('metrics','')} {row.get('headline_result','')}"
    if contains_keywords(metrics_headline, ['variance', 'std', 'standard deviation', 'confidence interval', 'trials']):
        a_score += 1

    # Dimension B: Reporting Completeness (0-3)
    b_score = 0
    if contains_keywords(row.get('metrics',''), ['ate', 'rmse', 'odometry error', 'absolute trajectory error']):
        b_score += 1
        
    if contains_keywords(row.get('environment',''), [' m', 'meters', 'km', 'minutes', 'sec', ' hz']):
        b_score += 1
        
    if str(row.get('ablation', '')).strip().upper() not in ['NOT_REPORTED', 'NO_ABLATION', '']:
        b_score += 1
    elif contains_keywords(row.get('limitations',''), ['fail', 'robustness', 'edge case', 'latency']):
        b_score += 1

    # Dimension C: Baseline Fairness (0-2)
    c_score = 0
    baseline = str(row.get('baseline', '')).strip().upper()
    if baseline not in ['NO_BASELINE', 'NOT_REPORTED', 'NONE', '']:
        c_score += 1
        
    dataset = str(row.get('dataset', '')).strip().upper()
    if dataset not in ['NOT_REPORTED', 'NONE', ''] and not dataset.startswith('CUSTOM'):
        # using a standard/shared dataset implies matched conditions
        c_score += 1
    elif contains_keywords(row.get('environment',''), ['euroc', 'kitti', 'tum', 'benchmark']):
        c_score += 1

    # Dimension D: Reproducibility (0-1)
    d_score = 0
    repo_text = f"{row.get('notes','')} {row.get('contribution_type','')} {row.get('dataset','')}"
    if contains_keywords(repo_text, ['open source', 'github', 'publicly available', 'code release']):
        d_score += 1

    total = a_score + b_score + c_score + d_score

    # Tier Assignment
    if total >= 8:
        raw_tier = "Q-High"
    elif total >= 5:
        raw_tier = "Q-Medium"
    else:
        raw_tier = "Q-Low"

    # Simulation cap
    final_tier = raw_tier
    if real_sim == 'SIM' and raw_tier == 'Q-High':
        final_tier = "Q-Medium (capped)"

    return {
        'id': row['id'],
        'qa_rigor': a_score,
        'qa_reporting': b_score,
        'qa_baseline': c_score,
        'qa_repro': d_score,
        'qa_total': total,
        'qa_tier': final_tier
    }

def main():
    if not os.path.exists(MASTER_CSV):
        print("ERROR: MASTER_EVIDENCE.csv not found")
        return 1
        
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    
    with open(MASTER_CSV, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        
    scored_rows = []
    for row in reader:
        scored_rows.append(score_paper(row))
        
    fieldnames = ['id', 'qa_rigor', 'qa_reporting', 'qa_baseline', 'qa_repro', 'qa_total', 'qa_tier']
    
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(scored_rows)
        
    out_hash = sha256_file(OUTPUT_CSV)
    
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"{ts} | PHASE7 | T3 QUALITY APPRAISAL | {OUTPUT_CSV} | rows: {len(scored_rows)} | sha256: {out_hash}\n")

    print(f"Scored {len(scored_rows)} papers.")
    print(f"Output saved to {OUTPUT_CSV}")
    print(f"SHA256: {out_hash}")
    return 0

if __name__ == '__main__':
    main()
