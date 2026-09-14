import math

import numpy as np
import pytest

from trustworthy_ai_evaluation import (
    brier_score_summary,
    calibration_curve_data,
    expected_calibration_error,
    metric_comparability_check,
    subgroup_metric_report,
)


def test_calibration_curve_data_returns_non_empty_bins():
    bins = calibration_curve_data([0, 1, 1, 0], [0.1, 0.2, 0.8, 0.9], n_bins=2)
    assert [item.count for item in bins] == [2, 2]
    assert bins[0].observed_frequency == 0.5
    assert bins[1].observed_frequency == 0.5


def test_expected_calibration_error_is_zero_for_perfect_predictions():
    assert expected_calibration_error([0, 1, 0, 1], [0.0, 1.0, 0.0, 1.0], n_bins=2) == 0.0


def test_expected_calibration_error_handles_single_class_samples():
    value = expected_calibration_error([1, 1, 1], [0.7, 0.8, 0.9], n_bins=3)
    assert value >= 0.0


def test_brier_score_summary_handles_all_correct_and_all_incorrect_cases():
    all_correct = brier_score_summary([1, 1], [1.0, 1.0], n_bins=2)
    all_incorrect = brier_score_summary([0, 0], [1.0, 1.0], n_bins=2)
    assert all_correct.brier_score == 0.0
    assert all_correct.uncertainty == 0.0
    assert all_incorrect.brier_score == 1.0


def test_subgroup_metric_report_returns_expected_groups():
    rows = subgroup_metric_report(
        ["Simple", "Simple", "Complex", "Complex"],
        [0, 1, 0, 1],
        [0.2, 0.8, 0.4, 0.6],
        n_bins=2,
    )
    assert [row.group for row in rows] == ["Complex", "Simple"]
    assert all(row.count == 2 for row in rows)


def test_metric_comparability_flags_semantic_mismatch():
    report = metric_comparability_check(
        metric_name="confidence",
        producing_component_a="classification",
        producing_component_b="retrieval",
        intended_meaning_a="Estimated probability the predicted class is correct.",
        intended_meaning_b="Ranking margin for the top evidence chunk.",
        mathematical_range_a=(0.0, 1.0),
        mathematical_range_b=(0.0, 1.0),
        claims_probability_a=True,
        claims_probability_b=False,
    )
    assert report.verdict == "not directly comparable"
    assert any("different intended meanings" in reason.lower() for reason in report.reasons)


@pytest.mark.parametrize(
    "y_true,scores",
    [([], []), ([0, 1], [0.2]), ([0, 1], [0.2, np.nan])],
)
def test_confidence_utilities_reject_invalid_inputs(y_true, scores):
    with pytest.raises(ValueError):
        calibration_curve_data(y_true, scores)


def test_subgroup_metric_report_rejects_missing_group_values():
    with pytest.raises(ValueError):
        subgroup_metric_report(["A", None], [0, 1], [0.2, 0.8])
