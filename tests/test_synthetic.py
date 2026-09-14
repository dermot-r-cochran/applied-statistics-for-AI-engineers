import pandas as pd
import pytest

from trustworthy_ai_evaluation.synthetic import PROJECT_FROG_SEED, generate_project_frog_data, summarize_component_performance


def test_project_frog_generation_is_reproducible() -> None:
    first = generate_project_frog_data(seed=PROJECT_FROG_SEED)
    second = generate_project_frog_data(seed=PROJECT_FROG_SEED)
    pd.testing.assert_frame_equal(first, second)


def test_project_frog_schema_and_components() -> None:
    frame = generate_project_frog_data(n_cases=12, seed=10)
    assert list(frame.columns) == [
        "project_id",
        "document_id",
        "case_id",
        "difficulty",
        "predicted_class",
        "reference_class",
        "prediction_correct",
        "component_name",
        "raw_confidence",
        "calibrated_probability",
        "evidence_relevance",
        "processing_latency",
        "processing_cost",
    ]
    assert set(frame["difficulty"]) <= {"Simple", "Moderate", "Complex"}
    assert set(frame["predicted_class"]) <= {"Clear", "Review", "Insufficient", "Escalate"}
    assert frame["component_name"].nunique() == 4


def test_generate_project_frog_rejects_non_positive_n_cases() -> None:
    with pytest.raises(ValueError):
        generate_project_frog_data(n_cases=0)


def test_component_summary_requires_columns() -> None:
    with pytest.raises(KeyError):
        summarize_component_performance(pd.DataFrame({"prediction_correct": [True, False]}))
