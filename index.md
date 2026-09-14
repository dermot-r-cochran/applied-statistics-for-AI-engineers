# Trustworthy AI Evaluation

*Experimental Design, Metrics, Confidence, and Decision-Making for AI Engineers*

```{admonition} Central question
:class: note
When should an engineer trust an observed AI metric?
```

```{admonition} Central thesis
:class: important
An AI metric is useful only when its meaning, uncertainty, population, assumptions, and relationship to a decision are understood.
```

## Why this book exists

AI teams regularly make consequential decisions from evaluation reports, dashboards, regressions, benchmark tables, experiments, and monitoring signals. The numbers often look precise. The reasoning behind them is usually less precise.

This book is for engineers who already know how to build AI systems, but who need a sharper framework for deciding whether an observed difference is noise, signal, bias, leakage, drift, measurement error, or evidence strong enough to act on.

The goal is not to turn every reader into a statistician. The goal is to make readers statistically dangerous in the best sense: able to question assumptions, quantify uncertainty, detect invalid comparisons, and communicate what the evidence does and does not support.

## What you will learn

By the end of the book, you should be able to:

1. Define the decision before interpreting the metric.
2. Identify the unit of inference and the target population.
3. Quantify uncertainty instead of reporting point estimates alone.
4. Distinguish statistical detectability from practical importance.
5. Recognize when two evaluations are not truly comparable.
6. Diagnose sampling bias, leakage, dependence, and dataset shift.
7. Decide what additional evidence would materially reduce uncertainty.
8. Communicate evaluation results in a form decision-makers can trust.

## How the material is organized

The book combines four layers:

- **Decision framing** pages that explain what must be true before a metric can support action.
- **Core chapters** covering probability, intervals, tests, power, metrics, experiments, sampling, measurement, and monitoring.
- **Project Frog case studies** that practice release and evaluation decisions in realistic fictional scenarios.
- **Reusable Python utilities, examples, tests, and notebooks** that let readers inspect the calculations directly.

## Synthetic-only teaching environment

Everything in this repository is synthetic and fictional. Examples are intentionally designed to teach recurring engineering patterns without describing any real organization, product, customer, dataset, pipeline, or internal framework.

Project Frog is the continuous case study used across the book. It is a fictional AI-assisted document analysis and decision-support platform that emits synthetic classifications, extracted fields, evidence, explanations, recommendations, decisions, latency measures, and cost measures.

## Suggested reading paths

- If you need to interpret a regression report, start with {doc}`book/decision_framework`, then {doc}`docs/03_confidence_intervals`, {doc}`docs/10_metric_uncertainty`, and {doc}`docs/11_model_comparison`.
- If you design evaluations, follow {doc}`docs/12_experimental_design`, {doc}`docs/14_test_set_design`, {doc}`docs/15_sampling_bias`, and {doc}`docs/16_data_leakage`.
- If you own launch decisions, read {doc}`docs/18_decision_theory` and the Project Frog case studies.
- If you want executable material first, jump to the tutorials and notebooks.
