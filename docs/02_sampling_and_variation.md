# Sampling and Variation

## Why does an AI engineer need to understand this?
AI engineers rarely evaluate every possible production case, so they live with samples. Understanding variation is what prevents false alarms when a metric moves after an apparently minor release.

## 1. Engineering Problem
Project Frog evaluates a new release on a sample of projects and accuracy drops by three points. The problem is deciding whether the sample captured a real regression or ordinary evaluation noise.

## 2. Intuition
Sampling variation is the natural wobble created by observing only part of a larger process. Even if true accuracy stays fixed, repeated evaluations produce slightly different observed metrics.

## 3. Mathematical Foundation
Cover populations, samples, random variation, and the law of large numbers. The crucial mathematical idea is that estimators vary, and their variability often shrinks with more informative data.

## 4. Python Example
Generate repeated synthetic samples from the same Project Frog process and visualize the distribution of observed accuracy. Show that the center stays near the true value while the spread depends on sample size.

## 5. Interpretation
Interpret each evaluation as one draw from a range of plausible draws. The engineering question shifts from 'what number did we get?' to 'how noisy is this number?'.

## 6. Common Mistakes
Mistakes include assuming one sample is representative by default, treating bigger datasets as automatically unbiased, and comparing metrics without checking whether sampling procedures matched.

## 7. AI Engineering Applications
Use sampling reasoning for offline test sets, human-annotation audits, canary rollouts, and incident reviews. It is foundational for later chapters on confidence intervals and power.


## 8. Trust Checkpoint
Before trusting an observed Project Frog metric in this setting, write down:
- the metric definition and unit of analysis
- the uncertainty estimate and how it was computed
- the population or slice the result is supposed to represent
- the assumptions required for the estimate to be interpretable
- the decision that would change if the result moved

## 9. Exercises
Design two synthetic Project Frog sampling plans and predict which one produces more stable latency estimates. Explain why stability alone does not guarantee representativeness.

## 10. Further Reading
Further reading should include applied discussions of estimator variance, sampling plans, and simulation-based intuition building.
