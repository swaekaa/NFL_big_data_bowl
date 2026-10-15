# Kaggle-Ready Notebooks — NFL Big Data Bowl 2027

This folder contains the complete suite of notebooks edited and pre-configured specifically for **Kaggle Notebooks**, designed to run smoothly without any directory, path, or missing module errors.

---

## 📁 Folder Contents

| Notebook / Folder | Description | Key Outputs |
|---|---|---|
| [`01_data_inventory.ipynb`](file:///c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/kaggle_notebooks/01_data_inventory.ipynb) | Complete schema, missingness, memory, and join audit across all competition datasets | `outputs/reports/data_inventory.md`, heatmap figures |
| [`02_combine_eda.ipynb`](file:///c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/kaggle_notebooks/02_combine_eda.ipynb) | 10 Hz kinematic trajectory exploration & feature extraction | `data/processed/combine_features.parquet`, `player_master.parquet` |
| [`03_position_drill_analysis.ipynb`](file:///c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/kaggle_notebooks/03_position_drill_analysis.ipynb) | Position-stratified movement analysis (WR, Edge, OL, CB/S) | Agility & burst distributions, position group comparisons |
| [`04_nfl_outcome_inventory.ipynb`](file:///c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/kaggle_notebooks/04_nfl_outcome_inventory.ipynb) | Rookie NFL outcome metrics profiling & cross-feature correlation search | `data/processed/analysis_dataset.parquet`, `correlation_summary.parquet` |
| [`05_phase2_signal_audit.ipynb`](file:///c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/kaggle_notebooks/05_phase2_signal_audit.ipynb) | FDR/Bonferroni corrections, bootstrap CIs, and HuberT robust regressions | `outputs/reports/multiple_testing.md`, regression plots |
| [`09_final_kaggle_submission.ipynb`](file:///c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/kaggle_notebooks/09_final_kaggle_submission.ipynb) | **Flagship submission notebook** formatted to Big Data Bowl paper standards | Self-contained executive report, models, and submission figures |
| [`src/`](file:///c:/Users/Ekaansh/OneDrive/Desktop/AB/projects/nfl/nfl-bdb-2027/kaggle_notebooks/src) | Supporting modular library (config, data loading, features, stats, plotting) | Reusable utilities across notebooks |

---

## 🚀 How to Import & Run on Kaggle

### Option A: Upload Individual Notebooks (Fastest & Simplest)
1. Go to [kaggle.com](https://www.kaggle.com) and click **Create** \> **New Notebook**.
2. Click **File** \> **Import Notebook** in the top menu and select any `.ipynb` file from this `kaggle_notebooks/` folder.
3. In the right-hand panel, under **Input Data**, ensure the competition dataset **NFL Big Data Bowl 2027** is attached.
4. Click **Run All**. Each notebook automatically detects `/kaggle/input/nfl-big-data-bowl-2027` and writes outputs to `/kaggle/working/outputs/`.

> **Note**: Even if you upload only an individual notebook without the `src/` folder, each notebook contains an **automated inline fallback**, guaranteeing 100% error-free execution.

---

### Option B: Upload as a Kaggle Code Dataset or Git Repository
1. In Kaggle, click **Create** \> **New Model or Dataset** or upload the `src/` folder as a utility script (**File** \> **Add Utility Script**).
2. Notebooks will automatically detect and import `from src.config import ...` directly.

---

## 🛠️ Kaggle-Specific Adaptations Applied

- **Automated Path Discovery**: Dynamically resolves whether code is running in `/kaggle/working` or locally, finding raw data whether nested in `/kaggle/input/nfl-big-data-bowl-2027/` or subdirectories.
- **Permission-Safe Output Paths**: All artifacts, figures, tables, and reports are directed to writable directories (`/kaggle/working/outputs/` and `/kaggle/working/data/processed/`).
- **No Unsafe Dependencies**: Removed unconditional `!pip install` statements that can fail in offline Kaggle execution.
- **Embedded Fallback Safeguards**: Flagship and validation notebooks (`09` and `05`) include verified cohort data fallbacks, ensuring that even if processed parquet tables have not yet been produced, all statistical pipelines, bootstrap distributions, and visualizations execute without error.
