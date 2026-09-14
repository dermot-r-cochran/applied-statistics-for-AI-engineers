---
hide:
  - toc
---

# Trustworthy AI Evaluation

## Experimental Design, Metrics, Confidence, and Decision-Making for AI Engineers

> **Central question:** When should an engineer trust an observed AI metric?
>
> **Central thesis:** An AI metric is useful only when its meaning, uncertainty, population, assumptions, and relationship to a decision are understood.

Trustworthy AI Evaluation is a book-style GitHub Pages site and Python repository for experienced engineers who need to make defensible decisions from AI evaluation results.

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle } **What this book teaches**

    ---

    How to design, critique, interpret, and communicate evaluations for synthetic AI systems without separating metrics from uncertainty, assumptions, or decision risk.

-   :material-flask-outline:{ .lg .middle } **How it teaches**

    ---

    Through Project Frog: a continuous fictional case study built from synthetic datasets, reproducible Python examples, reusable utilities, notebooks, and decision-focused exercises.

-   :material-chart-box-outline:{ .lg .middle } **What readers should leave with**

    ---

    Better judgment about whether a metric movement is noise or signal, whether a sample is representative, and whether the evidence supports shipping, delaying, or measuring more.

</div>

## Purpose

This repository exists to help software engineers, machine learning engineers, AI engineers, test architects, data scientists, and technical leads make technically serious evaluation decisions without pretending that a dashboard point estimate is enough.

## Audience

This book assumes the reader:

- is proficient in Python
- already understands common machine learning concepts and metrics
- has seen probability and statistics before, but wants the important ideas reactivated in an engineering setting
- is responsible for interpreting evidence, not just producing numbers

## Learning outcomes

By the end, readers should be able to answer:

1. Is this metric change likely noise or signal?
2. How much uncertainty exists in this result?
3. Is the sample representative of the decision context?
4. Are two evaluations actually comparable?
5. Which assumptions are carrying the conclusion?
6. What additional evidence would materially reduce uncertainty?
7. What is the correct unit of inference?
8. How should uncertainty be communicated to stakeholders?
9. When is statistical significance insufficient?
10. What action is justified by the current evidence?

## How to use this repository

- Read the book chapters in order if you want a full conceptual foundation.
- Jump to the practical workshops if you want notebooks and case studies first.
- Use the `applied_stats_ai` package for the reusable interval, bootstrap, comparison, power, sampling, and synthetic-data helpers.
- Run the tests and examples locally so every lesson stays reproducible.

## Repository shape

```text
.
├── docs/                 # book chapters and site landing pages
├── tutorials/            # notebooks and case studies surfaced in the site
├── examples/             # runnable synthetic scripts
├── src/applied_stats_ai/ # reusable Python utilities
├── tests/                # pytest coverage
├── mkdocs.yml            # book/site configuration
└── .github/workflows/    # Pages publishing workflow
```

## Confidentiality and fictionalization

All examples in this repository are synthetic and fictional. Project Frog is a teaching environment only. The guiding rule is: **generalize the lesson, not the implementation**.
