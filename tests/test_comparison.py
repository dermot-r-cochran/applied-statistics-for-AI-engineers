import pytest

from applied_stats_ai import compare_two_models


def test_compare_two_models_reports_difference() -> None:
    y_true = [1, 0, 1, 1, 0, 1]
    predictions_a = [1, 0, 0, 1, 0, 1]
    predictions_b = [1, 1, 1, 1, 0, 1]
    result = compare_two_models(y_true, predictions_a, predictions_b)
    assert result["accuracy_b"] >= result["accuracy_a"]
    lower, upper = result["confidence_interval"]
    assert lower <= result["difference"] <= upper
    assert result["p_value"] == pytest.approx(1.0)
