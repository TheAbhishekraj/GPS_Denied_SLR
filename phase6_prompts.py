"""
Phase 6: Extraction Prompt Generation (1,692 lines)
Output: 03_prompts/extraction_prompts.jsonl
17 schema fields:
  paper_id, title, year, venue, doi, platform_type, sensor_list, primary_method,
  method_category, environment, experiment_type, metrics_reported, ate_rmse_m,
  real_or_sim, application_domain, multi_agent, notes

Enums:
  platform_type: fixed_wing, rotor, hybrid, general, unknown
  experiment_type: real, sim, both, unknown
  real_or_sim: real, sim, both, unknown
  multi_agent: true, false, unknown

Instruction: Write UNKNOWN, never guess.
"""

import csv
import json
import os

BASE = r"E:\GPS_Denied_SLR"
DEDUP_MASTER = os.path.join(BASE, "02_data_processed", "deduplicated_master.csv")
SCREENING_RESULTS = os.path.join(BASE, "04_ai_responses", "screening_results.jsonl")
OUT_JSONL = os.path.join(BASE, "03_prompts", "extraction_prompts.jsonl")

# Load screening results to identify 1,692 included
included_ids = set()
with open(SCREENING_RESULTS, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        if obj.get("decision") == "INCLUDE":
            included_ids.add(obj.get("paper_id"))

assert len(included_ids) == 1692, f"Expected 1692 included papers, got {len(included_ids)}"

# Load deduplicated master
with open(DEDUP_MASTER, "r", encoding="utf-8", errors="replace") as f:
    master_rows = list(csv.DictReader(f))

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "paper_id": {"type": "string"},
        "title": {"type": "string"},
        "year": {"type": "integer"},
        "venue": {"type": "string"},
        "doi": {"type": "string"},
        "platform_type": {"type": "string", "enum": ["fixed_wing", "rotor", "hybrid", "general", "unknown"]},
        "sensor_list": {"type": "array", "items": {"type": "string"}},
        "primary_method": {"type": "string"},
        "method_category": {"type": "string"},
        "environment": {"type": "string"},
        "experiment_type": {"type": "string", "enum": ["real", "sim", "both", "unknown"]},
        "metrics_reported": {"type": "array", "items": {"type": "string"}},
        "ate_rmse_m": {"type": ["number", "string", "null"]},
        "real_or_sim": {"type": "string", "enum": ["real", "sim", "both", "unknown"]},
        "application_domain": {"type": "string"},
        "multi_agent": {"type": ["boolean", "string"], "enum": [True, False, "unknown"]},
        "notes": {"type": "string"}
    },
    "required": [
        "paper_id", "title", "year", "venue", "doi",
        "platform_type", "sensor_list", "primary_method", "method_category",
        "environment", "experiment_type", "metrics_reported", "ate_rmse_m",
        "real_or_sim", "application_domain", "multi_agent", "notes"
    ]
}

EXTRACTION_PROMPT_TEMPLATE = """You are extracting structured metadata for a PRISMA Systematic Literature Review on GPS-Denied UAV Navigation.
Extract the 17 specified fields from the paper title and abstract below.
CRITICAL RULE: Write UNKNOWN, never guess. If a value cannot be definitively extracted from the text, write "unknown" or "UNKNOWN".

Paper ID: {paper_id}
Title: {title}
Year: {year}
Venue: {venue}
DOI: {doi}

Abstract:
{abstract}

Return JSON matching the schema with the 17 fields:
paper_id, title, year, venue, doi, platform_type, sensor_list, primary_method, method_category, environment, experiment_type, metrics_reported, ate_rmse_m, real_or_sim, application_domain, multi_agent, notes.
"""

line_count = 0
with open(OUT_JSONL, "w", encoding="utf-8") as out:
    for i, r in enumerate(master_rows, 1):
        pid = r.get("id") or f"REC_{i:04d}"
        if pid not in included_ids:
            continue

        title = r.get("title", "").strip()
        abstract = r.get("abstract", "").strip() or "[Abstract not available]"
        year_val = r.get("year", "").strip()
        try:
            year_int = int(year_val)
        except ValueError:
            year_int = 2020
        venue = r.get("venue", "").strip()
        doi = r.get("doi", "").strip()

        prompt_str = EXTRACTION_PROMPT_TEMPLATE.format(
            paper_id=pid,
            title=title,
            year=year_int,
            venue=venue,
            doi=doi,
            abstract=abstract
        )

        obj = {
            "paper_id": pid,
            "title": title,
            "year": year_int,
            "venue": venue,
            "doi": doi,
            "prompt": prompt_str,
            "schema": EXTRACTION_SCHEMA
        }

        out.write(json.dumps(obj) + "\n")
        line_count += 1

print(f"Written {OUT_JSONL}: {line_count} lines, {os.path.getsize(OUT_JSONL)} bytes")

# Checklist
print("\n=== PHASE 6 CHECKLIST ===")
c1 = (line_count == 1692)
c2 = (len(EXTRACTION_SCHEMA["required"]) == 17)
c3 = ("enum" in EXTRACTION_SCHEMA["properties"]["platform_type"] and "enum" in EXTRACTION_SCHEMA["properties"]["experiment_type"])
c4 = ("Write UNKNOWN, never guess" in EXTRACTION_PROMPT_TEMPLATE)

print(f"[{'x' if c1 else ' '}] Line count = 1,692 (got {line_count})")
print(f"[{'x' if c2 else ' '}] All 17 fields per line (required: {len(EXTRACTION_SCHEMA['required'])})")
print(f"[{'x' if c3 else ' '}] Enums constrained")
print(f"[{'x' if c4 else ' '}] \"Write UNKNOWN, never guess\" present")
