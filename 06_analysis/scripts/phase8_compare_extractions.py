#!/usr/bin/env python3
import os
import glob
import re
import csv
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL_DIR = os.path.join(REPO, "_MANUAL", "abhishek", "per_paper")
AI_DIR = os.path.join(REPO, "03_extraction", "per_paper")
REPORT = os.path.join(REPO, "_AUDIT", "extraction_comparison_report.csv")

def extract_fields(filepath):
    fields = {}
    if not os.path.exists(filepath):
        return fields
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We parse out headers and the first paragraph under them.
    # We'll just look for a few key fields for comparison, e.g., taxonomy, real_or_sim, sensors
    
    patterns = {
        'taxonomy_category': r'## 13\. Taxonomy Category\s*\n*(.*?)\n*(?:##|$)',
        'real_or_sim': r'## 7\. Experimental Setup.*?Real/Sim\s*:\s*(.*?)\n',
        'sensors': r'## 6\. System Architecture.*?Sensors\s*:\s*(.*?)\n'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            fields[key] = match.group(1).strip()
        else:
            fields[key] = 'NOT_FOUND'
            
    return fields

def main():
    manual_files = glob.glob(os.path.join(MANUAL_DIR, "REC_*.md"))
    
    total_compared = 0
    matches = {'taxonomy_category': 0, 'real_or_sim': 0, 'sensors': 0}
    
    results = []
    
    for mf in manual_files:
        basename = os.path.basename(mf)
        ai_f = os.path.join(AI_DIR, basename)
        
        if not os.path.exists(ai_f):
            continue
            
        man_data = extract_fields(mf)
        ai_data = extract_fields(ai_f)
        
        row = {'id': basename.replace('.md', '')}
        
        for k in matches.keys():
            man_val = man_data.get(k, '').lower()
            ai_val = ai_data.get(k, '').lower()
            
            # Simple match logic: if they contain similar keywords
            match_score = 1 if (man_val == ai_val and man_val != 'not_found') else 0
            # Be generous if one is a substring of the other
            if len(man_val) > 3 and len(ai_val) > 3:
                if man_val in ai_val or ai_val in man_val:
                    match_score = 1
                    
            row[f'{k}_manual'] = man_val[:50]
            row[f'{k}_ai'] = ai_val[:50]
            row[f'{k}_match'] = match_score
            matches[k] += match_score
            
        results.append(row)
        total_compared += 1
        
    with open(REPORT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'taxonomy_category_manual', 'taxonomy_category_ai', 'taxonomy_category_match', 'real_or_sim_manual', 'real_or_sim_ai', 'real_or_sim_match', 'sensors_manual', 'sensors_ai', 'sensors_match'])
        writer.writeheader()
        writer.writerows(results)
        
    print(f"Compared {total_compared} files.")
    for k, v in matches.items():
        accuracy = (v / total_compared) * 100 if total_compared > 0 else 0
        print(f"Accuracy for {k}: {accuracy:.1f}% ({v}/{total_compared})")

if __name__ == '__main__':
    main()
