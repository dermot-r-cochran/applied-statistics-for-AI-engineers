from applied_stats_ai import effective_sample_size, minimum_detectable_effect, power_analysis


def test_effective_sample_size_with_weights() -> None:
    value = effective_sample_size(weights=[1, 1, 2, 2])
    assert 3.0 < value < 4.0


def test_effective_sample_size_with_clusters() -> None:
    value = effective_sample_size(cluster_ids=[1, 1, 2, 2, 3, 3], intra_cluster_correlation=0.2)
    assert value < 6.0


def test_effective_sample_size_uses_observed_cluster_sizes() -> None:
    value = effective_sample_size(cluster_ids=[1, 1, 1, 1, 1, 2], intra_cluster_correlation=0.2)
    assert round(value, 2) == 3.6


def test_power_analysis_and_mde_are_positive() -> None:
    power = power_analysis(0.84, 0.88, 400)
    mde = minimum_detectable_effect(0.85, 500)
    assert 0.0 < power < 1.0
    assert 0.0 < mde < 0.5
