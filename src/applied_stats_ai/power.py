from __future__ import annotations

from scipy.optimize import brentq
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def power_analysis(
    baseline_rate: float,
    treatment_rate: float,
    sample_size_per_group: int,
    alpha: float = 0.05,
) -> float:
    """Return power for a two-sample comparison of proportions.

    Examples:
        >>> round(power_analysis(0.84, 0.88, 400), 3)
        0.475
    """
    if not 0 < baseline_rate < 1 or not 0 < treatment_rate < 1:
        raise ValueError("rates must be between 0 and 1")
    if sample_size_per_group <= 0:
        raise ValueError("sample_size_per_group must be positive")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    effect_size = proportion_effectsize(treatment_rate, baseline_rate)
    analysis = NormalIndPower()
    return float(
        analysis.power(effect_size=effect_size, nobs1=sample_size_per_group, alpha=alpha, ratio=1.0)
    )


def minimum_detectable_effect(
    baseline_rate: float,
    sample_size_per_group: int,
    target_power: float = 0.8,
    alpha: float = 0.05,
) -> float:
    """Return the minimum absolute lift detectable with the requested power.

    Examples:
        >>> round(minimum_detectable_effect(0.85, 500), 3)
        0.066
    """
    if not 0 < baseline_rate < 1:
        raise ValueError("baseline_rate must be between 0 and 1")
    if sample_size_per_group <= 0:
        raise ValueError("sample_size_per_group must be positive")
    if not 0 < target_power < 1:
        raise ValueError("target_power must be between 0 and 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    analysis = NormalIndPower()

    def solve(direction: int) -> float | None:
        upper_bound = (
            min(1 - baseline_rate - 1e-6, 0.499999)
            if direction > 0
            else min(baseline_rate - 1e-6, 0.499999)
        )
        if upper_bound <= 1e-6:
            return None

        def objective(delta: float) -> float:
            treatment = baseline_rate + (direction * delta)
            effect_size = proportion_effectsize(treatment, baseline_rate)
            power = analysis.power(
                effect_size=effect_size,
                nobs1=sample_size_per_group,
                alpha=alpha,
            )
            return power - target_power

        if objective(upper_bound) < 0:
            return None
        return float(brentq(objective, 1e-6, upper_bound))

    candidates = [value for value in (solve(1), solve(-1)) if value is not None]
    if not candidates:
        raise ValueError(
            "sample size is too small to reach target_power within valid proportion bounds"
        )
    return min(candidates)
