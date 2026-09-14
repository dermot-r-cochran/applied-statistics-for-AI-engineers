import unittest

from project_frog_eval.synthetic_data import (
    calibration_bins,
    generate_project_frog_examples,
    metric_interval_report,
    slice_summary,
    wilson_interval,
)


class SyntheticDataTests(unittest.TestCase):
    def test_generation_rejects_non_positive_sizes(self) -> None:
        with self.assertRaises(ValueError):
            generate_project_frog_examples(size=0)

    def test_generation_is_deterministic_for_seed(self) -> None:
        examples = generate_project_frog_examples(size=6, seed=11)

        self.assertEqual([example.example_id for example in examples], ["frog-001", "frog-002", "frog-003", "frog-004", "frog-005", "frog-006"])
        self.assertEqual([example.habitat for example in examples[:3]], ["wetland", "forest-edge", "urban-channel"])
        self.assertAlmostEqual(examples[0].score, 0.769, places=3)

    def test_calibration_bins_cover_all_examples(self) -> None:
        examples = generate_project_frog_examples(size=45, seed=5)
        bins = calibration_bins(examples, bins=5)

        self.assertEqual(sum(bucket.count for bucket in bins), len(examples))
        self.assertTrue(all(0 <= bucket.observed_rate <= 1 for bucket in bins))
        self.assertTrue(all(bucket.lower < bucket.upper for bucket in bins))

    def test_calibration_bins_handle_empty_and_invalid_input(self) -> None:
        self.assertEqual(calibration_bins([], bins=5), [])

        with self.assertRaises(ValueError):
            calibration_bins(generate_project_frog_examples(size=5, seed=2), bins=0)

    def test_calibration_bins_keep_high_resolution_boundaries(self) -> None:
        examples = generate_project_frog_examples(size=60, seed=9)
        bins = calibration_bins(examples, bins=200)

        self.assertTrue(all(bucket.lower < bucket.upper for bucket in bins))
        self.assertTrue(any((bucket.upper - bucket.lower) < 0.01 for bucket in bins))

    def test_slice_summary_groups_by_habitat(self) -> None:
        examples = generate_project_frog_examples(size=9, seed=3)
        summary = slice_summary(examples)

        self.assertEqual(set(summary.keys()), {"wetland", "forest-edge", "urban-channel"})
        self.assertEqual(sum(int(values["count"]) for values in summary.values()), len(examples))
        self.assertTrue(all(0 <= values["positive_rate"] <= 1 for values in summary.values()))

    def test_slice_summary_returns_empty_dict_for_no_examples(self) -> None:
        self.assertEqual(slice_summary([]), {})

    def test_wilson_interval_widens_when_sample_is_smaller(self) -> None:
        smaller = wilson_interval(successes=89, total=100)
        larger = wilson_interval(successes=890, total=1000)

        smaller_width = smaller.upper - smaller.lower
        larger_width = larger.upper - larger.lower

        self.assertEqual(smaller.point_estimate, larger.point_estimate)
        self.assertAlmostEqual(smaller.lower, 0.8136870349691969)
        self.assertAlmostEqual(smaller.upper, 0.9374580364293543)
        self.assertAlmostEqual(larger.lower, 0.8690945010531241)
        self.assertAlmostEqual(larger.upper, 0.9079206273281428)
        self.assertGreater(smaller_width, larger_width)

    def test_wilson_interval_can_widen_for_clustered_rows(self) -> None:
        row_count_interval = wilson_interval(successes=89, total=100)
        clustered_interval = wilson_interval(successes=89, total=100, effective_sample_size=40)

        row_count_width = row_count_interval.upper - row_count_interval.lower
        clustered_width = clustered_interval.upper - clustered_interval.lower

        self.assertEqual(clustered_interval.sample_size, 100)
        self.assertEqual(clustered_interval.effective_sample_size, 40)
        self.assertEqual(clustered_interval.method, "Wilson")
        self.assertAlmostEqual(clustered_interval.lower, 0.7571062032210649)
        self.assertAlmostEqual(clustered_interval.upper, 0.9545489478450515)
        self.assertGreater(clustered_width, row_count_width)

    def test_interval_report_carries_assumptions(self) -> None:
        report = metric_interval_report(
            metric_name=" accuracy ",
            successes=89,
            total=100,
            assumptions=("Synthetic amphibian sightings are treated as independent rows.",),
        )

        self.assertEqual(report.metric_name, "accuracy")
        self.assertEqual(report.total, 100)
        self.assertEqual(report.interval.method, "Wilson")
        self.assertEqual(
            report.assumptions,
            ("Synthetic amphibian sightings are treated as independent rows.",),
        )

    def test_interval_report_defaults_and_preserves_empty_assumptions(self) -> None:
        defaulted = metric_interval_report(metric_name="accuracy", successes=89, total=100)
        explicit_empty = metric_interval_report(
            metric_name="accuracy",
            successes=89,
            total=100,
            assumptions=(),
        )

        self.assertEqual(
            defaulted.assumptions,
            (
                "Rows are treated as exchangeable observations from the target evaluation set.",
                "If rows are clustered or dependent, the effective sample size should be reduced.",
            ),
        )
        self.assertEqual(explicit_empty.assumptions, ())

    def test_interval_helpers_reject_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            wilson_interval(successes=9, total=0)

        with self.assertRaises(ValueError):
            wilson_interval(successes=12, total=10)

        with self.assertRaises(ValueError):
            wilson_interval(successes=9, total=10, effective_sample_size=12)

        with self.assertRaises(ValueError):
            wilson_interval(successes=9, total=10, effective_sample_size=0.5)

        with self.assertRaises(ValueError):
            wilson_interval(successes=9, total=10, confidence_level=0)

        with self.assertRaises(ValueError):
            wilson_interval(successes=9, total=10, confidence_level=1)

        with self.assertRaises(ValueError):
            wilson_interval(successes=9, total=10, confidence_level=-0.1)

        with self.assertRaises(ValueError):
            metric_interval_report(metric_name=" ", successes=9, total=10)


if __name__ == "__main__":
    unittest.main()
