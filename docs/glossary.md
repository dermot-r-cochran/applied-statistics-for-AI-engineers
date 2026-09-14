# Glossary

## Accuracy

The share of evaluated predictions that exactly match the reference label. See [Accuracy and Its Discontents](chapters/accuracy-and-its-discontents.md).

## Calibration

The alignment between stated confidence and observed frequency, within a defined population and decision setting. See [What Does Confidence Mean?](chapters/what-does-confidence-mean.md).

## Comparability

The degree to which two evaluation results can be interpreted on the same footing because they used the same examples, labels, scoring rules, thresholds, preprocessing, and operating conditions. See [Start with the Decision](chapters/start-with-the-decision.md) and the [evaluation comparability checklist](reference/evaluation-comparability-checklist.md).

## Confidence interval

A range produced by a statistical procedure to summarize sampling uncertainty around an estimate. See [The Shrinking Pond](chapters/the-shrinking-pond.md).

## Decision threshold

A rule that maps evidence to an action, such as release, release with caveats, or collect more data. See [Start with the Decision](chapters/start-with-the-decision.md).

## End-to-end outcome

The final system-level result that matters for a real decision, not just an intermediate component score. See [The Metric Is Not the System](chapters/the-metric-is-not-the-system.md) and [Combining Confidence Scores](chapters/combining-confidence-scores.md).

## Expected calibration error

A binned summary of how far average predicted confidence differs from observed frequency. It is useful but incomplete because it depends on the binning design and can hide subgroup failures. See [What Does Confidence Mean?](chapters/what-does-confidence-mean.md).

## Evidence insufficiency

A state in which the available evidence is too weak, too imprecise, or too mismatched to justify a strong operational claim. See [Release Readiness Under Uncertainty](chapters/release-readiness-under-uncertainty.md).

## Population

The broader set of cases about which we want to make a claim. A dataset is not the population; it is only a sample from it or a proxy for it. See [The Shrinking Pond](chapters/the-shrinking-pond.md).

## Risk appetite

The amount and type of decision risk an organization is willing to tolerate given the consequences of being wrong. See [Release Readiness Under Uncertainty](chapters/release-readiness-under-uncertainty.md).

## Sampling uncertainty

Variation in observed results caused by which cases happened to appear in the sample. See [The Shrinking Pond](chapters/the-shrinking-pond.md).

## Synthetic data

Artificially generated data created for analysis, testing, or teaching. All Project Frog data in this repository are synthetic and fictional. See [Project Frog synthetic data](reference/project-frog-data.md).
