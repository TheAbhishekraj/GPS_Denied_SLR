import csv

f = r'E:\GPS_Denied_SLR\02_data_processed\extracted_master.csv'
with open(f, encoding='utf-8', errors='replace') as fh:
    reader = csv.DictReader(fh)
    rows = list(reader)

# F2: pure Adversarial environment
ew_primary = sum(1 for r in rows if (r.get('environment','') or '').strip() == "['Adversarial']")
print(f'F2 pure Adversarial env: {ew_primary}')

# F3: Multi-agent SLAM
ma_rows = [r for r in rows if 'multi' in (r.get('primary_method','') or '').lower() and 'slam' in (r.get('primary_method','') or '').lower()]
real_count = sum(1 for r in ma_rows if 'real' in (r.get('experiment_type','') or '').lower())
sim_count = sum(1 for r in ma_rows if 'sim' in (r.get('experiment_type','') or '').lower())
both_count = sum(1 for r in ma_rows if 'both' in (r.get('experiment_type','') or '').lower())
print(f'Multi-agent SLAM total: {len(ma_rows)}, real={real_count}, sim={sim_count}, both={both_count}')
for r in ma_rows[:5]:
    print(f'  title={r["title"][:60]}, exp={r["experiment_type"]}')

# top methods
methods = {}
for r in rows:
    m = (r.get('primary_method','') or '').strip()
    methods[m] = methods.get(m,0)+1
top = sorted(methods.items(), key=lambda x: -x[1])[:15]
print('Top methods:')
for m,c in top:
    print(f'  {c:4d}  {m}')
