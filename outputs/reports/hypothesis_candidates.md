# NFL Big Data Bowl 2027 — Hypothesis Candidates

*Generated: 2026-10-09 22:08*

> All numbers below come from actual data. Where data was unavailable, "NOT YET COMPUTED" is stated explicitly.

## Ranked Correlation Findings
Ranked by |ρ| (Spearman). Minimum n = 10 players.

| Rank | Position | Combine Feature | NFL Outcome | ρ | n | p-value |
|------|----------|-----------------|-------------|---|---|---------|
| 761 | S | mean_speed_THREE_CONE_DRILL | n_tackles | -0.871 | 10 | 0.0010 |
| 762 | S | time_to_75pct_peak_THREE_CONE_DRILL | n_tackles | 0.778 | 10 | 0.0080 |
| 763 | S | max_speed_THREE_CONE_DRILL | n_tackles | -0.755 | 10 | 0.0116 |
| 1 | WR | direction_change_rate_SHORT_SHUTTLE | mean_separation | -0.645 | 28 | 0.0002 |
| 201 | TE | time_to_75pct_peak_THREE_CONE_DRILL | target_share | -0.575 | 17 | 0.0158 |
| 721 | CB | max_speed_SHORT_SHUTTLE | n_tackles | 0.567 | 15 | 0.0277 |
| 722 | CB | mean_speed_THREE_CONE_DRILL | n_tackles | 0.557 | 12 | 0.0600 |
| 521 | DT | mean_speed_SHORT_SHUTTLE | quick_pressure_rate | 0.527 | 15 | 0.0436 |
| 723 | CB | time_to_75pct_peak_THREE_CONE_DRILL | n_tackles | -0.524 | 12 | 0.0804 |
| 522 | DT | movement_efficiency_SHORT_SHUTTLE | sack_rate | -0.514 | 16 | 0.0418 |


## Candidate Hypotheses (Template)

Fill in based on actual data findings above.


### Hypothesis #1
- **Hypothesis**: mean_speed_THREE_CONE_DRILL during Combine drills is associated with n_tackles in S players
- **Position**: S
- **Tracking Metric**: mean_speed_THREE_CONE_DRILL
- **Nfl Outcome**: n_tackles
- **Sample Size**: 10
- **Evidence**: ρ = -0.871, p = 0.0010 (statistically significant)
- **Potential Confounders**: draft position, team scheme, snap count, opponent quality, position within scheme

### Hypothesis #2
- **Hypothesis**: time_to_75pct_peak_THREE_CONE_DRILL during Combine drills is associated with n_tackles in S players
- **Position**: S
- **Tracking Metric**: time_to_75pct_peak_THREE_CONE_DRILL
- **Nfl Outcome**: n_tackles
- **Sample Size**: 10
- **Evidence**: ρ = 0.778, p = 0.0080 (statistically significant)
- **Potential Confounders**: draft position, team scheme, snap count, opponent quality, position within scheme

### Hypothesis #3
- **Hypothesis**: max_speed_THREE_CONE_DRILL during Combine drills is associated with n_tackles in S players
- **Position**: S
- **Tracking Metric**: max_speed_THREE_CONE_DRILL
- **Nfl Outcome**: n_tackles
- **Sample Size**: 10
- **Evidence**: ρ = -0.755, p = 0.0116 (statistically significant)
- **Potential Confounders**: draft position, team scheme, snap count, opponent quality, position within scheme

### Hypothesis #4
- **Hypothesis**: direction_change_rate_SHORT_SHUTTLE during Combine drills is associated with mean_separation in WR players
- **Position**: WR
- **Tracking Metric**: direction_change_rate_SHORT_SHUTTLE
- **Nfl Outcome**: mean_separation
- **Sample Size**: 28
- **Evidence**: ρ = -0.645, p = 0.0002 (statistically significant)
- **Potential Confounders**: draft position, team scheme, snap count, opponent quality, position within scheme

### Hypothesis #5
- **Hypothesis**: time_to_75pct_peak_THREE_CONE_DRILL during Combine drills is associated with target_share in TE players
- **Position**: TE
- **Tracking Metric**: time_to_75pct_peak_THREE_CONE_DRILL
- **Nfl Outcome**: target_share
- **Sample Size**: 17
- **Evidence**: ρ = -0.575, p = 0.0158 (statistically significant)
- **Potential Confounders**: draft position, team scheme, snap count, opponent quality, position within scheme


## Important Caveats

- Correlation ≠ causation. All findings are associations.
- Sample sizes are small (~510 players). Effect sizes may be unstable.
- Tracking frames are NOT independent observations. The player is the unit of analysis.
- Confounders (team, scheme, snap count, opponent) are not yet controlled.
- First-season performance may not reflect long-term potential.