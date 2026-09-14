# Confidence-related reference material

## Confidence semantics card

- **Score name**
- **Producing component**
- **Intended meaning**
- **Mathematical range**
- **Generation method**
- **Whether it claims to be a probability**
- **Calibration method**
- **Calibration population**
- **Dependency assumptions**
- **Known failure modes**
- **Valid comparisons**
- **Invalid interpretations**
- **Supported decisions**
- **Unsupported decisions**

## Project Frog component reminder

Project Frog’s synthetic pipeline contains four components:

1. Document extraction
2. Classification
3. Evidence retrieval
4. Explanation generation

Each component may emit a 0-1 score, but [Chapter 12](../part-iv-confidence-across-ai-pipelines/12-what-does-confidence-mean.md) and [Chapter 14](../part-iv-confidence-across-ai-pipelines/14-combining-confidence-scores.md) explain why matching scales do not guarantee matching semantics.

## Composition review prompts

- What event does each score refer to?
- Are any of the scores calibrated probabilities in the same population?
- Which dependencies would make a product or average misleading?
- Would a risk category or abstention policy communicate the evidence better than a single number?
- What end-to-end validation supports the final interpretation?
