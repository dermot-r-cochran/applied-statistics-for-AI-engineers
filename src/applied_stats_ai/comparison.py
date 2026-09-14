from __future__ import annotations

import numpy as np
from scipy.stats import binomtest, chi2

from ._typing import ArrayLike
from .bootstrap import bootstrap_metric

SMALL_SAMPLE_DISCORDANT_THRESHOLD = 25


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
    a paired bootstrap confidence interval for the difference, and a paired McNemar test
    p-value.

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
    paired_differences = correct_b - correct_a
    difference = float(paired_differences.mean())

    a_only = int(np.sum((correct_a == 1) & (correct_b == 0)))
    b_only = int(np.sum((correct_a == 0) & (correct_b == 1)))
    discordant = a_only + b_only

    if discordant == 0:
        p_value = 1.0
    elif discordant < SMALL_SAMPLE_DISCORDANT_THRESHOLD:
        p_value = float(binomtest(k=b_only, n=discordant, p=0.5).pvalue)
    else:
        numerator = max(abs(a_only - b_only) - 1, 0) ** 2
        statistic = numerator / discordant
        p_value = float(chi2.sf(statistic, df=1))

    bootstrap_result = bootstrap_metric(
        paired_differences,
        np.mean,
        n_resamples=n_resamples,
        confidence_level=confidence_level,
        random_state=random_state,
    )
    interval = (
        float(bootstrap_result["lower"]),
        float(bootstrap_result["upper"]),
    )

    return {
        "accuracy_a": accuracy_a,
        "accuracy_b": accuracy_b,
        "difference": difference,
        "confidence_interval": interval,
        "p_value": p_value,
        "same_sample": True,
    }
