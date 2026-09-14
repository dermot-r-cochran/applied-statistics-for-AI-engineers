# What Does Confidence Mean?

Equal numeric scales do not imply equal meaning. A score of `0.90` can represent very different claims depending on the component that produced it.

## Project Frog framing

Project Frog can emit synthetic component scores for extraction, classification, retrieval, and explanation. Those values may look comparable while being generated from different populations, assumptions, and calibration states.

## Use with the tutorial

The [interactive Project Frog tutorial](../tutorials/project-frog-progressive-evaluation.md) uses one system-level evaluation slice. Read this chapter alongside it to separate confidence semantics from decision thresholds.

## Key reminders

- Ask what a score is intended to mean.
- Check whether the score claims to estimate a probability.
- Validate confidence against end-to-end outcomes before using it for release decisions.
