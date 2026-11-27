import unittest

from alignment.baseline import match_guide_to_target


class TestBaselineMatching(unittest.TestCase):

    def test_exact_match(self):
        result = match_guide_to_target("ATGC", "TTATGCAA")

        self.assertEqual(result.aligned_guide, "ATGC")
        self.assertEqual(result.aligned_target, "ATGC")
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.start_position, 2)
        self.assertEqual(result.mismatches, 0)

    def test_best_partial_match(self):
        result = match_guide_to_target("ATGC", "AAAAATGT")

        self.assertEqual(result.aligned_target, "ATGT")
        self.assertEqual(result.score, 75.0)
        self.assertEqual(result.start_position, 4)
        self.assertEqual(result.mismatches, 1)

    def test_no_matching_bases(self):
        result = match_guide_to_target("AAAA", "TTTT")

        self.assertEqual(result.aligned_guide, "AAAA")
        self.assertEqual(result.aligned_target, "TTTT")
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.start_position, 0)
        self.assertEqual(result.mismatches, 4)

    def test_short_sequence_exact_match(self):
        result = match_guide_to_target("A", "TAC")

        self.assertEqual(result.aligned_guide, "A")
        self.assertEqual(result.aligned_target, "A")
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.start_position, 1)
        self.assertEqual(result.mismatches, 0)

    def test_short_sequence_mismatch(self):
        result = match_guide_to_target("A", "T")

        self.assertEqual(result.aligned_guide, "A")
        self.assertEqual(result.aligned_target, "T")
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.start_position, 0)
        self.assertEqual(result.mismatches, 1)

    def test_lowercase_sequences_are_normalized(self):
        result = match_guide_to_target("atgc", "ttatgcaa")

        self.assertEqual(result.guide_sequence, "ATGC")
        self.assertEqual(result.score, 100.0)

    def test_first_best_match_is_selected(self):
        result = match_guide_to_target("ATGC", "ATGTATGA")

        self.assertEqual(result.start_position, 0)

    def test_guide_longer_than_target(self):
        with self.assertRaisesRegex(ValueError, "longer than target"):
            match_guide_to_target("ATGCG", "ATGC")

    def test_invalid_base_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid DNA symbol"):
            match_guide_to_target("ATGX", "ATGC")

    def test_empty_guide_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            match_guide_to_target("", "ATGC")


if __name__ == "__main__":
    unittest.main()
