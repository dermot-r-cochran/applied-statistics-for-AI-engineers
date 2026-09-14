# Contributing

## Setup

```bash
uv sync
```

## Validate changes

```bash
uv run ruff check .
uv run pytest
uv run mkdocs build --strict
```

## Preview the book

```bash
uv run mkdocs serve
```

## Content rules

- Keep every example synthetic and fictional.
- Use Project Frog as the recurring case study.
- Prefer revising useful material over deleting it.
- Connect metrics to uncertainty, population, assumptions, and decisions.
