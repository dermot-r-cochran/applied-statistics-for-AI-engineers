# Confidence-interval selection guide

This page summarizes interval choices referenced in [Chapter 4](../part-ii-samples-test-sets-and-generalization/04-the-shrinking-pond.md), [Chapter 13](../part-iv-confidence-across-ai-pipelines/13-calibration.md), and [Chapter 20](../part-v-experimental-design/20-bootstrap-permutation-and-simulation.md).

## Quick chooser

- **Wilson interval** — Good default for binomial proportions when you need a stable interval for accuracy-like quantities.
- **Exact binomial interval** — Useful when sample sizes are very small or edge cases are prominent.
- **Bootstrap interval** — Useful when the metric is complex or analytic formulas are awkward, provided the resampling unit matches the data structure.
- **Cluster bootstrap interval** — Prefer when dependence is induced by repeated observations within documents or projects.
- **Simulation-based interval** — Prefer when the decision depends on multiple uncertain quantities or operational scenarios.

## Questions before choosing

1. What is the estimand?
2. Are observations plausibly independent?
3. Is the sample very small or near 0%/100% outcomes?
4. Does the metric involve thresholds, ratios, or model-based aggregation?
5. Will readers understand the interval’s assumptions?

## Warning

Intervals do not repair biased samples, missing coverage, or incomparable evaluation conditions.
