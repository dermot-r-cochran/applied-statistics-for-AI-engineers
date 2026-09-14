"""Confidence and calibration utilities for Project Frog examples."""

from __future__ import annotations

from typing import Literal, Sequence

import numpy as np
import pandas as pd


Strategy = Literal["quantile", "uniform"]


def _validate_binary_prob_inputs(y_true: Sequence[int | bool], y_prob: Sequence[float]) -> tuple[np.ndarray, np.ndarray]:
    truth = np.asarray(y_true, dtype=float)
    prob = np.asarray(y_prob, dtype=float)
    if truth.size == 0 or prob.size == 0:
        raise ValueError("Inputs must not be empty.")
    if truth.size != prob.size:
        raise ValueError("Inputs must have the same length.")
    if np.isnan(truth).any() or np.isnan(prob).any():
        raise ValueError("Inputs contain missing values.")
    if not np.isin(truth, [0.0, 1.0]).all():
        raise ValueError("y_true must be binary.")
    if np.any((prob < 0.0) | (prob > 1.0)):
        raise ValueError("y_prob values must lie between 0 and 1.")
    return truth.astype(int), prob


def calibration_curve_data(
    y_true: Sequence[int | bool],
    y_prob: Sequence[float],
    *,
    n_bins: int = 10,
    strategy: Strategy = "quantile",
) -> pd.DataFrame:
    """Create binned calibration-curve data.

    Assumptions:
        * ``y_true`` is binary.
        * Bins summarize the observed sample and can change with another sample.

    Examples:
        >>> curve = calibration_curve_data([0, 1, 1, 0], [0.1, 0.8, 0.6, 0.2], n_bins=2)
        >>> int(curve['count'].sum())
        4
    """

    if n_bins <= 0:
        raise ValueError("n_bins must be positive.")
    truth, prob = _validate_binary_prob_inputs(y_true, y_prob)

    if strategy == "quantile":
        edges = np.quantile(prob, np.linspace(0.0, 1.0, n_bins + 1))
        edges[0], edges[-1] = 0.0, 1.0
    elif strategy == "uniform":
        edges = np.linspace(0.0, 1.0, n_bins + 1)
    else:
        raise ValueError("strategy must be 'quantile' or 'uniform'.")

    bin_ids = np.digitize(prob, edges[1:-1], right=True)
    rows = []
    for bin_index in range(n_bins):
        mask = bin_ids == bin_index
        if not np.any(mask):
            continue
        rows.append(
            {
                "bin": bin_index,
                "lower": float(edges[bin_index]),
                "upper": float(edges[bin_index + 1]),
                "midpoint": float((edges[bin_index] + edges[bin_index + 1]) / 2.0),
                "mean_prediction": float(np.mean(prob[mask])),
                "observed_rate": float(np.mean(truth[mask])),
                "count": int(np.sum(mask)),
            }
        )
    return pd.DataFrame(rows)


def expected_calibration_error(
    y_true: Sequence[int | bool],
    y_prob: Sequence[float],
    *,
    n_bins: int = 10,
    strategy: Strategy = "quantile",
) -> float:
    """Compute expected calibration error (ECE) from binned predictions.

    Assumptions:
        * ECE is a descriptive summary, not a complete calibration assessment.
        * Different binning choices can produce different ECE values.

    Examples:
        >>> round(expected_calibration_error([0, 1], [0.1, 0.9], n_bins=2), 3)
        0.1
    """

    curve = calibration_curve_data(y_true, y_prob, n_bins=n_bins, strategy=strategy)
    total = curve["count"].sum()
    return float(((curve["count"] / total) * (curve["mean_prediction"] - curve["observed_rate"]).abs()).sum())


def brier_score_summary(y_true: Sequence[int | bool], y_prob: Sequence[float]) -> dict[str, float]:
    """Summarize Brier-score style quantities for binary predictions.

    Assumptions:
        * ``y_true`` is binary.
        * The decomposition here is descriptive and centered on the observed sample.

    Examples:
        >>> summary = brier_score_summary([0, 1], [0.2, 0.8])
        >>> round(summary['brier_score'], 3)
        0.04
    """

    truth, prob = _validate_binary_prob_inputs(y_true, y_prob)
    base_rate = float(np.mean(truth))
    brier = float(np.mean((prob - truth) ** 2))
    uncertainty = float(base_rate * (1.0 - base_rate))
    return {
        "brier_score": brier,
        "base_rate": base_rate,
        "uncertainty": uncertainty,
        "skill_against_base_rate": uncertainty - brier,
    }


def subgroup_metric_report(
    frame: pd.DataFrame,
    *,
    group_column: str,
    outcome_column: str,
    probability_column: str,
    n_bins: int = 5,
) -> pd.DataFrame:
    """Report discrimination and calibration summaries by subgroup.

    Assumptions:
        * ``frame`` contains one row per prediction.
        * ``outcome_column`` is binary and ``probability_column`` is scaled to [0, 1].

    Examples:
        >>> df = pd.DataFrame({'group': ['a', 'a', 'b', 'b'], 'y': [1, 0, 1, 1], 'p': [0.8, 0.3, 0.7, 0.6]})
        >>> report = subgroup_metric_report(df, group_column='group', outcome_column='y', probability_column='p')
        >>> report['group'].tolist()
        ['a', 'b']
    """

    required = {group_column, outcome_column, probability_column}
    missing = required.difference(frame.columns)
    if missing:
        raise KeyError(f"Missing columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("frame must not be empty.")
    if frame[list(required)].isna().any().any():
        raise ValueError("frame contains missing values in required columns.")

    rows = []
    for group_value, subset in frame.groupby(group_column, dropna=False):
        y_true = subset[outcome_column].astype(int).to_numpy()
        y_prob = subset[probability_column].astype(float).to_numpy()
        curve = calibration_curve_data(y_true, y_prob, n_bins=max(1, min(n_bins, len(subset))))
        total = curve["count"].sum()
        rows.append(
            {
                "group": group_value,
                "rows": int(len(subset)),
                "observed_rate": float(np.mean(y_true)),
                "mean_probability": float(np.mean(y_prob)),
                "ece": float(((curve["count"] / total) * (curve["mean_prediction"] - curve["observed_rate"]).abs()).sum()),
                "brier_score": float(np.mean((y_prob - y_true) ** 2)),
            }
        )
    return pd.DataFrame(rows).sort_values("group").reset_index(drop=True)
