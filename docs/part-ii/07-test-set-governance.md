# 7. Test-Set Governance

A benchmark is only as trustworthy as the rules that keep it stable. Governance turns a dataset from a pile of rows into an evaluation instrument.

Related resources: [Test-set manifest template](../artifacts/test-set-manifest-template.md), [Evaluation dataset review checklist](../artifacts/evaluation-dataset-review-checklist.md), and [Start with the Decision](../part-v/16-start-with-the-decision.md).

## Governance questions

- What is the target population?
- What is the unit of inference?
- Which changes create a new dataset version?
- Which changes break comparability with earlier runs?
- When must the dataset be refreshed or retired?

<svg viewBox="0 0 420 120" width="100%" role="img" aria-label="Governance workflow">
  <rect x="20" y="35" width="90" height="32" fill="#80b1d3" />
  <rect x="130" y="35" width="90" height="32" fill="#b3de69" />
  <rect x="240" y="35" width="90" height="32" fill="#fdb462" />
  <rect x="350" y="35" width="50" height="32" fill="#fb8072" />
  <text x="35" y="56" font-size="12">define</text>
  <text x="145" y="56" font-size="12">version</text>
  <text x="250" y="56" font-size="12">review</text>
  <text x="360" y="56" font-size="12">retire</text>
</svg>

## Worked Python example

```python
from trustworthy_ai_evaluation import metric_comparability_check

result = metric_comparability_check(
    same_examples=False,
    same_ground_truth=True,
    same_scoring_code=True,
    same_metric_definitions=True,
    same_thresholds=True,
    same_preprocessing=True,
    same_operating_conditions=True,
)
print(result.classification)
```

Changing the example set usually changes the benchmark identity. That does not make the later set useless, but it changes the safe claims you can make.

## What good governance records

- dataset version and creation date
- sampling frame and exclusions
- known clusters and dependence structure
- ground-truth process and reviewers
- scoring-code version and metric definitions
- change log with comparability impact

## Stable benchmark evaluation versus production surveillance

A stable benchmark is held fixed on purpose so that repeated experiments are comparable. Production surveillance is different:

- the case mix changes
- the environment changes
- the label process may lag or drift
- interventions may change user behavior

You need both, but they answer different questions.

## Assumptions

- Governance decisions are documented before the metric becomes politically important.
- Dataset changes are intentional and reviewable.
- Benchmark stability is preserved unless there is a declared reason to break it.

## Common incorrect interpretation

> More recent data automatically makes the benchmark better.

## Corrected interpretation

> More recent data may be better for production surveillance, but stable benchmark comparisons require version control and explicit comparability decisions.

## Decision-oriented conclusion

Treat benchmark updates like API changes: version them, review them, and document what claims remain valid afterward.

## Exercises

1. Draft a retirement rule for a benchmark whose target population drifts every quarter.
2. Identify one dataset change that should force a new major version.
3. Explain why stable benchmark evaluation and production surveillance should not share one summary number.

## Summary

- Governance makes evaluation datasets auditable.
- Dataset changes can invalidate trend claims.
- Stable benchmarks and production monitoring serve different goals.
- Versioning, manifests, and review checklists reduce avoidable confusion.
