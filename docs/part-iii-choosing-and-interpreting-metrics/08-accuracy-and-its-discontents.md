# Chapter 8. Accuracy and Its Discontents

Accuracy is easy to compute and easy to misunderstand because it hides class imbalance, asymmetric harms, and decision thresholds.

**In-part navigation:** Part overview: [Overview](index.md) · Next: [9. Precision, Recall, and the Cost of Being Wrong](09-precision-recall-and-the-cost-of-being-wrong.md)

## Why this chapter matters

Accuracy is easy to compute and easy to misunderstand because it hides class imbalance, asymmetric harms, and decision thresholds.

## Section outline
1. **Define what accuracy summarizes and omits** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Show why majority classes can dominate the headline result** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Connect threshold choices to operational consequences** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Use confusion-matrix views to recover hidden error modes** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Position accuracy as a starting point rather than a verdict** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- What kinds of mistakes are being averaged together?
- Which rare but important failures disappear inside overall accuracy?
- When is accuracy still a useful monitoring summary?


## Engineering interpretation

Report accuracy only with class balance, confusion patterns, and the decision context that explains whether its averaging rule is acceptable.

## Project Frog integration

Project Frog shows how `Escalate` errors can matter more than `Clear` wins even when the total accuracy looks strong.

## Future examples and tutorials

- _Placeholder_: Worked Python example: confusion-matrix decomposition on synthetic triage labels
- _Placeholder_: Visualization: how changing base rates alters the meaning of the same accuracy score

## Related chapters and reference material

- [Chapter 9: Precision, Recall, and the Cost of Being Wrong](09-precision-recall-and-the-cost-of-being-wrong.md)
- [Metric-selection guide](../appendices/metric-selection-guide.md)
- [Glossary](../appendices/glossary.md)


## Summary

Accuracy is a summary, not an argument. It becomes useful only when its averaging assumptions fit the decision.
