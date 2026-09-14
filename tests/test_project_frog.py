from applied_stats_ai import ProjectFrogScenario, generate_project_frog_evaluation


def test_generate_project_frog_evaluation_shape_and_label() -> None:
    dataset = generate_project_frog_evaluation(
        ProjectFrogScenario(sample_size=25, project_count=4),
        random_state=0,
    )
    assert len(dataset) == 25
    assert set(dataset["dataset_label"]) == {"synthetic_project_frog"}
    assert {"truth", "baseline_prediction", "comparison_prediction"}.issubset(dataset.columns)


def test_generate_project_frog_evaluation_is_reproducible() -> None:
    left = generate_project_frog_evaluation(ProjectFrogScenario(sample_size=10), random_state=42)
    right = generate_project_frog_evaluation(ProjectFrogScenario(sample_size=10), random_state=42)
    assert left.equals(right)
