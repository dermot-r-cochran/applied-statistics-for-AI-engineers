# Bootstrap Methods

## Why does an AI engineer need to understand this?
Bootstrap methods let engineers estimate uncertainty even when analytic formulas are awkward or when they need interval estimates for custom metrics. They are especially useful for metrics built from complex evaluation pipelines.

## 1. Engineering Problem
Project Frog tracks agreement rate and evidence quality summaries that are hard to analyze with a single closed-form variance formula. The problem is estimating uncertainty without pretending the metric is simpler than it is.

## 2. Intuition
The bootstrap resamples observed data to approximate how an estimator would vary across repeated samples. It is a computational method for learning about uncertainty from the data you have.

## 3. Mathematical Foundation
Explain resampling with replacement, percentile intervals, and when bootstrap assumptions can fail. Stress that the bootstrap still depends on the sample being informative about the population.

## 4. Python Example
Resample synthetic Project Frog evaluations, compute bootstrap distributions for accuracy and F1, and compare them with analytic intervals. Visualize skewness and interval width on small and large samples.

## 5. Interpretation
Interpret the bootstrap as an approximation to the estimator's sampling distribution, not as evidence that resampled points are new information. It helps quantify instability in the estimate.

## 6. Common Mistakes
Common mistakes include bootstrapping dependent data as if it were independent, using too few resamples for stable quantiles, and ignoring severe class imbalance.

## 7. AI Engineering Applications
Use bootstrap methods for custom risk metrics, stratified dashboards, and uncertainty summaries that combine several model outputs. They are often the fastest path from raw evaluation records to practical intervals.


## 8. Trust Checkpoint
Before trusting an observed Project Frog metric in this setting, write down:
- the metric definition and unit of analysis
- the uncertainty estimate and how it was computed
- the population or slice the result is supposed to represent
- the assumptions required for the estimate to be interpretable
- the decision that would change if the result moved

## 9. Exercises
Bootstrap a Project Frog metric that averages accuracy and evidence quality, then explain which assumptions must hold for the interval to be trustworthy.

## 10. Further Reading
Further reading should include applied bootstrap tutorials and warnings about dependence and resampling design.
