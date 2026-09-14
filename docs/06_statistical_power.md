# Statistical Power

## Why does an AI engineer need to understand this?
Power tells engineers whether an evaluation was capable of detecting a meaningful change. Without it, a null result may simply mean the test was too weak to be informative.

## 1. Engineering Problem
A Project Frog release review finds no significant difference from the baseline. The problem is determining whether the study truly rules out important regressions or merely lacked enough examples.

## 2. Intuition
Power is the chance that an evaluation design detects a real effect of a chosen size. It depends on sample size, noise, significance threshold, and the effect you care about.

## 3. Mathematical Foundation
Introduce Type I and Type II errors, power curves, and minimum detectable effect. Show why 'no significance' is ambiguous unless the study had reasonable power.

## 4. Python Example
Use Python to compute power for several Project Frog sample sizes and visualize the minimum detectable effect against evaluation budget. Translate sample size into decision confidence rather than abstract coverage.

## 5. Interpretation
Interpret low power as weak evidence, not a reassuring outcome. A powerless study can fail to catch both important improvements and important regressions.

## 6. Common Mistakes
Mistakes include selecting sample size after seeing the result, defining effect size too vaguely, and ignoring clustered data that reduces effective sample size.

## 7. AI Engineering Applications
Use power analysis to plan offline evaluations, manual audits, A/B tests, and red-team studies. It helps teams spend evaluation budget where it changes decisions.

## 8. Exercises
Choose a target effect for Project Frog accuracy and estimate how many examples are needed for 80% power. Then explain how the answer changes if the unit of inference becomes project-level instead of document-level.

## 9. Further Reading
Further reading should include practical experiment design resources and applied power analysis references.
