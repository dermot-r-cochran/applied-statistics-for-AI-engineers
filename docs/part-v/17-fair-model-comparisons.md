# 17. Fair Model Comparisons

A comparison is only fair when the underlying evaluation conditions are aligned. The first question is not "Which number is higher?" but "Are these numbers directly comparable?"

See the [Evaluation comparability checklist](../artifacts/evaluation-comparability-checklist.md) and [The Shrinking Pond](../part-ii/04-the-shrinking-pond.md).

## Required comparability fields

Document whether the comparison used:

- the same examples
- the same ground truth
- the same scoring code
- the same metric definitions
- the same thresholds
- the same preprocessing
- the same operating conditions

<svg viewBox="0 0 420 120" width="100%" role="img" aria-label="Comparability classification ladder">
  <rect x="20" y="40" width="110" height="28" fill="#4daf4a" />
  <rect x="155" y="40" width="120" height="28" fill="#ffcc33" />
  <rect x="300" y="40" width="100" height="28" fill="#e41a1c" />
  <text x="28" y="58" font-size="12">directly comparable</text>
  <text x="163" y="58" font-size="12">with limitations</text>
  <text x="308" y="58" font-size="12">not directly comparable</text>
</svg>

## Worked Python example

```python
from trustworthy_ai_evaluation import metric_comparability_check

result = metric_comparability_check(
    same_examples=True,
    same_ground_truth=True,
    same_scoring_code=True,
    same_metric_definitions=True,
    same_thresholds=False,
    same_preprocessing=True,
    same_operating_conditions=True,
    notes={"threshold_change": "candidate uses a stricter escalation threshold"},
)
print(result.classification)
print(result.limitations)
```

The correct result is **Comparable with limitations**, not **Directly comparable**.

## Classification rules

- **Directly comparable**: all seven comparability fields match.
- **Comparable with limitations**: the core metric meaning matches, but one or more thresholds, preprocessing steps, operating conditions, or documentation items differ.
- **Not directly comparable**: examples, ground truth, scoring code, or metric definitions differ enough that a direct numerical claim is unsafe.

## Paired versus independent comparisons

If both models are scored on the same examples, use a paired design whenever possible. Paired analysis removes a large amount of irrelevant example-to-example noise.

If the examples differ, you have an independent comparison question and must justify why the groups represent the same target population.

## Assumptions

- The documented fields reflect reality.
- Hidden pipeline changes are treated as operating-condition differences.
- Metric names alone do not guarantee identical metric definitions.

## Common incorrect interpretation

> Both reports say accuracy, so the higher number wins.

## Corrected interpretation

> Accuracy can mean different things under different thresholds, preprocessing rules, or datasets. Fair comparison requires explicit comparability evidence.

## Decision-oriented conclusion

Never report a numerical winner without a comparability classification beside it.

## Exercises

1. Identify a case where the same threshold still produces non-comparable results.
2. Rewrite a comparison summary so that its limitations are explicit.
3. Explain why a paired design is usually preferable when both systems can score the same cases.

## Summary

- Fair comparison is a design property, not a formatting choice.
- Comparability requires matching data, labels, scoring, definitions, thresholds, preprocessing, and conditions.
- Paired comparisons are often more informative than independent ones.
- Every comparison should receive a comparability classification.
