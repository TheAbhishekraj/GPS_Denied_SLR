#!/usr/bin/env python3
"""
SCREENING PROGRESS MONITOR - SIMPLE VERSION
Time: 2026-09-06 13:08 UTC
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Paths
PROMPT_DIR = Path('E:/GPS_Denied_SLR/03_prompts/screening_prompts')
RESPONSE_DIR = Path('E:/GPS_Denied_SLR/04_ai_responses/screening')

def check_status():
    """Check current screening status."""
    total_prompts = len(list(PROMPT_DIR.glob("screening_*.txt")))
    response_files = list(RESPONSE_DIR.glob("resp_*.json"))
    total_responses = len(response_files)
    
    include_count = 0
    exclude_count = 0
    errors = 0
    
    for resp_file in response_files:
        try:
            with open(resp_file, 'r') as f:
                data = json.load(f)
            if data.get('decision') == 'INCLUDE':
                include_count += 1
            elif data.get('decision') == 'EXCLUDE':
                exclude_count += 1
        except:
            errors += 1
    
    progress_percent = (total_responses / total_prompts * 100) if total_prompts > 0 else 0
    
    return {
        'total_prompts': total_prompts,
        'total_responses': total_responses,
        'include_count': include_count,
        'exclude_count': exclude_count,
        'errors': errors,
        'progress_percent': progress_percent,
        'remaining': total_prompts - total_responses,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    }

def display_status():
    """Display current status."""
    status = check_status()
    
    print("\n" + "="*60)
    print("🤖 AI SCREENING PROGRESS")
    print(f"Time: {status['timestamp']}")
    print("="*60)
    
    print(f"\n📁 Total Papers: {status['total_prompts']}")
    print(f"✅ Processed: {status['total_responses']}")
    print(f"⏳ Remaining: {status['remaining']}")
    
    # Progress bar
    bar_width = 40
    filled = int(bar_width * status['progress_percent'] / 100)
    bar = '█' * filled + '░' * (bar_width - filled)
    print(f"📈 [{bar}] {status['progress_percent']:.1f}%")
    
    print(f"\n🎯 DECISIONS:")
    print(f"   INCLUDE: {status['include_count']} papers")
    print(f"   EXCLUDE: {status['exclude_count']} papers")
    print(f"   ERRORS: {status['errors']} files")
    
    if status['total_responses'] > 0:
        # Show distribution
        total_decisions = status['include_count'] + status['exclude_count']
        if total_decisions > 0:
            include_pct = (status['include_count'] / total_decisions) * 100
            exclude_pct = (status['exclude_count'] / total_decisions) * 100
            print(f"\n📊 DISTRIBUTION:")
            print(f"   INCLUDE: {include_pct:.1f}% of screened papers")
            print(f"   EXCLUDE: {exclude_pct:.1f}% of screened papers")
    
    print(f"\n{'='*60}")
    
    return status

if __name__ == "__main__":
    display_status()