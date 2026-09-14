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
Applied Statistics and Metrics for AI Engineers

Interactive GitHub Pages content is provided via:

- `/index.html` — learning roadmap and lesson navigation
- `/lesson-01-sampling-distributions.html` — first lesson in the sequence
- `/session-template.html` — end-of-session output generator

Trustworthy AI Evaluation is a book-style GitHub Pages site for applied statistics, confidence, calibration, sampling, and evaluation decisions for AI engineers.

All examples in this repository are synthetic and fictional under the Project Frog teaching environment.

## Repository layout

- `docs/` - static GitHub Pages site with book-style navigation and interactive lesson pages
- `src/project_frog_eval/` - small Python utilities for synthetic evaluation data, summaries, and interval-aware metric reporting
- `tests/` - unit tests for the supporting utilities

## Local preview

Serve the GitHub Pages content locally with Python:

```bash
python3 -m http.server 8000 --directory docs
```

Then open `http://localhost:8000`.

## Run tests

Set the source path and run the standard library test suite:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```
