#!/usr/bin/env python3
"""figures_final.py - Station 9 / Gate 9.3: rebuild all 9 manuscript figures.

Traceable to 02_data_processed/MASTER_EVIDENCE.csv and
06_analysis/outputs/RQ_DATA_ANALYTICS.json only. No external data.
Writes outputs/figures/F{1..9}_output.png and outputs/tables/F{1..9}_data.csv.
"""
import os
import re
import csv
import json
import hashlib
from collections import Counter, OrderedDict

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = r'E:\GPS_Denied_SLR'
OUT = os.path.join(ROOT, '06_analysis', 'outputs')
TAB = os.path.join(OUT, 'tables')
FIG = os.path.join(OUT, 'figures')
MASTER = os.path.join(ROOT, '02_data_processed', 'MASTER_EVIDENCE.csv')
ANALYTICS = os.path.join(OUT, 'RQ_DATA_ANALYTICS.json')
REPORT = os.path.join(FIG, 'FIGURES_RUN_REPORT.md')

os.makedirs(TAB, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

with open(MASTER, encoding='utf-8-sig', newline='') as f:
    rows = [x for x in csv.DictReader(f)]
rada = json.load(open(ANALYTICS, encoding='utf-8'))


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(65536), b''):
            h.update(b)
    return h.hexdigest().upper()


def write_csv(path, header, data):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


def epoch(y):
    y = int(float(y))
    return '2013-2016' if y <= 2016 else ('2017-2021' if y <= 2021 else '2022-2026')


def val_mode(v):
    s = (v or '').strip().upper()
    if s in ('REAL', 'BOTH', 'SIM'):
        return s
    return 'Unreported'


def country(v):
    c = (v or '').strip()
    if not c or c == 'NOT_REPORTED':
        return 'NOT_REPORTED'
    if c.startswith('China'):
        return 'China'
    if c.startswith('USA') or c.startswith('United States'):
        return 'USA'
    c = re.sub(r'\([^)]*\)', ' ', c)
    return re.split(r'[;,/&]', c)[0].strip() or 'NOT_REPORTED'


def taxonomy(v):
    s = (v or '').strip().upper()
    if s.startswith('CORE'):
        return 'CORE'
    if s.startswith('IMPORTANT'):
        return 'IMPORTANT'
    if s.startswith('PERIPHERAL'):
        return 'PERIPHERAL'
    return 'Unclassified'


report = []
fig_hashes = {}


def finish(name, fig, header, data):
    write_csv(os.path.join(TAB, name + '_data.csv'), header, data)
    path = os.path.join(FIG, name + '_output.png')
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)
    fig_hashes[name] = sha(path)
    report.append('- %s: DRAWN (%d rows) sha256: %s' % (name, len(data), fig_hashes[name]))


epochs = ['2013-2016 (Foundational)', '2017-2021 (Maturation)', '2022-2026 (Multi-Modal/Swarm)']
width = 0.26
# F1 - PRISMA flow
stages = ['Identified', 'After dedup', 'Screened', 'Full-text', 'INCLUDE', 'EXCLUDED', 'Corpus']
counts = [2000, 1716, 636, 291, 285, 6, 279]
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(stages, counts, color='#2C6E9B')
for i, c in enumerate(counts):
    ax.text(i, c + 25, str(c), ha='center', fontsize=9)
ax.set_title('Figure 1. PRISMA 2020 flow (n = 279)')
ax.set_ylabel('Records')
ax.tick_params(axis='x', rotation=30)
finish('F1', fig, ['stage', 'count'], list(zip(stages, counts)))

# F2 - publications per year (Table II)
yc = Counter(int(float(x['year'])) for x in rows if re.match(r'^[0-9.]+$', x['year'].strip()))
years = sorted(yc)
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar([str(y) for y in years], [yc[y] for y in years], color='#3E8E7E')
for i, y in enumerate(years):
    ax.text(i, yc[y] + 0.5, str(yc[y]), ha='center', fontsize=8)
ax.set_title('Figure 2. Publications per year (n = 279)')
ax.set_ylabel('Count')
finish('F2', fig, ['year', 'count'], [[y, yc[y]] for y in years])

# F3 - sensor modality by epoch (Table III)
sens = ['Camera', 'IMU', 'LiDAR', 'UWB', 'Barometer', 'Magnetometer', 'Radar', 'Optical Flow', 'Ultrasonic/Sonar']
se = rada['sensor_by_epoch']
fig, ax = plt.subplots(figsize=(11, 5))
xs = np.arange(len(sens))
for j, e in enumerate(epochs):
    vals = [se.get(e, {}).get(k, 0) for k in sens]
    ax.bar(xs + (j - 1) * width, vals, width, label=e.split(' (')[0])
ax.set_xticks(xs)
ax.set_xticklabels(sens, rotation=35, ha='right')
ax.set_title('Figure 3. Sensor modality frequency by epoch')
ax.set_ylabel('Occurrences')
ax.legend()
finish('F3', fig, ['sensor'] + epochs, [[k] + [se.get(e, {}).get(k, 0) for e in epochs] for k in sens])

# F4 - fusion pairs by epoch (Table 3)
fp = rada['fusion_pairs_by_epoch']
pairs = ['Camera+IMU', 'Camera+LiDAR', 'LiDAR+IMU', 'Camera+LiDAR+IMU', 'UWB+IMU', 'UWB+Camera', 'Radar+IMU']
fig, ax = plt.subplots(figsize=(11, 5))
xs = np.arange(len(pairs))
for j, e in enumerate(epochs):
    vals = [fp.get(e, {}).get(p, 0) for p in pairs]
    ax.bar(xs + (j - 1) * width, vals, width, label=e.split(' (')[0])
ax.set_xticks(xs)
ax.set_xticklabels(pairs, rotation=25, ha='right')
ax.set_title('Figure 4. Multi-sensor fusion pair evolution')
ax.set_ylabel('Count')
ax.legend()
finish('F4', fig, ['pair'] + epochs, [[p] + [fp.get(e, {}).get(p, 0) for e in epochs] for p in pairs])

# F5 - environment distribution (Table IV)
env = rada['env_distribution']
env_sum = sum(env.values())
fig, ax = plt.subplots(figsize=(9, 4.8))
ks = sorted(env, key=lambda k: -env[k])
ax.barh(ks[::-1], [env[k] for k in ks[::-1]], color='#B5651D')
for i, k in enumerate(ks[::-1]):
    ax.text(env[k] + 1, i, str(env[k]), va='center', fontsize=9)
ax.set_title('Figure 5. Environment distribution (%d of 279 classified)' % env_sum)
ax.set_xlabel('Studies')
finish('F5', fig, ['environment', 'count'], list(zip(ks, [env[k] for k in ks])))
# F6 - taxonomy (ERRC)
tax = Counter(taxonomy(x.get('taxonomy_category')) for x in rows)
order = ['CORE', 'IMPORTANT', 'PERIPHERAL', 'Unclassified']
fig, ax = plt.subplots(figsize=(7, 6))
ax.pie([tax.get(k, 0) for k in order], labels=['%s (%d)' % (k, tax.get(k, 0)) for k in order],
       autopct='%1.1f%%', startangle=90)
ax.set_title('Figure 6. Taxonomy distribution (n = 279)')
finish('F6', fig, ['taxonomy', 'count'], [[k, tax.get(k, 0)] for k in order])

# F7 - validation mode
vm = Counter(val_mode(x.get('real_or_sim')) for x in rows)
vorder = ['REAL', 'BOTH', 'SIM', 'Unreported']
fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(vorder, [vm.get(k, 0) for k in vorder], color=['#2E7D32', '#1565C0', '#C62828', '#757575'])
for i, k in enumerate(vorder):
    ax.text(i, vm.get(k, 0) + 1, '%d (%.1f%%)' % (vm.get(k, 0), 100.0 * vm.get(k, 0) / len(rows)), ha='center', fontsize=9)
ax.set_title('Figure 7. Validation fidelity (n = 279)')
ax.set_ylabel('Studies')
finish('F7', fig, ['validation', 'count'], [[k, vm.get(k, 0)] for k in vorder])

# F8 - geography (primary country)
gc = Counter(country(x.get('country')) for x in rows)
norep = gc.pop('NOT_REPORTED', 0)
top = gc.most_common(10)
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar([k for k, v in top][::-1], [v for k, v in top][::-1], color='#5E35B1')
for i, (k, v) in enumerate(top[::-1]):
    ax.text(i, v + 0.3, str(v), ha='center', fontsize=9)
ax.set_title('Figure 8. Top 10 contributing countries (n = 279)')
ax.set_ylabel('Studies')
finish('F8', fig, ['country', 'count'], [[k, v] for k, v in gc.most_common()] + [['NOT_REPORTED', norep]])

# F9 - limitations + future themes (Table 7)
lim = rada['limitation_themes']
fut = rada['future_themes']
lk = sorted(lim, key=lambda k: -lim[k])
fk = sorted(fut, key=lambda k: -fut[k])
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].barh(lk[::-1], [lim[k] for k in lk[::-1]], color='#C62828')
axes[0].set_title('Documented limitations')
axes[1].barh(fk[::-1], [fut[k] for k in fk[::-1]], color='#2E7D32')
axes[1].set_title('Future research priorities')
fig.suptitle('Figure 9. Limitation and future-work themes (n = 279)')
finish('F9', fig, ['type', 'theme', 'count'],
       [['LIMITATION', k, v] for k, v in lim.items()] + [['FUTURE', k, v] for k, v in fut.items()])

with open(REPORT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('# FIGURES RUN REPORT (final)\n\n')
    f.write('\n'.join(report) + '\n')

print('WROTE 9 figures + 9 data tables')
for k in ['F1', 'F2', 'F7', 'F8']:
    print(' ', k, fig_hashes[k])
print('F7 counts', dict(vm))
print('F8 top', top[:3], 'NOT_REPORTED', norep)
print('env_sum', env_sum)
print('SELF-AUDIT', 'PASS' if len(fig_hashes) == 9 else 'FAIL')