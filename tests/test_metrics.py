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


def test_confusion_matrix_uncertainty_keeps_binary_shape_for_single_class_samples() -> None:
    result = confusion_matrix_uncertainty(
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        n_resamples=50,
        random_state=2,
    )
    assert result["confusion_matrix"].shape == (2, 2)
    assert result["confusion_matrix"][0, 0] == 0
    assert result["confusion_matrix"][1, 1] == 4
