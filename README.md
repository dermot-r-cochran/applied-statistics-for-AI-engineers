# Trustworthy AI Evaluation

*Experimental Design, Metrics, Confidence, and Decision-Making for AI Engineers*

This repository is an open-source book and utility library for engineers who need to evaluate AI systems rigorously enough to support defensible technical and product decisions.

The recurring question throughout the material is:

> **When should an engineer trust an observed AI metric?**

The book's central thesis is:

> **An AI metric is useful only when its meaning, uncertainty, population, assumptions, and relationship to a decision are understood.**

## What this repository contains

This repository preserves the earlier **Applied Statistics for AI Engineers** material and reorganizes it into a book-style GitHub Pages site while keeping the supporting Python utilities, tests, examples, and notebooks in place.

- `index.md`, `book/`, `docs/`, `tutorials/`: book content and hands-on case studies
- `src/applied_stats_ai/`: reusable statistical utilities for AI evaluation work
- `tests/`: pytest coverage for the public package
- `examples/`: synthetic scripts and datasets used in the book
- `notebooks/`: interactive companion material

All examples are synthetic and fictional. The recurring teaching environment is **Project Frog**, a fictional AI-assisted document analysis and decision-support platform.

## Read the book

After GitHub Pages is enabled for this repository, the book is built from the repository root with Jupyter Book.

Locally:

```bash
uv sync
uv run jupyter-book build .
open _build/html/index.html
```

The published book is organized for experienced:

- machine learning engineers
- AI engineers
- software engineers working on AI systems
- data scientists
- test architects
- technical leads
- engineering and product decision-makers

## Development

This project targets **Python 3.12+** and uses **uv**.

```bash
uv sync
uv run ruff check .
uv run pytest
uv run jupyter-book build .
```

## Preservation note

Useful existing educational material, notebooks, examples, utilities, and tests were retained and integrated into the book structure rather than deleted. The main change is the addition of a coherent book navigation layer and GitHub Pages publishing workflow.
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
