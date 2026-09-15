"""
06_analysis/scripts/99_verify_all_v2.py
One-Shot Verification (v2) per MASTER_PROMPT_v2.md Appendix B
"""

import pathlib
import sys
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]
em_path = ROOT / "02_data_processed/extracted_master_v2.csv"
sa_path = ROOT / "02_data_processed/screening_audit_v2.csv"

if not em_path.exists():
    print(f"Error: {em_path} does not exist yet. Run Phase 7 first.")
    sys.exit(1)

em = pd.read_csv(em_path)
checks = []

def ck(n, cond, a, e):
    checks.append((n, "PASS" if cond else "FAIL", a, e))

inc = len(em) - int(em.get("is_double_extraction", pd.Series([0] * len(em))).sum())
ck("inclusion rate in [0.25,0.45]", 0.25 <= inc / 1719 <= 0.45, round(inc / 1719, 3), "0.25-0.45")
ck("qa_total in 0-10", em.qa_total.between(0, 10).all(), em.qa_total.min(), ">=0")
ck("qa_tier valid", em.qa_tier.isin(["Q-high", "Q-medium", "Q-low"]).all(), "-", "-")
ck("sim-only capped", ((em.real_or_sim != "sim") | (em.qa_tier != "Q-high")).all(), "-", "-")

print("\n=======================================================")
print("      GPS_Denied_SLR v2 REPOSITORY VERIFICATION        ")
print("=======================================================")
for n, s, a, e in checks:
    print(f"[{s}] {n:32s} actual={a} expected={e}")
print("=======================================================")

all_pass = all(c[1] == "PASS" for c in checks)
sys.exit(0 if all_pass else 1)
