from __future__ import annotations

import numpy as np
from scipy.stats import norm
from statsmodels.stats.contingency_tables import mcnemar

from ._typing import ArrayLike


def compare_two_models(
    y_true: ArrayLike,
    predictions_a: ArrayLike,
    predictions_b: ArrayLike,
    confidence_level: float = 0.95,
) -> dict[str, float | bool | tuple[float, float]]:
    """Compare two classifiers on the same labeled examples.

    The function reports accuracy for each model, the observed difference in accuracy,
    a confidence interval for the difference, and a paired McNemar test p-value.

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

    correct_a = (a == y).astype(int)
    correct_b = (b == y).astype(int)
    accuracy_a = float(correct_a.mean())
    accuracy_b = float(correct_b.mean())
    difference = accuracy_b - accuracy_a

    both = int(np.sum((correct_a == 1) & (correct_b == 1)))
    a_only = int(np.sum((correct_a == 1) & (correct_b == 0)))
    b_only = int(np.sum((correct_a == 0) & (correct_b == 1)))
    neither = int(np.sum((correct_a == 0) & (correct_b == 0)))

    table = [[both, a_only], [b_only, neither]]
    p_value = float(mcnemar(table, exact=False, correction=True).pvalue)

    discordant = a_only + b_only
    z_value = norm.ppf(0.5 + confidence_level / 2)
    if discordant == 0:
        interval = (difference, difference)
    else:
        variance = ((discordant / len(y)) - difference**2) / len(y)
        margin = z_value * np.sqrt(max(variance, 0.0))
        interval = (difference - margin, difference + margin)

    return {
        "accuracy_a": accuracy_a,
        "accuracy_b": accuracy_b,
        "difference": float(difference),
        "confidence_interval": (float(interval[0]), float(interval[1])),
        "p_value": p_value,
        "same_sample": True,
    }
