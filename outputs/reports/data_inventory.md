# NFL Big Data Bowl 2027 — Data Inventory

*Generated: 2026-10-08 20:20*

## File Sizes
| File | Status | Size |
|------|--------|------|
| players | ✓ Found | 0.0 MB |
| combine_results | ✓ Found | 0.0 MB |
| combine_tracking | ✓ Found | 79.9 MB |
| player_career_successes | ✓ Found | 0.0 MB |
| player_play | ✓ Found | 140.1 MB |
| games | ✓ Found | 0.0 MB |
| game_tracking_2023 | ✓ Found | 319.9 MB |
| game_tracking_2024 | ✓ Found | 684.7 MB |
| game_tracking_2025 | ✓ Found | 975.2 MB |

## players

- **Rows**: 510
- **Columns**: 10
- **Memory**: 0.1 MB
- **Unique players**: 510

**Missing values:**
| Column | Missing | Pct |
|--------|---------|-----|
| draft_round | 127 | 24.9% |
| draft_pick_within_round | 127 | 24.9% |
| draft_overall_pick | 127 | 24.9% |

**Columns and dtypes:**
| Column | Dtype |
|--------|-------|
| nfl_id | int64 |
| display_name | str |
| draft_year | int64 |
| nfl_position | str |
| birth_date | str |
| college_name | str |
| college_conference | str |
| draft_round | float64 |
| draft_pick_within_round | float64 |
| draft_overall_pick | float64 |

## combine_results

- **Rows**: 510
- **Columns**: 11
- **Memory**: 0.0 MB
- **Unique players**: 510

**Missing values:**
| Column | Missing | Pct |
|--------|---------|-----|
| ten_yd_split | 85 | 16.7% |
| forty | 86 | 16.9% |
| vertical | 72 | 14.1% |
| broad_jump | 87 | 17.1% |
| three_cone | 330 | 64.7% |
| short_shuttle | 309 | 60.6% |
| bench_reps | 318 | 62.4% |
| ngs_college_production_score | 1 | 0.2% |
| ngs_final_score | 1 | 0.2% |

**Columns and dtypes:**
| Column | Dtype |
|--------|-------|
| nfl_id | int64 |
| ten_yd_split | float64 |
| forty | float64 |
| vertical | float64 |
| broad_jump | float64 |
| three_cone | float64 |
| short_shuttle | float64 |
| bench_reps | float64 |
| ngs_athleticism_score | int64 |
| ngs_college_production_score | float64 |
| ngs_final_score | float64 |

## combine_tracking

- **Rows**: 463,189
- **Columns**: 12
- **Memory**: 69.0 MB
- **Unique players**: 510
- **Unique drill types**: 9

**No missing values.**

**Columns and dtypes:**
| Column | Dtype |
|--------|-------|
| event_id | str |
| nfl_id | int64 |
| time | str |
| drill_type | str |
| drill_name | str |
| attempt | Int16 |
| x | float32 |
| y | float32 |
| s | float32 |
| a | float32 |
| dis | float32 |
| dir | float32 |

## player_play

- **Rows**: 314,197
- **Columns**: 19
- **Memory**: 65.5 MB
- **Unique players**: 497
- **Unique games**: 1,001

**Missing values:**
| Column | Missing | Pct |
|--------|---------|-----|
| rec_yards | 307,937 | 98.0% |
| yards_after_catch | 307,937 | 98.0% |
| route_ran | 260,889 | 83.0% |
| separation_at_pass_forward | 267,460 | 85.1% |
| cushion | 210,445 | 67.0% |
| expected_yards_after_catch | 305,221 | 97.1% |
| pressure_allowed | 253,394 | 80.6% |
| sack_allowed | 253,394 | 80.6% |
| time_to_pressure_allowed | 309,227 | 98.4% |
| quick_pressure | 310,434 | 98.8% |
| player_get_off | 270,195 | 86.0% |
| sack | 227,362 | 72.4% |
| tackle | 302,301 | 96.2% |
| tackle_for_loss | 302,301 | 96.2% |
| time_to_pressure | 310,393 | 98.8% |

**Columns and dtypes:**
| Column | Dtype |
|--------|-------|
| game_id | int64 |
| play_id | int64 |
| nfl_id | int64 |
| target | bool |
| rec_yards | float64 |
| yards_after_catch | float64 |
| route_ran | str |
| separation_at_pass_forward | float64 |
| cushion | float64 |
| expected_yards_after_catch | float64 |
| pressure_allowed | object |
| sack_allowed | float64 |
| time_to_pressure_allowed | float64 |
| quick_pressure | object |
| player_get_off | float64 |
| sack | float64 |
| tackle | float64 |
| tackle_for_loss | object |
| time_to_pressure | float64 |

## career_successes

- **Rows**: 510
- **Columns**: 9
- **Memory**: 0.0 MB
- **Unique players**: 510

**No missing values.**

**Columns and dtypes:**
| Column | Dtype |
|--------|-------|
| nfl_id | int64 |
| career_offensive_snaps | int64 |
| career_defensive_snaps | int64 |
| career_special_teams_snaps | int64 |
| career_games_active | int64 |
| career_games_started | int64 |
| ap_all_pro_1st_team | int64 |
| ap_all_pro_2nd_team | int64 |
| pro_bowl_original_ballot | int64 |

## games

- **Rows**: 1,002
- **Columns**: 7
- **Memory**: 0.1 MB
- **Unique games**: 1,002

**No missing values.**

**Columns and dtypes:**
| Column | Dtype |
|--------|-------|
| game_id | int64 |
| game_key | int64 |
| season | int64 |
| season_type | str |
| week | int64 |
| home_team_abbr | str |
| visitor_team_abbr | str |

## Join Validation
- Master player table: **510** players
- Players with ALL datasets: **497**
- combine_results: **510** players (510 in master)
- combine_tracking: **510** players (510 in master)
- player_play: **497** players (497 in master)
- career_successes: **510** players (510 in master)