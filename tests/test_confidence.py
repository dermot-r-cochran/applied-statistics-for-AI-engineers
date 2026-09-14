import math

import pandas as pd
import pytest

from trustworthy_ai_evaluation.confidence import (
    brier_score_summary,
    calibration_curve_data,
    expected_calibration_error,
    subgroup_metric_report,
)


def test_calibration_curve_counts_sum_to_rows() -> None:
    curve = calibration_curve_data([0, 1, 1, 0], [0.1, 0.8, 0.6, 0.2], n_bins=2)
    assert int(curve["count"].sum()) == 4


def test_expected_calibration_error_known_value() -> None:
    ece = expected_calibration_error([0, 1], [0.1, 0.9], n_bins=2, strategy="uniform")
    assert math.isclose(ece, 0.1)


def test_brier_score_summary_single_class_sample() -> None:
    summary = brier_score_summary([1, 1, 1], [0.9, 0.8, 0.7])
    assert summary["base_rate"] == 1.0
    assert summary["brier_score"] >= 0.0


def test_subgroup_metric_report_returns_sorted_groups() -> None:
    frame = pd.DataFrame(
        {
            "difficulty": ["Complex", "Simple", "Simple", "Complex"],
            "correct": [1, 1, 0, 1],
            "prob": [0.7, 0.8, 0.4, 0.6],
        }
    )
    report = subgroup_metric_report(
        frame,
        group_column="difficulty",
        outcome_column="correct",
        probability_column="prob",
    )
    assert report["group"].tolist() == ["Complex", "Simple"]


def test_subgroup_metric_report_rejects_missing_values() -> None:
    frame = pd.DataFrame({"group": ["a"], "y": [1], "p": [None]})
    with pytest.raises(ValueError):
        subgroup_metric_report(frame, group_column="group", outcome_column="y", probability_column="p")
