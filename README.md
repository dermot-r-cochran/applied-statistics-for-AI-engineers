# applied-statistics-for-AI-engineers

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
