# Chapter 15. System-Level Trust Is Not the Average of Component Confidence

End-to-end trust must be evaluated against end-to-end outcomes because dependencies, cascades, and handoffs can break any naïve inference from component scores.

**In-part navigation:** Previous: [14. Combining Confidence Scores](14-combining-confidence-scores.md) · Part overview: [Overview](index.md)

## Why this chapter matters

End-to-end trust must be evaluated against end-to-end outcomes because dependencies, cascades, and handoffs can break any naïve inference from component scores.

## Section outline
1. **Define system-level outcomes and failure decomposition** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Explain conditional dependence and cascading errors** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Teach coverage-risk trade-offs, abstention, and escalation** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Validate trust with end-to-end outcomes rather than component summaries** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Design monitoring that preserves system-level meaning over time** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- Which system failure modes emerge only when components interact?
- How should abstention or escalation change the interpretation of trust?
- What end-to-end evidence is required before using a trust label operationally?


## Engineering interpretation

Model pipelines as interacting evidence channels, not independent score emitters. Trust claims must be backed by outcome-level validation, decomposition, and monitoring.

## Project Frog integration

Project Frog uses correlated synthetic failures across extraction, retrieval, and explanation generation to show why strong component-level scores can still produce unsafe end-to-end behavior.

## Future examples and tutorials

- _Placeholder_: Worked example: coverage-risk curves for selective prediction in Project Frog
- _Placeholder_: Visualization: failure cascades across a synthetic four-stage pipeline

## Related chapters and reference material

- [Chapter 14: Combining Confidence Scores](14-combining-confidence-scores.md)
- [Chapter 21: Release Readiness Under Uncertainty](../part-vi-from-evidence-to-decisions/21-release-readiness-under-uncertainty.md)
- [AI evaluation review checklist](../appendices/ai-evaluation-review-checklist.md)


## Summary

System-level trust is an empirical claim about outcomes, not an arithmetic summary of component confidences.
