"""Generate synthetic data and figures for the Trustworthy AI Evaluation site."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from trustworthy_ai_evaluation.confidence import calibration_curve_data
from trustworthy_ai_evaluation.sampling import (
    bootstrap_interval,
    compare_independent_proportions,
    exact_binomial_interval,
    wilson_interval,
)
from trustworthy_ai_evaluation.synthetic import PROJECT_FROG_SEED, generate_project_frog_data, summarize_component_performance

REPO_ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = REPO_ROOT / "docs" / "assets" / "figures"
DATA_DIR = REPO_ROOT / "data" / "synthetic"


def _save_figure(filename: str) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=200, bbox_inches="tight")
    plt.close()


def generate_dataset() -> pd.DataFrame:
    data = generate_project_frog_data(seed=PROJECT_FROG_SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data.to_csv(DATA_DIR / "project_frog_synthetic.csv", index=False)
    summarize_component_performance(data).to_csv(DATA_DIR / "project_frog_component_summary.csv", index=False)
    return data


def plot_metric_is_not_system(data: pd.DataFrame) -> None:
    summary = summarize_component_performance(data)
    end_to_end = 0.71
    plt.figure(figsize=(7.5, 4.2))
    plt.bar(summary["component_name"], summary["accuracy"], color="#6aaed6", label="Component accuracy")
    plt.axhline(end_to_end, color="#d1495b", linestyle="--", label="Synthetic end-to-end success")
    plt.ylim(0.5, 1.0)
    plt.ylabel("Observed rate")
    plt.title("High component scores do not guarantee high system success")
    plt.xticks(rotation=20, ha="right")
    plt.legend()
    _save_figure("metric_is_not_system.png")


def plot_shrinking_pond() -> None:
    baseline_successes, baseline_n = 1056, 1200
    later_successes, later_n = 63, 75
    points = [baseline_successes / baseline_n, later_successes / later_n]
    wilson_bounds = [wilson_interval(baseline_successes, baseline_n), wilson_interval(later_successes, later_n)]
    exact_bounds = [exact_binomial_interval(baseline_successes, baseline_n), exact_binomial_interval(later_successes, later_n)]
    plt.figure(figsize=(7.2, 4.2))
    x = np.arange(2)
    plt.errorbar(
        x - 0.05,
        points,
        yerr=np.array([[p - lo for p, (lo, hi) in zip(points, wilson_bounds)], [hi - p for p, (lo, hi) in zip(points, wilson_bounds)]]),
        fmt="o",
        capsize=4,
        label="Wilson 95% CI",
    )
    plt.errorbar(
        x + 0.05,
        points,
        yerr=np.array([[p - lo for p, (lo, hi) in zip(points, exact_bounds)], [hi - p for p, (lo, hi) in zip(points, exact_bounds)]]),
        fmt="s",
        capsize=4,
        label="Exact 95% CI",
    )
    plt.xticks(x, ["Baseline\n88% of 1,200", "Later\n84% of 75"])
    plt.ylim(0.7, 0.95)
    plt.ylabel("Observed accuracy")
    plt.title("Smaller samples widen uncertainty without proving regression")
    plt.legend()
    _save_figure("shrinking_pond_intervals.png")


def plot_accuracy_discontents(data: pd.DataFrame) -> None:
    classification = data[data["component_name"] == "Classification"]
    pivot = (
        classification.groupby(["difficulty", "reference_class"], observed=False)["prediction_correct"]
        .mean()
        .unstack(fill_value=0.0)
        .reindex(index=["Simple", "Moderate", "Complex"])
    )
    plt.figure(figsize=(7.0, 4.5))
    image = plt.imshow(pivot.values, cmap="Blues", vmin=0.45, vmax=1.0)
    plt.colorbar(image, label="Observed accuracy")
    plt.xticks(np.arange(len(pivot.columns)), pivot.columns, rotation=25, ha="right")
    plt.yticks(np.arange(len(pivot.index)), pivot.index)
    plt.title("Aggregate accuracy hides difficulty and class-specific variation")
    for row_idx in range(len(pivot.index)):
        for col_idx in range(len(pivot.columns)):
            plt.text(col_idx, row_idx, f"{pivot.iloc[row_idx, col_idx]:.2f}", ha="center", va="center")
    _save_figure("accuracy_discontents_heatmap.png")


def plot_confidence_meaning(data: pd.DataFrame) -> None:
    subset = data[data["component_name"].isin(["Classification", "Explanation generation"])]
    plt.figure(figsize=(7.0, 4.5))
    for component, style in [("Classification", "-"), ("Explanation generation", "--")]:
        component_rows = subset[subset["component_name"] == component]
        curve = calibration_curve_data(
            component_rows["prediction_correct"].astype(int),
            component_rows["raw_confidence"],
            n_bins=8,
            strategy="quantile",
        )
        plt.plot(curve["mean_prediction"], curve["observed_rate"], linestyle=style, marker="o", label=component)
    plt.plot([0, 1], [0, 1], color="black", linewidth=1, alpha=0.5, label="Perfect calibration")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel("Mean predicted confidence")
    plt.ylabel("Observed correctness")
    plt.title("Equal-looking scores can mean different things")
    plt.legend()
    _save_figure("confidence_meaning_calibration.png")


def plot_combining_confidence(data: pd.DataFrame) -> None:
    wide = (
        data.pivot_table(index="case_id", columns="component_name", values="calibrated_probability")
        .dropna()
        .reset_index(drop=True)
    )
    methods = pd.DataFrame(
        {
            "mean": wide.mean(axis=1),
            "minimum": wide.min(axis=1),
            "product": wide.prod(axis=1),
            "weighted_mean": 0.2 * wide["Document extraction"] + 0.4 * wide["Classification"] + 0.25 * wide["Evidence retrieval"] + 0.15 * wide["Explanation generation"],
        }
    )
    plt.figure(figsize=(7.2, 4.4))
    plt.boxplot([methods[column] for column in methods.columns], labels=[column.replace("_", " ") for column in methods.columns])
    plt.ylabel("Aggregate score")
    plt.title("Different composition rules create different scales and meanings")
    _save_figure("combining_confidence_scores.png")


def plot_start_with_decision() -> None:
    thresholds = np.linspace(0.5, 0.95, 10)
    release_utility = 100 * thresholds - 65
    caveat_utility = 20 + 50 * (1.0 - np.abs(thresholds - 0.8))
    collect_more_data = np.full_like(thresholds, 30.0)
    plt.figure(figsize=(7.2, 4.2))
    plt.plot(thresholds, release_utility, marker="o", label="Release now")
    plt.plot(thresholds, caveat_utility, marker="s", label="Release with caveats")
    plt.plot(thresholds, collect_more_data, marker="^", label="Collect more data")
    plt.xlabel("Required certainty threshold")
    plt.ylabel("Illustrative expected utility")
    plt.title("Decision design starts with consequences, not favorite metrics")
    plt.legend()
    _save_figure("start_with_the_decision_utility.png")


def plot_release_readiness() -> None:
    observed = 0.89
    lower, upper = 0.84, 0.93
    target = 0.90
    plt.figure(figsize=(6.8, 3.8))
    plt.errorbar([0], [observed], yerr=[[observed - lower], [upper - observed]], fmt="o", capsize=5)
    plt.axhline(target, color="#d1495b", linestyle="--", label="Nominal release target")
    plt.axhspan(0.90, 1.0, color="#98c379", alpha=0.15, label="Supports release")
    plt.axhspan(0.86, 0.90, color="#e5c07b", alpha=0.18, label="Supports release with caveats")
    plt.axhspan(0.0, 0.86, color="#e06c75", alpha=0.12, label="Insufficient or risk")
    plt.xlim(-0.75, 0.75)
    plt.ylim(0.78, 0.96)
    plt.xticks([0], ["Observed 89%\n95% CI 84% to 93%"])
    plt.ylabel("Accuracy")
    plt.title("Release evidence depends on uncertainty, not only the point estimate")
    plt.legend(loc="lower right")
    _save_figure("release_readiness_under_uncertainty.png")


def write_reading_path_summary() -> None:
    baseline = compare_independent_proportions(1056, 1200, 63, 75)
    later_bootstrap = bootstrap_interval([1] * 63 + [0] * 12, seed=PROJECT_FROG_SEED, n_resamples=1500)
    output = REPO_ROOT / "data" / "synthetic" / "reading_path_metrics.txt"
    output.write_text(
        "Synthetic metrics for chapter examples\n"
        f"Baseline vs later independent difference: {baseline['difference']:.4f} (95% approx CI {baseline['lower']:.4f}, {baseline['upper']:.4f})\n"
        f"Later bootstrap interval: ({later_bootstrap[0]:.4f}, {later_bootstrap[1]:.4f})\n",
        encoding="utf-8",
    )


def main() -> None:
    data = generate_dataset()
    plot_metric_is_not_system(data)
    plot_shrinking_pond()
    plot_accuracy_discontents(data)
    plot_confidence_meaning(data)
    plot_combining_confidence(data)
    plot_start_with_decision()
    plot_release_readiness()
    write_reading_path_summary()


if __name__ == "__main__":
    main()
