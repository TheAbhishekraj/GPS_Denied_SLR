import csv
import os
import shutil

base = r'E:\GPS_Denied_SLR\01_data_raw'

# The actual raw exports are ieee_xplore.csv and scopus.csv
# AGENT_TASK requires ieee_xplore_raw.csv and scopus_raw.csv with 8 canonical columns:
# id, title, abstract, authors, year, doi, venue, source

def normalize_ieee(src, dst):
    """Re-map IEEE Xplore columns to canonical schema."""
    with open(src, encoding='utf-8', errors='replace') as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    with open(dst, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['id','title','abstract','authors','year','doi','venue','source'])
        writer.writeheader()
        for i, r in enumerate(rows, 1):
            writer.writerow({
                'id': f'IEEE_{i:04d}',
                'title': r.get('Document Title', r.get('Title', '')).strip(),
                'abstract': r.get('Abstract', '').strip(),
                'authors': r.get('Authors', '').strip(),
                'year': r.get('Publication Year', r.get('Year', '')).strip(),
                'doi': r.get('DOI', '').strip(),
                'venue': r.get('Publication Title', r.get('Venue', '')).strip(),
                'source': 'IEEE',
            })
    count = len(rows)
    size = os.path.getsize(dst)
    print(f'Wrote {dst}: {count} rows, {size} bytes')
    return count

def normalize_scopus(src, dst):
    """Re-map Scopus columns to canonical schema."""
    with open(src, encoding='utf-8-sig', errors='replace') as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    # Scopus column names vary; try multiple keys
    def get(r, *keys):
        for k in keys:
            v = r.get(k, '')
            if v:
                return v.strip()
        return ''

    with open(dst, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['id','title','abstract','authors','year','doi','venue','source'])
        writer.writeheader()
        for i, r in enumerate(rows, 1):
            writer.writerow({
                'id': f'SCOPUS_{i:04d}',
                'title': get(r, 'Title', 'Document Title'),
                'abstract': get(r, 'Abstract'),
                'authors': get(r, 'Authors', 'Author full names', 'Author Names'),
                'year': get(r, 'Year', 'Publication Year'),
                'doi': get(r, 'DOI'),
                'venue': get(r, 'Source title', 'Publication Title', 'Venue'),
                'source': 'Scopus',
            })
    count = len(rows)
    size = os.path.getsize(dst)
    print(f'Wrote {dst}: {count} rows, {size} bytes')
    return count

ieee_count = normalize_ieee(
    os.path.join(base, 'ieee_xplore.csv'),
    os.path.join(base, 'ieee_xplore_raw.csv')
)
scopus_count = normalize_scopus(
    os.path.join(base, 'scopus.csv'),
    os.path.join(base, 'scopus_raw.csv')
)

# Verify
for fn in ['ieee_xplore_raw.csv', 'scopus_raw.csv']:
    fp = os.path.join(base, fn)
    with open(fp, encoding='utf-8') as fh:
        rows = list(csv.reader(fh))
    assert rows[0] == ['id','title','abstract','authors','year','doi','venue','source'], f'Column mismatch: {rows[0]}'
    assert len(rows)-1 == 1000, f'Row count mismatch: {len(rows)-1}'
    print(f'VERIFIED {fn}: {len(rows)-1} rows, cols OK')
