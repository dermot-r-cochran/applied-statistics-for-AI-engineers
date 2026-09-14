# 20. Bootstrap, Permutation, and Simulation

Resampling methods are useful because AI evaluations rarely fit one textbook template. They are also easy to misuse. The resampling unit must match the design.

Related chapters: [The Tadpole Problem](../part-ii/06-the-tadpole-problem.md) and [Fair Model Comparisons](17-fair-model-comparisons.md).

## Which method answers which question?

- **Ordinary bootstrap**: row-level uncertainty when rows are exchangeable.
- **Paired bootstrap**: paired comparisons on the same examples.
- **Cluster bootstrap**: uncertainty when dependence exists inside documents, projects, or similar groups.
- **Permutation testing**: null testing when labels or paired system assignments are exchangeable under the null.
- **Simulation**: design exploration when analytic formulas are fragile or incomplete.

<svg viewBox="0 0 420 140" width="100%" role="img" aria-label="Resampling method chooser">
  <rect x="20" y="30" width="110" height="30" fill="#80b1d3" />
  <rect x="155" y="30" width="110" height="30" fill="#b3de69" />
  <rect x="290" y="30" width="110" height="30" fill="#fdb462" />
  <text x="30" y="50" font-size="12">exchangeable rows</text>
  <text x="165" y="50" font-size="12">paired examples</text>
  <text x="300" y="50" font-size="12">clustered samples</text>
</svg>

## Worked Python example

```python
from trustworthy_ai_evaluation import (
    bootstrap_metric,
    cluster_bootstrap_metric,
    compare_paired_predictions,
)

rows = [1, 1, 0, 1, 1, 0, 1, 1]
clusters = ["doc-1", "doc-1", "doc-1", "doc-2", "doc-2", "doc-3", "doc-3", "doc-3"]

ordinary = bootstrap_metric(rows, seed=3, n_resamples=1000)
clustered = cluster_bootstrap_metric(rows, clusters, seed=3, n_resamples=1000)
paired = compare_paired_predictions(
    [1, 0, 1, 1],
    [1, 0, 1, 0],
    [1, 1, 1, 0],
    seed=3,
    n_permutations=500,
)

print(ordinary.confidence_interval)
print(clustered.confidence_interval)
print(paired.difference, paired.p_value)
```

The ordinary and cluster bootstrap intervals can differ materially because they answer different uncertainty questions.

## Common invalid approaches

Do **not**:

- resample rows independently when the real dependence is document-level or project-level
- permute labels across non-exchangeable groups
- treat a bootstrap interval as valid after changing the scoring threshold without updating the metric definition
- use one universal resampling recipe for every evaluation design

## Simulation as a design tool

Simulation is especially valuable when:

- the benchmark is hierarchical
- the release rule uses multiple metrics
- abstention or human review changes the loss function
- the analytic planning formula hides too many assumptions

## Assumptions

- The resampling scheme matches the sampling scheme.
- Exchangeability is justified for the chosen unit.
- Synthetic simulations are tied to a stated decision question.

## Common incorrect interpretation

> The bootstrap is nonparametric, so it is automatically safe.

## Corrected interpretation

> The bootstrap only inherits credibility from the sample design and the resampling unit. Wrong unit, wrong answer.

## Decision-oriented conclusion

Choose the method that preserves the structure relevant to the decision claim. When that structure is unclear, treat the uncertainty result as fragile until the design is clarified.

## Exercises

1. Explain why a paired bootstrap is inappropriate for independently sampled model runs.
2. Describe one invalid permutation scheme for clustered data.
3. Sketch a simulation plan for a document-level abstention policy.

## Summary

- Different resampling methods serve different designs.
- Cluster-aware resampling matters when repeated observations exist.
- Permutation tests require exchangeability under the null.
- Simulation helps when the design is too rich for one closed-form formula.
