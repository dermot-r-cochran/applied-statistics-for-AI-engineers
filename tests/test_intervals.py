from applied_stats_ai import clopper_pearson_interval, confidence_interval_accuracy, wilson_interval


def test_wilson_interval_contains_observed_rate() -> None:
    lower, upper = wilson_interval(85, 100)
    assert lower < 0.85 < upper


def test_clopper_pearson_interval_bounds() -> None:
    lower, upper = clopper_pearson_interval(0, 10)
    assert lower == 0.0
    assert 0.0 < upper < 1.0


def test_confidence_interval_dispatch_matches_wilson() -> None:
    assert confidence_interval_accuracy(42, 50) == wilson_interval(42, 50)


def test_full_success_interval_stays_within_unit_bounds() -> None:
    wilson_lower, wilson_upper = wilson_interval(10, 10)
    exact_lower, exact_upper = clopper_pearson_interval(10, 10)
    assert 0.0 <= wilson_lower <= wilson_upper <= 1.0
    assert 0.0 <= exact_lower <= exact_upper == 1.0
