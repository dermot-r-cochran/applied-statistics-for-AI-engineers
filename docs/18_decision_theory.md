# Decision Theory

## Why does an AI engineer need to understand this?
Decision theory matters because engineering choices depend on costs, benefits, and uncertainty together. A release should not hinge on a metric threshold alone when the consequences of being wrong are asymmetric.

## 1. Engineering Problem
Project Frog reports 89% observed accuracy with a 95% interval from 84% to 93%, while the release target is 90%. The problem is whether to ship, delay, or collect more evidence.

## 2. Intuition
Decision theory reframes evaluation from 'what does the estimate say?' to 'what action has the best expected consequences under uncertainty?'. It makes trade-offs explicit.

## 3. Mathematical Foundation
Introduce losses, utilities, thresholds, and value of information. The mathematical core is that the optimal action depends on both probability and consequence.

## 4. Python Example
Work through a synthetic Project Frog release decision where shipping early saves effort but increases the risk of incorrect compliance recommendations. Compare decisions under optimistic and cautious loss assumptions.

## 5. Interpretation
Interpret the same metric differently when error costs change. A borderline accuracy estimate may be acceptable for low-risk automation but unacceptable for high-risk decisions.

## 6. Common Mistakes
Mistakes include using fixed thresholds without cost context, pretending uncertainty disappears after a single evaluation, and failing to communicate downside scenarios.

## 7. AI Engineering Applications
Use decision theory for release gates, rollback triggers, escalation policies, and monitoring thresholds. It is where statistics meets engineering accountability.


## 8. Trust Checkpoint
Before trusting an observed Project Frog metric in this setting, write down:
- the metric definition and unit of analysis
- the uncertainty estimate and how it was computed
- the population or slice the result is supposed to represent
- the assumptions required for the estimate to be interpretable
- the decision that would change if the result moved

## 9. Exercises
Write a decision rule for Project Frog when the cost of a false approval is five times the cost of a false rejection. Explain how additional evaluation data changes the preferred action.

## 10. Further Reading
Further reading should include expected utility, decision analysis for practitioners, and value-of-information thinking.
