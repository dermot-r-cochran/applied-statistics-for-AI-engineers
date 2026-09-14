# Trustworthy AI Evaluation

Experimental Design, Metrics, Confidence, and Decision-Making for AI Engineers.

This repository contains a synthetic, fictional book project built around **Project Frog**, a fictional AI-assisted document analysis platform. The current repository state completes **Part II** and **Part V** of the book, along with reusable Python utilities for evaluation design, resampling, and comparability checks.

## Contents

- Book chapters under `/docs`
- Evaluation utilities in `/trustworthy_ai_evaluation`
- Unit tests in `/tests`
- Reusable templates and checklists in `/docs/artifacts`

## Install

```bash
python -m pip install -e .[docs]
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Build the site

```bash
mkdocs build --strict
```

All examples, scenarios, and artifacts are synthetic and fictional.
Synthetic book materials and Python utilities for teaching applied statistics and metrics to AI engineers.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m trustworthy_ai_evaluation.project_frog_experiment
pytest
mkdocs build --strict
```

All datasets, figures, and examples in this repository are fully synthetic.
# applied-statistics-for-AI-engineers
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
