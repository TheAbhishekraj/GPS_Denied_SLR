import pandas as pd
import hashlib
import os

def main():
    os.makedirs("02_data_processed", exist_ok=True)
    os.makedirs("06_analysis/scripts", exist_ok=True)

    ieee_path = "01_data_raw/ieee_xplore_20260615.csv"
    scopus_path = "01_data_raw/scopus_20260615.csv"

    ieee_df = pd.read_csv(ieee_path)
    scopus_df = pd.read_csv(scopus_path)

    input_count = len(ieee_df) + len(scopus_df)

    ieee_std = pd.DataFrame({
        'title': ieee_df['Document Title'].fillna(''),
        'authors': ieee_df['Authors'].fillna(''),
        'year': ieee_df['Publication Year'].astype(str),
        'doi': ieee_df['DOI'].fillna(''),
        'venue': ieee_df['Publication Title'].fillna(''),
        'abstract': ieee_df['Abstract'].fillna(''),
        'source': 'IEEE',
        'original_id': ieee_df['Document Identifier'].fillna(''),
    })

    scopus_std = pd.DataFrame({
        'title': scopus_df['title'].fillna(''),
        'authors': scopus_df['authors'].fillna(''),
        'year': scopus_df['year'].astype(str),
        'doi': scopus_df['doi'].fillna(''),
        'venue': scopus_df['venue'].fillna(''),
        'abstract': scopus_df['abstract'].fillna(''),
        'source': 'Scopus',
        'original_id': scopus_df['id'].fillna(''),
    })

    combined = pd.concat([ieee_std, scopus_std], ignore_index=True)

    combined['norm_doi'] = combined['doi'].str.lower().str.strip()
    combined['norm_title'] = combined['title'].str.lower().str.replace(r'[^a-z0-9]', '', regex=True)
    combined['norm_year'] = combined['year'].str.strip()

    def get_row_hash(row):
        content = str(row['title']) + str(row['authors']) + str(row['abstract'])
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    combined['row_hash'] = combined.apply(get_row_hash, axis=1)

    deduplicated = []
    dropped_log = []
    
    seen_dois = set()
    seen_title_year = set()
    seen_hashes = set()

    for idx, row in combined.iterrows():
        is_duplicate = False
        drop_reason = ""
        
        if row['norm_doi'] != "":
            if row['norm_doi'] in seen_dois:
                is_duplicate = True
                drop_reason = "DOI Match"
            else:
                seen_dois.add(row['norm_doi'])
                
        title_year = row['norm_title'] + "_" + row['norm_year']
        if not is_duplicate and row['norm_title'] != "":
            if title_year in seen_title_year:
                is_duplicate = True
                drop_reason = "Title+Year Match"
            else:
                seen_title_year.add(title_year)
                
        if not is_duplicate:
            if row['row_hash'] in seen_hashes:
                is_duplicate = True
                drop_reason = "Row Hash Match"
            else:
                seen_hashes.add(row['row_hash'])
                
        if is_duplicate:
            dropped_log.append({
                'source': row['source'],
                'original_id': row['original_id'],
                'title': row['title'],
                'drop_reason': drop_reason
            })
        else:
            deduplicated.append(row)

    dedup_df = pd.DataFrame(deduplicated)
    log_df = pd.DataFrame(dropped_log)

    old_master_path = "E:/GPS_Denied_SLR/_QUARANTINE_20260919_FULL_RESET/02_data_processed/deduplicated_master.csv"
    old_df = pd.read_csv(old_master_path)
    
    def norm_doi(d): return str(d).lower().strip() if pd.notna(d) and str(d).strip() != '' else ''
    def norm_title(t): return __import__('re').sub(r'[^a-z0-9]', '', str(t).lower()) if pd.notna(t) else ''
    
    old_df['norm_doi'] = old_df.get('doi', pd.Series(index=old_df.index)).apply(norm_doi)
    old_df['norm_title'] = old_df.get('title', pd.Series(index=old_df.index)).apply(norm_title)
    old_df['norm_year'] = old_df.get('year', pd.Series(index=old_df.index)).astype(str).str.strip()
    
    rec_ids = []
    for _, row in dedup_df.iterrows():
        f_doi = row['norm_doi']
        f_ty = row['norm_title'] + "_" + row['norm_year']
        
        match_id = "UNRESOLVED"
        
        if f_doi:
            doi_matches = old_df[old_df['norm_doi'] == f_doi]
            if len(doi_matches) > 0:
                match_id = doi_matches.iloc[0]['id']
        
        if match_id == "UNRESOLVED" and f_ty:
            ty_matches = old_df[(old_df['norm_title'] + "_" + old_df['norm_year']) == f_ty]
            if len(ty_matches) > 0:
                match_id = ty_matches.iloc[0]['id']
                
        rec_ids.append(match_id)
        
    dedup_df['REC_id'] = rec_ids
    dedup_df = dedup_df.drop(columns=['norm_doi', 'norm_title', 'norm_year', 'row_hash'])

    output_count = len(dedup_df)
    dropped_count = len(log_df)

    dedup_df.to_csv("02_data_processed/deduplicated.csv", index=False)
    log_df.to_csv("02_data_processed/dedup_log.csv", index=False)

    print(f"INPUT: {input_count}")
    print(f"OUTPUT: {output_count}")
    print(f"DROPPED: {dropped_count}")
    
if __name__ == "__main__":
    main()
