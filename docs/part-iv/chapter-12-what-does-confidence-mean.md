# 12. What Does Confidence Mean?

**Synthetic note:** every Project Frog example in this chapter is fictional and generated for teaching.

A confidence score is useful only after you answer two questions:

1. **Confidence in what?**
2. **For which population and decision?**

Project Frog has four scores in `[0, 1]`, but they mean different things.

| Component | Example score | Meaning |
| --- | --- | --- |
| Document extraction | `0.90` | Heuristic extraction quality index |
| Classification | `0.90` | Claimed probability the predicted class is correct |
| Evidence retrieval | `0.90` | Ranking margin for retrieved evidence |
| Explanation generation | `0.90` | Self-check score for explanation quality |

The shared numeric range is real. The shared meaning is not.

See the reusable [confidence semantics card](../reference/confidence-semantics-card.md).

## Worked Python example

```python
from trustworthy_ai_evaluation import metric_comparability_check

report = metric_comparability_check(
    metric_name="confidence",
    producing_component_a="classification",
    producing_component_b="evidence retrieval",
    intended_meaning_a="Estimated probability the predicted class is correct.",
    intended_meaning_b="Ranking margin for the top evidence chunk.",
    mathematical_range_a=(0.0, 1.0),
    mathematical_range_b=(0.0, 1.0),
    claims_probability_a=True,
    claims_probability_b=False,
)
print(report.verdict)
```

Expected result: `not directly comparable`.

## Core assumptions

- Each score targets a different event or signal.
- The decision target is not automatically the same as the score target.
- Shared scale alone does not justify averaging or multiplication.

## Common incorrect interpretation

> “All four scores are on a 0-to-1 scale, so averaging them gives overall confidence.”

## Corrected interpretation

Averaging is meaningful only after establishing semantic compatibility and validating the aggregate against an end-to-end outcome.

## Decision-oriented conclusion

Before using a score operationally, write its semantics card and decide whether the score supports a **component decision**, an **escalation decision**, or an **end-to-end release decision**.

## Exercises

1. Which Project Frog score most naturally supports a re-scan decision?
2. Which score most naturally supports a retrieval broadening decision?
3. Which fields in the semantics card most directly block score averaging?

## Summary

Confidence is not a number first. It is a claim first. The number matters only after the claim is defined.
