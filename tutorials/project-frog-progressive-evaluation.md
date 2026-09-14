# Project Frog: a progressive evaluation walkthrough

## Why this page exists

Project Frog is a fictional engineering workflow that triages incoming case files into one of four outcomes:

- `Clear`
- `Review`
- `Insufficient`
- `Escalate`

The practical problem is simple: **can a team trust one benchmark snapshot enough to make an operational decision?**

This tutorial walks through that question in stages so readers can move from intuition to method to interpretation.

```{figure} ../assets/project-frog-progressive-flow.svg
:name: project-frog-progressive-flow
:alt: Progressive Project Frog evaluation flow from operational decision to sample review, error analysis, uncertainty, and release interpretation.
:width: 100%

A progressive learning path for evaluating Project Frog.
```

```{admonition} What you will practice
:class: note

By the end of this page, you should be able to:

1. describe what the evaluation sample actually contains,
2. spot where aggregate metrics hide operational risk,
3. compute and interpret uncertainty intervals, and
4. translate evidence into a cautious engineering decision.
```

## Step 1 — Start with the decision

Imagine a Project Frog release review. The team wants to know whether the current model is good enough to reduce manual triage load without creating too many missed escalations.

That means the real decision is not “what is the accuracy?” but **“what evidence would justify shipping this workflow with confidence?”**

```{dropdown} Checkpoint question
If the benchmark says `88%` accuracy, what is still missing before you decide to release?

A strong answer mentions the sample composition, the cost of specific mistakes, subgroup behavior, and uncertainty around the estimate.
```

## Step 2 — Inspect the synthetic evaluation slice

All examples on this page are synthetic, fictional, and reproducible. They use a fixed random seed for repeatability, but that does **not** remove sampling uncertainty.

```{code-cell} python3
from tutorial_examples import difficulty_summary, generate_project_frog_cases

cases = generate_project_frog_cases(seed=7, n=36)
summary = difficulty_summary(cases)
for difficulty, values in summary.items():
    print(f"{difficulty}: cases={int(values['cases'])}, accuracy={values['accuracy']:.3f}")
```

A small evaluation slice is enough to demonstrate the workflow:

| Difficulty | Cases | Accuracy |
| --- | ---: | ---: |
| Simple | 18 | 0.94 |
| Moderate | 12 | 0.83 |
| Complex | 6 | 0.67 |

The engineering lesson is immediate: the aggregate can look healthy while the hard cases remain fragile.

```{admonition} Reflection
:class: important

If your production workload shifted toward `Complex` cases next month, would the current aggregate still be a good summary of operational risk?
```

## Step 3 — Move from intuition to a method

The next step is to quantify the observed result and its uncertainty.

```{code-cell} python3
from tutorial_examples import overall_accuracy, wilson_interval

accuracy = overall_accuracy(cases)
successes = sum(case.prediction_correct for case in cases)
interval = wilson_interval(successes=successes, total=len(cases))
print(round(accuracy, 3), tuple(round(x, 3) for x in interval))
```

The executed cell shows the current observed accuracy and Wilson interval for this synthetic slice.

That range is the practical message. It reminds the team that a single measured value is not the same thing as a fixed, known system property.

```{dropdown} Why Wilson here?
Wilson intervals are usually more stable than the simple Wald interval, especially for smaller samples or when observed performance is close to 0 or 1.
```

## Step 4 — Interpret errors in operational terms

Project Frog is not just predicting labels. It is routing work.

A missed `Escalate` case is usually more serious than a `Clear` versus `Review` mix-up, so the team should read the confusion pattern before celebrating the top-line metric.

```{code-cell} python3
from tutorial_examples import class_error_table

print(class_error_table(cases))
```

A practical reading pattern is:

- verify whether `Escalate` errors are rare enough for the proposed workflow,
- check whether `Insufficient` cases are being over-cleared,
- review whether difficult cases dominate the observed failures.

## Step 5 — Turn evidence into a release-style interpretation

Now connect the metric back to the operational question.

```{code-cell} python3
from tutorial_examples import release_recommendation

print(release_recommendation(accuracy=accuracy, interval=interval, target=0.85))
```

The executed cell returns the current synthetic recommendation for a modest pilot-style target.

Why not a stronger claim?

- the point estimate clears a modest pilot target,
- the lower bound leaves room for materially weaker performance,
- the hardest cases are clearly less reliable.

```{admonition} Common incorrect interpretation
:class: caution

“The model scored about 86%, so the system is basically 86% reliable.”
```

```{admonition} Corrected interpretation
:class: tip

“This sample observed about 86% accuracy, but the plausible performance range is wider, case difficulty matters, and release confidence should depend on the consequences of the failures that remain.”
```

## Step 6 — Extend the workflow yourself

```{dropdown} Try these next questions
1. What happens to the release recommendation if the sample doubles but the error pattern stays similar?
2. What if the next benchmark contains far more `Complex` cases?
3. Which mistakes would justify automatic abstention or human review instead of a full release?
```

## Practical checkpoints

- Can you explain why a fixed seed improves reproducibility but not certainty?
- Can you name at least one way the sample might fail to represent production?
- Can you explain why uncertainty belongs in the release discussion?
- Can you describe one error type that matters more than overall accuracy?

## Related chapters

- [The Metric Is Not the System](../chapters/the-metric-is-not-the-system.md)
- [What Does Confidence Mean?](../chapters/what-does-confidence-mean.md)
- [Release Readiness Under Uncertainty](../chapters/release-readiness-under-uncertainty.md)

## Concise summary

Project Frog shows why practical AI evaluation should start with the decision, inspect the sample, measure uncertainty, and only then translate evidence into action. The metric is useful, but the release judgment depends on what the errors mean.
