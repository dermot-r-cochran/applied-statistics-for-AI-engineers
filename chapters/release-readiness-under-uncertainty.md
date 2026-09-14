# Release Readiness Under Uncertainty

Release decisions should be tied to evidence quality, uncertainty bounds, and the cost of being wrong.

## Project Frog framing

For Project Frog, a release target such as 90% accuracy is incomplete without asking:

- how many cases were evaluated,
- which kinds of cases were represented,
- how wide the uncertainty interval is, and
- what happens if failures reach production.

## Use with the tutorial

The [interactive Project Frog tutorial](../tutorials/project-frog-progressive-evaluation.md) ends with a release-style interpretation that shows why evidence can be practical yet still incomplete.

## Evidence categories

- Evidence supports release
- Evidence supports release with caveats
- Evidence is insufficient
- Evidence indicates release risk
