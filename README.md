# applied-statistics-for-AI-engineers

This repository now contains a synthetic **Trustworthy AI Evaluation** book prototype focused on a first reading path through seven connected chapters:

- Chapter 16 · Start with the Decision
- Chapter 1 · The Metric Is Not the System
- Chapter 4 · The Shrinking Pond
- Chapter 8 · Accuracy and Its Discontents
- Chapter 12 · What Does Confidence Mean?
- Chapter 14 · Combining Confidence Scores
- Chapter 21 · Release Readiness Under Uncertainty

All Project Frog datasets, figures, and scenarios are fictional, synthetic, and reproducible.

## Local setup

```bash
python -m pip install -e .[dev]
python scripts/generate_assets.py
pytest
mkdocs build --strict
```

## Key paths

- `docs/` — book pages, glossary, and reference templates
- `src/trustworthy_ai_evaluation/` — synthetic data generation and statistical utilities
- `data/synthetic/` — generated synthetic datasets and chapter metrics
- `scripts/generate_assets.py` — reproducible dataset and figure generation
- `tests/` — unit tests for generation and statistical utilities
