# Confidence semantics card

Use this card before comparing or combining scores from different components.

| Field | Guidance |
| --- | --- |
| Score name | Name the score exactly as exposed in code or reports |
| Producing component | Which component emits it |
| Intended meaning | What the score is supposed to mean |
| Mathematical range | Numeric range and whether bounds are closed |
| Generation method | Logit, ranker score, heuristic score, calibrated model output, or other mechanism |
| Whether it claims to be a probability | Yes, no, or only after calibration |
| Calibration method | Platt scaling, isotonic regression, temperature scaling, none, or other |
| Calibration population | Which population was used for calibration |
| Dependency assumptions | Independence or conditional assumptions required downstream |
| Known failure modes | When the score becomes misleading |
| Valid comparisons | Which other scores can be compared directly |
| Invalid interpretations | Common unsupported claims |
| Supported decisions | Decisions this score can inform |
| Unsupported decisions | Decisions this score must not drive alone |

## Project Frog examples

| Score name | Producing component | Intended meaning | Claims probability? | Valid comparisons | Unsupported decisions |
| --- | --- | --- | --- | --- | --- |
| `raw_confidence` | Classification | Internal model confidence before calibration | No | Within the same model family and population | Release decisions by itself |
| `calibrated_probability` | Classification | Estimated probability of correct classification on the calibration population | Yes | Against the same target event on comparable data | Comparison with retrieval rank scores |
| `evidence_relevance` | Evidence retrieval | Relative usefulness of retrieved evidence | No | Ranking within the same retrieval setting | Multiplying with class probability as if both were probabilities |
