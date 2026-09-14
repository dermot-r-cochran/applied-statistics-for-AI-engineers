# Different Pond

## Scenario
Original synthetic evaluation mix: **70% simple / 20% medium / 10% complex**. New evaluation mix: **40% simple / 30% medium / 30% complex**.

## Questions to answer
- Are the results comparable?
- Has dataset shift occurred?
- Should weighting be considered?
- What assumptions are required?

## Concepts to practice
- sampling bias
- distribution shift
- representativeness
- weighting

## Engineering discussion
Even if the model stayed constant, a harder evaluation mix could lower the observed headline metric. Engineers should compare slice-level performance, decide which population they actually want to represent, and consider reweighting only when the required assumptions are credible. A changed mix can be the entire story behind an apparent regression.

## What to inspect next
- slice metrics by difficulty level
- target population weights for reporting
- whether the sampling frame changed intentionally or accidentally
- whether the hard cases are more operationally relevant than the easy ones

## Trust prompts
- What exactly is being compared?
- What uncertainty is missing or understated?
- What population mismatch could invalidate the result?
- What decision would be premature here?
