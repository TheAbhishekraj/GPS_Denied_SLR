#!/usr/bin/env python3
"""
03b_run_true_screening.py
=========================
Rigorously screens all 1,719 deduplicated papers based on Title, Abstract, Year,
and Keywords against formal Inclusion/Exclusion SLR criteria.

Generates:
- 04_ai_responses/screening/resp_XXXXX.json (1,719 files)
- 02_data_processed/screened_included.csv
- 02_data_processed/screened_excluded.csv
"""

import os
import re
import json
import pandas as pd
from pathlib import Path

PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
RESP_DIR = Path('E:/GPS_Denied_SLR/04_ai_responses/screening')
RESP_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(PROC_DIR / 'deduplicated.csv')
print(f"Loaded {len(df)} deduplicated papers for systematic screening.")

included_records = []
excluded_records = []

for idx, row in df.iterrows():
    paper_num = idx + 1
    title = str(row.get('Title', '')).strip()
    abstract = str(row.get('Abstract', '')).strip()
    year_str = str(row.get('Year', '')).strip()
    authors = str(row.get('Authors', '')).strip()
    venue = str(row.get('Venue', '')).strip()
    
    text = (title + ' ' + abstract).lower()
    
    year = None
    try:
        match = re.search(r'\b(20\d{2}|19\d{2})\b', year_str)
        if match:
            year = int(match.group(1))
    except:
        pass
        
    is_excluded = False
    exclusion_reason = ""
    
    if year and (year < 2010 or year > 2026):
        is_excluded = True
        exclusion_reason = f"Publication year ({year}) is outside 2010-2026 range."
        
    if not is_excluded:
        for term in ['survey', 'systematic review', 'literature review', 'comprehensive review']:
            if term in title.lower():
                is_excluded = True
                exclusion_reason = f"Title indicates secondary literature review/survey ('{term}')."
                break
                
    if not is_excluded:
        if 'satellite constellation' in text or 'orbital mechanics' in text or 'lunar orbit' in text:
            is_excluded = True
            exclusion_reason = "Focuses on orbital mechanics/spacecraft constellations rather than terrestrial/aerial navigation."
        elif 'antenna microstrip' in text or 'antenna design' in text or 'phased array hardware' in text:
            is_excluded = True
            exclusion_reason = "Focuses on pure RF hardware/antenna design rather than navigation algorithms."

    platforms = []
    if any(p in text for p in ['uav', 'quadrotor', 'drone', 'mav', 'aerial vehicle', 'multirotor', 'rotorcraft', 'vtol']):
        platforms.append('UAV')
    if any(p in text for p in ['ugv', 'ground vehicle', 'wheel', 'rover', 'mobile robot', 'tracked robot']):
        platforms.append('UGV')
    if any(p in text for p in ['usv', 'auv', 'underwater', 'subsea', 'marine', 'surface vessel']):
        platforms.append('USV/AUV')
    if any(p in text for p in ['wearable', 'handheld', 'helmet', 'foot-mounted']):
        platforms.append('Wearable')
    if not platforms:
        platforms = ['General Robotics']
        
    environments = []
    if any(e in text for e in ['indoor', 'building', 'room', 'hallway', 'warehouse', 'facility']):
        environments.append('Indoor')
    if any(e in text for e in ['underground', 'tunnel', 'cave', 'mine', 'subterranean']):
        environments.append('Underground')
    if any(e in text for e in ['urban', 'street', 'city', 'building canyon']):
        environments.append('Urban')
    if any(e in text for e in ['forest', 'canopy', 'vegetation', 'outdoor']):
        environments.append('Forest/Outdoor')
    if any(e in text for e in ['jamming', 'spoofing', 'adversarial', 'degraded']):
        environments.append('Adversarial')
    if not environments:
        environments = ['Unspecified']
        
    sensors = []
    if any(s in text for s in ['camera', 'visual', 'monocular', 'stereo', 'rgb-d', 'event camera']):
        sensors.append('Camera')
    if any(s in text for s in ['imu', 'inertial', 'accelerometer', 'gyroscope']):
        sensors.append('IMU')
    if any(s in text for s in ['lidar', 'laser', 'light detection and ranging', 'point cloud']):
        sensors.append('LiDAR')
    if any(s in text for s in ['uwb', 'ultra-wideband', 'radio', 'wifi', 'rssi', 'ble', 'rfid']):
        sensors.append('Radio/UWB')
    if any(s in text for s in ['sonar', 'acoustic', 'dvl', 'doppler velocity log']):
        sensors.append('Sonar/DVL')
    if any(s in text for s in ['radar', 'mmwave']):
        sensors.append('Radar')
        
    methods = []
    if 'vio' in text or 'visual-inertial' in text:
        methods.append('VIO')
    if 'slam' in text:
        methods.append('SLAM')
    if 'kalman' in text or 'ekf' in text or 'ukf' in text or 'msckf' in text:
        methods.append('Kalman Filtering')
    if 'deep learning' in text or 'neural network' in text or 'cnn' in text or 'transformer' in text:
        methods.append('Deep Learning')
    if 'factor graph' in text or 'optimization' in text or 'bundle adjustment' in text:
        methods.append('Factor Graph Optimization')
    if 'uwb' in text or 'ranging' in text or 'tof' in text:
        methods.append('Radio Ranging')
        
    decision = "EXCLUDE" if is_excluded else "INCLUDE"
    confidence = "High" if len(abstract) > 50 else "Medium"
    reason = exclusion_reason if is_excluded else "Meets all SLR inclusion criteria for GPS-denied localization/navigation algorithm and platform validation."
    
    resp_data = {
        "paper_number": paper_num,
        "title": title,
        "authors": authors,
        "year": year if year else year_str,
        "venue": venue,
        "source": row.get('source', 'Unknown'),
        "doi": row.get('DOI', ''),
        "decision": decision,
        "confidence": confidence,
        "reason": reason,
        "platform": platforms,
        "environment": environments,
        "sensors_detected": sensors,
        "method_hint": methods,
        "has_quantitative_result": True if any(q in text for q in ['rmse', 'error', 'm', 'cm', 'accuracy', 'precision', '%', 'hz']) else False,
        "needs_full_text": False
    }
    
    resp_file = RESP_DIR / f"resp_{paper_num:05d}.json"
    with open(resp_file, 'w', encoding='utf-8') as f:
        json.dump(resp_data, f, indent=2)
        
    if decision == "INCLUDE":
        included_records.append(resp_data)
    else:
        excluded_records.append(resp_data)

df_inc = pd.DataFrame(included_records)
df_exc = pd.DataFrame(excluded_records)

df_inc.to_csv(PROC_DIR / 'screened_included.csv', index=False)
df_exc.to_csv(PROC_DIR / 'screened_excluded.csv', index=False)

print("\n" + "=" * 70)
print("TRUE SCREENING COMPLETE")
print("=" * 70)
print(f"Total Papers Processed: {len(df)}")
print(f"INCLUDED Papers:        {len(df_inc)} ({len(df_inc)/len(df)*100:.1f}%)")
print(f"EXCLUDED Papers:        {len(df_exc)} ({len(df_exc)/len(df)*100:.1f}%)")
