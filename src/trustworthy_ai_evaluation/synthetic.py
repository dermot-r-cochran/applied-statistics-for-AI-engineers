"""Synthetic Project Frog data generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd

PROJECT_FROG_SEED = 20260914
PROJECT_CLASSES = ["Clear", "Review", "Insufficient", "Escalate"]
DIFFICULTY_LEVELS = ["Simple", "Moderate", "Complex"]
COMPONENTS = [
    "Document extraction",
    "Classification",
    "Evidence retrieval",
    "Explanation generation",
]


@dataclass(frozen=True)
class ComponentProfile:
    """Configuration for a synthetic Project Frog component."""

    name: str
    confidence_shift: float
    calibration_temperature: float
    latency_mean_ms: float
    cost_mean_usd: float


_COMPONENT_PROFILES = [
    ComponentProfile("Document extraction", 0.65, 1.35, 180.0, 0.0040),
    ComponentProfile("Classification", 1.05, 1.10, 120.0, 0.0020),
    ComponentProfile("Evidence retrieval", 0.35, 0.85, 260.0, 0.0055),
    ComponentProfile("Explanation generation", 0.15, 0.75, 410.0, 0.0085),
]


def _sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


def _validate_positive_int(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive.")


def generate_project_frog_data(
    n_cases: int = 900,
    seed: int = PROJECT_FROG_SEED,
    component_names: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Generate reproducible synthetic Project Frog component-level data.

    The returned table is fully synthetic and fictional. A fixed random seed makes
    repeated generation reproducible, but it does not remove sampling uncertainty in
    later analyses.

    Assumptions:
        * Each case belongs to exactly one synthetic difficulty stratum.
        * Each row describes one component's output for one case.
        * Confidence scores have different semantics across components by design.

    Examples:
        >>> data = generate_project_frog_data(n_cases=3, seed=7)
        >>> sorted(data.columns)[0]
        'calibrated_probability'
        >>> data['case_id'].nunique()
        3
    """

    _validate_positive_int("n_cases", n_cases)
    rng = np.random.default_rng(seed)

    selected_components = list(component_names) if component_names is not None else COMPONENTS
    unknown_components = sorted(set(selected_components).difference(COMPONENTS))
    if unknown_components:
        raise ValueError(f"Unknown component names: {unknown_components}")
    profiles = [profile for profile in _COMPONENT_PROFILES if profile.name in selected_components]
    if not profiles:
        raise ValueError("At least one known component must be selected.")

    case_ids = np.arange(1, n_cases + 1)
    project_ids = np.array([f"PF-P{project_number:02d}" for project_number in ((case_ids - 1) % 6) + 1])
    document_ids = np.array([f"PF-D{document_number:04d}" for document_number in ((case_ids - 1) % 180) + 1])
    difficulty = rng.choice(DIFFICULTY_LEVELS, size=n_cases, p=[0.55, 0.30, 0.15])
    reference_class = rng.choice(PROJECT_CLASSES, size=n_cases, p=[0.44, 0.26, 0.18, 0.12])

    difficulty_penalty = np.select(
        [difficulty == "Simple", difficulty == "Moderate", difficulty == "Complex"],
        [0.55, 0.0, -0.65],
    )
    class_penalty = np.select(
        [reference_class == "Clear", reference_class == "Review", reference_class == "Insufficient", reference_class == "Escalate"],
        [0.15, 0.0, -0.25, -0.35],
    )
    latent_case_quality = rng.normal(0.0, 0.55, size=n_cases)
    latent_dependency = rng.normal(0.0, 0.45, size=n_cases)
    retrieval_relevance = np.clip(_sigmoid(0.7 * difficulty_penalty + latent_case_quality) + rng.normal(0.0, 0.08, size=n_cases), 0.0, 1.0)

    rows: list[dict[str, object]] = []
    predicted_class_options = np.array(PROJECT_CLASSES)

    for component_index, profile in enumerate(profiles):
        component_noise = rng.normal(0.0, 0.35, size=n_cases)
        success_logit = (
            profile.confidence_shift
            + difficulty_penalty
            + class_penalty
            + 0.45 * latent_case_quality
            + 0.55 * latent_dependency
            + 0.35 * retrieval_relevance
            + component_noise
        )
        calibrated_probability = np.clip(_sigmoid(success_logit / profile.calibration_temperature), 0.01, 0.99)
        raw_confidence = np.clip(_sigmoid(success_logit + rng.normal(0.0, 0.55, size=n_cases)), 0.01, 0.99)
        prediction_correct = rng.binomial(1, calibrated_probability).astype(bool)

        incorrect_offsets = rng.integers(1, len(PROJECT_CLASSES), size=n_cases)
        reference_indices = np.array([PROJECT_CLASSES.index(label) for label in reference_class])
        predicted_indices = np.where(
            prediction_correct,
            reference_indices,
            (reference_indices + incorrect_offsets) % len(PROJECT_CLASSES),
        )
        predicted_class = predicted_class_options[predicted_indices]

        evidence_relevance = np.clip(
            retrieval_relevance + 0.10 * component_index + rng.normal(0.0, 0.06, size=n_cases),
            0.0,
            1.0,
        )
        processing_latency = np.clip(
            rng.normal(profile.latency_mean_ms, profile.latency_mean_ms * 0.18, size=n_cases)
            + np.where(difficulty == "Complex", 70.0, np.where(difficulty == "Moderate", 25.0, 0.0)),
            20.0,
            None,
        )
        processing_cost = np.clip(
            rng.normal(profile.cost_mean_usd, profile.cost_mean_usd * 0.12, size=n_cases)
            + np.where(difficulty == "Complex", profile.cost_mean_usd * 0.25, 0.0),
            0.0005,
            None,
        )

        for idx in range(n_cases):
            rows.append(
                {
                    "project_id": project_ids[idx],
                    "document_id": document_ids[idx],
                    "case_id": f"PF-C{case_ids[idx]:05d}",
                    "difficulty": difficulty[idx],
                    "predicted_class": predicted_class[idx],
                    "reference_class": reference_class[idx],
                    "prediction_correct": bool(prediction_correct[idx]),
                    "component_name": profile.name,
                    "raw_confidence": float(raw_confidence[idx]),
                    "calibrated_probability": float(calibrated_probability[idx]),
                    "evidence_relevance": float(evidence_relevance[idx]),
                    "processing_latency": float(processing_latency[idx]),
                    "processing_cost": float(processing_cost[idx]),
                }
            )

    data = pd.DataFrame(rows)
    ordered_columns = [
        "project_id",
        "document_id",
        "case_id",
        "difficulty",
        "predicted_class",
        "reference_class",
        "prediction_correct",
        "component_name",
        "raw_confidence",
        "calibrated_probability",
        "evidence_relevance",
        "processing_latency",
        "processing_cost",
    ]
    return data[ordered_columns]


def summarize_component_performance(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize synthetic component performance for reporting.

    Assumptions:
        * ``data`` follows the Project Frog schema.
        * ``prediction_correct`` is boolean and missing values were removed upstream.

    Examples:
        >>> summary = summarize_component_performance(generate_project_frog_data(n_cases=8, seed=3))
        >>> set(summary.columns) >= {"component_name", "accuracy", "rows"}
        True
    """

    required = {"component_name", "prediction_correct", "processing_latency", "processing_cost"}
    missing = required.difference(data.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")

    summary = (
        data.groupby("component_name", dropna=False)
        .agg(
            rows=("prediction_correct", "size"),
            accuracy=("prediction_correct", "mean"),
            mean_latency_ms=("processing_latency", "mean"),
            mean_cost_usd=("processing_cost", "mean"),
        )
        .reset_index()
    )
    return summary.sort_values("component_name").reset_index(drop=True)
