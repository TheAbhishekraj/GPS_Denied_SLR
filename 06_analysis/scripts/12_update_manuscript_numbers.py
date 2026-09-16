#!/usr/bin/env python3
"""
12_update_manuscript_numbers.py
================================
Updates manuscript files (GPS_Denied_SLR_Manuscript_v2.md and GPS_Denied_SLR_IEEE.tex)
to replace legacy paper count references (1,692 / 1,700) with the canonical count (636).
"""

from pathlib import Path

MAN_MD = Path('07_manuscript/GPS_Denied_SLR_Manuscript_v2.md')
MAN_TEX = Path('07_manuscript/GPS_Denied_SLR_IEEE.tex')

def update_file(path: Path):
    if not path.exists():
        print(f"Skipping {path} (not found)")
        return
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        
    replacements = [
        ("1,692 peer-reviewed empirical studies", "636 peer-reviewed empirical studies"),
        ("1,692 included empirical studies", "636 included empirical studies"),
        ("1,692 from 1,719 dedup", "636 from 1,719 dedup"),
        ("1,692 empirical studies (98.4%)", "636 empirical studies (37.0%)"),
        ("27 non-empirical, orbital, or out-of-scope papers (1.6%)", "39 excluded records (2.3%)"),
        ("1,700 paper responses", "636 paper responses"),
        ("1,700 papers", "636 papers"),
        ("1,692 included studies", "636 included studies"),
        ("1,692 screened and extracted", "636 screened and extracted"),
        ("1,692", "636"),
        ("1,700", "636")
    ]
    
    modified = text
    for old_str, new_str in replacements:
        modified = modified.replace(old_str, new_str)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(modified)
    print(f"Updated {path}")

def main():
    update_file(MAN_MD)
    update_file(MAN_TEX)

if __name__ == '__main__':
    main()
