import os, sys, csv, json, glob
import pandas as pd

ROOT = r'E:\GPS_Denied_SLR'
DATA_DIR = os.path.join(ROOT, '02_data_processed')
MASTER_CSV = os.path.join(DATA_DIR, 'MASTER_EVIDENCE.csv')

print('TASK 1: FILE INVENTORY (Local Repo instead of Google Drive)')
print('---')
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        path = os.path.join(root, file)
        size = os.path.getsize(path)
        mtime = os.path.getmtime(path)
        print(f'{file} (Size: {size} bytes)')

print('\nTASK 2: SCHEMA SNAPSHOT')
print('---')
encoding = 'utf-8'
print(f'Using Encoding: {encoding}')

with open(MASTER_CSV, 'r', encoding=encoding, newline='') as f:
    lines = f.readlines()
    print('Header (Row 1):')
    print(lines[0].strip())
    print('\nRow 2:')
    print(lines[1].strip())
    print('\nRow 3:')
    print(lines[2].strip())
    print('\nRow 4:')
    print(lines[3].strip())

print('\nTASK 3: LIST-FIELD FORMAT')
print('---')
df = pd.read_csv(MASTER_CSV, encoding=encoding)
for idx in [0, 1]:
    if idx < len(df):
        print(f"Row {idx + 2} (ID: {df.iloc[idx].get('id', '')}):")
        print(f"  sensors: {repr(df.iloc[idx].get('sensors', ''))}")
        print(f"  metrics: {repr(df.iloc[idx].get('metrics', ''))}")

print('\nTASK 4: DATA QUALITY PROFILE')
print('---')
print(f'Total row count: {len(df)}')
print(f'Unique ID count: {df["id"].nunique() if "id" in df.columns else 0}')

print('\nMissing values per column:')
missing = df.replace(['NOT_REPORTED', ''], pd.NA).isna().sum()
print(missing.to_string())

for col in ['year', 'method_category', 'environment', 'real_or_sim', 'taxonomy_category', 'contribution_type']:
    print(f'\nValue counts for {col}:')
    if col in df.columns:
        print(df[col].value_counts(dropna=False).to_string())
    else:
        print(f'{col} not found')

print('\nOut of bounds method_category values:')
allowed_methods = {'SLAM', 'VIO', 'UWB', 'LIDAR', 'OPTICAL_FLOW', 'VISION_OBJECT', 'PSEUDOLITE', 'COOPERATIVE', 'QUANTUM', 'HYBRID', 'OTHER'}
if 'method_category' in df.columns:
    out_of_bounds = df[~df['method_category'].isin(allowed_methods)]['method_category'].unique()
    print(list(out_of_bounds))

print('\nTASK 5: QUALITY APPRAISAL STATUS')
print('---')
qa_files = glob.glob(os.path.join(ROOT, '**', 'quality_appraisal*.csv'), recursive=True)
if qa_files:
    for qa in qa_files:
        df_qa = pd.read_csv(qa)
        print(f'Found: {qa} (Rows: {len(df_qa)}, Cols: {len(df_qa.columns)})')
else:
    print('No quality_appraisal_scored.csv found.')

rubric_files = glob.glob(os.path.join(ROOT, '**', 'SCOPE.md'), recursive=True) + glob.glob(os.path.join(ROOT, '08_docs', '**', '*.md'), recursive=True)
for rf in rubric_files:
    with open(rf, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'Q7' in content or 'quality' in content.lower():
            print(f'\nPotential rubric found in {rf}:')
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if 'Q7' in line or 'quality' in line.lower():
                    print('\n'.join(lines[max(0, i-5):min(len(lines), i+15)]))
                    break
            break

print('\nTASK 6: EXISTING ANALYTICS')
print('---')
analytics = [
    'RQ_DATA_ANALYTICS.json',
    'evidence_matrix.csv',
    'inference_table.csv',
    'taxonomy_distribution.csv',
    'perf_summary.csv'
]
for a in analytics:
    matches = glob.glob(os.path.join(ROOT, '**', a), recursive=True)
    if matches:
        for m in matches:
            try:
                if m.endswith('.csv'):
                    d = pd.read_csv(m)
                    print(f'{m} (Rows: {len(d)})')
                elif m.endswith('.json'):
                    print(f'{m} (JSON file)')
            except Exception as e:
                print(f'{m} (Error reading: {e})')
    else:
        print(f'{a} not found')
