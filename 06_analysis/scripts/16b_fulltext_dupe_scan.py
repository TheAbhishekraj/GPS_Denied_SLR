"""Read-only verification before integrating the new staging batch.

1. Prints screened + priority rows for the 11 target ids (eyeball check).
2. Side-by-side comparison for the 3 DOI-less (title-matched) papers.
3. Scans all fulltext PDFs for hidden duplicates of the batch (by DOI or title).
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

# rec_id -> (printed_doi_or_empty, original_staging_filename)
TARGETS = {
    'REC_1115': ('10.1016/j.patcog.2026.114522',
                 '1-s2.0-S003132032601486X-main.pdf'),
    'REC_1502': ('10.1016/j.autcon.2023.104753',
                 '1-s2.0-S0926580523000134-main.pdf'),
    'REC_1439': ('10.1016/j.vehcom.2025.100986',
                 '1-s2.0-S2214209625001135-main.pdf'),
    'REC_1438': ('',
                 '3D_motion_planning_for_UAVs_in_GPS-denied_unknown_forest_environment.pdf'),
    'REC_1123': ('10.1109/jiot.2026.3664077',
                 'A_Novel_Scene-Matching_Positioning_Approach_for_Low-Altitude_UAVs_Considering_Elevation_Differences_in_Satellite_Images.pdf'),
    'REC_1423': ('',
                 'A_robust_real-time_vision_based_GPS-denied_navigation_system_of_UAV.pdf'),
    'REC_1399': ('10.1109/icuas69441.2026.11598726',
                 'Adaptive_Texture-Aware_Pixel_Selection_for_Robust_Direct_Visual_Odometry_in_UAV_Navigation.pdf'),
    'REC_1431': ('10.1109/codit58514.2023.10284425',
                 'Advancing_Autonomous_UAV_Target_Localization_in_GPS-Denied_Environments.pdf'),
    'REC_1002': ('',
                 'An_integrated_UAV_navigation_system_based_on_geo-registered_3D_point_cloud.pdf'),
    'REC_1295': ('10.1061/jccee5.cpeng-7010',
                 'matiki-et-al-2025-digital-twin-approach-for-drift-free-uav-localization-in-gps-denied-environments.pdf'),
    'REC_1474': ('10.1109/tgrs.2026.3689254',
                 'Robust_UAVSatellite_Imagery_Alignment_via_Cross-Domain_Descriptor_Learning_and_Homography_Optimization.pdf'),
}

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


screened = {r['id']: r for r in load(ROOT / '02_data_processed' / 'screened_included_v2.csv')}
priority = {r['id']: r for r in load(ROOT / '08_docs' / 'priority_300_download.csv')}

print('===== TARGET RECORD CHECK =====')
for rid, (doi, fname) in TARGETS.items():
    s = screened.get(rid, {})
    p = priority.get(rid, {})
    s_doi = (s.get('doi') or '').strip().lower().rstrip('.')
    if doi and s_doi and s_doi != doi:
        flag = '  << DOI MISMATCH vs printed'
    elif doi and not s_doi:
        flag = '  << screened has no DOI'
    else:
        flag = ''
    print(f'\n{rid}  [{fname}]')
    print(f'  screened : {s.get("title", "MISSING")}')
    print(f'             authors={s.get("authors", "")[:90]} year={s.get("year", "")} venue={s.get("venue", "")[:60]} doi={s_doi or "-"}')
    print(f'  priority : bucket={p.get("bucket", "")} done={p.get("done_Y_N", "") or "-"} year={p.get("year", "")}')
    print(f'  pdf-doi  : {doi or "-"}{flag}')

print('\n===== DOI-LESS PAPERS: PDF HEAD vs SCREENED TITLE =====')
for rid, (doi, fname) in TARGETS.items():
    if doi:
        continue
    d = pymupdf.open(ST / fname)
    head = ' '.join(d[0].get_text()[:400].split())
    print(f'\n{rid}:\n  PDF head  : {head[:200]}')
    print(f'  Screened  : {screened.get(rid, {}).get("title", "MISSING")}')

print('\n===== FULLTEXT DUPLICATE SCAN (221 PDFs) =====')
doi_targets = {doi: rid for rid, (doi, _) in TARGETS.items() if doi}
tk_targets = {rid: tkey(screened.get(rid, {}).get('title', '')) for rid in TARGETS}
hits = 0
skipped = 0
for p in sorted(FT.glob('REC_*.pdf')):
    try:
        d = pymupdf.open(p)
        text = ''
        for pg in d:
            text += (pg.get_text() or '') + ' '
            if len(text) > 9000:
                break
    except Exception:
        skipped += 1
        continue
    if not text.strip():
        skipped += 1
        continue
    m = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', text[:8000], re.I)
    if m and m.group(0).rstrip('.,;)').lower() in doi_targets:
        rid = doi_targets[m.group(0).rstrip('.,;)').lower()]
        print(f'  DOI DUP: {p.name} already holds {rid}')
        hits += 1
        continue
    head = ' '.join(text[:400].split())
    for rid, tk in tk_targets.items():
        if tk and SequenceMatcher(None, tkey(head), tk).ratio() >= 0.80:
            print(f'  TITLE DUP: {p.name} ~ {rid}')
            hits += 1
            break
print(f'\nduplicate hits: {hits} | unreadable/empty skipped: {skipped}')
