# Why this book exists

## The engineering problem behind the book

AI teams rarely fail because they cannot calculate a metric. They fail because they trust a metric before understanding what population it summarizes, how noisy it is, whether the evaluation is comparable, and what decision the result is supposed to support.

A reported gain from 84% to 86% may be a real improvement, or it may reflect sampling noise, slice drift, leakage, dependence, label changes, or a shift in error concentration on the cases that matter most. The same point estimate can support different actions when the consequences of error are different.

## What trustworthy evaluation means here

In this book, an evaluation is trustworthy only when the following questions are answered together:

1. **Meaning** — what exactly does the metric measure?
2. **Uncertainty** — how variable is the estimate under realistic re-sampling?
3. **Population** — which synthetic Project Frog cases does it represent?
4. **Assumptions** — what independence, labeling, and stationarity assumptions are required?
5. **Decision link** — what choice changes because of the result?

## Narrative structure

The book moves from foundations to metrics, then to evaluation design, and finally to decisions and monitoring:

- **Part I** rebuilds the statistical concepts engineers actually use.
- **Part II** connects those concepts to classification metrics and model comparison.
- **Part III** focuses on whether an evaluation deserves to be compared at all.
- **Part IV** connects evidence to release decisions, monitoring, and ongoing accountability.

## Working principle

Every chapter begins from an engineering question instead of a formula-first presentation. The math is there because the decisions require it, not because the notation is the goal.
