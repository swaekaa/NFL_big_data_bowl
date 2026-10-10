import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

PROJECT_ROOT = Path("C:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

# 1. Multiple Testing
df_corr = pd.read_parquet(DATA_PROCESSED / "correlation_summary.parquet")

# Apply Benjamini/Hochberg FDR
df_corr["p_adj_fdr"] = multipletests(df_corr["p_value"].fillna(1.0), method="fdr_bh")[1]

# Apply Bonferroni
df_corr["p_adj_bonf"] = multipletests(df_corr["p_value"].fillna(1.0), method="bonferroni")[1]

print("=== Top correlations after FDR adjustment ===")
print(df_corr.sort_values("p_adj_fdr").head(10)[['position_group', 'combine_feature', 'nfl_outcome', 'rho', 'p_value', 'p_adj_fdr', 'n']])

with open(REPORTS_DIR / "multiple_testing.md", "w", encoding="utf-8") as f:
    f.write("# Multiple Testing Analysis\n\n")
    f.write(f"Total hypotheses tested: {len(df_corr)}\n\n")
    f.write("## Top Results (FDR Adjusted)\n\n")
    f.write(df_corr.sort_values("p_adj_fdr").head(10)[['position_group', 'combine_feature', 'nfl_outcome', 'rho', 'p_value', 'p_adj_fdr', 'n']].to_markdown(index=False))

# 2. Load Analysis Dataset for Bootstrapping & Outliers
analysis_df = pd.read_parquet(DATA_PROCESSED / "analysis_dataset.parquet")

print("\n=== WR Candidate 1: direction_change_rate (Short Shuttle) vs mean_separation ===")
wr_data = analysis_df[analysis_df['position_group_pos'] == 'WR'].copy().dropna(subset=['direction_change_rate_SHORT_SHUTTLE', 'mean_separation'])
n_wr = len(wr_data)
if n_wr > 0:
    x = wr_data['direction_change_rate_SHORT_SHUTTLE'].values
    y = wr_data['mean_separation'].values
    print(f"N = {n_wr}")
    
    # Bootstrap
    n_boot = 5000
    boot_rhos = []
    np.random.seed(42)
    for _ in range(n_boot):
        idx = np.random.choice(n_wr, size=n_wr, replace=True)
        # add small noise to prevent constant arrays during bootstrap
        bx, by = x[idx] + np.random.normal(0, 1e-8, n_wr), y[idx] + np.random.normal(0, 1e-8, n_wr)
        r, _ = stats.spearmanr(bx, by)
        if not np.isnan(r):
            boot_rhos.append(r)
    
    ci_lower = np.percentile(boot_rhos, 2.5)
    ci_upper = np.percentile(boot_rhos, 97.5)
    print(f"Bootstrap 95% CI for Spearman rho: [{ci_lower:.3f}, {ci_upper:.3f}]")
    
    # Robust regression
    X = sm.add_constant(x)
    rlm = sm.RLM(y, X, M=sm.robust.norms.HuberT())
    res = rlm.fit()
    print("Robust Regression (HuberT):")
    print(f"Coefficient: {res.params[1]:.4f}, p-value: {res.pvalues[1]:.4f}")
else:
    print("No WR data available.")

print("\n=== Edge Candidate 2: burst_impulse_0_1s (3-Cone) vs mean_get_off ===")
edge_data = analysis_df[analysis_df['position_group_pos'] == 'Edge'].copy().dropna(subset=['burst_impulse_0_1s_THREE_CONE_DRILL', 'mean_get_off'])
n_edge = len(edge_data)
if n_edge > 0:
    x = edge_data['burst_impulse_0_1s_THREE_CONE_DRILL'].values
    y = edge_data['mean_get_off'].values
    print(f"N = {n_edge}")
    
    # Bootstrap
    n_boot = 5000
    boot_rhos = []
    np.random.seed(42)
    for _ in range(n_boot):
        idx = np.random.choice(n_edge, size=n_edge, replace=True)
        bx, by = x[idx] + np.random.normal(0, 1e-8, n_edge), y[idx] + np.random.normal(0, 1e-8, n_edge)
        r, _ = stats.spearmanr(bx, by)
        if not np.isnan(r):
            boot_rhos.append(r)
    
    ci_lower = np.percentile(boot_rhos, 2.5)
    ci_upper = np.percentile(boot_rhos, 97.5)
    print(f"Bootstrap 95% CI for Spearman rho: [{ci_lower:.3f}, {ci_upper:.3f}]")

    # Let's also check burst_impulse_0_5s
    edge_data_5 = analysis_df[analysis_df['position_group_pos'] == 'Edge'].copy().dropna(subset=['burst_impulse_0_5s_THREE_CONE_DRILL', 'mean_get_off'])
    x5 = edge_data_5['burst_impulse_0_5s_THREE_CONE_DRILL'].values
    y5 = edge_data_5['mean_get_off'].values
    r5, p5 = stats.spearmanr(x5, y5)
    print(f"Checking 0.5s window instead: rho = {r5:.3f}, p = {p5:.4f}")

else:
    print("No Edge data available.")

