"""Synthetic Project Frog confidence experiment for Part IV of the book."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB

from .confidence import brier_score_summary, calibration_curve_data, expected_calibration_error, subgroup_metric_report

ROOT = Path(__file__).resolve().parents[2]
GENERATED_DIR = ROOT / "docs" / "assets" / "generated"
COMPONENTS = (
    "document_extraction",
    "classification",
    "evidence_retrieval",
    "explanation_generation",
)


@dataclass(frozen=True)
class ComponentSemantics:
    score_name: str
    producing_component: str
    intended_meaning: str
    mathematical_range: str
    generation_method: str
    claims_probability: bool
    calibration_method: str
    calibration_population: str
    dependency_assumptions: str
    known_failure_modes: str
    valid_comparisons: str
    invalid_interpretations: str
    supported_decisions: str
    unsupported_decisions: str


@dataclass(frozen=True)
class MethodResult:
    method: str
    output_meaning: str
    assumptions: str
    brier_score: float | None
    expected_calibration_error: float | None
    roc_auc: float | None
    decision_utility: float
    coverage: float | None
    selective_risk: float | None
    suitable_applications: str
    unsuitable_applications: str
    failure_mode: str


SEMANTICS_CARDS = {
    "document_extraction": ComponentSemantics(
        score_name="extraction quality index",
        producing_component="Document extraction",
        intended_meaning="Heuristic estimate that required fields were read cleanly enough to attempt downstream processing.",
        mathematical_range="0 to 1",
        generation_method="Rule-based blend of OCR completeness, field coverage, and parser stability checks.",
        claims_probability=False,
        calibration_method="Isotonic mapping to extraction success for descriptive analysis only.",
        calibration_population="Synthetic development split with milder difficulty mix than deployment.",
        dependency_assumptions="Downstream classifiers behave similarly when extraction succeeds at the same observed index.",
        known_failure_modes="High scores on template-like scans with systematic field swaps.",
        valid_comparisons="Compare only to the same score on the same extraction pipeline and population.",
        invalid_interpretations="Not the probability the final system answer is correct.",
        supported_decisions="Whether to request re-scan or proceed to classification.",
        unsupported_decisions="Whether the overall case is safe to auto-approve.",
    ),
    "classification": ComponentSemantics(
        score_name="class confidence",
        producing_component="Classification",
        intended_meaning="Model-reported confidence that the predicted case class is correct.",
        mathematical_range="0 to 1",
        generation_method="Softmax-like score from a multi-class classifier.",
        claims_probability=True,
        calibration_method="Isotonic regression fitted on the synthetic development split.",
        calibration_population="Synthetic development split; complex cases are under-represented.",
        dependency_assumptions="Prediction quality is conditionally stable given similar extraction quality and case difficulty.",
        known_failure_modes="Overconfidence on difficult or ambiguous cases.",
        valid_comparisons="Compare with later classifier outputs only after checking calibration drift.",
        invalid_interpretations="Not directly comparable to retrieval margin or explanation self-check scores.",
        supported_decisions="Whether to abstain or request reviewer confirmation of the predicted class.",
        unsupported_decisions="Whether the end-to-end Project Frog packet is trustworthy without more evidence.",
    ),
    "evidence_retrieval": ComponentSemantics(
        score_name="retrieval relevance margin",
        producing_component="Evidence retrieval",
        intended_meaning="Margin between the top retrieved evidence chunk and the next-best chunk.",
        mathematical_range="0 to 1",
        generation_method="Normalized ranking-margin statistic from the retrieval stack.",
        claims_probability=False,
        calibration_method="Isotonic mapping to evidence relevance for descriptive analysis only.",
        calibration_population="Synthetic development split built from the same fictional policy corpus.",
        dependency_assumptions="The margin is informative only for the same query formulation and corpus quality.",
        known_failure_modes="Looks confident when all candidate passages are consistently wrong.",
        valid_comparisons="Compare only across the same retrieval system and corpus snapshot.",
        invalid_interpretations="Not the probability the predicted class or explanation is correct.",
        supported_decisions="Whether to ask for broader retrieval or human evidence search.",
        unsupported_decisions="Whether to multiply directly with classifier confidence.",
    ),
    "explanation_generation": ComponentSemantics(
        score_name="explanation self-check score",
        producing_component="Explanation generation",
        intended_meaning="Internal consistency score saying the generated rationale matches the retrieved evidence and output template.",
        mathematical_range="0 to 1",
        generation_method="Self-consistency and rubric matching score from the explanation model.",
        claims_probability=False,
        calibration_method="Isotonic mapping to explanation adequacy for descriptive analysis only.",
        calibration_population="Synthetic development split with shorter explanations than the evaluation split.",
        dependency_assumptions="Template conformity is associated with adequate explanations.",
        known_failure_modes="High scores for polished but unsupported rationales.",
        valid_comparisons="Compare within the same explanation model and rubric version.",
        invalid_interpretations="Not a calibrated probability of end-to-end correctness.",
        supported_decisions="Whether to request a stronger explanation or route to human review.",
        unsupported_decisions="Whether to auto-release a case packet without checking evidence and class correctness.",
    ),
}


def _sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


def _logit(probabilities: np.ndarray) -> np.ndarray:
    clipped = np.clip(probabilities, 1e-6, 1 - 1e-6)
    return np.log(clipped / (1.0 - clipped))


def _clip(values: np.ndarray) -> np.ndarray:
    return np.clip(values, 0.0, 1.0)


def generate_project_frog_data(n_cases: int = 4000, random_state: int = 7) -> dict[str, np.ndarray]:
    """Generate a fully synthetic Project Frog dataset.

    The dataset is intentionally fictional. It is designed to teach that equal numeric
    scales do not imply equal meaning.
    """

    rng = np.random.default_rng(random_state)
    split = np.where(rng.random(n_cases) < 0.6, "development", "evaluation")

    difficulty = np.empty(n_cases, dtype=object)
    dev_diff = np.array([0.55, 0.30, 0.15])
    eval_diff = np.array([0.35, 0.35, 0.30])
    labels = np.array(["Simple", "Moderate", "Complex"], dtype=object)
    for current_split, probs in (("development", dev_diff), ("evaluation", eval_diff)):
        mask = split == current_split
        difficulty[mask] = rng.choice(labels, size=mask.sum(), p=probs)

    source_type = np.where(rng.random(n_cases) < 0.55, "native_pdf", "scan")
    cohort = np.where(rng.random(n_cases) < 0.5, "pond_a", "pond_b")
    case_id = np.arange(1, n_cases + 1)

    difficulty_level = np.select(
        [difficulty == "Simple", difficulty == "Moderate", difficulty == "Complex"],
        [0.0, 1.0, 2.0],
    )
    source_penalty = (source_type == "scan").astype(float)
    cohort_penalty = (cohort == "pond_b").astype(float)

    common_stress = rng.normal(size=n_cases)
    evidence_gap = rng.normal(size=n_cases)
    explanation_noise = rng.normal(size=n_cases)
    ambiguity = rng.normal(size=n_cases)

    p_extract = _sigmoid(2.2 - 0.9 * difficulty_level - 1.0 * source_penalty - 0.8 * common_stress)
    extract_ok = rng.binomial(1, p_extract).astype(int)

    p_class = _sigmoid(
        1.9 - 0.8 * difficulty_level - 0.7 * ambiguity - 0.7 * common_stress + 1.0 * (extract_ok - 0.5)
    )
    class_ok = rng.binomial(1, p_class).astype(int)

    p_retrieve = _sigmoid(
        1.8 - 0.9 * difficulty_level - 0.8 * evidence_gap - 0.6 * common_stress + 0.9 * (class_ok - 0.5)
    )
    retrieve_ok = rng.binomial(1, p_retrieve).astype(int)

    p_explain = _sigmoid(
        1.7 - 0.7 * difficulty_level - 0.7 * explanation_noise - 0.7 * common_stress + 0.8 * (retrieve_ok - 0.5)
    )
    explain_ok = rng.binomial(1, p_explain).astype(int)

    extraction_score = _clip(_sigmoid(0.9 + 0.7 * _logit(p_extract) + 0.35 * rng.normal(size=n_cases)))
    classification_score = _clip(_sigmoid(0.25 + 1.35 * _logit(p_class) + 0.30 * rng.normal(size=n_cases)))
    retrieval_score = _clip(_sigmoid(-0.35 + 0.75 * _logit(p_retrieve) + 0.25 * rng.normal(size=n_cases)))
    explanation_score = _clip(
        _sigmoid(1.1 + 0.35 * explain_ok - 0.25 * difficulty_level + 0.55 * cohort_penalty + 0.35 * rng.normal(size=n_cases))
    )

    end_to_end_ok = (extract_ok & class_ok & retrieve_ok & explain_ok).astype(int)

    return {
        "case_id": case_id,
        "split": split,
        "difficulty": difficulty,
        "source_type": source_type,
        "cohort": cohort,
        "extract_ok": extract_ok,
        "class_ok": class_ok,
        "retrieve_ok": retrieve_ok,
        "explain_ok": explain_ok,
        "end_to_end_ok": end_to_end_ok,
        "extraction_score": extraction_score,
        "classification_score": classification_score,
        "retrieval_score": retrieval_score,
        "explanation_score": explanation_score,
    }


def _fit_isotonic(raw_scores: np.ndarray, labels: np.ndarray) -> IsotonicRegression:
    model = IsotonicRegression(y_min=0.0, y_max=1.0, out_of_bounds="clip")
    model.fit(raw_scores, labels)
    return model


def _prepare_component_probabilities(data: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    dev = data["split"] == "development"
    calibrators = {
        "extract": _fit_isotonic(data["extraction_score"][dev], data["extract_ok"][dev]),
        "class": _fit_isotonic(data["classification_score"][dev], data["class_ok"][dev]),
        "retrieve": _fit_isotonic(data["retrieval_score"][dev], data["retrieve_ok"][dev]),
        "explain": _fit_isotonic(data["explanation_score"][dev], data["explain_ok"][dev]),
    }
    return {
        "extract": calibrators["extract"].predict(data["extraction_score"]),
        "class": calibrators["class"].predict(data["classification_score"]),
        "retrieve": calibrators["retrieve"].predict(data["retrieval_score"]),
        "explain": calibrators["explain"].predict(data["explanation_score"]),
    }


def _fit_meta_models(data: dict[str, np.ndarray], probs: dict[str, np.ndarray]) -> tuple[LogisticRegression, GaussianNB]:
    X = _feature_matrix(data, probs)
    dev = data["split"] == "development"
    y = data["end_to_end_ok"]
    meta_model = LogisticRegression(max_iter=2000, solver="liblinear")
    meta_model.fit(X[dev], y[dev])
    bayes_model = GaussianNB()
    bayes_model.fit(X[dev], y[dev])
    return meta_model, bayes_model


def _feature_matrix(data: dict[str, np.ndarray], probs: dict[str, np.ndarray]) -> np.ndarray:
    difficulty_numeric = np.select(
        [data["difficulty"] == "Simple", data["difficulty"] == "Moderate", data["difficulty"] == "Complex"],
        [0.0, 1.0, 2.0],
    )
    return np.column_stack([probs["extract"], probs["class"], probs["retrieve"], probs["explain"], difficulty_numeric])


def _decision_utility(predictions: np.ndarray, truth: np.ndarray, *, abstain_value: int = -2) -> float:
    utility = np.zeros_like(truth, dtype=float)
    utility[predictions == 1] = np.where(truth[predictions == 1] == 1, 5.0, -20.0)
    utility[predictions == -1] = abstain_value
    return float(utility.mean())


def _coverage_and_risk(decisions: np.ndarray, truth: np.ndarray) -> tuple[float, float | None]:
    automatic = decisions != -1
    coverage = float(automatic.mean())
    if automatic.sum() == 0:
        return coverage, None
    risk = float(1.0 - truth[automatic].mean())
    return coverage, risk


def _summarize_scalar_method(
    name: str,
    scores: np.ndarray,
    truth: np.ndarray,
    *,
    output_meaning: str,
    assumptions: str,
    suitable_applications: str,
    unsuitable_applications: str,
    failure_mode: str,
) -> MethodResult:
    predictions = (scores >= 0.75).astype(int)
    return MethodResult(
        method=name,
        output_meaning=output_meaning,
        assumptions=assumptions,
        brier_score=float(brier_score_summary(truth, scores).brier_score),
        expected_calibration_error=float(expected_calibration_error(truth, scores)),
        roc_auc=float(roc_auc_score(truth, scores)),
        decision_utility=_decision_utility(predictions, truth),
        coverage=1.0,
        selective_risk=float(1.0 - truth.mean()),
        suitable_applications=suitable_applications,
        unsuitable_applications=unsuitable_applications,
        failure_mode=failure_mode,
    )


def run_experiment(random_state: int = 7) -> dict[str, object]:
    """Run the synthetic Part IV experiment and return summary objects."""

    data = generate_project_frog_data(random_state=random_state)
    probs = _prepare_component_probabilities(data)
    meta_model, bayes_model = _fit_meta_models(data, probs)

    X = _feature_matrix(data, probs)

    anti_pattern_average = np.mean(
        np.column_stack(
            [
                data["extraction_score"],
                data["classification_score"],
                data["retrieval_score"],
                data["explanation_score"],
            ]
        ),
        axis=1,
    )
    min_prob = np.min(np.column_stack(list(probs.values())), axis=1)
    max_prob = np.max(np.column_stack(list(probs.values())), axis=1)
    mean_prob = np.mean(np.column_stack(list(probs.values())), axis=1)
    weighted_mean = np.average(np.column_stack(list(probs.values())), axis=1, weights=[0.15, 0.4, 0.25, 0.2])
    geometric_mean = np.prod(np.column_stack(list(probs.values())), axis=1) ** 0.25
    product_prob = np.prod(np.column_stack(list(probs.values())), axis=1)
    meta_prob = meta_model.predict_proba(X)[:, 1]
    bayes_prob = bayes_model.predict_proba(X)[:, 1]

    truth = data["end_to_end_ok"]
    evaluation = data["split"] == "evaluation"

    scalar_methods = [
        _summarize_scalar_method(
            "anti_pattern_average_raw",
            anti_pattern_average[evaluation],
            truth[evaluation],
            output_meaning="Unvalidated average of four semantically different raw scores.",
            assumptions="Pretends the four scores share a common meaning and scale.",
            suitable_applications="None for consequential trust estimation; only as a didactic anti-pattern.",
            unsuitable_applications="Any operational release or automation decision.",
            failure_mode="Looks numerically plausible while hiding component incompatibility and dependence.",
        ),
        _summarize_scalar_method(
            "minimum_calibrated_probability",
            min_prob[evaluation],
            truth[evaluation],
            output_meaning="Weakest calibrated component probability.",
            assumptions="The weakest component should dominate the decision threshold.",
            suitable_applications="Conservative gating and safety-focused review triggers.",
            unsuitable_applications="Estimating end-to-end probability of success.",
            failure_mode="Over-penalizes cases with one noisy but non-critical component.",
        ),
        _summarize_scalar_method(
            "maximum_calibrated_probability",
            max_prob[evaluation],
            truth[evaluation],
            output_meaning="Strongest calibrated component probability.",
            assumptions="One strong signal can dominate the decision.",
            suitable_applications="Finding cases for deeper review where at least one component is promising.",
            unsuitable_applications="Automation confidence or release decisions.",
            failure_mode="Masks weak upstream components.",
        ),
        _summarize_scalar_method(
            "arithmetic_mean_calibrated_probability",
            mean_prob[evaluation],
            truth[evaluation],
            output_meaning="Simple average of calibrated component event probabilities.",
            assumptions="Averaged component probabilities summarize the desired system event.",
            suitable_applications="Coarse monitoring after empirical validation.",
            unsuitable_applications="General trust estimation without end-to-end labels.",
            failure_mode="Still ignores dependence and event mismatch.",
        ),
        _summarize_scalar_method(
            "weighted_mean_calibrated_probability",
            weighted_mean[evaluation],
            truth[evaluation],
            output_meaning="Weighted average of calibrated component event probabilities.",
            assumptions="Weights reflect component importance and remain stable.",
            suitable_applications="Policy scorecards with fixed, reviewed semantics.",
            unsuitable_applications="Transportable probability estimates across datasets.",
            failure_mode="The output meaning changes with arbitrary weight choices.",
        ),
        _summarize_scalar_method(
            "geometric_mean_calibrated_probability",
            geometric_mean[evaluation],
            truth[evaluation],
            output_meaning="Multiplicative-style average that penalizes low components.",
            assumptions="Scores share probabilistic semantics and partial independence.",
            suitable_applications="Soft conservative ranking after validation.",
            unsuitable_applications="Any setting where components target different events.",
            failure_mode="Collapses for dependent low-probability components.",
        ),
        _summarize_scalar_method(
            "product_of_calibrated_probabilities",
            product_prob[evaluation],
            truth[evaluation],
            output_meaning="Naive product of component event probabilities.",
            assumptions="Marginal probabilities can be multiplied as if independent and aligned.",
            suitable_applications="Rare narrow cases where chain assumptions are justified.",
            unsuitable_applications="This Project Frog pipeline, which has correlated failures.",
            failure_mode="Severe underestimation under dependence.",
        ),
        _summarize_scalar_method(
            "calibrated_meta_model",
            meta_prob[evaluation],
            truth[evaluation],
            output_meaning="Learned estimate of end-to-end correctness from the full score vector.",
            assumptions="Development labels and deployment conditions are relevant to the target setting.",
            suitable_applications="End-to-end probability estimation when training data and monitoring exist.",
            unsuitable_applications="Zero-label settings or settings with large distribution shift.",
            failure_mode="Can drift when score semantics or populations change.",
        ),
        _summarize_scalar_method(
            "bayesian_composition",
            bayes_prob[evaluation],
            truth[evaluation],
            output_meaning="Naive-Bayes estimate of end-to-end correctness from the component vector.",
            assumptions="Conditional independence and approximate Gaussian feature behavior given the outcome.",
            suitable_applications="Fast baseline when those assumptions are defensible enough to test.",
            unsuitable_applications="Claims of universal trust aggregation.",
            failure_mode="Breaks when conditional dependence dominates.",
        ),
    ]

    rule_accept = np.where(
        (probs["extract"] >= 0.75)
        & (probs["class"] >= 0.80)
        & (probs["retrieve"] >= 0.70)
        & (probs["explain"] >= 0.60),
        1,
        -1,
    )
    meta_review = np.where(
        (meta_prob >= 0.80) & (np.min(np.column_stack(list(probs.values())), axis=1) >= 0.55),
        1,
        -1,
    )
    risk_category = np.where(
        meta_prob >= 0.80,
        "low_risk",
        np.where(meta_prob >= 0.55, "medium_risk", "high_risk"),
    )

    policy_results = [
        MethodResult(
            method="rule_based_policy",
            output_meaning="Accept automatically only when all component-specific thresholds are met; otherwise abstain.",
            assumptions="Thresholds reflect review policy rather than probability theory.",
            brier_score=None,
            expected_calibration_error=None,
            roc_auc=None,
            decision_utility=_decision_utility(rule_accept[evaluation], truth[evaluation]),
            coverage=_coverage_and_risk(rule_accept[evaluation], truth[evaluation])[0],
            selective_risk=_coverage_and_risk(rule_accept[evaluation], truth[evaluation])[1],
            suitable_applications="Governed review workflows with explicit abstention.",
            unsuitable_applications="Reporting a single numeric trust probability.",
            failure_mode="Can be brittle around manually chosen thresholds.",
        ),
        MethodResult(
            method="retain_score_vector",
            output_meaning="Keep the four scores separate and review them jointly.",
            assumptions="Humans or downstream policies can use structured evidence better than a single scalar.",
            brier_score=None,
            expected_calibration_error=None,
            roc_auc=None,
            decision_utility=_decision_utility(np.full(evaluation.sum(), -1), truth[evaluation], abstain_value=-1),
            coverage=0.0,
            selective_risk=None,
            suitable_applications="High-stakes review, auditing, debugging, and failure analysis.",
            unsuitable_applications="Fully automated ranking that requires one scalar score.",
            failure_mode="Needs governance and can slow down throughput.",
        ),
        MethodResult(
            method="risk_category",
            output_meaning="Convert the score vector into low/medium/high system risk bands.",
            assumptions="The category boundaries are decision artifacts, not latent truths.",
            brier_score=None,
            expected_calibration_error=None,
            roc_auc=None,
            decision_utility=float(np.mean(np.where(risk_category[evaluation] == "low_risk", np.where(truth[evaluation] == 1, 4.0, -18.0), -2.0))),
            coverage=float(np.mean(risk_category[evaluation] == "low_risk")),
            selective_risk=float(1.0 - truth[evaluation][risk_category[evaluation] == "low_risk"].mean()) if np.any(risk_category[evaluation] == "low_risk") else None,
            suitable_applications="Triage and operational dashboards.",
            unsuitable_applications="Fine-grained probability statements.",
            failure_mode="Hides uncertainty inside coarse categories.",
        ),
        MethodResult(
            method="abstention_and_human_review",
            output_meaning="Accept only high-confidence cases under a learned end-to-end model and abstain on the rest.",
            assumptions="Human review is available and better than unsafe automation.",
            brier_score=None,
            expected_calibration_error=None,
            roc_auc=None,
            decision_utility=_decision_utility(meta_review[evaluation], truth[evaluation]),
            coverage=_coverage_and_risk(meta_review[evaluation], truth[evaluation])[0],
            selective_risk=_coverage_and_risk(meta_review[evaluation], truth[evaluation])[1],
            suitable_applications="Selective prediction and escalation workflows.",
            unsuitable_applications="Contexts that forbid abstention.",
            failure_mode="Coverage can collapse on hard subgroups.",
        ),
    ]

    subgroup_rows = subgroup_metric_report(
        data["difficulty"][evaluation], truth[evaluation], meta_prob[evaluation], n_bins=5
    )

    calibration_report = {
        "classification_raw": {
            "ece": expected_calibration_error(data["class_ok"][evaluation], data["classification_score"][evaluation], n_bins=10),
            "brier": asdict(brier_score_summary(data["class_ok"][evaluation], data["classification_score"][evaluation], n_bins=10)),
        },
        "classification_calibrated": {
            "ece": expected_calibration_error(data["class_ok"][evaluation], probs["class"][evaluation], n_bins=10),
            "brier": asdict(brier_score_summary(data["class_ok"][evaluation], probs["class"][evaluation], n_bins=10)),
        },
    }

    failure_mask = (anti_pattern_average[evaluation] >= 0.80) & (truth[evaluation] == 0)
    failure_rows = []
    eval_indices = np.where(evaluation)[0]
    for index in eval_indices[failure_mask][:10]:
        failure_rows.append(
            {
                "case_id": int(data["case_id"][index]),
                "difficulty": str(data["difficulty"][index]),
                "source_type": str(data["source_type"][index]),
                "anti_pattern_average_raw": float(anti_pattern_average[index]),
                "meta_model_probability": float(meta_prob[index]),
                "system_correct": int(truth[index]),
                "raw_scores": {
                    "document_extraction": float(data["extraction_score"][index]),
                    "classification": float(data["classification_score"][index]),
                    "evidence_retrieval": float(data["retrieval_score"][index]),
                    "explanation_generation": float(data["explanation_score"][index]),
                },
            }
        )

    return {
        "data": data,
        "component_probabilities": probs,
        "score_arrays": {
            "anti_pattern_average_raw": anti_pattern_average,
            "minimum_calibrated_probability": min_prob,
            "maximum_calibrated_probability": max_prob,
            "arithmetic_mean_calibrated_probability": mean_prob,
            "weighted_mean_calibrated_probability": weighted_mean,
            "geometric_mean_calibrated_probability": geometric_mean,
            "product_of_calibrated_probabilities": product_prob,
            "calibrated_meta_model": meta_prob,
            "bayesian_composition": bayes_prob,
            "rule_based_policy": rule_accept,
            "abstention_and_human_review": meta_review,
            "risk_category": risk_category,
        },
        "scalar_method_results": [asdict(item) for item in scalar_methods],
        "policy_results": [asdict(item) for item in policy_results],
        "subgroup_rows": [asdict(item) for item in subgroup_rows],
        "calibration_report": calibration_report,
        "failure_rows": failure_rows,
    }


def write_artifacts(random_state: int = 7) -> dict[str, object]:
    """Generate CSV, JSON, and figure artifacts for the synthetic Part IV chapters."""

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    results = run_experiment(random_state=random_state)
    data = results["data"]
    probs = results["component_probabilities"]
    score_arrays = results["score_arrays"]
    evaluation = data["split"] == "evaluation"

    csv_path = GENERATED_DIR / "project_frog_confidence_dataset.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "case_id",
                "split",
                "difficulty",
                "source_type",
                "cohort",
                "document_extraction_score",
                "classification_score",
                "evidence_retrieval_score",
                "explanation_generation_score",
                "document_extraction_probability",
                "classification_probability",
                "evidence_retrieval_probability",
                "explanation_generation_probability",
                "end_to_end_correct",
            ]
        )
        for row in range(len(data["case_id"])):
            writer.writerow(
                [
                    int(data["case_id"][row]),
                    data["split"][row],
                    data["difficulty"][row],
                    data["source_type"][row],
                    data["cohort"][row],
                    round(float(data["extraction_score"][row]), 6),
                    round(float(data["classification_score"][row]), 6),
                    round(float(data["retrieval_score"][row]), 6),
                    round(float(data["explanation_score"][row]), 6),
                    round(float(probs["extract"][row]), 6),
                    round(float(probs["class"][row]), 6),
                    round(float(probs["retrieve"][row]), 6),
                    round(float(probs["explain"][row]), 6),
                    int(data["end_to_end_ok"][row]),
                ]
            )

    with (GENERATED_DIR / "project_frog_method_results.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "scalar_method_results": results["scalar_method_results"],
                "policy_results": results["policy_results"],
                "subgroup_rows": results["subgroup_rows"],
                "calibration_report": results["calibration_report"],
                "failure_rows": results["failure_rows"],
                "semantics_cards": {name: asdict(card) for name, card in SEMANTICS_CARDS.items()},
                "seed": random_state,
                "synthetic_notice": "All values in this file are fully synthetic and generated for teaching only.",
            },
            handle,
            indent=2,
        )

    fig, ax = plt.subplots(figsize=(6, 4.5))
    raw_bins = calibration_curve_data(data["class_ok"][evaluation], data["classification_score"][evaluation], n_bins=10)
    calibrated_bins = calibration_curve_data(data["class_ok"][evaluation], probs["class"][evaluation], n_bins=10)
    ax.plot([0, 1], [0, 1], linestyle="--", color="black", label="perfect calibration")
    ax.plot([item.mean_score for item in raw_bins], [item.observed_frequency for item in raw_bins], marker="o", label="raw classifier score")
    ax.plot([item.mean_score for item in calibrated_bins], [item.observed_frequency for item in calibrated_bins], marker="s", label="calibrated classifier probability")
    ax.set_xlabel("Mean predicted score")
    ax.set_ylabel("Observed frequency")
    ax.set_title("Synthetic reliability diagram: classification")
    ax.legend()
    fig.tight_layout()
    fig.savefig(GENERATED_DIR / "classification_reliability.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    scalar_results = results["scalar_method_results"]
    labels = [item["method"].replace("_", "\n") for item in scalar_results]
    briers = [item["brier_score"] for item in scalar_results]
    eces = [item["expected_calibration_error"] for item in scalar_results]
    x = np.arange(len(labels))
    width = 0.38
    ax.bar(x - width / 2, briers, width=width, label="Brier score")
    ax.bar(x + width / 2, eces, width=width, label="ECE")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_title("Synthetic composition comparison on evaluation data")
    ax.legend()
    fig.tight_layout()
    fig.savefig(GENERATED_DIR / "composition_metrics.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    anti = score_arrays["anti_pattern_average_raw"][evaluation]
    truth = data["end_to_end_ok"][evaluation]
    bins = calibration_curve_data(truth, anti, n_bins=8)
    ax.plot([0, 1], [0, 1], linestyle="--", color="black", label="if average were a probability")
    ax.plot([item.mean_score for item in bins], [item.observed_frequency for item in bins], marker="o", color="tab:red", label="anti-pattern average")
    ax.set_xlabel("Average raw score")
    ax.set_ylabel("Observed end-to-end correctness")
    ax.set_title("Why the average raw score is misleading")
    ax.legend()
    fig.tight_layout()
    fig.savefig(GENERATED_DIR / "average_score_misleading.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    thresholds = np.linspace(0.50, 0.95, 10)
    coverages = []
    risks = []
    score = score_arrays["calibrated_meta_model"][evaluation]
    eval_truth = data["end_to_end_ok"][evaluation]
    for threshold in thresholds:
        decisions = np.where(score >= threshold, 1, -1)
        coverage, risk = _coverage_and_risk(decisions, eval_truth)
        coverages.append(coverage)
        risks.append(np.nan if risk is None else risk)
    ax.plot(coverages, risks, marker="o")
    ax.set_xlabel("Coverage")
    ax.set_ylabel("Selective risk")
    ax.set_title("Coverage-risk trade-off with abstention")
    fig.tight_layout()
    fig.savefig(GENERATED_DIR / "coverage_risk_tradeoff.png", dpi=160)
    plt.close(fig)

    return results


if __name__ == "__main__":
    write_artifacts()
