#!/usr/bin/env python3
"""10_commit_extraction.py — validate, merge and render extracted papers.

The extraction itself is authored as compact JSON (one object per paper). This
script is the only writer of the two deliverables, so no invariant can be broken
by a typo in a row:

    input  06_analysis/output/extraction_inbox/*.json   (authored records)
    output 02_data_processed/MASTER_EVIDENCE_V1.csv      (63 columns, 1 row/paper)
    output 03_extraction/per_paper/<id>.md              (16 sections, 0..15)

Enforced invariants (fail loudly, never silently repair semantics):
  I1  Every `id` exists in extracted_master_v2.csv; unknown ids abort the run.
  I2  Exactly the 63 header columns; unknown keys abort, missing keys become
      the literal `NOT_REPORTED` (never blank).
  I3  `qa_rigor`, `qa_reporting`, `qa_baseline`, `qa_reproducibility`,
      `qa_total`, `qa_tier`, `citation_tier` are copied VERBATIM from
      extracted_master_v2.csv. A supplied value that disagrees is reported and
      the master CSV wins (prompt Step 2.5 / gate G6).
  I4  `sensor_fusion_count` and every *_pct / best_* numeric column hold a bare
      number or NOT_REPORTED - never a number with a unit glued on.
  I5  `sensors_used` and `algorithmic_components` use `;` separators;
      `rq_relevance` uses `,` and only RQ1..RQ4.
  I6  CSV is written UTF-8, rows sorted by id, one trailing newline.
  I7  The per-paper MD is rendered from the template: all 15 sections present,
      no field left blank.

Usage:
    python 06_analysis/scripts/10_commit_extraction.py --check          # dry run
    python 06_analysis/scripts/10_commit_extraction.py --commit         # write
    python 06_analysis/scripts/10_commit_extraction.py --commit --gates # + G1..G6
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MASTER_CSV = REPO / "02_data_processed" / "extracted_master_v2.csv"
EVIDENCE_CSV = REPO / "02_data_processed" / "MASTER_EVIDENCE_V1.csv"
INBOX = REPO / "06_analysis" / "output" / "extraction_inbox"
PER_PAPER = REPO / "03_extraction" / "per_paper"
FAILURES = REPO / "08_docs" / "EXTRACTION_FAILURES.md"

VERBATIM_FROM_MASTER = (
    "qa_rigor", "qa_reporting", "qa_baseline", "qa_reproducibility",
    "qa_total", "qa_tier", "citation_tier",
)
NUMERIC_FIELDS = (
    "sensor_fusion_count", "number_of_runs", "best_ate_rmse", "best_rpe",
    "drift_rate_pct", "success_rate_pct", "improvement_vs_baseline_pct",
    "other_metric_value",
)
RQ_ALLOWED = {"RQ1", "RQ2", "RQ3", "RQ4"}
RE_BARE_NUMBER = re.compile(r"^-?\d+(?:\.\d+)?$")


def header_fields() -> list[str]:
    with EVIDENCE_CSV.open(newline="", encoding="utf-8") as fh:
        return next(csv.reader(fh))


def load_master() -> dict[str, dict[str, str]]:
    with MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        return {r["id"]: r for r in csv.DictReader(fh)}


def load_records() -> tuple[list[dict[str, str]], list[str]]:
    """Read the inbox.

    Two formats are accepted, and both are additive-safe:
      *.json   - a single object, or a list of objects
      *.jsonl  - one JSON object per line (recommended for long runs: an
                 appended line is committed on its own, so an interrupted run
                 cannot corrupt records that were already written)
    """
    records: list[dict[str, str]] = []
    errors: list[str] = []
    for path in sorted(INBOX.glob("*.json")) + sorted(INBOX.glob("*.jsonl")):
        raw = path.read_text(encoding="utf-8")
        try:
            if path.suffix == ".jsonl":
                for n, line in enumerate(raw.splitlines(), 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError as exc:
                        errors.append(f"{path.name}:{n}: invalid JSON ({exc})")
                        continue
                    if not isinstance(rec, dict):
                        errors.append(f"{path.name}:{n}: not an object")
                        continue
                    rec.setdefault("_source_file", f"{path.name}:{n}")
                    records.append(rec)
                continue
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}: invalid JSON ({exc})")
            continue
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            errors.append(f"{path.name}: expected object or list of objects")
            continue
        for i, rec in enumerate(data):
            if not isinstance(rec, dict):
                errors.append(f"{path.name}[{i}]: not an object")
                continue
            rec.setdefault("_source_file", path.name)
            records.append(rec)
    return records, errors


def normalise(rec: dict[str, str], fields: list[str], master: dict[str, dict[str, str]]
              ) -> tuple[dict[str, str] | None, list[str]]:
    """Return (row, notes). row is None if the record must be rejected."""
    problems: list[str] = []
    notes: list[str] = []
    rid = str(rec.get("id", "")).strip()
    if not rid:
        return None, ["record has no id"]
    if rid not in master:
        return None, [f"{rid}: id not present in extracted_master_v2.csv (prompt: STOP)"]

    unknown = set(rec) - set(fields) - {"_source_file"}
    if unknown:
        return None, [f"{rid}: unknown column(s): {', '.join(sorted(unknown))}"]

    row: dict[str, str] = {}
    for field in fields:
        value = rec.get(field, "")
        if isinstance(value, (list, tuple)):
            value = ";".join(str(v) for v in value)
        value = str(value).strip()
        row[field] = value if value != "" else "NOT_REPORTED"

    # I3 - qa_* and citation_tier come from the master CSV, verbatim.
    src = master[rid]
    for field in VERBATIM_FROM_MASTER:
        canonical = (src.get(field) or "NOT_REPORTED").strip() or "NOT_REPORTED"
        if row[field] != "NOT_REPORTED" and row[field] != canonical:
            notes.append(
                f"{rid}: supplied {field}={row[field]!r} overridden by master "
                f"CSV value {canonical!r}"
            )
        row[field] = canonical

    # I4 - numeric columns must be bare numbers or NOT_REPORTED.
    for field in NUMERIC_FIELDS:
        if row[field] == "NOT_REPORTED":
            continue
        if not RE_BARE_NUMBER.match(row[field]):
            problems.append(
                f"{rid}: {field}={row[field]!r} is not a bare number - units "
                f"belong in the *_unit column"
            )

    # I5 - separator and vocabulary checks.
    rqs = [x.strip() for x in row["rq_relevance"].split(",") if x.strip()]
    bad_rq = [x for x in rqs if x not in RQ_ALLOWED and x != "NOT_REPORTED"]
    if bad_rq:
        problems.append(f"{rid}: rq_relevance has invalid token(s) {bad_rq}")
    if row["rq_relevance"] != "NOT_REPORTED":
        row["rq_relevance"] = ",".join(rqs)
    for field in ("sensors_used", "algorithmic_components"):
        if "|" in row[field] or ("," in row[field] and ";" not in row[field]):
            notes.append(f"{rid}: {field} used a non-';' separator (normalised)")
            row[field] = ";".join(
                x.strip() for x in re.split(r"[|,]", row[field]) if x.strip()
            )

    return row, problems + notes


def render_md(row: dict[str, str]) -> str:
    """Render one paper into MASTER_PAPER_TEMPLATE.md, sections 0..15 (16 total)."""

    def g(key: str) -> str:
        return row.get(key, "NOT_REPORTED")

    def bullets(*keys: str) -> str:
        out = [f"- {g(k)}" for k in keys if g(k) != "NOT_REPORTED"]
        return "\n".join(out) if out else "- NOT_REPORTED"

    def metric(label: str, value_key: str, unit_key: str) -> str:
        val = g(value_key)
        # A cell is never left blank: when the value is absent the unit cell
        # says so too, rather than rendering as "| NOT_REPORTED |  |".
        if val == "NOT_REPORTED":
            return f"| {label} | NOT_REPORTED | NOT_REPORTED | (see extraction_source) |"
        unit = g(unit_key)
        return f"| {label} | {val} | {unit} | (see extraction_source) |"

    return f"""# {g('id')} — {g('title')}

Rendered from `01_corpus/MASTER_PAPER_TEMPLATE.md`. Machine extraction, not yet
human-verified. Every field is filled; `NOT_REPORTED` means the paper does not
report it and `NOT_STATED` means the authors do not state it. Nothing here is
inferred.

---

## 0. Identity

| Field | Value |
|---|---|
| id | `{g('id')}` |
| authors | {g('authors')} |
| title | {g('title')} |
| year | {g('year')} |
| venue | {g('venue')} |
| venue_type | {g('venue_type')} |
| doi | {g('doi')} |
| url | {g('url')} |

## 1. Abstract summary

> {g('abstract_summary')}

## 2. Problem setting

> {g('problem_setting')}

## 3. Historical context

> {g('historical_context')}

## 4. Methodology (summarized)

- **Approach family:** {g('approach_family')}
- **Named method:** {g('named_method')}
- **Core idea:** {g('core_idea')}
- **Algorithmic components:** {g('algorithmic_components')}
- **Fusion strategy:** {g('fusion_strategy')}
- **Any learning used:** {g('learning_used')}

## 5. Sensors and hardware

| Field | Value |
|---|---|
| sensors_used | {g('sensors_used')} |
| sensor_fusion_count | {g('sensor_fusion_count')} |
| hardware_platform | {g('hardware_platform')} |
| compute_onboard | {g('compute_onboard')} |
| flight_time_or_trajectory_length | {g('flight_time_or_trajectory_length')} |

## 6. Experimental setup

| Field | Value |
|---|---|
| environment_tested | {g('environment_tested')} |
| environment_category | {g('environment_category')} |
| real_or_sim | {g('real_or_sim')} |
| dataset_used | {g('dataset_used')} |
| ground_truth_method | {g('ground_truth_method')} |
| number_of_runs | {g('number_of_runs')} |

## 7. Reported performance (numeric, verbatim)

| Metric | Value | Unit | Source |
|---|---|---|---|
{metric('best_ate_rmse', 'best_ate_rmse', 'best_ate_rmse_unit')}
{metric('best_rpe', 'best_rpe', 'best_rpe_unit')}
| drift_rate | {g('drift_rate_pct')} | % | (see extraction_source) |
| success_rate | {g('success_rate_pct')} | % | (see extraction_source) |
| improvement_vs_baseline | {g('improvement_vs_baseline_pct')} | % | (see extraction_source) |
| {g('other_metric_name')} | {g('other_metric_value')} | {g('other_metric_unit')} | (see extraction_source) |

## 8. Baseline comparison

| Field | Value |
|---|---|
| baseline_compared | {g('baseline_compared')} |
| baseline_type | {g('baseline_type')} |
| head_to_head_result | {g('head_to_head_result')} |

## 9. Novelty claim

> {g('claimed_novelty')}

## 10. Reported failure modes

{bullets('failure_mode_1', 'failure_mode_2', 'failure_mode_3')}

## 11. Stated limitations

> {g('stated_limitations')}

## 12. Stated future work

> {g('stated_future_work')}

## 13. Quality appraisal (verbatim from extracted_master_v2.csv)

| Dimension | Score | Max |
|---|---|---|
| qa_rigor | {g('qa_rigor')} | 4 |
| qa_reporting | {g('qa_reporting')} | 3 |
| qa_baseline | {g('qa_baseline')} | 2 |
| qa_reproducibility | {g('qa_reproducibility')} | 1 |
| **qa_total** | **{g('qa_total')}** | **10** |
| qa_tier | {g('qa_tier')} | - |
| citation_tier | {g('citation_tier')} | - |

## 14. Extraction provenance

| Field | Value |
|---|---|
| extraction_source | {g('extraction_source')} |
| extractor | {g('extractor')} |
| verified_by_human | {g('verified_by_human')} |
| verifier_initials | {g('verifier_initials')} |
| verification_date | {g('verification_date')} |
| notes | {g('notes')} |

## 15. Cross-references for the manuscript

- **RQ:** {g('rq_relevance')}
- **Manuscript table:** {g('manuscript_table')}
- **Manuscript figure:** {g('manuscript_figure')}

---
"""


FORBIDDEN = ("1,692", "1,700", "1,719", "2,000", "281", "1,332", "495", "98.4%")
RE_FORBIDDEN = re.compile("|".join(re.escape(x) for x in FORBIDDEN))


def run_gates() -> list[tuple[str, str, str]]:
    """Return [(gate, PASS/FAIL, detail)] for G1..G6."""
    with EVIDENCE_CSV.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    master = load_master()

    def md_count() -> int:
        return len(list(PER_PAPER.glob("*.md")))

    # G5 scope = Amendment V4.1 (new artifacts only, self-referential files out).
    targets = [EVIDENCE_CSV]
    targets += sorted(PER_PAPER.glob("*.md"))
    targets += sorted((REPO / "07_manuscript").glob("*V1_171_EVIDENCE*"))
    hits: list[str] = []
    for path in targets:
        if not path.is_file() or path.suffix.lower() not in {".csv", ".md"}:
            continue
        for n, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            if RE_FORBIDDEN.search(line):
                hits.append(f"{path.name}:{n}")

    sample = REPO / "08_docs" / "MASTER_EVIDENCE_VERIFY_SAMPLE.csv"
    sample_rows = 0
    if sample.exists():
        with sample.open(newline="", encoding="utf-8") as fh:
            sample_rows = len(list(csv.DictReader(fh)))

    orphan = [r["id"] for r in rows if r["id"] not in master]
    qa_bad = [
        r["id"] for r in rows
        if r["id"] in master
        and (r.get("qa_total") or "") != (master[r["id"]].get("qa_total") or "")
    ]

    return [
        ("G1", "PASS" if len(rows) == 171 else "FAIL",
         f"data rows = {len(rows)} (need 171)"),
        ("G2", "PASS" if not orphan else "FAIL",
         f"orphan ids = {len(orphan)}" + (f": {orphan[:5]}" if orphan else "")),
        ("G3", "PASS" if md_count() == 171 else "FAIL",
         f"per-paper md = {md_count()} (need 171)"),
        ("G4", "PASS" if sample_rows == 34 else "FAIL",
         f"verify sample rows = {sample_rows} (need 34)"),
        ("G5", "PASS" if not hits else "FAIL",
         f"forbidden matches in new artifacts = {len(hits)}"
         + (f": {hits[:5]}" if hits else "")),
        ("G6", "PASS" if not qa_bad else "FAIL",
         f"qa_total mismatches = {len(qa_bad)}"
         + (f": {qa_bad[:5]}" if qa_bad else "")),
    ]


def write_sample() -> int:
    import random

    with EVIDENCE_CSV.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    if not rows:
        print("no rows to sample")
        return 1
    rng = random.Random(42)  # fixed seed, matches the protocol's SetSeed 42 intent
    picked = rng.sample(rows, min(34, len(rows)))
    picked.sort(key=lambda r: r["id"])
    out = REPO / "08_docs" / "MASTER_EVIDENCE_VERIFY_SAMPLE.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(picked)
    print(f"verify sample: {len(picked)} rows -> {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="validate/merge/render extractions")
    ap.add_argument("--commit", action="store_true", help="write the deliverables")
    ap.add_argument("--check", action="store_true", help="dry run (default)")
    ap.add_argument("--gates", action="store_true", help="run G1..G6 and report")
    ap.add_argument("--sample", action="store_true", help="write the 34-row sample")
    args = ap.parse_args()

    if args.sample:
        return write_sample()

    fields = header_fields()
    master = load_master()
    records, errors = load_records()

    good: dict[str, dict[str, str]] = {}
    notes: list[str] = []
    for rec in records:
        row, msgs = normalise(rec, fields, master)
        if row is None:
            errors.extend(msgs)
            continue
        if row["id"] in good:
            errors.append(f"{row['id']}: duplicate record in inbox")
            continue
        good[row["id"]] = row
        notes.extend(msgs)

    numeric_fields = (
        "best_ate_rmse", "best_rpe", "drift_rate_pct", "success_rate_pct",
        "improvement_vs_baseline_pct", "other_metric_value",
    )
    numeric_rows = sum(
        1 for row in good.values()
        if any(row[f] != "NOT_REPORTED" for f in numeric_fields)
    )

    print(f"header columns: {len(fields)}")
    print(f"inbox records accepted: {len(good)} / {len(records)}")
    print(f"rows with >=1 unit-anchored numeric metric: {numeric_rows} "
          f"(probe expectation ~44, band 38-61)")
    for n in notes:
        print(f"  note: {n}")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        print("nothing written; fix the inbox and re-run")
        return 1

    if not args.commit:
        print("dry run complete (--check). Nothing written.")
        return 0

    existing: dict[str, dict[str, str]] = {}
    if EVIDENCE_CSV.exists():
        with EVIDENCE_CSV.open(newline="", encoding="utf-8") as fh:
            existing = {r["id"]: r for r in csv.DictReader(fh)}
    merged = {**existing, **good}
    with EVIDENCE_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for rid in sorted(merged):
            writer.writerow(merged[rid])
    print(f"MASTER_EVIDENCE_V1.csv: {len(merged)} rows written")

    PER_PAPER.mkdir(parents=True, exist_ok=True)
    for rid, row in sorted(good.items()):
        (PER_PAPER / f"{rid}.md").write_text(render_md(row), encoding="utf-8")
    print(f"per-paper md: {len(good)} written -> {PER_PAPER}")

    if args.gates:
        print("")
        print("GATES")
        for gate, verdict, detail in run_gates():
            print(f"  {gate} {verdict}  {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())