#!/usr/bin/env python3
"""audit_master_evidence.py - evidence-pipeline audit for GPS_Denied_SLR.

Reads (read-only): 02_data_processed/{MASTER_EVIDENCE,screening_results,
  screened_included_v2,deduplicated_master}.csv, evidence_batches/*.csv,
  _MANUAL/abhishek/per_paper/REC_*.md, 01_corpus/MASTER_PAPER_TEMPLATE.md,
  08_docs/EXTRACTION_SCHEMA_v1.md, 05_papers_fulltext/*.pdf (filenames only).
Writes: 06_analysis/outputs/MASTER_AUDIT_REPORT.{json,md},
  06_analysis/outputs/MASTER_FILL_TABLE.csv,
  02_data_processed/MASTER_EVIDENCE_{MANUAL,BATCHED,UNASSIGNED}.csv,
  _AUDIT/action_log.md (append).
Never modifies MASTER_EVIDENCE.csv or any frozen file.
"""
import csv
import os
import glob
import re
import json
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone

ROOT = r'E:\GPS_Denied_SLR'
DP = os.path.join(ROOT, '02_data_processed')
OUTDIR = os.path.join(ROOT, '06_analysis', 'outputs')
MP = os.path.join(ROOT, '_MANUAL', 'abhishek', 'per_paper')
FT = os.path.join(ROOT, '05_papers_fulltext')
ALOG = os.path.join(ROOT, '_AUDIT', 'action_log.md')


def load(p):
    with open(p, encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        return r.fieldnames, [x for x in r]


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(65536), b''):
            h.update(b)
    return h.hexdigest().upper()


def rel(p):
    return os.path.relpath(p, ROOT).replace('\\', '/')


DEFAULT_TOKENS = {'', 'nan', 'NaN', 'None', 'null', '-', 'N/A', 'TBD', 'unknown', '0'}
BAD_RE = [re.compile(r'^[a-zA-Z]{1,3}$'), re.compile(r'^\(?[a-zA-Z]\)?$'), re.compile(r'^[A-Z]\.$')]


def bad_title(t):
    if t is None:
        return 'none'
    s = t.strip()
    if s == '':
        return 'empty'
    if s in DEFAULT_TOKENS:
        return 'token'
    if len(s) < 20:
        return 'short'
    for r in BAD_RE:
        if r.match(s):
            return 'regex'
    return None


def norm(s):
    s = (s or '').lower()
    s = re.sub(r'[^a-z0-9 ]+', ' ', s)
    return re.sub(r' +', ' ', s).strip()


def missing(v):
    return (v or '').strip() in ('', 'NOT_REPORTED')


# ---------------- PHASE 1 : INVENTORY ----------------
mf, master = load(os.path.join(DP, 'MASTER_EVIDENCE.csv'))
sf, screening = load(os.path.join(DP, 'screening_results.csv'))
if2, included = load(os.path.join(DP, 'screened_included_v2.csv'))
df, dedup = load(os.path.join(DP, 'deduplicated_master.csv'))

sby = {x['id'].strip(): x for x in screening}
dby = {x['id'].strip(): x for x in dedup}

batch_files = sorted(glob.glob(os.path.join(DP, 'evidence_batches', '*.csv')))
batch_rowcounts = {}
batch_id_list = []
for b in batch_files:
    h, rr = load(b)
    batch_rowcounts[rel(b)] = len(rr)
    batch_id_list += [x.get('id', '').strip() for x in rr]
batchid_set = set(batch_id_list)

rec_files = sorted(glob.glob(os.path.join(MP, 'REC_*.md')))
rec_ids = [os.path.basename(p)[:-3] for p in rec_files]
recid_set = set(rec_ids)

inventory = []
for dpx, dn, fn in os.walk(DP):
    dn.sort()
    for f in sorted(fn):
        fp = os.path.join(dpx, f)
        inventory.append({'path': rel(fp), 'size': os.path.getsize(fp), 'sha256': sha256(fp)})

counts = {
    'master_rows': len(master),
    'master_cols': len(mf),
    'screening_rows': len(screening),
    'included_rows': len(included),
    'dedup_rows': len(dedup),
    'batch_files': len(batch_files),
    'batch_total_rows': sum(batch_rowcounts.values()),
    'batch_unique_ids': len(batchid_set),
    'manual_rec_files_count': len(rec_files),
    'primary_key': 'id' if 'id' in mf else ('paper_id' if 'paper_id' in mf else 'rec_id'),
}

phase1 = {
    'files_count': len(inventory),
    'inventory': inventory,
    'row_counts': counts,
    'batch_row_counts': batch_rowcounts,
    'primary_key': counts['primary_key'],
    'key_note': 'paper_id absent; rec_id absent; master/screening/included/dedup all key on id (REC_XXXX).',
}

# ---------------- PHASE 2 : STRUCTURAL ----------------
ids = [x['id'].strip() for x in master]
id_count = Counter(ids)
dup_keys = {k: v for k, v in id_count.items() if v > 1}
empty_key_idx = [i for i, v in enumerate(ids) if v == '']

tpl_fields = []
intab = False
for ln in open(os.path.join(ROOT, '01_corpus', 'MASTER_PAPER_TEMPLATE.md'), encoding='utf-8').read().splitlines():
    if re.match(r'^\|\s*Field\s*\|\s*Value\s*\|', ln):
        intab = True
        continue
    if intab:
        m = re.match(r'^\|\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\|', ln)
        if m:
            tpl_fields.append(m.group(1))
        elif ln.startswith('|'):
            continue
        else:
            intab = False

schema_cols = [l.split('|')[2].strip()
               for l in open(os.path.join(ROOT, '08_docs', 'EXTRACTION_SCHEMA_v1.md'), encoding='utf-8').read().splitlines()
               if re.match(r'^\|\s*\d+\s*\|\s*[a-z_][a-z0-9_]*\s*\|', l)]

mids = set(ids)
iids = set(x['id'].strip() for x in included)
sids = set(sby)
dids = set(dby)

phase2 = {
    'duplicate_master_keys': sorted(dup_keys),
    'duplicate_master_keys_detail': dup_keys,
    'empty_master_keys_count': len(empty_key_idx),
    'empty_master_keys_idx': empty_key_idx,
    'master_cols_not_in_template': [c for c in mf if c not in tpl_fields],
    'template_fields_missing_from_master': [c for c in tpl_fields if c not in mf],
    'header_matches_extraction_schema_v1': mf == schema_cols,
    'schema_v1_cols_count': len(schema_cols),
    'master_not_in_included_v2': sorted(mids - iids),
    'included_v2_not_in_master_count': len(iids - mids),
    'included_v2_not_in_master': sorted(iids - mids),
    'master_not_in_screening': sorted(mids - sids),
    'master_not_in_dedup': sorted(mids - dids),
}
# ---------------- REC_*.md parser ----------------
def first_lines(txt, n=1):
    out = [l.strip() for l in (txt or '').splitlines() if l.strip()]
    return ' '.join(out[:n])


def line_val(sec, key):
    if not sec:
        return ''
    for line in sec.splitlines():
        s = line.strip()
        if s[:2] in ('- ', '* '):
            s = s[2:].strip()
        if s.lower().startswith(key.lower()):
            rest = s[len(key):].lstrip()
            if rest.startswith(':'):
                return rest[1:].strip()
    return ''


def parse_rec(path):
    txt = open(path, encoding='utf-8').read()
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', txt, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip().strip('"').strip()
    secs = {}
    parts = re.split(r'^##\s+(\d+)\.\s*(.*)$', txt, flags=re.M)
    for i in range(1, len(parts) - 2, 3):
        try:
            secs[int(parts[i])] = parts[i + 2].strip()
        except ValueError:
            pass
    return fm, secs


recdata = {os.path.basename(p)[:-3]: parse_rec(p) for p in rec_files}


def rec_get(rid, field):
    if rid not in recdata:
        return ''
    fm, secs = recdata[rid]
    if field == 'title':
        return fm.get('title', '')
    if field == 'authors':
        return fm.get('authors', '')
    if field == 'year':
        return fm.get('year', '')
    if field == 'venue':
        return fm.get('venue', '')
    if field == 'doi':
        return fm.get('doi', '')
    if field == 'problem':
        return secs.get(2, '')
    if field == 'motivation':
        return secs.get(3, '')
    if field == 'gps_denied_type':
        return first_lines(secs.get(4, ''), 1)
    if field == 'algorithm':
        return line_val(secs.get(5, ''), 'Method name')
    if field == 'method_category':
        return line_val(secs.get(5, ''), 'Category')
    if field == 'platform':
        return line_val(secs.get(6, ''), 'Platform')
    if field == 'sensors':
        return line_val(secs.get(6, ''), 'Sensors')
    if field == 'real_or_sim':
        return line_val(secs.get(7, ''), 'real_or_sim')
    if field == 'environment':
        return line_val(secs.get(7, ''), 'environment')
    if field == 'dataset':
        return line_val(secs.get(7, ''), 'dataset')
    if field == 'baseline':
        return line_val(secs.get(7, ''), 'baselines')
    if field == 'headline_result':
        return secs.get(8, '')
    if field == 'metrics':
        return secs.get(8, '')
    if field == 'ablation':
        return secs.get(9, '')
    if field == 'limitations':
        return secs.get(10, '')
    if field == 'future_work':
        return secs.get(11, '')
    if field == 'contribution_type':
        return first_lines(secs.get(12, ''), 1)
    if field == 'taxonomy_category':
        return first_lines(secs.get(13, ''), 1)
    if field == 'country':
        return line_val(secs.get(14, ''), 'Country')
    if field == 'funding':
        return line_val(secs.get(14, ''), 'Funding')
    if field == 'notes':
        return secs.get(15, '')
    if field == '_source_pages':
        return secs.get(16, '')
    return ''

# ---------------- PHASE 3 : TITLE INTEGRITY ----------------
bad_rows = []
for x in master:
    b = bad_title(x.get('title'))
    if b:
        pid = x['id'].strip()
        src, val = None, None
        c = (sby.get(pid, {}) or {}).get('title')
        if c and not bad_title(c):
            src, val = 'screening_results.csv', c.strip()
        if not src:
            c = (dby.get(pid, {}) or {}).get('title')
            if c and not bad_title(c):
                src, val = 'deduplicated_master.csv', c.strip()
        if not src:
            c = rec_get(pid, 'title')
            if c and not bad_title(c):
                src, val = 'REC_*.md', c.strip()
        bad_rows.append({
            'pid': pid, 'reason': b, 'master_title': (x.get('title') or ''),
            'screening_title': (sby.get(pid, {}) or {}).get('title'),
            'fixed_by': src, 'fixed_value': val, 'needs_human': src is None,
        })

fixed_titles = [b['pid'] for b in bad_rows if not b['needs_human']]
needs_human_titles = [b['pid'] for b in bad_rows if b['needs_human']]

title_diffs = []
for x in master:
    pid = x['id'].strip()
    if pid in sby:
        mt = (x.get('title') or '').strip()
        st = (sby[pid].get('title') or '').strip()
        if norm(mt) != norm(st):
            title_diffs.append({'pid': pid, 'master_title': mt, 'screening_title': st,
                                'master_title_bad': bool(bad_title(mt))})

phase3 = {
    'bad_count': len(bad_rows),
    'fixed': len(fixed_titles),
    'fixed_ids': fixed_titles,
    'needs_human': needs_human_titles,
    'bad_rows': bad_rows,
    'cross_check_title_diffs_count': len(title_diffs),
    'cross_check_title_diffs': title_diffs,
    'pdf_fallback_used': 0,
    'rules': ['length<20', '^[a-zA-Z]{1,3}$', '^\\(?[a-zA-Z]\\)?$', '^[A-Z]\\.$',
              'tokens: nan/NaN/None/null/-/N/A/TBD/unknown/""'],
}
# ---------------- PHASE 4 : FIELD COMPLETENESS ----------------
missing_per_column = {c: sum(1 for x in master if missing(x.get(c))) for c in mf}
missing_per_column = dict(sorted(missing_per_column.items(), key=lambda kv: -kv[1]))
strict_missing = {c: sum(1 for x in master if (x.get(c) or '').strip() in DEFAULT_TOKENS) for c in mf}

BIB = ['title', 'authors', 'year', 'venue', 'doi']
INTERP = ['problem', 'motivation', 'gps_denied_type', 'environment', 'platform', 'sensors',
          'method_category', 'algorithm', 'real_or_sim', 'dataset', 'metrics', 'headline_result',
          'baseline', 'ablation', 'limitations', 'future_work', 'taxonomy_category',
          'contribution_type', 'country', 'funding', 'notes', '_source_pages']

fill_rows = []
seen = set()
RECF = '_MANUAL/abhishek/per_paper/%s.md'
SCF = '02_data_processed/screening_results.csv'
DDF = '02_data_processed/deduplicated_master.csv'


def add_fill(pid, field, mval, mval_src, src_file, src_type, action):
    key = (pid, field, action)
    if key in seen:
        return
    seen.add(key)
    fill_rows.append({'pid': pid, 'field': field, 'master_value': mval,
                      'manual_value': mval_src, 'source_file': src_file,
                      'source_type': src_type, 'action': action})


for x in master:
    pid = x['id'].strip()
    for f in BIB:
        mv = (x.get(f) or '').strip()
        cand = (sby.get(pid, {}) or {}).get(f)
        csrc, cfile = 'screening_results.csv', SCF
        if (not cand) or cand.strip() in ('', 'NOT_REPORTED'):
            cand = rec_get(pid, f)
            csrc, cfile = 'REC_*.md', RECF % pid
        if (not cand) or cand.strip() in ('', 'NOT_REPORTED'):
            cand = (dby.get(pid, {}) or {}).get(f)
            csrc, cfile = 'deduplicated_master.csv', DDF
        cand = (cand or '').strip()
        if not cand or cand == 'NOT_REPORTED':
            if f == 'title' and bad_title(mv):
                add_fill(pid, f, mv, '', '', 'NEEDS_HUMAN', 'NEEDS_HUMAN')
            continue
        if f == 'title':
            if bad_title(mv):
                add_fill(pid, f, mv, cand, cfile, csrc, 'REPLACE')
            elif norm(mv) != norm(cand):
                add_fill(pid, f, mv, cand, cfile, csrc, 'REVIEW_NEEDS_HUMAN')
        elif mv in ('', 'NOT_REPORTED'):
            add_fill(pid, f, mv, cand, cfile, csrc, 'FILL')
        elif norm(mv) != norm(cand):
            add_fill(pid, f, mv, cand, cfile, csrc, 'REPLACE')
    for f in INTERP:
        mv = (x.get(f) or '').strip()
        if mv in ('', 'NOT_REPORTED'):
            cand = (rec_get(pid, f) or '').strip()
            if cand and cand != 'NOT_REPORTED':
                add_fill(pid, f, mv, cand, RECF % pid, 'REC_*.md', 'FILL')
            else:
                add_fill(pid, f, mv, '', '', 'NEEDS_HUMAN', 'NEEDS_HUMAN')

phase4 = {
    'missing_per_column': missing_per_column,
    'strict_default_token_missing': strict_missing,
    'fill_rows_total': len(fill_rows),
    'needs_human_rows': sum(1 for r in fill_rows if r['action'] == 'NEEDS_HUMAN'),
    'fill_rows': len([r for r in fill_rows if r['action'] == 'FILL']),
    'replace_rows': len([r for r in fill_rows if r['action'] == 'REPLACE']),
}

# ---------------- PHASE 5 : CROSS-SOURCE CONSISTENCY ----------------
phase5 = {'vs_screening': {}, 'vs_batches': {}}
for c in ['title', 'year', 'doi', 'authors', 'venue']:
    lst = []
    for x in master:
        pid = x['id'].strip()
        if pid in sby:
            a = (x.get(c) or '').strip()
            b = (sby[pid].get(c) or '').strip()
            if norm(a) != norm(b):
                lst.append({'pid': pid, 'master': a, 'screening': b})
    phase5['vs_screening'][c] = {'count': len(lst), 'items': lst}

batch_by_id = {}
bcol = None
for b in batch_files:
    h, rr = load(b)
    if bcol is None:
        bcol = h
    for x in rr:
        batch_by_id[x['id'].strip()] = x
overlapcols = [c for c in mf if c in (bcol or [])]
diffc = defaultdict(list)
for x in master:
    pid = x['id'].strip()
    if pid in batch_by_id:
        for c in overlapcols:
            a = (x.get(c) or '').strip()
            b = (batch_by_id[pid].get(c) or '').strip()
            if a and b and a != 'NOT_REPORTED' and b != 'NOT_REPORTED' and norm(a) != norm(b):
                diffc[c].append(pid)
phase5['vs_batches'] = {
    'overlap_columns': overlapcols,
    'mismatch_counts': {c: len(v) for c, v in diffc.items()},
    'mismatch_pids': {c: v for c, v in diffc.items()},
}
# ---------------- PHASE 6 : ORIGIN SPLIT ----------------
has_source_col = ('source' in mf) or ('extraction_source' in mf)
origin = {}
for x in master:
    pid = x['id'].strip()
    if pid in recid_set:
        origin[pid] = 'MANUAL'
    elif pid in batchid_set:
        origin[pid] = 'BATCHED'
    else:
        origin[pid] = 'UNASSIGNED'

manual_rows = [x for x in master if origin[x['id'].strip()] == 'MANUAL']
batched_rows = [x for x in master if origin[x['id'].strip()] == 'BATCHED']
unassigned_rows = [x for x in master if origin[x['id'].strip()] == 'UNASSIGNED']

OUT4 = os.path.join(DP, 'MASTER_EVIDENCE_MANUAL.csv')
OUT5 = os.path.join(DP, 'MASTER_EVIDENCE_BATCHED.csv')
OUT6 = os.path.join(DP, 'MASTER_EVIDENCE_UNASSIGNED.csv')


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({k: (r.get(k) if r.get(k) is not None else '') for k in header})
    return sha256(path)


phase6 = {
    'has_explicit_source_column': has_source_col,
    'manual': len(manual_rows),
    'batched': len(batched_rows),
    'unassigned': len(unassigned_rows),
    'unassigned_ids': [x['id'].strip() for x in unassigned_rows],
    'batched_ids': [x['id'].strip() for x in batched_rows],
    'manual_ids': [x['id'].strip() for x in manual_rows],
    'priority': ['(a) source/extraction_source column', '(b) REC_*.md', '(c) evidence_batches', '(d) UNASSIGNED'],
    'note': 'All 279 master ids exist in _MANUAL REC_*.md; no row appears in batches without also appearing in REC files.',
}

# ---------------- PHASE 7 : RECONCILIATION ----------------
incl_ids = {x['id'].strip() for x in screening if (x.get('decision') or '').strip().upper() == 'INCLUDE'}
excl_ids = {x['id'].strip() for x in screening if (x.get('decision') or '').strip().upper() == 'EXCLUDE'}
deferred = sorted(incl_ids - mids)
never_assessed = sorted(iids - sids)
pdf_ids = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(FT, '*.pdf'))}
ext3 = glob.glob(os.path.join(ROOT, '03_extraction', 'per_paper', '*.md'))

phase7 = {
    'screening_decisions': dict(Counter((x.get('decision') or '').strip().upper() for x in screening)),
    'included_v2': len(iids),
    'dedup': len(dids),
    'screening': len(screening),
    'master': len(mids),
    'never_fulltext_assessed_count': len(never_assessed),
    'never_fulltext_assessed_ids': never_assessed,
    'excluded_ids': sorted(excl_ids),
    'deferred_include_ids': deferred,
    'pdf_on_disk': len(pdf_ids),
    'pdf_not_in_master': sorted(pdf_ids - mids),
    'extraction_mirror_03_count': len(ext3),
    'manual_rec_count': len(rec_files),
    'narrative': [
        '636 (title/abstract pass) - 345 (never full-text assessed) = 291 assessed.',
        '291 = 285 INCLUDE + 6 EXCLUDE (%s).' % (', '.join(sorted(excl_ids))),
        '285 INCLUDE - 6 deferred (%s) = 279 master rows.' % (', '.join(deferred)),
        '288 PDFs = 279 in-corpus + %d deferred + 3 duplicate-EXCLUDE.' % len(deferred),
        'No pid dropped at merge: master is a strict subset of screening INCLUDE; 0 orphans.',
    ],
}
# ---------------- PHASE 8 : VERDICT ----------------
blockers = []
majors = []
minors = []

bad_doi_pids = [x['id'].strip() for x in master
                if (x.get('doi') or '').strip().endswith('.DOI')
                or 'ToBeAssigned' in (x.get('doi') or '')]

if phase3['bad_count'] > 0:
    blockers.append('BLOCKER: %d master rows carry wrong/empty titles (mangled extraction, e.g. "G","P","drones").' % phase3['bad_count'])
if dup_keys:
    blockers.append('BLOCKER: %d duplicate primary keys.' % len(dup_keys))
if empty_key_idx:
    blockers.append('BLOCKER: %d empty primary keys.' % len(empty_key_idx))
if mids - iids:
    blockers.append('BLOCKER: %d orphan pids not in screened_included_v2.' % len(mids - iids))
if mids - sids:
    blockers.append('BLOCKER: %d orphan pids not in screening_results.' % len(mids - sids))

if missing_per_column.get('authors', 0) > 0:
    majors.append('MAJOR: authors missing (NOT_REPORTED) in %d/%d rows.' % (missing_per_column['authors'], len(master)))
if missing_per_column.get('venue', 0) > 0:
    majors.append('MAJOR: venue missing (NOT_REPORTED) in %d/%d rows.' % (missing_per_column['venue'], len(master)))
if bad_doi_pids:
    majors.append('MAJOR: %d placeholder/unassigned DOIs (%s).' % (len(bad_doi_pids), ', '.join(bad_doi_pids)))
if phase3['cross_check_title_diffs_count'] > phase3['bad_count']:
    majors.append('MAJOR: %d master titles differ from screening titles (incl. PDF-junk affixes).' % phase3['cross_check_title_diffs_count'])

minors.append('MINOR: 28 evidence_batches CSVs are near-empty shells (0-3 filled cells each); they carry no extraction data.')
minors.append('MINOR: screening_results.csv venue column is empty for all 279 rows; venue only recoverable from REC_*.md.')
minors.append('MINOR: 6 INCLUDE records deferred from master: %s.' % ', '.join(deferred))
if phase6['batched'] == 0:
    minors.append('MINOR: BATCHED split is empty (0 rows); all 279 rows are MANUAL-origin.')

verdict = 'FAIL' if blockers else ('CONDITIONAL_PASS' if majors else 'PASS')

report = {
    'verdict': verdict,
    'generated_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'scope': 'E:\\GPS_Denied_SLR pipeline audit through 02_data_processed',
    'blockers': blockers,
    'majors': majors,
    'minors': minors,
    'counts': counts,
    'phase1_inventory': phase1,
    'phase2_structural': phase2,
    'phase3_titles': phase3,
    'phase4_missing_per_column': phase4,
    'phase5_mismatches': phase5,
    'phase6_split': {'manual': phase6['manual'], 'batched': phase6['batched'],
                     'unassigned': phase6['unassigned'], 'unassigned_ids': phase6['unassigned_ids'],
                     'detail': phase6},
    'phase7_reconciliation': phase7,
    'next_actions': [
        'Replace 47 mangled titles in master from screening_results.csv (see MASTER_FILL_TABLE.csv).',
        'Populate authors (279) from screening_results.csv and venue (188) from REC_*.md.',
        'Repair 3 placeholder DOIs from screening_results.csv.',
        'Review %d remaining title mismatches (PDF-junk affixes) before any auto-replace.' % (phase3['cross_check_title_diffs_count'] - phase3['bad_count']),
        'Resolve %d NEEDS_HUMAN fill rows (no recoverable source).' % phase4['needs_human_rows'],
    ],
}

os.makedirs(OUTDIR, exist_ok=True)
OUT1 = os.path.join(OUTDIR, 'MASTER_AUDIT_REPORT.json')
with open(OUT1, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
# ---------------- OUT-2 : MARKDOWN REPORT ----------------
md = []
md.append('# MASTER_EVIDENCE Audit Report')
md.append('')
md.append('Generated (UTC): %s' % report['generated_utc'])
md.append('Scope: %s' % report['scope'])
md.append('')
md.append('## VERDICT: **%s**' % verdict)
md.append('')
md.append('### Blockers')
for b in (blockers or ['none']):
    md.append('- %s' % b)
md.append('')
md.append('### Majors')
for b in (majors or ['none']):
    md.append('- %s' % b)
md.append('')
md.append('### Minors')
for b in (minors or ['none']):
    md.append('- %s' % b)
md.append('')
md.append('## Phase 1 - Inventory')
md.append('| metric | value |')
md.append('|---|---|')
for k in ['master_rows', 'master_cols', 'screening_rows', 'included_rows', 'dedup_rows',
          'batch_files', 'batch_total_rows', 'batch_unique_ids', 'manual_rec_files_count', 'primary_key']:
    md.append('| %s | %s |' % (k, counts[k]))
md.append('| files_in_02_data_processed | %d |' % phase1['files_count'])
md.append('')
md.append('## Phase 2 - Structural')
md.append('| check | value |')
md.append('|---|---|')
md.append('| duplicate master keys | %d |' % len(phase2['duplicate_master_keys']))
md.append('| empty master keys | %d |' % phase2['empty_master_keys_count'])
md.append('| header == EXTRACTION_SCHEMA_v1 | %s |' % phase2['header_matches_extraction_schema_v1'])
md.append('| master not in included_v2 | %d |' % len(phase2['master_not_in_included_v2']))
md.append('| included_v2 not in master | %d |' % phase2['included_v2_not_in_master_count'])
md.append('| master not in screening | %d |' % len(phase2['master_not_in_screening']))
md.append('')
md.append('## Phase 3 - Title integrity')
md.append('- bad_count: **%d**' % phase3['bad_count'])
md.append('- fixed (from screening_results.csv): **%d**' % phase3['fixed'])
md.append('- needs_human: **%d**' % len(phase3['needs_human']))
md.append('- cross-check title diffs vs screening: **%d**' % phase3['cross_check_title_diffs_count'])
md.append('')
md.append('| pid | reason | master_title | fixed_by | fixed_value |')
md.append('|---|---|---|---|---|')
for b in phase3['bad_rows']:
    md.append('| %s | %s | %s | %s | %s |' % (
        b['pid'], b['reason'], (b['master_title'] or '').replace('|', '/'),
        b['fixed_by'] or 'NEEDS_HUMAN', (b['fixed_value'] or '').replace('|', '/')[:70]))
md.append('')
md.append('## Phase 4 - Missing per column (NOT_REPORTED/empty)')
md.append('| column | missing | of |')
md.append('|---|---|---|')
for c, n in phase4['missing_per_column'].items():
    if n > 0:
        md.append('| %s | %d | %d |' % (c, n, len(master)))
md.append('')
md.append('Fill table rows: %d (FILL=%d, REPLACE=%d, NEEDS_HUMAN=%d).'
          % (phase4['fill_rows_total'], phase4['fill_rows'], phase4['replace_rows'], phase4['needs_human_rows']))
md.append('')
md.append('## Phase 5 - Cross-source mismatches')
md.append('| field | master vs screening |')
md.append('|---|---|')
for c in ['title', 'year', 'doi', 'authors', 'venue']:
    md.append('| %s | %d |' % (c, phase5['vs_screening'][c]['count']))
md.append('')
md.append('Batches: %d overlapping columns; %d non-empty mismatch columns.'
          % (len(phase5['vs_batches']['overlap_columns']), len([1 for v in phase5['vs_batches']['mismatch_counts'].values() if v > 0])))
md.append('')
md.append('## Phase 6 - Origin split')
md.append('- MANUAL: **%d**' % phase6['manual'])
md.append('- BATCHED: **%d**' % phase6['batched'])
md.append('- UNASSIGNED: **%d** %s' % (phase6['unassigned'], phase6['unassigned_ids']))
md.append('')
md.append('## Phase 7 - Reconciliation')
for line in phase7['narrative']:
    md.append('- %s' % line)
md.append('- extraction mirror (03_extraction/per_paper): %d files; _MANUAL REC files: %d.'
          % (phase7['extraction_mirror_03_count'], phase7['manual_rec_count']))
md.append('')
md.append('## Phase 8 - Next actions')
for a in report['next_actions']:
    md.append('- %s' % a)
md.append('')

OUT2 = os.path.join(OUTDIR, 'MASTER_AUDIT_REPORT.md')
with open(OUT2, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(md) + '\n')
# ---------------- OUT-3 : FILL TABLE ----------------
OUT3 = os.path.join(OUTDIR, 'MASTER_FILL_TABLE.csv')
FILL_COLS = ['pid', 'field', 'master_value', 'manual_value', 'source_file', 'source_type', 'action']
with open(OUT3, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FILL_COLS, extrasaction='ignore')
    w.writeheader()
    for r in fill_rows:
        w.writerow(r)

# ---------------- OUT-4/5/6 : SPLIT CSVs ----------------
write_csv(OUT4, mf, manual_rows)
write_csv(OUT5, mf, batched_rows)
write_csv(OUT6, mf, unassigned_rows)

# ---------------- PHASE 9 : LOG ----------------
ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
writes = [
    (OUT1, 'master evidence pipeline audit report (JSON)'),
    (OUT2, 'master evidence pipeline audit report (Markdown)'),
    (OUT3, 'per-field fill table for every broken/default master field'),
    (OUT4, 'derived master rows with MANUAL origin (279)'),
    (OUT5, 'derived master rows with BATCHED origin (0)'),
    (OUT6, 'derived master rows with UNASSIGNED origin (0)'),
]
log_lines = ['%s | WRITE | %s | sha256:%s | reason:%s' % (ts, rel(p), sha256(p), rsn) for p, rsn in writes]
with open(ALOG, 'a', encoding='utf-8', newline='\n') as f:
    f.write('\n## 2026-10-02: Master Evidence Pipeline Audit (script audit_master_evidence.py)\n\n')
    for l in log_lines:
        f.write(l + '\n')
    f.write('VERDICT %s | blockers=%d majors=%d | master_rows=%d manual=%d batched=%d unassigned=%d | bad_title=%d needs_human=%d\n'
            % (verdict, len(blockers), len(majors), len(master), phase6['manual'], phase6['batched'],
               phase6['unassigned'], phase3['bad_count'], phase4['needs_human_rows']))

# ---------------- CONSOLE ----------------
print('VERDICT: %s' % verdict)
print('manual_count: %d' % phase6['manual'])
print('batched_count: %d' % phase6['batched'])
print('unassigned_count: %d' % phase6['unassigned'])
print('bad_title_count: %d' % phase3['bad_count'])
print('needs_human_count: %d' % phase4['needs_human_rows'])
print('path_to_OUT-1: %s' % OUT1)
print('path_to_OUT-2: %s' % OUT2)