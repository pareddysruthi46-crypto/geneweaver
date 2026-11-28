import json
import unittest

from alignment.baseline import match_guide_to_target
from backend.schemas import AnalysisResponse
from backend.serialization import response_to_dict, response_to_json


class TestConfigurableAlignmentScoring(unittest.TestCase):

    def test_default_scoring_preserves_existing_behavior(self):
        result = match_guide_to_target("ATGC", "TTATGCAA")

        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.alignment_score, 4.0)
        self.assertEqual(result.match_score, 1.0)
        self.assertEqual(result.mismatch_score, 0.0)

    def test_custom_match_and_mismatch_scores(self):
        result = match_guide_to_target(
            "ATGC",
            "TTATACAA",
            match_score=2,
            mismatch_score=-1,
        )

        self.assertEqual(result.matches, 3)
        self.assertEqual(result.mismatches, 1)
        self.assertEqual(result.alignment_score, 5.0)

    def test_custom_scoring_selects_highest_weighted_window(self):
        result = match_guide_to_target(
            "AAAA",
            "TTTAAAA",
            match_score=2,
            mismatch_score=-3,
        )

        self.assertEqual(result.aligned_target, "AAAA")
        self.assertEqual(result.alignment_score, 8.0)

    def test_minimum_score_accepts_sufficient_alignment(self):
        result = match_guide_to_target(
            "ATGC",
            "TTATGCAA",
            match_score=2,
            mismatch_score=-1,
            minimum_score=7,
        )

        self.assertEqual(result.alignment_score, 8.0)
        self.assertEqual(result.minimum_score, 7.0)

    def test_minimum_score_rejects_weak_alignment(self):
        with self.assertRaisesRegex(ValueError, "below the minimum"):
            match_guide_to_target(
                "AAAA",
                "TTTT",
                match_score=1,
                mismatch_score=-1,
                minimum_score=0,
            )

    def test_invalid_scoring_values_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "match_score"):
            match_guide_to_target("ATGC", "ATGC", match_score=float("nan"))

        with self.assertRaisesRegex(ValueError, "mismatch_score"):
            match_guide_to_target(
                "ATGC", "ATGC", mismatch_score=float("inf")
            )

        with self.assertRaisesRegex(ValueError, "minimum_score"):
            match_guide_to_target(
                "ATGC", "ATGC", minimum_score=float("nan")
            )

    def test_scoring_values_are_included_in_json_response(self):
        result = match_guide_to_target(
            "ATGC",
            "TTATACAA",
            match_score=2,
            mismatch_score=-1,
        )
        response = AnalysisResponse(
            success=True,
            message="Alignment completed.",
            result=result,
            request_id="scoring-test",
        )

        data = response_to_dict(response)
        json_data = json.loads(response_to_json(response))

        self.assertEqual(data["result"]["alignment_score"], 5.0)
        self.assertEqual(data["result"]["match_score"], 2.0)
        self.assertEqual(data["result"]["mismatch_score"], -1.0)
        self.assertEqual(json_data["result"]["alignment_score"], 5.0)


if __name__ == "__main__":
    unittest.main()

