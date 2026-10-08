"""
combine_features.py — Per-attempt movement feature extraction from Combine tracking data.

Design principles:
- Every function operates on a single attempt's tracking DataFrame.
- Handles 0/360-degree wraparound for direction correctly.
- Features are interpretable and football-relevant.
- No future information is used.
- The main entry point is extract_all_features(attempt_df) which returns a flat dict.
"""

from __future__ import annotations

import logging
import warnings
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

log = logging.getLogger(__name__)

# Sampling interval (10 Hz → 0.1 seconds between frames)
DT = 0.1  # seconds

# Speed threshold below which a player is considered "stopped"
STOP_SPEED_THRESHOLD = 0.5  # yards/s

# Deceleration threshold: a must be below this (negative) to count as braking
DECEL_THRESHOLD = -1.0  # yards/s²

# Reacceleration threshold: a must be above this (positive) to count as driving
REACCEL_THRESHOLD = 1.0  # yards/s²

# Minimum speed to consider a direction change meaningful (filter noise)
MIN_SPEED_FOR_DIR_CHANGE = 1.0  # yards/s

# A "burst" starts when speed exceeds this fraction of attempt peak speed
BURST_FRACTION = 0.75


# ═══════════════════════════════════════════════════════════════════════════════
# Core helpers
# ═══════════════════════════════════════════════════════════════════════════════

def _require_cols(df: pd.DataFrame, required: list[str], name: str = "attempt") -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{name}: required columns missing: {missing}")


def _circular_diff_degrees(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Compute the signed angular difference (a - b) in degrees, mapped to [-180, 180].
    Handles the 0/360 wraparound correctly.
    """
    diff = (a - b + 180) % 360 - 180
    return diff


def _abs_circular_diff(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Absolute angular difference in [0, 180] degrees."""
    return np.abs(_circular_diff_degrees(a, b))


def sort_attempt(df: pd.DataFrame) -> pd.DataFrame:
    """Sort a single attempt's frames by time."""
    if "time" in df.columns:
        return df.sort_values("time").reset_index(drop=True)
    return df.reset_index(drop=True)


# ═══════════════════════════════════════════════════════════════════════════════
# Speed features
# ═══════════════════════════════════════════════════════════════════════════════

def speed_features(df: pd.DataFrame) -> dict:
    """
    Derive speed-based features from a single attempt.

    Uses the 's' column (speed in yards/s) directly from tracking data.
    If 's' is missing, estimates from 'dis' / DT.
    """
    _require_cols(df, ["x", "y"], "speed_features")
    df = sort_attempt(df)

    if "s" in df.columns and df["s"].notna().any():
        spd = df["s"].astype(float).values
    else:
        # Fallback: estimate from Euclidean distance between consecutive frames
        dx = df["x"].diff().fillna(0).values
        dy = df["y"].diff().fillna(0).values
        spd = np.sqrt(dx**2 + dy**2) / DT

    n = len(spd)
    if n < 2:
        return _null_speed_features()

    peak_idx = int(np.argmax(spd))

    return {
        "mean_speed": float(np.nanmean(spd)),
        "median_speed": float(np.nanmedian(spd)),
        "max_speed": float(np.nanmax(spd)),
        "speed_std": float(np.nanstd(spd)),
        "time_to_peak_speed": float(peak_idx * DT),  # seconds from start
        "speed_at_5s": _value_at_time(spd, 5.0),
        "speed_at_10s": _value_at_time(spd, 10.0),
        # Fraction of total time spent above 80% of peak speed
        "pct_time_above_80pct_peak": float(np.mean(spd >= 0.8 * np.nanmax(spd))) if np.nanmax(spd) > 0 else 0.0,
    }


def _null_speed_features() -> dict:
    return {k: np.nan for k in [
        "mean_speed", "median_speed", "max_speed", "speed_std",
        "time_to_peak_speed", "speed_at_5s", "speed_at_10s",
        "pct_time_above_80pct_peak",
    ]}


def _value_at_time(arr: np.ndarray, t: float) -> float:
    """Value at index corresponding to time t (seconds from start at DT rate)."""
    idx = int(round(t / DT))
    if idx < len(arr):
        return float(arr[idx])
    return np.nan


# ═══════════════════════════════════════════════════════════════════════════════
# Acceleration features
# ═══════════════════════════════════════════════════════════════════════════════

def acceleration_features(df: pd.DataFrame) -> dict:
    """
    Derive acceleration-based features.

    Uses 'a' column if available; otherwise derives from speed differences.
    """
    df = sort_attempt(df)

    if "a" in df.columns and df["a"].notna().any():
        acc = df["a"].astype(float).values
    elif "s" in df.columns:
        spd = df["s"].astype(float).fillna(0).values
        acc = np.gradient(spd, DT)
    else:
        return _null_accel_features()

    n = len(acc)
    if n < 2:
        return _null_accel_features()

    pos_acc = acc[acc > 0]
    neg_acc = acc[acc < 0]

    # First-step acceleration: mean acceleration over first 0.5 seconds (5 frames)
    first_step_frames = max(1, int(0.5 / DT))
    first_step_acc = float(np.nanmean(acc[:first_step_frames])) if len(acc) >= first_step_frames else np.nan

    return {
        "mean_acceleration": float(np.nanmean(acc)),
        "max_acceleration": float(np.nanmax(acc)),
        "min_acceleration": float(np.nanmin(acc)),  # most negative = peak decel
        "acceleration_std": float(np.nanstd(acc)),
        "first_step_acceleration": first_step_acc,
        "mean_positive_acceleration": float(np.nanmean(pos_acc)) if len(pos_acc) > 0 else 0.0,
        "mean_deceleration": float(np.nanmean(neg_acc)) if len(neg_acc) > 0 else 0.0,
        "max_deceleration": float(np.nanmin(acc)),  # alias for clarity in reports
        # Fraction of time spent actively accelerating / decelerating
        "pct_time_accelerating": float(np.mean(acc > REACCEL_THRESHOLD)),
        "pct_time_decelerating": float(np.mean(acc < DECEL_THRESHOLD)),
    }


def _null_accel_features() -> dict:
    return {k: np.nan for k in [
        "mean_acceleration", "max_acceleration", "min_acceleration", "acceleration_std",
        "first_step_acceleration", "mean_positive_acceleration", "mean_deceleration",
        "max_deceleration", "pct_time_accelerating", "pct_time_decelerating",
    ]}


# ═══════════════════════════════════════════════════════════════════════════════
# Direction-change features
# ═══════════════════════════════════════════════════════════════════════════════

def direction_features(df: pd.DataFrame) -> dict:
    """
    Derive direction-change features using circular statistics.

    Only uses frames where speed >= MIN_SPEED_FOR_DIR_CHANGE to avoid
    counting noise as direction changes when the player is nearly stopped.
    """
    df = sort_attempt(df)
    _require_cols(df, ["dir"], "direction_features")

    d = df["dir"].astype(float).values

    # Mask low-speed frames
    if "s" in df.columns:
        spd = df["s"].astype(float).values
        mask = spd >= MIN_SPEED_FOR_DIR_CHANGE
    else:
        mask = np.ones(len(d), dtype=bool)

    d_masked = d[mask]
    if len(d_masked) < 2:
        return _null_dir_features()

    # Absolute angular changes between consecutive frames (only during movement)
    consecutive_changes = _abs_circular_diff(d_masked[1:], d_masked[:-1])

    # Total direction change (sum of abs angular differences)
    total_change = float(np.sum(consecutive_changes))

    # Detect discrete direction-change events (threshold: > 20 degrees in one frame)
    CHANGE_EVENT_THRESHOLD = 20.0  # degrees
    event_mask = consecutive_changes > CHANGE_EVENT_THRESHOLD
    n_direction_events = int(np.sum(event_mask))

    # Circular mean and std of direction
    d_rad = np.deg2rad(d_masked)
    circ_mean_rad = np.arctan2(np.mean(np.sin(d_rad)), np.mean(np.cos(d_rad)))
    circ_mean_deg = float(np.rad2deg(circ_mean_rad) % 360)
    circ_std_deg = float(np.rad2deg(
        np.sqrt(-2 * np.log(np.sqrt(np.mean(np.sin(d_rad))**2 + np.mean(np.cos(d_rad))**2)))
    ))

    return {
        "total_direction_change": total_change,
        "max_direction_change": float(np.max(consecutive_changes)) if len(consecutive_changes) > 0 else 0.0,
        "mean_direction_change_per_frame": float(np.mean(consecutive_changes)),
        "direction_change_rate": float(n_direction_events / (len(d_masked) * DT)) if len(d_masked) > 0 else 0.0,
        "n_direction_events": n_direction_events,
        "circular_mean_direction": circ_mean_deg,
        "circular_std_direction": circ_std_deg,
    }


def _null_dir_features() -> dict:
    return {k: np.nan for k in [
        "total_direction_change", "max_direction_change",
        "mean_direction_change_per_frame", "direction_change_rate",
        "n_direction_events", "circular_mean_direction", "circular_std_direction",
    ]}


# ═══════════════════════════════════════════════════════════════════════════════
# Movement efficiency
# ═══════════════════════════════════════════════════════════════════════════════

def efficiency_features(df: pd.DataFrame) -> dict:
    """
    Movement efficiency = straight-line displacement / total path length.
    A 40-yard dash should have efficiency ≈ 1.0.
    A 3-cone drill will have much lower efficiency.
    """
    df = sort_attempt(df)
    _require_cols(df, ["x", "y"], "efficiency_features")

    x = df["x"].astype(float).values
    y = df["y"].astype(float).values

    if len(x) < 2:
        return {"movement_efficiency": np.nan, "total_path_length": np.nan,
                "straight_line_distance": np.nan, "displacement_x": np.nan,
                "displacement_y": np.nan}

    # Total path length
    if "dis" in df.columns and df["dis"].notna().any():
        total_path = float(df["dis"].astype(float).sum())
    else:
        dists = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
        total_path = float(np.sum(dists))

    # Straight-line displacement from first to last point
    dx = x[-1] - x[0]
    dy = y[-1] - y[0]
    straight_line = float(np.sqrt(dx**2 + dy**2))

    efficiency = straight_line / total_path if total_path > 0 else np.nan

    return {
        "movement_efficiency": efficiency,
        "total_path_length": total_path,
        "straight_line_distance": straight_line,
        "displacement_x": float(dx),
        "displacement_y": float(dy),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Re-acceleration features (the key football metric)
# ═══════════════════════════════════════════════════════════════════════════════

def reacceleration_features(df: pd.DataFrame) -> dict:
    """
    Detect braking → direction-change → reacceleration sequences.

    This is the "cut" pattern: the ability to rapidly decelerate,
    change direction, and then re-drive at speed.

    Returns metrics for the BEST (highest peak reaccel) sequence found.
    If multiple sequences exist, also returns aggregate statistics.
    """
    df = sort_attempt(df)

    if "a" in df.columns and df["a"].notna().any():
        acc = df["a"].astype(float).values
    elif "s" in df.columns:
        spd = df["s"].astype(float).fillna(0).values
        acc = np.gradient(spd, DT)
    else:
        return _null_reaccel_features()

    if "s" in df.columns:
        spd = df["s"].astype(float).values
    else:
        spd = np.abs(acc) * DT  # rough approximation

    if "dir" in df.columns:
        direction = df["dir"].astype(float).values
    else:
        direction = None

    n = len(acc)
    if n < 10:
        return _null_reaccel_features()

    sequences = []

    # Scan for braking phases
    i = 0
    while i < n - 5:
        # Find start of braking: acc < DECEL_THRESHOLD
        if acc[i] < DECEL_THRESHOLD:
            brake_start = i
            # Find end of braking: acc returns above threshold or speed near zero
            j = i + 1
            while j < n and acc[j] < DECEL_THRESHOLD:
                j += 1
            brake_end = j

            brake_duration = (brake_end - brake_start) * DT
            brake_magnitude = float(np.mean(acc[brake_start:brake_end]))
            speed_at_brake_end = spd[min(brake_end, n-1)]

            # Check if a direction change occurred during / just after braking
            dir_change = 0.0
            if direction is not None and brake_end < n:
                window = slice(max(0, brake_start), min(n, brake_end + 3))
                d_window = direction[window]
                if len(d_window) >= 2:
                    diffs = _abs_circular_diff(d_window[1:], d_window[:-1])
                    dir_change = float(np.sum(diffs))

            # Find subsequent reacceleration: acc > REACCEL_THRESHOLD
            k = brake_end
            while k < n and acc[k] < REACCEL_THRESHOLD:
                k += 1

            if k < n:
                reaccel_start = k
                # Find end of reaccel phase
                m = k + 1
                while m < n and acc[m] > REACCEL_THRESHOLD:
                    m += 1
                reaccel_end = m

                reaccel_duration = (reaccel_end - reaccel_start) * DT
                reaccel_magnitude = float(np.mean(acc[reaccel_start:reaccel_end]))
                peak_reaccel = float(np.max(acc[reaccel_start:reaccel_end]))

                # Time from brake end to reaccel start (transition time)
                transition_time = (reaccel_start - brake_end) * DT

                sequences.append({
                    "brake_start_t": brake_start * DT,
                    "brake_duration": brake_duration,
                    "brake_magnitude": brake_magnitude,
                    "speed_at_brake_end": speed_at_brake_end,
                    "direction_change_during_brake": dir_change,
                    "transition_time": transition_time,
                    "reaccel_duration": reaccel_duration,
                    "reaccel_magnitude": reaccel_magnitude,
                    "peak_reaccel": peak_reaccel,
                    "total_sequence_time": brake_duration + transition_time + reaccel_duration,
                })

                i = reaccel_end  # skip to after this sequence
            else:
                i = brake_end
        else:
            i += 1

    if not sequences:
        return _null_reaccel_features()

    # Select best sequence by peak reacceleration
    best = max(sequences, key=lambda s: s["peak_reaccel"])

    return {
        "n_cut_sequences": len(sequences),
        "best_brake_duration": best["brake_duration"],
        "best_brake_magnitude": best["brake_magnitude"],
        "best_speed_at_brake_end": best["speed_at_brake_end"],
        "best_dir_change_during_brake": best["direction_change_during_brake"],
        "best_transition_time": best["transition_time"],
        "best_reaccel_magnitude": best["reaccel_magnitude"],
        "best_peak_reaccel": best["peak_reaccel"],
        "best_total_sequence_time": best["total_sequence_time"],
        "mean_peak_reaccel": float(np.mean([s["peak_reaccel"] for s in sequences])),
        "mean_brake_magnitude": float(np.mean([s["brake_magnitude"] for s in sequences])),
        "mean_transition_time": float(np.mean([s["transition_time"] for s in sequences])),
    }


def _null_reaccel_features() -> dict:
    return {k: np.nan for k in [
        "n_cut_sequences", "best_brake_duration", "best_brake_magnitude",
        "best_speed_at_brake_end", "best_dir_change_during_brake",
        "best_transition_time", "best_reaccel_magnitude", "best_peak_reaccel",
        "best_total_sequence_time", "mean_peak_reaccel", "mean_brake_magnitude",
        "mean_transition_time",
    ]}


# ═══════════════════════════════════════════════════════════════════════════════
# First-step burst (key for DL/Edge)
# ═══════════════════════════════════════════════════════════════════════════════

def first_step_burst_features(df: pd.DataFrame) -> dict:
    """
    Quantify the initial burst of acceleration at the start of a drill.

    Especially relevant for DL/Edge rushers: time to reach X% of peak speed,
    acceleration impulse in the first 0.5 seconds.
    """
    df = sort_attempt(df)

    if "s" in df.columns and df["s"].notna().any():
        spd = df["s"].astype(float).values
    else:
        return {k: np.nan for k in [
            "time_to_50pct_peak", "time_to_75pct_peak", "time_to_90pct_peak",
            "burst_impulse_0_5s", "burst_impulse_0_1s",
        ]}

    if len(spd) < 3:
        return {k: np.nan for k in [
            "time_to_50pct_peak", "time_to_75pct_peak", "time_to_90pct_peak",
            "burst_impulse_0_5s", "burst_impulse_0_1s",
        ]}

    peak = np.nanmax(spd)
    if peak <= 0:
        return {k: np.nan for k in [
            "time_to_50pct_peak", "time_to_75pct_peak", "time_to_90pct_peak",
            "burst_impulse_0_5s", "burst_impulse_0_1s",
        ]}

    def time_to_pct(pct: float) -> float:
        threshold = pct * peak
        idxs = np.where(spd >= threshold)[0]
        if len(idxs) == 0:
            return np.nan
        return float(idxs[0] * DT)

    # Impulse = area under acceleration curve in first N frames
    if "a" in df.columns:
        acc = df["a"].astype(float).values
    else:
        acc = np.gradient(spd, DT)

    frames_0_5s = max(1, int(0.5 / DT))
    frames_0_1s = max(1, int(0.1 / DT))

    burst_impulse_0_5s = float(np.sum(np.maximum(acc[:frames_0_5s], 0)) * DT)
    burst_impulse_0_1s = float(np.sum(np.maximum(acc[:frames_0_1s], 0)) * DT)

    return {
        "time_to_50pct_peak": time_to_pct(0.50),
        "time_to_75pct_peak": time_to_pct(0.75),
        "time_to_90pct_peak": time_to_pct(0.90),
        "burst_impulse_0_5s": burst_impulse_0_5s,
        "burst_impulse_0_1s": burst_impulse_0_1s,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Main feature extraction entry point
# ═══════════════════════════════════════════════════════════════════════════════

def extract_all_features(
    attempt_df: pd.DataFrame,
    feature_groups: Optional[list[str]] = None,
) -> dict:
    """
    Extract the full movement feature set from one tracking attempt.

    Parameters
    ----------
    attempt_df : pd.DataFrame
        Rows for a single (nfl_id, drill_type, attempt) combination.
    feature_groups : list[str] | None
        Subset of groups to compute. Options:
        ['speed', 'acceleration', 'direction', 'efficiency', 'reaccel', 'burst']
        Defaults to all groups.

    Returns
    -------
    dict
        Flat dictionary of feature names → values.
        NaN where computation was not possible.
    """
    if feature_groups is None:
        feature_groups = ["speed", "acceleration", "direction", "efficiency", "reaccel", "burst"]

    features = {}

    if "speed" in feature_groups:
        features.update(speed_features(attempt_df))

    if "acceleration" in feature_groups:
        features.update(acceleration_features(attempt_df))

    if "direction" in feature_groups:
        try:
            features.update(direction_features(attempt_df))
        except Exception as e:
            log.warning(f"direction_features failed: {e}")
            features.update(_null_dir_features())

    if "efficiency" in feature_groups:
        features.update(efficiency_features(attempt_df))

    if "reaccel" in feature_groups:
        try:
            features.update(reacceleration_features(attempt_df))
        except Exception as e:
            log.warning(f"reacceleration_features failed: {e}")
            features.update(_null_reaccel_features())

    if "burst" in feature_groups:
        features.update(first_step_burst_features(attempt_df))

    features["n_frames"] = len(attempt_df)
    features["duration_s"] = len(attempt_df) * DT

    return features


# ═══════════════════════════════════════════════════════════════════════════════
# Batch processing
# ═══════════════════════════════════════════════════════════════════════════════

def extract_features_from_tracking(
    tracking_df: pd.DataFrame,
    feature_groups: Optional[list[str]] = None,
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Apply extract_all_features to every unique (nfl_id, drill_type, attempt) combination.

    Parameters
    ----------
    tracking_df : pd.DataFrame
        Full combine_tracking DataFrame (or a filtered subset).
    feature_groups : list[str] | None
        Which feature groups to compute. Defaults to all.
    verbose : bool
        Log progress every 100 players.

    Returns
    -------
    pd.DataFrame
        One row per attempt, with attempt metadata + all features.
    """
    group_keys = ["nfl_id", "drill_type", "attempt"]
    # Only use keys that exist in the DataFrame
    keys = [k for k in group_keys if k in tracking_df.columns]

    if not keys:
        raise ValueError("tracking_df must have at least 'nfl_id' and 'drill_type' columns.")

    rows = []
    players_seen = set()
    total_attempts = tracking_df.groupby(keys).ngroups

    log.info(f"Extracting features from {total_attempts:,} attempts ...")

    for idx, (group_vals, attempt_df) in enumerate(tracking_df.groupby(keys)):
        if not isinstance(group_vals, tuple):
            group_vals = (group_vals,)

        meta = dict(zip(keys, group_vals))

        if "nfl_id" in meta:
            players_seen.add(meta["nfl_id"])

        feats = extract_all_features(attempt_df, feature_groups=feature_groups)
        feats.update(meta)
        rows.append(feats)

        if verbose and (idx + 1) % 500 == 0:
            log.info(
                f"  {idx+1}/{total_attempts} attempts | "
                f"{len(players_seen)} unique players"
            )

    result = pd.DataFrame(rows)

    # Move metadata columns to front
    meta_cols = [k for k in keys if k in result.columns]
    other_cols = [c for c in result.columns if c not in meta_cols]
    result = result[meta_cols + other_cols]

    log.info(
        f"Feature extraction complete: {len(result)} attempts | "
        f"{len(players_seen)} unique players | {result.shape[1]} features"
    )
    return result


def aggregate_player_features(
    features_df: pd.DataFrame,
    agg_strategy: str = "best_attempt",
) -> pd.DataFrame:
    """
    Aggregate per-attempt features to per-player-per-drill features.

    Parameters
    ----------
    features_df : pd.DataFrame
        Output of extract_features_from_tracking.
    agg_strategy : str
        'best_attempt' — for each player/drill, keep the attempt with the
            highest max_speed (proxy for best effort).
        'mean' — average across all attempts.

    Returns
    -------
    pd.DataFrame
        One row per (nfl_id, drill_type).
    """
    group_cols = ["nfl_id", "drill_type"]
    group_cols = [c for c in group_cols if c in features_df.columns]

    numeric_cols = features_df.select_dtypes(include=np.number).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in group_cols]

    if agg_strategy == "best_attempt":
        if "max_speed" not in features_df.columns:
            log.warning("max_speed not in features; falling back to mean aggregation")
            agg_strategy = "mean"
        else:
            # For each (nfl_id, drill_type), select the attempt with highest max_speed
            idx = features_df.groupby(group_cols)["max_speed"].idxmax()
            result = features_df.loc[idx].reset_index(drop=True)
            log.info(f"aggregate_player_features (best_attempt): {len(result)} rows")
            return result

    if agg_strategy == "mean":
        result = features_df.groupby(group_cols)[numeric_cols].mean().reset_index()
        log.info(f"aggregate_player_features (mean): {len(result)} rows")
        return result

    raise ValueError(f"Unknown agg_strategy: {agg_strategy}")
