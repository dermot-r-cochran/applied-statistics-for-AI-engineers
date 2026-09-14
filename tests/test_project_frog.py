import pytest

from applied_stats_ai import ProjectFrogScenario, generate_project_frog_evaluation


def test_generate_project_frog_evaluation_shape_and_label() -> None:
    dataset = generate_project_frog_evaluation(
        ProjectFrogScenario(sample_size=25, project_count=4),
        random_state=0,
    )
    assert len(dataset) == 25
    assert set(dataset["dataset_label"]) == {"synthetic_project_frog"}
    assert {"truth", "baseline_prediction", "comparison_prediction"}.issubset(dataset.columns)
    assert dataset["project_id"].nunique() == 4
    assert (dataset["latency_ms"] >= 0).all()


def test_generate_project_frog_evaluation_is_reproducible() -> None:
    scenario = ProjectFrogScenario(sample_size=10, project_count=10)
    left = generate_project_frog_evaluation(scenario, random_state=42)
    right = generate_project_frog_evaluation(scenario, random_state=42)
    assert left.equals(right)


@pytest.mark.parametrize(
    "scenario",
    [
        ProjectFrogScenario(sample_size=0),
        ProjectFrogScenario(sample_size=4, project_count=5),
        ProjectFrogScenario(baseline_accuracy=0.0),
        ProjectFrogScenario(comparison_accuracy=1.0),
    ],
)
def test_generate_project_frog_evaluation_validates_inputs(
    scenario: ProjectFrogScenario,
) -> None:
    with pytest.raises(ValueError):
        generate_project_frog_evaluation(scenario)
