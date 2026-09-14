# Metric-selection guide

Use this guide when choosing a primary metric for a decision. Start from [Chapter 16](../part-v-experimental-design/16-start-with-the-decision.md), then verify measurement scope with [Chapter 1](../part-i-what-are-we-measuring/01-the-metric-is-not-the-system.md).

## Selection steps

1. Name the operational decision.
2. Identify the error types that matter most.
3. Define the unit of inference and target population.
4. Choose a metric whose aggregation rule matches that decision.
5. Record blind spots and companion metrics.

## Common pairings

- **Overall routing stability** → accuracy plus subgroup breakdowns.
- **High-cost false positives** → precision-oriented metrics and review burden estimates.
- **High-cost misses** → recall-oriented metrics and escalation analysis.
- **Probability quality** → calibration plots, Brier score, and subgroup calibration checks.
- **Pipeline trust** → end-to-end outcome metrics, abstention coverage, and failure decomposition.

## Do not skip

- A [metric definition card](metric-definition-card.md)
- A [test-set manifest](test-set-manifest-template.md)
- A [minimum meaningful effect statement](minimum-meaningful-effect-statement.md)
