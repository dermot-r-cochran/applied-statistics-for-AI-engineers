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
This repository currently focuses on **Part IV: Confidence Across AI Pipelines** of the synthetic *Trustworthy AI Evaluation* book.

All datasets, figures, examples, and results in this repository are **fully synthetic** and exist only to teach evaluation practice.

## Current reading path

- [Part IV overview](part-iv/index.md)
- [12. What Does Confidence Mean?](part-iv/chapter-12-what-does-confidence-mean.md)
- [13. Calibration](part-iv/chapter-13-calibration.md)
- [14. Combining Confidence Scores](part-iv/chapter-14-combining-confidence-scores.md)
- [15. System-Level Trust Is Not the Average of Component Confidence](part-iv/chapter-15-system-level-trust.md)
- [Confidence semantics card](reference/confidence-semantics-card.md)
- [Glossary](reference/glossary.md)

## Package utilities

The accompanying Python package exposes:

- `calibration_curve_data`
- `expected_calibration_error`
- `brier_score_summary`
- `subgroup_metric_report`
- `metric_comparability_check`

Use `python -m trustworthy_ai_evaluation.project_frog_experiment` to regenerate the synthetic Part IV artifacts.
