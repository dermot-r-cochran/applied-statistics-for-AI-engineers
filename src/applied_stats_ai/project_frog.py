from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ProjectFrogScenario:
    """Configuration for a synthetic Project Frog evaluation dataset.

    Examples:
        >>> scenario = ProjectFrogScenario(sample_size=10, baseline_accuracy=0.8)
        >>> scenario.sample_size
        10
    """

    sample_size: int = 200
    baseline_accuracy: float = 0.85
    comparison_accuracy: float = 0.88
    project_count: int = 12


DEFAULT_PROJECT_FROG_SCENARIO = ProjectFrogScenario()


def generate_project_frog_evaluation(
    scenario: ProjectFrogScenario | None = None,
    *,
    random_state: int | None = None,
) -> pd.DataFrame:
    """Generate a synthetic Project Frog classification dataset.

    The dataset is fictional and intended for examples, notebooks, and tests.

    Examples:
        >>> df = generate_project_frog_evaluation(
        ...     ProjectFrogScenario(sample_size=8),
        ...     random_state=0,
        ... )
        >>> sorted(df.columns)[:4]
        ['baseline_prediction', 'comparison_prediction', 'complexity', 'confidence_like_score']
    """
    scenario = scenario or DEFAULT_PROJECT_FROG_SCENARIO
    if scenario.sample_size <= 0:
        raise ValueError('sample_size must be positive')
    if scenario.project_count <= 0:
        raise ValueError('project_count must be positive')
    if scenario.project_count > scenario.sample_size:
        raise ValueError('project_count cannot exceed sample_size')
    if not 0 < scenario.baseline_accuracy < 1:
        raise ValueError('baseline_accuracy must be between 0 and 1')
    if not 0 < scenario.comparison_accuracy < 1:
        raise ValueError('comparison_accuracy must be between 0 and 1')

    rng = np.random.default_rng(random_state)
    complexities = np.array(['simple', 'medium', 'complex'])
    complexity = rng.choice(complexities, size=scenario.sample_size, p=[0.5, 0.3, 0.2])
    truth = rng.integers(0, 2, size=scenario.sample_size)
    project_ids = rng.integers(1, scenario.project_count + 1, size=scenario.sample_size)

    baseline_correct = rng.binomial(1, scenario.baseline_accuracy, size=scenario.sample_size)
    comparison_correct = rng.binomial(1, scenario.comparison_accuracy, size=scenario.sample_size)

    baseline_prediction = np.where(baseline_correct == 1, truth, 1 - truth)
    comparison_prediction = np.where(comparison_correct == 1, truth, 1 - truth)

    evidence_quality = np.clip(
        rng.normal(
            loc=np.select(
                [complexity == "simple", complexity == "medium", complexity == "complex"],
                [0.86, 0.76, 0.64],
            ),
            scale=0.06,
            size=scenario.sample_size,
        ),
        0,
        1,
    )
    confidence_like_score = np.clip(
        rng.normal(
            loc=np.select(
                [complexity == "simple", complexity == "medium", complexity == "complex"],
                [0.81, 0.69, 0.57],
            ),
            scale=0.08,
            size=scenario.sample_size,
        ),
        0,
        1,
    )
    latency_ms = np.round(
        rng.normal(
            loc=np.select(
                [complexity == 'simple', complexity == 'medium', complexity == 'complex'],
                [180, 260, 340],
            ),
            scale=25,
        ),
        1,
    )
    processing_cost = np.round(
        0.0025 + latency_ms / 100_000 + rng.uniform(0, 0.0015, size=scenario.sample_size),
        5,
    )

    return pd.DataFrame(
        {
            'dataset_label': 'synthetic_project_frog',
            'document_id': [f'DOC-{index:05d}' for index in range(1, scenario.sample_size + 1)],
            'project_id': [f'PROJ-{project_id:03d}' for project_id in project_ids],
            'complexity': complexity,
            'truth': truth,
            'baseline_prediction': baseline_prediction,
            'comparison_prediction': comparison_prediction,
            'baseline_correct': baseline_correct,
            'comparison_correct': comparison_correct,
            'evidence_quality': np.round(evidence_quality, 3),
            'confidence_like_score': np.round(confidence_like_score, 3),
            'latency_ms': latency_ms,
            'processing_cost_usd': processing_cost,
        }
    )
