import unittest

from project_frog_eval.synthetic_data import calibration_bins, generate_project_frog_examples, slice_summary


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


if __name__ == "__main__":
    unittest.main()
