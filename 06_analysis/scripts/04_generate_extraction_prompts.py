#!/usr/bin/env python3
"""
04_generate_extraction_prompts.py
=================================
Generates data extraction prompts for INCLUDED papers only.

USAGE:
    python 04_generate_extraction_prompts.py

INPUT:
    - 02_data_processed/screened_included.csv

OUTPUT:
    - 03_prompts/extraction_prompts/extraction_XXXXX_*.txt (one per included paper)
"""

import pandas as pd
from pathlib import Path

PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
PROMPT_DIR = Path('E:/GPS_Denied_SLR/03_prompts/extraction_prompts')
PROMPT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GPS-DENIED SLR — STEP 4: GENERATE EXTRACTION PROMPTS")
print("=" * 70)

df = pd.read_csv(PROC_DIR / 'screened_included.csv')
print(f"\nLoading {len(df)} INCLUDED papers")
print(f"Generating extraction prompts...\n")

for idx, row in df.iterrows():
    title = str(row.get('title', row.get('Title', 'Unknown')))
    abstract = str(row.get('abstract', row.get('Abstract', 'NOT_AVAILABLE')))
    year = str(row.get('year', row.get('Year', 'Unknown')))
    authors = str(row.get('authors', row.get('Authors', 'Unknown')))
    doi = str(row.get('doi', row.get('DOI', '')))

    prompt = f"""SYSTEMATIC REVIEW DATA EXTRACTION — PAPER #{idx+1}

TITLE: {title}
AUTHORS: {authors}
YEAR: {year}
DOI: {doi}
ABSTRACT: {abstract}

=== EXTRACTION INSTRUCTIONS ===
Extract the following from the abstract. If NOT mentioned, write "NOT_IN_ABSTRACT". NEVER guess.

=== OUTPUT FORMAT ===
Return ONLY valid JSON:

{{
  "paper_number": {idx+1},
  "title": "exact title",
  "first_author": "surname of first author only",
  "year": {year},
  "venue": "venue name or NOT_IN_ABSTRACT",
  "venue_tier": "Top" or "Major" or "Regional" or "Unknown",
  "doi": "{doi}",

  "platform": ["UAV" or "UGV" or "USV" or "Underwater" or "Wearable" or "General" or "Unknown"],
  "environment": ["Indoor" or "Urban" or "Underground" or "Underwater" or "Forest" or "Adversarial" or "Mixed" or "Unknown"],

  "sensors": [
    "List each sensor mentioned. Choose from:
    Monocular_Camera, Stereo_Camera, Event_Camera, Thermal_Camera,
    LiDAR_2D, LiDAR_3D, Solid_State_LiDAR, Radar_mmWave, Sonar, Depth_Camera,
    IMU, Magnetometer, Barometer, UWB, WiFi, BLE, 5G, LoRa, Optical_Flow"
  ],

  "primary_method": "ONE of: Filter_Based_VIO, Optimization_Based_VIO, Visual_SLAM, LiDAR_SLAM, Visual_LiDAR_Inertial_Fusion, Radio_Based_Positioning, Deep_Learning_Odometry, Multi_Agent_Collaborative_SLAM, Map_Based_Localization, Hybrid_Classical_Learning, Unknown",

  "secondary_methods": ["any additional methods mentioned"],

  "performance_metric": "ATE_RMSE or RPE or Absolute_Error or Relative_Error or Other or NOT_IN_ABSTRACT",
  "performance_value": "numerical value or NOT_IN_ABSTRACT",
  "performance_unit": "m or cm or mm or % or NOT_IN_ABSTRACT",
  "dataset_used": "EuRoC or KITTI or UZH_FPV or TUM or Custom or Public or NOT_IN_ABSTRACT",
  "experiment_type": "Real_World or Simulation or Both or NOT_IN_ABSTRACT",

  "key_contribution": "One sentence: What is the NOVEL contribution?",
  "problem_solved": "One sentence: What specific GPS-denied problem does it address?",
  "methodology_summary": "Two sentences: How does it work?",
  "limitation_stated": "What limitation do authors admit?",
  "future_work_hint": "What future work do authors suggest?",

  "application_domain": ["SAR" or "Inspection" or "Agriculture" or "Driving" or "Military" or "Logistics" or "Mining" or "Marine" or "Disaster" or "Mapping" or "General" or "Unknown"],

  "citation_tier": "Core" or "Important" or "Peripheral",
  "extraction_confidence": "High" or "Medium" or "Low",
  "needs_full_text_reading": true or false
}}

CITATION TIER GUIDE:
- "Core": Breakthrough method, >100 citations likely, foundational algorithm, from top venue
- "Important": Significant improvement, good experimental validation, solid contribution
- "Peripheral": Minor variation, application-specific, limited novelty"""

    safe_title = "".join(c if c.isalnum() or c in '-_' else '_' for c in title[:50])
    filename = f"extraction_{idx+1:05d}_{safe_title}.txt"

    with open(PROMPT_DIR / filename, 'w', encoding='utf-8') as f:
        f.write(prompt)

    if (idx + 1) % 50 == 0:
        print(f"  Generated {idx+1}/{len(df)} prompts...")

print(f"\n✅ Generated {len(df)} extraction prompts in:")
print(f"   {PROMPT_DIR}")
print(f"\nNEXT STEP: Feed these prompts to AI one-by-one.")
print(f"   Save AI responses to: 04_ai_responses/extraction/")
