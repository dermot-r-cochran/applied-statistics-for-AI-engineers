# Python API

The package lives at `trustworthy_ai_evaluation`.

## Resampling

### `bootstrap_metric`
Ordinary bootstrap for exchangeable rows. Use for unclustered samples when row-level resampling is defensible.

### `cluster_bootstrap_metric`
Cluster bootstrap for repeated observations within documents, projects, or other grouped units.

## Comparisons

### `compare_paired_predictions`
Paired accuracy comparison for the same examples. Returns an accuracy difference, paired-bootstrap interval, and paired permutation p-value.

### `compare_independent_proportions`
Independent two-sample comparison for Bernoulli outcomes. Returns a Newcombe-Wilson interval and pooled z-test p-value.

### `metric_comparability_check`
Documents whether two results are directly comparable, comparable with limitations, or not directly comparable.

## Planning

### `minimum_detectable_effect`
Approximate the smallest effect a balanced two-group study can detect under a normal approximation.

### `required_sample_size`
Approximate the balanced per-group sample size needed to detect a chosen minimum meaningful effect.

## Deliberate limits

These utilities intentionally do **not** automate:

- intraclass-correlation estimation for clustered designs
- equivalence and non-inferiority margin selection
- universal effective-sample-size conversion for hierarchical samples
- automatic repair of non-comparable evaluations

Those tasks require domain judgment that should stay explicit in the experiment record.
