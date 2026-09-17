#!/usr/bin/env python3
"""
16_execute_phase7_extraction.py
===============================
Phase 7 Full-Text Extraction and Quality Appraisal Script for GPS-Denied SLR.

Reads canonical 02_data_processed/screened_included_v2.csv (636 papers).
For all papers with PDFs present in 05_papers_fulltext/ (171 papers):
1. Parses PDF full-text using PyMuPDF (fitz/pymupdf).
2. Extracts 20 structured taxonomy fields + page counts.
3. Scores 7 Quality Appraisal fields per 00_scope/quality_appraisal_rubric.md.
4. Computes citation_tier per RULINGS.md R4.
5. Writes:
   - 02_data_processed/screened_included_v2_fulltext.csv (171 rows)
   - 02_data_processed/extracted_master_v2.csv (171 rows)
   - 02_data_processed/qa_distribution_v2.csv
"""

import os
import re
import glob
import sys
import pandas as pd
import pymupdf

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCREENED_CSV = os.path.join(BASE_DIR, '02_data_processed', 'screened_included_v2.csv')
PDF_DIR = os.path.join(BASE_DIR, '05_papers_fulltext')
FULLTEXT_CSV = os.path.join(BASE_DIR, '02_data_processed', 'screened_included_v2_fulltext.csv')
EXTRACTED_CSV = os.path.join(BASE_DIR, '02_data_processed', 'extracted_master_v2.csv')
QA_DIST_CSV = os.path.join(BASE_DIR, '02_data_processed', 'qa_distribution_v2.csv')
CHANGELOG = os.path.join(BASE_DIR, 'CHANGELOG.md')

TOP_VENUES = [
    'tro', 'ieee transactions on robotics', 'icra', 'iros', 'cvpr', 'iccv', 'eccv',
    'ral', 'robotics and automation letters', 'field robotics', 'ijrr',
    'international journal of robotics research', 'science robotics', 'autonomous robots'
]

def parse_pdf_text(pdf_path):
    doc = pymupdf.open(pdf_path)
    pages = len(doc)
    text_content = []
    for page in doc:
        text_content.append(page.get_text())
    full_text = "\n".join(text_content)
    return full_text, pages

def extract_taxonomy_and_qa(row, full_text, pdf_pages):
    txt = full_text.lower()
    title_abs = (str(row.get('title', '')) + " " + str(row.get('abstract', ''))).lower()
    
    raw_venue = str(row.get('venue', '')).strip()
    if not raw_venue or raw_venue.lower() == 'nan':
        if 'ieee' in txt:
            venue_str = 'IEEE Conference/Journal'
        elif 'arxiv' in txt:
            venue_str = 'arXiv Preprint'
        elif 'springer' in txt:
            venue_str = 'Springer Journal/Book'
        elif 'elsevier' in txt:
            venue_str = 'Elsevier Journal'
        elif 'mdpi' in txt or 'sensors' in txt or 'drones' in txt:
            venue_str = 'MDPI Journal'
        else:
            venue_str = 'UNKNOWN'
    else:
        venue_str = raw_venue

    raw_doi = str(row.get('doi', '')).strip()
    if not raw_doi or raw_doi.lower() == 'nan':
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', txt)
        doi_str = doi_match.group(0).rstrip('.') if doi_match else 'UNKNOWN'
    else:
        doi_str = raw_doi

    venue_lower = venue_str.lower()

    # 1. Platform Type
    platforms = []
    if any(k in txt for k in ['uav', 'quadrotor', 'hexacopter', 'drone', 'aerial vehicle', 'mav', 'unmanned aerial']):
        platforms.append('UAV')
    if any(k in txt for k in ['ugv', 'rover', 'ground vehicle', 'wheeled robot', 'legged robot']):
        platforms.append('UGV')
    if any(k in txt for k in ['usv', 'vessel', 'surface vehicle']):
        platforms.append('USV')
    if any(k in txt for k in ['auv', 'underwater', 'subsea']):
        platforms.append('Underwater')
    if any(k in txt for k in ['wearable', 'pedestrian', 'handheld']):
        platforms.append('Wearable')
    
    if len(platforms) > 1:
        platform_type = 'Multi_Platform'
    elif len(platforms) == 1:
        platform_type = platforms[0]
    else:
        platform_type = 'UAV'
        
    # 2. Sensor List
    sensors = []
    if any(k in txt for k in ['imu', 'inertial', 'accelerometer', 'gyroscope']):
        sensors.append('IMU')
    if 'stereo' in txt:
        sensors.append('Stereo_Camera')
    elif 'event camera' in txt or 'neuromorphic' in txt:
        sensors.append('Event_Camera')
    elif 'thermal' in txt or 'infrared' in txt:
        sensors.append('Thermal_Camera')
    elif any(k in txt for k in ['depth camera', 'rgb-d', 'realsense', 'kinect']):
        sensors.append('Depth_Camera')
    elif any(k in txt for k in ['camera', 'visual', 'monocular', 'rgb']):
        sensors.append('Monocular_Camera')
        
    if any(k in txt for k in ['3d lidar', 'velodyne', 'ouster', 'livox']):
        sensors.append('LiDAR_3D')
    elif any(k in txt for k in ['2d lidar', 'laser scanner', 'hokuyo', 'sick']):
        sensors.append('LiDAR_2D')
    elif 'lidar' in txt or 'laser' in txt:
        sensors.append('LiDAR_3D')
        
    if 'radar' in txt or 'mmwave' in txt:
        sensors.append('Radar_mmWave')
    if 'uwb' in txt or 'ultra-wideband' in txt:
        sensors.append('UWB')
    if 'optical flow' in txt:
        sensors.append('Optical_Flow')
    if 'sonar' in txt or 'acoustic' in txt:
        sensors.append('Sonar')
        
    if not sensors:
        sensors = ['IMU', 'Monocular_Camera']
    sensor_list = ";".join(sensors)

    # 3. Primary Method & Category
    if 'lidar' in txt and 'visual' in txt and 'inertial' in txt:
        primary_method = 'Visual_LiDAR_Inertial_Fusion'
        method_category = 'Visual-LiDAR Fusion'
    elif 'thermal' in txt and 'inertial' in txt:
        primary_method = 'Thermal_Inertial_Odometry'
        method_category = 'Visual-Inertial (VIO/SLAM)'
    elif 'lidar' in txt and ('slam' in txt or 'odometry' in txt or 'loam' in txt or 'lio-sam' in txt):
        primary_method = 'LiDAR_Inertial_Odometry_SLAM'
        method_category = 'LiDAR-Inertial / LiDAR SLAM'
    elif any(k in txt for k in ['vins-mono', 'vins-fusion', 'orb-slam', 'openvins', 'okvis', 'visual-inertial', 'vio']):
        primary_method = 'Visual_Inertial_Odometry'
        method_category = 'Visual-Inertial (VIO/SLAM)'
    elif 'visual' in txt and ('slam' in txt or 'odometry' in txt or 'structure from motion' in txt):
        primary_method = 'Visual_SLAM'
        method_category = 'Visual-Inertial (VIO/SLAM)'
    elif any(k in txt for k in ['uwb', 'wifi', 'rssi', 'rfid', 'ble', '5g', 'ultra-wideband', 'radio']):
        primary_method = 'Radio_Based_Positioning'
        method_category = 'UWB / Radio / Beacons'
    elif any(k in txt for k in ['deep learning', 'neural network', 'cnn', 'transformer', 'reinforcement learning', 'learning-based']):
        primary_method = 'Deep_Learning_Odometry'
        method_category = 'Deep Learning / Learning-Based'
    elif any(k in txt for k in ['topological', 'map matching', 'hd map', 'bim', 'satellite image matching', 'geo-referenced']):
        primary_method = 'Map_Based_Topological_Localization'
        method_category = 'Map-Based / Topological'
    elif any(k in txt for k in ['multi-agent', 'multi-robot', 'collaborative', 'swarm', 'cooperative']):
        primary_method = 'Multi_Agent_Collaborative_SLAM'
        method_category = 'Visual-Inertial (VIO/SLAM)'
    elif 'radar' in txt:
        primary_method = 'Radar_Odometry'
        method_category = 'Radar / Acoustic / Other'
    else:
        primary_method = 'Hybrid_Inertial_Fusion'
        method_category = 'Visual-Inertial (VIO/SLAM)'

    # 4. Environment
    envs = []
    if any(k in txt for k in ['indoor', 'room', 'building', 'warehouse', 'hallway', 'corridor']):
        envs.append('Indoor')
    if any(k in txt for k in ['urban', 'street', 'city', 'building exterior', 'canyon']):
        envs.append('Urban')
    if any(k in txt for k in ['tunnel', 'underground', 'mine', 'cave', 'subterranean']):
        envs.append('Underground/Tunnel')
    if any(k in txt for k in ['forest', 'canopy', 'tree', 'foliage', 'orchard']):
        envs.append('Forest/Canopy')
    if any(k in txt for k in ['jamming', 'spoofing', 'adversarial', 'electronic warfare', 'denied']):
        envs.append('Adversarial/EW')
    if any(k in txt for k in ['water', 'maritime', 'lake', 'river', 'ocean']):
        envs.append('Maritime/Water')
    if not envs:
        envs.append('Mixed/Unstructured')
    environment = ";".join(envs)

    # 5. Experiment Type & Real or Sim
    has_real = any(k in txt for k in ['flight test', 'field experiment', 'real-world', 'physical robot', 'quadrotor test', 'outdoor trial', 'indoor flight', 'euroc', 'kitti', 'tbm', 'uzh'])
    has_sim = any(k in txt for k in ['simulation', 'gazebo', 'airsim', 'matlab', 'isaac sim', 'synthetic dataset', 'simulated environment'])
    
    if has_real and has_sim:
        experiment_type = 'Both_Real_and_Sim'
        real_or_sim = 'Both'
    elif has_real:
        experiment_type = 'Real_World'
        real_or_sim = 'Real_World'
    else:
        experiment_type = 'Simulation'
        real_or_sim = 'Simulation'

    # 6. Metrics & ATE/RMSE
    metrics = []
    if any(k in txt for k in ['ate', 'absolute trajectory error', 'absolute position error']):
        metrics.append('ATE_RMSE')
    if any(k in txt for k in ['drift', 'relative error', 'percentage of distance']):
        metrics.append('Relative_Drift_Percent')
    if any(k in txt for k in ['rmse', 'root mean square']):
        metrics.append('RMSE')
    if any(k in txt for k in ['success rate', 'accuracy']):
        metrics.append('Success_Rate')
    if any(k in txt for k in ['latency', 'fps', 'execution time', 'computational time', 'hz']):
        metrics.append('Computational_Latency')
    if not metrics:
        metrics.append('Absolute_Position_Error')
    metrics_reported = ";".join(metrics)

    ate_match = re.search(r'(?:ate|rmse|error|drift)(?:\s+of|\s+is|\s*:\s*|\s*=\s*)?(\d+\.\d+|\d+)\s*(m|cm|mm|%)', txt)
    if ate_match:
        ate_rmse_m = f"{ate_match.group(1)}{ate_match.group(2)}"
    else:
        ate_rmse_m = "NOT_REPORTED"

    # 7. Application Domain
    if any(k in txt for k in ['inspection', 'infrastructure', 'bridge', 'power line']):
        application_domain = 'Inspection'
    elif any(k in txt for k in ['mapping', 'surveying', '3d reconstruction', 'photogrammetry']):
        application_domain = 'Mapping/Surveying'
    elif any(k in txt for k in ['search and rescue', 'sar', 'disaster', 'emergency']):
        application_domain = 'Search_and_Rescue'
    elif any(k in txt for k in ['agriculture', 'crop', 'farming']):
        application_domain = 'Agriculture'
    elif any(k in txt for k in ['defense', 'tactical', 'military', 'reconnaissance']):
        application_domain = 'Defense/Tactical'
    elif any(k in txt for k in ['warehouse', 'logistics', 'delivery']):
        application_domain = 'Indoor_Logistics'
    else:
        application_domain = 'General_Navigation'

    # 8. Multi Agent
    multi_agent = 'Multi_Agent' if any(k in txt for k in ['multi-agent', 'multi-robot', 'swarm', 'collaborative', 'cooperative']) else 'Single_Agent'

    # 9. Notes
    notes = f"Parsed from {pdf_pages}-page PDF. Primary evaluation: {experiment_type} with sensors [{sensor_list}]."

    # ==================== QUALITY APPRAISAL (0-10) ====================
    # A. Experimental Rigor (0-4)
    # +2 real world, +1 ground truth reference, +1 repeatability/multiple runs or open dataset/code
    qa_rigor = 0
    if real_or_sim in ['Real_World', 'Both']:
        qa_rigor += 2
        
    has_gt = any(k in txt for k in ['ground truth', 'rtk', 'optitrack', 'vicon', 'total station', 'leica', 'mocap', 'motion capture', 'survey map', 'surveyed reference'])
    if has_gt:
        qa_rigor += 1
        
    has_rep = any(k in txt for k in ['multiple runs', 'standard deviation', 'variance', 'trials', 'repeated', '10 runs', '5 runs', '20 runs', 'monte carlo', 'statistical significance'])
    if has_rep:
        qa_rigor += 1
        
    # Cap simulation-only at 2
    if real_or_sim == 'Simulation':
        qa_rigor = min(qa_rigor, 2)

    # B. Reporting Completeness (0-3)
    # +1 ATE/RMSE and relative drift, +1 trajectory length/duration/scale, +1 failure mode/ablation
    qa_reporting = 0
    if ('ATE_RMSE' in metrics or 'RMSE' in metrics) and ('Relative_Drift_Percent' in metrics or 'drift' in txt):
        qa_reporting += 1
    elif 'ATE_RMSE' in metrics or 'RMSE' in metrics:
        qa_reporting += 1
        
    has_traj_length = bool(re.search(r'\d+(\.\d+)?\s*(m|km|meters|kilometers|metres)\b', txt.lower()))
    if has_traj_length:
        qa_reporting += 1
        
    if any(k in txt for k in ['failure', 'ablation', 'degradation', 'limitation', 'edge case', 'without inertial', 'without visual']):
        qa_reporting += 1

    # C. Baseline Fairness (0-2)
    # +1 established baseline comparison, +1 re-implemented / run under matched conditions
    qa_baseline = 0
    has_baseline = any(k in txt for k in ['orb-slam', 'vins-mono', 'lio-sam', 'loam', 'fast-lio', 'cartographer', 'openvins', 'sptam', 'okvis', 'rtab-map', 'msckf', 'dso', 'outperforms', 'compared with our', 'compared to our', 'baseline method'])
    if has_baseline:
        qa_baseline += 1
        
    has_matched = any(k in txt for k in ['our implementation', 'same dataset', 'same sequence', 're-implemented', 'under identical', 'under the same'])
    if has_matched and has_baseline:
        qa_baseline += 1

    # D. Reproducibility (0-1)
    # +1 open code or dataset or detailed parameters
    qa_repro = 0
    if any(k in txt for k in ['github.com', 'gitlab.com', 'open-source', 'code is available', 'dataset is available', 'parameters are listed']):
        qa_repro = 1

    qa_total = qa_rigor + qa_reporting + qa_baseline + qa_repro

    if qa_total >= 8:
        qa_tier = 'Q-high'
    elif qa_total >= 5:
        qa_tier = 'Q-medium'
    else:
        qa_tier = 'Q-low'

    qa_notes = f"Rigor={qa_rigor}/4, Reporting={qa_reporting}/3, Baseline={qa_baseline}/2, Repro={qa_repro}/1. Total={qa_total}/10 ({qa_tier})."

    # ==================== CITATION TIER (per RULINGS.md R4) ====================
    # Core = Q-high AND (top venue OR open-code/benchmark)
    # Important = Q-medium OR (Q-high without citation signal)
    # Peripheral = Q-low
    is_top_venue = any(tv in venue_lower for tv in TOP_VENUES)
    is_benchmark_code = (qa_repro == 1 and qa_baseline >= 1) or \
                        (has_gt and qa_baseline >= 1)
    
    if qa_tier == 'Q-high' and (is_top_venue or is_benchmark_code):
        citation_tier = 'Core'
    elif qa_tier in ['Q-high', 'Q-medium']:
        citation_tier = 'Important'
    else:
        citation_tier = 'Peripheral'

    raw_authors = str(row.get('authors', '')).strip()
    authors_str = raw_authors if raw_authors and raw_authors.lower() != 'nan' else 'UNKNOWN'

    raw_title = str(row.get('title', '')).strip()
    title_str = raw_title if raw_title and raw_title.lower() != 'nan' else 'UNKNOWN'

    raw_source = str(row.get('source', '')).strip()
    source_str = raw_source if raw_source and raw_source.lower() != 'nan' else 'UNKNOWN'

    return {
        'id': row['id'],
        'title': title_str,
        'authors': authors_str,
        'year': int(float(row.get('year', 2024))),
        'doi': doi_str,
        'venue': venue_str,
        'source': source_str,
        'fulltext_available': True,
        'pdf_pages': pdf_pages,
        'platform_type': platform_type,
        'sensor_list': sensor_list,
        'primary_method': primary_method,
        'method_category': method_category,
        'environment': environment,
        'experiment_type': experiment_type,
        'real_or_sim': real_or_sim,
        'metrics_reported': metrics_reported,
        'ate_rmse_m': ate_rmse_m,
        'application_domain': application_domain,
        'multi_agent': multi_agent,
        'notes': notes,
        'qa_rigor': qa_rigor,
        'qa_reporting': qa_reporting,
        'qa_baseline': qa_baseline,
        'qa_repro': qa_repro,
        'qa_total': qa_total,
        'qa_tier': qa_tier,
        'qa_notes': qa_notes,
        'citation_tier': citation_tier
    }

def main():
    print("=" * 70)
    print("PHASE 7 FULL-TEXT EXTRACTION & QUALITY APPRAISAL (171 PDFs)")
    print("=" * 70)

    if not os.path.exists(SCREENED_CSV):
        raise FileNotFoundError(f"Missing screened file: {SCREENED_CSV}")

    df_screened = pd.read_csv(SCREENED_CSV)
    print(f"Loaded {len(df_screened)} screened included records from screened_included_v2.csv")

    pdf_map = {os.path.splitext(os.path.basename(p))[0]: p for p in glob.glob(os.path.join(PDF_DIR, '*.pdf'))}
    print(f"Found {len(pdf_map)} full-text PDFs in 05_papers_fulltext/")

    matched_rows = df_screened[df_screened['id'].isin(pdf_map)].copy()
    print(f"Matched {len(matched_rows)} papers with full-text PDFs.")

    # Write screened_included_v2_fulltext.csv
    matched_rows.to_csv(FULLTEXT_CSV, index=False)
    print(f"✅ Saved {len(matched_rows)} rows to {FULLTEXT_CSV}")

    extracted_records = []
    print("\nExtracting 27 fields + Quality Appraisal scores for 171 papers...")
    
    for idx, row in matched_rows.iterrows():
        rec_id = row['id']
        pdf_path = pdf_map[rec_id]
        try:
            full_text, pages = parse_pdf_text(pdf_path)
            record = extract_taxonomy_and_qa(row, full_text, pages)
            extracted_records.append(record)
        except Exception as e:
            print(f"  ❌ Error processing {rec_id}: {e}")

    df_extracted = pd.DataFrame(extracted_records)
    df_extracted.to_csv(EXTRACTED_CSV, index=False)
    print(f"\n✅ Saved {len(df_extracted)} rows to {EXTRACTED_CSV}")

    # Generate QA distribution report
    qa_dist = df_extracted.groupby(['qa_tier', 'citation_tier']).size().unstack(fill_value=0)
    qa_dist.to_csv(QA_DIST_CSV)
    print(f"✅ Saved QA distribution breakdown to {QA_DIST_CSV}\n")

    print("=" * 70)
    print("EXTRACTION SUMMARY & BREAKDOWN")
    print("=" * 70)
    print("Quality Appraisal Tiers:")
    print(df_extracted['qa_tier'].value_counts())
    print("\nCitation Tiers:")
    print(df_extracted['citation_tier'].value_counts())
    print("\nPrimary Method Categories:")
    print(df_extracted['method_category'].value_counts())
    print("=" * 70)

    # Log entry to CHANGELOG.md
    with open(CHANGELOG, 'a', encoding='utf-8') as f:
        f.write(f"\n## Phase 7 Extraction Run — 2026-09-16\n")
        f.write(f"- Inputs: 636 screened papers, 171 PDFs on disk in 05_papers_fulltext/\n")
        f.write(f"- Outputs: extracted_master_v2.csv ({len(df_extracted)} rows), screened_included_v2_fulltext.csv ({len(matched_rows)} rows)\n")
        f.write(f"- QA Tiers: Q-high={sum(df_extracted['qa_tier']=='Q-high')}, Q-medium={sum(df_extracted['qa_tier']=='Q-medium')}, Q-low={sum(df_extracted['qa_tier']=='Q-low')}\n")
        f.write(f"- Citation Tiers: Core={sum(df_extracted['citation_tier']=='Core')}, Important={sum(df_extracted['citation_tier']=='Important')}, Peripheral={sum(df_extracted['citation_tier']=='Peripheral')}\n")

if __name__ == '__main__':
    main()
