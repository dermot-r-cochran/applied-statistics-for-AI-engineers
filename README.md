# Trustworthy AI Evaluation

Applied Statistics and Metrics for AI Engineers, rebuilt as a practical book-style GitHub Pages site.

## Current book pages

- `intro.md`
- `tutorials/project-frog-progressive-evaluation.md`
- `chapters/the-metric-is-not-the-system.md`
- `chapters/what-does-confidence-mean.md`
- `chapters/release-readiness-under-uncertainty.md`

## Local build

Use an environment where the `jb` script from the `jupyter-book` install is on `PATH`.


```bash
python -m pip install -r requirements.txt
jb build . -W
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
