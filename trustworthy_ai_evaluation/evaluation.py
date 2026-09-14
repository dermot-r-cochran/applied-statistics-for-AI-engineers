from __future__ import annotations

from dataclasses import dataclass
import math
import random
from statistics import fmean
from typing import Callable, Iterable, Mapping, Sequence

Number = float | int
MetricFunction = Callable[[Sequence[float]], float]


@dataclass(frozen=True)
class BootstrapResult:
    """Summary of a bootstrap procedure.

    Attributes:
        estimate: Metric value on the observed sample.
        confidence_interval: Percentile bootstrap interval.
        standard_error: Standard deviation of bootstrap estimates.
        resamples: Number of bootstrap draws.
        method: Human-readable resampling description.
        assumptions: Main assumptions that justify the calculation.
    """

    estimate: float
    confidence_interval: tuple[float, float]
    standard_error: float
    resamples: int
    method: str
    assumptions: str


@dataclass(frozen=True)
class PairedPredictionComparison:
    """Result of a paired comparison between two prediction sets."""

    metric_name: str
    difference: float
    confidence_interval: tuple[float, float]
    p_value: float
    n_pairs: int
    method: str
    assumptions: str


@dataclass(frozen=True)
class IndependentProportionComparison:
    """Result of an independent two-sample proportion comparison."""

    proportion_a: float
    proportion_b: float
    difference: float
    confidence_interval: tuple[float, float]
    p_value: float
    method: str
    assumptions: str


@dataclass(frozen=True)
class ComparabilityResult:
    """Classification for metric comparability checks."""

    classification: str
    details: dict[str, str]
    limitations: tuple[str, ...]


def _is_missing(value: object) -> bool:
    return value is None or (isinstance(value, float) and math.isnan(value))


def _normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def _normal_ppf(probability: float) -> float:
    if not 0.0 < probability < 1.0:
        raise ValueError("probability must be between 0 and 1")
    # Peter John Acklam's rational approximation.
    a = (
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    )
    b = (
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    )
    c = (
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    )
    d = (
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    )
    plow = 0.02425
    phigh = 1 - plow
    if probability < plow:
        q = math.sqrt(-2 * math.log(probability))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q) + 1
        )
    if probability > phigh:
        q = math.sqrt(-2 * math.log(1 - probability))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q) + 1
        )
    q = probability - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (
        (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r) + 1
    )


def _clean_numeric(values: Iterable[Number | None], *, drop_missing: bool, name: str) -> list[float]:
    cleaned: list[float] = []
    for value in values:
        if _is_missing(value):
            if drop_missing:
                continue
            raise ValueError(f"{name} contains missing values")
        cleaned.append(float(value))
    if not cleaned:
        raise ValueError(f"{name} must contain at least one non-missing value")
    return cleaned


def _clean_pairs(
    y_true: Iterable[object | None],
    pred_a: Iterable[object | None],
    pred_b: Iterable[object | None],
    *,
    drop_missing: bool,
) -> list[tuple[object, object, object]]:
    true_list = list(y_true)
    a_list = list(pred_a)
    b_list = list(pred_b)
    if not (len(true_list) == len(a_list) == len(b_list)):
        raise ValueError("paired inputs must have equal length")
    cleaned: list[tuple[object, object, object]] = []
    for truth, first, second in zip(true_list, a_list, b_list):
        if _is_missing(truth) or _is_missing(first) or _is_missing(second):
            if drop_missing:
                continue
            raise ValueError("paired inputs contain missing values")
        cleaned.append((truth, first, second))
    if not cleaned:
        raise ValueError("at least one complete pair is required")
    return cleaned


def _percentile_interval(samples: Sequence[float], confidence_level: float) -> tuple[float, float]:
    ordered = sorted(samples)
    alpha = 1.0 - confidence_level
    lower_index = max(0, min(len(ordered) - 1, int(math.floor((alpha / 2) * (len(ordered) - 1)))))
    upper_index = max(0, min(len(ordered) - 1, int(math.ceil((1 - alpha / 2) * (len(ordered) - 1)))))
    return (ordered[lower_index], ordered[upper_index])


def _default_metric(values: Sequence[float]) -> float:
    return fmean(values)


def bootstrap_metric(
    values: Iterable[Number | None],
    metric: MetricFunction | None = None,
    *,
    n_resamples: int = 2000,
    confidence_level: float = 0.95,
    seed: int | None = None,
    drop_missing: bool = False,
) -> BootstrapResult:
    """Estimate uncertainty for a sample metric using the ordinary bootstrap.

    Args:
        values: Observed sample values. For binary accuracy data, use 1 for correct
            and 0 for incorrect.
        metric: Function applied to each resample. Defaults to the arithmetic mean.
        n_resamples: Number of bootstrap draws.
        confidence_level: Central interval mass.
        seed: Optional random seed for reproducible resamples.
        drop_missing: When ``True``, rows with ``None`` or ``NaN`` are ignored.

    Returns:
        ``BootstrapResult`` with the observed estimate, percentile interval, and
        bootstrap standard error.

    Assumptions:
        The observed rows are treated as exchangeable draws from the target sample
        design. This is not appropriate for clustered or repeated-measures data.

    Example:
        >>> result = bootstrap_metric([1, 1, 0, 1], seed=7, n_resamples=200)
        >>> round(result.estimate, 2)
        0.75
    """

    cleaned = _clean_numeric(values, drop_missing=drop_missing, name="values")
    if metric is not None and not callable(metric):
        raise ValueError("metric must be callable")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")
    metric_function = metric or _default_metric
    rng = random.Random(seed)
    estimate = float(metric_function(cleaned))
    draws = [
        float(metric_function([cleaned[rng.randrange(len(cleaned))] for _ in range(len(cleaned))]))
        for _ in range(n_resamples)
    ]
    standard_error = 0.0 if len(draws) == 1 else math.sqrt(
        sum((draw - fmean(draws)) ** 2 for draw in draws) / (len(draws) - 1)
    )
    return BootstrapResult(
        estimate=estimate,
        confidence_interval=_percentile_interval(draws, confidence_level),
        standard_error=standard_error,
        resamples=n_resamples,
        method="ordinary bootstrap",
        assumptions="Rows are exchangeable and capture the variation relevant to the metric.",
    )


def cluster_bootstrap_metric(
    values: Iterable[Number | None],
    clusters: Iterable[object | None],
    metric: MetricFunction | None = None,
    *,
    n_resamples: int = 2000,
    confidence_level: float = 0.95,
    seed: int | None = None,
    drop_missing: bool = False,
) -> BootstrapResult:
    """Estimate uncertainty using a cluster bootstrap.

    Args:
        values: Metric inputs such as 1/0 correctness indicators.
        clusters: Cluster identifier for each value, such as document or project ID.
        metric: Function applied within each cluster before averaging across
            sampled clusters. The default returns the mean cluster-level value.
        n_resamples: Number of bootstrap cluster draws.
        confidence_level: Central interval mass.
        seed: Optional random seed.
        drop_missing: When ``True``, pairs with missing values or missing cluster IDs
            are removed before resampling.

    Returns:
        ``BootstrapResult`` summarizing a cluster-level metric estimate.

    Assumptions:
        Clusters are the resampling unit and the estimand is the average
        cluster-level metric. Dependence is allowed within a cluster, but sampled
        clusters are assumed representative of the cluster population.

    Example:
        >>> result = cluster_bootstrap_metric([1, 0, 1, 1], ["a", "a", "b", "b"], seed=11, n_resamples=200)
        >>> round(result.estimate, 2)
        0.75
    """

    value_list = list(values)
    cluster_list = list(clusters)
    if len(value_list) != len(cluster_list):
        raise ValueError("values and clusters must have equal length")
    if metric is not None and not callable(metric):
        raise ValueError("metric must be callable")
    paired: list[tuple[float, object]] = []
    for value, cluster in zip(value_list, cluster_list):
        if _is_missing(value) or _is_missing(cluster):
            if drop_missing:
                continue
            raise ValueError("values and clusters must not contain missing entries")
        paired.append((float(value), cluster))
    if not paired:
        raise ValueError("at least one non-missing clustered observation is required")
    groups: dict[object, list[float]] = {}
    for value, cluster in paired:
        groups.setdefault(cluster, []).append(value)
    cluster_ids = list(groups)
    if not cluster_ids:
        raise ValueError("at least one non-empty cluster is required")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")
    metric_function = metric or _default_metric
    rng = random.Random(seed)
    cluster_summaries = [float(metric_function(cluster_values)) for cluster_values in groups.values()]
    estimate = fmean(cluster_summaries)
    draws: list[float] = []
    for _ in range(n_resamples):
        resampled_summaries: list[float] = []
        for _ in cluster_ids:
            sampled_cluster = cluster_ids[rng.randrange(len(cluster_ids))]
            resampled_summaries.append(float(metric_function(groups[sampled_cluster])))
        draws.append(fmean(resampled_summaries))
    standard_error = 0.0 if len(draws) == 1 else math.sqrt(
        sum((draw - fmean(draws)) ** 2 for draw in draws) / (len(draws) - 1)
    )
    return BootstrapResult(
        estimate=estimate,
        confidence_interval=_percentile_interval(draws, confidence_level),
        standard_error=standard_error,
        resamples=n_resamples,
        method="cluster bootstrap",
        assumptions="Clusters are exchangeable; within-cluster dependence is preserved, and the estimand is the average cluster-level metric.",
    )


def compare_paired_predictions(
    y_true: Iterable[object | None],
    pred_a: Iterable[object | None],
    pred_b: Iterable[object | None],
    *,
    n_resamples: int = 2000,
    n_permutations: int = 5000,
    confidence_level: float = 0.95,
    seed: int | None = None,
    drop_missing: bool = False,
) -> PairedPredictionComparison:
    """Compare paired prediction accuracy for the same examples.

    The returned effect is ``accuracy_a - accuracy_b``.

    Assumptions:
        The same evaluation examples are scored by both systems, and the sampled
        pairs are representative of the comparison question.

    Example:
        >>> result = compare_paired_predictions([1, 0, 1], [1, 0, 1], [1, 1, 0], seed=5, n_resamples=200, n_permutations=200)
        >>> round(result.difference, 2)
        0.67
    """

    cleaned = _clean_pairs(y_true, pred_a, pred_b, drop_missing=drop_missing)
    if n_resamples <= 0 or n_permutations <= 0:
        raise ValueError("n_resamples and n_permutations must be positive")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")
    rng = random.Random(seed)
    correctness_a = [1.0 if truth == first else 0.0 for truth, first, _ in cleaned]
    correctness_b = [1.0 if truth == second else 0.0 for truth, _, second in cleaned]
    differences = [a - b for a, b in zip(correctness_a, correctness_b)]
    observed = fmean(differences)
    bootstrap_draws: list[float] = []
    for _ in range(n_resamples):
        sampled = [differences[rng.randrange(len(differences))] for _ in range(len(differences))]
        bootstrap_draws.append(fmean(sampled))
    discordant = [difference for difference in differences if difference != 0.0]
    if not discordant:
        p_value = 1.0
    elif len(discordant) <= 20:
        extreme = 0
        total = 2 ** len(discordant)
        observed_sum = abs(sum(discordant))
        for mask in range(total):
            signed_sum = 0.0
            for index, value in enumerate(discordant):
                sign = -1.0 if (mask >> index) & 1 else 1.0
                signed_sum += sign * abs(value)
            if abs(signed_sum) >= observed_sum - 1e-12:
                extreme += 1
        p_value = extreme / total
    else:
        observed_sum = abs(sum(discordant))
        extreme = 0
        for _ in range(n_permutations):
            signed_sum = sum((1 if rng.random() < 0.5 else -1) * abs(value) for value in discordant)
            if abs(signed_sum) >= observed_sum - 1e-12:
                extreme += 1
        p_value = extreme / n_permutations
    return PairedPredictionComparison(
        metric_name="accuracy",
        difference=observed,
        confidence_interval=_percentile_interval(bootstrap_draws, confidence_level),
        p_value=p_value,
        n_pairs=len(cleaned),
        method="paired bootstrap interval with paired-label permutation test",
        assumptions="Pairs refer to the same evaluation units; interpretation depends on paired comparability and representative sampling.",
    )


def _wilson_interval(successes: int, total: int, confidence_level: float) -> tuple[float, float]:
    if total <= 0:
        raise ValueError("total must be positive")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")
    proportion = successes / total
    z = _normal_ppf(1.0 - (1.0 - confidence_level) / 2.0)
    denominator = 1.0 + (z * z) / total
    center = (proportion + (z * z) / (2.0 * total)) / denominator
    margin = (z / denominator) * math.sqrt((proportion * (1.0 - proportion) / total) + (z * z) / (4.0 * total * total))
    return (max(0.0, center - margin), min(1.0, center + margin))


def compare_independent_proportions(
    successes_a: int,
    total_a: int,
    successes_b: int,
    total_b: int,
    *,
    confidence_level: float = 0.95,
) -> IndependentProportionComparison:
    """Compare two independent proportions.

    The effect is ``proportion_a - proportion_b``. The p-value uses the pooled
    two-sided z-test and the interval uses the Newcombe-Wilson difference method.

    Assumptions:
        The two groups are independent, each group consists of Bernoulli outcomes,
        and the estimand is a difference in group-level proportions.

    Example:
        >>> result = compare_independent_proportions(45, 50, 40, 50)
        >>> round(result.difference, 2)
        0.1
    """

    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")
    for successes, total, label in ((successes_a, total_a, "a"), (successes_b, total_b, "b")):
        if total <= 0:
            raise ValueError(f"total_{label} must be positive")
        if successes < 0 or successes > total:
            raise ValueError(f"successes_{label} must be between 0 and total_{label}")
    proportion_a = successes_a / total_a
    proportion_b = successes_b / total_b
    difference = proportion_a - proportion_b
    pooled = (successes_a + successes_b) / (total_a + total_b)
    variance = pooled * (1.0 - pooled) * ((1.0 / total_a) + (1.0 / total_b))
    if variance == 0.0:
        p_value = 1.0 if difference == 0.0 else 0.0
    else:
        z_score = difference / math.sqrt(variance)
        p_value = math.erfc(abs(z_score) / math.sqrt(2.0))
    interval_a = _wilson_interval(successes_a, total_a, confidence_level)
    interval_b = _wilson_interval(successes_b, total_b, confidence_level)
    lower = difference - math.sqrt((proportion_a - interval_a[0]) ** 2 + (proportion_b - interval_b[0]) ** 2)
    upper = difference + math.sqrt((interval_a[1] - proportion_a) ** 2 + (interval_b[1] - proportion_b) ** 2)
    return IndependentProportionComparison(
        proportion_a=proportion_a,
        proportion_b=proportion_b,
        difference=difference,
        confidence_interval=(max(-1.0, lower), min(1.0, upper)),
        p_value=p_value,
        method="Newcombe-Wilson interval with pooled two-sided z-test",
        assumptions="Groups are independent Bernoulli samples; dependence or repeated measures require a different design.",
    )


def _power_for_difference(
    baseline_rate: float,
    alternative_rate: float,
    sample_size_per_group: int,
    *,
    alpha: float,
    two_sided: bool,
    design_effect: float,
) -> float:
    if sample_size_per_group <= 0:
        raise ValueError("sample_size_per_group must be positive")
    effective_n = sample_size_per_group / design_effect
    if effective_n <= 0:
        raise ValueError("design_effect must be positive")
    delta = alternative_rate - baseline_rate
    pbar = (baseline_rate + alternative_rate) / 2.0
    threshold = _normal_ppf(1.0 - alpha / (2.0 if two_sided else 1.0)) * math.sqrt(
        max(1e-12, 2.0 * pbar * (1.0 - pbar) / effective_n)
    )
    standard_error = math.sqrt(
        max(1e-12, (baseline_rate * (1.0 - baseline_rate) + alternative_rate * (1.0 - alternative_rate)) / effective_n)
    )
    upper_tail = 1.0 - _normal_cdf((threshold - delta) / standard_error)
    if not two_sided:
        return upper_tail
    lower_tail = _normal_cdf((-threshold - delta) / standard_error)
    return upper_tail + lower_tail


def _validate_planning_inputs(
    baseline_rate: float,
    alpha: float,
    power: float,
    design_effect: float,
    direction: str,
) -> None:
    if not 0.0 < baseline_rate < 1.0:
        raise ValueError("baseline_rate must be between 0 and 1")
    if not 0.0 < alpha < 1.0 or not 0.0 < power < 1.0:
        raise ValueError("alpha and power must be between 0 and 1")
    if design_effect <= 0.0:
        raise ValueError("design_effect must be positive")
    if direction not in {"increase", "decrease"}:
        raise ValueError("direction must be 'increase' or 'decrease'")


def minimum_detectable_effect(
    baseline_rate: float,
    sample_size_per_group: int,
    *,
    alpha: float = 0.05,
    power: float = 0.8,
    two_sided: bool = True,
    design_effect: float = 1.0,
    direction: str = "increase",
) -> float:
    """Approximate the minimum detectable absolute effect for two proportions.

    Args:
        baseline_rate: Reference success rate for the current system.
        sample_size_per_group: Planned sample size for each arm.
        alpha: Type I error rate.
        power: Desired statistical power.
        two_sided: Whether the test is two-sided.
        design_effect: Inflation factor for clustered sampling. Use ``1.0`` only
            when the independent-sampling approximation is credible.
        direction: ``"increase"`` or ``"decrease"``.

    Returns:
        Absolute effect size on the proportion scale.

    Assumptions:
        Equal-sized groups and a normal approximation for independent Bernoulli data.
        Clustered studies should supply an externally justified design effect.

    Example:
        >>> effect = minimum_detectable_effect(0.8, 400, power=0.8)
        >>> 0 < effect < 0.2
        True
    """

    if sample_size_per_group <= 0:
        raise ValueError("sample_size_per_group must be positive")
    _validate_planning_inputs(baseline_rate, alpha, power, design_effect, direction)
    upper_bound = 1.0 - baseline_rate if direction == "increase" else baseline_rate
    extreme_rate = baseline_rate + upper_bound if direction == "increase" else baseline_rate - upper_bound
    max_power = _power_for_difference(
        baseline_rate,
        extreme_rate,
        sample_size_per_group,
        alpha=alpha,
        two_sided=two_sided,
        design_effect=design_effect,
    )
    if max_power < power:
        raise ValueError("requested power is unattainable for the given sample size and baseline rate")
    low, high = 0.0, upper_bound
    for _ in range(60):
        midpoint = (low + high) / 2.0
        alternative_rate = baseline_rate + midpoint if direction == "increase" else baseline_rate - midpoint
        if _power_for_difference(
            baseline_rate,
            alternative_rate,
            sample_size_per_group,
            alpha=alpha,
            two_sided=two_sided,
            design_effect=design_effect,
        ) >= power:
            high = midpoint
        else:
            low = midpoint
    return high


def required_sample_size(
    baseline_rate: float,
    minimum_effect: float,
    *,
    alpha: float = 0.05,
    power: float = 0.8,
    two_sided: bool = True,
    design_effect: float = 1.0,
    direction: str = "increase",
) -> int:
    """Approximate the per-group sample size for a two-proportion comparison.

    Args:
        baseline_rate: Reference success rate.
        minimum_effect: Smallest effect worth detecting on the absolute proportion scale.
        alpha: Type I error rate.
        power: Desired power.
        two_sided: Whether the test is two-sided.
        design_effect: Inflation factor for clustered designs.
        direction: ``"increase"`` or ``"decrease"``.

    Returns:
        Integer per-group sample size.

    Assumptions:
        Equal-sized groups and a normal approximation for independent Bernoulli data.
        This function deliberately does not automate cluster-correlation estimation.

    Example:
        >>> required_sample_size(0.8, 0.05, power=0.8) > 0
        True
    """

    if minimum_effect <= 0.0:
        raise ValueError("minimum_effect must be positive")
    _validate_planning_inputs(baseline_rate, alpha, power, design_effect, direction)
    alternative_rate = baseline_rate + minimum_effect if direction == "increase" else baseline_rate - minimum_effect
    if not 0.0 < alternative_rate < 1.0:
        raise ValueError("minimum_effect is incompatible with baseline_rate and direction")
    low, high = 2, 4
    while _power_for_difference(
        baseline_rate,
        alternative_rate,
        high,
        alpha=alpha,
        two_sided=two_sided,
        design_effect=design_effect,
    ) < power:
        low, high = high, high * 2
        if high > 10_000_000:
            raise ValueError("required sample size exceeds search limit")
    while low + 1 < high:
        midpoint = (low + high) // 2
        if _power_for_difference(
            baseline_rate,
            alternative_rate,
            midpoint,
            alpha=alpha,
            two_sided=two_sided,
            design_effect=design_effect,
        ) >= power:
            high = midpoint
        else:
            low = midpoint
    return high


def metric_comparability_check(
    *,
    same_examples: bool | None,
    same_ground_truth: bool | None,
    same_scoring_code: bool | None,
    same_metric_definitions: bool | None,
    same_thresholds: bool | None,
    same_preprocessing: bool | None,
    same_operating_conditions: bool | None,
    notes: Mapping[str, str] | None = None,
) -> ComparabilityResult:
    """Classify how directly two evaluation results can be compared.

    The function does not estimate metric values. It documents whether the core
    ingredients of comparability match closely enough for a direct numerical claim.

    Example:
        >>> result = metric_comparability_check(
        ...     same_examples=True,
        ...     same_ground_truth=True,
        ...     same_scoring_code=True,
        ...     same_metric_definitions=True,
        ...     same_thresholds=False,
        ...     same_preprocessing=True,
        ...     same_operating_conditions=True,
        ... )
        >>> result.classification
        'Comparable with limitations'
    """

    status_map = {
        "same_examples": same_examples,
        "same_ground_truth": same_ground_truth,
        "same_scoring_code": same_scoring_code,
        "same_metric_definitions": same_metric_definitions,
        "same_thresholds": same_thresholds,
        "same_preprocessing": same_preprocessing,
        "same_operating_conditions": same_operating_conditions,
    }
    details = {
        key: "same" if value is True else "different" if value is False else "undocumented"
        for key, value in status_map.items()
    }
    critical_fields = (
        "same_examples",
        "same_ground_truth",
        "same_scoring_code",
        "same_metric_definitions",
    )
    limitations = [
        f"{field.replace('_', ' ')}: {details[field]}"
        for field, value in status_map.items()
        if value is not True
    ]
    if any(status_map[field] is False for field in critical_fields):
        classification = "Not directly comparable"
    elif all(value is True for value in status_map.values()):
        classification = "Directly comparable"
    else:
        classification = "Comparable with limitations"
    if notes:
        limitations.extend(f"note - {key}: {value}" for key, value in notes.items())
    return ComparabilityResult(
        classification=classification,
        details=details,
        limitations=tuple(limitations),
    )
