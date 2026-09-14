# Classification Metrics

## Why does an AI engineer need to understand this?
AI engineers need more than a single accuracy number because different failure modes create different operational costs. A trustworthy evaluation starts with choosing metrics that align with the system's decisions.

## 1. Engineering Problem
Project Frog classifies documents for downstream recommendations and compliance decisions. The problem is selecting metrics that distinguish missing risky cases from over-triggering unnecessary reviews.

## 2. Intuition
Metric intuition begins with the confusion matrix. Accuracy summarizes overall correctness, while precision, recall, F1, and coverage highlight different trade-offs.

## 3. Mathematical Foundation
Define confusion matrix entries and derive common metrics from them. Explain why class imbalance and asymmetric error costs make metric choice a design decision rather than a reporting preference.

## 4. Python Example
Build a synthetic confusion matrix for Project Frog and compute several metrics in Python. Show how the same accuracy can hide very different precision and recall behavior.

## 5. Interpretation
Interpret each metric relative to a decision. High recall may matter most when missed risky cases are costly, while precision may matter most when manual review capacity is scarce.

## 6. Common Mistakes
Mistakes include optimizing a metric without checking whether it matches the deployment objective, mixing macro and micro averages carelessly, and ignoring threshold dependence.

## 7. AI Engineering Applications
Use these metrics for model selection, alerting, audit programs, and communication with reviewers. Good measurement starts by choosing the right summary for the decision.

## 8. Exercises
Create two synthetic confusion matrices with similar accuracy but different review cost implications. Explain which metric tells the more decision-relevant story.

## 9. Further Reading
Further reading should cover metric selection under imbalance, threshold analysis, and calibration-aware evaluation.
