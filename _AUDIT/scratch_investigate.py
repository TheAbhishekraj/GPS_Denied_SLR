import os
import glob
import pandas as pd
import re

def main():
    pdf_dir = "E:/GPS_Denied_SLR/05_papers_fulltext/"
    pdfs = glob.glob(pdf_dir + "*.pdf")
    rec_ids = []
    for p in pdfs:
        fname = os.path.basename(p)
        match = re.search(r'(REC_\d+)', fname)
        if match: rec_ids.append(match.group(1))
    
    old_master_path = "E:/GPS_Denied_SLR/_QUARANTINE_20260919_FULL_RESET/02_data_processed/deduplicated_master.csv"
    old_df = pd.read_csv(old_master_path)
    print("Old master sample:")
    for _, row in old_df.head(5).iterrows():
        print(f"  {row['id']} | {row.get('doi', '')} | {row.get('title', '')}")
    
    fresh_df = pd.read_csv("E:/GPS_Denied_SLR/02_data_processed/deduplicated.csv")
    def norm_doi(d): return str(d).lower().strip() if pd.notna(d) and str(d).strip() != '' else ''
    def norm_title(t): return re.sub(r'[^a-z0-9]', '', str(t).lower()) if pd.notna(t) else ''
    
    old_df['norm_doi'] = old_df.get('doi', pd.Series(index=old_df.index)).apply(norm_doi)
    fresh_df['norm_doi'] = fresh_df['doi'].apply(norm_doi)
    old_df['norm_title'] = old_df.get('title', pd.Series(index=old_df.index)).apply(norm_title)
    old_df['norm_year'] = old_df.get('year', pd.Series(index=old_df.index)).astype(str).str.strip()
    fresh_df['norm_title'] = fresh_df['title'].apply(norm_title)
    fresh_df['norm_year'] = fresh_df['year'].astype(str).str.strip()
    
    matches = 0
    for _, f_row in fresh_df.iterrows():
        f_doi = f_row['norm_doi']
        f_ty = f_row['norm_title'] + "_" + f_row['norm_year']
        if f_doi and (old_df['norm_doi'] == f_doi).any():
            matches += 1
            continue
        if f_ty:
            old_ty = old_df['norm_title'] + "_" + old_df['norm_year']
            if (old_ty == f_ty).any():
                matches += 1
                
    match_rate = matches / len(fresh_df) if len(fresh_df) > 0 else 0
    print(f"Fresh dedup rows: {len(fresh_df)}")
    print(f"Fresh rows matched to old by DOI or Title+Year: {matches}")
    print(f"Match rate: {match_rate*100:.2f}%")
    
    old_recs = set(old_df['id'])
    pdf_recs = set(rec_ids)
    pdf_matched = pdf_recs.intersection(old_recs)
    print(f"PDFs matched to old REC_ids (using id column): {len(pdf_matched)} / {len(pdf_recs)}")

if __name__ == "__main__":
    main()
