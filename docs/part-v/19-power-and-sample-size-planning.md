# 19. Power and Sample-Size Planning

Sample-size planning is about decision risk, not formula memorization. It asks whether the planned study can reliably detect the smallest effect that would change what you do.

See also: [Minimum meaningful effect statement](../artifacts/minimum-meaningful-effect-statement.md) and [The Tadpole Problem](../part-ii/06-the-tadpole-problem.md).

## Terms to keep separate

- **Type I error**: acting as if a change exists when it does not
- **Type II error**: missing a real change that matters
- **power**: the probability of detecting a specified effect under the design
- **minimum detectable effect**: the smallest effect the planned study can usually detect

<svg viewBox="0 0 420 130" width="100%" role="img" aria-label="Power curve concept">
  <path d="M30 95 C120 95, 170 70, 220 50 S320 20, 390 20" stroke="#377eb8" stroke-width="4" fill="none" />
  <line x1="220" y1="20" x2="220" y2="100" stroke="#e41a1c" stroke-dasharray="6 4" />
  <text x="190" y="115" font-size="12">minimum detectable effect</text>
</svg>

## Worked Python example

```python
from trustworthy_ai_evaluation import minimum_detectable_effect, required_sample_size

mde = minimum_detectable_effect(0.89, 400, power=0.8, alpha=0.05)
required = required_sample_size(0.89, 0.03, power=0.8, alpha=0.05)
print(round(mde, 4), required)
```

These are planning approximations for balanced two-group proportion studies. They are useful when their assumptions are explicit.

## Cluster-aware planning

If the sample is clustered, a row-level plan is too optimistic. You need an externally justified design effect or a cluster-level simulation. This repository deliberately does **not** automate design-effect estimation because it depends on the sampling hierarchy and the inferential target.

## Engineering interpretation

Suppose a 1-point accuracy change would not alter release behavior, but a 3-point drop would. Then the planning target should be 3 points, not the smallest change the metric can mathematically detect.

## Assumptions

- Groups are balanced.
- The estimand is a difference in Bernoulli proportions.
- The normal approximation is adequate for planning.
- Cluster dependence is summarized externally, if used at all.

## Common incorrect interpretation

> Bigger sample sizes are always better.

## Corrected interpretation

> Bigger sample sizes reduce uncertainty, but the real planning question is whether the study can resolve the decision-relevant effect under the actual sampling design.

## Decision-oriented conclusion

Plan around the smallest effect worth acting on and the strongest plausible dependence structure. If that plan is too expensive, change the decision rule or the data strategy explicitly.

## Exercises

1. Recalculate the required sample size after doubling the design effect.
2. Explain why power targets should not be chosen after observing the result.
3. Identify one situation where an equivalence design would be preferable.

## Summary

- Power planning is decision planning.
- Minimum meaningful effect should precede minimum detectable effect.
- Cluster dependence can dominate nominal row count.
- Planning formulas are useful only within their stated assumptions.
