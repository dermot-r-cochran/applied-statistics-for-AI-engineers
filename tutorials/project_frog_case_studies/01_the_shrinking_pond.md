# The Shrinking Pond

## Scenario
Project Frog version 2.4 reports **accuracy = 88%** on **1,200** synthetic evaluation examples. A later release reports **accuracy = 84%** on only **75** examples.

## Questions to answer
- Did the system actually get worse?
- Does the smaller sample alone explain the lower observed accuracy?
- How much did uncertainty increase?
- What interval should be reported with the later score?
- What additional information is needed before concluding regression?

## Concepts to practice
- sampling variability
- confidence intervals
- expected versus observed accuracy
- statistical uncertainty

## Engineering discussion
The point estimate fell, but the later evaluation carries much more uncertainty because it is based on far fewer observations. A smaller sample lowers confidence in the estimate, yet it does not automatically lower the true underlying accuracy. The right response is to compute intervals for both evaluations, inspect whether the datasets are comparable, and ask whether any slice mix or labeling changes occurred.

## What additional evidence helps?
- the same metric interval for each release
- class and complexity mix for both evaluation sets
- whether the examples are paired or independent
- any project-level clustering that reduces effective sample size
- whether the release changed latency, coverage, or error concentration on critical cases
