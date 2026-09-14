# Trustworthy AI Evaluation

**Experimental Design, Metrics, Confidence, and Decision-Making for AI Engineers**

Trustworthy AI Evaluation is a book-style GitHub Pages site and Python repository for engineers who need to decide when an observed AI metric is strong enough to support action.

> **Central question:** When should an engineer trust an observed AI metric?
>
> **Central thesis:** An AI metric is useful only when its meaning, uncertainty, population, assumptions, and relationship to a decision are understood.

The repository preserves the original Applied Statistics for AI Engineers direction while reorganizing it into a coherent technical book with runnable code, tests, notebooks, examples, and a lightweight GitHub Pages workflow.

## What is in the repository?

- **Book chapters** in `docs/` covering probability, sampling, intervals, testing, effect size, power, bootstrap, Bayesian reasoning, classification metrics, experimental design, measurement, decision theory, and monitoring.
- **Project Frog tutorials** in `tutorials/`, including case studies and a notebook on confidence intervals for accuracy.
- **Reusable utilities** in `src/applied_stats_ai/` for interval estimation, bootstrap uncertainty, paired model comparison, power analysis, effective sample size, and synthetic Project Frog data generation.
- **Tests** in `tests/` so the educational material stays executable and trustworthy.

## Project Frog

Project Frog is the repository's continuous fictional case study: an AI-assisted document analysis and decision-support platform built entirely from synthetic examples. It may report accuracy, precision, recall, F1/F-beta, agreement rate, coverage, evidence quality, text similarity, latency, processing cost, and confidence-like component scores.

All Project Frog data in this repository is synthetic and programmatically generated.

## Local setup

This repository targets **Python 3.12+** and uses **uv**.

```bash
uv sync
```

## Run the checks

```bash
uv run ruff check .
uv run pytest
uv run mkdocs build --strict
```

## Preview the book locally

```bash
uv run mkdocs serve
```

## Repository map

```text
.
├── docs/
├── tutorials/
├── examples/
├── src/applied_stats_ai/
├── tests/
├── mkdocs.yml
└── .github/workflows/pages.yml
```

## Suggested reading path

1. Start at `docs/index.md` or the published GitHub Pages site.
2. Read Parts I-IV in order if you want the full narrative.
3. Jump to `tutorials/confidence_intervals/confidence_intervals_for_accuracy.ipynb` if you want a notebook-first entry point.
4. Use the Project Frog case studies to practice making evidence-based release decisions.

## Contributor notes

See `CONTRIBUTING.md` for concise setup, preview, and validation instructions.
