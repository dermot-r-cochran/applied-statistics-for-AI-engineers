import numpy as np

from applied_stats_ai import bootstrap_metric


def test_bootstrap_metric_returns_interval() -> None:
    values = np.array([1, 0, 1, 1, 0, 1])
    result = bootstrap_metric(values, np.mean, n_resamples=300, random_state=0)
    assert 0.0 <= result["lower"] <= result["estimate"] <= result["upper"] <= 1.0
    assert len(result["bootstrap_distribution"]) == 300


def test_bootstrap_metric_supports_rowwise_resampling_for_2d_inputs() -> None:
    values = np.array([[1, 1], [1, 0], [0, 1], [0, 0]])

    def row_match_rate(sample: np.ndarray) -> float:
        return float(np.mean(sample[:, 0] == sample[:, 1]))

    result = bootstrap_metric(values, row_match_rate, n_resamples=100, random_state=0)
    assert 0.0 <= result["lower"] <= result["estimate"] <= result["upper"] <= 1.0
