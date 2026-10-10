# Phase 2 Audit Report

## Introduction
Before beginning new validation experiments, we conducted a code-level audit of the Phase 1 feature engineering and statistical methods to ensure the candidates are robust and mathematically sound.

---

## Candidate 1: Wide Receivers (The "Fluidity" Signal)

- **Feature Definition**: `direction_change_rate`. The number of direction change events (> 20 degrees per 0.1s frame) divided by the total time spent moving at ≥ 1.0 yards/s.
- **Outcome Definition**: `mean_separation`. The mean of `separation_at_pass_forward` across the player's rookie season.
- **Position Filter**: WR
- **Drill Filter**: Short Shuttle
- **Sample Size**: N = 28 players
- **Correlation**: ρ = -0.645
- **P-value**: 0.0002
- **Missing-data handling**: Handled appropriately. Frames with speeds < 1.0 yards/s are masked out to avoid GPS noise masquerading as direction changes.
- **Potential Leakage**: None. Combine tracking is strictly pre-draft, and NFL outcomes are filtered strictly to the rookie season.
- **Potential Confounders**: Draft position, route types run (some routes inherently create more separation), team scheme, snap volume.
- **Implementation Concerns**: **None. Excellent feature design.** The circular difference math correctly handles the 360-to-0 degree wrap-around. The filtering of low-speed frames successfully isolates true, at-speed direction changes.

---

## Candidate 2: Edge Rushers (The "First Step" Signal)

- **Feature Definition**: `burst_impulse_0_1s`. The integral of positive acceleration in the first 0.1 seconds of the drill.
- **Outcome Definition**: `mean_get_off`. The mean `player_get_off` across the player's rookie season.
- **Position Filter**: Edge
- **Drill Filter**: 3-Cone
- **Sample Size**: N = 25 players
- **Correlation**: ρ = -0.480
- **P-value**: 0.014
- **Missing-data handling**: NaNs are treated as 0 for impulse accumulation.
- **Potential Leakage**: None.
- **Potential Confounders**: True pass-rush opportunities vs. run-defense snaps.
- **Implementation Concerns**: **High Risk.** At 10 Hz, 0.1 seconds is exactly ONE frame of data (`burst_impulse_0_1s = max(acc[0], 0) * 0.1`). This relies entirely on the tracking system starting exactly when the player initiates movement. If the player is standing still for the first 0.1s of the data snippet, the impulse is 0, missing the true burst. We must test if `burst_impulse_0_5s` (5 frames) or `time_to_75pct_peak` are more robust.

---

## Candidate 3: Defensive Tackles (The "Efficiency" Signal)

- **Feature Definition**: `movement_efficiency`. Straight-line displacement (from the very first (X,Y) point to the very last (X,Y) point) divided by the total path distance traveled.
- **Outcome Definition**: `sack_rate`. Number of sacks divided by total plays recorded in the NFL season.
- **Position Filter**: DT
- **Drill Filter**: Short Shuttle
- **Sample Size**: N = 16 players
- **Correlation**: ρ = -0.514
- **P-value**: 0.041
- **Missing-data handling**: Handled via Euclidean distance summation.
- **Potential Leakage**: None.
- **Potential Confounders**: Overall snap volume. Total plays vs. True Pass Sets.
- **Implementation Concerns**: **Fatal Flaw.** `movement_efficiency` is mathematically invalid for the Short Shuttle. The shuttle drill requires a player to start at the origin, run 5 yards right, 10 yards left, and 5 yards right, finishing exactly where they started. Therefore, straight-line displacement is near zero for everyone. The metric is accidentally measuring minor stopping-position variances rather than true efficiency. Furthermore, the p-value (0.041) will not survive multiple testing correction. This candidate should be discarded.
