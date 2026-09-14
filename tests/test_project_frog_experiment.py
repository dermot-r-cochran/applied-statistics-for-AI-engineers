from pathlib import Path

from trustworthy_ai_evaluation.project_frog_experiment import (
    GENERATED_DIR,
    generate_project_frog_data,
    run_experiment,
    write_artifacts,
)


def test_generate_project_frog_data_is_reproducible_for_fixed_seed():
    first = generate_project_frog_data(n_cases=50, random_state=7)
    second = generate_project_frog_data(n_cases=50, random_state=7)
    assert first["difficulty"].tolist() == second["difficulty"].tolist()
    assert first["classification_score"].tolist() == second["classification_score"].tolist()


def test_run_experiment_contains_required_methods_and_groups():
    results = run_experiment(random_state=7)
    method_names = {row["method"] for row in results["scalar_method_results"]}
    policy_names = {row["method"] for row in results["policy_results"]}
    groups = {row["group"] for row in results["subgroup_rows"]}
    assert "anti_pattern_average_raw" in method_names
    assert "calibrated_meta_model" in method_names
    assert "bayesian_composition" in method_names
    assert "abstention_and_human_review" in policy_names
    assert groups == {"Simple", "Moderate", "Complex"}


def test_meta_model_outperforms_anti_pattern_on_brier_score():
    results = run_experiment(random_state=7)
    by_name = {row["method"]: row for row in results["scalar_method_results"]}
    assert by_name["calibrated_meta_model"]["brier_score"] < by_name["anti_pattern_average_raw"]["brier_score"]


def test_write_artifacts_creates_expected_files():
    write_artifacts(random_state=7)
    expected = {
        "project_frog_confidence_dataset.csv",
        "project_frog_method_results.json",
        "classification_reliability.png",
        "composition_metrics.png",
        "average_score_misleading.png",
        "coverage_risk_tradeoff.png",
    }
    created = {path.name for path in Path(GENERATED_DIR).glob("*")}
    assert expected.issubset(created)
