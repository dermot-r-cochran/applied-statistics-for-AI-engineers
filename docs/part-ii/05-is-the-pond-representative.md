# 5. Is the Pond Representative?

A larger sample can still mislead if it is drawn from the wrong pond. This chapter separates [sample size](../reference/glossary.md#sampling-variance) from [sample representativeness](../reference/glossary.md#sampling-bias).

Related chapters: [The Shrinking Pond](04-the-shrinking-pond.md), [Test-Set Governance](07-test-set-governance.md), and [Fair Model Comparisons](../part-v/17-fair-model-comparisons.md).

## The Different Pond case study

Project Frog is evaluated on the same unchanged model in two benchmark cycles.

**Baseline composition**

- 70% Simple
- 20% Moderate
- 10% Complex

**Later composition**

- 40% Simple
- 30% Moderate
- 30% Complex

Suppose the stratum-level accuracies do not change:

- Simple: 95%
- Moderate: 86%
- Complex: 72%

Then the aggregate can still change because the mixture changed.

<svg viewBox="0 0 420 140" width="100%" role="img" aria-label="Difficulty composition shift">
  <rect x="20" y="30" width="210" height="24" fill="#66c2a5" />
  <rect x="230" y="30" width="60" height="24" fill="#fc8d62" />
  <rect x="290" y="30" width="30" height="24" fill="#8da0cb" />
  <rect x="20" y="80" width="120" height="24" fill="#66c2a5" />
  <rect x="140" y="80" width="90" height="24" fill="#fc8d62" />
  <rect x="230" y="80" width="90" height="24" fill="#8da0cb" />
  <text x="330" y="47" font-size="14">baseline mix</text>
  <text x="330" y="97" font-size="14">later mix</text>
</svg>

## Worked Python example

```python
baseline_mix = {"Simple": 0.70, "Moderate": 0.20, "Complex": 0.10}
later_mix = {"Simple": 0.40, "Moderate": 0.30, "Complex": 0.30}
stratum_accuracy = {"Simple": 0.95, "Moderate": 0.86, "Complex": 0.72}

baseline_accuracy = sum(baseline_mix[k] * stratum_accuracy[k] for k in baseline_mix)
later_accuracy = sum(later_mix[k] * stratum_accuracy[k] for k in later_mix)
print(round(baseline_accuracy, 3), round(later_accuracy, 3))
```

The aggregate drops from 0.913 to 0.865 even though every stratum stayed the same.

## What this teaches

- Aggregate metrics mix performance with composition.
- [Stratified reporting](../reference/glossary.md#stratified-reporting) is often more informative than one top-line number.
- Standardization and weighting can answer counterfactual questions such as: *What would later performance look like under the baseline composition?*

## What weighting can and cannot do

Weighting can help only when:

- the relevant strata are observed
- each stratum has support in both datasets
- the metric is estimable for those strata
- the weighting target is explicitly chosen

Weighting **cannot** repair:

- missing coverage for a subgroup never sampled
- label drift hidden inside a stratum
- unmeasured bias in the sample design

## Assumptions

- Difficulty labels are available and measured consistently.
- Strata are relevant to the decision.
- Within-stratum metric estimates are themselves credible.

## Common incorrect interpretation

> The later aggregate is lower, so the model must have become worse.

## Corrected interpretation

> The later aggregate may be lower because the benchmark contains a harder mix of cases. Without stratified reporting or standardization, aggregate change alone confounds difficulty composition with model performance.

## Decision-oriented conclusion

When the dataset mixture changes, report:

- stratum definitions
- stratum weights
- within-stratum results
- standardized or weighted totals and their assumptions

If a subgroup is missing, say so explicitly. Do not let weighting pretend coverage exists where it does not.

## Exercises

1. Change the Complex weight from 30% to 40% and recompute the later aggregate.
2. Identify one subgroup that should probably be stratified in your own evaluation context.
3. Explain why weighting is not a cure for unmeasured bias.

## Summary

- Sample size and representativeness are different properties.
- Aggregate metrics can change without any model change.
- Stratified reporting is the first defense against composition shift.
- Weighting requires overlap, measured strata, and explicit assumptions.
