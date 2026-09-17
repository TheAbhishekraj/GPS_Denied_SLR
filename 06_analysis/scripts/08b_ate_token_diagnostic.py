#!/usr/bin/env python3
"""08b_ate_token_diagnostic.py — why does the ATE probe return so few hits?

The loose probe `(ATE|RMSE|drift)[^\\n]{0,40}\\d` fires on 167/171 PDFs, but the
word-bounded `\\bATE\\b` + unit pattern fires on very few. One of the two is
wrong. This script decides which, by measuring the raw token frequency and
dumping real context windows for manual reading.

Read-only. Prints a report to stdout; writes nothing.

Usage:  python 06_analysis/scripts/08b_ate_token_diagnostic.py
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:  # pragma: no cover
    import fitz  # type: ignore

REPO = Path(__file__).resolve().parents[2]
PDF_DIR = REPO / "05_papers_fulltext"
MASTER_CSV = REPO / "02_data_processed" / "extracted_master_v2.csv"

RE_BOUND_ATE = re.compile(r"\bATE\b", re.I)
RE_BOUND_RMSE = re.compile(r"\bRMSE\b", re.I)
RE_BOUND_RPE = re.compile(r"\bRPE\b", re.I)
RE_LOOSE = re.compile(r"(ATE|RMSE|drift)[^\n]{0,40}\d", re.I)
RE_ATE_UNIT = re.compile(r"\bATE\b[^\n]{0,50}?(\d+(?:\.\d+)?)\s*(km|cm|mm|m)\b", re.I)
RE_ATE_PAREN = re.compile(r"\bATE\b\s*\(\s*(km|cm|mm|m)\s*\)", re.I)
RE_ATE_LOOSE_NEAR = re.compile(r"\bATE\b[^\n]{0,50}?\d", re.I)


def main() -> int:
    texts: dict[str, str] = {}
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        with fitz.open(pdf) as doc:
            texts[pdf.stem] = "\n".join(p.get_text() for p in doc)

    def has(pattern: re.Pattern[str], text: str) -> bool:
        return bool(pattern.search(text))

    n = len(texts)
    print(f"PDFs: {n}\n")
    print("-- token presence --")
    for label, pat in (
        ("\\bATE\\b", RE_BOUND_ATE),
        ("\\bRMSE\\b", RE_BOUND_RMSE),
        ("\\bRPE\\b", RE_BOUND_RPE),
        ("\\bATE\\b + number within 50 chars", RE_ATE_LOOSE_NEAR),
        ("\\bATE\\b + number + length unit", RE_ATE_UNIT),
        ("\\bATE\\b followed by (m) header", RE_ATE_PAREN),
        ("loose (ATE|RMSE|drift)[^\\n]{0,40}\\d", RE_LOOSE),
    ):
        c = sum(1 for t in texts.values() if has(pat, t))
        print(f"  {label:<42} {c:>4} / {n}")

    print("\n-- what the loose pattern is actually matching --")
    counter: Counter[str] = Counter()
    for text in texts.values():
        for m in RE_LOOSE.finditer(text):
            token = m.group(1).lower()
            ctx = text[max(0, m.start() - 12): m.start()].lower()
            word = re.search(r"[a-z]+$", ctx)
            counter[f"{token}  <- ...{(word.group(0) if word else '')}"] += 1
    for key, c in counter.most_common(15):
        print(f"  {c:>5}  {key}")

    print("\n-- \\bATE\\b context windows (first 3 per PDF, up to 25 PDFs) --")
    shown = 0
    for pid, text in texts.items():
        m = RE_BOUND_ATE.search(text)
        if not m or shown >= 25:
            continue
        shown += 1
        snip = " ".join(text[max(0, m.start() - 70): m.end() + 50].split())
        print(f"  {pid}: ...{snip}...")

    print("\n-- ATE hit list (\\bATE\\b + number + unit) --")
    hits = [pid for pid, t in texts.items() if has(RE_ATE_UNIT, t)]
    print(f"  count: {len(hits)}")
    for pid in hits[:20]:
        m = RE_ATE_UNIT.search(texts[pid])
        snip = " ".join(texts[pid][max(0, m.start() - 40): m.end() + 20].split())
        print(f"  {pid}: {snip}")

    print("\n-- text-layer health (is the low ATE count just bad extraction?) --")
    lens = sorted(len(t) for t in texts.values())
    thin = {pid: len(t) for pid, t in texts.items() if len(t) < 3000}
    print(f"  chars: min={lens[0]} median={lens[len(lens) // 2]} max={lens[-1]}")
    print(f"  PDFs with <3000 extractable chars (likely scanned/image-only): "
          f"{len(thin)}")
    print(f"  {', '.join(sorted(thin)[:25])}")

    print("\n-- metric phrase availability (spelled out, case-insensitive) --")
    phrases = [
        "absolute trajectory error", "absolute translation error",
        "absolute translational error", "relative pose error",
        "trajectory error", "positioning error", "position error",
        "localization error", "localisation error", "accuracy",
        "rmse", "cep", "circular error", "drift", "success rate",
        "loop closure", "ground truth", "simulation",
    ]
    for phrase in phrases:
        pat = re.compile(re.escape(phrase), re.I)
        c = sum(1 for t in texts.values() if pat.search(t))
        if c:
            print(f"  {phrase:<30} {c:>4} / {n}")

    print("\n-- every \\bATE\\b occurrence in the 9 PDFs that have one --")
    for pid, text in texts.items():
        if not RE_BOUND_ATE.search(text):
            continue
        for m in list(RE_BOUND_ATE.finditer(text))[:4]:
            snip = " ".join(text[max(0, m.start() - 55): m.end() + 45].split())
            print(f"  {pid}: ...{snip}...")

    ms = MASTER_CSV
    if ms.exists():
        import csv

        with ms.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        with_ate_col = [
            r["id"] for r in rows
            if r.get("ate_rmse_m", "").strip() not in ("", "NOT_REPORTED", "n/a")
        ]
        print(f"\n-- extracted_master_v2.csv already carries ate_rmse_m for "
              f"{len(with_ate_col)} / {len(rows)} rows --")
        print("  sample:", ", ".join(with_ate_col[:15]))
        print("  overlap with \\bATE\\b+unit hits:",
              len(set(with_ate_col) & set(hits)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())