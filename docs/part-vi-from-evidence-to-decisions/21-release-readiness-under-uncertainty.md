# Chapter 21. Release Readiness Under Uncertainty

Release readiness is a decision under uncertainty, so point estimates must be combined with thresholds, risk appetite, and the consequences of being wrong.

**In-part navigation:** Part overview: [Overview](index.md) · Next: [22. Monitoring Is an Ongoing Experiment](22-monitoring-is-an-ongoing-experiment.md)

## Why this chapter matters

Release readiness is a decision under uncertainty, so point estimates must be combined with thresholds, risk appetite, and the consequences of being wrong.

## Section outline
1. **Work through the 89% estimate with a 95% interval from 84% to 93%** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Compare point-target thinking with evidence-threshold thinking** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Use release categories tied to uncertainty and consequence severity** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Explain release with caveats and evidence insufficiency** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Plan additional data collection when the decision remains borderline** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- Does the interval support, threaten, or fail to resolve the release target?
- What harms follow from releasing too early versus delaying too long?
- What extra evidence would most efficiently reduce uncertainty?


## Engineering interpretation

Turn release reviews into explicit evidence classifications: supports release, supports release with caveats, insufficient, or indicates release risk.

## Project Frog integration

Project Frog uses synthetic deployment thresholds to show why a nominal 90% target cannot be interpreted responsibly from an 89% point estimate alone.

## Future examples and tutorials

- _Placeholder_: Worked Python example: mapping interval evidence to release categories
- _Placeholder_: Visualization: target thresholds overlaid on interval estimates

## Related chapters and reference material

- [Chapter 16: Start with the Decision](../part-v-experimental-design/16-start-with-the-decision.md)
- [AI evaluation review checklist](../appendices/ai-evaluation-review-checklist.md)
- [Confidence-interval selection guide](../appendices/confidence-interval-selection-guide.md)


## Summary

Release readiness depends on the decision threshold, uncertainty bounds, and consequences of error—not on the point estimate alone.
