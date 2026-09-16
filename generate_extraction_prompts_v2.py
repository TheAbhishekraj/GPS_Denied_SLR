"""
generate_extraction_prompts_v2.py
==================================
Phase 6 — generates one extraction prompt per included paper.

Input:  02_data_processed/screened_included_v2.csv  (636 rows, REC_* keyed)
        02_data_processed/deduplicated.csv           (full metadata)
        00_scope/quality_appraisal_rubric.md         (qa_* schema)
Output: 03_prompts/extraction_prompts/prompt_<id>.json  (636 files)
        03_prompts/extraction_prompts_v2.jsonl            (636 lines)

Schema fields (MASTER_PROMPT_FINAL §4 Phase 6 + RULINGS.md R2):
  Taxonomy: id, title, authors, year, venue, doi, source,
            platform, environment, sensors, algorithm_family,
            estimation_architecture, primary_metric, metric_value,
            metric_unit, dataset_used, experiment_type,
            key_contribution, application_domain,
            fulltext_available, citation_tier, notes
  QA (7 required): qa_rigor, qa_reporting, qa_baseline, qa_repro,
                   qa_total, qa_tier, qa_notes
  Citation:        citation_count_approx, is_benchmark_paper
"""

import csv
import json
import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
INC_PATH  = ROOT / "02_data_processed" / "screened_included_v2.csv"
DEDUP_PATH = ROOT / "02_data_processed" / "deduplicated.csv"
RUBRIC_PATH = ROOT / "00_scope" / "quality_appraisal_rubric.md"
OUT_DIR   = ROOT / "03_prompts" / "extraction_prompts"
JSONL_OUT = ROOT / "03_prompts" / "extraction_prompts_v2.jsonl"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Load included IDs ────────────────────────────────────────────────────────
with open(INC_PATH, encoding="utf-8-sig") as f:
    inc_rows = list(csv.DictReader(f))
id_col = "id" if "id" in inc_rows[0] else list(inc_rows[0].keys())[0]
included_ids = {r[id_col].strip() for r in inc_rows}
print(f"Included papers: {len(included_ids)}")

# ── Load full metadata: join master (REC_* IDs) + dedup (rich cols) ──────────
MASTER_PATH = ROOT / "02_data_processed" / "deduplicated_master.csv"

with open(MASTER_PATH, encoding="utf-8-sig") as f:
    master_rows = list(csv.DictReader(f))
with open(DEDUP_PATH, encoding="utf-8-sig") as f:
    dedup_rows = list(csv.DictReader(f))

def pick(row, *names):
    for n in names:
        for k in row:
            if k.strip().lower() == n.lower() and str(row[k]).strip():
                return str(row[k]).strip()
    return ""

# Positional join is safe (verified in CHANGELOG: 1719/1719 title match at identical index)
# Merge: master provides id/abstract/source; dedup provides richer venue/authors/doi
dedup_lookup = {}
for i, mrow in enumerate(master_rows):
    rec_id = mrow.get("id", "").strip()
    if not rec_id:
        continue
    merged = dict(dedup_rows[i]) if i < len(dedup_rows) else {}
    merged.update({k: v for k, v in mrow.items() if v and v.strip()})
    dedup_lookup[rec_id] = merged

print(f"Merged lookup built: {len(dedup_lookup)} entries (master + dedup positional join)")

# ── Load rubric text ─────────────────────────────────────────────────────────
rubric_text = RUBRIC_PATH.read_text(encoding="utf-8")

# ── Output schema (required fields for extracted_master.csv) ────────────────
SCHEMA = {
    "id": "string — canonical record ID (REC_XXXX)",
    "title": "string",
    "authors": "string",
    "year": "integer",
    "venue": "string — journal or conference name",
    "doi": "string or null",
    "source": "string — IEEE_Xplore | Scopus | snowball",
    "platform": "string — UAV | UGV | USV | underwater | multi | other",
    "environment": "string — indoor | outdoor | simulation | mixed",
    "sensors": "list[string] — e.g. [IMU, LiDAR, camera, GPS_denied_confirmed]",
    "algorithm_family": "string — VIO | LiDAR_SLAM | EKF | UKF | particle_filter | DNN | hybrid | other",
    "estimation_architecture": "string — loosely_coupled | tightly_coupled | deep_learning | other",
    "primary_metric": "string — ATE | RMSE | drift_pct | RPE | success_rate | other",
    "metric_value": "number or null",
    "metric_unit": "string — m | m/s | % | deg | null",
    "dataset_used": "string — name of dataset or 'custom'",
    "experiment_type": "string — real_world | simulation | hybrid",
    "key_contribution": "string — one sentence max",
    "application_domain": "string — search_rescue | inspection | mapping | military | agriculture | other",
    "fulltext_available": "boolean — true if full text was used; false if abstract-only",
    "citation_tier": "null — to be computed in Phase 7 from qa_tier + citation signal",
    "notes": "string — any extraction caveats",
    "citation_count_approx": "integer or null — approximate citation count if visible in metadata",
    "is_benchmark_paper": "boolean — true if paper introduces a widely-used benchmark or dataset",
    "qa_rigor": "integer 0-4 — Experimental Rigor (see rubric)",
    "qa_reporting": "integer 0-3 — Reporting Completeness (see rubric)",
    "qa_baseline": "integer 0-2 — Baseline Fairness (see rubric)",
    "qa_repro": "integer 0-1 — Reproducibility (see rubric)",
    "qa_total": "integer 0-10 — sum of qa_rigor + qa_reporting + qa_baseline + qa_repro",
    "qa_tier": "string — Q-high (7-10) | Q-medium (4-6) | Q-low (0-3); simulation-only caps at Q-medium",
    "qa_notes": "string — brief rationale for each dimension score"
}

PROMPT_TEMPLATE = """\
You are a systematic review extraction assistant for the GPS-denied navigation SLR.
Extract ONLY what is explicitly stated in the paper. Do NOT infer or hallucinate values.
If a field cannot be determined from the available text, set it to null.

## Paper metadata
ID:      {id}
Title:   {title}
Authors: {authors}
Year:    {year}
Venue:   {venue}
DOI:     {doi}

## Abstract
{abstract}

## Quality Appraisal Rubric (apply STRICTLY)
{rubric}

## Extraction task
Return a single valid JSON object with EXACTLY the following fields.
Every field must be present; use null if unknown.

{schema_json}

## Rules
- citation_tier: set to null — it will be computed in Phase 7.
- qa_total: must equal qa_rigor + qa_reporting + qa_baseline + qa_repro.
- qa_tier: Q-high if qa_total >= 7; Q-medium if 4-6; Q-low if 0-3.
  Simulation-only papers (experiment_type = simulation) cap at Q-medium.
- fulltext_available: set to false if you are working from abstract only.
- Output valid JSON only; no prose before or after the JSON object.
"""

# ── Generate prompts ─────────────────────────────────────────────────────────
generated = []
missing_from_dedup = []

schema_json = json.dumps(SCHEMA, indent=2)

for rec_id in sorted(included_ids):
    meta = dedup_lookup.get(rec_id, {})
    if not meta:
        missing_from_dedup.append(rec_id)

    title    = pick(meta, "Title", "title") or pick(meta, "Document Title") or "UNKNOWN"
    authors  = pick(meta, "Authors", "authors", "Author") or ""
    year     = pick(meta, "Year", "year", "Publication Year") or ""
    venue    = pick(meta, "Venue", "venue", "Publication Title", "Source title") or ""
    doi      = pick(meta, "DOI", "doi") or ""
    abstract = pick(meta, "Abstract", "abstract") or "(abstract not available)"
    source   = pick(meta, "source", "Source") or ""

    prompt_text = PROMPT_TEMPLATE.format(
        id=rec_id, title=title, authors=authors, year=year,
        venue=venue, doi=doi, abstract=abstract[:3000],
        rubric=rubric_text, schema_json=schema_json
    )

    prompt_record = {
        "id": rec_id,
        "title": title,
        "year": year,
        "venue": venue,
        "doi": doi,
        "source": source,
        "prompt": prompt_text,
        "schema": SCHEMA
    }

    # Write individual JSON file
    out_file = OUT_DIR / f"prompt_{rec_id}.json"
    out_file.write_text(json.dumps(prompt_record, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    generated.append(prompt_record)

# Write JSONL
with open(JSONL_OUT, "w", encoding="utf-8") as f:
    for rec in generated:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"\nGenerated: {len(generated)} prompt files -> {OUT_DIR}")
print(f"JSONL:     {JSONL_OUT} ({JSONL_OUT.stat().st_size:,} bytes)")
print(f"Missing from dedup lookup: {len(missing_from_dedup)}")
if missing_from_dedup:
    print(f"  IDs: {missing_from_dedup[:10]}")

# ── Verification gate ─────────────────────────────────────────────────────────
prompt_files = list(OUT_DIR.glob("prompt_REC_*.json"))
print(f"\nVERIFICATION")
print(f"  prompt files in dir: {len(prompt_files)}")
print(f"  expected:            {len(included_ids)}")
print(f"  GATE: {'PASS' if len(prompt_files) == len(included_ids) else 'FAIL'}")

# Spot-check schema completeness
sample = json.loads(prompt_files[0].read_text(encoding="utf-8"))
has_qa = all(f"qa_{k}" in sample["schema"] for k in
             ["rigor","reporting","baseline","repro","total","tier","notes"])
print(f"  All 7 qa_* fields in schema: {'PASS' if has_qa else 'FAIL'}")
has_citation = "citation_tier" in sample["schema"]
print(f"  citation_tier field in schema: {'PASS' if has_citation else 'FAIL'}")
