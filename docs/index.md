# Trustworthy AI Evaluation

**Subtitle:** Experimental Design, Metrics, Confidence, and Decision-Making for AI Engineers

This site develops a synthetic, fictional book built around **Project Frog**, a fictional AI-assisted document analysis platform. The chapters in this repository focus on two failure-prone parts of evaluation work:

- **Part II:** how samples, test sets, and clustering shape what a benchmark result means
- **Part V:** how to design comparisons and decisions that remain valid under uncertainty

## What is included here

- Completed Part II chapters on sample quality, representativeness, clustering, and governance
- Completed Part V chapters on decision-driven experimentation, fair comparisons, effect sizes, power, and resampling
- Practical templates and checklists for evaluation operations
- A small Python package with bootstrap, comparison, and planning utilities

## Project Frog reminder

All examples are synthetic. Fixed random seeds can improve **reproducibility**, but they do **not** remove [sampling uncertainty](reference/glossary.md#sampling-variance) or [sampling bias](reference/glossary.md#sampling-bias).

## Reading paths

- Start with [The Shrinking Pond](part-ii/04-the-shrinking-pond.md) if you need to reset how you think about sample size and observed metrics.
- Start with [Start with the Decision](part-v/16-start-with-the-decision.md) if you need to design an evaluation before running it.
- Use the [Glossary](reference/glossary.md) and [Python API](reference/python-api.md) as supporting references.
