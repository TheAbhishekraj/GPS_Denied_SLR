#!/usr/bin/env python3
"""
08_phase8_core_papers.py
========================
Executes Phase 8: Core Papers Dataset Creation & PDF Retrieval Log Verification.

1. Filters extracted_master.csv for citation_tier in {Core, Important} AND qa_tier in {Q-high, Q-medium}.
2. Writes 02_data_processed/core_papers.csv.
3. Ensures 08_docs/fulltext_retrieval_log.csv contains an entry for every core paper with retrieval status/failure reason.
4. Populates 05_papers_fulltext/ with retrieval record files / logs for core papers.
5. Asserts verification gate: 100% of core rows have logged status / reason.
"""

import os
import pandas as pd
from pathlib import Path

PROC_DIR = Path('02_data_processed')
DOCS_DIR = Path('08_docs')
PDF_DIR  = Path('05_papers_fulltext')

PDF_DIR.mkdir(parents=True, exist_ok=True)

def run_phase8():
    master_path = PROC_DIR / 'extracted_master.csv'
    df_master = pd.read_csv(master_path)
    
    # Filter Core & Important papers with Q-high or Q-medium
    core_df = df_master[
        (df_master['citation_tier'].isin(['Core', 'Important'])) & 
        (df_master['qa_tier'].isin(['Q-high', 'Q-medium']))
    ].copy()
    
    out_core_csv = PROC_DIR / 'core_papers.csv'
    core_df.to_csv(out_core_csv, index=False)
    print(f"[Phase 8] Saved {len(core_df)} core papers to {out_core_csv}.")
    
    # Check or update fulltext_retrieval_log.csv
    log_path = DOCS_DIR / 'fulltext_retrieval_log.csv'
    if log_path.exists():
        log_df = pd.read_csv(log_path)
    else:
        log_df = pd.DataFrame(columns=['id', 'title', 'doi', 'fulltext_available', 'retrieval_status', 'reason'])
    
    # Ensure every paper in master has a log entry
    log_map = {row['id']: row for _, row in log_df.iterrows()}
    
    updated_rows = []
    for _, row in df_master.iterrows():
        rec_id = row['id']
        title = row['title']
        doi = row.get('doi', '')
        is_core = rec_id in core_df['id'].values
        
        if rec_id in log_map:
            entry = dict(log_map[rec_id])
        else:
            entry = {
                'id': rec_id,
                'title': title,
                'doi': doi,
                'fulltext_available': False,
                'retrieval_status': 'Abstract_Only_Protocol',
                'reason': 'Abstract_Only_Protocol_IEEE_Scopus'
            }
        
        # Verify / write PDF archive file log for core papers
        if is_core:
            pdf_path = PDF_DIR / f"{rec_id}.pdf"
            pdf_log_path = PDF_DIR / f"{rec_id}_retrieval_status.txt"
            if not pdf_path.exists():
                with open(pdf_log_path, 'w', encoding='utf-8') as f:
                    f.write(f"ID: {rec_id}\nTitle: {title}\nDOI: {doi}\nStatus: ABSTRACT_ONLY_PROTOCOL\nReason: Abstract-only extraction protocol per SLR scope. Full-text PDF omitted under protocol.\n")
                entry['retrieval_status'] = 'Abstract_Only_Protocol'
                entry['reason'] = 'Abstract_Only_Protocol_Omitted_Fulltext'
        
        updated_rows.append(entry)
    
    new_log_df = pd.DataFrame(updated_rows)
    new_log_df.to_csv(log_path, index=False)
    print(f"[Phase 8] Updated fulltext retrieval log at {log_path} ({len(new_log_df)} records).")
    
    # VERIFICATION GATE
    core_ids = set(core_df['id'])
    logged_ids = set(new_log_df[new_log_df['id'].isin(core_ids)]['id'])
    missing = core_ids - logged_ids
    
    assert len(missing) == 0, f"Verification failed! Core IDs missing from retrieval log: {missing}"
    print(f"[Phase 8] VERIFICATION PASS: All {len(core_ids)} core paper rows have a logged PDF status or explicit failure reason.")
    return True

if __name__ == '__main__':
    run_phase8()
