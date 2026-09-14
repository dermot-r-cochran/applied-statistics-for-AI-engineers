"""Sampling and comparison utilities for synthetic evaluation chapters."""

from __future__ import annotations

from math import ceil, sqrt
from typing import Callable, Literal, Sequence

import numpy as np
from scipy.optimize import brentq
from scipy.stats import beta, binomtest, fisher_exact, norm


ArrayLike = Sequence[float] | np.ndarray


def _scalar_metric_value(metric: Callable[[np.ndarray], float], values: np.ndarray) -> float:
    result = metric(values)
    scalar = np.asarray(result)
    if scalar.ndim != 0:
        raise ValueError("metric must return a scalar value.")
    return float(scalar)


def standard_error_proportion(successes: int, trials: int) -> float:
    """Return the binomial standard error for an observed proportion.

    Assumptions:
        * ``trials`` is positive.
        * The standard error is a normal-approximation summary, not a confidence interval.

    Examples:
        >>> round(standard_error_proportion(88, 100), 4)
        0.0325
    """

    if trials <= 0:
        raise ValueError("trials must be positive.")
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between 0 and trials.")
    p_hat = successes / trials
    return sqrt((p_hat * (1.0 - p_hat)) / trials)


def wilson_interval(successes: int, trials: int, confidence_level: float = 0.95) -> tuple[float, float]:
    """Compute a Wilson score interval for a binomial proportion.

    Assumptions:
        * ``confidence_level`` lies strictly between 0 and 1.
        * Observations are treated as exchangeable Bernoulli draws.

    Examples:
        >>> lo, hi = wilson_interval(66, 75)
        >>> 0.7 < lo < hi < 1.0
        True
    """

    if trials <= 0:
        raise ValueError("trials must be positive.")
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between 0 and trials.")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1.")

    z_value = norm.ppf(0.5 + confidence_level / 2.0)
    p_hat = successes / trials
    denominator = 1.0 + (z_value**2 / trials)
    center = p_hat + (z_value**2 / (2.0 * trials))
    spread = z_value * sqrt((p_hat * (1.0 - p_hat) / trials) + (z_value**2 / (4.0 * trials**2)))
    return max(0.0, (center - spread) / denominator), min(1.0, (center + spread) / denominator)


def exact_binomial_interval(successes: int, trials: int, confidence_level: float = 0.95) -> tuple[float, float]:
    """Compute the equal-tailed exact binomial interval.

    Assumptions:
        * ``trials`` is positive.
        * The interval conditions on the observed sample size.

    Examples:
        >>> lo, hi = exact_binomial_interval(0, 5)
        >>> lo == 0.0 and hi < 1.0
        True
    """

    if trials <= 0:
        raise ValueError("trials must be positive.")
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between 0 and trials.")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1.")

    alpha = 1.0 - confidence_level
    lower = 0.0 if successes == 0 else beta.ppf(alpha / 2.0, successes, trials - successes + 1)
    upper = 1.0 if successes == trials else beta.ppf(1.0 - alpha / 2.0, successes + 1, trials - successes)
    return float(lower), float(upper)


def bootstrap_metric(
    values: ArrayLike,
    metric: Callable[[np.ndarray], float] | None = None,
    *,
    n_resamples: int = 2_000,
    confidence_level: float = 0.95,
    seed: int | None = None,
) -> dict[str, float | np.ndarray]:
    """Bootstrap a one-sample metric from row-level observations.

    Assumptions:
        * Rows are sampled as if they were independent draws.
        * ``metric`` returns a scalar for any non-empty resample.

    Examples:
        >>> result = bootstrap_metric([1, 0, 1, 1], seed=1, n_resamples=200)
        >>> round(float(result["estimate"]), 2)
        0.75
    """

    sample = np.asarray(values, dtype=float)
    if sample.size == 0:
        raise ValueError("values must not be empty.")
    if np.isnan(sample).any():
        raise ValueError("values contains missing values.")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive.")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1.")

    metric_fn = metric or (lambda arr: float(np.mean(arr)))
    estimate = _scalar_metric_value(metric_fn, sample)
    rng = np.random.default_rng(seed)
    draws = np.empty(n_resamples, dtype=float)
    for idx in range(n_resamples):
        resample = rng.choice(sample, size=sample.size, replace=True)
        draws[idx] = _scalar_metric_value(metric_fn, resample)

    alpha = 1.0 - confidence_level
    return {
        "estimate": estimate,
        "lower": float(np.quantile(draws, alpha / 2.0)),
        "upper": float(np.quantile(draws, 1.0 - alpha / 2.0)),
        "samples": draws,
    }


def bootstrap_interval(
    values: ArrayLike,
    *,
    n_resamples: int = 2_000,
    confidence_level: float = 0.95,
    seed: int | None = None,
) -> tuple[float, float]:
    """Convenience wrapper returning only the percentile bootstrap interval.

    Examples:
        >>> lo, hi = bootstrap_interval([1, 1, 0, 1], seed=2, n_resamples=200)
        >>> 0.0 <= lo <= hi <= 1.0
        True
    """

    result = bootstrap_metric(
        values,
        n_resamples=n_resamples,
        confidence_level=confidence_level,
        seed=seed,
    )
    return float(result["lower"]), float(result["upper"])


def cluster_bootstrap_metric(
    values: ArrayLike,
    clusters: Sequence[object],
    metric: Callable[[np.ndarray], float] | None = None,
    *,
    n_resamples: int = 2_000,
    confidence_level: float = 0.95,
    seed: int | None = None,
) -> dict[str, float | np.ndarray]:
    """Bootstrap a metric by resampling clusters instead of rows.

    Assumptions:
        * Clusters, not rows, are exchangeable sampling units.
        * ``clusters`` and ``values`` have identical length.
        * Empty cluster labels are invalid because the sampling unit would be undefined.

    Examples:
        >>> result = cluster_bootstrap_metric([1, 0, 1, 1], ['a', 'a', 'b', 'b'], seed=3, n_resamples=200)
        >>> round(float(result['estimate']), 2)
        0.75
    """

    sample = np.asarray(values, dtype=float)
    cluster_array = np.asarray(clusters, dtype=object)
    if sample.size == 0:
        raise ValueError("values must not be empty.")
    if sample.size != cluster_array.size:
        raise ValueError("values and clusters must have the same length.")
    if np.isnan(sample).any():
        raise ValueError("values contains missing values.")
    if any(cluster in (None, "") for cluster in cluster_array):
        raise ValueError("clusters contains an empty cluster label.")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive.")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1.")

    metric_fn = metric or (lambda arr: float(np.mean(arr)))
    estimate = _scalar_metric_value(metric_fn, sample)
    unique_clusters = np.unique(cluster_array)
    rng = np.random.default_rng(seed)
    draws = np.empty(n_resamples, dtype=float)

    for idx in range(n_resamples):
        sampled_clusters = rng.choice(unique_clusters, size=unique_clusters.size, replace=True)
        resampled_rows = []
        for cluster in sampled_clusters:
            cluster_values = sample[cluster_array == cluster]
            resampled_rows.append(cluster_values)
        combined = np.concatenate(resampled_rows)
        draws[idx] = _scalar_metric_value(metric_fn, combined)

    alpha = 1.0 - confidence_level
    return {
        "estimate": estimate,
        "lower": float(np.quantile(draws, alpha / 2.0)),
        "upper": float(np.quantile(draws, 1.0 - alpha / 2.0)),
        "samples": draws,
    }


def compare_paired_predictions(
    y_true: Sequence[object],
    pred_a: Sequence[object],
    pred_b: Sequence[object],
    confidence_level: float = 0.95,
    *,
    seed: int | None = None,
) -> dict[str, float | int | tuple[float, float]]:
    """Compare two systems evaluated on the same examples.

    The routine reports paired accuracy estimates and a McNemar-style exact p-value on
    the discordant cases.

    Assumptions:
        * Inputs represent the same ordered cases.
        * Missing values are not allowed.
        * The p-value tests a null of equal marginal accuracy, not practical equivalence.

    Examples:
        >>> result = compare_paired_predictions([1, 0, 1], [1, 0, 1], [1, 1, 1])
        >>> result['accuracy_a'] > result['accuracy_b']
        True
    """

    truth = np.asarray(y_true, dtype=object)
    first = np.asarray(pred_a, dtype=object)
    second = np.asarray(pred_b, dtype=object)
    if not (truth.size == first.size == second.size):
        raise ValueError("Paired inputs must have the same length.")
    if truth.size == 0:
        raise ValueError("Paired inputs must not be empty.")
    arrays = (truth, first, second)

    def _is_missing(value: object) -> bool:
        if value is None:
            return True
        try:
            return bool(np.isnan(value))
        except TypeError:
            return False

    if any(_is_missing(value) for array in arrays for value in array):
        raise ValueError("Paired inputs contain missing values.")

    correct_a = first == truth
    correct_b = second == truth
    b_only = int(np.sum(correct_b & ~correct_a))
    a_only = int(np.sum(correct_a & ~correct_b))
    discordant = a_only + b_only
    if discordant == 0:
        p_value = 1.0
    else:
        p_value = binomtest(min(a_only, b_only), n=discordant, p=0.5, alternative="two-sided").pvalue

    diff = float(np.mean(correct_a) - np.mean(correct_b))
    ci = bootstrap_interval(
        (correct_a.astype(float) - correct_b.astype(float)),
        confidence_level=confidence_level,
        seed=seed,
    )
    return {
        "n": int(truth.size),
        "accuracy_a": float(np.mean(correct_a)),
        "accuracy_b": float(np.mean(correct_b)),
        "accuracy_difference": diff,
        "difference_interval": ci,
        "a_only_correct": a_only,
        "b_only_correct": b_only,
        "p_value": float(p_value),
    }


def compare_independent_proportions(
    successes_a: int,
    trials_a: int,
    successes_b: int,
    trials_b: int,
    confidence_level: float = 0.95,
) -> dict[str, float]:
    """Compare independent observed proportions with a normal-approximation interval.

    Assumptions:
        * Group A and group B are independent samples.
        * The confidence interval uses an unpooled large-sample approximation.
        * The p-value uses Fisher's exact test for boundary-rate small samples and a pooled
          null distribution otherwise.
        * Both summaries are weakest for tiny samples.

    Examples:
        >>> result = compare_independent_proportions(88, 100, 84, 100)
        >>> round(result['difference'], 2)
        0.04
    """

    for name, successes, trials in (
        ("A", successes_a, trials_a),
        ("B", successes_b, trials_b),
    ):
        if trials <= 0:
            raise ValueError(f"trials_{name.lower()} must be positive.")
        if successes < 0 or successes > trials:
            raise ValueError(f"successes_{name.lower()} must be between 0 and trials_{name.lower()}.")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1.")

    p_a = successes_a / trials_a
    p_b = successes_b / trials_b
    difference = p_a - p_b
    se = sqrt((p_a * (1.0 - p_a) / trials_a) + (p_b * (1.0 - p_b) / trials_b))
    z_value = norm.ppf(0.5 + confidence_level / 2.0)
    lower = difference - z_value * se
    upper = difference + z_value * se
    pooled = (successes_a + successes_b) / (trials_a + trials_b)
    pooled_se = sqrt(pooled * (1.0 - pooled) * ((1.0 / trials_a) + (1.0 / trials_b)))
    uses_exact_test = pooled_se == 0.0 or p_a in {0.0, 1.0} or p_b in {0.0, 1.0}
    if uses_exact_test:
        contingency = np.array(
            [
                [successes_a, trials_a - successes_a],
                [successes_b, trials_b - successes_b],
            ]
        )
        p_value = float(fisher_exact(contingency, alternative="two-sided").pvalue)
    else:
        z_stat = difference / pooled_se
        p_value = float(2.0 * (1.0 - norm.cdf(abs(z_stat))))
    return {
        "rate_a": float(p_a),
        "rate_b": float(p_b),
        "difference": float(difference),
        "lower": float(lower),
        "upper": float(upper),
        "p_value": p_value,
    }


def minimum_detectable_effect(
    baseline_rate: float,
    sample_size_per_group: int,
    power: float = 0.8,
    alpha: float = 0.05,
    direction: Literal["increase", "decrease", "either"] = "either",
) -> float:
    """Approximate the minimum detectable effect for two independent proportions.

    Assumptions:
        * Both groups have the same sample size.
        * Observations are treated as independent Bernoulli draws.
        * Clustering and repeated measures are not modeled.

    Examples:
        >>> minimum_detectable_effect(0.88, 400) > 0
        True
    """

    if not 0.0 < baseline_rate < 1.0:
        raise ValueError("baseline_rate must be between 0 and 1.")
    if sample_size_per_group <= 1:
        raise ValueError("sample_size_per_group must be greater than 1.")
    if not 0.0 < power < 1.0:
        raise ValueError("power must be between 0 and 1.")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be between 0 and 1.")
    if direction not in {"increase", "decrease", "either"}:
        raise ValueError("direction must be 'increase', 'decrease', or 'either'.")

    z_alpha = norm.ppf(1.0 - alpha / 2.0)
    z_beta = norm.ppf(power)

    def solve(selected_direction: Literal["increase", "decrease"]) -> float:
        sign = 1.0 if selected_direction == "increase" else -1.0
        upper_bound = (1.0 - baseline_rate - 1e-6) if sign > 0 else (baseline_rate - 1e-6)
        if upper_bound <= 0.0:
            raise ValueError("baseline_rate leaves no room for the requested detectable effect.")

        def objective(delta: float) -> float:
            comparison_rate = baseline_rate + sign * delta
            se = sqrt(
                baseline_rate * (1.0 - baseline_rate) / sample_size_per_group
                + comparison_rate * (1.0 - comparison_rate) / sample_size_per_group
            )
            return delta - (z_alpha + z_beta) * se

        if objective(upper_bound) < 0.0:
            raise ValueError("Requested direction has no detectable effect within the feasible probability range.")
        return float(brentq(objective, 1e-6, upper_bound))

    if direction == "either":
        candidates = []
        for selected_direction in ("increase", "decrease"):
            try:
                candidates.append(solve(selected_direction))
            except ValueError:
                continue
        if not candidates:
            raise ValueError("No detectable effect was found within the feasible probability range.")
        return min(candidates)

    return solve(direction)


def required_sample_size(
    baseline_rate: float,
    minimum_effect: float,
    power: float = 0.8,
    alpha: float = 0.05,
    direction: Literal["increase", "decrease"] = "increase",
) -> int:
    """Approximate required sample size per group for two independent proportions.

    Assumptions:
        * Planned analysis is a two-sided independent comparison.
        * The calculation ignores clustering and assumes complete labels.

    Examples:
        >>> required_sample_size(0.88, 0.03) > 0
        True
    """

    if not 0.0 < baseline_rate < 1.0:
        raise ValueError("baseline_rate must be between 0 and 1.")
    if not 0.0 < minimum_effect < 1.0:
        raise ValueError("minimum_effect must be between 0 and 1.")
    if not 0.0 < power < 1.0:
        raise ValueError("power must be between 0 and 1.")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be between 0 and 1.")
    if direction not in {"increase", "decrease"}:
        raise ValueError("direction must be 'increase' or 'decrease'.")

    if direction == "increase":
        target_rate = baseline_rate + minimum_effect
        if target_rate >= 1.0:
            raise ValueError("baseline_rate + minimum_effect must be less than 1.")
    else:
        target_rate = baseline_rate - minimum_effect
        if target_rate <= 0.0:
            raise ValueError("baseline_rate - minimum_effect must be greater than 0.")

    z_alpha = norm.ppf(1.0 - alpha / 2.0)
    z_beta = norm.ppf(power)
    numerator = (
        z_alpha * sqrt(2.0 * baseline_rate * (1.0 - baseline_rate))
        + z_beta * sqrt(
            baseline_rate * (1.0 - baseline_rate)
            + target_rate * (1.0 - target_rate)
        )
    ) ** 2
    return int(ceil(numerator / (minimum_effect**2)))
