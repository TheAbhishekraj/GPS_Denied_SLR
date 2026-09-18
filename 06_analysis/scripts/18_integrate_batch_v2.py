"""Dynamic staging-batch integration v2: match -> verify -> integrate.

No hardcoded targets. Per staging PDF:
  1. DOI match against master/screened/priority (exact, normalized).
  2. Else title-sim >= 0.55 AND >= 1 shared author surname -> candidate.
  3. Fulltext dupe scan (DOI exact, or title >= 0.80) for every target.
  4. Fulltext already holds the id -> duplicate: drop staging copy.
  5. Else (with --apply): rename+move, flip priority done_Y_N, append log.
A .htm sibling whose stem is contained in a resolved ScienceDirect PDF name
is treated as a browser-page artifact and removed on --apply.
"""
import csv
import hashlib
import io
import re
import shutil
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import pymupdf

ROOT = Path(r'E:\GPS_Denied_SLR')
ST = ROOT / '08_docs' / 'downloads_staging'
FT = ROOT / '05_papers_fulltext'
APPLY = '--apply' in sys.argv

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


def col(keys, needle):
    for k in keys:
        if needle in k.lower():
            return k
    return None


master = load(ROOT / '02_data_processed' / 'extracted_master_v2.csv')
screened = load(ROOT / '02_data_processed' / 'screened_included_v2.csv')
priority = {r['id']: r for r in load(ROOT / '08_docs' / 'priority_300_download.csv')}

records = []
for src, rows in (('master', master), ('screened', screened)):
    ck, ct, ci = (col(rows[0].keys(), n) for n in ('doi', 'title', 'id'))
    for r in rows:
        records.append({'src': src, 'id': (r.get(ci) or '').strip(),
                        'doi': (r.get(ck) or '').strip().lower().rstrip('.'),
                        'tkey': tkey(r.get(ct) or ''),
                        'title': (r.get(ct) or '').strip(),
                        'authors': (r.get('authors') or '')})

doi_map = {}
for rec in records:
    if rec['doi']:
        doi_map.setdefault(rec['doi'], []).append(rec)


def surnames(authors_field):
    out = set()
    for seg in authors_field.split(';'):
        seg = seg.replace(' Jr', '').strip().rstrip('.')
        if not seg:
            continue
        first = seg.split()[0].strip(',.')
        if len(first) >= 3:
            out.add(first.lower())
    return out


def extract_doi(text):
    m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text[:8000], re.I)
    return m.group(0).rstrip('.,;)').lower() if m else ''


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


# --- match every staging pdf ----------------------------------------------
decisions = []
for p in sorted(ST.glob('*.pdf')):
    d = pymupdf.open(p)
    text = ' '.join((pg.get_text() or '') for pg in d)
    head = ' '.join(d[0].get_text()[:1500].split())
    doi = extract_doi(text)
    ids = {r['id'] for r in doi_map.get(doi, [])} if doi else set()
    how = 'doi'
    if len(ids) > 1:
        decisions.append({'file': p, 'status': 'ambiguous', 'doi': doi,
                          'ids': sorted(ids), 'how': how})
        continue
    if not ids:
        scored = sorted(((SequenceMatcher(None, tkey(head[:150]), r['tkey']).ratio(), r)
                         for r in records), key=lambda x: -x[0])
        strong = []
        for ratio, r in scored[:5]:
            if ratio < 0.55:
                break
            if surnames(r['authors']) & {w.lower() for w in head.split() if len(w) >= 3}:
                strong.append((ratio, r))
        if len({r['id'] for _, r in strong}) == 1:
            ids = {strong[0][1]['id']}
            how = f'title-sim-{strong[0][0]:.2f}+surname'
    if not ids:
        # fallback: record title appears verbatim on page 1 (references are
        # excluded so cited titles cannot produce false hits)
        page1key = tkey(d[0].get_text())
        hits = [r for r in records
                if len(r['tkey']) >= 40 and r['tkey'] in page1key]
        if len(hits) == 1:
            ids = {hits[0]['id']}
            how = 'title-in-page1'
    rid = next(iter(ids)) if ids else None
    decisions.append({'file': p, 'status': 'match' if rid else 'nomatch',
                      'doi': doi, 'ids': sorted(ids) if rid else [], 'how': how})

# --- fulltext duplicate scan ----------------------------------------------
tk_by_rid = {r['id']: r['tkey'] for r in records if r['tkey']}
doi_by_rid = {r['id']: r['doi'] for r in records if r['doi']}
ft_dois = {}
ft_text_cache = {}
for p in sorted(FT.glob('REC_*.pdf')):
    try:
        d = pymupdf.open(p)
        t = ''
        for pg in d:
            t += (pg.get_text() or '') + ' '
            if len(t) > 9000:
                break
    except Exception:
        continue
    ft_text_cache[p.name] = t
    doi = extract_doi(t)
    if doi:
        ft_dois[p.name] = doi

for dec in decisions:
    if dec['status'] not in ('match',):
        continue
    rid = dec['ids'][0]
    if (FT / f'{rid}.pdf').exists():
        dec['status'] = 'duplicate'
        continue
    dup = None
    for name, fdoi in ft_dois.items():
        if dec['doi'] and fdoi == dec['doi']:
            dup = f'{name} (doi)'
            break
    if not dup:
        for name, t in ft_text_cache.items():
            h = ' '.join(t[:400].split())
            if SequenceMatcher(None, tkey(h), tk_by_rid.get(rid, '')).ratio() >= 0.80:
                dup = f'{name} (title)'
                break
    if dup:
        dec['status'] = 'existing-dup-content'
        dec['dup'] = dup

print('===== DECISION TABLE =====')
for dec in decisions:
    print(f"\n{dec['file'].name}")
    print(f"  pages/present  doi={dec['doi'] or '-'}")
    print(f"  status={dec['status']}  ids={dec['ids']}  how={dec['how']}"
          + (f"  dup-of={dec['dup']}" if 'dup' in dec else ''))

# --- apply phase -----------------------------------------------------------
if not APPLY:
    print('\n(verify-only run; re-run with --apply to integrate)')
    sys.exit(0)

bad = [d for d in decisions if d['status'] in ('ambiguous',)]
assert not bad, f'ambiguous matches: {[b["ids"] for b in bad]}'
to_move = [d for d in decisions if d['status'] == 'match']
to_drop = [d for d in decisions if d['status'] in ('duplicate', 'existing-dup-content')]
print(f'\n--apply: {len(to_move)} to integrate, {len(to_drop)} staging dups to drop, '
      f'{sum(1 for d in decisions if d["status"] == "nomatch")} left unmatched')

# .htm sibling cleanup: stem contained in a resolved pdf's stem
resolved_stems = {d['file'].stem for d in decisions} | \
                 {p.stem for p in FT.glob('REC_*.pdf')}
for p in sorted(ST.iterdir()):
    if p.suffix.lower() == '.pdf':
        continue
    stem = p.stem
    hit = next((s for s in resolved_stems if stem.lower() in s.lower()), None)
    if hit and p.stat().st_size > 0:
        p.unlink()
        print(f'removed page artifact: {p.name} (matches {hit})')
    else:
        print(f'left in staging (no pdf match): {p.name}')

hashes = {}
for dec in to_move:
    rid = dec['ids'][0]
    src, dst = dec['file'], FT / f'{rid}.pdf'
    assert not dst.exists()
    hashes[rid] = sha256(src)
    shutil.move(str(src), str(dst))
    assert dst.exists() and dst.stat().st_size > 0
    print(f'{src.name[:60]:<60} -> {rid}.pdf')
for dec in to_drop:
    hashes[dec['ids'][0]] = sha256(dec['file'])
    dec['file'].unlink()
    print(f'dropped staging duplicate: {dec["file"].name} ({dec["status"]})')

# priority CSV: set done_Y_N=Y for all resolved ids (moved + dropped)
ids_all = [d['ids'][0] for d in to_move + to_drop]
ppath = ROOT / '08_docs' / 'priority_300_download.csv'
raw = ppath.read_bytes()
try:
    text = raw.decode('utf-8'); enc = 'utf-8'
except UnicodeDecodeError:
    text = raw.decode('cp1252'); enc = 'cp1252'
nl = '\r\n' if '\r\n' in text[:2000] else '\n'
rows = list(csv.reader(io.StringIO(text)))
header = rows[0]
i_id, i_done = header.index('id'), header.index('done_Y_N')
new_rows = []
changed = []
for r in rows[1:]:
    if r and len(r) > i_id and r[i_id] in ids_all:
        r2 = list(r)
        if r2[i_done] != 'Y':
            r2[i_done] = 'Y'
            changed.append(r2[i_id])
        new_rows.append(r2)
    else:
        new_rows.append(r)
assert set(changed) == set(ids_all), f'flips {changed} vs {ids_all}'
buf = io.StringIO()
w = csv.writer(buf, lineterminator=nl)
w.writerow(header); w.writerows(new_rows)
new_text = buf.getvalue()
if not text.endswith(nl) and new_text.endswith(nl):
    new_text = new_text[:-len(nl)]
recheck = list(csv.reader(io.StringIO(new_text)))
assert len(recheck) == len(rows)
for o, n in zip(rows, recheck):
    if o == n:
        continue
    assert o and len(o) > i_id and o[i_id] in ids_all
    assert [k for k in range(len(header)) if o[k] != n[k]] == [i_done]
ppath.write_bytes(new_text.encode(enc))
print(f'priority CSV: done_Y_N=Y for {len(changed)} ids')

# rename_log: append provenance rows
lpath = ROOT / '08_docs' / 'rename_log.csv'
with open(lpath, 'a', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n')
    for dec in to_move:
        w.writerow([dec['file'].name, dec['ids'][0], 'renamed+moved',
                    hashes[dec['ids'][0]], dec['how']])
    for dec in to_drop:
        w.writerow([dec['file'].name, dec['ids'][0],
                    f'duplicate-removed ({dec["status"]})',
                    hashes[dec['ids'][0]], dec['how']])
print(f'rename_log.csv: +{len(to_move) + len(to_drop)} rows')

print('\nDONE.')
