import unittest

from gpu.parallel_windows import compare_sequence_windows


class TestParallelSequenceWindows(unittest.TestCase):

    def test_exact_match(self):
        result = compare_sequence_windows("ATGC", "TTATGCAA")
        self.assertEqual(result["start_position"], 2)
        self.assertEqual(result["end_position"], 5)
        self.assertEqual(result["matches"], 4)
        self.assertEqual(result["mismatches"], 0)
        self.assertEqual(result["score"], 100.0)

    def test_best_partial_match(self):
        result = compare_sequence_windows("ATGC", "AAAAATGT")
        self.assertEqual(result["start_position"], 4)
        self.assertEqual(result["matches"], 3)
        self.assertEqual(result["mismatches"], 1)
        self.assertEqual(result["score"], 75.0)

    def test_no_matching_bases(self):
        result = compare_sequence_windows("AAAA", "TTTT")
        self.assertEqual(result["matches"], 0)
        self.assertEqual(result["mismatches"], 4)
        self.assertEqual(result["score"], 0.0)

    def test_lowercase_is_normalized(self):
        result = compare_sequence_windows("atgc", "ttatgcaa")
        self.assertEqual(result["guide_sequence"], "ATGC")
        self.assertEqual(result["score"], 100.0)

    def test_cpu_fallback_or_opencl_execution_is_reported(self):
        result = compare_sequence_windows("ATGC", "TTATGCAA")
        self.assertTrue(
            result["execution_device"].startswith("CPU")
            or result["execution_device"].startswith("OpenCL GPU:")
        )

    def test_guide_longer_than_target(self):
        with self.assertRaisesRegex(ValueError, "longer than target"):
            compare_sequence_windows("ATGCG", "ATGC")

    def test_invalid_base(self):
        with self.assertRaisesRegex(ValueError, "Invalid DNA symbol"):
            compare_sequence_windows("ATGX", "ATGC")


if __name__ == "__main__":
    unittest.main()
