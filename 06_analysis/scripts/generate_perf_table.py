"""
generate_perf_table.py
Reads extracted_master.csv and outputs:
  1. perf_table_ate.md  - Markdown table: method vs ATE stats (numeric only)
  2. perf_table_full.md - Full method breakdown table (all papers, all metrics)
  3. perf_summary.csv   - Machine-readable summary
"""

import pandas as pd
import numpy as np
import ast
import os

CSV_PATH = r"E:\GPS_Denied_SLR\02_data_processed\extracted_master.csv"
OUT_DIR  = r"E:\GPS_Denied_SLR\07_manuscript"

df = pd.read_csv(CSV_PATH, low_memory=False)
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

# Headline performance claims exclude Q-low papers once Stage-2 appraisal is
# populated. Until then, retain the full set and label the output as pending QA.
qa_available = "qa_tier" in df.columns and df["qa_tier"].fillna("").isin(["Q-high", "Q-medium", "Q-low"]).any()
qa_note = (
    "Q-high/Q-medium only; Q-low papers are excluded from headline claims."
    if qa_available
    else
    "QA tiers are not populated; headline-quality filtering is pending Stage-2 appraisal."
)

# ── Clean method names ─────────────────────────────────────────────────────────
METHOD_LABELS = {
    "Filter_Based_VIO":               "Filter-Based VIO (MSCKF/EKF)",
    "Optimization_Based_VIO":         "Optimization-Based VIO (OKVIS/VINS-Mono/ORB-SLAM3)",
    "LiDAR_SLAM":                     "LiDAR SLAM (LOAM/FAST-LIO2/LIO-SAM)",
    "Visual_SLAM":                    "Visual SLAM",
    "Visual_LiDAR_Inertial_Fusion":   "Visual-LiDAR-Inertial Fusion (VLI)",
    "Hybrid_Classical_Learning":      "Hybrid Classical-DL",
    "Deep_Learning_Odometry":         "Deep Learning Odometry",
    "Radio_Based_Positioning":        "Radio/Infrastructure (UWB/WiFi/5G)",
    "Multi_Agent_Collaborative_SLAM": "Multi-Agent Collaborative SLAM",
    "Map_Based_Localization":         "Map-Based Localization",
}

df["method_label"] = df["primary_method"].map(METHOD_LABELS).fillna(df["primary_method"])

# ── TABLE 1: Full method breakdown ─────────────────────────────────────────────
grp = df.groupby("primary_method")

rows = []
for method, g in grp:
    label   = METHOD_LABELS.get(method, method)
    n_total = len(g)
    q_high_medium = (
        g["qa_tier"].isin(["Q-high", "Q-medium"]).sum()
        if qa_available else "pending"
    )
    n_real  = (g["experiment_type"] == "Real_World").sum()
    n_sim   = (g["experiment_type"] == "Simulation").sum()
    n_both  = (g["experiment_type"] == "Both").sum()
    ratio   = f"{n_real/n_sim:.1f}:1" if n_sim > 0 else "N/A"

    # ATE numeric subset
    metric_source = g[g["qa_tier"].isin(["Q-high", "Q-medium"])] if qa_available else g
    ate_df  = metric_source[(metric_source["performance_metric"] == "ATE_RMSE") &
                (g["performance_unit"] == "m") &
                pd.to_numeric(g["performance_value"], errors="coerce").notna()].copy()
    ate_df["perf_num"] = pd.to_numeric(ate_df["performance_value"], errors="coerce")
    # Cap at 200 m — values above are likely unit mismatches in abstract extraction
    ate_df = ate_df[(ate_df["perf_num"] > 0) & (ate_df["perf_num"] <= 200)]

    if len(ate_df) >= 3:
        ate_med  = f"{ate_df['perf_num'].median():.3f} m"
        ate_min  = f"{ate_df['perf_num'].min():.3f} m"
        ate_max  = f"{ate_df['perf_num'].max():.3f} m"
        ate_n    = len(ate_df)
    else:
        ate_med = ate_min = ate_max = "N/A"
        ate_n = len(ate_df)

    rows.append({
        "Method":          label,
        "Total":           n_total,
        "Q-high/Q-medium": q_high_medium,
        "Real-World":      n_real,
        "Simulation":      n_sim,
        "Both":            n_both,
        "Real:Sim":        ratio,
        "ATE Papers (m)":  ate_n,
        "ATE Median":      ate_med,
        "ATE Min":         ate_min,
        "ATE Max":         ate_max,
    })

summary_df = pd.DataFrame(rows).sort_values("Total", ascending=False)

# ── Write full breakdown markdown ──────────────────────────────────────────────
def df_to_md(df):
    cols = list(df.columns)
    header = "| " + " | ".join(cols) + " |"
    sep    = "| " + " | ".join(["---"] * len(cols)) + " |"
    lines  = [header, sep]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)

full_md = f"""### Table 1: Method Distribution and Validation Breakdown (N={len(df)})

{df_to_md(summary_df[['Method','Total','Q-high/Q-medium','Real-World','Simulation','Both','Real:Sim']])}

*Real:Sim* = ratio of real-world to simulation experiments. Higher = more field-validated.
{qa_note}
Each performance claim must state: **N papers (Q-high/Q-medium) informed each claim.**
"""

# ── TABLE 2: ATE performance only (numeric, metres) ───────────────────────────
ate_rows = [r for r in rows if r["ATE Papers (m)"] >= 3]
ate_summary = pd.DataFrame(ate_rows)[["Method","Total","ATE Papers (m)","ATE Median","ATE Min","ATE Max"]]
ate_summary = ate_summary.sort_values("ATE Papers (m)", ascending=False)

ate_md = f"""### Table 2: ATE_RMSE Performance by Primary Method (numeric metres, outliers >200 m excluded, N>=3)

{df_to_md(ate_summary)}

*ATE Median/Min/Max* computed only on papers reporting numeric ATE_RMSE in metres.
Values >200 m excluded as likely unit-mismatch artefacts from abstract-only extraction.
Methods with <3 valid ATE papers omitted from this table.
{qa_note}
"""

# ── TABLE 3: Sensor co-occurrence with IMU ─────────────────────────────────────
imu_count = df["sensors"].str.contains("IMU", na=False).sum()
imu_pct   = imu_count / len(df) * 100

sensor_counts = {}
for s_str in df["sensors"].dropna():
    try:
        sensors = ast.literal_eval(s_str)
    except Exception:
        sensors = [s.strip() for s in s_str.strip("[]").replace("'","").split(",")]
    for s in sensors:
        s = s.strip()
        if s:
            sensor_counts[s] = sensor_counts.get(s, 0) + 1

sensor_df = pd.DataFrame(
    [{"Sensor": k, "Papers": v, "Pct": f"{v/len(df)*100:.1f}%"}
     for k, v in sorted(sensor_counts.items(), key=lambda x: -x[1]) if v >= 10]
)

sensor_md = f"""### Table 3: Sensor Modality Frequency (N=1,700, multi-label)

{df_to_md(sensor_df)}

IMU appears in **{imu_count}/{len(df)} = {imu_pct:.1f}%** of all papers.
"""

# ── Write outputs ──────────────────────────────────────────────────────────────
combined = "\n\n---\n\n".join([full_md, ate_md, sensor_md])

with open(os.path.join(OUT_DIR, "perf_tables.md"), "w", encoding="utf-8") as f:
    f.write(combined)

summary_df.to_csv(os.path.join(OUT_DIR, "perf_summary.csv"), index=False)

print("perf_tables.md written")
print("perf_summary.csv written")
print(f"\nTop 5 methods by paper count:")
print(summary_df[["Method","Total","Real:Sim","ATE Median"]].head(5).to_string(index=False))
