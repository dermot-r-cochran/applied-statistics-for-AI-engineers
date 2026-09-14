# Hypothesis Testing

## Why does an AI engineer need to understand this?
Hypothesis tests help engineers avoid mistaking random fluctuation for a real product change. They are useful when a release decision depends on whether an observed difference is larger than expected noise.

## 1. Engineering Problem
Project Frog version B scores higher than version A on a shared evaluation set. The engineering problem is whether the observed lift is strong enough to challenge the 'no real difference' explanation.

## 2. Intuition
Hypothesis testing is easier to understand as a structured stress test of a null explanation. Ask: if there were no true improvement, how surprising would this result be?

## 3. Mathematical Foundation
Define null and alternative hypotheses, test statistics, p-values, and paired versus unpaired comparisons. Emphasize that the model and sampling design matter as much as the resulting p-value.

## 4. Python Example
Show a model comparison with paired synthetic predictions, compute discordant outcomes, and estimate a McNemar p-value. Pair the test with a confidence interval for the observed difference.

## 5. Interpretation
Interpret the p-value as evidence against one reference explanation, not as the probability that the new release is good. Low p-values can coexist with trivial improvements and high operational cost.

## 6. Common Mistakes
Common mistakes include equating non-significant with no effect, ignoring multiple comparisons, and forgetting that dependence between observations can invalidate the test.

## 7. AI Engineering Applications
Use testing for model comparison, rollback analysis, experiment readouts, and audit sampling. In all cases, tie statistical evidence back to product impact.

## 8. Exercises
Write a null and alternative hypothesis for a Project Frog comparison where the new release increases recall but may reduce precision. Explain which test design assumptions matter most.

## 9. Further Reading
Further reading should include practical texts on test interpretation and resources comparing p-values with estimation-based workflows.
