"""Comparability checks for evaluation reports."""

from __future__ import annotations

from typing import TypedDict


class MetricComparabilityResult(TypedDict):
    """Typed return value for metric comparability checks."""

    classification: str
    passed: dict[str, bool]
    limitations: list[str]


def metric_comparability_check(
    *,
    same_examples: bool,
    same_ground_truth: bool,
    same_scoring_code: bool,
    same_metric_definition: bool,
    same_thresholds: bool,
    same_preprocessing: bool,
    same_operating_conditions: bool,
) -> MetricComparabilityResult:
    """Classify whether two evaluation results are directly comparable.

    Assumptions:
        * Inputs summarize known design choices honestly.
        * The result is qualitative and does not replace technical review.

    Examples:
        >>> metric_comparability_check(
        ...     same_examples=True,
        ...     same_ground_truth=True,
        ...     same_scoring_code=True,
        ...     same_metric_definition=True,
        ...     same_thresholds=True,
        ...     same_preprocessing=True,
        ...     same_operating_conditions=True,
        ... )['classification']
        'Directly comparable'
    """

    checks = {
        "same_examples": same_examples,
        "same_ground_truth": same_ground_truth,
        "same_scoring_code": same_scoring_code,
        "same_metric_definition": same_metric_definition,
        "same_thresholds": same_thresholds,
        "same_preprocessing": same_preprocessing,
        "same_operating_conditions": same_operating_conditions,
    }
    failed = [name for name, value in checks.items() if not value]
    critical = {"same_examples", "same_ground_truth", "same_metric_definition"}
    if not failed:
        classification = "Directly comparable"
    elif critical.intersection(failed):
        classification = "Not directly comparable"
    else:
        classification = "Comparable with limitations"

    return {
        "classification": classification,
        "passed": {name: value for name, value in checks.items() if value},
        "limitations": failed,
    }
