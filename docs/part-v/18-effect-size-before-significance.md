# 18. Effect Size Before Significance

A measurable effect is not automatically a meaningful effect. Significance asks whether an observed difference is surprising under a null model; practical significance asks whether the difference matters.

Related chapter: [Start with the Decision](16-start-with-the-decision.md).

## Project Frog example

Suppose a candidate model improves observed accuracy from 89.0% to 89.7%. On a huge dataset, this may be statistically significant. That does not mean the change is operationally worth shipping.

<svg viewBox="0 0 420 120" width="100%" role="img" aria-label="Small significant effect versus minimum meaningful effect">
  <line x1="30" y1="70" x2="390" y2="70" stroke="#555" stroke-width="2" />
  <line x1="190" y1="50" x2="190" y2="90" stroke="#d95f02" stroke-width="4" />
  <line x1="280" y1="45" x2="280" y2="95" stroke="#1b9e77" stroke-width="4" />
  <text x="160" y="35" font-size="12">observed +0.7 pt</text>
  <text x="245" y="35" font-size="12">meaningful +3 pt</text>
</svg>

## Worked Python example

```python
from trustworthy_ai_evaluation import compare_independent_proportions

comparison = compare_independent_proportions(897, 1000, 890, 1000)
print(round(comparison.difference, 4), comparison.confidence_interval)
```

The point estimate is measurable. The decision question is whether it clears the minimum meaningful effect stated in advance.

## What to compare against

Compare the observed effect to:

- the minimum meaningful effect
- uncertainty around the estimate
- decision thresholds
- trade-offs in latency, cost, or escalation burden

## Equivalence and non-inferiority

Sometimes the important question is not "Is the candidate better?" but:

- **equivalence**: is it close enough for the intended use?
- **non-inferiority**: is it no worse than an acceptable margin while improving something else?

These are decision concepts first and hypothesis-testing concepts second.

## Assumptions

- The effect size is stated on a scale relevant to the decision.
- The comparison design matches the data collection process.
- Operational costs are considered alongside the metric.

## Common incorrect interpretation

> The p-value is below 0.05, so the improvement matters.

## Corrected interpretation

> Statistical significance says little about whether the effect changes the decision. A tiny, precisely estimated change can still be operationally irrelevant.

## Decision-oriented conclusion

Ask "Would I act differently if the true effect were near the lower bound of the interval?" If the answer is no, significance alone should not move the roadmap.

## Exercises

1. Write a minimum meaningful effect for both accuracy and processing cost.
2. Give an example of a non-inferiority question for Project Frog.
3. Explain why effect-size thresholds should be set before looking at the result.

## Summary

- Significance and practical significance are different.
- A meaningful effect is defined by the decision, not by the p-value.
- Equivalence and non-inferiority can be more appropriate than superiority.
- Intervals matter because they show which practical effects remain plausible.
