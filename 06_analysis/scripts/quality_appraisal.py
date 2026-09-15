#!/usr/bin/env python3
"""Generate the QA double-appraisal sample or apply completed QA scores."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "02_data_processed" / "extracted_master.csv"
SAMPLE = ROOT / "08_docs" / "quality_appraisal_sample.csv"
SEED = 42

QA_FIELDS = [
    "qa_rigor", "qa_reporting", "qa_baseline", "qa_repro",
    "qa_total", "qa_tier", "qa_notes",
]
CRITERIA = [
    "real_robot", "ground_truth", "repeatability",
    "absolute_and_relative_error", "trajectory_duration_scale",
    "failure_or_ablation", "established_baseline", "matched_baseline",
    "released_code_data_detail",
]
SAMPLE_FIELDS = ["paper_number", "title", "year", "experiment_type"]
for reviewer in ("appraiser1", "appraiser2"):
    SAMPLE_FIELDS.extend(f"{reviewer}_{criterion}" for criterion in CRITERIA)
SAMPLE_FIELDS.extend(["consensus_rigor", "consensus_reporting", "consensus_baseline",
                      "consensus_repro", "consensus_notes"])


def read_master() -> list[dict[str, str]]:
    with MASTER.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def generate_sample() -> None:
    rows = read_master()
    target = math.ceil(len(rows) * 0.20)
    rng = np.random.default_rng(SEED)
    indices = sorted(int(i) for i in rng.choice(len(rows), size=target, replace=False))
    with SAMPLE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SAMPLE_FIELDS)
        writer.writeheader()
        for index in indices:
            row = rows[index]
            output = {
                "paper_number": row["paper_number"],
                "title": row["title"],
                "year": row["year"],
                "experiment_type": row["experiment_type"],
            }
            output.update({field: "" for field in SAMPLE_FIELDS[4:]})
            writer.writerow(output)
    print(f"Generated {len(indices)} double-appraisal records using seed {SEED}: {SAMPLE}")


def binary(value: str, field: str) -> int:
    if value not in {"0", "1"}:
        raise ValueError(f"{field} must be 0 or 1, got {value!r}")
    return int(value)


def integer(value: str, field: str, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise ValueError(f"{field} must be an integer, got {value!r}") from error
    if not minimum <= parsed <= maximum:
        raise ValueError(f"{field} must be between {minimum} and {maximum}, got {parsed}")
    return parsed


def score(row: dict[str, str], prefix: str) -> tuple[int, int, int, int, str]:
    values = {criterion: binary(row[f"{prefix}_{criterion}"], f"{prefix}_{criterion}") for criterion in CRITERIA}
    rigor = 2 * values["real_robot"] + values["ground_truth"] + values["repeatability"]
    reporting = (
        values["absolute_and_relative_error"]
        + values["trajectory_duration_scale"]
        + values["failure_or_ablation"]
    )
    baseline = values["established_baseline"] + values["matched_baseline"]
    repro = values["released_code_data_detail"]
    if row["experiment_type"].strip().lower() == "simulation":
        rigor = min(rigor, 2)
    return rigor, reporting, baseline, repro, row.get(f"{prefix}_notes", "")


def apply_scores() -> None:
    with SAMPLE.open(newline="", encoding="utf-8-sig") as handle:
        appraisals = {row["paper_number"]: row for row in csv.DictReader(handle)}
    rows = read_master()
    for row in rows:
        appraisal = appraisals.get(row["paper_number"])
        if appraisal is None:
            raise ValueError(f"Missing QA appraisal for paper {row['paper_number']}")
        rigor = integer(appraisal["consensus_rigor"], "consensus_rigor", 0, 4)
        reporting = integer(appraisal["consensus_reporting"], "consensus_reporting", 0, 3)
        baseline = integer(appraisal["consensus_baseline"], "consensus_baseline", 0, 2)
        repro = integer(appraisal["consensus_repro"], "consensus_repro", 0, 1)
        notes = appraisal.get("consensus_notes", "")
        if not notes.strip():
            raise ValueError(f"consensus_notes is required for paper {row['paper_number']}")
        if row["experiment_type"].strip().lower() == "simulation":
            rigor = min(rigor, 2)
        total = rigor + reporting + baseline + repro
        tier = "Q-high" if total >= 7 else "Q-medium" if total >= 4 else "Q-low"
        row.update({
            "qa_rigor": str(rigor),
            "qa_reporting": str(reporting),
            "qa_baseline": str(baseline),
            "qa_repro": str(repro),
            "qa_total": str(total),
            "qa_tier": tier,
            "qa_notes": notes,
        })
    fieldnames = list(rows[0])
    for field in QA_FIELDS:
        if field not in fieldnames:
            fieldnames.append(field)
    with MASTER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Applied QA scores to {len(rows)} records: {MASTER}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("sample", "apply"))
    args = parser.parse_args()
    if args.action == "sample":
        generate_sample()
    else:
        apply_scores()


if __name__ == "__main__":
    main()
