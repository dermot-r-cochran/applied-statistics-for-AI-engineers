# Trustworthy AI Evaluation

This repository is being developed as the **Trustworthy AI Evaluation** book site.

## Book structure

The site is organized as a six-part book:

1. **What Are We Measuring?**
2. **Samples, Test Sets, and Generalization**
3. **Choosing and Interpreting Metrics**
4. **Confidence Across AI Pipelines**
5. **Experimental Design**
6. **From Evidence to Decisions**

It also includes appendix and reference pages for glossary terms, metric and interval guides, evaluation checklists, and reusable templates.

## Case study rules

The book uses **Project Frog** as a continuous fictional case study. All examples are synthetic, reproducible where code is later introduced, and free of internal or proprietary references.

## Local development

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

## Validation

Build the site in strict mode before publishing changes:

```bash
mkdocs build --strict
```

## Repository goal

The current phase focuses on establishing complete navigation and structured chapter outlines so future drafting, examples, and tutorials can extend the book coherently.
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
- `src/project_frog_eval/` - small Python utilities for synthetic evaluation data and summaries
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
