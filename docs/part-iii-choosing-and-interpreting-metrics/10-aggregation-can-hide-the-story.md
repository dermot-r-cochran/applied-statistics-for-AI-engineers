# Chapter 10. Aggregation Can Hide the Story

Averages can conceal subgroup failures, unstable components, and distribution shifts that matter more than the overall trend.

**In-part navigation:** Previous: [9. Precision, Recall, and the Cost of Being Wrong](09-precision-recall-and-the-cost-of-being-wrong.md) · Part overview: [Overview](index.md) · Next: [11. Similarity Is Not Correctness](11-similarity-is-not-correctness.md)

## Why this chapter matters

Averages can conceal subgroup failures, unstable components, and distribution shifts that matter more than the overall trend.

## Section outline
1. **Explain macro, micro, and weighted aggregation** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Show subgroup masking and Simpson-style reversals** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Decide when stratified reporting is mandatory** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Connect aggregation choices to governance and fairness review** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Build reporting habits that preserve the story behind the mean** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- Which subgroups are being pooled together?
- Would a different weighting scheme reverse the ranking?
- Which audience needs the disaggregated view to act responsibly?


## Engineering interpretation

Publish aggregation rules with subgroup breakdowns and rationale. If the action differs by subgroup, the report should too.

## Project Frog integration

Project Frog uses difficulty groups and component stages to show how an apparently stable overall metric can hide worsening behavior on complex cases.

## Future examples and tutorials

- _Placeholder_: Worked example: macro versus micro results on synthetic component data
- _Placeholder_: Visualization: subgroup trend dashboard for benchmark and monitoring sets

## Related chapters and reference material

- [Chapter 5: Is the Pond Representative?](../part-ii-samples-test-sets-and-generalization/05-is-the-pond-representative.md)
- [Chapter 14: Combining Confidence Scores](../part-iv-confidence-across-ai-pipelines/14-combining-confidence-scores.md)
- [AI evaluation review checklist](../appendices/ai-evaluation-review-checklist.md)


## Summary

Aggregation decisions are modeling decisions. If they hide operationally meaningful variation, they are the wrong summary.
