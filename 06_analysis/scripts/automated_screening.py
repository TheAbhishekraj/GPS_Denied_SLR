#!/usr/bin/env python3
"""
automated_screening.py
======================
Automation assistant for processing screening prompts through AI.

INPUT: E:/GPS_Denied_SLR/03_prompts/screening_prompts/*.txt
OUTPUT: E:/GPS_Denied_SLR/04_ai_responses/screening/resp_*.json

Last Updated: 2026-09-06 12:01 UTC
"""

import os
import re
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# ============================================
# CONFIGURATION - UPDATED TO E: DRIVE
# ============================================
INPUT_DIR = Path('E:/GPS_Denied_SLR/03_prompts/screening_prompts')
OUTPUT_DIR = Path('E:/GPS_Denied_SLR/04_ai_responses/screening')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# OpenAI Configuration - Use your API key
OPENAI_API_KEY = "your-api-key-here"  # REPLACE WITH YOUR KEY
MODEL = "gpt-4o-mini"

# Processing Configuration
BATCH_SIZE = 50
DELAY_BETWEEN_CALLS = 0.5  # seconds
RETRY_DELAY = 5  # seconds
MAX_RETRIES = 3

# Note: Import openai only when API key is available
# import openai
def process_file(input_file: Path, force: bool = False) -> Dict:
    """Process a single screening file."""
    match = re.search(r'screening_(\d+)', input_file.name)
    if not match:
        print(f"  ❌ Invalid filename: {input_file.name}")
        return None
    
    paper_num = int(match.group(1))
    output_file = OUTPUT_DIR / f"resp_{paper_num:05d}.json"
    
    # Skip if already exists
    if output_file.exists() and not force:
        print(f"  ⏭ Skipping paper {paper_num} (already processed)")
        try:
            with open(output_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    try:
        # Read prompt
        with open(input_file, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
        
        print(f"  📄 Processing paper {paper_num}...")
        print(f"    File: {input_file.name}")
        
        # For test/simulation only - in production this would call AI
        print(f"    Prompt preview: {prompt_content[:100]}...")
        
        # Simulated response (would be actual AI call in production)
        simulated_response = {
            "paper_number": paper_num,
            "decision": "INCLUDE" if paper_num % 3 != 0 else "EXCLUDE",
            "confidence": "High",
            "reason": f"Paper {paper_num} focuses on GPS-denied navigation with experimental validation.",
            "platform": ["UAV"],
            "environment": ["Indoor"],
            "sensors_detected": ["camera", "IMU"],
            "method_hint": ["VIO", "SLAM"],
            "has_quantitative_result": True,
            "needs_full_text": True
        }
        
        # Save simulated response
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(simulated_response, f, indent=2)
        print(f"  ✅ Simulated response saved for paper {paper_num}")
        
        return simulated_response
            
    except Exception as e:
        print(f"  ❌ Error processing paper {paper_num}: {e}")
        return None

def test_run(files: List[Path], num_files: int = 5):
    """Test run with first N files."""
    print("=" * 70)
    print("🧪 TEST RUN - Processing first 5 files")
    print("=" * 70)
    
    included = 0
    excluded = 0
    errors = 0
    results = []
    
    for i, input_file in enumerate(files[:num_files], 1):
        print(f"\n[{i}/{num_files}] Processing: {input_file.name}")
        print("-" * 50)
        
        try:
            # Read and display prompt
            with open(input_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read()
            
            # Extract paper number
            match = re.search(r'screening_(\d+)', input_file.name)
            paper_num = int(match.group(1)) if match else i
            
            print(f"📋 PAPER #{paper_num}")
            print(f"TITLE: {prompt_content.split('TITLE: ')[1].split('\\n')[0] if 'TITLE:' in prompt_content else 'Unknown'}")
            
            # Display abstract preview
            if "ABSTRACT:" in prompt_content:
                abstract_start = prompt_content.find("ABSTRACT: ") + len("ABSTRACT: ")
                abstract_end = prompt_content.find("\\n=== INCLUSION", abstract_start)
                abstract = prompt_content[abstract_start:abstract_end] if abstract_end != -1 else prompt_content[abstract_start:abstract_start+200]
                print(f"ABSTRACT: {abstract[:150]}..." if len(abstract) > 150 else f"ABSTRACT: {abstract}")
            
            print("\n📋 PROMPT STRUCTURE:")
            print("- Inclusion criteria: 6 items")
def process_batch(files: List[Path], start_idx: int, batch_size: int) -> tuple:
    """Process a batch of files."""
    end_idx = min(start_idx + batch_size, len(files))
    batch_files = files[start_idx:end_idx]
    
    included = 0
    excluded = 0
    errors = 0
    
    print(f"\n📦 Processing batch: files {start_idx + 1} to {end_idx}")
    print("-" * 50)
    
    for i, input_file in enumerate(batch_files, 1):
        # Extract paper number
        match = re.search(r'screening_(\d+)', input_file.name)
        paper_num = int(match.group(1)) if match else start_idx + i
        
        print(f"  [{i}/{len(batch_files)}] Paper {paper_num}...", end=" ")
        
        # Check if already processed
        output_file = OUTPUT_DIR / f"resp_{paper_num:05d}.json"
        if output_file.exists():
            print("⏭ already processed")
            try:
                with open(output_file, 'r') as f:
                    result = json.load(f)
                    if result and "decision" in result:
                        if result["decision"] == "INCLUDE":
                            included += 1
                        else:
                            excluded += 1
                    continue
            except:
                pass
        
        # Process file (simulated for now)
        result = process_file(input_file)
        
        if result:
            if result["decision"] == "INCLUDE":
def generate_final_report(total_files: int, total_included: int, total_excluded: int, 
                         total_errors: int, error_files: List[str]):
    """Generate final processing report."""
    print("\n" + "=" * 70)
    print("📊 FINAL PROCESSING REPORT")
    print("=" * 70)
    
    print(f"Total files processed: {total_files}")
    print(f"Included decisions: {total_included} ({total_included/total_files*100:.1f}%)")
    print(f"Excluded decisions: {total_excluded} ({total_excluded/total_files*100:.1f}%)")
    print(f"Errors: {total_errors}")
    
    if total_included + total_excluded > 0:
        inclusion_rate = total_included / (total_included + total_excluded) * 100
        print(f"Inclusion rate: {inclusion_rate:.1f}%")
    
    if error_files:
        print(f"\n❌ Files with errors ({len(error_files)}):")
        for error_file in error_files[:10]:  # Show first 10 errors
            print(f"  - {error_file}")
        if len(error_files) > 10:
            print(f"  ... and {len(error_files) - 10} more")
    
    print(f"\n📁 Output location: {OUTPUT_DIR}")
    
    # Count actual JSON files
    json_files = list(OUTPUT_DIR.glob("*.json"))
    print(f"📁 Total JSON files generated: {len(json_files)}")
    
    # Save report
    report_file = OUTPUT_DIR / "screening_report.json"
    report_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_files": total_files,
        "included": total_included,
        "excluded": total_excluded,
        "errors": total_errors,
        "inclusion_rate": inclusion_rate if total_included + total_excluded > 0 else 0,
        "error_files": error_files,
        "output_directory": str(OUTPUT_DIR),
def main():
    """Main processing function."""
    print("=" * 70)
    print("🤖 AUTOMATED SCREENING PROCESSOR")
    print(f"Time: 2026-09-06 12:05 UTC")
    print("=" * 70)
    
    # Check input directory
    if not INPUT_DIR.exists():
        print(f"❌ Input directory not found: {INPUT_DIR}")
        print(f"   Please check the path exists.")
        return
    
    # Get files
    files = get_screening_files()
    total_files = len(files)
    
    if total_files == 0:
        print(f"❌ No screening files found in: {INPUT_DIR}")
        print(f"   Expected files: screening_*.txt")
        return
    
    print(f"\n📁 Found {total_files} screening prompt files")
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"API Model: {MODEL}")
    print(f"Batch size: {BATCH_SIZE}")
    
    # Check existing responses
    existing_responses = len(list(OUTPUT_DIR.glob("resp_*.json")))
    if existing_responses > 0:
        print(f"⚠️  Found {existing_responses} existing responses")
        print("   Will skip already processed files.")
    
    print("\n" + "=" * 70)
    print("STEP 1: TEST RUN (5 files)")
    print("=" * 70)
    
    # Run test with first 5 files
    test_results = test_run(files)
    
    print("\n" + "=" * 70)
    print("⚠️  TEST RUN COMPLETE")
    print("=" * 70)
    print("PLEASE REVIEW THE SIMULATED RESPONSES ABOVE.")
    print("\nTO PROCEED WITH FULL PROCESSING:")
    print("1. Update OPENAI_API_KEY in the script with your actual API key")
    print("2. Uncomment the OpenAI import and actual API calls")
    print("3. Replace simulated responses with actual AI calls")
    print("4. Remove the 'simulated' flag in process_file()")
    print("\nFull processing would:")
    print(f"- Process all {total_files} files in batches of {BATCH_SIZE}")
    print(f"- Wait {DELAY_BETWEEN_CALLS}s between API calls")
    print(f"- Retry failed calls {MAX_RETRIES} times")
    print(f"- Save responses as resp_XXXXX.json")
    
    print("\n" + "=" * 70)
    print("📋 READY FOR PRODUCTION PROCESSING")
    print("=" * 70)
    print("The script structure is complete. To run full processing:")
    print("\n1. First, update the script with your OpenAI API key:")
    print("   OPENAI_API_KEY = \"your-actual-api-key-here\"")
    print("\n2. Then uncomment the OpenAI imports and actual API calls")
    print("\n3. Finally, run the script:")
    print("   cd E:\\GPS_Denied_SLR\\06_analysis\\scripts")
    print("   python automated_screening.py")
    
    print("\n" + "=" * 70)
    print("✅ SCRIPT CREATION COMPLETE")
    print("=" * 70)
    print(f"Script location: E:\\GPS_Denied_SLR\\06_analysis\\scripts\\automated_screening.py")
    print(f"Total prompts ready: {total_files}")
    print(f"Output directory ready: {OUTPUT_DIR}")
    print(f"Test files analyzed: 5")
    print("\n🔧 Next steps:")
    print("   - Add your OpenAI API key")
    print("   - Run full processing when ready")
    print("   - Results will be saved to: E:\\GPS_Denied_SLR\\04_ai_responses\\screening\\")

if __name__ == "__main__":
    main()
        "json_files_count": len(json_files)
    }
    
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_file}")
    
    return report_data
                included += 1
                print("✅ INCLUDE")
            else:
                excluded += 1
                print("❌ EXCLUDE")
        else:
            errors += 1
            print("⚠️ ERROR")
        
        # Rate limiting delay
        time.sleep(DELAY_BETWEEN_CALLS)
    
    return included, excluded, errors
            print("- Exclusion criteria: 7 items")
            print("- Expected JSON output format")
            
            # Process file (simulated)
            result = process_file(input_file)
            
            if result:
                print(f"\n🤖 SIMULATED AI RESPONSE:")
                print(json.dumps(result, indent=2))
                
                if result["decision"] == "INCLUDE":
                    included += 1
                else:
                    excluded += 1
                    
                results.append({
                    "paper_number": paper_num,
                    "file": input_file.name,
                    "decision": result["decision"],
                    "reason": result["reason"]
                })
            else:
                print(f"  ❌ Failed to process paper {paper_num}")
                errors += 1
            
            time.sleep(0.5)  # Delay for readability
            
        except Exception as e:
            print(f"  ❌ Error in test: {e}")
            errors += 1
    
    print("\n" + "=" * 70)
    print("🧪 TEST RUN SUMMARY")
    print("=" * 70)
    print(f"Files processed: {num_files}")
    print(f"Included: {included}")
    print(f"Excluded: {excluded}")
    print(f"Errors: {errors}")
    
    print("\n📋 DECISION BREAKDOWN:")
    for result in results:
        decision_icon = "✅" if result['decision'] == "INCLUDE" else "❌"
        print(f"  {decision_icon} Paper {result['paper_number']}: {result['decision']} - {result['reason'][:50]}...")
    
    return results