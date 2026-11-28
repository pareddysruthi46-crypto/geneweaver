import unittest

from alignment.baseline import match_guide_to_target


class TestScoringBoundaries(unittest.TestCase):

    def test_exact_threshold_boundary_is_accepted(self):
        result = match_guide_to_target(
            "ATGC",
            "ATGA",
            match_score=2,
            mismatch_score=-1,
            minimum_score=5,
        )
        self.assertEqual(result.alignment_score, 5.0)
        self.assertEqual(result.minimum_score, 5.0)

    def test_score_just_below_threshold_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "below the minimum"):
            match_guide_to_target(
                "ATGC",
                "ATGA",
                match_score=2,
                mismatch_score=-1,
                minimum_score=5.01,
            )

    def test_score_above_threshold_is_accepted(self):
        result = match_guide_to_target(
            "ATGC",
            "ATGA",
            match_score=2,
            mismatch_score=-1,
            minimum_score=4.99,
        )
        self.assertEqual(result.alignment_score, 5.0)

    def test_zero_match_score(self):
        result = match_guide_to_target(
            "ATGC",
            "ATGC",
            match_score=0,
            mismatch_score=-1,
        )
        self.assertEqual(result.alignment_score, 0.0)

    def test_negative_mismatch_score(self):
        result = match_guide_to_target(
            "ATGC",
            "ATGA",
            match_score=2,
            mismatch_score=-3,
        )
        self.assertEqual(result.alignment_score, 3.0)

    def test_negative_match_score_is_supported(self):
        result = match_guide_to_target(
            "ATGC",
            "ATGA",
            match_score=-1,
            mismatch_score=-2,
        )
        self.assertEqual(result.alignment_score, -5.0)

    def test_negative_infinity_match_score_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "match_score"):
            match_guide_to_target(
                "ATGC", "ATGC", match_score=float("-inf")
            )

    def test_negative_infinity_mismatch_score_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "mismatch_score"):
            match_guide_to_target(
                "ATGC", "ATGC", mismatch_score=float("-inf")
            )

    def test_positive_infinity_minimum_score_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "minimum_score"):
            match_guide_to_target(
                "ATGC", "ATGC", minimum_score=float("inf")
            )

    def test_boolean_match_score_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "match_score"):
            match_guide_to_target(
                "ATGC", "ATGC", match_score=True
            )

    def test_string_mismatch_score_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "mismatch_score"):
            match_guide_to_target(
                "ATGC", "ATGC", mismatch_score="-1"
            )

    def test_boolean_minimum_score_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "minimum_score"):
            match_guide_to_target(
                "ATGC", "ATGC", minimum_score=True
            )


if __name__ == "__main__":
    unittest.main()
