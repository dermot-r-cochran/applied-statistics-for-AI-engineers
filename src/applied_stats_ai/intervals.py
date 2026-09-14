from __future__ import annotations

from statistics import NormalDist
from typing import Literal

import numpy as np
from scipy.stats import beta


def _validate_binomial_inputs(
    successes: int,
    trials: int,
    confidence_level: float,
) -> None:
    if trials <= 0:
        raise ValueError("trials must be positive")
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between 0 and trials")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1")


def wilson_interval(
    successes: int,
    trials: int,
    confidence_level: float = 0.95,
) -> tuple[float, float]:
    """Return a Wilson score interval for a binomial proportion.

    Examples:
        >>> wilson_interval(85, 100)
        (0.767..., 0.906...)
    """
    _validate_binomial_inputs(successes, trials, confidence_level)
    z = NormalDist().inv_cdf(0.5 + confidence_level / 2)
    n = float(trials)
    p_hat = successes / n
    denom = 1 + z**2 / n
    center = (p_hat + z**2 / (2 * n)) / denom
    margin = z * np.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n)) / n) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def clopper_pearson_interval(
    successes: int,
    trials: int,
    confidence_level: float = 0.95,
) -> tuple[float, float]:
    """Return the exact Clopper-Pearson interval for a binomial proportion.

    Examples:
        >>> clopper_pearson_interval(17, 20)
        (0.621..., 0.967...)
    """
    _validate_binomial_inputs(successes, trials, confidence_level)
    alpha = 1 - confidence_level
    lower = (
        0.0
        if successes == 0
        else beta.ppf(alpha / 2, successes, trials - successes + 1)
    )
    upper = (
        1.0
        if successes == trials
        else beta.ppf(1 - alpha / 2, successes + 1, trials - successes)
    )
    return float(lower), float(upper)


def confidence_interval_accuracy(
    successes: int,
    trials: int,
    method: Literal["wilson", "clopper_pearson"] = "wilson",
    confidence_level: float = 0.95,
) -> tuple[float, float]:
    """Return a confidence interval for observed accuracy.

    Examples:
        >>> confidence_interval_accuracy(42, 50, method="wilson")
        (0.716..., 0.914...)
    """
    if method == "wilson":
        return wilson_interval(successes, trials, confidence_level)
    if method == "clopper_pearson":
        return clopper_pearson_interval(successes, trials, confidence_level)
    raise ValueError(f"Unsupported method: {method}")
