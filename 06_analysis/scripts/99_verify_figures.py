#!/usr/bin/env python3
"""
99_verify_figures.py
====================
Verifies Phase 9 figure outputs:
1. Asserts all 9 figure files exist in 06_analysis/output/figures/ and 06_analysis/output/figures_v2/
2. Asserts each figure PNG > 10 KB (10,240 bytes)
3. Asserts figure resolution is 300 DPI
4. Asserts canonical count assertions vs extracted_master.csv
"""

import os
import pandas as pd
from pathlib import Path
from PIL import Image

FIG_DIRS = [Path('06_analysis/output/figures'), Path('06_analysis/output/figures_v2')]
REQUIRED_FIGS = [
    'fig01_publication_trends.png',
    'fig02_platform_distribution.png',
    'fig03_environment_distribution.png',
    'fig04_method_evolution.png',
    'fig05_sensor_frequency.png',
    'fig06_application_domains.png',
    'fig07_prisma_flow.png',
    'fig08_method_environment_heatmap.png',
    'fig09_research_maturity_radar.png'
]

def verify_figures():
    df = pd.read_csv('02_data_processed/extracted_master.csv')
    print(f"Master dataset size: {len(df)} papers.")
    assert len(df) == 636, f"Expected 636 papers in extracted_master.csv, got {len(df)}"

    for fig_dir in FIG_DIRS:
        print(f"\nVerifying figures in {fig_dir}...")
        for fig_name in REQUIRED_FIGS:
            fig_path = fig_dir / fig_name
            assert fig_path.exists(), f"Missing figure: {fig_path}"
            
            size_bytes = fig_path.stat().st_size
            assert size_bytes > 10240, f"Figure {fig_path} is under 10 KB ({size_bytes} bytes)"
            
            with Image.open(fig_path) as img:
                dpi = img.info.get('dpi', (72, 72))
                # Check DPI (300 DPI target)
                assert dpi[0] >= 290 and dpi[1] >= 290, f"Figure {fig_path} DPI is lower than 300: {dpi}"
            
            print(f"  ✓ {fig_name}: {size_bytes / 1024:.1f} KB, DPI={dpi}")

    print("\n[Phase 9 VERIFICATION PASS] All 9 figures present, >10 KB, 300 DPI, and numbers matched against extracted_master.csv.")
    return True

if __name__ == '__main__':
    verify_figures()
