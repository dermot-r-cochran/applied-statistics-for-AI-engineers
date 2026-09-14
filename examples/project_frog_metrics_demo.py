from __future__ import annotations

from pathlib import Path

import pandas as pd

from applied_stats_ai import compare_two_models, confidence_interval_accuracy

DATA_PATH = Path(__file__).resolve().with_name("project_frog_accuracy_samples.csv")


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    successes = int(data["correct_v2_4"].sum())
    interval = confidence_interval_accuracy(successes, len(data))
    comparison = compare_two_models(data["truth"], data["pred_v2_4"], data["pred_v2_5"])

    print("Project Frog v2.4 accuracy interval:", interval)
    print("Release comparison summary:")
    for key, value in comparison.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
