"""
config.py — Central configuration: paths, column definitions, position group mappings.

All notebooks and src modules import from here so that paths and column lists
are defined in exactly one place.
"""

from __future__ import annotations

import os
from pathlib import Path

# ── Project Root ───────────────────────────────────────────────────────────────
# Resolves to nfl-bdb-2027/ regardless of where the script is called from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ── Data Directories ──────────────────────────────────────────────────────────
DATA_RAW = PROJECT_ROOT / "data" / "raw" / "nfl-big-data-bowl-2027" / "nfl-big-data-bowl-2027"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# ── Output Directories ────────────────────────────────────────────────────────
OUTPUTS_ROOT = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_ROOT / "figures"
TABLES_DIR = OUTPUTS_ROOT / "tables"
REPORTS_DIR = OUTPUTS_ROOT / "reports"

# ── Raw File Paths ────────────────────────────────────────────────────────────
PLAYERS_CSV = DATA_RAW / "players.csv"
COMBINE_RESULTS_CSV = DATA_RAW / "combine_results.csv"
COMBINE_TRACKING_CSV = DATA_RAW / "combine_tracking.csv"
CAREER_SUCCESSES_CSV = DATA_RAW / "player_career_successes.csv"
PLAYER_PLAY_CSV = DATA_RAW / "player_play.csv"
GAMES_CSV = DATA_RAW / "games.csv"
GAME_TRACKING_2023_CSV = DATA_RAW / "game_tracking_2023.csv"
GAME_TRACKING_2024_CSV = DATA_RAW / "game_tracking_2024.csv"
GAME_TRACKING_2025_CSV = DATA_RAW / "game_tracking_2025.csv"

ALL_RAW_FILES = {
    "players": PLAYERS_CSV,
    "combine_results": COMBINE_RESULTS_CSV,
    "combine_tracking": COMBINE_TRACKING_CSV,
    "player_career_successes": CAREER_SUCCESSES_CSV,
    "player_play": PLAYER_PLAY_CSV,
    "games": GAMES_CSV,
    "game_tracking_2023": GAME_TRACKING_2023_CSV,
    "game_tracking_2024": GAME_TRACKING_2024_CSV,
    "game_tracking_2025": GAME_TRACKING_2025_CSV,
}

GAME_TRACKING_FILES = {
    2023: GAME_TRACKING_2023_CSV,
    2024: GAME_TRACKING_2024_CSV,
    2025: GAME_TRACKING_2025_CSV,
}

# ── Processed Parquet Paths ───────────────────────────────────────────────────
COMBINE_FEATURES_PARQUET = DATA_PROCESSED / "combine_features.parquet"
NFL_FEATURES_PARQUET = DATA_PROCESSED / "nfl_features.parquet"
PLAYER_MASTER_PARQUET = DATA_PROCESSED / "player_master.parquet"

# ── Column Definitions ────────────────────────────────────────────────────────
# Only load the columns we actually need from large files.

COMBINE_TRACKING_COLS = [
    "event_id",
    "nfl_id",
    "time",
    "drill_type",
    "drill_name",
    "attempt",
    "x",
    "y",
    "s",      # speed (yards/s)
    "a",      # acceleration (yards/s²)
    "dis",    # distance from previous frame
    "dir",    # direction of motion (degrees, 0=N, clockwise)
]

GAME_TRACKING_COLS = [
    "game_id",
    "play_id",
    "nfl_id",
    "time",
    "x",
    "y",
    "s",
    "a",
    "dis",
    "o",      # player orientation (degrees)
    "dir",    # motion direction (degrees)
    "event",
]

PLAYER_PLAY_COLS = [
    "game_id",
    "play_id",
    "nfl_id",
    # Receiver/WR/TE
    "target",
    "rec_yards",
    "yards_after_catch",
    "route_ran",
    "separation_at_pass_forward",
    "cushion",
    "expected_yards_after_catch",
    # DL
    "player_get_off",
    "sack",
    "tackle",
    "tackle_for_loss",
    "time_to_pressure",
    "quick_pressure",
    # OL
    "pressure_allowed",
    "sack_allowed",
    "time_to_pressure_allowed",
    # Extra
    "position",
]

TRADITIONAL_COMBINE_COLS = [
    "nfl_id",
    "position",
    "ten_yd_split",
    "forty",
    "vertical",
    "broad_jump",
    "three_cone",
    "short_shuttle",
    "bench_reps",
    "ngs_athleticism_score",
    "ngs_college_production_score",
    "ngs_final_score",
]

# ── Position Group Mappings ───────────────────────────────────────────────────
# Maps individual position codes → analysis group labels.
POSITION_GROUPS = {
    # Skill offense
    "WR": "WR",
    "TE": "TE",
    "RB": "RB",
    "FB": "RB",      # Fullbacks grouped with RB
    "QB": "QB",
    # Offensive Line
    "T":  "OL",
    "G":  "OL",
    "C":  "OL",
    "OT": "OL",
    "OG": "OL",
    "OL": "OL",
    # Defensive Line / pass rushers
    "DE": "Edge",
    "OLB": "Edge",   # 4-3 OLB acting as edge rusher
    "DT": "DT",
    "NT": "DT",
    "DL": "DT",
    # Linebackers
    "ILB": "LB",
    "MLB": "LB",
    "LB":  "LB",
    # Defensive Backs
    "CB":  "CB",
    "DB":  "DB",
    "S":   "S",
    "FS":  "S",
    "SS":  "S",
    "SAF": "S",
    # Specialists (may have combine tracking but excluded from outcome analysis)
    "K":   "Specialist",
    "P":   "Specialist",
    "LS":  "Specialist",
}

# Minimum sample size (players) to report a position-group finding.
MIN_SAMPLE_SIZE = 10

# ── Combine Drill Metadata ────────────────────────────────────────────────────
# Human-readable drill type labels.
DRILL_TYPE_LABELS = {
    "40": "40-Yard Dash",
    "bench": "Bench Press",
    "vertical": "Vertical Jump",
    "broad": "Broad Jump",
    "3cone": "3-Cone Drill",
    "shuttle": "Short Shuttle",
    "position": "Position Drill",
}

# ── Plot Styling ──────────────────────────────────────────────────────────────
FIGURE_DPI = 150
FIGURE_SIZE_STANDARD = (10, 6)
FIGURE_SIZE_WIDE = (14, 6)
FIGURE_SIZE_SQUARE = (8, 8)

# ── Misc ──────────────────────────────────────────────────────────────────────
RANDOM_SEED = 42
BOOTSTRAP_N = 1000     # Number of bootstrap resamples for CIs
ALPHA = 0.05           # Significance level


def ensure_dirs() -> None:
    """Create all output and processed-data directories if they don't exist."""
    for d in [DATA_PROCESSED, FIGURES_DIR, TABLES_DIR, REPORTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def check_raw_files() -> dict[str, bool]:
    """
    Return a dict of {dataset_name: exists} for all expected raw files.
    Useful to run at the top of every notebook.
    """
    return {name: path.exists() for name, path in ALL_RAW_FILES.items()}


def print_file_status() -> None:
    """Print a human-readable table of raw file availability."""
    status = check_raw_files()
    print(f"{'File':<30} {'Status':<10} {'Size':>12}")
    print("-" * 55)
    for name, exists in status.items():
        path = ALL_RAW_FILES[name]
        if exists:
            size_mb = path.stat().st_size / 1_048_576
            status_str = "✓ FOUND"
            size_str = f"{size_mb:>10.1f} MB"
        else:
            status_str = "✗ MISSING"
            size_str = ""
        print(f"{name:<30} {status_str:<10} {size_str}")
