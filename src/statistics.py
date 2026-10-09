"""
statistics.py — Statistical discovery utilities.

Design principles:
- Player is always the unit of analysis (not frames).
- Use Spearman correlations for robustness to outliers.
- Report effect sizes and bootstrap CIs, not just p-values.
- Bootstrap functions use the player as the resampling unit.
- Flag when sample sizes are insufficient (<MIN_SAMPLE_SIZE).
"""

from __future__ import annotations

import logging
import warnings
from typing import Optional, Sequence

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats

log = logging.getLogger(__name__)

# Minimum n to report findings.
MIN_N = 10
BOOTSTRAP_N = 1000
RANDOM_SEED = 42
RNG = np.random.default_rng(RANDOM_SEED)


# ═══════════════════════════════════════════════════════════════════════════════
# Correlation utilities
# ═══════════════════════════════════════════════════════════════════════════════

def spearman_with_ci(
    x: np.ndarray,
    y: np.ndarray,
    n_boot: int = BOOTSTRAP_N,
    alpha: float = 0.05,
) -> dict:
    """
    Compute Spearman correlation with bootstrap confidence interval.

    Parameters
    ----------
    x, y : array-like
        Paired observations. Must have the same length.
        NaN pairs are dropped automatically.
    n_boot : int
        Number of bootstrap resamples.
    alpha : float
        CI coverage = 1 - alpha.

    Returns
    -------
    dict with keys:
        rho, p_value, n, ci_lower, ci_upper, interpretation
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    mask = ~(np.isnan(x) | np.isnan(y))
    x, y = x[mask], y[mask]
    n = len(x)

    if n < MIN_N:
        return {
            "rho": np.nan,
            "p_value": np.nan,
            "n": n,
            "ci_lower": np.nan,
            "ci_upper": np.nan,
            "interpretation": f"INSUFFICIENT SAMPLE (n={n}, min={MIN_N})",
        }

    rho, p_val = scipy_stats.spearmanr(x, y)

    # Bootstrap CI
    boot_rhos = []
    idx_all = np.arange(n)
    for _ in range(n_boot):
        idx = RNG.choice(idx_all, size=n, replace=True)
        r, _ = scipy_stats.spearmanr(x[idx], y[idx])
        boot_rhos.append(r)

    boot_rhos = np.array(boot_rhos)
    ci_lower = float(np.percentile(boot_rhos, 100 * alpha / 2))
    ci_upper = float(np.percentile(boot_rhos, 100 * (1 - alpha / 2)))

    interp = _interpret_correlation(float(rho), n)

    return {
        "rho": float(rho),
        "p_value": float(p_val),
        "n": n,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "interpretation": interp,
    }


def pearson_with_ci(
    x: np.ndarray,
    y: np.ndarray,
    n_boot: int = BOOTSTRAP_N,
    alpha: float = 0.05,
) -> dict:
    """
    Compute Pearson correlation with bootstrap confidence interval.
    Use Spearman when normality is not guaranteed.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    mask = ~(np.isnan(x) | np.isnan(y))
    x, y = x[mask], y[mask]
    n = len(x)

    if n < MIN_N:
        return {"r": np.nan, "p_value": np.nan, "n": n,
                "ci_lower": np.nan, "ci_upper": np.nan}

    r, p_val = scipy_stats.pearsonr(x, y)

    boot_rs = []
    idx_all = np.arange(n)
    for _ in range(n_boot):
        idx = RNG.choice(idx_all, size=n, replace=True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r_b, _ = scipy_stats.pearsonr(x[idx], y[idx])
        boot_rs.append(r_b)

    boot_rs = np.array(boot_rs)
    ci_lower = float(np.percentile(boot_rs, 100 * alpha / 2))
    ci_upper = float(np.percentile(boot_rs, 100 * (1 - alpha / 2)))

    return {
        "r": float(r),
        "p_value": float(p_val),
        "n": n,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
    }


def _interpret_correlation(rho: float, n: int) -> str:
    """Human-readable interpretation of a Spearman correlation."""
    abs_rho = abs(rho)
    direction = "positive" if rho > 0 else "negative"

    if abs_rho >= 0.5:
        strength = "strong"
    elif abs_rho >= 0.3:
        strength = "moderate"
    elif abs_rho >= 0.15:
        strength = "weak"
    else:
        strength = "negligible"

    return f"{strength} {direction} (ρ={rho:.3f}, n={n})"


# ═══════════════════════════════════════════════════════════════════════════════
# Correlation matrix over player-level data
# ═══════════════════════════════════════════════════════════════════════════════

def correlation_matrix(
    df: pd.DataFrame,
    x_cols: list[str],
    y_cols: list[str],
    method: str = "spearman",
) -> pd.DataFrame:
    """
    Compute a correlation matrix between x_cols and y_cols.

    Parameters
    ----------
    df : pd.DataFrame
        Player-level data.
    x_cols : list[str]
        Combine tracking features (rows of matrix).
    y_cols : list[str]
        NFL outcome metrics (columns of matrix).
    method : str
        'spearman' or 'pearson'.

    Returns
    -------
    pd.DataFrame
        Correlation matrix with x_cols as index, y_cols as columns.
        Values are correlation coefficients.
    """
    x_cols = [c for c in x_cols if c in df.columns]
    y_cols = [c for c in y_cols if c in df.columns]

    if not x_cols or not y_cols:
        log.warning("correlation_matrix: no valid columns found")
        return pd.DataFrame()

    results = []
    for x in x_cols:
        row = {}
        for y in y_cols:
            if x == y:
                row[y] = 1.0
                continue
                
            valid = df[[x, y]].dropna()
            n = len(valid)
            if n < MIN_N:
                row[y] = np.nan
            else:
                # Force 1D arrays in case of accidental duplicate columns in df
                x_data = valid.iloc[:, 0].values
                y_data = valid.iloc[:, 1].values
                
                if method == "spearman":
                    rho, _ = scipy_stats.spearmanr(x_data, y_data)
                    row[y] = float(rho)
                else:
                    r, _ = scipy_stats.pearsonr(x_data, y_data)
                    row[y] = float(r)
        results.append(pd.Series(row, name=x))

    return pd.DataFrame(results)


# ═══════════════════════════════════════════════════════════════════════════════
# Effect size utilities
# ═══════════════════════════════════════════════════════════════════════════════

def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """
    Compute Cohen's d effect size between two groups.
    Positive = group1 > group2.
    """
    g1 = np.asarray(group1, dtype=float)
    g2 = np.asarray(group2, dtype=float)
    g1 = g1[~np.isnan(g1)]
    g2 = g2[~np.isnan(g2)]

    if len(g1) < 2 or len(g2) < 2:
        return np.nan

    pooled_std = np.sqrt(
        ((len(g1) - 1) * g1.std(ddof=1)**2 + (len(g2) - 1) * g2.std(ddof=1)**2)
        / (len(g1) + len(g2) - 2)
    )
    if pooled_std == 0:
        return 0.0

    return float((g1.mean() - g2.mean()) / pooled_std)


def rank_biserial_r(group1: np.ndarray, group2: np.ndarray) -> float:
    """
    Rank-biserial correlation — non-parametric effect size for two groups.
    Equivalent to 2 * (U / (n1 * n2)) - 1, where U is Mann-Whitney U.
    Range: [-1, 1]. Values near ±1 indicate strong group separation.
    """
    g1 = np.asarray(group1, dtype=float)
    g2 = np.asarray(group2, dtype=float)
    g1 = g1[~np.isnan(g1)]
    g2 = g2[~np.isnan(g2)]

    if len(g1) < 2 or len(g2) < 2:
        return np.nan

    u_stat, _ = scipy_stats.mannwhitneyu(g1, g2, alternative="two-sided")
    rbr = 1 - (2 * u_stat) / (len(g1) * len(g2))
    return float(rbr)


# ═══════════════════════════════════════════════════════════════════════════════
# Group comparison
# ═══════════════════════════════════════════════════════════════════════════════

def compare_groups(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    min_n_per_group: int = MIN_N,
) -> pd.DataFrame:
    """
    Compare a numeric metric across categories (e.g., position groups).

    Returns a summary DataFrame with median, IQR, mean, std, n per group,
    plus pairwise Mann-Whitney p-values.
    """
    if group_col not in df.columns or value_col not in df.columns:
        log.warning(f"compare_groups: columns not found ({group_col}, {value_col})")
        return pd.DataFrame()

    valid = df[[group_col, value_col]].dropna()
    groups = valid[group_col].unique()

    summary_rows = []
    for g in sorted(groups):
        gdata = valid[valid[group_col] == g][value_col].values
        if len(gdata) < min_n_per_group:
            continue
        summary_rows.append({
            "group": g,
            "n": len(gdata),
            "mean": float(np.mean(gdata)),
            "median": float(np.median(gdata)),
            "std": float(np.std(gdata, ddof=1)),
            "q25": float(np.percentile(gdata, 25)),
            "q75": float(np.percentile(gdata, 75)),
            "min": float(np.min(gdata)),
            "max": float(np.max(gdata)),
        })

    if not summary_rows:
        return pd.DataFrame()

    return pd.DataFrame(summary_rows).set_index("group")


def mannwhitney_matrix(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    min_n_per_group: int = MIN_N,
) -> pd.DataFrame:
    """
    Compute pairwise Mann-Whitney p-values between groups.
    """
    valid = df[[group_col, value_col]].dropna()
    groups = [
        g for g in sorted(valid[group_col].unique())
        if len(valid[valid[group_col] == g]) >= min_n_per_group
    ]

    mat = pd.DataFrame(index=groups, columns=groups, dtype=float)

    for i, g1 in enumerate(groups):
        for j, g2 in enumerate(groups):
            if i == j:
                mat.loc[g1, g2] = np.nan
            else:
                d1 = valid[valid[group_col] == g1][value_col].values
                d2 = valid[valid[group_col] == g2][value_col].values
                _, p = scipy_stats.mannwhitneyu(d1, d2, alternative="two-sided")
                mat.loc[g1, g2] = float(p)

    return mat


# ═══════════════════════════════════════════════════════════════════════════════
# Incremental value (tracking vs traditional)
# ═══════════════════════════════════════════════════════════════════════════════

def incremental_r_squared(
    y: np.ndarray,
    x_baseline: pd.DataFrame,
    x_full: pd.DataFrame,
) -> dict:
    """
    Compute the incremental R² of adding tracking features on top of
    traditional combine features.

    Uses OLS: not a final model evaluation, just a discovery tool.

    Parameters
    ----------
    y : array-like
        NFL outcome (player-level, aligned with x_baseline/x_full).
    x_baseline : pd.DataFrame
        Traditional combine features only.
    x_full : pd.DataFrame
        Traditional + tracking features.

    Returns
    -------
    dict with r2_baseline, r2_full, delta_r2.
    """
    from sklearn.linear_model import Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import cross_val_score

    y = np.asarray(y, dtype=float)
    mask = ~np.isnan(y)

    # Also mask rows where baseline features are all NaN
    baseline_mask = x_baseline.notna().any(axis=1).values
    full_mask = x_full.notna().any(axis=1).values
    valid_mask = mask & baseline_mask & full_mask

    if valid_mask.sum() < MIN_N:
        return {
            "r2_baseline": np.nan,
            "r2_full": np.nan,
            "delta_r2": np.nan,
            "n": int(valid_mask.sum()),
            "note": "Insufficient valid observations",
        }

    y_v = y[valid_mask]
    xb_v = x_baseline[valid_mask].fillna(0)
    xf_v = x_full[valid_mask].fillna(0)

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("ridge", Ridge(alpha=1.0)),
    ])

    # Use leave-one-out or 5-fold depending on sample size
    cv = min(5, len(y_v) // 5)
    cv = max(cv, 2)

    r2_baseline = float(np.mean(cross_val_score(pipe, xb_v, y_v, cv=cv, scoring="r2")))
    r2_full = float(np.mean(cross_val_score(pipe, xf_v, y_v, cv=cv, scoring="r2")))

    return {
        "r2_baseline": r2_baseline,
        "r2_full": r2_full,
        "delta_r2": r2_full - r2_baseline,
        "n": int(valid_mask.sum()),
        "cv_folds": cv,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Summary table builder
# ═══════════════════════════════════════════════════════════════════════════════

def build_correlation_summary(
    df: pd.DataFrame,
    combine_cols: list[str],
    outcome_cols: list[str],
    method: str = "spearman",
    min_n: int = MIN_N,
) -> pd.DataFrame:
    """
    Build a ranked summary table of correlations between combine features
    and NFL outcomes.

    Returns rows sorted by abs(rho) descending.
    """
    rows = []
    for c in combine_cols:
        for o in outcome_cols:
            if c not in df.columns or o not in df.columns:
                continue
            valid = df[[c, o]].dropna()
            n = len(valid)
            if n < min_n:
                continue
            if method == "spearman":
                rho, p = scipy_stats.spearmanr(valid[c], valid[o])
            else:
                rho, p = scipy_stats.pearsonr(valid[c], valid[o])

            rows.append({
                "combine_feature": c,
                "nfl_outcome": o,
                "rho": float(rho),
                "abs_rho": float(abs(rho)),
                "p_value": float(p),
                "n": n,
                "significant": p < 0.05,
            })

    result = (
        pd.DataFrame(rows)
        .sort_values("abs_rho", ascending=False)
        .reset_index(drop=True)
    )
    log.info(
        f"build_correlation_summary: {len(result)} pairs | "
        f"{result['significant'].sum()} significant at p<0.05"
    )
    return result
