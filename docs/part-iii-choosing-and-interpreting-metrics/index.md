# Part III: Choosing and Interpreting Metrics

Metrics become trustworthy only when their error trade-offs, aggregation rules, and semantic limits are made explicit.

## What this part does

This part establishes the main questions, failure modes, and decision responsibilities for the chapters that follow.

## Chapters in this part

- [8. Accuracy and Its Discontents](08-accuracy-and-its-discontents.md) — Accuracy is easy to compute and easy to misunderstand because it hides class imbalance, asymmetric harms, and decision thresholds.
- [9. Precision, Recall, and the Cost of Being Wrong](09-precision-recall-and-the-cost-of-being-wrong.md) — Precision and recall surface different operational risks, so selecting or tuning between them is fundamentally a decision problem.
- [10. Aggregation Can Hide the Story](10-aggregation-can-hide-the-story.md) — Averages can conceal subgroup failures, unstable components, and distribution shifts that matter more than the overall trend.
- [11. Similarity Is Not Correctness](11-similarity-is-not-correctness.md) — Similarity metrics often track surface closeness rather than task success, so they must not be mistaken for validated correctness or usefulness.

## Throughline

Project Frog reappears across these chapters so ideas connect through one synthetic workflow rather than isolated examples.
