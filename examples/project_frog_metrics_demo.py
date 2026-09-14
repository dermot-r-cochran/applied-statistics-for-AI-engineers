from __future__ import annotations

from applied_stats_ai import (
    ProjectFrogScenario,
    compare_two_models,
    confidence_interval_accuracy,
    generate_project_frog_evaluation,
)


def main() -> None:
    dataset = generate_project_frog_evaluation(
        ProjectFrogScenario(sample_size=250, baseline_accuracy=0.84, comparison_accuracy=0.87),
        random_state=7,
    )
    successes = int(dataset["baseline_correct"].sum())
    interval = confidence_interval_accuracy(successes, len(dataset))
    comparison = compare_two_models(
        dataset["truth"],
        dataset["baseline_prediction"],
        dataset["comparison_prediction"],
    )

    print("Synthetic Project Frog dataset label:", dataset["dataset_label"].iat[0])
    print("Baseline release accuracy interval:", interval)
    print("Release comparison summary:")
    for key, value in comparison.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
