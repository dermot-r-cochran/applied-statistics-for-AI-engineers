# Frog Leap

## Scenario
Project Frog version A reports **84%** accuracy and version B reports **86%** accuracy on synthetic evaluation data.

## Questions to answer
- Is the difference meaningful?
- Is it statistically detectable?
- Is it operationally important?
- Should deployment decisions change?

## Concepts to practice
- effect size
- hypothesis testing
- statistical significance
- practical significance

## Engineering discussion
A two-point lift might be important or trivial depending on sample size, disagreement concentration, and the cost of errors. Engineers should estimate the difference with uncertainty, ask whether the models were compared on the same examples, and translate the lift into expected downstream impact such as avoided incorrect recommendations per thousand decisions.

## What to inspect next
- confidence interval for the difference
- p-value or equivalent evidence summary from a paired comparison
- disagreement pattern by case complexity
- latency or cost changes introduced by version B
- minimum practical improvement required to justify deployment

## Trust prompts
- What exactly is being compared?
- What uncertainty is missing or understated?
- What population mismatch could invalidate the result?
- What decision would be premature here?
