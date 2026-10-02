#!/usr/bin/env python3
"""build_refs.py - Station 9 / Gate 9.2: rebuild 07_manuscript/references.bib.

Per-ID sources (no external data):
  author  <- screening_results.csv (initials+surname; ';' -> ' and ')
  title   <- MASTER_EVIDENCE.csv, replaced by screening title if junk
  year    <- MASTER_EVIDENCE.csv
  journal <- _MANUAL/abhishek/per_paper/REC_XXXX.md YAML venue (else NOT_REPORTED)
  doi     <- MASTER_EVIDENCE.csv (placeholder repaired from screening)
Scope: all 279 in-corpus keys, master order. Writes references.bib only.
"""
import csv
import os
import re
import glob
import hashlib

ROOT = r'E:\GPS_Denied_SLR'
MP = os.path.join(ROOT, '07_manuscript')
DP = os.path.join(ROOT, '02_data_processed')
RECP = os.path.join(ROOT, '_MANUAL', 'abhishek', 'per_paper')
OUT = os.path.join(MP, 'references.bib')


def load(p):
    with open(p, encoding='utf-8-sig', newline='') as f:
        return [x for x in csv.DictReader(f)]


master = load(os.path.join(DP, 'MASTER_EVIDENCE.csv'))
sby = {x['id'].strip(): x for x in load(os.path.join(DP, 'screening_results.csv'))}

# REC YAML venue
venue = {}
for fp in glob.glob(os.path.join(RECP, 'REC_*.md')):
    rid = os.path.basename(fp)[:-3]
    head = open(fp, encoding='utf-8').read(1200)
    m = re.search(r'^venue:\s*(.*)$', head, re.M)
    v = (m.group(1).strip().strip('"').strip() if m else '')
    venue[rid] = v

DEFAULT = {'', 'nan', 'NaN', 'None', 'null', '-', 'N/A', 'TBD', 'unknown'}
BAD_RE = [re.compile(r'^[a-zA-Z]{1,3}$'), re.compile(r'^\(?[a-zA-Z]\)?$'), re.compile(r'^[A-Z]\.$')]
JUNK_MARK = ['this may be the author', 'electronic reprint', 'authorized licensed use',
             'downloaded on', 'arxiv:', '©', 'all rights reserved', 'personal use of this material']


def junk_title(t):
    if t is None:
        return True
    s = t.strip()
    if s == '' or s in DEFAULT or len(s) < 20:
        return True
    for r in BAD_RE:
        if r.match(s):
            return True
    low = s.lower()
    if any(j in low for j in JUNK_MARK):
        return True
    # mojibake / non-printable
    for ch in s:
        if ord(ch) < 32 or ord(ch) > 0x2122:
            return True
    if re.search(r'[ÂâÃ][\x80-\xBF]|ï¬|ï½|\ufffd|[¸˘ﬃﬁﬂ]', s):
        return True
    return False


def clean(s):
    s = re.sub(r'\s+', ' ', s or '').strip()
    return s.replace('{', '').replace('}', '')


def bib(s):
    return '{' + clean(s) + '}'


recs = []
junk_fixed = 0
for x in master:
    pid = x['id'].strip()
    sj = sby.get(pid, {})
    title = (x.get('title') or '').strip()
    if junk_title(title):
        cand = (sj.get('title') or '').strip()
        if cand and not junk_title(cand):
            title = cand
            junk_fixed += 1
        else:
            title = title if not junk_title(title) else 'NOT_REPORTED'
    # author
    au = (sj.get('authors') or '').strip()
    if au and au != 'NOT_REPORTED':
        au = ' and '.join(p.strip() for p in au.split(';') if p.strip())
    else:
        au = 'NOT_REPORTED'
    year = (x.get('year') or '').strip() or 'NOT_REPORTED'
    jr = venue.get(pid, '')
    jr = jr if jr and jr != 'NOT_REPORTED' else 'NOT_REPORTED'
    doi = (x.get('doi') or '').strip()
    if (not doi) or doi.endswith('.DOI') or 'ToBeAssigned' in doi:
        d2 = (sj.get('doi') or '').strip()
        doi = d2 if d2 and d2 != 'NOT_REPORTED' else 'NOT_REPORTED'
    recs.append({'key': pid, 'title': title, 'author': au, 'journal': jr,
                 'year': year, 'doi': doi})

blocks = []
for r in recs:
    blocks.append('@article{%s,\n  title = %s,\n  author = %s,\n  journal = %s,\n  year = %s,\n  doi = %s,\n}\n'
                  % (r['key'], bib(r['title']), bib(r['author']), bib(r['journal']), bib(r['year']), bib(r['doi'])))
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(blocks))

h = hashlib.sha256(open(OUT, 'rb').read()).hexdigest().upper()
print('WROTE', OUT)
print('entries', len(recs), 'bytes', os.path.getsize(OUT), 'sha256', h)
print('author NOT_REPORTED:', sum(1 for r in recs if r['author'] == 'NOT_REPORTED'))
print('journal NOT_REPORTED:', sum(1 for r in recs if r['journal'] == 'NOT_REPORTED'))
print('doi NOT_REPORTED:', sum(1 for r in recs if r['doi'] == 'NOT_REPORTED'))
print('titles junk-repaired:', junk_fixed)
cited = ['REC_0003', 'REC_0037', 'REC_0242', 'REC_0388', 'REC_0464', 'REC_0502', 'REC_0870',
         'REC_0960', 'REC_1006', 'REC_1019', 'REC_1025', 'REC_1026', 'REC_1069', 'REC_1253',
         'REC_1267', 'REC_1274', 'REC_1277', 'REC_1348']
keys = set(r['key'] for r in recs)
print('cited missing from new bib:', [c for c in cited if c not in keys])
print('SELF-AUDIT', 'PASS' if len(recs) == 279 and not [c for c in cited if c not in keys] else 'FAIL')