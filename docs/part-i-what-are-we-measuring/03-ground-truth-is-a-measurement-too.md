# Chapter 3. Ground Truth Is a Measurement Too

Reference labels are produced by people, guidelines, tools, and compromises, so they deserve the same scrutiny as model outputs.

**In-part navigation:** Previous: [2. From Concepts to Measurements](02-from-concepts-to-measurements.md) · Part overview: [Overview](index.md)

## Why this chapter matters

Reference labels are produced by people, guidelines, tools, and compromises, so they deserve the same scrutiny as model outputs.

## Section outline
1. **Treat annotation as a measurement process** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Document adjudication, disagreement, and unresolved ambiguity** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Separate label quality from model quality** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Use error analysis to find reference instability** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Govern reference changes over time** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- Who created the reference labels and under what instructions?
- How much ambiguity is structural rather than annotator error?
- When should disagreement become a separate output instead of forced consensus?


## Engineering interpretation

Reference data should be versioned, audited, and monitored for drift. A model cannot be more trustworthy than the measurement process used to judge it.

## Project Frog integration

Project Frog’s synthetic case study uses fictional reviewers and adjudication notes to show how `reference_class` is itself the outcome of a controlled measurement pipeline.

## Future examples and tutorials

- _Placeholder_: Worked example: synthetic adjudication drift and its effect on accuracy
- _Placeholder_: Tutorial: writing label guidance for ambiguous escalation cases

## Related chapters and reference material

- [Chapter 2: From Concepts to Measurements](02-from-concepts-to-measurements.md)
- [Chapter 7: Test-Set Governance](../part-ii-samples-test-sets-and-generalization/07-test-set-governance.md)
- [Glossary](../appendices/glossary.md)


## Summary

Ground truth is not a magical constant. It is evidence produced by a process that must be documented and evaluated on its own terms.
