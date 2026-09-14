# Chapter 12. What Does Confidence Mean?

Equal numeric scales do not imply equal meaning: two scores of 0.90 can represent different events, data-generating processes, and decisions.

**In-part navigation:** Part overview: [Overview](index.md) · Next: [13. Calibration](13-calibration.md)

## Why this chapter matters

Equal numeric scales do not imply equal meaning: two scores of 0.90 can represent different events, data-generating processes, and decisions.

## Section outline
1. **Define confidence semantics for each Project Frog component** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Separate scores, probabilities, ranks, and heuristics** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Introduce the reusable confidence semantics card** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Explain valid versus invalid score comparisons** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Link confidence meaning to supported decisions** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- What event does this score claim to describe?
- Is the score intended as a probability or only an ordinal signal?
- Which cross-component comparisons are meaningless even when the scales match numerically?


## Engineering interpretation

Engineers should refuse to average, rank, or threshold scores until each score has a written semantics card that states what it means and what it cannot mean.

## Project Frog integration

Project Frog contrasts extraction, classification, evidence retrieval, and explanation generation so readers see immediately that a single 0-1 scale hides different mechanisms and failure modes.

## Future examples and tutorials

- _Placeholder_: Worked Python example: validating score metadata before composition
- _Placeholder_: Visualization: a semantic map of Project Frog confidence scores

## Related chapters and reference material

- [Chapter 13: Calibration](13-calibration.md)
- [Confidence-related reference material](../appendices/confidence-reference.md)
- [Metric definition card](../appendices/metric-definition-card.md)


## Summary

Confidence is not a universal quantity. Meaning comes from the event, model, calibration process, and decision context behind the number.
