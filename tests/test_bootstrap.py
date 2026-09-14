import numpy as np

from applied_stats_ai import bootstrap_metric


def test_bootstrap_metric_returns_interval() -> None:
    values = np.array([1, 0, 1, 1, 0, 1])
    result = bootstrap_metric(values, np.mean, n_resamples=300, random_state=0)
    assert 0.0 <= result["lower"] <= result["estimate"] <= result["upper"] <= 1.0
    assert len(result["bootstrap_distribution"]) == 300
