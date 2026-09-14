"""Synthetic helpers for the Project Frog progressive tutorial.

All examples in this module are fictional and reproducible.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import sqrt
from random import Random
from typing import Iterable, Sequence


@dataclass(frozen=True)
class FrogCase:
    """Synthetic Project Frog evaluation record.

    Attributes:
        case_id: Stable synthetic identifier.
        difficulty: One of ``Simple``, ``Moderate``, or ``Complex``.
        reference_class: Fictional reference label.
        predicted_class: Fictional model prediction.

    Assumptions:
        - The records are synthetic and do not represent real users or documents.
        - Difficulty acts as a coarse proxy for error risk.

    Example:
        >>> rows = generate_project_frog_cases(seed=7, n=2)
        >>> rows[0].difficulty in {"Simple", "Moderate", "Complex"}
        True
    """

    case_id: str
    difficulty: str
    reference_class: str
    predicted_class: str

    @property
    def prediction_correct(self) -> bool:
        """Return whether the fictional prediction matches the reference label.

        Example:
            >>> case = FrogCase("frog-1", "Simple", "Clear", "Clear")
            >>> case.prediction_correct
            True
        """

        return self.reference_class == self.predicted_class


CLASSES = ("Clear", "Review", "Insufficient", "Escalate")
DIFFICULTIES = ("Simple", "Moderate", "Complex")


def generate_project_frog_cases(seed: int = 7, n: int = 36) -> list[FrogCase]:
    """Generate a reproducible synthetic Project Frog evaluation slice.

    The generated sample uses a fixed class set and a difficulty-dependent error
    profile so tutorial examples remain stable across builds and tests.

    Assumptions:
        - ``n`` must be non-negative.
        - A fixed seed improves reproducibility but not statistical certainty.

    Example:
        >>> len(generate_project_frog_cases(seed=7, n=3))
        3
    """

    if n < 0:
        raise ValueError("n must be non-negative")

    rng = Random(seed)
    difficulty_counts = _allocate_counts(n, {"Simple": 0.50, "Moderate": 0.33, "Complex": 0.17})
    target_accuracy = {"Simple": 0.94, "Moderate": 0.83, "Complex": 0.67}
    rows: list[FrogCase] = []
    next_id = 1

    for difficulty in DIFFICULTIES:
        total = difficulty_counts[difficulty]
        correct_count = min(total, max(0, round(total * target_accuracy[difficulty])))
        for index in range(total):
            reference = CLASSES[index % len(CLASSES)]
            if index < correct_count:
                predicted = reference
            else:
                alternatives = [label for label in CLASSES if label != reference]
                predicted = alternatives[rng.randrange(len(alternatives))]
            rows.append(
                FrogCase(
                    case_id=f"frog-{next_id:03d}",
                    difficulty=difficulty,
                    reference_class=reference,
                    predicted_class=predicted,
                )
            )
            next_id += 1

    rng.shuffle(rows)
    return rows


def difficulty_summary(cases: Sequence[FrogCase]) -> dict[str, dict[str, float]]:
    """Summarize counts and accuracy by difficulty.

    Assumptions:
        - ``cases`` may be empty.
        - Accuracy is returned as ``0.0`` for empty groups.

    Example:
        >>> summary = difficulty_summary(generate_project_frog_cases(seed=7, n=6))
        >>> sorted(summary)
        ['Complex', 'Moderate', 'Simple']
    """

    counts: dict[str, list[FrogCase]] = {name: [] for name in DIFFICULTIES}
    for case in cases:
        counts.setdefault(case.difficulty, []).append(case)

    summary: dict[str, dict[str, float]] = {}
    for difficulty in DIFFICULTIES:
        group = counts.get(difficulty, [])
        total = len(group)
        correct = sum(case.prediction_correct for case in group)
        summary[difficulty] = {
            "cases": float(total),
            "accuracy": correct / total if total else 0.0,
        }
    return summary


def overall_accuracy(cases: Iterable[FrogCase]) -> float:
    """Return the observed accuracy for a synthetic evaluation slice.

    Assumptions:
        - ``cases`` must contain at least one row.

    Example:
        >>> rows = [FrogCase("frog-1", "Simple", "Clear", "Clear")]
        >>> overall_accuracy(rows)
        1.0
    """

    rows = list(cases)
    if not rows:
        raise ValueError("cases must not be empty")
    return sum(case.prediction_correct for case in rows) / len(rows)


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Compute a Wilson score interval for a binomial proportion.

    Assumptions:
        - ``0 <= successes <= total``.
        - ``total`` must be positive.
        - The interval is approximate and does not remove sampling bias.

    Example:
        >>> tuple(round(x, 3) for x in wilson_interval(31, 36))
        (0.711, 0.941)
    """

    if total <= 0:
        raise ValueError("total must be positive")
    if successes < 0 or successes > total:
        raise ValueError("successes must be between 0 and total")

    p = successes / total
    denominator = 1 + (z**2 / total)
    center = (p + (z**2 / (2 * total))) / denominator
    margin = (z / denominator) * sqrt((p * (1 - p) / total) + (z**2 / (4 * total**2)))
    return max(0.0, center - margin), min(1.0, center + margin)


def class_error_table(cases: Sequence[FrogCase]) -> dict[str, int]:
    """Count misclassifications by reference class.

    Assumptions:
        - Missing classes are reported as zero.

    Example:
        >>> rows = [FrogCase('frog-1', 'Simple', 'Clear', 'Review')]
        >>> class_error_table(rows)['Clear']
        1
    """

    counts = Counter(case.reference_class for case in cases if not case.prediction_correct)
    return {label: counts.get(label, 0) for label in CLASSES}


def release_recommendation(
    accuracy: float, interval: tuple[float, float], target: float = 0.90
) -> str:
    """Map an observed metric summary to a simple tutorial recommendation.

    Assumptions:
        - This helper is intentionally simple and for teaching only.
        - Real release decisions require richer cost, risk, and subgroup analysis.

    Example:
        >>> release_recommendation(0.93, (0.91, 0.96), target=0.90)
        'Evidence supports release'

    A caveated release requires the observed accuracy to meet the target while
    the lower bound still falls short. A high upper bound alone is not treated
    as positive release evidence.
    """

    lower, upper = interval
    if lower >= target:
        return "Evidence supports release"
    if accuracy >= target:
        return "Evidence supports release with caveats"
    if upper >= target or accuracy >= target - 0.05:
        return "Evidence is insufficient"
    return "Evidence indicates release risk"


def _allocate_counts(total: int, weights: dict[str, float]) -> dict[str, int]:
    raw = {label: total * weight for label, weight in weights.items()}
    base = {label: int(value) for label, value in raw.items()}
    remainder = total - sum(base.values())
    ranked = sorted(weights, key=lambda label: raw[label] - base[label], reverse=True)
    for label in ranked[:remainder]:
        base[label] += 1
    return base
