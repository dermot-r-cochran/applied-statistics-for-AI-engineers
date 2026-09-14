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
