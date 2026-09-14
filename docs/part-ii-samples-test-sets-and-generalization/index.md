# Part II: Samples, Test Sets, and Generalization

Evaluation quality depends on what was sampled, how representative it is, and whether the evidence remains comparable over time.

## What this part does

This part establishes the main questions, failure modes, and decision responsibilities for the chapters that follow.

## Chapters in this part

- [4. The Shrinking Pond](04-the-shrinking-pond.md) — A smaller evaluation sample makes observed results noisier, but it does not by itself prove that the underlying system became worse.
- [5. Is the Pond Representative?](05-is-the-pond-representative.md) — Sample size and representativeness are different properties; a large but skewed test set can mislead more than a small but well-targeted one.
- [6. The Tadpole Problem](06-the-tadpole-problem.md) — Counting rows as independent evidence can wildly overstate certainty when many observations come from the same documents, projects, or other shared sources.
- [7. Test-Set Governance](07-test-set-governance.md) — Reliable evaluation requires governed datasets: documented purpose, controlled updates, protected holdouts, and explicit rules for when comparisons remain valid.

## Throughline

Project Frog reappears across these chapters so ideas connect through one synthetic workflow rather than isolated examples.
