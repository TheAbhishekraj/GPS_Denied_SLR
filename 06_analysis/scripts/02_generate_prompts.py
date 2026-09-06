#!/usr/bin/env python3
"""
02_generate_prompts.py
======================
Generates AI prompts for face-by-face screening of all papers.

USAGE:
    python 02_generate_prompts.py

INPUT:
    - 02_data_processed/deduplicated.csv

OUTPUT:
    - 03_prompts/screening_prompts/screening_XXXXX_*.txt (one per paper)
"""

import pandas as pd
from pathlib import Path

PROC_DIR = Path('E:/GPS_Denied_SLR/02_data_processed')
PROMPT_DIR = Path('E:/GPS_Denied_SLR/03_prompts/screening_prompts')
PROMPT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("GPS-DENIED SLR — STEP 2: GENERATE SCREENING PROMPTS")
print("=" * 70)

df = pd.read_csv(PROC_DIR / 'deduplicated.csv')
print(f"\nLoading {len(df)} papers from deduplicated.csv")
print(f"Generating prompts... This may take a minute.\n")

for idx, row in df.iterrows():
    title = str(row.get('Title', 'Unknown'))
    abstract = str(row.get('Abstract', 'NOT_AVAILABLE'))
    year = str(row.get('Year', 'Unknown'))
    authors = str(row.get('Authors', 'Unknown'))

    prompt = f"""SYSTEMATIC REVIEW SCREENING — PAPER #{idx+1}

TITLE: {title}
AUTHORS: {authors}
YEAR: {year}
ABSTRACT: {abstract}

=== INCLUSION CRITERIA (Must meet ALL) ===
1. Published 2010–2026, peer-reviewed journal or conference
2. PRIMARY focus: Localization, navigation, SLAM, odometry, or positioning in GPS/GNSS-DENIED conditions
3. Platform: UAV, UGV, USV, underwater vehicle, wearable, OR general robotics method
4. Environment: Indoor, urban canyon, underground, underwater, forest, OR adversarial (jamming/spoofing)
5. Presents a METHOD/ALGORITHM/SYSTEM (not just a survey)
6. Has SOME experimental validation (real-world OR high-fidelity simulation with metrics)

=== EXCLUSION CRITERIA (Exclude if ANY apply) ===
1. GPS/GNSS is available and used as the primary localization sensor (GPS-aided, not GPS-denied)
2. Pure communication/networking paper with no localization algorithm
3. Pure sensor calibration or hardware design with no navigation algorithm
4. Review/survey/tutorial with no primary experiments
5. Human pedestrian navigation without robotics relevance
6. Pure spacecraft orbital mechanics (no terrestrial robot)
7. Preprint without peer-reviewed counterpart
8. GNSS-processing, satellite-navigation, geolocation, or GPS-correction paper without a primary terrestrial GPS/GNSS-denied localization/navigation contribution
9. Pure spacecraft, orbital, satellite, or planetary-navigation paper without a terrestrial robotic platform

=== OUTPUT FORMAT ===
Return ONLY this JSON. No extra text.

{{
  "paper_number": {idx+1},
  "decision": "INCLUDE" or "EXCLUDE",
  "confidence": "High" or "Medium" or "Low",
  "reason": "One sentence explaining why",
  "platform": ["UAV" or "UGV" or "USV" or "Underwater" or "Wearable" or "General" or "Unknown"],
  "environment": ["Indoor" or "Urban" or "Underground" or "Underwater" or "Forest" or "Adversarial" or "Mixed" or "Unknown"],
  "sensors_detected": ["list sensors mentioned in abstract, comma-separated"],
  "method_hint": ["list methods mentioned: VIO, SLAM, Deep Learning, UWB, etc."],
  "has_quantitative_result": true or false,
  "needs_full_text": true or false
}}"""

    safe_title = "".join(c if c.isalnum() or c in '-_' else '_' for c in title[:50])
    filename = f"screening_{idx+1:05d}_{safe_title}.txt"

    with open(PROMPT_DIR / filename, 'w', encoding='utf-8') as f:
        f.write(prompt)

    if (idx + 1) % 100 == 0:
        print(f"  Generated {idx+1}/{len(df)} prompts...")

print(f"\n✅ Generated {len(df)} screening prompts in:")
print(f"   {PROMPT_DIR}")
print(f"\nNEXT STEP: Feed these prompts to AI one-by-one.")
print(f"   Save AI responses to: 04_ai_responses/screening/")
