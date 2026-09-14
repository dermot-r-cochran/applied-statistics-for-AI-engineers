# Trustworthy AI Evaluation

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
