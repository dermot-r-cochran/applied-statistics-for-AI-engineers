# Glossary

## Cluster bootstrap
A bootstrap that resamples whole [clusters](#clustering) rather than individual rows so that within-cluster dependence is preserved.

## Clustering
A situation in which rows are grouped by a higher-level unit such as project, document, user, or session. Rows inside the same cluster are often correlated.

## Comparability
Whether two reported metrics can be interpreted as measuring the same thing under the same conditions. See [Fair Model Comparisons](../part-v/17-fair-model-comparisons.md).

## Confidence interval
A range produced by a stated procedure that quantifies uncertainty in an estimate under explicit assumptions.

## Design effect
An inflation factor that converts a nominal sample size into an approximate effective sample size when dependence increases variance.

## Effective sample size
A context-specific summary of how much information a dependent sample provides relative to an idealized independent sample. It is model-dependent, not universal.

## Exchangeable rows
Rows that can reasonably be treated as drawn from the same sampling mechanism for a specific uncertainty calculation.

## Experimental validity
The degree to which an evaluation design supports the decision claim being made.

## Hierarchical sampling
A sample structure with more than one level, such as projects containing documents containing extracted rows.

## Independent evidence
Information from units that can reasonably contribute separate evidence for the inference question. Many rows do not guarantee much independent evidence.

## Minimum detectable effect
The smallest effect a planned study is powered to detect with a chosen test, alpha, and power target.

## Minimum meaningful effect
The smallest effect that would change an engineering or product decision.

## Operating conditions
The scoring environment, pipeline settings, prompts, thresholds, latency constraints, and related conditions under which a model is evaluated.

## Paired comparison
A comparison in which the same evaluation units are scored by both systems, allowing within-unit differences to be analyzed directly.

## Practical significance
Whether an observed effect matters for a real decision. See [Effect Size Before Significance](../part-v/18-effect-size-before-significance.md).

## Production surveillance
Ongoing monitoring after deployment. It is not the same as a stable benchmark study because the population and operating context may drift.

## Sampling bias
Systematic mismatch between the [target population](#target-population) and the observed sample.

## Sampling variance
Random variation in an observed estimate caused by sampling only part of the target population.

## Stable benchmark evaluation
An evaluation design intended to hold dataset definition, labeling, scoring, and operating conditions fixed so that repeated comparisons remain interpretable.

## Stratified reporting
Reporting results separately for meaningful subgroups, such as difficulty strata or document types.

## Target population
The set of cases a metric is intended to describe.

## Test-set governance
The operational rules that define how an evaluation dataset is created, changed, reviewed, versioned, and retired.

## Unit of inference
The level about which you want to make a claim, such as document-level or project-level performance.

## Unit of observation
The row or event recorded in the dataset. This may be lower-level than the [unit of inference](#unit-of-inference).
## Abstention
A policy that withholds an automated decision and routes the case for review.

## Brier score
The mean squared error between predicted probabilities and binary outcomes.

## Calibration
Agreement between predicted probabilities and observed frequencies for a defined event and population.

## Calibration drift
A change in calibration behavior when the deployment population differs from the calibration population.

## Conditional dependence
A setting where component failures remain related even after accounting for observed covariates.

## Confidence semantics
The operational meaning attached to a score, including what event it targets and what assumptions it requires.

## End-to-end correctness
Whether the final system output is correct for the decision that matters.

## Expected calibration error
A binned summary of calibration gaps. It is useful but incomplete because it depends on the chosen bins and hides subgroup failures.

## Reliability diagram
A plot comparing mean predicted score with observed event frequency across bins.

## Selective prediction
Prediction with an option to abstain on cases judged too uncertain for automation.

## Subgroup calibration
Calibration evaluated separately for meaningful subpopulations instead of only in aggregate.
