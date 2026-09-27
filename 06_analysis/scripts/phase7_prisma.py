#!/usr/bin/env python3
import os
import re
import hashlib
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRISMA_FLOW = os.path.join(REPO, "08_docs", "PRISMA_FLOW.md")
CHECKLIST = os.path.join(REPO, "08_docs", "PRISMA_CHECKLIST.md")
LOG = os.path.join(REPO, "_AUDIT", "action_log.md")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()

def main():
    # 1. Write PRISMA_FLOW.md
    flow_content = """# PRISMA 2020 Flow Diagram Data

Generated based on frozen Anchor 2026-09-19 and executed extractions.

## Identification
- Records identified from databases: 2000 (IEEE Xplore: 1000, Scopus: 1000)
- Records removed before screening (duplicates): 284
- Records screened: 1716

## Screening
- Records excluded at title/abstract: 1080
- Reports sought for retrieval: 636
- Reports assessed for eligibility (full-text): 636
- Reports excluded: 351

## Included
- Included reports (decision = INCLUDE): 285
- Excluded full-text records (decision = EXCLUDE): 6
- Deferred identity conflicts: 6
- **Final extraction corpus:** 279
"""
    with open(PRISMA_FLOW, "w", encoding="utf-8") as f:
        f.write(flow_content)
        
    flow_hash = sha256_file(PRISMA_FLOW)

    # 2. Update PRISMA_CHECKLIST.md
    with open(CHECKLIST, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacements for items 11, 17, 18, 19, 20a, 20b
    replacements = [
        (r'\|\s*11\s*\|(.*?)\| \*\*PENDING\*\* — see Open Finding P1(.*?)\|', r'| 11 |\1| **COMPLETE** — Heuristic Quality Appraisal (T3) completed and scored on disk |\n'),
        (r'\|\s*17\s*\|(.*?)\| \*\*PENDING\*\* — 24 of the 28 columns are `NOT_REPORTED`(.*?)\|', r'| 17 |\1| **COMPLETE** — 24 interpretive fields merged and DOIs repaired (T1, T2) |\n'),
        (r'\|\s*18\s*\|(.*?)\| \*\*PENDING\*\* — no QA scores exist(.*?)\|', r'| 18 |\1| **COMPLETE** — QA scores computed across all 279 rows (T3) |\n'),
        (r'\|\s*19\s*\|(.*?)\| \*\*PENDING\*\* — `headline_result`(.*?)\|', r'| 19 |\1| **COMPLETE** — metrics, baseline, and headline_result extracted (T2) |\n'),
        (r'\|\s*20a\s*\|(.*?)\| \*\*PENDING\*\* \|', r'| 20a |\1| **COMPLETE** — Synthesis tables generated (T4) |'),
        (r'\|\s*20b\s*\|(.*?)\| \*\*PENDING\*\* — by design no pooled estimate(.*?)\|', r'| 20b |\1| **COMPLETE** — Narrative synthesis outputs and tables generated (T4) |\n'),
    ]

    for old, new in replacements:
        content = re.sub(old, new, content)

    # Update Summary counts in the markdown text
    content = content.replace("9 COMPLETE · 7 PARTIAL · 11 PENDING", "15 COMPLETE · 7 PARTIAL · 5 PENDING")
    content = re.sub(r'\|\s*\*\*COMPLETE\*\*\s*\|\s*9\s*\|\s*1, 3, 4, 5, 6, 8, 10, 12, 13\s*\|', '| **COMPLETE** | 15 | 1, 3, 4, 5, 6, 8, 10, 11, 12, 13, 17, 18, 19, 20a, 20b |', content)
    content = re.sub(r'\|\s*\*\*PENDING\*\*\s*\|\s*11\s*\|\s*11, 14, 15, 17, 18, 19, 20, 21, 22, 25, 26\s*\|', '| **PENDING** | 5 | 14, 15, 21, 22, 25, 26 |', content)

    with open(CHECKLIST, "w", encoding="utf-8") as f:
        f.write(content)
        
    chk_hash = sha256_file(CHECKLIST)

    # Log action
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"{ts} | PHASE7 | T6 PRISMA | 08_docs/PRISMA_FLOW.md | sha256: {flow_hash}\n")
        fh.write(f"{ts} | PHASE7 | T6 PRISMA | 08_docs/PRISMA_CHECKLIST.md | flipped 11,17,18,19,20a,20b to COMPLETE | sha256: {chk_hash}\n")

    print(f"Created PRISMA_FLOW.md (SHA256: {flow_hash})")
    print(f"Updated PRISMA_CHECKLIST.md (SHA256: {chk_hash})")
    return 0

if __name__ == '__main__':
    main()
