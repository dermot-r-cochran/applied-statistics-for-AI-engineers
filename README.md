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
```
