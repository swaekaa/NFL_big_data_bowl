"""
visualization.py — Reusable, competition-quality plotting functions.

Every figure answers a specific football or research question.
Follows the project's visualization philosophy: no decorative plots,
every figure must be interpretable and usable in the final submission.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Sequence

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import seaborn as sns

from src.config import FIGURES_DIR, FIGURE_DPI, FIGURE_SIZE_STANDARD, FIGURE_SIZE_WIDE, FIGURE_SIZE_SQUARE

log = logging.getLogger(__name__)

# ── Style Defaults ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.facecolor": "white",
    "axes.facecolor": "#f8f9fa",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})

# NFL-inspired color palette
POSITION_COLORS = {
    "WR": "#003f7f",
    "TE": "#0072CE",
    "RB": "#4da6ff",
    "QB": "#ff6600",
    "OL": "#8B4513",
    "Edge": "#cc0000",
    "DT": "#8B0000",
    "LB": "#B22222",
    "CB": "#228B22",
    "S":  "#32CD32",
    "DB": "#006400",
    "Other": "#888888",
}

CORR_CMAP = "RdBu_r"     # For correlation heatmaps
SPEED_CMAP = "plasma"    # For speed-colored trajectories


def _save(fig: plt.Figure, filename: str, subdir: Optional[str] = None) -> Path:
    """Save figure to FIGURES_DIR (or subdir of it) and return the path."""
    base = FIGURES_DIR
    if subdir:
        base = base / subdir
    base.mkdir(parents=True, exist_ok=True)
    path = base / filename
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    log.info(f"Figure saved: {path}")
    return path


# ═══════════════════════════════════════════════════════════════════════════════
# Drill / dataset overview
# ═══════════════════════════════════════════════════════════════════════════════

def plot_drill_player_counts(
    tracking: pd.DataFrame,
    save: bool = True,
    filename: str = "drill_player_counts.png",
) -> plt.Figure:
    """
    Bar chart: number of unique players per drill type.
    Answers: "Which drills have the most data?"
    """
    if "drill_type" not in tracking.columns or "nfl_id" not in tracking.columns:
        log.warning("plot_drill_player_counts: missing required columns")
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Data not available", ha="center", va="center")
        return fig

    counts = (
        tracking.groupby("drill_type")["nfl_id"]
        .nunique()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_STANDARD)
    bars = ax.bar(
        counts.index, counts.values,
        color="#003f7f", edgecolor="white", linewidth=0.5,
    )
    ax.bar_label(bars, fmt="%d", padding=2, fontsize=9)
    ax.set_title("Unique Players per Combine Drill Type", fontweight="bold")
    ax.set_xlabel("Drill Type")
    ax.set_ylabel("Number of Players")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig


def plot_drill_duration_distribution(
    tracking: pd.DataFrame,
    drill_col: str = "drill_type",
    time_col: str = "time",
    save: bool = True,
    filename: str = "drill_duration_dist.png",
) -> plt.Figure:
    """
    Box plot of drill duration in seconds, stratified by drill type.
    Answers: "How long does each drill typically last?"
    """
    if drill_col not in tracking.columns:
        log.warning("plot_drill_duration_distribution: drill_col not found")
        fig, ax = plt.subplots()
        return fig

    group_keys = [c for c in ["nfl_id", drill_col, "attempt"] if c in tracking.columns]
    if not group_keys or time_col not in tracking.columns:
        log.warning("plot_drill_duration_distribution: insufficient columns")
        fig, ax = plt.subplots()
        return fig

    try:
        times = pd.to_datetime(tracking[time_col])
        tracking = tracking.copy()
        tracking["_t"] = times
        durations = (
            tracking.groupby(group_keys)["_t"]
            .agg(lambda x: (x.max() - x.min()).total_seconds())
            .reset_index(name="duration_s")
        )
    except Exception:
        # If time isn't datetime, use frame count * 0.1
        durations = (
            tracking.groupby(group_keys)
            .size()
            .reset_index(name="n_frames")
        )
        durations["duration_s"] = durations["n_frames"] * 0.1

    order = durations.groupby(drill_col)["duration_s"].median().sort_values(ascending=False).index.tolist()

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)
    drills_present = [d for d in order if d in durations[drill_col].values]
    sns.boxplot(
        data=durations, x=drill_col, y="duration_s", order=drills_present,
        color="#4da6ff", linewidth=0.8, flierprops={"marker": "o", "alpha": 0.3},
        ax=ax,
    )
    ax.set_title("Combine Drill Duration Distribution", fontweight="bold")
    ax.set_xlabel("Drill Type")
    ax.set_ylabel("Duration (seconds)")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Speed and acceleration distributions
# ═══════════════════════════════════════════════════════════════════════════════

def plot_speed_distribution_by_drill(
    tracking: pd.DataFrame,
    drill_col: str = "drill_type",
    speed_col: str = "s",
    max_speed_only: bool = True,
    save: bool = True,
    filename: str = "speed_dist_by_drill.png",
) -> plt.Figure:
    """
    Distribution of speed (or peak speed per attempt) by drill type.
    Answers: "Which drills produce the highest / most variable speeds?"
    """
    if speed_col not in tracking.columns or drill_col not in tracking.columns:
        log.warning("plot_speed_distribution_by_drill: missing columns")
        fig, ax = plt.subplots()
        return fig

    data = tracking.copy()

    if max_speed_only:
        group_keys = [c for c in ["nfl_id", drill_col, "attempt"] if c in data.columns]
        data = data.groupby(group_keys)[speed_col].max().reset_index()
        ylabel = "Peak Speed per Attempt (yards/s)"
        title = "Peak Speed Distribution by Drill Type"
    else:
        ylabel = "Instantaneous Speed (yards/s)"
        title = "Speed Distribution by Drill Type"

    order = data.groupby(drill_col)[speed_col].median().sort_values(ascending=False).index.tolist()

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)
    sns.violinplot(
        data=data, x=drill_col, y=speed_col, order=order,
        palette="Blues_d", inner="quartile", ax=ax,
    )
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("Drill Type")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig


def plot_acceleration_distribution(
    features_df: pd.DataFrame,
    drill_col: str = "drill_type",
    save: bool = True,
    filename: str = "acceleration_dist.png",
) -> plt.Figure:
    """
    Distribution of max acceleration and max deceleration by drill.
    Answers: "Which drills require the most explosive acceleration/deceleration?"
    """
    cols_needed = ["max_acceleration", "max_deceleration", drill_col]
    missing = [c for c in cols_needed if c not in features_df.columns]
    if missing:
        log.warning(f"plot_acceleration_distribution: missing {missing}")
        fig, ax = plt.subplots()
        return fig

    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZE_WIDE)

    for ax, col, color, label in zip(
        axes,
        ["max_acceleration", "max_deceleration"],
        ["#003f7f", "#cc0000"],
        ["Peak Acceleration (yd/s²)", "Peak Deceleration (yd/s²)"],
    ):
        order = features_df.groupby(drill_col)[col].median().sort_values(ascending=False).index
        sns.boxplot(
            data=features_df, x=drill_col, y=col, order=order,
            color=color, linewidth=0.8, ax=ax,
        )
        ax.set_xlabel("Drill Type")
        ax.set_ylabel(label)
        ax.tick_params(axis="x", rotation=30)

    axes[0].set_title("Peak Acceleration by Drill", fontweight="bold")
    axes[1].set_title("Peak Deceleration by Drill", fontweight="bold")
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Trajectory plots
# ═══════════════════════════════════════════════════════════════════════════════

def plot_movement_trajectory(
    attempt_df: pd.DataFrame,
    color_by: str = "s",
    title: str = "",
    ax: Optional[plt.Axes] = None,
    cmap: str = SPEED_CMAP,
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plot a single attempt's x-y trajectory, colored by speed (or other metric).
    Answers: "What does this player's movement look like?"
    """
    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_SQUARE)

    x = attempt_df["x"].astype(float).values
    y = attempt_df["y"].astype(float).values

    if color_by in attempt_df.columns:
        c_vals = attempt_df[color_by].astype(float).values
        norm = mcolors.Normalize(vmin=np.nanmin(c_vals), vmax=np.nanmax(c_vals))
        scalar_map = cm.ScalarMappable(norm=norm, cmap=cmap)

        for i in range(len(x) - 1):
            ax.plot(
                [x[i], x[i+1]], [y[i], y[i+1]],
                color=scalar_map.to_rgba((c_vals[i] + c_vals[i+1]) / 2),
                linewidth=2.5, solid_capstyle="round",
            )
        if fig is not None:
            cbar = fig.colorbar(scalar_map, ax=ax)
            cbar.set_label(color_by, rotation=270, labelpad=15)
    else:
        ax.plot(x, y, color="#003f7f", linewidth=2.5)

    # Mark start and end
    ax.scatter([x[0]], [y[0]], color="green", s=80, zorder=5, label="Start")
    ax.scatter([x[-1]], [y[-1]], color="red", s=80, zorder=5, label="End")
    ax.legend(loc="upper right", fontsize=9)

    ax.set_aspect("equal")
    ax.set_xlabel("x (yards)")
    ax.set_ylabel("y (yards)")
    ax.set_title(title or "Movement Trajectory", fontweight="bold")

    return fig or ax.figure, ax


def plot_trajectories_comparison(
    tracking: pd.DataFrame,
    nfl_ids: Sequence[int],
    drill_type: str,
    attempt: int = 1,
    id_label_map: Optional[dict] = None,
    color_by: str = "s",
    save: bool = True,
    filename: str = "trajectory_comparison.png",
) -> plt.Figure:
    """
    Side-by-side trajectory comparison for multiple players in the same drill.
    Answers: "Do players with different outcomes move differently?"
    """
    n = len(nfl_ids)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 6))
    if n == 1:
        axes = [axes]

    for ax, nfl_id in zip(axes, nfl_ids):
        mask = (tracking["nfl_id"] == nfl_id) & (tracking["drill_type"] == drill_type)
        if "attempt" in tracking.columns:
            mask &= tracking["attempt"] == attempt
        player_df = tracking[mask]
        label = id_label_map.get(nfl_id, str(nfl_id)) if id_label_map else str(nfl_id)
        plot_movement_trajectory(player_df, color_by=color_by, title=label, ax=ax)

    fig.suptitle(
        f"Trajectory Comparison — {drill_type} (Attempt {attempt})",
        fontsize=14, fontweight="bold", y=1.02,
    )
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Correlation heatmap
# ═══════════════════════════════════════════════════════════════════════════════

def plot_correlation_heatmap(
    corr_df: pd.DataFrame,
    title: str = "Correlation: Combine Features vs NFL Outcomes",
    save: bool = True,
    filename: str = "correlation_heatmap.png",
    annot: bool = True,
) -> plt.Figure:
    """
    Heatmap of combine-feature × NFL-outcome correlations.
    Answers: "Which combine metrics are associated with which NFL outcomes?"
    """
    fig, ax = plt.subplots(figsize=(
        max(8, len(corr_df.columns) * 1.2),
        max(6, len(corr_df.index) * 0.6),
    ))

    sns.heatmap(
        corr_df.astype(float),
        cmap=CORR_CMAP,
        center=0,
        vmin=-0.6,
        vmax=0.6,
        annot=annot,
        fmt=".2f",
        linewidths=0.5,
        ax=ax,
        cbar_kws={"label": "Spearman ρ"},
    )
    ax.set_title(title, fontweight="bold", pad=12)
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Scatter: combine metric vs NFL outcome
# ═══════════════════════════════════════════════════════════════════════════════

def plot_combine_vs_nfl(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    position_col: Optional[str] = "position_group",
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    annotate_ids: Optional[list] = None,
    save: bool = True,
    filename: Optional[str] = None,
) -> plt.Figure:
    """
    Scatter plot: one combine tracking feature vs one NFL outcome.
    Colored by position group. Includes OLS trendline.
    Answers: "Is there a relationship between this combine metric and NFL performance?"
    """
    if x_col not in df.columns or y_col not in df.columns:
        log.warning(f"plot_combine_vs_nfl: columns not found ({x_col}, {y_col})")
        fig, ax = plt.subplots()
        return fig

    valid = df[[x_col, y_col] + ([position_col] if position_col and position_col in df.columns else [])].dropna(subset=[x_col, y_col])

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_STANDARD)

    if position_col and position_col in valid.columns:
        groups = valid[position_col].unique()
        for grp in sorted(groups):
            gdata = valid[valid[position_col] == grp]
            color = POSITION_COLORS.get(grp, "#888888")
            ax.scatter(gdata[x_col], gdata[y_col], label=grp, color=color, alpha=0.7, s=50, edgecolors="white", linewidths=0.5)
    else:
        ax.scatter(valid[x_col], valid[y_col], color="#003f7f", alpha=0.7, s=50)

    # OLS trendline
    try:
        from numpy.polynomial import polynomial as P
        mask = valid[[x_col, y_col]].notna().all(axis=1)
        xv = valid[x_col][mask].values
        yv = valid[y_col][mask].values
        coefs = np.polyfit(xv, yv, 1)
        xfit = np.linspace(xv.min(), xv.max(), 200)
        ax.plot(xfit, np.polyval(coefs, xfit), color="#ff6600", linewidth=2, linestyle="--", label="OLS trend", zorder=3)

        from scipy.stats import spearmanr
        rho, p = spearmanr(xv, yv)
        ax.text(0.04, 0.95, f"ρ = {rho:.2f}  (p={p:.3f}, n={len(xv)})",
                transform=ax.transAxes, fontsize=9, va="top",
                bbox=dict(boxstyle="round", fc="white", alpha=0.7))
    except Exception:
        pass

    # Annotate specific players
    if annotate_ids is not None and "nfl_id" in valid.columns:
        for nfl_id in annotate_ids:
            row = valid[valid["nfl_id"] == nfl_id]
            if not row.empty:
                ax.annotate(
                    str(nfl_id),
                    (row[x_col].values[0], row[y_col].values[0]),
                    fontsize=7, alpha=0.8,
                    xytext=(5, 5), textcoords="offset points",
                )

    ax.set_title(title or f"{x_col} vs {y_col}", fontweight="bold")
    ax.set_xlabel(xlabel or x_col)
    ax.set_ylabel(ylabel or y_col)
    if position_col and position_col in valid.columns:
        ax.legend(fontsize=8, framealpha=0.7)
    fig.tight_layout()

    if save:
        fname = filename or f"scatter_{x_col}_vs_{y_col}.png"
        _save(fig, fname)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Model comparison
# ═══════════════════════════════════════════════════════════════════════════════

def plot_model_comparison(
    model_results: dict,
    metric: str = "R²",
    title: str = "Traditional vs Tracking-Enhanced Model",
    save: bool = True,
    filename: str = "model_comparison.png",
) -> plt.Figure:
    """
    Bar chart comparing model performance: traditional only vs tracking-enhanced.
    
    model_results: {model_name: score_value}
    Answers: "Does tracking data add predictive value?"
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    names = list(model_results.keys())
    scores = list(model_results.values())
    colors = ["#888888"] + ["#003f7f"] * (len(names) - 1)

    bars = ax.bar(names, scores, color=colors, edgecolor="white", linewidth=0.8)
    ax.bar_label(bars, fmt="%.3f", padding=3, fontsize=10)
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel(metric)
    ax.set_ylim(0, max(max(scores) * 1.2, 0.1))
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Position group profile
# ═══════════════════════════════════════════════════════════════════════════════

def plot_position_group_profiles(
    features_df: pd.DataFrame,
    feature_cols: list[str],
    position_col: str = "position_group",
    save: bool = True,
    filename: str = "position_profiles.png",
) -> plt.Figure:
    """
    Radar / spider chart of normalized feature medians by position group.
    Answers: "How do different position groups move during the combine?"
    """
    feature_cols = [c for c in feature_cols if c in features_df.columns]
    if not feature_cols or position_col not in features_df.columns:
        log.warning("plot_position_group_profiles: missing columns")
        fig, ax = plt.subplots()
        return fig

    # Normalize each feature to [0, 1]
    normed = features_df.copy()
    for col in feature_cols:
        col_min = normed[col].min()
        col_max = normed[col].max()
        if col_max > col_min:
            normed[col] = (normed[col] - col_min) / (col_max - col_min)
        else:
            normed[col] = 0.5

    group_profiles = normed.groupby(position_col)[feature_cols].median()
    valid_groups = group_profiles.index.tolist()

    N = len(feature_cols)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

    for group in valid_groups:
        values = group_profiles.loc[group].tolist()
        values += values[:1]
        color = POSITION_COLORS.get(group, "#888888")
        ax.plot(angles, values, color=color, linewidth=2, label=group)
        ax.fill(angles, values, color=color, alpha=0.08)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(feature_cols, fontsize=8)
    ax.set_title("Combine Movement Profile by Position Group", fontweight="bold", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=8)
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Missing data overview
# ═══════════════════════════════════════════════════════════════════════════════

def plot_missing_data_heatmap(
    df: pd.DataFrame,
    title: str = "Missing Data Overview",
    max_cols: int = 40,
    save: bool = True,
    filename: str = "missing_data.png",
) -> plt.Figure:
    """
    Visualize missing values across columns.
    Answers: "Which columns / players have missing data?"
    """
    cols = df.columns[:max_cols].tolist()
    miss_pct = df[cols].isnull().mean() * 100
    miss_pct = miss_pct[miss_pct > 0].sort_values(ascending=False)

    if miss_pct.empty:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No missing data detected!", ha="center", va="center",
                fontsize=12, color="green")
        ax.set_title(title)
        if save:
            _save(fig, filename)
        return fig

    fig, ax = plt.subplots(figsize=(max(8, len(miss_pct) * 0.4), 5))
    bars = ax.bar(miss_pct.index, miss_pct.values, color="#cc0000", edgecolor="white")
    ax.bar_label(bars, fmt="%.1f%%", padding=2, fontsize=7)
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel("Missing (%)")
    ax.set_ylim(0, min(miss_pct.max() * 1.2, 100))
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    if save:
        _save(fig, filename)
    return fig
