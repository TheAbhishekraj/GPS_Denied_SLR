#!/usr/bin/env python3
import os
import csv

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MASTER = os.path.join(REPO, "02_data_processed", "MASTER_EVIDENCE.csv")
QA_CSV = os.path.join(REPO, "06_analysis", "outputs", "quality_appraisal_scored.csv")
MANUAL_DIR = os.path.join(REPO, "_MANUAL", "abhishek", "per_paper")
OUT_MATRIX = os.path.join(REPO, "_AUDIT", "file_wise_progress_matrix.csv")

def main():
    if not os.path.exists(MASTER):
        print("MASTER_EVIDENCE.csv not found.")
        return

    qa_dict = {}
    if os.path.exists(QA_CSV):
        with open(QA_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                qa_dict[row['id']] = row['qa_tier']

    with open(MASTER, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

    results = []
    for row in reader:
        rec_id = row['id']
        has_manual = "YES" if os.path.exists(os.path.join(MANUAL_DIR, f"{rec_id}.md")) else "NO"
        qa_tier = qa_dict.get(rec_id, 'UNSCORED')
        
        # Simple evaluation of whether interpretive fields are filled
        method = row.get('method_category', 'NOT_REPORTED')
        extracted = "YES" if method != 'NOT_REPORTED' else "NO"

        results.append({
            'Paper_ID': rec_id,
            'DOI': row.get('doi', ''),
            'Year': row.get('year', ''),
            'Quality_Tier': qa_tier,
            'Manual_Extraction_Present': has_manual,
            'Interpretive_Fields_Extracted': extracted,
            'Status': 'COMPLETED' if extracted == 'YES' else 'PENDING',
            'SME_Recommendation': 'Reliable for Synthesis' if qa_tier in ['Q-High', 'Q-Medium'] else 'Use with Caution (Q-Low)'
        })

    with open(OUT_MATRIX, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Paper_ID', 'DOI', 'Year', 'Quality_Tier', 
            'Manual_Extraction_Present', 'Interpretive_Fields_Extracted', 
            'Status', 'SME_Recommendation'
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"Generated file-wise matrix at {OUT_MATRIX} for {len(results)} records.")

if __name__ == '__main__':
    main()
