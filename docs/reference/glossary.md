# Glossary

## Abstention
A policy that withholds an automated decision and routes the case for review.

## Brier score
The mean squared error between predicted probabilities and binary outcomes.

## Calibration
Agreement between predicted probabilities and observed frequencies for a defined event and population.

## Calibration drift
A change in calibration behavior when the deployment population differs from the calibration population.

## Conditional dependence
A setting where component failures remain related even after accounting for observed covariates.

## Confidence semantics
The operational meaning attached to a score, including what event it targets and what assumptions it requires.

## End-to-end correctness
Whether the final system output is correct for the decision that matters.

## Expected calibration error
A binned summary of calibration gaps. It is useful but incomplete because it depends on the chosen bins and hides subgroup failures.

## Reliability diagram
A plot comparing mean predicted score with observed event frequency across bins.

## Selective prediction
Prediction with an option to abstain on cases judged too uncertain for automation.

## Subgroup calibration
Calibration evaluated separately for meaningful subpopulations instead of only in aggregate.
