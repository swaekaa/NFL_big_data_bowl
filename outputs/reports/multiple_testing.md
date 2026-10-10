# Multiple Testing Analysis

Total hypotheses tested (feature/outcome pairs): 800

## Top Results (FDR Adjusted)

| position_group   | combine_feature                         | nfl_outcome         |       rho |     p_value |   p_adj_fdr |   n |
|:-----------------|:----------------------------------------|:--------------------|----------:|------------:|------------:|----:|
| WR               | direction_change_rate_SHORT_SHUTTLE     | mean_separation     | -0.64519  | 0.000209743 |    0.167795 |  28 |
| WR               | max_speed_FORTY_YARD_DASH               | yac_over_expected   | -0.338053 | 0.00127623  |    0.308008 |  88 |
| S                | mean_speed_THREE_CONE_DRILL             | n_tackles           | -0.871231 | 0.00102679  |    0.308008 |  10 |
| OL               | max_speed_FORTY_YARD_DASH               | sack_allowed_rate   |  0.322207 | 0.00154004  |    0.308008 |  94 |
| WR               | movement_efficiency_FORTY_YARD_DASH     | yac_over_expected   |  0.305819 | 0.00376057  |    0.429779 |  88 |
| OL               | movement_efficiency_FORTY_YARD_DASH     | sack_allowed_rate   | -0.298509 | 0.00347378  |    0.429779 |  94 |
| S                | max_speed_FORTY_YARD_DASH               | n_tackles           |  0.443084 | 0.00292403  |    0.429779 |  43 |
| S                | total_direction_change_SKILL_DRILLS_DB  | n_tackles           | -0.368079 | 0.00787336  |    0.47638  |  51 |
| Edge             | mean_speed_FORTY_YARD_DASH              | quick_pressure_rate |  0.367153 | 0.00945768  |    0.47638  |  49 |
| Edge             | movement_efficiency_FORTY_YARD_DASH     | mean_get_off        |  0.384082 | 0.00643926  |    0.47638  |  49 |
| TE               | mean_speed_SKILL_DRILLS_TE              | target_share        |  0.442969 | 0.00603888  |    0.47638  |  37 |
| WR               | first_step_acceleration_SKILL_DRILLS_WR | mean_yac            |  0.250605 | 0.0119095   |    0.47638  | 100 |
| OL               | mean_speed_FORTY_YARD_DASH              | sack_allowed_rate   |  0.268381 | 0.00891211  |    0.47638  |  94 |
| WR               | burst_impulse_0_5s_SKILL_DRILLS_WR      | mean_yac            |  0.250605 | 0.0119095   |    0.47638  | 100 |
| DT               | movement_efficiency_FORTY_YARD_DASH     | quick_pressure_rate | -0.404897 | 0.0105622   |    0.47638  |  39 |