# Sampling Bias

## Why does an AI engineer need to understand this?
Sampling bias can make an evaluation look precise while pointing at the wrong reality. AI engineers must recognize when the data collection process systematically distorts conclusions.

## 1. Engineering Problem
Project Frog metrics look strong because the evaluation mostly includes easy documents from responsive projects. The problem is that the sample may not reflect the cases where the system actually struggles.

## 2. Intuition
Bias is not random wobble; it is directional error introduced by how observations enter the sample. More biased data can make confidence intervals tighter without making conclusions truer.

## 3. Mathematical Foundation
Define selection bias, coverage bias, survivorship bias, and weighting adjustments. Stress that variance reduction does not repair systematic mismatch between the sample and the target population.

## 4. Python Example
Build a synthetic example where Project Frog is evaluated on an easy-heavy sample and compare the observed score with a reweighted score under a harder target mix. Use this to separate variance from bias.

## 5. Interpretation
Interpret biased results as limited to the sampled process unless correction assumptions are credible. Sampling fixes often require better collection, not just better formulas.

## 6. Common Mistakes
Common mistakes include treating random sampling within a biased frame as sufficient, ignoring missingness mechanisms, and assuming historical test sets stay representative.

## 7. AI Engineering Applications
Use sampling-bias reasoning for benchmark maintenance, annotation programs, feedback loops, and monitoring drift across customer-like segments in fictional examples.

## 8. Exercises
List three ways Project Frog could accidentally oversample easy cases and describe how each would distort the reported metrics.

## 9. Further Reading
Further reading should include survey sampling, dataset shift, and practical discussions of representativeness.
