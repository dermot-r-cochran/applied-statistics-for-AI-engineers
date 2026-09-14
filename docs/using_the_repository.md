# How to use the repository

## Read, run, and adapt

This repository is both a book and a working Python project.

### If you want the conceptual path

Read the chapters in order from Part I through Part IV. The sequencing is designed to move from uncertainty basics to release and monitoring decisions.

### If you want the practical path

Start with:

- the confidence-interval notebook
- the Project Frog case studies
- the runnable examples in `examples/`

Then return to the relevant chapters when you need the underlying assumptions or mathematics.

## Local preview

```bash
uv sync
uv run mkdocs serve
```

## Validation commands

```bash
uv run ruff check .
uv run pytest
uv run mkdocs build --strict
```

## Useful repository entry points

- `src/applied_stats_ai/`: reusable statistical helpers and synthetic-data generators
- `tests/`: unit tests for the library
- `tutorials/`: notebooks and applied walkthroughs
- `examples/`: compact runnable scripts

## Reading rule

Do not treat a metric in isolation. Use the chapters and utilities together to ask what the metric means, how uncertain it is, which population it represents, and whether it can support the engineering decision in front of you.
