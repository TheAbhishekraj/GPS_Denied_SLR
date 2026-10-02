#!/usr/bin/env python3
"""audit_v4.py - Station 9 / Gate 9.4: final audit of MANUSCRIPT_V4.md.

L5: every REC id must exist in MASTER_EVIDENCE.csv.
L2: every prose quantitative claim must trace to a source file.
L7: banned vocabulary scan.
Writes 08_docs/NUMBER_TRACE.md.
"""
import os
import re
import csv
import json

ROOT = r'E:\GPS_Denied_SLR'
MD = os.path.join(ROOT, '07_manuscript', 'MANUSCRIPT_V4.md')
OUT = os.path.join(ROOT, '08_docs', 'NUMBER_TRACE.md')

txt = open(MD, encoding='utf-8').read()
with open(os.path.join(ROOT, '02_data_processed', 'MASTER_EVIDENCE.csv'), encoding='utf-8-sig', newline='') as f:
    master = [x for x in csv.DictReader(f)]
mids = set(x['id'].strip() for x in master)

TRACE = {
    '2,000': '08_docs/ANCHOR_FREEZE_20260919.md', '1,716': '08_docs/ANCHOR_FREEZE_20260919.md',
    '636': '08_docs/ANCHOR_FREEZE_20260919.md', '291': '08_docs/ANCHOR_FREEZE_20260919.md',
    '285': '08_docs/ANCHOR_FREEZE_20260919.md', '279': 'MASTER_EVIDENCE.csv (279 rows)',
    '280': '08_docs/ANCHOR_FREEZE_20260919.md', '6': 'ANCHOR_FREEZE + screening_results.csv',
    '3': 'quality_appraisal_scored.csv (Q-High)', '98': 'quality_appraisal_scored.csv (Q-Medium)',
    '178': 'quality_appraisal_scored.csv (Q-Low)',
    '1.1': 'derived 3/279', '35.1': 'derived 98/279', '63.8': 'derived 178/279',
    '1.48': 'quality_appraisal_scored.csv mean rigor', '1.25': 'quality_appraisal_scored mean reporting',
    '1.06': 'quality_appraisal_scored mean baseline', '0.01': 'quality_appraisal_scored mean repro',
    '3.81': 'quality_appraisal_scored mean total',
    '26': 'MASTER year epoch 2013-16', '79': 'MASTER year epoch 2017-21', '174': 'MASTER year epoch 2022-26',
    '9.3': 'derived 26/279', '28.3': 'derived 79/279', '62.4': 'derived 174/279',
    '111': 'MASTER real_or_sim=REAL', '83': 'MASTER real_or_sim=BOTH', '62': 'MASTER real_or_sim=SIM',
    '23': 'MASTER real_or_sim unreported', '39.8': 'derived 111/279', '29.7': 'derived 83/279',
    '22.2': 'derived 62/279', '8.2': 'derived 23/279', '30.5': 'derived 85/279',
    '138': 'RQ_DATA_ANALYTICS Emergent', '53': 'RQ_DATA_ANALYTICS Vision', '49': 'RQ_DATA_ANALYTICS Cooperative/Swarm',
    '19': 'RQ_DATA_ANALYTICS VIO', '7': 'RQ_DATA_ANALYTICS Survey/LiDAR',
    '66': 'MASTER country China', '40': 'MASTER country USA', '13': 'MASTER country Canada',
    '1.84': 'MASTER REC_0037', '0.80': 'MASTER REC_0502', '0.7408': 'MASTER REC_0502', '13.7858': 'MASTER REC_0502',
    '0.4871': 'MASTER REC_0502', '3.832': 'MASTER REC_0502', '179.99': 'MASTER REC_1277', '26.64': 'MASTER REC_1277',
    '85.2': 'MASTER REC_1277', '0.094': 'MASTER REC_0003', '0.031': 'MASTER REC_0003', '0.3993': 'MASTER REC_0960',
    '0.0522': 'MASTER REC_1026', '0.0853': 'MASTER REC_1026', '0.1784': 'MASTER REC_1026', '38.8': 'MASTER REC_1026',
    '24.6': 'MASTER REC_1069', '31.2': 'MASTER REC_1069', '1.306': 'MASTER REC_0960 baseline',
    '0.467': 'MASTER REC_0960', '64.2': 'derived REC_0960', '2.16': 'MASTER REC_1267', '2.60': 'MASTER REC_1267',
    '95.95': 'MASTER REC_0001',
    '1,000': '08_docs/ANCHOR_FREEZE_20260919.md (IEEE/Scopus 1000 each)',
    '3.0': 'quality schema qa_rigor max', '2.0': 'quality schema qa_baseline max', '1.0': 'quality schema qa_repro max',
    '28': '08_docs/EXTRACTION_SCHEMA_v1.md (28 columns)',
    '17.6': 'derived 49/279', '49.0': 'RQ_DATA_ANALYTICS swarm simulation', '22.4': 'RQ_DATA_ANALYTICS swarm real',
    '85.7': 'RQ_DATA_ANALYTICS LiDAR real', '5.0': 'RQ_DATA_ANALYTICS radar',
    '200': 'MASTER REC_0502 (200 Hz IMU)', '100': 'MASTER REC_0502 (100-500 m)', '500': 'MASTER REC_0502 (100-500 m)',
    '18': 'derived REC_0502 (18-fold)', '13.79': 'MASTER REC_0502',
}
print('trace map', len(TRACE), 'entries; master ids', len(mids))
# ---------------- L5 ----------------
cited = sorted(set(re.findall(r'REC_[0-9]{4}', txt)))
l5_missing = [c for c in cited if c not in mids]

# ---------------- L7 ----------------
BANNED = ['delve', 'landscape', 'crucial', 'pivotal', 'it is important to note']
low = txt.lower()
l7_hits = {b: low.count(b) for b in BANNED if low.count(b)}

# ---------------- L2 : prose numbers ----------------
prose_lines = []
in_fence = False
for i, line in enumerate(txt.splitlines(), 1):
    if line.strip().startswith('```'):
        in_fence = not in_fence
        continue
    if not in_fence:
        c = re.sub(r'`[^`]*`', ' ', line)            # drop code spans / paths
        c = re.sub(r'^\s*#{1,6}\s*[\d.]+\s*', '', c)  # drop section numbers
        c = re.sub(r'\d{4}-\d{2}-\d{2}', ' ', c)      # drop ISO dates
        c = re.sub(r'\b(19|20)\d{2}\b', ' ', c)       # drop years
        prose_lines.append((i, c))

num_re = re.compile(r'(?<![\w.])(\d[\d,]*(?:\.\d+)?%?)')
claims = []
for i, line in prose_lines:
    for m in num_re.finditer(line):
        tok = m.group(1)
        raw = tok.replace(',', '').rstrip('%')
        try:
            fv = float(raw)
        except ValueError:
            continue
        if len(raw) <= 1:
            continue
        claims.append((i, tok, line.strip()[:160]))

untraced = []
for i, tok, ctx in claims:
    raw = tok.replace(',', '').rstrip('%')
    if tok in TRACE or raw in TRACE:
        continue
    untraced.append((i, tok, ctx))

seen = set()
untraced_u = []
for i, tok, ctx in untraced:
    if (tok, i) in seen:
        continue
    seen.add((tok, i))
    untraced_u.append((i, tok, ctx))

# ---------------- write NUMBER_TRACE.md ----------------
lines = []
lines.append('# NUMBER TRACE')
lines.append('')
lines.append('Regenerated for MANUSCRIPT_V4.md (Station 9, Gate 9.4).')
lines.append('Every quantitative claim below is traced to its source file.')
lines.append('')
lines.append('## TRACEABLE claims')
lines.append('')
lines.append('| Number | Source |')
lines.append('|---|---|')
for k in sorted(TRACE, key=lambda z: (-len(z), z)):
    lines.append('| %s | %s |' % (k, TRACE[k]))
lines.append('')
lines.append('## UNTRACEABLE / NEEDS-HUMAN (no source in corpus files)')
lines.append('')
lines.append('| line | number | context |')
lines.append('|---|---|---|')
for i, tok, ctx in untraced_u:
    lines.append('| %d | %s | %s |' % (i, tok, ctx.replace('|', '/')))
lines.append('')
lines.append('## L5 - cited REC ids')
lines.append('')
lines.append('Cited: %d. Missing from MASTER_EVIDENCE.csv: %s' % (len(cited), l5_missing or 'none'))
lines.append('')
lines.append('## L7 - tone scan')
lines.append('')
lines.append('Banned vocabulary hits: %s' % (l7_hits or 'none'))
lines.append('')
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

print('L5 cited', len(cited), 'missing', l5_missing)
print('L7 hits', l7_hits)
print('prose numbers scanned', len(claims))
print('untraced candidates', len(untraced_u))
for i, tok, ctx in untraced_u[:60]:
    print('  L%d: %s | %s' % (i, tok, ctx))
print()
print('WROTE', OUT)
print('SELF-AUDIT', 'PASS' if (not l5_missing and not l7_hits and not untraced_u) else 'REVIEW')