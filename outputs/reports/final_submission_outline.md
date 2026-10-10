# Final Submission Outline

**Title:** Beyond the Stopwatch: Measuring Route-Ready Movement
**Track:** NFL Big Data Bowl 2027
**Primary Focus:** Wide Receivers + Short Shuttle + NFL Separation

## 1. The Core Narrative
Traditional Combine testing measures straight-line speed via the 40-yard dash. However, NFL route-running relies on the ability to decelerate, change direction smoothly, and re-accelerate without losing momentum. This notebook investigates whether 10 Hz tracking data from the Short Shuttle can quantify "movement fluidity" (the rate of abrupt direction changes) and whether this metric predicts rookie NFL separation better than traditional stopwatch times.

## 2. Notebook Structure

### Introduction
- **Executive Summary:** Quick highlight of the key finding (`direction_change_rate` vs `mean_separation`, Spearman rho = -0.645) and the statistical robustness (Bootstrap 95% CI [-0.81, -0.34]).
- **The Football Question:** Explain the difference between straight-line speed and route-running efficiency.
- **The Dataset:** Combine tracking (pre-draft) predicting NFL outcomes (rookie season).

### The Feature
- **Why 10 Hz Tracking?**: Introduce tracking paths vs stopwatches.
- **Defining Direction Change**: Explain how `direction_change_rate` is calculated (circular differences, speed filters, 20-degree thresholds).
- **Distribution**: Histogram of the metric across WRs.

### The Analysis
- **Traditional Combine Relationship**: Show that `direction_change_rate` has low/moderate correlation with 40-yard dash and traditional Shuttle times, proving it measures a distinct athletic trait.
- **NFL Separation**: The main scatter plot showing the strong negative association between direction change rate (jerky movement) and NFL separation.
- **Statistical Robustness**:
  - Bootstrap resampling distribution.
  - Robust regression (HuberT) to down-weight outliers.
  - Multiple Testing caveat: Honest reporting of the FDR-adjusted p-value (~0.168) and the exploratory nature of the study.

### Context & Predictive Value
- **Does Tracking Add Information?**: Ridge regression comparing a model built solely on traditional metrics versus a model enhanced by our tracking feature.
- **Same Stopwatch, Different Athlete**: Visual proof that two receivers with identical 40-yard dash times can have vastly different movement fluidity scores and NFL outcomes.

### Conclusion
- **Limitations**: Acknowledging the small sample size (N=28), the observational nature of the data, and confounding variables in NFL separation (QB play, scheme).
- **Final Takeaway**: "The next step for NFL evaluation is not replacing the 40-yard dash—it is understanding what the stopwatch leaves out."
