# Effect Size

## Why does an AI engineer need to understand this?
AI engineers need effect size because statistically detectable changes can still be operationally irrelevant. Deployment decisions should care about magnitude, not only detectability.

## 1. Engineering Problem
Project Frog improves from 84% to 86% accuracy and the team wants to know whether two points matter. The problem is separating a real but tiny lift from a change that justifies operational disruption.

## 2. Intuition
Effect size turns 'is there a difference?' into 'how large is the difference and how should we value it?'. It keeps decisions anchored to engineering goals such as manual review load or error costs.

## 3. Mathematical Foundation
Introduce absolute lift, relative lift, risk difference, odds ratios, and standardized effects where appropriate. Emphasize choosing an effect measure that matches the product question.

## 4. Python Example
Compute absolute accuracy lift, relative error reduction, and the downstream effect on expected incorrect decisions per thousand Project Frog documents. Compare those summaries to raw percentage-point changes.

## 5. Interpretation
Interpret the effect in business and operational terms: hours saved, reviews avoided, or risk reduced. A small effect may still matter if the cost of each error is high.

## 6. Common Mistakes
Mistakes include reporting only percent change without the baseline, cherry-picking whichever effect measure looks biggest, and ignoring uncertainty around the effect estimate.

## 7. AI Engineering Applications
Effect size matters in release gates, ranking model candidates, and setting minimum practical improvements for experimentation. It is the missing link between metric math and operational value.


## 8. Trust Checkpoint
Before trusting an observed Project Frog metric in this setting, write down:
- the metric definition and unit of analysis
- the uncertainty estimate and how it was computed
- the population or slice the result is supposed to represent
- the assumptions required for the estimate to be interpretable
- the decision that would change if the result moved

## 9. Exercises
Define a minimum meaningful effect for evidence quality and justify it from a synthetic stakeholder perspective. Then explain how the answer would change if latency costs doubled.

## 10. Further Reading
Further reading should cover practical significance, equivalence thinking, and interpretable effect measures for proportions.
