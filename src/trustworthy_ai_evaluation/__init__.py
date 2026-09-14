"""Utilities and synthetic assets for the Trustworthy AI Evaluation book."""

from .confidence import (
    brier_score_summary,
    calibration_curve_data,
    expected_calibration_error,
    subgroup_metric_report,
)
from .sampling import (
    bootstrap_interval,
    bootstrap_metric,
    cluster_bootstrap_metric,
    compare_independent_proportions,
    compare_paired_predictions,
    exact_binomial_interval,
    minimum_detectable_effect,
    required_sample_size,
    standard_error_proportion,
    wilson_interval,
)
from .synthetic import generate_project_frog_data, summarize_component_performance
from .validation import metric_comparability_check

__all__ = [
    "brier_score_summary",
    "bootstrap_interval",
    "bootstrap_metric",
    "calibration_curve_data",
    "cluster_bootstrap_metric",
    "compare_independent_proportions",
    "compare_paired_predictions",
    "exact_binomial_interval",
    "expected_calibration_error",
    "generate_project_frog_data",
    "metric_comparability_check",
    "minimum_detectable_effect",
    "required_sample_size",
    "standard_error_proportion",
    "subgroup_metric_report",
    "summarize_component_performance",
    "wilson_interval",
]
