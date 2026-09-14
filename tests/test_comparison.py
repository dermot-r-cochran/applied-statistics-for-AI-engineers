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


def test_compare_two_models_returns_unit_p_value_when_models_match() -> None:
    y_true = [1, 0, 1, 0]
    predictions = [1, 0, 1, 0]
    result = compare_two_models(y_true, predictions, predictions)
    assert result["difference"] == pytest.approx(0.0)
    assert result["p_value"] == pytest.approx(1.0)


def test_compare_two_models_large_discordant_balance_uses_chi_square_branch() -> None:
    y_true = [0] * 30
    predictions_a = [0] * 15 + [1] * 15
    predictions_b = [1] * 15 + [0] * 15
    result = compare_two_models(y_true, predictions_a, predictions_b)
    assert result["difference"] == pytest.approx(0.0)
    assert result["p_value"] == pytest.approx(1.0)
