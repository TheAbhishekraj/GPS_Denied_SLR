#!/usr/bin/env python3
"""build_v4.py - Station 9 / Gate 9.1b: repair MANUSCRIPT_V3.md into MANUSCRIPT_V4.md.

Reads V3, writes V4 only. Every replacement is asserted to occur exactly once
so a silent miss cannot pass. No external data: all replacement values trace to
MASTER_EVIDENCE.csv, quality_appraisal_scored.csv, or RQ_DATA_ANALYTICS.json.
"""
import os
import re
import csv
import hashlib

ROOT = r'E:\GPS_Denied_SLR'
MP = os.path.join(ROOT, '07_manuscript')
SRC = os.path.join(MP, 'MANUSCRIPT_V3.md')
DST = os.path.join(MP, 'MANUSCRIPT_V4.md')

txt = open(SRC, encoding='utf-8', newline='').read()


def rep(old, new, n=1):
    global txt
    c = txt.count(old)
    assert c == n, 'expected %d got %d for: %r' % (n, c, old[:60])
    txt = txt.replace(old, new)


def replace_fenced(anchor, new_inner):
    global txt
    i = txt.index(anchor)
    f1 = txt.rindex('```', 0, i)
    f2 = txt.index('```', i)
    txt = txt[:f1] + '```\n' + new_inner + '\n```' + txt[f2 + 3:]


# R1 title (American spelling + protocol window)
rep('Review of Multi-Sensor Fusion, Vision-Based Localisation, and Cooperative Autonomy (2013–2026)',
    'Review of Multi-Sensor Fusion, Vision-Based Localization, and Cooperative Autonomy (2010–2026)')

# R2 target venue
rep('**Target Publication:** *IEEE Transactions on Robotics* / *IEEE Access*',
    '**Target Publication:** *IEEE Access*')

# R3 corpus window in abstract + conclusion
rep('published between 2013 and 2026', 'published between 2010 and 2026')
rep('published between 2013 and mid-2026', 'published between 2010 and mid-2026')

# R4 PRISMA flow (canonical)
replace_fenced('PRISMA 2020 Flow Summary:',
               'PRISMA 2020 Flow Summary:\n'
               '  Records identified (IEEE Xplore 1,000 + Scopus 1,000):   2,000\n'
               '  Records after duplicate removal (280 duplicates):        1,716\n'
               '  Records screened at title/abstract level:                  636\n'
               '  Full-text articles assessed for eligibility:               291\n'
               '  Studies meeting eligibility (INCLUDE):                      285\n'
               '  Studies excluded at full text (EXCLUDE):                      6\n'
               '  Studies deferred (identified, not extracted):                 6\n'
               '  Studies included in the frozen synthesis corpus:            279')

# R5 geography (recounted from MASTER_EVIDENCE.csv country)
rep('* **China ($n = 28$ primary, plus 12 institutional affiliations):** Dominated by Tsinghua University, Beijing Institute of Technology, Northwestern Polytechnical University (NWPU), and Beihang University.',
    '* **China ($n = 66$):** Leading institutions include Tsinghua University, Beijing Institute of Technology, Northwestern Polytechnical University (NWPU), and Beihang University.')
rep('* **United States ($n = 16$):** Led by West Virginia University, Cal Poly Pomona, and DARPA SubT contributors.',
    '* **United States ($n = 40$):** Led by West Virginia University, Cal Poly Pomona, and DARPA SubT contributors.')
rep('* **Singapore ($n = 9$):** Focused primarily at the National University of Singapore (TLAB) and Temasek Laboratories.',
    '* **Singapore ($n = 12$):** Focused primarily at the National University of Singapore (TLAB) and Temasek Laboratories.')
rep('* **Other Contributing Nations:** Taiwan ($n = 6$), Canada ($n = 6$), Australia ($n = 3$), Spain ($n = 3$), Finland ($n = 3$), India ($n = 3$), Iran ($n = 3$), Italy ($n = 2$), Germany ($n = 2$).',
    '* **Other Contributing Nations:** Canada ($n = 13$), Taiwan ($n = 11$), Australia ($n = 11$), India ($n = 11$), Spain ($n = 10$), Germany ($n = 7$), Italy ($n = 6$), Iran ($n = 6$), South Korea ($n = 5$), Finland ($n = 5$).')

# R6 QA denominator clarity
rep('establishing an average corpus composite quality score of 3.81 out of 8.0.',
    'establishing an average corpus composite quality score of 3.81 on a realized 0-8 scale.')

# R7 51% -> 30.5%
rep('Over **51% of all studies in the corpus never execute closed-loop autonomous flight**.',
    'Over **30.5% of all studies in the corpus never execute closed-loop autonomous flight** (62 simulation-only studies plus 23 that do not report a validation mode).')

# R8 related-work survey table -> real IDs only
replace_fenced('Existing Survey Articles in Screened Literature:',
               'Existing Survey Articles in Screened Literature:\n\n'
               '| Study ID | Year | Focus & Claimed Scope | Identified Methodological Gap |\n'
               '|---|---|---|---|\n'
               '| REC_0242 | 2016 | Survey on UAV navigation in GPS-denied environments | Pre-dates the deep-learning and multi-sensor fusion era |\n'
               '| REC_1025 | 2021 | Radio-frequency precise localization for UAVs in GPS-denied settings | No prior up-to-date review in this niche at the time |\n'
               '| REC_0388 | 2026 | Multi-UAV cooperative navigation via multisource information fusion | Prior surveys focus on single platforms; cooperative navigation in swarms left underexplored |\n'
               '| REC_0870 | 2026 | Recent trends and applications of AI-based autonomous drones | Most reported advances remain simulation-heavy with limited field-tested systems |\n'
               '| REC_1006 | 2026 | Comprehensive survey of autonomous UAV navigation and control | Excludes hardware-level, cybersecurity, and regulatory analysis |\n'
               '| REC_1019 | 2026 | Multi-sensor fusion SLAM for interceptor UAVs in GNSS-denied settings | No single SLAM scheme covers the full flight envelope; adaptation boundaries remain |\n'
               '| REC_0464 | 2026 | Systematic review of multi-sensor fusion SLAM | Broad robotics focus; no SWaP-C analysis |')

# R9 Table 5 -> rebuilt from RQ_DATA_ANALYTICS.json algo_families_vs_validation
replace_fenced('Table 5: Algorithmic Family Distribution',
               'Table 5: Algorithmic Family Distribution vs. Validation Mode (n = 279)\n\n'
               '| Algorithmic Paradigm | Total | % Corpus | Real Flight | Simulation | Other / Not Reported | Both |\n'
               '|---|---|---|---|---|---|---|\n'
               '| Emergent / Physics-Guided | 138 | 49.5% | 59 (42.8%) | 28 (20.3%) | 50 (36.2%) | 1 (0.7%) |\n'
               '| Vision & Place Recognition | 53 | 19.0% | 32 (60.4%) | 7 (13.2%) | 13 (24.5%) | 1 (1.9%) |\n'
               '| Cooperative / Swarm | 49 | 17.6% | 11 (22.4%) | 24 (49.0%) | 14 (28.6%) | 0 (0.0%) |\n'
               '| Visual-Inertial Odometry (VIO) | 19 | 6.8% | 7 (36.8%) | 5 (26.3%) | 7 (36.8%) | 0 (0.0%) |\n'
               '| Survey / Systematic Review | 7 | 2.5% | 0 (0.0%) | 0 (0.0%) | 7 (100.0%) | 0 (0.0%) |\n'
               '| LiDAR SLAM / Odometry (LIO) | 7 | 2.5% | 6 (85.7%) | 0 (0.0%) | 1 (14.3%) | 0 (0.0%) |\n'
               '| Ultra-Wideband (UWB) / Radio | 6 | 2.2% | 2 (33.3%) | 1 (16.7%) | 3 (50.0%) | 0 (0.0%) |')

# R10 indoor numbers: drop nonexistent REC_0086/REC_0093, re-source to real owners
rep('Exemplary studies report mean path deviations as low as **0.0395 m** (SIL simulation, `REC_0086`), **0.094 ± 0.031 m** (physical indoor trajectory, `REC_0028`), and maximum horizontal deviations within **±0.10 m** (`REC_0093`).',
    'Exemplary studies report a mean path error of **0.094 ± 0.031 m** (physical indoor trajectory, `REC_0003`) and a nominal position MAE of **0.3993 m** (`REC_0960`).')

# R11 subterranean FGO: REC_0884 -> REC_1026 with verified LC/VIO baselines
rep('* **REC_0884 (2022):** Factor Graph Optimization with tightly coupled LiDAR-inertial updates achieved an underground rectangle-trajectory RMSE of **0.0522 m** (versus loosely coupled 0.1412 m).',
    '* **REC_1026 (2022):** Factor Graph Optimization with tight coupling achieved an underground rectangle-trajectory RMSE of **0.0522 m**, versus **0.0853 m** for loosely coupled FGO and **0.1784 m** for VIO.')

# R12 urban canyon: remove misattributed 95.95% (true owner REC_0001 is indoor)
rep('Systems fusing visual-inertial odometry with 3D building city models (e.g., OpenStreetMap or aerial LiDAR meshes) achieve localization coverage exceeding **95.95%** (`REC_0312`) and mean horizontal positioning errors of **0.80 m**, compared to uncontrolled GNSS multipath deviations exceeding 15–35 m.',
    'Systems fusing visual-inertial odometry with 3D building city models (e.g., OpenStreetMap or aerial LiDAR meshes) report sub-meter mean horizontal positioning errors, compared with uncontrolled GNSS multipath deviations exceeding 15–35 m.')

# R13 baseline gains: replace unsourceable 42-63% with verified figures
rep('   * Factor Graph Optimization reduces trajectory RMSE by **42%–63%** relative to loosely coupled EKF backends (`REC_0884`, `REC_1069`).',
    '   * Factor Graph Optimization with tight coupling reduced rectangle-trajectory RMSE by **38.8%** relative to a loosely coupled FGO backend (`REC_1026`), while a UAV-UGV collaborative localization framework reported a **24.6%** RMSE reduction and **31.2%** maximum-error reduction over a single-agent baseline (`REC_1069`).')

# R14 L7: drop loose "state-of-the-art" (no named baseline adjacent)
rep('Achieves a state-of-the-art average localization error of **0.80 m**',
    'Achieves an average localization error of **0.80 m**')

# ---- write V4 ----
open(DST, 'w', encoding='utf-8', newline='').write(txt)
h = hashlib.sha256(open(DST, 'rb').read()).hexdigest().upper()
print('WROTE', DST)
print('bytes', os.path.getsize(DST), 'sha256', h)

# ---- self-audit: L5 ID check + legacy token check ----
with open(os.path.join(ROOT, '02_data_processed', 'MASTER_EVIDENCE.csv'), encoding='utf-8-sig', newline='') as f:
    mids = set(r['id'].strip() for r in csv.DictReader(f))
cited = sorted(set(re.findall(r'REC_[0-9]{4}', txt)))
missing = [c for c in cited if c not in mids]
print('cited_ids', len(cited), 'missing', missing)
for tok in ['1,418', '382', '103', '51%']:
    print('  token', tok, '->', txt.count(tok))
for bad in ['REC_0045', 'REC_0068', 'REC_0099', 'REC_0176', 'REC_0488', 'REC_0513', 'REC_0086', 'REC_0093', 'REC_0884', 'REC_0312']:
    if bad in txt:
        print('  STILL PRESENT:', bad)
print('SELF-AUDIT', 'PASS' if not missing else 'FAIL')