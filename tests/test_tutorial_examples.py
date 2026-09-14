import unittest

from tutorial_examples import (
    FrogCase,
    class_error_table,
    difficulty_summary,
    generate_project_frog_cases,
    overall_accuracy,
    release_recommendation,
    wilson_interval,
)


class TutorialExampleTests(unittest.TestCase):
    def test_generation_is_reproducible(self) -> None:
        self.assertEqual(
            generate_project_frog_cases(seed=7, n=10),
            generate_project_frog_cases(seed=7, n=10),
        )

    def test_generation_rejects_negative_size(self) -> None:
        with self.assertRaises(ValueError):
            generate_project_frog_cases(n=-1)

    def test_summary_handles_empty_input(self) -> None:
        summary = difficulty_summary([])
        self.assertEqual(summary["Simple"]["cases"], 0.0)
        self.assertEqual(summary["Complex"]["accuracy"], 0.0)

    def test_overall_accuracy_rejects_empty_input(self) -> None:
        with self.assertRaises(ValueError):
            overall_accuracy([])

    def test_wilson_interval_supports_all_correct(self) -> None:
        low, high = wilson_interval(5, 5)
        self.assertGreaterEqual(low, 0.5)
        self.assertEqual(high, 1.0)

    def test_wilson_interval_supports_all_incorrect(self) -> None:
        low, high = wilson_interval(0, 5)
        self.assertEqual(low, 0.0)
        self.assertLessEqual(high, 0.5)

    def test_wilson_interval_rejects_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            wilson_interval(6, 5)
        with self.assertRaises(ValueError):
            wilson_interval(0, 0)

    def test_error_table_reports_missing_classes(self) -> None:
        rows = [FrogCase("frog-1", "Simple", "Clear", "Review")]
        table = class_error_table(rows)
        self.assertEqual(table["Clear"], 1)
        self.assertEqual(table["Escalate"], 0)

    def test_release_recommendation_categories(self) -> None:
        self.assertEqual(
            release_recommendation(0.93, (0.91, 0.95), target=0.90),
            "Evidence supports release",
        )
        self.assertEqual(
            release_recommendation(0.90, (0.84, 0.93), target=0.90),
            "Evidence supports release with caveats",
        )
        self.assertEqual(
            release_recommendation(0.87, (0.82, 0.91), target=0.90),
            "Evidence is insufficient",
        )
        self.assertEqual(
            release_recommendation(0.87, (0.82, 0.89), target=0.90),
            "Evidence is insufficient",
        )
        self.assertEqual(
            release_recommendation(0.85, (0.80, 0.88), target=0.90),
            "Evidence is insufficient",
        )
        self.assertEqual(
            release_recommendation(0.80, (0.72, 0.86), target=0.90),
            "Evidence indicates release risk",
        )


if __name__ == "__main__":
    unittest.main()
