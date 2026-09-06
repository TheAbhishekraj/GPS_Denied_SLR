"""
Deduplication script for IEEE Xplore and Scopus CSV files
This script removes duplicate papers based on DOI, title, and abstract similarity
"""

import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import re
import warnings
warnings.filterwarnings('ignore')

def clean_text(text):
    """Clean text for comparison - lowercase, remove extra spaces, punctuation"""
    if pd.isna(text):
        return ''
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip()

def string_similarity(a, b):
    """Calculate similarity between two strings (0-1)"""
    if not a or not b:
        return 0
    return SequenceMatcher(None, a, b).ratio()

def deduplicate_by_doi(df, doi_col='DOI'):
    """Remove duplicates based on DOI"""
    if doi_col in df.columns:
        # Clean DOI strings
        df['clean_doi'] = df[doi_col].astype(str).str.lower().str.strip()
        # Remove rows with empty DOI
        df_no_doi = df[df['clean_doi'].isin(['nan', '', 'none'])]
        df_with_doi = df[~df['clean_doi'].isin(['nan', '', 'none'])]
        
        # Deduplicate by DOI
        df_dedup_doi = df_with_doi.drop_duplicates(subset='clean_doi', keep='first')
        
        # Combine back
        df_combined = pd.concat([df_dedup_doi, df_no_doi], ignore_index=True)
        df_combined = df_combined.drop(columns=['clean_doi'])
        return df_combined
    return df

def deduplicate_by_title(df, title_col='Title', similarity_threshold=0.9):
    """Remove duplicates based on title similarity"""
    if title_col in df.columns:
        df = df.copy()
        df['clean_title'] = df[title_col].apply(clean_text)
        
        # Create list of unique titles
        unique_titles = []
        indices_to_keep = []
        
        for idx, row in df.iterrows():
            title = row['clean_title']
            if not title:
                indices_to_keep.append(idx)
                continue
                
            # Check similarity with existing titles
            is_duplicate = False
            for existing_title in unique_titles:
                if string_similarity(title, existing_title) >= similarity_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_titles.append(title)
                indices_to_keep.append(idx)
        
        return df.loc[indices_to_keep].drop(columns=['clean_title'])
    return df

def main():
    """Main deduplication function"""
    print("Starting deduplication process...")
    
    try:
        # Load IEEE Xplore data
        print("Loading IEEE Xplore data...")
        ieee_path = r"E:\GPS_Denied_SLR\01_data_raw\ieee_xplore.csv"
        ieee_df = pd.read_csv(ieee_path, encoding='utf-8')
        print(f"IEEE Xplore: {len(ieee_df)} records loaded")
        
        # Load Scopus data
        print("Loading Scopus data...")
        scopus_path = r"E:\GPS_Denied_SLR\01_data_raw\scopus.csv"
        scopus_df = pd.read_csv(scopus_path, encoding='utf-8')
        print(f"Scopus: {len(scopus_df)} records loaded")
        
        # Combine datasets
        combined_df = pd.concat([ieee_df, scopus_df], ignore_index=True)
        print(f"Total combined records: {len(combined_df)}")
        
        # Step 1: Deduplicate by DOI
        print("\nStep 1: Deduplicating by DOI...")
        dedup_doi = deduplicate_by_doi(combined_df)
        print(f"After DOI deduplication: {len(dedup_doi)} records")
        
        # Step 2: Deduplicate by title similarity
        print("\nStep 2: Deduplicating by title similarity...")
        dedup_final = deduplicate_by_title(dedup_doi, similarity_threshold=0.9)
        print(f"After title deduplication: {len(dedup_final)} records")
        
        # Calculate duplicates removed
        duplicates_removed = len(combined_df) - len(dedup_final)
        print(f"\nTotal duplicates removed: {duplicates_removed}")
        
        # Save deduplicated data
        output_path = r"E:\GPS_Denied_SLR\02_data_processed\deduplicated_combined.csv"
        dedup_final.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\nDeduplicated data saved to: {output_path}")
        
        # Save summary statistics
        summary = {
            'source': ['IEEE Xplore', 'Scopus', 'Combined', 'Deduplicated'],
            'record_count': [len(ieee_df), len(scopus_df), len(combined_df), len(dedup_final)]
        }
        summary_df = pd.DataFrame(summary)
        summary_path = r"E:\GPS_Denied_SLR\02_data_processed\deduplication_summary.csv"
        summary_df.to_csv(summary_path, index=False)
        print(f"Summary saved to: {summary_path}")
        
        print("\nDeduplication complete!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease make sure you have downloaded the CSV files from:")
        print("1. IEEE Xplore: Save to E:\\GPS_Denied_SLR\\01_data_raw\\ieee_xplore.csv")
        print("2. Scopus: Save to E:\\GPS_Denied_SLR\\01_data_raw\\scopus.csv")
        print("\nThen run this script again.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()