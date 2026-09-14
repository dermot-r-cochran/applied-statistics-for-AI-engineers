# Project Frog synthetic data

Project Frog is the fictional running example used across this repository.

## Synthetic-only guarantee

All Project Frog data are synthetic, fictional, reproducible, and generated locally by `scripts/generate_assets.py`. No confidential, proprietary, or real-user content is included.

## Stable schema

| Field | Meaning |
| --- | --- |
| `project_id` | Synthetic project identifier |
| `document_id` | Synthetic document identifier |
| `case_id` | Synthetic case identifier |
| `difficulty` | `Simple`, `Moderate`, or `Complex` |
| `predicted_class` | Fictional predicted class |
| `reference_class` | Fictional reference class |
| `prediction_correct` | Whether the prediction matches the reference class |
| `component_name` | Producing component |
| `raw_confidence` | Component-native score between 0 and 1 |
| `calibrated_probability` | Post-calibration probability estimate between 0 and 1 |
| `evidence_relevance` | Synthetic relevance signal used in retrieval and explanation examples |
| `processing_latency` | Synthetic latency in milliseconds |
| `processing_cost` | Synthetic per-case cost in USD |

## Allowed labels

- Classes: `Clear`, `Review`, `Insufficient`, `Escalate`
- Difficulty groups: `Simple`, `Moderate`, `Complex`
- Components:
  - Document extraction
  - Classification
  - Evidence retrieval
  - Explanation generation

## Reproducibility

The default generator seed is `20260914`.

```python
from trustworthy_ai_evaluation.synthetic import generate_project_frog_data

data = generate_project_frog_data(seed=20260914)
print(data.head())
```

Fixed seeds support reproducibility, but they do **not** remove [sampling uncertainty](../glossary.md#sampling-uncertainty). A reproducible synthetic sample is still one sample.

## Generated artifacts

- `data/synthetic/project_frog_synthetic.csv`
- `data/synthetic/project_frog_component_summary.csv`
- `data/synthetic/reading_path_metrics.txt`
