import argparse
import csv
import json
import pathlib
import random
from collections import Counter
from sklearn.metrics import cohen_kappa_score

ROOT = pathlib.Path(__file__).resolve().parents[2]

def cmd_sample(args):
    src = ROOT / "04_ai_responses/screening_results_v2.jsonl"
    if not src.exists():
        print(f"Error: {src} does not exist yet. Run Phase 5 first.")
        return
    rows = []
    with src.open("r", encoding="utf-8") as f:
        for l in f:
            if l.strip():
                rows.append(json.loads(l))

    random.seed(42)
    # Stratified: 10% per decision, floor 100, cap 300
    by_dec = {}
    for r in rows:
        by_dec.setdefault(r["decision"], []).append(r)
    n_total = len(rows)
    n_target = min(300, max(100, int(0.10 * n_total)))
    sample = []
    for dec, group in by_dec.items():
        k = max(1, int(round(n_target * len(group) / n_total)))
        sample += random.sample(group, min(k, len(group)))
    out = ROOT / "10_validation/sample.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["paper_id", "stratum", "decision_ai", "title", "abstract"])
        w.writeheader()
        for r in sample:
            w.writerow({
                "paper_id": r["paper_id"],
                "stratum": r["decision"],
                "decision_ai": r["decision"],
                "title": r.get("title", ""),
                "abstract": r.get("abstract", "")
            })
    print(f"Wrote {out} with {len(sample)} rows")
    inc = sum(1 for r in rows if r["decision"] == "INCLUDE")
    rate = inc / n_total
    print(f"Full corpus inclusion rate: {rate:.3f}")
    if rate > 0.55:
        print("WARNING: inclusion rate > 0.55 — criteria may be too loose.")

def cmd_kappa(args):
    a = {r["paper_id"]: r["decision"] for r in csv.DictReader(open(ROOT / "10_validation/reviewer_A.csv", encoding="utf-8"))}
    b = {r["paper_id"]: r["decision"] for r in csv.DictReader(open(ROOT / "10_validation/reviewer_B.csv", encoding="utf-8"))}
    adj = {r["paper_id"]: r["decision"] for r in csv.DictReader(open(ROOT / "10_validation/adjudicated.csv", encoding="utf-8"))}
    ai = {r["paper_id"]: r["decision_ai"] for r in csv.DictReader(open(ROOT / "10_validation/sample.csv", encoding="utf-8"))}
    ids = sorted(set(a) & set(b) & set(adj) & set(ai))
    k_hh = cohen_kappa_score([a[i] for i in ids], [b[i] for i in ids])
    k_ai = cohen_kappa_score([ai[i] for i in ids], [adj[i] for i in ids])
    print(f"Human-vs-human kappa: {k_hh:.3f}")
    print(f"AI-vs-adjudicated kappa: {k_ai:.3f}")
    if k_ai >= 0.80:
        v = "ACCEPT"
    elif k_ai >= 0.60:
        v = "CORRECT (apply error-model correction)"
    else:
        v = "REJECT (recalibrate criteria and re-screen)"
    print(f"Verdict: {v}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("sample")
    sp.add_parser("kappa")
    a = p.parse_args()
    {"sample": cmd_sample, "kappa": cmd_kappa}[a.cmd](a)
