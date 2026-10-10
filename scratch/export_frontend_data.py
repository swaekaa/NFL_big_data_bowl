"""
Export all data needed by the frontend to lightweight JSON files.
Run once from the project root to generate frontend/public/data/*.json
"""
import sys, json
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"
OUT_DIR = PROJECT_ROOT / "frontend" / "public" / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading processed data …")

# ── 1. analysis_dataset (WR only, tiny) ──────────────────────────────────────
df = pd.read_parquet(PROCESSED / "analysis_dataset.parquet")

# load and merge traditional combine results
try:
    combine_res = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "nfl-big-data-bowl-2027" / "nfl-big-data-bowl-2027" / "combine_results.csv")
    if 'nfl_id' in df.columns and 'nfl_id' in combine_res.columns:
        df = df.merge(combine_res, on='nfl_id', how='left')
except Exception as e:
    print(f"Warning: could not load combine_results.csv: {e}")

wr = (
    df[df["position_group_pos"] == "WR"]
    .dropna(subset=["direction_change_rate_SHORT_SHUTTLE", "mean_separation"])
    .copy()
)

# traditional combine columns that may or may not be present after merging
TRAD = ["forty", "ten_yd_split", "short_shuttle", "three_cone", "vertical", "broad_jump"]
keep = (
    ["nfl_id", "direction_change_rate_SHORT_SHUTTLE", "mean_separation"]
    + [c for c in TRAD if c in wr.columns]
)
wr_out = wr[keep].copy()

# round floats to 4 decimal places for file size
for col in wr_out.select_dtypes("float").columns:
    wr_out[col] = wr_out[col].round(4)

records = wr_out.replace({np.nan: None}).to_dict(orient="records")
with open(OUT_DIR / "wr_scatter.json", "w") as f:
    json.dump(records, f)
print(f"  wr_scatter.json — {len(records)} players")

# ── 2. Correlation summary (ALL positions) for multiple-testing section ───────
corr = pd.read_parquet(PROCESSED / "correlation_summary.parquet")
corr_keep = ["position_group", "combine_feature", "nfl_outcome", "rho", "p_value", "n"]
corr_out = corr[[c for c in corr_keep if c in corr.columns]].copy()
for col in corr_out.select_dtypes("float").columns:
    corr_out[col] = corr_out[col].round(4)
corr_out = corr_out.replace({np.nan: None})
with open(OUT_DIR / "correlations.json", "w") as f:
    json.dump(corr_out.to_dict(orient="records"), f)
print(f"  correlations.json — {len(corr_out)} rows")

# ── 3. Short Shuttle sample trajectories (2 contrasting WR attempts) ──────────
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "nfl-big-data-bowl-2027" / "nfl-big-data-bowl-2027"

# load only the short shuttle rows to keep memory low
try:
    tracking = pd.read_csv(
        RAW_DIR / "combine_tracking.csv",
        usecols=["nfl_id", "draft_year", "attempt", "time", "drill_name", "x", "y", "s", "dir", "event_id"],
    )
    tracking_ss = tracking[tracking["drill_name"] == "SHORT_SHUTTLE"].copy()

    # We want a high-dcr player and a low-dcr player who both have NFL separation
    dcr_col = "direction_change_rate_SHORT_SHUTTLE"
    feats_wr = wr.dropna(subset=[dcr_col, "mean_separation"]).sort_values(dcr_col)

    if len(feats_wr) >= 2:
        low_id = int(feats_wr.iloc[0]["nfl_id"])   # smoothest
        high_id = int(feats_wr.iloc[-1]["nfl_id"])  # jerkiest

        def get_traj(nfl_id: int, label: str) -> list:
            sub = tracking_ss[tracking_ss["nfl_id"] == nfl_id].copy()
            # pick attempt 1
            attempt = sub[sub["attempt"] == sub["attempt"].min()]
            attempt = attempt.sort_values("time").reset_index(drop=True)
            rows = []
            for _, r in attempt.iterrows():
                rows.append({
                    "x": round(float(r["x"]), 3),
                    "y": round(float(r["y"]), 3),
                    "s": round(float(r["s"]) if pd.notna(r["s"]) else 0.0, 3),
                    "dir": round(float(r["dir"]) if pd.notna(r["dir"]) else 0.0, 2),
                })
            return rows

        traj_data = {
            "low_dcr": {
                "nfl_id": low_id,
                "dcr": round(float(feats_wr.iloc[0][dcr_col]), 4),
                "mean_separation": round(float(wr[wr["nfl_id"] == low_id]["mean_separation"].values[0]), 4) if low_id in wr["nfl_id"].values else None,
                "label": "Lower direction-change rate",
                "points": get_traj(low_id, "low"),
            },
            "high_dcr": {
                "nfl_id": high_id,
                "dcr": round(float(feats_wr.iloc[-1][dcr_col]), 4),
                "mean_separation": round(float(wr[wr["nfl_id"] == high_id]["mean_separation"].values[0]), 4) if high_id in wr["nfl_id"].values else None,
                "label": "Higher direction-change rate",
                "points": get_traj(high_id, "high"),
            },
        }
        with open(OUT_DIR / "trajectories.json", "w") as f:
            json.dump(traj_data, f)
        print(f"  trajectories.json — low_dcr id={low_id}, high_dcr id={high_id}")
    else:
        print("  WARNING: not enough WR observations for trajectory comparison")
except Exception as e:
    print(f"  WARNING: could not generate trajectories.json — {e}")

# ── 4. Bootstrap distribution ─────────────────────────────────────────────────
from scipy import stats as scipy_stats

np.random.seed(42)
x = wr["direction_change_rate_SHORT_SHUTTLE"].values
y_arr = wr["mean_separation"].values
n = len(x)
boot_rhos = []
for _ in range(5000):
    idx = np.random.choice(n, n, replace=True)
    bx = x[idx] + np.random.normal(0, 1e-8, n)
    by = y_arr[idx] + np.random.normal(0, 1e-8, n)
    r, _ = scipy_stats.spearmanr(bx, by)
    if not np.isnan(r):
        boot_rhos.append(round(float(r), 4))

ci = np.percentile(boot_rhos, [2.5, 97.5]).tolist()
with open(OUT_DIR / "bootstrap.json", "w") as f:
    json.dump({"rhos": boot_rhos, "ci_lower": round(ci[0], 4), "ci_upper": round(ci[1], 4), "observed_rho": -0.645}, f)
print(f"  bootstrap.json — {len(boot_rhos)} bootstrap samples, CI=[{ci[0]:.3f}, {ci[1]:.3f}]")

# ── 5. Summary stats ──────────────────────────────────────────────────────────
summary = {
    "n_wr": int(len(wr)),
    "spearman_rho": -0.645,
    "raw_p": 0.0002,
    "bh_adj_p": 0.168,
    "huber_p": 0.0234,
    "ci_lower": -0.812,
    "ci_upper": -0.337,
    "n_hypotheses": 140,
    "ridge_traditional_r2": 0.064,
    "ridge_tracking_r2": 0.173,
    "ridge_combined_r2": 0.242,
    "dcr_vs_forty_rho": 0.06,
    "dcr_vs_split_rho": -0.05,
    "dcr_mean": round(float(wr["direction_change_rate_SHORT_SHUTTLE"].mean()), 4),
    "dcr_std": round(float(wr["direction_change_rate_SHORT_SHUTTLE"].std()), 4),
    "dcr_min": round(float(wr["direction_change_rate_SHORT_SHUTTLE"].min()), 4),
    "dcr_max": round(float(wr["direction_change_rate_SHORT_SHUTTLE"].max()), 4),
}
with open(OUT_DIR / "summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"  summary.json — written")

print("\nAll data exported successfully to frontend/public/data/")
