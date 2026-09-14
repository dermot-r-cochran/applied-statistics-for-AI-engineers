from __future__ import annotations

from scipy.optimize import brentq
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def power_analysis(
    baseline_rate: float,
    variant_rate: float,
    sample_size_per_group: int,
    alpha: float = 0.05,
) -> float:
    """Return approximate power for detecting a difference in two proportions.

    Examples:
        >>> round(power_analysis(0.84, 0.88, 400), 3)
        0.393
    """
    if not 0 < baseline_rate < 1 or not 0 < variant_rate < 1:
        raise ValueError("rates must be between 0 and 1")
    if sample_size_per_group <= 1:
        raise ValueError("sample_size_per_group must be greater than 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")

    effect_size = proportion_effectsize(variant_rate, baseline_rate)
    analysis = NormalIndPower()
    return float(
        analysis.power(
            effect_size=effect_size,
            nobs1=sample_size_per_group,
            alpha=alpha,
        )
    )


def minimum_detectable_effect(
    baseline_rate: float,
    sample_size_per_group: int,
    alpha: float = 0.05,
    target_power: float = 0.8,
) -> float:
    """Return the minimum detectable absolute lift for a two-sample proportion test.

    Examples:
        >>> round(minimum_detectable_effect(0.85, 500), 3)
        0.064
    """
    if not 0 < baseline_rate < 1:
        raise ValueError("baseline_rate must be between 0 and 1")
    if sample_size_per_group <= 1:
        raise ValueError("sample_size_per_group must be greater than 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if not 0 < target_power < 1:
        raise ValueError("target_power must be between 0 and 1")

    analysis = NormalIndPower()

    def objective(delta: float) -> float:
        treatment = min(max(baseline_rate + delta, 1e-6), 1 - 1e-6)
        effect_size = proportion_effectsize(treatment, baseline_rate)
        power = analysis.power(
            effect_size=effect_size,
            nobs1=sample_size_per_group,
            alpha=alpha,
        )
        return power - target_power

    upper_bound = min(1 - baseline_rate - 1e-6, 0.499999)
    if objective(upper_bound) < 0:
        raise ValueError(
            "sample size is too small to reach target_power within valid proportion bounds"
        )
    return float(brentq(objective, 1e-6, upper_bound))
