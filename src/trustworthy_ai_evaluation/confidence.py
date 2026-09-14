"""Confidence, calibration, and comparability utilities for synthetic AI evaluation examples."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal, Sequence

import numpy as np
from sklearn.metrics import brier_score_loss


@dataclass(frozen=True)
class CalibrationBin:
    """One bin in a calibration curve.

    Attributes:
        bin_index: Zero-based bin index.
        lower: Inclusive lower score bound used for reporting.
        upper: Upper score bound used for reporting.
        count: Number of examples in the bin.
        mean_score: Mean score within the bin.
        observed_frequency: Empirical event frequency within the bin.
    """

    bin_index: int
    lower: float
    upper: float
    count: int
    mean_score: float
    observed_frequency: float


@dataclass(frozen=True)
class BrierScoreSummary:
    """Binary Brier score summary.

    Attributes:
        brier_score: Mean squared error between probabilities and outcomes.
        uncertainty: Baseline variance of the outcome prevalence.
        resolution: Between-bin separation in observed event rates.
        reliability: Within-bin calibration error contribution.
        mean_probability: Mean predicted probability.
        observed_rate: Mean observed outcome rate.
    """

    brier_score: float
    uncertainty: float
    resolution: float
    reliability: float
    mean_probability: float
    observed_rate: float


@dataclass(frozen=True)
class SubgroupMetricRow:
    """Metrics for one subgroup."""

    group: str
    count: int
    positive_rate: float
    accuracy_at_0_5: float
    mean_score: float
    brier_score: float
    expected_calibration_error: float


@dataclass(frozen=True)
class MetricComparabilityReport:
    """Structured comparability result for two metrics or scores."""

    verdict: Literal[
        "directly comparable",
        "comparable with limitations",
        "not directly comparable",
    ]
    reasons: tuple[str, ...]
    recommended_actions: tuple[str, ...]


ArrayLike = Sequence[float] | Sequence[int] | np.ndarray


def _as_numpy(values: ArrayLike, *, name: str) -> np.ndarray:
    array = np.asarray(values)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional.")
    if array.size == 0:
        raise ValueError(f"{name} must not be empty.")
    if array.dtype.kind in {"i", "u", "f", "b"}:
        if np.isnan(array.astype(float)).any():
            raise ValueError(f"{name} must not contain missing values.")
    else:
        for value in array.tolist():
            if value is None or (isinstance(value, float) and np.isnan(value)):
                raise ValueError(f"{name} must not contain missing values.")
    return array


def _validate_binary_targets(y_true: ArrayLike) -> np.ndarray:
    targets = _as_numpy(y_true, name="y_true").astype(int)
    unique = np.unique(targets)
    if not np.all(np.isin(unique, [0, 1])):
        raise ValueError("y_true must contain only 0 and 1.")
    return targets


def _validate_unit_interval(values: ArrayLike, *, name: str) -> np.ndarray:
    array = _as_numpy(values, name=name).astype(float)
    if np.any((array < 0.0) | (array > 1.0)):
        raise ValueError(f"{name} must lie in the closed interval [0, 1].")
    return array


def _validate_equal_lengths(**arrays: np.ndarray) -> None:
    lengths = {name: array.shape[0] for name, array in arrays.items()}
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Inputs must have equal length; got {lengths}.")


def _bin_edges(scores: np.ndarray, n_bins: int, strategy: Literal["uniform", "quantile"]) -> np.ndarray:
    if n_bins < 1:
        raise ValueError("n_bins must be at least 1.")
    if strategy == "uniform":
        edges = np.linspace(0.0, 1.0, n_bins + 1)
    elif strategy == "quantile":
        edges = np.quantile(scores, np.linspace(0.0, 1.0, n_bins + 1))
        edges[0] = 0.0
        edges[-1] = 1.0
        edges = np.unique(edges)
        if edges.size == 1:
            edges = np.array([0.0, 1.0])
    else:
        raise ValueError("strategy must be 'uniform' or 'quantile'.")
    return edges


def calibration_curve_data(
    y_true: ArrayLike,
    scores: ArrayLike,
    *,
    n_bins: int = 10,
    strategy: Literal["uniform", "quantile"] = "uniform",
) -> list[CalibrationBin]:
    """Return calibration-curve bin summaries for binary outcomes.

    Args:
        y_true: Binary outcomes encoded as 0 or 1.
        scores: Scores or probabilities in the unit interval.
        n_bins: Requested number of bins.
        strategy: Bin construction strategy.

    Returns:
        A list of non-empty :class:`CalibrationBin` objects.

    Assumptions:
        - ``y_true`` and ``scores`` describe the same examples in the same order.
        - ``scores`` lie in ``[0, 1]`` but need not already be calibrated probabilities.
        - The returned empirical frequencies are descriptive summaries, not ground-truth functions.

    Examples:
        >>> bins = calibration_curve_data([0, 1, 1, 0], [0.1, 0.8, 0.7, 0.2], n_bins=2)
        >>> [item.count for item in bins]
        [2, 2]
        >>> round(bins[-1].observed_frequency, 2)
        1.0
    """

    targets = _validate_binary_targets(y_true)
    score_array = _validate_unit_interval(scores, name="scores")
    _validate_equal_lengths(y_true=targets, scores=score_array)

    edges = _bin_edges(score_array, n_bins=n_bins, strategy=strategy)
    bins: list[CalibrationBin] = []

    for index, (lower, upper) in enumerate(zip(edges[:-1], edges[1:])):
        if index == len(edges) - 2:
            mask = (score_array >= lower) & (score_array <= upper)
        else:
            mask = (score_array >= lower) & (score_array < upper)
        if not np.any(mask):
            continue
        bins.append(
            CalibrationBin(
                bin_index=index,
                lower=float(lower),
                upper=float(upper),
                count=int(mask.sum()),
                mean_score=float(score_array[mask].mean()),
                observed_frequency=float(targets[mask].mean()),
            )
        )
    return bins


def expected_calibration_error(
    y_true: ArrayLike,
    scores: ArrayLike,
    *,
    n_bins: int = 10,
    strategy: Literal["uniform", "quantile"] = "uniform",
) -> float:
    """Compute expected calibration error for binary outcomes.

    The result is a weighted average of absolute bin-level calibration gaps.

    Assumptions:
        - The task is binary.
        - Calibration is evaluated over the chosen binning scheme, so the result depends on that scheme.
        - This statistic does not capture ranking quality, subgroup harm, or all forms of calibration failure.

    Examples:
        >>> round(expected_calibration_error([0, 1], [0.0, 1.0], n_bins=2), 4)
        0.0
        >>> round(expected_calibration_error([0, 0, 1, 1], [0.9, 0.8, 0.2, 0.1], n_bins=2), 2)
        0.85
    """

    bins = calibration_curve_data(y_true, scores, n_bins=n_bins, strategy=strategy)
    total = sum(item.count for item in bins)
    return float(
        sum(
            (item.count / total) * abs(item.mean_score - item.observed_frequency)
            for item in bins
        )
    )


def brier_score_summary(
    y_true: ArrayLike,
    probabilities: ArrayLike,
    *,
    n_bins: int = 10,
    strategy: Literal["uniform", "quantile"] = "uniform",
) -> BrierScoreSummary:
    """Summarize the binary Brier score and a coarse Murphy-style decomposition.

    Args:
        y_true: Binary outcomes encoded as 0 or 1.
        probabilities: Estimated probabilities in ``[0, 1]``.
        n_bins: Number of bins for the decomposition summary.
        strategy: Binning strategy for the decomposition summary.

    Returns:
        A :class:`BrierScoreSummary` object.

    Assumptions:
        - ``probabilities`` aim to estimate ``P(Y=1)`` for the same event measured in ``y_true``.
        - The reliability and resolution terms use binning, so they are approximations rather than exact decompositions.
        - For single-class samples, uncertainty becomes zero by definition.

    Examples:
        >>> summary = brier_score_summary([0, 1], [0.1, 0.9], n_bins=2)
        >>> round(summary.brier_score, 2)
        0.01
        >>> round(summary.observed_rate, 2)
        0.5
    """

    targets = _validate_binary_targets(y_true)
    probs = _validate_unit_interval(probabilities, name="probabilities")
    _validate_equal_lengths(y_true=targets, probabilities=probs)

    bins = calibration_curve_data(targets, probs, n_bins=n_bins, strategy=strategy)
    observed_rate = float(targets.mean())
    uncertainty = observed_rate * (1.0 - observed_rate)
    reliability = 0.0
    resolution = 0.0
    total = len(targets)
    for item in bins:
        weight = item.count / total
        reliability += weight * (item.mean_score - item.observed_frequency) ** 2
        resolution += weight * (item.observed_frequency - observed_rate) ** 2

    return BrierScoreSummary(
        brier_score=float(brier_score_loss(targets, probs)),
        uncertainty=float(uncertainty),
        resolution=float(resolution),
        reliability=float(reliability),
        mean_probability=float(probs.mean()),
        observed_rate=observed_rate,
    )


def subgroup_metric_report(
    groups: Sequence[str] | np.ndarray,
    y_true: ArrayLike,
    scores: ArrayLike,
    *,
    n_bins: int = 10,
) -> list[SubgroupMetricRow]:
    """Compute simple binary-score diagnostics for each subgroup.

    Args:
        groups: Group label for each example.
        y_true: Binary outcomes encoded as 0 or 1.
        scores: Scores or probabilities in ``[0, 1]``.
        n_bins: Bin count passed to expected calibration error.

    Returns:
        One :class:`SubgroupMetricRow` per observed subgroup.

    Assumptions:
        - Group labels are observed without error.
        - Scores are comparable within each subgroup because they target the same event.
        - Small subgroups can yield unstable calibration summaries.

    Examples:
        >>> rows = subgroup_metric_report(
        ...     ["A", "A", "B", "B"],
        ...     [0, 1, 0, 1],
        ...     [0.1, 0.9, 0.2, 0.8],
        ...     n_bins=2,
        ... )
        >>> [row.group for row in rows]
        ['A', 'B']
    """

    group_array = _as_numpy(groups, name="groups").astype(str)
    targets = _validate_binary_targets(y_true)
    score_array = _validate_unit_interval(scores, name="scores")
    _validate_equal_lengths(groups=group_array, y_true=targets, scores=score_array)

    rows: list[SubgroupMetricRow] = []
    for group in sorted(np.unique(group_array)):
        mask = group_array == group
        group_targets = targets[mask]
        group_scores = score_array[mask]
        rows.append(
            SubgroupMetricRow(
                group=str(group),
                count=int(mask.sum()),
                positive_rate=float(group_targets.mean()),
                accuracy_at_0_5=float(((group_scores >= 0.5).astype(int) == group_targets).mean()),
                mean_score=float(group_scores.mean()),
                brier_score=float(brier_score_loss(group_targets, group_scores)),
                expected_calibration_error=expected_calibration_error(
                    group_targets,
                    group_scores,
                    n_bins=min(n_bins, max(1, group_targets.size)),
                    strategy="uniform",
                ),
            )
        )
    return rows


def metric_comparability_check(
    *,
    metric_name: str,
    producing_component_a: str,
    producing_component_b: str,
    intended_meaning_a: str,
    intended_meaning_b: str,
    mathematical_range_a: tuple[float, float],
    mathematical_range_b: tuple[float, float],
    claims_probability_a: bool,
    claims_probability_b: bool,
    calibration_population_a: str | None = None,
    calibration_population_b: str | None = None,
    dependency_assumptions_a: str | None = None,
    dependency_assumptions_b: str | None = None,
) -> MetricComparabilityReport:
    """Assess whether two confidence-like scores are directly comparable.

    Args:
        metric_name: Human-readable score or metric name.
        producing_component_a: Name of the first component.
        producing_component_b: Name of the second component.
        intended_meaning_a: What the first score is supposed to mean.
        intended_meaning_b: What the second score is supposed to mean.
        mathematical_range_a: Reported numeric range for the first score.
        mathematical_range_b: Reported numeric range for the second score.
        claims_probability_a: Whether the first score claims to be a probability.
        claims_probability_b: Whether the second score claims to be a probability.
        calibration_population_a: Calibration population for the first score, if any.
        calibration_population_b: Calibration population for the second score, if any.
        dependency_assumptions_a: Dependence assumptions attached to the first score.
        dependency_assumptions_b: Dependence assumptions attached to the second score.

    Returns:
        A structured :class:`MetricComparabilityReport`.

    Assumptions:
        - This is a governance aid, not a theorem prover.
        - Direct comparability requires semantic alignment, not just shared numeric range.
        - Human review is still needed for important decisions.

    Examples:
        >>> report = metric_comparability_check(
        ...     metric_name="confidence",
        ...     producing_component_a="classifier",
        ...     producing_component_b="retriever",
        ...     intended_meaning_a="Estimated probability the class label is correct.",
        ...     intended_meaning_b="Ranking margin for the top evidence chunk.",
        ...     mathematical_range_a=(0.0, 1.0),
        ...     mathematical_range_b=(0.0, 1.0),
        ...     claims_probability_a=True,
        ...     claims_probability_b=False,
        ... )
        >>> report.verdict
        'not directly comparable'
    """

    reasons: list[str] = []
    recommended_actions: list[str] = []

    if mathematical_range_a != mathematical_range_b:
        reasons.append("The scores do not even share the same reported numeric range.")
    if intended_meaning_a.strip().lower() != intended_meaning_b.strip().lower():
        reasons.append("The scores have different intended meanings.")
    if claims_probability_a != claims_probability_b:
        reasons.append("Only one score claims to be a probability.")
    if claims_probability_a and claims_probability_b and calibration_population_a != calibration_population_b:
        reasons.append("The scores were calibrated on different populations.")
    if (dependency_assumptions_a or "") != (dependency_assumptions_b or ""):
        reasons.append("The scores rely on different dependency assumptions.")
    if producing_component_a != producing_component_b:
        recommended_actions.append(
            "Do not average or multiply the scores until you validate a shared end-to-end target."
        )
    if claims_probability_a and claims_probability_b:
        recommended_actions.append(
            "Validate calibration on the deployment population before treating either score as a probability."
        )
    else:
        recommended_actions.append(
            "Translate each score into an explicitly defined event probability or keep the scores separate."
        )

    if not reasons:
        verdict: Literal[
            "directly comparable",
            "comparable with limitations",
            "not directly comparable",
        ] = "directly comparable"
    elif any(
        problem in reasons
        for problem in (
            "The scores have different intended meanings.",
            "Only one score claims to be a probability.",
            "The scores do not even share the same reported numeric range.",
        )
    ):
        verdict = "not directly comparable"
    else:
        verdict = "comparable with limitations"

    return MetricComparabilityReport(
        verdict=verdict,
        reasons=tuple(reasons),
        recommended_actions=tuple(recommended_actions),
    )
