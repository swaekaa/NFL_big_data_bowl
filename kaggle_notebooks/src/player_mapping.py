"""
player_mapping.py — Utilities for joining player data across datasets.

Key tasks:
- Validate join integrity between datasets.
- Resolve duplicate nfl_ids.
- Map combine players to their first NFL season.
- Build a master player table.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# Join validation
# ═══════════════════════════════════════════════════════════════════════════════

def validate_player_joins(
    players: pd.DataFrame,
    combine_results: Optional[pd.DataFrame] = None,
    combine_tracking: Optional[pd.DataFrame] = None,
    player_play: Optional[pd.DataFrame] = None,
    career_successes: Optional[pd.DataFrame] = None,
) -> dict:
    """
    Report join statistics between players and other datasets.

    Returns a dict with counts of:
    - players in each dataset
    - players in players.csv that also appear in each dataset
    - players unique to each dataset (not in players.csv)
    """
    all_player_ids = set(players["nfl_id"].unique())
    n_players = len(all_player_ids)

    report = {"n_players_master": n_players}

    if combine_results is not None and "nfl_id" in combine_results.columns:
        cr_ids = set(combine_results["nfl_id"].dropna().unique())
        report["combine_results_n"] = len(cr_ids)
        report["combine_results_in_master"] = len(cr_ids & all_player_ids)
        report["combine_results_only"] = len(cr_ids - all_player_ids)

    if combine_tracking is not None and "nfl_id" in combine_tracking.columns:
        ct_ids = set(combine_tracking["nfl_id"].dropna().unique())
        report["combine_tracking_n"] = len(ct_ids)
        report["combine_tracking_in_master"] = len(ct_ids & all_player_ids)
        report["combine_tracking_only"] = len(ct_ids - all_player_ids)

    if player_play is not None and "nfl_id" in player_play.columns:
        pp_ids = set(player_play["nfl_id"].dropna().unique())
        report["player_play_n"] = len(pp_ids)
        report["player_play_in_master"] = len(pp_ids & all_player_ids)
        report["player_play_only"] = len(pp_ids - all_player_ids)

    if career_successes is not None and "nfl_id" in career_successes.columns:
        cs_ids = set(career_successes["nfl_id"].dropna().unique())
        report["career_successes_n"] = len(cs_ids)
        report["career_successes_in_master"] = len(cs_ids & all_player_ids)
        report["career_successes_only"] = len(cs_ids - all_player_ids)

    # Players with ALL datasets
    all_ids_list = [all_player_ids]
    if combine_results is not None and "nfl_id" in combine_results.columns:
        all_ids_list.append(set(combine_results["nfl_id"].dropna()))
    if combine_tracking is not None and "nfl_id" in combine_tracking.columns:
        all_ids_list.append(set(combine_tracking["nfl_id"].dropna()))
    if player_play is not None and "nfl_id" in player_play.columns:
        all_ids_list.append(set(player_play["nfl_id"].dropna()))

    complete_players = set.intersection(*all_ids_list) if len(all_ids_list) > 1 else all_player_ids
    report["n_players_with_all_datasets"] = len(complete_players)
    report["complete_player_ids"] = complete_players

    return report


def print_join_report(report: dict) -> None:
    """Print the join validation report in a readable format."""
    print(f"\n{'='*55}")
    print("  Player Join Validation Report")
    print(f"{'='*55}")
    print(f"  Players in master table:          {report.get('n_players_master', 'N/A'):>6}")
    print(f"  Players with ALL datasets:        {report.get('n_players_with_all_datasets', 'N/A'):>6}")
    print()

    for key_prefix in ["combine_results", "combine_tracking", "player_play", "career_successes"]:
        n_key = f"{key_prefix}_n"
        in_key = f"{key_prefix}_in_master"
        only_key = f"{key_prefix}_only"
        if n_key in report:
            print(f"  {key_prefix}:")
            print(f"    total players:    {report[n_key]:>6}")
            print(f"    in master:        {report[in_key]:>6}")
            print(f"    not in master:    {report[only_key]:>6}")
    print(f"{'='*55}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# First-season mapping
# ═══════════════════════════════════════════════════════════════════════════════

def map_first_nfl_season(
    player_play: pd.DataFrame,
    season_col: str = "season",
) -> pd.DataFrame:
    """
    For each player, identify their first NFL season in the dataset.

    Returns a DataFrame with (nfl_id, first_season).
    This is used to filter player_play to the rookie year only.
    """
    if season_col not in player_play.columns:
        # Try to extract year from game_id if it looks like "2023_XX_XX_XX"
        if "game_id" in player_play.columns:
            log.info("Attempting to extract season from game_id column")
            player_play = player_play.copy()
            player_play[season_col] = player_play["game_id"].astype(str).str[:4].astype(float)
        else:
            log.warning(f"Column '{season_col}' not found and game_id unavailable. Cannot determine first season.")
            return pd.DataFrame(columns=["nfl_id", "first_season"])

    first_seasons = (
        player_play.groupby("nfl_id")[season_col]
        .min()
        .reset_index()
        .rename(columns={season_col: "first_season"})
    )
    log.info(f"map_first_nfl_season: {len(first_seasons)} players with season data")
    return first_seasons


def filter_to_first_season(
    player_play: pd.DataFrame,
    season_col: str = "season",
) -> pd.DataFrame:
    """
    Filter player_play to each player's first NFL season.

    This provides the cleanest prospective scouting interpretation:
    "Could combine data have predicted rookie performance?"
    """
    first_seasons = map_first_nfl_season(player_play, season_col=season_col)
    if first_seasons.empty:
        return player_play

    merged = player_play.merge(first_seasons, on="nfl_id", how="left")
    before = len(merged)

    if season_col in merged.columns:
        merged = merged[merged[season_col] == merged["first_season"]]
        log.info(
            f"filter_to_first_season: {before:,} → {len(merged):,} rows "
            f"({merged['nfl_id'].nunique()} players)"
        )

    return merged.drop(columns=["first_season"], errors="ignore")


# ═══════════════════════════════════════════════════════════════════════════════
# Master player table builder
# ═══════════════════════════════════════════════════════════════════════════════

def build_master_player_table(
    players: pd.DataFrame,
    combine_results: Optional[pd.DataFrame] = None,
    career_successes: Optional[pd.DataFrame] = None,
    first_seasons: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    """
    Build a single master player table joining:
    - players (physical measurements, position, draft info)
    - combine_results (traditional combine scores)
    - career_successes (career outcomes — only for secondary analysis)
    - first_seasons (first NFL season per player)

    Returns a wide DataFrame with one row per player.
    """
    master = players.copy()
    n_start = len(master)

    if combine_results is not None:
        # Drop position from combine_results to avoid duplication
        cr = combine_results.drop(columns=["position"], errors="ignore")
        master = master.merge(cr, on="nfl_id", how="left")
        log.info(
            f"Master: merged combine_results — {master['nfl_id'].notna().sum()} rows, "
            f"{len(master.columns)} columns"
        )

    if first_seasons is not None:
        master = master.merge(first_seasons, on="nfl_id", how="left")
        log.info("Master: merged first_season column")

    if career_successes is not None:
        cs = career_successes.drop(columns=["position"], errors="ignore")
        master = master.merge(cs, on="nfl_id", how="left", suffixes=("", "_career"))
        log.info("Master: merged career_successes (for secondary analysis only)")

    assert len(master) == n_start, (
        f"Master table grew during joins ({n_start} → {len(master)}). "
        "Check for duplicate nfl_ids in joined tables."
    )
    assert master["nfl_id"].is_unique, "master nfl_id is not unique after joins"

    log.info(
        f"build_master_player_table complete: {len(master)} players | {master.shape[1]} columns"
    )
    return master


# ═══════════════════════════════════════════════════════════════════════════════
# Position group assignment
# ═══════════════════════════════════════════════════════════════════════════════

def assign_position_groups(
    df: pd.DataFrame,
    position_col: str = "position",
    group_map: Optional[dict] = None,
) -> pd.DataFrame:
    """
    Add a 'position_group' column based on position_col.
    Uses config.POSITION_GROUPS by default.
    """
    if group_map is None:
        from src.config import POSITION_GROUPS
        group_map = POSITION_GROUPS

    df = df.copy()
    if position_col in df.columns:
        df["position_group"] = df[position_col].map(group_map).fillna("Other")
    else:
        log.warning(f"Column '{position_col}' not found; 'position_group' will be 'Unknown'")
        df["position_group"] = "Unknown"

    return df


# ═══════════════════════════════════════════════════════════════════════════════
# Combine tracking attempt validation
# ═══════════════════════════════════════════════════════════════════════════════

def validate_combine_tracking(tracking: pd.DataFrame) -> dict:
    """
    Validate the structure of combine_tracking.

    Returns a summary dict with:
    - n_rows, n_players, n_drills, n_attempts
    - Missing nfl_id count
    - Timestamp spacing statistics
    - Players with BALL rows (if any)
    """
    report = {
        "n_rows": len(tracking),
        "n_players": tracking["nfl_id"].nunique() if "nfl_id" in tracking.columns else np.nan,
        "n_drill_types": tracking["drill_type"].nunique() if "drill_type" in tracking.columns else np.nan,
    }

    if "nfl_id" in tracking.columns:
        null_id = tracking["nfl_id"].isna().sum()
        report["n_null_nfl_id"] = int(null_id)
        # Check for BALL rows (sometimes tracking data has a "BALL" entry)
        if tracking["nfl_id"].dtype == object:
            ball_rows = (tracking["nfl_id"].astype(str).str.upper() == "BALL").sum()
            report["n_ball_rows"] = int(ball_rows)
        else:
            report["n_ball_rows"] = 0

    if "attempt" in tracking.columns:
        report["n_total_attempts"] = int(tracking.groupby(
            [c for c in ["nfl_id", "drill_type", "attempt"] if c in tracking.columns]
        ).ngroups)

    # Timestamp spacing
    if "time" in tracking.columns:
        try:
            times = pd.to_datetime(tracking["time"])
            dt_sample = times.diff().dropna()
            dt_seconds = dt_sample.dt.total_seconds()
            report["median_dt_seconds"] = float(dt_seconds.median())
            report["mean_dt_seconds"] = float(dt_seconds.mean())
            report["pct_dt_near_01"] = float(
                np.mean((dt_seconds > 0.08) & (dt_seconds < 0.12))
            )
        except Exception:
            report["median_dt_seconds"] = "COULD NOT PARSE"

    return report
