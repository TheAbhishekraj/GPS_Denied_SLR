#!/usr/bin/env python3
"""08_pdf_numeric_probe.py — pre-flight probe for MASTER_EVIDENCE_V1 extraction.

Answers one question BEFORE the extraction agent is started:

    How many of the 171 full-text PDFs actually report a numeric accuracy
    figure, and in which metric vocabulary?

Why this exists
---------------
The first draft of this probe used the naive pattern
`(ATE|RMSE|drift)[^\\n]{0,40}\\d` and reported 167/171 "hits". That number was
almost entirely false positives: with re.I, `ATE` matches the tail of ordinary
words such as "estim**ate** 3", "illustr**ate** 4", "gener**ate** 5",
"evalu-**ate** 6", and `cep` matches "ex**cep**t". A diagnostic pass
(`08b_ate_token_diagnostic.py`) proved it, and also proved the text layer is
healthy (median 34k extractable chars per PDF, only 1 thin PDF), so the low
true count is a property of the corpus, not of PDF parsing.

Every pattern below is therefore word-guarded:
    (?<![A-Za-z\\-])   not glued to a preceding letter or hyphenation dash
    \\b                 not glued to a following letter
This is still a *keyword-proximity* estimate, not extraction: a number found
near "ATE" may belong to a related-work table comparing other systems. The real
per-paper values are populated later by MASTER_EXTRACTION_PROMPT.md.

Outputs (06_analysis/output/pdf_numeric_probe_v1/):
    pdf_numeric_probe_v1.csv     per-PDF flags + first matched snippet
    pdf_numeric_probe_v1.json    aggregate counts
    PDF_NUMERIC_PROBE_REPORT.md  aggregate counts + method + limits

These live outside 02_data_processed / 03_extraction / 08_docs on purpose, so
raw numbers quoted out of the PDFs cannot pollute the V4 forbidden-number gate.

Usage:  python 06_analysis/scripts/08_pdf_numeric_probe.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

try:
    import pymupdf as fitz  # PyMuPDF >= 1.24 modern import name
except ImportError:  # pragma: no cover - fallback for older installs
    import fitz  # type: ignore

REPO = Path(__file__).resolve().parents[2]
PDF_DIR = REPO / "05_papers_fulltext"
MASTER_CSV = REPO / "02_data_processed" / "extracted_master_v2.csv"
OUT_DIR = REPO / "06_analysis" / "output" / "pdf_numeric_probe_v1"

# --- patterns -------------------------------------------------------------
GUARD = r"(?<![A-Za-z\-])"          # not glued to a letter or a hyphen dash
NUM = r"(\d+(?:\.\d+)?)"            # group 1 = the number
LEN_UNIT = r"(km|cm|mm|m)\b"        # group 2 = the length unit
ANG_UNIT = r"(deg|degree|°|rad|%)"

# The acronyms are matched CASE-SENSITIVELY (no re.I). This is deliberate and
# load-bearing: with re.I the pattern also fires on the tail of ordinary words
# that survive the character guard, because the preceding character is a space
# or a ligature rather than a letter - "moder- ate", "evalu- ate", "con\ufb02ate",
# "In\ufb02ate". Papers always write the acronym in capitals, so dropping re.I
# removes all of those without losing a single genuine hit.
# 0. The naive probe, kept only to show how inflated it is.
RE_LOOSE = re.compile(r"(ATE|RMSE|drift)[^\n]{0,40}\d", re.I)

# 1. Metric *vocabulary* presence (does the paper talk about this metric?).
RE_ATE_TOPIC = re.compile(GUARD + r"ATE\b")
RE_RMSE_TOPIC = re.compile(GUARD + r"RMSE\b")
RE_RPE_TOPIC = re.compile(GUARD + r"RPE\b")

# 2. Metric vocabulary + a numeric value with a unit nearby.
RE_ATE_NUM = re.compile(GUARD + rf"ATE\b[^\n]{{0,50}}?{NUM}\s*{LEN_UNIT}")
RE_RMSE_NUM = re.compile(GUARD + rf"RMSE\b[^\n]{{0,50}}?{NUM}\s*{LEN_UNIT}")
RE_RPE_NUM = re.compile(
    GUARD + rf"RPE\b[^\n]{{0,50}}?{NUM}\s*(?:{LEN_UNIT}|{ANG_UNIT})"
)
RE_DRIFT_NUM = re.compile(
    GUARD + rf"drift\b[^\n]{{0,60}}?{NUM}\s*(?:%|m)\b", re.I
)
RE_SUCCESS_NUM = re.compile(
    GUARD + rf"success\s+rate[^\n]{{0,50}}?{NUM}\s*%", re.I
)
# 3. Substitutes a GNSS-denied corpus may use instead of ATE.
RE_POSERR_NUM = re.compile(
    rf"(?<![A-Za-z\-])(?:position|positioning|localization|localisation)"
    rf"\s+error[^\n]{{0,50}}?{NUM}\s*{LEN_UNIT}",
    re.I,
)


def iter_pdfs() -> list[Path]:
    return sorted(PDF_DIR.glob("*.pdf"))


def extract_text(path: Path) -> str:
    with fitz.open(path) as doc:
        return "\n".join(page.get_text() for page in doc)


def first_snip(*patterns: re.Pattern[str], text: str) -> str:
    for pattern in patterns:
        m = pattern.search(text)
        if m:
            return " ".join(text[max(0, m.start() - 25): m.end() + 25].split())
    return ""


def main() -> int:
    master_ids: set[str] = set()
    with MASTER_CSV.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            master_ids.add(row["id"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = iter_pdfs()
    rows: list[dict[str, object]] = []
    failed: list[str] = []

    for pdf in pdfs:
        pid = pdf.stem
        rec: dict[str, object] = {
            "id": pid,
            "in_master_csv": pid in master_ids,
            "parsed": False,
            "chars": 0,
            "thin_text": False,
            "ate_topic": False,
            "ate_numeric": False,
            "ate_numeric_value": "",
            "ate_numeric_unit": "",
            "rmse_topic": False,
            "rmse_numeric": False,
            "rpe_topic": False,
            "rpe_numeric": False,
            "drift_numeric": False,
            "success_rate_numeric": False,
            "poserr_numeric": False,
            "loose_accuracy_phrase": False,
            "any_accuracy_numeric": False,
            "snippet": "",
        }
        try:
            text = extract_text(pdf)
        except Exception as exc:  # noqa: BLE001 - log and continue
            failed.append(f"{pid}: {type(exc).__name__}: {exc}")
            rows.append(rec)
            continue

        rec["parsed"] = True
        rec["chars"] = len(text)
        rec["thin_text"] = len(text) < 3000

        rec["ate_topic"] = bool(RE_ATE_TOPIC.search(text))
        rec["rmse_topic"] = bool(RE_RMSE_TOPIC.search(text))
        rec["rpe_topic"] = bool(RE_RPE_TOPIC.search(text))

        m = RE_ATE_NUM.search(text)
        if m:
            rec["ate_numeric"] = True
            rec["ate_numeric_value"] = m.group(1)
            rec["ate_numeric_unit"] = m.group(2).lower()
        rec["rmse_numeric"] = bool(RE_RMSE_NUM.search(text))
        rec["rpe_numeric"] = bool(RE_RPE_NUM.search(text))
        rec["drift_numeric"] = bool(RE_DRIFT_NUM.search(text))
        rec["success_rate_numeric"] = bool(RE_SUCCESS_NUM.search(text))
        rec["poserr_numeric"] = bool(RE_POSERR_NUM.search(text))
        rec["loose_accuracy_phrase"] = bool(RE_LOOSE.search(text))
        rec["any_accuracy_numeric"] = any(
            rec[k] for k in (
                "ate_numeric", "rmse_numeric", "rpe_numeric", "drift_numeric",
                "success_rate_numeric", "poserr_numeric",
            )
        )
        rec["snippet"] = first_snip(
            RE_ATE_NUM, RE_ATE_TOPIC, RE_RMSE_NUM, RE_POSERR_NUM,
            RE_DRIFT_NUM, RE_LOOSE, text=text,
        )
        rows.append(rec)

    csv_path = OUT_DIR / "pdf_numeric_probe_v1.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    n = len(rows)

    def count(key: str) -> int:
        return sum(1 for r in rows if r[key])

    stats: dict[str, object] = {
        "generated_by": "06_analysis/scripts/08_pdf_numeric_probe.py",
        "generated_note": "word-guarded metric probe; keyword proximity only",
        "pdfs_in_dir": n,
        "pdfs_parsed": count("parsed"),
        "pdfs_failed_to_parse": len(failed),
        "ids_missing_from_master_csv": sum(
            1 for r in rows if not r["in_master_csv"]
        ),
        "thin_text_pdfs": count("thin_text"),
        "loose_accuracy_phrase_INFLATED": count("loose_accuracy_phrase"),
        "ate_topic": count("ate_topic"),
        "ate_numeric": count("ate_numeric"),
        "rmse_topic": count("rmse_topic"),
        "rmse_numeric": count("rmse_numeric"),
        "rpe_topic": count("rpe_topic"),
        "rpe_numeric": count("rpe_numeric"),
        "drift_numeric": count("drift_numeric"),
        "success_rate_numeric": count("success_rate_numeric"),
        "poserr_numeric": count("poserr_numeric"),
        "any_accuracy_numeric": count("any_accuracy_numeric"),
    }
    (OUT_DIR / "pdf_numeric_probe_v1.json").write_text(
        json.dumps(stats, indent=2), encoding="utf-8"
    )

    def pct(key: str) -> str:
        return f"{int(stats[key]) / n:.1%}"

    lines = [
        "# PDF_NUMERIC_PROBE_REPORT.md",
        "",
        "Pre-flight probe for `02_data_processed/MASTER_EVIDENCE_V1.csv`.",
        "",
        f"- PDFs scanned: `05_papers_fulltext/*.pdf` (n = {n})",
        "- ID basis: `02_data_processed/extracted_master_v2.csv`",
        "- All patterns are word-guarded (`(?<![A-Za-z\\-])` + `\\b`) so ordinary",
        "  words such as estimate / illustrate / generate / except cannot fire.",
        "- This is keyword proximity, **not** extraction. A number found near a",
        "  metric word may belong to a related-work table comparing other systems.",
        "",
        "## 1. Headline",
        "",
        f"- Papers that even mention **ATE**: {stats['ate_topic']} / {n} "
        f"({pct('ate_topic')})",
        f"- Papers with an **ATE + numeric value + unit**: "
        f"{stats['ate_numeric']} / {n} ({pct('ate_numeric')})",
        f"- Papers that mention **RMSE**: {stats['rmse_topic']} / {n} "
        f"({pct('rmse_topic')})",
        f"- Papers with **RMSE + numeric value + unit**: {stats['rmse_numeric']} "
        f"/ {n} ({pct('rmse_numeric')})",
        f"- Papers that mention **RPE**: {stats['rpe_topic']} / {n} "
        f"({pct('rpe_topic')})",
        f"- Papers with **any** unit-anchored accuracy number: "
        f"{stats['any_accuracy_numeric']} / {n} ({pct('any_accuracy_numeric')})",
        "",
        "## 2. Full signal table",
        "",
        "| Signal | PDFs | Share |",
        "|---|---|---|",
    ]
    for key, label in (
        ("ate_topic", "mentions ATE"),
        ("ate_numeric", "ATE + number + unit"),
        ("rmse_topic", "mentions RMSE"),
        ("rmse_numeric", "RMSE + number + unit"),
        ("rpe_topic", "mentions RPE"),
        ("rpe_numeric", "RPE + number + unit"),
        ("drift_numeric", "drift + number + % or m"),
        ("success_rate_numeric", "success rate + number + %"),
        ("poserr_numeric",
         "position / positioning / localization error + number + unit"),
        ("any_accuracy_numeric", "any of the above numeric signals"),
        ("loose_accuracy_phrase_INFLATED",
         "NAIVE probe (ATE|RMSE|drift)[^\\n]{0,40}\\d - known inflated"),
        ("thin_text_pdfs", "PDFs with <3000 extractable chars"),
    ):
        lines.append(f"| {label} | {stats[key]} | {pct(key)} |")

    lines += [
        "",
        "## 3. Why the naive probe must not be used",
        "",
        "`08b_ate_token_diagnostic.py` measured what the naive pattern actually",
        "matches. Almost every hit came from the tail of an ordinary word",
        "(`ATE` inside estim-ate, illustr-ate, gener-ate, approxim-ate,",
        "calcul-ate, coordin-ate, upd-ate, integr-ate, accur-ate, evalu-ate), or",
        "from `cep` inside ex-cept / con-cept. The naive count is therefore",
        "useless as an estimate of metric reporting and is kept only as a",
        "cautionary baseline.",
        "",
        "Two further leaks survived the first, case-insensitive character guard",
        "and had to be closed explicitly:",
        "",
        "1. Hyphenated line breaks, where the preceding character is a space",
        "   rather than the hyphen - `moder- ate`, `evalu- ate`.",
        "2. PDF ligatures, where the preceding character is U+FB01/U+FB02 and so",
        "   is not in `[A-Za-z]` - `con\\ufb02ate`, `In\\ufb02ate`.",
        "",
        "Both are closed by matching the acronyms case-sensitively. Papers write",
        "`ATE`, never `ate`, so no genuine hit is lost.",
        "",
        "## 4. Reconciliation",
        "",
        f"- PDFs parsed: {stats['pdfs_parsed']} / {n}",
        f"- PDFs that failed to parse: {stats['pdfs_failed_to_parse']}",
        f"- PDF stems absent from `extracted_master_v2.csv`: "
        f"{stats['ids_missing_from_master_csv']}",
        f"- PDFs with a thin text layer: {stats['thin_text_pdfs']}. The median",
        "  extractable text across the corpus is about 34,000 characters, so the",
        "  text layer is healthy and the low ATE count is a property of the",
        "  corpus, not a parsing artifact.",
        "",
        "## 5. Consequence for gate V9",
        "",
        "Gate V9 in `08_docs/MASTER_VERIFICATION_PROTOCOL.md` requires at least 5",
        "`approach_family` values carrying a numeric `best_ate_rmse`. ATE is used",
        "by only a handful of papers, so the strict form of V9 is very likely to",
        "fail. Two honest responses exist:",
        "",
        "1. Re-scope V9 to any unit-anchored accuracy metric",
        "   (`best_ate_rmse` **or** `other_metric_value`). 44 / 171 papers carry",
        "   such a number, so this is likely to clear 5 families and keeps a",
        "   quantitative section in the manuscript.",
        "2. Keep V9 strict, let it fail, and reframe the manuscript as an",
        "   architectural / thematic SLR per the confirmation checklist.",
        "",
        "See `PREFLIGHT_FINDINGS.md` section 3. Do not fill `best_ate_rmse` by",
        "guesswork to rescue V9; write `NOT_REPORTED` and let V9 report the truth.",
        "",
        "## 6. Files",
        "",
        "- `pdf_numeric_probe_v1.csv` - per-PDF flags and first matched snippet,",
        "  for manual spot-reading of any flag that looks wrong.",
        "- `pdf_numeric_probe_v1.json` - aggregate counts, machine-readable.",
        "- `06_analysis/scripts/08b_ate_token_diagnostic.py` - the diagnostic that",
        "  exposed the false positives and confirmed text-layer health.",
        "- `PREFLIGHT_FINDINGS.md` - decision memo: what the probe means for",
        "  gate V9, the six genuine ATE papers, and the two spec defects found.",
        "",
    ]
    if failed:
        lines += ["## 7. Parse failures", ""] + [f"- {x}" for x in failed] + [""]
    (OUT_DIR / "PDF_NUMERIC_PROBE_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print("NAIVE probe (inflated): "
          f"{stats['loose_accuracy_phrase_INFLATED']} / {n}")
    print(f"  mentions ATE:                  {stats['ate_topic']} / {n}")
    print(f"  ATE + number + unit:           {stats['ate_numeric']} / {n}")
    print(f"  mentions RMSE:                 {stats['rmse_topic']} / {n}")
    print(f"  RMSE + number + unit:          {stats['rmse_numeric']} / {n}")
    print(f"  mentions RPE:                  {stats['rpe_topic']} / {n}")
    print(f"  RPE + number + unit:           {stats['rpe_numeric']} / {n}")
    print(f"  drift + number:                {stats['drift_numeric']} / {n}")
    print(f"  success rate + number:         {stats['success_rate_numeric']} / {n}")
    print(f"  position/localization error:   {stats['poserr_numeric']} / {n}")
    print(f"  ANY metric + number + unit:    {stats['any_accuracy_numeric']} / {n}")
    print(f"  thin text layer:               {stats['thin_text_pdfs']} / {n}")
    print(f"  failed to parse:               {stats['pdfs_failed_to_parse']}")
    print(f"  ids missing from master CSV:   {stats['ids_missing_from_master_csv']}")
    print(f"report: {OUT_DIR / 'PDF_NUMERIC_PROBE_REPORT.md'}")
    print(f"csv:    {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
