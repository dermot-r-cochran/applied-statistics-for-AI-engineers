# Chapter 7. Test-Set Governance

Reliable evaluation requires governed datasets: documented purpose, controlled updates, protected holdouts, and explicit rules for when comparisons remain valid.

**In-part navigation:** Previous: [6. The Tadpole Problem](06-the-tadpole-problem.md) · Part overview: [Overview](index.md)

## Why this chapter matters

Reliable evaluation requires governed datasets: documented purpose, controlled updates, protected holdouts, and explicit rules for when comparisons remain valid.

## Section outline
1. **Define ownership, versioning, and intended use** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Separate benchmark evaluation from production monitoring** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Set change-control rules for labels, inclusion criteria, and scoring** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Create comparability statuses for evolving datasets** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Link governance artifacts to release decisions** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- Who can change the dataset, labels, or scoring pipeline?
- When is a refreshed test set comparable enough for trend reporting?
- How should benchmark, shadow, and monitoring datasets relate to one another?


## Engineering interpretation

Treat evaluation data as production infrastructure. Governance records should explain what changed, why it changed, and which comparisons are still defensible.

## Project Frog integration

Project Frog uses synthetic manifest versions to illustrate how a well-governed holdout, a surveillance sample, and an adjudication refresh can each serve different decisions.

## Future examples and tutorials

- _Placeholder_: Worked example: issuing a comparability ruling after a label-policy update
- _Placeholder_: Template walkthrough: test-set governance review for a fictional release

## Related chapters and reference material

- [Chapter 5: Is the Pond Representative?](05-is-the-pond-representative.md)
- [Evaluation dataset review checklist](../appendices/evaluation-dataset-review-checklist.md)
- [Evaluation comparability checklist](../appendices/evaluation-comparability-checklist.md)


## Summary

Governance keeps evaluation evidence interpretable over time. Without it, changes in the benchmark can masquerade as changes in the model.
