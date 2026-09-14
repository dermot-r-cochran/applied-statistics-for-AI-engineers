from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import TypedDict


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
                lower=round(index * bucket_width, 2),
                upper=round((index + 1) * bucket_width, 2),
                count=len(bucket),
                average_score=round(average_score, 3),
                observed_rate=round(observed_rate, 3),
            )
        )

    return output


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
