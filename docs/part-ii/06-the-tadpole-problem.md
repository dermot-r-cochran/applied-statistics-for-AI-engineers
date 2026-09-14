# 6. The Tadpole Problem

Project Frog evaluates **1,000 rows**, but those rows came from only **20 documents** inside **6 projects**. Row count is not the same as [independent evidence](../reference/glossary.md#independent-evidence).

This chapter connects directly to [Bootstrap, Permutation, and Simulation](../part-v/20-bootstrap-permutation-and-simulation.md) and the glossary entries for [clustering](../reference/glossary.md#clustering) and [hierarchical sampling](../reference/glossary.md#hierarchical-sampling).

## Why the rows are not enough

If many rows come from the same document, they share context, prompting conditions, extraction quality, and labeling conventions. If many documents come from the same project, they may share even more.

<svg viewBox="0 0 420 150" width="100%" role="img" aria-label="Rows nested inside documents and projects">
  <circle cx="55" cy="45" r="18" fill="#8da0cb" />
  <circle cx="105" cy="45" r="18" fill="#8da0cb" />
  <circle cx="155" cy="45" r="18" fill="#8da0cb" />
  <rect x="25" y="80" width="160" height="40" fill="#ccebc5" stroke="#4daf4a" />
  <rect x="220" y="30" width="170" height="90" fill="#fdb462" stroke="#d95f02" />
  <text x="28" y="105" font-size="14">documents</text>
  <text x="240" y="80" font-size="14">projects containing documents</text>
</svg>

## Unit of observation versus unit of inference

The dataset stores rows. The release decision might depend on document-level or project-level reliability. Those are different inferential targets.

## Worked Python example

```python
from trustworthy_ai_evaluation import cluster_bootstrap_metric

rows = [1] * 870 + [0] * 130
# Synthetic document IDs: 50 rows per document for 20 documents
clusters = [f"doc-{i // 50:02d}" for i in range(1000)]

result = cluster_bootstrap_metric(rows, clusters, seed=19, n_resamples=2000)
print(result.estimate, result.confidence_interval)
```

This calculation treats the **document** as the inferential unit, estimates the average document-level accuracy, and respects document-level dependence by resampling whole documents instead of pretending that all 1,000 rows are independent.

## Project-level and document-level variation

In Project Frog, uncertainty can arise from at least two levels:

- **document-level variation**: some documents are easy, some are ambiguous
- **project-level variation**: some projects contain systematically harder language or structure

A cluster bootstrap can preserve one level at a time, but the choice of cluster must match the decision question.

## Why there is no universal effective-sample-size formula

People often ask for a single conversion like "1,000 rows equals 180 independent examples." That is too simple.

Effective sample size depends on:

- the metric
- the level of dependence
- the sampling design
- the level of inference
- the heterogeneity across clusters

A project-level claim and a document-level claim can produce different effective sample sizes from the same raw rows.

## Assumptions

- The chosen cluster level matches the inferential question.
- Resampled clusters are representative of the population of clusters.
- Empty or missing clusters are handled explicitly rather than silently ignored.

## Common incorrect interpretation

> We evaluated 1,000 rows, so our uncertainty is tiny.

## Corrected interpretation

> We evaluated 1,000 observations, but they are nested within only 20 documents and 6 projects. The independent evidence may be much smaller than the row count suggests.

## Decision-oriented conclusion

Document the hierarchy before reporting precision. If the decision is project-level, row-level standard errors are usually too optimistic.

## Exercises

1. Re-run the example with project IDs instead of document IDs.
2. Describe a case where document-level resampling would still be too optimistic.
3. Explain why repeated observations from one source should not automatically count as new evidence.

## Summary

- Row count is not equivalent to independent evidence.
- Clustering and repeated observations create dependence.
- The resampling unit must match the inference unit.
- No universal effective-sample-size shortcut is appropriate for hierarchical samples.
