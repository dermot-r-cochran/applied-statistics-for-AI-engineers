"""Public utilities for the Trustworthy AI Evaluation book."""

from .evaluation import (
    BootstrapResult,
    ComparabilityResult,
    IndependentProportionComparison,
    PairedPredictionComparison,
    bootstrap_metric,
    cluster_bootstrap_metric,
    compare_independent_proportions,
    compare_paired_predictions,
    metric_comparability_check,
    minimum_detectable_effect,
    required_sample_size,
)

__all__ = [
    "BootstrapResult",
    "ComparabilityResult",
    "IndependentProportionComparison",
    "PairedPredictionComparison",
    "bootstrap_metric",
    "cluster_bootstrap_metric",
    "compare_independent_proportions",
    "compare_paired_predictions",
    "metric_comparability_check",
    "minimum_detectable_effect",
    "required_sample_size",
]
