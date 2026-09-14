# Trustworthy AI Evaluation

This site is a synthetic, reproducible book prototype for **Trustworthy AI Evaluation**. Every dataset, chart, identifier, scenario, and score on this site is fictional and programmatically generated for teaching purposes.

## First reading path

This reading path follows the narrative arc **decision → measurement → sampling uncertainty → metric interpretation → component confidence → experimental design → defensible release decision**.

1. [Chapter 16 · Start with the Decision](chapters/start-with-the-decision.md)
2. [Chapter 1 · The Metric Is Not the System](chapters/the-metric-is-not-the-system.md)
3. [Chapter 4 · The Shrinking Pond](chapters/the-shrinking-pond.md)
4. [Chapter 8 · Accuracy and Its Discontents](chapters/accuracy-and-its-discontents.md)
5. [Chapter 12 · What Does Confidence Mean?](chapters/what-does-confidence-mean.md)
6. [Chapter 14 · Combining Confidence Scores](chapters/combining-confidence-scores.md)
7. [Chapter 21 · Release Readiness Under Uncertainty](chapters/release-readiness-under-uncertainty.md)

## Project Frog

Project Frog is the running fictional case study. See the [Project Frog synthetic data reference](reference/project-frog-data.md) for the stable schema, component list, class labels, reproducibility note, and data-generation assumptions.

## Reproducibility note

The repository uses fixed random seeds so the same synthetic examples can be rebuilt exactly. That supports reproducibility, but it does **not** remove [sampling uncertainty](glossary.md#sampling-uncertainty): a fixed-seed sample is still only one sample.

## Validation workflow

```bash
python -m pip install -e .[dev]
python scripts/generate_assets.py
pytest
mkdocs build --strict
```

## Supporting references

- [Glossary](glossary.md)
- [Confidence semantics card](reference/confidence-semantics-card.md)
- [Experiment protocol template](reference/experiment-protocol-template.md)
- [Evaluation comparability checklist](reference/evaluation-comparability-checklist.md)
- [Sample-size planning worksheet](reference/sample-size-planning-worksheet.md)
