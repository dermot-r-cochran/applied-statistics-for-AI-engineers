# Chapter 9. Precision, Recall, and the Cost of Being Wrong

Precision and recall surface different operational risks, so selecting or tuning between them is fundamentally a decision problem.

**In-part navigation:** Previous: [8. Accuracy and Its Discontents](08-accuracy-and-its-discontents.md) · Part overview: [Overview](index.md) · Next: [10. Aggregation Can Hide the Story](10-aggregation-can-hide-the-story.md)

## Why this chapter matters

Precision and recall surface different operational risks, so selecting or tuning between them is fundamentally a decision problem.

## Section outline
1. **Relate false positives and false negatives to workflow cost** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Describe threshold tuning and operating points** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Compare class-specific trade-offs in multi-class settings** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Tie metric choice to human review capacity** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Document acceptable error trade-offs** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- Which error is more expensive in this workflow?
- How much review load can the organization absorb?
- Which operating point best matches stakeholder risk tolerance?


## Engineering interpretation

Choose precision- and recall-oriented targets only after documenting the operational costs of wrong actions, missed actions, and abstentions.

## Project Frog integration

Project Frog uses `Review` and `Escalate` cases to show how higher recall may be preferred when missing a risky case is more expensive than extra manual review.

## Future examples and tutorials

- _Placeholder_: Worked example: threshold sweep for a synthetic escalation detector
- _Placeholder_: Visualization: precision-recall trade-offs by difficulty subgroup

## Related chapters and reference material

- [Chapter 8: Accuracy and Its Discontents](08-accuracy-and-its-discontents.md)
- [Chapter 16: Start with the Decision](../part-v-experimental-design/16-start-with-the-decision.md)
- [Metric-selection guide](../appendices/metric-selection-guide.md)


## Summary

Precision and recall are cost statements in metric form. They matter only relative to a concrete decision and workload.
