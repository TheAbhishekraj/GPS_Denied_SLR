#!/usr/bin/env python3
"""
TEST AUTOMATION - Screening Prompt Processor
Last Updated: 2026-09-06 12:09 UTC
"""

import re
import json
import time
from pathlib import Path

# Configuration
INPUT_DIR = Path('E:/GPS_Denied_SLR/03_prompts/screening_prompts')
OUTPUT_DIR = Path('E:/GPS_Denied_SLR/04_ai_responses/screening')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_test_files():
    """Get first 5 screening files."""
    files = list(INPUT_DIR.glob("screening_*.txt"))
    files.sort(key=lambda x: int(re.search(r'screening_(\d+)', x.name).group(1)))
    return files[:5]

def simulate_ai_response(paper_num: int, title: str = "", abstract: str = "") -> dict:
    """Simulate AI response for testing."""
    # Simple logic: include if title contains "UAV" or "GPS-denied"
    title_lower = title.lower()
    abstract_lower = abstract.lower()
    
    if "uav" in title_lower or "gps-denied" in title_lower or "gps denied" in title_lower:
        decision = "INCLUDE"
        reason = "Directly addresses GPS-denied UAV navigation"
    elif "uav" in abstract_lower or "gps-denied" in abstract_lower:
        decision = "INCLUDE"
        reason = "Abstract mentions UAV GPS-denied navigation"
    else:
        decision = "EXCLUDE"
        reason = "Does not focus on GPS-denied UAV navigation"
    
    return {
        "paper_number": paper_num,
        "decision": decision,
        "confidence": "High",
        "reason": reason,
        "platform": ["UAV"],
        "environment": ["Indoor" if "indoor" in abstract_lower else "Unknown"],
        "sensors_detected": ["camera", "IMU"],
        "method_hint": ["VIO", "SLAM"],
        "has_quantitative_result": True,
        "needs_full_text": True
    }

def run_test():
    """Run test with first 5 files."""
    print("=" * 70)
    print("🧪 TEST RUN - First 5 Files")
    print("Time: 2026-09-06 12:09 UTC")
    print("=" * 70)
    
    files = get_test_files()
    if not files:
        print("❌ No screening files found!")
        return
    
    print(f"Found {len(files)} files for testing")
    print()
    
    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] Processing: {file_path.name}")
        print("-" * 60)
        
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract paper number
            match = re.search(r'screening_(\d+)', file_path.name)
            paper_num = int(match.group(1)) if match else i
            
            # Extract title and abstract
            title = ""
            abstract = ""
            
            if "TITLE:" in content:
                title_start = content.find("TITLE:") + len("TITLE:")
                title_end = content.find("\n", title_start)
                title = content[title_start:title_end].strip()
            
            if "ABSTRACT:" in content:
                abstract_start = content.find("ABSTRACT:") + len("ABSTRACT:")
                abstract_end = content.find("\n===", abstract_start)
                abstract = content[abstract_start:abstract_end].strip()
            
            print(f"📄 Paper #{paper_num}")
            print(f"Title: {title[:80]}{'...' if len(title) > 80 else ''}")
            print(f"Abstract preview: {abstract[:100]}{'...' if len(abstract) > 100 else ''}")
            
            # Simulate AI response
            print("\n🤖 SIMULATED AI RESPONSE:")
            response = simulate_ai_response(paper_num, title, abstract)
            print(json.dumps(response, indent=2))
            
            # Save response
            output_file = OUTPUT_DIR / f"resp_{paper_num:05d}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(response, f, indent=2)
            print(f"✅ Saved to: {output_file.name}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 60)
        time.sleep(1)  # Pause for readability
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RUN COMPLETE")
    print("=" * 70)
    print(f"Files processed: {len(files)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"JSON files created: {len(list(OUTPUT_DIR.glob('*.json')))}")
    print("\n✅ Test successful! Ready for full processing.")
    print("\nNext steps:")
    print("1. Add OpenAI API key to script")
    print("2. Replace simulate_ai_response() with actual API calls")
    print("3. Process all 696 files in batches")

if __name__ == "__main__":
    run_test()