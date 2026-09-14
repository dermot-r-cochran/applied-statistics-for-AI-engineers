# Trustworthy AI Evaluation

This repository is being developed as the **Trustworthy AI Evaluation** book site.

## Book structure

The site is organized as a six-part book:

1. **What Are We Measuring?**
2. **Samples, Test Sets, and Generalization**
3. **Choosing and Interpreting Metrics**
4. **Confidence Across AI Pipelines**
5. **Experimental Design**
6. **From Evidence to Decisions**

It also includes appendix and reference pages for glossary terms, metric and interval guides, evaluation checklists, and reusable templates.

## Case study rules

The book uses **Project Frog** as a continuous fictional case study. All examples are synthetic, reproducible where code is later introduced, and free of internal or proprietary references.

## Local development

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

## Validation

Build the site in strict mode before publishing changes:

```bash
mkdocs build --strict
```

## Repository goal

The current phase focuses on establishing complete navigation and structured chapter outlines so future drafting, examples, and tutorials can extend the book coherently.
