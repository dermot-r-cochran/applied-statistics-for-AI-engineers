# Repository guide

This repository is both a book and a working codebase.

## Content layers

### Book chapters
The `docs/` directory contains short, practical chapters on the statistical foundations of trustworthy AI evaluation.

### Tutorials and case studies
The `tutorials/` directory contains hands-on walkthroughs and scenario-based exercises, including the Project Frog case studies.

### Executable utilities
The `src/applied_stats_ai/` package contains reusable functions for interval estimation, bootstrap methods, model comparison, power analysis, confusion-matrix uncertainty, and effective sample size calculations.

### Tests
The `tests/` directory keeps the public utility code honest and provides executable examples of expected behavior.

## Local workflow

```bash
uv sync
uv run ruff check .
uv run pytest
uv run jupyter-book build .
```

The built site is written to `_build/html/`.

## What was preserved

The original educational direction of the repository, the Python package, example scripts, notebook, tutorials, and tests were preserved. The main transformation is the addition of a navigable book layer and a GitHub Pages publishing path.
