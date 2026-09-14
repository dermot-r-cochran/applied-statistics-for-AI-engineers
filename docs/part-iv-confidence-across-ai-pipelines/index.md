# Part IV: Confidence Across AI Pipelines

Confidence scores are only meaningful when their semantics, calibration, comparability, and end-to-end validation are explicit.

## What this part does

This part establishes the main questions, failure modes, and decision responsibilities for the chapters that follow.

## Chapters in this part

- [12. What Does Confidence Mean?](12-what-does-confidence-mean.md) — Equal numeric scales do not imply equal meaning: two scores of 0.90 can represent different events, data-generating processes, and decisions.
- [13. Calibration](13-calibration.md) — Calibration asks whether stated confidence aligns with observed frequencies, but no single summary statistic captures every calibration concern.
- [14. Combining Confidence Scores](14-combining-confidence-scores.md) — There is no universal formula for combining component scores; every composition rule inherits semantic assumptions, dependence assumptions, and validation obligations.
- [15. System-Level Trust Is Not the Average of Component Confidence](15-system-level-trust-is-not-the-average-of-component-confidence.md) — End-to-end trust must be evaluated against end-to-end outcomes because dependencies, cascades, and handoffs can break any naïve inference from component scores.

## Throughline

Project Frog reappears across these chapters so ideas connect through one synthetic workflow rather than isolated examples.
