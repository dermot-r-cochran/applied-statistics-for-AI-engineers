import pytest

from applied_stats_ai import effective_sample_size, minimum_detectable_effect, power_analysis


def test_effective_sample_size_with_weights() -> None:
    value = effective_sample_size(weights=[1, 1, 2, 2])
    assert 3.0 < value < 4.0


def test_effective_sample_size_with_clusters() -> None:
    value = effective_sample_size(cluster_ids=[1, 1, 2, 2, 3, 3], intra_cluster_correlation=0.2)
    assert value < 6.0


def test_effective_sample_size_rejects_multiple_adjustment_modes() -> None:
    with pytest.raises(ValueError):
        effective_sample_size(
            weights=[1, 1, 1],
            cluster_ids=[1, 1, 2],
            intra_cluster_correlation=0.1,
        )


def test_power_analysis_and_mde_are_positive() -> None:
    power = power_analysis(0.84, 0.88, 400)
    mde = minimum_detectable_effect(0.85, 500)
    assert 0.0 < power < 1.0
    assert 0.0 < mde < 0.5


def test_minimum_detectable_effect_hits_requested_power() -> None:
    baseline = 0.85
    target_power = 0.8
    mde = minimum_detectable_effect(baseline, 500, target_power=target_power)
    achieved_power = power_analysis(baseline, baseline + mde, 500)
    assert achieved_power == pytest.approx(target_power, abs=0.01)


def test_minimum_detectable_effect_raises_when_power_is_unreachable() -> None:
    with pytest.raises(ValueError):
        minimum_detectable_effect(0.99, 5, target_power=0.99)


@pytest.mark.parametrize(
    ("baseline_rate", "treatment_rate", "sample_size_per_group", "alpha"),
    [
        (0.0, 0.8, 100, 0.05),
        (0.8, 1.0, 100, 0.05),
        (0.8, 0.85, 0, 0.05),
        (0.8, 0.85, 100, 1.0),
    ],
)
def test_power_analysis_rejects_invalid_inputs(
    baseline_rate: float,
    treatment_rate: float,
    sample_size_per_group: int,
    alpha: float,
) -> None:
    with pytest.raises(ValueError):
        power_analysis(
            baseline_rate,
            treatment_rate,
            sample_size_per_group,
            alpha=alpha,
        )


@pytest.mark.parametrize(
    ("baseline_rate", "sample_size_per_group", "target_power", "alpha"),
    [
        (0.0, 100, 0.8, 0.05),
        (0.85, 0, 0.8, 0.05),
        (0.85, 100, 1.0, 0.05),
        (0.85, 100, 0.8, 0.0),
    ],
)
def test_minimum_detectable_effect_rejects_invalid_inputs(
    baseline_rate: float,
    sample_size_per_group: int,
    target_power: float,
    alpha: float,
) -> None:
    with pytest.raises(ValueError):
        minimum_detectable_effect(
            baseline_rate,
            sample_size_per_group,
            target_power=target_power,
            alpha=alpha,
        )
