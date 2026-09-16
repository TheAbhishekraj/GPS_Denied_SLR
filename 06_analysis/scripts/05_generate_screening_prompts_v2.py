#!/usr/bin/env python3
"""Phase 5-R step 2 - generate per-paper v2 screening prompts.

The criteria are embedded VERBATIM from 00_scope/screening_criteria_v2.md
(sections 1-8 + 12), so the prompt can never drift from the approved rule text.
All paths are repo-relative (AGENT_RUNBOOK.md Part 0 rule 3).
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CRITERIA = ROOT / "00_scope" / "screening_criteria_v2.md"
CORPUS = ROOT / "02_data_processed" / "deduplicated_master.csv"
OUT_DIR = ROOT / "03_prompts" / "screening_prompts_v2"
OUT_JSONL = ROOT / "03_prompts" / "screening_prompts_v2.jsonl"

HEADER = (
    "You are screening a single paper for a PRISMA 2020 systematic literature\n"
    "review on GPS-denied UAV navigation and localization. Apply screening\n"
    "criteria v2 exactly as given. Decide include, exclude, or borderline_exclude.\n"
    "\n"
    "The criteria text below is copied VERBATIM from\n"
    "00_scope/screening_criteria_v2.md (approved 2026-09-15 via RULINGS.md,\n"
    "with the R1 rate band incorporated). Criteria SHA-256: {sha}\n"
)
FOOTER = (
    "\nPAPER UNDER REVIEW\n"
    "paper_id: {pid}\n"
    "title: {title}\n"
    "abstract: {abstract}\n"
    "\n"
    "Respond with ONE JSON object and nothing else, exactly these keys:\n"
    '{{"paper_id": "{pid}",\n'
    ' "decision": "include" | "exclude" | "borderline_exclude",\n'
    ' "criteria_triggered": ["<primary code>", "<...>"],\n'
    ' "confidence": "high" | "medium" | "low",\n'
    ' "one_line_justification": "<evidence from the title/abstract>"}}\n'
    "\n"
    "Non-negotiable rules:\n"
    "- exclude and borderline_exclude MUST cite at least one code from E1-E8;\n"
    "- include MUST cite the satisfied codes from I1-I6;\n"
    "- list the primary code first, per the section 4 precedence order;\n"
    "- never guess: if the abstract is silent on a criterion, it does not hold;\n"
    "- Section 6 S1 applies: when genuinely ambiguous, prefer exclusion.\n"
)
SCHEMA = {
    "paper_id": "string",
    "decision": "include | exclude | borderline_exclude",
    "criteria_triggered": "array of I1-I6 / E1-E8 codes, primary first",
    "confidence": "high | medium | low",
    "one_line_justification": "string, cites the abstract evidence used",
}


def slice_between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j].strip()


def build_prompt(pid: str, title: str, abstract: str, core: str, schema: str, sha: str) -> str:
    return (HEADER.format(sha=sha) + "\n--- CRITERIA v2 (verbatim) ---\n" + core
            + "\n--- END CRITERIA v2 ---\n" + schema + "\n"
            + FOOTER.format(pid=pid, title=title, abstract=abstract))


def main() -> int:
    text = CRITERIA.read_text(encoding="utf-8")
    sha = hashlib.sha256(CRITERIA.read_bytes()).hexdigest()
    core = slice_between(text, "## 1. Inclusion criteria", "## 9. v1")
    schema = slice_between(text, "## 12. Required output schema", "## 13. Approval block")
    if "borderline_exclude" not in core or "STRICTNESS" not in core:
        print("REFUSING: criteria sections 1-8 incomplete (borderline/STRICTNESS missing).")
        return 2
    for code in ("I6", "E8"):
        if code not in core:
            print(f"REFUSING: approved criteria code {code} absent from section 1-8 slice.")
            return 2

    with CORPUS.open(newline="", encoding="utf-8-sig") as handle:
        papers = list(csv.DictReader(handle))
    if not papers:
        print("REFUSING: corpus is empty.")
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    for paper in papers:
        pid = paper["id"]
        prompt = build_prompt(pid, paper["title"], paper["abstract"], core, schema, sha)
        (OUT_DIR / f"prompt_{pid}.txt").write_text(prompt, encoding="utf-8")
        lines.append(json.dumps({
            "paper_id": pid,
            "title": paper["title"],
            "abstract": paper["abstract"],
            "prompt": prompt,
            "schema": SCHEMA,
            "criteria_version": "v2",
            "criteria_sha256": sha,
        }, ensure_ascii=False))

    OUT_JSONL.write_text("\n".join(lines) + "\n", encoding="utf-8")
    written = len(list(OUT_DIR.glob("prompt_*.txt")))
    blob = OUT_JSONL.read_text(encoding="utf-8")
    print(f"criteria sha256      : {sha}")
    print(f"core slice bytes     : {len(core)}   schema slice bytes: {len(schema)}")
    print(f"prompt files written : {written}")
    print(f"jsonl lines          : {len(lines)}")
    print(f"jsonl bytes          : {OUT_JSONL.stat().st_size}")
    print(f"token counts in jsonl: I6={blob.count('I6')} E8={blob.count('E8')} "
          f"STRICTNESS={blob.count('STRICTNESS')} borderline_exclude={blob.count('borderline_exclude')}")
    ok = written == len(papers) == len(lines)
    print("VERIFY:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())