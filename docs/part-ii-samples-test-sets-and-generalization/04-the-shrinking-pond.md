# Chapter 4. The Shrinking Pond

A smaller evaluation sample makes observed results noisier, but it does not by itself prove that the underlying system became worse.

**In-part navigation:** Part overview: [Overview](index.md) · Next: [5. Is the Pond Representative?](05-is-the-pond-representative.md)

## Why this chapter matters

A smaller evaluation sample makes observed results noisier, but it does not by itself prove that the underlying system became worse.

## Section outline
1. **Revisit population versus sample with Project Frog** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Work through the 88% on 1,200 versus 84% on 75 scenario** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Compare standard error, Wilson intervals, exact binomial intervals, and bootstrap intervals** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Explain why observed drops can arise from sampling variability alone** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **List what additional evidence is needed before declaring regression** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- What does the sample tell us about the target population?
- How much wider does uncertainty become when the sample shrinks?
- What composition checks are required before comparing two test runs?


## Engineering interpretation

Interpret a small follow-up test as provisional evidence. Engineers should report interval estimates, composition summaries, and comparability notes before escalating regression claims.

## Project Frog integration

Project Frog compares two synthetic evaluation rounds with identical generation rules except for sample size to show that fixed random seeds support reproducibility but do not remove sampling uncertainty.

## Future examples and tutorials

- _Placeholder_: Worked Python example: interval comparison for two synthetic evaluation rounds
- _Placeholder_: Visualization: interval widths as sample size changes

## Related chapters and reference material

- [Chapter 5: Is the Pond Representative?](05-is-the-pond-representative.md)
- [Chapter 16: Start with the Decision](../part-v-experimental-design/16-start-with-the-decision.md)
- [Confidence-interval selection guide](../appendices/confidence-interval-selection-guide.md)


## Summary

Small samples increase uncertainty and caution. They do not automatically diagnose a regression in the underlying system.
