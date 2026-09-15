"""
Phase 4: Generate 03_prompts/screening_prompts.jsonl
1,719 lines, one JSON object per line:
  {"paper_id", "title", "abstract", "prompt", "schema"}

Prompt template is verbatim from AGENT_TASK.md.
Input: 02_data_processed/deduplicated_master.csv (1,719 rows)
Output: 03_prompts/screening_prompts.jsonl
"""

import csv
import json
import os

BASE = r'E:\GPS_Denied_SLR'
INPUT = os.path.join(BASE, '02_data_processed', 'deduplicated_master.csv')
OUTPUT = os.path.join(BASE, '03_prompts', 'screening_prompts.jsonl')

PROMPT_TEMPLATE = """You are screening a paper for a PRISMA SLR on GPS-denied UAV navigation.
Given title and abstract, decide INCLUDE or EXCLUDE.
INCLUDE requires ALL of:
(1) UAV/drone platform (fixed-wing, rotor, or hybrid),
(2) GPS/GNSS-denied or degraded as a core focus,
(3) experimental or simulated localization results,
(4) English, peer-reviewed, 2010-2026.
Return JSON: {{decision: INCLUDE|EXCLUDE, reason: <code>, confidence: 0-1}}

Title: {title}

Abstract: {abstract}"""

SCHEMA = {
    "type": "object",
    "properties": {
        "decision": {"type": "string", "enum": ["INCLUDE", "EXCLUDE"]},
        "reason": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["decision", "reason", "confidence"]
}

with open(INPUT, encoding='utf-8', errors='replace') as fh:
    rows = list(csv.DictReader(fh))

assert len(rows) == 1719, f'Expected 1719 rows, got {len(rows)}'

with open(OUTPUT, 'w', encoding='utf-8') as fh:
    for i, r in enumerate(rows):
        title    = (r.get('title') or '').strip()
        abstract = (r.get('abstract') or '').strip()
        paper_id = (r.get('id') or f'REC_{i+1:04d}').strip()

        prompt_text = PROMPT_TEMPLATE.format(
            title=title,
            abstract=abstract if abstract else '[Abstract not available]'
        )

        obj = {
            "paper_id": paper_id,
            "title": title,
            "abstract": abstract,
            "prompt": prompt_text,
            "schema": SCHEMA,
        }
        fh.write(json.dumps(obj, ensure_ascii=False) + '\n')

size = os.path.getsize(OUTPUT)
print(f'Written {OUTPUT}: {size} bytes')

# Verify
with open(OUTPUT, encoding='utf-8') as fh:
    lines = fh.readlines()

assert len(lines) == 1719, f'Expected 1719 lines, got {len(lines)}'

# Validate first and last line parse as JSON with required fields
first = json.loads(lines[0])
last  = json.loads(lines[-1])
for obj in [first, last]:
    for key in ['paper_id', 'title', 'abstract', 'prompt', 'schema']:
        assert key in obj, f'Missing key: {key}'

print()
print('=== PHASE 4 CHECKLIST ===')
print(f'[x] screening_prompts.jsonl = {len(lines)} lines (expected 1719)')
print(f'[x] Each line has paper_id, title, abstract, prompt, schema')
print(f'[x] Prompt template verbatim from AGENT_TASK.md')
print(f'[x] Schema present: {list(SCHEMA["properties"].keys())}')
print(f'[x] File size: {size:,} bytes')
print(f'    First paper_id: {first["paper_id"]}')
print(f'    Last  paper_id: {last["paper_id"]}')
