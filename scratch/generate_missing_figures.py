import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(r"c:\Users\Ekaansh\OneDrive\Desktop\AB\projects\nfl\nfl-bdb-2027")
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures" / "final"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# FIGURE 5: Ridge Regression R² Bar Chart
# ---------------------------------------------------------
# Based on the results obtained earlier:
# Traditional Only: 0.064
# Tracking Only: 0.173
# Traditional + Tracking: 0.242

models = ['Traditional Only', 'Tracking Only', 'Traditional + Tracking']
r_squared = [0.064, 0.173, 0.242]

plt.figure(figsize=(8, 5))
bars = plt.bar(models, r_squared, color=['#95a5a6', '#3498db', '#2ecc71'])
plt.title("Explanatory Power (R²) for NFL Separation", fontsize=14)
plt.ylabel("Ridge Regression R²", fontsize=12)
plt.ylim(0, 0.3)

# Add value labels
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.005, f"{yval:.3f}", ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.savefig(FIGURES_DIR / "ridge_r2_comparison.png", bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# FIGURE 1: Short Shuttle Trajectories
# ---------------------------------------------------------
# Load raw tracking data to get trajectories
try:
    data_path = PROJECT_ROOT / "data" / "raw" / "nfl-big-data-bowl-2027" / "nfl-big-data-bowl-2027" / "combine_tracking.csv"
    tracking_df = pd.read_csv(data_path)
    
    # We just need two example Short Shuttle trajectories (one smooth, one jerky)
    ss_tracking = tracking_df[tracking_df['drill_name'] == 'SHORT_SHUTTLE']
    
    # Get two random distinct nfl_ids
    unique_ids = ss_tracking['nfl_id'].unique()
    if len(unique_ids) >= 2:
        player1 = ss_tracking[ss_tracking['nfl_id'] == unique_ids[0]]
        player2 = ss_tracking[ss_tracking['nfl_id'] == unique_ids[1]]
        
        plt.figure(figsize=(10, 6))
        plt.plot(player1['x'], player1['y'], marker='o', markersize=3, linestyle='-', color='#3498db', alpha=0.7, label='Player A (Example)')
        plt.plot(player2['x'], player2['y'], marker='o', markersize=3, linestyle='-', color='#e74c3c', alpha=0.7, label='Player B (Example)')
        
        plt.title("Short Shuttle Tracking Trajectories (Example X/Y Paths)", fontsize=14)
        plt.xlabel("X Coordinate (Yards)", fontsize=12)
        plt.ylabel("Y Coordinate (Yards)", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(FIGURES_DIR / "short_shuttle_trajectories.png", bbox_inches='tight')
        plt.close()
        print("Generated trajectory plot successfully.")
except Exception as e:
    print(f"Could not generate trajectory plot (data might be unavailable): {e}")

print(f"Saved new figures to: {FIGURES_DIR}")
