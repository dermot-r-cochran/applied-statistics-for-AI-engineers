# Trustworthy AI Evaluation

Welcome to the working book site for **Trustworthy AI Evaluation**. This repository turns an applied-statistics codebase into a book-shaped reference for AI engineers who need to make defensible decisions from imperfect evidence.

## What this site contains

- A six-part navigation that moves from measurement design to release decisions.
- Structured chapter outlines for all 24 planned chapters.
- Appendix and reference pages for reusable evaluation artifacts.
- A continuous fictional case study, **Project Frog**, used to connect ideas across parts.

## Project Frog

Project Frog is a fully fictional AI document-triage pipeline used throughout the book. It uses synthetic identifiers such as `project_id`, `document_id`, and `case_id`, plus fictional classes (`Clear`, `Review`, `Insufficient`, `Escalate`) and difficulty groups (`Simple`, `Moderate`, `Complex`).

All future worked examples in this repository should remain synthetic and reproducible. Fixed random seeds can make examples repeatable, but they do **not** remove sampling uncertainty.

## Reading paths

### First-pass narrative

A compact first reading path runs through:

1. [The Metric Is Not the System](part-i-what-are-we-measuring/01-the-metric-is-not-the-system.md)
2. [The Shrinking Pond](part-ii-samples-test-sets-and-generalization/04-the-shrinking-pond.md)
3. [Accuracy and Its Discontents](part-iii-choosing-and-interpreting-metrics/08-accuracy-and-its-discontents.md)
4. [What Does Confidence Mean?](part-iv-confidence-across-ai-pipelines/12-what-does-confidence-mean.md)
5. [Combining Confidence Scores](part-iv-confidence-across-ai-pipelines/14-combining-confidence-scores.md)
6. [Start with the Decision](part-v-experimental-design/16-start-with-the-decision.md)
7. [Release Readiness Under Uncertainty](part-vi-from-evidence-to-decisions/21-release-readiness-under-uncertainty.md)

This path follows the intended narrative:

**decision → measurement → sampling uncertainty → metric interpretation → component confidence → experimental design → release decision**

### Full-book route

Use the left navigation to move through the complete part/chapter structure in book order.

## Editorial status

This stage establishes coherent chapter scaffolds: why each chapter matters, the concepts it will teach, the Project Frog angle, and the artifacts or examples that should be added next.
