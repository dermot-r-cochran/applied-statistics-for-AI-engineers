# Chapter 6. The Tadpole Problem

Counting rows as independent evidence can wildly overstate certainty when many observations come from the same documents, projects, or other shared sources.

**In-part navigation:** Previous: [5. Is the Pond Representative?](05-is-the-pond-representative.md) · Part overview: [Overview](index.md) · Next: [7. Test-Set Governance](07-test-set-governance.md)

## Why this chapter matters

Counting rows as independent evidence can wildly overstate certainty when many observations come from the same documents, projects, or other shared sources.

## Section outline
1. **Introduce the 1,000 rows, 20 documents, and 6 projects scenario** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Distinguish unit of observation from unit of inference** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Explain clustering, repeated observations, and hierarchical variation** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Use cluster-aware uncertainty and cluster bootstrap concepts** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Show why no universal effective sample size formula is appropriate** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- How many independent opportunities for failure are really represented?
- At which level should uncertainty be summarized: row, document, or project?
- Which dependence structures matter for the decision at hand?


## Engineering interpretation

Choose the inferential unit first, then design uncertainty estimates around that structure. Avoid presenting repeated rows as if they were separate independent confirmations.

## Project Frog integration

Project Frog uses repeated component outputs per `document_id` and `project_id` so the chapter can show how clustered evidence changes interval width and model-comparison claims.

## Future examples and tutorials

- _Placeholder_: Worked Python example: row bootstrap versus cluster bootstrap
- _Placeholder_: Visualization: project-level variation hiding inside row-level counts

## Related chapters and reference material

- [Chapter 17: Fair Model Comparisons](../part-v-experimental-design/17-fair-model-comparisons.md)
- [Sample-size planning worksheet](../appendices/sample-size-planning-worksheet.md)
- [Glossary](../appendices/glossary.md)


## Summary

Rows are not automatically independent evidence. Dependence changes uncertainty, comparability, and the credibility of experimental claims.
