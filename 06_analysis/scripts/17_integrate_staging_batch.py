"""Integrate the verified staging batch into the fulltext corpus.

Actions (each asserted before execution):
1. Drop the byte-identical "(1)" duplicate and the 0-byte getPDF.jsp.
2. Rename + move 11 verified PDFs to 05_papers_fulltext/REC_xxxx.pdf.
3. Set done_Y_N=Y for exactly the 11 ids in priority_300_download.csv
   (row-level assertion: nothing else changes).
4. Append provenance rows to rename_log.csv (header extended with
   sha256 + matched_by; safe because the log is header-only today).
"""
import csv
import hashlib
import io
import shutil
from pathlib import Path

ROOT = Path(r'E:\GPS_Denied_SLR')
ST = ROOT / '08_docs' / 'downloads_staging'
FT = ROOT / '05_papers_fulltext'

TARGETS = {
    'REC_1115': ('10.1016/j.patcog.2026.114522',
                 '1-s2.0-S003132032601486X-main.pdf', 'doi'),
    'REC_1502': ('10.1016/j.autcon.2023.104753',
                 '1-s2.0-S0926580523000134-main.pdf', 'doi'),
    'REC_1439': ('10.1016/j.vehcom.2025.100986',
                 '1-s2.0-S2214209625001135-main.pdf', 'doi'),
    'REC_1438': ('',
                 '3D_motion_planning_for_UAVs_in_GPS-denied_unknown_forest_environment.pdf',
                 'title-sim-0.61'),
    'REC_1123': ('10.1109/jiot.2026.3664077',
                 'A_Novel_Scene-Matching_Positioning_Approach_for_Low-Altitude_UAVs_Considering_Elevation_Differences_in_Satellite_Images.pdf',
                 'doi'),
    'REC_1423': ('',
                 'A_robust_real-time_vision_based_GPS-denied_navigation_system_of_UAV.pdf',
                 'title-sim-0.59'),
    'REC_1399': ('10.1109/icuas69441.2026.11598726',
                 'Adaptive_Texture-Aware_Pixel_Selection_for_Robust_Direct_Visual_Odometry_in_UAV_Navigation.pdf',
                 'doi'),
    'REC_1431': ('10.1109/codit58514.2023.10284425',
                 'Advancing_Autonomous_UAV_Target_Localization_in_GPS-Denied_Environments.pdf',
                 'doi'),
    'REC_1002': ('',
                 'An_integrated_UAV_navigation_system_based_on_geo-registered_3D_point_cloud.pdf',
                 'title-sim-0.64'),
    'REC_1295': ('10.1061/jccee5.cpeng-7010',
                 'matiki-et-al-2025-digital-twin-approach-for-drift-free-uav-localization-in-gps-denied-environments.pdf',
                 'doi'),
    'REC_1474': ('10.1109/tgrs.2026.3689254',
                 'Robust_UAVSatellite_Imagery_Alignment_via_Cross-Domain_Descriptor_Learning_and_Homography_Optimization.pdf',
                 'doi'),
}

DUP = 'Adaptive_Texture-Aware_Pixel_Selection_for_Robust_Direct_Visual_Odometry_in_UAV_Navigation (1).pdf'
JSP = 'getPDF.jsp'


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


# --- 1. duplicate + failed download cleanup -------------------------------
canon = ST / TARGETS['REC_1399'][1]
dup = ST / DUP
assert dup.exists() and canon.exists(), 'dup or canonical missing'
assert sha256(dup) == sha256(canon), '"(1)" file is NOT byte-identical - aborting'
dup.unlink()
print(f'removed byte-identical duplicate: {DUP}')

jsp = ST / JSP
if jsp.exists():
    assert jsp.stat().st_size == 0, 'getPDF.jsp not empty - inspect manually'
    jsp.unlink()
    print('removed 0-byte failed download: getPDF.jsp')

# --- 2. rename + move -----------------------------------------------------
print('\n--- rename + move ---')
hashes = {}
for rid, (doi, fname, how) in TARGETS.items():
    src = ST / fname
    dst = FT / f'{rid}.pdf'
    assert src.exists(), f'missing staging file for {rid}: {fname}'
    assert not dst.exists(), f'fulltext already has {rid}.pdf'
    hashes[rid] = sha256(src)
    shutil.move(str(src), str(dst))
    print(f'{fname[:70]:<70} -> {rid}.pdf  [{how}]')
    assert dst.exists() and dst.stat().st_size > 0

# --- 3. priority CSV update with positional row assertion -----------------
ppath = ROOT / '08_docs' / 'priority_300_download.csv'
raw = ppath.read_bytes()
try:
    text = raw.decode('utf-8')
    enc = 'utf-8'
except UnicodeDecodeError:
    text = raw.decode('cp1252')
    enc = 'cp1252'
nl = '\r\n' if '\r\n' in text[:2000] else '\n'

all_rows = list(csv.reader(io.StringIO(text)))
header = all_rows[0]
i_id = header.index('id')
i_done = header.index('done_Y_N')

new_rows = []
changed = []
for r in all_rows[1:]:
    if r and len(r) > i_id and r[i_id] in TARGETS:
        r2 = list(r)
        if r2[i_done] != 'Y':
            r2[i_done] = 'Y'
            changed.append(r2[i_id])
        new_rows.append(r2)
    else:
        new_rows.append(r)  # preserves blank/odd rows verbatim
assert set(changed) == set(TARGETS), f'expected 11 flips, got {sorted(changed)}'

buf = io.StringIO()
w = csv.writer(buf, lineterminator=nl)
w.writerow(header)
w.writerows(new_rows)
new_text = buf.getvalue()
if not text.endswith(nl) and new_text.endswith(nl):
    new_text = new_text[:-len(nl)]
new_raw = new_text.encode(enc)
assert new_raw != raw

# positional assertion: same row count; only the 11 done_Y_N cells differ
recheck = list(csv.reader(io.StringIO(new_text)))
assert len(recheck) == len(all_rows), 'row count changed'
for idx, (o, n) in enumerate(zip(all_rows, recheck)):
    if o == n:
        continue
    assert o and len(o) > i_id and o[i_id] in TARGETS, f'row {idx}: unexpected change'
    diff_cols = [k for k in range(len(header)) if o[k] != n[k]]
    assert diff_cols == [i_done], f'row {idx} ({o[i_id]}): changed cols {diff_cols}'

ppath.write_bytes(new_raw)
crlf = 'CRLF' if nl == chr(13) + chr(10) else 'LF'
print(f'\npriority CSV: done_Y_N=Y for {len(changed)} ids ({enc}, {crlf} preserved)')

# --- 4. rename log --------------------------------------------------------
lpath = ROOT / '08_docs' / 'rename_log.csv'
lines = lpath.read_text(encoding='utf-8-sig').splitlines()
assert len(lines) <= 1, f'rename_log not header-only ({len(lines)} lines) - aborting'
with open(lpath, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['original', 'rec_id', 'status', 'sha256', 'matched_by'])
    for rid, (doi, fname, how) in TARGETS.items():
        w.writerow([fname, rid, 'renamed+moved', hashes[rid], how])
print(f'rename_log.csv: extended header + {len(TARGETS)} provenance rows')

print('\nDONE: 11 papers integrated.')
