"""
Phase 4: Screening Prompt Generation (v2)
Input: 02_data_processed/deduplicated_master.csv (1,719 rows)
Output: 03_prompts/screening_prompts_v2.jsonl (1,719 lines)

Each line: {"paper_id", "title", "abstract", "prompt", "schema", "criteria_version": "v2"}
"""

import csv
import json
import os

BASE = r"E:\GPS_Denied_SLR"
INPUT_CSV = os.path.join(BASE, "02_data_processed", "deduplicated_master.csv")
OUT_JSONL = os.path.join(BASE, "03_prompts", "screening_prompts_v2.jsonl")

PROMPT_TEMPLATE = """You are screening a paper for a PRISMA SLR on GPS-denied UAV navigation.
Apply criteria v2. Decide INCLUDE or EXCLUDE.

INCLUSION (ALL must hold):
 I1. UAV/drone platform (fixed-wing, rotorcraft, hybrid) OR a method
     explicitly transferable to UAVs.
 I2. The paper's PRIMARY claimed contribution is GNSS-denied navigation
     or localization. If removing the GPS-denied setting would not change
     the paper's main claim, EXCLUDE.
 I3. Quantitative localization results (ATE, RMSE, RPE, success rate,
     or equivalent) are reported.
 I4. English, peer-reviewed, 2010-01-01 to 2026-06-30.
 I5. Full text is available.

EXCLUSION (ANY triggers EXCLUDE):
 E1. Theoretical only — no experimental or simulated results.
 E2. GPS-augmented rather than GPS-denied (GPS is a fusion input, not
     the denied modality).
 E3. Non-UAV platform with no transferable result.
 E4. Quality score <= 2/8 (deferred to full-text stage).

Decision rule:
- If I1..I5 all clearly hold AND E1..E3 do not apply -> INCLUDE.
- If any of I1..I5 clearly fails OR E1..E3 applies -> EXCLUDE.
- If ambiguous -> BORDERLINE_EXCLUDE (counts as EXCLUDE for rate
  calculation; flagged for human review).

Return JSON: {{decision: INCLUDE|EXCLUDE|BORDERLINE_EXCLUDE,
              rule_triggered: I1..I5|E1..E4,
              confidence: 0.0-1.0,
              one_line_justification: string}}

Title: {title}

Abstract: {abstract}
"""

SCHEMA_V2 = {
    "type": "object",
    "properties": {
        "decision": {
            "type": "string",
            "enum": ["INCLUDE", "EXCLUDE", "BORDERLINE_EXCLUDE"]
        },
        "rule_triggered": {
            "type": "string",
            "enum": ["I1", "I2", "I3", "I4", "I5", "E1", "E2", "E3", "E4"]
        },
        "confidence": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 1.0
        },
        "one_line_justification": {
            "type": "string"
        }
    },
    "required": ["decision", "rule_triggered", "confidence", "one_line_justification"]
}

with open(INPUT_CSV, "r", encoding="utf-8", errors="replace") as f:
    rows = list(csv.DictReader(f))

assert len(rows) == 1719, f"Expected 1719 rows, got {len(rows)}"

line_count = 0
with open(OUT_JSONL, "w", encoding="utf-8") as out:
    for i, r in enumerate(rows, 1):
        paper_id = r.get("id") or f"REC_{i:04d}"
        title = r.get("title", "").strip()
        abstract = r.get("abstract", "").strip() or "[Abstract not available]"

        prompt_str = PROMPT_TEMPLATE.format(title=title, abstract=abstract)

        record = {
            "paper_id": paper_id,
            "title": title,
            "abstract": abstract,
            "prompt": prompt_str,
            "schema": SCHEMA_V2,
            "criteria_version": "v2"
        }

        out.write(json.dumps(record) + "\n")
        line_count += 1

print(f"Written {OUT_JSONL}: {line_count} lines, {os.path.getsize(OUT_JSONL)} bytes")

# Audit checks
print("\n=== PHASE 4 (v2) CHECKLIST ===")
c1 = (line_count == 1719)
c2 = True
with open(OUT_JSONL, "r", encoding="utf-8") as check_f:
    for line in check_f:
        obj = json.loads(line)
        if set(obj.keys()) != {"paper_id", "title", "abstract", "prompt", "schema", "criteria_version"}:
            c2 = False
            break
c3 = all(r in PROMPT_TEMPLATE for r in ["I1.", "I2.", "I3.", "I4.", "I5.", "E1.", "E2.", "E3.", "E4."])
c4 = "BORDERLINE_EXCLUDE" in SCHEMA_V2["properties"]["decision"]["enum"]
c5 = (SCHEMA_V2["properties"]["confidence"]["minimum"] == 0.0 and SCHEMA_V2["properties"]["confidence"]["maximum"] == 1.0)
c6 = (line_count == len(rows))

print(f"[{'x' if c1 else ' '}] screening_prompts_v2.jsonl = 1,719 lines (got {line_count})")
print(f"[{'x' if c2 else ' '}] Every line has 6 keys incl. criteria_version=\"v2\"")
print(f"[{'x' if c3 else ' '}] I1-I5 + E1-E4 all present in template")
print(f"[{'x' if c4 else ' '}] BORDERLINE_EXCLUDE included as decision value")
print(f"[{'x' if c5 else ' '}] Confidence field 0.0-1.0")
print(f"[{'x' if c6 else ' '}] No paper skipped")
