# Release Readiness

## Scenario
Observed Project Frog accuracy is **89%** with a **95% confidence interval from 84% to 93%**. The release target is **90%**.

## Questions to answer
- Has the target been achieved?
- What should be communicated to stakeholders?
- How can uncertainty be reduced?

## Concepts to practice
- decision theory
- confidence intervals
- risk-based decision making

## Engineering discussion
The point estimate is close to the target, but the interval still includes values below it. That means the current evidence does not cleanly rule out underperformance. A strong recommendation should combine the interval with error costs, stakeholder tolerance for risk, and the cost of collecting more data.

## What to communicate
- the observed estimate and interval together
- the risk that true performance remains below target
- whether the current uncertainty is acceptable for the deployment context
- what extra sampling or slice analysis would reduce uncertainty fastest
