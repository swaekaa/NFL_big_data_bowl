"""
nfl_features.py — Per-player NFL performance metric aggregation.

Design principles:
- Aggregates player_play data to per-player-per-season metrics.
- Position-aware: only computes metrics relevant to the player's position.
- Handles sparse data (many plays will have NaN for most columns).
- Temporal boundary: only uses the player's first NFL season after the Combine.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

# ── Position group helpers ────────────────────────────────────────────────────

WR_TE_POSITIONS = {"WR", "TE"}
RB_POSITIONS = {"RB", "FB"}
SKILL_OFFENSE = WR_TE_POSITIONS | RB_POSITIONS
EDGE_POSITIONS = {"DE", "OLB"}
DT_POSITIONS = {"DT", "NT", "DL"}
LB_POSITIONS = {"LB", "ILB", "MLB"}
DEFENSE_FRONT = EDGE_POSITIONS | DT_POSITIONS | LB_POSITIONS
CB_POSITIONS = {"CB", "DB"}
SAFETY_POSITIONS = {"S", "FS", "SS", "SAF"}
DEFENSIVE_BACKS = CB_POSITIONS | SAFETY_POSITIONS
OL_POSITIONS = {"T", "G", "C", "OT", "OG", "OL"}


def classify_position(pos: str) -> str:
    """Map raw position string to broad functional group."""
    if pos in WR_TE_POSITIONS:
        return "skill_offense"
    if pos in RB_POSITIONS:
        return "rb"
    if pos in EDGE_POSITIONS:
        return "edge"
    if pos in DT_POSITIONS:
        return "dt"
    if pos in LB_POSITIONS:
        return "lb"
    if pos in CB_POSITIONS:
        return "cb"
    if pos in SAFETY_POSITIONS:
        return "safety"
    if pos in OL_POSITIONS:
        return "ol"
    return "other"


# ═══════════════════════════════════════════════════════════════════════════════
# Skill offense: WR / TE metrics
# ═══════════════════════════════════════════════════════════════════════════════

def wr_te_metrics(plays: pd.DataFrame) -> dict:
    """
    Aggregate receiving metrics for WR / TE.

    Unit of analysis: per-player-season.

    Requires columns (subset of): target, rec_yards, yards_after_catch,
    separation_at_pass_forward, cushion, expected_yards_after_catch, route_ran.
    """
    n_plays = len(plays)
    if n_plays == 0:
        return _null_wr_te_metrics()

    result = {}

    # --- Target metrics ---
    if "target" in plays.columns:
        result["n_targets"] = int(plays["target"].sum(min_count=1) or 0)
        result["target_share"] = result["n_targets"] / n_plays
    else:
        result["n_targets"] = np.nan
        result["target_share"] = np.nan

    # --- Reception metrics ---
    if "rec_yards" in plays.columns:
        rec_plays = plays[plays["rec_yards"].notna()]
        result["n_receptions"] = len(rec_plays)
        result["total_rec_yards"] = float(rec_plays["rec_yards"].sum())
        result["yards_per_reception"] = float(rec_plays["rec_yards"].mean()) if len(rec_plays) > 0 else np.nan
    else:
        result["n_receptions"] = np.nan
        result["total_rec_yards"] = np.nan
        result["yards_per_reception"] = np.nan

    # --- Yards after catch ---
    if "yards_after_catch" in plays.columns:
        yac = plays["yards_after_catch"].dropna()
        result["mean_yac"] = float(yac.mean()) if len(yac) > 0 else np.nan
        result["median_yac"] = float(yac.median()) if len(yac) > 0 else np.nan
    else:
        result["mean_yac"] = np.nan
        result["median_yac"] = np.nan

    # --- Separation at pass forward (key metric) ---
    if "separation_at_pass_forward" in plays.columns:
        sep = plays["separation_at_pass_forward"].dropna()
        result["mean_separation"] = float(sep.mean()) if len(sep) > 0 else np.nan
        result["median_separation"] = float(sep.median()) if len(sep) > 0 else np.nan
        result["pct_top_quartile_separation"] = float(np.mean(sep >= sep.quantile(0.75))) if len(sep) > 0 else np.nan
        result["n_separation_obs"] = len(sep)
    else:
        result["mean_separation"] = np.nan
        result["median_separation"] = np.nan
        result["pct_top_quartile_separation"] = np.nan
        result["n_separation_obs"] = np.nan

    # --- Cushion ---
    if "cushion" in plays.columns:
        cush = plays["cushion"].dropna()
        result["mean_cushion"] = float(cush.mean()) if len(cush) > 0 else np.nan
    else:
        result["mean_cushion"] = np.nan

    # --- Expected YAC (model-based, from data) ---
    if "expected_yards_after_catch" in plays.columns:
        eyac = plays["expected_yards_after_catch"].dropna()
        result["mean_expected_yac"] = float(eyac.mean()) if len(eyac) > 0 else np.nan
        # YAC over expectation
        if "yards_after_catch" in plays.columns:
            both = plays[["yards_after_catch", "expected_yards_after_catch"]].dropna()
            if len(both) > 0:
                result["yac_over_expected"] = float((both["yards_after_catch"] - both["expected_yards_after_catch"]).mean())
            else:
                result["yac_over_expected"] = np.nan
        else:
            result["yac_over_expected"] = np.nan
    else:
        result["mean_expected_yac"] = np.nan
        result["yac_over_expected"] = np.nan

    result["n_plays"] = n_plays
    return result


def _null_wr_te_metrics() -> dict:
    return {k: np.nan for k in [
        "n_targets", "target_share", "n_receptions", "total_rec_yards",
        "yards_per_reception", "mean_yac", "median_yac", "mean_separation",
        "median_separation", "pct_top_quartile_separation", "n_separation_obs",
        "mean_cushion", "mean_expected_yac", "yac_over_expected", "n_plays",
    ]}


# ═══════════════════════════════════════════════════════════════════════════════
# Defensive line / edge rusher metrics
# ═══════════════════════════════════════════════════════════════════════════════

def dl_edge_metrics(plays: pd.DataFrame) -> dict:
    """
    Aggregate pass-rush and run-defense metrics for DL / Edge rushers.
    """
    n_plays = len(plays)
    if n_plays == 0:
        return _null_dl_edge_metrics()

    result = {}
    result["n_plays"] = n_plays

    # --- Sacks ---
    if "sack" in plays.columns:
        result["n_sacks"] = float(plays["sack"].sum(min_count=1) or 0)
        result["sack_rate"] = result["n_sacks"] / n_plays
    else:
        result["n_sacks"] = np.nan
        result["sack_rate"] = np.nan

    # --- Quick pressure ---
    if "quick_pressure" in plays.columns:
        result["n_quick_pressure"] = float(plays["quick_pressure"].sum(min_count=1) or 0)
        result["quick_pressure_rate"] = result["n_quick_pressure"] / n_plays
    else:
        result["n_quick_pressure"] = np.nan
        result["quick_pressure_rate"] = np.nan

    # --- Time to pressure ---
    if "time_to_pressure" in plays.columns:
        ttp = plays["time_to_pressure"].dropna()
        result["mean_time_to_pressure"] = float(ttp.mean()) if len(ttp) > 0 else np.nan
        result["median_time_to_pressure"] = float(ttp.median()) if len(ttp) > 0 else np.nan
        result["n_pressures"] = len(ttp)
    else:
        result["mean_time_to_pressure"] = np.nan
        result["median_time_to_pressure"] = np.nan
        result["n_pressures"] = np.nan

    # --- Player get-off (first step after snap) ---
    if "player_get_off" in plays.columns:
        go = plays["player_get_off"].dropna()
        result["mean_get_off"] = float(go.mean()) if len(go) > 0 else np.nan
        result["median_get_off"] = float(go.median()) if len(go) > 0 else np.nan
        result["n_get_off_obs"] = len(go)
    else:
        result["mean_get_off"] = np.nan
        result["median_get_off"] = np.nan
        result["n_get_off_obs"] = np.nan

    # --- Tackles / TFLs ---
    if "tackle" in plays.columns:
        result["n_tackles"] = float(plays["tackle"].sum(min_count=1) or 0)
    else:
        result["n_tackles"] = np.nan

    if "tackle_for_loss" in plays.columns:
        result["n_tfl"] = float(plays["tackle_for_loss"].sum(min_count=1) or 0)
    else:
        result["n_tfl"] = np.nan

    return result


def _null_dl_edge_metrics() -> dict:
    return {k: np.nan for k in [
        "n_plays", "n_sacks", "sack_rate", "n_quick_pressure", "quick_pressure_rate",
        "mean_time_to_pressure", "median_time_to_pressure", "n_pressures",
        "mean_get_off", "median_get_off", "n_get_off_obs", "n_tackles", "n_tfl",
    ]}


# ═══════════════════════════════════════════════════════════════════════════════
# Offensive line metrics
# ═══════════════════════════════════════════════════════════════════════════════

def ol_metrics(plays: pd.DataFrame) -> dict:
    """
    Aggregate pass-protection metrics for OL.
    """
    n_plays = len(plays)
    if n_plays == 0:
        return _null_ol_metrics()

    result = {"n_plays": n_plays}

    if "pressure_allowed" in plays.columns:
        result["n_pressure_allowed"] = float(plays["pressure_allowed"].sum(min_count=1) or 0)
        result["pressure_allowed_rate"] = result["n_pressure_allowed"] / n_plays
    else:
        result["n_pressure_allowed"] = np.nan
        result["pressure_allowed_rate"] = np.nan

    if "sack_allowed" in plays.columns:
        result["n_sack_allowed"] = float(plays["sack_allowed"].sum(min_count=1) or 0)
        result["sack_allowed_rate"] = result["n_sack_allowed"] / n_plays
    else:
        result["n_sack_allowed"] = np.nan
        result["sack_allowed_rate"] = np.nan

    if "time_to_pressure_allowed" in plays.columns:
        ttp = plays["time_to_pressure_allowed"].dropna()
        result["mean_time_to_pressure_allowed"] = float(ttp.mean()) if len(ttp) > 0 else np.nan
        result["n_pressure_allowed_obs"] = len(ttp)
    else:
        result["mean_time_to_pressure_allowed"] = np.nan
        result["n_pressure_allowed_obs"] = np.nan

    return result


def _null_ol_metrics() -> dict:
    return {k: np.nan for k in [
        "n_plays", "n_pressure_allowed", "pressure_allowed_rate",
        "n_sack_allowed", "sack_allowed_rate",
        "mean_time_to_pressure_allowed", "n_pressure_allowed_obs",
    ]}


# ═══════════════════════════════════════════════════════════════════════════════
# CB / Safety metrics (defensive back coverage proxies)
# ═══════════════════════════════════════════════════════════════════════════════

def db_metrics(plays: pd.DataFrame) -> dict:
    """
    Coverage-related metrics for defensive backs.
    
    Note: player_play may not have direct coverage success metrics.
    We use targets allowed (if position is in coverage), separation (from offense side),
    and cushion as proxies. This will be augmented during EDA.
    """
    n_plays = len(plays)
    if n_plays == 0:
        return _null_db_metrics()

    result = {"n_plays": n_plays}

    # Tackles and pass breakups are sometimes available
    if "tackle" in plays.columns:
        result["n_tackles"] = float(plays["tackle"].sum(min_count=1) or 0)
    else:
        result["n_tackles"] = np.nan

    if "quick_pressure" in plays.columns:
        result["n_qb_pressures"] = float(plays["quick_pressure"].sum(min_count=1) or 0)
    else:
        result["n_qb_pressures"] = np.nan

    return result


def _null_db_metrics() -> dict:
    return {k: np.nan for k in ["n_plays", "n_tackles", "n_qb_pressures"]}


# ═══════════════════════════════════════════════════════════════════════════════
# Main aggregation entry point
# ═══════════════════════════════════════════════════════════════════════════════

def aggregate_nfl_metrics(
    player_play: pd.DataFrame,
    players: pd.DataFrame,
    season_col: Optional[str] = None,
    first_season_only: bool = True,
) -> pd.DataFrame:
    """
    Aggregate player_play data to per-player (optionally per-season) NFL metrics.

    Parameters
    ----------
    player_play : pd.DataFrame
        Play-level data with nfl_id and position columns.
    players : pd.DataFrame
        Player master table with nfl_id and position (used for position lookup
        when player_play doesn't have position column).
    season_col : str | None
        Name of the season/year column in player_play. If None, all plays are
        treated as a single period.
    first_season_only : bool
        If True and season_col is provided, only keep the first season
        for each player (cleanest scouting interpretation).

    Returns
    -------
    pd.DataFrame
        One row per player (or player-season) with all available metrics.
    """
    # Ensure position is available in player_play
    if "position" not in player_play.columns:
        if "position" in players.columns:
            pos_map = players.set_index("nfl_id")["position"].to_dict()
            player_play = player_play.copy()
            player_play["position"] = player_play["nfl_id"].map(pos_map)
            log.info("aggregate_nfl_metrics: joined 'position' from players table")
        else:
            log.warning("position column not found in player_play or players — cannot stratify metrics")
            player_play = player_play.copy()
            player_play["position"] = "UNK"

    # Build grouping keys
    group_keys = ["nfl_id"]
    if season_col is not None and season_col in player_play.columns:
        group_keys.append(season_col)

    all_rows = []

    for group_vals, group_df in player_play.groupby(group_keys):
        if not isinstance(group_vals, tuple):
            group_vals = (group_vals,)

        meta = dict(zip(group_keys, group_vals))

        # Position from this player's plays
        if "position" in group_df.columns:
            positions = group_df["position"].dropna().unique()
            pos = positions[0] if len(positions) > 0 else "UNK"
        else:
            pos = "UNK"

        pos_group = classify_position(pos)
        meta["position"] = pos
        meta["position_group"] = pos_group

        # Compute position-appropriate metrics
        if pos_group in ("skill_offense",):
            metrics = wr_te_metrics(group_df)
        elif pos_group in ("edge", "dt", "lb"):
            metrics = dl_edge_metrics(group_df)
        elif pos_group == "ol":
            metrics = ol_metrics(group_df)
        elif pos_group in ("cb", "safety"):
            metrics = db_metrics(group_df)
        else:
            # Generic: just count plays
            metrics = {"n_plays": len(group_df)}

        meta.update(metrics)
        all_rows.append(meta)

    result = pd.DataFrame(all_rows)

    if first_season_only and season_col is not None and season_col in result.columns:
        result = result.sort_values(season_col).groupby("nfl_id").first().reset_index()
        log.info(f"aggregate_nfl_metrics: kept first season only — {len(result)} players")

    log.info(
        f"aggregate_nfl_metrics complete: {len(result)} rows | "
        f"{result['nfl_id'].nunique()} unique players"
    )
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# Snap count / playing time
# ═══════════════════════════════════════════════════════════════════════════════

def compute_snap_counts(
    player_play: pd.DataFrame,
    season_col: Optional[str] = None,
) -> pd.DataFrame:
    """
    Compute per-player total snap count (proxy for playing time / opportunity).

    This is a critical confounder: a player who barely played cannot be expected
    to produce stats, regardless of their athletic profile.

    Returns a DataFrame with nfl_id, [season,] n_snaps.
    """
    group_keys = ["nfl_id"]
    if season_col is not None and season_col in player_play.columns:
        group_keys.append(season_col)

    result = player_play.groupby(group_keys).size().reset_index(name="n_snaps")
    log.info(f"compute_snap_counts: {len(result)} player-season rows")
    return result
