import math

import numpy as np
import pytest
from scipy.stats import beta

from trustworthy_ai_evaluation.sampling import (
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


def test_standard_error_matches_closed_form() -> None:
    assert math.isclose(standard_error_proportion(88, 100), math.sqrt(0.88 * 0.12 / 100))


@pytest.mark.parametrize(
    ("successes", "trials"),
    [(0, 5), (5, 5), (66, 75)],
)
def test_exact_interval_matches_beta_formula(successes: int, trials: int) -> None:
    lower, upper = exact_binomial_interval(successes, trials)
    if successes == 0:
        assert lower == 0.0
    else:
        assert math.isclose(lower, beta.ppf(0.025, successes, trials - successes + 1))
    if successes == trials:
        assert upper == 1.0
    else:
        assert math.isclose(upper, beta.ppf(0.975, successes + 1, trials - successes))


def test_wilson_interval_bounds_probability() -> None:
    lower, upper = wilson_interval(66, 75)
    assert 0.0 <= lower < upper <= 1.0


def test_bootstrap_interval_reproducible_for_fixed_seed() -> None:
    values = [1, 1, 0, 1, 0]
    first = bootstrap_interval(values, seed=2, n_resamples=300)
    second = bootstrap_interval(values, seed=2, n_resamples=300)
    assert first == second


def test_bootstrap_metric_rejects_missing_values() -> None:
    with pytest.raises(ValueError):
        bootstrap_metric([1.0, np.nan, 0.0])


def test_bootstrap_metric_rejects_non_scalar_metric() -> None:
    with pytest.raises(ValueError):
        bootstrap_metric([1.0, 0.0], metric=lambda values: values)


def test_cluster_bootstrap_handles_clustered_inputs() -> None:
    result = cluster_bootstrap_metric([1, 0, 1, 1, 0], ["a", "a", "b", "c", "c"], seed=5, n_resamples=250)
    assert 0.0 <= result["lower"] <= result["upper"] <= 1.0


def test_cluster_bootstrap_rejects_empty_cluster_labels() -> None:
    with pytest.raises(ValueError):
        cluster_bootstrap_metric([1, 0], ["", "b"])


@pytest.mark.parametrize("kwargs", [{"n_resamples": 0}, {"confidence_level": 1.0}])
def test_cluster_bootstrap_rejects_invalid_resampling_args(kwargs: dict[str, float | int]) -> None:
    with pytest.raises(ValueError):
        cluster_bootstrap_metric([1, 0], ["a", "b"], **kwargs)


def test_compare_paired_predictions_rejects_unequal_lengths() -> None:
    with pytest.raises(ValueError):
        compare_paired_predictions([1, 0], [1, 0], [1])


def test_compare_paired_predictions_rejects_nan_values() -> None:
    with pytest.raises(ValueError):
        compare_paired_predictions([1, 0, np.nan], [1, 0, 1], [1, 0, 1])


def test_compare_paired_predictions_all_agree() -> None:
    result = compare_paired_predictions([1, 0, 1], [1, 0, 1], [1, 0, 1])
    assert result["p_value"] == 1.0
    assert result["accuracy_difference"] == 0.0


def test_compare_independent_proportions_small_samples() -> None:
    result = compare_independent_proportions(1, 2, 0, 2)
    assert math.isclose(result["difference"], 0.5)
    assert math.isclose(result["p_value"], 0.24821307898992373)


@pytest.mark.parametrize("confidence_level", [0.0, 1.0])
def test_compare_independent_proportions_rejects_invalid_confidence_level(confidence_level: float) -> None:
    with pytest.raises(ValueError):
        compare_independent_proportions(1, 2, 0, 2, confidence_level=confidence_level)


def test_compare_independent_proportions_rejects_invalid_successes() -> None:
    with pytest.raises(ValueError):
        compare_independent_proportions(3, 2, 1, 2)


def test_minimum_detectable_effect_and_required_sample_size_are_positive() -> None:
    mde = minimum_detectable_effect(0.88, 400)
    needed = required_sample_size(0.88, 0.03)
    assert mde > 0.0
    assert needed > 0


@pytest.mark.parametrize("kwargs", [{"power": 1.2}, {"alpha": 0.0}])
def test_required_sample_size_rejects_invalid_probability_inputs(kwargs: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        required_sample_size(0.88, 0.03, **kwargs)


def test_required_sample_size_rejects_impossible_target_rate() -> None:
    with pytest.raises(ValueError):
        required_sample_size(0.98, 0.03)
