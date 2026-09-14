# Chapter 13. Calibration

Calibration asks whether stated confidence aligns with observed frequencies, but no single summary statistic captures every calibration concern.

**In-part navigation:** Previous: [12. What Does Confidence Mean?](12-what-does-confidence-mean.md) · Part overview: [Overview](index.md) · Next: [14. Combining Confidence Scores](14-combining-confidence-scores.md)

## Why this chapter matters

Calibration asks whether stated confidence aligns with observed frequencies, but no single summary statistic captures every calibration concern.

## Section outline
1. **Contrast raw scores with estimated probabilities** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Teach reliability diagrams, calibration curves, and Brier score** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Explain expected calibration error and its limitations** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Show subgroup calibration and calibration drift** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Define when recalibration is warranted and how to validate it** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- If the model says 0.80, how often is it correct in the relevant population?
- Does calibration hold across subgroups and time periods?
- Which calibration failures matter for the decision being made?


## Engineering interpretation

Calibration should be evaluated with multiple views: visual curves, proper scoring rules, subgroup slices, and drift monitoring, not only a single ECE number.

## Project Frog integration

Project Frog uses synthetic components with intentionally different calibration properties so readers can compare overconfidence, underconfidence, and subgroup drift on shared plots.

## Future examples and tutorials

- _Placeholder_: Worked Python example: reliability diagrams and Brier decomposition
- _Placeholder_: Visualization: subgroup calibration drift between evaluation rounds

## Related chapters and reference material

- [Chapter 12: What Does Confidence Mean?](12-what-does-confidence-mean.md)
- [Chapter 14: Combining Confidence Scores](14-combining-confidence-scores.md)
- [Confidence-related reference material](../appendices/confidence-reference.md)


## Summary

Calibration is population-dependent evidence about how a score behaves. It requires visual, numerical, and subgroup-aware validation.
