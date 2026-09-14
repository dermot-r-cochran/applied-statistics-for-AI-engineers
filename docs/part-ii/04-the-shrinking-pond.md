# 4. The Shrinking Pond

Project Frog reports **88% accuracy on 1,200 rows** in one benchmark cycle and **84% accuracy on 75 rows** in a later cycle. The small sample is worrying, but it does **not** prove the system regressed.

See also: [Is the Pond Representative?](05-is-the-pond-representative.md), [Fair Model Comparisons](../part-v/17-fair-model-comparisons.md), and the [sampling variance](../reference/glossary.md#sampling-variance) glossary entry.

## What changed?

Two things changed at once:

1. the observed point estimate dropped from 88% to 84%
2. the later estimate was based on a much smaller sample

The first change raises a product question. The second change raises an uncertainty question. They are not the same question.

<svg viewBox="0 0 420 120" width="100%" role="img" aria-label="Two benchmark samples with different widths">
  <rect x="20" y="30" width="260" height="24" fill="#4f83cc" />
  <rect x="20" y="72" width="60" height="24" fill="#d95f02" />
  <text x="290" y="47" font-size="14">1,200 rows, 88%</text>
  <text x="90" y="89" font-size="14">75 rows, 84%</text>
</svg>

## Population versus sample

The [target population](../reference/glossary.md#target-population) is the full set of future Project Frog cases we care about. The benchmark sample is only a partial view. A smaller pond gives a noisier reflection.

## Worked Python example

```python
from math import sqrt
from trustworthy_ai_evaluation import bootstrap_metric

baseline = [1] * 1056 + [0] * 144  # 88% of 1,200
later = [1] * 63 + [0] * 12        # 84% of 75

baseline_se = sqrt(0.88 * 0.12 / 1200)
later_se = sqrt(0.84 * 0.16 / 75)

baseline_boot = bootstrap_metric(baseline, seed=7, n_resamples=2000)
later_boot = bootstrap_metric(later, seed=7, n_resamples=2000)

print(round(baseline_se, 4), baseline_boot.confidence_interval)
print(round(later_se, 4), later_boot.confidence_interval)
```

The later estimate has a much larger standard error and a much wider interval. That is the main lesson.

## Wilson, exact, and bootstrap intervals

For binary outcomes, three interval families often appear together:

- **Wilson intervals** behave well for many practical sample sizes.
- **Exact binomial intervals** protect coverage conservatively, especially with very small samples.
- **Bootstrap intervals** are flexible but only when row-level resampling is defensible.

When all three tell a similar story, confidence in the qualitative conclusion improves. When they disagree, the sample is usually telling you that it is fragile.

## Assumptions

- Rows are treated as independent for this chapter's simple illustration.
- The later sample is assumed to target the same population as the baseline sample.
- Scoring rules are assumed unchanged.

Those assumptions are exactly what [Chapter 5](05-is-the-pond-representative.md) and [Chapter 17](../part-v/17-fair-model-comparisons.md) force you to check.

## Common incorrect interpretation

> Accuracy fell from 88% to 84%, so the model definitely regressed.

## Corrected interpretation

> The observed estimate fell, but the later sample is much smaller and therefore much noisier. A true regression is possible, but the result alone does not identify regression without more evidence about uncertainty and comparability.

## Decision-oriented conclusion

Do not escalate directly from a point-estimate drop to a causal claim. First ask:

- Was the later sample drawn from the same population?
- Was the evaluation directly comparable?
- How wide is the uncertainty interval?
- Would the decision change even if the lower bound were true?

## Exercises

1. Recompute the later interval after increasing the sample from 75 to 300 with the same 84% observed rate.
2. Compare Wilson and bootstrap intervals for 63/75 correct.
3. List three reasons an 84% observation might appear without any model change.

## Summary

- Sample size affects uncertainty, not truth.
- Smaller samples increase sampling variability.
- A lower observed metric on a smaller sample does not automatically imply a lower true metric.
- Comparability and representativeness must be checked before claiming regression.
