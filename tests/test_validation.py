from trustworthy_ai_evaluation.validation import metric_comparability_check


def test_metric_comparability_direct() -> None:
    result = metric_comparability_check(
        same_examples=True,
        same_ground_truth=True,
        same_scoring_code=True,
        same_metric_definition=True,
        same_thresholds=True,
        same_preprocessing=True,
        same_operating_conditions=True,
    )
    assert result["classification"] == "Directly comparable"


def test_metric_comparability_not_direct() -> None:
    result = metric_comparability_check(
        same_examples=False,
        same_ground_truth=True,
        same_scoring_code=True,
        same_metric_definition=True,
        same_thresholds=True,
        same_preprocessing=True,
        same_operating_conditions=True,
    )
    assert result["classification"] == "Not directly comparable"


def test_metric_comparability_with_limitations() -> None:
    result = metric_comparability_check(
        same_examples=True,
        same_ground_truth=True,
        same_scoring_code=True,
        same_metric_definition=True,
        same_thresholds=True,
        same_preprocessing=False,
        same_operating_conditions=True,
    )
    assert result["classification"] == "Comparable with limitations"
