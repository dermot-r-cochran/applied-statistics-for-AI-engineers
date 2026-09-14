import math
import unittest

from trustworthy_ai_evaluation import (
    bootstrap_metric,
    cluster_bootstrap_metric,
    compare_independent_proportions,
    compare_paired_predictions,
    metric_comparability_check,
    minimum_detectable_effect,
    required_sample_size,
)


class BootstrapMetricTests(unittest.TestCase):
    def test_bootstrap_reproducible_with_seed(self):
        first = bootstrap_metric([1, 0, 1, 1, 0], seed=13, n_resamples=500)
        second = bootstrap_metric([1, 0, 1, 1, 0], seed=13, n_resamples=500)
        self.assertEqual(first.confidence_interval, second.confidence_interval)
        self.assertAlmostEqual(first.standard_error, second.standard_error)

    def test_bootstrap_handles_all_correct(self):
        result = bootstrap_metric([1, 1, 1, 1], seed=1, n_resamples=200)
        self.assertEqual(result.estimate, 1.0)
        self.assertEqual(result.confidence_interval, (1.0, 1.0))

    def test_bootstrap_handles_all_incorrect(self):
        result = bootstrap_metric([0, 0, 0], seed=1, n_resamples=200)
        self.assertEqual(result.estimate, 0.0)
        self.assertEqual(result.confidence_interval, (0.0, 0.0))

    def test_bootstrap_handles_very_small_sample(self):
        result = bootstrap_metric([1], seed=2, n_resamples=20)
        self.assertEqual(result.estimate, 1.0)
        self.assertEqual(result.confidence_interval, (1.0, 1.0))

    def test_bootstrap_missing_values_raise_by_default(self):
        with self.assertRaises(ValueError):
            bootstrap_metric([1, None, 0], seed=1)

    def test_bootstrap_missing_values_can_be_dropped(self):
        result = bootstrap_metric([1, None, 0], seed=1, drop_missing=True, n_resamples=100)
        self.assertAlmostEqual(result.estimate, 0.5)

    def test_bootstrap_accepts_custom_metric(self):
        result = bootstrap_metric([1, 0, 1], metric=sum, seed=1, n_resamples=100)
        self.assertEqual(result.estimate, 2.0)


class ClusterBootstrapMetricTests(unittest.TestCase):
    def test_cluster_bootstrap_reproducible_with_seed(self):
        values = [1, 1, 0, 0, 1, 1]
        clusters = ["a", "a", "b", "b", "c", "c"]
        first = cluster_bootstrap_metric(values, clusters, seed=9, n_resamples=300)
        second = cluster_bootstrap_metric(values, clusters, seed=9, n_resamples=300)
        self.assertEqual(first.confidence_interval, second.confidence_interval)

    def test_cluster_bootstrap_supports_clustered_inputs(self):
        values = [1, 1, 0, 0, 1, 1]
        clusters = ["a", "a", "b", "b", "c", "c"]
        result = cluster_bootstrap_metric(values, clusters, seed=9, n_resamples=300)
        self.assertAlmostEqual(result.estimate, 4 / 6)

    def test_cluster_bootstrap_uses_cluster_level_weighting(self):
        values = [1, 1, 1, 0]
        clusters = ["a", "a", "a", "b"]
        result = cluster_bootstrap_metric(values, clusters, seed=9, n_resamples=300)
        self.assertAlmostEqual(result.estimate, 0.5)

    def test_cluster_bootstrap_rejects_empty_clustered_sample(self):
        with self.assertRaises(ValueError):
            cluster_bootstrap_metric([], [], seed=1)

    def test_cluster_bootstrap_rejects_missing_clusters(self):
        with self.assertRaises(ValueError):
            cluster_bootstrap_metric([1, 0], ["a", None], seed=1)

    def test_cluster_bootstrap_can_drop_missing(self):
        result = cluster_bootstrap_metric([1, None, 0], ["a", "b", "c"], seed=1, drop_missing=True, n_resamples=50)
        self.assertAlmostEqual(result.estimate, 0.5)

    def test_cluster_bootstrap_accepts_custom_metric(self):
        result = cluster_bootstrap_metric([1, 1, 0], ["a", "a", "b"], metric=max, seed=1, n_resamples=50)
        self.assertAlmostEqual(result.estimate, 0.5)


class PairedComparisonTests(unittest.TestCase):
    def test_paired_predictions_reject_unequal_lengths(self):
        with self.assertRaises(ValueError):
            compare_paired_predictions([1, 0], [1], [1], seed=1)

    def test_paired_predictions_support_single_class_sample(self):
        result = compare_paired_predictions(
            ["Clear", "Clear", "Clear"],
            ["Clear", "Review", "Clear"],
            ["Clear", "Clear", "Review"],
            seed=1,
            n_resamples=200,
            n_permutations=200,
        )
        self.assertEqual(result.n_pairs, 3)
        self.assertTrue(-1.0 <= result.difference <= 1.0)

    def test_paired_predictions_missing_values(self):
        with self.assertRaises(ValueError):
            compare_paired_predictions([1, None], [1, 0], [1, 0], seed=1)
        result = compare_paired_predictions([1, None], [1, 0], [1, 0], seed=1, drop_missing=True, n_resamples=50, n_permutations=50)
        self.assertEqual(result.n_pairs, 1)


class IndependentProportionTests(unittest.TestCase):
    def test_independent_proportion_known_difference(self):
        result = compare_independent_proportions(45, 50, 40, 50)
        self.assertAlmostEqual(result.proportion_a, 0.9)
        self.assertAlmostEqual(result.proportion_b, 0.8)
        self.assertAlmostEqual(result.difference, 0.1)
        self.assertLess(result.confidence_interval[0], result.difference)
        self.assertGreater(result.confidence_interval[1], result.difference)

    def test_independent_proportion_single_class_samples(self):
        result = compare_independent_proportions(10, 10, 10, 10)
        self.assertEqual(result.difference, 0.0)
        self.assertEqual(result.p_value, 1.0)

    def test_independent_proportion_all_failure_boundary(self):
        result = compare_independent_proportions(0, 10, 0, 10)
        self.assertEqual(result.difference, 0.0)
        self.assertEqual(result.p_value, 1.0)

    def test_independent_proportion_very_small_samples(self):
        result = compare_independent_proportions(1, 1, 0, 1)
        self.assertAlmostEqual(result.difference, 1.0)
        self.assertTrue(result.confidence_interval[0] <= result.confidence_interval[1])

    def test_independent_proportion_extreme_opposite_groups(self):
        result = compare_independent_proportions(10, 10, 0, 10)
        self.assertAlmostEqual(result.difference, 1.0)
        self.assertLess(result.confidence_interval[0], result.confidence_interval[1])

class PlanningTests(unittest.TestCase):
    def test_required_sample_size_and_mde_are_consistent(self):
        n = required_sample_size(0.8, 0.05, power=0.8, alpha=0.05)
        mde = minimum_detectable_effect(0.8, n, power=0.8, alpha=0.05)
        self.assertLessEqual(mde, 0.051)

    def test_design_effect_increases_required_sample_size(self):
        without_clusters = required_sample_size(0.8, 0.05, design_effect=1.0)
        with_clusters = required_sample_size(0.8, 0.05, design_effect=2.0)
        self.assertGreater(with_clusters, without_clusters)

    def test_minimum_detectable_effect_raises_when_target_power_is_unattainable(self):
        with self.assertRaises(ValueError):
            minimum_detectable_effect(0.99, 2, power=0.999, alpha=0.05)

    def test_required_sample_size_validates_inputs(self):
        with self.assertRaises(ValueError):
            required_sample_size(1.0, 0.05)
        with self.assertRaises(ValueError):
            required_sample_size(0.8, 0.05, design_effect=0.0)

    def test_planning_helpers_support_decrease_direction(self):
        n = required_sample_size(0.8, 0.05, direction="decrease")
        mde = minimum_detectable_effect(0.8, n, direction="decrease")
        self.assertGreater(n, 0)
        self.assertLessEqual(mde, 0.051)

    def test_minimum_detectable_effect_accepts_high_baseline_two_sided_case(self):
        effect = minimum_detectable_effect(0.95, 600, power=0.8, alpha=0.05, two_sided=True)
        self.assertGreater(effect, 0.0)


class ComparabilityTests(unittest.TestCase):
    def test_directly_comparable(self):
        result = metric_comparability_check(
            same_examples=True,
            same_ground_truth=True,
            same_scoring_code=True,
            same_metric_definitions=True,
            same_thresholds=True,
            same_preprocessing=True,
            same_operating_conditions=True,
        )
        self.assertEqual(result.classification, "Directly comparable")

    def test_comparable_with_limitations(self):
        result = metric_comparability_check(
            same_examples=True,
            same_ground_truth=True,
            same_scoring_code=True,
            same_metric_definitions=True,
            same_thresholds=False,
            same_preprocessing=True,
            same_operating_conditions=True,
        )
        self.assertEqual(result.classification, "Comparable with limitations")

    def test_not_directly_comparable(self):
        result = metric_comparability_check(
            same_examples=False,
            same_ground_truth=True,
            same_scoring_code=True,
            same_metric_definitions=True,
            same_thresholds=True,
            same_preprocessing=True,
            same_operating_conditions=True,
        )
        self.assertEqual(result.classification, "Not directly comparable")


if __name__ == "__main__":
    unittest.main()
