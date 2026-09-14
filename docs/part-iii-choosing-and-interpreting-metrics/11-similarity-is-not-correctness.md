# Chapter 11. Similarity Is Not Correctness

Similarity metrics often track surface closeness rather than task success, so they must not be mistaken for validated correctness or usefulness.

**In-part navigation:** Previous: [10. Aggregation Can Hide the Story](10-aggregation-can-hide-the-story.md) · Part overview: [Overview](index.md)

## Why this chapter matters

Similarity metrics often track surface closeness rather than task success, so they must not be mistaken for validated correctness or usefulness.

## Section outline
1. **Separate lexical or embedding similarity from task truth** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Identify tasks where similarity is a proxy at best** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Document validation needed before operational use** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Show failure modes for semantically plausible but wrong outputs** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Connect proxy metrics to human evaluation** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- What notion of similarity is being measured?
- Why should this proxy correlate with the real task outcome?
- Which counterexamples break the assumed relationship?


## Engineering interpretation

Use similarity scores only after empirically validating that they support a real decision in the target workflow.

## Project Frog integration

Project Frog uses evidence retrieval and explanation generation examples to show how close-looking outputs can still justify the wrong class or omit decisive evidence.

## Future examples and tutorials

- _Placeholder_: Worked example: synthetic retrieval relevance versus end-to-end correctness
- _Placeholder_: Visualization: similarity score overlap for correct and incorrect outputs

## Related chapters and reference material

- [Chapter 1: The Metric Is Not the System](../part-i-what-are-we-measuring/01-the-metric-is-not-the-system.md)
- [Chapter 12: What Does Confidence Mean?](../part-iv-confidence-across-ai-pipelines/12-what-does-confidence-mean.md)
- [Glossary](../appendices/glossary.md)


## Summary

Similarity can be useful evidence, but it is not correctness until validated against the decision that matters.
