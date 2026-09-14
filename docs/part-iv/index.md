# Part IV: Confidence Across AI Pipelines

Part IV teaches a single discipline: **equal numeric scales do not imply equal meaning**.

Project Frog contains four fictional components:

1. Document extraction
2. Classification
3. Evidence retrieval
4. Explanation generation

Each component emits a score in `[0, 1]`, but the scores differ in definition, generating process, calibration behavior, population, and failure mode. A `0.90` from one component therefore does **not** automatically mean what a `0.90` from another component means.

## Part IV chapters

- [12. What Does Confidence Mean?](chapter-12-what-does-confidence-mean.md)
- [13. Calibration](chapter-13-calibration.md)
- [14. Combining Confidence Scores](chapter-14-combining-confidence-scores.md)
- [15. System-Level Trust Is Not the Average of Component Confidence](chapter-15-system-level-trust.md)

## Reusable references

- [Confidence semantics card](../reference/confidence-semantics-card.md)
- [Glossary](../reference/glossary.md)

## Synthetic experiment assets

- Dataset: [`project_frog_confidence_dataset.csv`](../assets/generated/project_frog_confidence_dataset.csv)
- Results: [`project_frog_method_results.json`](../assets/generated/project_frog_method_results.json)
- Reliability figure: ![Synthetic reliability diagram](../assets/generated/classification_reliability.png)
