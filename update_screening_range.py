#!/usr/bin/env python3
"""
UPDATE SCREENING RANGE TO INCLUDE 2026 PAPERS
Changes "2010–2025" to "2010–2026" in all screening prompts.
"""

import os
import re
from datetime import datetime
from pathlib import Path

INPUT_DIR = Path('E:/GPS_Denied_SLR/03_prompts/screening_prompts')

def update_prompts():
    """Update year range in all screening prompts."""
    print("=" * 80)
    print("🔧 UPDATING SCREENING YEAR RANGE: 2010–2025 → 2010–2026")
    print("=" * 80)
    
    if not INPUT_DIR.exists():
        print(f"❌ Directory not found: {INPUT_DIR}")
        return
    
    # Get all screening prompt files
    prompt_files = list(INPUT_DIR.glob("screening_*.txt"))
    total_files = len(prompt_files)
    
    if total_files == 0:
        print("❌ No screening prompt files found")
        return
    
    print(f"📁 Found {total_files} screening prompt files")
    print(f"Directory: {INPUT_DIR}")
    
    # Patterns to replace
    patterns_to_update = [
        # Pattern 1: "2010–2025" with em dash
        (r'2010–2025', '2010–2026'),
        # Pattern 2: "2010-2025" with hyphen
        (r'2010-2025', '2010-2026'),
        # Pattern 3: "2010–2025" in systematic review title
        (r'GPS-Denied Environment Localization and Navigation: A Systematic Review of Sensors, Methods, and Platforms \(2010–2025\)',
         'GPS-Denied Environment Localization and Navigation: A Systematic Review of Sensors, Methods, and Platforms (2010–2026)'),
    ]
    
    updated_count = 0
    skipped_count = 0
    
    for prompt_file in prompt_files:
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all pattern replacements
            for pattern, replacement in patterns_to_update:
                content = re.sub(pattern, replacement, content)
            
            # Check if content changed
            if content != original_content:
                # Save updated content
                with open(prompt_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated_count += 1
            else:
                # Check if already has 2026
                if '2026' in content:
                    skipped_count += 1
                else:
                    print(f"⚠ {prompt_file.name}: No year range found to update")
                    skipped_count += 1
                    
        except Exception as e:
            print(f"❌ Error updating {prompt_file.name}: {e}")
    
    # Summary
    print(f"\n{'=' * 80}")
    print("📊 UPDATE SUMMARY")
    print(f"{'=' * 80}")
    print(f"✅ Updated: {updated_count} files")
    print(f"⏭️  Skipped: {skipped_count} files (already correct or no range found)")
    print(f"📈 Total: {total_files} files processed")
    
    # Verify the change
    print(f"\n🔍 VERIFICATION")
    print(f"{'=' * 80}")
    for i in range(1, min(4, total_files) + 1):
        filename = INPUT_DIR / f"screening_{i:05d}_nan.txt" if i == 1 else INPUT_DIR / f"screening_{i:05d}_*.txt"
        actual_files = list(INPUT_DIR.glob(f"screening_{i:05d}_*"))
        if actual_files:
            with open(actual_files[0], 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[:10]:
                    if '2010' in line or '2026' in line:
                        print(f"📄 {actual_files[0].name}: {line.strip()}")
    
    # Update batch processing prompt
    print(f"\n{'=' * 80}")
    print("📝 UPDATED AI SCREENING PROMPT")
    print(f"{'=' * 80}")
    print("""
Updated screening rules (now includes 2026):
- GPS/GNSS must NOT be the primary localization sensor.
- Exclude GPS-aided, GNSS-processing, satellite-navigation papers unless operating WITHOUT GPS/GNSS.
- Exclude pure communication/networking papers without localization method.
- Exclude pure spacecraft/orbital papers unless evaluating terrestrial robotics.
- Exclude surveys/reviews unless explicitly permitted.
- Publication years: 2010–2026 (NOW INCLUDES 2026).
- Do not infer unsupported metadata.
- Use needs_full_text=true for borderline cases.
""")
    
    print(f"\n✅ UPDATE COMPLETE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

if __name__ == "__main__":
    update_prompts()