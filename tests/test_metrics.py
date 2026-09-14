from applied_stats_ai import confusion_matrix_uncertainty


def test_confusion_matrix_uncertainty_returns_metrics() -> None:
    result = confusion_matrix_uncertainty(
        [1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 1],
        n_resamples=200,
        random_state=5,
    )
    assert result["confusion_matrix"].shape == (2, 2)
    for metric_name in ["accuracy", "precision", "recall", "f1"]:
        metric = result["metrics"][metric_name]
        assert 0.0 <= metric["lower"] <= metric["estimate"] <= metric["upper"] <= 1.0
