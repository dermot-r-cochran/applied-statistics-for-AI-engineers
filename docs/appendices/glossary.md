# Glossary

This glossary anchors the core language used throughout the book. Each entry points back to the chapters where the concept is introduced or applied most directly.

## Core terms

- **Calibration** — The alignment between stated confidence and observed frequency. See [Chapter 13](../part-iv-confidence-across-ai-pipelines/13-calibration.md).
- **Comparability** — The degree to which two evaluation results can be interpreted side by side. See [Chapter 17](../part-v-experimental-design/17-fair-model-comparisons.md).
- **Confidence interval** — A range produced by a stated procedure to summarize estimation uncertainty. See [Chapter 4](../part-ii-samples-test-sets-and-generalization/04-the-shrinking-pond.md).
- **Confidence semantics** — The explicitly documented meaning of a score, including the event it refers to and the decisions it supports. See [Chapter 12](../part-iv-confidence-across-ai-pipelines/12-what-does-confidence-mean.md).
- **Ground truth** — Reference labels used for evaluation, treated here as outputs of a measurement process. See [Chapter 3](../part-i-what-are-we-measuring/03-ground-truth-is-a-measurement-too.md).
- **Minimum meaningful effect** — The smallest change that would justify action. See [Chapter 18](../part-v-experimental-design/18-effect-size-before-significance.md).
- **Representative sample** — A sample that supports the intended population claim because the relevant conditions are covered appropriately. See [Chapter 5](../part-ii-samples-test-sets-and-generalization/05-is-the-pond-representative.md).
- **Selective prediction** — A system behavior in which the model abstains or escalates rather than always producing a final answer. See [Chapter 15](../part-iv-confidence-across-ai-pipelines/15-system-level-trust-is-not-the-average-of-component-confidence.md).
- **Target population** — The set of cases the evaluation intends to say something about. See [Chapter 5](../part-ii-samples-test-sets-and-generalization/05-is-the-pond-representative.md).
- **Unit of inference** — The level at which conclusions are intended, such as row, document, project, or deployment period. See [Chapter 6](../part-ii-samples-test-sets-and-generalization/06-the-tadpole-problem.md).

## Project Frog data model

The fictional Project Frog case study reuses this stable synthetic schema:

- `project_id`
- `document_id`
- `case_id`
- `difficulty`
- `predicted_class`
- `reference_class`
- `prediction_correct`
- `component_name`
- `raw_confidence`
- `calibrated_probability`
- `evidence_relevance`
- `processing_latency`
- `processing_cost`

Allowed synthetic classes are `Clear`, `Review`, `Insufficient`, and `Escalate`; allowed difficulty groups are `Simple`, `Moderate`, and `Complex`.

## Reading note

Fixed random seeds support reproducible examples, but they do not remove sampling uncertainty. Reproducibility controls the draw you can recreate; uncertainty concerns what would change under other plausible draws from the same target population.
