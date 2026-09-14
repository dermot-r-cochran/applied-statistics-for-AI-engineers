# Chapter 5. Is the Pond Representative?

Sample size and representativeness are different properties; a large but skewed test set can mislead more than a small but well-targeted one.

**In-part navigation:** Previous: [4. The Shrinking Pond](04-the-shrinking-pond.md) · Part overview: [Overview](index.md) · Next: [6. The Tadpole Problem](06-the-tadpole-problem.md)

## Why this chapter matters

Sample size and representativeness are different properties; a large but skewed test set can mislead more than a small but well-targeted one.

## Section outline
1. **Define the target population and coverage claims** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Analyze the changing Simple/Moderate/Complex composition scenario** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Use stratified reporting, standardization, and weighting carefully** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Explain what weighting can and cannot repair** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Design representativeness checks for evolving deployments** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- Which parts of the target population are over- or under-represented?
- Would the conclusion change if the deployment mix changed?
- Which important conditions are missing entirely from the sample?


## Engineering interpretation

Engineers should ship evaluation manifests that name the target population, sampling frame, known exclusions, and any reweighting assumptions used in reporting.

## Project Frog integration

Project Frog tracks `difficulty` explicitly so the reader can see how unchanged component behavior can look better or worse when case mix shifts from 70/20/10 to 40/30/30.

## Future examples and tutorials

- _Placeholder_: Worked Python example: standardized accuracy across changing difficulty mix
- _Placeholder_: Visualization: stacked composition shift and stratified metrics

## Related chapters and reference material

- [Chapter 4: The Shrinking Pond](04-the-shrinking-pond.md)
- [Chapter 7: Test-Set Governance](07-test-set-governance.md)
- [Test-set manifest template](../appendices/test-set-manifest-template.md)


## Summary

Representativeness is about coverage, not row count. Weighting can help with known composition differences but cannot repair missing or biased evidence.
