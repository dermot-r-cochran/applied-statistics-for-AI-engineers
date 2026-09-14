"""Public package interface for Trustworthy AI Evaluation."""

from .confidence import (
    BrierScoreSummary,
    CalibrationBin,
    MetricComparabilityReport,
    SubgroupMetricRow,
    brier_score_summary,
    calibration_curve_data,
    expected_calibration_error,
    metric_comparability_check,
    subgroup_metric_report,
)

__all__ = [
    "BrierScoreSummary",
    "CalibrationBin",
    "MetricComparabilityReport",
    "SubgroupMetricRow",
    "brier_score_summary",
    "calibration_curve_data",
    "expected_calibration_error",
    "metric_comparability_check",
    "subgroup_metric_report",
]
