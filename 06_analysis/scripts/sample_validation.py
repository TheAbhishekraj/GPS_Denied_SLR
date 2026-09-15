#!/usr/bin/env python3
"""Create the fixed-seed, stratified human-validation sample for screening."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
INCLUDED = ROOT / "02_data_processed" / "screened_included.csv"
EXCLUDED = ROOT / "02_data_processed" / "screened_excluded.csv"
OUTPUT = ROOT / "08_docs" / "validation_sample.csv"
SEED = 42


def normalize_source(value: str) -> str:
    value = value.strip()
    if value == "IEEE_Xplore":
        return "IEEE Xplore"
    if value in {"IEEE Xplore", "Scopus"}:
        return value
    return value or "Unknown"


def load_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for path in (INCLUDED, EXCLUDED):
        with path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                decision = row["decision"].strip().upper()
                if decision not in {"INCLUDE", "EXCLUDE", "BORDERLINE_EXCLUDE"}:
                    raise ValueError(f"Unsupported AI decision: {decision}")
                row["ai_decision"] = decision
                row["source_database"] = normalize_source(row.get("source", ""))
                records.append(row)
    return records


def allocation_sizes(groups: dict[tuple[str, str], list[dict[str, str]]], target: int) -> dict[tuple[str, str], int]:
    total = sum(len(rows) for rows in groups.values())
    raw = {key: target * len(rows) / total for key, rows in groups.items()}
    sizes = {key: int(value) for key, value in raw.items()}
    remaining = target - sum(sizes.values())
    for key in sorted(raw, key=lambda item: (-(raw[item] - sizes[item]), item)):
        if remaining == 0:
            break
        if sizes[key] < len(groups[key]):
            sizes[key] += 1
            remaining -= 1
    if remaining:
        raise RuntimeError("Could not allocate the requested sample across non-empty strata.")
    return sizes


def main() -> None:
    records = load_records()
    corpus_size = len(records)
    target = min(300, max(100, int(np.ceil(corpus_size * 0.10))))
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for record in records:
        groups[(record["ai_decision"], record["source_database"])].append(record)

    rng = np.random.default_rng(SEED)
    sizes = allocation_sizes(groups, target)
    selected: list[dict[str, str]] = []
    for key in sorted(groups):
        rows = groups[key]
        indices = rng.choice(len(rows), size=sizes[key], replace=False)
        selected.extend(rows[int(index)] for index in indices)
    selected.sort(key=lambda row: int(row["paper_number"]))

    fields = [
        "paper_number", "title", "authors", "year", "venue", "source_database",
        "ai_decision", "source_file", "human1_decision", "human1_exclusion_codes",
        "human1_justification", "human2_decision", "human2_exclusion_codes",
        "human2_justification", "adjudicated_decision", "adjudication_notes",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in selected:
            writer.writerow({
                "paper_number": row["paper_number"],
                "title": row["title"],
                "authors": row["authors"],
                "year": row["year"],
                "venue": row["venue"],
                "source_database": row["source_database"],
                "ai_decision": row["ai_decision"],
                "source_file": row["source_file"],
                **{field: "" for field in fields[8:]},
            })

    print(f"Corpus: {corpus_size}")
    print(f"Sample: {len(selected)}")
    print(f"Seed: {SEED}")
    for key in sorted(sizes):
        print(f"{key[0]} x {key[1]}: {sizes[key]}/{len(groups[key])}")


if __name__ == "__main__":
    main()
