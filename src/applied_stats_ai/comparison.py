from __future__ import annotations

import numpy as np
from statsmodels.stats.contingency_tables import mcnemar

from ._typing import ArrayLike
from .bootstrap import bootstrap_metric
from .intervals import clopper_pearson_interval


def compare_two_models(
    y_true: ArrayLike,
    predictions_a: ArrayLike,
    predictions_b: ArrayLike,
    confidence_level: float = 0.95,
    n_resamples: int = 2_000,
    random_state: int | None = 0,
) -> dict[str, float | bool | tuple[float, float]]:
    """Compare two classifiers on the same labeled examples.

    The function reports accuracy for each model, the observed difference in accuracy,
    a bootstrap confidence interval for the paired difference, and a McNemar test p-value.

    Examples:
        >>> y_true = [1, 0, 1, 1]
        >>> predictions_a = [1, 0, 0, 1]
        >>> predictions_b = [1, 1, 1, 1]
        >>> sorted(compare_two_models(y_true, predictions_a, predictions_b).keys())
        ['accuracy_a', 'accuracy_b', 'confidence_interval', 'difference', 'p_value', 'same_sample']
    """
    y = np.asarray(y_true)
    a = np.asarray(predictions_a)
    b = np.asarray(predictions_b)

    if not (len(y) == len(a) == len(b)):
        raise ValueError("y_true, predictions_a, and predictions_b must have equal length")
    if len(y) == 0:
        raise ValueError("inputs must not be empty")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive")

    correct_a = (a == y).astype(int)
    correct_b = (b == y).astype(int)
    accuracy_a = float(correct_a.mean())
    accuracy_b = float(correct_b.mean())
    difference = accuracy_b - accuracy_a

    a_correct = correct_a == 1
    b_correct = correct_b == 1
    both = int(np.sum(a_correct & b_correct))
    a_only = int(np.sum(a_correct & ~b_correct))
    b_only = int(np.sum(~a_correct & b_correct))
    neither = int(np.sum(~a_correct & ~b_correct))

    table = [
        [both, a_only],
        [b_only, neither],
    ]
    discordant = a_only + b_only
    use_exact = discordant < 25
    p_value = float(mcnemar(table, exact=use_exact, correction=not use_exact).pvalue)
    if discordant == 0:
        interval = (0.0, 0.0)
    elif use_exact:
        lower_q, upper_q = clopper_pearson_interval(
            b_only,
            discordant,
            confidence_level=confidence_level,
        )
        scale = discordant / len(y)
        interval = (scale * ((2 * lower_q) - 1), scale * ((2 * upper_q) - 1))
    else:
        paired_differences = correct_b - correct_a
        interval_result = bootstrap_metric(
            paired_differences,
            np.mean,
            n_resamples=n_resamples,
            confidence_level=confidence_level,
            random_state=random_state,
        )
        interval = (float(interval_result["lower"]), float(interval_result["upper"]))

    return {
        "accuracy_a": accuracy_a,
        "accuracy_b": accuracy_b,
        "difference": float(difference),
        "confidence_interval": (float(interval[0]), float(interval[1])),
        "p_value": p_value,
        "same_sample": True,
    }
