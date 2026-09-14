from __future__ import annotations

import numpy as np

from ._typing import ArrayLike


def effective_sample_size(
    sample_size: int | None = None,
    *,
    weights: ArrayLike | None = None,
    cluster_ids: ArrayLike | None = None,
    intra_cluster_correlation: float | None = None,
) -> float:
    """Estimate effective sample size under weighting or clustering.

    Use weights for a Kish effective sample size or cluster IDs with an intra-cluster
    correlation coefficient for a design-effect adjustment.

    Examples:
        >>> round(effective_sample_size(weights=[1, 1, 2, 2]), 2)
        3.6
        >>> round(
        ...     effective_sample_size(
        ...         cluster_ids=[1, 1, 2, 2, 3, 3],
        ...         intra_cluster_correlation=0.2,
        ...     ),
        ...     2,
        ... )
        5.0
    """
    if weights is not None:
        w = np.asarray(weights, dtype=float)
        if w.size == 0 or np.any(w <= 0):
            raise ValueError("weights must be positive and non-empty")
        return float((w.sum() ** 2) / np.sum(w**2))

    if cluster_ids is not None:
        clusters = np.asarray(cluster_ids)
        if clusters.size == 0:
            raise ValueError("cluster_ids must not be empty")
        if intra_cluster_correlation is None:
            raise ValueError("intra_cluster_correlation is required when cluster_ids are provided")
        if not 0 <= intra_cluster_correlation < 1:
            raise ValueError("intra_cluster_correlation must be between 0 and 1")
        _, counts = np.unique(clusters, return_counts=True)
        average_cluster_size = counts.mean()
        design_effect = 1 + (average_cluster_size - 1) * intra_cluster_correlation
        return float(clusters.size / design_effect)

    if sample_size is None or sample_size <= 0:
        raise ValueError("provide a positive sample_size, weights, or cluster_ids")
    return float(sample_size)
