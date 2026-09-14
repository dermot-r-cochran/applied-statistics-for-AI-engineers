# Chapter 14. Combining Confidence Scores

There is no universal formula for combining component scores; every composition rule inherits semantic assumptions, dependence assumptions, and validation obligations.

**In-part navigation:** Previous: [13. Calibration](13-calibration.md) · Part overview: [Overview](index.md) · Next: [15. System-Level Trust Is Not the Average of Component Confidence](15-system-level-trust-is-not-the-average-of-component-confidence.md)

## Why this chapter matters

There is no universal formula for combining component scores; every composition rule inherits semantic assumptions, dependence assumptions, and validation obligations.

## Section outline
1. **Critique the anti-pattern of averaging every available score** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Compare minimum, maximum, means, products, rules, and meta-models** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Document semantic compatibility and dependence requirements** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Show when it is safer to retain a vector of scores or convert to risk categories** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Connect abstention and human review to score composition** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- What does the combined output mean, exactly?
- Are the component scores compatible enough to combine numerically?
- What validation would show that the composed score is decision-useful rather than merely plausible?


## Engineering interpretation

Before adopting any combination rule, state its intended interpretation, validate it end-to-end, and specify which deployments or populations would invalidate the rule.

## Project Frog integration

Project Frog runs a synthetic composition experiment in which numerically plausible aggregates become badly calibrated when component errors are correlated or score semantics differ.

## Future examples and tutorials

- _Placeholder_: Worked Python example: comparing aggregation rules on synthetic pipeline outputs
- _Placeholder_: Visualization: calibration and utility trade-offs for candidate composition methods

## Related chapters and reference material

- [Chapter 13: Calibration](13-calibration.md)
- [Chapter 15: System-Level Trust Is Not the Average of Component Confidence](15-system-level-trust-is-not-the-average-of-component-confidence.md)
- [Confidence-related reference material](../appendices/confidence-reference.md)


## Summary

A combined score is meaningful only if its interpretation, assumptions, and validation evidence are explicit. Plausible arithmetic is not enough.
