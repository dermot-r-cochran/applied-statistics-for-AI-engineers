from __future__ import annotations

from scipy.optimize import brentq
from statsmodels.stats.proportion import power_proportions_2indep


def power_analysis(
    baseline_rate: float,
    treatment_rate: float,
    sample_size_per_group: int,
    alpha: float = 0.05,
) -> float:
    """Return power for a two-sample comparison of proportions.

    Examples:
        >>> round(power_analysis(0.84, 0.88, 400), 3)
        0.371
    """
    if not 0 < baseline_rate < 1 or not 0 < treatment_rate < 1:
        raise ValueError("rates must be between 0 and 1")
    if sample_size_per_group <= 0:
        raise ValueError("sample_size_per_group must be positive")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    result = power_proportions_2indep(
        diff=treatment_rate - baseline_rate,
        prop2=baseline_rate,
        nobs1=sample_size_per_group,
        ratio=1,
        alpha=alpha,
        alternative="two-sided",
    )
    return float(result.power)


def minimum_detectable_effect(
    baseline_rate: float,
    sample_size_per_group: int,
    target_power: float = 0.8,
    alpha: float = 0.05,
) -> float:
    """Return the minimum absolute rate change detectable with the requested power.

    Examples:
        >>> round(minimum_detectable_effect(0.85, 500), 3)
        0.075
    """
    if not 0 < baseline_rate < 1:
        raise ValueError("baseline_rate must be between 0 and 1")
    if sample_size_per_group <= 0:
        raise ValueError("sample_size_per_group must be positive")
    if not 0 < target_power < 1:
        raise ValueError("target_power must be between 0 and 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    def solve_for_direction(direction: int) -> float | None:
        upper_bound = (
            1 - baseline_rate - 1e-6
            if direction > 0
            else baseline_rate - 1e-6
        )
        if upper_bound <= 1e-6:
            return None

        def objective(delta: float) -> float:
            result = power_proportions_2indep(
                diff=direction * delta,
                prop2=baseline_rate,
                nobs1=sample_size_per_group,
                ratio=1,
                alpha=alpha,
                alternative="two-sided",
            )
            return float(result.power) - target_power

        lower_bound = 1e-6
        lower_value = objective(lower_bound)
        if lower_value >= 0:
            return lower_bound
        if objective(upper_bound) < 0:
            return None
        return float(brentq(objective, lower_bound, upper_bound))

    candidates = [
        value
        for value in (solve_for_direction(1), solve_for_direction(-1))
        if value is not None
    ]
    if not candidates:
        raise ValueError(
            "sample size is too small to reach target_power within valid proportion bounds",
        )
    return min(candidates)
