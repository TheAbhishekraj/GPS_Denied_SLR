import pandas as pd
import re

def main():
    input_path = "02_data_processed/deduplicated.csv"
    df = pd.read_csv(input_path)
    
    input_count = len(df)
    
    passed = []
    rejected = []
    
    uav_keywords = ['uav', 'uavs', 'drone', 'drones', 'unmanned aerial', 'quadrotor', 'micro aerial', 'mav', 'hexarotor']
    denied_keywords = ['denied', 'indoor', 'subterranean', 'underground', 'gps-less', 'gnss-less', 'without gps']
    fusion_keywords = ['fusion', 'multi-sensor', 'multisensor', 'integrate', 'kalman', 'ekf', 'vio', 'slam', 'lio', 'filter']
    
    def check_keywords(text, keywords):
        if pd.isna(text):
            return False
        text_lower = str(text).lower()
        for kw in keywords:
            if kw in text_lower:
                return True
        return False

    for idx, row in df.iterrows():
        year_valid = False
        try:
            year = int(row['year'])
            if 2010 <= year <= 2026:
                year_valid = True
        except:
            pass
            
        title_abs = str(row['title']) + " " + str(row['abstract'])
        
        has_uav = check_keywords(title_abs, uav_keywords)
        has_denied = check_keywords(title_abs, denied_keywords)
        has_fusion = check_keywords(title_abs, fusion_keywords)
        
        # Exclude purely theoretical or terrestrial based on keywords if we want to be stricter,
        # but a positive match for uav, denied, and fusion is a solid programmatic proxy.
        
        if year_valid and has_uav and has_denied and has_fusion:
            passed.append(row)
        else:
            rejected.append(row)
            
    # Handle empty lists to maintain columns
    passed_df = pd.DataFrame(passed) if passed else pd.DataFrame(columns=df.columns)
    rejected_df = pd.DataFrame(rejected) if rejected else pd.DataFrame(columns=df.columns)
        
    passed_df.to_csv("02_data_processed/screened.csv", index=False)
    rejected_df.to_csv("02_data_processed/screening_rejected.csv", index=False)
    
    passed_count = len(passed_df)
    rejected_count = len(rejected_df)
    
    print(f"INPUT: {input_count}")
    print(f"PASSED: {passed_count}")
    print(f"REJECTED: {rejected_count}")

if __name__ == "__main__":
    main()
