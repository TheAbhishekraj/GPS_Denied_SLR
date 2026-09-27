#!/usr/bin/env python3
import os
import re
import csv
import json
import shutil
import hashlib
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MASTER = os.path.join(REPO, "02_data_processed", "MASTER_EVIDENCE.csv")
MANUAL_DIR = os.path.join(REPO, "_MANUAL", "abhishek", "per_paper")
LOG = os.path.join(REPO, "_AUDIT", "action_log.md")

INTERPRETIVE_FIELDS = [
    'problem', 'motivation', 'gps_denied_type', 'environment', 'platform',
    'sensors', 'method_category', 'algorithm', 'real_or_sim', 'dataset',
    'metrics', 'headline_result', 'baseline', 'ablation', 'limitations',
    'future_work', 'taxonomy_category', 'contribution_type', 'country',
    'funding', 'notes', '_source_pages'
]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()

def get_field(pattern, text, default='NOT_REPORTED'):
    m = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if m:
        return m.group(1).strip()
    return default

def parse_markdown(text):
    sections = {}
    for m in re.finditer(r'##\s+(\d+)\.\s+(.*?)\n(.*?)(?=\n##\s+\d+\.|\Z)', text, re.DOTALL):
        sections[int(m.group(1))] = m.group(3).strip()
    
    sec4 = sections.get(4, 'NOT_REPORTED')
    gps_type = sec4.split('\n')[0].strip() if sec4 != 'NOT_REPORTED' else 'NOT_REPORTED'
    
    sec13 = sections.get(13, 'NOT_REPORTED')
    tax_cat = sec13.split('\n')[0].strip() if sec13 != 'NOT_REPORTED' else 'NOT_REPORTED'
    
    sec12 = sections.get(12, 'NOT_REPORTED')
    contrib_type = sec12.split('\n')[0].strip() if sec12 != 'NOT_REPORTED' else 'NOT_REPORTED'

    sec8 = sections.get(8, 'NOT_REPORTED')
    metrics = []
    for line in sec8.split('\n'):
        if line.startswith('|') and 'metric' not in line.lower() and '----' not in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if parts:
                metrics.append(parts[0])
    metrics_str = ', '.join(metrics) if metrics else 'NOT_REPORTED'

    return {
        'problem': sections.get(2, 'NOT_REPORTED'),
        'motivation': sections.get(3, 'NOT_REPORTED'),
        'gps_denied_type': gps_type,
        'environment': get_field(r'^-\s*environment:\s*(.*)', sections.get(7, '')),
        'platform': get_field(r'^-\s*Platform:\s*(.*)', sections.get(6, '')),
        'sensors': get_field(r'^-\s*Sensors:\s*(.*)', sections.get(6, '')),
        'method_category': get_field(r'^Category:\s*(.*)', sections.get(5, '')),
        'algorithm': get_field(r'^Method name:\s*(.*)', sections.get(5, '')),
        'real_or_sim': get_field(r'^-\s*real_or_sim:\s*(.*)', sections.get(7, '')),
        'dataset': get_field(r'^-\s*dataset:\s*(.*)', sections.get(7, '')),
        'metrics': metrics_str,
        'headline_result': sections.get(8, 'NOT_REPORTED'),
        'baseline': get_field(r'^-\s*baselines:\s*(.*)', sections.get(7, '')),
        'ablation': sections.get(9, 'NOT_REPORTED'),
        'limitations': sections.get(10, 'NOT_REPORTED'),
        'future_work': sections.get(11, 'NOT_REPORTED'),
        'taxonomy_category': tax_cat,
        'contribution_type': contrib_type,
        'country': get_field(r'^Country:\s*(.*)', sections.get(14, '')),
        'funding': get_field(r'^Funding:\s*(.*)', sections.get(14, '')),
        'notes': sections.get(15, 'NOT_REPORTED'),
        '_source_pages': sections.get(16, 'NOT_REPORTED')
    }

def main():
    if not os.path.exists(MASTER):
        print("Error: MASTER_EVIDENCE.csv not found")
        return 1

    with open(MASTER, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        
    before_hash = sha256_file(MASTER)
    fieldnames = reader[0].keys() if reader else []
    
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_path = MASTER.replace('.csv', f'_backup_T2_{ts}.csv')
    shutil.copy2(MASTER, backup_path)
    print(f"Backup created at: {backup_path}")
    
    parsed_count = 0
    missing = []
    
    for row in reader:
        rec_id = row['id']
        md_path = os.path.join(MANUAL_DIR, f"{rec_id}.md")
        if not os.path.exists(md_path):
            missing.append(rec_id)
            continue
            
        with open(md_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
            
        extracted = parse_markdown(md_text)
        
        for field in INTERPRETIVE_FIELDS:
            if field in extracted:
                row[field] = extracted[field] if extracted[field] != "" else "NOT_REPORTED"
                
        parsed_count += 1

    if missing:
        print(f"Warning: {len(missing)} files missing (e.g. {missing[:5]})")
        
    with open(MASTER, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(reader)
        
    after_hash = sha256_file(MASTER)
    
    ts_log = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"{ts_log} | PHASE7 | T2 MERGE INTERPRETIVE FIELDS | {MASTER} | rows modified: {parsed_count} | master {before_hash[:12]} -> {after_hash[:12]} | backup: {backup_path}\n")

    print(f"Successfully processed {parsed_count} out of {len(reader)} rows.")
    print(f"MASTER_EVIDENCE.csv updated.")
    print(f"Before Hash: {before_hash}")
    print(f"After Hash: {after_hash}")
    return 0

if __name__ == '__main__':
    main()
