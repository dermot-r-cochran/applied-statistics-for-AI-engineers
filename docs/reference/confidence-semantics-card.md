# Confidence semantics card

Use this card before comparing, averaging, multiplying, thresholding, or operationalizing any confidence-like score.

## Reusable template

| Field | Guidance |
| --- | --- |
| Score name | Name used in code, dashboards, and documentation |
| Producing component | Which model or subsystem emits the score |
| Intended meaning | What event, property, or ranking signal the score is supposed to represent |
| Mathematical range | Numeric bounds and whether the scale is bounded or open |
| Generation method | Model output, heuristic, ranking margin, rule-based score, or learned estimate |
| Whether it claims to be a probability | Yes, no, or only after calibration |
| Calibration method | None, isotonic, Platt, temperature scaling, empirical mapping, or other |
| Calibration population | Dataset, time period, and subgroup coverage used for calibration |
| Dependency assumptions | Conditional independence, shared upstream data, known coupling, or no assumption |
| Known failure modes | Cases where the score looks strong but is misleading |
| Valid comparisons | What the score can be compared against without semantic distortion |
| Invalid interpretations | Common but invalid readings of the score |
| Supported decisions | Decisions the score can support after validation |
| Unsupported decisions | Decisions the score must not support on its own |

## Project Frog cards

### Document extraction

| Field | Value |
| --- | --- |
| Score name | Extraction quality index |
| Producing component | Document extraction |
| Intended meaning | Heuristic estimate that required fields were extracted cleanly enough to proceed |
| Mathematical range | 0 to 1 |
| Generation method | OCR completeness, parser stability, and field-coverage heuristics |
| Whether it claims to be a probability | No |
| Calibration method | Isotonic mapping to extraction success for descriptive analysis |
| Calibration population | Synthetic development cases with milder difficulty mix |
| Dependency assumptions | Similar extraction quality implies similar downstream usability |
| Known failure modes | Template-like scans with systematic field swaps |
| Valid comparisons | Same extraction pipeline, same rubric, same population |
| Invalid interpretations | “0.90 means the whole case is 90% correct” |
| Supported decisions | Re-scan, proceed, or route to review |
| Unsupported decisions | End-to-end trust judgment |

### Classification

| Field | Value |
| --- | --- |
| Score name | Class confidence |
| Producing component | Classification |
| Intended meaning | Estimated probability that the predicted class is correct |
| Mathematical range | 0 to 1 |
| Generation method | Softmax-like classifier output |
| Whether it claims to be a probability | Yes |
| Calibration method | Isotonic regression on the synthetic development split |
| Calibration population | Synthetic development cases that under-sample complex examples |
| Dependency assumptions | Similar extraction quality and difficulty imply similar error rates |
| Known failure modes | Overconfidence on ambiguous cases |
| Valid comparisons | Same classifier family after drift checks |
| Invalid interpretations | “Equivalent to the retrieval score because both are 0 to 1” |
| Supported decisions | Abstain, review, or accept class prediction |
| Unsupported decisions | Whole-system release decision without end-to-end validation |

### Evidence retrieval

| Field | Value |
| --- | --- |
| Score name | Retrieval relevance margin |
| Producing component | Evidence retrieval |
| Intended meaning | Margin between the best and second-best evidence candidate |
| Mathematical range | 0 to 1 |
| Generation method | Normalized ranking-margin statistic |
| Whether it claims to be a probability | No |
| Calibration method | Isotonic mapping to evidence relevance for descriptive analysis |
| Calibration population | Synthetic development queries on the same fictional corpus |
| Dependency assumptions | Same query formulation and corpus state |
| Known failure modes | High margin when all retrieved passages are consistently wrong |
| Valid comparisons | Same retriever and same corpus snapshot |
| Invalid interpretations | “0.90 means 90% chance the answer is correct” |
| Supported decisions | Broaden retrieval or route to human search |
| Unsupported decisions | Direct multiplication with classifier confidence |

### Explanation generation

| Field | Value |
| --- | --- |
| Score name | Explanation self-check score |
| Producing component | Explanation generation |
| Intended meaning | Internal consistency score for rationale quality and format adherence |
| Mathematical range | 0 to 1 |
| Generation method | Self-consistency and rubric matching |
| Whether it claims to be a probability | No |
| Calibration method | Isotonic mapping to explanation adequacy for descriptive analysis |
| Calibration population | Synthetic development split with shorter explanations than evaluation |
| Dependency assumptions | Template conformity is informative about adequacy |
| Known failure modes | Polished but unsupported rationales |
| Valid comparisons | Same explanation model and rubric version |
| Invalid interpretations | “A high score proves the system is trustworthy” |
| Supported decisions | Ask for a stronger rationale or human review |
| Unsupported decisions | Final automation trust estimate |

## Interpretation rule

If two cards differ on **intended meaning**, **probability claim**, **calibration population**, or **dependency assumptions**, do not treat the scores as directly interchangeable.
