import nbformat as nbf
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
import os

nb = new_notebook()

nb.cells.append(new_markdown_cell("""# 05 — Phase 2 Signal Audit & Validation
This notebook performs:
1. Multiple testing correction (FDR & Bonferroni) across all hypotheses tested.
2. Bootstrap confidence intervals for the top candidates.
3. Outlier and Robust Regression analysis."""))

nb.cells.append(new_code_cell("""import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

PROJECT_ROOT = Path().resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures" / "phase2"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
print("Setup complete.")
"""))

nb.cells.append(new_markdown_cell("""## 1. Multiple Testing Correction
We tested many feature-outcome pairs. We must apply Benjamini-Hochberg (FDR) to see which correlations survive."""))

nb.cells.append(new_code_cell("""# Load all correlations
df_corr = pd.read_parquet(DATA_PROCESSED / 'correlation_summary.parquet')

# Apply Benjamini/Hochberg FDR
df_corr['p_adj_fdr'] = multipletests(df_corr['p_value'].fillna(1.0), method='fdr_bh')[1]

# Apply Bonferroni for sensitivity
df_corr['p_adj_bonf'] = multipletests(df_corr['p_value'].fillna(1.0), method='bonferroni')[1]

top_fdr = df_corr.sort_values('p_adj_fdr').head(15)[
    ['position_group', 'combine_feature', 'nfl_outcome', 'rho', 'p_value', 'p_adj_fdr', 'n']
]

display(top_fdr)

# Save to Markdown
with open(REPORTS_DIR / 'multiple_testing.md', 'w', encoding='utf-8') as f:
    f.write("# Multiple Testing Analysis\\n\\n")
    f.write(f"Total hypotheses tested (feature/outcome pairs): {len(df_corr)}\\n\\n")
    f.write("## Top Results (FDR Adjusted)\\n\\n")
    f.write(top_fdr.to_markdown(index=False))
"""))

nb.cells.append(new_markdown_cell("""## 2. Bootstrapping & Robust Regression (WR Candidate)
**Signal:** `direction_change_rate_SHORT_SHUTTLE` vs `mean_separation` (WR)"""))

nb.cells.append(new_code_cell("""analysis_df = pd.read_parquet(DATA_PROCESSED / 'analysis_dataset.parquet')

# Filter for WR
wr_data = analysis_df[analysis_df['position_group_pos'] == 'WR'].copy()
wr_data = wr_data.dropna(subset=['direction_change_rate_SHORT_SHUTTLE', 'mean_separation'])

x = wr_data['direction_change_rate_SHORT_SHUTTLE'].values
y = wr_data['mean_separation'].values
n_wr = len(wr_data)

print(f"WR Sample Size: {n_wr}")

# Bootstrap
n_boot = 5000
boot_rhos = []
np.random.seed(42)
for _ in range(n_boot):
    idx = np.random.choice(n_wr, size=n_wr, replace=True)
    bx, by = x[idx] + np.random.normal(0, 1e-8, n_wr), y[idx] + np.random.normal(0, 1e-8, n_wr)
    r, p = stats.spearmanr(bx, by)
    if not np.isnan(r):
        boot_rhos.append(r)

ci_lower = np.percentile(boot_rhos, 2.5)
ci_upper = np.percentile(boot_rhos, 97.5)
print(f"Bootstrap 95% CI for Spearman rho: [{ci_lower:.3f}, {ci_upper:.3f}]")

# Robust regression
X = sm.add_constant(x)
rlm = sm.RLM(y, X, M=sm.robust.norms.HuberT())
res = rlm.fit()
print("\\nRobust Regression (HuberT):")
print(f"Coefficient: {res.params[1]:.4f}, p-value: {res.pvalues[1]:.4f}")

# Plot
plt.figure(figsize=(8, 6))
sns.regplot(x=x, y=y, robust=True, ci=95, scatter_kws={'alpha': 0.6})
plt.title(f"WR: Direction Change Rate vs Mean Separation\\nrho = -0.645, 95% CI [{ci_lower:.2f}, {ci_upper:.2f}], n={n_wr}")
plt.xlabel("Direction Change Rate (Short Shuttle)")
plt.ylabel("Mean Separation (NFL Rookie Season)")
plt.savefig(FIGURES_DIR / "wr_separation_robust.png", bbox_inches='tight')
plt.show()
"""))

nb.cells.append(new_markdown_cell("""## 3. Bootstrapping & Robust Regression (Edge Candidate)
**Signal:** `burst_impulse_0_1s` and `burst_impulse_0_5s` vs `mean_get_off` (Edge)"""))

nb.cells.append(new_code_cell("""# Filter for Edge
edge_data = analysis_df[analysis_df['position_group_pos'] == 'Edge'].copy()
edge_data = edge_data.dropna(subset=['burst_impulse_0_1s_THREE_CONE_DRILL', 'burst_impulse_0_5s_THREE_CONE_DRILL', 'mean_get_off'])

x1 = edge_data['burst_impulse_0_1s_THREE_CONE_DRILL'].values
x5 = edge_data['burst_impulse_0_5s_THREE_CONE_DRILL'].values
y = edge_data['mean_get_off'].values
n_edge = len(edge_data)

print(f"Edge Sample Size: {n_edge}\\n")

r1, p1 = stats.spearmanr(x1, y)
r5, p5 = stats.spearmanr(x5, y)

print(f"0.1s Window: rho = {r1:.3f}, p = {p1:.4f}")
print(f"0.5s Window: rho = {r5:.3f}, p = {p5:.4f}\\n")

# Bootstrap for 0.5s window
n_boot = 5000
boot_rhos = []
np.random.seed(42)
for _ in range(n_boot):
    idx = np.random.choice(n_edge, size=n_edge, replace=True)
    bx, by = x5[idx] + np.random.normal(0, 1e-8, n_edge), y[idx] + np.random.normal(0, 1e-8, n_edge)
    r, _ = stats.spearmanr(bx, by)
    if not np.isnan(r):
        boot_rhos.append(r)

ci_lower = np.percentile(boot_rhos, 2.5)
ci_upper = np.percentile(boot_rhos, 97.5)
print(f"0.5s Window - Bootstrap 95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]")

# Plot 0.5s Window
plt.figure(figsize=(8, 6))
sns.regplot(x=x5, y=y, robust=True, ci=95, scatter_kws={'alpha': 0.6})
plt.title(f"Edge: Burst Impulse (0.5s) vs Mean Get-Off\\nrho = {r5:.3f}, 95% CI [{ci_lower:.2f}, {ci_upper:.2f}], n={n_edge}")
plt.xlabel("Burst Impulse 0.5s (3-Cone)")
plt.ylabel("Mean Get-Off Time (NFL Rookie Season)")
plt.savefig(FIGURES_DIR / "edge_burst_0_5s_robust.png", bbox_inches='tight')
plt.show()
"""))

# Save Notebook
with open(r'C:\Users\Ekaansh\OneDrive\Desktop\AB\projects\nfl\nfl-bdb-2027\notebooks\05_phase2_signal_audit.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook created successfully.")
