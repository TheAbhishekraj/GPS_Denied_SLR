#!/usr/bin/env python3
"""Phase 5-V / 5-K validation harness for the GPS-denied SLR.

Binding interface (RULINGS.md R3, Appendix R3-A):

    validate_screening.py sample --corpus <csv> --ai-screened <csv> --n <frac> --seed <int>
    validate_screening.py kappa  --human <csv>

Design constraints:
  * Repo-relative paths only (AGENT_RUNBOOK.md Part 0 rule 3).
  * Pure standard library: Cohen's kappa is implemented directly, so this runs in
    the project venv without scikit-learn.
  * Protocol section 4 is enforced: agreement statistics are refused until both
    reviewers' decisions are complete. No partial or placeholder statistics.
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_OUT = ROOT / "08_docs" / "validation_sample.csv"
REPORT_OUT = ROOT / "08_docs" / "screening_validation_report.md"

SAMPLE_FIELDS = ["id", "title", "abstract", "ai_decision", "ai_confidence",
                 "human1", "human2", "adjudicated"]
ID_FIELDS = ("id", "paper_id")
DECISION_FIELDS = ("decision", "ai_decision", "label")
CONFIDENCE_FIELDS = ("confidence", "ai_confidence")
VALID_DECISIONS = ("include", "exclude", "borderline_exclude")
FLOOR, CAP = 100, 300


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def pick(row: dict[str, str], names: tuple[str, ...]) -> str | None:
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip() != "":
            return str(value).strip()
    return None


def cohen_kappa(first: list[str], second: list[str]) -> float | None:
    n = len(first)
    if n == 0:
        return None
    labels = sorted(set(first) | set(second))
    observed = sum(1 for x, y in zip(first, second) if x == y) / n
    expected = sum((first.count(label) / n) * (second.count(label) / n) for label in labels)
    if abs(1.0 - expected) < 1e-12:
        return None
    return (observed - expected) / (1.0 - expected)


def raw_agreement(first: list[str], second: list[str]) -> float:
    if not first:
        return 0.0
    return sum(1 for x, y in zip(first, second) if x == y) / len(first)


def cmd_sample(args: argparse.Namespace) -> int:
    corpus_path, ai_path = Path(args.corpus), Path(args.ai_screened)
    if not corpus_path.exists():
        print(f"ERROR: corpus not found: {corpus_path}")
        return 2
    if not ai_path.exists():
        print(f"ERROR: ai-screened not found: {ai_path}")
        return 2

    corpus = read_csv(corpus_path)
    ai_rows = read_csv(ai_path)
    print(f"corpus: {corpus_path.name} -> {len(corpus)} rows")
    print(f"ai-screened: {ai_path.name} -> {len(ai_rows)} rows")

    has_decision_column = bool(ai_rows) and any(
        field in ai_rows[0] for field in DECISION_FIELDS
    )
    decisions: dict[str, tuple[str, str]] = {}
    for row in ai_rows:
        paper_id = pick(row, ID_FIELDS)
        if paper_id is None:
            continue
        decision = pick(row, DECISION_FIELDS) or "include"
        decisions[paper_id] = (decision.lower(), pick(row, CONFIDENCE_FIELDS) or "unknown")
    if not has_decision_column:
        print("WARNING: ai-screened input has no decision column; every row is read as")
        print("         'include'. Only one stratum is representable. Supply a file")
        print("         covering all decision classes to satisfy the strata gate.")

    strata: dict[str, list[dict[str, str]]] = {}
    unscreened: list[str | None] = []
    for row in corpus:
        paper_id = pick(row, ID_FIELDS)
        if paper_id in decisions:
            strata.setdefault(decisions[paper_id][0], []).append(row)
        else:
            unscreened.append(paper_id)

    screened_total = sum(len(group) for group in strata.values())
    if screened_total == 0:
        print("ERROR: no corpus paper matched an ai-screened id; nothing to sample.")
        return 2

    target = max(FLOOR, min(CAP, int(round(args.n * len(corpus)))))
    rng = random.Random(args.seed)
    sample: list[dict[str, str]] = []
    for decision in sorted(strata):
        group = strata[decision]
        quota = max(1, int(round(target * len(group) / screened_total)))
        sample.extend(rng.sample(group, min(quota, len(group))))

    SAMPLE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with SAMPLE_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SAMPLE_FIELDS)
        writer.writeheader()
        for row in sample:
            paper_id = pick(row, ID_FIELDS)
            decision, confidence = decisions[paper_id]
            writer.writerow({
                "id": paper_id,
                "title": pick(row, ("title", "Title")) or "",
                "abstract": pick(row, ("abstract", "Abstract")) or "",
                "ai_decision": decision,
                "ai_confidence": confidence,
                "human1": "", "human2": "", "adjudicated": "",
            })

    print("")
    print("strata (AI decision classes): " +
          ", ".join(f"{d}={len(g)}" for d, g in sorted(strata.items())))
    print(f"unscreened corpus rows (not sampled): {len(unscreened)}")
    print(f"target={target} (n={args.n}, floor={FLOOR}, cap={CAP}, seed={args.seed})")
    print(f"wrote {SAMPLE_OUT.name} with {len(sample)} rows")
    print("columns: " + ", ".join(SAMPLE_FIELDS))
    covered = sorted(strata)
    print(f"strata covered: {covered} ({'ALL decision classes' if len(covered) > 1 else 'ONE class only'})")
    print("")
    print("PAUSE: two humans fill human1/human2, adjudicate disagreements, then run")
    print("       'kappa --human <csv>'.")
    return 0


def cmd_kappa(args: argparse.Namespace) -> int:
    path = Path(args.human)
    if not path.exists():
        print(f"ERROR: worksheet not found: {path}")
        return 2
    rows = read_csv(path)
    if not rows:
        print("ERROR: worksheet is empty.")
        return 2

    complete = [r for r in rows
                if pick(r, ("human1",)) and pick(r, ("human2",)) and pick(r, ("adjudicated",))]
    incomplete = len(rows) - len(complete)
    if incomplete:
        print(f"REFUSING to compute: {incomplete} of {len(rows)} rows lack "
              "human1/human2/adjudicated (protocol section 4).")
        return 2

    ai = [pick(r, ("ai_decision", "decision")) or "" for r in complete]
    h1 = [pick(r, ("human1",)) or "" for r in complete]
    h2 = [pick(r, ("human2",)) or "" for r in complete]
    adj = [pick(r, ("adjudicated",)) or "" for r in complete]

    unknown = sorted({v for v in ai + h1 + h2 + adj if v not in VALID_DECISIONS})
    if unknown:
        print(f"ERROR: unrecognised decision labels: {unknown}. Permitted: {list(VALID_DECISIONS)}")
        return 2

    pairs = [("Human 1 vs Human 2", h1, h2), ("Human 1 vs AI", h1, ai),
             ("Human 2 vs AI", h2, ai), ("Adjudicated vs AI", adj, ai)]
    kappas = {name: cohen_kappa(a, b) for name, a, b in pairs}
    agreements = {name: raw_agreement(a, b) for name, a, b in pairs}
    pabak = 2 * agreements["Adjudicated vs AI"] - 1

    predicted = [v == "include" for v in ai]
    reference = [v == "include" for v in adj]
    tp = sum(1 for p, t in zip(predicted, reference) if p and t)
    fn = sum(1 for p, t in zip(predicted, reference) if not p and t)
    fp = sum(1 for p, t in zip(predicted, reference) if p and not t)
    tn = sum(1 for p, t in zip(predicted, reference) if not p and not t)
    sensitivity = tp / (tp + fn) if (tp + fn) else float("nan")
    specificity = tn / (tn + fp) if (tn + fp) else float("nan")

    ai_vs_adj = kappas["Adjudicated vs AI"]
    if ai_vs_adj is None:
        verdict, action = "UNDETERMINED", "kappa is degenerate; inspect label distributions"
    elif ai_vs_adj >= 0.80:
        verdict, action = "ACCEPT", "use AI screening as-is"
    elif ai_vs_adj >= 0.60:
        verdict, action = "CORRECT", "apply error-model correction (protocol section 5)"
    else:
        verdict, action = "REJECT", "recalibrate criteria and re-run screening"

    for name, _, _ in pairs:
        value = kappas[name]
        shown = "degenerate" if value is None else f"{value:.3f}"
        print(f"{name:<22} kappa={shown:<11} raw agreement={agreements[name]:.3f}")
    print(f"PABAK (adjudicated vs AI): {pabak:.3f}")
    print(f"AI sensitivity={sensitivity:.3f} specificity={specificity:.3f} "
          "(reference: adjudicated)")
    print(f"VERDICT: {verdict} - {action}")

    lines = [
        "# Screening validation report (Phase 5-K)",
        "",
        f"Source worksheet: `{path.name}` ({len(complete)} adjudicated rows)",
        "",
        "## Agreement statistics (protocol section 3)",
        "",
        "| Comparison | Cohen's kappa | Raw agreement |",
        "|---|---:|---:|",
    ]
    for name, _, _ in pairs:
        value = kappas[name]
        shown = "degenerate" if value is None else f"{value:.3f}"
        lines.append(f"| {name} | {shown} | {agreements[name]:.3f} |")
    lines += [
        "",
        f"- Prevalence-adjusted kappa (PABAK), adjudicated vs AI: **{pabak:.3f}**",
        f"- AI sensitivity vs adjudicated reference: **{sensitivity:.3f}**",
        f"- AI specificity vs adjudicated reference: **{specificity:.3f}**",
        "",
        "## Confusion counts (include vs not-include, AI vs adjudicated)",
        "",
        "| | adjudicated include | adjudicated not-include |",
        "|---|---:|---:|",
        f"| AI include | {tp} | {fp} |",
        f"| AI not-include | {fn} | {tn} |",
        "",
        "## Decision-rule verdict (protocol section 3)",
        "",
        "| kappa band | Action |",
        "|---|---|",
        "| >= 0.80 | accept AI screening without correction |",
        "| 0.60 - 0.80 | apply error-model correction (protocol section 5) |",
        "| < 0.60 | recalibrate prompt, re-run screening from scratch |",
        "",
    ]
    if ai_vs_adj is None:
        lines.append(f"**Verdict: {verdict}** - {action}.")
    else:
        lines.append(f"**Verdict: {verdict}** - {action} "
                     f"(AI-vs-adjudicated kappa={ai_vs_adj:.3f}).")

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {REPORT_OUT.name}")
    return 0 if verdict in ("ACCEPT", "CORRECT") else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="validate_screening.py",
        description="Phase 5-V/5-K validation harness (interface fixed by RULINGS.md R3).")
    sub = parser.add_subparsers(dest="command", required=True)

    sampler = sub.add_parser("sample", help="draw the stratified human-validation sample")
    sampler.add_argument("--corpus", required=True, help="full corpus CSV")
    sampler.add_argument("--ai-screened", required=True, help="AI-screened CSV")
    sampler.add_argument("--n", type=float, default=0.10, help="sampling fraction")
    sampler.add_argument("--seed", type=int, default=42, help="RNG seed")
    sampler.set_defaults(func=cmd_sample)

    kappa_parser = sub.add_parser("kappa", help="compute agreement and the verdict")
    kappa_parser.add_argument("--human", required=True, help="completed worksheet CSV")
    kappa_parser.set_defaults(func=cmd_kappa)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())