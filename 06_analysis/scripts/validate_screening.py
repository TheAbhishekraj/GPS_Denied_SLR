#!/usr/bin/env python3
"""Validate AI screening with a deterministic sample and reviewer agreement."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SCREENING = ROOT / "04_ai_responses" / "screening_results.jsonl"
SAMPLE = ROOT / "08_docs" / "validation_sample.csv"
SEED = 42
DECISIONS = {"INCLUDE", "EXCLUDE", "BORDERLINE_EXCLUDE"}
HUMAN_DECISIONS = {"include", "exclude"}


def normalize_decision(value: str, *, allow_borderline: bool = True) -> str:
    decision = value.strip().upper().replace("-", "_")
    allowed = DECISIONS if allow_borderline else {"INCLUDE", "EXCLUDE"}
    if decision not in allowed:
        raise ValueError(f"Unsupported decision {value!r}; expected one of {sorted(allowed)}")
    return decision


def load_screening() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with SCREENING.open(encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON on line {line_number}") from error
            if not isinstance(row, dict):
                raise ValueError(f"Line {line_number} is not a JSON object")
            raw_decision = row.get("decision")
            if not isinstance(raw_decision, str):
                raise ValueError(f"Line {line_number} has no decision")
            row["decision"] = normalize_decision(raw_decision)
            row["source_database"] = str(
                row.get("source_database", row.get("source", "unknown"))
            ).strip() or "unknown"
            rows.append(row)
    if not rows:
        raise ValueError(f"No screening records found in {SCREENING}")
    return rows


def allocation(groups: dict[tuple[str, str], list[dict[str, str]]], target: int) -> dict[tuple[str, str], int]:
    total = sum(map(len, groups.values()))
    raw = {key: target * len(rows) / total for key, rows in groups.items()}
    sizes = {key: min(len(groups[key]), int(value)) for key, value in raw.items()}
    remaining = target - sum(sizes.values())
    order = sorted(raw, key=lambda key: (-(raw[key] - int(raw[key])), key))
    while remaining:
        progressed = False
        for key in order:
            if sizes[key] < len(groups[key]):
                sizes[key] += 1
                remaining -= 1
                progressed = True
                if not remaining:
                    break
        if not progressed:
            raise RuntimeError("Unable to allocate the requested sample across strata")
    return sizes


def cmd_sample(_: argparse.Namespace) -> None:
    rows = load_screening()
    target = min(300, max(100, int(np.ceil(len(rows) * 0.10))))
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["decision"], row["source_database"])].append(row)

    sizes = allocation(groups, target)
    rng = np.random.default_rng(SEED)
    selected: list[dict[str, str]] = []
    for key in sorted(groups):
        indices = rng.choice(len(groups[key]), size=sizes[key], replace=False)
        selected.extend(groups[key][int(index)] for index in indices)
    selected.sort(key=lambda row: str(row.get("paper_id", row.get("id", ""))))

    fields = ["paper_id", "stratum", "source_database", "decision_ai", "title", "abstract",
              "human1", "human2", "adjudicated"]
    SAMPLE.parent.mkdir(parents=True, exist_ok=True)
    with SAMPLE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in selected:
            paper_id = row.get("paper_id", row.get("id", ""))
            writer.writerow({
                "paper_id": paper_id,
                "stratum": row["decision"],
                "source_database": row["source_database"],
                "decision_ai": row["decision"],
                "title": row.get("title", ""),
                "abstract": row.get("abstract", ""),
                "human1": "",
                "human2": "",
                "adjudicated": "",
            })

    inclusion_rate = sum(row["decision"] == "INCLUDE" for row in rows) / len(rows)
    print(f"Wrote {SAMPLE} with {len(selected)} records (seed={SEED})")
    print(f"Full-corpus inclusion rate: {inclusion_rate:.1%}")
    if inclusion_rate > 0.55:
        print("WARNING: inclusion rate > 55%; tighten I2 and recalibrate.")
    for key in sorted(sizes):
        print(f"{key[0]} x {key[1]}: {sizes[key]}/{len(groups[key])}")


def kappa(a: list[str], b: list[str]) -> dict[str, float]:
    if len(a) != len(b) or not a:
        raise ValueError("Kappa requires equally sized, non-empty paired decisions")
    matrix = np.zeros((2, 2), dtype=int)
    for left, right in zip(a, b):
        matrix[int(left == "include"), int(right == "include")] += 1
    n = int(matrix.sum())
    observed = float(np.trace(matrix) / n)
    row_rates = matrix.sum(axis=1) / n
    col_rates = matrix.sum(axis=0) / n
    expected = float(np.dot(row_rates, col_rates))
    value = (observed - expected) / (1 - expected) if expected < 1 else 1.0
    return {"n": n, "po": observed, "pe": expected, "kappa": value}


def read_decisions(path: Path, field: str) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        result = {}
        for row in csv.DictReader(handle):
            key = row.get("paper_id") or row.get("id")
            if not key:
                raise ValueError(f"{path} has a row without paper_id/id")
            value = row.get(field, "")
            if value.strip().lower() not in HUMAN_DECISIONS:
                raise ValueError(f"{path}: {field} must be include or exclude")
            result[key] = value.strip().lower()
        return result


def cmd_kappa(args: argparse.Namespace) -> None:
    sample = read_decisions(SAMPLE, "decision_ai")
    human1 = read_decisions(Path(args.human1), "human1")
    human2 = read_decisions(Path(args.human2), "human2")
    adjudicated = read_decisions(Path(args.adjudicated), "adjudicated")
    ids = sorted(set(sample) & set(human1) & set(human2) & set(adjudicated))
    ai = ["include" if sample[key] == "INCLUDE" else "exclude" for key in ids]
    for label, left, right in (
        ("human1 vs human2", [human1[key] for key in ids], [human2[key] for key in ids]),
        ("human1 vs adjudicated", [human1[key] for key in ids], [adjudicated[key] for key in ids]),
        ("human2 vs adjudicated", [human2[key] for key in ids], [adjudicated[key] for key in ids]),
        ("AI vs adjudicated", ai, [adjudicated[key] for key in ids]),
    ):
        result = kappa(left, right)
        print(f"{label}: kappa={result['kappa']:.3f}, po={result['po']:.3f}, n={result['n']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("sample").set_defaults(function=cmd_sample)
    kappa_parser = subparsers.add_parser("kappa")
    kappa_parser.add_argument("--human1", required=True)
    kappa_parser.add_argument("--human2", required=True)
    kappa_parser.add_argument("--adjudicated", required=True)
    kappa_parser.set_defaults(function=cmd_kappa)
    args = parser.parse_args()
    args.function(args)


if __name__ == "__main__":
    main()
