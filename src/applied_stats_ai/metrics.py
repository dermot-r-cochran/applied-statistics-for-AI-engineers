from __future__ import annotations

from collections.abc import Callable

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from ._typing import ArrayLike
from .bootstrap import bootstrap_metric


def confusion_matrix_uncertainty(
    y_true: ArrayLike,
    y_pred: ArrayLike,
    n_resamples: int = 2_000,
    confidence_level: float = 0.95,
    random_state: int | None = None,
) -> dict[str, dict[str, float | np.ndarray] | np.ndarray]:
    """Return confusion matrix counts with bootstrap uncertainty for common metrics.

    Examples:
        >>> result = confusion_matrix_uncertainty(
        ...     [1, 0, 1],
        ...     [1, 0, 0],
        ...     n_resamples=100,
        ...     random_state=0,
        ... )
        >>> sorted(result["metrics"].keys())
        ['accuracy', 'f1', 'precision', 'recall']
    """
    y_true_array = np.asarray(y_true)
    y_pred_array = np.asarray(y_pred)
    if len(y_true_array) != len(y_pred_array):
        raise ValueError("y_true and y_pred must have equal length")
    if len(y_true_array) == 0:
        raise ValueError("inputs must not be empty")
    labels = set(np.unique(np.concatenate((y_true_array, y_pred_array))).tolist())
    if not labels.issubset({0, 1}):
        raise ValueError(
            "confusion_matrix_uncertainty currently supports binary labels encoded as 0/1"
        )

    pairs = np.column_stack((y_true_array, y_pred_array))

    def metric_from_pairs(
        metric_func: Callable[[np.ndarray, np.ndarray], float],
    ) -> Callable[[np.ndarray], float]:
        return lambda sample: float(metric_func(sample[:, 0], sample[:, 1]))

    metrics = {
        "accuracy": metric_from_pairs(accuracy_score),
        "precision": metric_from_pairs(lambda yt, yp: precision_score(yt, yp, zero_division=0)),
        "recall": metric_from_pairs(lambda yt, yp: recall_score(yt, yp, zero_division=0)),
        "f1": metric_from_pairs(lambda yt, yp: f1_score(yt, yp, zero_division=0)),
    }

    metric_results = {
        name: bootstrap_metric(
            pairs,
            metric,
            n_resamples=n_resamples,
            confidence_level=confidence_level,
            random_state=None if random_state is None else random_state + index,
        )
        for index, (name, metric) in enumerate(metrics.items())
    }

    return {
        "confusion_matrix": confusion_matrix(y_true_array, y_pred_array, labels=[0, 1]),
        "metrics": metric_results,
    }
