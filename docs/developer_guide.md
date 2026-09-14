# Contributing and local development

This repository keeps development lightweight and Python-first.

## Setup

```bash
uv sync
```

## Run the quality checks

```bash
uv run ruff check .
uv run pytest
uv run mkdocs build --strict
```

## Preview the book locally

```bash
uv run mkdocs serve
```

## Editing guidance

- Preserve synthetic, fictional framing.
- Prefer revising or reorganizing working material over deleting it.
- Keep Project Frog as the recurring teaching environment.
- Connect any new metric discussion back to uncertainty, population, assumptions, and decisions.

A repository-level contributor summary is also available in `CONTRIBUTING.md`.
