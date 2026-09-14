from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from random import Random
from statistics import NormalDist
from typing import Sequence, TypedDict


@dataclass(frozen=True)
class FrogExample:
    example_id: str
    habitat: str
    season: str
    score: float
    label: int


@dataclass(frozen=True)
class CalibrationBin:
    lower: float
    upper: float
    count: int
    average_score: float
    observed_rate: float


@dataclass(frozen=True)
class ProportionInterval:
    lower: float
    upper: float
    point_estimate: float
    sample_size: int
    effective_sample_size: float
    confidence_level: float
    method: str


@dataclass(frozen=True)
class MetricIntervalReport:
    metric_name: str
    successes: int
    total: int
    interval: ProportionInterval
    assumptions: tuple[str, ...]


class SliceSummary(TypedDict):
    count: int
    positive_rate: float
    average_score: float


def generate_project_frog_examples(size: int = 120, seed: int = 7) -> list[FrogExample]:
    if size <= 0:
        raise ValueError("size must be positive")

    habitats = ("wetland", "forest-edge", "urban-channel")
    seasons = ("spring", "summer", "autumn")
    rng = Random(seed)
    examples: list[FrogExample] = []

    for index in range(size):
        habitat = habitats[index % len(habitats)]
        season = seasons[(index // len(habitats)) % len(seasons)]
        habitat_bias = {"wetland": 0.18, "forest-edge": 0.04, "urban-channel": -0.08}[habitat]
        season_bias = {"spring": 0.12, "summer": -0.02, "autumn": 0.05}[season]
        latent_risk = 0.48 + habitat_bias + season_bias + rng.uniform(-0.24, 0.24)
        score = min(max(latent_risk + rng.uniform(-0.1, 0.1), 0.01), 0.99)
        event_threshold = min(max(latent_risk + rng.uniform(-0.12, 0.12), 0.05), 0.95)
        label = int(rng.random() < event_threshold)
        examples.append(
            FrogExample(
                example_id=f"frog-{index + 1:03d}",
                habitat=habitat,
                season=season,
                score=round(score, 3),
                label=label,
            )
        )

    return examples


def calibration_bins(examples: list[FrogExample], bins: int = 5) -> list[CalibrationBin]:
    if bins <= 0:
        raise ValueError("bins must be positive")
    if not examples:
        return []

    bucket_width = 1 / bins
    grouped: list[list[FrogExample]] = [[] for _ in range(bins)]

    for example in examples:
        index = min(int(example.score / bucket_width), bins - 1)
        grouped[index].append(example)

    output: list[CalibrationBin] = []
    for index, bucket in enumerate(grouped):
        if not bucket:
            continue
        average_score = sum(example.score for example in bucket) / len(bucket)
        observed_rate = sum(example.label for example in bucket) / len(bucket)
        output.append(
            CalibrationBin(
                lower=index * bucket_width,
                upper=(index + 1) * bucket_width,
                count=len(bucket),
                average_score=round(average_score, 3),
                observed_rate=round(observed_rate, 3),
            )
        )

    return output


def wilson_interval(
    successes: int,
    total: int,
    confidence_level: float = 0.95,
    effective_sample_size: float | None = None,
) -> ProportionInterval:
    """Estimate a Wilson interval for an observed proportion.

    The observed point estimate is always computed from `successes / total`.
    When `effective_sample_size` is provided, the interval width is computed as
    though that observed proportion came from a smaller effective sample size.
    This is a teaching-oriented approximation for clustered or dependent rows:
    it preserves the observed rate while widening the interval under a reduced
    independence assumption.
    """
    if total <= 0:
        raise ValueError("total must be positive")
    if successes < 0 or successes > total:
        raise ValueError("successes must be between 0 and total")
    if confidence_level <= 0 or confidence_level >= 1:
        raise ValueError("confidence_level must be between 0 and 1")

    n = float(total if effective_sample_size is None else effective_sample_size)
    if n < 1 or n > total:
        raise ValueError("effective_sample_size must be at least 1 and no larger than total")

    point_estimate = successes / total
    effective_successes = point_estimate * n
    effective_point_estimate = effective_successes / n
    z_score = NormalDist().inv_cdf(0.5 + (confidence_level / 2))
    z_squared = z_score**2
    denominator = 1 + (z_squared / n)
    adjusted_center = (effective_point_estimate + (z_squared / (2 * n))) / denominator
    adjusted_margin = (
        z_score
        * sqrt(
            (effective_point_estimate * (1 - effective_point_estimate) / n)
            + (z_squared / (4 * n**2))
        )
        / denominator
    )

    return ProportionInterval(
        lower=max(0.0, adjusted_center - adjusted_margin),
        upper=min(1.0, adjusted_center + adjusted_margin),
        point_estimate=point_estimate,
        sample_size=total,
        effective_sample_size=n,
        confidence_level=confidence_level,
        method="Wilson",
    )


def metric_interval_report(
    metric_name: str,
    successes: int,
    total: int,
    confidence_level: float = 0.95,
    effective_sample_size: float | None = None,
    assumptions: Sequence[str] | None = None,
) -> MetricIntervalReport:
    """Package an observed metric with interval metadata and assumptions."""
    normalized_metric_name = metric_name.strip()
    if not normalized_metric_name:
        raise ValueError("metric_name must not be empty")

    interval = wilson_interval(
        successes=successes,
        total=total,
        confidence_level=confidence_level,
        effective_sample_size=effective_sample_size,
    )

    default_assumptions = (
        "Rows are treated as exchangeable observations from the target evaluation set.",
        "If rows are clustered or dependent, the effective sample size should be reduced.",
    )

    return MetricIntervalReport(
        metric_name=normalized_metric_name,
        successes=successes,
        total=total,
        interval=interval,
        assumptions=default_assumptions if assumptions is None else tuple(assumptions),
    )


def slice_summary(examples: list[FrogExample]) -> dict[str, SliceSummary]:
    if not examples:
        return {}

    grouped: dict[str, list[FrogExample]] = {}
    for example in examples:
        grouped.setdefault(example.habitat, []).append(example)

    return {
        habitat: {
            "count": len(bucket),
            "positive_rate": round(sum(example.label for example in bucket) / len(bucket), 3),
            "average_score": round(sum(example.score for example in bucket) / len(bucket), 3),
        }
        for habitat, bucket in grouped.items()
    }
