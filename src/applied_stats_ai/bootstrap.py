from __future__ import annotations

from collections.abc import Callable

import numpy as np

from ._typing import ArrayLike


def bootstrap_metric(
    values: ArrayLike,
    metric: Callable[[np.ndarray], float],
    n_resamples: int = 2_000,
    confidence_level: float = 0.95,
    random_state: int | None = None,
) -> dict[str, float | np.ndarray]:
    """Estimate metric uncertainty with a percentile bootstrap.

    Examples:
        >>> import numpy as np
        >>> result = bootstrap_metric(
        ...     np.array([1, 0, 1, 1]),
        ...     np.mean,
        ...     n_resamples=100,
        ...     random_state=0,
        ... )
        >>> sorted(result.keys())
        ['bootstrap_distribution', 'estimate', 'lower', 'upper']
    """
    data = np.asarray(values)
    if data.size == 0:
        raise ValueError("values must not be empty")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1")

    rng = np.random.default_rng(random_state)
    estimates = np.empty(n_resamples, dtype=float)
    for index in range(n_resamples):
        sample = rng.choice(data, size=data.shape[0], replace=True)
        estimates[index] = float(metric(sample))

    alpha = 1 - confidence_level
    lower, upper = np.quantile(estimates, [alpha / 2, 1 - alpha / 2])
    return {
        "estimate": float(metric(data)),
        "lower": float(lower),
        "upper": float(upper),
        "bootstrap_distribution": estimates,
    }
