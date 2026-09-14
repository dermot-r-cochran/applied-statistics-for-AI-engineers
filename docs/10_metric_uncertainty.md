# Metric Uncertainty

## Why does an AI engineer need to understand this?
Observed metrics can look stable even when uncertainty is large, especially on rare classes or small slices. Engineers need uncertainty estimates to avoid overreacting to noisy segment-level dashboards.

## 1. Engineering Problem
Project Frog shows precision by project type and one slice appears to regress sharply. The problem is deciding whether the slice metric is informative enough to support action.

## 2. Intuition
Uncertainty depends on both sample size and metric structure. A narrow overall interval can coexist with a wide interval on a rare but important subgroup.

## 3. Mathematical Foundation
Explain uncertainty for derived metrics, uncertainty propagation, and why class prevalence affects precision and recall stability. Tie these ideas back to bootstrap and proportion intervals.

## 4. Python Example
Estimate uncertainty for confusion-matrix-derived metrics on synthetic Project Frog slices. Use bootstrap intervals to compare stability across common and rare categories.

## 5. Interpretation
Interpret unstable slice metrics as prompts for additional evidence, not immediate grounds for rollback. Precision without uncertainty is incomplete reporting.

## 6. Common Mistakes
Common mistakes include ranking models by tiny metric differences, ignoring subgroup sample size, and comparing slice metrics drawn from different case mixes.

## 7. AI Engineering Applications
Use metric uncertainty for dashboards, incident triage, fairness-style slice reviews, and prioritizing new data collection.

## 8. Exercises
Pick two Project Frog slices with the same point precision but different support counts. Explain which one should drive stakeholder concern and why.

## 9. Further Reading
Further reading should include uncertainty estimation for classification metrics and resampling-based interval methods.
