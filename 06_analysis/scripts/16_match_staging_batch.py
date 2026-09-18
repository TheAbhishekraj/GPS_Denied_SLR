"""Match new downloads_staging PDFs against master/screened/priority records.

Read-only diagnostics: prints a decision table per staging file. No writes.
DOI match first; title-similarity fallback for PDFs without a printed DOI.
"""
import csv
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf

ROOT = Path(r'E:\GPS_Denied_SLR')
ST = ROOT / '08_docs' / 'downloads_staging'
FT = ROOT / '05_papers_fulltext'

STOP = {'a', 'an', 'the', 'of', 'for', 'in', 'on', 'and', 'with', 'based',
        'via', 'from', 'to', 'under'}


def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9 ]', ' ', s.lower()).strip()


def tkey(s):
    return ' '.join(w for w in norm(s).split() if w not in STOP)


def load(p):
    with open(p, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


master = load(ROOT / '02_data_processed' / 'extracted_master_v2.csv')
screened = load(ROOT / '02_data_processed' / 'screened_included_v2.csv')
priority = load(ROOT / '08_docs' / 'priority_300_download.csv')

print('master cols  :', list(master[0].keys()))
print('screened cols:', list(screened[0].keys()))
print('priority cols:', list(priority[0].keys()))
print('counts: master=%d screened=%d priority=%d' % (len(master), len(screened), len(priority)))


def col(keys, needle):
    for k in keys:
        if needle in k.lower():
            return k
    return None


records = []
for name, rows in (('master', master), ('screened', screened), ('priority', priority)):
    ck = col(rows[0].keys(), 'doi')
    ct = col(rows[0].keys(), 'title')
    ci = col(rows[0].keys(), 'id')
    if not ck:
        print(f'!! {name}: no DOI column')
    for r in rows:
        doi = (r.get(ck) or '').strip().lower().rstrip('.') if ck else ''
        title = (r.get(ct) or '').strip() if ct else ''
        rid = (r.get(ci) or '').strip() if ci else ''
        records.append({'src': name, 'id': rid, 'doi': doi,
                        'tkey': tkey(title), 'title': title})

doi_map = {}
for rec in records:
    if rec['doi']:
        doi_map.setdefault(rec['doi'], []).append(rec)

for p in sorted(ST.iterdir()):
    if p.suffix.lower() != '.pdf':
        print(f'\n{p.name} : NOT-PDF size={p.stat().st_size}')
        continue
    try:
        d = pymupdf.open(p)
        text = ' '.join((pg.get_text() or '') for pg in d)
    except Exception as e:
        print(f'\n{p.name} : UNREADABLE {e}')
        continue
    m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text[:8000], re.I)
    doi = m.group(0).rstrip('.,;)').lower() if m else ''
    head = ' '.join(text[:400].split())
    cand = doi_map.get(doi, []) if doi else []
    sim = ''
    if not cand:
        scored = sorted(
            ((SequenceMatcher(None, tkey(head[:150]), r['tkey']).ratio(), r)
             for r in records),
            key=lambda x: -x[0])
        cand = [r for ratio, r in scored[:3] if ratio >= 0.55]
        if scored:
            sim = (f' (title-sim top={scored[0][0]:.2f} '
                   f'{scored[0][1]["src"]}:{scored[0][1]["id"]})')
    tags = []
    for rec in cand:
        exists = (FT / f"{rec['id']}.pdf").exists()
        tags.append(f"{rec['src']}:{rec['id']} fulltext={exists}")
    print(f'\n{p.name}\n  pages={d.page_count} doi={doi or "-"}{sim}')
    print('  match: ' + (' | '.join(tags) if tags else 'NO MATCH'))
