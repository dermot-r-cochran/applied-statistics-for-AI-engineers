from math import isclose

from scipy.stats import norm

from applied_stats_ai import compare_two_models


def test_compare_two_models_reports_difference() -> None:
    y_true = [1, 0, 1, 1, 0, 1]
    predictions_a = [1, 0, 0, 1, 0, 1]
    predictions_b = [1, 1, 1, 1, 0, 1]
    result = compare_two_models(y_true, predictions_a, predictions_b)
    assert result["accuracy_b"] >= result["accuracy_a"]
    lower, upper = result["confidence_interval"]
    assert lower <= result["difference"] <= upper
    assert 0.0 <= result["p_value"] <= 1.0


def test_compare_two_models_uses_paired_difference_variance() -> None:
    y_true = [1, 0, 1, 0]
    predictions_a = [1, 1, 0, 0]
    predictions_b = [1, 0, 1, 1]
    result = compare_two_models(y_true, predictions_a, predictions_b)

    difference = 0.25
    discordant = 3
    variance = ((discordant / 4) - difference**2) / 4
    margin = norm.ppf(0.975) * variance**0.5

    expected_interval = (difference - margin, difference + margin)
    assert isclose(result["difference"], difference)
    assert result["confidence_interval"] == expected_interval
