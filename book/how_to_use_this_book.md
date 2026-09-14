# How to use this book

## Who this book assumes you are

This book assumes you can already write Python, understand common machine learning workflows, and interpret familiar metrics such as accuracy, precision, recall, F1, latency, and cost. It does not assume that your statistical memory is fresh.

The intended reader is often the person asked to answer questions like these:

- Did the model actually regress?
- Is this A/B result actionable?
- Is the test set representative?
- Are these two offline evaluations comparable?
- Is the target met strongly enough to release?
- What should we tell leadership about uncertainty?

## What this book optimizes for

This is not a general statistics text. It is an engineering decision book.

That means each chapter emphasizes:

1. the decision at stake
2. the assumptions required
3. the operational meaning of the calculation
4. the failure modes that make a metric misleading
5. the communication required for a trustworthy conclusion

## Recommended reading strategies

### If you are diagnosing a metric change
Read the decision framework first, then confidence intervals, metric uncertainty, model comparison, and the Shrinking Pond and Frog Leap case studies.

### If you are designing an evaluation
Focus on sampling and variation, experimental design, test set design, sampling bias, data leakage, and the Different Pond and Tadpole Problem case studies.

### If you are making a release decision
Read confidence intervals, effect size, power, decision theory, and Release Readiness.

### If you prefer executable material
Start with the confidence interval notebook, the synthetic examples, and the package functions in `src/applied_stats_ai/`.

## How to get the most value from it

Do not stop at the formulas. For each chapter, ask:

- What population does this result describe?
- What assumptions are silently required?
- What would make this comparison invalid?
- What uncertainty is still unresolved?
- What action would change if the estimate moved within its plausible range?
