export interface WRPlayer {
  nfl_id: number;
  direction_change_rate_SHORT_SHUTTLE: number;
  mean_separation: number;
  forty?: number | null;
  ten_yd_split?: number | null;
  short_shuttle?: number | null;
  three_cone?: number | null;
  vertical?: number | null;
  broad_jump?: number | null;
}

export interface TrajectoryPoint {
  x: number;
  y: number;
  s: number;
  dir: number;
}

export interface TrajectoryGroup {
  nfl_id: number;
  dcr: number;
  mean_separation: number | null;
  label: string;
  points: TrajectoryPoint[];
}

export interface TrajectoryData {
  low_dcr: TrajectoryGroup;
  high_dcr: TrajectoryGroup;
}

export interface BootstrapData {
  rhos: number[];
  ci_lower: number;
  ci_upper: number;
  observed_rho: number;
}

export interface SummaryData {
  n_wr: number;
  spearman_rho: number;
  raw_p: number;
  bh_adj_p: number;
  huber_p: number;
  ci_lower: number;
  ci_upper: number;
  n_hypotheses: number;
  ridge_traditional_r2: number;
  ridge_tracking_r2: number;
  ridge_combined_r2: number;
  dcr_vs_forty_rho: number;
  dcr_vs_split_rho: number;
  dcr_mean: number;
  dcr_std: number;
  dcr_min: number;
  dcr_max: number;
}

export interface CorrelationRow {
  position_group: string;
  combine_feature: string;
  nfl_outcome: string;
  rho: number;
  p_value: number;
  n: number;
}
