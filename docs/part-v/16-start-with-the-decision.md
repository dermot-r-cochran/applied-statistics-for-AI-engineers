# 16. Start with the Decision

A metric is useful only when it is tied to an action. Before collecting rows or computing intervals, define the decision the evidence must support.

Related artifacts: [Experiment protocol template](../artifacts/experiment-protocol-template.md), [Minimum meaningful effect statement](../artifacts/minimum-meaningful-effect-statement.md), and [Sample-size planning worksheet](../artifacts/sample-size-planning-worksheet.md).

## Decision-first design

Project Frog has to choose between three actions:

- ship the candidate model
- ship with caveats and extra review
- collect more evidence first

Those actions determine what effect size matters, which comparison is appropriate, and how much uncertainty is tolerable.

<svg viewBox="0 0 420 130" width="100%" role="img" aria-label="Decision-first experiment flow">
  <rect x="20" y="45" width="90" height="30" fill="#8dd3c7" />
  <rect x="135" y="45" width="90" height="30" fill="#ffffb3" />
  <rect x="250" y="45" width="90" height="30" fill="#bebada" />
  <rect x="350" y="45" width="50" height="30" fill="#fb8072" />
  <text x="35" y="64" font-size="12">decision</text>
  <text x="150" y="64" font-size="12">metric</text>
  <text x="260" y="64" font-size="12">design</text>
  <text x="358" y="64" font-size="12">act</text>
</svg>

## Worked Python example

```python
from trustworthy_ai_evaluation import required_sample_size

baseline_accuracy = 0.89
minimum_meaningful_effect = 0.03
n_per_group = required_sample_size(
    baseline_accuracy,
    minimum_meaningful_effect,
    power=0.8,
    alpha=0.05,
)
print(n_per_group)
```

This is not a magic answer. It is a design prompt: *Is a 3-point change the smallest effect that would alter the release decision?*

## What to define before the experiment starts

- the decision threshold
- the minimum meaningful effect
- the error trade-off between false approval and false rejection
- whether the comparison is [paired](../reference/glossary.md#paired-comparison) or independent
- the unit of inference
- the consequence of getting the answer wrong

## Assumptions

- Decision thresholds are explicit rather than implied after the fact.
- The primary metric is aligned with the operational decision.
- Consequences of error are discussed before seeing the result.

## Common incorrect interpretation

> We will run the benchmark and decide later what counts as meaningful.

## Corrected interpretation

> The benchmark design must be chosen around the decision. Otherwise significance, sample size, and even the metric itself are easy to manipulate after seeing the data.

## Decision-oriented conclusion

Write the release decision in plain language first. Then build the statistical plan backward from that action.

## Exercises

1. Define a minimum meaningful degradation for a safety-critical review queue.
2. Explain why a latency increase might matter even if accuracy improves.
3. Rewrite a vague evaluation goal as a concrete engineering decision.

## Summary

- Start with the decision, not the metric.
- Minimum meaningful effect belongs in the protocol before data collection.
- Error costs determine how much uncertainty is acceptable.
- A good design is an argument structure, not just a formula.
