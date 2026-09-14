# Chapter 20. Bootstrap, Permutation, and Simulation

Resampling methods are useful because they can align uncertainty estimation with complex metrics and sampling designs, but each method has assumptions that can be violated easily.

**In-part navigation:** Previous: [19. Power and Sample-Size Planning](19-power-and-sample-size-planning.md) · Part overview: [Overview](index.md)

## Why this chapter matters

Resampling methods are useful because they can align uncertainty estimation with complex metrics and sampling designs, but each method has assumptions that can be violated easily.

## Section outline
1. **Contrast ordinary bootstrap, paired bootstrap, cluster bootstrap, permutation tests, and simulation** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Match each method to the right data-generating assumptions** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Explain common invalid resampling shortcuts** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Use resampling to stress-test decision robustness** — Outline material to be expanded into narrative text, examples, and decision guidance.
1. **Summarize when analytic formulas remain preferable** — Outline material to be expanded into narrative text, examples, and decision guidance.

## Key questions

- Which resampling unit should be preserved to respect dependence?
- What null hypothesis does this permutation design actually encode?
- When is simulation the clearest way to communicate uncertainty?


## Engineering interpretation

Choose resampling methods that mirror the data structure and decision question. Document what is resampled, what is held fixed, and what failures the method cannot detect.

## Project Frog integration

Project Frog uses synthetic clustered cases to compare row-level bootstrap, cluster bootstrap, and paired permutation workflows under realistic dependency patterns.

## Future examples and tutorials

- _Placeholder_: Worked Python example: cluster bootstrap versus naïve bootstrap
- _Placeholder_: Visualization: sampling distributions under different resampling choices

## Related chapters and reference material

- [Chapter 4: The Shrinking Pond](../part-ii-samples-test-sets-and-generalization/04-the-shrinking-pond.md)
- [Confidence-interval selection guide](../appendices/confidence-interval-selection-guide.md)
- [Experiment protocol template](../appendices/experiment-protocol-template.md)


## Summary

Resampling is powerful when it matches the design. Misaligned resampling can manufacture certainty just as easily as it can reveal it.
