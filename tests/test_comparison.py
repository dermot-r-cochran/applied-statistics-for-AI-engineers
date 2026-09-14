import pytest
from statsmodels.stats.contingency_tables import mcnemar

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


def test_compare_two_models_bootstrap_interval_stays_nonzero_for_one_sided_discordance() -> None:
    y_true = [0] * 10
    predictions_a = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    predictions_b = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

    result = compare_two_models(
        y_true,
        predictions_a,
        predictions_b,
        n_resamples=500,
        random_state=3,
    )

    lower, upper = result["confidence_interval"]
    assert result["difference"] == pytest.approx(0.2)
    assert lower < upper
    assert lower <= result["difference"] <= upper


def test_compare_two_models_p_value_matches_mcnemar() -> None:
    y_true = [0] * 10
    predictions_a = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    predictions_b = [0, 0, 0, 0, 0, 1, 0, 0, 1, 1]

    result = compare_two_models(y_true, predictions_a, predictions_b)
    expected_p_value = mcnemar([[5, 1], [2, 2]], exact=False, correction=True).pvalue

    assert result["p_value"] == pytest.approx(expected_p_value)
