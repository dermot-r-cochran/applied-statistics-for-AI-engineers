# A decision framework for trustworthy AI evaluation

A trustworthy evaluation is not one that produces a large table of metrics. It is one that supports a specific decision with clearly stated assumptions and uncertainty.

Before trusting an observed AI metric, an engineer should be able to answer five questions.

## 1. What decision is this metric supposed to support?

A metric without a decision context is easy to overinterpret. A one-point difference might matter for a safety gate, be irrelevant for a product ranking change, or be dominated entirely by latency or cost constraints.

Always define:

- the decision to be made
- the threshold for action
- the direction of acceptable risk
- what happens if the estimate is wrong

## 2. What population does the result describe?

Every estimate belongs to a population, even when a dashboard does not say so.

Ask:

- Which cases were eligible for sampling?
- What unit was sampled: requests, documents, projects, users, or sessions?
- Are clusters or repeated observations present?
- Is the sample representative of the population the decision actually concerns?

If the sampled population differs from the deployment population, the metric may be internally correct and externally misleading.

## 3. How uncertain is the estimate?

A point estimate hides sampling variability. Uncertainty is not a formatting detail; it changes what conclusions are defensible.

Report uncertainty in a form appropriate to the problem, such as:

- confidence intervals
- bootstrap intervals
- standard errors
- power or minimum detectable effect calculations
- sensitivity analyses when assumptions are fragile

## 4. What assumptions make the number meaningful?

Most evaluation errors are not arithmetic mistakes. They are assumption mistakes.

Typical assumptions include:

- independent observations
- stable data generating conditions
- valid labels or reference data
- comparable test sets across versions
- no leakage from training or prompt construction into evaluation
- operationally meaningful metric definitions

If the assumptions fail, the statistic may still be computed correctly while the conclusion is wrong.

## 5. How does the metric relate to action?

A statistically detectable difference is not automatically decision-relevant. A difference that clears a release target may still be too uncertain to support deployment. A seemingly small regression may matter if it concentrates in a high-risk slice.

Trustworthy reporting therefore connects the estimate to:

- the operational threshold
- the downside of false confidence
- the cost of gathering more evidence
- the trade-off among quality, latency, coverage, and cost

## A minimal trustworthy evaluation statement

A useful evaluation summary should usually be able to say, in plain language:

1. what was measured
2. on which population
3. with what uncertainty
4. under which assumptions
5. for which decision
6. with what remaining risks

That is the standard this book tries to teach.
